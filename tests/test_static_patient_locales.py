"""Static patient language and deterministic overlapping render passes."""
import concurrent.futures

import pytest

from scripts import build_site as site
from scripts.build_clinical_locales import localize_page
from scripts.clinical_curated_copy import messages_for


def test_excluded_scenarios_are_removed_in_both_modes_and_all_languages(tmp_path, monkeypatch):
    from types import SimpleNamespace
    monkeypatch.setattr(site, 'CASES', [
        SimpleNamespace(case_id='public', visibility='public'),
        SimpleNamespace(case_id='internal', visibility='internal'),
        SimpleNamespace(case_id='quarantined', visibility='quarantined'),
    ])
    preserved = []
    for prefix in ('', 'ukr', 'es', 'pt', 'de', 'fr'):
        directory = tmp_path / prefix / 'cases'
        directory.mkdir(parents=True)
        for case in ('public', 'internal', 'quarantined'):
            for suffix in ('.html', '.patient.html'):
                path = directory / (case + suffix)
                path.write_text('synthetic ' + case, encoding='utf-8')
                if case == 'public':
                    preserved.append(path)
        unrelated = directory / 'internal-followup.html'
        unrelated.write_text('unrelated', encoding='utf-8')
        preserved.append(unrelated)
    assert site._remove_excluded_case_pages(tmp_path) == 24
    assert site._remove_excluded_case_pages(tmp_path) == 0
    assert set(tmp_path.rglob('*.html')) == set(preserved)
    assert all(p.read_text(encoding='utf-8') in {'synthetic public', 'unrelated'} for p in preserved)


def test_published_artifacts_have_no_internal_or_quarantined_case_twins():
    excluded = {c.case_id for c in site.CASES if c.visibility != 'public'}
    assert excluded
    sitemap = (site.REPO_ROOT / 'docs/sitemap.xml').read_text(encoding='utf-8')
    for case_id in excluded:
        for suffix in ('.html', '.patient.html'):
            assert f'/cases/{case_id}{suffix}' not in sitemap
    for prefix in ('', 'ukr', 'es', 'pt', 'de', 'fr'):
        for case_id in excluded:
            for suffix in ('.html', '.patient.html'):
                path = site.REPO_ROOT / 'docs' / prefix / 'cases' / (case_id + suffix)
                assert not path.exists(), path


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
