#!/usr/bin/env python3
"""只读核对失败暂存并重开原工程；不能将部分成功升级为交付通过。"""
import argparse
import importlib.util
import os
from pathlib import Path
import platform
import sys
import tempfile
sys.dont_write_bytecode=True
_spec=importlib.util.spec_from_file_location('checkpoint_native_verify',Path(__file__).with_name('native_verify.py'));_module=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_module);load=_module.load

def safe(path, root):
 path=Path(os.path.abspath(path));root=Path(root).absolute()
 if path==root or not path.is_relative_to(root):raise ValueError('checkpoint_outside_authorization')
 for part in (path,*path.parents):
  if part.is_symlink():raise ValueError('checkpoint_symlink')
 return path

def verify(output,write_root,runtime_home):
 delivery=load('delivery');output=safe(output,write_root);record_path=output/'failure.json';record_sha=delivery.sha(record_path);record=delivery.read_json(record_path)
 if record.get('schema')!='craft-failed-stage/v1' or record.get('replayAllowed') is not False:raise ValueError('checkpoint_record_invalid')
 stage=safe(output/record['stage'],write_root)
 if delivery.read_json(stage/'failure.json')!=record:raise ValueError('checkpoint_record_conflict')
 def check():
  if delivery.sha(record_path)!=record_sha:raise ValueError('checkpoint_changed')
  for name,entry in record['files'].items():
   path=delivery.file_path(stage,name)
   if delivery.sha(path)!=entry['sha256'] or path.stat().st_size!=entry['bytes']:raise ValueError('checkpoint_file_changed')
 check();project=delivery.file_path(stage,'project.pcraft')
 if 'project.pcraft' not in record['files']:raise ValueError('checkpoint_project_missing')
 lock=delivery.read_json(Path(__file__).with_name('runtime.lock.json'));key=f'{platform.system().lower()}-{platform.machine().lower()}'
 if key not in lock['artifacts']:raise ValueError('unsupported_platform')
 installed=load('bootstrap').inspect_install(Path(runtime_home)/'photocraft'/lock['resolvedVersion'],lock['artifact'],lock['artifacts'][key])
 with tempfile.TemporaryDirectory(prefix='photocraft-checkpoint-readonly-') as temporary:
  with load('mcp_session').Session([installed['executable'],'mcp','--automation-read-root',str(stage),'--automation-write-root',temporary]) as session:
   commands=load('commands')
   def call(name,args):
    result=commands.parse_reply(session.request('tools/call',{'name':name,'arguments':args}))
    return commands.validate_tool_reply(name,result,args)
   call('doc_open',{'path':'project.pcraft'})
   native=call('doc_inspect',{})
 check()
 result={'schema':'photocraft-checkpoint-verification/v1','result':'PASS','stage':str(stage),'recordSha256':record_sha,'projectSha256':delivery.sha(project),'files':record['files'],'lastAttempt':record.get('lastAttempt'),'completedOperations':record.get('completedOperations'),'nativeReopened':True,'objectCount':len(load('domain_assertions').index(native)),'runtimeSha256':installed['binarySha256'],'replayAllowed':False,'technical':'NOT_RUN','creative':'NOT_RUN','scope':'partial saved project only; unknown operations are not replayed'}
 if 'recovery-context.json' in record['files']:
  context=delivery.read_json(stage/'recovery-context.json');source=load('checkpoint_source');bound=source.snapshot(output,write_root,{'expectedCheckpointSha256':record_sha,'expectedCheckpointPlanSha256':context['executionIdentity']['planHash'],'expectedProjectSha256':result['projectSha256']},installed['binarySha256'])
  result['origin']={'taskBinding':context['taskBinding'],'planSha256':context['executionIdentity']['planHash'],'projectRevision':context['executionIdentity']['projectRevision'],'inputHashes':context['executionIdentity']['inputHashes'],'bindingsSha256':source.canonical_sha(context['bindings']),'capabilitySha256':source.canonical_sha(context['capability'])}
  result['nativeDocument']=native
 return result

if __name__=='__main__':
 import json
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output');parser.add_argument('--write-root',required=True);parser.add_argument('--runtime-home',default=os.environ.get('CRAFT_RUNTIME_HOME',str(Path.home()/'.local/share/craft-runtimes')));args=parser.parse_args()
 try:print(json.dumps(verify(args.output,args.write_root,args.runtime_home),ensure_ascii=False))
 except (ValueError,OSError,RuntimeError,KeyError,TypeError) as error:
  print(json.dumps({'result':'FAIL',**load('operation_errors').describe(error,'verification'),'phase':'verification'},ensure_ascii=False));raise SystemExit(1)
