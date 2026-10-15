"""BV-specific safety must not inherit myeloma substitutions or pooled dose rules."""
import copy
import json
from pathlib import Path

import pytest
import yaml
from bs4 import BeautifulSoup

from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.engine._patient_watchpoint_translations import translate_watchpoint

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


def result(case='aitl-cd30-positive'):
    rows = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    return generate_plan(copy.deepcopy(next(row['json'] for row in rows if row['case_id'] == case)), kb_root=KB)


@pytest.mark.parametrize('case', ['aitl-cd30-positive', 'ptcl-cd30-positive', 'alcl-alk-negative'])
def test_bv_tracks_surface_own_contraindication_without_myeloma_substitutions(case):
    plan = result(case)
    track = next(t for t in plan.plan.tracks if t.regimen_data['id'] == 'REG-CHP-BV')
    ids = {ci['id'] for ci in track.contraindications_data}
    assert 'CI-BRENTUXIMAB-BLEOMYCIN' in ids
    assert 'CI-BORTEZOMIB-SEVERE-NEUROPATHY' not in ids
    ci = next(ci for ci in track.contraindications_data if ci['id'] == 'CI-BRENTUXIMAB-BLEOMYCIN')
    assert set(ci['affects_drugs']) == {'DRUG-BRENTUXIMAB-VEDOTIN', 'DRUG-BLEOMYCIN'}
    assert ci['sources'] == ['SRC-ADCETRIS-US-LABEL']
    for locale in ['en', 'uk']:
        output = render_plan_html(plan, target_lang=locale)
        assert 'CI-BORTEZOMIB-SEVERE-NEUROPATHY' not in output
        assert 'Consider carfilzomib-based regimen' not in output
        assert 'Grade ≥2 baseline = absolute CI' not in output


def test_adult_combination_rows_keep_grade_type_and_protocol_separate():
    regimen = yaml.safe_load((KB / 'regimens/chp_bv.yaml').read_text(encoding='utf-8'))
    rows = regimen['dose_adjustments']
    sensory2 = next(row for row in rows if row['condition'].startswith('US') and 'grade 2 sensory' in row['condition'])
    motor2 = next(row for row in rows if row['condition'].startswith('US') and 'grade 2 motor' in row['condition'])
    assert 'Same-dose' in sensory2['modification'] and 'Delay' not in sensory2['modification']
    assert '1.2 mg/kg' in motor2['modification'] and 'maximum 120 mg' in motor2['modification']
    assert 'Delay' not in motor2['modification']
    protocol = next(row for row in rows if row['condition'].startswith('eviQ') and 'grade 2 motor' in row['condition'])
    assert 'Delay until grade 1 or baseline' in protocol['modification']
    assert sensory2['source_refs'] == ['SRC-ADCETRIS-US-LABEL']
    assert protocol['source_refs'] == ['SRC-EVIQ-BV-CHP-4038']
    assert not any(row['condition'] == 'Grade ≥2 peripheral neuropathy' for row in rows)
    assert 'monotherapy' in regimen['notes'] and 'pediatric' in regimen['notes']


def test_patient_points_remove_unsafe_cycle_windows_and_self_dose_changes():
    reg = yaml.safe_load((KB / 'regimens/chp_bv.yaml').read_text(encoding='utf-8'))
    points = reg['between_visit_watchpoints']
    assert len(points) == 12
    assert all(not point.get('cycle_day_window') for point in points)
    assert all(point['sources'] == ['SRC-EVIQ-BV-CHP-PATIENT-4038'] for point in points)
    fever = next(point for point in points if '38°C' in point['trigger_ua'])
    assert fever['urgency'] == 'contact_clinic_now'
    assert 'навіть без температури' in fever['trigger_ua']
    ordinary = points[0]
    assert ordinary['urgency'] == 'contact_clinic'
    assert 'потрібна корекція дози' not in json.dumps(points, ensure_ascii=False)
    assert any('не змінюйте дозу самостійно' in point['action_ua'] for point in points)
    assert sum(point['urgency'] == 'contact_clinic_now' for point in points) == 7


def test_complete_english_pairs_are_source_bound_and_marked_as_drafts():
    plan = result()
    reg = next(t.regimen_data for t in plan.plan.tracks if t.regimen_data['id'] == 'REG-CHP-BV')
    assert all(translate_watchpoint(reg['id'], point) for point in reg['between_visit_watchpoints'])
    stale = copy.deepcopy(reg['between_visit_watchpoints'][0])
    stale['urgency'] = 'log_at_next_visit'
    assert translate_watchpoint(reg['id'], stale) is None
    output = BeautifulSoup(render_plan_html(plan, target_lang='en', mode='patient'), 'html.parser')
    track = output.select_one('.bv-track[data-source-id="REG-CHP-BV"]')
    assert track and len(track.select('.bv-trigger[lang="en"][data-original-source]')) == 12
    assert len(track.select('[data-translation-status="draft_pending_clinical_and_language_review"]')) == 24
    assert 'Contact your doctor or nurse immediately' in track.get_text()
    assert 'do not change the dose yourself' in track.get_text()
