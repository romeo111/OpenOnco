"""End-to-end engine test for Multiple Myeloma 1L — second disease.

Validates that the schema + rule engine generalize beyond HCV-MZL
(etiologically_driven archetype) to MM (risk_stratified archetype).
Per REFERENCE_CASE_SPECIFICATION §7.1 milestone M6.

Two synthetic patients:

- examples/patient_mm_standard_risk.json — t(11;14) + hyperdiploidy, no
  high-risk markers → engine selects VRd (standard track) as default.
- examples/patient_mm_high_risk.json — t(4;14) + gain 1q → engine selects
  D-VRd (aggressive quadruplet) as default.

Both run through generate_plan + render_plan_html. Asserts cover the
algorithm decision, two-track architecture, regimen materialization,
contraindication / supportive-care wiring, sources, and FDA Criterion-4
metadata population from MM content.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from knowledge_base.engine import (
    generate_plan,
    orchestrate_mdt,
    render_plan_html,
)

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


# ── Disease + algorithm resolution ────────────────────────────────────────


def test_mm_disease_resolves_via_icd_o_3():
    p = _patient("patient_mm_standard_risk.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-MM"
    assert plan.algorithm_id == "ALGO-MM-1L"


def test_mm_two_tracks_present_for_both_patients():
    """ALGO-MM-1L outputs 4 indications (2x standard, 2x aggressive for
    transplant-eligible vs ineligible sub-tracks); verify at least the
    canonical standard+aggressive pair is present."""
    for name in ("patient_mm_standard_risk.json", "patient_mm_high_risk.json"):
        p = _patient(name)
        plan = generate_plan(p, kb_root=KB_ROOT)
        assert plan.plan is not None, f"{name}: no Plan object"
        assert len(plan.plan.tracks) >= 2, (
            f"{name}: expected ≥2 tracks, got {len(plan.plan.tracks)}"
        )
        track_ids = {t.track_id for t in plan.plan.tracks}
        assert {"standard", "aggressive"} <= track_ids, (
            f"{name}: missing standard/aggressive tracks; got {track_ids}"
        )


# ── Algorithm decision ────────────────────────────────────────────────────


def test_standard_risk_patient_defaults_to_vrd():
    """Standard-risk MM (t(11;14) + hyperdiploidy, no high-risk FISH)
    → VRd standard track default."""
    p = _patient("patient_mm_standard_risk.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-MM-1L-VRD"
    assert plan.alternative_indication_id == "IND-MM-1L-DVRD"


def test_high_risk_patient_defaults_to_dvrd():
    """High-risk MM (t(4;14) + gain 1q) fires RF-MM-HIGH-RISK-CYTOGENETICS
    → D-VRd aggressive track default."""
    p = _patient("patient_mm_high_risk.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-MM-1L-DVRD"
    assert plan.alternative_indication_id == "IND-MM-1L-VRD"


def test_high_risk_redflag_appears_in_trace():
    """The decision must be auditable: high-risk patient's trace records
    that RF-MM-HIGH-RISK-CYTOGENETICS fired."""
    p = _patient("patient_mm_high_risk.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    trace_str = json.dumps(plan.trace)
    assert "RF-MM-HIGH-RISK-CYTOGENETICS" in trace_str, (
        f"high-risk RedFlag not surfaced in trace: {plan.trace}"
    )


# ── Regimen + safety layer materialization ────────────────────────────────


def test_vrd_track_carries_full_regimen():
    p = _patient("patient_mm_standard_risk.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    standard = next(t for t in plan.plan.tracks if t.track_id == "standard")
    reg = standard.regimen_data
    assert reg["id"] == "REG-VRD"
    drug_ids = {c["drug_id"] for c in reg["components"]}
    assert drug_ids == {
        "DRUG-BORTEZOMIB",
        "DRUG-LENALIDOMIDE",
        "DRUG-DEXAMETHASONE",
    }


def test_dvrd_track_carries_quadruplet_regimen():
    p = _patient("patient_mm_high_risk.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    aggressive = next(t for t in plan.plan.tracks if t.track_id == "aggressive")
    reg = aggressive.regimen_data
    assert reg["id"] == "REG-DARA-VRD"
    drug_ids = {c["drug_id"] for c in reg["components"]}
    assert drug_ids == {
        "DRUG-DARATUMUMAB",
        "DRUG-BORTEZOMIB",
        "DRUG-LENALIDOMIDE",
        "DRUG-DEXAMETHASONE",
    }


def test_mm_supportive_care_wired_through_regimen():
    """Both regimens require HSV prophylaxis + VTE prophylaxis + bone
    protection; D-VRd additionally requires PJP prophylaxis."""
    p = _patient("patient_mm_standard_risk.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    standard = next(t for t in plan.plan.tracks if t.track_id == "standard")
    sup_ids = {s["id"] for s in standard.supportive_care_data}
    assert {"SUP-HSV-PROPHYLAXIS", "SUP-MM-VTE-PROPHYLAXIS",
            "SUP-MM-BONE-PROTECTION"} <= sup_ids

    p2 = _patient("patient_mm_high_risk.json")
    plan2 = generate_plan(p2, kb_root=KB_ROOT)
    aggressive = next(t for t in plan2.plan.tracks if t.track_id == "aggressive")
    sup_ids_agg = {s["id"] for s in aggressive.supportive_care_data}
    assert "SUP-PJP-PROPHYLAXIS" in sup_ids_agg, (
        "D-VRd track must include PJP prophylaxis (anti-CD38 immunosuppression)"
    )


def test_mm_hard_contraindications_surfaced():
    """Both VRd and D-VRd carry lenalidomide pregnancy + bortezomib
    severe-neuropathy contraindications. D-VRd additionally carries
    HBV-no-prophylaxis."""
    p = _patient("patient_mm_standard_risk.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    standard = next(t for t in plan.plan.tracks if t.track_id == "standard")
    ci_ids = {c["id"] for c in standard.contraindications_data}
    assert {"CI-LENALIDOMIDE-PREGNANCY",
            "CI-BORTEZOMIB-SEVERE-NEUROPATHY"} <= ci_ids

    aggressive = next(t for t in plan.plan.tracks if t.track_id == "aggressive")
    ci_ids_agg = {c["id"] for c in aggressive.contraindications_data}
    assert "CI-HBV-NO-PROPHYLAXIS" in ci_ids_agg, (
        "D-VRd must flag HBV-no-prophylaxis hard contraindication"
    )


def test_mm_monitoring_schedule_attached():
    p = _patient("patient_mm_standard_risk.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    standard = next(t for t in plan.plan.tracks if t.track_id == "standard")
    assert standard.monitoring_data is not None
    assert standard.monitoring_data["id"] == "MON-VRD-REGIMEN"
    phase_names = {ph["name"] for ph in standard.monitoring_data["phases"]}
    assert "baseline" in phase_names
    assert "maintenance" in phase_names


# ── Expected outcomes + sourcing ──────────────────────────────────────────


def test_mm_expected_outcomes_populated_with_sources():
    for name in ("patient_mm_standard_risk.json", "patient_mm_high_risk.json"):
        p = _patient(name)
        plan = generate_plan(p, kb_root=KB_ROOT)
        for t in plan.plan.tracks:
            ind = t.indication_data
            assert ind["expected_outcomes"], (
                f"{name}/{t.track_id}: missing expected_outcomes"
            )
            assert ind["sources"], (
                f"{name}/{t.track_id}: indication missing sources"
            )


def test_mm_fda_metadata_aggregates_sources():
    p = _patient("patient_mm_standard_risk.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    fda = plan.plan.fda_compliance
    assert fda.data_sources_summary, "FDA Criterion-4 sources empty for MM plan"
    # NCCN MM source must be cited
    assert any("SRC-NCCN-MM-2025" in s for s in fda.data_sources_summary)


# ── Render ────────────────────────────────────────────────────────────────


def test_mm_html_render_well_formed_for_both_patients():
    for name in ("patient_mm_standard_risk.json", "patient_mm_high_risk.json"):
        p = _patient(name)
        plan = generate_plan(p, kb_root=KB_ROOT)
        mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
        html = render_plan_html(plan, mdt=mdt)
        assert html.startswith("<!DOCTYPE html>")
        assert "</html>" in html
        # Both indications surface in HTML
        assert "IND-MM-1L-VRD" in html
        assert "IND-MM-1L-DVRD" in html
        # SRC-NCCN-MM-2025 cited in sources block
        assert "SRC-NCCN-MM-2025" in html


def test_mm_high_risk_html_marks_dvrd_as_default():
    p = _patient("patient_mm_high_risk.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None)
    # Rendering preserves track ordering — default first
    dvrd_pos = html.find("IND-MM-1L-DVRD")
    vrd_pos = html.find("IND-MM-1L-VRD")
    assert 0 < dvrd_pos < vrd_pos, (
        f"D-VRd should appear before VRd for high-risk patient (default first); "
        f"D-VRd@{dvrd_pos}, VRd@{vrd_pos}"
    )
