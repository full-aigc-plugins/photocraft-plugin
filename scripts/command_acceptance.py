#!/usr/bin/env python3
"""逐命令上下文及绑定证据索引；目录、候选证据和固定安装验收分别记录。"""
import argparse
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
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('operation',choices=['scaffold','check']);parser.add_argument('--skill-root',required=True,type=Path);parser.add_argument('--index',required=True,type=Path);parser.add_argument('--evidence-root',type=Path,default=Path('.'));args=parser.parse_args()
 try:
  if args.operation=='scaffold':
   index=scaffold(args.skill_root)
   with args.index.open('x')as output:output.write(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
  else:index=read(args.index)
  print(json.dumps(validate(index,args.skill_root,args.evidence_root),ensure_ascii=False,indent=2));return 0
 except (ValueError,OSError,KeyError,TypeError) as error:print(json.dumps({'status':'FAIL','error':str(error)},ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
