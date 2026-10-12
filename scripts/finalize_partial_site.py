"""Finalize an explicit HTML release batch without scanning the public tree."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path, PurePosixPath

from scripts.shared_clinical_reader import _ReaderBinding, _PRESERVED_PREFIXES, synchronize_reader_source_hashes
from scripts.site_head import finalize_public_page, geo_lang_payload, geo_lang_url

_HEADER = re.compile(r'<header class="top-bar site-header">.*?</header>|<!-- shared-site-header:start -->.*?<!-- shared-site-header:end -->', re.S)


def _relative(value: str) -> str:
    if not isinstance(value, str) or not value or any(c in value for c in '\\:%?#'):
        raise ValueError('Expected an unescaped relative HTML path')
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or str(path) != value or path.suffix != '.html':
        raise ValueError(f'Invalid relative HTML path: {value}')
    if path.name.lower().startswith(_PRESERVED_PREFIXES):
        raise ValueError('Preserved clinical pages cannot belong to a partial release')
    return value


def _target(root: Path, relative: str) -> Path:
    target = (root / relative).resolve()
    if not target.is_relative_to(root) or target.name.lower().startswith(_PRESERVED_PREFIXES):
        raise ValueError('Page must remain inside the public directory')
    return target


def _clinical_body(text: str) -> str:
    match = re.search(r'<body\b[^>]*>(.*?)</body>', text, re.S | re.I)
    if match is None or not re.search(r'<head\b', text, re.I):
        raise ValueError('Partial release pages require complete HTML documents')
    return _HEADER.sub('', match[1])


def finalize_batch(output: Path, pages: list[str], *, available_paths: set[str], write: bool = False) -> dict:
    """Validate the entire batch and reader dependencies before replacing pages.

    Originals outside the manifest are read only when a selected reader binds
    to them. They must be inventoried and are never finalized or written.
    Dry runs leave the public output untouched. Fingerprints prove identity,
    never clinical correctness or review approval.
    """
    root = Path(output).resolve()
    if not isinstance(pages, list) or not pages or not all(isinstance(p, str) for p in pages) or len(pages) != len(set(pages)):
        raise ValueError('Manifest must be a nonempty list of unique HTML paths')
    paths = [_relative(p) for p in pages]
    targets = {p: _target(root, p) for p in paths}
    if len(set(targets.values())) != len(targets):
        raise ValueError('Manifest aliases the same file more than once')
    inventory = set(available_paths) | set(paths)
    originals = {p: target.read_bytes() for p, target in targets.items()}
    prepared = {}
    dependencies = {}
    for relative, raw in originals.items():
        before = raw.decode('utf-8').replace('\r\n', '\n')
        after = finalize_public_page(before, path=relative, available_paths=inventory)
        if _clinical_body(before) != _clinical_body(after):
            raise ValueError(f'Clinical body changed during finalization: {relative}')
        prepared[relative] = after
        binding = _ReaderBinding(after)
        for href in binding.sources:
            if not href.startswith(('/kb/', '/cases/', '/handbook/', '/plans/', '/disease/')):
                raise ValueError('Reader original must be a public clinical document')
            source = _relative(href.removeprefix('/'))
            if source not in inventory:
                raise ValueError(f'Reader original is not inventoried: {source}')
            if _target(root, source) == targets[relative]:
                raise ValueError('Reader cannot bind to itself')
            if source not in prepared and source not in paths:
                dependencies[source] = _target(root, source).read_bytes()

    # Use the existing binding validator on a private shadow, so malformed
    # readers or missing originals fail before any published file changes.
    with tempfile.TemporaryDirectory(prefix='.partial-site-', dir=root.parent) as directory:
        shadow = Path(directory)
        if not shadow.resolve().is_relative_to(root.parent):
            raise ValueError('Private preparation directory must remain inside the output parent')
        for relative, text in prepared.items():
            dest = shadow / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding='utf-8', newline='\n')
        for relative, raw in dependencies.items():
            dest = shadow / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
        bindings = synchronize_reader_source_hashes(shadow, pages=[shadow / p for p in paths])
        result_bytes = {p: (shadow / p).read_text(encoding='utf-8').encode('utf-8') for p in paths}

    requires_geo = any(f'src="{geo_lang_url()}"' in text for text in prepared.values())
    if requires_geo and (root / geo_lang_url().lstrip('/')).read_bytes() != geo_lang_payload():
        raise ValueError('Versioned geographic-language asset does not match the builder')
    if any('data-shared-site-header' in text for text in prepared.values()):
        for asset in ['shared-site-header.js', 'header.css']:
            if not (root / asset).is_file():
                raise ValueError(f'Missing shared header asset: {asset}')

    changed = [p for p in paths if result_bytes[p] != originals[p]]
    if write:
        # Detect concurrent edits before the first mutation. Stage all output
        # files first; restore replaced files if a filesystem operation fails.
        if any(targets[p].read_bytes() != originals[p] for p in paths):
            raise ValueError('A selected page changed during preparation; retry from current files')
        for relative, raw in dependencies.items():
            if _target(root, relative).read_bytes() != raw:
                raise ValueError('A reader original changed during preparation')
        staged = {}
        replaced = []
        try:
            for p in changed:
                with tempfile.NamedTemporaryFile(dir=targets[p].parent, prefix='.partial-page-', suffix='.tmp', delete=False) as file:
                    staged[p] = Path(file.name)
                    file.write(result_bytes[p])
            for p in changed:
                staged[p].replace(targets[p])
                replaced.append(p)
        except Exception:
            for p in replaced:
                targets[p].write_bytes(originals[p])
            raise
        finally:
            for temp in staged.values():
                temp.unlink(missing_ok=True)
    return {'pages': len(paths), 'changed': changed, 'reader_bindings': bindings,
            'written': write, 'clinical_body_preserved': True, 'clinical_approval': False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True, help='JSON list of relative HTML paths')
    parser.add_argument('--inventory', type=Path, help='Optional JSON list of all available public HTML paths')
    parser.add_argument('--write', action='store_true', help='Apply the verified batch; default is a dry run')
    args = parser.parse_args()
    pages = json.loads(args.manifest.read_text(encoding='utf-8'))
    if not isinstance(pages, list) or not all(isinstance(p, str) for p in pages):
        parser.error('Manifest must be a JSON list of HTML paths')
    if args.inventory:
        inventory = json.loads(args.inventory.read_text(encoding='utf-8'))
        if not isinstance(inventory, list) or not all(isinstance(p, str) for p in inventory):
            parser.error('Inventory must be a JSON list of HTML paths')
        available = set(inventory)
    else:
        repo = Path(__file__).resolve().parents[1]
        tracked = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', 'HEAD'], cwd=repo, text=True)
        available = {p[5:] for p in tracked.splitlines() if p.startswith('docs/') and p.endswith('.html')}
    print(json.dumps(finalize_batch(args.output, pages, available_paths=available, write=args.write), indent=2))


if __name__ == '__main__':
    main()
