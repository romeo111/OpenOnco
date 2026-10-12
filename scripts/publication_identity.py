"""Check consistency with dated primary-record observations, not clinical validity."""
import re
import unicodedata
from urllib.parse import urlsplit


def normalized_title(value):
    text = unicodedata.normalize('NFKC', str(value)).casefold()
    return ' '.join(text.translate(str.maketrans({'–': '-', '—': '-', '‑': '-'})).split()).rstrip('.')


def compare_observed_metadata(source, observation):
    """Return changed fields; the caller must independently collect observations."""
    changed = []
    if not observation.get('source_id') or source.get('id') != observation['source_id']:
        changed.append('source_id')
    for field in ('pmid', 'doi'):
        actual = str(source.get(field) or '').strip().casefold()
        expected = str(observation.get(field) or '').strip().casefold()
        if not actual or actual != expected:
            changed.append(field)
    expected_title = normalized_title(observation.get('title') or '')
    if not expected_title or normalized_title(source.get('title', '')) != expected_title:
        changed.append('title')
    expected_year = str(observation.get('publication_year') or '')
    if not re.fullmatch(r'[0-9]{4}', expected_year) or str(source.get('version')) != expected_year:
        changed.append('publication_year')
    pmid = str(observation.get('pmid') or '')
    if not re.fullmatch(r'[0-9]+', pmid) or observation.get('primary_record_url') != f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/':
        changed.append('primary_record_url')
    try:
        url = urlsplit(source.get('url') or '')
        official_port = url.port in (None, 443)
    except ValueError:
        changed.append('source_url_binding')
        return changed
    doi = str(observation.get('doi') or '').casefold()
    bound = (url.scheme == 'https' and official_port and not url.username and not url.password and (
        (url.hostname == 'pubmed.ncbi.nlm.nih.gov' and url.path.strip('/') == pmid)
        or (url.hostname in {'nejm.org', 'www.nejm.org'} and url.path.casefold() in {
            '/doi/full/' + doi, '/doi/abs/' + doi, '/doi/pdf/' + doi})
        or (url.hostname == 'doi.org' and url.path.strip('/').casefold() == doi)))
    if not bound:
        changed.append('source_url_binding')
    return changed
