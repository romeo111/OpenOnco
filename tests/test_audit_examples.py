from __future__ import annotations

from scripts.audit_examples import audit_examples
from scripts.site_cases import CASES, QUARANTINED_CASE_IDS
import json
from dataclasses import replace
from types import SimpleNamespace
import pytest
from scripts import audit_examples as audit_module


def test_example_registry_has_structured_publication_metadata():
    assert QUARANTINED_CASE_IDS
    assert all(case.visibility in {"public", "internal"} for case in CASES)
    assert all(case.quality_tier for case in CASES)
    assert all(case.scenario_type for case in CASES)
    assert all(
        case.visibility == "internal" for case in CASES if case.case_id in QUARANTINED_CASE_IDS
    )


def test_public_example_audit_passes_and_all_bma_profiles_are_registered():
    report = audit_examples()
    assert report["summary"]["failed"] == 0
    assert report["summary"]["unregistered_bma_profiles"] == 0
    assert report["summary"]["by_quality_tier"]["molecular"] >= 100
    withheld = {record['case_id']: record for record in report['records']
                if record['status'] == 'withheld'}
    assert set(withheld) == {
        'burkitt-high-risk',
        'bma-bma-nrg1-fusion-nsclc',
        'bma-bma-ntrk-fusion-nsclc',
    }
    assert report['summary']['withheld'] == len(withheld)
    assert withheld['burkitt-high-risk']['withheld_reason'] == (
        'Required profile/protocol context not confirmed; no automatic substitute.'
    )
    for case_id in ['bma-bma-nrg1-fusion-nsclc', 'bma-bma-ntrk-fusion-nsclc']:
        assert withheld[case_id]['withheld_reason'] == (
            'Histology-specific treatment route not confirmed; no automatic substitute.'
        )
    assert report['summary']['passed'] + report['summary']['withheld'] == report['summary']['checked']


@pytest.mark.parametrize('scenario,flag,has_default,expected', [
    ('molecular', True, False, 'withheld'), ('molecular', False, False, 'fail'),
    ('molecular', True, True, 'fail'), ('treatment', True, False, 'fail'),
])
def test_only_explicitly_safe_incomplete_molecular_selection_is_withheld(monkeypatch, tmp_path, scenario, flag, has_default, expected):
    case = replace(next(case for case in CASES if case.scenario_type == 'molecular'),
                   file='synthetic.json', scenario_type=scenario)
    (tmp_path / case.file).write_text(json.dumps({'disease': {'id': 'DIS-TEST'}}))
    plan = SimpleNamespace(tracks=[], sequencing_tracks=[], knowledge_base_state={'histology_selection_withheld': flag})
    result = SimpleNamespace(plan=plan, default_indication_id='IND-TEST' if has_default else None,
                             warnings=['Histology applicability is not confirmed'])
    monkeypatch.setattr(audit_module, 'generate_plan', lambda *args, **kwargs: result)
    monkeypatch.setattr(audit_module, 'is_diagnostic_profile', lambda profile: False)
    record = audit_module._audit_case(case, examples_dir=tmp_path, kb_root=tmp_path)
    assert record['status'] == expected
