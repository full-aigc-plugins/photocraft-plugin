import copy
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
ROOT=Path(__file__).resolve().parents[1]
def module():
 spec=importlib.util.spec_from_file_location('candidate_reuse',ROOT/'scripts/verify_candidate.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class CandidateReuseTests(unittest.TestCase):
 def fixture(self):return {'schema':'photocraft-candidate-validation/v1','status':'PASS','sourceUnchanged':True,'source':{'skills':{'sha256':'a'*64}},'layers':{'native':True,'desktop':True},'checks':[{'name':'skills-tests','status':'PASS','exitCode':0,'tests':{'total':201,'passed':201,'failed':0,'skipped':0}}]}
 def test_matching_native_layer_and_source_can_reuse_only_skills_check(self):
  m=module();check=m.reusable_skills_check(self.fixture(),{'sha256':'a'*64},SimpleNamespace(native=True,desktop=True));self.assertEqual(check['tests']['passed'],201)
 def test_changed_source_or_layer_cannot_reuse_old_pass(self):
  m=module()
  with self.assertRaisesRegex(ValueError,'reuse_source_mismatch'):m.reusable_skills_check(self.fixture(),{'sha256':'b'*64},SimpleNamespace(native=True,desktop=True))
  old=self.fixture();old['layers']['desktop']=False
  with self.assertRaisesRegex(ValueError,'reuse_layer_mismatch'):m.reusable_skills_check(old,{'sha256':'a'*64},SimpleNamespace(native=True,desktop=True))
 def test_failed_unstable_or_skipped_native_baseline_is_refused(self):
  m=module()
  for key in ('status','sourceUnchanged','skipped'):
   old=self.fixture()
   if key=='status':old[key]='FAIL'
   elif key=='sourceUnchanged':old[key]=False
   else:old['checks'][0]['tests'][key]=1
   with self.subTest(key=key),self.assertRaises(ValueError):m.reusable_skills_check(old,{'sha256':'a'*64},SimpleNamespace(native=True,desktop=True))
if __name__=='__main__':unittest.main()
