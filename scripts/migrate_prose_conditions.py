#!/usr/bin/env python3
"""Mechanically normalize prose-shaped Algorithm ``condition`` clauses.

The engine cannot safely infer predicates such as ``ECOG PS 0-2`` from an
English sentence. This migration preserves the original label and legacy
lookup compatibility, but makes the executable input an explicit
``clinician_confirmation`` with a stable ID.

Usage:
    python -m scripts.migrate_prose_conditions --check
    python -m scripts.migrate_prose_conditions --write
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from knowledge_base.engine.redflag_eval import _looks_like_prose_condition


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ALGORITHM_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "algorithms"
_LIST_CONDITION_RE = re.compile(
    r"^(?P<indent>\s*)-\s+condition:\s*(?P<value>.+?)\s*$"
)
_INLINE_CONDITION_RE = re.compile(
    r"^(?P<indent>\s*)-\s*\{\s*condition:\s*(?P<value>.+?)\s*\}\s*$"
)


@dataclass(frozen=True)
class MigrationReport:
    files_changed: int
    clauses_migrated: int
    legacy_prose_remaining: int


def confirmation_id(algorithm_id: str, label: str) -> str:
    """Return a readable deterministic ID for one original prose label."""
    safe_algorithm_id = re.sub(r"[^A-Z0-9]+", "-", algorithm_id.upper()).strip("-")
    digest = hashlib.sha256(label.encode("utf-8")).hexdigest()[:12].upper()
    return f"CC-{safe_algorithm_id}-{digest}"


def _count_legacy_prose(value: Any) -> int:
    if isinstance(value, dict):
        current = int(
            isinstance(value.get("condition"), str)
            and _looks_like_prose_condition(value["condition"])
        )
        return current + sum(_count_legacy_prose(child) for child in value.values())
    if isinstance(value, list):
        return sum(_count_legacy_prose(child) for child in value)
    return 0


def _parse_condition_literal(value: str) -> str | None:
    try:
        parsed = yaml.safe_load(value)
    except yaml.YAMLError:
        return None
    return parsed if isinstance(parsed, str) else None


def _replacement(indent: str, algorithm_id: str, label: str) -> str:
    condition_id = confirmation_id(algorithm_id, label)
    quoted = json.dumps(label, ensure_ascii=False)
    return "\n".join(
        (
            f"{indent}- clinician_confirmation:",
            f"{indent}    id: {condition_id}",
            f"{indent}    label: {quoted}",
            f"{indent}    legacy_condition: {quoted}",
        )
    )


def _migrate_text(text: str, algorithm_id: str) -> tuple[str, int]:
    output: list[str] = []
    replacements = 0
    for line in text.splitlines(keepends=True):
        newline = "\n" if line.endswith("\n") else ""
        bare_line = line[:-1] if newline else line
        match = _LIST_CONDITION_RE.match(bare_line) or _INLINE_CONDITION_RE.match(bare_line)
        if match:
            label = _parse_condition_literal(match.group("value"))
            if label is not None and _looks_like_prose_condition(label):
                output.append(_replacement(match.group("indent"), algorithm_id, label) + newline)
                replacements += 1
                continue
        output.append(line)
    return "".join(output), replacements


def migrate_prose_conditions(
    *, algorithm_dir: Path = DEFAULT_ALGORITHM_DIR, write: bool = False
) -> MigrationReport:
    """Plan or apply the lossless mechanical migration.

    All files are validated before any write occurs. A mismatch between the
    parsed inventory and raw-line replacements aborts the run rather than
    silently leaving a prose gate behind.
    """
    planned: list[tuple[Path, str, int]] = []
    legacy_before = 0
    for path in sorted(algorithm_dir.glob("*.yaml")):
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text) or {}
        if not isinstance(data, dict) or not isinstance(data.get("id"), str):
            raise ValueError(f"{path}: Algorithm YAML requires a string id")
        prose_count = _count_legacy_prose(data)
        legacy_before += prose_count
        migrated_text, replacements = _migrate_text(text, data["id"])
        if replacements != prose_count:
            raise ValueError(
                f"{path}: found {prose_count} prose condition clause(s) in YAML, "
                f"but only {replacements} raw-line replacement(s) are safe"
            )
        planned.append((path, migrated_text, replacements))

    if write:
        for path, migrated_text, replacements in planned:
            if replacements:
                path.write_text(migrated_text, encoding="utf-8")

    remaining = 0
    if write:
        for path, _, _ in planned:
            remaining += _count_legacy_prose(yaml.safe_load(path.read_text(encoding="utf-8")) or {})
        if remaining:
            raise RuntimeError(f"Migration left {remaining} prose condition clause(s)")
    else:
        remaining = legacy_before

    return MigrationReport(
        files_changed=sum(1 for _, _, count in planned if count),
        clauses_migrated=sum(count for _, _, count in planned),
        legacy_prose_remaining=remaining,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report unresolved prose clauses")
    mode.add_argument("--write", action="store_true", help="apply the mechanical migration")
    args = parser.parse_args(argv)
    report = migrate_prose_conditions(write=args.write)
    action = "Migrated" if args.write else "Found"
    print(
        f"{action} {report.clauses_migrated} prose clause(s) in "
        f"{report.files_changed} algorithm file(s); "
        f"{report.legacy_prose_remaining} remaining"
    )
    return 0 if args.write or report.legacy_prose_remaining == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
