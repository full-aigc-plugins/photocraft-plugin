#!/usr/bin/env python3
"""校验固定公共协议引用；可额外核对所有者 Git 对象的真实摘要。"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
PATHS = {'taskSpec': 'openspec/changes/establish-v1-plugin/specs/craft-task-protocol/spec.md', 'artifactSpec': 'openspec/changes/establish-v1-plugin/specs/craft-artifact-protocol/spec.md', 'taskSchema': 'schemas/craft-task-v1.json', 'artifactSchema': 'schemas/craft-artifact-v1.json'}
def validate_reference(value, authority=None):
    """返回结构及可选真实 Git 内容校验错误，不修改任何文件。"""
    errors = []
    if not isinstance(value, dict):
        return ['contract reference must be an object']
    source = value.get('source', {})
    files = value.get('files', {})
    if not isinstance(source, dict) or not isinstance(files, dict):
        return ['contract source/files must be objects']
    sha = source.get('sha', '')
    ref = source.get('ref', '')
    if value.get('status') != 'fixed-protocol-authority-reference' or value.get('owner') != 'full-aigc-plugins/artcraft-plugin':
        errors.append('contract authority owner/status mismatch')
    if not isinstance(sha, str) or not re.fullmatch(r'[a-f0-9]{40}', sha):
        errors.append('contract authority needs immutable commit')
    if not isinstance(ref, str) or not re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+(?:-[a-zA-Z0-9.]+)?', ref):
        errors.append('contract authority needs release tag')
    if source.get('repository') != 'https://github.com/full-aigc-plugins/artcraft-plugin.git':
        errors.append('contract authority repository mismatch')
    if value.get('protocols') != {'task':'craft-task/v1', 'artifact':'craft-artifact/v1'}:
        errors.append('contract protocol versions mismatch')
    if set(files) != set(PATHS):
        errors.append('contract authority file set mismatch')
    for key, path in PATHS.items():
        item = files.get(key, {})
        if not isinstance(item, dict):
            errors.append('contract file must be an object: '+key)
            continue
        digest = item.get('sha256', '')
        if item.get('path') != path or not isinstance(digest, str) or not re.fullmatch(r'[a-f0-9]{64}', digest):
            errors.append('contract path/digest invalid: '+key)
        if item.get('url') != 'https://github.com/full-aigc-plugins/artcraft-plugin/blob/'+str(sha)+'/'+path:
            errors.append('contract URL is not pinned: '+key)
    if authority is not None and not errors:
        try:
            commit = subprocess.check_output(['git','rev-parse','refs/tags/'+ref+'^{commit}'], cwd=authority, text=True).strip()
            if commit != sha:
                errors.append('contract tag/commit mismatch')
            for key, path in PATHS.items():
                data = subprocess.check_output(['git','show',sha+':'+path], cwd=authority)
                if hashlib.sha256(data).hexdigest() != files[key]['sha256']:
                    errors.append('contract content digest mismatch: '+key)
        except (OSError, subprocess.CalledProcessError) as exc:
            errors.append('contract authority unavailable: '+str(exc))
    return errors
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--authority', type=Path)
    parser.add_argument('--reference', type=Path, default=Path(__file__).resolve().parents[1]/'docs/contracts-reference.json')
    args = parser.parse_args()
    errors = validate_reference(json.loads(args.reference.read_text()), args.authority)
    print(json.dumps({'status':'failed' if errors else 'passed','scope':'git-content' if args.authority else 'reference-structure-only','errors':errors}, indent=2))
    raise SystemExit(bool(errors))
