"""Explicit CNS variant has independently sourced patient contact instructions."""
import json
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from knowledge_base.engine import generate_plan, render_plan_html

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


@pytest.fixture(scope='module')
def result():
    profile = json.loads((ROOT / 'examples/patient_burkitt_high_risk.json').read_text())
    profile['findings']['burkitt_protocol_variant'] = 'eviq_proven_cns'
    return generate_plan(profile, kb_root=KB)


@pytest.mark.parametrize('language', ['en', 'uk'])
def test_actual_selected_cns_report_has_contact_actions_instead_of_empty_fallback(result, language):
    assert len(result.plan.tracks) == 1
    soup = BeautifulSoup(render_plan_html(result, mode='patient', target_lang=language), 'html.parser')
    section = soup.select_one('.between-visits .bv-track[data-source-id="REG-CODOX-IVAC-PROVEN-CNS"]')
    assert section and not section.select_one('.bv-fallback')
    heading = ('Contact your doctor or nurse immediately' if language == 'en'
               else 'Негайно зв’яжіться з лікарем або медсестрою')
    urgent = next(group for group in section.select('.bv-urgency-group') if heading in group.get_text())
    symptoms = ['A temperature of 38°C or higher', 'New shortness of breath',
                'Very severe headache', 'New confusion', 'Unable to eat or drink'] if language == 'en' else ['Температура 38°C або вище', 'Нова задишка',
                    'Дуже сильний головний біль', 'Нова сплутаність', 'Не можете їсти чи пити']
    for symptom in symptoms:
        assert symptom in urgent.get_text()
    assert ('If you cannot reach' if language == 'en' else 'Якщо не можете зв’язатися') in urgent.get_text()
    assert ('After leaving the clinic' if language == 'en' else 'Після виходу з клініки') in urgent.get_text()


def test_each_symptom_uses_own_protocol_or_explicit_linked_mouth_source(result):
    reg = result.plan.tracks[0].regimen_data
    points = reg['between_visit_watchpoints']
    assert len(points) == 12
    allowed = {'SRC-EVIQ-CNS-CODOX-PATIENT-4492', 'SRC-EVIQ-CNS-IVAC-PATIENT-4493',
               'SRC-EVIQ-MOUTH-PATIENT-3099'}
    assert all(point['sources'] and set(point['sources']) <= allowed for point in points)
    assert all(not point.get('cycle_day_window') for point in points)
    assert reg['last_reviewed'] is None and reg['review_status'] == 'pending_clinical_signoff'
    kidney = next(point for point in points if 'кількості сечі' in point['trigger_ua'])
    assert kidney['urgency'] == 'contact_clinic'
    assert 'Якнайшвидше' in kidney['action_ua']
    assert not any('літр' in point['action_ua'] for point in points)
    general_neuro = next(point for point in points if 'незалежно від дня циклу' in point['trigger_ua'])
    assert general_neuro['urgency'] == 'contact_clinic_now'


def test_unselected_original_cns_profile_remains_withheld():
    profile = json.loads((ROOT / 'examples/patient_burkitt_high_risk.json').read_text())
    result = generate_plan(profile, kb_root=KB)
    assert not result.plan.tracks and result.default_indication_id is None
