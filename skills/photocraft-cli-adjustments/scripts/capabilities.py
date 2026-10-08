"""绑定命令参数说明、MCP 工具模式、二进制和会话；不将目录发现视为执行成功。"""
import hashlib
import json
import uuid
from pathlib import Path

def encoded(value):
 return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def snapshot(rows,tools,binary_sha256,backend,session_id):
 if (not isinstance(rows,list) or not isinstance(tools,list) or not session_id
     or any(not isinstance(r,dict) or not isinstance(r.get('id'),str) or not isinstance(r.get('params'),str) for r in rows)
     or len({r['id'] for r in rows})!=len(rows)
     or any(not isinstance(t,dict) or not isinstance(t.get('name'),str) or not isinstance(t.get('inputSchema'),dict) for t in tools)
     or len({t['name'] for t in tools})!=len(tools)):raise ValueError('invalid_capability_registry')
 contracts=sorted([{'id':r['id'],'params':r['params']} for r in rows],key=lambda r:r['id'])
 schemas=sorted([{'name':t['name'],'inputSchema':t['inputSchema']} for t in tools],key=lambda t:t['name'])
 return {'schema':'photocraft-capabilities/v1','sessionId':session_id,'backend':backend,'binarySha256':binary_sha256,'commandsSha256':hashlib.sha256(encoded(contracts)).hexdigest(),'toolsSha256':hashlib.sha256(encoded(schemas)).hexdigest(),'commandCount':len(rows),'toolCount':len(tools),'parameterContract':'runtime parameter descriptions plus MCP tool schemas; not per-command JSON Schema'}
def ensure(expected,actual):
 if expected!=actual:raise ValueError('capability_changed')
def match_catalog(actual,expected):
 rows={r['id']:r for r in actual}
 for row in expected:
  if row['id'] not in rows:raise ValueError('catalog_command_missing: '+row['id'])
  if rows[row['id']]['params']!=row['params']:raise ValueError('catalog_parameter_drift: '+row['id'])
class Gate:
 def __init__(self,session,commands,binary_sha256,backend='headless',reference=None):
  self.session=session;self.commands=commands;self.backend=backend;self.binary_sha256=binary_sha256;self.session_id=str(uuid.uuid4());self.expected=None;self.reference=reference
  if backend=='bridge':
   if self.reference is None:self.reference=commands.reply_json((Path(__file__).parent.parent/'references/desktop-command-snapshot.json').read_text())
   if self.reference.get('cliBinarySha256')!=binary_sha256:raise ValueError('backend_runtime_identity_mismatch')
 def check(self,command=None):
  tools=self.session.request('tools/list',{}).get('tools')
  rows=self.commands.runtime_rows(self.session)
  current=snapshot(rows,tools,self.binary_sha256,self.backend,self.session_id)
  if self.expected is None:
   if self.reference:
    pinned=snapshot(self.reference['commands'],self.reference['tools'],self.binary_sha256,self.backend,self.session_id)
    ensure(pinned,current)
   else:match_catalog(rows,self.commands.catalog()['commands'])
   self.expected=current
  else:ensure(self.expected,current)
  if command is not None:
   row=next((r for r in rows if r['id']==command),None)
   if row is None:raise ValueError('command_unavailable: '+command)
   if row.get('enabled') is not True:raise ValueError('command_disabled: '+command)
  return current
