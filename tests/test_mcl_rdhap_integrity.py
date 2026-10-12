"""MCL alternating induction must retain the actual R-DHAP drugs and monitoring."""
import json
from pathlib import Path
import pytest
import yaml
from knowledge_base.engine import generate_plan, render_plan_html

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


@pytest.fixture(scope='module')
def mcl_plan():
    examples = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    profile = next(e['json'] for e in examples if e['case_id'] == 'mcl-fit-younger')
    return generate_plan(profile, kb_root=KB)


def test_actual_mcl_track_contains_missing_platinum_and_two_cytarabine_doses(mcl_plan):
    track = next(t for t in mcl_plan.plan.tracks if (t.regimen_data or {}).get('id') == 'REG-MCL-INTENSIVE-RDHAP-AUTOSCT')
    regimen = track.regimen_data
    components = regimen['phases'][0]['components']
    # Materialization also fills the legacy component view. It must retain
    # the same block-specific administration restrictions as the phase.
    assert regimen['components'] == components
    cisplatin = [c for c in components if c['drug_id'] == 'DRUG-CISPLATIN']
    assert len(cisplatin) == 1
    assert cisplatin[0]['dose'] == '100 mg/m²'
    assert '24 hours' in cisplatin[0]['schedule']
    assert 'day 1 of R-DHAP cycles only (cycles 2, 4, 6)' in cisplatin[0]['schedule']
    cytarabine = next(c for c in components if c['drug_id'] == 'DRUG-CYTARABINE')
    assert cytarabine['dose'] == '2 g/m² per dose'
    assert 'two doses 12 hours apart on day 2' in cytarabine['schedule']
    assert regimen['last_reviewed'] is None
    assert 'Nordic regimen' not in regimen['alternate_names']
    assert 'separate protocol' in regimen['total_cycles']
    assert 'both cisplatin and high-dose cytarabine' in regimen['dose_adjustments'][1]['modification']


@pytest.mark.parametrize('locale,needle', [('en', 'Assess cerebellar function before every'), ('uk', 'Оцініть функцію мозочка перед кожною')])
def test_actual_plan_renders_rdhap_specific_monitoring(mcl_plan, locale, needle):
    html = render_plan_html(mcl_plan, target_lang=locale)
    assert 'MON-MCL-RCHOP-RDHAP-INDUCTION' in html
    assert needle in html
    assert 'MON-R-CHOP-REGIMEN' not in html
    assert 'Confirm CD20+ DLBCL histology' not in html
    assert 'DRUG-CISPLATIN' in html
    assert ('On treatment: R-DHAP' if locale == 'en' else 'Під час лікування: R-DHAP') in html
    assert ('Assessment before consolidation' if locale == 'en' else 'Оцінка перед консолідацією') in html


def test_endpoint_and_monitoring_scope_do_not_claim_transplant_or_whole_record_approval():
    indication = yaml.safe_load((KB / 'indications/ind_mcl_1l_intensive.yaml').read_text(encoding='utf-8'))
    assert 'time to treatment failure' in indication['expected_outcomes']['progression_free_survival']
    assert indication['last_reviewed'] is None
    monitoring = yaml.safe_load((KB / 'monitoring/mon_mcl_rchop_rdhap_induction.yaml').read_text(encoding='utf-8'))
    assert 'Not a complete transplant' in monitoring['notes']
    for phase in monitoring['phases']:
        assert len(phase['checkpoints']) == len(phase['checkpoints_ua'])
    rdhap = next(p for p in monitoring['phases'] if p['name'] == 'on_treatment_rdhap')
    assert '72 hours' in rdhap['checkpoints'][2]
    assert 'audiometry' in rdhap['checkpoints'][3]
