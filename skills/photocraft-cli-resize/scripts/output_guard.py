"""原生会话前认领输出；进程消失不代表原生副作用已停止。"""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import stat


def _write(stream, value):
    """在持有文件锁时持久化身份，保留同一 inode。"""
    data = (json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)+'\n').encode()
    stream.seek(0); stream.write(data); stream.truncate(); stream.flush()
    os.fsync(stream.fileno())


@contextmanager
def claim(output, identity):
    """认领不存在的目标；失败或中断必须先核对原结果，不能自动重放。"""
    output = Path(output).absolute()
    output = output.parent.resolve()/output.name
    if output.exists() or output.is_symlink():
        raise ValueError('output_exists')
    output.parent.mkdir(parents=True, exist_ok=True)
    target_hash = hashlib.sha256(str(output).encode()).hexdigest()
    path = output.parent/('.photocraft-execution-'+target_hash+'.json')
    try:
        fd = os.open(path, os.O_CREAT|os.O_EXCL|os.O_RDWR|os.O_NOFOLLOW, 0o600)
        created = True
    except FileExistsError:
        fd = os.open(path, os.O_RDWR|os.O_NOFOLLOW)
        created = False
    with os.fdopen(fd, 'r+b') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > 1024*1024:
            raise ValueError('output_execution_record_invalid')
        try:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('output_execution_conflict') from None
        if not created:
            try:
                previous = json.loads(stream.read())
            except (ValueError, UnicodeDecodeError):
                raise ValueError('output_execution_record_invalid') from None
            if (not isinstance(previous, dict) or previous.get('schema')!='photocraft-output-execution/v1'
                    or previous.get('targetHash')!=target_hash):
                raise ValueError('output_execution_record_invalid')
            if previous.get('state') in ('running', 'reconciling'):
                raise ValueError('output_execution_reconciling')
            if previous.get('state')!='finished':
                raise ValueError('output_execution_record_invalid')
        if output.exists() or output.is_symlink():
            raise ValueError('output_exists')
        record = {'schema':'photocraft-output-execution/v1', 'targetHash':target_hash,
                  'identity':identity, 'ownerPid':os.getpid(), 'state':'running', 'replayAllowed':False}
        _write(stream, record)
        try:
            yield record
        except BaseException:
            record['state']='reconciling'
            try:
                _write(stream, record)
            except OSError:
                pass  # 原 running 身份仍阻止重放，不遮蔽原异常。
            raise
        else:
            record['state']='finished'
            _write(stream, record)
