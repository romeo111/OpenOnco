"""Resistance-conflict detector — safe-rollout v3 §6 (T3 mitigation).

Pure function. NO I/O. Detects when an engine-recommended drug appears
in actionability evidence flagged as "resistance" for one of the
patient's biomarkers.

Source-agnostic: the "drug X appears in resistance evidence for
biomarker Y" pattern works for any actionability source. CIViC encodes
resistance via direction=Supports & significance=Resistance; OncoKB
encodes via R1/R2 levels. Either way, the matcher only sees a
ResistanceConflict-eligible level token (matchers populate
RESISTANCE_LEVELS at lookup time).

This is the most safety-critical part of the actionability integration:
without it, a clinician scrolling top-down might miss resistance
evidence in the lower actionability section. Per CHARTER §15.2 C6
(automation-bias mitigation), conflicts must surface inline in the
track-card, not only in the actionability layer.

Wired by `generate_plan` after both `tracks` and
`actionability_layer.results` are populated. Output drives:
  - inline banner in render
  - ProvenanceEvent("resistance_conflict_detected") on the plan
  - MDT trigger: molecular_geneticist role added
"""

from __future__ import annotations

import re
from typing import Iterable

from .actionability_types import (
    ActionabilityLayer,
    ActionabilityResult,
    RESISTANCE_LEVELS,
    ResistanceConflict,
)


def _drugs_from_track_regimen(regimen_data: dict | None) -> set[str]:
    """Extract drug names referenced by a regimen. Lower-cased for
    case-insensitive comparison with reported drug names."""
    if not regimen_data:
        return set()
    out: set[str] = set()
    for comp in regimen_data.get("components") or []:
        if not isinstance(comp, dict):
            continue
        # Drug name as stored on the component (preferred name)
        name = comp.get("drug_name") or comp.get("name")
        if name:
            out.update(_drug_match_keys(name))
        # Drug ID — strip canonical prefix like "DRUG-VEMURAFENIB" → "vemurafenib"
        did = comp.get("drug_id")
        if did and isinstance(did, str):
            stripped = did.split("-", 1)[-1] if did.startswith("DRUG-") else did
            out.update(_drug_match_keys(stripped))
    return out


def _drug_match_keys(value: str | None) -> set[str]:
    if not value:
        return set()
    raw = str(value).strip().lower()
    compact = re.sub(r"[^a-z0-9]+", "", raw)
    keys = {raw}
    if compact:
        keys.add(compact)
    return keys


def _is_resistance_option(opt: ActionabilityTherapeuticOption) -> bool:
    if opt.level in RESISTANCE_LEVELS:
        return True
    description = (opt.description or "").lower()
    if "does not support" in description or "does_not_support" in description:
        return True
    return "resistance" in description


def detect_resistance_conflicts(
    tracks: Iterable,  # list[PlanTrack] — kept loose to avoid import cycle
    actionability_results: list[ActionabilityResult],
) -> list[ResistanceConflict]:
    """Pure. Returns conflicts where a track-recommended drug overlaps
    with resistance evidence from any actionability source for one of the
    patient's queried biomarkers.

    Comparison is case-insensitive. Both `drug_name` and `drug_id`
    (sans `DRUG-` prefix) on each regimen component are compared
    against actionability-source-reported drug names.

    A level is treated as a resistance level iff it appears in
    `RESISTANCE_LEVELS`. That set is populated by per-source matchers
    at lookup time (Phase 2 — CIViC reader will set it). Until that
    happens this function returns no conflicts (fail-quiet, not fail-loud)."""

    conflicts: list[ResistanceConflict] = []

    # Build (drug → list of (gene, variant, level, description)) index
    # from resistance-level results
    resistance_index: list[tuple[str, str, str, str, str | None]] = []
    for result in actionability_results:
        for opt in result.therapeutic_options:
            if not _is_resistance_option(opt):
                continue
            for drug in opt.drugs:
                for drug_key in _drug_match_keys(drug):
                    resistance_index.append(
                        (
                            drug_key,
                            result.query.gene,
                            result.query.variant,
                            opt.level,
                            opt.description,
                        )
                    )

    if not resistance_index:
        return conflicts

    seen: set[tuple[str, str, str, str, str]] = set()
    for track in tracks:
        track_id = getattr(track, "track_id", None) or "?"
        regimen = getattr(track, "regimen_data", None)
        track_drugs = _drugs_from_track_regimen(regimen)
        if not track_drugs:
            continue

        for drug_lower, gene, variant, level, description in resistance_index:
            if drug_lower not in track_drugs:
                continue
            key = (track_id, drug_lower, gene, variant, level)
            if key in seen:
                continue
            seen.add(key)
            conflicts.append(
                ResistanceConflict(
                    track_id=track_id,
                    drug=drug_lower,
                    gene=gene,
                    variant=variant,
                    level=level,
                    description=description,
                )
            )

    return conflicts


def annotate_layer_with_conflicts(
    layer: ActionabilityLayer,
    tracks: Iterable,
) -> ActionabilityLayer:
    """Convenience wrapper. Mutates and returns the layer for chaining."""
    layer.resistance_conflicts = detect_resistance_conflicts(tracks, layer.results)
    return layer


__all__ = [
    "detect_resistance_conflicts",
    "annotate_layer_with_conflicts",
]
