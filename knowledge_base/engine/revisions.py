"""Plan revisions — close the supersedes/superseded_by loop.

This module realises infographic step 5 ("Спостереження → повернення при
нових даних"): when new patient data arrives, generate a new Plan or
DiagnosticPlan version that explicitly supersedes the previous one.

Three legal transitions, one illegal:

| Previous            | Updated patient profile shape  | Transition                | Result                  |
|---------------------|-------------------------------|---------------------------|-------------------------|
| DiagnosticPlan vN   | suspicion-only (no .id)       | diagnostic → diagnostic   | DiagnosticPlan v(N+1)   |
| DiagnosticPlan vN   | confirmed disease.id          | diagnostic → treatment    | Plan v1 (first treatment) |
| Plan vN             | confirmed disease.id          | treatment  → treatment    | Plan v(N+1)             |
| Plan vN             | suspicion-only (no .id)       | ILLEGAL — refused         | ValueError              |

Hard rules:
- supersedes/superseded_by chain wired both directions.
- Previous result is NOT mutated; a deep copy is returned with
  superseded_by populated. Caller decides what to do with both.
- Per CHARTER §10.2 — old version retained indefinitely; this module
  only marks it as superseded.
- Per CHARTER §15.2 C7 — treatment Plan generation still requires
  confirmed histology, even on revision. Downgrades blocked.
"""

from __future__ import annotations

import copy
from typing import Optional, Union

from pathlib import Path

from .diagnostic import (
    DiagnosticPlanResult,
    generate_diagnostic_brief,
    is_diagnostic_profile,
    is_treatment_profile,
)
from .plan import PlanResult, generate_plan
from .provenance import make_event


PreviousResult = Union[PlanResult, DiagnosticPlanResult]
NewResult = Union[PlanResult, DiagnosticPlanResult]


def _previous_id_and_version(previous: PreviousResult) -> tuple[str, int]:
    """Extract (plan_id, version) from either previous result type."""
    if isinstance(previous, DiagnosticPlanResult):
        if previous.diagnostic_plan is None:
            raise ValueError(
                "Previous DiagnosticPlanResult has no diagnostic_plan attached "
                "(empty result). Cannot revise from an empty baseline."
            )
        return previous.diagnostic_plan.id, previous.diagnostic_plan.version
    # PlanResult
    if previous.plan is None:
        raise ValueError(
            "Previous PlanResult has no plan attached (empty result). "
            "Cannot revise from an empty baseline."
        )
    return previous.plan.id, previous.plan.version


def _set_superseded_by(previous: PreviousResult, new_id: str) -> PreviousResult:
    """Return a deep copy of `previous` with .plan.superseded_by set.
    Leaves the original input untouched (callers like CLI persist both)."""
    cloned = copy.deepcopy(previous)
    if isinstance(cloned, DiagnosticPlanResult) and cloned.diagnostic_plan is not None:
        cloned.diagnostic_plan = cloned.diagnostic_plan.model_copy(
            update={"superseded_by": new_id}
        )
    elif isinstance(cloned, PlanResult) and cloned.plan is not None:
        cloned.plan = cloned.plan.model_copy(update={"superseded_by": new_id})
    return cloned


def _add_revision_provenance(
    new_result: NewResult,
    previous_id: str,
    revision_trigger: str,
) -> None:
    """Append a `modified` provenance event to the new result so the
    transition is auditable. Mutates new_result.plan/diagnostic_plan in
    place — these are freshly-generated, not external state."""

    new_plan = (
        new_result.diagnostic_plan
        if isinstance(new_result, DiagnosticPlanResult)
        else new_result.plan
    )
    if new_plan is None:
        return  # nothing to log against

    # PlanResult exposes provenance via mdt orchestrator separately;
    # for revisions we emit one event into the new plan's `trace` so
    # the audit chain survives even before MDT brief is generated.
    event_summary = (
        f"Plan revised from {previous_id} (trigger: {revision_trigger}). "
        f"This is version {new_plan.version} of patient {new_plan.patient_id}."
    )

    event = make_event(
        event_id=f"EV-{new_plan.id}-revision-001",
        actor_role="engine",
        event_type="modified",
        target_type="plan_section",
        target_id=new_plan.id,
        summary=event_summary,
    )

    # Append to the new plan's trace as a structured dict so consumers
    # that read trace see the revision in the same stream as decision-tree
    # steps. The full provenance graph is built later by orchestrate_mdt().
    new_plan.trace.append(event.to_dict())


# ── Public entry point ────────────────────────────────────────────────────


def revise_plan(
    updated_patient: dict,
    previous: PreviousResult,
    revision_trigger: str,
    kb_root: Path | str = "knowledge_base/hosted/content",
    *,
    oncokb_enabled: bool = False,
    oncokb_client=None,
) -> tuple[PreviousResult, NewResult]:
    """Generate a new Plan / DiagnosticPlan version that supersedes the
    previous one, given an updated patient profile and a description of
    what triggered the revision.

    Returns (previous_with_superseded_by_set, new_result).

    Auto-detects the transition from the shape of `previous` and the
    shape of `updated_patient`. Raises ValueError on illegal downgrade
    (treatment → diagnostic) per CHARTER §15.2 C7.

    Per Q7 lock (safe-rollout v3 §2): when OncoKB integration is
    enabled, every revision re-queries OncoKB rather than reusing the
    previous version's cached layer. Data may have updated between
    versions; staleness defeats the integration's value.
    """
    if not revision_trigger or not str(revision_trigger).strip():
        raise ValueError(
            "revise_plan requires a non-empty revision_trigger (audit hook)."
        )

    prev_id, prev_version = _previous_id_and_version(previous)
    is_treat_now = is_treatment_profile(updated_patient)
    is_diag_now = is_diagnostic_profile(updated_patient)

    if isinstance(previous, PlanResult):
        # Treatment baseline — must remain treatment. No downgrade.
        if not is_treat_now:
            raise ValueError(
                "Illegal revision: previous is a treatment Plan but the updated "
                "patient profile lacks a confirmed diagnosis (disease.id / "
                "icd_o_3_morphology). Treatment-to-diagnostic downgrade is not "
                "allowed (CHARTER §15.2 C7). To re-open diagnostic workup, "
                "create a new DiagnosticPlan independently."
            )
        new_result = generate_plan(
            updated_patient,
            kb_root=kb_root,
            plan_version=prev_version + 1,
            supersedes=prev_id,
            revision_trigger=revision_trigger,
            oncokb_enabled=oncokb_enabled,
            oncokb_client=oncokb_client,
        )
    elif isinstance(previous, DiagnosticPlanResult):
        if is_treat_now:
            # diagnostic → treatment promotion. New treatment Plan v1.
            new_result = generate_plan(
                updated_patient,
                kb_root=kb_root,
                plan_version=1,
                supersedes=prev_id,
                revision_trigger=revision_trigger,
                oncokb_enabled=oncokb_enabled,  # Q7: re-query on revision
                oncokb_client=oncokb_client,
            )
        elif is_diag_now:
            # diagnostic → diagnostic (still no histology, but new data)
            new_result = generate_diagnostic_brief(
                updated_patient,
                kb_root=kb_root,
                plan_version=prev_version + 1,
                supersedes=prev_id,
                revision_trigger=revision_trigger,
            )
        else:
            raise ValueError(
                "Updated patient profile has neither suspicion nor confirmed "
                "diagnosis. revise_plan() needs a recognisable mode."
            )
    else:
        raise TypeError(
            f"revise_plan expected PlanResult or DiagnosticPlanResult, got {type(previous).__name__}"
        )

    new_id = (
        new_result.diagnostic_plan.id
        if isinstance(new_result, DiagnosticPlanResult)
        and new_result.diagnostic_plan
        else (new_result.plan.id if isinstance(new_result, PlanResult) and new_result.plan else None)
    )
    if new_id is None:
        # generate_* returned an empty result (e.g. no workup matched).
        # Don't pretend we revised — return the previous untouched + new empty.
        return previous, new_result

    revised_previous = _set_superseded_by(previous, new_id)
    _add_revision_provenance(new_result, prev_id, revision_trigger)

    return revised_previous, new_result


__all__ = ["revise_plan", "PreviousResult", "NewResult"]
