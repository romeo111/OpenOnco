"""Small language readers sharing immutable original clinical documents.

Avoid duplicating five large clinical trees on free static hosting. Interactive
tool pages still use complete templates; these readers are for source documents.
"""
import hashlib
import html
import re
from pathlib import Path, PurePosixPath

from scripts.additional_locale_copy import NOTICES
from scripts.site_nav import render_top_bar


def render_shared_reader(source: str, locale: str, path: str, title: str) -> str:
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
<script src="/clinical-localization.js?v=20261011-source-language" data-locale="{locale}" data-catalog="/{locale}/clinical-translations.json" defer></script>
</body></html>\n'''


def write_reader_assets(output_dir: Path, locale: str) -> None:
    (output_dir / locale / 'shared-header.fragment').write_text(render_top_bar('', locale), encoding='utf-8')
    (output_dir / 'shared-clinical-reader.js').write_text(Path(__file__).with_name('shared-clinical-reader.js').read_text(encoding='utf-8'), encoding='utf-8')
