"""Algorithm entity — KNOWLEDGE_SCHEMA_SPECIFICATION §13.

An Algorithm is the decision tree that selects a default Indication
(and usually an alternative) for a given Disease + line of therapy,
based on RedFlag evaluations against patient data."""

from typing import Optional

from pydantic import Field

from .base import Base


class DecisionStep(Base):
    step: int
    evaluate: dict = Field(default_factory=dict)
    # Flexible eval clause — typically {any_of: [{red_flag: RF-X}, ...]}
    # or {all_of: [...]}, or {red_flag: RF-Y}, etc.

    if_true: Optional[dict] = None  # {result: IND-X} or {next_step: N}
    if_false: Optional[dict] = None


class Algorithm(Base):
    id: str
    applicable_to_disease: str  # Disease ID
    applicable_to_line_of_therapy: int
    purpose: Optional[str] = None

    output_indications: list[str]  # Indication IDs — all candidates this algo selects among
    default_indication: Optional[str] = None  # the "standard plan" default
    alternative_indication: Optional[str] = None  # the "aggressive plan" default

    decision_tree: list[DecisionStep] = Field(default_factory=list)

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    notes: Optional[str] = None
