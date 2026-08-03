"""BiomarkerActionability entity — maps (gene-variant, tumor_type) pairs to
clinical actionability tiers, anchored on ESMO ESCAT.

Each instance answers "what does this specific variant mean for treatment in
this specific cancer?" Composes existing BIO-* (gene/variant taxonomy) and
DIS-* (disease taxonomy) entities into a per-tumor clinical interpretation.

Phase 1 of the CIViC pivot (2026-04-27): the OncoKB-specific fields
`oncokb_level` and `oncokb_snapshot_version` were dropped — see
docs/reviews/oncokb-public-civic-coverage-2026-04-27.md for the ToS
audit that triggered the pivot. Per-source level information now lives
in the `evidence_sources` list, where each entry references a Source
entity (SRC-*) and carries the source-native level token.

ESCAT remains the primary actionability tier (`escat_tier`) because it
is open-license and source-neutral. CIViC, OncoKB, NCCN page-section
references, ESMO sections, etc. all become entries inside
`evidence_sources`.

The canonical structure is registered in KNOWLEDGE_SCHEMA_SPECIFICATION.
ESCAT assignment remains a clinician-owned adjudication: this schema records
the evidence and review state, but never derives a tier from source-native
levels or from a model.
"""

from dataclasses import dataclass
from typing import Any, Literal, Mapping, Optional

from pydantic import Field, field_validator, model_validator

from ._reviewer_signoff import ReviewerSignoff, _migrate_int_signoffs
from .base import Base, ClinicalClaim


# ── ESCAT (ESMO Scale for Clinical Actionability of molecular Targets) ────────
# Mateo et al. 2018, Ann Oncol 29(9):1895-1902. Tiers I–V plus X (no evidence).
# ``IV`` is retained only as a legacy broad bucket; newly reviewed cells use
# the framework's ``IVA`` or ``IVB`` sub-tier where applicable.
EscatTier = Literal[
    "IA", "IB", "IC",
    "IIA", "IIB",
    "IIIA", "IIIB",
    "IVA", "IVB", "IV",
    "V", "X",
]
ActionabilityScope = Literal[
    "therapeutic_predictive",
    "therapeutic_resistance",
    "diagnostic",
    "prognostic",
    "monitoring",
    "screening",
    "surveillance",
    "germline_risk",
    "unclassified",
]
EscatApplicability = Literal["applicable", "not_applicable", "review_required"]
EscatAssessmentStatus = Literal["not_started", "draft", "clinically_reviewed"]
EscatStudyDesign = Literal[
    "prospective_randomized",
    "prospective_non_randomized",
    "basket_trial",
    "retrospective",
    "preclinical",
    "in_silico",
    "other",
]
EvidenceLaneToken = Literal[
    "standard_care",
    "molecular_evidence_option",
    "resistance_or_avoidance_signal",
    "trial_research_option",
    "insufficient_evidence",
]


class EscatEvidenceRecord(Base):
    """One source-grounded alteration-therapy assessment for ESCAT review.

    ESCAT is assigned to a specific alteration-drug pair in a tumour
    context; it cannot safely be derived from a CIViC level, a regulatory
    label, or a guideline reference alone. This compact dossier records
    reviewer-visible evidence coordinates without duplicating source
    content in the KB.
    """

    source: str
    therapy_context: str
    tumour_context: str
    study_design: EscatStudyDesign
    endpoint: Optional[str] = None
    outcome_summary: Optional[str] = None
    same_tumour_type: Optional[bool] = None


class EscatEvidenceDossier(Base):
    """Reviewer-owned rationale for a clinically adjudicated ESCAT tier."""

    assessment_status: EscatAssessmentStatus = "not_started"
    tier_rationale: Optional[str] = None
    evidence_records: list[EscatEvidenceRecord] = Field(default_factory=list)
    civic_snapshot_id: Optional[str] = None
    reviewed_against: Optional[str] = None


@dataclass(frozen=True)
class ActionabilityReleaseReadiness:
    """Result of the clinical-use gate for one BMA cell.

    The result carries human-readable reasons so release tooling can create
    a reviewer queue rather than silently dropping a BMA entry. It is never
    used to choose treatment tracks.
    """

    ready: bool
    reasons: tuple[str, ...]


def actionability_release_readiness(data: Mapping[str, Any]) -> ActionabilityReleaseReadiness:
    """Return whether a BMA can be shown as clinically reviewed ESCAT context.

    Passing requires an explicitly applicable therapeutic-predictive claim,
    a clinically reviewed evidence dossier, current-version sign-offs from
    two distinct in-scope reviewers, and a non-empty tier. All other BMA
    cells remain labelled context for review; they never participate in
    treatment-track selection.
    """

    reasons: list[str] = []
    if data.get("actionability_scope") != "therapeutic_predictive":
        reasons.append("ESCAT scope is not clinically classified as therapeutic_predictive")
    if data.get("escat_applicability") != "applicable":
        reasons.append("ESCAT applicability is not clinically approved")
    if not data.get("escat_tier"):
        reasons.append("ESCAT tier is absent")

    dossier = data.get("escat_evidence_dossier") or {}
    if not isinstance(dossier, Mapping) or dossier.get("assessment_status") != "clinically_reviewed":
        reasons.append("ESCAT evidence dossier is not clinically reviewed")
    elif not dossier.get("tier_rationale") or not dossier.get("evidence_records"):
        reasons.append("ESCAT evidence dossier lacks rationale or evidence records")

    # A sign-off is current only when it is explicitly in scope and pinned
    # to the BMA's current verification revision. The sign-off CLI writes
    # this version for BMAs; changing `last_verified` invalidates earlier
    # approvals until the evidence is re-reviewed.
    current_version = str(data.get("last_verified") or "").strip()
    reviewer_ids: set[str] = set()
    raw_signoffs = data.get("reviewer_signoffs") or []
    if isinstance(raw_signoffs, list):
        for signoff in raw_signoffs:
            if not isinstance(signoff, Mapping) or signoff.get("scope_match") is False:
                continue
            reviewer_id = str(signoff.get("reviewer_id") or "").strip()
            if reviewer_id and str(signoff.get("entity_version") or "").strip() == current_version:
                reviewer_ids.add(reviewer_id)
    if len(reviewer_ids) < 2:
        reasons.append("fewer than two current, in-scope reviewer sign-offs")

    return ActionabilityReleaseReadiness(ready=not reasons, reasons=tuple(reasons))


class RegulatoryApproval(Base):
    """Per-jurisdiction approval strings for regimens tied to this actionability cell.

    Free-form short strings (e.g. "encorafenib + cetuximab — mCRC 2L+ (FDA approved 2020)").
    Not a structured FK to Drug/Regimen because the same actionability cell often
    spans multiple regimens authorized at different times in different jurisdictions;
    structured links live on the Regimen.regulatory_status entity itself.
    """

    fda: list[str] = Field(default_factory=list)
    ema: list[str] = Field(default_factory=list)
    ukraine: list[str] = Field(default_factory=list)


class EvidenceSourceRef(Base):
    """Per-source actionability evidence reference.

    One BMA cell typically has 1–N entries here, one per source that
    independently attests the actionability claim. Source-native
    vocabulary is preserved verbatim (e.g. CIViC level "A" is stored as
    "A", not coerced to OncoKB "1"). The render layer iterates these
    entries and presents each with a link to the source where available.

    Fields:
        source: SRC-* ID, FK → Source entity (e.g. "SRC-CIVIC",
            "SRC-NCCN-NSCLC-V3-2026", "SRC-ESMO-CRC-2023").
        level: source-native level token. Examples: CIViC "A"/"B"/"C"/"D"/"E",
            NCCN "Category 1"/"Category 2A", OncoKB "1"/"2"/"3A" (legacy
            data only — not authored going forward).
        evidence_ids: source-internal evidence identifiers (e.g. CIViC
            evidence_id like "EID12345", NCCN page-section locator,
            PubMed-only references). Free-form list of strings.
        direction: CIViC-style "supports" | "does_not_support" | None. Other
            sources may leave this null. Generalizable: any source that
            distinguishes confirming vs. refuting evidence can use these
            tokens.
        significance: CIViC-style fine-grained label
            ("sensitivity"/"resistance"/"reduced_sensitivity"/etc.). Other
            sources may leave it null.
        evidence_lane: OpenOnco display lane for separating guideline-backed
            care, molecular options, resistance signals, and research-only
            evidence without collapsing all CIViC rows into standard care.
        note: free-form short clinical note (e.g. "FDA-CDx for osimertinib").
    """

    source: str  # FK → Source entity (SRC-*)
    level: str
    evidence_ids: list[str] = Field(default_factory=list)
    direction: Optional[str] = None  # "supports" | "does_not_support" | None
    significance: Optional[str] = None  # CIViC-specific significance label
    evidence_lane: Optional[EvidenceLaneToken] = None
    note: Optional[str] = None


class BiomarkerActionability(Base):
    """Tumor-specific clinical actionability of a biomarker variant.

    ID convention: ``BMA-{biomarker}-{variant?}-{disease}``
    e.g. ``BMA-BRAF-V600E-CRC``, ``BMA-EGFR-T790M-NSCLC``.

    The ``biomarker_id`` may already encode the variant (e.g. BIO-BRAF-V600E);
    in that case ``variant_qualifier`` may repeat or refine it (sub-variant /
    co-occurrence). Use null ``variant_qualifier`` when the cell is gene-level
    (any pathogenic alteration treated identically).

    Sources: each cell carries a primary `evidence_sources` list (per-source
    leveled attestations) plus a `primary_sources` list (FK strings to Source
    entities used for general citation). Both are required to be non-empty
    in active production data; the loader enforces ≥1 entry on
    `primary_sources`. Phase 1.5 migration populates `evidence_sources` from
    legacy `oncokb_level` claims plus existing `primary_sources`.

    `escat_tier` is the **primary** actionability tier only after an explicit
    therapeutic-predictive applicability decision and clinical review. It is
    source-neutral and open-license; per-source levels live in
    `evidence_sources[*].level`. Unclassified legacy records retain their
    historical tier for audit visibility, but cannot pass the clinical-use
    release gate.
    """

    id: str  # BMA-{biomarker}-{variant?}-{disease}
    biomarker_id: str  # FK → BIO-*
    variant_qualifier: Optional[str] = None  # e.g. "V600E", "T790M"; null = gene-level
    disease_id: str  # FK → DIS-*

    # Primary actionability tier — source-neutral, open-license.
    escat_tier: Optional[EscatTier] = None

    # ESCAT applies only to a therapeutic-predictive alteration-drug claim.
    # Older cells default to `unclassified` / `review_required` so migration
    # does not silently reinterpret their clinical meaning.
    actionability_scope: ActionabilityScope = "unclassified"
    escat_applicability: EscatApplicability = "review_required"
    escat_non_applicable_reason: Optional[str] = None
    escat_evidence_dossier: Optional[EscatEvidenceDossier] = None

    # Per-source attestations (CIViC level + direction + significance,
    # NCCN page-section, OncoKB legacy, etc.). Populated by Phase 1.5
    # migration from legacy `oncokb_level` claims; default empty for
    # back-compat with un-migrated YAML loads (loader will surface a
    # warning when this list is empty in Phase 2).
    evidence_sources: list[EvidenceSourceRef] = Field(default_factory=list)

    # Phase 1.5 sets this where a BMA's `escat_tier` / drug claims could
    # not be migrated mechanically and need a clinical co-lead to
    # re-verify (e.g. JAK2 V617F where the legacy `oncokb_level: "1"`
    # claim diverges from CIViC + oncokb-datahub gene-level evidence).
    actionability_review_required: bool = False

    evidence_summary: str  # 1–3 sentences clinical interpretation
    regulatory_approval: RegulatoryApproval = Field(default_factory=RegulatoryApproval)

    recommended_combinations: list[str] = Field(default_factory=list)
    contraindicated_monotherapy: list[str] = Field(default_factory=list)

    primary_sources: list[str]  # FK → SRC-*, ≥1 required (enforced by loader)
    last_verified: str  # ISO date (YYYY-MM-DD)
    # CHARTER §6.1: ≥2 sign-offs to publish. Structured form — legacy
    # `reviewer_signoffs: 0` (int) coerced to [] by the validator below.
    reviewer_signoffs: list[ReviewerSignoff] = Field(default_factory=list)
    clinical_claims: list[ClinicalClaim] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator("reviewer_signoffs", mode="before")
    @classmethod
    def _migrate_signoffs(cls, v):
        return _migrate_int_signoffs(v)

    @model_validator(mode="before")
    @classmethod
    def _normalize_legacy_shape(cls, v):
        return normalize_legacy_biomarker_actionability_payload(v)

    @model_validator(mode="after")
    def _validate_escat_applicability(self):
        """Prevent a reviewed non-therapeutic record from carrying ESCAT.

        The validator intentionally does not infer scope for pre-existing
        cells. A clinical reviewer must make that classification explicitly.
        """

        if self.escat_applicability == "not_applicable":
            if self.escat_tier is not None:
                raise ValueError("ESCAT-not-applicable BMA cells must not carry escat_tier")
            if not self.escat_non_applicable_reason:
                raise ValueError(
                    "ESCAT-not-applicable BMA cells require escat_non_applicable_reason"
                )

        if self.escat_applicability == "applicable":
            if self.actionability_scope != "therapeutic_predictive":
                raise ValueError(
                    "ESCAT-applicable BMA cells must use therapeutic_predictive scope"
                )
            if self.escat_tier is None:
                raise ValueError("ESCAT-applicable BMA cells require escat_tier")
            dossier = self.escat_evidence_dossier
            if dossier is None or dossier.assessment_status != "clinically_reviewed":
                raise ValueError(
                    "ESCAT-applicable BMA cells require a clinically reviewed evidence dossier"
                )
            if not dossier.tier_rationale or not dossier.evidence_records:
                raise ValueError(
                    "clinically reviewed ESCAT dossier requires rationale and evidence records"
                )

        return self


def normalize_legacy_biomarker_actionability_payload(raw: object) -> object:
    """Normalize older BMA authoring fields into the current schema."""
    if not isinstance(raw, dict):
        return raw

    normalized = dict(raw)

    if normalized.get("escat_tier") == "III":
        normalized["escat_tier"] = "IIIA"

    if not normalized.get("evidence_summary") and normalized.get("summary"):
        normalized["evidence_summary"] = normalized.get("summary")

    if not normalized.get("last_verified") and normalized.get("last_reviewed"):
        normalized["last_verified"] = normalized.get("last_reviewed")

    if not normalized.get("primary_sources"):
        primary_sources: list[str] = []
        for item in normalized.get("sources") or []:
            if isinstance(item, str):
                primary_sources.append(item)
            elif isinstance(item, dict) and item.get("source_id"):
                primary_sources.append(item["source_id"])
        if primary_sources:
            normalized["primary_sources"] = primary_sources

    evidence_sources = []
    for item in normalized.get("evidence_sources") or []:
        if not isinstance(item, dict):
            continue
        if item.get("source"):
            evidence_sources.append(item)
            continue
        source_id = item.get("source_id")
        if not source_id:
            continue
        evidence_sources.append({
            "source": source_id,
            "level": str(item.get("evidence_type") or normalized.get("evidence_level") or "legacy"),
            "evidence_lane": "insufficient_evidence",
            "note": item.get("description"),
        })
    if evidence_sources:
        normalized["evidence_sources"] = evidence_sources

    return normalized
