import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photocraft-use'
def module():
 spec=importlib.util.spec_from_file_location('command_acceptance',ROOT/'scripts/command_acceptance.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class CommandAcceptanceTests(unittest.TestCase):
 def test_inventory_preserves_every_command_and_never_promotes_catalog_to_pass(self):
  m=module();index=m.scaffold(SKILL);report=m.validate(index,SKILL,ROOT);self.assertEqual(report['commands'],755);self.assertEqual(report['acceptedCommands'],0);self.assertEqual(report['fullCommandAcceptance'],'NOT_RUN')
  for change in ('missing','duplicate','catalog-pass'):
   invalid=copy.deepcopy(index)
   if change=='missing':invalid['commands'].pop()
   elif change=='duplicate':invalid['commands'].append(invalid['commands'][0])
   else:invalid['commands'][0]['contexts'][0]['status']='PASS'
   with self.subTest(change=change),self.assertRaises(ValueError):m.validate(invalid,SKILL,ROOT)
 def test_snapshot_and_parameter_drift_are_rejected_without_rewriting_evidence(self):
  m=module();index=m.scaffold(SKILL)
  for field in ('sourceSha256','commandContractSha256'):
   invalid=copy.deepcopy(index)
   if field=='sourceSha256':invalid[field]='0'*64
   else:invalid['commands'][0][field]='0'*64
   before=json.dumps(invalid,sort_keys=True)
   with self.assertRaisesRegex(ValueError,'stale_'):m.validate(invalid,SKILL,ROOT)
   self.assertEqual(json.dumps(invalid,sort_keys=True),before)
 def test_not_applicable_requires_reason_and_does_not_reduce_acceptance_scope(self):
  m=module();index=m.scaffold(SKILL);context=index['commands'][0]['contexts'][0];context['status']='NOT_APPLICABLE'
  with self.assertRaisesRegex(ValueError,'applicability_reason_required'):m.validate(index,SKILL,ROOT)
  context['reason']='This empty session is not an applicable document context; other contexts remain required'
  result=m.validate(index,SKILL,ROOT);self.assertEqual(result['acceptedCommands'],0);self.assertEqual(result['commands'],755)
 def test_missing_context_and_unsupported_backend_cannot_supply_native_evidence(self):
  m=module();index=m.scaffold(SKILL)
  context=index['commands'][0]['contexts'][0];context['status']='PASS';context['requirements']={k:'Explicit test fixture context' for k in context['requirements']}
  with self.assertRaisesRegex(ValueError,'bound_native_evidence_required'):m.validate(index,SKILL,ROOT)
  missing=next(row for row in index['commands'] if not row['contexts'][1]['registered']);missing['contexts'][1]['status']='PASS';missing['contexts'][1]['requirements']={k:'Explicit context' for k in missing['contexts'][1]['requirements']};context['status']='NOT_RUN'
  with self.assertRaisesRegex(ValueError,'backend_not_registered'):m.validate(index,SKILL,ROOT)
 def test_bound_native_proof_is_accepted_only_with_current_context_and_business_assertions(self):
  m=module();index=m.scaffold(SKILL);row=index['commands'][0];context=row['contexts'][0];context['status']='PASS';context['requirements']={key:'Synthetic fixture, not production acceptance' for key in m.REQUIREMENTS}
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);files={}
   def write(key,value):
    path=root/key;path.write_bytes(m.encoded(value) if isinstance(value,dict) else value);files[key]={'path':key,'sha256':m.sha(path)}
   plan={'schema':'craft-command-plan/v1','operations':[{'command':row['id'],'params':{}}]};write('plan',plan);write('project',b'fixture original');write('revisionProject',b'fixture revision');write('preview',b'fixture image')
   snapshot=m.read(SKILL/'references/native-command-snapshot.json')
   contracts=sorted([{'id':item['id'],'params':item['params']}for item in snapshot['commands']],key=lambda item:item['id']);tools=sorted([{'name':item['name'],'inputSchema':item['inputSchema']}for item in snapshot['tools']],key=lambda item:item['name'])
   receipt={'schema':'craft-command-receipt/v1','result':'PASS','mode':'headless','planSha256':m.digest(json.dumps(plan,ensure_ascii=False,sort_keys=True,allow_nan=False).encode()),'catalogSha256':m.sha(SKILL/'references/command-coverage.json'),'runtimeSha256':index['runtimeSha256'],'steps':[{'command':row['id'],'state':'succeeded','phase':'reply_validated'}],'capabilitySnapshot':{'backend':'headless','binarySha256':index['runtimeSha256'],'sessionId':'fixture','commandsSha256':m.digest(m.encoded(contracts)),'toolsSha256':m.digest(m.encoded(tools))}}
   write('receipt',receipt)
   for key,project in [('nativeVerification','project'),('revisionVerification','revisionProject')]:write(key,{'schema':'photocraft-native-verification/v1','result':'PASS','projectSha256':files[project]['sha256'],'runtimeSha256':index['runtimeSha256']})
   assertions={'status':'PASS','commandId':row['id'],'contextSha256':m.digest(m.encoded(context['requirements'])),'sourceSha256':index['sourceSha256'],'planSha256':files['plan']['sha256'],'projectSha256':files['project']['sha256'],'previewSha256':files['preview']['sha256'],'revisionSha256':files['revisionProject']['sha256'],'inputsSha256':m.digest(m.encoded([])),'checks':[{'id':'fixture-result','expected':1,'actual':1}]};write('assertions',assertions);context['evidence']={'files':files,'inputs':[]}
   result=m.validate(index,SKILL,root);self.assertEqual(result['boundNativeContexts'],1);self.assertEqual(result['fullCommandAcceptance'],'NOT_RUN');self.assertEqual(result['sourceAuthenticity'],'NOT_PROVEN')
   context['requirements']['selection']='Different context'
   with self.assertRaisesRegex(ValueError,'assertion_binding_mismatch'):m.validate(index,SKILL,root)
   context['requirements']['selection']='Synthetic fixture, not production acceptance';assertions['checks'][0]['actual']=2;write('assertions',assertions)
   with self.assertRaisesRegex(ValueError,'business_assertions_required'):m.validate(index,SKILL,root)
 def test_evidence_path_escape_and_same_name_replacement_are_rejected(self):
  m=module()
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);path=root/'proof';path.write_text('original');ref={'path':'proof','sha256':m.sha(path)};self.assertEqual(m.proof_file(root,ref),path.resolve())
   path.write_text('replacement')
   with self.assertRaisesRegex(ValueError,'evidence_digest_mismatch'):m.proof_file(root,ref)
   with self.assertRaisesRegex(ValueError,'evidence_path_escape'):m.proof_file(root,{'path':'../outside','sha256':'a'*64})
if __name__=='__main__':unittest.main()
