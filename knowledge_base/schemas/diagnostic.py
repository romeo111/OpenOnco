"""Diagnostic-mode schemas: DiagnosticWorkup (KB content entity) and
DiagnosticPlan (per-patient artifact, gitignored).

See specs/DIAGNOSTIC_MDT_SPEC.md for full design. Core invariants:

- DiagnosticPlan is NOT a treatment Plan. Mode is `diagnostic`. Tracks
  list does not exist; instead workup_steps describes the diagnostic
  workup required before any treatment discussion is appropriate.
- Hard rule (CHARTER §15.2 C7): treatment Plan generation blocked when
  histology absent. DiagnosticPlan is the only output OpenOnco emits
  for pre-biopsy patients.
- DiagnosticWorkup lives in `knowledge_base/hosted/content/workups/`
  (validator and loader register it). DiagnosticPlan instances live
  outside the public KB (per CHARTER §9.3 — patient data).
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field

from .base import Base


# ── DiagnosticWorkup (curated content) ───────────────────────────────────────


class WorkupApplicability(Base):
    """Match patient's suspicion against this workup. Match if ANY of
    lineage_hints, tissue_locations, or presentation_keywords intersect
    with patient.suspicion fields."""

    lineage_hints: list[str] = Field(default_factory=list)
    tissue_locations: list[str] = Field(default_factory=list)
    presentation_keywords: list[str] = Field(default_factory=list)


class BiopsyApproach(Base):
    preferred: str
    alternatives: list[str] = Field(default_factory=list)
    rationale: Optional[str] = None


class IHCPanel(Base):
    baseline: list[str] = Field(default_factory=list)
    if_b_cell: list[str] = Field(default_factory=list)
    if_t_cell: list[str] = Field(default_factory=list)
    if_aggressive: list[str] = Field(default_factory=list)
    if_solid: list[str] = Field(default_factory=list)


class WorkupMDTHints(Base):
    """Roles a clinical reviewer expects to need for this workup type.
    The MDT Orchestrator may use these as additional triggers, but its
    standalone D1-D6 rules also fire independently."""

    required: list[str] = Field(default_factory=list)
    recommended: list[str] = Field(default_factory=list)
    optional: list[str] = Field(default_factory=list)


class DiagnosticWorkup(Base):
    id: str
    applicable_to: WorkupApplicability

    required_tests: list[str] = Field(default_factory=list)
    biopsy_approach: Optional[BiopsyApproach] = None
    required_ihc_panel: Optional[IHCPanel] = None

    mandatory_questions_to_resolve: list[str] = Field(default_factory=list)

    expected_timeline_days: Optional[int] = None
    expected_workup_cost_uah_estimate: Optional[float] = None

    triggers_mdt_roles: Optional[WorkupMDTHints] = None

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    reviewers: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


# ── DiagnosticPlan (per-patient artifact) ────────────────────────────────────


class SuspicionSnapshot(Base):
    lineage_hint: Optional[str] = None
    tissue_locations: list[str] = Field(default_factory=list)
    icd_o_3_topography: list[str] = Field(default_factory=list)
    presentation: Optional[str] = None
    working_hypotheses: list[str] = Field(default_factory=list)


class WorkupStep(Base):
    step: int
    category: Literal["lab", "imaging", "histology", "consult", "other"]
    test_id: Optional[str] = None  # → Test entity; null for biopsy/consult steps
    description: Optional[str] = None
    rationale: Optional[str] = None
    biopsy_approach: Optional[BiopsyApproach] = None
    ihc_panel: Optional[IHCPanel] = None


class DiagnosticPlan(Base):
    id: str  # "DPLAN-PZ-DIAG-001-V1"
    patient_id: str
    mode: Literal["diagnostic"] = "diagnostic"
    version: int = 1
    generated_at: str

    supersedes: Optional[str] = None
    superseded_by: Optional[str] = None
    revision_trigger: Optional[str] = None

    patient_snapshot: dict
    suspicion_snapshot: SuspicionSnapshot

    matched_workup_id: Optional[str] = None
    workup_steps: list[WorkupStep] = Field(default_factory=list)
    mandatory_questions: list[str] = Field(default_factory=list)
    expected_timeline_days: Optional[int] = None

    # Compliance metadata mirrors the FDA Criterion-4 fields for treatment Plan
    # but with diagnostic-mode wording. Surfaced in the rendered brief.
    intended_use: str = (
        "Diagnostic-phase MDT support: structure the workup, identify the team, "
        "surface unresolved questions. Informational support; not a treatment plan."
    )
    hcp_user_specification: str = (
        "Licensed oncologist/hematologist/pathologist participating in initial "
        "tumor-board discussion of a patient with suspected malignancy."
    )
    population_scope: Optional[str] = None
    automation_bias_warning: str = (
        "DIAGNOSTIC PHASE — this output describes diagnostic workup only. "
        "Treatment plan generation is blocked until histology is confirmed "
        "(CHARTER §15.2 C7). Do not treat on suspicion."
    )

    trace: list[dict] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
