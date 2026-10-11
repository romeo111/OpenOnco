
import pytest
from scripts.submit_indexnow import BASE, MAX_URLS_PER_POST, batches, payload_for, submit


def test_payload_rejects_foreign_urls_and_invalid_keys(tmp_path):
    key = 'a' * 32
    (tmp_path / f'{key}.txt').write_text(key)
    sitemap = tmp_path / 'sitemap.xml'
    sitemap.write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://other.example/x</loc></url></urlset>')
    with pytest.raises(ValueError, match='canonical URLs'):
        payload_for(tmp_path)
    sitemap.write_text(f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}participate.html</loc></url></urlset>')
    assert payload_for(tmp_path)['urlList'] == [BASE + 'participate.html']
    (tmp_path / f'{key}.txt').write_text('wrong')
    with pytest.raises(ValueError, match='must match'):
        payload_for(tmp_path)


def test_submit_checks_live_ownership_before_post(monkeypatch):
    calls = []

    class Response:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def read(self):
            return b'wrong-key'

    def fake_open(request, **kwargs):
        calls.append(request)
        return Response()

    monkeypatch.setattr('scripts.submit_indexnow.urlopen', fake_open)
    with pytest.raises(ValueError, match='does not match'):
        submit({'key': 'expected', 'keyLocation': BASE + 'proof.txt'})
    assert calls == [BASE + 'proof.txt']


def test_large_sitemap_is_split_without_losing_or_repeating_urls(tmp_path):
    key = 'b' * 32
    (tmp_path / f'{key}.txt').write_text(key)
    urls = [BASE + f'page-{i}.html' for i in range(MAX_URLS_PER_POST * 2 + 1)]
    body = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    body += ''.join(f'<url><loc>{url}</loc></url>' for url in urls)
    (tmp_path / 'sitemap.xml').write_text(body + '</urlset>')
    payload = payload_for(tmp_path)
    parts = list(batches(payload))
    assert [len(part['urlList']) for part in parts] == [10_000, 10_000, 1]
    assert [url for part in parts for url in part['urlList']] == sorted(urls)
