"""Explicit source-variant selection must never blend CNS and no-CNS references."""
import json
from pathlib import Path

import pytest
import yaml

from knowledge_base.engine import generate_plan, render_plan_html

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'
CNS_IND = 'IND-BURKITT-1L-CODOX-IVAC-PROVEN-CNS'


def profile():
    data = json.loads((ROOT / 'examples/patient_burkitt_high_risk.json').read_text())
    data['findings']['burkitt_protocol_variant'] = 'eviq_proven_cns'
    return data


def test_explicit_matching_variant_materializes_separate_source_and_calendar():
    result = generate_plan(profile(), kb_root=KB)
    assert result.default_indication_id == CNS_IND
    assert len(result.plan.tracks) == 1  # Explicit variant never exposes another protocol
    track = next(t for t in result.plan.tracks if t.indication_id == CNS_IND)
    reg = track.regimen_data
    assert reg['id'] == 'REG-CODOX-IVAC-PROVEN-CNS'
    assert track.monitoring_data['id'] == 'MON-CODOX-IVAC-PROVEN-CNS'
    a, b = [phase['components'] for phase in reg['phases']]
    assert reg['components'] == a + b
    assert 'days 1 and 11' in next(c for c in a if c['drug_id'] == 'DRUG-RITUXIMAB')['schedule']
    assert 'days 1, 3 and 5' in next(c for c in a if c['drug_id'] == 'DRUG-CYTARABINE')['schedule']
    assert 'days 15 and 17' in next(c for c in a if c['drug_id'] == 'DRUG-METHOTREXATE' and c['route'] == 'IT')['schedule']
    assert 'reference days 16 and 18' in next(c for c in a if c['drug_id'] == 'DRUG-LEUCOVORIN' and c['route'] == 'PO')['schedule']
    assert {c['route'] for c in b if c['drug_id'] == 'DRUG-CYTARABINE'} == {'IV', 'IT'}
    assert 'days 7 and 9' in next(c for c in b if c['drug_id'] == 'DRUG-CYTARABINE' and c['route'] == 'IT')['schedule']
    assert all((t.regimen_data or {}).get('id') != 'REG-CODOX-M-IVAC' for t in result.plan.tracks)
    assert 'committee adaptation' in reg['notes'] and '16 IT treatments' in reg['notes']
    assert reg['last_reviewed'] is None
    assert 'expected_outcomes' not in track.indication_data
    assert 'ukraine_availability' not in reg


@pytest.mark.parametrize('field,value', [
    ('cns_involvement', False), ('cns_involvement', None),
    ('cns_involvement', 'true'), ('cns_involvement', 1),
    ('burkitt_high_risk', False), ('burkitt_high_risk', None),
    ('burkitt_high_risk', 'true'),
])
def test_opt_in_with_failed_scope_never_substitutes_another_regimen(field, value):
    data = profile()
    data['findings'][field] = value
    result = generate_plan(data, kb_root=KB)
    assert not result.plan.tracks and result.default_indication_id is None
    assert result.plan.knowledge_base_state['profile_selection_withheld']


@pytest.mark.parametrize('variant', [None, 'unknown', 'other_trial', True])
def test_cns_status_without_exact_variant_does_not_opt_in(variant):
    data = profile()
    data['findings']['burkitt_protocol_variant'] = variant
    result = generate_plan(data, kb_root=KB)
    assert not result.plan.tracks and result.default_indication_id is None


def test_cross_section_conflict_blocks_even_explicit_variant():
    data = profile()
    data['disease']['cns_involvement'] = False
    result = generate_plan(data, kb_root=KB)
    assert not result.plan.tracks


@pytest.mark.parametrize('locale,needle', [
    ('en', 'CNS-specific eviQ CODOX-M reference'),
    ('uk', 'Довідковий CODOX-M eviQ для ураження ЦНС'),
])
def test_render_discloses_identified_variant_and_separate_monitor(locale, needle):
    result = generate_plan(profile(), kb_root=KB)
    html = render_plan_html(result, target_lang=locale)
    assert needle in html and 'MON-CODOX-IVAC-PROVEN-CNS' in html
    assert 'DRUG-IFOSFAMIDE' in html and 'DRUG-MESNA' in html


def test_variant_question_has_no_implicit_choice():
    q = yaml.safe_load((KB / 'questionnaires/quest_burkitt_1l.yaml').read_text(encoding='utf-8'))
    question = next(i for g in q['groups'] for i in g['questions'] if i['field'] == 'findings.burkitt_protocol_variant')
    assert 'default_value' not in question
    assert question['options'][0]['value'] == 'eviq_proven_cns'
