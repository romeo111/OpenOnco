"""Structured ReviewerSignoff replaces the legacy int counter.

Per CHARTER §6.1 — every clinical content entity that publishes (Indication,
Algorithm, Regimen, RedFlag, BiomarkerActionability) needs ≥2 sign-offs
from distinct Clinical Co-Leads. The legacy schema stored only a counter
(`reviewer_signoffs: int`); the structured form records *who* signed off,
*when*, and *why*, so the publish-gate can be audited and per-reviewer
provenance can be surfaced in the rendered plan.

Backwards compatibility: each affected entity wraps this list with a
`field_validator(..., mode="before")` that coerces the legacy `int 0` to
an empty list. Existing YAML with `reviewer_signoffs: 0` continues to
load. New entities should use the structured list form directly.
"""

from typing import Optional

from pydantic import Field

from .base import Base


class ReviewerSignoff(Base):
    """A single sign-off action by a Clinical Co-Lead (CHARTER §6.1)."""

    reviewer_id: str  # FK → ReviewerProfile (REV-*)
    timestamp: str  # ISO 8601 datetime (UTC preferred)
    rationale: Optional[str] = None
    # Optional: pin the reviewer's approval to a specific entity revision
    # (typically the entity's `last_reviewed` value at sign-off time).
    entity_version: Optional[str] = None


def _migrate_int_signoffs(v):
    """Coerce the legacy `reviewer_signoffs: int` to an empty list.

    Used by every affected entity schema as a `field_validator(..., mode="before")`.
    The legacy counter never carried identity, so we cannot recover *who*
    signed off; existing entries become empty and are re-signed via the
    new structured tooling (CSD-5A).
    """
    if isinstance(v, int):
        return []
    return v


__all__ = ["ReviewerSignoff", "_migrate_int_signoffs"]
