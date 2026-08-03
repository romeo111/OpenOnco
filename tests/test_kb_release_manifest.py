from __future__ import annotations

import textwrap
from pathlib import Path

from knowledge_base.release_manifest import build_release_artifacts
from knowledge_base.validation.loader import clear_load_cache


def _write(root: Path, rel: str, content: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def _make_minimal_kb(root: Path) -> None:
    _write(root, "diseases/dis_test.yaml", """
        id: DIS-TEST
        names: {preferred: Test disease}
        codes: {icd_10: C00}
        schema_version: '1.0'
    """)
    _write(root, "drugs/drug_test.yaml", """
        id: DRUG-TEST
        names: {preferred: Test drug}
        drug_class: test
        schema_version: '1.0'
    """)
    _write(root, "sources/src_test.yaml", """
        id: SRC-TEST
        source_type: guideline
        title: Test guideline
        doi: 10.1000/test
        schema_version: '1.0'
    """)
    _write(root, "regimens/reg_test.yaml", """
        id: REG-TEST
        name: Test regimen
        components: [{drug_id: DRUG-TEST}]
        clinical_claims:
          - claim_id: REG-TEST-1
            text: A source-addressable test statement.
            source_ids: [SRC-TEST]
            scope: synthetic test only
        schema_version: '1.0'
    """)
    _write(root, "indications/ind_test.yaml", """
        id: IND-TEST
        applicable_to: {disease_id: DIS-TEST, line_of_therapy: 1}
        recommended_regimen: REG-TEST
        clinical_claims:
          - claim_id: IND-TEST-1
            text: A second source-addressable test statement.
            source_ids: [SRC-TEST]
        schema_version: '1.0'
    """)


def test_release_manifest_and_graph_are_deterministic(tmp_path: Path) -> None:
    kb_root = tmp_path / "content"
    _make_minimal_kb(kb_root)
    clear_load_cache()

    manifest, graph = build_release_artifacts(kb_root)
    clear_load_cache()
    repeated_manifest, repeated_graph = build_release_artifacts(kb_root)

    assert manifest == repeated_manifest
    assert graph == repeated_graph
    assert manifest["entity_count"] == 5
    assert manifest["validation"] == {
        "schema_errors": 0,
        "reference_errors": 0,
        "contract_errors": 0,
        "contract_warnings": 0,
        "strict_source_refs": False,
    }
    assert manifest["claim_grounding"]["claim_fields"] == 2
    assert manifest["claim_grounding"]["anchored_claim_fields"] == 2
    assert manifest["sources"]["with_doi"] == 1
    assert manifest["schema_extensions"] == {}
    assert any(
        edge["from"] == "IND-TEST"
        and edge["to"] == "SRC-TEST"
        and edge["relation"] == "cites"
        for edge in graph["edges"]
    )


def test_release_manifest_exposes_legacy_signoff_inventory(tmp_path: Path) -> None:
    kb_root = tmp_path / "content"
    _make_minimal_kb(kb_root)
    _write(kb_root, "algorithms/algo_test.yaml", """
        id: ALGO-TEST
        applicable_to_disease: DIS-TEST
        applicable_to_line_of_therapy: 1
        output_indications: [IND-TEST]
        default_indication: IND-TEST
        reviewer_signoffs: 2
    """)
    clear_load_cache()

    manifest, _graph = build_release_artifacts(kb_root)

    assert manifest["clinical_review"]["legacy_signoff_counters"] == 1
    assert manifest["schema_extensions"] == {}
