from pathlib import Path
from bs4 import BeautifulSoup
from scripts.shared_site_header import render_header_mount, write_shared_header_assets
from scripts.site_head import inject_geo_lang_redirect
from scripts.site_locales import LOCALES


def test_mount_preserves_missing_language_fallbacks_and_small_size():
    page = 'kb/drugs/example.html'
    markup = render_header_mount('fr', page, 'kb', {page, 'fr/' + page})
    soup = BeautifulSoup(markup, 'html.parser')
    mount = soup.select_one('[data-shared-site-header]')
    assert mount['data-page'] == page and mount['data-active'] == 'kb'
    assert '"fr"' not in mount['data-missing'] and '"it"' in mount['data-missing']
    assert len(markup.encode()) < 1000
    assert soup.select_one('nav a')['href'] == '/fr/'


def test_shared_fragments_keep_all_native_flag_menus(tmp_path):
    for prefix, _, _ in LOCALES.values():
        (tmp_path / prefix).mkdir(exist_ok=True)
    write_shared_header_assets(tmp_path)
    for prefix, _, _ in LOCALES.values():
        soup = BeautifulSoup((tmp_path / prefix / 'shared-header.fragment').read_text(encoding='utf-8'), 'html.parser')
        assert [link['lang'] for link in soup.select('.language-menu a')] == list(LOCALES)
        assert len(soup.select('.language-menu a svg.language-flag')) == 11
    assert (tmp_path / 'shared-site-header.js').is_file()


def test_explicit_shared_readers_do_not_repeat_unused_geo_lookup():
    original = '<html><head><meta charset="utf-8"></head><body><div data-shared-site-header></div><p>100 mg</p></body></html>'
    en = inject_geo_lang_redirect(original, path='cases/example.html')
    assert 'openonco-geo-lang:start' in en
    translated = inject_geo_lang_redirect(en, path='fr/cases/example.html')
    assert 'openonco-geo-lang:start' not in translated
    assert '<p>100 mg</p>' in translated
