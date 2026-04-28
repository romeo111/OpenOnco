"""MdtSkill entity — versioned metadata for one MDT specialist role
(= virtual doctor) used by `engine/mdt_orchestrator.py`.

Migrated from `_SKILL_REGISTRY` in mdt_orchestrator.py per skill candidate
#7a. Living in the KB (rather than as a Python dict) lets clinical
co-leads bump version, add sign-offs, and register sources via the
two-reviewer flow described in CHARTER §6.1 / ADR-0002 — same governance
as Indications and RedFlags.

The orchestrator's `get_skill(role_id)` reads from the KB by `role_id`,
not by `id`. `id` follows the project's uppercase-prefixed convention
(e.g., `MDT-SKILL-HEMATOLOGIST`) for cross-entity uniqueness; `role_id`
is the lowercase identifier the engine uses to look up roles.
"""

from typing import Optional

from pydantic import Field

from .base import Base


class MdtSkill(Base):
    id: str  # MDT-SKILL-<UPPER>
    role_id: str  # lowercase, matches engine's _ROLE_CATALOG keys
    name: str  # UA display name
    version: str = "0.1.0"
    last_reviewed: str  # ISO date
    clinical_lead: Optional[str] = None
    verified_by: list[dict] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    domain: Optional[str] = None
    notes: Optional[str] = None
