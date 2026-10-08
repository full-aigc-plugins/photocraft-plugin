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

def validate_asset(params,path,resolved=False):
    contract=load_module('parameter_contract')
    if not isinstance(params,dict) or set(params)-{'asset','center','name'}:raise ValueError('parameter_unknown_field: '+path)
    for key,value in params.items():contract.validate_value({'asset':'str','center':'[x,y]','name':'str'}[key],value,path+'.'+key,resolved)


def native_module():
    spec = importlib.util.spec_from_file_location('craft_native_workflow', Path(__file__).with_name('native_workflow.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def validate(plan, bindings=None, check_references=True, inherited_assets=()):
    if not isinstance(plan, dict) or not isinstance(plan.get('operations'), list):
        raise ValueError('operations_required: $.operations')
    allowed = {'document', 'operations', 'assets', 'exports', 'minimumLayers',
               'expectedProjectSha256', 'expectedManifestSha256', 'protectedRegions', 'variant', 'assertions', 'preserveObjects', 'filterContract','acceptedFontSubstitutions','psdPolicy','flatExport','assetProvenance'}
    if set(plan) - allowed:
        raise ValueError('unknown_plan_field: $.' + sorted(set(plan) - allowed)[0])
    # 保留旧的片段校验入口；完整 execute 总会传入已核验的绑定再严格检查。
    check_references = check_references and (bindings is not None or 'document' in plan or 'assets' in plan)
    for operation in plan['operations']:
        if isinstance(operation, dict):
            validate_smart(operation.get('command'), operation.get('params', {}))
    try:
        json.dumps(plan, allow_nan=False)
    except (ValueError, TypeError):
        raise ValueError('invalid_json_parameters') from None
    if 'minimumLayers' in plan and (type(plan['minimumLayers']) is not int or plan['minimumLayers'] < 0):
        raise ValueError('invalid_minimum_layers')
    for key in ('expectedProjectSha256', 'expectedManifestSha256'):
        if key in plan and (not isinstance(plan[key], str) or not re.fullmatch(r'[a-f0-9]{64}', plan[key])):
            raise ValueError('invalid_expected_digest: ' + key)
    assets = plan.get('assets', {})
    if not isinstance(assets, dict):
        raise ValueError('invalid_assets')
    for name, entry in assets.items():
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z][\w-]*', name):
            raise ValueError('invalid_asset_name')
        if (not isinstance(entry, dict) or set(entry) != {'path', 'sha256'}
                or not isinstance(entry['path'], str) or not entry['path']
                or not isinstance(entry['sha256'], str) or not re.fullmatch(r'[a-f0-9]{64}', entry['sha256'])):
            raise ValueError('invalid_asset: ' + name)
    load_module('flat_export').validate_provenance(plan)
    if 'flatExport' in plan:load_module('flat_export').validate(plan['flatExport'])
    if 'filterContract' in plan:load_module('filter_contract').validate(plan['filterContract'])
    if 'assertions' in plan:load_module('domain_assertions').validate_assertions(plan['assertions'])
    if 'preserveObjects' in plan:
        changes=plan['preserveObjects']
        if (not isinstance(changes,dict) or any(not isinstance(k,str) or not k.isdigit() or not isinstance(v,list) or any(not isinstance(f,str) or f.startswith('_') or f in ('id','kind') for f in v) for k,v in changes.items())):raise ValueError('invalid_preserve_objects')
    if 'protectedRegions' in plan:load_module('pixel_guard').validate(plan['protectedRegions'])
    if 'variant' in plan:load_module('layout_variant').validate(plan['variant'])
    aliases = set()
    available = set(bindings or {}) | {'asset_' + name for name in assets}
    commands = load_module('commands')
    if 'acceptedFontSubstitutions' in plan:
        mapping=plan['acceptedFontSubstitutions']
        if not isinstance(mapping,dict) or not mapping or any(not isinstance(k,str) or not k or not isinstance(v,str) or not v for k,v in mapping.items()):raise ValueError('invalid_font_substitutions')
    rows = {row['id']: row for row in commands.catalog()['commands']}
    if check_references and 'variant' in plan:commands.references(plan['variant']['roles'],available,'$.variant.roles')
    for operation_index,operation in enumerate(plan['operations']):
        if not isinstance(operation, dict) or set(operation) - {'command', 'params', 'as'}:
            raise ValueError('invalid_operation: $.operations['+str(operation_index)+']')
        params = operation.get('params', {})
        if not isinstance(params, dict):
            raise ValueError('invalid_params: $.operations['+str(operation_index)+'].params')
        if check_references:
            commands.references(params, available,'$.operations['+str(operation_index)+'].params')
            if operation.get('command')=='native.command' and str(params.get('command','')).startswith('filter.') and 'filterContract' in plan:commands.references(plan['filterContract'],available,'$.filterContract')
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
            available.add(alias)
        validate_smart(operation['command'], params)
        command = operation['command']
        if command=='asset.place':validate_asset(params,'$.operations['+str(operation_index)+'].params')
        if command in rows and command not in SMART_LAYER:commands.validate_parameters(command,params,'$.operations['+str(operation_index)+'].params')
        if command in {'asset.place', 'asset.placeSmart', *SMART_SOURCE}:
            asset = params.get('asset')
            if not isinstance(asset, str) or (check_references and asset not in set(assets) | set(inherited_assets)):
                raise ValueError('unregistered_asset_path')
        if command == 'asset.place' and set(params) - {'asset', 'center', 'name'}:
            raise ValueError('unregistered_asset_path')
        if command in rows and command not in SMART_LAYER:
            fields = set(re.findall(r'"([A-Za-z][A-Za-z0-9]*)"\s*:', rows[command]['params']))
            if command == 'type.create':
                fields.update(re.findall(r'"([A-Za-z][A-Za-z0-9]*)"\s*:', rows['type.setStyle']['params']))
            if command=='shape.create':
                fields.add('shape')
                if 'shape' in params and ('kind' in params or params['shape'] not in ('rectangle','ellipse','roundedRect','polygon','star','line','path')):raise ValueError('invalid_legacy_shape')
            if fields and set(params) - fields:
                raise ValueError('unknown_command_parameter: ' + command)
    if 'filterContract' in plan:
        if not any(op['command']=='native.command' and str(op['params'].get('command','')).startswith('filter.') for op in plan['operations']):raise ValueError('filter_operation_required')
    if check_references and 'assertions' in plan:commands.references(plan['assertions'],available,'$.assertions')
    formats = []
    if not isinstance(plan.get('exports', []), list):
        raise ValueError('invalid_exports')
    for item in plan.get('exports', []):
        if not isinstance(item, dict) or set(item) != {'format'} or item['format'] not in ('png', 'psd', 'jpg', 'tif', 'webp'):
            raise ValueError('invalid_export')
        formats.append(item['format'])
    if len(formats) != len(set(formats)):
        raise ValueError('duplicate_export')
    if 'flatExport' in plan and not set(formats) & load_module('flat_export').FORMATS:raise ValueError('flat_export_format_required')
    if 'psdPolicy' in plan:
        load_module('psd_policy').validate(plan['psdPolicy'])
        if 'psd' not in formats:
            raise ValueError('psd_policy_requires_psd')
    if 'document' in plan:
        doc = plan['document']
        if not isinstance(doc, dict) or set(doc) - {'name', 'width', 'height', 'background', 'mode', 'depth'}:
            raise ValueError('unsupported_document_setting')
        commands.validate_tool_parameters('doc_new',doc,'$.document')
        for field in ('width', 'height'):
            if type(doc.get(field)) is not int or not 0 < doc[field] <= 16384:
                raise ValueError('invalid_document_size: $.document.'+field)


def load_module(name):
    spec = importlib.util.spec_from_file_location('craft_' + name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def call_tool(session, name, args, state, receipts):
    """原生请求可能已产生副作用；仅在回复验证后登记成功。"""
    load_module('commands').validate_tool_parameters(name,args,'$.tools.'+name,True)
    if os.environ.get('CRAFT_STOP_FILE') and Path(os.environ['CRAFT_STOP_FILE']).exists():raise load_module('operation_errors').error('outcome_unknown: stop_requested; reconcile preserved work')
    state['lastAttempt'] = {'tool': name, 'arguments': args, 'phase': 'submitted'}
    reply = session.request('tools/call', {'name': name, 'arguments': args})
    value = load_module('commands').parse_reply(reply)
    state['lastAttempt']['phase'] = 'reply_validated'
    receipts.append({'tool': name, 'arguments': args, 'result': value})
    return value


def preflight(plan, output=None, source=None):
    validate(plan, check_references=not bool(source))
    if output is not None:
        output = Path(output).absolute()
        output = output.parent.resolve()/output.name
        if output.exists() or output.is_symlink():
            raise ValueError('output_exists')
    if 'protectedRegions' in plan and not source:raise ValueError('protected_source_required')
    if 'variant' in plan and not source:raise ValueError('variant_source_required')
    if plan.get('psdPolicy', {}).get('acceptedLosses'):
        if not source or plan['psdPolicy']['acceptedForSourceSha256'] != plan.get('expectedProjectSha256'):
            raise ValueError('psd_acceptance_source_mismatch')
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
    validate(plan, bindings, inherited_assets=inherited_assets)
    if source:
        source_model=load_module('delivery').read_json(source/'native.json')
        if 'protectedRegions' in plan and (source_model.get('mode')!='Rgb' or source_model.get('depth')!=8):raise ValueError('protected_pixel_mode_unsupported: RGB8 native source required')
        known=set(load_module('domain_assertions').index(source_model))
        creates=False
        for operation in plan['operations']:
            layer=operation.get('params',{}).get('layer')
            if type(layer) is int and not creates and str(layer) not in known:raise ValueError('unknown_source_layer: '+str(layer))
            if operation['command'].startswith(('layer.new','asset.place','type.create','shape.create')) or operation['command']=='native.command':creates=True
    load_module('flat_export').provenance_preflight(plan,inherited_assets,source)
    if 'flatExport' in plan:
        model=source_model if source else plan['document']
        if model.get('depth',8)!=8 or model.get('mode','rgb').lower() not in ('rgb',):raise ValueError('flat_source_mode_unsupported: RGB8 required')
    registered=set(inherited_assets)|set(plan.get('assets',{}))
    for operation in plan['operations']:
        if operation['command'] in SMART_SOURCE | {'asset.placeSmart'} and operation['params']['asset'] not in registered:raise ValueError('unregistered_asset_path')
    for name, entry in plan.get('assets', {}).items():
        original = Path(entry['path'])
        if original.is_symlink() or not original.is_file() or sha(original) != entry['sha256']:
            raise ValueError('asset_checksum_mismatch: ' + name)
        if original.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp', '.tif', '.tiff'):
            raise ValueError('unsupported_asset_format')
    if 'preserveObjects' in plan and not source:raise ValueError('preservation_source_required')
    return output, source, source_project, source_hash, source_manifest_hash, bindings, inherited_assets


def execute(plan, output, runtime_home=None, source=None):
    output, source, source_project, source_hash, source_manifest_hash, bindings, inherited_assets = preflight(plan, output, source)
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
            gate=load_module('capabilities').Gate(session,load_module('commands'),installed['binarySha256'],runtime_identity=installed.get('runtimeIdentity'))
            capability=gate.check()
            def call(name, args):
                if name=='command_run':
                    load_module('commands').validate_parameters(args['id'],args['params'],'$.native.'+args['id'],True)
                gate.check_scope([args['id']] if name=='command_run' else [],[name],args['id'] if name=='command_run' else None)
                return call_tool(session, name, args, recovery_state, receipts)
            opened = call('doc_open', {'path': 'source.pcraft'}) if source_project else call('doc_new', plan['document'])
            target_index = opened.get('index', opened.get('document'))
            initial_inspection = call('doc_inspect', {}) if 'variant' in plan or 'preserveObjects' in plan else None
            facts_before=load_module('native_facts').collect(stage/'source.pcraft',initial_inspection,call) if source_project and 'preserveObjects' in plan and load_module('native_facts').required(plan) else None
            variant_before = initial_inspection if 'variant' in plan else None
            variant_roles = resolve(plan['variant']['roles'], bindings) if 'variant' in plan else None
            variant_steps = []
            filter_steps=[]
            if 'protectedRegions' in plan:
                call('doc_export', {'path':'protection-before.png','format':'png'})
            for operation in plan['operations']:
                if os.environ.get('CRAFT_STOP_FILE') and Path(os.environ['CRAFT_STOP_FILE']).exists():raise load_module('operation_errors').error('outcome_unknown: stop_requested')
                params = resolve(operation.get('params', {}), bindings)
                if operation['command']=='asset.place':validate_asset(params,'$.asset.place.params',True)
                validate_smart(operation['command'],params,True)
                if operation['command']=='shape.create' and 'shape' in params:
                    params=dict(params);params['kind']={'rectangle':'rect'}.get(params['shape'],params['shape']);del params['shape']
                is_filter=operation['command']=='native.command' and str(params.get('command','')).startswith('filter.') and 'filterContract' in plan
                if is_filter:
                    filter_config=resolve(plan['filterContract'],bindings)
                    filter_context=load_module('filter_contract').check(filter_config,call('doc_inspect',{}))
                    filter_before='filter-'+str(len(filter_steps))+'-before.png';filter_after='filter-'+str(len(filter_steps))+'-after.png'
                    call('doc_export',{'path':filter_before,'format':'png'})
                if operation['command'] == 'native.command':
                    gate.check_scope([params['command']],['command_run'],params['command'])
                    result = native_module().execute(session, params, recovery_state, receipts, stage)
                elif operation['command'] in SMART_SOURCE | {'asset.placeSmart'}:
                    asset=params['asset']
                    native_params={key:value for key,value in params.items() if key!='asset'}
                    native_params['path']=assets[asset]['path']
                    command='file.placeEmbedded' if operation['command']=='asset.placeSmart' else operation['command']
                    # 目录 enabled 依赖当前选中对象；显式目标先选中再探测，不能沿用重开后的默认选择。
                    if 'layer' in params:call('command_run',{'id':'layer.select','params':{'layer':params['layer']}})
                    result=call('command_run',{'id':command,'params':native_params})
                    if operation['command']=='layer.smartObjects.relinkToFile':
                        inspected=load_module('domain_assertions').index(call('doc_inspect',{})).get(str(params['layer']),{})
                        if inspected.get('smartSourceKind')=='linked':call('command_run',{'id':'layer.smartObjects.convertToEmbedded','params':{'layer':params['layer']}})
                        elif inspected.get('smartSourceKind')!='embedded':raise ValueError('smart_source_kind_unverified')
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
                if is_filter:
                    call('doc_export',{'path':filter_after,'format':'png'})
                    pixels=load_module('filter_contract').changed(stage/filter_before,stage/filter_after,filter_config['region'])
                    filter_steps.append({'command':params['command'],'context':filter_context,'pixels':pixels,'before':filter_before,'after':filter_after})
                if operation.get('as'):
                    bindings[operation['as']] = result
            # 原生命令仅允许含文字的文档；纯图片合成不具备此命令前置条件。
            font_inspection = call('doc_inspect', {})
            if contains_type_layers(font_inspection.get('layers')):
                fonts = call('command_run', {'id': 'type.resolveMissingFonts', 'params': {}})
                if fonts.get('missing') and plan.get('acceptedFontSubstitutions'):
                    accepted=plan['acceptedFontSubstitutions']
                    replacement=call('command_run',{'id':'type.resolveMissingFonts','params':{'map':accepted}})
                    # 替换回复的 missing 是替换前列表，必须重新只读查询当前字体状态。
                    fonts_after=call('command_run',{'id':'type.resolveMissingFonts','params':{}})
                    (stage/'font-substitutions.json').write_text(json.dumps({'schema':'photocraft-font-substitutions/v1','accepted':accepted,'before':fonts,'replacement':replacement,'after':fonts_after},ensure_ascii=False,indent=2)+'\n')
                    fonts=fonts_after
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
            native_facts=load_module('native_facts').collect(stage/'project.pcraft',native,call) if load_module('native_facts').required(plan) else None
            if native_facts:
                (stage/'native-facts.json').write_text(json.dumps(native_facts,ensure_ascii=False,indent=2)+'\n')
                if facts_before:
                    facts_preservation=load_module('native_facts').preserve(facts_before,native_facts,plan['preserveObjects'])
                    (stage/'native-facts-preservation.json').write_text(json.dumps(facts_preservation,ensure_ascii=False,indent=2)+'\n')
            editable=load_module('domain_assertions').editable_count(native)
            if editable < plan.get('minimumLayers', 1):
                raise ValueError('editable_layer_gate_failed')
            if 'assertions' in plan:
                assertion_report=load_module('domain_assertions').assert_objects(native,resolve(plan['assertions'],bindings),native_facts)
                (stage/'object-assertions.json').write_text(json.dumps(assertion_report,ensure_ascii=False,indent=2)+'\n')
            if 'preserveObjects' in plan:
                preservation=load_module('domain_assertions').compare(initial_inspection,native,plan['preserveObjects'])
                (stage/'object-preservation.json').write_text(json.dumps(preservation,ensure_ascii=False,indent=2)+'\n')
            if 'variant' in plan:
                variant = load_module('layout_variant').assess(plan['variant'],variant_before,native,variant_steps,variant_roles)
                (stage/'layout-variant.json').write_text(json.dumps(variant,ensure_ascii=False,indent=2)+'\n')
            if 'protectedRegions' in plan:
                call('doc_export', {'path':'protection-after.png','format':'png'})
                protection = load_module('pixel_guard').compare(stage/'protection-before.png',stage/'protection-after.png',plan['protectedRegions'])
                (stage/'pixel-protection.json').write_text(json.dumps(protection,ensure_ascii=False,indent=2)+'\n')
            load_module('flat_export').collect(stage,plan,call,native)
            psd = None
            if any(item['format'] == 'psd' for item in plan.get('exports', [])):
                call('doc_open', {'path': 'design.psd'})
                psd = call('doc_inspect', {})
        if source_project and sha(source_project) != source_hash:
            raise ValueError('revision_conflict')
        if (stage / 'source.pcraft').exists():
            (stage / 'source.pcraft').unlink()
        if filter_steps:(stage/'filter-contract.json').write_text(json.dumps({'schema':'photocraft-filter-execution/v1','steps':filter_steps},ensure_ascii=False,indent=2)+'\n')
        (stage/'capabilities.json').write_text(json.dumps(capability,ensure_ascii=False,indent=2)+'\n')
        (stage/'capability-checks.json').write_text(json.dumps(gate.checks,ensure_ascii=False,indent=2)+'\n')
        for name, value in [('native.json', native), ('plan.json', plan), ('operations.json', receipts)]:
            (stage / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
        if psd is not None:
            (stage / 'psd-inspection.json').write_text(json.dumps(psd, ensure_ascii=False, indent=2) + '\n')
        load_module('flat_export').write_provenance(stage,plan,assets,source)
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
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', action='store_true', help='仅验证计划、素材和源包，不安装或编辑')
    parser.add_argument('--source', type=Path)
    parser.add_argument('--runtime-home', type=Path)
    parser.add_argument('--asset', action='append', default=[], metavar='NAME=PATH', help='登记实际素材并计算 SHA-256')
    args = parser.parse_args()
    phase='validation'
    try:
        plan = load_module('commands').reply_json(args.plan.read_text())
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
        if args.check:
            preflight(plan,args.output,args.source)
            result={'result':'PASS','scope':'strict plan, input files and source delivery integrity','nativeExecution':'NOT_RUN'}
        else:
            if args.output is None:raise ValueError('output_required')
            preflight(plan,args.output,args.source)
            phase='execution'
            result=execute(plan,args.output,args.runtime_home,args.source)
        print(json.dumps(result,ensure_ascii=False))
    except (ValueError, RuntimeError, OSError) as error:
        print(json.dumps(load_module('operation_errors').describe(error, phase), ensure_ascii=False))
        raise SystemExit(1)

if __name__ == '__main__':
    main()
