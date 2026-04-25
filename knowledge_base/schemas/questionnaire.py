"""Questionnaire schema — guided patient profile builder.

A Questionnaire describes the questions a clinician should answer (in
order) to build a valid patient profile for one specific Disease + line
of therapy. Each Question maps 1:1 to a profile field path
(e.g. `demographics.ecog`, `biomarkers.del_17p`) and carries metadata
that the live preview pane on /try uses to surface impact:

  - impact: critical | required | recommended | optional
    "critical"   = absence blocks Plan generation (engine returns warning)
    "required"   = absence forces engine to use conservative default
    "recommended"= absence may miss a relevant alternative track
    "optional"   = nice-to-have, no plan effect

  - triggers: list of opaque strings naming what changes if this field flips:
    - "RF-X-FIRES"              fires a RedFlag
    - "filter:ecog_max"         participates in Indication.applicable_to filter
    - "select:IND-X"            biases Algorithm decision_tree toward IND-X
    - "ci:CI-X-applies"         activates a Contraindication
    These are display labels, NOT executed by the engine. The actual
    rule evaluation is done by the existing engine on the assembled JSON.

The questionnaire is curated content — every entry needs the same dual
sign-off as Indications per CHARTER §6.1.
"""

from __future__ import annotations

from typing import Optional, Union

from pydantic import Field

from .base import Base


class QuestionOption(Base):
    value: Union[str, int, float, bool]
    label: str  # Ukrainian display label
    helper: Optional[str] = None


class Question(Base):
    field: str  # dotted path: "demographics.ecog", "biomarkers.del_17p"
    label: str
    type: str  # integer | float | boolean | enum | text | range_with_threshold
    impact: str = "optional"  # critical | required | recommended | optional
    triggers: list[str] = Field(default_factory=list)
    helper: Optional[str] = None
    helper_link: Optional[str] = None  # URL to spec or KB entity
    options: list[QuestionOption] = Field(default_factory=list)
    range_min: Optional[float] = None
    range_max: Optional[float] = None
    units: Optional[str] = None
    default_value: Optional[Union[str, int, float, bool]] = None
    when: Optional[str] = None  # JS-style guard: "biomarkers.del_17p == true"


class QGroup(Base):
    title: str  # group heading
    description: Optional[str] = None
    questions: list[Question] = Field(default_factory=list)


class Questionnaire(Base):
    id: str
    disease_id: str
    line_of_therapy: int = 1
    title: str
    intro: Optional[str] = None
    groups: list[QGroup] = Field(default_factory=list)
    fixed_fields: dict = Field(default_factory=dict)
    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    reviewer_signoffs: int = 0
    notes: Optional[str] = None
