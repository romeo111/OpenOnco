"""End-to-end acceptance test for the HCV-MZL reference case.

Per specs/REFERENCE_CASE_SPECIFICATION.md §1.3, this test is the **P0
acceptance criterion** for the engine. It runs the full pipeline:

    examples/patient_zero_reference_case.json
        → generate_plan(...)        # treatment Plan with two tracks
        → orchestrate_mdt(...)       # MDT brief
        → render_plan_html(...)      # rendered HTML

and asserts the §1.3 critical structural criteria. Gaps where the engine
or render layer doesn't yet meet a criterion are encoded as `pytest.xfail`
markers — they're logged so the project knows what's missing without
silently passing, and they flip green automatically once implemented.

The criteria are split into three blocks:

1. ENGINE/PLAN structure (PlanResult fields)
2. RENDER HTML (visible content + structural classes)
3. MDT brief (orchestrator output)

Plus a final block for §1.3 "should-have" items.
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

REFERENCE_PATIENT_FILE = EXAMPLES / "patient_zero_reference_case.json"


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def reference_patient() -> dict:
    return json.loads(REFERENCE_PATIENT_FILE.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def plan_result(reference_patient: dict):
    return generate_plan(reference_patient, kb_root=KB_ROOT)


@pytest.fixture(scope="module")
def mdt_result(reference_patient: dict, plan_result):
    return orchestrate_mdt(reference_patient, plan_result, kb_root=KB_ROOT)


@pytest.fixture(scope="module")
def html(plan_result, mdt_result) -> str:
    return render_plan_html(plan_result, mdt=mdt_result)


# ── §1.3 critical: ENGINE / PLAN structure ────────────────────────────────


def test_disease_resolves_to_hcv_mzl(plan_result):
    """Reference case input → engine resolves DIS-HCV-MZL via ICD-O-3 9699/3."""
    assert plan_result.disease_id == "DIS-HCV-MZL"


def test_two_plan_tracks_present(plan_result):
    """§1.3 critical: Два варіанти плану (стандартний + агресивний)."""
    plan = plan_result.plan
    assert plan is not None
    assert len(plan.tracks) >= 2
    track_ids = {t.track_id for t in plan.tracks}
    assert "standard" in track_ids
    assert "aggressive" in track_ids


def test_default_track_for_indolent_is_antiviral(plan_result):
    """Indolent presentation + HCV+ + non-bulky → STANDARD (antiviral) wins."""
    assert plan_result.default_indication_id == "IND-HCV-MZL-1L-ANTIVIRAL"
    assert plan_result.alternative_indication_id == "IND-HCV-MZL-1L-BR-AGGRESSIVE"


def test_each_track_has_regimen_and_indication(plan_result):
    """§1.3 critical: Regimen details (drug, dose, schedule, particularities) для both plans."""
    for t in plan_result.plan.tracks:
        assert t.indication_id, f"track {t.track_id} missing indication_id"
        assert t.indication_data, f"track {t.track_id} missing indication_data"
        assert t.regimen_data, f"track {t.track_id} missing regimen_data"
        # Regimen should at minimum carry name + drugs
        assert t.regimen_data.get("name"), f"track {t.track_id} regimen missing name"


def test_algorithm_decision_documented(plan_result):
    """§1.3 critical: Decision algorithm (step 1 → step 2)."""
    assert plan_result.algorithm_id == "ALGO-HCV-MZL-1L"
    assert plan_result.trace, "algorithm trace must be populated for auditability"
    # Trace must show the algorithm walked at least one step
    step_numbers = [
        e.get("step") for e in plan_result.trace if isinstance(e, dict) and "step" in e
    ]
    assert step_numbers, f"no step entries in trace: {plan_result.trace}"


def test_hard_contraindications_surfaced_on_aggressive(plan_result):
    """§1.3 critical: Hard contraindications highlighted (BR-aggressive carries CIs)."""
    aggressive = next(
        t for t in plan_result.plan.tracks if t.track_id == "aggressive"
    )
    assert aggressive.contraindications_data, (
        "aggressive track must expose hard_contraindications "
        "(CI-HBV-NO-PROPHYLAXIS, CI-SEVERE-CYTOPENIA-BR per indication)"
    )


def test_supportive_care_present_on_aggressive(plan_result):
    """§1.3 critical: Supportive care (per regimen) — aggressive BR regimen
    carries PJP / antiemetic / TLS / G-CSF / HBV prophylaxis."""
    aggressive = next(
        t for t in plan_result.plan.tracks if t.track_id == "aggressive"
    )
    assert aggressive.supportive_care_data, (
        "aggressive track must expose mandatory_supportive_care from regimen"
    )


def test_monitoring_schedule_present_on_aggressive(plan_result):
    """§1.3 critical: Monitoring schedule with phases (regimen-bound)."""
    aggressive = next(
        t for t in plan_result.plan.tracks if t.track_id == "aggressive"
    )
    assert aggressive.monitoring_data, (
        "aggressive track must expose monitoring_schedule (MON-BR-REGIMEN)"
    )


def test_expected_outcomes_with_source_refs(plan_result):
    """§1.3 critical: Expected outcomes with source-referenced numbers."""
    for t in plan_result.plan.tracks:
        ind = t.indication_data
        assert ind.get("expected_outcomes"), (
            f"track {t.track_id} indication missing expected_outcomes block"
        )
        # Must have at least one numeric/percentage signal in expected outcomes
        outcomes_str = json.dumps(ind["expected_outcomes"])
        assert "%" in outcomes_str or "year" in outcomes_str.lower() or ">" in outcomes_str
        # And the indication itself must cite at least one source
        assert ind.get("sources"), (
            f"track {t.track_id} indication missing sources — violates CCS §5.2"
        )


def test_all_recommendations_sourced_via_fda_metadata(plan_result):
    """§1.3 critical: All recommendations sourced (per CCS §5.2). Verified
    via FDA Criterion-4 data_sources_summary aggregation."""
    fda = plan_result.plan.fda_compliance
    assert fda.data_sources_summary, "FDA Criterion-4 data_sources_summary empty"
    assert len(fda.data_sources_summary) >= 2


def test_kb_version_stamp_and_timestamp(plan_result):
    """§1.3 critical: Knowledge base version stamp + generation timestamp."""
    plan = plan_result.plan
    assert plan.generated_at, "plan missing generated_at timestamp"
    # ISO-8601 with date prefix
    assert plan.generated_at[:4].isdigit()
    assert plan.knowledge_base_state, "plan missing knowledge_base_state"
    assert plan.knowledge_base_state.get("loaded_entities"), (
        "knowledge_base_state must record loaded entity count for audit"
    )


# ── §1.3 critical: RENDER HTML ────────────────────────────────────────────


def test_html_well_formed_and_self_contained(html):
    assert html.startswith("<!DOCTYPE html>")
    assert "</html>" in html
    assert "<style>" in html  # CSS embedded


def test_html_renders_two_tracks_with_default_marker(html, plan_result):
    """§1.3 critical: both tracks visible side-by-side; default badged."""
    assert plan_result.default_indication_id in html
    assert plan_result.alternative_indication_id in html
    assert "DEFAULT" in html or "★" in html
    # Side-by-side grid class is present
    assert 'class="tracks"' in html


def test_html_includes_disclaimer(html):
    """§1.3 critical: Явний disclaimer з CCS §11 formulating."""
    assert "medical-disclaimer" in html
    assert "тумор-борд" in html or "tumor-board" in html.lower()


def test_html_includes_fda_disclosure(html):
    """§1.3 critical: FDA non-device CDS positioning surfaced."""
    assert "fda-disclosure" in html
    assert "CHARTER §15" in html


def test_html_includes_version_chain(html, plan_result):
    """§1.3 critical: KB version stamp + timestamp visible to reader."""
    assert "version-chain" in html
    assert plan_result.plan.id in html
    # Date YYYY-MM appears (timestamp slice)
    import re
    assert re.search(r"\d{4}-\d{2}-\d{2}", html)


def test_html_lists_sources_cited(html):
    """§1.3 critical: All recommendations sourced — sources block visible."""
    assert "Sources cited" in html or "sources" in html.lower()
    # At least one known source ID from HCV-MZL KB must appear
    known_sources = [
        "SRC-ESMO-MZL-2024",
        "SRC-NCCN-BCELL-2025",
        "SRC-MOZ-UA-LYMPH-2024",
        "SRC-EASL-HCV-2023",
    ]
    assert any(s in html for s in known_sources), (
        "no known HCV-MZL source IDs surfaced in rendered HTML"
    )


def test_html_does_not_leak_real_patient_initials(html):
    """Defensive: synthetic ID only, no real-patient initials anywhere."""
    forbidden = ["В.Д.В.", "V.D.V.", "В. Д. В.", "V. D. V."]
    for token in forbidden:
        assert token not in html, f"leaked patient identifier: {token}"


# ── §1.3 critical: MDT brief ──────────────────────────────────────────────


def test_mdt_includes_required_roles(mdt_result):
    """MDT brief must surface at least the core required roles for HCV-MZL
    (hematologist + hepatologist + radiologist for an HCV-driven extranodal
    lymphoma at root of tongue)."""
    assert mdt_result.required_roles, "MDT produced no required roles"
    role_ids = {r.role_id for r in mdt_result.required_roles}
    # Hematologist always required for any lymphoma plan
    assert any("hemat" in rid.lower() for rid in role_ids), (
        f"hematologist role missing from required_roles: {role_ids}"
    )


def test_mdt_provenance_is_populated(mdt_result):
    """Append-only event log present for auditability of MDT formation."""
    assert mdt_result.provenance is not None
    assert mdt_result.provenance.events, "provenance graph has no events"


# ── §1.3 critical: render-layer sections (formerly xfailed gaps) ──────────


def test_html_etiological_driver_section_for_etiologically_driven_archetype(html):
    """§1.3 critical: Etiological driver section (for etiologically_driven archetype)."""
    assert "Етіологічний драйвер" in html or "Etiological driver" in html


def test_html_pre_treatment_investigations_with_priority(html):
    """§1.3 critical: Pre-treatment investigations з priority class."""
    assert "Pre-treatment" in html or "Дослідження перед" in html
    assert any(
        marker in html for marker in ["TEST-CBC", "TEST-LFT", "TEST-FIB4"]
    )


def test_html_red_flags_categorized_pro_contra(html):
    """§1.3 critical: Red flags: both PRO aggressive + CONTRA aggressive."""
    has_pro = "PRO-AGGRESSIVE" in html or "за агресивний" in html.lower()
    has_contra = "CONTRA-AGGRESSIVE" in html or "проти агресивн" in html.lower()
    assert has_pro and has_contra


def test_html_what_not_to_do_section(html):
    """§1.3 critical: 'What NOT to do' section."""
    assert (
        "What NOT to do" in html
        or "Що НЕ робити" in html
        or "Чого не робити" in html
    )


def test_html_monitoring_schedule_phases_visible(html):
    """§1.3 critical: Monitoring schedule with phases visible to reader."""
    assert "Monitoring" in html or "Моніторинг" in html
    assert "MON-BR-REGIMEN" in html or "phase" in html.lower()


# ── §1.3 should-have ──────────────────────────────────────────────────────


def test_ukrainian_localization_present(html):
    """Should-have: Ukrainian localization (primary output language)."""
    assert 'lang="uk"' in html
    # Some Ukrainian content visible
    ukrainian_markers = [
        "План лікування",
        "Стандартний",
        "Альтернативний",
        "тумор-борд",
        "Перегляд",
    ]
    assert any(m in html for m in ukrainian_markers), (
        "no Ukrainian content in rendered HTML"
    )


def test_side_by_side_comparison_layout(html):
    """Should-have: Side-by-side comparison of plans (CSS grid 2-column)."""
    assert 'class="tracks"' in html
    # Grid layout class with 2 columns
    assert "grid-template-columns: 1fr 1fr" in html


def test_html_timeline_visualization(html):
    """Should-have: Timeline visualization (rendered as a visible section,
    not merely the word 'timeline' appearing in CSS comments)."""
    # Must be inside an <h2>...</h2> heading to count as a real section
    import re
    headings = re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.IGNORECASE | re.DOTALL)
    heading_text = " | ".join(headings)
    assert (
        "Timeline" in heading_text
        or "Хронологія" in heading_text
        or "Хронология" in heading_text
    )
