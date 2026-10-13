"""PSD 必要功能门禁及精确损失接受；不把接受损失升级为保真。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re

FEATURES = {'structure', 'text', 'mask', 'blend', 'opacity', 'smartObject',
            'smartSourceKind', 'smartTransform', 'adjustment', 'shape', 'effects', 'tree-size'}
STATUSES = {'retained', 'degraded', 'lost', 'unknown'}


def load(name):
    spec = importlib.util.spec_from_file_location('psd_policy_' + name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def selector(value, exact=False):
    if not isinstance(value, str):
        return False
    if value in ('effects', 'tree-size'):
        return True
    if not exact and (value == '*' or value in FEATURES):
        return True
    parts = value.split(':')
    return (len(parts) == 2 and parts[1] in FEATURES - {'effects', 'tree-size'}
            and re.fullmatch(r'(?:0|[1-9][0-9]*)(?:/(?:0|[1-9][0-9]*))*', parts[0]) is not None)


def validate(policy):
    """静态策略错误必须在安装、编辑及输出目录创建前拒绝。"""
    if not isinstance(policy, dict) or set(policy) - {'requiredFeatures', 'acceptedLosses', 'acceptedForSourceSha256'}:
        raise ValueError('invalid_psd_policy')
    required = policy.get('requiredFeatures', [])
    if (not isinstance(required, list) or any(not selector(item) for item in required)
            or len(required) != len(set(required))):
        raise ValueError('invalid_psd_policy: requiredFeatures')
    accepted = policy.get('acceptedLosses', {})
    if not isinstance(accepted, dict):
        raise ValueError('invalid_psd_policy: acceptedLosses')
    if accepted and (not isinstance(policy.get('acceptedForSourceSha256'), str)
                     or re.fullmatch('[a-f0-9]{64}', policy['acceptedForSourceSha256']) is None):
        raise ValueError('invalid_psd_policy: acceptedForSourceSha256')
    if not accepted and 'acceptedForSourceSha256' in policy:
        raise ValueError('invalid_psd_policy: unused acceptedForSourceSha256')
    for feature, receipt in accepted.items():
        if (not selector(feature, exact=True) or not isinstance(receipt, dict)
                or set(receipt) != {'status', 'observationSha256', 'reason'}
                or receipt['status'] not in ('lost', 'degraded', 'unknown')
                or not isinstance(receipt['observationSha256'], str)
                or re.fullmatch('[a-f0-9]{64}', receipt['observationSha256']) is None
                or not isinstance(receipt['reason'], str) or not receipt['reason'].strip()
                or len(receipt['reason']) > 2048):
            raise ValueError('invalid_psd_policy: acceptedLosses.' + str(feature))


def assess(report, policy, plan_sha256, source_sha256=None):
    """绑定实际候选摘要，逐项核对所需特性和此前明确接受的同一观察。"""
    validate(policy)
    outputs = [out for out in report.get('outputs', []) if out.get('format') == 'psd']
    if len(outputs) != 1:
        raise ValueError('psd_gate_requires_one_psd')
    output = outputs[0]
    matrix = output.get('observations', {}).get('featureMatrix', {}).get('features')
    if not isinstance(matrix, dict) or not matrix:
        raise ValueError('psd_feature_matrix_unavailable')
    features = {}
    for key, observation in matrix.items():
        if (not selector(key, exact=True) or not isinstance(observation, dict)
                or not isinstance(observation.get('status'), str) or observation['status'] not in STATUSES):
            raise ValueError('psd_feature_matrix_invalid')
        features[key] = {**observation, 'observationSha256': digest({'feature': key, 'observation': observation})}
    required, missing = set(), []
    for requested in policy.get('requiredFeatures', []):
        matched = {key for key in features if requested == '*' or requested == key or requested == key.rsplit(':', 1)[-1]}
        required.update(matched)
        if not matched:
            missing.append(requested)
    # 已观察的丢失／降级默认阻止交付；unknown 仅在用户要求该特性时成为必要门禁。
    needed = required | {key for key, value in features.items() if value['status'] in ('lost', 'degraded')}
    accepted, unaccepted = {}, []
    receipts = policy.get('acceptedLosses', {})
    source_matches = source_sha256 is not None and policy.get('acceptedForSourceSha256') == source_sha256
    for key in sorted(needed):
        observation = features[key]
        if observation['status'] == 'retained':
            continue
        receipt = receipts.get(key)
        if (receipt and source_matches and receipt['status'] == observation['status']
                and receipt['observationSha256'] == observation['observationSha256']):
            accepted[key] = receipt
        else:
            unaccepted.append(key)
    unused = sorted(set(receipts) - set(accepted))
    status = 'FAIL' if unaccepted or missing or unused else 'ACCEPTED_LOSS' if accepted else 'PASS'
    return {'schema': 'photocraft-psd-acceptance/v1', 'status': status,
            'native': report['native'], 'inspection': report['inspection'],
            'psdInspection': report.get('psdInspection'),
            'psd': {'location': output['location'], 'sha256': output['sha256']},
            'planSha256': plan_sha256, 'sourceProjectSha256': source_sha256, 'policy': policy, 'features': features,
            'unaccepted': unaccepted, 'unobservedRequired': missing, 'unusedAcceptances': unused,
            'acceptedLosses': accepted, 'completeFidelity': False,
            'scope': 'Required observed PSD properties and exact accepted losses only; independent visual/editor fidelity and creative acceptance NOT_RUN.'}


def validate_saved(root, plan, report, files):
    """只读交付检查重算功能矩阵及门禁，兼容无新策略的历史包。"""
    # 新报告使用公开允许的输出观察；旧顶层引用只读兼容，双份引用冲突拒绝。
    nested = [output['observations']['psdGate'] for output in report.get('outputs', [])
              if isinstance(output, dict) and output.get('format') == 'psd'
              and isinstance(output.get('observations'), dict) and 'psdGate' in output['observations']]
    if len(nested) > 1:
        raise ValueError('delivery_psd_gate_identity_mismatch')
    legacy = report.get('psdGate')
    if legacy is not None and nested and legacy != nested[0]:
        raise ValueError('delivery_psd_gate_identity_mismatch')
    ref = nested[0] if nested else legacy
    if ref is None:
        if 'psdPolicy' in plan or 'psd-acceptance.json' in files:
            raise ValueError('delivery_psd_gate_missing')
        return
    if (not isinstance(ref, dict) or ref.get('location') != 'psd-acceptance.json'
            or 'psd-acceptance.json' not in files or ref.get('sha256') != files['psd-acceptance.json']
            or not isinstance(report.get('psdInspection'), dict)):
        raise ValueError('delivery_psd_gate_identity_mismatch')
    delivery = load('delivery')
    native = delivery.read_json(delivery.file_path(root, 'native.json'))
    psd = delivery.read_json(delivery.file_path(root, 'psd-inspection.json'))
    effects = used_effects(plan)
    matrix = load('psd_features').assess(native, psd, effects)
    outputs = [out for out in report['outputs'] if out.get('format') == 'psd']
    if len(outputs) != 1 or outputs[0].get('observations', {}).get('featureMatrix') != matrix:
        raise ValueError('delivery_psd_matrix_mismatch')
    gate = assess(report, plan.get('psdPolicy', {}), files['plan.json'], plan.get('expectedProjectSha256'))
    stored = delivery.read_json(delivery.file_path(root, 'psd-acceptance.json'))
    if stored != gate or gate['status'] == 'FAIL':
        raise ValueError('delivery_psd_gate_unaccepted_or_mismatched')


def used_effects(plan):
    return any(str(op.get('command', '')).startswith(('filter.', 'layer.smartFilter.'))
               or op.get('command') == 'native.command' and str(op.get('params', {}).get('command', '')).startswith(('filter.', 'layer.smartFilter.'))
               for op in plan.get('operations', []))
