#!/usr/bin/env python3
"""Verify that Algorithm decision gates are executable and auditable.

Prose-shaped legacy ``condition:`` clauses cannot be evaluated as clinical
predicates. They must be represented as ``clinician_confirmation`` mappings
with a stable ID, visible label, and legacy lookup label for backwards
compatibility with historical synthetic profiles.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

import yaml

from knowledge_base.engine.redflag_eval import _looks_like_prose_condition


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ALGORITHM_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "algorithms"
_CONFIRMATION_ID_RE = re.compile(r"^CC-[A-Z0-9]+(?:-[A-Z0-9]+)*-[A-F0-9]{12}$")


def _walk_clauses(value: Any, path: tuple[str, ...] = ()) -> Iterator[tuple[tuple[str, ...], dict]]:
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            yield from _walk_clauses(child, path + (str(key),))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_clauses(child, path + (str(index),))


def audit_algorithm_conditions(*, algorithm_dir: Path = DEFAULT_ALGORITHM_DIR) -> dict[str, Any]:
    """Return an audit report without mutating the knowledge base."""
    counts: Counter[str] = Counter()
    errors: list[str] = []
    confirmation_definitions: dict[str, tuple[str, str]] = {}
    files = sorted(algorithm_dir.glob("*.yaml"))

    for file_path in files:
        try:
            data = yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"{file_path.name}: unreadable YAML ({type(exc).__name__})")
            continue
        if not isinstance(data, dict):
            errors.append(f"{file_path.name}: root must be a mapping")
            continue
        algorithm_id = data.get("id") or file_path.stem
        for location, clause in _walk_clauses(data):
            location_text = ".".join(location) or "root"
            legacy = clause.get("condition")
            if isinstance(legacy, str):
                if _looks_like_prose_condition(legacy):
                    counts["legacy_prose"] += 1
                    errors.append(
                        f"{file_path.name}:{location_text}: legacy prose condition {legacy!r}"
                    )
                else:
                    counts["named_condition_lookup"] += 1

            if "clinician_confirmation" not in clause:
                continue
            counts["clinician_confirmation"] += 1
            confirmation = clause["clinician_confirmation"]
            if not isinstance(confirmation, dict):
                errors.append(
                    f"{file_path.name}:{location_text}: clinician_confirmation must be a mapping"
                )
                continue
            condition_id = confirmation.get("id")
            label = confirmation.get("label")
            legacy_label = confirmation.get("legacy_condition")
            if not isinstance(condition_id, str) or not _CONFIRMATION_ID_RE.fullmatch(condition_id):
                errors.append(
                    f"{file_path.name}:{location_text}: invalid clinician confirmation id {condition_id!r}"
                )
                continue
            if not isinstance(label, str) or not label.strip():
                errors.append(f"{file_path.name}:{location_text}: missing clinician confirmation label")
                continue
            if not isinstance(legacy_label, str) or legacy_label != label:
                errors.append(
                    f"{file_path.name}:{location_text}: legacy_condition must exactly preserve label"
                )
                continue
            definition = (label, legacy_label)
            prior = confirmation_definitions.setdefault(condition_id, definition)
            if prior != definition:
                errors.append(
                    f"{file_path.name}:{location_text}: conflicting definition for {condition_id}"
                )

    return {
        "summary": {
            "algorithm_files": len(files),
            "clinician_confirmations": counts["clinician_confirmation"],
            "named_condition_lookups": counts["named_condition_lookup"],
            "legacy_prose_conditions": counts["legacy_prose"],
            "unique_confirmation_ids": len(confirmation_definitions),
            "errors": len(errors),
        },
        "errors": errors,
    }


def _markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = ["# Algorithm condition audit", ""]
    for key in (
        "algorithm_files",
        "clinician_confirmations",
        "named_condition_lookups",
        "legacy_prose_conditions",
        "unique_confirmation_ids",
        "errors",
    ):
        lines.append(f"- {key.replace('_', ' ').capitalize()}: {summary[key]}")
    if report["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    args = parser.parse_args(argv)
    report = audit_algorithm_conditions()
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(_markdown(report), encoding="utf-8")
    summary = report["summary"]
    print(
        "Algorithm condition audit: "
        f"{summary['clinician_confirmations']} confirmations; "
        f"{summary['legacy_prose_conditions']} legacy prose; "
        f"{summary['errors']} error(s)"
    )
    for error in report["errors"]:
        print(f"ERROR {error}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
