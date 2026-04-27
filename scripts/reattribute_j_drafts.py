"""Phase 5+ — re-attribute J-agent BMA drafts from primary_sources.

Context (CIViC pivot, 2026-04-27):

- Phase 1.5 migrated legacy ``oncokb_level: <N>`` claims into structured
  ``evidence_sources: [{source: SRC-ONCOKB, level: <N>, ...}]`` entries.
- Phase 3-N attached CIViC therapeutic-option evidence where available.
- Phase 3-O audit (`docs/reviews/bma-j-drafts-civic-diff-2026-04-27.md`)
  found 18 of 23 J-agent BMA drafts where CIViC has no actionable
  evidence (IHC/methylation/composite biomarkers). These BMAs still
  carry only the legacy ``SRC-ONCOKB`` evidence-sources entry, which
  the render layer skips per OncoKB ToS. Effectively they are
  uncited.

This script processes those 18 BMAs (filter: ``drafted_by:
claude_extraction`` AND ``evidence_sources`` contains only
``SRC-ONCOKB``):

1. Drop the legacy ``SRC-ONCOKB`` ``evidence_sources`` entry.
2. For each non-OncoKB tier-1 source already cited in
   ``primary_sources``, build a citation-only ``evidence_sources``
   entry with ``level: "pending-extraction"`` (sentinel — schema
   requires a string, but we explicitly do NOT invent the source's
   level call here; clinical co-lead extracts it during the
   actionability-review pass).
3. If post-promotion the BMA has fewer than 2 ``evidence_sources``
   entries (e.g. only one primary_source, and it's a stub), set
   ``blocked_on_source_ingestion: [<stub-source-ids>]`` so a clinical
   co-lead can prioritise ingestion of those sources.
4. Mark ``actionability_review_required: true``.

Idempotent: re-runs are safe. Won't double-promote or re-add a
SRC-ONCOKB entry.

Usage:

    # Inspect plan, no writes
    python scripts/reattribute_j_drafts.py --dry-run

    # Apply
    python scripts/reattribute_j_drafts.py
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml as _safe_yaml
from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent
BMA_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarker_actionability"
SOURCES_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"

# OncoKB legacy tag — render skips it; we drop it on re-attribution.
LEGACY_ONCOKB_SRC = "SRC-ONCOKB"

# Sentinel for promoted entries: schema requires `level: str`, but we
# refuse to invent a per-source level token when we haven't actually
# extracted it from the source. Clinical co-lead replaces this during
# actionability review.
PENDING_LEVEL_SENTINEL = "pending-extraction"

PROMOTION_NOTE = (
    "Auto-promoted from primary_sources by Phase 5+ re-attribution; "
    "clinical review for evidence-level extraction pending."
)


# ─── Stub detection ───────────────────────────────────────────────────────


def _load_sources_index() -> dict[str, dict]:
    """Return {SRC-id: raw_dict} for every Source YAML."""
    out: dict[str, dict] = {}
    for p in SOURCES_DIR.rglob("*.yaml"):
        try:
            data = _safe_yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if isinstance(data, dict) and isinstance(data.get("id"), str):
            out[data["id"]] = data
    return out


def _is_stub_source(src_id: str, idx: dict[str, dict]) -> bool:
    """Heuristic: a Source is a 'stub' if it's auto-drafted and not
    yet ingested. Used to flag BMAs that fall below ≥2 real cites
    after re-attribution.
    """
    if src_id not in idx:
        # Missing source FK = treat as stub (broken citation).
        return True
    d = idx[src_id]
    title = str(d.get("title") or "").lower()
    notes = str(d.get("notes") or "").lower()
    legal_notes = str((d.get("legal_review") or {}).get("notes") or "").lower()
    ingestion_method = ((d.get("ingestion") or {}).get("method")) or ""
    if "auto-stub" in notes or "auto-stub" in legal_notes:
        return True
    if ingestion_method == "none" and "todo" in title:
        return True
    return False


# ─── BMA classification ───────────────────────────────────────────────────


def _is_j_draft(raw: dict) -> bool:
    return raw.get("drafted_by") == "claude_extraction"


def _is_target(raw: dict) -> bool:
    """A J-draft is a Phase-5+ re-attribution target iff its current
    ``evidence_sources`` contains *only* the legacy SRC-ONCOKB entry
    (i.e. CIViC didn't add anything in Phase 3-N). The 5 J-drafts that
    Phase 3-N enriched (BRAF/JAK2 cluster) are skipped.
    """
    if not _is_j_draft(raw):
        return False
    es = raw.get("evidence_sources") or []
    if not es:
        # Phase-1.5 didn't run on this draft; out of scope here.
        return False
    sources = {(e or {}).get("source") for e in es}
    return sources == {LEGACY_ONCOKB_SRC}


# ─── Plan & apply per-file ────────────────────────────────────────────────


@dataclass
class Outcome:
    bma_id: str
    path: Path
    biomarker_id: str
    disease_id: str
    before_count: int
    after_count: int
    promoted_sources: list[str]
    skipped_sources: list[str]  # e.g. SRC-ONCOKB (always dropped) or non-tier-1
    blocked_on: list[str]
    note: str = ""


# Tier-1 source-id prefixes we will auto-promote. Anything else (e.g.
# trial Source IDs like SRC-COMFORT-I-VERSTOVSEK-2012) is also tier-1
# evidence and gets promoted — the rule is just "anything in
# primary_sources except SRC-ONCOKB". Keeping the set explicit so a
# future extension can tighten it without touching the loop.
_PROMOTABLE_PREFIXES = ("SRC-",)


def _is_promotable(src_id: str) -> bool:
    if not isinstance(src_id, str):
        return False
    if not src_id.startswith(_PROMOTABLE_PREFIXES):
        return False
    if src_id == LEGACY_ONCOKB_SRC:
        return False
    return True


def _plan_one(raw: dict, sources_idx: dict[str, dict], path: Path) -> Outcome:
    bma_id = raw.get("id", path.stem)
    primary = list(raw.get("primary_sources") or [])
    es = list(raw.get("evidence_sources") or [])
    before = len(es)

    # Existing non-OncoKB evidence_sources we'd keep (idempotency: avoid
    # double-promote on re-runs).
    existing_kept = [e for e in es if (e or {}).get("source") != LEGACY_ONCOKB_SRC]
    existing_kept_ids = {(e or {}).get("source") for e in existing_kept}

    # Determine promotion candidates from primary_sources, in stable order.
    promoted_ids: list[str] = []
    skipped: list[str] = []
    for sid in primary:
        if sid == LEGACY_ONCOKB_SRC:
            skipped.append(sid)
            continue
        if not _is_promotable(sid):
            skipped.append(sid)
            continue
        if sid in existing_kept_ids:
            # Already promoted on a prior run — keep, don't duplicate.
            continue
        promoted_ids.append(sid)

    after_es = list(existing_kept)
    for sid in promoted_ids:
        after_es.append(
            {
                "source": sid,
                "level": PENDING_LEVEL_SENTINEL,
                "evidence_ids": [],
                "direction": None,
                "significance": None,
                "note": PROMOTION_NOTE,
            }
        )

    # Compute blocked-on flag: stubs amongst the after-set (or zero non-stubs).
    blocked_on: list[str] = []
    if len(after_es) < 2:
        # Mark all stubs (including missing-FK) and any single-source case.
        for entry in after_es:
            sid = entry.get("source")
            if sid and _is_stub_source(sid, sources_idx):
                blocked_on.append(sid)
        # Also include any primary_sources that are stubs and absent from after_es.
        for sid in primary:
            if sid == LEGACY_ONCOKB_SRC or not _is_promotable(sid):
                continue
            if sid in {e.get("source") for e in after_es}:
                continue
            if _is_stub_source(sid, sources_idx):
                blocked_on.append(sid)
        # Dedup, preserve order.
        seen = set()
        blocked_on = [x for x in blocked_on if not (x in seen or seen.add(x))]
        # Fallback: if we still flag <2 with no stubs identified, list
        # ALL primary_sources except SRC-ONCOKB as candidates needing
        # follow-up — clinical co-lead picks.
        if len(after_es) < 2 and not blocked_on:
            for sid in primary:
                if sid == LEGACY_ONCOKB_SRC or not _is_promotable(sid):
                    continue
                blocked_on.append(sid)
            seen = set()
            blocked_on = [x for x in blocked_on if not (x in seen or seen.add(x))]

    return Outcome(
        bma_id=bma_id,
        path=path,
        biomarker_id=str(raw.get("biomarker_id", "")),
        disease_id=str(raw.get("disease_id", "")),
        before_count=before,
        after_count=len(after_es),
        promoted_sources=promoted_ids,
        skipped_sources=skipped,
        blocked_on=blocked_on,
    )


def _apply_one(raw: dict, outcome: Outcome) -> dict:
    """Apply the planned changes to ``raw`` in-place and return it."""
    # Rebuild evidence_sources from the planned set.
    es_existing_kept = [
        e for e in (raw.get("evidence_sources") or [])
        if (e or {}).get("source") != LEGACY_ONCOKB_SRC
    ]
    new_es = list(es_existing_kept)
    for sid in outcome.promoted_sources:
        new_es.append(
            {
                "source": sid,
                "level": PENDING_LEVEL_SENTINEL,
                "evidence_ids": [],
                "direction": None,
                "significance": None,
                "note": PROMOTION_NOTE,
            }
        )
    raw["evidence_sources"] = new_es
    raw["actionability_review_required"] = True
    if outcome.blocked_on:
        raw["blocked_on_source_ingestion"] = list(outcome.blocked_on)
    return raw


# ─── YAML round-trip helpers ──────────────────────────────────────────────


def _make_yaml() -> YAML:
    y = YAML()
    y.preserve_quotes = True
    y.indent(mapping=2, sequence=4, offset=2)
    y.width = 4096  # keep long string lines unwrapped
    return y


def _load_yaml_rt(path: Path) -> dict:
    yml = _make_yaml()
    with path.open(encoding="utf-8") as f:
        return yml.load(f)


def _dump_yaml_rt(path: Path, data: dict) -> None:
    yml = _make_yaml()
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yml.dump(data, f)


# ─── Main ─────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print plan without writing files.",
    )
    parser.add_argument(
        "--bma-dir",
        type=Path,
        default=BMA_DIR,
        help="Override BMA directory (default: knowledge_base/hosted/content/biomarker_actionability).",
    )
    args = parser.parse_args(argv)

    sources_idx = _load_sources_index()

    target_paths: list[Path] = []
    for path in sorted(args.bma_dir.glob("bma_*.yaml")):
        # Cheap pre-filter using safe_yaml; round-trip read is heavier.
        try:
            raw_lite = _safe_yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            print(f"WARN: failed to parse {path.name}: {exc}", file=sys.stderr)
            continue
        if not isinstance(raw_lite, dict):
            continue
        if not _is_j_draft(raw_lite):
            continue
        if not _is_target(raw_lite):
            # Either a non-J-draft, or a J-draft with CIViC enrichment.
            continue
        target_paths.append(path)

    print(f"# J-draft re-attribution — {len(target_paths)} target file(s)")
    print()
    outcomes: list[Outcome] = []
    for path in target_paths:
        raw_rt = _load_yaml_rt(path)
        outcome = _plan_one(raw_rt, sources_idx, path)
        outcomes.append((outcome, raw_rt))

    # Print the plan table.
    print(
        f"{'BMA':<40} {'before':>6} {'after':>5} {'promoted':>9} {'blocked?':>9}"
    )
    for outcome, _ in outcomes:
        flag = "yes" if outcome.blocked_on else ""
        print(
            f"{outcome.bma_id:<40} {outcome.before_count:>6} "
            f"{outcome.after_count:>5} {len(outcome.promoted_sources):>9} {flag:>9}"
        )
    print()
    n_promoted_total = sum(1 for o, _ in outcomes if o.promoted_sources)
    n_blocked_total = sum(1 for o, _ in outcomes if o.blocked_on)
    print(
        f"# Summary: targets={len(outcomes)} files-with-promotions={n_promoted_total} "
        f"still-blocked={n_blocked_total}"
    )

    if args.dry_run:
        print()
        print("# Dry-run: no files written.")
        return 0

    # Apply.
    n_written = 0
    for outcome, raw_rt in outcomes:
        if not outcome.promoted_sources and not outcome.blocked_on:
            # Nothing to change (already re-attributed on a prior run AND
            # no new blocked-on flag needed).
            es_now = raw_rt.get("evidence_sources") or []
            if any((e or {}).get("source") == LEGACY_ONCOKB_SRC for e in es_now):
                # Still has legacy SRC-ONCOKB → write.
                pass
            else:
                continue
        _apply_one(raw_rt, outcome)
        _dump_yaml_rt(outcome.path, raw_rt)
        n_written += 1

    print(f"# Wrote {n_written} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
