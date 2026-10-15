"""Extend existing sitemap inventory after a manifest-scoped partial release."""
import argparse
import gzip
import io
import json
from pathlib import Path
import re
import shutil
import tempfile
from xml.etree import ElementTree as ET

from scripts.finalize_partial_site import _relative, _target, _PRESERVED_PREFIXES
from scripts.site_head import _HeadDirectives, _page_url, SITE_BASE_URL, write_sitemap

NS = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
MAX_XML_BYTES = 50_000_000


def inventory(root):
    """Read only local sitemap metadata, never page bodies or remote shards."""
    index = ET.fromstring((root / 'sitemap.xml').read_bytes())
    trees = [index]
    if index.tag == '{' + NS['s'] + '}sitemapindex':
        trees = []
        for node in index.findall('s:sitemap/s:loc', NS):
            url = node.text or ''
            name = url.removeprefix(SITE_BASE_URL + '/')
            if not re.fullmatch(r'sitemap-part-[1-9][0-9]*\.xml\.gz', name):
                raise ValueError('Unexpected sitemap shard URL')
            path = root / name
            if not path.resolve().is_relative_to(root.resolve()):
                raise ValueError('Sitemap shard escapes output')
            with gzip.GzipFile(fileobj=io.BytesIO(path.read_bytes())) as archive:
                data = archive.read(MAX_XML_BYTES + 1)
            if len(data) > MAX_XML_BYTES:
                raise ValueError('Sitemap shard exceeds XML size limit')
            trees.append(ET.fromstring(data))
    paths = set()
    for tree in trees:
        if tree.tag != '{' + NS['s'] + '}urlset':
            raise ValueError('Expected sitemap urlset')
        for node in tree.findall('s:url/s:loc', NS):
            url = node.text or ''
            if not url.startswith(SITE_BASE_URL + '/'):
                raise ValueError('Sitemap contains an external URL')
            relative = url[len(SITE_BASE_URL) + 1:]
            if not relative or relative.endswith('/'):
                relative += 'index.html'
            relative = _relative(relative)
            if _page_url(relative) != url:
                raise ValueError('Sitemap URL is not canonical')
            paths.add(relative)
    if not paths:
        raise ValueError('Existing sitemap inventory is empty')
    return paths


def update(root, manifest, *, write=False):
    root = root.resolve()
    if not isinstance(manifest, list) or not manifest:
        raise ValueError('Expected a nonempty page manifest')
    paths = [_relative(value) for value in manifest]
    if len(set(paths)) != len(paths):
        raise ValueError('Duplicate manifest paths')
    # Validate every protected filename before opening any selected HTML.
    if any(Path(p).name.lower().startswith(_PRESERVED_PREFIXES) for p in paths):
        raise ValueError('Preserved page is outside partial sitemap scope')
    existing = inventory(root)
    accepted, excluded = set(), []
    for relative in paths:
        if relative == 'ukr/capabilities.html' or relative.startswith('review/') or Path(relative).name == '404.html':
            excluded.append(relative)
            continue
        head = _target(root, relative).read_text(encoding='utf-8').split('</head>', 1)[0]
        directives = _HeadDirectives()
        directives.feed(head)
        if (directives.noindex or directives.redirect_url
                or directives.canonical and directives.canonical != _page_url(relative)):
            excluded.append(relative)
        else:
            accepted.add(relative)
    additions = accepted - existing
    desired = existing | accepted
    with tempfile.TemporaryDirectory(prefix='.sitemap-preview-', dir=root.parent) as directory:
        preview = Path(directory)
        write_sitemap(preview, available_paths=desired)
        if inventory(preview) != desired:
            raise ValueError('Generated sitemap inventory differs from requested union')
        files = sorted(preview.glob('sitemap*'))
        changed = [p.name for p in files
                   if not (root / p.name).is_file() or (root / p.name).read_bytes() != p.read_bytes()]
        if write:
            # Stage every shard before changing metadata; publish index last.
            originals = {name: (root / name).read_bytes() if (root / name).exists() else None
                         for name in changed}
            staged, replaced = {}, []
            try:
                for name in changed:
                    with tempfile.NamedTemporaryFile(dir=root, prefix='.sitemap-', delete=False) as file:
                        staged[name] = Path(file.name)
                    shutil.copyfile(preview / name, staged[name])
                for name in sorted(changed, key=lambda name: name == 'sitemap.xml'):
                    staged[name].replace(root / name)
                    replaced.append(name)
            except Exception:
                for name in reversed(replaced):
                    if originals[name] is None:
                        (root / name).unlink(missing_ok=True)
                    else:
                        (root / name).write_bytes(originals[name])
                raise
            finally:
                for path in staged.values():
                    path.unlink(missing_ok=True)
    return {'existing_urls': len(existing), 'added': sorted(additions),
            'excluded': excluded, 'result_urls': len(desired), 'changed': changed,
            'written': write, 'html_changed': False, 'clinical_approval': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    print(json.dumps(update(args.output, json.loads(args.manifest.read_text(encoding='utf-8')),
                            write=args.write), indent=2))


if __name__ == '__main__':
    main()
