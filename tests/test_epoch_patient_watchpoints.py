"""DA-EPOCH patient instructions must not delay source-defined urgent contact."""
import json
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from knowledge_base.engine import generate_plan, render_plan_html

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


@pytest.fixture(scope='module')
def result():
    examples = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    profile = next(e['json'] for e in examples if e['case_id'] == 'pmbcl-typical')
    return generate_plan(profile, kb_root=KB)


@pytest.mark.parametrize('language', ['uk', 'en'])
def test_actual_patient_output_places_breathing_and_fever_in_immediate_contact(result, language):
    soup = BeautifulSoup(render_plan_html(result, target_lang=language, mode='patient'), 'html.parser')
    track = soup.select_one('.between-visits .bv-track[data-source-id="REG-DA-EPOCH-R"]')
    assert track
    heading = ('Contact your doctor or nurse immediately' if language == 'en'
               else 'Негайно зв’яжіться з лікарем або медсестрою')
    group = next(g for g in track.select('.bv-urgency-group') if heading in g.get_text())
    text = group.get_text(' ', strip=True)
    symptoms = ['A temperature of 38°C or higher', 'New shortness of breath',
                'Uncontrolled vomiting', 'Unable to eat or drink', 'New problems with speech'] if language == 'en' else ['Температура 38°C або вище', 'Нова задишка',
                    'Неконтрольоване блювання', 'Не можете їсти чи пити',
                    'Нові проблеми з мовленням']
    for symptom in symptoms:
        assert symptom in text
    assert ('After leaving the clinic' if language == 'en' else 'Після виходу з клініки') in text
    assert 'Day 7-14' not in text and 'Day 1 of cycle 1' not in text
    assert 'того ж дня' not in text
    assert 'Лихоманка вище 38°C' not in track.get_text()
    assert 'Занотуйте і обговоріть на наступному візиті' not in track.get_text()


def test_urgent_sources_and_nonurgent_notifications_preserve_scope(result):
    regimen = next(t.regimen_data for t in result.plan.tracks
                   if (t.regimen_data or {}).get('id') == 'REG-DA-EPOCH-R')
    points = regimen['between_visit_watchpoints']
    urgent = [w for w in points if w['urgency'] == 'contact_clinic_now']
    assert len(urgent) == 6
    assert all(not w.get('cycle_day_window') for w in urgent)
    assert all(w['sources'] for w in points)
    routine = [w for w in points if w['urgency'] == 'contact_clinic']
    assert len(routine) == 4
    assert any(w['trigger_ua'] == 'Виражена втома' for w in routine)
    assert any('Поколювання' in w['trigger_ua'] for w in routine)
    assert regimen['last_reviewed'] is None
