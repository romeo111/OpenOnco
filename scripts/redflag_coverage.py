"""RedFlag coverage report.

Prints a disease × 5-flag-type matrix showing which RedFlag categories
each disease in the KB has covered. Categories follow
specs/REDFLAG_AUTHORING_GUIDE.md §2:

    organ-dysfunction
    infection-screening
    high-risk-biology
    transformation-progression
    frailty-age

Categorization is heuristic — derived from the RedFlag id and trigger
findings — because the schema doesn't carry an explicit category field
yet. Result: a pragmatic snapshot that shows the obvious holes (zero
coverage, single-category disease, etc.) without requiring a schema bump.

Usage:
    python scripts/redflag_coverage.py
    python scripts/redflag_coverage.py --tsv > coverage.tsv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"

CATEGORIES = [
    "organ-dysfunction",
    "infection-screening",
    "high-risk-biology",
    "transformation-progression",
    "frailty-age",
]


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _classify(rf: dict) -> str | None:
    """Read the explicit `category:` field. Returns one of CATEGORIES,
    or None for `other` / missing (so they show up in 'uncategorized')."""
    cat = rf.get("category")
    if cat in CATEGORIES:
        return cat
    return None


def _collect_finding_keys(trigger: dict) -> list[str]:
    out: list[str] = []
    if not isinstance(trigger, dict):
        return out
    for key in ("all_of", "any_of", "none_of"):
        for clause in trigger.get(key) or []:
            if isinstance(clause, dict):
                if "finding" in clause:
                    out.append(str(clause["finding"]))
                if "condition" in clause:
                    out.append(str(clause["condition"]))
                # nested
                out.extend(_collect_finding_keys(clause))
    if "finding" in trigger:
        out.append(str(trigger["finding"]))
    return out


def build_matrix() -> tuple[dict[str, dict[str, list[str]]], dict[str, list[str]]]:
    """Returns (per_disease_matrix, uncategorized).

    per_disease_matrix[disease_id][category] = list of RF IDs
    uncategorized[rf_id] = list with that single RF, for diagnostics
    """
    diseases: dict[str, dict] = {}
    for p in (KB_ROOT / "diseases").glob("*.yaml"):
        d = _load_yaml(p)
        if d.get("id"):
            diseases[d["id"]] = d

    matrix: dict[str, dict[str, list[str]]] = {
        d_id: {cat: [] for cat in CATEGORIES} for d_id in diseases
    }
    uncategorized: list[str] = []
    universal: dict[str, list[str]] = {cat: [] for cat in CATEGORIES}

    for p in (KB_ROOT / "redflags").rglob("*.yaml"):
        rf = _load_yaml(p)
        rid = rf.get("id")
        if not rid:
            continue
        cat = _classify(rf)
        rels = rf.get("relevant_diseases") or []

        if cat is None:
            uncategorized.append(rid)
            continue

        if "*" in rels:
            universal[cat].append(rid)
            for d_id in matrix:
                matrix[d_id][cat].append(rid + " (universal)")
            continue

        for d_id in rels:
            if d_id in matrix:
                matrix[d_id][cat].append(rid)

    return matrix, uncategorized


def render_text(matrix: dict[str, dict[str, list[str]]],
                uncategorized: list[str]) -> str:
    lines: list[str] = []

    n_diseases = len(matrix)
    n_with_any = sum(1 for d in matrix.values() if any(d.values()))
    n_full = sum(1 for d in matrix.values() if all(d.values()))

    lines.append("RedFlag coverage matrix (specs/REDFLAG_AUTHORING_GUIDE.md §2)")
    lines.append("=" * 78)
    lines.append("")
    lines.append(f"Diseases total:        {n_diseases}")
    lines.append(f"  with >=1 RedFlag:    {n_with_any}")
    lines.append(f"  with all 5 categories: {n_full}")
    lines.append(f"  uncategorized RFs:   {len(uncategorized)}")
    if uncategorized:
        lines.append(f"    {', '.join(sorted(uncategorized))}")
    lines.append("")

    headers = ["disease"] + [c[:6] for c in CATEGORIES] + ["total"]
    col_w = [max(28, max((len(d) for d in matrix), default=10))] + [7] * len(CATEGORIES) + [6]
    lines.append("  ".join(h.ljust(col_w[i]) for i, h in enumerate(headers)))
    lines.append("-" * 78)

    for d_id in sorted(matrix):
        row = [d_id.ljust(col_w[0])]
        total = 0
        for i, cat in enumerate(CATEGORIES):
            n = len(matrix[d_id][cat])
            total += n
            mark = str(n) if n else "-"
            row.append(mark.ljust(col_w[i + 1]))
        row.append(str(total).ljust(col_w[-1]))
        lines.append("  ".join(row))
    lines.append("")
    lines.append("Legend: numbers = RFs covering that category; '-' = no coverage.")
    lines.append("Universal RFs (relevant_diseases: ['*']) are counted on every disease.")
    return "\n".join(lines)


def render_tsv(matrix: dict[str, dict[str, list[str]]]) -> str:
    out: list[str] = []
    out.append("\t".join(["disease"] + CATEGORIES + ["total"]))
    for d_id in sorted(matrix):
        cells = [d_id]
        total = 0
        for cat in CATEGORIES:
            n = len(matrix[d_id][cat])
            total += n
            cells.append(str(n))
        cells.append(str(total))
        out.append("\t".join(cells))
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tsv", action="store_true", help="emit TSV instead of text")
    args = ap.parse_args()

    matrix, uncategorized = build_matrix()

    if args.tsv:
        print(render_tsv(matrix))
    else:
        print(render_text(matrix, uncategorized))
    return 0


if __name__ == "__main__":
    sys.exit(main())
