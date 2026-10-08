"""验收复用只能复用未变化且独立通过的首用用例，不能复用失败的追加场景。"""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FixedDomainVerifierTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('fixed_domain', ROOT / 'scripts/verify_fixed_domain.py')
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def fixture(self, root):
        m = self.module
        source = root / 'source/tests'
        source.mkdir(parents=True)
        previous = root / 'previous'
        previous.mkdir()
        driver = previous / 'driver.py'
        driver.write_bytes((ROOT / 'scripts/verify_fixed_domain.py').read_bytes())
        proof = previous / 'project.pcraft'
        proof.write_bytes(b'fixture only, not a native acceptance result')
        cases = []
        for name, filename, *unused in m.CASES:
            test = source / (filename + '.py')
            test.write_text('# fixture driver\n')
            cases.append({'case': name, 'status': 'PASS', 'tests': 1, 'failures': 0, 'errors': 0, 'skipped': 0, 'driverSha256': m.digest(test)})
        data = {'status': 'FAIL', 'additionalError': 'fixture failed outside first-use cases', 'driverSha256': m.digest(driver), 'skillSource': {'digests': {'skill': 'a' * 64}}, 'cases': cases, 'artifacts': {'project.pcraft': {'sha256': m.digest(proof), 'bytes': proof.stat().st_size}}}
        report = root / 'report.json'
        report.write_text(json.dumps(data))
        return report, previous, driver, root / 'source', data

    def test_source_identity_ignores_only_git_ignored_cache_not_authored_resources(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / '.gitignore').write_text('__pycache__/\n')
            script = root / 'skills/fixture/scripts/operation.py'
            script.parent.mkdir(parents=True)
            script.write_text('original\n')
            before = self.module.authored_skill_hash(root, 'fixture')
            cache = script.parent / '__pycache__/ignored.pyc'
            cache.parent.mkdir()
            cache.write_bytes(b'local ignored cache')
            self.assertEqual(self.module.authored_skill_hash(root, 'fixture'), before)
            script.write_text('changed behavior\n')
            self.assertNotEqual(self.module.authored_skill_hash(root, 'fixture'), before)

    def test_only_independently_passed_first_use_cases_can_be_reused(self):
        with tempfile.TemporaryDirectory() as temporary:
            report, previous, driver, source, data = self.fixture(Path(temporary))
            result = self.module.reusable_first_use(report, previous, driver, source, {'skill': 'a' * 64})
            self.assertEqual(len(result), len(self.module.CASES))
            self.assertTrue(all(c['status'] == 'PASS' for c in result))

    def test_failed_skipped_missing_or_changed_cases_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            report, previous, driver, source, data = self.fixture(Path(temporary))
            for change in ('failed', 'skipped', 'missing', 'source'):
                altered = copy.deepcopy(data)
                if change == 'failed': altered['cases'][0]['status'] = 'FAIL'
                elif change == 'skipped': altered['cases'][0]['skipped'] = 1
                elif change == 'missing': altered['cases'].pop()
                else: altered['skillSource']['digests']['skill'] = 'b' * 64
                report.write_text(json.dumps(altered))
                with self.subTest(change=change), self.assertRaisesRegex(ValueError, 'reuse_'):
                    self.module.reusable_first_use(report, previous, driver, source, {'skill': 'a' * 64})

    def test_changed_test_driver_artifact_or_runner_is_rejected(self):
        for change in ('test', 'artifact', 'runner', 'escaping-artifact'):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temporary:
                report, previous, driver, source, data = self.fixture(Path(temporary))
                if change == 'test': next((source / 'tests').glob('*.py')).write_text('# changed\n')
                elif change == 'artifact': (previous / 'project.pcraft').write_bytes(b'changed')
                elif change == 'escaping-artifact':
                    data['artifacts'] = {'../outside': next(iter(data['artifacts'].values()))}
                    report.write_text(json.dumps(data))
                else:
                    driver.write_text(driver.read_text().replace("os.environ['CRAFT_' + flag] = '1'", "os.environ['CRAFT_' + flag] = '0'"))
                    data['driverSha256'] = self.module.digest(driver)
                    report.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, 'reuse_'):
                    self.module.reusable_first_use(report, previous, driver, source, {'skill': 'a' * 64})
