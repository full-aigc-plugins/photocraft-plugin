#!/usr/bin/env python3
"""候选或固定安装入口验收：真实保存后故障注入、无重放与新会话重开。"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(root):
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts}


# 仅观察公开 CLI，不改动被测安装；任何安装／会话尝试都会计数并立即失败。
PREFLIGHT_WRAPPER = '''import importlib.util,json,runpy,subprocess,sys,urllib.request
from pathlib import Path
script,counts,*args=sys.argv[1:];calls={'install':0,'session':0,'download':0}
def denied(key):
 def call(*a,**kw):
  calls[key]+=1;raise AssertionError('preflight side effect: '+key)
 return call
subprocess.Popen=denied('session');urllib.request.urlopen=denied('download')
original=importlib.util.spec_from_file_location
def observe(name,location,*a,**kw):
 spec=original(name,location,*a,**kw)
 if Path(location).name in ('bootstrap.py','desktop.py'):
  execute=spec.loader.exec_module
  def wrapped(module):
   execute(module)
   if hasattr(module,'install'):module.install=denied('install')
  spec.loader.exec_module=wrapped
 return spec
importlib.util.spec_from_file_location=observe;sys.argv=[script,*args]
try:runpy.run_path(script,run_name='__main__')
finally:Path(counts).write_text(json.dumps(calls))
'''


def preflight(scripts, tests, root):
    cases = load(tests / 'test_entry_contract.py', 'entry_contract_cases')
    wrapper = root / 'preflight-wrapper.py'; wrapper.write_text(PREFLIGHT_WRAPPER)
    records = []
    for entry in ('workflow', 'commands', 'desktop'):
        for name, text, path in cases.invalid_cases(entry):
            case = root / (entry + '-' + name); case.mkdir()
            plan = case / 'plan.json'; plan.write_text(text)
            marker = case / 'user.txt'; marker.write_text('保留已有用户内容')
            cache = case / 'runtime'; cache.mkdir(); (cache / 'user.txt').write_text('已有缓存不得改变')
            before = fingerprint(cache); counts = case / 'counts.json'
            args = [sys.executable, '-I', '-B', str(wrapper), str(scripts / (entry + '.py')), str(counts)]
            if entry != 'workflow': args += ['run']
            args += [str(plan), '--output', str(case / 'output'), '--runtime-home', str(cache)]
            result = subprocess.run(args, capture_output=True, text=True, timeout=30)
            assert result.returncode == 1, result.stdout + result.stderr
            reply = json.loads(result.stdout)
            assert all(key in reply for key in ('code', 'phase', 'outcome', 'retryable', 'recoveryAction'))
            assert reply['phase'] == 'validation' and reply['outcome'] == 'not_executed'
            assert reply['category'] == 'validation_failed' and reply['fieldPath'] == path, reply
            calls = json.loads(counts.read_text()); assert not any(calls.values()), calls
            assert fingerprint(cache) == before and marker.read_text() == '保留已有用户内容'
            assert sorted(p.name for p in case.iterdir()) == ['counts.json', 'plan.json', 'runtime', 'user.txt']
            records.append({'entry': entry, 'case': name, 'inputSha256': sha(plan), 'fieldPath': path,
                            'code': reply['code'], 'calls': calls, 'userAndCacheUnchanged': True,
                            'outputAndRecoveryAbsent': True})
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill-root', required=True, type=Path)
    parser.add_argument('--tests-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--scope', required=True, choices=['candidate', 'fixed-installed'])
    args = parser.parse_args()
    skill = args.skill_root.resolve(); tests = args.tests_root.resolve(); root = args.output.resolve()
    if root.is_relative_to(skill) or root.is_relative_to(tests):
        parser.error('output must be outside the skill and test source')
    root.mkdir(parents=True, exist_ok=False); before = fingerprint(skill); scripts = skill / 'scripts'
    report = {'schema': 'photocraft-entry-contract-acceptance/v1', 'status': 'RUNNING',
              'scope': args.scope, 'platform': 'darwin-arm64', 'driverSha256': sha(Path(__file__)),
              'skillFilesSha256': hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest(),
              'testResources': {name: sha(tests / name) for name in ['test_entry_contract.py', 'fixtures/protocol_proxy.py']},
              'preflight': [], 'native': [], 'fullV1': 'INCOMPLETE', 'creativeAcceptance': 'NOT_RUN'}
    def save(): (root / 'evidence.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    save(); report['preflight'] = preflight(scripts, tests, root); save()
    print('Preflight PASS ' + str(len(report['preflight'])), flush=True)
    runtime = root / 'runtime'
    bootstrap = load(scripts / 'bootstrap.py', 'entry_bootstrap')
    lock = json.loads((scripts / 'runtime.lock.json').read_text())
    installed = bootstrap.install(lock, runtime)
    report['runtime'] = {key: installed[key] for key in ['binarySha256', 'runtimeIdentity']}; save()
    faults = ['malformed', 'scalar', 'missing', 'ambiguous', 'nonfinite', 'duplicate', 'overflow',
              'tool-content', 'inner-duplicate', 'inner-nonfinite', 'inner-overflow', 'inner-ambiguous',
              'inner-semantic-error', 'explicit-tool-error']
    for entry in ('workflow', 'commands', 'desktop'):
        for fault in ['none', 'dynamic-missing', *faults]:
            case = root / ('native-' + entry + '-' + fault); case.mkdir()
            output = case / 'output'; log = case / 'saves.jsonl'; capture = case / 'proxy-capture.pcraft'
            commands = load(scripts / 'commands.py', 'entry_commands')
            transport = load(scripts / 'mcp_session.py', 'entry_transport')
            if fault not in ('none', 'dynamic-missing'):
                base = transport.Session
                class Observed(base):
                    def __init__(self, argv, *pos, **kw):
                        super().__init__([sys.executable, '-I', '-B', str(tests / 'fixtures/protocol_proxy.py'),
                                          fault, str(log), str(capture), *argv], *pos, **kw)
                transport.Session = Observed
            dynamic = fault == 'dynamic-missing'
            if entry == 'workflow':
                plan = {'document': {'name': 'Entry contract', 'width': 32, 'height': 32},
                        'operations': [{'command': 'shape.create', 'params': {'shape': 'rectangle', 'rect': [2, 2, 8, 8], 'name': 'Legacy shape'}},
                                       {'command': 'layer.new.layer', 'params': {'name': 'Keep'}, 'as': 'keep'},
                                       {'command': 'layer.renameLayer', 'params': {'layer': {'$ref': 'keep.layer'}, 'name': 'Accepted'}}],
                        'exports': []}
                if dynamic:
                    source = root / 'native-workflow-none/output'
                    source_manifest = json.loads((source / 'manifest.json').read_text())
                    plan = {'expectedProjectSha256': source_manifest['files']['project.pcraft'], 'operations': [
                        {'command': 'layer.new.layer', 'params': {'name': 'Dynamic'}, 'as': 'fresh'},
                        {'command': 'layer.select', 'params': {'layer': {'$ref': 'fresh.absent'}}}], 'exports': []}
                workflow = load(scripts / 'workflow.py', 'entry_workflow'); old = workflow.load_module
                workflow.load_module = lambda name: transport if name == 'mcp_session' else old(name)
                try:
                    receipt = workflow.execute(plan, output, runtime, source if dynamic else None)
                    assert fault == 'none'
                except (ValueError, RuntimeError) as error:
                    assert fault != 'none', str(error)
                    receipt = json.loads((output / 'failure.json').read_text())
                project_root = output if fault == 'none' else (output / receipt['stage']).resolve()
                project = project_root / ('source.pcraft' if dynamic else 'project.pcraft')
                steps = json.loads((output / 'operations.json').read_text()) if fault == 'none' else json.loads((project_root / 'recovery-operations.json').read_text())
                if fault not in ('none', 'dynamic-missing'):
                    assert receipt['lastAttempt']['tool'] == 'doc_save' and receipt['lastAttempt']['phase'] == 'submitted'
                    assert all(s['tool'] != 'doc_save' for s in steps)
                    assert not receipt['replayAllowed'] and not (output / 'manifest.json').exists()
            else:
                plan = {'schema': 'craft-command-plan/v1', 'operations': [
                    {'tool': 'doc_new', 'params': {'width': 32, 'height': 32}},
                    {'command': 'layer.new.layer', 'params': {'name': 'Keep'}, 'as': 'keep'},
                    {'tool': 'doc_save', 'params': {'path': {'$output': 'checkpoint.pcraft'}}, 'as': 'saved'},
                    {'command': 'layer.renameLayer', 'params': {'layer': {'$ref': 'keep.absent' if dynamic else 'keep.layer'}, 'name': 'After save'}},
                    {'tool': 'doc_save', 'params': {'path': {'$output': 'final.pcraft'}}},
                    {'tool': 'doc_render_preview', 'params': {}}]}
                if entry == 'commands':
                    receipt = commands.execute(plan, output, runtime, session_factory=transport.Session)
                else:
                    desktop = load(scripts / 'desktop_session.py', 'entry_desktop'); old = desktop.load
                    desktop.load = lambda name: transport if name == 'mcp_session' else commands if name == 'commands' else old(name)
                    receipt = desktop.run(plan, output, runtime)
                    life = json.loads((output / 'desktop-session.json').read_text())
                    assert life['ownedProcessesStopped'] and life['listenerOwnedByPID'] and life['sessionsStarted'] == 1
                project = output / 'checkpoint.pcraft'; steps = receipt['steps']
                if fault == 'none':
                    assert receipt['result'] == 'PASS' and all(s['phase'] == 'reply_validated' for s in steps)
                    assert (output / 'final.pcraft').exists()
                    image = steps[-1]['result']['content'][0]; assert image['type'] == 'image'
                    from PIL import Image
                    with Image.open(output / image['path']) as img:
                        img.load(); rendered_size = list(img.size)
                        assert img.width > 0 and img.height > 0
                        if entry == 'commands': assert img.size == (32, 32)
                else:
                    assert not (output / 'success.json').exists() and not (output / 'final.pcraft').exists()
                    assert len(steps) == 3
                    if not dynamic:
                        assert steps[-1]['phase'] == 'submitted' and 'result' not in steps[-1]
            (case / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n')
            assert project.is_file(), (entry, fault, receipt)
            project_sha = sha(project)
            # 新的真实原生会话只读重开原工程；代理捕获从不作为恢复输入。
            with load(scripts / 'mcp_session.py', 'reopen_transport').Session(
                    [installed['executable'], 'mcp', '--automation-read-root', str(project.parent),
                     '--automation-write-root', str(project.parent)]) as session:
                commands.parse_reply(session.request('tools/call', {'name': 'doc_open', 'arguments': {'path': project.name}}))
                native = commands.parse_reply(session.request('tools/call', {'name': 'doc_inspect', 'arguments': {}}))
            assert native['width'] == native['height'] == 32 and sha(project) == project_sha
            assert any(l['name'] == ('Accepted' if entry == 'workflow' else 'Keep') for l in native['layers'])
            row = {'entry': entry, 'fault': fault, 'inputSha256': sha(case / 'plan.json'), 'projectSha256': project_sha,
                   'freshNativeReopen': True, 'originalProjectUnchanged': True, 'completedReceipts': len(steps),
                   'ownedProcessesStopped': entry != 'desktop' or life['ownedProcessesStopped']}
            if fault not in ('none', 'dynamic-missing'):
                saves = [json.loads(s) for s in log.read_text().splitlines()]; assert len(saves) == 1
                assert saves[0]['saveSucceeded'] and saves[0]['sha256'] == project_sha
                requests = [json.loads(s) for s in Path(str(log) + '.requests.jsonl').read_text().splitlines()]
                calls = [s['params'] for s in requests if s['method'] == 'tools/call']
                save_index = next(i for i, s in enumerate(calls) if s['name'] == 'doc_save')
                assert calls[save_index + 1:] == [], calls[save_index + 1:]
                details = receipt if entry == 'workflow' else receipt['errorDetails']
                known = fault in ('inner-semantic-error', 'explicit-tool-error')
                assert details['outcome'] == ('failed' if known else 'outcome_unknown' if entry == 'workflow' else 'unknown'), details
                assert details['phase'] == 'submitted' and not details['retryable']
                # 同一输出的重复请求必须在会话／编辑之前拒绝；未知结果不被重放。
                saved_trace = Path(str(log) + '.requests.jsonl').read_bytes()
                try:
                    if entry == 'workflow': workflow.execute(plan, output, runtime)
                    elif entry == 'commands': commands.execute(plan, output, runtime, session_factory=transport.Session)
                    else: desktop.run(plan, output, runtime)
                except ValueError as error: assert 'output_exists' in str(error)
                else: raise AssertionError('same output replayed')
                assert Path(str(log) + '.requests.jsonl').read_bytes() == saved_trace and sha(project) == project_sha
                row.update(nativeSaveCount=1, laterCalls=0, replayCalls=0, structuredError={key: details[key] for key in ['code', 'phase', 'outcome', 'retryable', 'recoveryAction']})
            if dynamic:
                assert len(steps) >= (2 if entry == 'workflow' else 3) and 'unresolved_reference' in receipt['error']
                row.update(dynamicFieldNotGuessed=True, missingFieldStopsBeforeUse=True)
            if entry != 'workflow' and fault == 'none':
                revision_plan = {'schema': 'craft-command-plan/v1', 'operations': [
                    {'tool': 'doc_open', 'params': {'path': {'$ref': 'source.path'}}},
                    {'tool': 'doc_inspect', 'params': {}, 'as': 'opened'},
                    {'command': 'layer.renameLayer', 'params': {'layer': {'$ref': 'opened.activeLayer'}, 'name': 'Revised'}},
                    {'tool': 'doc_save', 'params': {'path': {'$output': 'revision.pcraft'}}}]}
                revised_output = case / 'revision'
                if entry == 'commands':
                    revision_receipt = commands.execute(revision_plan, revised_output, runtime, inputs={'source': str(project)})
                else:
                    revision_receipt = desktop.run(revision_plan, revised_output, runtime, inputs={'source': str(project)})
                    revision_life = json.loads((revised_output / 'desktop-session.json').read_text())
                    assert revision_life['ownedProcessesStopped'] and revision_life['listenerOwnedByPID']
                assert revision_receipt['result'] == 'PASS' and sha(project) == project_sha
                with load(scripts / 'mcp_session.py', 'revision_reopen').Session(
                    [installed['executable'], 'mcp', '--automation-read-root', str(revised_output),
                     '--automation-write-root', str(revised_output)]) as session:
                    commands.parse_reply(session.request('tools/call', {'name': 'doc_open', 'arguments': {'path': 'revision.pcraft'}}))
                    changed = commands.parse_reply(session.request('tools/call', {'name': 'doc_inspect', 'arguments': {}}))
                assert any(layer['name'] == 'Revised' for layer in changed['layers'])
                row.update(sourceInputBindingsReused=True, sourceDeliveryUnchanged=True, revisionProjectSha256=sha(revised_output / 'revision.pcraft'),
                           renderedImageDimensions=rendered_size, previewScope='document' if entry == 'commands' else 'owned application window')
            if entry == 'workflow' and fault == 'none':
                source_before = fingerprint(output)
                revision = {'expectedProjectSha256': receipt['files']['project.pcraft'],
                            'operations': [{'command': 'layer.renameLayer', 'params': {'layer': {'$ref': 'keep.layer'}, 'name': 'Revised'}}], 'exports': []}
                revised = case / 'revision'; result = workflow.execute(revision, revised, runtime, output)
                assert fingerprint(output) == source_before and result['files']['project.pcraft'] != receipt['files']['project.pcraft']
                row.update(legalLegacyShapeParameterAccepted=True, sourceManifestBindingsReused=True, sourceDeliveryUnchanged=True, revisionProjectSha256=result['files']['project.pcraft'])
            report['native'].append(row); save(); print(entry + ' ' + fault + ' PASS', flush=True)
    assert fingerprint(skill) == before
    report.update(status='PASS', skillUnchanged=True, nativeCases=len(report['native']), preflightCases=len(report['preflight']),
                  injectionScope='Test-only stdio proxy replaces replies only after native save succeeds; fixed clients and binaries unchanged. Not spontaneous native faults or full command acceptance.')
    save(); print(json.dumps({'status': report['status'], 'preflight': len(report['preflight']), 'native': len(report['native'])}))


if __name__ == '__main__': main()
