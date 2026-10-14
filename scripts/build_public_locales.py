"""Render public translations from the same HTML templates as English."""
import html
import json
import re
from pathlib import Path

from scripts.build_clinical_locales import LocalizedHTML
from scripts.site_locales import PUBLIC_PAGES
from scripts.site_nav import render_top_bar
from scripts.site_translation_catalog import LANGUAGES, load_catalog, normalize
from scripts.clinical_curated_copy import messages_for as clinical_copy
from scripts.public_curated_copy import messages_for as public_copy
from scripts.clinical_translation_checks import acceptable_draft

PAGES = ('index.html', 'about.html', 'capabilities.html', 'specs.html', 'news.html', 'participate.html')
STYLE_VERSION = '/style.css?v=layout-20261011'


def safe_public_translation(source, translated, locale):
    """Keep route literals and corrupted drafts in their English source form."""
    if source.startswith('/') and not any(char.isspace() for char in source):
        return source
    return translated if acceptable_draft(source, translated, locale) else source


class PublicHTML(LocalizedHTML):
    """Translate display copy without changing the component tree or its CSS."""
    def link(self, value, *, localized=False):
        # The gap dashboard is generated only in English and Ukrainian. A
        # language-prefixed link on the other public editions would be a 404.
        if value.split('#', 1)[0].split('?', 1)[0] == '/clinical-gaps.html':
            return value
        return super().link(value, localized=localized)

    def text(self, value):
        key = normalize(html.unescape(value))
        target = self.catalog.get(key)
        if target is None:
            return html.escape(value, quote=False)
        left = re.match(r'^\s*', value).group()
        right = re.search(r'\s*$', value).group()
        return left + html.escape(target, quote=False) + right


def localize_public_page(source, locale, page, available, catalog):
    source = re.sub(r'<!-- openonco-seo:start -->.*?<!-- openonco-seo:end -->', '', source, flags=re.S)
    source = re.sub(r'<!-- openonco-geo-lang:start -->.*?<!-- openonco-geo-lang:end -->', '', source, flags=re.S)
    source = re.sub(r'<header class="top-bar site-header">.*?</header>', '', source, flags=re.S)
    parser = PublicHTML(catalog, locale, page, available)
    parser.feed(source)
    result = ''.join(parser.parts)
    active = 'home' if page == 'index.html' else page.removesuffix('.html')
    result = re.sub(r'(<body\b[^>]*>)', lambda match: match.group() + render_top_bar(active, locale, page_path=page), result, count=1)
    result = result.replace('</head>', '<meta name="translation-review" content="pending_language_review"></head>')
    return result


def synchronize_public_styles(root):
    """Every language uses the same shared CSS URL, including its cache version."""
    for prefix in ('', 'ukr', *LANGUAGES):
        for page in PUBLIC_PAGES:
            path = root / prefix / page
            if not path.exists():
                continue
            text = path.read_text(encoding='utf-8')
            head, separator, tail = text.partition('</head>')
            head = re.sub(r'(?<=href=")/style\.css(?:\?[^"\s]*)?(?=")', STYLE_VERSION, head)
            updated = head + separator + tail
            if updated != text:
                path.write_text(updated, encoding='utf-8')


def build_public_locales(root: Path):
    available = {path.relative_to(root).as_posix() for path in root.glob('*.html')}
    available.update(path.relative_to(root).as_posix() for folder in ('kb', 'cases', 'handbook', 'plans', 'disease') for path in (root / folder).rglob('*.html'))
    written = []
    for locale in LANGUAGES:
        catalog = load_catalog(locale)
        copy_path = Path(__file__).with_name('locales') / f'public.{locale}.json'
        if copy_path.exists():
            draft = json.loads(copy_path.read_text(encoding='utf-8'))
            catalog.update({
                source: safe_public_translation(source, translated, locale)
                for source, translated in draft.items()
            })
        catalog.update(clinical_copy(locale))
        catalog.update(public_copy(locale))
        for page in PAGES:
            source = root / page
            if not source.exists():
                continue
            text = source.read_text(encoding='utf-8')
            # Bootstrap fixtures can lack a canonical page; full site builds
            # always have a main component before this pass.
            if '<main' not in text:
                continue
            target = root / locale / page
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(localize_public_page(text, locale, page, available, catalog), encoding='utf-8')
            written.append(f'{locale}/{page}')
    synchronize_public_styles(root)
    return {'shared_public_pages': written}
