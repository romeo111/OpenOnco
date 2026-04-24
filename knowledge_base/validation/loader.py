"""YAML loader + Pydantic validation + referential integrity check.

Usage:
    python -m knowledge_base.validation.loader knowledge_base/hosted/content
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from pydantic import ValidationError

from knowledge_base.schemas import ENTITY_BY_DIR


# Which fields on which entity types carry IDs that must resolve elsewhere.
# Keys are dir names under hosted/content/; values are the entity_dir_name
# of the target, expected in a specific field or nested path.
#
# This is explicit (not reflection-based) so we can control what we check
# and produce useful messages. Extend as entities grow.
REF_FIELDS: dict[str, list[tuple[str, str]]] = {
    # (dotted field path relative to YAML root, target entity dir)
    "indications": [
        ("recommended_regimen", "regimens"),
        ("applicable_to.disease_id", "diseases"),
        # sources is list[Citation]; handled specially
    ],
    "regimens": [
        # components list handled specially (list of RegimenComponent.drug_id)
        ("monitoring_schedule_id", "monitoring"),
    ],
    "algorithms": [
        ("applicable_to_disease", "diseases"),
        ("default_indication", "indications"),
        ("alternative_indication", "indications"),
        # output_indications handled specially (list)
    ],
    "contraindications": [
        # affects_indications, affects_drugs, affects_regimens handled specially
    ],
    "redflags": [
        # shifts_algorithm handled specially
    ],
    "supportive_care": [
        # standard_intervention.drug_id handled specially
    ],
    "monitoring": [
        ("linked_to_regimen", "regimens"),
    ],
    "biomarkers": [],
    "tests": [],
    "drugs": [],
    "diseases": [],
    "sources": [],
}


@dataclass
class LoadResult:
    entities_by_id: dict[str, dict] = field(default_factory=dict)
    # id -> {"type": "diseases", "data": {...raw yaml...}, "path": Path}
    schema_errors: list[tuple[Path, str]] = field(default_factory=list)
    ref_errors: list[tuple[Path, str]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not (self.schema_errors or self.ref_errors)


def _extract(obj: dict, dotted: str):
    cur = obj
    for part in dotted.split("."):
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur


def load_content(root: Path) -> LoadResult:
    """Walk hosted/content/, validate each YAML against its schema,
    then do a referential-integrity pass."""

    result = LoadResult()

    # Pass 1: load + validate
    for entity_dir, model in ENTITY_BY_DIR.items():
        d = root / entity_dir
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.yaml")):
            try:
                raw = yaml.safe_load(path.read_text(encoding="utf-8"))
            except yaml.YAMLError as e:
                result.schema_errors.append((path, f"YAML parse error: {e}"))
                continue

            if not isinstance(raw, dict):
                result.schema_errors.append((path, "Root is not a mapping"))
                continue

            try:
                model.model_validate(raw)
            except ValidationError as e:
                result.schema_errors.append((path, str(e)))
                continue

            entity_id = raw.get("id")
            if not entity_id:
                result.schema_errors.append((path, "Missing 'id' field"))
                continue
            if entity_id in result.entities_by_id:
                existing = result.entities_by_id[entity_id]["path"]
                result.schema_errors.append(
                    (path, f"Duplicate id '{entity_id}' — already seen at {existing}")
                )
                continue

            result.entities_by_id[entity_id] = {
                "type": entity_dir,
                "data": raw,
                "path": path,
            }

    # Pass 2: referential integrity
    by_type: dict[str, set[str]] = {}
    for eid, info in result.entities_by_id.items():
        by_type.setdefault(info["type"], set()).add(eid)

    def check_ref(path: Path, ref_id, target_type: str, field_label: str) -> None:
        if ref_id is None or ref_id == "":
            return
        if ref_id not in result.entities_by_id:
            result.ref_errors.append(
                (path, f"{field_label}: '{ref_id}' not found in any loaded entity")
            )
            return
        actual_type = result.entities_by_id[ref_id]["type"]
        if actual_type != target_type:
            result.ref_errors.append(
                (path,
                 f"{field_label}: '{ref_id}' found but as {actual_type}, expected {target_type}")
            )

    for eid, info in result.entities_by_id.items():
        etype = info["type"]
        data = info["data"]
        path = info["path"]

        for dotted, target in REF_FIELDS.get(etype, []):
            val = _extract(data, dotted)
            if val is None:
                continue
            check_ref(path, val, target, dotted)

        # Entity-specific special cases
        if etype == "regimens":
            for i, comp in enumerate(data.get("components") or []):
                check_ref(path, comp.get("drug_id"), "drugs", f"components[{i}].drug_id")
            for sid in data.get("mandatory_supportive_care") or []:
                check_ref(path, sid, "supportive_care", "mandatory_supportive_care[]")
        elif etype == "algorithms":
            for sid in data.get("output_indications") or []:
                check_ref(path, sid, "indications", "output_indications[]")
        elif etype == "indications":
            for i, cit in enumerate(data.get("sources") or []):
                if isinstance(cit, dict):
                    check_ref(path, cit.get("source_id"), "sources", f"sources[{i}].source_id")
                elif isinstance(cit, str):
                    check_ref(path, cit, "sources", f"sources[{i}]")
            for sid in data.get("hard_contraindications") or []:
                check_ref(path, sid, "contraindications", "hard_contraindications[]")
            for sid in data.get("red_flags_triggering_alternative") or []:
                check_ref(path, sid, "redflags", "red_flags_triggering_alternative[]")
            for sid in data.get("required_tests") or []:
                check_ref(path, sid, "tests", "required_tests[]")
            for sid in data.get("desired_tests") or []:
                check_ref(path, sid, "tests", "desired_tests[]")
        elif etype == "contraindications":
            for sid in data.get("affects_indications") or []:
                check_ref(path, sid, "indications", "affects_indications[]")
            for sid in data.get("affects_drugs") or []:
                check_ref(path, sid, "drugs", "affects_drugs[]")
            for sid in data.get("affects_regimens") or []:
                check_ref(path, sid, "regimens", "affects_regimens[]")
        elif etype == "redflags":
            for sid in data.get("shifts_algorithm") or []:
                check_ref(path, sid, "algorithms", "shifts_algorithm[]")
        elif etype == "supportive_care":
            si = data.get("standard_intervention")
            if isinstance(si, dict):
                check_ref(path, si.get("drug_id"), "drugs", "standard_intervention.drug_id")
            for alt in data.get("alternatives") or []:
                if isinstance(alt, dict):
                    check_ref(path, alt.get("drug_id"), "drugs", "alternatives[].drug_id")

        # Generic top-level sources list (lots of entities have it)
        if etype != "indications":  # already handled above for indications
            for i, sid in enumerate(data.get("sources") or []):
                if isinstance(sid, str):
                    check_ref(path, sid, "sources", f"sources[{i}]")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OpenOnco knowledge-base YAML content.")
    parser.add_argument(
        "root",
        type=Path,
        help="Path to hosted/content/ (the parent of diseases/, drugs/, etc.)",
    )
    parser.add_argument(
        "--strict", action="store_true", help="Exit non-zero on ref errors (on by default)."
    )
    args = parser.parse_args()

    if not args.root.is_dir():
        print(f"ERROR: not a directory: {args.root}", file=sys.stderr)
        return 2

    result = load_content(args.root)
    print(f"Loaded {len(result.entities_by_id)} entities.")

    by_type: dict[str, int] = {}
    for info in result.entities_by_id.values():
        by_type[info["type"]] = by_type.get(info["type"], 0) + 1
    for t, n in sorted(by_type.items()):
        print(f"  {t}: {n}")

    if result.schema_errors:
        print(f"\nSchema errors ({len(result.schema_errors)}):", file=sys.stderr)
        for path, msg in result.schema_errors:
            print(f"  {path}:\n    {msg}", file=sys.stderr)

    if result.ref_errors:
        print(f"\nReferential-integrity errors ({len(result.ref_errors)}):", file=sys.stderr)
        for path, msg in result.ref_errors:
            print(f"  {path}: {msg}", file=sys.stderr)

    if result.ok:
        print("\nOK — all entities valid, all references resolve.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
