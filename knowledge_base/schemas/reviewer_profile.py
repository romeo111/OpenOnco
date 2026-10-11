"""Clinical reviewer profile for sign-off attribution per CHARTER §6.1.

A ReviewerProfile identifies one Clinical Co-Lead authorized to sign off
on KB entries within a declared scope (disease categories + entity types,
optionally narrowed to specific DIS-* IDs). Sign-offs reference profiles
by `id` so the audit trail survives reviewer-roster changes.

Three placeholder profiles ship under `hosted/content/reviewers/` as roster
templates, not eligible approvals. Positive gate tests use synthetic profiles
only inside isolated test fixtures.
Per CHARTER §6.1, two of three Co-Leads must approve clinical content;
the placeholders satisfy neither runtime review coverage nor the policy.
"""

from datetime import date
from typing import Literal, Optional

from pydantic import Field

from .base import Base


class SignOffScope(Base):
    """What entity types and disease categories a reviewer can sign off on.

    `disease_categories` are coarse buckets (lymphoma_b_cell, myeloma,
    breast, nsclc, …) used to scope sign-offs without enumerating every
    DIS-* id. Use `diseases_explicit` to narrow further or to grant
    out-of-bucket coverage. The wildcard `["all"]` in `disease_categories`
    means the reviewer can sign off across all categories (e.g. molecular
    pathology lead reviewing biomarker actionability across solid + heme).
    """

    disease_categories: list[str] = Field(default_factory=list)
    entity_types: list[str] = Field(default_factory=list)
    # values: Indication / Algorithm / Regimen / RedFlag / BiomarkerActionability
    diseases_explicit: list[str] = Field(default_factory=list)


class ReviewerAuthorization(Base):
    """Human-recorded governance provenance; never inferred from a profile name.

    Pending is the safe default. Approval eligibility additionally requires
    a dated decision reference and stable identity key in the release gate.
    A schema-valid record alone does not authenticate clinical credentials.
    """

    status: Literal["pending", "approved", "revoked"] = "pending"
    verified_on: Optional[date] = None
    decision_reference: Optional[str] = None
    identity_key: Optional[str] = None


class ReviewerProfile(Base):
    """A clinical co-lead authorized to sign off on KB entries.

    ID convention: ``REV-{role}-{name-or-PLACEHOLDER}``
    e.g. ``REV-HEME-LEAD-PLACEHOLDER``, ``REV-SOLID-LEAD-IVANENKO``.
    """

    id: str
    name: dict  # {preferred, ukrainian, english, suffix}
    specialty: str
    qualifications: list[str] = Field(default_factory=list)
    sign_off_scope: SignOffScope = Field(default_factory=SignOffScope)
    last_active: str  # ISO date (YYYY-MM-DD)
    notes: Optional[str] = None
    authorization: Optional[ReviewerAuthorization] = None


__all__ = ["ReviewerProfile", "ReviewerAuthorization", "SignOffScope"]
