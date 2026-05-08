from __future__ import annotations

import textwrap
from pathlib import Path

from knowledge_base.validation.loader import clear_load_cache, load_content


def _write(root: Path, rel: str, content: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def _seed_common(root: Path) -> None:
    _write(
        root,
        "diseases/dis_test.yaml",
        """
        id: DIS-TEST
        names: {preferred: Test disease}
        codes: {}
        """,
    )


def test_algorithm_blocks_active_track_without_regimen(tmp_path: Path) -> None:
    clear_load_cache()
    _seed_common(tmp_path)
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
        decision_tree:
          - step: 1
            evaluate: {}
            if_true: {result: IND-TEST-ACTIVE}
        """,
    )

    result = load_content(tmp_path)

    messages = [msg for _, msg in result.contract_errors]
    assert any("routes to IND-TEST-ACTIVE" in msg for msg in messages)
    assert not result.ok


def test_algorithm_allows_explicit_non_regimen_track(tmp_path: Path) -> None:
    clear_load_cache()
    _seed_common(tmp_path)
    _write(
        tmp_path,
        "indications/ind_test.yaml",
        """
        id: IND-TEST-SURVEILLANCE
        plan_track: surveillance
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
        output_indications: [IND-TEST-SURVEILLANCE]
        default_indication: IND-TEST-SURVEILLANCE
        """,
    )

    result = load_content(tmp_path)

    assert result.schema_errors == []
    assert result.ref_errors == []
    assert result.contract_errors == []
    assert result.ok


def test_algorithm_allows_active_track_with_regimen(tmp_path: Path) -> None:
    clear_load_cache()
    _seed_common(tmp_path)
    _write(
        tmp_path,
        "drugs/drug_test.yaml",
        """
        id: DRUG-TEST
        names: {preferred: Test drug}
        """,
    )
    _write(
        tmp_path,
        "regimens/reg_test.yaml",
        """
        id: REG-TEST
        name: Test regimen
        components:
          - drug_id: DRUG-TEST
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
        recommended_regimen: REG-TEST
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

    result = load_content(tmp_path)

    assert result.schema_errors == []
    assert result.ref_errors == []
    assert result.contract_errors == []
    assert result.ok


def test_algorithm_allows_active_track_with_authored_phases(tmp_path: Path) -> None:
    clear_load_cache()
    _seed_common(tmp_path)
    _write(
        tmp_path,
        "drugs/drug_test.yaml",
        """
        id: DRUG-TEST
        names: {preferred: Test drug}
        """,
    )
    _write(
        tmp_path,
        "regimens/reg_test.yaml",
        """
        id: REG-TEST
        name: Test regimen
        components:
          - drug_id: DRUG-TEST
        """,
    )
    _write(
        tmp_path,
        "indications/ind_test.yaml",
        """
        id: IND-TEST-PHASED
        plan_track: standard
        applicable_to:
          disease_id: DIS-TEST
          line_of_therapy: 1
        phases:
          - phase: induction
            type: chemotherapy
            regimen_id: REG-TEST
            cycles: 4
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
        output_indications: [IND-TEST-PHASED]
        default_indication: IND-TEST-PHASED
        """,
    )

    result = load_content(tmp_path)

    assert result.schema_errors == []
    assert result.ref_errors == []
    assert result.contract_errors == []
    assert result.ok
