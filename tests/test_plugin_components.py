"""宿主入口必须指向已打包技能，并且会话钩子不能启动原生实例。"""

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PluginComponentsTests(unittest.TestCase):
    def test_each_discovered_skill_has_a_direct_command(self):
        portable = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        host = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual((host["name"], host["version"]), (portable["name"], portable["version"]))
        self.assertEqual(host["commands"], "./com.anthropic.claude-code/commands/")
        self.assertEqual(host["hooks"], "./com.anthropic.claude-code/hooks/hooks.json")
        skills = {path.name for path in (ROOT / "skills").iterdir() if (path / "SKILL.md").is_file()}
        command_files = list((ROOT / "com.anthropic.claude-code/commands").glob("*.md"))
        self.assertEqual({path.stem for path in command_files}, skills)
        for path in command_files:
            body = path.read_text(encoding="utf-8")
            self.assertTrue(body.startswith("---\n"), path)
            self.assertIn(f"skills: {path.stem}\n", body, path)
            self.assertIn(f"`{path.stem}`", body, path)
            self.assertIn("$ARGUMENTS", body, path)

    def test_session_hook_is_once_per_session_and_advisory(self):
        config = json.loads((ROOT / "com.anthropic.claude-code/hooks/hooks.json").read_text(encoding="utf-8"))
        self.assertEqual(set(config["hooks"]), {"SessionStart"})
        entries = config["hooks"]["SessionStart"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["matcher"], "startup|resume")
        self.assertEqual(len(entries[0]["hooks"]), 1)
        self.assertEqual(entries[0]["hooks"][0]["type"], "command")
        self.assertIn("session_guidance.py", entries[0]["hooks"][0]["command"])
        script = ROOT / "com.anthropic.claude-code/hooks/session_guidance.py"
        run = subprocess.run([sys.executable, "-I", "-B", str(script)], input='{"source":"resume"}',
                             capture_output=True, text=True, timeout=3)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("复用", run.stdout)
        self.assertIn("原实例", run.stdout)


if __name__ == "__main__":
    unittest.main()
