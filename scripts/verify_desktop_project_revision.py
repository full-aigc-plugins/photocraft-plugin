"""在真实独占桌面进程中区分未保存编辑与已保存工程冲突，不把只读观察当写入权。"""
import argparse,hashlib,importlib.util,json,secrets,socket,subprocess,tempfile,time
from pathlib import Path

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def verify(skill,runtime_home,node):
 scripts=skill/'scripts';baseline={str(p.relative_to(skill)):sha(p) for p in skill.rglob('*') if p.is_file()};lock=json.loads((scripts/'runtime.lock.json').read_text());desktop_lock=json.loads((scripts/'desktop.lock.json').read_text())
 cli=load(scripts/'bootstrap.py','revision_bootstrap').install(lock,runtime_home);desktop=load(scripts/'desktop.py','revision_desktop_install').install(desktop_lock,runtime_home);owned=load(scripts/'desktop_session.py','revision_owned_session');cases=[]
 with tempfile.TemporaryDirectory(prefix='photo-desktop-revision-') as td:
  root=Path(td).resolve();output=root/'owned';output.mkdir();token=root/'token';token.write_text(secrets.token_hex(32));token.chmod(0o600)
  with socket.socket() as probe:probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
  argv=[cli['executable'],'mcp','--bridge','127.0.0.1:'+str(port),'--control-token-file',str(token),'--automation-read-root',str(output),'--automation-write-root',str(output)]
  session=owned.OwnedSession(argv,desktop,'photocraft',output,port,token)
  with session as connection:
   def call(tool,args):
    reply=connection.request('tools/call',{'name':tool,'arguments':args});assert not reply.get('isError'),reply;return json.loads(next(c['text'] for c in reply['content'] if c['type']=='text'))
   call('doc_new',{'width':32,'height':32,'name':'User project'})
   layer=call('command_run',{'id':'layer.new.layer','params':{'name':'Original'}})['layer'];call('doc_save',{'path':'user.pcraft'});project=output/'user.pcraft';original=sha(project)
   clean=call('session_list',{})['session'];doc=next(d for d in clean['documents'] if d['index']==clean['active']);assert doc['dirty'] is False
   # 模拟用户在实际 GUI 引擎中修改；不通过 headless 替代桌面内存状态。
   call('command_run',{'id':'layer.renameLayer','params':{'layer':layer,'name':'USER EDIT'}})
   dirty=call('session_list',{})['session'];dirty_doc=next(d for d in dirty['documents'] if d['index']==dirty['active']);assert dirty_doc['dirty'] is True and dirty_doc['revision']>doc['revision'];assert sha(project)==original
   def check(name,expected):
    state=root/('state-'+name);request={'idempotencyKey':name,'brief':'Preserve user changes','plan':{'document':{'width':32,'height':32},'operations':[]},'mutableProject':str(project),'expectedProjectSha256':original,'output':str(root/('delivery-'+name)),'authorization':{'ref':'explicit-test-only','writeRoot':str(root)},'budget':{'deadline':int(time.time()*1000)+120000,'maxRevisions':0,'reserveBytes':0}}
    path=root/(name+'.json');path.write_text(json.dumps(request));reply=subprocess.run([node,str(Path(__file__).with_name('verify_project_revision.ts')),str(path),str(state),str(skill),expected],capture_output=True,text=True,timeout=30);assert reply.returncode==0,reply.stdout+reply.stderr;return json.loads(reply.stdout)
   refusal=check('unsaved','mutable_desktop_execution_not_supported');assert call('session_list',{})['session']==dirty;facts=call('doc_inspect',{});assert next(l for l in facts['layers'] if l['id']==layer)['name']=='USER EDIT';cases.append({'case':'unsaved-user-edit','diskBytesUnchanged':True,'desktopRevisionBefore':doc['revision'],'desktopRevisionAfter':dirty_doc['revision'],'desktopDirty':True,'userMemoryPreserved':True,**refusal})
   call('doc_save',{'path':'user.pcraft'});saved=sha(project);assert saved!=original;saved_state=call('session_list',{})['session'];assert next(d for d in saved_state['documents'] if d['index']==saved_state['active'])['dirty'] is False
   refusal=check('saved','revision_conflict');assert call('session_list',{})['session']==saved_state and sha(project)==saved;cases.append({'case':'saved-user-edit','previousProjectSha256':original,'newProjectSha256':saved,'desktopDirty':False,'userMemoryPreserved':True,**refusal})
  assert session.stopped and session.listener_verified
 assert baseline=={str(p.relative_to(skill)):sha(p) for p in skill.rglob('*') if p.is_file()}
 return {'schema':'photocraft-desktop-project-revision/v1','status':'PASS','platform':'darwin-arm64','runtimeVersion':lock['resolvedVersion'],'runtimeSha256':cli['binarySha256'],'desktopVersion':desktop_lock['version'],'desktopBinarySha256':desktop_lock['binarySha256'],'cases':cases,'ownedProcessesStopped':session.stopped,'listenerOwnedByPID':session.listener_verified,'installedSkillUnchanged':True,'scope':'Real signed desktop GUI engine edited through existing control API, not human pointer interaction; saved revision conflict and unsaved-state refusal only','sharedMutableWriting':'NOT_RUN','closedTaskIds':[],'fullV1':'NOT_RUN'}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--skill-root',type=Path,required=True);parser.add_argument('--runtime-home',type=Path,required=True);parser.add_argument('--node',default='node');parser.add_argument('--evidence',type=Path,required=True);args=parser.parse_args();proof=verify(args.skill_root.resolve(),args.runtime_home.resolve(),args.node);proof['driverSha256']=sha(Path(__file__));args.evidence.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print('Actual desktop saved/unsaved project revision refusals:PASS')
