"""Unreviewed historical allo-CR1 reference must not become a routine PTCL route."""
import json
from pathlib import Path

import pytest

from knowledge_base.engine import generate_plan

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


@pytest.mark.parametrize('age', [18, 45, 65])
@pytest.mark.parametrize('ecog', [0, 1])
@pytest.mark.parametrize('case_id', ['ptcl-cd30-negative', 'ptcl-cd30-positive'])
def test_fit_firstline_profiles_do_not_auto_select_unsupported_allo_cr1_reference(age, ecog, case_id):
    examples = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    profile = json.loads(json.dumps(next(e['json'] for e in examples if e['case_id'] == case_id)))
    profile.setdefault('demographics', {}).update(age=age, ecog=ecog)
    result = generate_plan(profile, kb_root=KB)
    assert result.plan and result.plan.tracks
    assert result.default_indication_id != 'IND-PTCL-1L-CHOEP-ALLOSCT'
    assert all(t.indication_id != 'IND-PTCL-1L-CHOEP-ALLOSCT' for t in result.plan.tracks)
    assert all((t.regimen_data or {}).get('id') != 'REG-CHOEP-ALLOSCT-CONSOLIDATION'
               for t in result.plan.tracks)
    expected = {'REG-CHOEP': 'MON-CHOEP-REGIMEN', 'REG-CHP-BV': 'MON-CHP-BV-REGIMEN'}
    for track in result.plan.tracks:
        regimen = (track.regimen_data or {}).get('id')
        assert regimen in expected
        assert track.monitoring_data['id'] == expected[regimen]
