"""Add a second Tier-1/2 source citation to each of 18 single-cited
active RedFlags.

Per CLINICAL_REVIEW_QUEUE_REDFLAGS §A. Mapping is hand-curated to point
each RF at the most-relevant ESMO guideline (or other Tier-1 source).

Idempotent: if the target source is already cited, nothing changes.
Handles both inline (`sources: [A, B]`) and block (`sources:\n  - A`)
list styles in the existing YAMLs.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RF_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "redflags"

BACKFILL: dict[str, str] = {
    "rf_aggressive_histology_transformation.yaml":  "SRC-ESMO-MZL-2024",
    "rf_aitl_autoimmune_cytopenia.yaml":            "SRC-ESMO-PTCL-2024",
    "rf_aitl_ebv_driven_b_cell.yaml":               "SRC-ESMO-PTCL-2024",
    "rf_aitl_hypogamma.yaml":                       "SRC-ESMO-PTCL-2024",
    "rf_burkitt_high_risk.yaml":                    "SRC-ESMO-BURKITT-2024",
    "rf_chl_advanced_stage.yaml":                   "SRC-ESMO-HODGKIN-2024",
    "rf_cll_high_risk.yaml":                        "SRC-ESMO-CLL-2024",
    "rf_dlbcl_cns_risk.yaml":                       "SRC-ESMO-DLBCL-2024",
    "rf_dlbcl_high_ipi.yaml":                       "SRC-ESMO-DLBCL-2024",
    "rf_fl_high_tumor_burden_gelf.yaml":            "SRC-ESMO-FL-2024",
    "rf_fl_transformation_suspect.yaml":            "SRC-ESMO-FL-2024",
    "rf_mcl_blastoid_or_tp53.yaml":                 "SRC-ESMO-MCL-2024",
    "rf_mf_large_cell_transformation.yaml":         "SRC-ESMO-CTCL-2024",
    "rf_mf_sezary_leukemic.yaml":                   "SRC-ESMO-CTCL-2024",
    "rf_mm_high_risk_cytogenetics.yaml":            "SRC-ESMO-MM-2023",
    "rf_mm_renal_dysfunction.yaml":                 "SRC-ESMO-MM-2023",
    "rf_tcell_cd30_positive.yaml":                  "SRC-ESMO-PTCL-2024",
    "rf_wm_hyperviscosity.yaml":                    "SRC-ESMO-WM-2024",
}


# Inline list: `sources: [A, B]` — capture the bracket contents.
# Tolerates trailing comments on the same line.
_INLINE_RE = re.compile(
    r"^(?P<indent>\s*)sources:\s*\[(?P<items>[^\]]*)\](?P<rest>.*)$"
)


def add_source(text: str, new_src: str) -> tuple[str, bool]:
    """Return (new_text, edited). edited=False if new_src already present
    or no `sources:` block found."""
    if new_src in text:
        return text, False

    lines = text.split("\n")

    # Pass 1: try inline list match. Single-line edit.
    for i, line in enumerate(lines):
        m = _INLINE_RE.match(line)
        if m:
            items = m.group("items").strip()
            if items:
                items = items + ", " + new_src
            else:
                items = new_src
            lines[i] = f'{m.group("indent")}sources: [{items}]{m.group("rest")}'
            return "\n".join(lines), True

    # Pass 2: block-style. Find `sources:` line, then append after the
    # last `  - SRC-...` line of that block.
    block_start = None
    for i, line in enumerate(lines):
        if line.lstrip().startswith("sources:") and not _INLINE_RE.match(line):
            block_start = i
            break
    if block_start is None:
        return text, False  # no sources: block at all

    last_item_idx = block_start
    for j in range(block_start + 1, len(lines)):
        stripped = lines[j].lstrip()
        if stripped.startswith("- "):
            last_item_idx = j
            continue
        if stripped == "" or stripped.startswith("#"):
            continue
        # Hit a non-list, non-blank, non-comment line — block ended
        break

    # Determine indent from the existing list items if any, else 2 spaces.
    if last_item_idx != block_start:
        # Use indent of last item line
        indent_len = len(lines[last_item_idx]) - len(lines[last_item_idx].lstrip())
        indent = " " * indent_len
    else:
        indent = "  "

    new_line = f"{indent}- {new_src}"
    lines.insert(last_item_idx + 1, new_line)
    return "\n".join(lines), True


def main() -> int:
    edited = 0
    skipped = 0
    failed: list[str] = []
    for filename, new_src in BACKFILL.items():
        path = RF_DIR / filename
        if not path.exists():
            print(f"SKIP missing: {path}", file=sys.stderr)
            skipped += 1
            continue
        text = path.read_text(encoding="utf-8")
        new_text, did_edit = add_source(text, new_src)
        if not did_edit:
            print(f"already cites {new_src}: {filename}")
            skipped += 1
            continue
        path.write_text(new_text, encoding="utf-8")
        print(f"backfilled {new_src}: {filename}")
        edited += 1

    print(f"\nDone. Edited {edited}, skipped {skipped}.")
    if failed:
        print(f"FAILED: {failed}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
