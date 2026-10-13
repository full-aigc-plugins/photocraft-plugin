"""实际重开平面导出、透明/颜色门禁与外部素材回执；不调用生成服务。"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import shutil
import zlib

FORMATS = {'png', 'jpg', 'tif', 'webp'}
HEX = re.compile('[a-f0-9]{64}')

def load(name):
    spec = importlib.util.spec_from_file_location('flat_' + name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

def sha(path):
    with Path(path).open('rb') as stream: return hashlib.file_digest(stream, 'sha256').hexdigest()

def valid_sha(value): return isinstance(value, str) and HEX.fullmatch(value) is not None

def validate(policy):
    if (not isinstance(policy, dict) or set(policy) - {'colorSpace', 'iccSha256', 'transparency'}
            or policy.get('colorSpace', 'Rgb') not in ('Rgb', 'Grayscale', 'Cmyk', 'Lab')
            or 'iccSha256' in policy and not valid_sha(policy['iccSha256'])
            or policy.get('transparency', 'any') not in ('any', 'opaque', 'preserve')):
        raise ValueError('invalid_flat_export')

def validate_provenance(plan):
    mapping = plan.get('assetProvenance', {})
    if not isinstance(mapping, dict): raise ValueError('invalid_asset_provenance')
    for name, item in mapping.items():
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z][\w-]*', name) or not isinstance(item, dict):
            raise ValueError('invalid_asset_provenance')
        if item == {'kind': 'provided'}: continue
        if (set(item) != {'kind', 'provider', 'model', 'requestId', 'assetSha256', 'receipt', 'usage'}
                or item.get('kind') != 'generated' or not valid_sha(item['assetSha256'])
                or any(not isinstance(item[k], str) or not item[k].strip() or len(item[k]) > 512 for k in ('provider', 'model', 'requestId'))):
            raise ValueError('invalid_asset_provenance')
        receipt, usage = item['receipt'], item['usage']
        if (not isinstance(receipt, dict) or set(receipt) != {'path', 'sha256'}
                or not isinstance(receipt['path'], str) or not receipt['path'] or not valid_sha(receipt['sha256'])
                or not isinstance(usage, dict) or set(usage) != {'quantity', 'unit'}
                or type(usage['quantity']) not in (int, float) or not 0 <= usage['quantity'] <= 10**15 or not math.isfinite(usage['quantity'])
                or usage['unit'] not in ('credits', 'images', 'tokens', 'seconds')):
            raise ValueError('invalid_asset_provenance')

def provenance_preflight(plan, inherited_assets, source):
    validate_provenance(plan)
    assets = {**inherited_assets, **plan.get('assets', {})}
    for name, entry in plan.get('assetProvenance', {}).items():
        if name not in assets: raise ValueError('generation_asset_unregistered')
        if entry['kind'] == 'provided': continue
        if entry['assetSha256'] != assets[name]['sha256']: raise ValueError('generation_asset_identity')
        path = Path(entry['receipt']['path'])
        if path.is_symlink() or not path.is_file() or sha(path) != entry['receipt']['sha256']:
            raise ValueError('generation_receipt_checksum')
        if path.stat().st_size > 1024 * 1024 or not isinstance(load('delivery').read_json(path), dict):
            raise ValueError('generation_receipt_invalid')

def surface(path, model, profile):
    width, height, pixels, chunks = load('pixel_guard').decode(path)
    icc = None
    for kind, data in chunks:
        if kind == b'iCCP':
            try:
                _, packed = data.split(b'\0', 1)
                if not packed or packed[0] != 0: raise ValueError('flat_icc_invalid')
                decoder = zlib.decompressobj(); raw = decoder.decompress(packed[1:], 4 * 1024 * 1024 + 1)
                if len(raw) > 4 * 1024 * 1024 or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail: raise ValueError('flat_icc_invalid')
                icc = hashlib.sha256(raw).hexdigest()
            except (ValueError, zlib.error) as error: raise ValueError('flat_icc_invalid') from error
    alpha = pixels[3::4]
    return {'width': width, 'height': height, 'mode': model['mode'], 'depth': model['depth'],
            'profile': profile.get('profile'), 'iccSha256': icc, 'alphaSha256': hashlib.sha256(alpha).hexdigest(),
            'transparentPixels': sum(a < 255 for a in alpha), 'rgba8Sha256': hashlib.sha256(pixels).hexdigest()}

def check(policy, source, output):
    validate(policy)
    if (source['width'], source['height']) != (output['width'], output['height']): raise ValueError('flat_size_mismatch')
    if 'colorSpace' in policy and policy['colorSpace'] != output['mode']: raise ValueError('flat_color_space_mismatch')
    if 'iccSha256' in policy and policy['iccSha256'] != output['iccSha256']: raise ValueError('flat_icc_mismatch')
    if policy.get('transparency') == 'opaque' and output['transparentPixels']: raise ValueError('flat_transparency_not_opaque')
    if policy.get('transparency') == 'preserve' and source['alphaSha256'] != output['alphaSha256']: raise ValueError('flat_transparency_changed')

def collect(stage, plan, call, native):
    """原生工程已保存并重开后，实际打开每个平面导出并保留渲染/颜色观察。"""
    if 'flatExport' not in plan: return None
    profile = call('command_run', {'id': 'edit.profileInfo', 'params': {}})
    call('doc_export', {'path': 'flat-source.png', 'format': 'png'})
    source = surface(stage / 'flat-source.png', native, profile)
    report = {'schema': 'photocraft-flat-export/v1', 'status': 'PASS', 'policy': plan['flatExport'],
              'nativeSha256': sha(stage / 'project.pcraft'), 'sourceProjectSha256': plan.get('expectedProjectSha256'),
              'source': source, 'outputs': [], 'scope': 'actual reopened color metadata and normalized RGBA8/alpha; no external print/visual fidelity claim'}
    for item in plan['exports']:
        fmt = item['format']
        if fmt not in FORMATS: continue
        call('doc_open', {'path': 'design.' + fmt}); model = call('doc_inspect', {})
        profile = call('command_run', {'id': 'edit.profileInfo', 'params': {}})
        proof = 'flat-' + fmt + '.png'; call('doc_export', {'path': proof, 'format': 'png'})
        observation = surface(stage / proof, model, profile)
        report['outputs'].append({'path': 'design.' + fmt, 'sha256': sha(stage / ('design.' + fmt)),
                                  'proof': proof, 'proofSha256': sha(stage / proof), 'observation': observation})
        try: check(plan['flatExport'], source, observation)
        except ValueError as error:
            report['status'] = 'FAIL'; report['error'] = str(error)
            (stage / 'flat-export.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n'); raise
    (stage / 'flat-export.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report

def write_provenance(stage, plan, assets, source):
    """原始生成回执按摘要复制；本地执行次数和外部声明用量分别记录。"""
    previous = {}
    if source and (source / 'asset-provenance.json').is_file(): previous = load('delivery').read_json(source / 'asset-provenance.json')['assets']
    if 'assetProvenance' not in plan and not previous: return
    records = {}
    for name, asset in assets.items():
        entry = plan.get('assetProvenance', {}).get(name)
        origin = None
        if entry is not None:
            if entry['kind'] == 'generated': origin = Path(entry['receipt']['path'])
        elif name not in plan.get('assets', {}) and name in previous:
            entry = previous[name]
            if entry['kind'] == 'generated': origin = load('delivery').file_path(source, entry['receipt']['path'])
        else: entry = {'kind': 'provided'}
        entry = dict(entry)
        if entry['kind'] == 'generated':
            if entry['assetSha256'] != asset['sha256']: raise ValueError('generation_asset_identity')
            target = 'generation-' + name + '.json'
            if origin.is_symlink() or sha(origin) != entry['receipt']['sha256']: raise ValueError('generation_receipt_checksum')
            shutil.copyfile(origin, stage / target)
            if sha(stage / target) != entry['receipt']['sha256']: raise ValueError('generation_receipt_changed')
            entry['receipt'] = {'path': target, 'sha256': sha(stage / target)}
        entry['assetSha256'] = asset['sha256']; records[name] = entry
    report = {'schema': 'photocraft-asset-provenance/v1', 'nativeSha256': sha(stage / 'project.pcraft'), 'sourceProjectSha256': plan.get('expectedProjectSha256'), 'assets': records,
              'generationUsage': [{'asset': name, 'provider': entry['provider'], **entry['usage']} for name, entry in records.items() if entry['kind'] == 'generated'],
              'localEditing': {'executedPlanOperations': len(plan['operations']), 'cloudGenerationCalls': 0},
              'sourceAuthenticity': 'NOT_PROVEN', 'billing': 'upstream recorded usage only; no payment or billing verification'}
    (stage / 'asset-provenance.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')

def _validate_saved(root, plan, manifest):
    """核对已保存合同，不把摘要一致提升为重新执行或来源真实性。"""
    delivery = load('delivery'); files = manifest['files']
    if 'flatExport' in plan or 'flat-export.json' in files:
        if 'flat-export.json' not in files: raise ValueError('flat_report_missing')
        report = delivery.read_json(root / 'flat-export.json')
        expected = ['design.' + item['format'] for item in plan['exports'] if item['format'] in FORMATS]
        if (report.get('schema') != 'photocraft-flat-export/v1' or report.get('status') != 'PASS'
                or report.get('nativeSha256') != files['project.pcraft'] or report.get('sourceProjectSha256') != plan.get('expectedProjectSha256')
                or report.get('policy') != plan.get('flatExport') or [item.get('path') for item in report.get('outputs', [])] != expected): raise ValueError('flat_report_identity')
        if 'flat-source.png' not in files: raise ValueError('flat_source_proof_missing')
        source_observation = report['source']
        if surface(root / 'flat-source.png', source_observation, {'profile': source_observation['profile']}) != source_observation: raise ValueError('flat_source_proof_changed')
        for item in report['outputs']:
            if item['path'] not in files or item['proof'] not in files or item['proof'] != 'flat-' + item['path'].rsplit('.',1)[-1] + '.png' or item.get('sha256') != files.get(item['path']) or item.get('proofSha256') != files.get(item['proof']): raise ValueError('flat_report_identity')
            observation = item['observation']
            if surface(delivery.file_path(root, item['proof']), observation, {'profile': observation['profile']}) != observation: raise ValueError('flat_output_proof_changed')
            check(report['policy'], report['source'], observation)
    if 'assetProvenance' in plan or 'asset-provenance.json' in files:
        if 'asset-provenance.json' not in files: raise ValueError('generation_report_missing')
        report = delivery.read_json(root / 'asset-provenance.json'); records = report.get('assets', {})
        if report.get('schema') != 'photocraft-asset-provenance/v1' or report.get('nativeSha256') != files['project.pcraft'] or report.get('sourceProjectSha256') != plan.get('expectedProjectSha256') or set(records) != set(manifest['assets']): raise ValueError('generation_report_identity')
        for name, entry in records.items():
            if entry.get('assetSha256') != manifest['assets'][name]['sha256']: raise ValueError('generation_asset_identity')
            if entry.get('kind') == 'generated':
                validate_provenance({'assetProvenance': {name: entry}})
                if entry['receipt']['path'] not in files or entry['receipt']['sha256'] != files[entry['receipt']['path']]: raise ValueError('generation_receipt_checksum')
            elif entry != {'kind': 'provided', 'assetSha256': manifest['assets'][name]['sha256']}: raise ValueError('generation_report_identity')
        expected_usage = [{'asset': name, 'provider': entry['provider'], **entry['usage']} for name, entry in records.items() if entry['kind'] == 'generated']
        if report.get('generationUsage') != expected_usage or report.get('localEditing') != {'executedPlanOperations': len(plan['operations']), 'cloudGenerationCalls': 0} or report.get('sourceAuthenticity') != 'NOT_PROVEN': raise ValueError('generation_meter_identity')

def verify_reopen(root, temporary, call, actual_native):
    """新只读会话重开导出，以临时 PNG 观察核对保存的 RGBA8 与颜色身份。"""
    if not (root / 'flat-export.json').is_file(): return None
    report = load('delivery').read_json(root / 'flat-export.json')
    profile = call('command_run', {'id': 'edit.profileInfo', 'params': {}})
    call('doc_export', {'path': 'source-observation.png', 'format': 'png'})
    if surface(Path(temporary) / 'source-observation.png', actual_native, profile) != report['source']:
        raise ValueError('flat_native_observation_changed')
    for index, item in enumerate(report['outputs']):
        call('doc_open', {'path': item['path']}); model = call('doc_inspect', {})
        profile = call('command_run', {'id': 'edit.profileInfo', 'params': {}})
        name = 'export-observation-' + str(index) + '.png'; call('doc_export', {'path': name, 'format': 'png'})
        if surface(Path(temporary) / name, model, profile) != item['observation']:
            raise ValueError('flat_export_observation_changed')
    return {'status': 'PASS', 'outputs': len(report['outputs']), 'scope': 'fresh fixed native decoder, full normalized RGBA8/alpha and color observations; external consumer fidelity NOT_RUN'}


def validate_saved(root, plan, manifest):
    """畸形来源报告使用统一预检错误，不泄漏未捕获类型异常。"""
    try:
        return _validate_saved(root, plan, manifest)
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError("flat_report_invalid") from error
