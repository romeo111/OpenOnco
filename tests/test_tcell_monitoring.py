"""T-cell plans must not inherit B-cell diagnostic or drug checkpoints."""
import json
from pathlib import Path
import pytest
import yaml
from knowledge_base.engine import generate_plan, render_plan_html

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


@pytest.mark.parametrize('case_id', ['aitl-cd30-positive', 'alcl-alk-positive-typical', 'ptcl-cd30-positive'])
def test_actual_tcell_plans_resolve_drug_specific_monitoring(case_id):
    examples = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    profile = next(e['json'] for e in examples if e['case_id'] == case_id)
    result = generate_plan(profile, kb_root=KB)
    expected = {'REG-CHP-BV': 'MON-CHP-BV-REGIMEN', 'REG-CHOEP': 'MON-CHOEP-REGIMEN'}
    seen = set()
    for track in result.plan.tracks:
        reg = (track.regimen_data or {}).get('id')
        if reg not in expected:
            continue
        seen.add(reg)
        mon = track.monitoring_data
        assert mon['id'] == expected[reg] and mon['linked_to_regimen'] == reg
        assert mon['last_reviewed'] is None
        assert 'TEST-CD20-IHC' not in {test for phase in mon['phases'] for test in phase['tests']}
        assert '21-day' in mon['phases'][1]['window']
    assert seen == set(expected)
    for locale in ['en', 'uk']:
        html = render_plan_html(result, target_lang=locale)
        assert 'MON-R-CHOP-REGIMEN' not in html
        assert 'Confirm CD20+ DLBCL histology' not in html
        assert 'Підтвердити CD20+ DLBCL гістологію' not in html
        assert 'ANC ≥1500 + platelets ≥100K' not in html


def test_monitors_preserve_distinct_drugs_counts_and_parallel_ukrainian():
    records = {name: yaml.safe_load((KB / 'monitoring' / name).read_text(encoding='utf-8')) for name in ['mon_chp_bv_regimen.yaml', 'mon_choep_regimen.yaml']}
    for mon in records.values():
        for phase in mon['phases']:
            assert len(phase['checkpoints']) == len(phase['checkpoints_ua'])
            assert phase['window'] and phase['window_ua']
    bv = records['mon_chp_bv_regimen.yaml']['phases'][1]
    choep = records['mon_choep_regimen.yaml']['phases'][1]
    assert 'brentuximab vedotin' in bv['checkpoints'][1]
    assert 'vincristine is not a component' in bv['checkpoints'][1]
    assert 'ANC <1.0 × 10^9/L' in bv['checkpoints'][0]
    assert 'Cycle 1' in bv['checkpoints'][2] and 'US label' in bv['checkpoints'][2]
    assert 'eviQ 4038' in bv['checkpoints'][2]
    regimen = yaml.safe_load((KB / 'regimens/chp_bv.yaml').read_text(encoding='utf-8'))
    assert 'SUP-GCSF-NEUTROPENIA' in regimen['mandatory_supportive_care']
    claim = next(c for c in regimen['clinical_claims'] if c['claim_id'] == 'bv-chp-primary-gcsf-us-label')
    assert claim['source_ids'] == ['SRC-ADCETRIS-US-LABEL', 'SRC-EVIQ-BV-CHP-4038']
    assert 'dose modification is not generally indicated' in choep['checkpoints'][1]
    assert 'review of vincristine' in choep['checkpoints'][2]
    assert 'days 1-3' in choep['window']
