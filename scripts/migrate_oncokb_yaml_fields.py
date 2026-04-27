"""Phase 1.5 mechanical YAML migration for the OncoKB → CIViC pivot.

Two transforms:

1. ``knowledge_base/hosted/content/biomarkers/bio_*.yaml``
   Rename top-level field ``oncokb_lookup:`` → ``actionability_lookup:``.
   Value (the {gene, variant} mapping) is unchanged.

2. ``knowledge_base/hosted/content/biomarker_actionability/bma_*.yaml``
   * Capture ``oncokb_level:`` value (string).
   * Capture ``oncokb_snapshot_version:`` value (string, may be absent).
   * Delete those two top-level keys.
   * Insert a top-level ``evidence_sources:`` block with a single entry whose
     ``source: SRC-ONCOKB``, ``level: <oncokb_level>``, plus a fixed note.
   * Insert top-level ``actionability_review_required: true``.
   * If file already has top-level ``evidence_sources:`` — STOP (don't double-write).
   * If ``oncokb_level`` is empty/null — drop both keys + set
     ``actionability_review_required: true`` but skip the evidence_sources insert.

Idempotent: re-running on already-migrated files is a no-op.

Implementation note: works on raw lines (not a YAML round-trip) so we preserve
comments, folded-scalar formatting, and quoting exactly. The two field families
we touch are guaranteed top-level scalars or simple inline mappings, so a line-
based approach is safe and minimizes diff churn.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BIO_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarkers"
BMA_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarker_actionability"

ONCOKB_NOTE = (
    "Pre-CIViC-pivot legacy entry — pending Phase 3 reconciliation against "
    "CIViC. Per OncoKB ToS this entry is NOT surfaced in HCP or patient "
    "render; Phase 4 render skips evidence_sources entries with "
    "source=SRC-ONCOKB."
)


def _is_top_level_key(line: str, key: str) -> bool:
    """True if ``line`` starts a top-level key named ``key`` (no indent)."""
    return line.startswith(key + ":") or line.startswith(key + " :")


def _split_top_level_key_value(line: str, key: str) -> str:
    """Return the inline value after ``<key>:`` on the same line, stripped.

    For block-style keys (no inline value, value follows on indented lines), this
    returns ''.
    """
    after = line[len(key) + 1 :]  # drop "key:"
    return after.strip()


def _next_top_level_index(lines: list[str], start: int) -> int:
    """Return the index of the next non-indented, non-blank, non-comment line.

    Used to determine where a block-style top-level key's value ends. Returns
    ``len(lines)`` if no further top-level line exists.
    """
    i = start
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        # Top-level key = first column is non-whitespace and not a comment-only
        # line. We treat document-end markers and comments at col 0 as
        # passthrough; they end any block but they're not the *next key*.
        if line[0] not in " \t":
            return i
        i += 1
    return len(lines)


# ---------------------------------------------------------------------------
# BIO migration
# ---------------------------------------------------------------------------


def migrate_bio_file(path: Path) -> str:
    """Rename ``oncokb_lookup:`` → ``actionability_lookup:`` at top level.

    Returns one of: 'renamed', 'already_migrated', 'no_field'.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    has_old = any(_is_top_level_key(line, "oncokb_lookup") for line in lines)
    has_new = any(_is_top_level_key(line, "actionability_lookup") for line in lines)

    if has_new and not has_old:
        return "already_migrated"
    if not has_old:
        return "no_field"

    new_lines = []
    for line in lines:
        if _is_top_level_key(line, "oncokb_lookup"):
            # Replace just the key prefix; preserve everything after the colon.
            new_lines.append("actionability_lookup:" + line[len("oncokb_lookup:") :])
        else:
            new_lines.append(line)

    path.write_text("".join(new_lines), encoding="utf-8")
    return "renamed"


# ---------------------------------------------------------------------------
# BMA migration
# ---------------------------------------------------------------------------


def _strip_yaml_scalar(raw: str) -> str:
    """Strip surrounding single/double quotes from an inline YAML scalar."""
    s = raw.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    return s


def migrate_bma_file(path: Path) -> tuple[str, dict]:
    """Convert ``oncokb_level`` + ``oncokb_snapshot_version`` → ``evidence_sources``.

    Returns ``(status, info)`` where status is one of:
      'migrated'           — full conversion happened
      'migrated_no_level'  — oncokb_level empty/null; only flag set, no evidence_sources
      'already_migrated'   — file already has evidence_sources
      'no_field'           — no oncokb_level key present (idempotent re-run)
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    has_evidence_sources = any(
        _is_top_level_key(line, "evidence_sources") for line in lines
    )
    has_oncokb_level = any(_is_top_level_key(line, "oncokb_level") for line in lines)
    has_review_flag = any(
        _is_top_level_key(line, "actionability_review_required") for line in lines
    )

    if has_evidence_sources:
        # Be conservative: refuse to double-write.
        return ("already_migrated", {})

    if not has_oncokb_level:
        return ("no_field", {})

    # Locate top-level oncokb_level and oncokb_snapshot_version.
    level_value: str | None = None
    snapshot_value: str | None = None  # captured for telemetry only

    new_lines: list[str] = []
    i = 0
    n = len(lines)
    last_oncokb_block_end = -1  # index after which we'll insert the new block

    while i < n:
        line = lines[i]
        if _is_top_level_key(line, "oncokb_level"):
            inline = _split_top_level_key_value(line, "oncokb_level")
            if inline:
                level_value = _strip_yaml_scalar(inline)
                # treat YAML null as empty
                if level_value.lower() in ("~", "null", ""):
                    level_value = ""
                i += 1  # consume just the single line
                last_oncokb_block_end = len(new_lines)
                continue
            else:
                # block-style (rare) — skip until next top-level key
                end = _next_top_level_index(lines, i + 1)
                # We don't reconstruct multi-line scalar here; treat as empty.
                level_value = ""
                i = end
                last_oncokb_block_end = len(new_lines)
                continue

        if _is_top_level_key(line, "oncokb_snapshot_version"):
            inline = _split_top_level_key_value(line, "oncokb_snapshot_version")
            if inline:
                snapshot_value = _strip_yaml_scalar(inline)
                i += 1
                last_oncokb_block_end = len(new_lines)
                continue
            else:
                end = _next_top_level_index(lines, i + 1)
                snapshot_value = ""
                i = end
                last_oncokb_block_end = len(new_lines)
                continue

        new_lines.append(line)
        i += 1

    # Build the inserted block.
    insertion: list[str] = []

    # Ensure prior content ends with a newline before insertion.
    if new_lines and not new_lines[-1].endswith("\n"):
        new_lines[-1] = new_lines[-1] + "\n"

    if level_value:
        insertion.append("evidence_sources:\n")
        insertion.append("  - source: SRC-ONCOKB\n")
        # Keep level value quoted for safety (it's e.g. "1", "2", "R1").
        insertion.append(f"    level: \"{level_value}\"\n")
        insertion.append("    evidence_ids: []\n")
        insertion.append("    direction: null\n")
        insertion.append("    significance: null\n")
        insertion.append(f"    note: \"{ONCOKB_NOTE}\"\n")

    if not has_review_flag:
        insertion.append("actionability_review_required: true\n")

    # Insert at the position where the oncokb block used to be.
    if last_oncokb_block_end < 0:
        last_oncokb_block_end = len(new_lines)

    final_lines = (
        new_lines[:last_oncokb_block_end] + insertion + new_lines[last_oncokb_block_end:]
    )

    path.write_text("".join(final_lines), encoding="utf-8")

    info = {
        "level": level_value,
        "snapshot": snapshot_value,
    }
    if not level_value:
        return ("migrated_no_level", info)
    return ("migrated", info)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main() -> int:
    bio_files = sorted(BIO_DIR.glob("bio_*.yaml"))
    bma_files = sorted(BMA_DIR.glob("bma_*.yaml"))

    print(f"BIO files: {len(bio_files)}")
    print(f"BMA files: {len(bma_files)}")

    bio_renamed = bio_already = bio_nofield = 0
    for p in bio_files:
        status = migrate_bio_file(p)
        if status == "renamed":
            bio_renamed += 1
            print(f"  [BIO renamed] {p.name}")
        elif status == "already_migrated":
            bio_already += 1
        elif status == "no_field":
            bio_nofield += 1

    bma_migrated = bma_no_level = bma_already = bma_nofield = 0
    no_level_examples: list[str] = []
    for p in bma_files:
        status, info = migrate_bma_file(p)
        if status == "migrated":
            bma_migrated += 1
        elif status == "migrated_no_level":
            bma_no_level += 1
            if len(no_level_examples) < 5:
                no_level_examples.append(p.name)
        elif status == "already_migrated":
            bma_already += 1
        elif status == "no_field":
            bma_nofield += 1

    print()
    print("=== BIO summary ===")
    print(f"  renamed:           {bio_renamed}")
    print(f"  already_migrated:  {bio_already}")
    print(f"  no_field:          {bio_nofield}")
    print()
    print("=== BMA summary ===")
    print(f"  migrated:          {bma_migrated}")
    print(f"  migrated_no_level: {bma_no_level}")
    print(f"  already_migrated:  {bma_already}")
    print(f"  no_field:          {bma_nofield}")
    if no_level_examples:
        print(f"  no_level examples: {no_level_examples}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
