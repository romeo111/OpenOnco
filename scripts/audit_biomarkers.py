#!/usr/bin/env python3
"""Audit biomarker catalog: list every Biomarker entity, its references
across Indications/Algorithms/RedFlags, and any naming inconsistencies.

Generates `docs/BIOMARKER_CATALOG.md` — re-run anytime KB content changes.
This script is the source of truth for the catalog; do not hand-edit
the markdown output.

Usage:
    python scripts/audit_biomarkers.py
    # or with PYTHONPATH not set:
    PYTHONPATH=. python scripts/audit_biomarkers.py

Audit categories:
  ✓ defined+used        — entity exists, ≥1 rule reference
  ⚠ defined+unused      — entity exists, zero rule references (KB
                          coverage gap or pending wiring)
  ❌ referenced+missing  — rule cites BIO-X but no entity file
  🔧 naming-mismatch    — entity id ≠ rules' citation form
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
BIO_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarkers"
RULE_DIRS = [
    REPO_ROOT / "knowledge_base" / "hosted" / "content" / "indications",
    REPO_ROOT / "knowledge_base" / "hosted" / "content" / "algorithms",
    REPO_ROOT / "knowledge_base" / "hosted" / "content" / "redflags",
]
DISEASE_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "diseases"
EXAMPLES_DIR = REPO_ROOT / "examples"
OUTPUT = REPO_ROOT / "docs" / "BIOMARKER_CATALOG.md"

BIO_REF_RE = re.compile(r"BIO-[A-Z0-9_-]+")


def _load_yaml(path: Path) -> dict | None:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"  [warn] YAML parse failed for {path.name}: {exc}", file=sys.stderr)
        return None


def _walk_yaml(directory: Path):
    """Recursive YAML walk (rule dirs may have subfolders)."""
    if not directory.is_dir():
        return
    for path in sorted(directory.rglob("*.yaml")):
        yield path


def _disease_name_index() -> dict[str, str]:
    """`DIS-X` → preferred name."""
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


def _collect_biomarker_entities(bio_dir: Path = BIO_DIR) -> dict[str, dict]:
    """`BIO-X` → entity dict. Key is the actual `id` field, not filename."""
    out: dict[str, dict] = {}
    for path in _walk_yaml(bio_dir):
        data = _load_yaml(path)
        if not isinstance(data, dict):
            continue
        bid = data.get("id")
        if not bid:
            continue
        data["_file"] = path.name
        out[bid] = data
    return out


def _collect_rule_references(rule_dirs: list[Path] = None) -> tuple[Counter, dict[str, set[str]]]:
    """Walk rule entities; return (BIO-X → ref count, BIO-X → set(disease_ids))."""
    refs: Counter = Counter()
    bio_to_diseases: dict[str, set[str]] = defaultdict(set)
    dirs = rule_dirs if rule_dirs is not None else RULE_DIRS
    for d in dirs:
        for path in _walk_yaml(d):
            text = path.read_text(encoding="utf-8")
            data = _load_yaml(path)
            disease_id = None
            if isinstance(data, dict):
                applicable = data.get("applicable_to") or {}
                disease_id = (
                    data.get("applicable_to_disease")
                    or (applicable.get("disease_id") if isinstance(applicable, dict) else None)
                    or data.get("disease_id")
                    or data.get("disease")
                )
                if isinstance(disease_id, dict):
                    disease_id = disease_id.get("id")
            for match in BIO_REF_RE.findall(text):
                refs[match] += 1
                if disease_id:
                    bio_to_diseases[match].add(disease_id)
    return refs, bio_to_diseases


# ── Issue detection ─────────────────────────────────────────────────────


def _detect_naming_mismatches(
    defined: dict[str, dict],
    referenced: Counter,
) -> list[tuple[str, str]]:
    """Try to pair off near-miss IDs by token overlap. Returns
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
            # Need ≥3 shared tokens (incl. "BIO") and at least one
            # non-trivial token.
            non_trivial = shared - {"BIO", "IHC", "MUT", "STATUS"}
            if len(shared) >= 3 and non_trivial:
                pairs.append((d_id, r_id))
    return pairs


# ── Catalog rendering ───────────────────────────────────────────────────


def _measurement_label(data: dict) -> str:
    btype = (data.get("biomarker_type") or "").replace("_", " ")
    measurement = data.get("measurement") or {}
    method = measurement.get("method") or ""
    if method:
        # First sentence of the method blurb
        return method.split(".")[0][:80]
    return btype or "—"


def _method_group(data: dict) -> str:
    """Coarse method category. Drives PDF-extraction pattern complexity:
    IHC/serum/MSI report a single value (easy regex); FISH/NGS carry
    breakpoints + transcripts (medium); composite scores need
    multi-component arithmetic."""

    btype = (data.get("biomarker_type") or "").lower()
    method = ((data.get("measurement") or {}).get("method") or "").lower()
    if "composite" in btype:
        return "composite"
    if "imaging" in btype or "pet" in btype:
        return "imaging"
    if "tmb" in btype:
        return "NGS-TMB"
    if "msi" in btype or "msi" in method:
        return "MSI/MMR"
    if "methylation" in btype or "methylation" in method:
        return "methylation"
    if "viral" in btype:
        return "viral"
    if "serum" in btype or "serum immunoassay" in method:
        return "serum"
    if "fish" in method:
        return "FISH"
    if "ihc" in btype or "immunohistochem" in method:
        return "IHC"
    if "fusion" in btype:
        return "FISH/NGS"
    if "mutation" in btype or "ngs" in method or "pcr" in method:
        return "NGS"
    if "histology" in btype or "pathology" in btype:
        return "histology"
    return btype.replace("_", " ") or "other"


def _loinc_code(data: dict) -> str:
    codes = data.get("codes") or {}
    return codes.get("loinc") or ""


def _collect_fixture_coverage() -> dict[str, list[str]]:
    """`BIO-X` → [fixture filename ...] for example patient JSONs that
    include the marker in their `biomarkers` block."""

    out: dict[str, list[str]] = defaultdict(list)
    if not EXAMPLES_DIR.is_dir():
        return out
    import json
    for path in sorted(EXAMPLES_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        bio = data.get("biomarkers") or {}
        if isinstance(bio, dict):
            for k in bio:
                if isinstance(k, str) and k.startswith("BIO-"):
                    out[k].append(path.name)
    return out


def _extraction_priority(n_refs: int, method_group: str, has_fixture: bool) -> str:
    """Coarse PDF-extraction priority for the biopsy-extraction roadmap.

    high   = ≥5 refs AND a common, structured-text method (IHC / NGS /
             MSI / serum / methylation). These return on regex effort.
    medium = 2-4 refs OR an exotic method.
    low    = singleton refs or composite scores (manual entry preferable).
    """
    if n_refs >= 5:
        if method_group in {"IHC", "NGS", "MSI/MMR", "serum", "FISH/NGS",
                            "methylation", "FISH"}:
            return "**high**"
        return "medium"
    if n_refs >= 2:
        return "medium"
    return "low"


def _row(bid: str, defined: dict[str, dict], refs: Counter,
         diseases: set[str], disease_names: dict[str, str],
         fixtures: list[str], priority: str) -> str:
    data = defined.get(bid) or {}
    names = data.get("names") or {}
    preferred = names.get("preferred", "")
    method_group = _method_group(data) if data else "—"
    loinc = _loinc_code(data) or "—"
    n_refs = refs.get(bid, 0)
    diseases_str = ", ".join(
        sorted({disease_names.get(d, d).split(",")[0][:22] for d in diseases})
    ) if diseases else "—"
    fix_str = f"{len(fixtures)}× ✓" if fixtures else "—"
    flag = ""
    if bid in defined and n_refs > 0:
        flag = "✓"
    elif bid in defined and n_refs == 0:
        flag = "⚠ unused"
    elif bid not in defined and n_refs > 0:
        flag = "❌ MISSING"
    return (
        f"| `{bid}` | {flag} | {n_refs} | "
        f"{preferred or '—'} | "
        f"{method_group} | {loinc} | {fix_str} | {priority} | "
        f"{diseases_str} |"
    )


def _render_markdown(
    defined: dict[str, dict],
    refs: Counter,
    bio_to_diseases: dict[str, set[str]],
    disease_names: dict[str, str],
    naming_pairs: list[tuple[str, str]],
    fixture_coverage: dict[str, list[str]],
) -> str:
    all_ids = sorted(set(defined) | set(refs))
    lines: list[str] = []
    lines.append("# Biomarker catalog")
    lines.append("")
    lines.append(
        "**Auto-generated by** `scripts/audit_biomarkers.py`. Re-run after "
        "any change under `knowledge_base/hosted/content/{biomarkers,indications,"
        "algorithms,redflags}/`. Do not hand-edit."
    )
    lines.append("")
    lines.append(
        "Purpose: single source of truth for which biomarkers OpenOnco's engine "
        "actually consumes. Drives the PDF-extraction pattern library "
        "(`docs/plans/biopsy_pdf_extraction_2026-04-26.md`) — only catalog-listed "
        "biomarkers get regex patterns."
    )
    lines.append("")

    # Summary
    n_defined = len(defined)
    n_referenced = len(refs)
    n_used = sum(1 for b in defined if b in refs)
    n_unused = n_defined - n_used
    n_missing = sum(1 for b in refs if b not in defined)
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Defined entities:** {n_defined}")
    lines.append(f"- **Referenced by rules:** {n_referenced} unique IDs, "
                 f"{sum(refs.values())} total citations")
    lines.append(f"- **Defined + used (✓):** {n_used}")
    lines.append(f"- **Defined + unused (⚠):** {n_unused}")
    lines.append(f"- **Referenced + missing (❌):** {n_missing}")
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
        missing = sorted(b for b in refs if b not in defined)
        lines.append("### ❌ Referenced but no entity file")
        lines.append("")
        for bid in missing:
            count = refs[bid]
            diseases_for = bio_to_diseases.get(bid, set())
            disease_str = ", ".join(
                sorted({disease_names.get(d, d).split(",")[0][:32] for d in diseases_for})
            ) or "—"
            lines.append(f"- `{bid}` — cited {count}× ({disease_str}). "
                         "Author the entity, or remove the citation.")
        lines.append("")

    if n_unused:
        unused = sorted(b for b in defined if b not in refs)
        lines.append("### ⚠ Defined but no rule consumes them")
        lines.append("")
        for bid in unused:
            data = defined[bid]
            names = data.get("names") or {}
            preferred = names.get("preferred", "")
            lines.append(f"- `{bid}` — {preferred}. "
                         "Wire into ≥1 Indication or red-flag, or document why dormant.")
        lines.append("")

    # Top consumers
    lines.append("## Top-cited biomarkers (PDF-extraction priority)")
    lines.append("")
    lines.append(
        "Reference count below is a proxy for how often the engine reads the "
        "marker. High counts = high payoff for accurate PDF extraction."
    )
    lines.append("")
    lines.append("| Biomarker | Refs | Diseases |")
    lines.append("|---|---|---|")
    top = refs.most_common(20)
    for bid, count in top:
        diseases_for = bio_to_diseases.get(bid, set())
        disease_str = ", ".join(
            sorted({disease_names.get(d, d).split(",")[0][:24] for d in diseases_for})
        ) or "—"
        lines.append(f"| `{bid}` | {count} | {disease_str} |")
    lines.append("")

    # Method-group breakdown — drives PDF-extraction pattern complexity
    lines.append("## Distribution by measurement method")
    lines.append("")
    lines.append(
        "Method category drives PDF-extraction pattern complexity. IHC + serum "
        "+ MSI markers report as a single value (easy regex). FISH/NGS results "
        "carry positional + breakpoint metadata (medium). Composite scores "
        "(IPI, MIPI, FLIPI) need multi-component arithmetic."
    )
    lines.append("")
    method_counts: Counter = Counter()
    for bid in defined:
        method_counts[_method_group(defined[bid])] += 1
    lines.append("| Method group | Count |")
    lines.append("|---|---|")
    for grp, cnt in method_counts.most_common():
        lines.append(f"| {grp} | {cnt} |")
    lines.append("")

    # Coverage gaps — defined entities without LOINC or without fixture coverage
    no_loinc = sorted(b for b in defined if not _loinc_code(defined[b]))
    no_fixture = sorted(
        b for b in defined
        if b in refs and b not in fixture_coverage  # only flag used markers
    )
    if no_loinc or no_fixture:
        lines.append("## Coverage gaps")
        lines.append("")
        if no_loinc:
            lines.append(
                f"### Missing LOINC ({len(no_loinc)} of {len(defined)})"
            )
            lines.append("")
            lines.append(
                "LOINC required for FHIR R4/R5 + mCODE export. Add `codes.loinc` "
                "to each entity below; `https://search.loinc.org` for canonical codes."
            )
            lines.append("")
            for bid in no_loinc[:20]:
                lines.append(f"- `{bid}`")
            if len(no_loinc) > 20:
                lines.append(f"- ... and {len(no_loinc) - 20} more")
            lines.append("")
        if no_fixture:
            lines.append(
                f"### No fixture coverage ({len(no_fixture)} used markers)"
            )
            lines.append("")
            lines.append(
                "Markers consumed by rules but never appearing in `examples/*.json`. "
                "Either add a patient fixture exercising the marker, or document "
                "why no example is needed."
            )
            lines.append("")
            for bid in no_fixture[:20]:
                lines.append(f"- `{bid}` ({refs[bid]}× refs)")
            if len(no_fixture) > 20:
                lines.append(f"- ... and {len(no_fixture) - 20} more")
            lines.append("")

    # Full table
    lines.append("## Full catalog")
    lines.append("")
    lines.append(
        "Columns: **Status** = ✓/⚠/❌ from §Issues. **Refs** = total citations. "
        "**Method** = collapsed measurement category. **LOINC** for FHIR/mCODE. "
        "**Fix** = present in N example patient fixtures. **Pri** = "
        "PDF-extraction priority (refs × method × fixture)."
    )
    lines.append("")
    lines.append(
        "| ID | Status | Refs | Name | Method | LOINC | Fix | Pri | Diseases |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for bid in all_ids:
        diseases_for = bio_to_diseases.get(bid, set())
        fixtures_for = fixture_coverage.get(bid, [])
        method_grp = _method_group(defined.get(bid) or {})
        priority = _extraction_priority(refs.get(bid, 0), method_grp, bool(fixtures_for))
        lines.append(_row(
            bid, defined, refs, diseases_for, disease_names,
            fixtures_for, priority,
        ))
    lines.append("")

    return "\n".join(lines) + "\n"


def collect_biomarker_state(kb_root: Path = None) -> dict:
    """Public entry point for the scheduled-audit orchestrator.

    Returns a JSON-friendly summary of the biomarker catalog state.
    Does NOT regenerate the markdown — call `main()` for that. The
    schema is stable so the orchestrator can diff month-over-month.

    `kb_root`: when provided, scopes the audit to that root (used by
    fixture-driven tests). Defaults to the repo's hosted/content/.
    """

    if kb_root is not None:
        bio_dir = kb_root / "biomarkers"
        rule_dirs = [
            kb_root / "indications",
            kb_root / "algorithms",
            kb_root / "redflags",
        ]
    else:
        bio_dir = BIO_DIR
        rule_dirs = RULE_DIRS

    defined = _collect_biomarker_entities(bio_dir)
    refs, bio_to_diseases = _collect_rule_references(rule_dirs)
    naming_pairs = _detect_naming_mismatches(defined, refs)
    fixture_coverage = _collect_fixture_coverage()

    n_defined = len(defined)
    n_referenced = len(refs)
    missing_ids = sorted(b for b in refs if b not in defined)
    unused_ids = sorted(b for b in defined if b not in refs)

    no_loinc_ids = sorted(b for b in defined if not _loinc_code(defined[b]))
    no_fixture_ids = sorted(
        b for b in defined
        if b in refs and b not in fixture_coverage
    )

    return {
        "defined": n_defined,
        "referenced": n_referenced,
        "total_citations": sum(refs.values()),
        "dormant_count": len(unused_ids),
        "missing_count": len(missing_ids),
        "naming_mismatch_count": len(naming_pairs),
        "loinc_missing_count": len(no_loinc_ids),
        "fixture_missing_count": len(no_fixture_ids),
        "missing_ids": missing_ids,
        "dormant_ids": unused_ids,
        "naming_pairs": [list(p) for p in naming_pairs],
        "loinc_missing_ids": no_loinc_ids,
        "fixture_missing_ids": no_fixture_ids,
    }


def main() -> int:
    print("Auditing biomarker catalog...", file=sys.stderr)
    defined = _collect_biomarker_entities()
    refs, bio_to_diseases = _collect_rule_references()
    disease_names = _disease_name_index()
    naming_pairs = _detect_naming_mismatches(defined, refs)
    fixture_coverage = _collect_fixture_coverage()

    md = _render_markdown(
        defined, refs, bio_to_diseases, disease_names, naming_pairs,
        fixture_coverage,
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(md, encoding="utf-8")

    n_missing = sum(1 for b in refs if b not in defined)
    n_unused = sum(1 for b in defined if b not in refs)

    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}", file=sys.stderr)
    print(f"  defined={len(defined)} referenced={len(refs)} "
          f"unused={n_unused} missing={n_missing} mismatches={len(naming_pairs)}",
          file=sys.stderr)

    # Exit non-zero if there are integrity issues so CI catches them
    if n_missing or naming_pairs:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
