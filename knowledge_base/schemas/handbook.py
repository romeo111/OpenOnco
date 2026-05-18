"""OpenOnco Handbook content entities.

Handbook content is an educational layer over the existing KB. It does not
route the clinical engine; it links back to structured KB entities, synthetic
cases, and source records.

Review workflow (HANDBOOK_MODE_SPEC §4) — the schema enforces these
intrinsic invariants; the loader handles cross-entity checks (does
`reviewer_id` resolve to a REV-*?) and advisory warnings (stale review,
draft needs clinical merge):

  draft          (default)     — no metadata required.
  proposed                     — ≥1 reviewer_signoff + last_reviewed.
  reviewed                     — ≥2 distinct reviewer_signoffs +
                                  last_reviewed. Mirrors CHARTER §6.1
                                  two-reviewer publish gate for clinical
                                  content. (Drafts and proposed content
                                  remain permissive — does not change
                                  the §6.1 dev-mode exemption.)
  needs_refresh                — last_reviewed required; signoffs from
                                  a prior review may be carried over,
                                  but the loader flags content as stale.
  retired                      — permissive terminal state; render layer
                                  filters these out of the index.
"""

from datetime import date
from typing import Literal, Optional

from pydantic import Field, field_validator, model_validator

from ._reviewer_signoff import ReviewerSignoff, _migrate_int_signoffs
from .base import Base


ReviewStatus = Literal["draft", "proposed", "reviewed", "needs_refresh", "retired"]
Audience = Literal["hcp_learner", "clinician", "maintainer"]
QuestionType = Literal["type_a", "type_k", "mcq", "short_answer"]


def _parse_iso_date(value: Optional[str]) -> Optional[date]:
    """Accept YYYY-MM-DD or full ISO 8601 datetime; return a date or None.

    Raises ValueError on malformed input so the schema fails fast rather
    than silently treating a typo as "no date"."""
    if value is None or value == "":
        return None
    # date.fromisoformat handles "YYYY-MM-DD"; strip any trailing T-time
    # so authors can record either depth.
    head = value.split("T", 1)[0]
    return date.fromisoformat(head)


def _require_review_metadata(
    entity_id: str,
    review_status: str,
    last_reviewed: Optional[str],
    signoffs: list,
) -> None:
    """Enforce the status → metadata contract documented at the module
    top. Called from both HandbookChapter and HandbookQuestion model
    validators so the rules stay consistent across entity types."""
    if review_status == "draft" or review_status == "retired":
        return
    if review_status in {"proposed", "reviewed", "needs_refresh"}:
        if not last_reviewed:
            raise ValueError(
                f"{entity_id}: review_status={review_status!r} requires last_reviewed (ISO date)"
            )
        # Force the loader to surface malformed dates early.
        _parse_iso_date(last_reviewed)
    if review_status == "proposed" and len(signoffs) < 1:
        raise ValueError(
            f"{entity_id}: review_status='proposed' requires ≥1 reviewer_signoff"
        )
    if review_status == "reviewed":
        if len(signoffs) < 2:
            raise ValueError(
                f"{entity_id}: review_status='reviewed' requires ≥2 reviewer_signoffs (CHARTER §6.1)"
            )
        reviewer_ids = {getattr(s, "reviewer_id", None) for s in signoffs}
        if len(reviewer_ids) < 2:
            raise ValueError(
                f"{entity_id}: review_status='reviewed' requires signoffs from ≥2 distinct reviewers; "
                f"got {len(signoffs)} signoff(s) from {len(reviewer_ids)} reviewer(s)"
            )
Difficulty = Literal["intro", "intermediate", "advanced"]


class HandbookLinkedEntities(Base):
    diseases: list[str] = Field(default_factory=list)
    algorithms: list[str] = Field(default_factory=list)
    indications: list[str] = Field(default_factory=list)
    regimens: list[str] = Field(default_factory=list)
    redflags: list[str] = Field(default_factory=list)
    biomarkers: list[str] = Field(default_factory=list)
    workups: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)


class HandbookSection(Base):
    heading: str
    body: str
    source_ids: list[str] = Field(default_factory=list)
    linked_entity_ids: list[str] = Field(default_factory=list)


class HandbookCaseLink(Base):
    id: str
    title: str
    path: str
    learning_focus: list[str] = Field(default_factory=list)


class HandbookChapter(Base):
    id: str
    title: str
    audience: Audience = "hcp_learner"
    language: Literal["en", "uk"] = "en"
    disease_ids: list[str] = Field(default_factory=list)
    topic_tags: list[str] = Field(default_factory=list)
    learning_objectives: list[str] = Field(default_factory=list)
    at_a_glance: list[str] = Field(default_factory=list)
    sections: list[HandbookSection] = Field(default_factory=list)
    linked_entities: HandbookLinkedEntities = Field(default_factory=HandbookLinkedEntities)
    source_ids: list[str] = Field(default_factory=list)
    case_links: list[HandbookCaseLink] = Field(default_factory=list)
    question_ids: list[str] = Field(default_factory=list)
    review_status: ReviewStatus = "draft"
    last_reviewed: Optional[str] = None
    # CHARTER §6.1: ≥2 sign-offs to publish. Structured form; legacy
    # `reviewer_signoffs: 0` (int) coerced to [] by the validator below
    # to match RedFlag / Indication migration shape.
    reviewer_signoffs: list[ReviewerSignoff] = Field(default_factory=list)
    legal_notes: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("reviewer_signoffs", mode="before")
    @classmethod
    def _migrate_signoffs(cls, v):
        return _migrate_int_signoffs(v)

    @model_validator(mode="after")
    def _chapter_contract(self):
        if not self.learning_objectives:
            raise ValueError("HandbookChapter.learning_objectives must not be empty")
        if not self.source_ids:
            raise ValueError("HandbookChapter.source_ids must not be empty")
        if not self.at_a_glance:
            raise ValueError("HandbookChapter.at_a_glance must not be empty")
        _require_review_metadata(
            self.id, self.review_status, self.last_reviewed, self.reviewer_signoffs
        )
        return self


class HandbookQuestionOption(Base):
    key: str
    text: str


class HandbookQuestion(Base):
    id: str
    chapter_id: str
    type: QuestionType
    stem: str
    options: list[HandbookQuestionOption] = Field(default_factory=list)
    correct_answer: str
    explanation: str
    source_ids: list[str] = Field(default_factory=list)
    linked_entity_ids: list[str] = Field(default_factory=list)
    tests_reasoning: list[str] = Field(default_factory=list)
    difficulty: Difficulty = "intermediate"
    review_status: ReviewStatus = "draft"
    last_reviewed: Optional[str] = None
    reviewer_signoffs: list[ReviewerSignoff] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator("reviewer_signoffs", mode="before")
    @classmethod
    def _migrate_signoffs(cls, v):
        return _migrate_int_signoffs(v)

    @model_validator(mode="after")
    def _question_contract(self):
        if self.type in {"type_a", "type_k", "mcq"} and len(self.options) < 2:
            raise ValueError("Objective handbook questions need at least two options")
        keys = {option.key for option in self.options}
        if self.type in {"type_a", "mcq"} and self.correct_answer not in keys:
            raise ValueError("correct_answer must match one option key")
        if not self.source_ids:
            raise ValueError("HandbookQuestion.source_ids must not be empty")
        _require_review_metadata(
            self.id, self.review_status, self.last_reviewed, self.reviewer_signoffs
        )
        return self
