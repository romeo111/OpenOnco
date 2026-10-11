"""Fail-closed review provenance, independent of treatment-track selection."""
from datetime import date, datetime, timezone
from typing import Any, Mapping

from ._review_scope import entity_disease_ids, reviewer_scope_matches


def authorized_reviewer_identity(profile: Mapping[str, Any], reviewer_id: str,
                                 *, as_of: date | None = None) -> str | None:
    """Read explicit human governance metadata; never infer credentials."""
    if profile.get("id") != reviewer_id or "PLACEHOLDER" in reviewer_id.upper():
        return None
    authorization = profile.get("authorization")
    if not isinstance(authorization, Mapping) or authorization.get("status") != "approved":
        return None
    identity = str(authorization.get("identity_key") or "").strip()
    reference = str(authorization.get("decision_reference") or "").strip()
    try:
        verified = date.fromisoformat(str(authorization.get("verified_on") or ""))
    except ValueError:
        return None
    if not identity or not reference or verified > (as_of or datetime.now(timezone.utc).date()):
        return None
    return identity


def eligible_signoffs(entity_data: Mapping[str, Any],
                      reviewer_profiles: Mapping[str, Mapping[str, Any]] | None,
                      *, revision_field: str, entity_type: str,
                      disease_lineage: str | None = None,
                      rejection_reasons: list[str] | None = None) -> list[dict]:
    """Count current explicit in-scope reviews by distinct authorized identities.

    Unknown metadata stays visible in source/audit records but cannot confer
    release eligibility. The function does not mutate records or choose tracks.
    """
    def reject(reason: str) -> None:
        if rejection_reasons is not None and reason not in rejection_reasons:
            rejection_reasons.append(reason)

    current_revision = str(entity_data.get(revision_field) or "").strip()
    try:
        revision_date = date.fromisoformat(current_revision)
    except ValueError:
        reject("current content revision is absent or not an ISO date")
        return []
    now = datetime.now(timezone.utc)
    if revision_date > now.date():
        reject("current content revision is in the future")
        return []
    raw = entity_data.get("reviewer_signoffs")
    if not current_revision or not isinstance(raw, list) or not reviewer_profiles:
        reject("structured reviews or registered reviewer provenance are absent")
        return []
    accepted: list[dict] = []
    seen_identities: set[str] = set()
    for signoff in raw:
        if not isinstance(signoff, Mapping) or signoff.get("scope_match") is not True:
            reject("review scope is not explicitly affirmative")
            continue
        if str(signoff.get("entity_version") or "").strip() != current_revision:
            reject("review is not pinned to the current content revision")
            continue
        try:
            timestamp = datetime.fromisoformat(str(signoff.get("timestamp") or ""))
        except ValueError:
            reject("review timestamp is invalid or absent")
            continue
        if timestamp.tzinfo is None or timestamp > now:
            reject("review timestamp has no timezone or is in the future")
            continue
        if timestamp.astimezone(timezone.utc).date() < revision_date:
            reject("review predates the current content revision")
            continue
        reviewer_id = str(signoff.get("reviewer_id") or "").strip()
        profile = reviewer_profiles.get(reviewer_id)
        if not isinstance(profile, Mapping):
            reject("reviewer is not in the registered profile context")
            continue
        identity = authorized_reviewer_identity(profile, reviewer_id)
        if identity is None:
            reject("reviewer has no eligible current human-governance authorization")
            continue
        if identity in seen_identities:
            reject("reviews share a human identity and are not independent")
            continue
        authorization_date = date.fromisoformat(str(profile["authorization"]["verified_on"]))
        if timestamp.astimezone(timezone.utc).date() < authorization_date:
            reject("review predates reviewer authorization")
            continue
        disease_ids = entity_disease_ids(entity_data, entity_type)
        lineage = disease_lineage if len(disease_ids) == 1 else None
        if not all(reviewer_scope_matches(
            profile.get("sign_off_scope"), entity_type, disease_id, lineage,
        )[0] for disease_id in disease_ids):
            reject("current reviewer scope does not cover every entity disease context")
            continue
        seen_identities.add(identity)
        accepted.append(dict(signoff))
    return accepted
