"""Source-backed contact instructions must survive actual patient rendering."""
import json
from pathlib import Path

import pytest
import yaml
from bs4 import BeautifulSoup

from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.schemas.regimen import BetweenVisitWatchpoint

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


@pytest.fixture(scope='module')
def result():
    examples = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    profile = json.loads(json.dumps(next(e['json'] for e in examples
                                        if e['case_id'] == 'burkitt-high-risk')))
    profile['findings'].update(burkitt_high_risk=True, cns_involvement=False)
    return generate_plan(profile, kb_root=KB)


@pytest.mark.parametrize('language', ['uk', 'en'])
def test_contact_advice_is_not_reclassified_as_next_visit_or_hospital(result, language):
    soup = BeautifulSoup(render_plan_html(result, mode='patient', target_lang=language), 'html.parser')
    section = soup.select_one('.between-visits .bv-track[data-source-id="REG-CODOX-M-IVAC"]')
    assert section
    text = section.get_text(' ', strip=True)
    assert 'Температура 38°C або вище' in text
    assert 'Лихоманка вище 38°C' not in text
    assert 'Очікувано — кістковий мозок' not in text
    assert 'лежіть рівно' not in text
    routine_heading = 'Tell your doctor or nurse' if language == 'en' else 'Повідомте лікаря або медсестру'
    immediate_heading = ('Contact your doctor or nurse immediately' if language == 'en'
                         else 'Негайно зв’яжіться з лікарем або медсестрою')
    assert routine_heading in text and immediate_heading in text
    routine = next(g for g in section.select('.bv-urgency-group')
                   if routine_heading in g.get_text())
    immediate = next(g for g in section.select('.bv-urgency-group')
                     if immediate_heading in g.get_text())
    assert 'виражену втому' in routine.get_text()
    assert 'Не можете їсти чи пити' in immediate.get_text()
    assert 'Нова сплутаність' in immediate.get_text()
    assert 'Дуже сильний головний біль' in immediate.get_text()
    assert 'Якщо не можете зв’язатися' in immediate.get_text()


@pytest.mark.parametrize('urgency', ['contact_clinic', 'contact_clinic_now'])
def test_new_contact_tiers_are_validated_without_inventing_a_deadline(urgency):
    point = BetweenVisitWatchpoint(trigger_ua='Симптом', action_ua='Дія', urgency=urgency)
    assert point.urgency == urgency


def test_patient_sources_and_protocol_boundary_are_explicit(result):
    regimen = next(t.regimen_data for t in result.plan.tracks
                   if (t.regimen_data or {}).get('id') == 'REG-CODOX-M-IVAC')
    urgent = [w for w in regimen['between_visit_watchpoints']
              if w['urgency'] == 'contact_clinic_now']
    assert len(urgent) == 3
    for point in urgent:
        assert point['sources']
        for sid in point['sources']:
            matches = [yaml.safe_load(p.read_text(encoding='utf-8'))
                       for p in (KB / 'sources').glob('src_eviq_*patient*.yaml')]
            source = next(s for s in matches if s['id'] == sid)
            assert source['source_type'] == 'patient_information'
            assert source['url'].startswith('https://www.eviq.org.au/')
    cns = yaml.safe_load((KB / 'regimens/codox_ivac_proven_cns.yaml').read_text(encoding='utf-8'))
    assert cns.get('between_visit_watchpoints')
    assert not any(sid in {'SRC-EVIQ-CODOX-PATIENT-4489', 'SRC-EVIQ-IVAC-PATIENT-4490'}
                   for point in cns['between_visit_watchpoints'] for sid in point['sources'])
