"""Check the pinned public runtime inventory; optionally audit downloaded bytes."""
import argparse
import hashlib
import json
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def audit(files_dir=None):
    from scripts.build_site import _PYODIDE_VERSION

    manifest = json.loads(Path(__file__).with_name('pyodide-runtime-manifest.json').read_text(encoding='utf-8'))
    assert manifest['version'] == _PYODIDE_VERSION
    assert manifest['base_url'] == f'https://cdn.jsdelivr.net/pyodide/v{_PYODIDE_VERSION}/full/'
    assert manifest['packages'] == ['pydantic', 'pyyaml']
    assets = manifest['assets']
    core = {'pyodide.mjs', 'pyodide.asm.js', 'pyodide.asm.wasm', 'python_stdlib.zip', 'pyodide-lock.json'}
    assert core <= assets.keys()
    for name, asset in assets.items():
        assert name in core or re.fullmatch(r'[A-Za-z0-9_.-]+\.whl', name)
        assert re.fullmatch('[a-f0-9]{64}', asset['sha256'])
        assert isinstance(asset['bytes'], int) and asset['bytes'] > 0
    if files_dir:
        for name, asset in assets.items():
            data = (files_dir / name).read_bytes()
            assert len(data) == asset['bytes'], f'{name}: size mismatch'
            assert hashlib.sha256(data).hexdigest() == asset['sha256'], f'{name}: hash mismatch'
        lock = json.loads((files_dir / 'pyodide-lock.json').read_text(encoding='utf-8'))['packages']
        visited = set()

        def visit(name):
            name = name.replace('_', '-')
            if name in visited:
                return
            visited.add(name)
            package = lock[name]
            assert assets[package['file_name']]['sha256'] == package['sha256']
            for dependency in package['depends']:
                visit(dependency)

        for name in manifest['packages']:
            visit(name)
        assert set(assets) == core | {lock[name]['file_name'] for name in visited}
    return {'version': manifest['version'], 'assets': len(assets),
            'bytes': sum(asset['bytes'] for asset in assets.values()),
            'downloaded_bytes_and_dependency_closure_checked': bool(files_dir)}


def download(directory):
    audit()
    manifest = json.loads(Path(__file__).with_name('pyodide-runtime-manifest.json').read_text(encoding='utf-8'))
    directory.mkdir(parents=True, exist_ok=True)

    def retain(item):
        name, asset = item
        target = directory / name
        if target.exists():
            data = target.read_bytes()
            if len(data) == asset['bytes'] and hashlib.sha256(data).hexdigest() == asset['sha256']:
                return
        for attempt in range(2):
            try:
                with urllib.request.urlopen(manifest['base_url'] + name, timeout=60) as response:
                    data = response.read(asset['bytes'] + 1)
                assert len(data) == asset['bytes'], f'{name}: downloaded size mismatch'
                assert hashlib.sha256(data).hexdigest() == asset['sha256'], f'{name}: downloaded hash mismatch'
                target.write_bytes(data)
                return
            except (OSError, AssertionError):
                if attempt:
                    raise
                time.sleep(0.25)

    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(retain, manifest['assets'].items()))
    return audit(directory)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--files-dir', type=Path)
    parser.add_argument('--download-dir', type=Path)
    args = parser.parse_args()
    print(json.dumps(download(args.download_dir) if args.download_dir else audit(args.files_dir)))
