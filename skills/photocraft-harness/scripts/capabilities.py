"""绑定命令参数说明、MCP 工具模式、二进制和会话；不将目录发现视为执行成功。"""
import hashlib
import json
import re
import uuid
from pathlib import Path

def encoded(value):
 return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def snapshot(rows,tools,binary_sha256,backend,session_id,runtime_identity=None,desktop_identity=None):
 if runtime_identity is not None and (not isinstance(runtime_identity,dict) or set(runtime_identity)!={"version","versionOutput","platform"} or not isinstance(runtime_identity.get("version"),str) or not re.fullmatch(r"\d+\.\d+\.\d+(?:-craft\.[1-9]\d*)?",runtime_identity["version"]) or not isinstance(runtime_identity.get("versionOutput"),str) or not runtime_identity["versionOutput"] or runtime_identity.get("platform") not in ("darwin-arm64","darwin-x86_64","linux-x86_64","linux-aarch64","windows-amd64")):raise ValueError("runtime_identity_invalid")
 if desktop_identity is not None and (not isinstance(desktop_identity,dict) or set(desktop_identity)!={"version","binarySha256"} or not isinstance(desktop_identity.get("version"),str) or not re.fullmatch(r"\d+\.\d+\.\d+",desktop_identity["version"]) or not isinstance(desktop_identity.get("binarySha256"),str) or not re.fullmatch(r"[a-f0-9]{64}",desktop_identity["binarySha256"])):raise ValueError("desktop_identity_invalid")
 if (not isinstance(rows,list) or not isinstance(tools,list) or not session_id
     or any(not isinstance(r,dict) or not isinstance(r.get('id'),str) or not isinstance(r.get('params'),str) for r in rows)
     or len({r['id'] for r in rows})!=len(rows)
     or any(not isinstance(t,dict) or not isinstance(t.get('name'),str) or not isinstance(t.get('inputSchema'),dict) for t in tools)
     or len({t['name'] for t in tools})!=len(tools)):raise ValueError('invalid_capability_registry')
 contracts=sorted([{'id':r['id'],'params':r['params']} for r in rows],key=lambda r:r['id'])
 schemas=sorted([{'name':t['name'],'inputSchema':t['inputSchema']} for t in tools],key=lambda t:t['name'])
 return {'runtimeIdentity':dict(runtime_identity) if runtime_identity is not None else None,'desktopIdentity':dict(desktop_identity) if desktop_identity is not None else None,'schema':'photocraft-capabilities/v1','sessionId':session_id,'backend':backend,'binarySha256':binary_sha256,'commandsSha256':hashlib.sha256(encoded(contracts)).hexdigest(),'toolsSha256':hashlib.sha256(encoded(schemas)).hexdigest(),'commandCount':len(rows),'toolCount':len(tools),'parameterContract':'runtime parameter descriptions plus MCP tool schemas; not per-command JSON Schema'}
def ensure(expected,actual):
 if expected!=actual:raise ValueError('capability_mismatch: capability_changed')
def match_catalog(actual,expected):
 rows={r['id']:r for r in actual}
 for row in expected:
  if row['id'] not in rows:raise ValueError('capability_missing: catalog_command_missing: '+row['id'])
  if rows[row['id']]['params']!=row['params']:raise ValueError('capability_mismatch: catalog_parameter_drift: '+row['id'])
class Gate:
 def __init__(self,session,commands,binary_sha256,backend='headless',reference=None,runtime_identity=None):
  self.session=session;self.commands=commands;self.backend=backend;self.binary_sha256=binary_sha256;self.session_id=str(uuid.uuid4());self.expected=None;self.reference=reference;self.runtime_identity=runtime_identity;self.desktop_identity=None;self.rows={};self.tools={};self.checks=[]
  if backend=='bridge':
   desktop=getattr(session,'desktop',None)
   if desktop is not None:self.desktop_identity={k:desktop[k] for k in ('version','binarySha256')}
   if self.reference is None:self.reference=commands.reply_json((Path(__file__).parent.parent/'references/desktop-command-snapshot.json').read_text())
   if self.reference.get('cliBinarySha256')!=binary_sha256:raise ValueError('capability_mismatch: backend_runtime_identity_mismatch')
   if self.desktop_identity is not None and self.desktop_identity['binarySha256']!=self.reference.get('desktopBinarySha256'):raise ValueError('capability_mismatch: backend_desktop_identity_mismatch')
 def check(self,command=None):
  tools=self.session.request('tools/list',{}).get('tools')
  rows=self.commands.runtime_rows(self.session)
  current=snapshot(rows,tools,self.binary_sha256,self.backend,self.session_id,self.runtime_identity,self.desktop_identity)
  if self.expected is None:
   if self.reference:
    missing={r['id'] for r in self.reference['commands']}-{r['id'] for r in rows}
    if missing:raise ValueError('capability_missing: catalog_command_missing: '+sorted(missing)[0])
    pinned=snapshot(self.reference['commands'],self.reference['tools'],self.binary_sha256,self.backend,self.session_id,self.runtime_identity,self.desktop_identity)
    ensure(pinned,current)
   else:match_catalog(rows,self.commands.catalog()['commands'])
   self.expected=current
   self.rows={r['id']:dict(r) for r in rows};self.tools={t['name']:json.loads(encoded(t)) for t in tools}
  else:ensure(self.expected,current)
  if command is not None:
   row=next((r for r in rows if r['id']==command),None)
   if row is None:raise ValueError('capability_missing: command_unavailable: '+command)
   if row.get('enabled') is not True:raise ValueError('command_disabled: '+command)
  return current

 def check_scope(self,command_ids,tool_names,enabled_command=None):
  """保留完整发现摘要，仅核验本次调用及发现工具实际依赖的合同。"""
  if self.expected is None:self.check()
  tools=self.session.request('tools/list',{}).get('tools');rows=self.commands.runtime_rows(self.session)
  current=snapshot(rows,tools,self.binary_sha256,self.backend,self.session_id,self.runtime_identity,self.desktop_identity)
  identity=('schema','sessionId','backend','binarySha256','runtimeIdentity','desktopIdentity','parameterContract')
  ensure({k:self.expected[k] for k in identity},{k:current[k] for k in identity})
  actual_rows={r['id']:r for r in rows};actual_tools={t['name']:t for t in tools}
  required_commands=sorted(set(command_ids));required_tools=sorted(set(tool_names)|{self.commands.ROUTES[self.commands.DOMAIN][0]} if hasattr(self.commands,'ROUTES') else set(tool_names))
  for identifier in required_commands:
   if identifier not in actual_rows or identifier not in self.rows:raise ValueError('capability_missing: '+identifier)
   if actual_rows[identifier]['params']!=self.rows[identifier]['params']:raise ValueError('capability_mismatch: catalog_parameter_drift: '+identifier)
  for name in required_tools:
   if name not in actual_tools or name not in self.tools:raise ValueError('capability_missing: '+name)
   if actual_tools[name]['inputSchema']!=self.tools[name]['inputSchema']:raise ValueError('capability_mismatch: tool_schema_drift: '+name)
  if enabled_command is not None and (enabled_command not in actual_rows or actual_rows[enabled_command].get('enabled') is not True):raise ValueError('command_disabled: '+enabled_command)
  proof={'commands':required_commands,'tools':required_tools,'actualCommandsSha256':current['commandsSha256'],'actualToolsSha256':current['toolsSha256'],'enabledCommand':enabled_command,'status':'PASS'}
  self.checks.append(proof);return proof
