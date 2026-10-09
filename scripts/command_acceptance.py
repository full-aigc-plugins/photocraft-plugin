#!/usr/bin/env python3
"""逐命令上下文及绑定证据索引；目录、候选证据和固定安装验收分别记录。"""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re

REQUIREMENTS=('document','selection','assets','permissions','backend','resultAssertions','nativeSave','localRevision')
PROOF_FILES=('plan','receipt','project','preview','nativeVerification','revisionProject','revisionVerification','assertions')
def encoded(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(value):return hashlib.sha256(value).hexdigest()
def sha(path):return digest(Path(path).read_bytes())
def read(path):
 def pairs(items):
  result={}
  for key,value in items:
   if key in result:raise ValueError('duplicate_json_key: '+key)
   result[key]=value
  return result
 def number(value):
  result=float(value)
  if not math.isfinite(result):raise ValueError('nonfinite_json')
  return result
 def constant(value):raise ValueError('nonfinite_json: '+value)
 return json.loads(Path(path).read_text(),object_pairs_hook=pairs,parse_float=number,parse_constant=constant)
def source(root):
 root=Path(root).absolute();files={}
 for folder in ('scripts','references'):
  for path in sorted((root/folder).iterdir()):
   if path.suffix in ('.py','.json'):
    if path.is_symlink() or not path.is_file():raise ValueError('skill_resource_not_regular')
    files[str(path.relative_to(root))]=sha(path)
 return {'sha256':digest(encoded(files)),'files':files}
def scaffold(skill):
 skill=Path(skill);catalog=read(skill/'references/command-coverage.json');desktop=read(skill/'references/desktop-command-snapshot.json');bridge={row['id'] for row in desktop['commands']};identity=source(skill)
 return {'schema':'photocraft-command-acceptance/v1','scope':'candidate command-context evidence index; fixed installation, host/model and creative acceptance remain separate','sourceSha256':identity['sha256'],'sourceFiles':identity['files'],'runtimeSha256':catalog['runtimeSha256'],'commands':[{'id':row['id'],'commandContractSha256':digest(encoded({'id':row['id'],'params':row['params']})),'ownerSkill':row['ownerSkill'],'contextCoverage':'UNREVIEWED','contexts':[{'backend':backend,'registered':registered,'status':'NOT_RUN','reason':'Context and business assertions not yet reviewed' if registered else 'Not registered by this pinned backend; headless acceptance remains required','requirements':{key:'UNKNOWN' for key in REQUIREMENTS},'evidence':None}for backend,registered in [('headless',True),('bridge',row['id'] in bridge)]]}for row in catalog['commands']]}
def proof_file(root,ref):
 if not isinstance(ref,dict) or set(ref)!={'path','sha256'} or not isinstance(ref['path'],str) or not isinstance(ref['sha256'],str) or not re.fullmatch('[a-f0-9]{64}',ref['sha256']):raise ValueError('invalid_evidence_reference')
 path=Path(ref['path']);root=Path(root).resolve()
 if path.is_absolute() or '..' in path.parts:raise ValueError('evidence_path_escape')
 path=root/path
 if not path.resolve().is_relative_to(root) or any(part.is_symlink() for part in [path,*path.parents] if part!=root):raise ValueError('evidence_path_escape')
 if not path.is_file() or sha(path)!=ref['sha256']:raise ValueError('evidence_digest_mismatch')
 return path
def native_proof(row,context,index,skill,root):
 proof=context['evidence']
 if not isinstance(proof,dict) or set(proof)!={'files','inputs'} or not isinstance(proof['files'],dict) or set(proof['files'])!=set(PROOF_FILES) or not isinstance(proof['inputs'],list):raise ValueError('bound_native_evidence_required')
 paths={key:proof_file(root,ref)for key,ref in proof['files'].items()}
 for ref in proof['inputs']:proof_file(root,ref)
 plan=read(paths['plan']);receipt=read(paths['receipt']);assertions=read(paths['assertions'])
 expected_plan=digest(json.dumps(plan,ensure_ascii=False,sort_keys=True,allow_nan=False).encode())
 if receipt.get('schema')!='craft-command-receipt/v1' or receipt.get('result')!='PASS' or receipt.get('mode')!=context['backend'] or receipt.get('planSha256')!=expected_plan or receipt.get('runtimeSha256')!=index['runtimeSha256'] or receipt.get('catalogSha256')!=sha(Path(skill)/'references/command-coverage.json'):raise ValueError('command_receipt_binding_mismatch')
 matched=[step for step in receipt.get('steps',[]) if step.get('command')==row['id'] or step.get('tool')=='command_run' and step.get('params',{}).get('id')==row['id']]
 if not isinstance(receipt.get('inputs',{}),dict) or any(ref.get('sha256') not in {item['sha256']for item in proof['inputs']} for ref in receipt.get('inputs',{}).values()):raise ValueError('input_binding_mismatch')
 if not matched or any(step.get('state')!='succeeded' or step.get('phase')!='reply_validated' for step in matched):raise ValueError('validated_command_result_required')
 snapshot=read(Path(skill)/'references'/('desktop-command-snapshot.json' if context['backend']=='bridge' else 'native-command-snapshot.json'))
 contracts=sorted([{'id':item['id'],'params':item['params']}for item in snapshot['commands']],key=lambda item:item['id']);tools=sorted([{'name':item['name'],'inputSchema':item['inputSchema']}for item in snapshot['tools']],key=lambda item:item['name']);cap=receipt.get('capabilitySnapshot',{})
 if cap.get('backend')!=context['backend'] or cap.get('binarySha256')!=index['runtimeSha256'] or not cap.get('sessionId') or cap.get('commandsSha256')!=digest(encoded(contracts)) or cap.get('toolsSha256')!=digest(encoded(tools)):raise ValueError('capability_binding_mismatch')
 for key,project in [('nativeVerification','project'),('revisionVerification','revisionProject')]:
  verification=read(paths[key])
  if verification.get('schema')!='photocraft-native-verification/v1' or verification.get('result')!='PASS' or verification.get('projectSha256')!=sha(paths[project]) or verification.get('runtimeSha256')!=index['runtimeSha256']:raise ValueError('native_reopen_binding_mismatch')
 if sha(paths['project'])==sha(paths['revisionProject']):raise ValueError('local_revision_evidence_required')
 expected={'commandId':row['id'],'contextSha256':digest(encoded(context['requirements'])),'sourceSha256':index['sourceSha256'],'planSha256':sha(paths['plan']),'projectSha256':sha(paths['project']),'previewSha256':sha(paths['preview']),'revisionSha256':sha(paths['revisionProject']),'inputsSha256':digest(encoded(proof['inputs']))}
 if assertions.get('status')!='PASS' or any(assertions.get(key)!=value for key,value in expected.items()):raise ValueError('assertion_binding_mismatch')
 checks=assertions.get('checks')
 if not isinstance(checks,list) or not checks or any(not isinstance(check,dict) or not check.get('id') or 'actual' not in check or 'expected' not in check or check['actual']!=check['expected'] for check in checks):raise ValueError('business_assertions_required')
def context_identities(contexts):
 """同后端可有多个场景，但每个场景必须有不重复的明确身份。"""
 ids=set()
 for context in contexts:
  value=context.get('contextId',context['backend'])
  if not isinstance(value,str) or not value.strip() or (context['backend'],value) in ids:raise ValueError('duplicate_or_invalid_context_identity')
  ids.add((context['backend'],value))

def validate(index,skill,root):
 expected=scaffold(skill)
 if not isinstance(index,dict) or index.get('schema')!=expected['schema']:raise ValueError('invalid_acceptance_index')
 if any(index.get(key)!=expected[key]for key in ('sourceSha256','sourceFiles','runtimeSha256')):raise ValueError('stale_source_or_snapshot')
 rows=index.get('commands');catalog={row['id']:row for row in expected['commands']}
 if not isinstance(rows,list) or any(not isinstance(row,dict) or not isinstance(row.get('id'),str) for row in rows) or len(rows)!=len(catalog) or {row['id']for row in rows}!=set(catalog):raise ValueError('command_inventory_mismatch')
 bound=0;accepted=0;counts={key:0 for key in ('PASS','FAIL','NOT_RUN','NOT_APPLICABLE')}
 for row in rows:
  original=catalog[row['id']]
  if row.get('ownerSkill')!=original['ownerSkill'] or row.get('contextCoverage') not in ('UNREVIEWED','REVIEWED'):raise ValueError('invalid_command_owner_or_coverage')
  if row.get('commandContractSha256')!=original['commandContractSha256']:raise ValueError('stale_command_contract: '+row['id'])
  contexts=row.get('contexts')
  if not isinstance(contexts,list) or len(contexts)<2 or {context.get('backend')for context in contexts if isinstance(context,dict)}!={'headless','bridge'}:raise ValueError('command_context_missing')
  context_identities(contexts)
  for context in contexts:
   baseline=next(item for item in original['contexts'] if item['backend']==context['backend'])
   if context.get('registered') is not baseline['registered']:raise ValueError('backend_registration_mismatch')
   status=context.get('status');requirements=context.get('requirements')
   if status not in counts or not isinstance(requirements,dict) or set(requirements)!=set(REQUIREMENTS):raise ValueError('invalid_context_contract')
   counts[status]+=1
   if status=='NOT_APPLICABLE' and (not isinstance(context.get('reason'),str) or not context['reason'].strip() or context['reason']==baseline['reason']):raise ValueError('applicability_reason_required')
   if status=='PASS':
    if not context['registered']:raise ValueError('backend_not_registered')
    if any(not isinstance(value,str) or not value.strip() or value=='UNKNOWN' for value in requirements.values()):raise ValueError('context_requirements_unknown')
    native_proof(row,context,index,skill,root);bound+=1
  if row.get('contextCoverage')=='REVIEWED' and all(context['status']=='PASS' for context in contexts if context['registered']):accepted+=1
 return {'schema':'photocraft-command-acceptance-check/v1','commands':len(rows),'acceptedCommands':accepted,'boundNativeContexts':bound,'contexts':counts,'fullCommandAcceptance':'NOT_RUN','fixedCandidateInstallation':'NOT_RUN','hostModelRouting':'NOT_RUN','creativeAcceptance':'NOT_RUN','sourceAuthenticity':'NOT_PROVEN','scope':'indexed context and bound report integrity only; independent execution authenticity and exhaustive context review require separate acceptance'}
def prior_index(index):
 """核对旧索引自身身份及结构，旧报告不获得当前执行真实性。"""
 if not isinstance(index,dict) or index.get('schema')!='photocraft-command-acceptance/v1':raise ValueError('invalid_acceptance_index')
 files=index.get('sourceFiles')
 if not isinstance(files,dict) or not files or any(not isinstance(k,str) or not isinstance(v,str) or not re.fullmatch('[a-f0-9]{64}',v) for k,v in files.items()):raise ValueError('invalid_prior_source_files')
 if digest(encoded(files))!=index.get('sourceSha256'):raise ValueError('prior_source_digest_mismatch')
 if not isinstance(index.get('runtimeSha256'),str) or not re.fullmatch('[a-f0-9]{64}',index['runtimeSha256']):raise ValueError('invalid_prior_runtime')
 rows=index.get('commands')
 if not isinstance(rows,list) or not rows:raise ValueError('invalid_prior_inventory')
 ids=set()
 for row in rows:
  if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id'] or row['id'] in ids:raise ValueError('invalid_prior_inventory')
  ids.add(row['id'])
  if not isinstance(row.get('ownerSkill'),str) or row.get('contextCoverage') not in ('UNREVIEWED','REVIEWED') or not isinstance(row.get('commandContractSha256'),str) or not re.fullmatch('[a-f0-9]{64}',row['commandContractSha256']):raise ValueError('invalid_prior_command')
  contexts=row.get('contexts')
  if not isinstance(contexts,list) or len(contexts)<2 or any(not isinstance(c,dict) for c in contexts) or {c.get('backend') for c in contexts}!={'headless','bridge'}:raise ValueError('invalid_prior_contexts')
  context_identities(contexts)
  for context in contexts:
   requirements=context.get('requirements')
   if type(context.get('registered')) is not bool or context.get('status') not in ('PASS','FAIL','NOT_RUN','NOT_APPLICABLE') or not isinstance(requirements,dict) or set(requirements)!=set(REQUIREMENTS) or any(not isinstance(v,str) or not v.strip() for v in requirements.values()):raise ValueError('invalid_prior_context')
   if not isinstance(context.get('history',[]),list):raise ValueError('invalid_prior_history')
 if not isinstance(index.get('retiredCommands',[]),list):raise ValueError('invalid_prior_history')
 return rows

def refresh(index,skill,root=Path('.')):
 """返回新索引与变化报告；不写输入或目标，不复用旧来源执行结果。"""
 old_rows=prior_index(index);fresh=scaffold(skill)
 before={row['id']:row for row in old_rows};current={row['id']:row for row in fresh['commands']}
 source_changed=any(index.get(key)!=fresh[key] for key in ('sourceSha256','sourceFiles','runtimeSha256'))
 report={'schema':'photocraft-command-index-refresh/v1','sourceChanged':source_changed,'addedCommands':sorted(set(current)-set(before)),'removedCommands':sorted(set(before)-set(current)),'changedCommands':[],'invalidatedContexts':0,'fullCommandAcceptance':'NOT_RUN','sourceAuthenticity':'NOT_PROVEN'}
 def unchanged(old,new):
  return all(old.get(k)==new[k] for k in ('commandContractSha256','ownerSkill')) and all(c['registered']==next(n for n in new['contexts'] if n['backend']==c['backend'])['registered'] for c in old['contexts'])
 report['changedCommands']=sorted(key for key in set(before)&set(current) if not unchanged(before[key],current[key]))
 if not source_changed:
  if report['addedCommands'] or report['removedCommands'] or report['changedCommands']:raise ValueError('prior_inventory_identity_mismatch')
  validate(index,skill,root)
  return copy.deepcopy(index),report
 retired=copy.deepcopy(index.get('retiredCommands',[]))
 for key in report['removedCommands']:
  retired.append({'sourceSha256':index['sourceSha256'],'sourceFiles':copy.deepcopy(index['sourceFiles']),'runtimeSha256':index['runtimeSha256'],'command':copy.deepcopy(before[key])})
 if retired:fresh['retiredCommands']=retired
 def archive(row,context):
  old=copy.deepcopy(context);history=old.pop('history',[])
  history.append({'sourceSha256':index['sourceSha256'],'runtimeSha256':index['runtimeSha256'],'commandContractSha256':row['commandContractSha256'],'context':old})
  return history
 for row in fresh['commands']:
  old=before.get(row['id'])
  if old is None:continue
  if row['id'] in report['changedCommands']:
   # 旧前置条件只能在历史中保存，不据旧合同继续声称已审查。
   for context in row['contexts']:
    previous=[c for c in old['contexts'] if c['backend']==context['backend']]
    context['history']=[]
    for previous_context in previous:
     context['history'].extend(archive(old,previous_context))
     if previous_context['status']!='NOT_RUN' or previous_context.get('evidence') is not None:report['invalidatedContexts']+=1
   continue
  row.update(copy.deepcopy(old))
  for context in row['contexts']:
   if context['status']!='NOT_RUN' or context.get('evidence') is not None:
    context['history']=archive(old,context);context.update(status='NOT_RUN',evidence=None,reason='Source identity changed; previous result retained in history, current execution required')
    report['invalidatedContexts']+=1
 # NOT_RUN 及历史只表示清单完整；真实原生与创作验收仍须逐项执行。
 validate(fresh,skill,Path('.'))
 return fresh,report

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('operation',choices=['scaffold','check','refresh']);parser.add_argument('--skill-root',required=True,type=Path);parser.add_argument('--index',required=True,type=Path);parser.add_argument('--output',type=Path);parser.add_argument('--evidence-root',type=Path,default=Path('.'));args=parser.parse_args()
 try:
  if args.operation=='refresh':
   if args.output is None:raise ValueError('refresh_output_required')
   index,report=refresh(read(args.index),args.skill_root,args.evidence_root)
   # x 模式拒绝现有文件及链接，旧索引始终只读。
   payload=(json.dumps(index,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
   with args.output.open('xb') as output:output.write(payload)
  else:
   if args.output is not None:raise ValueError('output_only_valid_for_refresh')
   if args.operation=='scaffold':
    index=scaffold(args.skill_root)
    payload=(json.dumps(index,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    with args.index.open('xb') as output:output.write(payload)
   else:index=read(args.index)
   report=validate(index,args.skill_root,args.evidence_root)
  print(json.dumps(report,ensure_ascii=False,indent=2));return 0
 except (ValueError,OSError,KeyError,TypeError) as error:print(json.dumps({'status':'FAIL','error':str(error)},ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
