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
    assert ('A temperature of 38°C or higher' if language == 'en' else 'Температура 38°C або вище') in text
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
    assert ('marked fatigue' if language == 'en' else 'виражену втому') in routine.get_text()
    assert ('Unable to eat or drink' if language == 'en' else 'Не можете їсти чи пити') in immediate.get_text()
    assert ('New confusion' if language == 'en' else 'Нова сплутаність') in immediate.get_text()
    assert ('Very severe headache' if language == 'en' else 'Дуже сильний головний біль') in immediate.get_text()
    assert ('If you cannot reach' if language == 'en' else 'Якщо не можете зв’язатися') in immediate.get_text()


@pytest.mark.parametrize('urgency', ['contact_clinic', 'contact_clinic_now'])
def test_new_contact_tiers_are_validated_without_inventing_a_deadline(urgency):
    point = BetweenVisitWatchpoint(trigger_ua='Симптом', action_ua='Дія', urgency=urgency)
    assert point.urgency == urgency


def test_patient_sources_and_protocol_boundary_are_explicit(result):
    regimen = next(t.regimen_data for t in result.plan.tracks
                   if (t.regimen_data or {}).get('id') == 'REG-CODOX-M-IVAC')
    urgent = [w for w in regimen['between_visit_watchpoints']
              if w['urgency'] == 'contact_clinic_now']
    assert len(urgent) == 5
    for point in urgent:
        assert point['sources']
        for sid in point['sources']:
            matches = [yaml.safe_load(p.read_text(encoding='utf-8'))
                       for p in (KB / 'sources').glob('src_eviq_*.yaml')]
            source = next(s for s in matches if s['id'] == sid)
            assert source['source_type'] in {'patient_information', 'clinical_resource'}
            assert source['url'].startswith('https://www.eviq.org.au/')
    cns = yaml.safe_load((KB / 'regimens/codox_ivac_proven_cns.yaml').read_text(encoding='utf-8'))
    assert cns.get('between_visit_watchpoints')
    assert not any(sid in {'SRC-EVIQ-CODOX-PATIENT-4489', 'SRC-EVIQ-IVAC-PATIENT-4490'}
                   for point in cns['between_visit_watchpoints'] for sid in point['sources'])


def test_kidney_contact_and_tls_emergency_have_no_invented_calendar_limits(result):
    regimen = next(t.regimen_data for t in result.plan.tracks
                   if (t.regimen_data or {}).get('id') == 'REG-CODOX-M-IVAC')
    kidney = next(point for point in regimen['between_visit_watchpoints'] if 'кількості сечі' in point['trigger_ua'])
    assert kidney['urgency'] == 'contact_clinic' and 'Якнайшвидше' in kidney['action_ua']
    assert 'того ж дня' not in kidney['action_ua']
    tls = next(point for point in regimen['between_visit_watchpoints'] if 'м’язові спазми' in point['trigger_ua'])
    assert tls['urgency'] == 'contact_clinic_now' and not tls.get('cycle_day_window')
    assert 'і до лікування' in tls['action_ua'] and 'не доводять діагноз' in tls['action_ua']
    assert 'SRC-EVIQ-TLS-108' in tls['sources']
    soup = BeautifulSoup(render_plan_html(result, mode='patient', target_lang='en'), 'html.parser')
    section = soup.select_one('.bv-track[data-source-id="REG-CODOX-M-IVAC"]')
    assert not section.select('.translation-fallback')
    assert 'before treatment' in section.get_text()
    assert 'as soon as possible' in section.get_text()
    assert 'Swollen ankles' in section.get_text()
    assert 'after treatment has finished' in section.get_text()
