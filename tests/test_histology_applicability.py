import copy
import json
from pathlib import Path

import pytest
from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.engine.histology import histology_confirmed

IND = {'applicable_to': {'histology_allowed_values': ['non-squamous', 'nonsquamous', 'adenocarcinoma']}}


@pytest.mark.parametrize('value', [None, '', 'unknown', 'squamous', 'non-squamous / squamous', [], {}, 1, False])
def test_missing_ambiguous_or_wrong_histology_cannot_confirm(value):
    assert not histology_confirmed(IND, {'findings': {'histology': value}})


def test_explicit_values_and_conflicting_namespaces():
    assert histology_confirmed(IND, {'findings': {'histology': 'ADENOCARCINOMA'}})
    assert histology_confirmed(IND, {'disease': {'histology': 'non_squamous'}})
    assert not histology_confirmed(IND, {'disease': {'histology': 'adenocarcinoma'}, 'findings': {'histology': 'squamous'}})
    assert histology_confirmed({'applicable_to': {}}, {})


@pytest.mark.parametrize('histology', ['adenocarcinoma', 'squamous', None, 'unknown'])
def test_real_nsclc_route_requires_positive_histology_and_never_promotes_a_substitute(histology):
    root = Path(__file__).resolve().parents[1]
    profile = json.loads((root / 'examples/patient_nsclc_pdl1_low_chemo_io.json').read_text())
    profile['patient_id'] = 'VIRTUAL-HISTOLOGY-REGRESSION'
    profile['findings']['histology'] = histology
    original = copy.deepcopy(profile)
    result = generate_plan(profile, kb_root=root / 'knowledge_base/hosted/content')
    assert profile == original
    if histology == 'adenocarcinoma':
        assert result.default_indication_id == 'IND-NSCLC-PDL1-LOW-NONSQ-MET-1L'
        assert result.plan.tracks[0].regimen_data['id'] == 'REG-PEMBRO-CHEMO-NSCLC-NONSQ'
    else:
        assert result.default_indication_id is None
        assert result.plan.tracks == [] and result.plan.sequencing_tracks == []
        reason = 'profile_selection_withheld' if histology == 'squamous' else 'histology_selection_withheld'
        assert result.plan.knowledge_base_state[reason] is True
        message = 'profile fields' if histology == 'squamous' else 'Histology applicability'
        assert any(message in warning for warning in result.warnings)
        assert 'No medicine plan has been selected' in render_plan_html(result, target_lang='en')
        assert 'REG-PEMBRO-CHEMO-NSCLC-NONSQ' not in render_plan_html(result, target_lang='en', mode='patient')


def test_withheld_report_keeps_fired_emergency_signals():
    root = Path(__file__).resolve().parents[1]
    profile = json.loads((root / 'examples/patient_nsclc_pdl1_low_chemo_io.json').read_text())
    profile['patient_id'] = 'VIRTUAL-EMERGENCY'
    profile['findings']['histology'] = None
    result = generate_plan(profile, kb_root=root / 'knowledge_base/hosted/content')
    result.trace = [{'fired_red_flags': ['RF-TEST-EMERGENCY']}]
    result.kb_resolved = {'red_flags': {'RF-TEST-EMERGENCY': {'id': 'RF-TEST-EMERGENCY', 'severity': 'critical', 'definition': 'Urgent synthetic test signal.'}}}
    rendered = render_plan_html(result, target_lang='en', mode='patient')
    assert 'Urgent synthetic test signal' in rendered
