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
    "workups": [
        # required_tests handled specially (list of Test IDs)
    ],
}


@dataclass
class LoadResult:
    entities_by_id: dict[str, dict] = field(default_factory=dict)
    # id -> {"type": "diseases", "data": {...raw yaml...}, "path": Path}
    schema_errors: list[tuple[Path, str]] = field(default_factory=list)
    ref_errors: list[tuple[Path, str]] = field(default_factory=list)
    contract_errors: list[tuple[Path, str]] = field(default_factory=list)
    contract_warnings: list[tuple[Path, str]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not (self.schema_errors or self.ref_errors or self.contract_errors)


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
        # Recursive — entity types like redflags/ permit subfolders
        # (e.g., redflags/universal/) for organizing cross-disease flags.
        for path in sorted(d.rglob("*.yaml")):
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
        elif etype == "workups":
            for sid in data.get("required_tests") or []:
                check_ref(path, sid, "tests", "required_tests[]")
            roles_block = data.get("triggers_mdt_roles") or {}
            # role IDs are NOT validated against KB entities — they're a
            # closed enum in mdt_orchestrator._ROLE_CATALOG, not KB content

        # Generic top-level sources list (lots of entities have it).
        # Drafts skip ref-check on sources because authors leave SRC-TODO
        # placeholders during scaffolding; the contract pass still emits
        # a draft warning so the work-in-progress is visible.
        if etype != "indications" and not data.get("draft"):
            for i, sid in enumerate(data.get("sources") or []):
                if isinstance(sid, str):
                    check_ref(path, sid, "sources", f"sources[{i}]")

    # Pass 3: entity-contract checks (semantics beyond schema)
    _check_redflag_contracts(result)
    _check_source_precedence_policy(result)

    return result


_VALID_DIRECTIONS = {"intensify", "de-escalate", "hold", "investigate"}
_VALID_SEVERITY = {"critical", "major", "minor"}


def _check_redflag_contracts(result: LoadResult) -> None:
    """RedFlag-specific contract validation (CHARTER §6.1, §8.3).

    Errors (block CI):
      - Non-draft RedFlag with empty sources (CHARTER §6.1 violation)
      - Unknown clinical_direction or severity value
      - relevant_diseases entry that doesn't resolve to a diseases/ entity
        (except "*" sentinel for universal RedFlags)
      - branch_targets key not present in shifts_algorithm

    Warnings (advisory):
      - draft: true RedFlag (kept loadable so authoring doesn't break)
      - shifts_algorithm non-empty but clinical_direction is "investigate"
        (investigate semantics shouldn't shift; flag for re-classification)
    """
    for eid, info in result.entities_by_id.items():
        if info["type"] != "redflags":
            continue
        data = info["data"]
        path = info["path"]

        is_draft = bool(data.get("draft"))

        sources = data.get("sources") or []
        if not is_draft and not sources:
            result.contract_errors.append(
                (path, f"{eid}: non-draft RedFlag missing sources (CHARTER §6.1)")
            )
        elif not is_draft and len(sources) < 2:
            result.contract_warnings.append(
                (path,
                 f"{eid}: only {len(sources)} source(s) — CLINICAL_CONTENT_STANDARDS §6.1 "
                 "asks for ≥2 independent Tier-1/2 sources for clinical content")
            )
        if is_draft:
            result.contract_warnings.append(
                (path, f"{eid}: draft — needs clinical review before merge")
            )

        direction = data.get("clinical_direction")
        if direction not in _VALID_DIRECTIONS:
            result.contract_errors.append(
                (path, f"{eid}: clinical_direction={direction!r} not in {sorted(_VALID_DIRECTIONS)}")
            )

        severity = data.get("severity", "major")
        if severity not in _VALID_SEVERITY:
            result.contract_errors.append(
                (path, f"{eid}: severity={severity!r} not in {sorted(_VALID_SEVERITY)}")
            )

        for d in data.get("relevant_diseases") or []:
            if d == "*":
                continue  # universal sentinel
            if d not in result.entities_by_id:
                result.contract_errors.append(
                    (path, f"{eid}: relevant_diseases entry {d!r} unresolved")
                )
                continue
            if result.entities_by_id[d]["type"] != "diseases":
                result.contract_errors.append(
                    (path,
                     f"{eid}: relevant_diseases entry {d!r} is "
                     f"{result.entities_by_id[d]['type']}, expected diseases")
                )

        algs = set(data.get("shifts_algorithm") or [])
        for alg_id in (data.get("branch_targets") or {}):
            if alg_id not in algs:
                result.contract_errors.append(
                    (path,
                     f"{eid}: branch_targets references {alg_id} which is not in shifts_algorithm")
                )

        if direction == "investigate" and algs:
            result.contract_warnings.append(
                (path,
                 f"{eid}: clinical_direction=investigate but shifts_algorithm is non-empty — "
                 "re-classify to intensify/de-escalate/hold or clear shifts_algorithm")
            )


_VALID_PRECEDENCE_POLICIES = {
    "leading",
    "confirmatory",
    "national_floor_only",
    "secondary_evidence_base",
}


def _check_source_precedence_policy(result: LoadResult) -> None:
    """Source.precedence_policy contract — Phase A invariant of
    docs/plans/ua_ingestion_and_alternatives_2026-04-26.md §0+§2.4.

    Errors (block CI):
      - Unknown precedence_policy value (typo guard)
      - Indication declared as default in some Algorithm cites a
        national_floor_only Source while a paralleled Tier-1/2 Source
        for the same disease+line_of_therapy scenario also exists in
        the KB. UA national guidelines must NOT outrank NCCN/ESMO when
        both cover the same patient situation.
    """

    # Index sources by id, with their precedence_policy + evidence_tier
    src_by_id: dict[str, dict] = {}
    for eid, info in result.entities_by_id.items():
        if info["type"] != "sources":
            continue
        src_by_id[eid] = info["data"]

    # Validate enum values
    for sid, sdata in src_by_id.items():
        pol = sdata.get("precedence_policy")
        if pol is not None and pol not in _VALID_PRECEDENCE_POLICIES:
            path = result.entities_by_id[sid]["path"]
            result.contract_errors.append((
                path,
                f"{sid}: precedence_policy={pol!r} not in "
                f"{sorted(_VALID_PRECEDENCE_POLICIES)}",
            ))

    # Build (disease_id, line_of_therapy) -> list of indication ids
    # for paralleled-source detection.
    by_scenario: dict[tuple[str, object], list[str]] = {}
    for iid, info in result.entities_by_id.items():
        if info["type"] != "indications":
            continue
        d = info["data"]
        applicable = d.get("applicable_to") or {}
        scenario = (
            applicable.get("disease_id"),
            applicable.get("line_of_therapy"),
        )
        if scenario[0] is None:
            continue
        by_scenario.setdefault(scenario, []).append(iid)

    # Identify indications that are reachable as default_indication of any algo
    default_inds: set[str] = set()
    for info in result.entities_by_id.values():
        if info["type"] != "algorithms":
            continue
        di = info["data"].get("default_indication")
        if di:
            default_inds.add(di)

    def _ind_source_ids(ind_data: dict) -> list[str]:
        out: list[str] = []
        for cit in ind_data.get("sources") or []:
            if isinstance(cit, dict):
                sid = cit.get("source_id")
                if sid:
                    out.append(sid)
            elif isinstance(cit, str):
                out.append(cit)
        return out

    for ind_id in default_inds:
        info = result.entities_by_id.get(ind_id)
        if info is None:
            continue
        ind_data = info["data"]
        ind_path = info["path"]
        ind_source_ids = _ind_source_ids(ind_data)
        if not ind_source_ids:
            continue

        # Does this default Indication rely SOLELY on national_floor_only
        # sources? (Mixed citations — e.g. МОЗ + NCCN — are fine: the Tier-1
        # source carries the recommendation, МОЗ adds national context.)
        all_floor = all(
            (src_by_id.get(sid) or {}).get("precedence_policy")
            == "national_floor_only"
            for sid in ind_source_ids
        )
        if not all_floor:
            continue

        # Is there a paralleled Indication for the same scenario that
        # cites a Tier-1/2 source (and is NOT itself national_floor_only)?
        applicable = ind_data.get("applicable_to") or {}
        scenario = (
            applicable.get("disease_id"),
            applicable.get("line_of_therapy"),
        )
        peers = by_scenario.get(scenario) or []

        has_better_peer = False
        for peer_id in peers:
            if peer_id == ind_id:
                continue
            peer_data = (result.entities_by_id.get(peer_id) or {}).get("data")
            if not peer_data:
                continue
            peer_src_ids = _ind_source_ids(peer_data)
            for sid in peer_src_ids:
                sdata = src_by_id.get(sid) or {}
                tier = sdata.get("evidence_tier")
                pol = sdata.get("precedence_policy")
                if pol == "national_floor_only":
                    continue
                if isinstance(tier, int) and tier in (1, 2):
                    has_better_peer = True
                    break
                if pol == "leading":
                    has_better_peer = True
                    break
            if has_better_peer:
                break

        if has_better_peer:
            result.contract_errors.append((
                ind_path,
                f"{ind_id}: default-Indication cites national_floor_only "
                f"Source while a paralleled Tier-1/2 Indication exists for "
                f"scenario disease={scenario[0]} line={scenario[1]}. "
                f"Re-rank the Tier-1/2 Indication as default, or move this "
                f"one to alternative_indication."
            ))


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

    if result.contract_errors:
        print(f"\nContract errors ({len(result.contract_errors)}):", file=sys.stderr)
        for path, msg in result.contract_errors:
            print(f"  {path}: {msg}", file=sys.stderr)

    if result.contract_warnings:
        print(f"\nContract warnings ({len(result.contract_warnings)}):", file=sys.stderr)
        for path, msg in result.contract_warnings:
            print(f"  {path}: {msg}", file=sys.stderr)

    if result.ok:
        print("\nOK — all entities valid, all references resolve.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
