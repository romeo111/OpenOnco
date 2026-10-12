"""ABVD must materialize its own monitoring in actual generated plans."""
import json
from pathlib import Path
import pytest
import yaml
from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.engine.plan import _materialize_track
from knowledge_base.validation.loader import load_content

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


@pytest.fixture(scope='module')
def early_hodgkin_plan():
    examples = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    profile = next(e['json'] for e in examples if e['case_id'] == 'chl-early')
    return generate_plan(profile, kb_root=KB)


def test_abvd_monitoring_is_resolved_in_actual_plan(early_hodgkin_plan):
    tracks = [t for t in early_hodgkin_plan.plan.tracks if (t.regimen_data or {}).get('id') == 'REG-ABVD']
    assert tracks, 'The synthetic early-stage example must exercise ABVD'
    for track in tracks:
        monitoring = track.monitoring_data
        assert monitoring['id'] == 'MON-ABVD-REGIMEN'
        assert monitoring['linked_to_regimen'] == track.regimen_data['id']
        during = next(p for p in monitoring['phases'] if p['name'] == 'on_treatment')
        assert 'days 1 and 15' in during['window'] and '28-day' in during['window']
        assert 'TEST-CD20-IHC' not in {test for phase in monitoring['phases'] for test in phase['tests']}
        assert 'TEST-PFT-SPIROMETRY-DLCO' not in monitoring['phases'][0]['tests']
        assert 'applicable protocol' in monitoring['phases'][0]['checkpoints'][3]
        assert monitoring['last_reviewed'] is None


@pytest.mark.parametrize('locale,needle', [('en', 'Before each administration on days 1 and 15'), ('uk', 'Перед кожним введенням у дні 1 і 15')])
def test_rendered_hodgkin_monitoring_does_not_leak_rchop(early_hodgkin_plan, locale, needle):
    html = render_plan_html(early_hodgkin_plan, target_lang=locale)
    assert 'MON-ABVD-REGIMEN' in html and needle in html
    assert 'MON-R-CHOP-REGIMEN' not in html
    assert 'Confirm CD20+ DLBCL histology' not in html
    assert 'Day 1 of every 21-day cycle' not in html
    assert 'ANC ≥1500 + platelets ≥100K' not in html
    assert 'Підтвердити CD20+ DLBCL гістологію' not in html


def test_abvd_checks_are_parallel_and_do_not_claim_full_surveillance():
    data = yaml.safe_load((KB / 'monitoring/mon_abvd_regimen.yaml').read_text(encoding='utf-8'))
    for phase in data['phases']:
        assert len(phase['checkpoints']) == len(phase['checkpoints_ua'])
        assert phase['window'] and phase['window_ua']
    assert 'complete survivorship' in data['notes']
    assert data['sources'] == ['SRC-EVIQ-ABVD-56', 'SRC-BSH-CHL-BLEOMYCIN-2025']


def test_advanced_hodgkin_tracks_have_distinct_monitoring():
    examples = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    profile = next(e['json'] for e in examples if e['case_id'] == 'chl-advanced')
    result = generate_plan(profile, kb_root=KB)
    expected = {'REG-ABVD': 'MON-ABVD-REGIMEN', 'REG-A-AVD': 'MON-A-AVD-REGIMEN', 'REG-NIVO-AVD': 'MON-NIVO-AVD-REGIMEN'}
    seen = set()
    for track in result.plan.tracks:
        regimen = (track.regimen_data or {}).get('id')
        if regimen in expected:
            seen.add(regimen)
            assert track.monitoring_data['id'] == expected[regimen]
            assert track.monitoring_data['linked_to_regimen'] == regimen
    assert {'REG-ABVD', 'REG-A-AVD'} <= seen
    # N-AVD is not selected by this legacy fixture's algorithm. Exercise
    # actual track materialization explicitly without changing selection.
    nivo = _materialize_track('aggressive', 'IND-CHL-1L-N-AVD', False, 'Synthetic materialization check', load_content(KB).entities_by_id)
    assert nivo.monitoring_data['id'] == 'MON-NIVO-AVD-REGIMEN'
    assert nivo.monitoring_data['linked_to_regimen'] == nivo.regimen_data['id']
    for locale in ['en', 'uk']:
        html = render_plan_html(result, target_lang=locale)
        assert 'MON-R-CHOP-REGIMEN' not in html
        assert 'Confirm CD20+ DLBCL histology' not in html
    for name in ['mon_a_avd_regimen.yaml', 'mon_nivo_avd_regimen.yaml']:
        monitoring = yaml.safe_load((KB / 'monitoring' / name).read_text(encoding='utf-8'))
        for phase in monitoring['phases']:
            assert len(phase['checkpoints']) == len(phase['checkpoints_ua'])
    nivolumab = yaml.safe_load((KB / 'monitoring/mon_nivo_avd_regimen.yaml').read_text(encoding='utf-8'))
    assert {'TEST-TSH', 'TEST-CORTISOL-MORNING'} <= set(nivolumab['phases'][0]['tests'])
    bv = yaml.safe_load((KB / 'monitoring/mon_a_avd_regimen.yaml').read_text(encoding='utf-8'))
    assert any('primary G-CSF prophylaxis' in c for c in bv['phases'][1]['checkpoints'])
