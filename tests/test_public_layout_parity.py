"""Locale switches preserve components and executable inputs."""
import re
from html.parser import HTMLParser
from types import SimpleNamespace

import pytest

from scripts.build_public_locales import build_public_locales, localize_public_page, STYLE_VERSION
from scripts.build_site import render_about
from scripts.site_nav import render_top_bar
from scripts.site_locales import locale_href


class Components(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.main = False

    def handle_starttag(self, tag, attrs):
        if tag == 'main':
            self.main = True
        if self.main:
            attrs = dict(attrs)
            self.nodes.append((tag, attrs.get('class'), attrs.get('id')))

    def handle_endtag(self, tag):
        if tag == 'main':
            self.main = False


def components(page):
    parser = Components()
    parser.feed(page)
    return parser.nodes


@pytest.mark.parametrize('locale', ('es', 'pt', 'de', 'fr'))
def test_public_translation_uses_canonical_components(locale):
    source = '''<html lang="en"><head><title>Example</title><style>.card{display:grid}</style></head>
    <body><main class="home-main"><section class="home-hero"><h1>Example</h1>
    <a href="/try.html">Open</a><input value="EN-SOURCE"><pre>{"dose":20}</pre></section></main>
    <script>const source = "EN-SOURCE";</script></body></html>'''
    result = localize_public_page(source, locale, 'index.html', {'try.html'}, {'Example': 'Translated', 'Open': 'Native'})
    assert components(result) == components(source)
    assert '<style>.card{display:grid}</style>' in result
    assert '<script>const source = "EN-SOURCE";</script>' in result
    assert 'value="EN-SOURCE"' in result and '{"dose":20}' in result
    assert f'href="/{locale}/try.html"' in result
    assert f'<html lang="{locale}">' in result and '<h1>Translated</h1>' in result
    assert 'international-main' not in result
    assert 'translation-original-fragment' not in result


def test_project_story_has_same_sections_in_both_source_languages():
    stats = SimpleNamespace(entities=[])
    en, uk = render_about(stats, target_lang='en'), render_about(stats, target_lang='uk')
    assert components(en) == components(uk)
    for name in ('purpose', 'work', 'effort', 'action'):
        assert f'class="about-{name}"' in en
    assert not re.search(r'[\u0400-\u04ff]', en.split('<main>', 1)[1])


def test_public_builder_uses_the_real_source_template(tmp_path):
    source = '<html lang="en"><head><link href="/style.css?v=old" rel="stylesheet"></head><body><main class="home-main"><section class="home-hero"><h1>About OpenOnco</h1><p>23</p></section></main></body></html>'
    (tmp_path / 'index.html').write_text(source, encoding='utf-8')
    (tmp_path / 'ukr').mkdir()
    (tmp_path / 'ukr/index.html').write_text(source.replace('lang="en"', 'lang="uk"'), encoding='utf-8')
    result = build_public_locales(tmp_path)
    assert len(result['shared_public_pages']) == 4
    for locale in ('es', 'pt', 'de', 'fr'):
        page = (tmp_path / locale / 'index.html').read_text(encoding='utf-8')
        assert components(page) == components(source)
        assert '<h1>About OpenOnco</h1>' not in page
        assert '<p>23</p>' in page
        assert STYLE_VERSION in page
    assert STYLE_VERSION in (tmp_path / 'ukr/index.html').read_text(encoding='utf-8')


@pytest.mark.parametrize('locale', ('en', 'uk', 'es', 'pt', 'de', 'fr'))
def test_all_headers_offer_the_same_sections(locale):
    header = render_top_bar('home', locale, page_path='index.html')
    assert len(re.findall(r'<nav class="top-nav">', header)) == 1
    assert header.count(f'href="{locale_href("capabilities.html", locale)}"') == 2
