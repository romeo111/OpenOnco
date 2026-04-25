"""Indication entity — KNOWLEDGE_SCHEMA_SPECIFICATION §7. The central
clinical recommendation unit: disease + line of therapy + patient
applicability → recommended regimen, with full provenance."""

from typing import Optional

from pydantic import Field

from .base import Base, Citation, EvidenceLevel, StrengthOfRecommendation


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


class ExpectedOutcomes(Base):
    """Per REFERENCE_CASE_SPECIFICATION §3.7 — aligns with HCV-MZL fields."""

    overall_response_rate: Optional[str] = None
    complete_response: Optional[str] = None
    progression_free_survival: Optional[str] = None
    overall_survival_5y: Optional[str] = None
    hcv_cure_rate_svr12: Optional[str] = None
    # extra='allow' handles disease-specific fields


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
    do_not_do: list[str] = Field(default_factory=list)

    plan_track: Optional[str] = None  # "standard" | "aggressive" | "trial" | "palliative"

    # FDA non-device CDS positioning (per specs/CHARTER.md §15).
    # If `time_critical: true`, this Indication falls OUTSIDE the §520(o)(1)(E)
    # carve-out — HCP cannot meaningfully independently-review-the-basis under
    # time pressure, so the software function would be device-classified.
    time_critical: bool = False

    last_reviewed: Optional[str] = None
    reviewers: list[str] = Field(default_factory=list)
    reviewer_signoffs: int = 0  # CHARTER §6.1: >= 2 to publish
    notes: Optional[str] = None
