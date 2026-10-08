#!/usr/bin/env python3
"""固定安装的单技能路由／资源与真实代表任务验收；模型派发另行验证。"""
import argparse,hashlib,importlib.util,json,os,re,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hashes(root):return {p.relative_to(root).as_posix():sha(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts}
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def verify(installed,source,out):
 installed=installed.resolve();source=source.resolve();out=out.resolve();out.mkdir(parents=True,exist_ok=False);before=hashes(installed);source_before=hashes(source);lock=json.loads((installed/'skills.lock.json').read_text())['sources'][0];suite=json.loads((source/'skill-suite.json').read_text());assert len(lock['skills'])==13
 env={k:v for k,v in os.environ.items() if not k.startswith(('CRAFT_','PHOTOCRAFT_'))};env.update(PYTHONDONTWRITEBYTECODE='1',PATH='/usr/bin:/bin')
 def run(argv,cwd=out):
  r=subprocess.run(argv,cwd=cwd,env=env,capture_output=True,text=True,timeout=600);assert r.returncode==0,r.stdout+r.stderr;return r.stdout
 vendor=load(installed/'scripts/vendor/skill_vendor.py','route_acceptance_vendor');skills=[];routes=[]
 for name in lock['skills']:
  actual=installed/'skills'/name;assert vendor.hash_skill_dir(actual)==lock['sha256'][name];assert vendor.hash_skill_dir(source/'skills'/name)==lock['sha256'][name]
  home=out/'single'/name/'only-skill';home.parent.mkdir(parents=True);shutil.copytree(actual,home);runtime=home.parent/'empty-runtime';assert not runtime.exists();assert list(home.parent.iterdir())==[home]
  for p in home.rglob('*.md'):
   text=p.read_text()
   if p.name=='SKILL.md':assert len(text.splitlines())<500
   for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
    if '://' in target or target.startswith('#'):continue
    target=(p.parent/target.split('#')[0]).resolve();assert target.is_relative_to(home) and target.is_file(),(name,str(target))
  contract=(home/'references/scenario-contract.md').read_text();assert all(word in contract for word in ['输入与前置','修改与副作用','保护范围','输出','恢复','验收','不适用'])
  for filename in ['happy-path.md','failure-recovery.md','boundary-refusal.md']:assert (home/'examples'/filename).is_file()
  start=hashes(home);version=run([sys.executable,'-I','-B',str(home/'scripts/cli.py'),'--runtime-home',str(runtime),'--','--version']);runtime_lock=json.loads((home/'scripts/runtime.lock.json').read_text());assert runtime_lock['artifacts']['darwin-arm64']['versionOutput'] in version
  rows=json.loads(run([sys.executable,'-I','-B',str(home/'scripts/cli.py'),'--runtime-home',str(runtime),'--','commands','--json']));ids={r['id']for r in rows};assert {r['id']for r in json.loads((home/'references/commands.json').read_text())['commands']}.issubset(ids)
  for intent,expected in [('query_commands',['photocraft-cli']),('edit_text',['photocraft-cli-text']),('filter_background',['photocraft-cli-filters']),('export',['photocraft-cli-export'])]:
   value=json.loads(run([sys.executable,'-I','-B',str(home/'scripts/route.py'),intent]));assert value['skills']==expected and value['hostModelRouting']=='NOT_RUN';routes.append(dict(skill=name,intent=intent,skills=value['skills']))
  value=json.loads(run([sys.executable,'-I','-B',str(home/'scripts/route.py'),'edit_text','--outcome','unknown']));assert value['action']=='reconcile' and value['skills']==[] and not value['replayAllowed']
  value=json.loads(run([sys.executable,'-I','-B',str(home/'scripts/route.py'),'poster','--skill','photocraft-cli']));assert value['skills']==['photocraft-cli']
  value=json.loads(run([sys.executable,'-I','-B',str(home/'scripts/route.py'),'poster','--completed','photocraft-cli-project','--completed','photocraft-cli-layers']));assert value['skills']==['photocraft-cli-text','photocraft-cli-export'];assert hashes(home)==start
  skills.append(dict(name=name,installedSha256=lock['sha256'][name],coldPublicRuntime=True,runtimeSha256=sha(runtime/'photocraft'/runtime_lock['resolvedVersion']/'photocraft-cli'),registeredCommands=len(rows),isolatedSkillUnchanged=True,documentationAndExamples=True,unknownNoEdit=True,explicitCliPreserved=True,reusesCompletedPrerequisites=True))
  print('PASS cold standalone '+name,flush=True)
 # 现有领域业务断言运行在实际安装资源上；输入、产物在自有目录留存。
 os.environ.update(CRAFT_TASK_FIRST_USE='1',CRAFT_NATIVE_WORKFLOW_FIRST_USE='1',CRAFT_INSTALLED_NATIVE_WORKFLOW_SKILL=str(installed/'skills/photocraft-use'),CRAFT_NATIVE_WORKFLOW_REPORT=str(out/'use-workflow.json'),PYTHONDONTWRITEBYTECODE='1')
 tasks=load(source/'tests/test_task_skill_first_use.py','fixed_route_task_tests');tasks.ROOT=installed;observed=[]
 original_install=tasks.TaskSkillFirstUseTests.install_only
 def install_only(case,task):
  original_install(case,task);case.fixed_skill_name=case.skill.name;assert not case.runtime.exists();assert vendor.hash_skill_dir(case.skill)==lock['sha256'][case.skill.name]
 tasks.TaskSkillFirstUseTests.install_only=install_only
 def retained(case):
  target=out/'representative'/case._testMethodName;target.mkdir(parents=True);entries={}
  for p in sorted(case.root.rglob('*')):
   if not p.is_file() or p.is_relative_to(case.runtime) or p.is_relative_to(case.skill):continue
   name=p.relative_to(case.root).as_posix();dest=target/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest);entries[name]=sha(p)
  observed.append(dict(test=case._testMethodName,skill=case.fixed_skill_name,files=entries,sourceProjectSha256=sha(case.project),sourceUnchanged=sha(case.project)==case.project_sha))
 tasks.TaskSkillFirstUseTests.tearDown=retained
 workflow=load(source/'tests/test_native_workflow_first_use.py','fixed_route_use_tests');tests=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(tasks),unittest.defaultTestLoader.loadTestsFromModule(workflow)]);result=unittest.TextTestRunner(verbosity=2).run(tests);assert result.wasSuccessful() and not result.skipped and result.testsRun==13;assert len(observed)==10 and all(x['sourceUnchanged'] for x in observed)
 # 公共CLI的原合法完整命令计划仍可执行。
 cli=out/'single/photocraft-cli/only-skill';reply=json.loads(run([sys.executable,'-I','-B',str(cli/'scripts/commands.py'),'run',str(cli/'examples/commands-advanced.json'),'--output',str(out/'cli-plan'),'--runtime-home',str(cli.parent/'empty-runtime')]));assert reply['result']=='PASS' and all(x.get('phase')=='reply_validated' for x in reply['steps'])
 # 发行检查拒绝缺少失败示例、场景合同变化及生成执行器漂移。
 drift=out/'drift-source';shutil.copytree(source,drift);negative=[]
 for relative in ['skills/photocraft-cli-text/examples/failure-recovery.md','skills/photocraft-cli-text/references/scenario-contract.md','skills/photocraft-cli-text/scripts/commands.py']:
  p=drift/relative;original=p.read_bytes();p.write_bytes(original+b'\ntest-only drift\n')
  if p.name=='failure-recovery.md':p.unlink()
  r=subprocess.run([sys.executable,'-I','-B',str(drift/'scripts/sync_skill_suite.py'),'--check'],capture_output=True,text=True,env=env);assert r.returncode!=0 and 'skill_resource_drift' in r.stdout+r.stderr;assert relative.removeprefix('skills/') in r.stdout+r.stderr;negative.append(dict(path=relative,result='REFUSED',outputSha256=hashlib.sha256((r.stdout+r.stderr).encode()).hexdigest()));p.write_bytes(original)
 assert hashes(installed)==before and hashes(source)==source_before
 evidence=dict(schema='photocraft-fixed-routing-acceptance/v1',status='PASS',pluginVersion=json.loads((installed/'plugin.json').read_text())['version'],skillsRef=lock['ref'],skillsCommit=lock['sha'],platform='darwin-arm64',standalone=skills,staticRoutes=routes,representativeTests=observed,tests=dict(total=13,passed=13,skipped=0),cliOldPlan=True,useWorkflow=json.loads((out/'use-workflow.json').read_text()),driftRefusals=negative,installedTreeUnchanged=True,installedTreeSha256=hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest(),sourceTreeSha256=hashlib.sha256(json.dumps(source_before,sort_keys=True,separators=(',',':')).encode()).hexdigest(),driverSha256=sha(Path(__file__)),testDriverSha256={n:sha(source/'tests'/n) for n in ['test_task_skill_first_use.py','test_native_workflow_first_use.py']},retainedFiles={p.relative_to(out).as_posix():sha(p) for p in out.rglob('*') if p.is_file() and p.is_relative_to(out/'representative')},scope='Fixed public-tag installed resources, each skill alone with cold public runtime, deterministic intent queries and native representative tasks; actual natural-language host/model routing and full command execution remain NOT_RUN')
 # 回执保留身份而非本地临时绝对路径。
 text=json.dumps(evidence,ensure_ascii=False,indent=2).replace(str(out),'ACCEPTANCE_OUTPUT').replace(str(Path.home()),'USER_HOME').replace(str(Path(tempfile.gettempdir()).resolve()),'TEMPORARY_WORKSPACE').replace(tempfile.gettempdir(),'TEMPORARY_WORKSPACE');(out/'evidence.json').write_text(text+'\n');print(json.dumps({'status':'PASS','standalone':len(skills),'nativeRepresentativeTests':13,'driftRefusals':len(negative)}))
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--installed-plugin',type=Path,required=True);parser.add_argument('--skills-source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();verify(args.installed_plugin,args.skills_source,args.output)
