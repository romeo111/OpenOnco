"""Share deep-page navigation without duplicating flags and menus in every record."""
import html
import json
from pathlib import Path
from scripts.site_locales import LOCALES, locale_path, locale_href
from scripts.site_nav import render_top_bar

DEEP_SECTIONS = ('kb/', 'cases/', 'handbook/', 'plans/', 'disease/')


def render_header_mount(locale, page, active, available_paths):
    missing = [code for code in LOCALES if locale_path(page, code) not in available_paths]
    config = html.escape(json.dumps(missing, separators=(',', ':')), quote=True)
    return ('<!-- shared-site-header:start -->'
            f'<div data-shared-site-header data-locale="{locale}" data-page="{html.escape(page, quote=True)}" '
            f'data-active="{active}" data-missing="{config}">'
            f'<nav aria-label="OpenOnco"><a href="{locale_href("index.html", locale)}">OpenOnco</a> · '
            f'<a href="{locale_href("kb.html", locale)}">Onco Wiki</a> · '
            f'<a href="{locale_href("try.html", locale)}">Plan Builder</a></nav></div>'
            '<link rel="stylesheet" href="/header.css?v=layout-20261011">'
            '<script src="/shared-site-header.js" defer></script><!-- shared-site-header:end -->')


def write_shared_header_assets(output_dir):
    output_dir = Path(output_dir)
    for locale, (prefix, _, _) in LOCALES.items():
        directory = output_dir / prefix
        if not directory.exists():
            continue
        (directory / 'shared-header.fragment').write_text(render_top_bar('', locale), encoding='utf-8', newline='\n')
    (output_dir / 'shared-site-header.js').write_text(
        Path(__file__).with_name('shared-site-header.js').read_text(encoding='utf-8'), encoding='utf-8', newline='\n')
