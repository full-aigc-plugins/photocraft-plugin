import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
def module():
 spec=importlib.util.spec_from_file_location('release_combination',ROOT/'scripts/check_release_identity.py');value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value
class ReleaseCombinationTests(unittest.TestCase):
 def test_current_plugin_combination_and_active_runtime_are_consistent(self):
  self.assertEqual(module().check(ROOT)['errors'],[])
 def test_stale_active_lock_and_version_conflict_are_refused(self):
  m=module();plugin={'id':'photocraft','version':'0.1.0-dev.38'};source={'package':'full-aigc-skills/photocraft-skills','ref':'v0.1.0-dev.34','sha':'a'*40}
  runtime={'artifact':'photocraft-cli','resolvedVersion':'0.2.0-craft.1','repository':'https://github.com/full-aigc-skills/photocraft-skills','artifacts':{'darwin-arm64':{'binarySha256':'b'*64}}}
  self.assertIn('active_runtime_lock_mismatch',m.validate(plugin,source,runtime,{**runtime,'resolvedVersion':'0.2.0'},plugin))
  self.assertIn('harness_version_mismatch',m.validate(plugin,source,runtime,runtime,{**plugin,'version':'0.1.0-dev.1'}))
 def test_maintained_repository_cannot_claim_official_runtime(self):
  m=module();plugin={'version':'candidate'};source={'package':'photocraft-skills','ref':'v0.1.0-dev.34','sha':'a'*40};runtime={'artifact':'photocraft-cli','repository':'https://github.com/full-aigc-skills/photocraft-skills','resolvedVersion':'0.2.0-craft.1'}
  self.assertIn('maintained_runtime_variant_missing',m.validate(plugin,source,runtime,runtime,plugin))
  invalid={**runtime,'runtimeVariant':'maintained','upstreamRepository':'https://github.com/storytold/photocraft','upstreamCommit':'main'}
  self.assertIn('maintained_runtime_provenance_missing',m.validate(plugin,source,invalid,invalid,plugin))
