#!/usr/bin/env python3
"""Audit red-flag catalog: list every RedFlag entity, its references
across Indications/Algorithms/RedFlags, the 5-type matrix coverage per
disease, and naming/lifecycle issues.

Generates `docs/REDFLAG_COVERAGE.md` — re-run anytime KB content changes.
This script is the source of truth for the catalog; do not hand-edit
the markdown output.

Usage:
    python scripts/audit_redflags.py
    # or with PYTHONPATH not set:
    PYTHONPATH=. python scripts/audit_redflags.py

Audit categories (mirror of audit_biomarkers.py):
  ✓ defined+used        — entity exists, ≥1 rule reference
  ⚠ defined+unused      — entity exists, zero rule references (KB
                          coverage gap or pending wiring)
  ❌ referenced+missing  — rule cites RF-X but no entity file
  🔧 naming-mismatch    — entity id ≠ rules' citation form

5-type matrix coverage uses the authored `category` + `relevant_diseases`
fields directly (REDFLAG_AUTHORING_GUIDE §2 + RedFlagCategory enum), so
it does not depend on filename / suffix heuristics.
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
RF_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "redflags"
RULE_DIRS = [
    REPO_ROOT / "knowledge_base" / "hosted" / "content" / "indications",
    REPO_ROOT / "knowledge_base" / "hosted" / "content" / "algorithms",
    REPO_ROOT / "knowledge_base" / "hosted" / "content" / "redflags",
]
DISEASE_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "diseases"
OUTPUT = REPO_ROOT / "docs" / "REDFLAG_COVERAGE.md"

# Match `RF-X-Y-Z` where each segment is alphanumeric/underscore — forbids
# trailing dash so a folded-block wrap like `RF-FL-\n  TRANSFORMATION-SUSPECT`
# doesn't get captured as `RF-FL-`. Captures the longest valid sequence.
RF_REF_RE = re.compile(r"RF-[A-Z0-9_]+(?:-[A-Z0-9_]+)*")

# Canonical 5-type matrix per RedFlagCategory enum + REDFLAG_AUTHORING_GUIDE §2.
MATRIX_TYPES = (
    "frailty-age",
    "infection-screening",
    "organ-dysfunction",
    "transformation-progression",
    "high-risk-biology",
)


def _load_yaml(path: Path) -> dict | None:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"  [warn] YAML parse failed for {path.name}: {exc}", file=sys.stderr)
        return None


def _walk_yaml(directory: Path):
    if not directory.is_dir():
        return
    for path in sorted(directory.rglob("*.yaml")):
        yield path


def _disease_name_index() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in _walk_yaml(DISEASE_DIR):
        data = _load_yaml(path)
        if not isinstance(data, dict):
            continue
        did = data.get("id")
        names = data.get("names") or {}
        if did:
            out[did] = (
                names.get("preferred")
                or names.get("english")
                or did
            )
    return out


def _collect_rf_entities(rf_dir: Path = RF_DIR) -> dict[str, dict]:
    """`RF-X` → entity dict. Key is the actual `id` field, not filename."""
    out: dict[str, dict] = {}
    for path in _walk_yaml(rf_dir):
        data = _load_yaml(path)
        if not isinstance(data, dict):
            continue
        rid = data.get("id")
        if not rid:
            continue
        data["_file"] = path.relative_to(rf_dir).as_posix()
        out[rid] = data
    return out


def _walk_strings(obj):
    """Yield every string value reachable by walking a parsed YAML object.

    Walking the parsed structure avoids false positives from YAML folded-
    block line-wraps (e.g. `RF-NK-T-NASAL-INFECTION-\n  SCREENING` in a
    `notes: >` block, which the raw-text regex would split mid-id but
    the YAML parser correctly joins to one string with a space).
    """
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _walk_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_strings(v)


# Inside `notes: >` folded scalars, an author may wrap a long ID across
# lines like `RF-NK-T-NASAL-INFECTION-\n  SCREENING`. YAML folding turns
# that into `RF-NK-T-NASAL-INFECTION- SCREENING` (with a single space),
# which would otherwise read as a truncated id. Normalize such wraps
# before regex extraction.
_HYPHEN_WRAP_RE = re.compile(r"-\s+(?=[A-Z0-9_])")


def _collect_rule_references(rule_dirs: list[Path] = None) -> Counter:
    """Walk rule entities; return Counter of RF-X reference counts.

    Self-references (RF cited in its own definition file) don't count —
    only consumption from algorithms/indications/other-RFs is meaningful.
    """
    refs: Counter = Counter()
    dirs = rule_dirs if rule_dirs is not None else RULE_DIRS
    for d in dirs:
        for path in _walk_yaml(d):
            data = _load_yaml(path)
            if not isinstance(data, dict):
                continue
            self_id = data.get("id")
            for value in _walk_strings(data):
                stitched = _HYPHEN_WRAP_RE.sub("-", value)
                for match in RF_REF_RE.findall(stitched):
                    if match == self_id:
                        continue
                    refs[match] += 1
    return refs


# ── Issue detection ─────────────────────────────────────────────────────


def _detect_naming_mismatches(
    defined: dict[str, dict],
    referenced: Counter,
) -> list[tuple[str, str]]:
    """Pair off near-miss IDs by token overlap. Returns
    (entity_id, ref_id) candidate pairs."""

    defined_ids = set(defined)
    ref_ids = set(referenced)
    only_defined = defined_ids - ref_ids
    only_ref = ref_ids - defined_ids

    pairs: list[tuple[str, str]] = []
    for d_id in only_defined:
        d_tokens = set(d_id.split("-"))
        for r_id in only_ref:
            r_tokens = set(r_id.split("-"))
            shared = d_tokens & r_tokens
            non_trivial = shared - {"RF", "HIGH", "RISK", "STATUS"}
            if len(shared) >= 3 and non_trivial:
                pairs.append((d_id, r_id))
    return pairs


# ── 5-type matrix coverage ──────────────────────────────────────────────


def _matrix_coverage(
    defined: dict[str, dict],
    disease_names: dict[str, str],
) -> tuple[dict[str, set[str]], list[tuple[str, list[str]]]]:
    """Return (per_disease_categories, incomplete_diseases).

    `per_disease_categories[DIS-X]` is the set of category strings
    covered by RFs whose `relevant_diseases` includes DIS-X (or "*").

    `incomplete_diseases` lists `(disease_id, missing_categories)` for
    each modeled disease that lacks ≥1 of the 5 matrix categories.
    """

    coverage: dict[str, set[str]] = {d: set() for d in disease_names}
    universal_cats: set[str] = set()

    for rid, data in defined.items():
        cat = data.get("category", "other")
        rel = data.get("relevant_diseases") or []
        if "*" in rel:
            universal_cats.add(cat)
            continue
        for did in rel:
            if did in coverage:
                coverage[did].add(cat)

    # Universal RFs (relevant_diseases: ["*"]) count toward every disease.
    for did in coverage:
        coverage[did] |= universal_cats

    incomplete = []
    for did in sorted(coverage):
        missing = [t for t in MATRIX_TYPES if t not in coverage[did]]
        if missing:
            incomplete.append((did, missing))
    return coverage, incomplete


# ── Catalog rendering ───────────────────────────────────────────────────


def _category_label(data: dict) -> str:
    return data.get("category", "other")


def _direction(data: dict) -> str:
    return str(data.get("clinical_direction") or "—")


def _severity(data: dict) -> str:
    return str(data.get("severity") or "—")


def _has_sources(data: dict) -> bool:
    return bool(data.get("sources"))


def _is_draft(data: dict) -> bool:
    return bool(data.get("draft"))


def _signoff_count(data: dict) -> int:
    val = data.get("reviewer_signoffs", 0)
    try:
        return int(val or 0)
    except (TypeError, ValueError):
        return 0


def _shifts_count(data: dict) -> int:
    return len(data.get("shifts_algorithm") or [])


def _row(rid: str, defined: dict[str, dict], refs: Counter) -> str:
    data = defined.get(rid) or {}
    n_refs = refs.get(rid, 0)
    flag = ""
    if rid in defined and n_refs > 0:
        flag = "✓"
    elif rid in defined and n_refs == 0:
        flag = "⚠ unused"
    elif rid not in defined and n_refs > 0:
        flag = "❌ MISSING"
    cat = _category_label(data) if data else "—"
    direction = _direction(data) if data else "—"
    sev = _severity(data) if data else "—"
    src = "✓" if _has_sources(data) else "—"
    draft = "draft" if _is_draft(data) else "—"
    rel_diseases = data.get("relevant_diseases") or []
    rel_str = ", ".join(rel_diseases[:3])
    if len(rel_diseases) > 3:
        rel_str += f" +{len(rel_diseases)-3}"
    return (
        f"| `{rid}` | {flag} | {n_refs} | {cat} | {direction} | "
        f"{sev} | {src} | {draft} | {rel_str or '—'} |"
    )


def _render_markdown(
    defined: dict[str, dict],
    refs: Counter,
    disease_names: dict[str, str],
    naming_pairs: list[tuple[str, str]],
    coverage: dict[str, set[str]],
    incomplete_diseases: list[tuple[str, list[str]]],
) -> str:
    all_ids = sorted(set(defined) | set(refs))
    lines: list[str] = []
    lines.append("# RedFlag coverage")
    lines.append("")
    lines.append(
        "**Auto-generated by** `scripts/audit_redflags.py`. Re-run after any "
        "change under `knowledge_base/hosted/content/{redflags,indications,"
        "algorithms}/`. Do not hand-edit."
    )
    lines.append("")
    lines.append(
        "Purpose: single source of truth for RedFlag catalog integrity + "
        "5-type matrix coverage per disease (REDFLAG_AUTHORING_GUIDE §2). "
        "Mirrors `BIOMARKER_CATALOG.md` so the same `defined+used / unused / "
        "missing / mismatch` discipline applies to clinical-trigger entities."
    )
    lines.append("")

    # Summary
    n_defined = len(defined)
    n_referenced = len(refs)
    n_used = sum(1 for r in defined if r in refs)
    n_unused = n_defined - n_used
    n_missing = sum(1 for r in refs if r not in defined)
    n_drafts = sum(1 for r in defined.values() if _is_draft(r))
    n_no_sources = sum(1 for r in defined.values() if not _has_sources(r))
    n_signed_off = sum(1 for r in defined.values() if _signoff_count(r) >= 2)
    cat_counts: Counter = Counter(_category_label(r) for r in defined.values())

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Defined entities:** {n_defined}")
    lines.append(f"- **Referenced by rules:** {n_referenced} unique IDs, "
                 f"{sum(refs.values())} total citations")
    lines.append(f"- **Defined + used (✓):** {n_used}")
    lines.append(f"- **Defined + unused (⚠):** {n_unused}")
    lines.append(f"- **Referenced + missing (❌):** {n_missing}")
    lines.append(f"- **Drafts:** {n_drafts}")
    lines.append(f"- **Without source citation:** {n_no_sources}")
    lines.append(f"- **With ≥2 reviewer signoffs (CHARTER §6.1):** "
                 f"{n_signed_off}")
    lines.append("")
    lines.append("By category:")
    for cat in MATRIX_TYPES:
        lines.append(f"- `{cat}`: {cat_counts.get(cat, 0)}")
    other = sum(cat_counts.get(c, 0) for c in cat_counts if c not in MATRIX_TYPES)
    if other:
        lines.append(f"- `other` (off-matrix): {other}")
    lines.append("")

    # Issues block
    if naming_pairs or n_missing or n_unused:
        lines.append("## Issues to resolve")
        lines.append("")

    if naming_pairs:
        lines.append("### 🔧 Naming mismatches (likely typos — engine sees broken ref)")
        lines.append("")
        lines.append("| Defined entity | Cited form | Action |")
        lines.append("|---|---|---|")
        for d_id, r_id in naming_pairs:
            lines.append(
                f"| `{d_id}` | `{r_id}` | Pick canonical id, "
                "update either the entity file or the citing rules. "
                "Two-reviewer per CHARTER §6.1. |"
            )
        lines.append("")

    if n_missing:
        missing = sorted(r for r in refs if r not in defined)
        lines.append("### ❌ Referenced but no entity file")
        lines.append("")
        for rid in missing:
            count = refs[rid]
            lines.append(f"- `{rid}` — cited {count}×. "
                         "Author the entity, or remove the citation.")
        lines.append("")

    if n_unused:
        unused = sorted(r for r in defined if r not in refs)
        lines.append("### ⚠ Defined but no rule consumes them")
        lines.append("")
        lines.append(
            "RedFlag exists in the catalog but no algorithm / indication "
            "/ other RedFlag references it. Either wire it into a rule or "
            "document why it is dormant (e.g. `notes:` block explaining "
            "why it is intentionally orphaned)."
        )
        lines.append("")
        for rid in unused:
            data = defined[rid]
            cat = _category_label(data)
            rel = ", ".join(data.get("relevant_diseases") or [])
            lines.append(f"- `{rid}` ({cat}) — diseases: {rel or 'none declared'}")
        lines.append("")

    # 5-type matrix coverage
    lines.append("## 5-type matrix coverage per disease")
    lines.append("")
    lines.append(
        "Every modeled disease should carry RedFlags in all five categories "
        "(REDFLAG_AUTHORING_GUIDE §2). Coverage uses the authored `category` "
        "+ `relevant_diseases` fields directly — universal RFs "
        "(`relevant_diseases: [\"*\"]`) count toward every disease."
    )
    lines.append("")
    n_complete = len(disease_names) - len(incomplete_diseases)
    lines.append(
        f"**Complete (all 5 categories): {n_complete} / {len(disease_names)} "
        f"diseases.**"
    )
    lines.append("")

    if incomplete_diseases:
        lines.append("### Diseases missing one or more matrix categories")
        lines.append("")
        lines.append("| Disease | Missing categories |")
        lines.append("|---|---|")
        for did, missing in incomplete_diseases:
            name = disease_names.get(did, did).split(",")[0][:40]
            cats = ", ".join(f"`{c}`" for c in missing)
            lines.append(f"| `{did}` ({name}) | {cats} |")
        lines.append("")

    # Top-cited RFs (engine hot-path)
    lines.append("## Top-cited RedFlags (engine hot-path)")
    lines.append("")
    lines.append(
        "Reference count below is a proxy for how often the engine evaluates "
        "the trigger. High-traffic RedFlags merit extra test coverage + "
        "lower priority for refactoring without review."
    )
    lines.append("")
    lines.append("| RedFlag | Refs | Category | Severity | Direction |")
    lines.append("|---|---|---|---|---|")
    for rid, count in refs.most_common(20):
        data = defined.get(rid) or {}
        lines.append(
            f"| `{rid}` | {count} | {_category_label(data)} | "
            f"{_severity(data)} | {_direction(data)} |"
        )
    lines.append("")

    # Authoring lifecycle
    lines.append("## Authoring lifecycle")
    lines.append("")
    if n_no_sources:
        lines.append(
            f"### Without source citation ({n_no_sources})"
        )
        lines.append("")
        lines.append(
            "CHARTER §6.1 requires a clinical source for every published "
            "RedFlag. Drafts may be sourceless during authoring; ship-ready "
            "RedFlags must cite ≥1 guideline / RCT / regulatory document."
        )
        lines.append("")
        no_src = sorted(r for r in defined if not _has_sources(defined[r]))
        for rid in no_src[:30]:
            cat = _category_label(defined[rid])
            lines.append(f"- `{rid}` ({cat})")
        if len(no_src) > 30:
            lines.append(f"- ... and {len(no_src) - 30} more")
        lines.append("")

    if n_signed_off < n_defined:
        lines.append(
            f"### Pending two-reviewer sign-off "
            f"({n_defined - n_signed_off} of {n_defined} STUB)"
        )
        lines.append("")
        lines.append(
            "CHARTER §6.1: clinical content must carry two of three Clinical "
            "Co-Lead approvals before leaving STUB status. The count above "
            "tracks the gap; don't list every RedFlag here — see the full "
            "catalog table."
        )
        lines.append("")

    # Full table
    lines.append("## Full catalog")
    lines.append("")
    lines.append(
        "Columns: **Status** = ✓/⚠/❌ from §Issues. **Refs** = total citations. "
        "**Cat** = 5-type matrix category. **Dir** = clinical_direction. "
        "**Sev** = severity. **Src** = ≥1 source cited. "
        "**Draft** = authoring lifecycle. **Diseases** = `relevant_diseases` "
        "(first 3)."
    )
    lines.append("")
    lines.append(
        "| ID | Status | Refs | Cat | Dir | Sev | Src | Draft | Diseases |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for rid in all_ids:
        lines.append(_row(rid, defined, refs))
    lines.append("")

    return "\n".join(lines) + "\n"


def collect_redflag_state(kb_root: Path = None) -> dict:
    """Public entry point for the scheduled-audit orchestrator.

    Returns a JSON-friendly summary of the RedFlag catalog state. Does
    NOT regenerate the markdown — call `main()` for that. Schema is
    stable so the orchestrator can diff month-over-month.

    `kb_root`: when provided, scopes the audit to that root. Defaults to
    the repo's hosted/content/.
    """

    if kb_root is not None:
        rf_dir = kb_root / "redflags"
        rule_dirs = [
            kb_root / "indications",
            kb_root / "algorithms",
            kb_root / "redflags",
        ]
    else:
        rf_dir = RF_DIR
        rule_dirs = RULE_DIRS

    defined = _collect_rf_entities(rf_dir)
    refs = _collect_rule_references(rule_dirs)
    disease_names = _disease_name_index()
    naming_pairs = _detect_naming_mismatches(defined, refs)
    _, incomplete_diseases = _matrix_coverage(defined, disease_names)

    n_defined = len(defined)
    missing_ids = sorted(r for r in refs if r not in defined)
    unused_ids = sorted(r for r in defined if r not in refs)
    no_sources_ids = sorted(r for r in defined if not _has_sources(defined[r]))
    drafts = sorted(r for r in defined if _is_draft(defined[r]))

    return {
        "defined": n_defined,
        "referenced": len(refs),
        "total_citations": sum(refs.values()),
        "dormant_count": len(unused_ids),
        "missing_count": len(missing_ids),
        "naming_mismatch_count": len(naming_pairs),
        "no_sources_count": len(no_sources_ids),
        "drafts_count": len(drafts),
        "matrix_incomplete_diseases": [
            {"disease_id": did, "missing_categories": miss}
            for did, miss in incomplete_diseases
        ],
        "missing_ids": missing_ids,
        "dormant_ids": unused_ids,
        "naming_pairs": [list(p) for p in naming_pairs],
    }


def main() -> int:
    print("Auditing RedFlag catalog...", file=sys.stderr)
    defined = _collect_rf_entities()
    refs = _collect_rule_references()
    disease_names = _disease_name_index()
    naming_pairs = _detect_naming_mismatches(defined, refs)
    coverage, incomplete = _matrix_coverage(defined, disease_names)

    md = _render_markdown(
        defined, refs, disease_names, naming_pairs, coverage, incomplete,
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(md, encoding="utf-8")

    n_missing = sum(1 for r in refs if r not in defined)
    n_unused = sum(1 for r in defined if r not in refs)

    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}", file=sys.stderr)
    print(
        f"  defined={len(defined)} referenced={len(refs)} "
        f"unused={n_unused} missing={n_missing} "
        f"mismatches={len(naming_pairs)} matrix_incomplete={len(incomplete)}",
        file=sys.stderr,
    )

    # Exit non-zero on integrity issues so CI catches them. Matrix gaps
    # are a coverage signal, not an integrity error — they don't fail CI.
    if n_missing or naming_pairs:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
