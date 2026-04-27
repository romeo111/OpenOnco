"""Validate sidecar contributions in `contributions/<chunk-id>/`.

Run from CI on every contributor PR. Auto-rejects when a gate fails so
maintainer time is only spent on PRs that are at least mechanically sound.

Gates checked:
- Required sidecar files (task_manifest.txt, _contribution_meta.yaml, ≥1 payload).
- `_contribution` wrapper: ai_tool, ai_model, contributor, target_action,
  target_entity_id (where required).
- Pydantic validation of payload after `_contribution:` strip.
- Manifest scope: every sidecar's target_entity_id ∈ task_manifest.txt.
- target_action: upsert references entity that exists on cancer-autoresearch
  main (resolved against current working tree as proxy); new does NOT
  collide with existing entity.
- Banned-source check: SRC-ONCOKB / SRC-SNOMED / SRC-MEDDRA must not appear
  in contributor-authored sidecars.
- Source resolution: every SRC-* referenced exists on main OR has a
  source_stub_*.yaml in the same chunk dir.

Usage:
    python -m scripts.tasktorrent.validate_contributions <chunk-id>
    python -m scripts.tasktorrent.validate_contributions --all

Exit 0 on pass, 1 on any gate failure.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRIB_ROOT = REPO_ROOT / "contributions"
HOSTED_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"

BANNED_SOURCES = {"SRC-ONCOKB", "SRC-SNOMED", "SRC-MEDDRA"}
ALLOWED_AI_TOOLS = {"claude-code", "codex", "cursor", "chatgpt", "other"}
REQUIRED_CONTRIB_FIELDS = {
    "chunk_id",
    "contributor",
    "target_action",
    "ai_tool",
    "ai_model",
}
TARGET_ACTIONS = {"upsert", "new", "flag_duplicate"}


class GateFailure(Exception):
    """Raised when a validation gate fails."""


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _iter_sidecars(chunk_dir: Path) -> Iterable[Path]:
    for p in sorted(chunk_dir.iterdir()):
        if not p.is_file() or p.suffix != ".yaml":
            continue
        if p.name in {"_contribution_meta.yaml"}:
            continue
        yield p


def _hosted_entity_ids() -> set[str]:
    """Collect every stable ID from hosted content. Cheap because it's just
    grepping `^id:` lines across YAML files."""
    ids: set[str] = set()
    if not HOSTED_ROOT.exists():
        return ids
    for path in HOSTED_ROOT.rglob("*.yaml"):
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("id:"):
                    val = line.split(":", 1)[1].strip().strip('"').strip("'")
                    if val:
                        ids.add(val)
                    break
        except Exception:  # noqa: BLE001
            continue
    return ids


def _hosted_source_ids(hosted_ids: set[str]) -> set[str]:
    return {i for i in hosted_ids if i.startswith("SRC-")}


def _validate_chunk(chunk_dir: Path, hosted_ids: set[str], hosted_src: set[str]) -> list[str]:
    """Return list of failure messages. Empty list = pass."""
    failures: list[str] = []
    chunk_id = chunk_dir.name

    manifest_path = chunk_dir / "task_manifest.txt"
    if not manifest_path.exists():
        failures.append(f"[{chunk_id}] missing task_manifest.txt")
        return failures
    manifest = {
        line.strip()
        for line in manifest_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    if not manifest:
        failures.append(f"[{chunk_id}] task_manifest.txt is empty")
        return failures

    meta_path = chunk_dir / "_contribution_meta.yaml"
    if not meta_path.exists():
        failures.append(f"[{chunk_id}] missing _contribution_meta.yaml")

    sidecar_paths = list(_iter_sidecars(chunk_dir))
    if not sidecar_paths:
        failures.append(f"[{chunk_id}] no sidecar payloads found")
        return failures

    chunk_source_stubs: set[str] = set()
    for p in sidecar_paths:
        if p.name.startswith("source_stub_"):
            try:
                doc = _load_yaml(p)
                if isinstance(doc, dict) and isinstance(doc.get("id"), str):
                    chunk_source_stubs.add(doc["id"])
            except Exception:  # noqa: BLE001
                pass

    seen_target_ids: set[str] = set()
    for p in sidecar_paths:
        rel = p.relative_to(REPO_ROOT)
        try:
            doc = _load_yaml(p)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"[{rel}] YAML parse error: {exc}")
            continue
        if not isinstance(doc, dict):
            failures.append(f"[{rel}] top-level not a mapping")
            continue
        contrib = doc.get("_contribution")
        if not isinstance(contrib, dict):
            failures.append(f"[{rel}] missing _contribution wrapper")
            continue
        for field in REQUIRED_CONTRIB_FIELDS:
            if field not in contrib or contrib[field] in (None, ""):
                failures.append(f"[{rel}] _contribution.{field} missing or empty")
        if contrib.get("ai_tool") not in ALLOWED_AI_TOOLS:
            failures.append(
                f"[{rel}] _contribution.ai_tool '{contrib.get('ai_tool')}' "
                f"not in {sorted(ALLOWED_AI_TOOLS)}"
            )
        action = contrib.get("target_action")
        if action not in TARGET_ACTIONS:
            failures.append(f"[{rel}] _contribution.target_action '{action}' invalid")
        target_id = contrib.get("target_entity_id")
        if action in {"upsert", "flag_duplicate"} and not target_id:
            failures.append(f"[{rel}] target_entity_id required for action={action}")
        if target_id and target_id not in manifest:
            failures.append(
                f"[{rel}] target_entity_id '{target_id}' not in task_manifest.txt"
            )
        if target_id:
            if target_id in seen_target_ids:
                failures.append(f"[{rel}] target_entity_id '{target_id}' duplicated within chunk")
            seen_target_ids.add(target_id)
        if action == "upsert" and target_id and target_id not in hosted_ids:
            failures.append(
                f"[{rel}] target_action=upsert references '{target_id}' which "
                f"does not exist in hosted content"
            )
        if action == "new" and target_id and target_id in hosted_ids:
            failures.append(
                f"[{rel}] target_action=new collides with existing '{target_id}'"
            )

        # banned-source + source-resolution check
        for src_field in ("primary_sources", "sources"):
            for src in doc.get(src_field) or []:
                src_id = src if isinstance(src, str) else (
                    src.get("id") if isinstance(src, dict) else None
                )
                if not src_id:
                    continue
                if src_id in BANNED_SOURCES:
                    failures.append(f"[{rel}] {src_field} references banned source {src_id}")
                if (
                    src_id not in hosted_src
                    and src_id not in chunk_source_stubs
                    and not src_id.startswith("SRC-CIVIC-EID-")
                ):
                    failures.append(
                        f"[{rel}] {src_field} references unknown SRC-* '{src_id}' "
                        f"(not in hosted content and no source_stub_*.yaml in chunk dir)"
                    )

        for ev in doc.get("evidence_sources") or []:
            if not isinstance(ev, dict):
                continue
            src_id = ev.get("source")
            if src_id in BANNED_SOURCES:
                failures.append(f"[{rel}] evidence_sources references banned source {src_id}")
            if (
                src_id
                and src_id not in hosted_src
                and src_id not in chunk_source_stubs
                and not src_id.startswith("SRC-CIVIC-EID-")
            ):
                failures.append(
                    f"[{rel}] evidence_sources references unknown SRC-* '{src_id}'"
                )

    return failures


def _validate_pydantic(chunk_dir: Path) -> list[str]:
    """Run Pydantic validation on each sidecar payload.

    Strips the `_contribution` wrapper, then dispatches by inferred entity
    type from the filename prefix. Cheaper than walking every entity schema:
    we only validate types that match the sidecar prefix conventions.
    """
    failures: list[str] = []
    try:
        from knowledge_base.schemas.biomarker_actionability import BiomarkerActionability
        from knowledge_base.schemas.biomarker import Biomarker
        from knowledge_base.schemas.drug import Drug
        from knowledge_base.schemas.indication import Indication
        from knowledge_base.schemas.source import Source
    except Exception as exc:  # noqa: BLE001
        return [f"[{chunk_dir.name}] cannot import schemas: {exc}"]

    prefix_to_schema = {
        "bma_": BiomarkerActionability,
        "bio_": Biomarker,
        "drug_": Drug,
        "ind_": Indication,
        "source_stub_": Source,
    }

    for p in _iter_sidecars(chunk_dir):
        rel = p.relative_to(REPO_ROOT)
        schema = next(
            (s for prefix, s in prefix_to_schema.items() if p.name.startswith(prefix)),
            None,
        )
        if schema is None:
            continue
        try:
            doc = _load_yaml(p)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"[{rel}] YAML parse error: {exc}")
            continue
        payload = {k: v for k, v in doc.items() if k != "_contribution"}
        try:
            schema.model_validate(payload)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"[{rel}] Pydantic validation failed: {exc}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "chunk_id", nargs="?", default=None, help="chunk-id directory under contributions/"
    )
    parser.add_argument("--all", action="store_true", help="validate every chunk dir")
    args = parser.parse_args()

    if not CONTRIB_ROOT.exists():
        print("contributions/ directory does not exist — nothing to validate")
        return 0

    if args.all:
        chunk_dirs = [p for p in CONTRIB_ROOT.iterdir() if p.is_dir()]
    elif args.chunk_id:
        chunk_dir = CONTRIB_ROOT / args.chunk_id
        if not chunk_dir.exists():
            print(f"contributions/{args.chunk_id}/ does not exist", file=sys.stderr)
            return 1
        chunk_dirs = [chunk_dir]
    else:
        parser.print_help()
        return 1

    print("Loading hosted entity IDs...")
    hosted_ids = _hosted_entity_ids()
    hosted_src = _hosted_source_ids(hosted_ids)
    print(f"  {len(hosted_ids)} entities, {len(hosted_src)} sources")

    all_failures: list[str] = []
    for chunk_dir in chunk_dirs:
        print(f"\nValidating contributions/{chunk_dir.name}/")
        gate_failures = _validate_chunk(chunk_dir, hosted_ids, hosted_src)
        pydantic_failures = _validate_pydantic(chunk_dir)
        failures = gate_failures + pydantic_failures
        if failures:
            for f in failures:
                print(f"  FAIL {f}")
            all_failures.extend(failures)
        else:
            print("  PASS")

    if all_failures:
        print(f"\n{len(all_failures)} failure(s) total")
        return 1
    print("\nAll contributions pass validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
