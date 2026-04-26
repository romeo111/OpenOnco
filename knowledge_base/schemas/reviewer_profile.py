"""ReviewerProfile — Clinical Co-Lead identity + sign-off scope.

YAML location: `knowledge_base/hosted/content/reviewers/rev_*.yaml`.

Per CHARTER §6.1, OpenOnco recognises three Clinical Co-Lead roles, each
with a defined sign-off scope (e.g., heme-onc lead can sign hematologic
indications/regimens but not solid-tumor entities). The profile encodes:

  - identity (display name, institutional affiliation — never PHI)
  - credentials (board certifications, year of certification)
  - sign-off scope (entity types + disease categories the reviewer is
    competent to approve)
  - lifecycle (active / inactive — inactive reviewers' historical
    sign-offs remain valid; new sign-offs are refused)

Placeholder profiles ship with the v0.1 KB so the CLI works end-to-end
*before* real Clinical Co-Leads onboard. Every placeholder profile has
the suffix `-PLACEHOLDER` in its ID so they're trivially greppable when
real profiles replace them.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from .base import Base


class ReviewerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PLACEHOLDER = "placeholder"  # demo / pre-onboarding profile


class SignoffScope(Base):
    """Which entity types + disease categories the reviewer can sign off.

    `entity_types` is a list of dir-names (`indications`, `algorithms`,
    `regimens`, `redflags`, `biomarker_actionability`). Empty list = no
    restriction.

    `disease_categories` is a list of free-form disease-family tags
    (e.g. `hematologic`, `lymphoid`, `myeloid`, `solid`,
    `gastrointestinal`, `breast`, `gu`, `gyn`, `thoracic`, `cns`).
    Matched against `Disease.category` (or filename heuristics) by the
    sign-off CLI. Empty list = no restriction.

    `disease_ids` is an explicit allow-list of `DIS-*` IDs that overrides
    the category match — useful for narrow expertise (e.g. "DIS-HCL only").
    Empty list = use categories.
    """

    entity_types: list[str] = Field(default_factory=list)
    disease_categories: list[str] = Field(default_factory=list)
    disease_ids: list[str] = Field(default_factory=list)


class ReviewerProfile(Base):
    id: str = Field(..., description="REV-* unique reviewer ID")
    display_name: str
    affiliation: Optional[str] = None
    role_title: Optional[str] = None  # e.g. "Hematology Clinical Co-Lead"
    credentials: list[str] = Field(default_factory=list)
    # e.g. ["MD", "PhD", "ESMO certified medical oncologist (2020)"]

    sign_off_scope: SignoffScope = Field(default_factory=SignoffScope)

    status: ReviewerStatus = ReviewerStatus.PLACEHOLDER
    onboarded_date: Optional[str] = None  # ISO YYYY-MM-DD
    last_active: Optional[str] = None
    contact: Optional[str] = None  # email / ORCID / institutional handle
    notes: Optional[str] = None


__all__ = ["ReviewerProfile", "ReviewerStatus", "SignoffScope"]
