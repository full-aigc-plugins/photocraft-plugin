import hashlib
import json
from pathlib import Path
import runpy
import tempfile
import unittest
candidate_names = runpy.run_path(str(Path(__file__).resolve().parents[1]/'scripts/validate_editor_scenes.py'))['candidate_names']
class SceneCandidateTests(unittest.TestCase):
    def test_candidate_is_separate_and_detects_drift(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);folder=root/'skills/photo-scene';folder.mkdir(parents=True)
            raw=b'---\nname: photo-scene\ndescription: example\n---\n'
            skill=folder/'SKILL.md';skill.write_bytes(raw)
            (root/'scenario-candidates.json').write_text(json.dumps({'status':'local-unreleased','skills':[{'name':'photo-scene','sha256':hashlib.sha256(raw).hexdigest()}]}))
            self.assertEqual(candidate_names(root),{'photo-scene'})
            skill.write_bytes(raw+b'changed')
            with self.assertRaisesRegex(ValueError,'scene_digest_mismatch'):candidate_names(root)
    def test_release_claim_is_not_accepted_as_local_candidate(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'scenario-candidates.json').write_text(json.dumps({'status':'published','skills':[]}))
            with self.assertRaisesRegex(ValueError,'invalid_scene_candidate'):candidate_names(root)
if __name__=='__main__':unittest.main()
