"""ReviewerSignoff — structured per-reviewer approval record.

Embedded inside Indication / Algorithm / Regimen / RedFlag /
BiomarkerActionability via a `reviewer_signoffs_v2` field (additive — the
legacy `reviewer_signoffs: int` counter on Indication is preserved for
backwards compatibility with existing YAML and the
`scripts/_close_signoffs.py` workflow).

CHARTER §6.1: any change to clinical content needs ≥2 of the three
Clinical Co-Leads to approve. The structured record makes it possible to
audit *which* reviewer approved *what*, *when*, and *why* — the bare
counter could be inflated without traceability.

The audit trail is duplicated in `knowledge_base/hosted/audit/signoffs.jsonl`
(append-only). When a reviewer withdraws a sign-off, the entry is removed
from the entity but a `withdraw` audit row is appended — history preserved.
"""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import Base


class ReviewerSignoff(Base):
    """One Clinical Co-Lead's structured sign-off on a clinical entity.

    Fields:
      reviewer_id: REV-* identifier of a profile in
        `knowledge_base/hosted/content/reviewers/`.
      signoff_date: ISO date of approval (YYYY-MM-DD).
      rationale: Free-form clinical rationale for approval. Required —
        a sign-off without justification is not a sign-off.
      entity_version_at_signoff: optional snapshot of the entity's
        `last_reviewed` (or git SHA, or schema version) at the moment of
        sign-off; used to detect "stale" sign-offs after later edits.
      scope_match: did the reviewer's `sign_off_scope` cover this
        entity at sign-off time? `True` for in-scope sign-offs; `False`
        when `--strict` was bypassed (auditable).
    """

    reviewer_id: str = Field(..., description="REV-* reviewer profile ID")
    signoff_date: str = Field(..., description="ISO date YYYY-MM-DD")
    rationale: str = Field(..., description="Clinical rationale for approval")
    entity_version_at_signoff: Optional[str] = None
    scope_match: bool = True


__all__ = ["ReviewerSignoff"]
