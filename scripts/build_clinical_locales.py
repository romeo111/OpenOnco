"""Publish source-linked draft translations without changing clinical data or JS."""
import html
import hashlib
import json
import posixpath
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from scripts.site_locales import locale_href
from scripts.site_nav import render_top_bar
from scripts.site_translation_catalog import LANGUAGES, PAGES, ProseCollector, load_catalog, normalize, source_pages

NOTICES = {
    'es': ('Traducción preliminar: revisión clínica pendiente.', 'Consultar el original en inglés'),
    'pt': ('Tradução preliminar: revisão clínica pendente.', 'Consultar o original em inglês'),
    'de': ('Vorläufige Übersetzung: klinische Prüfung ausstehend.', 'Englisches Original ansehen'),
    'fr': ('Traduction provisoire : vérification clinique en attente.', 'Consulter l’original en anglais'),
}
VOID_TAGS = {'img', 'input', 'br', 'hr', 'meta', 'link', 'source', 'area', 'wbr'}
ORIGINAL_LABELS = {
    'es': 'Texto original en inglés conservado para verificación',
    'pt': 'Texto original em inglês preservado para verificação',
    'de': 'Englischer Originaltext zur Überprüfung beibehalten',
    'fr': 'Texte original anglais conservé pour vérification',
}

class LocalizedHTML(HTMLParser):
    def __init__(self, catalog, locale, source_path, available, style_assets=None):
        super().__init__(convert_charrefs=True)
        self.catalog, self.locale, self.source_path, self.available = catalog, locale, source_path, available
        self.parts, self.stack = [], []
        self.style_assets = style_assets
        self.shared_style_start = None
    def text(self, value):
        stripped = normalize(html.unescape(value))
        replacement = self.catalog.get(stripped)
        if (replacement is None or replacement == stripped) and len(stripped) > 180 and not any(t in {'head', 'title', 'option'} for t in self.stack):
            return f'<span class="translation-original-fragment" lang="en" data-original-source data-label="{html.escape(ORIGINAL_LABELS[self.locale], quote=True)}">{html.escape(value, quote=False)}</span>'
        if replacement is None:
            return html.escape(value, quote=False)
        left = re.match(r'^\s*', value).group()
        right = re.search(r'\s*$', value).group()
        return left + html.escape(replacement, quote=False) + right
    def link(self, value, *, localized=False):
        url = urlsplit(value)
        if url.scheme or url.netloc or not url.path:
            return value
        path = posixpath.normpath(url.path.lstrip('/') if url.path.startswith('/') else posixpath.join(posixpath.dirname(self.source_path), url.path))
        if url.path.endswith('/'):
            path += '/index.html'
        if localized and path in self.available:
            path = locale_href(path, self.locale)
        else:
            path = '/' + path.lstrip('/')
        return urlunsplit(('', '', path, url.query, url.fragment))
    def handle_starttag(self, tag, attrs):
        original_attrs = dict(attrs)
        if tag == 'style' and self.style_assets is not None and (not attrs or original_attrs == {'type': 'text/css'}):
            self.shared_style_start = len(self.parts)
        if tag == 'html' and 'lang' not in original_attrs:
            attrs = [*attrs, ('lang', self.locale)]
        changed = []
        for key, value in attrs:
            if tag == 'html' and key == 'lang':
                value = self.locale
            elif key in {'title', 'aria-label', 'placeholder', 'alt', 'data-step-label'} and value:
                value = self.catalog.get(normalize(value), value)
            elif tag == 'meta' and key == 'content' and original_attrs.get('name') == 'description':
                value = self.catalog.get(normalize(value), value)
            elif key == 'data-search' and value:
                # Keep original identifiers and synonyms searchable too.
                value += ' ' + self.catalog.get(normalize(value), '')
            elif key == 'href' and value:
                value = self.link(value, localized=tag == 'a')
            elif key == 'src' and value:
                value = self.link(value, localized=tag == 'iframe')
            changed.append(key if value is None else f'{key}="{html.escape(value, quote=True)}"')
        self.parts.append('<' + tag + (' ' + ' '.join(changed) if changed else '') + '>')
        if tag not in VOID_TAGS:
            self.stack.append(tag)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.parts[-1] = self.parts[-1][:-1] + '/>'
        if tag not in VOID_TAGS:
            self.stack.pop()
    def handle_endtag(self, tag):
        if tag == 'style' and self.shared_style_start is not None:
            css = ''.join(self.parts[self.shared_style_start + 1:])
            digest = hashlib.sha256(css.encode('utf-8')).hexdigest()
            self.style_assets[digest] = css
            self.parts[self.shared_style_start:] = [f'<link rel="stylesheet" href="/clinical-styles/{digest}.css">']
            self.shared_style_start = None
        else:
            self.parts.append(f'</{tag}>')
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
    def handle_data(self, data):
        if any(t in {'script', 'style'} for t in self.stack):
            self.parts.append(data)
        elif any(t in {'code', 'pre', 'textarea'} for t in self.stack):
            self.parts.append(html.escape(data, quote=False))
        else:
            self.parts.append(self.text(data))
    def handle_entityref(self, name):
        self.parts.append(f'&{name};')
    def handle_charref(self, name):
        self.parts.append(f'&#{name};')
    def handle_decl(self, data):
        self.parts.append(f'<!{data}>')
    def handle_comment(self, data):
        self.parts.append(f'<!--{data}-->')

def localize_page(source, locale, path, available, catalog, *, style_assets=None):
    # The final discovery pass will create canonical/hreflang/JSON-LD for this URL.
    source = re.sub(r'<!-- openonco-seo:start -->.*?<!-- openonco-seo:end -->', '', source, flags=re.S)
    source = re.sub(r'<header class="top-bar site-header">.*?</header>', '', source, flags=re.S)
    parser = LocalizedHTML(catalog, locale, path, available, style_assets)
    parser.feed(source)
    page = ''.join(parser.parts)
    active = path.split('/')[0].removesuffix('.html')
    active = {'cases': 'gallery', 'disease': 'diseases', 'plans': 'try'}.get(active, active)
    page = re.sub(r'(<body\b[^>]*>)', lambda m: m.group() + render_top_bar(active, locale, page_path=path), page, count=1)
    note, original = NOTICES[locale]
    banner = f'<aside class="translation-notice" role="note"><strong>{html.escape(note)}</strong> <a href="/{path}" lang="en" hreflang="en" data-original-source>{html.escape(original)}</a></aside>'
    page = re.sub(r'(<main\b[^>]*>)', lambda m: m.group() + banner, page, count=1)
    if '<main' not in page:
        page = re.sub(r'(</header>)', lambda m: m.group() + banner, page, count=1)
    # Same English computation inputs; the display catalog localizes dynamic DOM.
    if path == 'kb.html':
        page = page.replace("'/kb_search_index.json'", f"'/{locale}/kb_search_index.json'")
        page = page.replace('"/kb_search_index.json"', f'"/{locale}/kb_search_index.json"')
    if path in PAGES or path.startswith('handbook/'):
        catalog_file = 'clinical-translations.json' if path == 'try.html' else 'clinical-ui-translations.json'
        runtime = f'<script src="/clinical-localization.js?v=20261010-2" data-locale="{locale}" data-catalog="/{locale}/{catalog_file}" defer></script>'
        page = page.replace('</body>', runtime + '</body>')
    digest = hashlib.sha256(source.encode('utf-8')).hexdigest()
    page = page.replace('</head>', f'<meta name="translation-review" content="pending_clinical_review"><meta name="translation-source-sha256" content="{digest}"></head>')
    return '\n'.join(line.rstrip() for line in page.splitlines()) + '\n'

def build_clinical_locales(output_dir: Path, catalog_dir: Path | None = None):
    catalog_dir = catalog_dir or Path(__file__).with_name('locales')
    manifest = catalog_dir / 'clinical_manifest.json'
    if not manifest.exists():
        return {'clinical_localized_pages': 0, 'pages': []}
    inventory = json.loads(manifest.read_text(encoding='utf-8'))['languages']
    for locale in LANGUAGES:
        catalog_path = manifest.parent / f'clinical.{locale}.json'
        if hashlib.sha256(catalog_path.read_bytes()).hexdigest() != inventory[locale]['sha256']:
            raise ValueError(f'Clinical catalog checksum mismatch: {locale}')
    pages = source_pages(output_dir)
    available = {p.relative_to(output_dir).as_posix() for p in pages}
    published = []
    style_assets = {}
    ui_sources = set()
    for page in pages:
        relative = page.relative_to(output_dir).as_posix()
        if (relative in PAGES and relative != 'try.html') or relative.startswith('handbook/'):
            collector = ProseCollector(dynamic_only=True)
            collector.feed(page.read_text(encoding='utf-8'))
            ui_sources.update(collector.strings)
    from serverless.clinical_locale_messages import messages_for
    from scripts.clinical_curated_copy import messages_for as clinical_titles
    from serverless.clinical_question import DISCLAIMER_EN, DISCLAIMER_TRANSLATIONS
    for locale in LANGUAGES:
        catalog = load_catalog(locale, catalog_dir)
        if not catalog:
            raise ValueError(f'Missing completed clinical translation catalog: {locale}')
        root = output_dir / locale
        root.mkdir(exist_ok=True)
        # A generated plan can use any current clinical record. Keep the full
        # checked display catalog there; small interactive surfaces need only
        # their own script literals and curated UI messages.
        runtime_catalog = dict(catalog)
        curated = messages_for(locale)
        curated.update(clinical_titles(locale))
        runtime_catalog.update(curated)
        runtime_catalog.update({value: value for value in curated.values()})
        runtime_catalog[normalize(DISCLAIMER_EN)] = normalize(DISCLAIMER_TRANSLATIONS[locale])
        runtime_catalog[normalize(DISCLAIMER_TRANSLATIONS[locale])] = normalize(DISCLAIMER_TRANSLATIONS[locale])
        (root / 'clinical-translations.json').write_text(json.dumps(runtime_catalog, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
        ui_catalog = {key: value for key, value in runtime_catalog.items() if key in ui_sources}
        ui_catalog.update(curated)
        ui_catalog.update({value: value for value in curated.values()})
        (root / 'clinical-ui-translations.json').write_text(json.dumps(ui_catalog, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
        for path in pages:
            relative = path.relative_to(output_dir).as_posix()
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(localize_page(path.read_text(encoding='utf-8'), locale, relative, available, catalog, style_assets=style_assets), encoding='utf-8')
            published.append(f'{locale}/{relative}')
        index = json.loads((output_dir / 'kb_search_index.json').read_text(encoding='utf-8'))
        for entry in index['entries']:
            for field in ('title', 'summary', 'subtitle', 'kind'):
                if isinstance(entry.get(field), str):
                    entry[field] = catalog.get(normalize(entry[field]), entry[field])
            if entry.get('url'):
                entry['url'] = locale_href(entry['url'], locale)
            entry['search_text'] = entry.get('search_text', '') + ' ' + ' '.join(str(entry.get(k, '')) for k in ('title', 'summary', 'subtitle', 'kind')).lower()
        (root / 'kb_search_index.json').write_text(json.dumps(index, ensure_ascii=False), encoding='utf-8')
    if published:
        (output_dir / 'clinical-localization.js').write_text(Path(__file__).with_name('clinical-localization.js').read_text(encoding='utf-8'), encoding='utf-8')
        styles_root = output_dir / 'clinical-styles'
        styles_root.mkdir(exist_ok=True)
        for digest, css in style_assets.items():
            (styles_root / f'{digest}.css').write_text(css, encoding='utf-8')
    return {'clinical_localized_pages': len(published), 'style_assets': len(style_assets), 'pages': published}
