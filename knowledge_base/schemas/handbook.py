"""OpenOnco Handbook content entities.

Handbook content is an educational layer over the existing KB. It does not
route the clinical engine; it links back to structured KB entities, synthetic
cases, and source records.
"""

from typing import Literal, Optional

from pydantic import Field, model_validator

from .base import Base


ReviewStatus = Literal["draft", "proposed", "reviewed", "needs_refresh", "retired"]
Audience = Literal["hcp_learner", "clinician", "maintainer"]
QuestionType = Literal["type_a", "type_k", "mcq", "short_answer"]
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
    reviewer_signoffs: list[dict] = Field(default_factory=list)
    legal_notes: Optional[str] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def _chapter_contract(self):
        if not self.learning_objectives:
            raise ValueError("HandbookChapter.learning_objectives must not be empty")
        if not self.source_ids:
            raise ValueError("HandbookChapter.source_ids must not be empty")
        if not self.at_a_glance:
            raise ValueError("HandbookChapter.at_a_glance must not be empty")
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
    reviewer_signoffs: list[dict] = Field(default_factory=list)
    notes: Optional[str] = None

    @model_validator(mode="after")
    def _question_contract(self):
        if self.type in {"type_a", "type_k", "mcq"} and len(self.options) < 2:
            raise ValueError("Objective handbook questions need at least two options")
        keys = {option.key for option in self.options}
        if self.type in {"type_a", "mcq"} and self.correct_answer not in keys:
            raise ValueError("correct_answer must match one option key")
        if not self.source_ids:
            raise ValueError("HandbookQuestion.source_ids must not be empty")
        return self
