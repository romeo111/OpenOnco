"""Extract claim-bearing text fields from KB entities.

Used by `scripts/audit_claim_grounding.py` (Q4 + Q5 of
`docs/plans/kb_data_quality_plan_2026-04-29.md`).

A "claim-bearing field" is a free-text field on a KB entity that asserts
clinical fact — outcomes, mechanism, comparative efficacy, line-of-therapy
rationale, etc. Each such field should be backed by ≥1 cited source.
This module walks an already-loaded KB (LoadResult-style dict) and yields
one `ExtractedClaim` per (entity, claim-bearing field) pair.

Field map (chosen after reading schemas/indication.py, schemas/regimen.py,
schemas/biomarker_actionability.py):

  Indication
    - rationale          (free-text rationale paragraph)
    - notes              (clinical notes)
    - expected_outcomes  (structured object — stringified by joining
                          non-null subfields; the `notes` subfield is
                          included if present)
  Regimen
    - notes              (clinical notes)
    - notes_ua           (Ukrainian translation — same claim, separate
                          extraction so contributors can see the UA-side
                          grounding state independently)
  BiomarkerActionability
    - evidence_summary   (1-3 sentence clinical interpretation)
    - notes              (clinical notes)

The brief (slice 3 spec) lists `evidence_summary` and `recommendation_rationale`
on Indication. Those names don't exist on the schema — see commit notes —
so we map them to the actual schema fields `rationale` and `notes`. The
schema for `expected_outcomes` is structured; we stringify it so the
grounding check has prose to score.

`cited_sources` is the union of source IDs mentioned anywhere on the
entity (top-level `sources`/`primary_sources`/`supporting_sources`,
nested Citation.source_id, dose_adjustments[].source_refs, and
evidence_sources[].source). A field's claim is "anchored" iff that
union is non-empty AND ≥1 of the cited IDs resolves to a Source entity
in the KB. Field-local citation precision (which specific source backs
which specific sentence) is out of scope for this layer — that's PR4
work — but a fully detached claim (no SRC-* anywhere on the entity)
is what we flag here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


# Entities we extract claims from, and how their claim-bearing fields
# are stringified. Order matters only for stable report output.
CLAIM_BEARING_ENTITIES: tuple[str, ...] = (
    "indications",
    "regimens",
    "biomarker_actionability",
)


@dataclass
class ExtractedClaim:
    """One claim-bearing field on one entity, plus its citation context."""

    entity_type: str          # "indications" | "regimens" | "biomarker_actionability"
    entity_id: str            # IND-FOO-123 / REG-BAR / BMA-BAZ
    entity_path: str          # repo-relative POSIX path to source YAML
    field: str                # "expected_outcomes" | "notes" | "evidence_summary" | ...
    text: str                 # the claim-bearing prose (stringified)
    cited_sources: list[str] = field(default_factory=list)
    has_anchor: bool = False  # cited_sources non-empty AND ≥1 resolves


# ---------- Source ID collection ----------

def _walk_source_ids(value: Any, out: set[str]) -> None:
    """Recursively collect SRC-* strings from any nested structure.

    Picks up:
      - bare strings starting with "SRC-"
      - Citation dicts with a `source_id` key
      - dose_adjustments[].source_refs
      - evidence_sources[].source
      - any list/dict containing the above
    """
    if value is None:
        return
    if isinstance(value, str):
        if value.startswith("SRC-"):
            out.add(value)
        return
    if isinstance(value, list):
        for v in value:
            _walk_source_ids(v, out)
        return
    if isinstance(value, dict):
        # Common citation patterns
        for key in ("source_id", "source"):
            v = value.get(key)
            if isinstance(v, str) and v.startswith("SRC-"):
                out.add(v)
        for key in ("source_refs", "sources", "primary_sources",
                   "supporting_sources"):
            v = value.get(key)
            if isinstance(v, list):
                _walk_source_ids(v, out)
        # Recurse into nested values that aren't already handled, so
        # we catch SRC-* IDs nested inside e.g. known_controversies →
        # positions[].sources, or evidence_sources[].source.
        for v in value.values():
            if isinstance(v, (list, dict)):
                _walk_source_ids(v, out)


def _collect_cited_sources(entity_data: dict) -> list[str]:
    """All SRC-* IDs cited anywhere on the entity, sorted+deduped."""
    out: set[str] = set()
    _walk_source_ids(entity_data, out)
    return sorted(out)


# ---------- Per-entity-type field extraction ----------

def _stringify_expected_outcomes(eo: Any) -> str:
    """Turn ExpectedOutcomes (struct) into a single prose blob.

    Joins non-null subfield values with field labels so the resulting
    text reads like a coherent claim ("ORR ~70%; PFS median 7 mo;
    notes: OlympiAD"). Empty if no subfields populated.
    """
    if not isinstance(eo, dict):
        return ""
    parts: list[str] = []
    # Stable order for cache-key stability.
    for k in sorted(eo.keys()):
        v = eo.get(k)
        if v is None or v == "":
            continue
        if isinstance(v, (list, dict)):
            # Defensive: skip unexpected nested shapes.
            continue
        parts.append(f"{k}: {v}")
    return "; ".join(parts)


def _coerce_text(value: Any) -> str:
    """Best-effort conversion of YAML scalar/list to a prose string."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(_coerce_text(v) for v in value if v).strip()
    if isinstance(value, dict):
        return _stringify_expected_outcomes(value)
    return str(value).strip()


def _extract_indication_fields(data: dict) -> Iterable[tuple[str, str]]:
    """Yield (field_name, text) for each claim-bearing field on an Indication."""
    for fname in ("rationale", "notes"):
        text = _coerce_text(data.get(fname))
        if text:
            yield fname, text
    eo_text = _stringify_expected_outcomes(data.get("expected_outcomes"))
    if eo_text:
        yield "expected_outcomes", eo_text


def _extract_regimen_fields(data: dict) -> Iterable[tuple[str, str]]:
    for fname in ("notes", "notes_ua"):
        text = _coerce_text(data.get(fname))
        if text:
            yield fname, text


def _extract_bma_fields(data: dict) -> Iterable[tuple[str, str]]:
    for fname in ("evidence_summary", "notes"):
        text = _coerce_text(data.get(fname))
        if text:
            yield fname, text


_EXTRACTORS = {
    "indications": _extract_indication_fields,
    "regimens": _extract_regimen_fields,
    "biomarker_actionability": _extract_bma_fields,
}


# ---------- Public API ----------

def extract_claims(kb_resolved: dict) -> list[ExtractedClaim]:
    """Walk a loaded KB and produce one ExtractedClaim per claim-bearing field.

    Parameters
    ----------
    kb_resolved
        Either a `LoadResult` instance (has `entities_by_id` attribute)
        or its `entities_by_id` dict directly. Each entry is
        ``{"type": <dir name>, "data": <raw YAML dict>, "path": <Path>}``.

    Returns
    -------
    list of ExtractedClaim sorted by (entity_type, entity_id, field).
    """
    entities = _normalize_entities(kb_resolved)

    # Index Source entity IDs so we can compute has_anchor per claim.
    source_ids: set[str] = {
        eid for eid, info in entities.items()
        if info.get("type") == "sources"
    }

    out: list[ExtractedClaim] = []
    for eid, info in entities.items():
        etype = info.get("type")
        if etype not in CLAIM_BEARING_ENTITIES:
            continue
        data = info.get("data") or {}
        path_obj = info.get("path")
        path_str = _path_to_repo_relative(path_obj)

        cited = _collect_cited_sources(data)
        has_anchor = bool(cited) and any(s in source_ids for s in cited)

        extractor = _EXTRACTORS[etype]
        for field_name, text in extractor(data):
            out.append(ExtractedClaim(
                entity_type=etype,
                entity_id=eid,
                entity_path=path_str,
                field=field_name,
                text=text,
                cited_sources=cited,
                has_anchor=has_anchor,
            ))

    out.sort(key=lambda c: (c.entity_type, c.entity_id, c.field))
    return out


def _normalize_entities(kb_resolved: Any) -> dict:
    """Accept either a LoadResult or its `entities_by_id` dict."""
    if hasattr(kb_resolved, "entities_by_id"):
        return kb_resolved.entities_by_id
    if isinstance(kb_resolved, dict):
        # Heuristic: a LoadResult-style dict has values with "type"/"data" keys.
        sample = next(iter(kb_resolved.values()), None)
        if isinstance(sample, dict) and "data" in sample and "type" in sample:
            return kb_resolved
    raise TypeError(
        "extract_claims expects a LoadResult or its entities_by_id dict"
    )


def _path_to_repo_relative(p: Any) -> str:
    """Convert a Path to a repo-relative POSIX-style string when possible."""
    if p is None:
        return ""
    try:
        from pathlib import Path
        path = Path(p)
        # Best-effort: strip everything before knowledge_base/ if present
        parts = path.parts
        for marker in ("knowledge_base",):
            if marker in parts:
                idx = parts.index(marker)
                return "/".join(parts[idx:])
        return path.as_posix()
    except Exception:
        return str(p)


__all__ = ["ExtractedClaim", "extract_claims", "CLAIM_BEARING_ENTITIES"]
