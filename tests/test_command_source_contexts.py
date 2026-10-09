"""命令前置条件源码必须与参数、资源及原始行范围共同绑定。"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class CommandSourceContextTests(unittest.TestCase):
 def module(self):
  path=ROOT/'scripts/command_source_contexts.py';self.assertTrue(path.is_file(),'missing command source-context binding entry');return load('source_context_test',path)
 def fixture(self,root):
  a=load('acceptance_fixture',ROOT/'scripts/command_acceptance.py');skill=root/'skill';(skill/'scripts').mkdir(parents=True);(skill/'references').mkdir();(skill/'scripts/entry.py').write_text('resource')
  catalog={'runtimeSha256':'a'*64,'upstreamCommit':'b'*40,'commands':[{'id':'file.new','params':'{}','ownerSkill':'photocraft-cli-project'}]};(skill/'references/command-coverage.json').write_text(json.dumps(catalog));(skill/'references/desktop-command-snapshot.json').write_text('{"commands":[]}');index=a.scaffold(skill)
  upstream=root/'upstream';path=upstream/'crates/engine/src/commands.rs';path.parent.mkdir(parents=True);raw=b'CommandSpec { id: "file.new", params: "{}", enabled: always }\nfn always(_: &Session) -> Result<(), String> { Ok(()) }\n';path.write_bytes(raw);file_sha=hashlib.sha256(raw).hexdigest()
  def loc(start,end):return {'path':'crates/engine/src/commands.rs','sha256':file_sha,'lineStart':start,'lineEnd':end,'spanSha256':hashlib.sha256(b''.join(raw.splitlines(keepends=True)[start-1:end])).hexdigest()}
  profile={'schema':'photocraft-command-source-contexts/v1','upstreamRepository':'https://github.com/storytold/photocraft','upstreamCommit':'b'*40,'patchSha256':'c'*64,'skillSourceSha256':index['sourceSha256'],'runtimeSha256':'a'*64,'files':{'crates/engine/src/commands.rs':file_sha},'commands':[{'id':'file.new','commandContractSha256':index['commands'][0]['commandContractSha256'],'registration':loc(1,1),'macroDefinition':None,'generationSource':None,'enabledExpression':'always','predicateDefinitions':[loc(2,2)]}]}
  return a,skill,upstream,index,profile
 def test_binding_preserves_unknown_review_and_execution_and_original_index(self):
  m=self.module()
  with tempfile.TemporaryDirectory() as td:
   a,skill,upstream,index,profile=self.fixture(Path(td));before=copy.deepcopy(index);updated,report=m.bind(index,profile,skill,upstream)
   self.assertEqual(index,before);self.assertEqual(updated['commands'],before['commands']);self.assertEqual(report['upstreamBytes'],'VERIFIED');self.assertEqual(report['sourceBoundCommands'],1);self.assertEqual(a.validate(updated,skill,Path(td))['acceptedCommands'],0)
   report=m.check(updated,profile,skill,None);self.assertEqual(report['upstreamBytes'],'NOT_VERIFIED');self.assertEqual(report['nativeExecution'],'NOT_RUN')
 def test_source_edit_and_span_edit_are_rejected_without_touching_index(self):
  m=self.module()
  with tempfile.TemporaryDirectory() as td:
   a,skill,upstream,index,profile=self.fixture(Path(td));before=copy.deepcopy(index)
   bad=copy.deepcopy(profile);bad['commands'][0]['registration']['spanSha256']='0'*64
   with self.assertRaises(ValueError):m.bind(index,bad,skill,upstream)
   (upstream/'crates/engine/src/commands.rs').write_bytes(b'changed')
   with self.assertRaises(ValueError):m.bind(index,profile,skill,upstream)
   self.assertEqual(index,before)
 def test_missing_duplicate_and_wrong_parameter_contract_are_rejected(self):
  m=self.module()
  with tempfile.TemporaryDirectory() as td:
   a,skill,upstream,index,profile=self.fixture(Path(td))
   for kind in ('missing','duplicate','params'):
    bad=copy.deepcopy(profile)
    if kind=='missing':bad['commands']=[]
    elif kind=='duplicate':bad['commands'].append(copy.deepcopy(bad['commands'][0]))
    else:bad['commands'][0]['commandContractSha256']='0'*64
    with self.subTest(kind=kind),self.assertRaises(ValueError):m.bind(index,bad,skill,upstream)
 def test_unregistered_predicate_and_path_escape_are_rejected(self):
  m=self.module()
  with tempfile.TemporaryDirectory() as td:
   a,skill,upstream,index,profile=self.fixture(Path(td))
   for kind in ('predicate','path'):
    bad=copy.deepcopy(profile)
    if kind=='predicate':bad['commands'][0]['enabledExpression']='invented_enabled'
    else:bad['commands'][0]['registration']['path']='../outside'
    with self.subTest(kind=kind),self.assertRaises(ValueError):m.bind(index,bad,skill,upstream)
 def test_changed_profile_or_skill_resources_cannot_reuse_binding(self):
  m=self.module()
  with tempfile.TemporaryDirectory() as td:
   a,skill,upstream,index,profile=self.fixture(Path(td));updated,_=m.bind(index,profile,skill,upstream);changed=copy.deepcopy(profile);changed['patchSha256']='d'*64
   with self.assertRaises(ValueError):m.check(updated,changed,skill,None)
   (skill/'scripts/entry.py').write_text('changed')
   with self.assertRaises(ValueError):m.check(updated,profile,skill,None)
 def test_cli_writes_new_copy_and_refuses_overwrite_without_modifying_input(self):
  import subprocess,sys
  self.module()
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);a,skill,upstream,index,profile=self.fixture(root)
   old=root/'index.json';facts=root/'profile.json';out=root/'bound.json'
   old.write_text(json.dumps(index));facts.write_text(json.dumps(profile));before=old.read_bytes()
   args=[sys.executable,'-I','-B',str(ROOT/'scripts/command_source_contexts.py'),'bind','--index',str(old),'--profile',str(facts),'--skill-root',str(skill),'--source-root',str(upstream),'--output',str(out)]
   first=subprocess.run(args,capture_output=True,text=True);self.assertEqual(first.returncode,0,first.stdout+first.stderr);payload=out.read_bytes()
   second=subprocess.run(args,capture_output=True,text=True);self.assertEqual(second.returncode,1);self.assertEqual(out.read_bytes(),payload);self.assertEqual(old.read_bytes(),before)
   args[4]='check';args=args[:-2];args[6]=str(out)
   check=subprocess.run(args,capture_output=True,text=True);self.assertEqual(check.returncode,0,check.stdout+check.stderr);self.assertEqual(json.loads(check.stdout)['upstreamBytes'],'VERIFIED')
 def test_source_symlink_is_rejected(self):
  m=self.module()
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);a,skill,upstream,index,profile=self.fixture(root);source=upstream/'crates/engine/src/commands.rs';outside=root/'outside.rs';outside.write_bytes(source.read_bytes());source.unlink();source.symlink_to(outside)
   with self.assertRaises(ValueError):m.bind(index,profile,skill,upstream)
 def test_source_resource_refresh_drops_obsolete_profile_binding(self):
  m=self.module()
  with tempfile.TemporaryDirectory() as td:
   a,skill,upstream,index,profile=self.fixture(Path(td));updated,_=m.bind(index,profile,skill,upstream)
   (skill/'scripts/entry.py').write_text('new resource')
   refreshed,_=a.refresh(updated,skill,Path(td));self.assertNotIn('sourceContextProfile',refreshed);self.assertEqual(refreshed['commands'][0]['contextCoverage'],'UNREVIEWED')
if __name__=='__main__':unittest.main()
