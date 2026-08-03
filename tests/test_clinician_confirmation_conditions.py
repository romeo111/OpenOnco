"""Executable clinician-confirmation gates for formerly prose-only rules."""

from __future__ import annotations

from pathlib import Path

import yaml

from knowledge_base.engine.plan import _flatten_findings
from knowledge_base.engine.redflag_eval import _eval_clause
from scripts.audit_algorithm_conditions import audit_algorithm_conditions
from scripts.build_site import _inject_clinician_confirmations
from scripts.migrate_prose_conditions import confirmation_id, migrate_prose_conditions


def test_clinician_confirmation_is_explicit_with_legacy_profile_compatibility():
    clause = {
        "clinician_confirmation": {
            "id": "CC-ALGO-TEST-1L-0123456789AB",
            "label": "ECOG PS 0-2",
            "legacy_condition": "ECOG PS 0-2",
        }
    }
    key = "clinician_confirmation.CC-ALGO-TEST-1L-0123456789AB"

    assert _eval_clause(clause, {}) is False
    assert _eval_clause(clause, {key: True}) is True
    assert _eval_clause(clause, {key: False}) is False
    # Old synthetic JSON profiles sometimes supplied the exact prose label.
    assert _eval_clause(clause, {"ECOG PS 0-2": True}) is True


def test_profile_confirmations_are_namespaced_when_flattened():
    findings = _flatten_findings(
        {
            "findings": {"stage": "IV"},
            "clinician_confirmations": {"CC-ALGO-TEST-1L-0123456789AB": True},
        }
    )
    assert findings["stage"] == "IV"
    assert findings["clinician_confirmation.CC-ALGO-TEST-1L-0123456789AB"] is True


def test_questionnaire_injection_makes_confirmation_visible_without_defaulting_it():
    question_id = "CC-ALGO-TEST-1L-0123456789AB"
    questionnaire = {"disease_id": "DIS-TEST", "line_of_therapy": 1, "groups": []}
    output = _inject_clinician_confirmations(
        questionnaire,
        {("DIS-TEST", 1): [{"id": question_id, "label": "Verified gate"}]},
    )

    group = output["groups"][-1]
    question = group["questions"][0]
    assert question["field"] == f"clinician_confirmations.{question_id}"
    assert question["type"] == "boolean"
    assert "default_value" not in question
    assert "never inferred" in question["helper"]


def test_mechanical_migration_and_audit_are_lossless_on_a_small_algorithm(tmp_path: Path):
    algorithm_dir = tmp_path / "algorithms"
    algorithm_dir.mkdir()
    path = algorithm_dir / "algo_test.yaml"
    path.write_text(
        """id: ALGO-TEST-1L
applicable_to_disease: DIS-TEST
applicable_to_line_of_therapy: 1
output_indications: [IND-TEST]
decision_tree:
  - step: 1
    evaluate:
      any_of:
        - condition: \"ECOG PS 0-2\"
        - condition: BIO-TEST
    if_true: {result: IND-TEST}
    if_false: {result: IND-TEST}
""",
        encoding="utf-8",
    )

    report = migrate_prose_conditions(algorithm_dir=algorithm_dir, write=True)
    assert report.clauses_migrated == 1
    assert report.legacy_prose_remaining == 0

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    confirmation = data["decision_tree"][0]["evaluate"]["any_of"][0]["clinician_confirmation"]
    assert confirmation["id"] == confirmation_id("ALGO-TEST-1L", "ECOG PS 0-2")
    assert confirmation["label"] == "ECOG PS 0-2"
    assert confirmation["legacy_condition"] == "ECOG PS 0-2"
    assert data["decision_tree"][0]["evaluate"]["any_of"][1] == {"condition": "BIO-TEST"}

    audit = audit_algorithm_conditions(algorithm_dir=algorithm_dir)
    assert audit["summary"]["legacy_prose_conditions"] == 0
    assert audit["summary"]["errors"] == 0


def test_full_catalog_has_no_legacy_prose_conditions():
    report = audit_algorithm_conditions()
    assert report["summary"]["legacy_prose_conditions"] == 0
    assert report["summary"]["clinician_confirmations"] == 654
    assert report["summary"]["errors"] == 0
