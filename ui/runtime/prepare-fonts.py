"""Add the distribution's pinned Chinese font to archived upstream Web builds.

Use the apps' existing CRAFT_FONTS document databases. Keep a fallback in every
egui font stack, including stacks rebuilt after a theme or language change.
No locale persistence or translation catalog is changed here.
"""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
name = sys.argv[2]
runtime = Path(__file__).resolve().parent


def replace(path, old, new):
    p = root / path
    source = p.read_text()
    if source.count(old) != 1:
        raise RuntimeError(f'{name}: font overlay anchor is not unique: {path}: {old}')
    p.write_text(source.replace(old, new, 1))


if name != 'photocraft':
    raise RuntimeError('This font overlay only supports PhotoCraft')
# 插件按摘要分块交付资源，编译输入显式包含文档与界面中文字体。
replace('crates/text/build.rs', '!d.is_empty() && !wasm', '!d.is_empty()')

ui = root / 'crates/ui-egui/src'
count = 0
for p in ui.rglob('*.rs'):
    source = p.read_text()
    # Pinned upstream calls each occupy a single line; greedy capture retains
    # nested constructor arguments. Fail below if an unhandled call appears.
    source, n = re.subn(r'\.set_fonts\(([^\n]+)\);',
                        r'.set_fonts(crate::craft_fonts::definitions(\1));', source)
    if n:
        p.write_text(source)
        count += n
    for line in source.splitlines():
        if '.set_fonts(' in line and 'crate::craft_fonts::definitions(' not in line:
            raise RuntimeError(f'{name}: unhandled font stack: {p}: {line}')
if not count:
    raise RuntimeError(f'{name}: no egui font installation found')
(ui / 'craft_fonts.rs').write_text((runtime / 'rust/fonts.rs').read_text())
with (ui / 'lib.rs').open('a') as f:
    f.write('\nmod craft_fonts;\n')
print(f'{name}: Chinese fallback added to {count} font stack installations')
