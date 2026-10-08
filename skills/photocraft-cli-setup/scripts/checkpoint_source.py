"""已核对失败工程的显式修订来源；保留原暂存，不生成虚假的成功清单。"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re


def load(name):
    spec = importlib.util.spec_from_file_location('checkpoint_source_' + name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def safe(path, root):
    path = Path(os.path.abspath(path))
    root = Path(root).absolute()
    if path == root or not path.is_relative_to(root):
        raise ValueError('checkpoint_outside_authorization')
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError('checkpoint_symlink')
    return path


def snapshot(output, write_root, plan, runtime_sha256=None):
    """只读核对完整原记录、依赖及已验证绑定；缺少来源信息的旧记录不能获得修订权。"""
    delivery = load('delivery')
    output = safe(output, write_root)
    interrupted = (output / 'checkpoint.json').exists()
    captured = load('interrupted_checkpoint').read(output, write_root) if interrupted else None
    record_file = delivery.file_path(output, 'checkpoint.json' if interrupted else 'failure.json')
    record_sha = delivery.sha(record_file)
    for key in ('expectedCheckpointSha256', 'expectedCheckpointPlanSha256', 'expectedProjectSha256'):
        if not isinstance(plan.get(key), str) or not re.fullmatch(r'[a-f0-9]{64}', plan[key]):
            raise ValueError('checkpoint_binding_required: ' + key)
    if record_sha != plan['expectedCheckpointSha256']:
        raise ValueError('checkpoint_record_conflict')
    record = delivery.read_json(record_file)
    if not interrupted and (not isinstance(record, dict) or record.get('schema') != 'craft-failed-stage/v1'
            or record.get('status') != 'failed' or record.get('replayAllowed') is not False
            or record.get('outcome') not in ('failed', 'outcome_unknown')
            or not isinstance(record.get('stage'), str) or Path(record['stage']).is_absolute()
            or not isinstance(record.get('files'), dict)
            or type(record.get('completedOperations')) is not int or record['completedOperations'] < 0):
        raise ValueError('checkpoint_record_invalid')
    stage = safe(output / record['stage'], write_root)
    if not interrupted and delivery.read_json(delivery.file_path(stage, 'failure.json')) != record:
        raise ValueError('checkpoint_record_conflict')
    files = record['files']
    required = {'project.pcraft'} if interrupted else {'project.pcraft', 'recovery-context.json', 'recovery-operations.json'}
    if not required.issubset(files):
        raise ValueError('checkpoint_context_missing')
    for name, entry in files.items():
        path = delivery.file_path(stage, name)
        if (name == 'failure.json' or not isinstance(entry, dict) or set(entry) != {'sha256', 'bytes'}
                or not isinstance(entry['sha256'], str) or not re.fullmatch(r'[a-f0-9]{64}', entry['sha256'])
                or type(entry['bytes']) is not int or entry['bytes'] < 0
                or path.stat().st_size != entry['bytes'] or delivery.sha(path) != entry['sha256']):
            raise ValueError('checkpoint_file_changed')
    attempt = record.get('lastAttempt')
    if attempt is not None and (not isinstance(attempt, dict) or not isinstance(attempt.get('tool'), str) or not attempt['tool'] or not isinstance(attempt.get('arguments'), dict) or attempt.get('phase') not in ('submitted','reply_validated')):
        raise ValueError('checkpoint_attempt_invalid')
    operations = captured['operations'] if interrupted else delivery.read_json(stage / 'recovery-operations.json')
    if not isinstance(operations, list) or len(operations) != record['completedOperations']:
        raise ValueError('checkpoint_operations_invalid')
    context = captured['context'] if interrupted else delivery.read_json(stage / 'recovery-context.json')
    if (not isinstance(context, dict) or context.get('schema') != 'photocraft-recovery-context/v1'
            or set(context) != {'schema', 'plan', 'executionIdentity', 'bindings', 'assets', 'capability', 'taskBinding'}
            or not isinstance(context['plan'], dict) or not isinstance(context['executionIdentity'], dict)
            or not isinstance(context['bindings'], dict) or not isinstance(context['assets'], dict)):
        raise ValueError('checkpoint_context_invalid')
    task=context['taskBinding']
    if task is not None and (not isinstance(task,dict) or set(task)!={'taskId','taskIdentity','epoch','workerToken','sourceSha256'} or not isinstance(task.get('taskId'),str) or not task['taskId'] or not isinstance(task.get('workerToken'),str) or not task['workerToken'] or type(task.get('epoch')) is not int or task['epoch']<1 or any(not isinstance(task.get(key),str) or not re.fullmatch(r'[a-f0-9]{64}',task[key]) for key in ('taskIdentity','sourceSha256'))):
        raise ValueError('checkpoint_task_binding_invalid')
    identity = context['executionIdentity']
    if load('plan_identity').sha(context['plan'], identity.get('planHashAlgorithm')) != plan['expectedCheckpointPlanSha256'] or identity.get('planHash') != plan['expectedCheckpointPlanSha256']:
        raise ValueError('checkpoint_plan_conflict')
    if files['project.pcraft']['sha256'] != plan['expectedProjectSha256']:
        raise ValueError('checkpoint_project_conflict')
    if runtime_sha256 is not None and identity.get('runtimeSha256') != runtime_sha256:
        raise ValueError('checkpoint_runtime_conflict')
    if not isinstance(identity.get('runtimeSha256'), str) or not re.fullmatch(r'[a-f0-9]{64}',identity['runtimeSha256']):
        raise ValueError('checkpoint_runtime_conflict')
    capability=context['capability']
    if capability is not None and (not isinstance(capability, dict) or capability.get('schema')!='photocraft-capabilities/v1' or capability.get('binarySha256')!=identity['runtimeSha256']):
        raise ValueError('checkpoint_capability_conflict')
    if not isinstance(identity.get('inputHashes'), dict):
        raise ValueError('checkpoint_inputs_invalid')
    for name, asset in context['assets'].items():
        if (not re.fullmatch(r'[A-Za-z][\w-]*', name) or not isinstance(asset, dict)
                or set(asset) != {'path', 'sha256'} or not isinstance(asset['path'], str) or Path(asset['path']).name != asset['path']
                or files.get(asset['path'], {}).get('sha256') != asset['sha256']
                or identity['inputHashes'].get(name) != asset['sha256']):
            raise ValueError('checkpoint_asset_conflict')
    for name,asset in context['plan'].get('assets',{}).items():
        if not isinstance(asset,dict) or identity['inputHashes'].get(name)!=asset.get('sha256'):raise ValueError('checkpoint_original_input_conflict')
    if set(context['assets']) != set(identity['inputHashes']):
        raise ValueError('checkpoint_asset_conflict')
    if interrupted and load('interrupted_checkpoint').read(output, write_root)['recordSha256'] != record_sha:
        raise ValueError('checkpoint_changed')
    if delivery.sha(record_file) != record_sha or not interrupted and delivery.sha(stage / 'failure.json') != record_sha:
        raise ValueError('checkpoint_changed')
    return {'stage': stage, 'recordSha256': record_sha, 'projectSha256': files['project.pcraft']['sha256'], 'context': context, 'files': files}
