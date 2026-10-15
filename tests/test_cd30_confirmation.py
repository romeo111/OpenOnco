"""BV-CHP candidates require the canonical confirmed CD30 result.

This input contract is not histology-specific comparative efficacy approval.
"""
import copy
import json
from pathlib import Path

import pytest

from knowledge_base.engine import generate_plan, render_plan_html

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


def profile(case):
    rows = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    return copy.deepcopy(next(row['json'] for row in rows if row['case_id'] == case))


@pytest.mark.parametrize('case', ['ptcl-cd30-negative', 'aitl-cd30-negative'])
@pytest.mark.parametrize('value', ['negative', 'unknown', None, False, True, 10, '10%', {'status': 'positive'}])
def test_unconfirmed_cd30_cannot_open_bv_alternative(case, value):
    patient = profile(case)
    patient['biomarkers']['BIO-CD30-IHC'] = value
    before = copy.deepcopy(patient)
    result = generate_plan(patient, kb_root=KB)
    assert result.plan.tracks
    assert all(track.regimen_data['id'] != 'REG-CHP-BV' for track in result.plan.tracks)
    assert result.plan.tracks[0].regimen_data['id'] == 'REG-CHOEP'
    assert patient == before


@pytest.mark.parametrize('case', ['ptcl-cd30-positive', 'aitl-cd30-positive'])
@pytest.mark.parametrize('value', ['negative', None, False, True, 'unknown'])
def test_stale_positive_finding_cannot_unlock_selected_bv_or_substitute(case, value):
    patient = profile(case)
    patient['biomarkers']['BIO-CD30-IHC'] = value
    patient['findings']['cd30_positive'] = True
    patient['clinician_confirmations'] = {'specialist_confirmation': True}
    result = generate_plan(patient, kb_root=KB)
    assert not result.plan.tracks
    assert result.plan.knowledge_base_state['profile_selection_withheld']
    assert 'biomarkers.BIO-CD30-IHC' in result.plan.knowledge_base_state['unconfirmed_profile_fields']
    assert result.default_indication_id is None


@pytest.mark.parametrize('case', ['ptcl-cd30-positive', 'aitl-cd30-positive'])
def test_confirmed_positive_keeps_existing_route_without_claiming_eligibility(case):
    result = generate_plan(profile(case), kb_root=KB)
    assert result.plan.tracks[0].regimen_data['id'] == 'REG-CHP-BV'


@pytest.mark.parametrize('case', ['ptcl-cd30-negative', 'aitl-cd30-negative'])
@pytest.mark.parametrize('finding', [False, 'false', 0])
def test_positive_marker_cannot_override_conflicting_cd30_finding(case, finding):
    patient = profile(case)
    patient['biomarkers']['BIO-CD30-IHC'] = 'positive'
    patient['findings']['cd30_positive'] = finding
    result = generate_plan(patient, kb_root=KB)
    assert all(track.regimen_data['id'] != 'REG-CHP-BV' for track in result.plan.tracks)


@pytest.mark.parametrize('mode', ['patient', 'clinician'])
@pytest.mark.parametrize('locale', ['en', 'uk'])
def test_missing_selected_marker_notice_has_cd30_context_without_wrong_disease(mode, locale):
    patient = profile('aitl-cd30-positive')
    del patient['biomarkers']['BIO-CD30-IHC']
    result = generate_plan(patient, kb_root=KB)
    output = render_plan_html(result, target_lang=locale, mode=mode)
    assert 'CD30' in output
    assert 'Check metastatic stage' not in output
    assert 'перевірте метастатичну стадію' not in output
    assert 'DRUG-BRENTUXIMAB-VEDOTIN' not in output
    assert not result.plan.tracks and not result.plan.sequencing_tracks
