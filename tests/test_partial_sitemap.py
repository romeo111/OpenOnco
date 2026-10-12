"""Partial sitemap releases preserve prior URLs and respect page scope."""
from pathlib import Path

import pytest

from scripts.site_head import write_sitemap
from scripts.update_partial_sitemap import inventory, update


def page(root, path, head=''):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('<html><head>' + head + '</head><body>unchanged</body></html>')


def test_missing_old_html_is_preserved_and_new_language_links_are_reciprocal(tmp_path):
    from xml.etree import ElementTree as ET
    # The normal discovery writer advertises a clinical locale once its
    # completed handbook sentinel is in the indexable inventory.
    write_sitemap(tmp_path, available_paths={
        'index.html', 'missing-old.html', 'fi/handbook/hb-dlbcl-1l.html',
    })
    page(tmp_path, 'kb/new.html')
    page(tmp_path, 'fi/kb/new.html')
    before = (tmp_path / 'kb/new.html').read_bytes()
    report = update(tmp_path, ['kb/new.html', 'fi/kb/new.html'], write=True)
    assert report['result_urls'] == 5
    assert inventory(tmp_path) == {
        'index.html', 'missing-old.html', 'kb/new.html', 'fi/kb/new.html',
        'fi/handbook/hb-dlbcl-1l.html',
    }
    assert (tmp_path / 'kb/new.html').read_bytes() == before
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'x': 'http://www.w3.org/1999/xhtml'}
    for node in ET.parse(tmp_path / 'sitemap.xml').getroot().findall('s:url', ns):
        if node.find('s:loc', ns).text.endswith('/kb/new.html'):
            assert {link.get('hreflang') for link in node.findall('x:link', ns)} == {'en', 'fi', 'x-default'}
    assert not update(tmp_path, ['kb/new.html', 'fi/kb/new.html'])['changed']


def test_noindex_redirect_and_alias_are_not_added_and_dry_run_is_read_only(tmp_path):
    write_sitemap(tmp_path, available_paths={'index.html'})
    original = (tmp_path / 'sitemap.xml').read_bytes()
    page(tmp_path, 'hidden.html', '<meta name="robots" content="noindex">')
    page(tmp_path, 'redirect.html', '<meta http-equiv="refresh" content="0;url=/">')
    page(tmp_path, 'alias.html', '<link rel="canonical" href="https://openonco.info/">')
    page(tmp_path, 'new.html')
    report = update(tmp_path, ['hidden.html', 'redirect.html', 'alias.html', 'new.html'])
    assert report['added'] == ['new.html'] and len(report['excluded']) == 3
    assert (tmp_path / 'sitemap.xml').read_bytes() == original


def test_protected_path_rejected_before_any_html_read(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError('No files may be read before scope validation')
    monkeypatch.setattr(Path, 'read_text', forbidden)
    with pytest.raises(ValueError, match='Preserved'):
        update(tmp_path, ['cases/VERIFIED-CRC-L2-TUCATINIB-TRASTUZUMAB-CRC.html'])


def test_external_shard_cannot_be_read(tmp_path):
    (tmp_path / 'sitemap.xml').write_text('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>https://other.test/sitemap-part-1.xml.gz</loc></sitemap></sitemapindex>')
    with pytest.raises(ValueError, match='shard URL'):
        inventory(tmp_path)


def test_failed_index_publication_rolls_back_new_metadata(tmp_path, monkeypatch):
    write_sitemap(tmp_path, available_paths={f'legacy-{n}.html' for n in range(5000)})
    index = tmp_path / 'sitemap.xml'
    assert 'sitemapindex' in index.read_text()
    # Existing custom formatting ensures the index also needs replacement,
    # after the changed shard has already been published.
    index.write_text(index.read_text().replace('</sitemapindex>', '<!-- old -->\n</sitemapindex>'))
    originals = {p.name: p.read_bytes() for p in tmp_path.glob('sitemap*')}
    page(tmp_path, 'new.html')
    replace = Path.replace
    def fail_index(path, target):
        if Path(target).name == 'sitemap.xml':
            raise OSError('simulated metadata replacement failure')
        return replace(path, target)
    monkeypatch.setattr(Path, 'replace', fail_index)
    with pytest.raises(OSError, match='simulated'):
        update(tmp_path, ['new.html'], write=True)
    assert all((tmp_path / name).read_bytes() == data for name, data in originals.items())
    assert not list(tmp_path.glob('.sitemap-*'))


@pytest.mark.parametrize('path', ['../outside.html', '/outside.html', 'new.html?q=x'])
def test_bad_manifest_paths_are_rejected(tmp_path, path):
    with pytest.raises(ValueError):
        update(tmp_path, [path])
