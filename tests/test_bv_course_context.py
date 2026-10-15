"""A shared BV reference must not invent an individual course or omit its cap."""
import copy
import json
from pathlib import Path

import pytest
import yaml
from bs4 import BeautifulSoup

from knowledge_base.engine import generate_plan, render_plan_html

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


def profile(case='aitl-cd30-positive'):
    entries = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    return copy.deepcopy(next(row['json'] for row in entries if row['case_id'] == case))


@pytest.mark.parametrize('weight', [50, 100, 120])
def test_reference_keeps_maximum_without_inventing_a_patient_dose(weight):
    patient = profile()
    patient['demographics']['weight_kg'] = weight
    before = copy.deepcopy(patient)
    result = generate_plan(patient, kb_root=KB)
    reg = result.plan.tracks[0].regimen_data
    component = next(c for c in reg['components'] if c['drug_id'] == 'DRUG-BRENTUXIMAB-VEDOTIN')
    assert component['dose'] == '1.8 mg/kg (maximum 180 mg)'
    assert reg['total_cycles'] is None
    assert '× 6' not in component['schedule']
    assert patient == before


@pytest.mark.parametrize('case', ['aitl-cd30-positive', 'ptcl-cd30-positive', 'alcl-alk-negative'])
@pytest.mark.parametrize('age', [None, 17, 17.9, True, '18'])
def test_unconfirmed_adult_age_withholds_selected_reference_without_substitution(case, age):
    patient = profile(case)
    patient['demographics']['age'] = age
    result = generate_plan(patient, kb_root=KB)
    assert not result.plan.tracks and not result.plan.sequencing_tracks
    assert result.default_indication_id is None
    assert 'demographics.age' in result.plan.knowledge_base_state['unconfirmed_profile_fields']
    for lang in ['en', 'uk']:
        output = render_plan_html(result, target_lang=lang, mode='patient')
        assert ('adult age' if lang == 'en' else 'вік дорослого') in output
        assert 'Check metastatic stage' not in output


@pytest.mark.parametrize('mode', ['patient', 'clinician'])
@pytest.mark.parametrize('lang', ['en', 'uk'])
def test_both_reports_show_explicit_course_uncertainty_as_original_source(mode, lang):
    result = generate_plan(profile(), kb_root=KB)
    output = BeautifulSoup(render_plan_html(result, target_lang=lang, mode=mode), 'html.parser')
    note = output.select_one('.course-context[data-source-id="REG-CHP-BV"]')
    assert note and note.has_attr('data-original-source') and note['lang'] == lang
    text = note.get_text()
    assert '6–8' in text and '3–4' in text and 'IPI 0–1' in text
    assert 'ESMO' in text and 'ALCL' in text
    assert ('No course is selected' if lang == 'en' else 'не обирає тривалість') in text
    assert 'maximum 180 mg' in str(output) if mode == 'clinician' else True


def test_course_note_is_escaped_and_unrelated_regimens_keep_their_existing_duration():
    result = copy.deepcopy(generate_plan(profile(), kb_root=KB))
    reg = result.plan.tracks[0].regimen_data
    reg['course_context_note'] = '<img src=x onerror="attack()">'
    output = BeautifulSoup(render_plan_html(result, target_lang='en'), 'html.parser')
    note = output.select_one('.course-context[data-source-id="REG-CHP-BV"]')
    assert note and not note.select('img') and '<img' in note.get_text()
    negative = generate_plan(profile('ptcl-cd30-negative'), kb_root=KB)
    choep = next(t.regimen_data for t in negative.plan.tracks if t.regimen_data['id'] == 'REG-CHOEP')
    assert choep['total_cycles'] is not None
    assert 'course_context_note' not in choep
    source = yaml.safe_load((KB / 'regimens/chp_bv.yaml').read_text(encoding='utf-8'))
    assert source['review_status'] == 'pending_clinical_signoff'
