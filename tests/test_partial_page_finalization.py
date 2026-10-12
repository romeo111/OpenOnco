"""Partial clinical releases must preserve the normal header and cached assets."""
import re
import pytest
from scripts.site_head import finalize_public_page, geo_lang_url
from scripts.site_nav import render_top_bar
from scripts.shared_clinical_reader import render_shared_reader


@pytest.mark.parametrize('locale,prefix', [('en', ''), ('uk', 'ukr/')])
def test_deep_source_pages_use_shared_header_and_versioned_geo_asset(locale, prefix):
    page = 'cases/synthetic.html'
    available = {page, 'ukr/' + page, 'fi/' + page}
    original = '<html><head><meta charset="utf-8"><title>Synthetic</title></head><body>' + render_top_bar('gallery', locale, page_path=page, available_paths=available) + '<main>Unchanged clinical body: 20 mg.</main></body></html>'
    final = finalize_public_page(original, path=prefix + page, available_paths=available)
    assert 'data-shared-site-header' in final
    assert f'src="{geo_lang_url()}"' in final
    assert '<main>Unchanged clinical body: 20 mg.</main>' in final
    assert finalize_public_page(final, path=prefix + page, available_paths=available) == final


def test_explicit_translated_reader_does_not_redirect_to_geographic_language():
    original = '<html lang="en"><head><title>Synthetic</title></head><body><main>Source</main></body></html>'
    reader = render_shared_reader(original, 'fi', 'cases/synthetic.html', 'Synthetic')
    final = finalize_public_page(reader, path='fi/cases/synthetic.html', available_paths={'cases/synthetic.html', 'fi/cases/synthetic.html'})
    assert 'data-shared-clinical-source' in final
    assert 'openonco-geo-lang:start' not in final
    assert not re.search(r'src="/geo-lang\.', final)
