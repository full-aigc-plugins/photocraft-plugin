#!/usr/bin/env python3
"""把已停止原执行的固定现场记录为独立检查点；不补造 failure、不写原工程、不重放。"""
import argparse
import errno
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
sys.dont_write_bytecode = True


def load(name):
    spec = importlib.util.spec_from_file_location('interrupted_' + name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def inventory(stage):
    """登记整个原暂存；链接、特殊文件和后续新增文件均不能被隐藏。"""
    delivery = load('delivery'); files = {}
    for path in sorted(stage.rglob('*')):
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)):
            raise ValueError('interrupted_stage_unsafe')
        if stat.S_ISREG(info.st_mode):
            if info.st_nlink != 1: raise ValueError('interrupted_stage_unsafe')
            files[path.relative_to(stage).as_posix()] = {'sha256': delivery.sha(path), 'bytes': info.st_size}
    if 'project.pcraft' not in files: raise ValueError('interrupted_project_missing')
    if 'failure.json' in files:
        raise ValueError('interrupted_existing_delivery_record')
    return files


def stopped(observed, receipt_path, launch_path):
    """原任务监督回执、启动摘要和实际消失的两个进程组必须同时一致。"""
    delivery = load('delivery'); receipt_path, launch_path = Path(receipt_path), Path(launch_path)
    for path in (receipt_path, launch_path):
        if any(part.is_symlink() for part in (path, *path.parents)) or not path.is_file():
            raise ValueError('interrupted_worker_record_unsafe')
    receipt_sha, launch_sha = delivery.sha(receipt_path), delivery.sha(launch_path)
    receipt, launch = delivery.read_json(receipt_path), delivery.read_json(launch_path)
    binding = observed['record']['context']['taskBinding']
    if (not isinstance(binding, dict) or not isinstance(receipt, dict) or not isinstance(launch, dict)
            or receipt.get('schema') != 'photocraft-worker-exit/v1' or launch.get('schema') != 'photocraft-worker-launch/v1'
            or any(receipt.get(key) != value or launch.get(key) != value for key, value in binding.items())
            or receipt.get('launchSha256') != launch_sha or receipt.get('processGroupGone') is not True
            or receipt.get('workflowPid') != observed['record']['ownerPid'] or receipt.get('stoppedAt') is not None
            or type(receipt.get('finishedAt')) is not int or receipt['finishedAt'] < observed['record']['updatedAt']):
        raise ValueError('interrupted_worker_identity_mismatch')
    if os.name == 'nt': raise ValueError('interrupted_worker_group_unavailable')
    for pid in (receipt.get('supervisorPid'), receipt.get('workflowPid')):
        if type(pid) is not int or not 0 < pid < 2**31: raise ValueError('interrupted_worker_identity_mismatch')
        try: os.kill(-pid, 0)
        except OSError as error:
            if error.errno != errno.ESRCH: raise ValueError('interrupted_worker_state_unknown') from error
        else: raise ValueError('interrupted_worker_still_active')
    if delivery.sha(receipt_path) != receipt_sha or delivery.sha(launch_path) != launch_sha:
        raise ValueError('interrupted_worker_snapshot_changed')
    return receipt_sha, launch_sha


def read(checkpoint, write_root):
    """重新核对记录、原进度、退出证明及所有原文件；读取不产生副作用。"""
    progress = load('progress'); delivery = load('delivery')
    checkpoint = progress.safe(checkpoint, write_root); path = checkpoint / 'checkpoint.json'
    progress.safe(path, write_root)
    if not path.is_file() or path.stat().st_nlink != 1 or path.stat().st_size > progress.MAX_BYTES: raise ValueError('interrupted_record_invalid')
    record_sha = delivery.sha(path); record = delivery.read_json(path)
    keys = {'schema', 'status', 'outcome', 'stage', 'stageIdentity', 'progressOutput', 'progressSha256', 'receiptPath', 'receiptSha256', 'launchPath', 'launchSha256', 'context', 'operations', 'files', 'completedOperations', 'lastAttempt', 'replayAllowed'}
    if (not isinstance(record, dict) or set(record) != keys or record['schema'] != 'photocraft-interrupted-checkpoint/v1'
            or record['status'] != 'interrupted' or record['outcome'] != 'outcome_unknown' or record['replayAllowed'] is not False
            or not isinstance(record['stage'], str) or Path(record['stage']).is_absolute()):
        raise ValueError('interrupted_record_invalid')
    observed = progress.read_progress(record['progressOutput'], write_root)
    if observed['recordSha256'] != record['progressSha256'] or not observed['stageAvailable']:
        raise ValueError('interrupted_progress_changed')
    original = observed['record']; stage = progress.safe(checkpoint / record['stage'], write_root)
    if str(stage) != observed['stage'] or any(record[key] != original[key] for key in ('context', 'operations', 'stageIdentity', 'completedOperations', 'lastAttempt')):
        raise ValueError('interrupted_origin_conflict')
    receipt_sha, launch_sha = stopped(observed, record['receiptPath'], record['launchPath'])
    if receipt_sha != record['receiptSha256'] or launch_sha != record['launchSha256']:
        raise ValueError('interrupted_worker_snapshot_changed')
    if inventory(stage) != record['files']: raise ValueError('interrupted_stage_changed')
    if delivery.sha(path) != record_sha or progress.read_progress(record['progressOutput'], write_root)['recordSha256'] != record['progressSha256']:
        raise ValueError('interrupted_snapshot_changed')
    return {'record': record, 'recordSha256': record_sha, 'stage': stage, 'context': record['context'], 'operations': record['operations']}


def capture(output, write_root, checkpoint, expected_progress_sha, receipt_path, launch_path):
    """已授权 reconcile 记录独立旁车；已存在记录只能重新验证，绝不覆盖。"""
    progress = load('progress'); observed = progress.read_progress(output, write_root)
    checkpoint = progress.safe(checkpoint, write_root)
    if observed['recordSha256'] != expected_progress_sha or not observed['stageAvailable']:
        raise ValueError('interrupted_progress_changed')
    receipt_sha, launch_sha = stopped(observed, receipt_path, launch_path)
    stage = Path(observed['stage']); original = observed['record']; files = inventory(stage)
    if checkpoint.exists():
        existing = read(checkpoint, write_root)
        if existing['record']['progressOutput'] != str(progress.safe(output, write_root)) or existing['record']['progressSha256'] != expected_progress_sha:
            raise ValueError('interrupted_checkpoint_conflict')
        return existing
    record = {'schema': 'photocraft-interrupted-checkpoint/v1', 'status': 'interrupted', 'outcome': 'outcome_unknown',
              'stage': os.path.relpath(stage, checkpoint), 'stageIdentity': original['stageIdentity'],
              'progressOutput': str(progress.safe(output, write_root)), 'progressSha256': expected_progress_sha,
              'receiptPath': str(Path(receipt_path).absolute()), 'receiptSha256': receipt_sha,
              'launchPath': str(Path(launch_path).absolute()), 'launchSha256': launch_sha,
              'context': original['context'], 'operations': original['operations'], 'files': files,
              'completedOperations': original['completedOperations'], 'lastAttempt': original['lastAttempt'], 'replayAllowed': False}
    if progress.read_progress(output, write_root)['recordSha256'] != expected_progress_sha or inventory(stage) != files:
        raise ValueError('interrupted_snapshot_changed')
    data = json.dumps(record, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode()
    if len(data) > progress.MAX_BYTES: raise ValueError('interrupted_record_too_large')
    checkpoint.mkdir(mode=0o700)
    # 独占文件即使在写入中断也保全为不可接受状态；不重建、不覆盖损坏记录。
    with (checkpoint / 'checkpoint.json').open('xb') as stream:
        os.chmod(stream.fileno(), 0o600); stream.write(data); stream.flush(); os.fsync(stream.fileno())
    directory = os.open(checkpoint, os.O_RDONLY)
    try: os.fsync(directory)
    finally: os.close(directory)
    return read(checkpoint, write_root)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('output'); parser.add_argument('--write-root', required=True)
    parser.add_argument('--checkpoint-output', required=True); parser.add_argument('--progress-sha256', required=True)
    parser.add_argument('--worker-receipt', required=True); parser.add_argument('--worker-launch', required=True)
    args = parser.parse_args()
    try:
        result = capture(args.output, args.write_root, args.checkpoint_output, args.progress_sha256, args.worker_receipt, args.worker_launch)
        print(json.dumps({'schema': 'photocraft-interrupted-capture/v1', 'result': 'PASS', 'recordSha256': result['recordSha256'], 'replayAllowed': False}, ensure_ascii=False))
    except (ValueError, OSError, RuntimeError, KeyError, TypeError) as error:
        print(json.dumps({'result': 'FAIL', **load('operation_errors').describe(error, 'verification'), 'phase': 'verification', 'replayAllowed': False}, ensure_ascii=False)); raise SystemExit(1)
