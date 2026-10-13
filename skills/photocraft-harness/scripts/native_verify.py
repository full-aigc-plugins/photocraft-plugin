#!/usr/bin/env python3
"""使用已安装固定二进制在新会话只读重开；不安装、不修改交付包。"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
sys.dont_write_bytecode=True

def load(name):
 spec=importlib.util.spec_from_file_location('verify_'+name,Path(__file__).with_name(name+'.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def verify(root,runtime_home):
 root=Path(root).absolute();delivery=load('delivery');manifest=delivery.validate_delivery(root);manifest_sha=delivery.sha(root/'manifest.json')
 lock=delivery.read_json(Path(__file__).with_name('runtime.lock.json'));key=f'{platform.system().lower()}-{platform.machine().lower()}'
 if key not in lock['artifacts']:raise ValueError('unsupported_platform')
 installed=load('bootstrap').inspect_install(Path(runtime_home)/'photocraft'/lock['resolvedVersion'],lock['artifact'],lock['artifacts'][key])
 if installed['binarySha256']!=manifest['runtimeSha256']:raise ValueError('runtime_identity_mismatch')
 psd_verification=None
 flat_verification=None
 with tempfile.TemporaryDirectory(prefix='photocraft-readonly-') as temporary:
  with load('mcp_session').Session([installed['executable'],'mcp','--automation-read-root',str(root),'--automation-write-root',temporary]) as session:
   commands=load('commands')
   def call(name,args):
    result=commands.parse_reply(session.request('tools/call',{'name':name,'arguments':args}))
    return commands.validate_tool_reply(name,result,args)
   call('doc_open',{'path':'project.pcraft'});actual=call('doc_inspect',{})
   if 'native-facts.json' in manifest['files']:
    facts=load('native_facts').collect(root/'project.pcraft',actual,call)
    if facts!=delivery.read_json(root/'native-facts.json'):raise ValueError('native_facts_changed')
   flat_verification=load('flat_export').verify_reopen(root,temporary,call,actual)
   if 'psd-inspection.json' in manifest['files']:
    call('doc_open',{'path':'design.psd'});actual_psd=call('doc_inspect',{})
    psd_verification=load('psd_features').verify_reopen(delivery.read_json(root/'psd-inspection.json'),actual_psd)
 load('domain_assertions').compare(delivery.read_json(root/'native.json'),actual,{})
 delivery.validate_delivery(root,manifest_sha)
 result={'schema':'photocraft-native-verification/v1','result':'PASS','manifestSha256':manifest_sha,'projectSha256':manifest['files']['project.pcraft'],'runtimeSha256':installed['binarySha256'],'scope':'fresh headless reopen and recorded object preservation; creative review NOT_RUN'}
 if psd_verification is not None:result['psdVerification']=psd_verification
 if flat_verification is not None:result['flatExportVerification']=flat_verification
 return result

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('delivery');parser.add_argument('--runtime-home',default=os.environ.get('CRAFT_RUNTIME_HOME',str(Path.home()/'.local/share/craft-runtimes')));args=parser.parse_args()
 try:print(json.dumps(verify(args.delivery,args.runtime_home),ensure_ascii=False))
 except (ValueError,OSError,RuntimeError,KeyError,TypeError) as error:
  print(json.dumps({'result':'FAIL',**load('operation_errors').describe(error,'verification'),'phase':'verification'},ensure_ascii=False));raise SystemExit(1)
