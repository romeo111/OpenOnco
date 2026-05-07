"""Indication entity — KNOWLEDGE_SCHEMA_SPECIFICATION §7. The central
clinical recommendation unit: disease + line of therapy + patient
applicability → recommended regimen, with full provenance."""

from typing import Optional

from pydantic import Field, field_validator

from ._reviewer_signoff import ReviewerSignoff, _migrate_int_signoffs
from .base import Base, Citation, EvidenceLevel, StrengthOfRecommendation


# Sentinel SRC-* id assigned to outcome values that pre-date the Phase 2
# schema migration (Pivotal Trial Outcomes Ingestion Plan §"Schema
# evolution"). Defined as a Source entity at
# `knowledge_base/hosted/content/sources/src_legacy_uncited.yaml` so the
# referential integrity check succeeds. Phase 3 (gap-fill) replaces these
# with real SRC-* ids as values get traced back to pivotal trials.
LEGACY_UNCITED_SOURCE_ID = "SRC-LEGACY-UNCITED"


class BiomarkerRequirement(Base):
    biomarker_id: str
    required: bool = True
    value_constraint: Optional[str] = None  # free-form for now, e.g. ">= 30%"


class IndicationApplicability(Base):
    disease_id: str
    line_of_therapy: int  # 1, 2, 3...
    stage_requirements: list[str] = Field(default_factory=list)
    biomarker_requirements_required: list[BiomarkerRequirement] = Field(default_factory=list)
    biomarker_requirements_excluded: list[BiomarkerRequirement] = Field(default_factory=list)
    demographic_constraints: dict = Field(default_factory=dict)
    # e.g. {age_min: 18, age_max: null, ecog_max: 2, fit_for_chemo: true}


class OutcomeValue(Base):
    """Citation-bearing wrapper around a clinical-trial outcome value.

    Phase 2 of the Pivotal Trial Outcomes Ingestion Plan
    (`docs/plans/pivotal_trial_outcomes_ingestion_plan_2026-04-30.md`).
    Plain-string outcome values are coerced to
    ``OutcomeValue(value=<str>, source="SRC-LEGACY-UNCITED")`` by
    ``ExpectedOutcomes._coerce_legacy_string`` so the Phase-1 audit can
    flag pre-migration entries; Phase 3 replaces those placeholders with
    real ``SRC-*`` ids as outcomes get traced to their pivotal-trial
    publications.
    """

    value: str
    source: str
    source_refs: list[str] = Field(default_factory=list)
    confidence_interval: Optional[str] = None  # e.g. "95% CI 4.7-6.5"
    median_followup_months: Optional[float] = None


# The schema-declared outcome fields on `ExpectedOutcomes`. Disease-
# specific extras admitted via `extra='allow'` are deliberately NOT
# coerced — they keep their raw shape (string, int, dict, …) until a
# future migration formalizes each one.
_OUTCOME_FIELDS: tuple[str, ...] = (
    "overall_response_rate",
    "complete_response",
    "progression_free_survival",
    "overall_survival_5y",
    "overall_survival_median",
    "disease_free_survival_hr",
    "hcv_cure_rate_svr12",
)


class ExpectedOutcomes(Base):
    """Per REFERENCE_CASE_SPECIFICATION §3.7 — aligns with HCV-MZL fields.

    Each outcome field accepts EITHER a plain string (legacy, pre-Phase-2
    YAML — coerced to ``OutcomeValue(value=str, source="SRC-LEGACY-UNCITED")``)
    OR an ``OutcomeValue`` dict (Phase 2+ format). The
    ``_coerce_legacy_string`` validator runs in ``mode="before"`` so the
    coercion happens before Pydantic's per-field type check; ``None`` and
    dict shapes pass through untouched.
    """

    overall_response_rate: Optional[OutcomeValue] = None
    complete_response: Optional[OutcomeValue] = None
    progression_free_survival: Optional[OutcomeValue] = None
    overall_survival_5y: Optional[OutcomeValue] = None
    overall_survival_median: Optional[OutcomeValue] = None  # Phase 2 (new)
    disease_free_survival_hr: Optional[OutcomeValue] = None  # Phase 2 (new - adjuvant)
    hcv_cure_rate_svr12: Optional[OutcomeValue] = None
    # extra='allow' (inherited from Base) handles disease-specific fields

    @field_validator(*_OUTCOME_FIELDS, mode="before")
    @classmethod
    def _coerce_legacy_string(cls, v):
        """Plain string → OutcomeValue(value=str, source="SRC-LEGACY-UNCITED").

        Backward-compat shim for Phase 2: the 312 indication YAMLs all
        carry plain-string outcomes today. Coercing here preserves the
        loader contract (KB validator stays green) while exposing a
        `source` pointer to render-layer code and to Phase 3 gap-fill.
        ``None`` (absent field) and ``dict`` (already-migrated) values
        pass through unchanged.
        """
        if isinstance(v, str):
            return {"value": v, "source": LEGACY_UNCITED_SOURCE_ID}
        return v


class ControversyPosition(Base):
    position: str
    sources: list[str] = Field(default_factory=list)
    evidence_note: Optional[str] = None


class KnownControversy(Base):
    topic: str
    positions: list[ControversyPosition]
    our_default: Optional[str] = None
    rationale: Optional[str] = None


class Indication(Base):
    id: str
    applicable_to: IndicationApplicability

    recommended_regimen: Optional[str] = None  # Regimen ID
    concurrent_therapy: list[str] = Field(default_factory=list)
    followed_by: list[str] = Field(default_factory=list)  # next-line Indication IDs

    evidence_level: Optional[EvidenceLevel] = None
    strength_of_recommendation: Optional[StrengthOfRecommendation] = None
    nccn_category: Optional[str] = None  # "1" | "2A" | "2B" | "3"

    expected_outcomes: Optional[ExpectedOutcomes] = None

    hard_contraindications: list[str] = Field(default_factory=list)  # Contraindication IDs
    red_flags_triggering_alternative: list[str] = Field(default_factory=list)  # RedFlag IDs

    required_tests: list[str] = Field(default_factory=list)  # Test IDs (priority_class=critical)
    desired_tests: list[str] = Field(default_factory=list)

    rationale: Optional[str] = None
    sources: list[Citation] = Field(default_factory=list)
    known_controversies: list[KnownControversy] = Field(default_factory=list)

    # "What NOT to do" list per REFERENCE_CASE_SPECIFICATION §1.3 critical:
    # explicit prohibitive bullets that frame avoidable harm. Surfaced by
    # render_plan_html as a dedicated section.
    #
    # `do_not_do` is the canonical Ukrainian-language list (legacy primary
    # language, per CHARTER §1). `do_not_do_en` is the optional English
    # companion list — when populated, EN-side render prefers it over the
    # UA list. Bullets pair positionally; if `do_not_do_en` is shorter
    # than `do_not_do`, render falls back to UA for the un-translated
    # tail.
    do_not_do: list[str] = Field(default_factory=list)
    do_not_do_en: list[str] = Field(default_factory=list)

    plan_track: Optional[str] = None  # "standard" | "aggressive" | "trial" | "palliative"

    # FDA non-device CDS positioning (per specs/CHARTER.md §15).
    # If `time_critical: true`, this Indication falls OUTSIDE the §520(o)(1)(E)
    # carve-out — HCP cannot meaningfully independently-review-the-basis under
    # time pressure, so the software function would be device-classified.
    time_critical: bool = False

    last_reviewed: Optional[str] = None
    reviewers: list[str] = Field(default_factory=list)
    # CHARTER §6.1: ≥2 sign-offs to publish. Migrated from int counter to
    # structured list — see _reviewer_signoff.py. Legacy YAML with
    # `reviewer_signoffs: 0` is coerced to [] by the validator below.
    reviewer_signoffs: list[ReviewerSignoff] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator("reviewer_signoffs", mode="before")
    @classmethod
    def _migrate_signoffs(cls, v):
        return _migrate_int_signoffs(v)
