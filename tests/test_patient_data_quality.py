"""Patient input completeness is distinct from clinical approval."""
from copy import deepcopy
from pathlib import Path
import json
import re

import pytest

from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.engine.mdt_orchestrator import MDTOrchestrationResult, orchestrate_mdt

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


@pytest.fixture(scope='module')
def aitl():
    patient = json.loads((ROOT / 'examples/patient_aitl_cd30_negative.json').read_text(encoding='utf-8'))
    plan = generate_plan(patient, kb_root=KB)
    return plan, orchestrate_mdt(patient, plan, kb_root=KB)


@pytest.mark.parametrize('lang', ['en', 'uk'])
def test_real_incomplete_profile_qualifies_patient_options_without_mutation(aitl, lang):
    plan, mdt = aitl
    before_plan, before_mdt = deepcopy(plan), deepcopy(mdt)
    html = render_plan_html(plan, mdt=mdt, mode='patient', target_lang=lang)
    block = re.search(r'<section class="patient-data-quality".*?</section>', html, re.S).group()
    assert mdt.data_quality_summary['status'] == 'incomplete_for_default_track'
    assert 'data-data-quality-status="incomplete_for_default_track"' in block
    assert html.index(block) < html.index('<section class="what-now">')
    assert str(len(mdt.data_quality_summary['missing_critical_fields'])) in block
    assert 'RF-' not in block and 'BIO-' not in block
    assert ('does not mean a test was not performed' if lang == 'en' else 'не означає, що обстеження не проводили') in block
    assert plan == before_plan and mdt == before_mdt


@pytest.mark.parametrize('lang', ['en', 'uk'])
def test_missing_assessment_is_not_presented_as_complete(aitl, lang):
    plan, _ = aitl
    html = render_plan_html(plan, mode='patient', target_lang=lang)
    assert 'data-data-quality-status="not_assessed"' in html
    assert ('has not been assessed' if lang == 'en' else 'не оцінено') in html


@pytest.mark.parametrize('lang', ['en', 'uk'])
def test_complete_technical_checks_do_not_imply_treatment_approval(aitl, lang):
    plan, _ = aitl
    mdt = MDTOrchestrationResult(None, None, None, data_quality_summary={'status': 'complete_for_mdt_review'})
    html = render_plan_html(plan, mdt=mdt, mode='patient', target_lang=lang)
    assert 'data-data-quality-status="complete_for_mdt_review"' in html
    assert ('does not mean that treatment has been approved' if lang == 'en' else 'не означає, що лікування схвалено') in html


def test_unknown_quality_status_is_escaped_and_not_called_complete(aitl):
    plan, _ = aitl
    mdt = MDTOrchestrationResult(None, None, None, data_quality_summary={'status': '"><script>unsafe</script>'})
    html = render_plan_html(plan, mdt=mdt, mode='patient', target_lang='en')
    assert '<script>unsafe' not in html
    assert 'Data completeness has not been assessed' in html


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
def test_native_quality_copy_preserves_status_and_counts(aitl, locale):
    from scripts.build_clinical_locales import localize_page
    from scripts.clinical_curated_copy import messages_for
    plan, mdt = aitl
    source = render_plan_html(plan, mdt=mdt, mode='patient', target_lang='en')
    catalog = messages_for(locale)
    output = localize_page(source, locale, 'cases/test.patient.html', set(), catalog)
    block = re.search(r'<section class="patient-data-quality".*?</section>', output, re.S).group()
    for key in ('Information to clarify with your doctor',
                'Required biomarker information is missing from the profile. Review of the main option in this report is incomplete.',
                'Important clinical information missing',
                'Biomarker gaps for the main option in this report',
                'Missing from the profile does not mean a test was not performed. Ask your doctor which results to add or verify. Do not change treatment based only on this report.'):
        assert catalog[key] in block
        assert key not in block
    assert 'data-data-quality-status="incomplete_for_default_track"' in block
    assert f'</span>: {len(mdt.data_quality_summary["missing_critical_fields"])}</li>' in block


def test_generated_patient_quality_is_consistent_across_all_languages():
    from html import unescape
    from scripts.clinical_curated_copy import messages_for
    english_labels = ('Option in this report', 'A) Main option in this report',
                      'B) Main option in this report', 'A) Alternative option in this report',
                      'B) Alternative option in this report')
    ukrainian_labels = ('Варіант у звіті', 'А) Основний варіант у звіті',
                        'Б) Основний варіант у звіті', 'А) Альтернативний варіант у звіті',
                        'Б) Альтернативний варіант у звіті')
    reference = None
    for prefix in ('', 'ukr', 'es', 'pt', 'de', 'fr'):
        translated_labels = (ukrainian_labels if prefix == 'ukr' else
                             tuple(messages_for(prefix)[label] for label in english_labels)
                             if prefix else english_labels)
        canonical_roles = dict(zip(translated_labels, english_labels))
        inventory = {}
        for path in (ROOT / 'docs' / prefix / 'cases').glob('*.patient.html'):
            document = path.read_text(encoding='utf-8')
            labels = tuple(unescape(label) for label in re.findall(r'<p class="track-label">(.*?)</p>', document, re.S))
            unknown = [label for label in labels if label not in canonical_roles]
            assert not unknown, (path, unknown)
            roles = tuple(canonical_roles[label] for label in labels)
            block = re.search(r'<section class="patient-data-quality".*?</section>', document, re.S)
            if '<section class="what-now">' in document:
                assert block, path
                assert labels, path
                assert block.start() < document.index('<section class="what-now">'), path
            if block:
                status = re.search(r'data-data-quality-status="([^"]+)"', block.group())[1]
                counts = tuple(re.findall(r'</span>: (\d+)</li>', block.group()))
                inventory[path.name] = (status, counts, roles)
            else:
                inventory[path.name] = ('no-plan', (), roles)
        assert inventory, prefix
        if reference is None:
            reference = inventory
        else:
            assert inventory == reference, prefix


def test_generated_rationale_review_notices_match_across_languages():
    reference = None
    for prefix in ('', 'ukr', 'es', 'pt', 'de', 'fr'):
        inventory = {}
        for path in (ROOT / 'docs' / prefix / 'cases').glob('*.patient.html'):
            document = path.read_text(encoding='utf-8')
            pending_count = document.count('data-biomarker-review="pending"')
            signals = re.search(r'<div class="why-signals-context".*?</div>', document, re.S)
            signal_ids = tuple(re.findall(r'data-source-id="([^"]+)"', signals.group())) if signals else ()
            assert len(signal_ids) == len(set(signal_ids)), path
            inventory[path.name] = (pending_count, signal_ids)
            assert pending_count <= 1, path
            blocks = re.findall(r'<div class="why-track".*?</div>', document, re.S)
            assert all('data-biomarker-review=' not in block for block in blocks), path
            if pending_count:
                assert 'data-rationale-scope="plan-findings"' in document, path
                assert 'data-clinical-review="pending"' in document, path
        assert inventory, prefix
        assert any(count for count, ids in inventory.values()), prefix
        if reference is None:
            reference = inventory
        else:
            assert inventory == reference, prefix
