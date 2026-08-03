"""Deterministic release manifest and reference graph for the YAML KB.

The YAML files and Git history remain the authoring source of truth.  This
module creates read-only, reproducible artefacts from a validated load so a
release can be audited, searched, or mirrored to a future database without
making that database authoritative.  It never reads or writes patient data
and does not make clinical decisions.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
from pathlib import Path
from typing import Any

from knowledge_base.engine._claim_extraction import extract_claims
from knowledge_base.schemas import ENTITY_BY_DIR
from knowledge_base.validation.loader import (
    REVIEWER_SIGNOFF_TYPES,
    LoadResult,
    load_content,
)


MANIFEST_VERSION = "1.0"


def _content_hash(root: Path) -> str:
    """Hash YAML path+bytes in a stable order, independent of filesystem time."""
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*.yaml")):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _file_hash(path: Any) -> str | None:
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except (OSError, TypeError, ValueError):
        return None


def _walk_entity_refs(
    value: Any,
    known_ids: set[str],
    *,
    path: str = "",
) -> list[tuple[str, str]]:
    """Return ``(field_path, entity_id)`` pairs without inferring prose links."""
    if isinstance(value, str):
        return [(path, value)] if value in known_ids else []
    if isinstance(value, list):
        out: list[tuple[str, str]] = []
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]" if path else f"[{index}]"
            out.extend(_walk_entity_refs(child, known_ids, path=child_path))
        return out
    if isinstance(value, dict):
        out = []
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            out.extend(_walk_entity_refs(child, known_ids, path=child_path))
        return out
    return []


def _extension_field_inventory(entities: dict[str, dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Count fields admitted through ``extra='allow'`` for deliberate schema work."""
    inventory: dict[str, Counter[str]] = defaultdict(Counter)
    for info in entities.values():
        entity_type = str(info.get("type") or "")
        model = ENTITY_BY_DIR.get(entity_type)
        data = info.get("data") or {}
        if model is None or not isinstance(data, dict):
            continue
        known = set(model.model_fields)
        for field_name in data:
            if field_name not in known:
                inventory[entity_type][str(field_name)] += 1
    return {
        entity_type: dict(sorted(counts.items()))
        for entity_type, counts in sorted(inventory.items())
    }


def _review_summary(entities: dict[str, dict[str, Any]]) -> dict[str, int]:
    """Describe review metadata without treating it as endpoint access control."""
    eligible = 0
    structured_entries = 0
    legacy_counters = 0
    pending = 0
    for info in entities.values():
        if info.get("type") not in REVIEWER_SIGNOFF_TYPES:
            continue
        eligible += 1
        data = info.get("data") or {}
        signoffs = data.get("reviewer_signoffs") if isinstance(data, dict) else None
        if isinstance(signoffs, list):
            structured_entries += len(signoffs)
        elif isinstance(signoffs, int):
            legacy_counters += 1
        status = str(data.get("ukrainian_review_status") or "")
        if "pending_clinical_signoff" in status.casefold():
            pending += 1
    return {
        "signoff_eligible_entities": eligible,
        "structured_signoff_entries": structured_entries,
        "legacy_signoff_counters": legacy_counters,
        "pending_clinical_signoff_entities": pending,
    }


def _source_summary(entities: dict[str, dict[str, Any]]) -> dict[str, int]:
    sources = [info.get("data") or {} for info in entities.values() if info.get("type") == "sources"]
    return {
        "source_entities": len(sources),
        "with_doi": sum(bool(source.get("doi")) for source in sources),
        "with_pmid": sum(bool(source.get("pmid")) for source in sources),
        "with_url": sum(bool(source.get("url")) for source in sources),
        "legal_review_pending": sum(
            str((source.get("legal_review") or {}).get("status") or "pending") == "pending"
            for source in sources
            if isinstance(source, dict)
        ),
    }


def build_release_artifacts(
    kb_root: Path,
    *,
    strict_source_refs: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build deterministic manifest + graph from one validated KB snapshot."""
    result: LoadResult = load_content(kb_root, strict_source_refs=strict_source_refs)
    entities = result.entities_by_id
    known_ids = set(entities)
    entity_types = Counter(str(info.get("type") or "unknown") for info in entities.values())
    claims = extract_claims(result)

    nodes: list[dict[str, Any]] = []
    edges_by_key: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for entity_id, info in sorted(entities.items()):
        entity_type = str(info.get("type") or "unknown")
        path = info.get("path")
        try:
            relative_path = Path(path).relative_to(kb_root).as_posix()
        except (TypeError, ValueError):
            relative_path = str(path or "")
        nodes.append({
            "id": entity_id,
            "entity_type": entity_type,
            "path": relative_path,
            "content_hash": _file_hash(path),
        })
        for field_path, target_id in _walk_entity_refs(info.get("data") or {}, known_ids):
            if target_id == entity_id:
                continue
            target_type = str(entities[target_id].get("type") or "unknown")
            relation = "cites" if target_type == "sources" else "references"
            key = (entity_id, target_id, relation, field_path)
            edges_by_key[key] = {
                "from": entity_id,
                "to": target_id,
                "relation": relation,
                "field": field_path,
            }
    edges = [edges_by_key[key] for key in sorted(edges_by_key)]
    edge_counts = Counter(edge["relation"] for edge in edges)

    manifest: dict[str, Any] = {
        "manifest_version": MANIFEST_VERSION,
        "content_hash_sha256": _content_hash(kb_root),
        "entity_count": len(entities),
        "entities_by_type": dict(sorted(entity_types.items())),
        "validation": {
            "schema_errors": len(result.schema_errors),
            "reference_errors": len(result.ref_errors),
            "contract_errors": len(result.contract_errors),
            "contract_warnings": len(result.contract_warnings),
            "strict_source_refs": strict_source_refs,
        },
        "claim_grounding": {
            "claim_fields": len(claims),
            "anchored_claim_fields": sum(claim.has_anchor for claim in claims),
            "unanchored_claim_fields": sum(not claim.has_anchor for claim in claims),
        },
        "sources": _source_summary(entities),
        "clinical_review": _review_summary(entities),
        "schema_extensions": _extension_field_inventory(entities),
        "reference_graph": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "edges_by_relation": dict(sorted(edge_counts.items())),
        },
    }
    graph = {
        "graph_version": MANIFEST_VERSION,
        "content_hash_sha256": manifest["content_hash_sha256"],
        "nodes": nodes,
        "edges": edges,
    }
    return manifest, graph


__all__ = ["MANIFEST_VERSION", "build_release_artifacts"]
