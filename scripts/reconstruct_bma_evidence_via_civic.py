"""Phase 3-N — BMA evidence reconstruction via CIViC snapshot.

Walks every ``bma_*.yaml`` whose biomarker carries an ``actionability_lookup``
block, queries the local CIViC snapshot via ``SnapshotCIViCClient``, and
appends one ``evidence_sources`` entry per (level, direction, significance)
bucket to the BMA. Legacy ``SRC-ONCOKB`` entries are preserved verbatim
(Phase 4 render layer skips them per OncoKB ToS audit).

USAGE
    python scripts/reconstruct_bma_evidence_via_civic.py [--dry-run]

DESIGN NOTES
- Idempotent: re-running over a BMA that already has a SRC-CIVIC entry with
  the same (level, direction, significance) bucket will not duplicate it.
- Disease-agnostic: the BMA's disease_id is *not* used to filter CIViC
  entries. Rationale: CIViC's "disease" field is an OncoTree-ish free text
  string, our disease_ids are DIS-* slugs; mapping is non-trivial. The
  Phase 4 render layer is responsible for surfacing-time filtering. We
  intentionally over-include here so the human review surface in the
  generated report can flag pan-tumor vs. tumor-specific evidence.
- ``evidence_ids`` extraction: the snapshot exposes each item's ``id``
  (the CIViC evidence_item id, e.g. "1234"). We collect the IDs of every
  CIViC entry that contributed to a given (level, direction, significance)
  bucket. PMIDs are NOT included here — they live on the Source entity
  level via SRC-CIVIC, and adding them would duplicate provenance already
  captured in the snapshot.
- Defensive fail-open: a BMA whose ``evidence_sources`` is malformed
  (not a list, or items not dicts) is logged and skipped — never written.

ALLOWLIST: writes only to
  knowledge_base/hosted/content/biomarker_actionability/bma_*.yaml
  docs/reviews/bma-civic-rebuild-2026-04-27.md
"""

from __future__ import annotations

import argparse
import logging
import sys
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import yaml

# Make `python scripts/...` style invocation work — make repo root importable.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from knowledge_base.engine.actionability_types import (  # noqa: E402
    ActionabilityError,
    ActionabilityQuery,
    ActionabilityResult,
)
from knowledge_base.engine.civic_evidence_lanes import (  # noqa: E402
    classify_civic_evidence_item,
    classify_civic_evidence_source_ref,
    standard_care_confirming_source_ids,
    summarize_lanes,
)
from knowledge_base.engine.civic_disease_matcher import (  # noqa: E402
    civic_entry_matches_disease,
)
from knowledge_base.engine.civic_variant_matcher import (  # noqa: E402
    matches_civic_entry,
)
from knowledge_base.engine.snapshot_civic_client import (  # noqa: E402
    SnapshotCIViCClient,
)

_LOG = logging.getLogger("reconstruct_bma_evidence_via_civic")

CIVIC_SNAPSHOT_PATH = (
    _REPO_ROOT / "knowledge_base" / "hosted" / "civic" / "2026-04-25" / "evidence.yaml"
)
BIO_DIR = _REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarkers"
BMA_DIR = _REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarker_actionability"
DISEASE_DIR = _REPO_ROOT / "knowledge_base" / "hosted" / "content" / "diseases"
REPORT_PATH = _REPO_ROOT / "docs" / "reviews" / "bma-civic-rebuild-2026-04-27.md"
SOURCE_TOKEN = "SRC-CIVIC"
NOTE_PREFIX = "Auto-added Phase 3-N from CIViC snapshot 2026-04-25"


# ── Data containers for the report ───────────────────────────────────────


@dataclass
class BMAOutcome:
    bma_id: str
    biomarker_id: str
    gene: Optional[str]
    variant: Optional[str]
    disease_id: str
    skip_reason: Optional[str]  # populated when no write was made
    civic_entries_added: int  # entries added IN THIS RUN
    civic_entries_total: int  # entries currently on the BMA (post-write)
    civic_levels_present: tuple[str, ...]  # levels currently on the BMA
    has_resistance: bool  # any CIViC bucket on this BMA is resistance
    legacy_oncokb_level: Optional[str]
    review_required: bool
    file_modified: bool  # this run wrote this file
    lanes_present: tuple[str, ...] = ()


# ── BIO index ────────────────────────────────────────────────────────────


def build_bio_lookup_index() -> dict[str, tuple[str, str]]:
    """Glob bio_*.yaml; return {BIO-ID: (gene, variant)} for those with
    ``actionability_lookup``. BIOs without lookup are absent from the dict."""
    out: dict[str, tuple[str, str]] = {}
    for path in sorted(BIO_DIR.glob("bio_*.yaml")):
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            _LOG.warning("BIO %s: not a mapping; skipping", path.name)
            continue
        bio_id = data.get("id")
        lookup = data.get("actionability_lookup")
        if bio_id and isinstance(lookup, dict):
            gene = lookup.get("gene")
            variant = lookup.get("variant")
            if gene and variant:
                out[str(bio_id)] = (str(gene), str(variant))
    return out


def build_disease_index() -> dict[str, dict[str, Any]]:
    """Glob disease YAMLs; return {DIS-ID: raw disease data}."""
    out: dict[str, dict[str, Any]] = {}
    for path in sorted(DISEASE_DIR.glob("*.yaml")):
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if isinstance(data, dict) and data.get("id"):
            out[str(data["id"])] = data
    return out


# ── Bucketing helper ─────────────────────────────────────────────────────


def _bucket_key(entry: dict[str, Any]) -> tuple[str, str, str]:
    """A bucket = (evidence_level, evidence_direction, significance). Each
    becomes one ``evidence_sources`` entry on the BMA."""
    level = str(entry.get("evidence_level") or "?")
    direction = str(entry.get("evidence_direction") or "")
    significance = str(entry.get("significance") or "")
    return (level, direction, significance)


def _matched_civic_entries(
    raw_snapshot_items: list[dict[str, Any]],
    gene: str,
    variant: str,
) -> list[dict[str, Any]]:
    """Re-run the matcher locally so we can keep the raw CIViC items (with
    their ``id`` field) instead of just the ActionabilityTherapeuticOption
    aggregate. The client is the source of truth for "did anything match";
    we just need item-level resolution for evidence_ids."""
    out = []
    for entry in raw_snapshot_items:
        if not isinstance(entry, dict):
            continue
        civic_gene = str(entry.get("gene") or "")
        civic_variant = str(entry.get("variant") or "")
        if not civic_gene or not civic_variant:
            continue
        if matches_civic_entry(
            query_gene=gene,
            query_variant=variant,
            civic_gene=civic_gene,
            civic_variant=civic_variant,
        ):
            out.append(entry)
    return out


def _collect_drugs(bucket_entries: list[dict[str, Any]]) -> list[str]:
    drugs: list[str] = []
    seen: set[str] = set()
    for e in bucket_entries:
        for t in e.get("therapies") or []:
            t_str = str(t)
            if t_str and t_str not in seen:
                seen.add(t_str)
                drugs.append(t_str)
    return drugs


def _is_resistance_bucket(direction: str, significance: str) -> bool:
    """CIViC encodes resistance two ways:
        (a) Predictive evidence with direction=Does Not Support &
            significance=Sensitivity/Response  → drug should NOT work
        (b) Predictive evidence with direction=Supports &
            significance=Resistance            → drug confers resistance
    Both are clinically a "resistance" surface."""
    d = (direction or "").strip().lower()
    s = (significance or "").strip().lower()
    if d == "does not support":
        return True
    if "resistance" in s:
        return True
    return False


def _build_evidence_entry(
    bucket_entries: list[dict[str, Any]],
    bucket_key: tuple[str, str, str],
    standard_care_source_ids: tuple[str, ...] = (),
) -> dict[str, Any]:
    level, direction, significance = bucket_key
    ids = [str(e["id"]) for e in bucket_entries if e.get("id") is not None]
    drugs = _collect_drugs(bucket_entries)
    drug_str = ", ".join(drugs) if drugs else "(no therapy attached)"
    lane = classify_civic_evidence_item(
        bucket_entries[0],
        standard_care_confirmed=bool(standard_care_source_ids),
        standard_care_source_ids=standard_care_source_ids,
    ).lane.value
    return {
        "source": SOURCE_TOKEN,
        "level": level,
        "evidence_lane": lane,
        "evidence_ids": ids,
        "direction": direction or None,
        "significance": significance or None,
        "note": f"{NOTE_PREFIX}; therapies: {drug_str}",
    }


def _existing_civic_buckets(
    evidence_sources: list[dict[str, Any]],
) -> set[tuple[str, str, str]]:
    """Dedup key for idempotency."""
    out: set[tuple[str, str, str]] = set()
    for entry in evidence_sources:
        if not isinstance(entry, dict):
            continue
        if entry.get("source") != SOURCE_TOKEN:
            continue
        level = str(entry.get("level") or "?")
        direction = str(entry.get("direction") or "")
        significance = str(entry.get("significance") or "")
        out.add((level, direction, significance))
    return out


def _legacy_oncokb_level(evidence_sources: list[dict[str, Any]]) -> Optional[str]:
    for entry in evidence_sources:
        if isinstance(entry, dict) and entry.get("source") == "SRC-ONCOKB":
            lvl = entry.get("level")
            if lvl is not None:
                return str(lvl)
    return None


# ── YAML round-trip (preserves key order, allows unicode) ────────────────


def _yaml_load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level not a mapping")
    return data


def _yaml_dump(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(
            data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )


# ── Main walk ────────────────────────────────────────────────────────────


def process_bma(
    path: Path,
    bio_lookup: dict[str, tuple[str, str]],
    disease_index: dict[str, dict[str, Any]],
    raw_civic_items: list[dict[str, Any]],
    client: SnapshotCIViCClient,
    dry_run: bool,
) -> BMAOutcome:
    data = _yaml_load(path)
    bma_id = str(data.get("id") or path.stem)
    biomarker_id = str(data.get("biomarker_id") or "")
    disease_id = str(data.get("disease_id") or "")

    evidence_sources_raw = data.get("evidence_sources") or []
    if not isinstance(evidence_sources_raw, list):
        _LOG.warning(
            "BMA %s: evidence_sources is not a list (%s); skipping",
            bma_id,
            type(evidence_sources_raw).__name__,
        )
        return BMAOutcome(
            bma_id=bma_id,
            biomarker_id=biomarker_id,
            gene=None,
            variant=None,
            disease_id=disease_id,
            skip_reason="malformed_evidence_sources",
            civic_entries_added=0,
            civic_entries_total=0,
            civic_levels_present=(),
            has_resistance=False,
            legacy_oncokb_level=None,
            review_required=bool(data.get("actionability_review_required")),
            file_modified=False,
        )
    # Validate items individually too
    cleaned_existing: list[dict[str, Any]] = []
    malformed = False
    for e in evidence_sources_raw:
        if not isinstance(e, dict):
            malformed = True
            break
        cleaned_existing.append(e)
    if malformed:
        _LOG.warning("BMA %s: evidence_sources has non-dict entries; skipping", bma_id)
        return BMAOutcome(
            bma_id=bma_id,
            biomarker_id=biomarker_id,
            gene=None,
            variant=None,
            disease_id=disease_id,
            skip_reason="malformed_evidence_sources",
            civic_entries_added=0,
            civic_entries_total=0,
            civic_levels_present=(),
            has_resistance=False,
            legacy_oncokb_level=None,
            review_required=bool(data.get("actionability_review_required")),
            file_modified=False,
        )

    legacy_lvl = _legacy_oncokb_level(cleaned_existing)
    review_required = bool(data.get("actionability_review_required"))

    def _civic_summary(
        entries: list[dict[str, Any]],
    ) -> tuple[int, tuple[str, ...], bool, tuple[str, ...]]:
        n = 0
        levels: list[str] = []
        any_resistance = False
        lane_decisions = []
        for ent in entries:
            if not isinstance(ent, dict):
                continue
            if ent.get("source") != SOURCE_TOKEN:
                continue
            n += 1
            lvl = str(ent.get("level") or "?")
            levels.append(lvl)
            lane_decisions.append(classify_civic_evidence_source_ref(ent))
            if _is_resistance_bucket(
                str(ent.get("direction") or ""),
                str(ent.get("significance") or ""),
            ):
                any_resistance = True
        return n, tuple(levels), any_resistance, summarize_lanes(lane_decisions)

    lookup = bio_lookup.get(biomarker_id)
    if lookup is None:
        n_total, lvls_present, has_res, lanes_present = _civic_summary(cleaned_existing)
        return BMAOutcome(
            bma_id=bma_id,
            biomarker_id=biomarker_id,
            gene=None,
            variant=None,
            disease_id=disease_id,
            skip_reason="biomarker_not_actionable_for_civic_lookup",
            civic_entries_added=0,
            civic_entries_total=n_total,
            civic_levels_present=lvls_present,
            has_resistance=has_res,
            legacy_oncokb_level=legacy_lvl,
            review_required=review_required,
            file_modified=False,
            lanes_present=lanes_present,
        )
    gene, variant = lookup

    # Run client lookup primarily for the (cached, source_url, etc) result
    # contract; but we work off the raw matched entries to preserve IDs.
    query = ActionabilityQuery(
        gene=gene,
        variant=variant,
        oncotree_code=None,
        source_biomarker_id=biomarker_id,
    )
    result_or_err = client.lookup(query)
    if isinstance(result_or_err, ActionabilityError):
        _LOG.warning(
            "BMA %s: CIViC client error %s — %s",
            bma_id,
            result_or_err.error_kind,
            result_or_err.detail,
        )
        n_total, lvls_present, has_res, lanes_present = _civic_summary(cleaned_existing)
        return BMAOutcome(
            bma_id=bma_id,
            biomarker_id=biomarker_id,
            gene=gene,
            variant=variant,
            disease_id=disease_id,
            skip_reason=f"civic_lookup_error_{result_or_err.error_kind}",
            civic_entries_added=0,
            civic_entries_total=n_total,
            civic_levels_present=lvls_present,
            has_resistance=has_res,
            legacy_oncokb_level=legacy_lvl,
            review_required=review_required,
            file_modified=False,
            lanes_present=lanes_present,
        )

    all_matched = _matched_civic_entries(raw_civic_items, gene, variant)
    if not all_matched:
        n_total, lvls_present, has_res, lanes_present = _civic_summary(cleaned_existing)
        return BMAOutcome(
            bma_id=bma_id,
            biomarker_id=biomarker_id,
            gene=gene,
            variant=variant,
            disease_id=disease_id,
            skip_reason="civic_no_evidence",
            civic_entries_added=0,
            civic_entries_total=n_total,
            civic_levels_present=lvls_present,
            has_resistance=has_res,
            legacy_oncokb_level=legacy_lvl,
            review_required=review_required,
            file_modified=False,
            lanes_present=lanes_present,
        )

    matched = [
        entry
        for entry in all_matched
        if civic_entry_matches_disease(entry, disease_index.get(disease_id))
    ]
    if not matched:
        n_total, lvls_present, has_res, lanes_present = _civic_summary(cleaned_existing)
        return BMAOutcome(
            bma_id=bma_id,
            biomarker_id=biomarker_id,
            gene=gene,
            variant=variant,
            disease_id=disease_id,
            skip_reason="civic_no_disease_matched_evidence",
            civic_entries_added=0,
            civic_entries_total=n_total,
            civic_levels_present=lvls_present,
            has_resistance=has_res,
            legacy_oncokb_level=legacy_lvl,
            review_required=review_required,
            file_modified=False,
            lanes_present=lanes_present,
        )

    # Bucket
    buckets: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for e in matched:
        buckets[_bucket_key(e)].append(e)

    existing = _existing_civic_buckets(cleaned_existing)
    standard_care_source_ids = standard_care_confirming_source_ids(
        cleaned_existing,
        data.get("primary_sources") or (),
    )
    new_entries: list[dict[str, Any]] = []
    for bkey, entries in buckets.items():
        if bkey in existing:
            continue
        new_entries.append(_build_evidence_entry(entries, bkey, standard_care_source_ids))

    if not new_entries:
        n_total, lvls_present, has_res, lanes_present = _civic_summary(cleaned_existing)
        return BMAOutcome(
            bma_id=bma_id,
            biomarker_id=biomarker_id,
            gene=gene,
            variant=variant,
            disease_id=disease_id,
            skip_reason="civic_already_recorded_idempotent",
            civic_entries_added=0,
            civic_entries_total=n_total,
            civic_levels_present=lvls_present,
            has_resistance=has_res,
            legacy_oncokb_level=legacy_lvl,
            review_required=review_required,
            file_modified=False,
            lanes_present=lanes_present,
        )

    # Append, preserve order: legacy first, new CIViC after.
    cleaned_existing.extend(new_entries)
    data["evidence_sources"] = cleaned_existing
    # Always keep review flag on (Phase 4 / clinical signoff lifts it).
    data["actionability_review_required"] = True

    if not dry_run:
        _yaml_dump(path, data)

    n_total, lvls_present, has_res, lanes_present = _civic_summary(cleaned_existing)
    return BMAOutcome(
        bma_id=bma_id,
        biomarker_id=biomarker_id,
        gene=gene,
        variant=variant,
        disease_id=disease_id,
        skip_reason=None,
        civic_entries_added=len(new_entries),
        civic_entries_total=n_total,
        civic_levels_present=lvls_present,
        has_resistance=has_res,
        legacy_oncokb_level=legacy_lvl,
        review_required=True,
        file_modified=not dry_run,
        lanes_present=lanes_present,
    )


# ── Report ───────────────────────────────────────────────────────────────


def _md_escape(s: str) -> str:
    return (s or "").replace("|", "\\|")


def write_report(outcomes: list[BMAOutcome], dry_run: bool) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    total = len(outcomes)
    # "BMA with CIViC" = post-write state has any SRC-CIVIC entry. Stable
    # across re-runs (the per-BMA detail table reflects current YAML state).
    bmas_with_civic = [o for o in outcomes if o.civic_entries_total > 0]
    new_writes = [o for o in outcomes if o.civic_entries_added > 0]
    no_lookup = [
        o for o in outcomes if o.skip_reason == "biomarker_not_actionable_for_civic_lookup"
    ]
    no_civic = [o for o in outcomes if o.skip_reason == "civic_no_evidence"]
    no_disease_match = [
        o for o in outcomes if o.skip_reason == "civic_no_disease_matched_evidence"
    ]
    idempotent = [
        o for o in outcomes if o.skip_reason == "civic_already_recorded_idempotent"
    ]
    malformed = [o for o in outcomes if o.skip_reason == "malformed_evidence_sources"]
    civic_errors = [
        o
        for o in outcomes
        if (o.skip_reason or "").startswith("civic_lookup_error_")
    ]
    resistance_bmas = [o for o in bmas_with_civic if o.has_resistance]

    contradictions: list[BMAOutcome] = []
    for o in bmas_with_civic:
        if o.legacy_oncokb_level is None:
            continue
        # Heuristic: legacy OncoKB Level 1/2 is "high", but CIViC max is D/E.
        if o.legacy_oncokb_level in {"1", "2"}:
            highest_civic = _civic_highest(o.civic_levels_present)
            if highest_civic in {"D", "E"}:
                contradictions.append(o)

    gene_counter: Counter[str] = Counter()
    for o in bmas_with_civic:
        if o.gene:
            gene_counter[o.gene] += 1

    lines: list[str] = []
    mode_str = "DRY-RUN preview" if dry_run else "applied"
    lines.append(f"# BMA evidence reconstruction via CIViC ({mode_str})")
    lines.append("")
    lines.append("Generated by `scripts/reconstruct_bma_evidence_via_civic.py`")
    lines.append(f"Snapshot: `knowledge_base/hosted/civic/2026-04-25/evidence.yaml`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total BMAs scanned: **{total}**")
    lines.append(
        f"- BMAs carrying CIViC evidence (post-write): **{len(bmas_with_civic)}**"
    )
    lines.append(f"- BMAs newly written this run: **{len(new_writes)}**")
    lines.append(
        f"- BMAs unmodified — biomarker has no `actionability_lookup`: "
        f"**{len(no_lookup)}**"
    )
    lines.append(
        f"- BMAs unmodified — biomarker actionable but no CIViC evidence: "
        f"**{len(no_civic)}**"
    )
    lines.append(
        f"- BMAs unmodified - CIViC evidence exists only for another disease: "
        f"**{len(no_disease_match)}**"
    )
    lines.append(
        f"- BMAs unmodified — CIViC evidence already present (idempotent): "
        f"**{len(idempotent)}**"
    )
    lines.append(
        f"- BMAs unmodified — malformed `evidence_sources` (manual fix): "
        f"**{len(malformed)}**"
    )
    lines.append(
        f"- BMAs unmodified — CIViC client error: **{len(civic_errors)}**"
    )
    lines.append(
        f"- BMAs with CIViC resistance evidence (urgent surfacing review): "
        f"**{len(resistance_bmas)}**"
    )
    lines.append("")
    lines.append("## Per-BMA detail (BMAs carrying CIViC evidence)")
    lines.append("")
    lines.append(
        "| BMA-ID | biomarker | (gene, variant) | CIViC entries (total) | "
        "added this run | levels | lanes | resistance | review_required |"
    )
    lines.append(
        "|---|---|---|---|---|---|---|---|---|"
    )
    for o in sorted(bmas_with_civic, key=lambda x: x.bma_id):
        levels = ", ".join(sorted(set(o.civic_levels_present)))
        lanes = ", ".join(o.lanes_present)
        lines.append(
            f"| {_md_escape(o.bma_id)} | {_md_escape(o.biomarker_id)} | "
            f"({_md_escape(o.gene or '')}, {_md_escape(o.variant or '')}) | "
            f"{o.civic_entries_total} | {o.civic_entries_added} | {levels} | "
            f"{_md_escape(lanes)} | "
            f"{'yes' if o.has_resistance else 'no'} | "
            f"{'yes' if o.review_required else 'no'} |"
        )
    lines.append("")

    lines.append("## Contradictions: legacy SRC-ONCOKB vs CIViC")
    lines.append("")
    lines.append(
        "BMAs whose legacy OncoKB level was 1 or 2, but the CIViC snapshot "
        "carries only Level D/E for the same (gene, variant). These warrant "
        "clinical review — the high-confidence label was OncoKB-derived and "
        "may not be defensible in the CIViC-only render."
    )
    lines.append("")
    if contradictions:
        lines.append(
            "| BMA-ID | biomarker | (gene, variant) | legacy SRC-ONCOKB | "
            "highest CIViC | levels present |"
        )
        lines.append("|---|---|---|---|---|---|")
        for o in sorted(
            contradictions,
            key=lambda x: (x.legacy_oncokb_level or "", x.bma_id),
        ):
            highest = _civic_highest(o.civic_levels_present)
            levels = ", ".join(sorted(set(o.civic_levels_present)))
            lines.append(
                f"| {_md_escape(o.bma_id)} | {_md_escape(o.biomarker_id)} | "
                f"({_md_escape(o.gene or '')}, {_md_escape(o.variant or '')}) | "
                f"{_md_escape(o.legacy_oncokb_level or '')} | {highest} | "
                f"{levels} |"
            )
    else:
        lines.append("_None detected._")
    lines.append("")

    lines.append("## CIViC resistance — `Does Not Support` / `significance=Resistance`")
    lines.append("")
    lines.append(
        "BMAs where CIViC carries resistance evidence. These are the urgent "
        "surfacing decisions for the Phase 4 render: a drug suggested by "
        "the regimen track may be contradicted by CIViC for this exact "
        "(biomarker, variant)."
    )
    lines.append("")
    if resistance_bmas:
        lines.append(
            "| BMA-ID | biomarker | (gene, variant) | levels present |"
        )
        lines.append("|---|---|---|---|")
        for o in sorted(resistance_bmas, key=lambda x: x.bma_id):
            levels = ", ".join(sorted(set(o.civic_levels_present)))
            lines.append(
                f"| {_md_escape(o.bma_id)} | {_md_escape(o.biomarker_id)} | "
                f"({_md_escape(o.gene or '')}, {_md_escape(o.variant or '')}) | "
                f"{levels} |"
            )
    else:
        lines.append("_No resistance evidence surfaced for any BMA with CIViC._")
    lines.append("")

    lines.append("## Coverage by gene (BMAs carrying CIViC evidence)")
    lines.append("")
    lines.append("| gene | BMAs modified |")
    lines.append("|---|---|")
    for gene, n in sorted(gene_counter.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"| {gene} | {n} |")
    lines.append("")

    lines.append("## Skips by reason")
    lines.append("")
    skip_counter: Counter[str] = Counter()
    for o in outcomes:
        if o.skip_reason:
            skip_counter[o.skip_reason] += 1
    if skip_counter:
        lines.append("| reason | count |")
        lines.append("|---|---|")
        for reason, n in sorted(skip_counter.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"| {reason} | {n} |")
    else:
        lines.append("_No skips._")
    lines.append("")

    lines.append("## TODO / clinical-signoff blockers")
    lines.append("")
    lines.append(
        "- Every modified BMA carries `actionability_review_required: true`. "
        "Clinical co-leads must validate the CIViC-derived levels and the "
        "(gene, variant)→disease applicability (CIViC entries are not pre-"
        "filtered by disease in this script — see DESIGN NOTES)."
    )
    lines.append(
        "- Contradictions table above is the priority queue for the next "
        "two-reviewer pass."
    )
    lines.append(
        "- CIViC `evidence_ids` reference snapshot 2026-04-25; the next "
        "monthly refresh CI may flip levels — re-run this script after "
        "every snapshot update."
    )
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


_CIVIC_LEVEL_RANK = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}


def _civic_highest(levels: Iterable[str]) -> str:
    items = [lvl for lvl in levels if lvl in _CIVIC_LEVEL_RANK]
    if not items:
        return "?"
    return min(items, key=lambda x: _CIVIC_LEVEL_RANK[x])


# ── Entrypoint ───────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute changes and write the report; do NOT modify BMAs.",
    )
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    if not CIVIC_SNAPSHOT_PATH.exists():
        _LOG.error("CIViC snapshot not found at %s — STOP", CIVIC_SNAPSHOT_PATH)
        return 2

    _LOG.info("Building BIO actionability_lookup index…")
    bio_lookup = build_bio_lookup_index()
    _LOG.info("Building Disease index...")
    disease_index = build_disease_index()
    _LOG.info("  -> %d diseases", len(disease_index))
    _LOG.info("  → %d BIOs with actionability_lookup", len(bio_lookup))

    _LOG.info("Loading raw CIViC snapshot for ID-level resolution…")
    with CIVIC_SNAPSHOT_PATH.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    raw_items = raw.get("evidence_items") or []
    if not isinstance(raw_items, list):
        _LOG.error("CIViC snapshot 'evidence_items' not a list — STOP")
        return 2
    _LOG.info("  → %d raw evidence items", len(raw_items))

    _LOG.info("Initializing SnapshotCIViCClient…")
    client = SnapshotCIViCClient(CIVIC_SNAPSHOT_PATH)

    _LOG.info("Walking BMAs in %s…", BMA_DIR)
    bma_paths = sorted(BMA_DIR.glob("bma_*.yaml"))
    outcomes: list[BMAOutcome] = []
    for path in bma_paths:
        try:
            outcomes.append(
                process_bma(
                    path,
                    bio_lookup,
                    disease_index,
                    raw_items,
                    client,
                    args.dry_run,
                )
            )
        except Exception as exc:
            _LOG.exception("BMA %s: unexpected error — %s", path.name, exc)
            outcomes.append(
                BMAOutcome(
                    bma_id=path.stem,
                    biomarker_id="",
                    gene=None,
                    variant=None,
                    disease_id="",
                    skip_reason=f"unexpected_error_{type(exc).__name__}",
                    civic_entries_added=0,
                    civic_entries_total=0,
                    civic_levels_present=(),
                    has_resistance=False,
                    legacy_oncokb_level=None,
                    review_required=False,
                    file_modified=False,
                )
            )

    write_report(outcomes, args.dry_run)

    modified = sum(1 for o in outcomes if o.civic_entries_added > 0)
    _LOG.info("Done. %d/%d BMAs modified%s.", modified, len(outcomes),
              " (dry-run)" if args.dry_run else "")
    _LOG.info("Report written to %s", REPORT_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
