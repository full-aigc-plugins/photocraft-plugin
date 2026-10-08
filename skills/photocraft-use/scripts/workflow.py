#!/usr/bin/env python3
"""PhotoCraft 原生分层计划；独立会话、限定读写目录和不可变修订交付。"""
import argparse
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import tempfile

def exchange_report(root,outputs,warnings):
    spec=importlib.util.spec_from_file_location('craft_exchange_loss',Path(__file__).with_name('exchange_loss.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.write_report(root,outputs,warnings)

ALLOWED = {'native.command', 
    'asset.placeSmart', 'layer.smartObjects.convertToSmartObject',
    'layer.smartObjects.replaceContents', 'layer.smartObjects.relinkToFile',
    'layer.smartObjects.convertToEmbedded',
    'shape.create', 'type.create', 'type.edit', 'type.setStyle',
    'layer.new.layer', 'layer.new.group', 'layer.renameLayer', 'layer.select',
    'layer.newFillLayer.solidColor', 'layer.newFillLayer.gradient',
    'layer.newAdjustmentLayer.brightnessContrast', 'layer.newAdjustmentLayer.hueSaturation',
    'layer.layerMask.revealAll', 'layer.layerMask.hideAll',
    'layer.layerMask.revealSelection', 'layer.layerMask.hideSelection',
    'layer.layerMask.enabled', 'layer.vectorMask.add', 'layer.vectorMask.edit',
    'select.rect', 'select.deselect', 'asset.place',
    'paint.stroke', 'paint.cloneStamp', 'paint.healingBrush',
    'image.imageSize', 'image.canvasSize',
}


def contains_type_layers(layers):
    """检查原生图层树；含组内文字时仍执行字体门禁，未知结构不能绕过检查。"""
    if not isinstance(layers, list):
        raise ValueError('invalid_native_layer_inspection')
    found = False
    for layer in layers:
        if not isinstance(layer, dict) or not isinstance(layer.get('kind'), str):
            raise ValueError('invalid_native_layer_inspection')
        found = (layer['kind'] == 'Type') or found
        if layer['kind'] == 'Group' or 'children' in layer:
            found = contains_type_layers(layer.get('children')) or found
    return found

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def resolve(value, bindings):
    if isinstance(value, dict):
        if set(value) == {'$ref'}:
            try:
                parts = value['$ref'].split('.')
                result = bindings[parts[0]]
                for field in parts[1:]:
                    result = result[int(field)] if isinstance(result, list) else result[field]
                return result
            except (KeyError, IndexError, TypeError, ValueError, AttributeError):
                raise ValueError('unresolved_reference: ' + str(value['$ref'])) from None
        return {key: resolve(item, bindings) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve(item, bindings) for item in value]
    return value


SMART_SOURCE = {'layer.smartObjects.replaceContents', 'layer.smartObjects.relinkToFile'}
SMART_LAYER = SMART_SOURCE | {'layer.smartObjects.convertToSmartObject', 'layer.smartObjects.convertToEmbedded'}

def validate_smart(command, params, resolved=False):
    """智能对象只接受显式图层和登记素材；原生路径由执行器生成。"""
    if command not in SMART_LAYER | {'asset.placeSmart'}:return
    allowed = {'asset', 'center', 'scale', 'fit'} if command == 'asset.placeSmart' else {'layer', *({'asset'} if command in SMART_SOURCE else set())}
    if not isinstance(params, dict) or set(params)-allowed:raise ValueError('invalid_smart_params')
    if command in SMART_LAYER:
        layer=params.get('layer')
        reference=not resolved and isinstance(layer,dict) and set(layer)=={'$ref'} and isinstance(layer['$ref'],str) and re.fullmatch(r'[A-Za-z][\w-]*(?:\.[A-Za-z0-9_]+)+',layer['$ref'])
        if not reference and not (type(layer) is int and 0 < layer <= 2**64-1):raise ValueError('invalid_smart_params')
    if command in SMART_SOURCE or command=='asset.placeSmart':
        if not isinstance(params.get('asset'),str) or not re.fullmatch(r'[A-Za-z][\w-]*',params['asset']):raise ValueError('invalid_smart_params')
    if command=='asset.placeSmart':
        finite=lambda n:type(n) in (int,float) and math.isfinite(n)
        if 'center' in params and (not isinstance(params['center'],list) or len(params['center'])!=2 or not all(finite(n) for n in params['center'])):raise ValueError('invalid_smart_params')
        if 'scale' in params and (not finite(params['scale']) or not 0 < params['scale'] <= 10000):raise ValueError('invalid_smart_params')
        if 'fit' in params and type(params['fit']) is not bool:raise ValueError('invalid_smart_params')


def native_module():
    spec = importlib.util.spec_from_file_location('craft_native_workflow', Path(__file__).with_name('native_workflow.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def validate(plan):
    if not isinstance(plan, dict) or not isinstance(plan.get('operations'), list):
        raise ValueError('operations_required')
    if 'protectedRegions' in plan:load_module('pixel_guard').validate(plan['protectedRegions'])
    if 'variant' in plan:load_module('layout_variant').validate(plan['variant'])
    aliases = set()
    for operation in plan['operations']:
        if operation.get('command') == 'native.command':
            native_module().validate(operation.get('params'))
        if operation.get('command') not in ALLOWED:
            raise ValueError('unsupported_command')
        alias = operation.get('as')
        if alias is not None:
            if alias in aliases:
                raise ValueError('duplicate_alias')
            if not isinstance(alias, str) or not re.fullmatch(r'[a-zA-Z][\w-]*', alias):
                raise ValueError('invalid_alias')
            aliases.add(alias)
        if not isinstance(operation.get('params', {}), dict):
            raise ValueError('invalid_params')
        validate_smart(operation['command'],operation.get('params',{}))
    formats = []
    for item in plan.get('exports', []):
        if set(item) != {'format'} or item['format'] not in ('png', 'psd', 'jpg', 'tif', 'webp'):
            raise ValueError('invalid_export')
        formats.append(item['format'])
    if len(formats) != len(set(formats)):
        raise ValueError('duplicate_export')
    if 'document' in plan:
        doc = plan['document']
        if set(doc) - {'name', 'width', 'height', 'background', 'mode', 'depth'}:
            raise ValueError('unsupported_document_setting')
        for field in ('width', 'height'):
            if type(doc.get(field)) is not int or not 0 < doc[field] <= 16384:
                raise ValueError('invalid_document_size')


def load_module(name):
    spec = importlib.util.spec_from_file_location('craft_' + name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def execute(plan, output, runtime_home=None, source=None):
    validate(plan)
    output = Path(output).absolute()
    output = output.parent.resolve()/output.name
    if output.exists() or output.is_symlink():
        raise ValueError('output_exists')
    if 'protectedRegions' in plan and not source:raise ValueError('protected_source_required')
    if 'variant' in plan and not source:raise ValueError('variant_source_required')
    source_project, source_hash, source_manifest_hash = None, None, None
    bindings = {}
    inherited_assets = {}
    if source:
        source = Path(source).resolve()
        source_project = source / 'project.pcraft'
        if source_project.is_symlink():
            raise ValueError('invalid_source')
        source_manifest_hash = sha(source / 'manifest.json')
        prior = load_module('delivery').read_json(source / 'manifest.json')
        source_hash = sha(source_project)
        if source_hash != prior['files']['project.pcraft'] or source_hash != plan.get('expectedProjectSha256'):
            raise ValueError('revision_conflict')
        load_module('delivery').validate_delivery(source, plan.get('expectedManifestSha256', source_manifest_hash))
        if 'document' in plan:
            raise ValueError('revision_cannot_recreate_document')
        bindings = prior['bindings']
        inherited_assets = prior.get('assets', {})
    elif 'document' not in plan:
        raise ValueError('document_required')
    registered=set(inherited_assets)|set(plan.get('assets',{}))
    for operation in plan['operations']:
        if operation['command'] in SMART_SOURCE | {'asset.placeSmart'} and operation['params']['asset'] not in registered:raise ValueError('unregistered_asset_path')
    installed = load_module('bootstrap').install(
        json.loads(Path(__file__).with_name('runtime.lock.json').read_text()),
        runtime_home or os.environ.get('CRAFT_RUNTIME_HOME', str(Path.home() / '.local/share/craft-runtimes')))
    output.parent.mkdir(parents=True, exist_ok=True)
    recovery_state = {}
    execution_identity = {'planHash': hashlib.sha256(json.dumps(plan, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest(),
                         'inputHashes': {name: asset['sha256'] for name, asset in {**inherited_assets, **plan.get('assets', {})}.items()},
                         'projectRevision': source_hash, 'runtimeSha256': installed['binarySha256']}
    with load_module('output_guard').claim(output, execution_identity), load_module('preserved_stage').preserved_stage(output, '.photocraft-', recovery_state) as temporary:
        stage = Path(temporary)
        assets = {}
        for name, entry in inherited_assets.items():
            filename = entry['path']
            if Path(filename).name != filename or (source / filename).is_symlink():
                raise ValueError('invalid_inherited_asset_path')
            if sha(source / filename) != entry['sha256']:
                raise ValueError('asset_checksum_mismatch')
            shutil.copyfile(source / filename, stage / filename)
            if sha(stage / filename) != entry['sha256']:
                raise ValueError('asset_changed_during_copy')
            assets[name] = entry
        for name, entry in plan.get('assets', {}).items():
            if not re.fullmatch(r'[a-zA-Z][\w-]*', name):
                raise ValueError('invalid_asset_name')
            original = Path(entry['path'])
            if original.is_symlink() or not original.is_file() or sha(original) != entry['sha256']:
                raise ValueError('asset_checksum_mismatch')
            suffix = original.suffix.lower()
            if suffix not in ('.png', '.jpg', '.jpeg', '.webp', '.tif', '.tiff'):
                raise ValueError('unsupported_asset_format')
            target = stage / ('asset-' + name + suffix)
            shutil.copyfile(original, target)
            if sha(target) != entry['sha256']:
                raise ValueError('asset_changed_during_copy')
            assets[name] = {'path': target.name, 'sha256': entry['sha256']}
            bindings['asset_' + name] = {'path': target.name}
        if source_project:
            shutil.copyfile(source_project, stage / 'source.pcraft')
        argv = [installed['executable'], 'mcp', '--automation-read-root', str(stage), '--automation-write-root', str(stage)]
        receipts = []
        recovery_state['operations'] = receipts
        with load_module('mcp_session').Session(argv) as session:
            def call(name, args):
                recovery_state['lastAttempt'] = {'tool': name, 'arguments': args, 'phase': 'submitted'}
                result = session.request('tools/call', {'name': name, 'arguments': args})
                recovery_state['lastAttempt']['phase'] = 'reply_received'
                if result.get('isError'):
                    raise RuntimeError('command_failed: ' + name + ': ' + json.dumps(result['content']))
                content = result.get('content', [])
                if len(content) != 1 or content[0].get('type') != 'text':
                    raise RuntimeError('unexpected_result')
                value = json.loads(content[0]['text'])
                receipts.append({'tool': name, 'arguments': args, 'result': value})
                return value
            opened = call('doc_open', {'path': 'source.pcraft'}) if source_project else call('doc_new', plan['document'])
            target_index = opened.get('index', opened.get('document'))
            variant_before = call('doc_inspect', {}) if 'variant' in plan else None
            variant_roles = resolve(plan['variant']['roles'], bindings) if 'variant' in plan else None
            variant_steps = []
            if 'protectedRegions' in plan:
                call('doc_export', {'path':'protection-before.png','format':'png'})
            for operation in plan['operations']:
                params = resolve(operation.get('params', {}), bindings)
                validate_smart(operation['command'],params,True)
                if operation['command'] == 'native.command':
                    result = native_module().execute(session, params, recovery_state, receipts, stage)
                elif operation['command'] in SMART_SOURCE | {'asset.placeSmart'}:
                    asset=params['asset']
                    native_params={key:value for key,value in params.items() if key!='asset'}
                    native_params['path']=assets[asset]['path']
                    command='file.placeEmbedded' if operation['command']=='asset.placeSmart' else operation['command']
                    result=call('command_run',{'id':command,'params':native_params})
                    if operation['command']=='layer.smartObjects.relinkToFile':
                        call('command_run',{'id':'layer.smartObjects.convertToEmbedded','params':{'layer':params['layer']}})
                elif operation['command'] == 'asset.place':
                    if params.get('asset') not in assets or set(params) - {'asset', 'center', 'name'}:
                        raise ValueError('unregistered_asset_path')
                    opened_asset = call('doc_open', {'path': assets[params['asset']]['path']})
                    call('command_run', {'id': 'select.all', 'params': {}})
                    call('command_run', {'id': 'edit.copy', 'params': {}})
                    call('doc_select', {'index': target_index})
                    result = call('command_run', {'id': 'edit.paste', 'params': {'center': params['center']} if 'center' in params else {}})
                    call('command_run', {'id': 'layer.renameLayer', 'params': {'name': params.get('name', params['asset'])}})
                    current = call('doc_inspect', {})
                    result = {'layer': current['activeLayer']}
                    call('doc_close', {'index': opened_asset['index']})
                    call('doc_select', {'index': target_index})
                else:
                    geometry_before = call('doc_inspect', {}) if 'variant' in plan and operation['command'] in ('image.canvasSize', 'image.imageSize') else None
                    result = call('command_run', {'id': operation['command'], 'params': params})
                    if geometry_before is not None:
                        variant_steps.append({'command':operation['command'], 'before':[geometry_before['width'],geometry_before['height']], 'result':result})
                if operation.get('as'):
                    bindings[operation['as']] = result
            # 原生命令仅允许含文字的文档；纯图片合成不具备此命令前置条件。
            font_inspection = call('doc_inspect', {})
            if contains_type_layers(font_inspection.get('layers')):
                fonts = call('command_run', {'id': 'type.resolveMissingFonts', 'params': {}})
                if fonts.get('missing'):
                    raise ValueError('missing_fonts: ' + json.dumps(fonts['missing']))
            saved = call('doc_save', {'path': 'project.pcraft'})
            outputs = []
            for item in plan.get('exports', []):
                target = 'design.' + item['format']
                exported = call('doc_export', {'path': target, 'format': item['format']})
                if not (stage / target).is_file() or (stage / target).stat().st_size == 0:
                    raise ValueError('export_missing')
                outputs.append({'path': target, 'warnings': exported.get('warnings', [])})
            # 重新打开实际保存的工程，避免把内存状态当作持久化验收。
            call('doc_open', {'path': 'project.pcraft'})
            native = call('doc_inspect', {})
            if len(native['layers']) < plan.get('minimumLayers', 1):
                raise ValueError('editable_layer_gate_failed')
            if 'variant' in plan:
                variant = load_module('layout_variant').assess(plan['variant'],variant_before,native,variant_steps,variant_roles)
                (stage/'layout-variant.json').write_text(json.dumps(variant,ensure_ascii=False,indent=2)+'\n')
            if 'protectedRegions' in plan:
                call('doc_export', {'path':'protection-after.png','format':'png'})
                protection = load_module('pixel_guard').compare(stage/'protection-before.png',stage/'protection-after.png',plan['protectedRegions'])
                (stage/'pixel-protection.json').write_text(json.dumps(protection,ensure_ascii=False,indent=2)+'\n')
            psd = None
            if any(item['format'] == 'psd' for item in plan.get('exports', [])):
                call('doc_open', {'path': 'design.psd'})
                psd = call('doc_inspect', {})
        if source_project and sha(source_project) != source_hash:
            raise ValueError('revision_conflict')
        if (stage / 'source.pcraft').exists():
            (stage / 'source.pcraft').unlink()
        for name, value in [('native.json', native), ('plan.json', plan), ('operations.json', receipts)]:
            (stage / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
        if psd is not None:
            (stage / 'psd-inspection.json').write_text(json.dumps(psd, ensure_ascii=False, indent=2) + '\n')
        exchange_report(stage,[item['path'] for item in outputs],{item['path']:item['warnings'] for item in outputs})
        manifest = {'schema': 'photocraft-delivery/v1', 'sourceProjectSha256': source_hash,
                    'runtimeSha256': installed['binarySha256'], 'bindings': bindings, 'assets': assets,
                    'outputs': outputs, 'nativeWarnings': saved.get('warnings', []),
                    'files': {f.name: sha(f) for f in stage.iterdir() if f.is_file()},
                    'lossReport': {'path':'exchange-loss.json','sha256':sha(stage/'exchange-loss.json')}, 'acceptance': 'requires-domain-and-visual-review'}
        if 'variant' in plan:
            manifest['layoutVariant'] = {'path':'layout-variant.json','sha256':sha(stage/'layout-variant.json')}
        (stage / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        load_module('delivery').validate_delivery(stage)
        if source:
            load_module('delivery').validate_delivery(source, plan.get('expectedManifestSha256', source_manifest_hash))
        if output.exists() or output.is_symlink():
            raise ValueError('output_exists')
        stage.rename(output)
        return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--runtime-home', type=Path)
    parser.add_argument('--asset', action='append', default=[], metavar='NAME=PATH', help='登记实际素材并计算 SHA-256')
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text())
        seen = set()
        for value in args.asset:
            name, separator, filename = value.partition('=')
            if not separator or name in seen:
                raise ValueError('invalid_or_duplicate_asset_argument')
            seen.add(name)
            path = Path(filename).absolute()
            if path.is_symlink():
                raise ValueError('invalid_asset_path')
            plan.setdefault('assets', {})[name] = {'path': str(path), 'sha256': sha(path)}
        print(json.dumps(execute(plan, args.output, args.runtime_home, args.source), ensure_ascii=False))
    except (ValueError, RuntimeError, OSError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False))
        raise SystemExit(1)

if __name__ == '__main__':
    main()
