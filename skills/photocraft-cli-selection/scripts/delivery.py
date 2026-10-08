#!/usr/bin/env python3
"""只读核对 PhotoCraft 交付清单、依赖和交换身份；不安装运行时。"""
import argparse
import hashlib
import json
from pathlib import Path
import re

HEX = re.compile(r'[a-f0-9]{64}')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate_json_key: ' + key)
            result[key] = value
        return result
    def constant(value):
        raise ValueError('invalid_json_number: ' + value)
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs, parse_constant=constant)


def file_path(root, location):
    if (not isinstance(location, str) or not location or '\\' in location or ':' in location
            or '\x00' in location or Path(location).is_absolute()
            or any(part in ('', '.', '..') for part in location.split('/'))):
        raise ValueError('delivery_path_invalid')
    path = root
    for part in location.split('/'):
        path = path / part
        if path.is_symlink():
            raise ValueError('delivery_file_missing_or_escaping: ' + location)
    if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('delivery_file_missing_or_escaping: ' + location)
    return path


def validate_delivery(root, expected_manifest_sha256=None):
    """返回核验后的原清单；外部清单摘要可绑定已记录的版本，未提供时不证明来源真实性。"""
    root = Path(root).absolute()
    if root.is_symlink() or not root.is_dir():
        raise ValueError('delivery_directory_invalid')
    manifest_file = file_path(root, 'manifest.json')
    if expected_manifest_sha256 is not None:
        if (not isinstance(expected_manifest_sha256, str) or not HEX.fullmatch(expected_manifest_sha256)
                or sha(manifest_file) != expected_manifest_sha256):
            raise ValueError('delivery_manifest_checksum_mismatch')
    manifest_digest = sha(manifest_file)
    manifest = read_json(manifest_file)
    if (not isinstance(manifest, dict) or manifest.get('schema') != 'photocraft-delivery/v1'
            or not isinstance(manifest.get('files'), dict) or not manifest['files']
            or not isinstance(manifest.get('assets', {}), dict)
            or not isinstance(manifest.get('outputs'), list)):
        raise ValueError('delivery_manifest_invalid')
    files = manifest['files']
    if not {'project.pcraft', 'native.json', 'plan.json', 'operations.json', 'exchange-loss.json'}.issubset(files):
        raise ValueError('delivery_required_file_missing')
    for name, digest in files.items():
        path = file_path(root, name)
        if not isinstance(digest, str) or not HEX.fullmatch(digest):
            raise ValueError('delivery_digest_invalid')
        if sha(path) != digest:
            raise ValueError('delivery_file_checksum_mismatch: ' + name)
    for asset in manifest.get('assets', {}).values():
        if (not isinstance(asset, dict) or not isinstance(asset.get('path'), str) or asset.get('path') not in files
                or asset.get('sha256') != files[asset['path']]):
            raise ValueError('delivery_asset_identity_mismatch')
    if 'layoutVariant' in manifest:
        ref = manifest['layoutVariant']
        if (not isinstance(ref, dict) or ref.get('path') != 'layout-variant.json'
                or ref.get('sha256') != files.get('layout-variant.json')
                or 'layout-variant.json' not in files):
            raise ValueError('delivery_reference_identity_mismatch')
    loss_ref = manifest.get('lossReport')
    if (not isinstance(loss_ref, dict) or loss_ref.get('path') != 'exchange-loss.json'
            or loss_ref.get('sha256') != files['exchange-loss.json']):
        raise ValueError('delivery_loss_identity_mismatch')
    loss = read_json(root / 'exchange-loss.json')
    def identity(value, location):
        return isinstance(value, dict) and value.get('location') == location and value.get('sha256') == files.get(location)
    if (not isinstance(loss, dict) or loss.get('schema') != 'craft-exchange-loss/v1'
            or loss.get('pluginId') != 'photocraft'
            or not identity(loss.get('native'), 'project.pcraft')
            or not identity(loss.get('inspection'), 'native.json')
            or not isinstance(loss.get('outputs'), list)):
        raise ValueError('delivery_loss_identity_mismatch')
    if 'psdInspection' in loss and not identity(loss['psdInspection'], 'psd-inspection.json'):
        raise ValueError('delivery_loss_identity_mismatch')
    output_paths = []
    for output in manifest['outputs']:
        if not isinstance(output, dict) or not isinstance(output.get('path'), str) or output['path'] not in files:
            raise ValueError('delivery_output_identity_mismatch')
        output_paths.append(output['path'])
    if len(output_paths) != len(set(output_paths)) or len(loss['outputs']) != len(output_paths):
        raise ValueError('delivery_output_identity_mismatch')
    observed = set()
    for output in loss['outputs']:
        location = output.get('location') if isinstance(output, dict) else None
        if (location not in output_paths or location in observed or not identity(output, location)
                or output.get('role') != 'derivative' or output.get('nativeSubstitute') is not False):
            raise ValueError('delivery_loss_identity_mismatch')
        observed.add(location)
    if sha(manifest_file) != manifest_digest:
        raise ValueError('delivery_manifest_changed')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('delivery', type=Path)
    parser.add_argument('--expected-manifest-sha256')
    args = parser.parse_args()
    try:
        manifest = validate_delivery(args.delivery, args.expected_manifest_sha256)
        result = {'schema': 'photocraft-delivery-integrity/v1', 'result': 'PASS',
                  'manifestSha256': sha(args.delivery / 'manifest.json'),
                  'nativeSha256': manifest['files']['project.pcraft'], 'files': len(manifest['files']),
                  'scope': 'File and exchange identity only; not native reopening, external authorship or creative acceptance.'}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ValueError, OSError, TypeError, KeyError) as error:
        print(json.dumps({'result': 'FAIL', 'error': str(error)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
