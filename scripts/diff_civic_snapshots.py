"""Diff two CIViC snapshot YAMLs and emit a markdown summary.

Pure-Python (stdlib + pyyaml). No network. Informational — exit code is
always 0.

The CIViC YAML format is produced by `knowledge_base.ingestion.civic_loader`
and contains an `evidence_items` list of dicts keyed by `id` (the CIViC
evidence_id).

Diff buckets:
- ``added``    — evidence_ids in *new* but not *old*
- ``removed``  — evidence_ids in *old* but not *new*
- ``changed``  — evidence_ids in both, but at least one of the watched
                 fields differs: ``evidence_level``, ``evidence_direction``,
                 ``significance``, ``therapies``, ``disease``

The markdown report ranks each bucket by clinical impact:
- evidence_level: A → B → C → D → E (then unknown/None last)
- ⚠️ marker on entries whose direction is "Does Not Support" or whose
  significance is "Resistance" (these are the actionable-vs-not signals
  most likely to flip an engine recommendation)

A "biomarker intersection" section at the top calls out diffs that touch
gene+variant pairs we declare in our 29 ``actionability_lookup`` BIO-*
YAMLs — these are the ones that can directly affect engine output, so
clinicians should review them first.

Usage::

    python scripts/diff_civic_snapshots.py OLD.yaml NEW.yaml [--out diff.md]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

import yaml

# Watched fields — a difference in any of these classifies an item as "changed".
WATCHED_FIELDS = (
    "evidence_level",
    "evidence_direction",
    "significance",
    "therapies",
    "disease",
)

# Level ranking for sorting (lower is more clinically impactful).
_LEVEL_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}


def _level_rank(level: object) -> int:
    if isinstance(level, str) and level.upper() in _LEVEL_ORDER:
        return _LEVEL_ORDER[level.upper()]
    return 99


def _flag(item: dict) -> str:
    direction = (item.get("evidence_direction") or "").strip().lower()
    significance = (item.get("significance") or "").strip().lower()
    if direction == "does not support" or significance == "resistance":
        return "⚠️ "
    return ""


def load_snapshot(path: Path) -> dict[str, dict]:
    """Load a CIViC snapshot YAML and return {evidence_id: item}."""
    with path.open(encoding="utf-8") as f:
        payload = yaml.safe_load(f) or {}
    items = payload.get("evidence_items") or []
    out: dict[str, dict] = {}
    for item in items:
        ev_id = item.get("id")
        if ev_id is None:
            continue
        out[str(ev_id)] = item
    return out


def _therapies_key(item: dict) -> tuple:
    """Stable comparison for therapies (list ordering shouldn't matter)."""
    therapies = item.get("therapies") or []
    if isinstance(therapies, list):
        return tuple(sorted(str(t) for t in therapies))
    return (str(therapies),)


def _equal_on_watched(old: dict, new: dict) -> bool:
    for f in WATCHED_FIELDS:
        if f == "therapies":
            if _therapies_key(old) != _therapies_key(new):
                return False
        else:
            if (old.get(f) or None) != (new.get(f) or None):
                return False
    return True


def diff_snapshots(
    old: dict[str, dict], new: dict[str, dict]
) -> dict[str, list]:
    """Compute added / removed / changed buckets."""
    old_ids = set(old)
    new_ids = set(new)

    added_ids = sorted(new_ids - old_ids, key=lambda i: _safe_int(i))
    removed_ids = sorted(old_ids - new_ids, key=lambda i: _safe_int(i))

    added = [new[i] for i in added_ids]
    removed = [old[i] for i in removed_ids]

    changed: list[dict] = []
    for ev_id in sorted(old_ids & new_ids, key=lambda i: _safe_int(i)):
        old_item = old[ev_id]
        new_item = new[ev_id]
        if not _equal_on_watched(old_item, new_item):
            changed.append({"id": ev_id, "old": old_item, "new": new_item})

    return {"added": added, "removed": removed, "changed": changed}


def _safe_int(s: str) -> int:
    try:
        return int(s)
    except (TypeError, ValueError):
        return 0


def load_actionability_lookup_pairs(
    biomarkers_dir: Path,
) -> set[tuple[str, str]]:
    """Read all BIO-* YAMLs and return {(gene, variant)} pairs.

    Pairs missing either gene or variant are skipped. Returns empty set if
    the directory does not exist (so the diff script can run from a
    fixture-only context with no real KB).
    """
    pairs: set[tuple[str, str]] = set()
    if not biomarkers_dir.is_dir():
        return pairs
    for yaml_path in sorted(biomarkers_dir.glob("*.yaml")):
        try:
            with yaml_path.open(encoding="utf-8") as f:
                payload = yaml.safe_load(f) or {}
        except (OSError, yaml.YAMLError):
            continue
        lookup = payload.get("actionability_lookup")
        if not isinstance(lookup, dict):
            continue
        gene = (lookup.get("gene") or "").strip()
        variant = (lookup.get("variant") or "").strip()
        if gene and variant:
            pairs.add((gene.upper(), variant))
    return pairs


def _item_pair(item: dict) -> tuple[str, str] | None:
    gene = (item.get("gene") or "").strip()
    variant = (item.get("variant") or "").strip()
    if not gene or not variant:
        return None
    return (gene.upper(), variant)


def intersect_with_actionability(
    diff: dict[str, list], pairs: set[tuple[str, str]]
) -> dict[str, list]:
    """Filter diff buckets to only entries touching watched gene+variant pairs."""
    if not pairs:
        return {"added": [], "removed": [], "changed": []}

    out: dict[str, list] = {"added": [], "removed": [], "changed": []}
    for item in diff["added"]:
        if _item_pair(item) in pairs:
            out["added"].append(item)
    for item in diff["removed"]:
        if _item_pair(item) in pairs:
            out["removed"].append(item)
    for entry in diff["changed"]:
        # Use the new item's gene/variant; fallback to old.
        pair = _item_pair(entry["new"]) or _item_pair(entry["old"])
        if pair in pairs:
            out["changed"].append(entry)
    return out


def _sort_for_report(items: Iterable[dict]) -> list[dict]:
    """Sort items by (level rank ascending, evidence_id ascending)."""
    return sorted(
        items,
        key=lambda i: (_level_rank(i.get("evidence_level")), _safe_int(str(i.get("id") or ""))),
    )


def _sort_changed_for_report(entries: Iterable[dict]) -> list[dict]:
    return sorted(
        entries,
        key=lambda e: (
            min(
                _level_rank(e["old"].get("evidence_level")),
                _level_rank(e["new"].get("evidence_level")),
            ),
            _safe_int(str(e.get("id") or "")),
        ),
    )


def _fmt_item_line(item: dict) -> str:
    flag = _flag(item)
    ev_id = item.get("id") or "?"
    gene = item.get("gene") or "?"
    variant = item.get("variant") or ""
    level = item.get("evidence_level") or "?"
    direction = item.get("evidence_direction") or "?"
    significance = item.get("significance") or "?"
    disease = item.get("disease") or "?"
    therapies = item.get("therapies") or []
    if isinstance(therapies, list):
        ther_str = ", ".join(str(t) for t in therapies) or "—"
    else:
        ther_str = str(therapies)
    return (
        f"- {flag}**EID {ev_id}** · `{gene} {variant}` · level **{level}** · "
        f"{direction} / {significance} · _{disease}_ · therapies: {ther_str}"
    )


def _fmt_changed_line(entry: dict) -> str:
    old, new = entry["old"], entry["new"]
    flag = _flag(new) or _flag(old)
    ev_id = entry["id"]
    gene = new.get("gene") or old.get("gene") or "?"
    variant = new.get("variant") or old.get("variant") or ""
    deltas: list[str] = []
    for f in WATCHED_FIELDS:
        if f == "therapies":
            ov = ", ".join(sorted(str(t) for t in (old.get("therapies") or []))) or "—"
            nv = ", ".join(sorted(str(t) for t in (new.get("therapies") or []))) or "—"
        else:
            ov = old.get(f) or "—"
            nv = new.get(f) or "—"
        if ov != nv:
            deltas.append(f"{f}: `{ov}` → `{nv}`")
    delta_str = "; ".join(deltas) if deltas else "(no watched-field delta)"
    return f"- {flag}**EID {ev_id}** · `{gene} {variant}` · {delta_str}"


def render_markdown(
    old_path: Path,
    new_path: Path,
    diff: dict[str, list],
    actionability_diff: dict[str, list],
    *,
    top_n: int = 30,
) -> str:
    lines: list[str] = []
    lines.append("# CIViC snapshot diff")
    lines.append("")
    lines.append(f"- **Old:** `{old_path}`")
    lines.append(f"- **New:** `{new_path}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Added: **{len(diff['added'])}**")
    lines.append(f"- Removed: **{len(diff['removed'])}**")
    lines.append(f"- Changed (level/direction/significance/therapies/disease): **{len(diff['changed'])}**")
    lines.append("")
    intersect_total = (
        len(actionability_diff["added"])
        + len(actionability_diff["removed"])
        + len(actionability_diff["changed"])
    )
    lines.append(
        f"- Intersect with our actionability_lookup biomarkers: **{intersect_total}**"
    )
    lines.append("")

    if (
        not diff["added"]
        and not diff["removed"]
        and not diff["changed"]
    ):
        lines.append("_No differences detected._")
        lines.append("")
        return "\n".join(lines)

    # Special attention section first — these are the high-priority items.
    lines.append("## ⚠️ Special attention — touches our actionability_lookup biomarkers")
    lines.append("")
    if intersect_total == 0:
        lines.append("_None of the diff entries touch our 29 BIO-* gene+variant pairs._")
        lines.append("")
    else:
        if actionability_diff["added"]:
            lines.append(f"### Added ({len(actionability_diff['added'])})")
            lines.append("")
            for item in _sort_for_report(actionability_diff["added"])[:top_n]:
                lines.append(_fmt_item_line(item))
            lines.append("")
        if actionability_diff["removed"]:
            lines.append(f"### Removed ({len(actionability_diff['removed'])})")
            lines.append("")
            for item in _sort_for_report(actionability_diff["removed"])[:top_n]:
                lines.append(_fmt_item_line(item))
            lines.append("")
        if actionability_diff["changed"]:
            lines.append(f"### Changed ({len(actionability_diff['changed'])})")
            lines.append("")
            for entry in _sort_changed_for_report(actionability_diff["changed"])[:top_n]:
                lines.append(_fmt_changed_line(entry))
            lines.append("")

    # Full diff (top-N each).
    lines.append(f"## Full diff (top {top_n} per bucket, ranked by level)")
    lines.append("")

    if diff["added"]:
        total = len(diff["added"])
        lines.append(f"### Added — {total} total")
        lines.append("")
        for item in _sort_for_report(diff["added"])[:top_n]:
            lines.append(_fmt_item_line(item))
        if total > top_n:
            lines.append("")
            lines.append(f"_…and {total - top_n} more._")
        lines.append("")

    if diff["removed"]:
        total = len(diff["removed"])
        lines.append(f"### Removed — {total} total")
        lines.append("")
        for item in _sort_for_report(diff["removed"])[:top_n]:
            lines.append(_fmt_item_line(item))
        if total > top_n:
            lines.append("")
            lines.append(f"_…and {total - top_n} more._")
        lines.append("")

    if diff["changed"]:
        total = len(diff["changed"])
        lines.append(f"### Changed — {total} total")
        lines.append("")
        for entry in _sort_changed_for_report(diff["changed"])[:top_n]:
            lines.append(_fmt_changed_line(entry))
        if total > top_n:
            lines.append("")
            lines.append(f"_…and {total - top_n} more._")
        lines.append("")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old", type=Path, help="Old snapshot YAML")
    parser.add_argument("new", type=Path, help="New snapshot YAML")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Write markdown summary to this path (otherwise stdout).",
    )
    parser.add_argument(
        "--biomarkers-dir",
        type=Path,
        default=Path("knowledge_base/hosted/content/biomarkers"),
        help="Directory of BIO-* YAMLs for actionability_lookup intersection.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=30,
        help="Top-N entries per bucket in the report (default 30).",
    )
    args = parser.parse_args(argv)

    if not args.old.is_file():
        print(f"ERROR: old snapshot not found: {args.old}", file=sys.stderr)
        return 0  # informational — never hard-fail
    if not args.new.is_file():
        print(f"ERROR: new snapshot not found: {args.new}", file=sys.stderr)
        return 0

    old = load_snapshot(args.old)
    new = load_snapshot(args.new)
    diff = diff_snapshots(old, new)
    pairs = load_actionability_lookup_pairs(args.biomarkers_dir)
    actionability_diff = intersect_with_actionability(diff, pairs)
    md = render_markdown(args.old, args.new, diff, actionability_diff, top_n=args.top_n)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(md, encoding="utf-8")
        print(
            f"diff: added={len(diff['added'])} removed={len(diff['removed'])} "
            f"changed={len(diff['changed'])} "
            f"actionability_intersect={len(actionability_diff['added']) + len(actionability_diff['removed']) + len(actionability_diff['changed'])} "
            f"-> {args.out}"
        )
    else:
        sys.stdout.write(md)

    return 0


if __name__ == "__main__":
    sys.exit(main())
