import math
from pathlib import Path

import pytest

from knowledge_base.engine import generate_diagnostic_brief, generate_plan, is_diagnostic_profile
from knowledge_base.engine.profile_input import validate_json_object, validate_patient_profile
from serverless.clinical_question import _safe_json_object, handle_json_request


@pytest.mark.parametrize('profile', [None, [], [1], 1, False, 'profile'])
def test_rejects_non_object_before_kb_io(profile, tmp_path):
    for generate in (generate_plan, generate_diagnostic_brief):
        with pytest.raises(ValueError, match='object'):
            generate(profile, kb_root=tmp_path / 'nonexistent-kb')


@pytest.mark.parametrize('number', [math.nan, math.inf, -math.inf])
def test_nested_nonfinite_stops_routing_and_generation(number, tmp_path):
    profile = {'disease': {'suspicion': {}}, 'findings': {'nested': [0, {'value': number}]}}
    for generate in (generate_plan, generate_diagnostic_brief):
        with pytest.raises(ValueError, match='non-finite'):
            generate(profile, kb_root=tmp_path / 'nonexistent-kb')
    with pytest.raises(ValueError, match='non-finite'):
        is_diagnostic_profile(profile)


@pytest.mark.parametrize('section', ['disease', 'demographics', 'findings', 'biomarkers', 'clinician_confirmations'])
def test_nonobject_sections_rejected(section):
    for wrong in ([], 0, False, 'unknown'):
        with pytest.raises(ValueError, match=section):
            validate_patient_profile({section: wrong})


def test_preserves_unknown_zero_false_and_shared_structure():
    shared = {'value': 0.836, 'negative': False}
    profile = {'findings': shared, 'metadata': [shared, None], 'demographics': None, 'patient_id': 'VIRTUAL-BOUNDARY-001'}
    before = repr(profile)
    validate_patient_profile(profile)
    assert repr(profile) == before
    cyclic = {}; cyclic['self'] = cyclic
    with pytest.raises(ValueError, match='cyclic'):
        validate_json_object(cyclic)


@pytest.mark.parametrize('text', ['{"findings":{"value":NaN}}', '{"findings":{"value":Infinity}}', '{"findings":{"value":-Infinity}}', '{"findings":{"value":1e9999}}'])
def test_model_json_cannot_bypass_finite_boundary(text):
    with pytest.raises(ValueError, match='non-finite'):
        _safe_json_object(text)


def test_bad_request_rejected_before_quota_or_model(monkeypatch):
    import serverless.clinical_question as endpoint
    def forbidden(*args, **kwargs):
        raise AssertionError('Invalid payload reached quota/provider work')
    monkeypatch.setattr(endpoint, '_quota_principal', forbidden)
    status, _, response = handle_json_request({'case_text': 'VIRTUAL ONLY', 'extra': math.inf})
    assert status == 400 and response['status'] == 'error'


"""Candidate input contract only; no treatment-selection or safety approval."""
import copy
from dataclasses import FrozenInstanceError

import pytest

from scripts.medication_input_contract import parse_medication_input

DRUGS = {"DRUG-BLEOMYCIN", "DRUG-BRENTUXIMAB-VEDOTIN"}


@pytest.mark.parametrize("profile", [{}, {"concomitant_medications": None}])
def test_missing_input_is_unknown_not_empty_reconciliation(profile):
    value = parse_medication_input(profile, DRUGS)
    assert value.status == "unknown" and not value.reported_complete
    assert value.drug_ids == ()


@pytest.mark.parametrize("status,drugs", [("unknown", []), ("partial", []), ("partial", ["DRUG-BLEOMYCIN"]), ("complete", []), ("complete", ["DRUG-BLEOMYCIN"])])
def test_explicit_states_are_preserved_without_mutation(status, drugs):
    profile = {"concomitant_medications": {"status": status, "drug_ids": drugs}}
    before = copy.deepcopy(profile)
    value = parse_medication_input(profile, DRUGS)
    assert value.status == status and value.drug_ids == tuple(drugs)
    assert value.reported_complete == (status == "complete")
    assert profile == before
    drugs.append("DRUG-BRENTUXIMAB-VEDOTIN")
    assert value.drug_ids == tuple(before["concomitant_medications"]["drug_ids"])
    with pytest.raises(FrozenInstanceError):
        value.status = "complete"


@pytest.mark.parametrize("value", [True, False, [], "complete", {}, {"status": "complete"}, {"status": "complete", "drug_ids": [], "clinician_verified": True}, {"status": True, "drug_ids": []}, {"status": "COMPLETE", "drug_ids": []}, {"status": "complete", "drug_ids": None}, {"status": "complete", "drug_ids": ()}, {"status": "complete", "drug_ids": [True]}, {"status": "complete", "drug_ids": ["bleomycin"]}, {"status": "complete", "drug_ids": ["DRUG-UNKNOWN"]}, {"status": "complete", "drug_ids": ["DRUG-BLEOMYCIN "]}, {"status": "complete", "drug_ids": ["DRUG-BLEOMYCIN", "DRUG-BLEOMYCIN"]}, {"status": "unknown", "drug_ids": ["DRUG-BLEOMYCIN"]}])
def test_malformed_or_ambiguous_input_cannot_be_complete(value):
    with pytest.raises(ValueError):
        parse_medication_input({"concomitant_medications": value}, DRUGS)


@pytest.mark.parametrize("patch,path", [({"medications": []}, "medications"), ({"concomitant_drugs": None}, "concomitant_drugs"), ({"findings": {"concomitant_drugs": ["DRUG-BLEOMYCIN"]}}, "findings.concomitant_drugs"), ({"findings": {"bleomycin_concomitant": True}}, "findings.bleomycin_concomitant")])
def test_unsupported_fields_do_not_create_false_complete_state(patch, path):
    profile = {"concomitant_medications": {"status": "complete", "drug_ids": []}, **patch}
    value = parse_medication_input(profile, DRUGS)
    assert value.status == "complete" and not value.reported_complete
    assert path in value.unsupported_paths


def test_historical_exposure_is_not_active_medication():
    value = parse_medication_input({"prior_therapies": ["DRUG-BLEOMYCIN"]}, DRUGS)
    assert value.status == "unknown" and not value.drug_ids


@pytest.mark.parametrize("profile", [None, True, [], "profile"])
def test_non_object_profile_rejected(profile):
    with pytest.raises(ValueError):
        parse_medication_input(profile, DRUGS)
