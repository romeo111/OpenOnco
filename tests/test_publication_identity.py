import json
from pathlib import Path

import pytest
import yaml
from scripts.publication_identity import compare_observed_metadata


def pair():
    source = {'id': 'SRC-EXAMPLE', 'pmid': '123', 'doi': '10.1/example', 'title': 'Example Non-Small-Cell Study', 'version': '2018', 'url': 'https://pubmed.ncbi.nlm.nih.gov/123'}
    observation = {'source_id': 'SRC-EXAMPLE', 'pmid': '123', 'doi': '10.1/example', 'title': 'Example Non–Small-Cell Study', 'publication_year': 2018, 'primary_record_url': 'https://pubmed.ncbi.nlm.nih.gov/123/'}
    return source, observation


@pytest.mark.parametrize('field,value', [('pmid', '456'), ('doi', '10.1/other'), ('title', 'Another Study'), ('version', '2026'), ('url', 'https://pubmed.ncbi.nlm.nih.gov/456/')])
def test_changed_publication_binding_is_detected(field, value):
    source, observed = pair()
    source[field] = value
    assert compare_observed_metadata(source, observed)


def test_bibliographic_check_does_not_validate_notes_or_currency():
    source, observed = pair()
    source.update(notes='Unreviewed clinical claim', current_as_of='2026-10-12', currency_status='current')
    assert compare_observed_metadata(source, observed) == []


def test_untrusted_primary_record_domain_is_rejected():
    source, observed = pair()
    observed['primary_record_url'] = 'https://pubmed.ncbi.nlm.nih.gov.example/123/'
    assert 'primary_record_url' in compare_observed_metadata(source, observed)


@pytest.mark.parametrize('url', ['https://[invalid', 'https://pubmed.ncbi.nlm.nih.gov:1234/123/', 'https://user@pubmed.ncbi.nlm.nih.gov/123/'])
def test_broken_or_noncanonical_source_binding_is_not_accepted(url):
    source, observed = pair()
    source['url'] = url
    assert 'source_url_binding' in compare_observed_metadata(source, observed)


def test_missing_identity_fields_are_not_treated_as_matching():
    source, observed = pair()
    for key in ('source_id', 'publication_year'):
        observed.pop(key)
    source.pop('id'); source.pop('version')
    assert {'source_id', 'publication_year'} <= set(compare_observed_metadata(source, observed))


def test_committed_observations_match_current_source_bibliography():
    root = Path(__file__).resolve().parents[1]
    report = json.loads((root / 'docs/audits/publication_identity_2026-10-12.json').read_text(encoding='utf-8'))
    assert report['scope'] == 'publication_identity_only'
    assert report['clinical_validation'] is False
    assert report['live_verification_required_for_refresh'] is True
    assert len({row['source_id'] for row in report['observations']}) == len(report['observations']) == 5
    assert len({row['pmid'] for row in report['observations']}) == 5
    assert len({row['doi'].casefold() for row in report['observations']}) == 5
    for row in report['observations']:
        name = row['source_file']
        assert Path(name).name == name and name.endswith('.yaml')
        source = yaml.safe_load((root / 'knowledge_base/hosted/content/sources' / name).read_text(encoding='utf-8'))
        assert compare_observed_metadata(source, row) == [], row['source_id']
