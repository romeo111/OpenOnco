from __future__ import annotations

import textwrap
from pathlib import Path

from scripts.audit_validator import collect_validator_state


def _write(root: Path, rel: str, content: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def test_audit_validator_reports_contract_errors(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "diseases/dis_test.yaml",
        """
        id: DIS-TEST
        names: {preferred: Test disease}
        codes: {}
        """,
    )
    _write(
        tmp_path,
        "indications/ind_test.yaml",
        """
        id: IND-TEST-ACTIVE
        plan_track: standard
        applicable_to:
          disease_id: DIS-TEST
          line_of_therapy: 1
        recommended_regimen: null
        """,
    )
    _write(
        tmp_path,
        "algorithms/algo_test.yaml",
        """
        id: ALGO-TEST
        applicable_to_disease: DIS-TEST
        applicable_to_line_of_therapy: 1
        output_indications: [IND-TEST-ACTIVE]
        default_indication: IND-TEST-ACTIVE
        """,
    )

    state = collect_validator_state(tmp_path)

    assert state["schema_errors_count"] == 0
    assert state["ref_errors_count"] == 0
    assert state["contract_errors_count"] == 1
    assert state["errors"][0]["type"] == "contract"
    assert "routes to IND-TEST-ACTIVE" in state["errors"][0]["message"]


def test_audit_validator_strict_mode_promotes_narrative_source_gap(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "drugs/drug_test.yaml",
        """
        id: DRUG-TEST
        names: {preferred: Test drug}
        notes: "Legacy prose mentions SRC-MISSING."
        """,
    )

    state = collect_validator_state(tmp_path, strict_source_refs=True)

    assert state["ref_errors_count"] == 1
    assert "SRC-MISSING" in state["errors"][0]["message"]


def test_clinical_claim_sources_are_structural_references(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "diseases/dis_test.yaml",
        """
        id: DIS-TEST
        names: {preferred: Test disease}
        codes: {}
        """,
    )
    _write(
        tmp_path,
        "indications/ind_test.yaml",
        """
        id: IND-TEST
        applicable_to: {disease_id: DIS-TEST, line_of_therapy: 1}
        clinical_claims:
          - claim_id: IND-TEST-ONE
            text: A test clinical statement.
            source_ids: [SRC-MISSING]
        """,
    )

    state = collect_validator_state(tmp_path)

    assert state["schema_errors_count"] == 0
    assert state["ref_errors_count"] == 1
    assert "clinical_claims[0].source_ids[0]" in state["errors"][0]["message"]


def test_duplicate_clinical_claim_id_is_a_contract_error(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "diseases/dis_test.yaml",
        """
        id: DIS-TEST
        names: {preferred: Test disease}
        codes: {}
        """,
    )
    _write(
        tmp_path,
        "sources/src_test.yaml",
        """
        id: SRC-TEST
        source_type: guideline
        title: Test guideline
        """,
    )
    _write(
        tmp_path,
        "indications/ind_test.yaml",
        """
        id: IND-TEST
        applicable_to: {disease_id: DIS-TEST, line_of_therapy: 1}
        clinical_claims:
          - claim_id: IND-TEST-ONE
            text: First test clinical statement.
            source_ids: [SRC-TEST]
          - claim_id: IND-TEST-ONE
            text: Second test clinical statement.
            source_ids: [SRC-TEST]
        """,
    )

    state = collect_validator_state(tmp_path)

    assert state["schema_errors_count"] == 0
    assert state["ref_errors_count"] == 0
    assert state["contract_errors_count"] == 1
    assert "duplicates" in state["errors"][0]["message"]
