"""Actual engine output must preserve block, route and rescue-clock distinctions."""
import json
from pathlib import Path

import pytest
import yaml

from knowledge_base.engine import generate_plan, render_plan_html

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


@pytest.fixture(scope='module')
def results():
    examples = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    ids = {'bma-bma-myc-rearrangement-burkitt', 'burkitt-high-risk', 'burkitt-low-risk'}
    # Positive synthetic protocol-scope fixtures; original low-risk/CNS cases
    # are separately tested for withholding in test_burkitt_protocol_scope.py.
    profiles = [json.loads(json.dumps(e['json'])) for e in examples if e['case_id'] in ids]
    for profile in profiles:
        profile['findings'].update(burkitt_high_risk=True, cns_involvement=False)
    return [generate_plan(profile, kb_root=KB) for profile in profiles]


def test_actual_phase_and_legacy_views_retain_missing_drug_and_uroprotection(results):
    assert len(results) == 3
    for result in results:
        tracks = [t for t in result.plan.tracks
                  if (t.regimen_data or {}).get('id') == 'REG-CODOX-M-IVAC']
        assert tracks
        for track in tracks:
            regimen = track.regimen_data
            a, b = regimen['phases']
            ifos = [c for c in b['components'] if c['drug_id'] == 'DRUG-IFOSFAMIDE']
            assert len(ifos) == 1 and ifos[0]['dose'] == '1500 mg/m² per day'
            assert 'days 1-5 of IVAC blocks only' in ifos[0]['schedule']
            assert 'mesna and hydration' in ifos[0]['schedule']
            assert len([c for c in b['components'] if c['drug_id'] == 'DRUG-MESNA']) == 2
            assert not any(c['drug_id'] == 'DRUG-IFOSFAMIDE' for c in a['components'])
            assert regimen['components'] == a['components'] + b['components']
            assert track.monitoring_data['id'] == 'MON-CODOX-IVAC-REGIMEN'


def test_separate_routes_and_clocks_do_not_collapse_into_one_methotrexate_recipe():
    regimen = yaml.safe_load((KB / 'regimens/codox_m_ivac.yaml').read_text(encoding='utf-8'))
    a, b = [p['components'] for p in regimen['phases']]
    mtx = [c for c in a if c['drug_id'] == 'DRUG-METHOTREXATE']
    assert {c['route'] for c in mtx} == {'IV', 'IT'}
    assert 'day 10' in next(c for c in mtx if c['route'] == 'IV')['schedule']
    assert 'day 15' in next(c for c in mtx if c['route'] == 'IT')['schedule']
    rescue = next(c for c in a if c['drug_id'] == 'DRUG-LEUCOVORIN' and c['route'] == 'IV')
    assert '36 hours after IV methotrexate START' in rescue['schedule']
    assert '36-48' in rescue['schedule'] and '<0.1 micromol/L' in rescue['schedule']
    oral = [c for c in a + b if c['drug_id'] == 'DRUG-LEUCOVORIN' and c['route'] == 'PO']
    assert len(oral) == 2 and all('24 hours after INTRATHECAL' in c['schedule'] for c in oral)
    assert next(c for c in a if c['drug_id'] == 'DRUG-CYTARABINE')['route'] == 'IT'
    assert 'days 1 and 8' in next(c for c in a if c['drug_id'] == 'DRUG-VINCRISTINE')['schedule']
    assert 'day 13' in next(c for c in a if c['drug_id'] == 'DRUG-FILGRASTIM')['schedule']
    assert 'day 7' in next(c for c in b if c['drug_id'] == 'DRUG-FILGRASTIM')['schedule']
    assert 'days 1 and 9' in next(c for c in a if c['drug_id'] == 'DRUG-RITUXIMAB')['schedule']
    assert 'days 3 and 7' in next(c for c in b if c['drug_id'] == 'DRUG-RITUXIMAB')['schedule']
    assert 'LMB-style' not in regimen['alternate_names']
    assert 'broader eligibility, ranking and other protocol variants' in regimen['notes']
    assert regimen['last_reviewed'] is None


@pytest.mark.parametrize('locale,needle', [
    ('en', 'Assess neurological function before each ifosfamide dose'),
    ('uk', 'Оцініть неврологічний стан перед кожною дозою іфосфаміду'),
])
def test_actual_plan_renders_specific_monitoring_and_explicit_scope(results, locale, needle):
    html = render_plan_html(results[1], target_lang=locale)
    assert needle in html and 'MON-CODOX-IVAC-REGIMEN' in html
    assert 'DRUG-IFOSFAMIDE' in html and 'DRUG-MESNA' in html
    mon = yaml.safe_load((KB / 'monitoring/mon_codox_ivac_regimen.yaml').read_text(encoding='utf-8'))
    assert all(len(p['checkpoints']) == len(p['checkpoints_ua']) for p in mon['phases'])
    assert mon['review_status'] == 'pending_clinical_signoff'
