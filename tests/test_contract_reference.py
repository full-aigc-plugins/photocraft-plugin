"""固定公共协议来源不能退回分支引用或接受内容漂移。"""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
class ContractReferenceTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('contract_reference', ROOT/'scripts/contract_reference.py')
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.value = json.loads((ROOT/'docs/contracts-reference.json').read_text())
    def test_current_reference(self):
        self.assertEqual(self.module.validate_reference(self.value), [])
    def test_floating_or_inconsistent_identity_rejected(self):
        for field, bad in [('sha', 'main'), ('ref', 'main'), ('repository', 'https://github.com/other/repo.git')]:
            value = copy.deepcopy(self.value)
            value['source'][field] = bad
            self.assertTrue(self.module.validate_reference(value), field)
    def test_bad_digest_path_and_url_rejected(self):
        for field, bad in [('sha256', 'bad'), ('path', '../secret'), ('url', 'https://github.com/full-aigc-plugins/artcraft-plugin/blob/main/schema.json')]:
            value = copy.deepcopy(self.value)
            value['files']['taskSchema'][field] = bad
            self.assertTrue(self.module.validate_reference(value), field)
    def test_missing_file_or_protocol_rejected(self):
        value = copy.deepcopy(self.value)
        del value['files']['artifactSpec']
        self.assertTrue(self.module.validate_reference(value))
        value = copy.deepcopy(self.value)
        value['protocols']['task'] = 'craft-task/v2'
        self.assertTrue(self.module.validate_reference(value))
    def test_authority_bytes_and_tag_are_checked(self):
        def content(args, **kwargs):
            if args[1] == 'rev-parse':
                return self.value['source']['sha']+'\n'
            return b'changed protocol content'
        with patch.object(self.module.subprocess, 'check_output', side_effect=content):
            errors = self.module.validate_reference(self.value, ROOT)
        self.assertEqual(len(errors), 4)
        self.assertTrue(all('content digest mismatch' in error for error in errors))
        def moved_tag(args, **kwargs):
            if args[1] == 'rev-parse':
                return '0'*40+'\n'
            return b'changed protocol content'
        with patch.object(self.module.subprocess, 'check_output', side_effect=moved_tag):
            self.assertIn('contract tag/commit mismatch', self.module.validate_reference(self.value, ROOT))
