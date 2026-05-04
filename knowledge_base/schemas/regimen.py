"""Regimen entity — KNOWLEDGE_SCHEMA_SPECIFICATION §6.

Phase-aware schema (added 2026-04-29 — PR1 of regimen-phases-refactor; see
`docs/reviews/regimen-phases-refactor-plan-2026-04-28.md` §4).

`Regimen.phases` decomposes a treatment course into ordered, named blocks
("lymphodepletion", "main", "il2_support", …) so the render layer can show
each phase as a distinct section instead of flattening them into a single
component list. `Regimen.bridging_options` carries acceptable bridging
regimen IDs for therapies with a manufacturing window (CAR-T, TIL).

Back-compat invariant: legacy YAMLs lack `phases:`. The
`@model_validator(mode="after")` below auto-wraps such regimens into a
single phase named "main" containing all original `components`. Therefore
`regimen.phases[0].components == regimen.components` always holds for
legacy data, and downstream code may iterate either field. New YAMLs
that author `phases:` explicitly are left as-is — `components` and
`phases` are independent on input; the auto-wrap is one-way only.
"""

from typing import Literal, Optional

from pydantic import Field, field_validator, model_validator

from ._reviewer_signoff import ReviewerSignoff, _migrate_int_signoffs
from .base import Base, UkraineRegistration


class RegimenComponent(Base):
    drug_id: str
    dose: Optional[str] = None  # "375 mg/m² IV"
    schedule: Optional[str] = None  # "day 1 of every 28-day cycle"
    route: Optional[str] = None  # IV | PO | SC
    duration: Optional[str] = None


class RegimenPhase(Base):
    """One named block of a multi-phase Regimen (KNOWLEDGE_SCHEMA_SPECIFICATION §6.4).

    `name` is open-string but the curator-facing vocabulary is:
        lymphodepletion | bridging | induction | consolidation | maintenance |
        main | premedication | conditioning | salvage_induction |
        alternating_block_a | alternating_block_b | il2_support

    Auto-wrapped legacy regimens always carry `name="main"`. PR2 will
    rename phases per-file as part of the manual migration.
    """

    name: str
    purpose_ua: str  # e.g. "виснаження лімфоцитів перед CAR-T для приживлення клітин"
    purpose_en: Optional[str] = None
    components: list[RegimenComponent]
    duration: Optional[str] = None  # "3 days, days -5 to -3"
    # "main_infusion" | "next_phase" | "absolute" | "previous_phase_completion"
    timing_relative_to: Optional[str] = None
    timing_offset_days: Optional[int] = None  # -5 = "5 days before main"
    optional: bool = False  # bridging — optional; lymphodepletion — required
    sources: list[str] = Field(default_factory=list)


class DoseAdjustment(Base):
    condition: str  # e.g. "FIB-4 > 3.25 OR cirrhosis"
    modification: str  # e.g. "Reduce bendamustine to 70 mg/m²"
    rationale: Optional[str] = None
    source_refs: list[str] = Field(default_factory=list)


class RegimenUkraineAvailability(Base):
    all_components_registered: bool = False
    all_components_reimbursed: bool = False
    per_component: dict[str, UkraineRegistration] = Field(default_factory=dict)
    notes: Optional[str] = None


class BetweenVisitWatchpoint(Base):
    """One between-visit watchpoint for the patient-mode renderer.

    PATIENT_MODE_SPEC §3.4: render-only field that powers the "На що
    звернути увагу між візитами" patient bundle section. The renderer
    groups items by `urgency` tier; engine MUST NOT consult this field
    as a treatment-selection signal (CHARTER §8.3).

    Authoring queue: `docs/plans/patient_watchpoints_authoring_queue_2026-05-01-0100.md`.
    Two Clinical Co-Lead sign-offs required per regimen before the
    `between_visit_watchpoints` field can be considered authored
    (CHARTER §6.1; see PATIENT_MODE_SPEC §6).
    """

    trigger_ua: str  # plain UA: what the patient might notice at home
    action_ua: str  # plain UA: what to do — log, call clinic, or ER
    urgency: Literal["log_at_next_visit", "call_clinic_same_day", "er_now"]
    cycle_day_window: Optional[str] = None  # e.g. "Day 7-14 — nadir"
    sources: list[str] = Field(default_factory=list)


class Regimen(Base):
    id: str
    name: str
    name_ua: Optional[str] = None
    alternate_names: list[str] = Field(default_factory=list)

    components: list[RegimenComponent]
    cycle_length_days: Optional[int] = None
    total_cycles: Optional[str] = None  # "6", "6-8", "until progression"

    # Phase-aware fields (added 2026-04-29). See module docstring.
    phases: list[RegimenPhase] = Field(default_factory=list)
    bridging_options: list[str] = Field(default_factory=list)  # regimen IDs

    toxicity_profile: Optional[str] = None  # none | low | moderate | severe | variable

    premedication: list[str] = Field(default_factory=list)
    mandatory_supportive_care: list[str] = Field(default_factory=list)  # SupportiveCare IDs
    monitoring_schedule_id: Optional[str] = None

    dose_adjustments: list[DoseAdjustment] = Field(default_factory=list)

    ukraine_availability: Optional[RegimenUkraineAvailability] = None

    # Patient-mode "between visits" watchpoints (PATIENT_MODE_SPEC §3.4).
    # Optional — existing regimens load without it. The renderer falls
    # back to a "ще не узгоджено клінічною командою" placeholder when
    # the list is empty so an empty list ≡ unauthored, never fabricated.
    between_visit_watchpoints: list[BetweenVisitWatchpoint] = Field(default_factory=list)

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    reviewers: list[str] = Field(default_factory=list)
    # CHARTER §6.1: ≥2 sign-offs to publish. Structured form — legacy
    # `reviewer_signoffs: 0` (int) coerced to [] by the validator below.
    reviewer_signoffs: list[ReviewerSignoff] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator("reviewer_signoffs", mode="before")
    @classmethod
    def _migrate_signoffs(cls, v):
        return _migrate_int_signoffs(v)

    @model_validator(mode="after")
    def _auto_wrap_legacy_components(self) -> "Regimen":
        """Back-compat: legacy YAMLs lack `phases:`. Auto-wrap their flat
        `components` list into a single phase named "main" so downstream
        code may iterate `regimen.phases` uniformly.

        One-way only: if `phases` is authored explicitly, `components` is
        left as-is. The render layer (PR2) decides the canonical source.
        """
        if not self.phases and self.components:
            self.phases = [
                RegimenPhase(
                    name="main",
                    purpose_ua="основна терапія",
                    components=list(self.components),
                )
            ]
        return self
