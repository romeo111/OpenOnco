"""Small language readers sharing immutable original clinical documents.

Avoid duplicating five large clinical trees on free static hosting. Interactive
tool pages still use complete templates; these readers are for source documents.
"""
import hashlib
import html
import re
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath

from scripts.additional_locale_copy import NOTICES
from scripts.site_nav import render_top_bar
from scripts.clinical_asset_versions import clinical_runtime_url


_PRESERVED_PREFIXES = ('verified-crc-l2-tucatinib-trastuzumab-crc', 'verified-prostate-l2-cabazitaxel-mcrpc')
_ATTR = re.compile(r'''([^\s=/>]+)(?:\s*=\s*("[^"]*"|'[^']*'|[^\s>]+))?''')


class _ReaderBinding(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.offsets = [0]
        self.offsets.extend(match.end() for match in re.finditer('\n', source))
        self.sources = []
        self.digests = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'iframe' and 'data-shared-clinical-source' in values:
            self.sources.append(values.get('src'))
        if tag != 'meta' or values.get('name') != 'translation-source-sha256':
            return
        raw = self.get_starttag_text()
        start = re.match(r'<\s*meta\b', raw, re.I).end()
        candidates = [match for match in _ATTR.finditer(raw, start) if match[1].lower() == 'content']
        if len(candidates) != 1 or not candidates[0][2]:
            self.digests.append(None)
            return
        match = candidates[0]
        value = match[2]
        quoted = value[0] in ('"', "'")
        begin, end = match.span(2)
        line, column = self.getpos()
        offset = self.offsets[line - 1] + column
        self.digests.append((offset + begin + int(quoted), offset + end - int(quoted), values.get('content')))

    handle_startendtag = handle_starttag


def synchronize_reader_source_hashes(output_dir, *, pages=None):
    """Bind readers to final original HTML after SEO and whitespace changes.

    This proves file identity only, never clinical approval. Validate the whole
    requested batch before writing. Preserved files and sources are not read.
    """
    root = Path(output_dir).resolve()
    inventory = pages if pages is not None else root.rglob('*.html')
    changes, digests = [], {}
    checked = preserved = 0
    for candidate in inventory:
        page = Path(candidate)
        if page.name.startswith(_PRESERVED_PREFIXES):
            preserved += 1
            continue
        page = page.resolve()
        if not page.is_relative_to(root):
            raise ValueError('Reader must remain in the public output directory')
        if page.name.startswith(_PRESERVED_PREFIXES):
            preserved += 1
            continue
        text = page.read_text(encoding='utf-8')
        if 'data-shared-clinical-source' not in text:
            continue
        binding = _ReaderBinding(text)
        if not binding.sources:
            continue  # A script string or an example is not an actual reader.
        if len(binding.sources) != 1 or len(binding.digests) != 1 or binding.digests[0] is None:
            raise ValueError(f'Ambiguous reader binding: {page.relative_to(root)}')
        href = binding.sources[0]
        if not isinstance(href, str) or not href.startswith(('/kb/', '/cases/', '/handbook/', '/plans/', '/disease/')) or not href.endswith('.html') or any(char in href for char in '\\?#%:') or '..' in PurePosixPath(href).parts:
            raise ValueError(f'Invalid original path: {page.relative_to(root)}')
        original = root / href.lstrip('/')
        if original.name.startswith(_PRESERVED_PREFIXES):
            preserved += 1
            continue
        original = original.resolve()
        if original.name.startswith(_PRESERVED_PREFIXES):
            preserved += 1
            continue
        if not original.is_relative_to(root) or original == page:
            raise ValueError(f'Original must be a separate public document: {page.relative_to(root)}')
        begin, end, declared = binding.digests[0]
        if not isinstance(declared, str) or not re.fullmatch('[a-f0-9]{64}', declared):
            raise ValueError(f'Invalid original fingerprint: {page.relative_to(root)}')
        if original not in digests:
            digests[original] = hashlib.sha256(original.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
        expected = digests[original]
        checked += 1
        if declared != expected:
            changes.append((page, text[:begin] + expected + text[end:]))
    for page, updated in changes:
        page.write_text(updated, encoding='utf-8')
    return {'checked': checked, 'updated': len(changes), 'preserved': preserved}


def render_shared_reader(source: str, locale: str, path: str, title: str, *, runtime_assets=None) -> str:
    # Paths come from the builder's existing public source inventory, never a
    # request parameter or an external destination.
    if (not path.endswith('.html') or '\\' in path
            or not path.startswith(('kb/', 'cases/', 'handbook/', 'plans/', 'disease/'))
            or '..' in PurePosixPath(path).parts):
        raise ValueError('Shared clinical reader requires an inventoried relative HTML path')
    notice, english_original, _, ukrainian_original, unspecified_original = NOTICES[locale]
    declaration = re.search(r'<html\b[^>]*\blang=["\']([a-z]{2,3}(?:-[a-z0-9]{2,8})*)["\']', source, re.I)
    source_language = declaration[1].lower() if declaration else 'und'
    original = english_original if source_language.split('-')[0] == 'en' else ukrainian_original if source_language.split('-')[0] == 'uk' else unspecified_original
    digest = hashlib.sha256(source.encode('utf-8')).hexdigest()
    escaped_title, escaped_path = html.escape(title), html.escape('/' + path, quote=True)
    assets = runtime_assets or {}
    runtime = assets.get('runtime', clinical_runtime_url())
    catalog = assets.get('clinical-translations.json', f'/{locale}/clinical-translations.json')
    return f'''<!doctype html>
<html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escaped_title}</title><link rel="stylesheet" href="/header.css?v=layout-20261011">
<meta name="translation-review" content="pending_clinical_review"><meta name="translation-source-sha256" content="{digest}">
<style>body{{margin:0;background:#f7faf9;color:#173d2b}}.clinical-reader{{width:100%;margin:0}}.reader-notice{{max-width:1100px;margin:16px auto;padding:12px 18px;font:16px/1.5 system-ui}}.clinical-reader iframe{{display:block;width:100%;min-height:600px;border:0}}.reader-loading{{padding:16px;text-align:center;font:16px system-ui}}</style>
</head><body>
<div data-reader-header><noscript><a href="/{locale}/">OpenOnco</a> · <a href="/">English</a> · <a href="/ukr/">Українська</a></noscript></div>
<main class="clinical-reader"><aside class="reader-notice" role="note"><strong>{html.escape(notice)}</strong> <a href="{escaped_path}" lang="{source_language}" hreflang="{source_language}" data-original-source>{html.escape(original)}</a></aside>
<iframe data-shared-clinical-source src="{escaped_path}" title="{escaped_title}"></iframe>
<noscript><p class="reader-loading"><a href="{escaped_path}">{html.escape(original)}</a></p></noscript></main>
<script src="/shared-clinical-reader.js" data-locale="{locale}" data-source="{escaped_path}" defer></script>
<script src="{runtime}" data-locale="{locale}" data-catalog="{catalog}" defer></script>
</body></html>\n'''


def write_reader_assets(output_dir: Path, locale: str) -> None:
    (output_dir / locale / 'shared-header.fragment').write_text(render_top_bar('', locale), encoding='utf-8')
    (output_dir / 'shared-clinical-reader.js').write_text(Path(__file__).with_name('shared-clinical-reader.js').read_text(encoding='utf-8'), encoding='utf-8', newline='\n')
