"""索引刷新必须使旧结果失效、保留历史，不能覆盖人工上下文。"""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
def module():
 spec=importlib.util.spec_from_file_location('command_index_refresh',ROOT/'scripts/command_acceptance.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class CommandIndexRefreshTests(unittest.TestCase):
 def fixture(self,root):
  skill=root/'skill';(skill/'scripts').mkdir(parents=True);(skill/'references').mkdir();(skill/'scripts/entry.py').write_text('original')
  catalog={'runtimeSha256':'a'*64,'commands':[{'id':'file.new','params':'{}','ownerSkill':'photocraft-cli-project'},{'id':'file.close','params':'{}','ownerSkill':'photocraft-cli-project'}]}
  (skill/'references/command-coverage.json').write_text(json.dumps(catalog));(skill/'references/desktop-command-snapshot.json').write_text(json.dumps({'commands':[{'id':'file.new'},{'id':'file.close'}]}))
  return skill
 def refresh(self,m,index,skill):
  self.assertTrue(callable(getattr(m,'refresh',None)),'missing public index refresh capability')
  return m.refresh(index,skill)
 def test_unchanged_index_preserves_review_and_does_not_add_history(self):
  m=module()
  with tempfile.TemporaryDirectory() as td:
   skill=self.fixture(Path(td));index=m.scaffold(skill);index['commands'][0]['contexts'][0]['reason']='Human reviewed: requires blank document'
   before=copy.deepcopy(index);updated,report=self.refresh(m,index,skill)
   self.assertEqual(updated,before);self.assertEqual(index,before);self.assertFalse(report['sourceChanged']);self.assertEqual(report['invalidatedContexts'],0)
 def test_resource_change_invalidates_results_and_keeps_bound_historical_record(self):
  m=module()
  with tempfile.TemporaryDirectory() as td:
   skill=self.fixture(Path(td));index=m.scaffold(skill);row=index['commands'][0];row['contextCoverage']='REVIEWED';context=row['contexts'][0];context.update(status='FAIL',reason='Actual command failed on this input',evidence={'files':{'failure':{'path':'run/failure.json','sha256':'b'*64}},'inputs':[]});context['requirements']['document']='Blank 16x16 RGB document'
   before=copy.deepcopy(index);(skill/'scripts/entry.py').write_text('changed')
   updated,report=self.refresh(m,index,skill);new=updated['commands'][0]['contexts'][0]
   self.assertEqual(index,before);self.assertEqual(new['status'],'NOT_RUN');self.assertIsNone(new['evidence']);self.assertEqual(new['requirements']['document'],'Blank 16x16 RGB document');self.assertEqual(updated['commands'][0]['contextCoverage'],'REVIEWED');self.assertEqual(report['invalidatedContexts'],1)
   old=new['history'][-1];self.assertEqual(old['sourceSha256'],before['sourceSha256']);self.assertEqual(old['context'],before['commands'][0]['contexts'][0]);self.assertEqual(old['commandContractSha256'],before['commands'][0]['commandContractSha256'])
   self.assertEqual(m.validate(updated,skill,Path(td))['acceptedCommands'],0)
   again,next_report=self.refresh(m,updated,skill);self.assertEqual(again,updated);self.assertEqual(next_report['invalidatedContexts'],0)
 def test_contract_or_registration_change_requires_review_and_preserves_retired_commands(self):
  m=module()
  with tempfile.TemporaryDirectory() as td:
   skill=self.fixture(Path(td));index=m.scaffold(skill);index['commands'][0]['contextCoverage']='REVIEWED';index['commands'][0]['contexts'][0]['requirements']['document']='Previous human contract'
   catalog=json.loads((skill/'references/command-coverage.json').read_text());catalog['commands']=[{'id':'file.new','params':'{"width":u32}','ownerSkill':'photocraft-cli-project'},{'id':'edit.undo','params':'{}','ownerSkill':'photocraft-cli'}];(skill/'references/command-coverage.json').write_text(json.dumps(catalog));(skill/'references/desktop-command-snapshot.json').write_text('{"commands":[]}')
   updated,report=self.refresh(m,index,skill)
   self.assertEqual(report['addedCommands'],['edit.undo']);self.assertEqual(report['removedCommands'],['file.close']);self.assertEqual(report['changedCommands'],['file.new'])
   self.assertEqual(updated['commands'][0]['contextCoverage'],'UNREVIEWED');self.assertTrue(all(v=='UNKNOWN' for v in updated['commands'][0]['contexts'][0]['requirements'].values()));self.assertEqual(updated['retiredCommands'][0]['command']['id'],'file.close');self.assertEqual(updated['retiredCommands'][0]['sourceSha256'],index['sourceSha256']);self.assertEqual(updated['commands'][1]['contextCoverage'],'UNREVIEWED')
 def test_corrupt_source_or_duplicate_command_refused_without_mutating_index(self):
  m=module()
  with tempfile.TemporaryDirectory() as td:
   skill=self.fixture(Path(td));index=m.scaffold(skill)
   for mutation in ('source','duplicate'):
    bad=copy.deepcopy(index)
    if mutation=='source':bad['sourceFiles']['scripts/entry.py']='c'*64
    else:bad['commands'].append(copy.deepcopy(bad['commands'][0]))
    before=copy.deepcopy(bad)
    self.assertTrue(callable(getattr(m,'refresh',None)),'missing public index refresh capability')
    with self.assertRaises(ValueError):m.refresh(bad,skill)
    self.assertEqual(bad,before)
 def test_unchanged_invalid_pass_is_refused_instead_of_echoed_as_valid(self):
  m=module()
  with tempfile.TemporaryDirectory() as td:
   skill=self.fixture(Path(td));index=m.scaffold(skill);index['commands'][0]['contexts'][0]['status']='PASS'
   with self.assertRaises(ValueError):m.refresh(index,skill)
 def test_duplicate_context_without_distinct_identity_is_rejected(self):
  m=module()
  with tempfile.TemporaryDirectory() as td:
   skill=self.fixture(Path(td));index=m.scaffold(skill);index['commands'][0]['contexts'].append(copy.deepcopy(index['commands'][0]['contexts'][0]));(skill/'scripts/entry.py').write_text('changed')
   with self.assertRaises(ValueError):m.refresh(index,skill)
 def test_corrupt_cli_input_creates_no_new_output(self):
  m=module()
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);skill=self.fixture(root);value=m.scaffold(skill);value['sourceSha256']='0'*64;index=root/'index.json';index.write_text(json.dumps(value));before=index.read_bytes();output=root/'new.json'
   result=subprocess.run([sys.executable,'-I','-B',str(ROOT/'scripts/command_acceptance.py'),'refresh','--skill-root',str(skill),'--index',str(index),'--output',str(output)],capture_output=True,text=True)
   self.assertNotEqual(result.returncode,0);self.assertFalse(output.exists());self.assertEqual(index.read_bytes(),before)
 def test_invalid_unicode_in_old_context_creates_no_partial_new_index(self):
  m=module()
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);skill=self.fixture(root);value=m.scaffold(skill);value['commands'][0]['contexts'][0]['requirements']['document']='\ud800';index=root/'index.json';index.write_text(json.dumps(value));before=index.read_bytes();(skill/'scripts/entry.py').write_text('changed');output=root/'new.json'
   result=subprocess.run([sys.executable,'-I','-B',str(ROOT/'scripts/command_acceptance.py'),'refresh','--skill-root',str(skill),'--index',str(index),'--output',str(output)],capture_output=True,text=True)
   self.assertNotEqual(result.returncode,0);self.assertFalse(output.exists(),'invalid Unicode must be rejected before creating output');self.assertEqual(index.read_bytes(),before)
 def test_cli_refresh_writes_new_copy_and_refuses_existing_output(self):
  m=module()
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);skill=self.fixture(root);index=root/'index.json';index.write_text(json.dumps(m.scaffold(skill)));original=index.read_bytes();(skill/'scripts/entry.py').write_text('changed');output=root/'new.json'
   args=[sys.executable,'-I','-B',str(ROOT/'scripts/command_acceptance.py'),'refresh','--skill-root',str(skill),'--index',str(index),'--output',str(output)]
   result=subprocess.run(args,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stdout+result.stderr);self.assertEqual(index.read_bytes(),original);self.assertEqual(json.loads(output.read_text())['sourceSha256'],m.source(skill)['sha256']);created=output.read_bytes()
   result=subprocess.run(args,capture_output=True,text=True);self.assertNotEqual(result.returncode,0);self.assertEqual(output.read_bytes(),created);self.assertEqual(index.read_bytes(),original)
class LockedIndexIntegrationTests(unittest.TestCase):
 def test_checked_in_index_matches_actual_skill_and_rejects_changed_execution_resource(self):
  index=ROOT/'docs/evidence/optimization/command-acceptance/current-index.json'
  def check(skill):return subprocess.run([sys.executable,'-I','-B',str(ROOT/'scripts/command_acceptance.py'),'check','--skill-root',str(skill),'--index',str(index)],capture_output=True,text=True)
  result=check(ROOT/'skills/photocraft-use');self.assertEqual(result.returncode,0,result.stdout+result.stderr);report=json.loads(result.stdout);self.assertEqual(report['commands'],755);self.assertEqual(report['acceptedCommands'],0);self.assertEqual(report['fullCommandAcceptance'],'NOT_RUN')
  with tempfile.TemporaryDirectory() as td:
   skill=Path(td)/'skill';shutil.copytree(ROOT/'skills/photocraft-use',skill);path=skill/'scripts/commands.py';path.write_bytes(path.read_bytes()+b'\n# changed execution resource\n');before=path.read_bytes();result=check(skill)
   self.assertNotEqual(result.returncode,0);self.assertIn('stale_source_or_snapshot',result.stdout);self.assertEqual(path.read_bytes(),before)
if __name__=='__main__':unittest.main()
