"""Tests for `_find_algorithm` disease-state disambiguation.

Regression for PR #150 KB-drift signal #2: when multiple algorithms exist
for the same disease + line_of_therapy but differ on
`applicable_to_disease_state`, the engine must pick the one matching the
patient's `disease_state`. Previously it returned whichever loaded first
(load-order coin flip), which caused 4 prostate cases (S5 chunk) to drop.
"""

from __future__ import annotations

from knowledge_base.engine.plan import _find_algorithm


def _algo_entity(algo_id: str, disease_id: str, line: int, state: str | None) -> dict:
    data: dict = {
        "id": algo_id,
        "applicable_to_disease": disease_id,
        "applicable_to_line_of_therapy": line,
    }
    if state is not None:
        data["applicable_to_disease_state"] = state
    return {"type": "algorithms", "data": data}


def _build_entities() -> dict:
    return {
        "ALGO-PROSTATE-MHSPC-1L": _algo_entity(
            "ALGO-PROSTATE-MHSPC-1L", "DIS-PROSTATE", 1, "mHSPC"
        ),
        "ALGO-PROSTATE-MCRPC-1L": _algo_entity(
            "ALGO-PROSTATE-MCRPC-1L", "DIS-PROSTATE", 1, "mCRPC"
        ),
    }


def test_state_matched_algorithm_wins_mcrpc():
    entities = _build_entities()
    algo = _find_algorithm("DIS-PROSTATE", 1, entities, disease_state="mCRPC")
    assert algo is not None
    assert algo["id"] == "ALGO-PROSTATE-MCRPC-1L"


def test_state_matched_algorithm_wins_mhspc():
    entities = _build_entities()
    algo = _find_algorithm("DIS-PROSTATE", 1, entities, disease_state="mHSPC")
    assert algo is not None
    assert algo["id"] == "ALGO-PROSTATE-MHSPC-1L"


def test_disease_state_match_is_case_insensitive():
    entities = _build_entities()
    algo = _find_algorithm("DIS-PROSTATE", 1, entities, disease_state="mcrpc")
    assert algo is not None
    assert algo["id"] == "ALGO-PROSTATE-MCRPC-1L"


def test_no_disease_state_falls_back_to_state_agnostic():
    """Patient with no disease_state and a state-agnostic algorithm available
    should match the state-agnostic algorithm."""
    entities = {
        "ALGO-PROSTATE-MCRPC-1L": _algo_entity(
            "ALGO-PROSTATE-MCRPC-1L", "DIS-PROSTATE", 1, "mCRPC"
        ),
        "ALGO-PROSTATE-GENERIC-1L": _algo_entity(
            "ALGO-PROSTATE-GENERIC-1L", "DIS-PROSTATE", 1, None
        ),
    }
    algo = _find_algorithm("DIS-PROSTATE", 1, entities, disease_state=None)
    assert algo is not None
    assert algo["id"] == "ALGO-PROSTATE-GENERIC-1L"


def test_state_agnostic_when_no_state_match_available():
    """Patient has disease_state but only a state-agnostic algorithm exists
    → use the state-agnostic one (don't return None)."""
    entities = {
        "ALGO-NSCLC-1L": _algo_entity("ALGO-NSCLC-1L", "DIS-NSCLC", 1, None),
    }
    algo = _find_algorithm("DIS-NSCLC", 1, entities, disease_state="any-state")
    assert algo is not None
    assert algo["id"] == "ALGO-NSCLC-1L"


def test_state_mismatch_returns_none_when_only_mismatched_available():
    """Patient is mCRPC, only mHSPC algorithm exists → no match (don't
    silently return mHSPC just because it's the only candidate)."""
    entities = {
        "ALGO-PROSTATE-MHSPC-1L": _algo_entity(
            "ALGO-PROSTATE-MHSPC-1L", "DIS-PROSTATE", 1, "mHSPC"
        ),
    }
    algo = _find_algorithm("DIS-PROSTATE", 1, entities, disease_state="mCRPC")
    assert algo is None


def test_no_state_falls_back_to_load_order_for_legacy_patients():
    """Legacy patient profile (no disease_state) + only state-specific
    algorithms → fall back to load-order pick rather than returning None.
    This preserves backward compat for example files predating disease_state.
    The caller emits a warning so the gap is visible."""
    entities = _build_entities()
    algo = _find_algorithm("DIS-PROSTATE", 1, entities)
    assert algo is not None
    assert algo["id"] in {"ALGO-PROSTATE-MHSPC-1L", "ALGO-PROSTATE-MCRPC-1L"}


def test_disease_id_mismatch_returns_none():
    entities = _build_entities()
    assert _find_algorithm("DIS-NSCLC", 1, entities, disease_state="mCRPC") is None


def test_line_mismatch_returns_none():
    entities = _build_entities()
    assert _find_algorithm("DIS-PROSTATE", 2, entities, disease_state="mCRPC") is None


# ── End-to-end via generate_plan: breast 2L subtype routing ─────────────


def test_breast_2l_subtype_routing_via_disease_state():
    """Three breast 2L algorithms (HER2-POS, HR-POS, TNBC) collide on
    disease + line. With disease_state populated on both algorithms and
    patients, each subtype routes to its correct algorithm.

    Regression for PR #150 KB-drift signal #3 (S2 BREAST chunk):
    load-order silently picked HER2-POS-2L for TNBC and HR-POS patients.
    """
    import json
    from pathlib import Path
    from knowledge_base.engine import generate_plan

    repo_root = Path(__file__).parent.parent
    kb_root = repo_root / "knowledge_base" / "hosted" / "content"
    cases = {
        "patient_breast_her2_pos_met_2l_tdxd.json": "ALGO-BREAST-HER2-POS-2L",
        "patient_breast_tnbc_met_sacituzumab_2l.json": "ALGO-BREAST-TNBC-2L",
        "patient_breast_hr_pos_post_cdk46i_pik3ca_alpelisib.json": "ALGO-BREAST-HR-POS-2L",
    }
    for fname, expected_algo in cases.items():
        path = repo_root / "examples" / fname
        with path.open(encoding="utf-8") as fh:
            patient = json.load(fh)
        result = generate_plan(patient, kb_root=kb_root)
        assert result.algorithm_id == expected_algo, (
            f"{fname}: expected {expected_algo}, got {result.algorithm_id}; "
            f"disease_state={patient.get('disease_state')}"
        )
