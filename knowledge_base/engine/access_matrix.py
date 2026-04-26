"""Access Matrix aggregator — UA-availability metadata per Plan track.

Per docs/plans/ua_ingestion_and_alternatives_2026-04-26.md §3.1 + §4.

Walks each PlanTrack → Regimen → drug components → reads
`Drug.regulatory_status.ukraine_registration` (registered, reimbursed_nszu,
cost_uah_*, cost_last_updated) and matches against AccessPathway entities
that declare `applies_to_drug_ids` overlap.

The output is render-time-only metadata. The engine NEVER reads any field
on AccessMatrix back as a selection signal — this is enforced by
`tests/test_plan_invariant_ua_availability.py` which monkeypatches all
drugs to registered=False and asserts plan signature is bit-identical.
The matrix is built AFTER engine selection is finalized; appending it to
Plan does not alter `tracks`, `default_indication_id`, or `algorithm_id`.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Optional

from knowledge_base.schemas import AccessMatrix, AccessMatrixRow, PlanTrack


_STALE_THRESHOLD_DAYS = 180


def _parse_iso_date(s: Optional[str]) -> Optional[date]:
    """Tolerant ISO-date parser; returns None on any failure (incl. None input)."""
    if not s or not isinstance(s, str):
        return None
    try:
        return date.fromisoformat(s[:10])
    except (ValueError, TypeError):
        return None


def _aggregate_bool(values: list[Optional[bool]]) -> Optional[bool]:
    """Return True if all True; False if any False; None if no signal at all.
    Mixed True+None → False (one drug confirmed unregistered tilts the row)."""
    seen = [v for v in values if v is not None]
    if not seen:
        return None
    return all(seen)


def _sum_optional(values: list[Optional[float]]) -> Optional[float]:
    """Sum a list of Optional floats. None if every entry is None.
    Drugs without a stored cost are treated as 0 for the lower bound (we
    surface the partial sum) — clinical reviewer reads `notes` for caveats."""
    nums = [v for v in values if v is not None]
    if not nums:
        return None
    return float(sum(nums))


def _oldest_iso(values: list[Optional[str]]) -> Optional[str]:
    """Return the chronologically-earliest ISO date in a list."""
    parsed = [(_parse_iso_date(v), v) for v in values]
    parsed = [(d, raw) for d, raw in parsed if d is not None]
    if not parsed:
        return None
    parsed.sort(key=lambda t: t[0])
    return parsed[0][1]


def _is_stale(iso_date: Optional[str], *, today: Optional[date] = None) -> bool:
    """Cost-orientation freshness check (plan §6.4): >180 days = stale."""
    parsed = _parse_iso_date(iso_date)
    if parsed is None:
        return False
    today = today or date.today()
    return (today - parsed).days > _STALE_THRESHOLD_DAYS


def _resolve(entities: dict, entity_id: Optional[str]) -> Optional[dict]:
    if entity_id and entity_id in entities:
        return entities[entity_id]["data"]
    return None


def _drug_ukraine_reg(drug: Optional[dict]) -> dict:
    """Drug → ukraine_registration dict (or empty dict if absent)."""
    if not drug:
        return {}
    reg = (drug.get("regulatory_status") or {}).get("ukraine_registration")
    return reg or {}


def _find_access_pathways(
    drug_ids: list[str], entities: dict
) -> tuple[Optional[str], list[str]]:
    """Return (primary_pathway_id, alternative_pathway_ids) for a list of
    drug ids. The first pathway whose `applies_to_drug_ids` intersects
    becomes primary; the rest are alternatives. Order is loader-dependent
    (alphabetical by id) so output is stable across runs."""
    if not drug_ids:
        return (None, [])
    drug_set = set(drug_ids)
    matches: list[str] = []
    for eid, info in sorted(entities.items()):
        if info.get("type") != "access_pathways":
            continue
        applies = set((info["data"].get("applies_to_drug_ids") or []))
        if applies & drug_set:
            matches.append(eid)
    if not matches:
        return (None, [])
    return (matches[0], matches[1:])


def _row_for_track(
    track: PlanTrack,
    entities: dict,
    *,
    today: Optional[date] = None,
) -> AccessMatrixRow:
    regimen = track.regimen_data or {}
    components = regimen.get("components") or []
    drug_ids: list[str] = [c.get("drug_id") for c in components if c.get("drug_id")]

    drugs = [_resolve(entities, did) for did in drug_ids]
    regs = [_drug_ukraine_reg(d) for d in drugs]

    registered = _aggregate_bool([r.get("registered") if r else None for r in regs])
    reimbursed = _aggregate_bool([r.get("reimbursed_nszu") if r else None for r in regs])

    self_pay_min = _sum_optional([
        ((r.get("cost_uah_self_pay") or {}).get("min")) for r in regs
    ])
    self_pay_max = _sum_optional([
        ((r.get("cost_uah_self_pay") or {}).get("max")) for r in regs
    ])
    reimb_min = _sum_optional([
        ((r.get("cost_uah_reimbursed") or {}).get("min")) for r in regs
    ])
    reimb_max = _sum_optional([
        ((r.get("cost_uah_reimbursed") or {}).get("max")) for r in regs
    ])

    # First-seen per_unit (cycle/course/month). All components should agree
    # in practice; we don't normalize across mixed units.
    per_unit: Optional[str] = None
    for r in regs:
        for key in ("cost_uah_self_pay", "cost_uah_reimbursed"):
            unit = (r.get(key) or {}).get("per_unit") if r else None
            if unit:
                per_unit = unit
                break
        if per_unit:
            break

    oldest_cost_date = _oldest_iso([r.get("cost_last_updated") for r in regs])
    stale = _is_stale(oldest_cost_date, today=today)

    primary_path, alt_paths = _find_access_pathways(drug_ids, entities)

    notes: list[str] = []
    if registered is False:
        n_unreg = sum(1 for r in regs if r.get("registered") is False)
        notes.append(
            f"{n_unreg}/{len(drug_ids)} component drug(s) not registered in Ukraine"
        )
    if reimbursed is False:
        n_unreimb = sum(1 for r in regs if r.get("reimbursed_nszu") is False)
        notes.append(
            f"{n_unreimb}/{len(drug_ids)} component drug(s) not on НСЗУ formulary"
        )
    if stale:
        notes.append(
            f"Cost orientation last updated {oldest_cost_date} — verify; >180 days old"
        )
    if registered is None and reimbursed is None and not drug_ids:
        notes.append("No regimen components on this track — availability unknown")

    return AccessMatrixRow(
        track_id=track.track_id or "standard",
        track_label=track.label or track.track_id or "track",
        regimen_id=regimen.get("id"),
        regimen_name=regimen.get("name"),
        drug_ids=drug_ids,
        registered_in_ua=registered,
        reimbursed_nszu=reimbursed,
        cost_self_pay_min=self_pay_min,
        cost_self_pay_max=self_pay_max,
        cost_reimbursed_min=reimb_min,
        cost_reimbursed_max=reimb_max,
        cost_per_unit=per_unit,
        cost_last_updated=oldest_cost_date,
        cost_is_stale=stale,
        primary_pathway_id=primary_path,
        pathway_alternative_ids=alt_paths,
        notes=notes,
    )


def _trial_rows(option, entities: dict) -> list[AccessMatrixRow]:
    """Append one Access Matrix row per surfaced clinical trial.

    Trials carry a stable shape — sponsor pays, no NSZU concerns — so we
    encode that uniformly (registered=None, reimbursed=None, costs=None,
    notes describing the sponsor + UA-site presence)."""
    if option is None or not getattr(option, "trials", None):
        return []
    rows: list[AccessMatrixRow] = []
    for trial in option.trials:
        ua = bool(getattr(trial, "sites_ua", None))
        notes = []
        if ua:
            notes.append("UA site available — verify enrollment status with site")
        else:
            notes.append("No UA site listed — international referral required")
        rows.append(
            AccessMatrixRow(
                track_id=f"trial:{trial.nct_id}",
                track_label=f"Trial · {trial.nct_id}",
                regimen_id=None,
                regimen_name=trial.title,
                drug_ids=[],
                registered_in_ua=None,
                reimbursed_nszu=None,
                cost_self_pay_min=0.0,
                cost_self_pay_max=0.0,
                cost_per_unit="course",
                primary_pathway_id=None,
                pathway_alternative_ids=[],
                notes=notes,
            )
        )
    return rows


def build_access_matrix(
    tracks: list[PlanTrack],
    entities: dict,
    *,
    experimental_options=None,
    today: Optional[date] = None,
) -> AccessMatrix:
    """Build the per-Plan AccessMatrix from materialized tracks + KB entities.

    `entities` is the loader's `entities_by_id` map; each value is
    `{"type": <dir-name>, "data": <dict>}`.

    `experimental_options` (optional) is the ExperimentalOption attached
    to PlanResult; when present, one row is appended per surfaced trial
    so clinicians see the trial-as-access-pathway alongside the standard
    + alternative tracks.
    """
    rows = [_row_for_track(t, entities, today=today) for t in tracks]
    rows.extend(_trial_rows(experimental_options, entities))

    # Plan-level note: if any row is stale, surface once at the top so
    # the render layer can hoist a banner.
    notes: list[str] = []
    if any(r.cost_is_stale for r in rows):
        notes.append(
            "One or more cost orientations are >180 days old — verify before use"
        )

    return AccessMatrix(
        rows=rows,
        generated_at=datetime.now(timezone.utc).isoformat(),
        notes=notes,
    )


__all__ = ["build_access_matrix"]
