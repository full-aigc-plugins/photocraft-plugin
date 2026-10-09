#!/usr/bin/env python3
"""绑定逐命令静态启用条件来源；不提升实际执行或上下文审查状态。"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re

spec=importlib.util.spec_from_file_location('source_context_acceptance',Path(__file__).with_name('command_acceptance.py'))
acceptance=importlib.util.module_from_spec(spec);spec.loader.exec_module(acceptance)

def hex_digest(value):
 if not isinstance(value,str) or not re.fullmatch('[a-f0-9]{64}',value):raise ValueError('invalid_source_digest')
 return value

def source_path(name,root):
 if not isinstance(name,str) or not name or Path(name).is_absolute() or '..' in Path(name).parts:raise ValueError('source_path_escape')
 if root is None:return None
 base=Path(root).resolve();path=base/name
 if not path.resolve().is_relative_to(base) or any(p.is_symlink() for p in [path,*path.parents] if p!=base):raise ValueError('source_path_escape')
 if not path.is_file():raise ValueError('source_file_missing')
 return path

def locator(value,files,root):
 if not isinstance(value,dict) or set(value)!={'path','sha256','lineStart','lineEnd','spanSha256'}:raise ValueError('invalid_source_locator')
 name=value['path'];path=source_path(name,root)
 if name not in files or hex_digest(value['sha256'])!=files[name]:raise ValueError('source_locator_file_mismatch')
 start=value['lineStart'];end=value['lineEnd'];hex_digest(value['spanSha256'])
 if type(start) is not int or type(end) is not int or not 1<=start<=end:raise ValueError('invalid_source_range')
 if path is None:return None
 raw=path.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=files[name]:raise ValueError('source_file_digest_mismatch')
 lines=raw.splitlines(keepends=True)
 if end>len(lines):raise ValueError('invalid_source_range')
 span=b''.join(lines[start-1:end])
 if hashlib.sha256(span).hexdigest()!=value['spanSha256']:raise ValueError('source_span_digest_mismatch')
 return span.decode('utf-8')

def verify_profile(index,profile,skill,root,evidence_root):
 acceptance.validate(index,skill,evidence_root)
 if not isinstance(profile,dict) or profile.get('schema')!='photocraft-command-source-contexts/v1':raise ValueError('invalid_source_profile')
 catalog=acceptance.read(Path(skill)/'references/command-coverage.json')
 if profile.get('upstreamRepository')!='https://github.com/storytold/photocraft' or profile.get('upstreamCommit')!=catalog.get('upstreamCommit'):raise ValueError('source_upstream_mismatch')
 hex_digest(profile.get('patchSha256'))
 if profile.get('skillSourceSha256')!=index['sourceSha256'] or profile.get('runtimeSha256')!=index['runtimeSha256']:raise ValueError('source_profile_identity_mismatch')
 files=profile.get('files')
 if not isinstance(files,dict) or not files:raise ValueError('source_manifest_required')
 for name,sha in files.items():
  path=source_path(name,root);hex_digest(sha)
  if path is not None and hashlib.sha256(path.read_bytes()).hexdigest()!=sha:raise ValueError('source_file_digest_mismatch')
 rows=profile.get('commands');expected={r['id']:r for r in index['commands']}
 if not isinstance(rows,list) or any(not isinstance(r,dict) or not isinstance(r.get('id'),str) for r in rows) or len(rows)!=len(expected) or {r['id'] for r in rows}!=set(expected):raise ValueError('source_command_inventory_mismatch')
 for row in rows:
  if row.get('commandContractSha256')!=expected[row['id']]['commandContractSha256']:raise ValueError('source_command_contract_mismatch')
  declarations=[locator(row.get('registration'),files,root)]
  for key in ('macroDefinition','generationSource'):
   if row.get(key) is not None:declarations.append(locator(row[key],files,root))
  expression=row.get('enabledExpression');definitions=row.get('predicateDefinitions')
  if not isinstance(expression,str) or not expression.strip() or not isinstance(definitions,list):raise ValueError('enabled_source_required')
  if not expression.lstrip().startswith('|') and not definitions:raise ValueError('predicate_definition_required')
  for value in definitions:locator(value,files,root)
  if root is not None and re.sub(r'\s+','',expression) not in ''.join(re.sub(r'\s+','',s or '') for s in declarations):raise ValueError('enabled_expression_not_in_registration')
 return {'schema':'photocraft-command-source-context-check/v1','sourceBoundCommands':len(rows),'upstreamBytes':'VERIFIED' if root is not None else 'NOT_VERIFIED','nativeExecution':'NOT_RUN','contextReview':'NOT_RUN','desktopPredicateAcceptance':'NOT_RUN','fullV1':'OPEN','scope':'Static source/file/range and parameter identity binding only; source authenticity, runtime enablement and full business prerequisites remain separate.'}

def binding(profile):
 return {'sha256':acceptance.digest(acceptance.encoded(profile)),'upstreamCommit':profile['upstreamCommit'],'patchSha256':profile['patchSha256']}

def bind(index,profile,skill,upstream,evidence_root=Path('.')):
 """核验实际源码后返回新索引；保留每条命令的人工审查和执行状态。"""
 if upstream is None:raise ValueError('binding_requires_original_source')
 report=verify_profile(index,profile,skill,upstream,evidence_root);identity=binding(profile)
 if index.get('sourceContextProfile') not in (None,identity):raise ValueError('source_profile_binding_conflict')
 result=copy.deepcopy(index);result['sourceContextProfile']=identity;return result,report

def check(index,profile,skill,upstream,evidence_root=Path('.')):
 """分别报告目录身份与原始源码字节核验，不补造实际命令运行证据。"""
 if index.get('sourceContextProfile')!=binding(profile):raise ValueError('source_profile_binding_mismatch')
 return verify_profile(index,profile,skill,upstream,evidence_root)

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('operation',choices=['bind','check']);parser.add_argument('--index',type=Path,required=True);parser.add_argument('--profile',type=Path,required=True);parser.add_argument('--skill-root',type=Path,required=True);parser.add_argument('--source-root',type=Path);parser.add_argument('--evidence-root',type=Path,default=Path('.'));parser.add_argument('--output',type=Path);args=parser.parse_args()
 try:
  index=acceptance.read(args.index);profile=acceptance.read(args.profile)
  if args.operation=='bind':
   if args.output is None:raise ValueError('binding_output_required')
   result,report=bind(index,profile,args.skill_root,args.source_root,args.evidence_root);payload=(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
   with args.output.open('xb') as stream:stream.write(payload)
  else:
   if args.output is not None:raise ValueError('output_only_valid_for_binding')
   report=check(index,profile,args.skill_root,args.source_root,args.evidence_root)
  print(json.dumps(report,ensure_ascii=False,indent=2));return 0
 except (ValueError,OSError,KeyError,TypeError) as error:print(json.dumps({'status':'FAIL','error':str(error)},ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
