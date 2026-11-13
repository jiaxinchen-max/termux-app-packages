#!/usr/bin/env python3
"""Verify the independent Hyprland catalog and optionally its downloaded assets."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'repository/hyprland'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def members(path):
    with tarfile.open(path, 'r:gz') as archive:
        result = {}
        for member in archive.getmembers():
            name = PurePosixPath(member.name)
            require(member.isfile() and not name.is_absolute() and '..' not in name.parts,
                    'Unsafe archive entry: ' + member.name)
            require(member.name not in result, 'Duplicate archive entry: ' + member.name)
            require(member.size <= 16 * 1024 * 1024, 'Oversized archive entry')
            result[member.name] = archive.extractfile(member).read()
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path)
    args = parser.parse_args()
    catalog_bytes = (BASE / 'components.json').read_bytes()
    catalog = json.loads(catalog_bytes)
    lock = json.loads((BASE / 'source-lock.json').read_text())
    require(catalog['schema'] == 1, 'Unknown catalog schema')
    require(set(catalog['runtimes']) == {'0.57.0-r7'}, 'Unexpected runtime identity')
    require(set(catalog['themes']) == {'classic-r7', 'm3ww-v1'}, 'Unexpected theme identities')
    require(catalog['runtimes'] == lock['runtimes'] and catalog['themes'] == lock['themes'],
            'Source lock differs from catalog')
    require(sha(catalog_bytes) == lock['catalog_sha256'], 'Catalog SHA-256 mismatch')
    for theme in catalog['themes'].values():
        require(theme['runtime_ids'] == ['0.57.0-r7'], 'Unsupported runtime/theme combination')
        require(theme['source'] == 'bundled', 'Unexpected theme installation source')
        require(theme['url'] == 'https://github.com/jiaxinchen-max/termux-app-packages/releases/download/'
                + lock['release'] + '/' + theme['asset'], 'Unexpected theme URL')
    if args.assets:
        require((args.assets / 'hyprland-components.json').read_bytes() == catalog_bytes,
                'Published catalog differs from repository')
        for theme_id, entry in catalog['themes'].items():
            path = args.assets / entry['asset']
            data = path.read_bytes()
            require(len(data) == entry['size'] and sha(data) == entry['archive_sha256'],
                    'Theme archive size/SHA mismatch: ' + theme_id)
            files = members(path)
            require(set(files) == set(entry['resource_files']), 'Resource list differs')
            manifest = files.pop('manifest.json')
            require(sha(manifest) == entry['manifest_sha256'], 'Manifest SHA mismatch')
            parsed = json.loads(manifest)
            require(parsed['schema'] == 1 and parsed['id'] == theme_id
                    and parsed['runtime_ids'] == entry['runtime_ids'], 'Invalid theme manifest')
            require(parsed['files'] == {n: sha(b) for n, b in files.items()},
                    'Manifest resource hashes differ')
        source = lock['source_overlay']
        path = args.assets / source['asset']
        data = path.read_bytes()
        require(len(data) == source['size'] and sha(data) == source['sha256'], 'Source SHA mismatch')
        require({n: sha(b) for n, b in members(path).items()} == lock['app_source_files_sha256'],
                'Source overlay file hashes differ')
        for name in ('source-lock.json', 'validation.json', 'README.md'):
            require((args.assets / name).read_bytes() == (BASE / name).read_bytes(),
                    'Published metadata differs: ' + name)
        for line in (args.assets / 'SHA256SUMS').read_text().splitlines():
            digest, name = line.split('  ', 1)
            require(Path(name).name == name, 'Invalid checksum filename')
            require(sha((args.assets / name).read_bytes()) == digest, 'Checksum differs: ' + name)
    print('Hyprland catalog' + (' and downloaded assets' if args.assets else '') + ' verified.')


if __name__ == '__main__':
    main()
