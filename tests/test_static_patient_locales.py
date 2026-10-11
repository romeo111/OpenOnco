"""Static patient language and deterministic overlapping render passes."""
import concurrent.futures

import pytest

from scripts import build_site as site
from scripts.build_clinical_locales import localize_page
from scripts.clinical_curated_copy import messages_for


def test_root_patient_twin_uses_english_draft_and_site_navigation(tmp_path, monkeypatch):
    case = next(c for c in site.CASES if c.case_id == 'aitl-cd30-negative')
    profile = site.EXAMPLES / case.file
    before = profile.read_bytes()
    monkeypatch.setattr(site, 'search_trials', lambda *args, **kwargs: [])
    output = site.build_one_case_patient(case, tmp_path)
    body = output.read_text(encoding='utf-8')
    assert output == tmp_path / 'cases/aitl-cd30-negative.patient.html'
    assert '<html lang="en">' in body
    assert 'data-translation-status="draft-partial"' in body
    assert 'Your oncology plan' in body
    assert 'class="top-bar site-header"' in body
    assert 'Back to gallery' in body
    assert 'Synthetic educational example.' in body
    assert '/cases/aitl-cd30-negative.html' in body
    assert profile.read_bytes() == before


def test_patient_pass_is_not_scheduled_with_competing_clinician_writes(tmp_path, monkeypatch):
    monkeypatch.setenv('OPENONCO_BUILD_WORKERS', '2')
    monkeypatch.setattr(site, '_public_case_entries', lambda: ['a', 'b'])
    monkeypatch.setattr(site, '_public_example_entries', lambda: ['a'])
    completed = []
    batches = []
    def worker(task):
        if task[2] == 'patient':
            assert set(completed) == {('a', 'uk'), ('b', 'uk'), ('a', 'en'), ('b', 'en')}
        completed.append((task[0], task[2]))
        return {'lang': task[2], 'path': 'synthetic.html'}
    class Pool:
        def __init__(self, **kwargs):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def map(self, function, tasks, **kwargs):
            tasks = list(tasks)
            kinds = {task[2] for task in tasks}
            assert not ('patient' in kinds and 'en' in kinds)
            batches.append(kinds)
            return map(function, tasks)
    monkeypatch.setattr(concurrent.futures, 'ProcessPoolExecutor', Pool)
    monkeypatch.setattr(site, '_build_one_case_worker', worker)
    groups = site._build_all_cases_parallel(tmp_path)
    assert [len(group) for group in groups] == [2, 2, 1]
    assert batches == [{'uk', 'en'}, {'patient'}]


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
def test_patient_report_structure_and_incomplete_notice_have_native_copy(locale):
    catalog = messages_for(locale)
    notice = 'English translation draft — incomplete and awaiting clinical/language review. Some explanations remain in their original language and are marked. Consult the original report and your doctor.'
    source = '<html lang="en"><head><title>Your oncology plan</title></head><body><main><h1>Your oncology plan</h1><aside data-translation-status="draft-partial">' + notice + '</aside><h2>What was found</h2><strong data-variant-original="V600E">BRAF V600E</strong><h2>What this means for treatment</h2><a href="/cases/test.html">Technical version for your doctor →</a></main></body></html>'
    output = localize_page(source, locale, 'cases/test.patient.html', set(), catalog)
    for key in ('Your oncology plan', 'What was found', 'What this means for treatment', 'Technical version for your doctor →', notice):
        assert catalog[key] in output
    assert 'data-translation-status="draft-partial"' in output
    assert 'data-variant-original="V600E">BRAF V600E' in output
