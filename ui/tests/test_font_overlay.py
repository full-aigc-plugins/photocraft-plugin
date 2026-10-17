from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'runtime/prepare-fonts.py'


class FontOverlayTest(unittest.TestCase):
    def test_pinned_font_reaches_document_and_ui(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build = root / 'crates/text/build.rs'
            build.parent.mkdir(parents=True)
            build.write_text('if !d.is_empty() && !wasm {}')
            ui = root / 'crates/ui-egui/src'
            ui.mkdir(parents=True)
            (ui / 'lib.rs').write_text('')
            (ui / 'theme.rs').write_text('ctx.set_fonts(fonts);')
            result = subprocess.run(['python3', str(SCRIPT), str(root), 'photocraft'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn('&& !wasm', build.read_text())
            self.assertIn('crate::craft_fonts::definitions(fonts)', (ui / 'theme.rs').read_text())
            self.assertIn('CRAFT_CJK_FONT', (ui / 'craft_fonts.rs').read_text())
