"""End-to-end tests for cutaneous T-cell lymphoma block (MF / Sézary).

Stage-driven (TNMB) algorithm with biomarker modifiers:
- Early-stage IA-IIA → skin-directed (no systemic regimen, NBUVB / topicals / TSEBT)
- Advanced IIB+ or B2 (Sézary) → systemic
  - Sézary blood-dominant or non-CD30 → mogamulizumab (MAVORIC, anti-CCR4 ADCC)
  - CD30+ skin/LCT-dominant → brentuximab vedotin monotherapy (ALCANZA)
"""

from __future__ import annotations

import json
from pathlib import Path

from knowledge_base.engine import generate_plan

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def test_mf_early_stage_routes_to_skin_directed():
    """MF stage IB without B2 / LCT / CD30 → skin-directed default
    (no recommended_regimen — NBUVB / topicals / TSEBT are procedural)."""
    plan = generate_plan(_patient("patient_mf_early_stage.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-MF-SEZARY"
    assert plan.algorithm_id == "ALGO-MF-SEZARY-1L"
    assert plan.default_indication_id == "IND-MF-EARLY-1L-SKIN-DIRECTED"


def test_mf_early_skin_directed_has_no_systemic_regimen():
    """Skin-directed track should resolve with regimen_data null/empty —
    procedural therapy, not a drug regimen. Engine must not crash on null."""
    plan = generate_plan(_patient("patient_mf_early_stage.json"), kb_root=KB_ROOT)
    local_therapy = next(t for t in plan.plan.tracks if t.track_id == "local_therapy")
    # No drug components for skin-directed
    assert local_therapy.regimen_data is None or not local_therapy.regimen_data.get("components")


def test_sezary_advanced_routes_to_mogamulizumab():
    """B2 Sézary, CD30-negative → mogamulizumab (best blood-compartment
    response per MAVORIC). Step 1 fires on RF-MF-SEZARY-LEUKEMIC,
    step 2 routes to MOGA (no CD30+, no LCT)."""
    plan = generate_plan(_patient("patient_sezary_advanced.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-MF-SEZARY"
    assert plan.default_indication_id == "IND-MF-ADVANCED-1L-MOGA"


def test_sezary_advanced_uses_mogamulizumab_drug():
    """Mogamulizumab regimen must contain the actual DRUG-MOGAMULIZUMAB."""
    plan = generate_plan(_patient("patient_sezary_advanced.json"), kb_root=KB_ROOT)
    standard = next(t for t in plan.plan.tracks if t.track_id == "standard")
    drug_ids = {c["drug_id"] for c in standard.regimen_data["components"]}
    assert "DRUG-MOGAMULIZUMAB" in drug_ids


def test_mf_advanced_cd30_lct_routes_to_bv_mono():
    """Advanced MF with CD30+ AND large-cell transformation → BV-mono
    per ALCANZA (CD30-targeted ADC for cutaneous-dominant disease)."""
    plan = generate_plan(_patient("patient_mf_advanced_cd30.json"), kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-MF-SEZARY"
    assert plan.default_indication_id == "IND-MF-ADVANCED-1L-BV"


def test_mf_advanced_bv_uses_brentuximab_monotherapy():
    """BV-MF regimen is monotherapy — only DRUG-BRENTUXIMAB-VEDOTIN,
    no chemo backbone (distinct from CHP-Bv combination)."""
    plan = generate_plan(_patient("patient_mf_advanced_cd30.json"), kb_root=KB_ROOT)
    track = next(t for t in plan.plan.tracks if t.regimen_data is not None)
    drug_ids = {c["drug_id"] for c in track.regimen_data["components"]}
    assert drug_ids == {"DRUG-BRENTUXIMAB-VEDOTIN"}, (
        f"BV-MF should be monotherapy; got {drug_ids}"
    )


def test_mf_workup_includes_sezary_count_and_tcr_clonality():
    """Every MF indication must require Sezary count + TCR clonality
    in baseline workup — these define TNMB B-stage and confirm clonality
    across compartments."""
    plan = generate_plan(_patient("patient_sezary_advanced.json"), kb_root=KB_ROOT)
    track = next(t for t in plan.plan.tracks if t.is_default)
    required = set(track.indication_data["required_tests"])
    assert "TEST-SEZARY-COUNT" in required, "MF baseline missing Sezary count"
    assert "TEST-TCR-CLONALITY" in required, "MF baseline missing TCR clonality"


def _fired_red_flags(plan_result) -> set[str]:
    """Walk the algorithm trace to collect every red flag fired across
    all evaluated steps. Mirrors mdt_orchestrator._collect_fired_red_flags."""
    fired: set[str] = set()
    for entry in plan_result.trace:
        for rf in entry.get("fired_red_flags") or []:
            fired.add(rf)
    return fired


def test_sezary_redflag_fires_on_b2():
    """Sezary B2 status must surface RF-MF-SEZARY-LEUKEMIC in fired flags
    so the MDT brief can flag the leukemic phase."""
    plan = generate_plan(_patient("patient_sezary_advanced.json"), kb_root=KB_ROOT)
    assert "RF-MF-SEZARY-LEUKEMIC" in _fired_red_flags(plan)


def test_lct_redflag_fires_on_large_cell_transformation():
    """Large-cell transformation must fire RF-MF-LARGE-CELL-TRANSFORMATION."""
    plan = generate_plan(_patient("patient_mf_advanced_cd30.json"), kb_root=KB_ROOT)
    assert "RF-MF-LARGE-CELL-TRANSFORMATION" in _fired_red_flags(plan)
