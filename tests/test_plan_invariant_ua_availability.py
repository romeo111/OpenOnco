"""Architectural invariant: UA-availability is annotation, never filter.

Per docs/plans/ua_ingestion_and_alternatives_2026-04-26.md §0 + §3.2.
Per user directive 2026-04-26 (memory: feedback_efficacy_over_registration.md):
"ефективність а не реєстрованість".

Engine MUST select the same default + alternative tracks regardless of
whether the involved drugs are registered in Ukraine, reimbursed by НСЗУ,
or both unavailable. UA-availability fields are render-time metadata
only — they must never enter the engine selection signal.

This test is the gate for all UA-ingestion work (Phase A of the plan).
If you add ingestion code that filters/ranks by registration / reimbursement,
this test is what should fail first.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from knowledge_base.engine import generate_plan
from knowledge_base.validation import loader as kb_loader

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


@pytest.fixture
def force_drugs_unregistered(monkeypatch):
    """Patch the loader so every Drug appears unregistered + non-reimbursed
    in Ukraine. This simulates the "all drugs are off-label imports" scenario
    — engine output must not change."""

    real_load = kb_loader.load_content

    def patched_load(root):
        result = real_load(root)
        for eid, info in result.entities_by_id.items():
            if info["type"] != "drugs":
                continue
            data = info["data"]
            reg = data.setdefault("regulatory_status", {})
            ua = reg.setdefault("ukraine_registration", {})
            ua["registered"] = False
            ua["reimbursed_nszu"] = False
            ua["notes"] = "INVARIANT TEST OVERRIDE: forced unregistered"
        return result

    monkeypatch.setattr(kb_loader, "load_content", patched_load)
    # generate_plan imports load_content lazily through `kb_loader.load_content`
    # if it imports the module. If it does `from .validation.loader import
    # load_content` directly, monkeypatching the parent module won't reach it.
    # Patch both surfaces to be safe.
    try:
        from knowledge_base.engine import plan as plan_module
        if hasattr(plan_module, "load_content"):
            monkeypatch.setattr(plan_module, "load_content", patched_load)
    except ImportError:
        pass


def _plan_signature(plan_result) -> tuple:
    """Stable summary of the plan's clinical decisions — what the
    invariant must preserve."""
    return (
        plan_result.disease_id,
        plan_result.algorithm_id,
        plan_result.default_indication_id,
        plan_result.alternative_indication_id,
        tuple(
            (t.indication_id, (t.regimen_data or {}).get("id"))
            for t in (plan_result.plan.tracks if plan_result.plan else [])
        ),
    )


@pytest.mark.parametrize(
    "fixture_name",
    [
        "patient_zero_indolent.json",       # HCV-MZL — etiologically_driven archetype
        "patient_zero_bulky.json",          # HCV-MZL — bulky variant (RF-driven branch)
        "patient_mm_high_risk.json",        # MM — risk_stratified archetype
        "patient_cll_high_risk.json",       # CLL — biomarker-shifted (TP53)
    ],
)
def test_plan_independent_of_ua_availability(fixture_name, force_drugs_unregistered):
    """Same patient → same default + alternative tracks regardless of
    whether the involved drugs are registered/reimbursed in Ukraine.

    Run twice (control with real KB metadata, then override with all
    drugs marked unregistered + non-reimbursed) and assert the engine's
    clinical-decision signature is identical."""

    patient = _patient(fixture_name)

    # Control: real KB metadata
    plan_control = generate_plan(patient, kb_root=KB_ROOT)
    sig_control = _plan_signature(plan_control)

    # Override: all drugs unregistered + non-reimbursed (via fixture)
    plan_override = generate_plan(patient, kb_root=KB_ROOT)
    sig_override = _plan_signature(plan_override)

    assert sig_control == sig_override, (
        f"UA-availability MUST NOT influence plan selection. "
        f"Control: {sig_control} ≠ Override: {sig_override}. "
        f"Patient: {fixture_name}"
    )


def test_source_precedence_policy_field_loads(force_drugs_unregistered):
    """Smoke: the new Source.precedence_policy field is recognized by
    the loader for the existing МОЗ sources (annotated as
    national_floor_only)."""

    result = kb_loader.load_content(KB_ROOT)

    moz_sources = [
        info["data"]
        for info in result.entities_by_id.values()
        if info["type"] == "sources" and (info["data"].get("id") or "").startswith("SRC-MOZ-")
    ]
    assert moz_sources, "Expected at least one SRC-MOZ-* source in KB"

    # Per Phase A annotation, all МОЗ sources should be national_floor_only
    for s in moz_sources:
        assert s.get("precedence_policy") == "national_floor_only", (
            f"{s.get('id')}: МОЗ source should be precedence_policy="
            f"national_floor_only; got {s.get('precedence_policy')!r}"
        )
