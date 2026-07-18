"""Algorithm entity — KNOWLEDGE_SCHEMA_SPECIFICATION §13.

An Algorithm is the decision tree that selects a default Indication
(and usually an alternative) for a given Disease + line of therapy,
based on RedFlag evaluations against patient data."""

from typing import Literal, Optional, Union, get_args

from pydantic import Field, field_validator

from ._reviewer_signoff import ReviewerSignoff, _migrate_int_signoffs
from .base import Base

# ── `applicable_to_disease_state` registry ──────────────────────────────
# Closed set of disambiguator values. This is a LIVE ROUTING KEY read by
# `engine/plan.py::_find_algorithm`, so an unregistered value is not a
# harmless typo: it changes which patients an algorithm can serve, and can
# silently re-route patients to a different algorithm (see the two failure
# modes documented on the field below). Keeping it closed makes a typo a
# load-time schema error instead of a silent routing change.
#
# Adding a value here is engine/schema work. Changing or removing one moves
# patients between algorithms and is therefore clinical content under
# CHARTER §6.1.
#
# NOTE — the values below span two different axes, and the field name only
# describes the first. This is deliberate and pre-existing, not drift:
# breast 2L uses the key for receptor subtype (PR #150 KB-drift signal #3,
# regression-tested in tests/test_engine_find_algorithm.py). The field is in
# practice a general "which of several same-disease-and-line algorithms
# applies" discriminator. Renaming it to match is a separate change.

DiseaseStateValue = Literal[
    # Stage / treatment intent.
    "adjuvant",
    "advanced",
    "locally_advanced",
    "metastatic",
    "resectable",
    "resectable_perioperative",
    "unresectable_definitive",
    # Disease-prefixed compounds. Inconsistent with the bare values above
    # (they re-encode the disease already named in `applicable_to_disease`),
    # but normalising them would re-route patients.
    "pdac_lapc_unresectable",
    "pdac_resectable_or_borderline",
    "rectal_locally_advanced_tnt",
    # Prostate hormone-sensitivity states, camelCase per clinical convention.
    "mCRPC",
    "mHSPC",
    # Receptor subtype — NOT a disease state (breast 2L; see note above).
    "HER2-positive",
    "HR-positive_HER2-negative",
    "TNBC",
]

DISEASE_STATE_VALUES: frozenset[str] = frozenset(get_args(DiseaseStateValue))


class DecisionStep(Base):
    step: Union[int, str]
    evaluate: dict = Field(default_factory=dict)
    # Flexible eval clause — typically {any_of: [{red_flag: RF-X}, ...]}
    # or {all_of: [...]}, or {red_flag: RF-Y}, etc.

    if_true: Optional[dict] = None  # {result: IND-X} or {next_step: N}
    if_false: Optional[dict] = None


class Algorithm(Base):
    id: str
    applicable_to_disease: str  # Disease ID
    applicable_to_line_of_therapy: int

    # Disambiguates several algorithms sharing one disease + line. Read by
    # `engine/plan.py::_find_algorithm`, which resolves
    # state-matched > state-agnostic > load-order legacy fallback, matching
    # case-insensitively.
    #
    # `None` is not "unspecified" — it makes the algorithm the STATE-AGNOSTIC
    # CATCH-ALL that wins for every patient with no `disease_state`. Two
    # consequences worth knowing before editing this field on any algorithm:
    #
    #   1. Adding a value to the sole catch-all in its group does not make
    #      unstaged patients unroutable. It drops them into the legacy
    #      fallback, which returns the first state-specific algorithm in
    #      `entities_by_id` insertion order — `sorted()` over full paths in
    #      `loader.py`, which for the flat `algorithms/` dir is filename
    #      order. Routing then changes, decided by a sort.
    #   2. A value outside the registry does not merely fail to state-match:
    #      the loader catches ValidationError and skips the file, so the
    #      algorithm drops out of `entities_by_id` entirely and is invisible
    #      to `_find_algorithm`. In a catch-all group that also removes the
    #      catch-all, triggering failure mode 1. Hence the closed Literal:
    #      this fails at load instead.
    #
    # Which algorithm an unstaged patient should get is an open clinical
    # policy question — docs/reviews/disease-state-routing-policy-2026-07-18.md.
    applicable_to_disease_state: Optional[DiseaseStateValue] = None

    purpose: Optional[str] = None

    output_indications: list[str]  # Indication IDs — all candidates this algo selects among
    default_indication: Optional[str] = None  # the "standard plan" default
    alternative_indication: Optional[str] = None  # the "aggressive plan" default

    decision_tree: list[DecisionStep] = Field(default_factory=list)

    sources: list[str] = Field(default_factory=list)
    last_reviewed: Optional[str] = None
    # CHARTER §6.1: ≥2 sign-offs to publish. Structured form — legacy
    # `reviewer_signoffs: 0` (int) coerced to [] by the validator below.
    reviewer_signoffs: list[ReviewerSignoff] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator("reviewer_signoffs", mode="before")
    @classmethod
    def _migrate_signoffs(cls, v):
        return _migrate_int_signoffs(v)
