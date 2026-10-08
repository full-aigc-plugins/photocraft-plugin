#!/usr/bin/env python3
"""可重现的候选分层验证；不发布、不修改固定快照，不把本地通过升级为完整验收。"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]

def fingerprint(root):
 names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=root).decode().split('\0')
 files={}
 for name in sorted(set(names)):
  if not name or name=='project-status.json' or name.startswith(('docs/','openspec/','product-docs/')) or '__pycache__' in name:continue
  path=root/name
  if path.is_file():files[name]=hashlib.sha256(path.read_bytes()).hexdigest()
 return {'sha256':hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'files':files}

def reusable_skills_check(baseline,current,args):
 if baseline.get('schema')!='photocraft-candidate-validation/v1' or baseline.get('status') not in ('PASS','FAIL') or baseline.get('sourceUnchanged') is not True:raise ValueError('reuse_unverified_baseline')
 # 整体失败仅允许复用独立通过的技能检查，且必须保留另一个失败检查的证据。
 if baseline['status']=='FAIL' and not any(item.get('name')!='skills-tests' and item.get('status')=='FAIL' and isinstance(item.get('exitCode'),int) and item['exitCode']!=0 for item in baseline.get('checks',[])):raise ValueError('reuse_unverified_baseline')
 if baseline.get('source',{}).get('skills')!=current:raise ValueError('reuse_source_mismatch')
 if any(baseline.get('layers',{}).get(key) is not getattr(args,key) for key in ('native','desktop')):raise ValueError('reuse_layer_mismatch')
 checks=[item for item in baseline.get('checks',[])if item.get('name')=='skills-tests']
 if len(checks)!=1 or checks[0].get('status')!='PASS' or checks[0].get('exitCode')!=0:raise ValueError('reuse_missing_skills_pass')
 check=checks[0];tests=check.get('tests',{})
 if tests.get('failed')!=0 or not tests.get('total') or tests.get('passed',0)+tests.get('skipped',0)!=tests['total'] or args.native and tests.get('skipped')!=0:raise ValueError('reuse_incomplete_native_baseline')
 return check

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--skills-repo',required=True,type=Path);parser.add_argument('--output',required=True,type=Path);parser.add_argument('--native',action='store_true');parser.add_argument('--desktop',action='store_true');parser.add_argument('--reuse-skills-evidence',type=Path,help='Reuse only an exact-source, same-layer verified skills test run; all plugin and static checks rerun');args=parser.parse_args()
 if args.desktop and not args.native:parser.error('--desktop requires --native')
 skills=args.skills_repo.resolve();output=args.output.resolve();output.parent.mkdir(parents=True,exist_ok=True)
 before={'skills':fingerprint(skills),'plugin':fingerprint(ROOT)}
 reused=None;baseline=None
 if args.reuse_skills_evidence:
  baseline=json.loads(args.reuse_skills_evidence.read_text());reused=reusable_skills_check(baseline,before['skills'],args)
 report={'schema':'photocraft-candidate-validation/v1','startedAt':datetime.now(timezone.utc).isoformat(),'status':'RUNNING','scope':'source regression with pinned installed/downloaded native runtimes; fixed public installation and host-model/creative acceptance are recorded separately','source':before,'layers':{'native':args.native,'desktop':args.desktop,'fixedCandidateInstallation':'NOT_RUN','hostModelRouting':'NOT_RUN','independentCreativeReview':'NOT_RUN','all755CommandContexts':'NOT_RUN','externalPsdEditor':'NOT_RUN'},'checks':[]}
 if reused is not None:
  report['reuse']={'baselineFile':str(args.reuse_skills_evidence.relative_to(ROOT)) if args.reuse_skills_evidence.is_relative_to(ROOT) else args.reuse_skills_evidence.name,'baselineSha256':hashlib.sha256(args.reuse_skills_evidence.read_bytes()).hexdigest(),'scope':'skills-tests only, byte-identical source and equal native/desktop opt-in layers; all plugin/static checks freshly executed'}
  report['reusedNativeReports']=baseline.get('nativeReports',{})
  report['reuse']['baselineStatus']=baseline['status'];report['reuse']['baselineFailedChecks']=[item['name'] for item in baseline['checks'] if item.get('status')=='FAIL']
 def save():output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 save()
 with tempfile.TemporaryDirectory(prefix='photocraft-candidate-validation-') as temporary:
  temp=Path(temporary).resolve();env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
  # 排除继承的外部验收路径，避免覆盖用户保留产物或调用非候选脚本。
  for key in list(env):
   if key.startswith(('CRAFT_','PHOTOCRAFT_')):env.pop(key)
  if args.native:
   for key in ('LIVE_TEST','LIVE_SUITE','NATIVE_WORKFLOW_FIRST_USE','NATIVE_COMMANDS','NATIVE_PROTOCOL_FAULTS','TASK_FIRST_USE','CHINESE_TEXT_FIRST_USE','PHOTO_PSD_FIRST_USE','PHOTO_FONTLESS_FIRST_USE','LAYOUT_FIRST_USE','RETOUCH_WORKFLOW_FIRST_USE','PROTECTED_FIRST_USE','SMART_FIRST_USE','PHOTO_ADJUSTMENT_FIRST_USE','SELECTION_FIRST_USE','PHOTO_DELIVERY_FIRST_USE','FLAT_EXPORT_FIRST_USE','UNICODE_PATH_FIRST_USE','OPTIMIZATION_NATIVE_TEST'):env['CRAFT_'+key]='1'
   env['CRAFT_PHOTO_DELIVERY_OUTPUT']=str(temp/'integrity-output');env['CRAFT_INSTALLED_PHOTO_EXPORT_SKILL']=str(skills/'skills/photocraft-cli-export')
   installation=temp/'installation.json';installation.write_text(json.dumps({'runtimeHome':str(Path.home()/'.local/share/craft-runtimes')}));env['CRAFT_PRESERVED_STAGE_INSTALLATION']=str(installation)
   env['PHOTOCRAFT_NATIVE_TEST']='1';env['PHOTOCRAFT_SKILL_ROOT']=str(skills/'skills/photocraft-use');env['PHOTOCRAFT_PYTHON']=sys.executable
  if args.desktop:
   env['CRAFT_CAPABILITY_FIRST_USE']='1';env['CRAFT_INSTALLED_CAPABILITY_SKILL']=str(skills/'skills/photocraft-cli');env['CRAFT_CAPABILITY_REPORT']=str(temp/'capability_report.json')
   for flag,path,report_key in [('DESKTOP_FIRST_USE','DESKTOP_SKILL','DESKTOP_REPORT'),('DESKTOP_SESSION_FIRST_USE','DESKTOP_SESSION_SKILL','DESKTOP_SESSION_REPORT'),('ADVANCED_DESKTOP','ADVANCED_DESKTOP_SKILL','ADVANCED_DESKTOP_REPORT')]:
    env['CRAFT_'+flag]='1';env['CRAFT_'+path]=str(skills/'skills/photocraft-cli');env['CRAFT_'+report_key]=str(temp/(report_key.lower()+'.json'))
  for key in ['NATIVE_PROTOCOL_REPORT','PRESERVED_STAGE_EVIDENCE','NATIVE_WORKFLOW_REPORT','PHOTO_ADJUSTMENT_REPORT','NATIVE_REPORT','NATIVE_REVISION_REPORT','PROTECTED_EVIDENCE_FILE','RETOUCH_EVIDENCE_FILE','LAYOUT_EVIDENCE_FILE','SMART_EVIDENCE','SELECTION_EVIDENCE_FILE','PHOTO_FONTLESS_EVIDENCE','FLAT_EXPORT_REPORT']:
   env['CRAFT_'+key]=str(temp/(key.lower()+'.json'))
  junit=temp/'skills-junit.xml'
  commands=[('skills-tests',[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','--junitxml='+str(junit)],skills),('plugin-tests',['node','--test',*[str(p.relative_to(ROOT)) for p in sorted((ROOT/'tests').glob('*.test.ts'))]],ROOT)]
  commands.extend([('plugin-python-tests',[sys.executable,'-B','-m','unittest','discover','-s','tests','-p','test_*.py'],ROOT),('skills-resources',[sys.executable,'-I','-B','scripts/sync_skill_suite.py','--check'],skills),('skills-command-coverage',[sys.executable,'-I','-B','scripts/build_command_coverage.py','--check'],skills),('skills-release-identity',[sys.executable,'-I','-B','scripts/check_release_identity.py'],skills),('command-acceptance-index',[sys.executable,'-I','-B','scripts/command_acceptance.py','check','--skill-root',str(skills/'skills/photocraft-use'),'--index','docs/evidence/optimization/command-acceptance-index.json'],ROOT),('plugin-release-identity',[sys.executable,'-I','-B','scripts/check_release_identity.py'],ROOT),('fixed-snapshot-integrity',[sys.executable,'-I','-B','scripts/vendor/skill_vendor.py','check','--offline'],ROOT),('openspec-validation',['openspec','validate','establish-v1-plugin','--strict'],ROOT),('documentation-validation',[sys.executable,'-I','-B','scripts/validate_docs.py'],ROOT),('skills-whitespace',['git','diff','--check'],skills),('plugin-whitespace',['git','diff','--check'],ROOT)])
  for label,command,cwd in commands:
   if label=='skills-tests' and reused is not None:
    item={**reused,'reused':True,'baselineSeconds':reused['seconds'],'seconds':0.0};report['checks'].append(item);save();print('skills-tests REUSED exact source and layers',flush=True);continue
   print('START '+label,flush=True);started=time.monotonic()
   try:
    result=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,timeout=1200);text=result.stdout+'\n'+result.stderr;code=result.returncode
   except (OSError,subprocess.TimeoutExpired) as error:text=str(error);code=-1
   # 只保存结论和失败诊断；删除本机私有路径。
   clean=text.replace(str(skills),'SKILLS_REPOSITORY').replace(str(ROOT),'PLUGIN_REPOSITORY').replace(str(temp),'TEMPORARY_WORKSPACE').replace(str(Path.home()),'USER_HOME')
   item={'name':label,'command':[arg.replace(str(skills),'SKILLS_REPOSITORY').replace(str(ROOT),'PLUGIN_REPOSITORY').replace(str(temp),'TEMPORARY_WORKSPACE').replace(str(Path.home()),'USER_HOME') for arg in command],'status':'PASS' if code==0 else 'FAIL','exitCode':code,'seconds':round(time.monotonic()-started,3),'outputSha256':hashlib.sha256(text.encode()).hexdigest(),'summary':clean[-1000:] if code==0 else clean[-10000:]}
   if label=='skills-tests' and junit.exists():
    tree=ET.parse(junit);cases=tree.findall('.//testcase');item['tests']={'total':len(cases),'passed':sum(not any(c.find(k)is not None for k in ['failure','error','skipped']) for c in cases),'failed':sum(c.find('failure') is not None or c.find('error') is not None for c in cases),'skipped':sum(c.find('skipped') is not None for c in cases),'caseIds':[c.attrib.get('classname','')+'::'+c.attrib['name'] for c in cases]}
    item['failures']=[{'case':c.attrib.get('classname','')+'::'+c.attrib['name'],'diagnostic':((c.find('failure') if c.find('failure') is not None else c.find('error')).text or '').replace(str(temp),'TEMPORARY_WORKSPACE').replace(str(Path.home()),'USER_HOME')} for c in cases if c.find('failure') is not None or c.find('error') is not None]
   if label=='plugin-tests':item['tests']={key:int(value) for key,value in re.findall(r'(?:# |ℹ )(tests|pass|fail|skipped) (\d+)',text)}
   report['checks'].append(item);save();print(label+' '+item['status']+' '+str(item['seconds'])+'s',flush=True)
  report['nativeReports']={}
  for path in sorted(temp.glob('*.json')):
   if args.native and path==installation:continue
   try:report['nativeReports'][path.name]=json.loads(path.read_text().replace(str(temp),'TEMPORARY_WORKSPACE').replace(str(Path.home()),'USER_HOME'))
   except (ValueError,OSError):pass
 after={'skills':fingerprint(skills),'plugin':fingerprint(ROOT)};report['sourceUnchanged']=all(after[key]['sha256']==before[key]['sha256'] for key in before)
 report['finishedAt']=datetime.now(timezone.utc).isoformat();report['status']='PASS' if report['sourceUnchanged'] and all(item['exitCode']==0 for item in report['checks']) else 'FAIL';save();print(json.dumps({'status':report['status'],'sourceUnchanged':report['sourceUnchanged'],'checks':len(report['checks'])}));return int(report['status']!='PASS')
if __name__=='__main__':raise SystemExit(main())
