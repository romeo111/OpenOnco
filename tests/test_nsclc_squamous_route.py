import copy
import json
from pathlib import Path

import pytest
from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.engine.profile_applicability import unconfirmed_profile_fields

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def profile():
    return json.loads((ROOT / 'examples/patient_nsclc_squamous_paclitaxel.json').read_text())


@pytest.mark.parametrize('value', [None, False, 1, 'true', [], {}])
def test_authored_true_requires_explicit_boolean(value):
    ind = {'applicable_to': {'confirmed_profile_values': {'findings.driver_negative': [True]}}}
    assert unconfirmed_profile_fields(ind, {'findings': {'driver_negative': value}}) == ['findings.driver_negative']
    assert not unconfirmed_profile_fields(ind, {'findings': {'driver_negative': True}})


def test_conflicting_stage_and_numeric_functional_status():
    ind = {'applicable_to': {'confirmed_profile_values': {'findings.stage': ['IV'], 'demographics.ecog': [0, 1]}}}
    assert not unconfirmed_profile_fields(ind, {'findings': {'stage': 'IV'}, 'demographics': {'ecog': 1.0}})
    assert unconfirmed_profile_fields(ind, {'findings': {'stage': 'IV'}, 'disease': {'stage': 'III'}, 'demographics': {'ecog': 1}}) == ['disease.stage']
    assert unconfirmed_profile_fields(ind, {'findings': {'stage': 'IV', 'ecog': 2}, 'demographics': {'ecog': 1}}) == ['findings.ecog']


@pytest.mark.parametrize('value', ['true', 'false', 1, 0, [], {}, True])
def test_exclusions_do_not_treat_malformed_boolean_as_negative(value):
    ind = {'applicable_to': {'excluded_profile_values': {'findings.autoimmune_disease_active': [True]}}}
    assert unconfirmed_profile_fields(ind, {'findings': {'autoimmune_disease_active': value}}) == ['findings.autoimmune_disease_active']
    assert not unconfirmed_profile_fields(ind, {'findings': {'autoimmune_disease_active': False}})
    assert unconfirmed_profile_fields(ind, {'findings': {'autoimmune_disease_active': False}, 'disease': {'autoimmune_disease_active': True}}) == ['disease.autoimmune_disease_active']


@pytest.mark.parametrize('choice,drug,days', [('paclitaxel', 'DRUG-PACLITAXEL', 'Day 1'), ('nab-paclitaxel', 'DRUG-NAB-PACLITAXEL', 'Days 1, 8 and 15')])
def test_actual_squamous_route_has_one_taxane_and_no_pemetrexed(profile, choice, drug, days):
    profile['findings']['nsclc_taxane_choice'] = choice
    original = copy.deepcopy(profile)
    result = generate_plan(profile, kb_root=ROOT / 'knowledge_base/hosted/content')
    assert profile == original
    assert result.default_indication_id == 'IND-NSCLC-SQ-PEMBRO-CARBO-' + choice.upper() + '-1L'
    selected = next(track for track in result.plan.tracks if track.is_default)
    components = selected.regimen_data['components']
    assert [c['drug_id'] for c in components] == ['DRUG-PEMBROLIZUMAB', 'DRUG-CARBOPLATIN', drug]
    assert days in components[2]['schedule']
    assert components[1]['dose'] == 'AUC 6 mg/mL/min IV'
    assert not selected.indication_data.get('expected_outcomes')
    assert not selected.indication_data.get('reviewers')
    for track in result.plan.tracks:
        assert 'DRUG-PEMETREXED' not in [c['drug_id'] for c in (track.regimen_data or {}).get('components', [])]
    assert 'KEYNOTE-407' in render_plan_html(result, target_lang='en')


@pytest.mark.parametrize('section,key,value', [('findings','nsclc_taxane_choice',None), ('findings','nsclc_taxane_choice','both'), ('findings','stage','III'), ('findings','driver_negative',None), ('demographics','ecog',2), ('demographics','age',17), ('findings','autoimmune_disease_active',True), ('findings','systemic_immunosuppression',True), ('findings','noninfectious_pneumonitis_requiring_steroids',True), ('findings','symptomatic_cns_metastases',True)])
def test_unconfirmed_route_never_promotes_an_automatic_substitute(profile, section, key, value):
    profile[section][key] = value
    result = generate_plan(profile, kb_root=ROOT / 'knowledge_base/hosted/content')
    assert result.default_indication_id is None
    assert result.plan.tracks == result.plan.sequencing_tracks == []
    assert result.plan.knowledge_base_state['profile_selection_withheld'] is True
    assert section + '.' + key in result.plan.knowledge_base_state['unconfirmed_profile_fields']
    for mode in ('hcp', 'patient'):
        report = render_plan_html(result, target_lang='en', mode=mode)
        assert 'No medicine plan has been selected' in report
        assert '200 mg' not in report
