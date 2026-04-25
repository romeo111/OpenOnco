"""Tests for revise_plan() — closes the supersedes/superseded_by loop
(infographic step 5: "Спостереження → повернення при нових даних").

Covers:
- treatment → treatment revision (new lab data, same diagnosis)
- diagnostic → treatment promotion (histology confirmed)
- diagnostic → diagnostic revision (still no biopsy, more findings)
- ILLEGAL: treatment → diagnostic downgrade (CHARTER §15.2 C7)
- supersedes/superseded_by chain wired BOTH directions
- modified ProvenanceEvent attached to the new plan's trace
- empty revision_trigger refused (audit hook)
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from knowledge_base.engine import (
    DiagnosticPlanResult,
    PlanResult,
    generate_diagnostic_brief,
    generate_plan,
    revise_plan,
)

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


# ── 1. treatment → treatment ──────────────────────────────────────────────


def test_treatment_to_treatment_revision_chain():
    p_v1 = _patient("patient_zero_indolent.json")
    p_v2 = _patient("patient_zero_indolent_v2.json")
    prev = generate_plan(p_v1, kb_root=KB_ROOT)

    revised_prev, new = revise_plan(
        p_v2, prev, "new lab results 2026-05-10: HBV serology + FIB-4", kb_root=KB_ROOT,
    )

    # Both ends of the chain wired
    assert isinstance(new, PlanResult)
    assert new.plan is not None
    assert new.plan.version == prev.plan.version + 1
    assert new.plan.supersedes == prev.plan.id
    assert revised_prev.plan.superseded_by == new.plan.id
    # Original previous untouched (deep copy semantics)
    assert prev.plan.superseded_by is None


def test_treatment_revision_carries_revision_trigger():
    p_v1 = _patient("patient_zero_indolent.json")
    p_v2 = _patient("patient_zero_indolent_v2.json")
    prev = generate_plan(p_v1, kb_root=KB_ROOT)
    trigger = "new lab 2026-05-10: HBV negative + FIB-4 1.8 + CD20+ confirmed"

    _, new = revise_plan(p_v2, prev, trigger, kb_root=KB_ROOT)

    assert new.plan.revision_trigger == trigger
    # Modified provenance event attached to new plan trace
    revision_events = [
        t for t in new.plan.trace
        if isinstance(t, dict) and t.get("event_type") == "modified"
    ]
    assert revision_events, "new plan must record a 'modified' event"
    assert revision_events[0]["target_id"] == new.plan.id
    assert prev.plan.id in revision_events[0]["summary"]


# ── 2. diagnostic → treatment promotion ───────────────────────────────────


def test_diagnostic_promotes_to_treatment_when_histology_confirmed():
    susp = _patient("patient_diagnostic_lymphoma_suspect.json")
    confirmed = _patient("patient_diagnostic_lymphoma_confirmed.json")
    prev = generate_diagnostic_brief(susp, kb_root=KB_ROOT)

    assert prev.diagnostic_plan is not None  # baseline sanity

    revised_prev, new = revise_plan(
        confirmed, prev,
        "biopsy result 2026-05-10: HCV-MZL confirmed (CD20+, MALT pattern)",
        kb_root=KB_ROOT,
    )

    # Promoted to treatment Plan v1
    assert isinstance(new, PlanResult)
    assert new.plan is not None
    assert new.plan.version == 1
    assert new.plan.supersedes == prev.diagnostic_plan.id
    assert revised_prev.diagnostic_plan.superseded_by == new.plan.id
    # And the treatment plan is the actual disease.
    # Clinically: confirmed patient has splenic_mass_cm 12.0 → bulky →
    # RF-BULKY-DISEASE fires → engine correctly picks BR-AGGRESSIVE as
    # default. This is not a regression; it's the rule engine doing
    # exactly what it should.
    assert new.disease_id == "DIS-HCV-MZL"
    assert new.default_indication_id == "IND-HCV-MZL-1L-BR-AGGRESSIVE"
    assert new.alternative_indication_id == "IND-HCV-MZL-1L-ANTIVIRAL"


# ── 3. diagnostic → diagnostic ────────────────────────────────────────────


def test_diagnostic_to_diagnostic_revision():
    """New findings arrived but biopsy still pending."""
    susp_v1 = _patient("patient_diagnostic_lymphoma_suspect.json")
    # v2: same suspicion shape (no disease.id), but updated history
    susp_v2 = json.loads(json.dumps(susp_v1))  # deep copy
    susp_v2["history"]["hcv_known_positive"] = False
    susp_v2["history"]["hbv_known_positive"] = False
    susp_v2["findings"]["pet_ct_date"] = "2026-05-08"

    prev = generate_diagnostic_brief(susp_v1, kb_root=KB_ROOT)
    revised_prev, new = revise_plan(
        susp_v2, prev,
        "PET/CT done 2026-05-08; viral serology results pending",
        kb_root=KB_ROOT,
    )

    assert isinstance(new, DiagnosticPlanResult)
    assert new.diagnostic_plan is not None
    assert new.diagnostic_plan.version == prev.diagnostic_plan.version + 1
    assert new.diagnostic_plan.supersedes == prev.diagnostic_plan.id
    assert revised_prev.diagnostic_plan.superseded_by == new.diagnostic_plan.id


# ── 4. ILLEGAL — treatment → diagnostic ───────────────────────────────────


def test_treatment_to_diagnostic_downgrade_refused():
    """CHARTER §15.2 C7 — once treatment plan exists, you don't drop
    back to diagnostic by removing disease.id from a profile."""
    p_v1 = _patient("patient_zero_indolent.json")
    prev = generate_plan(p_v1, kb_root=KB_ROOT)

    # Build a synthetic 'downgraded' profile — strip the diagnosis
    p_downgrade = {
        "patient_id": p_v1["patient_id"],
        "disease": {
            "suspicion": {
                "lineage_hint": "b_cell_lymphoma",
                "tissue_locations": ["spleen"],
                "presentation": "user mistakenly removed diagnosis",
            }
        },
        "demographics": p_v1["demographics"],
    }

    with pytest.raises(ValueError, match="Illegal revision"):
        revise_plan(p_downgrade, prev, "should not be allowed", kb_root=KB_ROOT)


# ── 5. revise_plan invariants ─────────────────────────────────────────────


def test_empty_revision_trigger_refused():
    p_v1 = _patient("patient_zero_indolent.json")
    p_v2 = _patient("patient_zero_indolent_v2.json")
    prev = generate_plan(p_v1, kb_root=KB_ROOT)

    with pytest.raises(ValueError, match="non-empty revision_trigger"):
        revise_plan(p_v2, prev, "", kb_root=KB_ROOT)
    with pytest.raises(ValueError, match="non-empty revision_trigger"):
        revise_plan(p_v2, prev, "   ", kb_root=KB_ROOT)


def test_revise_does_not_mutate_previous_input():
    p_v1 = _patient("patient_zero_indolent.json")
    p_v2 = _patient("patient_zero_indolent_v2.json")
    prev = generate_plan(p_v1, kb_root=KB_ROOT)
    prev_id_before = prev.plan.id
    prev_superseded_before = prev.plan.superseded_by

    _, _ = revise_plan(p_v2, prev, "trigger", kb_root=KB_ROOT)

    # Original prev still pristine
    assert prev.plan.id == prev_id_before
    assert prev.plan.superseded_by == prev_superseded_before
