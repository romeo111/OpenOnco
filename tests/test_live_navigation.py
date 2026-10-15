"""Deployment checks must fail on broken destinations and avoid external redirects."""
import httpx
import pytest

from scripts.check_live_navigation import audit, fetch, inspect_page
from scripts.site_nav import render_top_bar


def page(locale='en'):
    return (f'<html lang="{locale}"><head><link rel="canonical" href="https://test/">'
            '</head><body>' + render_top_bar('home', locale, page_path='index.html')
            + '<main>Example</main></body></html>')


def test_real_shared_header_passes_and_links_are_inventoried():
    issues, links = inspect_page(page(), 'en', 'https://test/')
    assert not issues
    assert 'https://test/fi/' in links
    assert 'https://test/try.html' in links
    assert all(url.startswith('https://test/') for url in links)


def test_missing_header_and_wrong_language_are_actionable():
    issues, _ = inspect_page('<html lang="it"><body></body></html>', 'fi', 'https://test/')
    assert 'missing shared header' in issues
    assert 'wrong document language' in issues
    assert 'expected one main landmark' in issues


def test_broken_registered_destination_fails_whole_audit():
    def serve(request):
        path = request.url.path
        locale = path.split('/')[1] if path.split('/')[1] in ('it', 'da', 'sv', 'nb', 'fi', 'es', 'pt', 'de', 'fr') else 'uk' if path.startswith('/ukr/') else 'en'
        status = 404 if path == '/fi/news.html' else 200
        return httpx.Response(status, text=page(locale), headers={'content-type': 'text/html'})
    with httpx.Client(transport=httpx.MockTransport(serve)) as client:
        report = audit('https://test/', client)
    assert report['public_pages_checked'] == 88
    assert report['navigation_destinations_checked'] > 0
    assert [row['url'] for row in report['failures']] == ['https://test/fi/news.html']


def test_external_redirect_is_rejected_before_following():
    visited = []
    def serve(request):
        visited.append(str(request.url))
        return httpx.Response(302, headers={'location': 'https://external.test/'})
    with httpx.Client(transport=httpx.MockTransport(serve)) as client:
        with pytest.raises(ValueError, match='leaves website origin'):
            fetch(client, 'https://test/', 'https://test/')
    assert visited == ['https://test/']


@pytest.mark.parametrize('body,content_type,error', [
    ('{}', 'application/json', 'not HTML'),
    ('x' * 2_000_001, 'text/html', 'size limit'),
], ids=['non-html', 'oversize'])
def test_non_html_and_unbounded_responses_fail(body, content_type, error):
    with httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(
            200, text=body, headers={'content-type': content_type}))) as client:
        with pytest.raises(ValueError, match=error):
            fetch(client, 'https://test/', 'https://test/')
