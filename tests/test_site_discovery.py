import re
from xml.etree import ElementTree as ET

from scripts.site_head import finalize_site_discovery, inject_seo_metadata, write_sitemap


def test_sitemap_excludes_redirect_noindex_and_noncanonical_pages(tmp_path):
    pages = {
        'index.html': '', 'ukr/index.html': '', 'handbook.html': '',
        'en/index.html': '<meta content="0; URL=/" http-equiv="refresh">',
        'hidden.html': '<meta content="NOINDEX,follow" name="robots">',
        'alias.html': '<link href="https://openonco.info/" rel="canonical">',
        '404.html': '', 'review/index.html': '', 'ukr/capabilities.html': '',
    }
    for name, head in pages.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'<html><head><title>OpenOnco</title>{head}</head><body></body></html>', encoding='utf-8')
    root = ET.parse(write_sitemap(tmp_path)).getroot()
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'x': 'http://www.w3.org/1999/xhtml'}
    urls = {node.find('s:loc', ns).text: node for node in root.findall('s:url', ns)}
    assert set(urls) == {'https://openonco.info/', 'https://openonco.info/ukr/', 'https://openonco.info/handbook.html'}
    assert root.find('.//s:lastmod', ns) is None  # no invented daily freshness
    assert root.find('.//s:changefreq', ns) is None
    for home in ('https://openonco.info/', 'https://openonco.info/ukr/'):
        links = {n.get('hreflang'): n.get('href') for n in urls[home].findall('x:link', ns)}
        assert links == {'en': 'https://openonco.info/', 'uk': 'https://openonco.info/ukr/', 'x-default': 'https://openonco.info/'}
    handbook = {n.get('hreflang'): n.get('href') for n in urls['https://openonco.info/handbook.html'].findall('x:link', ns)}
    assert 'uk' not in handbook


def test_discovery_preserves_body_and_uses_real_language_inventory(tmp_path):
    for name in ('kb.html', 'ukr/kb.html', 'handbook.html'):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('<html><head><meta charset="utf-8"><title>Onco Wiki</title></head><body><p>Unchanged content</p></body></html>', encoding='utf-8')
    finalize_site_discovery(tmp_path, stats={})
    handbook = (tmp_path / 'handbook.html').read_text(encoding='utf-8')
    assert 'hreflang="uk"' not in handbook
    assert '<body><p>Unchanged content</p></body>' in handbook
    english = (tmp_path / 'kb.html').read_text(encoding='utf-8')
    assert 'hreflang="uk" href="https://openonco.info/ukr/kb.html"' in english
    assert 'hreflang="x-default" href="https://openonco.info/kb.html"' in english
    assert finalize_site_discovery(tmp_path, stats={})['html_pages_enriched'] == 0


def test_metadata_keeps_noindex_and_redirect_canonical():
    markup = '<html><head><title>Old</title><meta http-equiv="refresh" content="0;url=/kb.html"></head><body>Moved</body></html>'
    output = inject_seo_metadata(markup, path='en/kb.html')
    assert 'rel="canonical" href="https://openonco.info/kb.html"' in output
    assert re.search(r'name="robots" content="noindex, follow"', output)
    assert '<body>Moved</body>' in output
    hidden = '<html><head><title>Internal</title><meta name="robots" content="noindex,follow"></head></html>'
    assert 'name="robots" content="noindex, follow"' in inject_seo_metadata(hidden, path='internal.html')
    alias = '<html><head><title>Alias</title><link rel="canonical" href="https://openonco.info/kb.html"></head><body>Alias</body></html>'
    assert 'rel="canonical" href="https://openonco.info/kb.html"' in inject_seo_metadata(alias, path='alias.html')
