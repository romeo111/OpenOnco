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
