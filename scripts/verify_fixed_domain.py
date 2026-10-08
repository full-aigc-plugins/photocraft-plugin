#!/usr/bin/env python3
"""在真实固定安装上逐场景验证领域合同，保留原生工程；不推导创作或完整 V1 通过。"""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ('smart', 'test_smart_first_use', 'SmartFirstUse', 'SMART_FIRST_USE', 'INSTALLED_SMART_SKILL', 'photocraft-cli-layers'),
    ('protected', 'test_protected_regions_first_use', 'ProtectedFirstUse', 'PROTECTED_FIRST_USE', 'INSTALLED_PROTECTED_SKILL_ROOT', 'photocraft-cli-masks'),
    ('retouch', 'test_retouch_workflow_first_use', 'RetouchWorkflowFirstUse', 'RETOUCH_WORKFLOW_FIRST_USE', 'INSTALLED_RETOUCH_SKILL_ROOT', 'photocraft-cli-retouch'),
    ('chinese', 'test_chinese_text_first_use', 'ChineseTextFirstUseTests', 'CHINESE_TEXT_FIRST_USE', 'INSTALLED_TEXT_SKILL_ROOT', 'photocraft-cli-text'),
    ('fontless', 'test_fontless_first_use', 'FontlessFirstUseTests', 'PHOTO_FONTLESS_FIRST_USE', 'INSTALLED_PHOTO_FONTLESS_SKILL', 'photocraft-cli-layers'),
    ('optimization', 'test_optimization_native', 'OptimizationNativeTests', 'OPTIMIZATION_NATIVE_TEST', None, 'photocraft-use'),
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hashes(root):
    return {p.relative_to(root).as_posix(): digest(p) for p in sorted(root.rglob('*')) if p.is_file()}


def authored_skill_hash(repository, name):
    """按发布文件计算来源摘要；本地忽略的字节码不属于技能源制品。"""
    prefix = 'skills/' + name + '/'
    files = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z', '--', prefix], cwd=repository).decode().split('\0')
    result = hashlib.sha256()
    for filename in sorted(set(files)):
        if not filename:
            continue
        path = repository / filename
        if path.is_symlink() or not path.is_file():
            raise ValueError('source_file_invalid')
        result.update(filename.removeprefix(prefix).encode())
        result.update(b'\0')
        result.update(digest(path).encode())
        result.update(b'\n')
    return result.hexdigest()


def reusable_first_use(report_path, previous_artifacts, previous_driver, skills_repo, expected_digests):
    """复用独立通过且驱动／输入／制品均未变化的首用组；追加失败场景始终重新运行。"""
    baseline = json.loads(report_path.read_text())
    if baseline.get('skillSource', {}).get('digests') != expected_digests or digest(previous_driver) != baseline.get('driverSha256'):
        raise ValueError('reuse_source_or_driver_mismatch')
    def runner(source):
        tree = ast.parse(source)
        return [ast.dump(node, include_attributes=False) for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in ('child', 'load', 'digest', 'hashes')
                or isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'CASES' for target in node.targets)]
    if runner(previous_driver.read_text()) != runner(Path(__file__).read_text()):
        raise ValueError('reuse_runner_changed')
    cases = baseline.get('cases', [])
    if len(cases) != len(CASES) or {c.get('case') for c in cases} != {c[0] for c in CASES}:
        raise ValueError('reuse_case_inventory_mismatch')
    for case in CASES:
        receipt = next(c for c in cases if c['case'] == case[0])
        if receipt.get('status') != 'PASS' or type(receipt.get('tests')) is not int or receipt['tests'] < 1 or any(receipt.get(k) != 0 for k in ('failures', 'errors', 'skipped')):
            raise ValueError('reuse_case_not_passed')
        if receipt.get('driverSha256') != digest(skills_repo / 'tests' / (case[1] + '.py')):
            raise ValueError('reuse_test_driver_changed')
    if not baseline.get('artifacts'):
        raise ValueError('reuse_artifacts_missing')
    for name, reference in baseline['artifacts'].items():
        path = previous_artifacts / name
        if path.is_symlink() or not path.resolve().is_relative_to(previous_artifacts.resolve()) or not path.is_file() or digest(path) != reference.get('sha256'):
            raise ValueError('reuse_artifact_changed_or_escaping')
    return [{**case, 'reused': True} for case in cases]


def child(args):
    """仅替换测试临时目录的清理方式；原有业务断言及冷安装不变。"""
    name, module_name, cls, flag, installed_key, skill = next(c for c in CASES if c[0] == args.case)
    os.environ['CRAFT_' + flag] = '1'
    if installed_key:
        os.environ['CRAFT_' + installed_key] = str(args.installed / 'skills' / skill)
    os.environ['CRAFT_RUNTIME_HOME'] = str(args.artifacts / 'native-runtime')
    sys.path.insert(0, str(args.skills_repo / 'tests'))
    module = load(args.skills_repo / 'tests' / (module_name + '.py'), 'fixed_' + module_name)
    if name == 'optimization':
        module.ROOT = args.installed
    class RetainedDirectory:
        def __init__(self, *unused, **options):
            self.path = tempfile.mkdtemp(prefix=options.get('prefix', name + '-'), dir=args.artifacts)
        def __enter__(self):
            return self.path
        def __exit__(self, *unused):
            return False
    module.tempfile = SimpleNamespace(TemporaryDirectory=RetainedDirectory)
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(getattr(module, cls))
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    reply = {'case': name, 'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors), 'skipped': len(result.skipped), 'log': stream.getvalue()}
    (args.artifacts / (name + '-test.json')).write_text(json.dumps(reply, ensure_ascii=False, indent=2) + '\n')
    print(stream.getvalue(), flush=True)
    return int(not result.wasSuccessful() or bool(result.skipped))


def extra_cases(installed, root):
    """使用当前安装脚本执行新增场景，记录实际保存、拒绝、重开与源保全。"""
    from PIL import Image
    workflow = load(installed / 'skills/photocraft-use/scripts/workflow.py', 'fixed_workflow')
    records = []
    root.mkdir()
    def execute(plan, name, source=None):
        plan_file = root / (name + '.json')
        plan_file.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n')
        before = hashes(source) if source else None
        manifest = workflow.execute(plan, root / name, source=source)
        assert source is None or before == hashes(source), 'source_changed'
        native = workflow.load_module('native_verify').verify(root / name, Path.home() / '.local/share/craft-runtimes')
        assert native['result'] == 'PASS'
        records.append({'case': name, 'result': 'PASS', 'nativeProjectSha256': manifest['files']['project.pcraft'], 'manifestSha256': digest(root / name / 'manifest.json'), 'freshNativeReopen': native, 'sourceUnchanged': source is None or before == hashes(source)})
        return manifest
    def reject(plan, name, pattern, source=None):
        before = hashes(source) if source else None
        try:
            execute(plan, name, source)
        except ValueError as error:
            assert pattern in str(error), str(error)
            target = root / name
            assert not (target / 'manifest.json').exists(), 'failed_case_published'
            assert source is None or before == hashes(source), 'source_changed'
            failure = target / 'failure.json'
            if failure.exists():
                receipt = json.loads(failure.read_text())
                assert receipt['replayAllowed'] is False
            records.append({'case': name, 'result': 'PASS', 'observedError': str(error), 'successfulDeliveryAbsent': True, 'sourceUnchanged': source is None or before == hashes(source), 'failureReceipt': digest(failure) if failure.exists() else None})
        else:
            raise AssertionError('expected_rejection: ' + name)
    background = root / 'background.png'
    image = Image.new('RGBA', (64, 64))
    image.putdata([(180 if (x // 4 + y // 4) % 2 else 60, 100, 140, 255) for y in range(64) for x in range(64)])
    image.save(background)
    product = root / 'product.png'
    Image.new('RGBA', (16, 16), (230, 20, 30, 255)).save(product)
    initial = {'document': {'width': 64, 'height': 64, 'background': '#ffffff'}, 'minimumLayers': 4,
               'assets': {key: {'path': str(path), 'sha256': digest(path)} for key, path in [('background', background), ('product', product)]},
               'operations': [{'command': 'asset.place', 'params': {'asset': 'background', 'center': [32, 32]}, 'as': 'background'},
                              {'command': 'asset.place', 'params': {'asset': 'product', 'center': [32, 32]}, 'as': 'product'},
                              {'command': 'type.create', 'params': {'x': 8, 'y': 16, 'text': '标题A', 'font': 'Songti SC', 'size': 8, 'tracking': 10}, 'as': 'title'},
                              {'command': 'native.command', 'params': {'command': 'layer.groupLayers', 'params': {'layer': {'$ref': 'title.layer'}, 'name': 'Nested title'}}}],
               'exports': [{'format': 'png'}, {'format': 'psd'}]}
    first = execute(initial, 'nested-source')
    source = root / 'nested-source'
    title = first['bindings']['title']['layer']
    objects = workflow.load_module('domain_assertions').index(json.loads((source / 'native.json').read_text()))
    assert objects[str(title)]['_parent'] is not None
    revision = {'expectedProjectSha256': first['files']['project.pcraft'], 'operations': [{'command': 'type.edit', 'params': {'layer': title, 'text': '新款A'}}], 'preserveObjects': {str(title): ['text.text', 'bounds']}, 'assertions': [{'layer': title, 'kind': 'Type', 'font': 'Songti SC', 'size': 8, 'tracking': 10, 'leading': 'auto', 'lineCount': 1}], 'exports': [{'format': 'png'}, {'format': 'psd'}]}
    second = execute(revision, 'nested-title-revision', source)
    execute({'expectedProjectSha256': second['files']['project.pcraft'], 'operations': [{'command': 'type.edit', 'params': {'layer': title, 'text': '再次A'}}], 'preserveObjects': {str(title): ['text.text', 'bounds']}, 'exports': [{'format': 'png'}]}, 'nested-second-edit', root / 'nested-title-revision')
    reject({'document': {'width': 32, 'height': 32, 'background': '#ffffff'}, 'operations': [], 'minimumLayers': 3, 'exports': [{'format': 'png'}]}, 'flat-preview-not-editable', 'editable_layer_gate_failed')
    for metric in ['noOverflow', 'glyphCoverage']:
        reject({**revision, 'operations': [], 'assertions': [{'layer': title, metric: True}]}, metric + '-unknown', 'layout_metric_unavailable', source)
    reject({**revision, 'operations': [{'command': 'layer.renameLayer', 'params': {'layer': first['bindings']['product']['layer'], 'name': 'unauthorized'}}]}, 'non-target-change', 'object_changed', source)
    roles = {'background': first['bindings']['background']['layer'], 'product': first['bindings']['product']['layer'], 'text': title}
    variant = {'expectedProjectSha256': first['files']['project.pcraft'], 'operations': [{'command': 'image.canvasSize', 'params': {'width': 80, 'height': 80, 'anchor': 'center'}}], 'variant': {'width': 80, 'height': 80, 'safeArea': [0, 0, 80, 80], 'roles': roles}, 'exports': [{'format': 'png'}, {'format': 'psd'}]}
    execute(variant, 'nested-padding', source)
    reject({**variant, 'variant': {**variant['variant'], 'safeArea': [0, 0, 8, 8]}}, 'unsafe-nested-variant', 'variant_safe_area_violation', source)
    reject({**variant, 'variant': {**variant['variant'], 'roles': {**roles, 'product': title}}}, 'duplicate-roles', 'variant_role_identity', source)
    reject({**variant, 'operations': [], 'variant': {**variant['variant'], 'width': 64, 'height': 64, 'safeArea': [0, 0, 64, 64]}}, 'unverified-transform', 'variant_geometry_required', source)
    target = roles['background']
    selection = {'command': 'select.rect', 'params': {'x': 0, 'y': 48, 'width': 16, 'height': 16, 'antiAlias': False, 'feather': 0}}
    for name, command, params in [('blur', 'filter.blur.gaussianBlur', {'radius': 1.5}), ('grain', 'filter.noise.addNoise', {'amount': 12, 'seed': 4}), ('sharpen', 'filter.sharpen.sharpen', {})]:
        plan = {'expectedProjectSha256': first['files']['project.pcraft'], 'operations': [{'command': 'layer.select', 'params': {'layer': target}}, selection, {'command': 'native.command', 'params': {'command': command, 'params': params}}, {'command': 'select.deselect', 'params': {}}], 'filterContract': {'target': target, 'method': 'raster', 'selection': True, 'mask': False, 'region': [0, 48, 16, 16]}, 'protectedRegions': [{'id': 'product', 'rect': [24, 24, 16, 16]}, {'id': 'title', 'rect': [4, 0, 44, 20]}], 'preserveObjects': {}, 'exports': [{'format': 'png'}, {'format': 'psd'}]}
        execute(plan, 'selected-' + name, source)
        observation = json.loads((root / ('selected-' + name) / 'filter-contract.json').read_text())
        assert observation['steps'][0]['context']['editable'] is False
        assert observation['steps'][0]['pixels']['changedPixels'] > 0
        for field, value in [('target', roles['product']), ('selection', False), ('mask', True), ('method', 'smart')]:
            reject({**plan, 'filterContract': {**plan['filterContract'], field: value}}, name + '-wrong-' + field, 'filter_editability_unverified' if field == 'method' else 'filter_context_mismatch', source)
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-repo', required=True, type=Path)
    parser.add_argument('--installed', required=True, type=Path)
    parser.add_argument('--artifacts', required=True, type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--case', choices=[c[0] for c in CASES])
    parser.add_argument('--reuse-first-use', type=Path)
    parser.add_argument('--previous-artifacts', type=Path)
    parser.add_argument('--previous-driver', type=Path)
    args = parser.parse_args()
    args.skills_repo = args.skills_repo.resolve()
    args.installed = args.installed.resolve()
    args.artifacts = args.artifacts.resolve()
    if args.case:
        return child(args)
    if not args.report:
        parser.error('--report required')
    vendor = load(ROOT / 'scripts/vendor/skill_vendor.py', 'fixed_vendor')
    lock = json.loads((args.installed / 'skills.lock.json').read_text())['sources'][0]
    # 原生执行前确认真正固定的安装资源与当前技能源一致，不手改安装目录。
    before = {name: vendor.hash_skill_dir(args.installed / 'skills' / name) for name in lock['skills']}
    if before != lock['sha256'] or any(authored_skill_hash(args.skills_repo, name) != value for name, value in before.items()):
        raise ValueError('fixed_source_identity_mismatch')
    reused = None
    if args.reuse_first_use:
        if not args.previous_artifacts or not args.previous_driver:
            parser.error('reuse requires --previous-artifacts and --previous-driver')
        reused = reusable_first_use(args.reuse_first_use, args.previous_artifacts.resolve(), args.previous_driver, args.skills_repo, before)
    args.artifacts.mkdir(parents=True, exist_ok=False)
    report = {'schema': 'photocraft-fixed-domain-acceptance/v1', 'status': 'RUNNING', 'startedAt': datetime.now(timezone.utc).isoformat(), 'pluginVersion': json.loads((args.installed / 'plugin.json').read_text())['version'], 'skillSource': {'ref': lock['ref'], 'sha': lock['sha'], 'digests': before}, 'platform': os.uname().sysname + '-' + os.uname().machine, 'driverSha256': digest(__file__), 'cases': [], 'excluded': ['independent creative acceptance', 'external PSD editor compatibility', 'complete PSD fidelity', 'complete glyph coverage or exact overflow metrics', 'other platforms', 'all755 commands', 'full V1']}
    def save():
        text = json.dumps(report, ensure_ascii=False, indent=2).replace(str(args.artifacts), 'RETAINED_ARTIFACTS').replace(str(Path.home()), 'USER_HOME')
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text + '\n')
    save()
    if reused is not None:
        report['cases'] = reused
        report['reuse'] = {'scope': 'independently passed first-use cases only; all additional native cases rerun', 'baselineFile': args.reuse_first_use.name, 'baselineSha256': digest(args.reuse_first_use), 'previousDriverSha256': digest(args.previous_driver), 'runnerAstUnchanged': True, 'testDriversUnchanged': True, 'retainedArtifactsUnchanged': True}
        save()
    for case in [] if reused is not None else CASES:
        name = case[0]
        workspace = args.artifacts / name
        workspace.mkdir()
        command = [sys.executable, '-I', '-B', str(Path(__file__).resolve()), '--skills-repo', str(args.skills_repo), '--installed', str(args.installed), '--artifacts', str(workspace), '--case', name]
        result = subprocess.run(command, capture_output=True, text=True, timeout=900)
        receipt = workspace / (name + '-test.json')
        item = json.loads(receipt.read_text()) if receipt.is_file() else {'case': name, 'log': result.stdout + result.stderr}
        item['driverSha256'] = digest(args.skills_repo / 'tests' / (case[1] + '.py'))
        item['status'] = 'PASS' if result.returncode == 0 else 'FAIL'
        item['retainedDirectory'] = name
        report['cases'].append(item)
        save()
        print(name + ' ' + item['status'], flush=True)
    try:
        report['additionalNativeCases'] = extra_cases(args.installed, args.artifacts / 'additional')
    except Exception as error:
        report['additionalError'] = str(error)
    after = {name: vendor.hash_skill_dir(args.installed / 'skills' / name) for name in lock['skills']}
    report['installedSkillsUnchanged'] = before == after
    # 仅列验收产物；运行时、复制的技能和缓存不混入工程证据。
    report['artifacts'] = {}
    for path in sorted(args.artifacts.rglob('*')):
        if not path.is_file() or path.suffix not in ('.pcraft', '.psd', '.png', '.json'):
            continue
        parts = path.relative_to(args.artifacts).parts
        if any(part in ('scripts', 'references', 'examples', 'empty-runtime', 'fresh-runtime', 'native-runtime', 'runtime', 'fresh runtime') for part in parts):
            continue
        report['artifacts']['/'.join(parts)] = {'sha256': digest(path), 'bytes': path.stat().st_size}
    report['finishedAt'] = datetime.now(timezone.utc).isoformat()
    report['status'] = 'PASS' if report['installedSkillsUnchanged'] and all(c['status'] == 'PASS' for c in report['cases']) and 'additionalError' not in report else 'FAIL'
    save()
    print(report['status'], flush=True)
    return int(report['status'] != 'PASS')


if __name__ == '__main__':
    raise SystemExit(main())
