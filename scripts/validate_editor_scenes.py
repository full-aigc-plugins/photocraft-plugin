#!/usr/bin/env python3
"""校验未发布场景候选与编辑器配置；不将其冒充既有发行快照。"""
from pathlib import Path
import hashlib
import json
import re


def candidate_names(root):
    root = Path(root)
    manifest = root / 'scenario-candidates.json'
    if not manifest.exists():
        return set()
    data = json.loads(manifest.read_text())
    if data.get('status') != 'local-unreleased' or not isinstance(data.get('skills'), list):
        raise ValueError('invalid_scene_candidate')
    names = set()
    for entry in data['skills']:
        name = entry['name']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or name in names:
            raise ValueError('invalid_scene_name')
        folder = root / 'skills' / name
        path = folder / 'SKILL.md'
        if folder.is_symlink() or path.is_symlink():
            raise ValueError('scene_symlink')
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry['sha256']:
            raise ValueError('scene_digest_mismatch: ' + name)
        text = raw.decode()
        if not text.startswith('---\nname: ' + name + '\n') or len(text.splitlines()) >= 500:
            raise ValueError('invalid_scene_skill')
        names.add(name)
    return names


def validate(root):
    root = Path(root)
    names = candidate_names(root)
    plugin = json.loads((root/'plugin.json').read_text())['name']
    server = plugin + '-editor'
    portable = json.loads((root/'mcp.json').read_text())
    if portable['$schema'] != 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json':
        raise ValueError('invalid_mcp_schema')
    if portable['mcpServers'].get(server) != {'type':'stdio','command':'node','args':['${PLUGIN_ROOT}/ui/dist/adapter.mjs']}:
        raise ValueError('invalid_portable_editor')
    codex = json.loads((root/'.codex-plugin/plugin.json').read_text())
    if codex.get('mcpServers') != './.codex-plugin/mcp.json':
        raise ValueError('missing_codex_mcp')
    if server not in json.loads((root/'.mcp.json').read_text())['mcpServers']:
        raise ValueError('missing_codex_editor')
    claude = json.loads((root/'.claude-plugin/plugin.json').read_text())
    if claude.get('skills') != './skills/':
        raise ValueError('missing_claude_skills')
    return {'plugin':plugin,'localCandidateSkills':len(names),'package':'PASS','hostAcceptance':'NOT_INFERRED'}


if __name__ == '__main__':
    print(json.dumps(validate(Path(__file__).resolve().parents[1]), ensure_ascii=False))
