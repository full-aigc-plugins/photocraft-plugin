#!/usr/bin/env python3
"""原执行的原子进度快照；只读查询不安装、不启动会话、不授予重放或修订权限。"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
sys.dont_write_bytecode = True
MAX_BYTES = 8 * 1024 * 1024
HEX = re.compile(r'[a-f0-9]{64}')
PHASES = {'prepared', 'submitted', 'reply_validated', 'publishing', 'finished'}


def load(name):
    spec = importlib.util.spec_from_file_location('progress_' + name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def target_hash(output):
    output = Path(output).absolute()
    return hashlib.sha256(str(output.parent.resolve() / output.name).encode()).hexdigest()


def record_path(output):
    output = Path(output).absolute()
    return output.parent / ('.photocraft-progress-' + target_hash(output) + '.json')


def guard_path(output):
    output = Path(output).absolute()
    return output.parent / ('.photocraft-execution-' + target_hash(output) + '.json')


def safe(path, root):
    path, root = Path(os.path.abspath(path)), Path(root).absolute()
    if path == root or not path.is_relative_to(root) or any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError('progress_outside_authorization')
    return path


class Journal:
    """在原输出认领范围内替换完整进度记录，不修改原执行意图或暂存工程。"""
    def __init__(self, output, stage, guard):
        self.output, self.stage = Path(output).absolute(), Path(stage).absolute()
        if (guard.get('ownerPid') != os.getpid() or guard.get('state') != 'running'
                or guard.get('targetHash') != target_hash(self.output)
                or load('delivery').read_json(guard_path(self.output)) != guard):
            raise ValueError('progress_owner_conflict')
        self.guard, self.sequence = guard, 0
        self.stage_identity = [str(self.stage.stat().st_dev), str(self.stage.stat().st_ino)]

    def publish(self, state, phase):
        """先刷盘完整记录再替换指针；发布失败不得继续下一次原生调用。"""
        if self.guard.get('ownerPid') != os.getpid() or self.guard.get('state') != 'running':
            raise ValueError('progress_owner_conflict')
        if phase not in PHASES:
            raise ValueError('progress_phase_invalid')
        self.sequence += 1
        operations = state.get('operations', [])
        value = {'schema': 'photocraft-progress/v1', 'targetHash': self.guard['targetHash'],
                 'ownerPid': os.getpid(), 'sequence': self.sequence, 'updatedAt': int(time.time() * 1000),
                 'stage': os.path.relpath(self.stage, self.output), 'stageIdentity': self.stage_identity,
                 'phase': phase, 'context': state['recoveryContext'], 'lastAttempt': state.get('lastAttempt'),
                 'operations': operations, 'completedOperations': len(operations), 'replayAllowed': False}
        data = (json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':')) + '\n').encode()
        if len(data) > MAX_BYTES:
            raise ValueError('progress_record_too_large')
        path = record_path(self.output)
        fd, temporary = tempfile.mkstemp(prefix='.photocraft-progress-writing-', dir=path.parent)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data); stream.flush(); os.fsync(stream.fileno())
            os.replace(temporary, path)
            directory = os.open(path.parent, os.O_RDONLY)
            try: os.fsync(directory)
            finally: os.close(directory)
        finally:
            if os.path.exists(temporary): os.unlink(temporary)


def read_progress(output, write_root):
    """只读核对原认领、计划与暂存身份；PASS 仅表示观察记录有效。"""
    output = safe(output, write_root); path = safe(record_path(output), write_root)
    guard_file = safe(guard_path(output), write_root); delivery = load('delivery')
    for file in (path, guard_file):
        if not file.is_file() or file.stat().st_size > MAX_BYTES: raise ValueError('progress_record_invalid')
    record_sha, guard_sha = delivery.sha(path), delivery.sha(guard_file)
    record, guard = delivery.read_json(path), delivery.read_json(guard_file)
    keys = {'schema', 'targetHash', 'ownerPid', 'sequence', 'updatedAt', 'stage', 'stageIdentity', 'phase', 'context', 'lastAttempt', 'operations', 'completedOperations', 'replayAllowed'}
    if (not isinstance(record, dict) or set(record) != keys or record['schema'] != 'photocraft-progress/v1'
            or record['targetHash'] != target_hash(output) or record['replayAllowed'] is not False
            or type(record['sequence']) is not int or not 0 < record['sequence'] < 2**53
            or type(record['updatedAt']) is not int or not 0 < record['updatedAt'] < 2**53
            or type(record['ownerPid']) is not int or not 0 < record['ownerPid'] < 2**53
            or not isinstance(record['phase'], str) or record['phase'] not in PHASES
            or not isinstance(record['stageIdentity'], list) or len(record['stageIdentity']) != 2
            or any(not isinstance(value, str) or not re.fullmatch(r'[0-9]+', value) for value in record['stageIdentity'])
            or not isinstance(record['stage'], str) or Path(record['stage']).is_absolute()
            or not isinstance(record['operations'], list) or type(record['completedOperations']) is not int
            or record['completedOperations'] != len(record['operations'])):
        raise ValueError('progress_record_invalid')
    context = record['context']
    if (not isinstance(context, dict) or set(context) != {'schema', 'plan', 'executionIdentity', 'bindings', 'assets', 'capability', 'taskBinding'}
            or context['schema'] != 'photocraft-recovery-context/v1' or not isinstance(context['plan'], dict)
            or not isinstance(context['bindings'], dict) or not isinstance(context['assets'], dict)
            or context['capability'] is not None and not isinstance(context['capability'], dict)):
        raise ValueError('progress_context_invalid')
    identity = context['executionIdentity']
    if (not isinstance(identity, dict) or set(identity) != {'planHash', 'inputHashes', 'projectRevision', 'runtimeSha256'}
            or identity['planHash'] != canonical_sha(context['plan']) or not isinstance(identity['inputHashes'], dict)
            or any(not isinstance(value, str) or not HEX.fullmatch(value) for value in identity['inputHashes'].values())
            or not isinstance(identity['runtimeSha256'], str) or not HEX.fullmatch(identity['runtimeSha256'])
            or identity['projectRevision'] is not None and (not isinstance(identity['projectRevision'], str) or not HEX.fullmatch(identity['projectRevision']))):
        raise ValueError('progress_identity_invalid')
    if context['taskBinding'] is not None: delivery.validate_task_binding(context['taskBinding'])
    if (not isinstance(guard, dict) or guard.get('schema') != 'photocraft-output-execution/v1'
            or guard.get('targetHash') != record['targetHash'] or guard.get('ownerPid') != record['ownerPid']
            or guard.get('identity') != identity or guard.get('state') not in ('running', 'reconciling', 'finished')
            or guard.get('replayAllowed') is not False):
        raise ValueError('progress_guard_conflict')
    attempt = record['lastAttempt']
    if attempt is not None and (not isinstance(attempt, dict) or set(attempt) != {'tool', 'arguments', 'phase'}
            or not isinstance(attempt['tool'], str) or not attempt['tool'] or not isinstance(attempt['arguments'], dict)
            or attempt['phase'] not in ('submitted', 'reply_validated')): raise ValueError('progress_attempt_invalid')
    for receipt in record['operations']:
        if (not isinstance(receipt, dict) or set(receipt) != {'tool', 'arguments', 'result'}
                or not isinstance(receipt['tool'], str) or not receipt['tool'] or not isinstance(receipt['arguments'], dict)):
            raise ValueError('progress_receipt_invalid')
    if record['phase'] in ('submitted', 'reply_validated') and (attempt is None or attempt['phase'] != record['phase']):
        raise ValueError('progress_attempt_invalid')
    if attempt is not None and attempt['phase'] == 'reply_validated':
        if not record['operations'] or any(record['operations'][-1][key] != attempt[key] for key in ('tool', 'arguments')):
            raise ValueError('progress_receipt_invalid')
    stage = safe(output / record['stage'], write_root)
    if stage.exists():
        if not stage.is_dir() or [str(stage.stat().st_dev), str(stage.stat().st_ino)] != record['stageIdentity']:
            raise ValueError('progress_stage_conflict')
    elif record['phase'] != 'finished': raise ValueError('progress_stage_missing')
    if delivery.sha(path) != record_sha or delivery.sha(guard_file) != guard_sha: raise ValueError('progress_snapshot_changed')
    return {'schema': 'photocraft-progress-inspection/v1', 'result': 'PASS', 'recordSha256': record_sha,
            'record': record, 'stage': str(stage), 'stageAvailable': stage.is_dir(), 'replayAllowed': False,
            'technical': 'NOT_RUN', 'creative': 'NOT_RUN', 'scope': 'Observed original execution progress only; no stopped-worker proof, native reopening, checkpoint revision or acceptance.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('output'); parser.add_argument('--write-root', required=True)
    args = parser.parse_args()
    try: print(json.dumps(read_progress(args.output, args.write_root), ensure_ascii=False))
    except (ValueError, OSError, RuntimeError, KeyError, TypeError) as error:
        print(json.dumps({'result': 'FAIL', 'error': str(error), 'replayAllowed': False}, ensure_ascii=False)); raise SystemExit(1)
