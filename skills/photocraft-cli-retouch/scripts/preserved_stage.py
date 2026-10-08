"""原生工作流失败暂存保留；绝不移动含绝对依赖的未知结果工程。"""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile


def _write_record(path, value):
    """只在本次拥有的目录内原子写入诊断。"""
    temporary = path.with_name(path.name + '.writing')
    with temporary.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    os.replace(temporary, path)


def claim_output(output, state):
    """创建并绑定本次输出目录身份；发生目录竞争时不覆盖。"""
    output.mkdir(mode=0o700)
    identity = output.stat()
    state['output'] = True
    state['outputIdentity'] = (identity.st_dev, identity.st_ino)


@contextmanager
def preserved_stage(output, prefix, state=None):
    """成功清理暂存；异常时保留原路径、摘要和回执，不改变原异常。"""
    output = Path(output).absolute()
    state = state if state is not None else {}
    stage = Path(tempfile.mkdtemp(prefix=prefix, dir=output.parent))
    try:
        yield str(stage)
    except BaseException as error:
        # 子会话先退出，文件位置不改变；不能将未知结果解释成未执行。
        try:
            operations = state.get('operations', [])
            _write_record(stage / 'recovery-operations.json', operations)
            files = {}
            for path in sorted(stage.rglob('*')):
                if path.is_file() and not path.is_symlink() and path.name != 'failure.json':
                    files[path.relative_to(stage).as_posix()] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}
            record = {'schema': 'craft-failed-stage/v1', 'status': 'failed',
                      'outcome': 'outcome_unknown' if (getattr(error, 'outcome', None) == 'unknown' or str(error).partition(':')[0] == 'outcome_unknown') else 'failed',
                      'error': str(error), 'code': getattr(error, 'code', 'execution_failed'),
                      'phase': getattr(error, 'phase', 'submitted'), 'retryable': False,
                      'recoveryAction': getattr(error, 'recoveryAction', 'reconcile'), 'stage': os.path.relpath(stage, output),
                      'files': files, 'completedOperations': len(operations), 'lastAttempt': state.get('lastAttempt'), 'replayAllowed': False,
                      'acceptance': 'not-a-successful-delivery', 'recovery': 'verify hashes and reopen original project in a new read-only session before any explicit revision'}
            _write_record(stage / 'failure.json', record)
            # 目录竞争时不写他人目录；暂存中的诊断仍可读取。
            if not output.exists() and not output.is_symlink():
                try:
                    claim_output(output, state)
                except FileExistsError:
                    pass
            if (state.get('outputIdentity') and output.is_dir() and not output.is_symlink()
                    and (output.stat().st_dev, output.stat().st_ino) == state['outputIdentity']):
                _write_record(output / 'failure.json', record)
        except (OSError, ValueError, TypeError):
            # 诊断写入失败也不删除工程或遮蔽原始异常。
            pass
        raise
    else:
        if stage.exists():
            shutil.rmtree(stage)
