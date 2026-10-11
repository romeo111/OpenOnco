"""Reports expose recorded publications without inventing citation links."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.engine.render import _render_cited_sources
from knowledge_base.validation.loader import load_content


@pytest.mark.parametrize('language, heading', [('en', 'Sources cited'), ('uk', 'Цитовані джерела')])
def test_source_labels_and_recorded_absolute_links_survive_export(language, heading):
    metadata = SimpleNamespace(
        data_sources_summary=['SRC-ONE: Evidence <draft> (2026)', 'SRC-MISSING: Missing URL'],
        source_links={'SRC-ONE': 'https://publisher.example/paper?a=1&b=2'},
    )
    result = _render_cited_sources(metadata, language)
    assert heading in result
    assert 'https://publisher.example/paper?a=1&amp;b=2' in result
    assert 'Evidence &lt;draft&gt;' in result
    assert 'rel="noopener noreferrer"' in result
    assert '<li>SRC-MISSING: Missing URL</li>' in result


@pytest.mark.parametrize('url', [
    'javascript:alert(1)', 'data:text/html,unsafe', '//publisher.example/paper',
    'https://user:password@publisher.example/paper', 'https://publisher.example/\nunsafe',
    'https://[invalid', '',
])
def test_unsafe_or_missing_source_url_remains_plain_text(url):
    result = _render_cited_sources(SimpleNamespace(
        data_sources_summary=['SRC-ONE: Preserved evidence'], source_links={'SRC-ONE': url},
    ), 'en')
    assert '<a ' not in result
    assert 'SRC-ONE: Preserved evidence' in result


def test_synthetic_plan_links_match_original_source_records():
    root = Path('knowledge_base/hosted/content')
    patient = json.loads(Path('examples/patient_zero_indolent.json').read_text(encoding='utf-8'))
    result = generate_plan(patient, kb_root=root)
    assert result.plan is not None
    links = result.plan.fda_compliance.source_links
    assert links
    records = load_content(root).entities_by_id
    for source_id, url in links.items():
        assert records[source_id]['type'] == 'sources'
        assert url == records[source_id]['data']['url']
    report = render_plan_html(result, target_lang='en')
    assert '<ul class=\'sources\'>' in report
    assert any(url.replace('&', '&amp;') in report for url in links.values())
