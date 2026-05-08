"""CIViC snapshot inventory helpers.

The inventory is intentionally descriptive: it counts what is present in a
snapshot without making clinical decisions. Lane assignment lives in
``knowledge_base.engine.civic_evidence_lanes``.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class CIViCInventory:
    snapshot_date: str | None
    evidence_items: int
    accepted_evidence_items: int
    unique_molecular_profiles: int
    unique_gene_variant_pairs: int
    unique_genes: int
    therapy_bearing_evidence_items: int
    resistance_evidence_items: int
    evidence_level_distribution: dict[str, int] = field(default_factory=dict)
    evidence_type_distribution: dict[str, int] = field(default_factory=dict)
    evidence_direction_distribution: dict[str, int] = field(default_factory=dict)
    significance_distribution: dict[str, int] = field(default_factory=dict)
    top_genes_by_evidence: list[tuple[str, int]] = field(default_factory=list)
    top_disease_therapy_pairs: list[tuple[str, str, int]] = field(default_factory=list)


def load_civic_snapshot(path: Path | str) -> dict[str, Any]:
    """Load a CIViC YAML snapshot and validate the top-level shape."""

    snapshot_path = Path(path)
    with snapshot_path.open("r", encoding="utf-8") as f:
        payload = yaml.safe_load(f) or {}
    if not isinstance(payload, dict):
        raise ValueError(
            f"CIViC snapshot {snapshot_path} did not parse as a mapping; "
            f"got {type(payload).__name__}"
        )
    items = payload.get("evidence_items") or []
    if not isinstance(items, list):
        raise ValueError(
            f"CIViC snapshot {snapshot_path}: evidence_items is not a list"
        )
    return payload


def build_civic_inventory(
    snapshot: dict[str, Any],
    *,
    top_n: int = 20,
) -> CIViCInventory:
    """Build deterministic inventory counts from a loaded CIViC snapshot."""

    raw_items = snapshot.get("evidence_items") or []
    if not isinstance(raw_items, list):
        raise ValueError("snapshot evidence_items is not a list")
    items = [item for item in raw_items if isinstance(item, dict)]

    profiles: set[str] = set()
    gene_variant_pairs: set[tuple[str, str]] = set()
    genes: set[str] = set()
    level_counter: Counter[str] = Counter()
    type_counter: Counter[str] = Counter()
    direction_counter: Counter[str] = Counter()
    significance_counter: Counter[str] = Counter()
    gene_counter: Counter[str] = Counter()
    disease_therapy_counter: Counter[tuple[str, str]] = Counter()

    accepted = 0
    therapy_bearing = 0
    resistance = 0

    for item in items:
        if str(item.get("evidence_status") or "").strip().lower() == "accepted":
            accepted += 1

        profile = _clean(item.get("molecular_profile"))
        if profile:
            profiles.add(profile)

        gene = _clean(item.get("gene"))
        variant = _clean(item.get("variant"))
        if gene:
            genes.add(gene)
            gene_counter[gene] += 1
        if gene or variant:
            gene_variant_pairs.add((gene, variant))

        _count_nonempty(level_counter, item.get("evidence_level"))
        _count_nonempty(type_counter, item.get("evidence_type"))
        _count_nonempty(direction_counter, item.get("evidence_direction"))
        _count_nonempty(significance_counter, item.get("significance"))

        therapies = _clean_therapies(item.get("therapies"))
        if therapies:
            therapy_bearing += 1
            disease = _clean(item.get("disease")) or "Unknown disease"
            for therapy in therapies:
                disease_therapy_counter[(disease, therapy)] += 1

        if is_resistance_evidence(item):
            resistance += 1

    return CIViCInventory(
        snapshot_date=_clean(snapshot.get("snapshot_date")) or None,
        evidence_items=len(items),
        accepted_evidence_items=accepted,
        unique_molecular_profiles=len(profiles),
        unique_gene_variant_pairs=len(gene_variant_pairs),
        unique_genes=len(genes),
        therapy_bearing_evidence_items=therapy_bearing,
        resistance_evidence_items=resistance,
        evidence_level_distribution=dict(sorted(level_counter.items())),
        evidence_type_distribution=dict(
            sorted(type_counter.items(), key=lambda kv: (-kv[1], kv[0]))
        ),
        evidence_direction_distribution=dict(
            sorted(direction_counter.items(), key=lambda kv: (-kv[1], kv[0]))
        ),
        significance_distribution=dict(
            sorted(significance_counter.items(), key=lambda kv: (-kv[1], kv[0]))
        ),
        top_genes_by_evidence=_top_counter(gene_counter, top_n),
        top_disease_therapy_pairs=[
            (disease, therapy, count)
            for (disease, therapy), count in _top_counter(disease_therapy_counter, top_n)
        ],
    )


def build_civic_inventory_from_path(
    path: Path | str,
    *,
    top_n: int = 20,
) -> CIViCInventory:
    return build_civic_inventory(load_civic_snapshot(path), top_n=top_n)


def render_inventory_markdown(
    inventory: CIViCInventory,
    *,
    snapshot_label: str,
) -> str:
    """Render a compact review artifact for a snapshot inventory."""

    lines: list[str] = [
        f"# CIViC snapshot inventory - {inventory.snapshot_date or 'unknown date'}",
        "",
        f"Snapshot: `{snapshot_label}`",
        "",
        "## Summary",
        "",
        f"- Evidence items: **{inventory.evidence_items}**",
        f"- Accepted evidence items: **{inventory.accepted_evidence_items}**",
        f"- Unique molecular profiles: **{inventory.unique_molecular_profiles}**",
        f"- Unique gene/variant pairs: **{inventory.unique_gene_variant_pairs}**",
        f"- Unique genes: **{inventory.unique_genes}**",
        f"- Therapy-bearing evidence items: **{inventory.therapy_bearing_evidence_items}**",
        f"- Resistance evidence items: **{inventory.resistance_evidence_items}**",
        "",
    ]
    _append_counter_table(
        lines,
        "Evidence Level Distribution",
        inventory.evidence_level_distribution,
    )
    _append_counter_table(lines, "Evidence Type Distribution", inventory.evidence_type_distribution)
    _append_counter_table(
        lines,
        "Evidence Direction Distribution",
        inventory.evidence_direction_distribution,
    )
    _append_counter_table(lines, "Significance Distribution", inventory.significance_distribution)

    lines.extend(["## Top Genes By Evidence", "", "| gene | evidence items |", "|---|---:|"])
    for gene, count in inventory.top_genes_by_evidence:
        lines.append(f"| {gene} | {count} |")
    lines.append("")

    lines.extend(
        [
            "## Top Disease/Therapy Pairs",
            "",
            "| disease | therapy | evidence items |",
            "|---|---|---:|",
        ]
    )
    for disease, therapy, count in inventory.top_disease_therapy_pairs:
        lines.append(f"| {_md_escape(disease)} | {_md_escape(therapy)} | {count} |")
    lines.append("")

    return "\n".join(lines)


def is_resistance_evidence(item: dict[str, Any]) -> bool:
    direction = _clean(item.get("evidence_direction")).lower()
    significance = _clean(item.get("significance")).lower()
    return direction == "does not support" or "resistance" in significance


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _clean_therapies(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [therapy for therapy in (_clean(v) for v in value) if therapy]


def _count_nonempty(counter: Counter[str], value: Any) -> None:
    cleaned = _clean(value)
    if cleaned:
        counter[cleaned] += 1


def _top_counter(counter: Counter, top_n: int) -> list:
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:top_n]


def _append_counter_table(lines: list[str], title: str, counter: dict[str, int]) -> None:
    lines.extend([f"## {title}", "", "| value | count |", "|---|---:|"])
    for key, count in counter.items():
        lines.append(f"| {_md_escape(key)} | {count} |")
    lines.append("")


def _md_escape(value: str) -> str:
    return value.replace("|", "\\|")


__all__ = [
    "CIViCInventory",
    "build_civic_inventory",
    "build_civic_inventory_from_path",
    "is_resistance_evidence",
    "load_civic_snapshot",
    "render_inventory_markdown",
]
