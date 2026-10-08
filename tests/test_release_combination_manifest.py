"""完整发行组合摘要及来源冲突拒绝；只修改自有测试副本。"""
import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load():
 spec=importlib.util.spec_from_file_location('release_combination_manifest',ROOT/'scripts/release_combination.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class ReleaseCombinationManifestTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)/'plugin';shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('.git','__pycache__','node_modules','.codegraph'))
  self.source=Path(self.temp.name)/'source';self.source.mkdir();(self.source/'.claude-plugin').mkdir();source=json.loads((ROOT/'skills.lock.json').read_text())['sources'][0];version=source['ref'].removeprefix('v');runtime=json.loads((ROOT/'skills/photocraft-use/scripts/runtime.lock.json').read_text())
  (self.source/'.claude-plugin/plugin.json').write_text(json.dumps({'name':'photocraft-skills','repository':'https://github.com/full-aigc-skills/photocraft-skills','version':version}));(self.source/'skill-suite.json').write_text(json.dumps({'version':version,'pluginId':'photocraft','runtimeVersion':runtime['resolvedVersion'],'skills':[{'name':n} for n in source['skills']]}));shutil.copytree(ROOT/'skills',self.source/'skills',ignore=shutil.ignore_patterns('photocraft-harness'));(self.source/'runtime').mkdir();shutil.copyfile(ROOT/'runtime/history/photocraft-cli-upstream-0.2.0.lock.json',self.source/'runtime/official-runtime-0.2.0.lock.json')
 def change(self,relative,key,value,source=False):
  p=(self.source if source else self.root)/relative;d=json.loads(p.read_text());d[key]=value;p.write_text(json.dumps(d))
 def test_current_roles_have_deterministic_bound_summary(self):
  m=load();a=m.check(self.root,self.source);b=m.check(self.root,self.source);self.assertEqual(a['status'],'PASS',a);self.assertEqual(a['combinationSha256'],b['combinationSha256']);self.assertEqual(a['combination']['skills']['version'],json.loads((ROOT/'skills.lock.json').read_text())['sources'][0]['ref'].removeprefix('v'));self.assertFalse(a['acceptance']['hostModelRouting']);self.assertEqual(len(a['combination']['skills']['sha256']),13)
 def test_source_same_role_version_conflict_is_rejected(self):
  self.change('skill-suite.json','version','0.0.0',source=True);d=load().check(self.root,self.source);self.assertEqual(d['status'],'FAIL');self.assertIn('source_suite_version_mismatch',d['errors']);self.assertIsNone(d['combinationSha256'])
 def test_tampered_source_or_installed_skill_is_rejected(self):
  for root,error in [(self.source,'source_skill_digest_mismatch'),(self.root,'installed_skill_digest_mismatch')]:
   p=root/'skills/photocraft-cli/SKILL.md';old=p.read_bytes();p.write_bytes(old+b'\nchanged\n');d=load().check(self.root,self.source);self.assertEqual(d['status'],'FAIL');self.assertTrue(any(x.startswith(error) for x in d['errors']));p.write_bytes(old)
 def test_stale_chinese_current_paragraph_is_rejected(self):
  p=self.root/'README.zh-CN.md';t=p.read_text();version=json.loads((self.root/'plugin.json').read_text())['version'];p.write_text(t.replace('当前插件：`'+version+'`','当前插件：`0.0.0`',1));self.assertIn('README.zh-CN.md: current_version_paragraph_mismatch',load().check(self.root,self.source)['errors'])
 def test_maintained_runtime_cannot_be_described_as_official_current_cli(self):
  p=self.root/'README.md';p.write_text(p.read_text()+'\nFirst use installs the pinned official CLI into user-level storage.\n');self.assertIn('README.md: current_runtime_provenance_mismatch',load().check(self.root,self.source)['errors'])
 def test_public_protocol_payload_and_historical_runtime_are_bound(self):
  m=load();a=m.check(self.root,self.source);p=self.root/'contracts/artcraft/craft-task-v1.json';p.write_text(p.read_text()+'\n');self.assertIn('contract_payload_digest_mismatch: taskSchema',m.check(self.root,self.source)['errors']);p=self.root/'runtime/history/photocraft-cli-upstream-0.2.0.lock.json';self.change(str(p.relative_to(self.root)),'repository','https://example.invalid/runtime');self.assertIn('historical_runtime_authority_mismatch',m.check(self.root,self.source)['errors'])

 def test_source_package_authority_conflict_is_rejected(self):
  self.change('.claude-plugin/plugin.json','repository','https://example.invalid/forged',source=True);self.assertIn('source_package_authority_mismatch',load().check(self.root,self.source)['errors'])
