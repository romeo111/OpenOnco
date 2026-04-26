"""One-shot script to populate Biomarker.oncokb_lookup hints.

Phase 2 PR-C of OncoKB safe-rollout v3 §4. Adds opt-in hints to
biomarker entities that have a canonical actionable variant. Per
plan invariant: only variant-specific entities get hints — generic
gene-level biomarkers (e.g. "EGFR mutation", "TP53 mutation") would
need a new variant-specific entity authored before they can carry
a hint, so we don't guess.

Each hint must normalize cleanly via engine/oncokb_extract.normalize_variant
(verified by tests/test_oncokb_variant_normalize.py).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Mapping: biomarker file basename -> (gene, variant)
# All variants here MUST round-trip through normalize_variant() to the
# same form (idempotency invariant from Phase 3a tests).
HINTS: dict[str, tuple[str, str]] = {
    # Variant-specific entities (no ambiguity)
    "bio_braf_v600e": ("BRAF", "V600E"),
    "bio_myd88_l265p": ("MYD88", "L265P"),
    "bio_kras_g12c": ("KRAS", "G12C"),
    "bio_rhoa_g17v": ("RHOA", "G17V"),
    # Semi-specific — use canonical/most-actionable variant per OncoKB
    "bio_ezh2_y641": ("EZH2", "Y641F"),  # most common; OncoKB Level 1 for tazemetostat
    "bio_flt3_d835": ("FLT3", "D835Y"),  # most common D835 substitution
    # Gene-level with overwhelmingly canonical actionable variant
    "bio_jak2": ("JAK2", "V617F"),       # >95% of MPN-actionable JAK2 mutations
    "bio_npm1": ("NPM1", "W288fs"),      # canonical AML mutation (type A); OncoKB has fs hotspot
}


HINT_BLOCK_TEMPLATE = """
# OncoKB integration hint (safe-rollout v3 §4 + PR-C). When a patient
# has this biomarker, the engine will issue an OncoKB lookup with these
# values. Conservative: only the canonical actionable variant; other
# variants on the same gene need their own variant-specific biomarker.
oncokb_lookup:
  gene: {gene}
  variant: {variant}
"""


def _insert_hint(text: str, gene: str, variant: str) -> str:
    """Insert oncokb_lookup block before the `last_reviewed:` line if
    present, else before `notes:`, else append. Idempotent."""
    if "oncokb_lookup:" in text:
        return text

    block = HINT_BLOCK_TEMPLATE.format(gene=gene, variant=variant).rstrip() + "\n"
    lines = text.splitlines(keepends=True)

    insert_before_keys = ("last_reviewed:", "notes:")
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if line == stripped and any(stripped.startswith(k) for k in insert_before_keys):
            return "".join(lines[:i]) + block + "\n" + "".join(lines[i:])

    # Fallback: append to end
    return text.rstrip() + "\n" + block


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    biomarkers_dir = repo_root / "knowledge_base" / "hosted" / "content" / "biomarkers"

    if not biomarkers_dir.exists():
        print(f"ERROR: {biomarkers_dir} not found", file=sys.stderr)
        return 1

    # Verify each hint normalizes correctly (sanity check)
    sys.path.insert(0, str(repo_root))
    from knowledge_base.engine.oncokb_extract import normalize_variant

    for stem, (gene, variant) in HINTS.items():
        nv = normalize_variant(variant, gene)
        if nv is None:
            print(
                f"ABORT: hint for {stem} ({gene}, {variant}) fails normalize_variant — "
                f"would be silently skipped at runtime",
                file=sys.stderr,
            )
            return 1
        if nv.oncokb_query_string != variant:
            print(
                f"WARN: hint for {stem} normalizes {variant!r} -> {nv.oncokb_query_string!r} "
                f"(non-idempotent; consider using {nv.oncokb_query_string!r} directly)"
            )

    updated = 0
    skipped = 0
    missing: list[str] = []

    for stem, (gene, variant) in HINTS.items():
        path = biomarkers_dir / f"{stem}.yaml"
        if not path.exists():
            missing.append(stem)
            continue
        text = path.read_text(encoding="utf-8")
        if "oncokb_lookup:" in text:
            skipped += 1
            continue
        new_text = _insert_hint(text, gene, variant)
        path.write_text(new_text, encoding="utf-8")
        updated += 1
        print(f"  + {stem:30s} -> oncokb_lookup: {gene} {variant}")

    print(f"\nUpdated {updated} biomarker YAMLs.")
    print(f"Already had hint: {skipped}")
    if missing:
        print(f"Missing files: {missing}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
