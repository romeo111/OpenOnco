"""Read-only smoke check of deployed public navigation; no clinical API requests."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup
import httpx

from scripts.site_locales import LOCALES, locale_href

PAGES = ('index.html', 'capabilities.html', 'handbook.html', 'try.html',
         'ask.html', 'prevent.html', 'kb.html', 'about.html')
MAX_BYTES = 2_000_000


def origin(url):
    parsed = urlsplit(url)
    return parsed.scheme, parsed.hostname, parsed.port


def fetch(client, url, base):
    """Bounded GET; redirects may never leave the selected website origin."""
    for _ in range(4):
        if origin(url) != origin(base):
            raise ValueError('redirect leaves website origin')
        with client.stream('GET', url) as response:
            if response.is_redirect:
                location = response.headers.get('location')
                if not location:
                    raise ValueError('redirect has no destination')
                url = urljoin(url, location)
                continue
            response.raise_for_status()
            chunks, size = [], 0
            for chunk in response.iter_bytes():
                size += len(chunk)
                if size > MAX_BYTES:
                    raise ValueError('response exceeds smoke-check size limit')
                chunks.append(chunk)
            if 'text/html' not in response.headers.get('content-type', ''):
                raise ValueError('destination is not HTML')
            return b''.join(chunks).decode('utf-8')
    raise ValueError('too many redirects')


def inspect_page(html, locale, base):
    soup = BeautifulSoup(html, 'html.parser')
    issues = []
    header = soup.select_one('.site-header')
    if not header:
        issues.append('missing shared header')
    if not soup.html or soup.html.get('lang') != locale:
        issues.append('wrong document language')
    if len(soup.select('main')) != 1:
        issues.append('expected one main landmark')
    if not soup.select_one('link[rel="canonical"]'):
        issues.append('missing canonical link')
    links = header.select('.language-menu nav a') if header else []
    if [a.get('lang') for a in links] != list(LOCALES):
        issues.append('language list differs from registered order')
    if any(not a.select_one('svg.language-flag') for a in links):
        issues.append('missing language flag')
    destinations = set()
    for link in header.select('a[href]') if header else []:
        url = urljoin(base, link['href'])
        parsed = urlsplit(url)
        if origin(url) == origin(base):
            if parsed.query or not (parsed.path.endswith(('.html', '/'))):
                issues.append('unexpected navigation destination: ' + link['href'])
            else:
                destinations.add(url.split('#', 1)[0])
    return issues, destinations


def audit(base, client):
    targets = [(locale, urljoin(base, locale_href(page, locale)))
               for locale in LOCALES for page in PAGES]

    def inspect(target):
        locale, url = target
        try:
            issues, destinations = inspect_page(fetch(client, url, base), locale, base)
            return {'url': url, 'issues': issues}, destinations
        except (httpx.HTTPError, ValueError, UnicodeError) as error:
            return {'url': url, 'issues': [str(error)]}, set()

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(inspect, targets))
        rows = [row for row, _ in results]
        seen = {row['url'] for row in rows}
        extra = sorted(set().union(*(urls for _, urls in results)) - seen)

        def destination(url):
            try:
                fetch(client, url, base)
                return {'url': url, 'issues': []}
            except (httpx.HTTPError, ValueError, UnicodeError) as error:
                return {'url': url, 'issues': [str(error)]}

        rows.extend(executor.map(destination, extra))
    return {'base_url': base, 'public_pages_checked': len(targets),
            'navigation_destinations_checked': len(extra),
            'failures': [row for row in rows if row['issues']],
            'scope': 'HTTP and static HTML only; not browser or clinical validation'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='https://openonco.info/')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    parsed = urlsplit(args.base_url)
    if (parsed.scheme not in ('http', 'https') or not parsed.hostname
            or parsed.username or parsed.password or parsed.query or parsed.fragment
            or parsed.path not in ('', '/')):
        parser.error('--base-url must be a website origin without credentials or query')
    base = args.base_url.rstrip('/') + '/'
    with httpx.Client(timeout=20, follow_redirects=False) as client:
        report = audit(base, client)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.write_text(output + '\n', encoding='utf-8')
    print(output)
    return bool(report['failures'])


if __name__ == '__main__':
    raise SystemExit(main())
