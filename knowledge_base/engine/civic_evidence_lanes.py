"""CIViC evidence lane classification.

This module turns raw CIViC evidence items into OpenOnco display lanes. It is
deliberately conservative: CIViC-only evidence never becomes standard care
unless a caller passes an explicit non-CIViC confirmation flag.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class EvidenceLane(str, Enum):
    STANDARD_CARE = "standard_care"
    MOLECULAR_EVIDENCE_OPTION = "molecular_evidence_option"
    RESISTANCE_OR_AVOIDANCE_SIGNAL = "resistance_or_avoidance_signal"
    TRIAL_RESEARCH_OPTION = "trial_research_option"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


@dataclass(frozen=True)
class EvidenceLaneDecision:
    lane: EvidenceLane
    reason: str
    source_ids: tuple[str, ...] = ()
    evidence_level: str | None = None
    evidence_type: str | None = None
    evidence_direction: str | None = None
    significance: str | None = None


HIGH_CIVIC_LEVELS: frozenset[str] = frozenset({"A", "B"})
LOW_CIVIC_LEVELS: frozenset[str] = frozenset({"C", "D", "E"})
THERAPEUTIC_EVIDENCE_TYPE = "predictive"
STANDARD_CARE_CONFIRMING_SOURCE_PREFIXES: tuple[str, ...] = (
    "SRC-NCCN",
    "SRC-ESMO",
    "SRC-FDA",
    "SRC-EMA",
    "SRC-ASCO",
    "SRC-EAU",
    "SRC-EANO",
    "SRC-NCI",
)


def classify_civic_evidence_item(
    item: dict[str, Any],
    *,
    standard_care_confirmed: bool = False,
    standard_care_source_ids: tuple[str, ...] = (),
) -> EvidenceLaneDecision:
    """Classify one raw CIViC evidence item into an OpenOnco lane."""

    level = _clean(item.get("evidence_level")).upper()
    evidence_type = _clean(item.get("evidence_type"))
    direction = _clean(item.get("evidence_direction"))
    significance = _clean(item.get("significance"))
    therapies = _therapies(item.get("therapies"))
    source_ids = _source_ids(item)

    if _is_resistance(direction, significance):
        return _decision(
            EvidenceLane.RESISTANCE_OR_AVOIDANCE_SIGNAL,
            "CIViC evidence indicates resistance or lack of support.",
            source_ids,
            level,
            evidence_type,
            direction,
            significance,
        )

    is_predictive = evidence_type.lower() == THERAPEUTIC_EVIDENCE_TYPE
    supports = direction.lower() == "supports"

    if standard_care_confirmed and is_predictive and supports and therapies:
        return _decision(
            EvidenceLane.STANDARD_CARE,
            "Non-CIViC source confirms this CIViC-supported treatment as standard care.",
            tuple(dict.fromkeys((*source_ids, *standard_care_source_ids))),
            level,
            evidence_type,
            direction,
            significance,
        )

    if not therapies:
        return _decision(
            EvidenceLane.INSUFFICIENT_EVIDENCE,
            "CIViC item has no therapy attached; it cannot create a treatment option.",
            source_ids,
            level,
            evidence_type,
            direction,
            significance,
        )

    if not is_predictive:
        return _decision(
            EvidenceLane.INSUFFICIENT_EVIDENCE,
            "Non-predictive CIViC evidence cannot create a therapy recommendation by itself.",
            source_ids,
            level,
            evidence_type,
            direction,
            significance,
        )

    if supports and level in HIGH_CIVIC_LEVELS:
        return _decision(
            EvidenceLane.MOLECULAR_EVIDENCE_OPTION,
            "CIViC A/B predictive evidence supports a molecular option, not standard care.",
            source_ids,
            level,
            evidence_type,
            direction,
            significance,
        )

    if level in LOW_CIVIC_LEVELS:
        return _decision(
            EvidenceLane.TRIAL_RESEARCH_OPTION,
            "CIViC lower-tier evidence should route to trial or research review.",
            source_ids,
            level,
            evidence_type,
            direction,
            significance,
        )

    return _decision(
        EvidenceLane.INSUFFICIENT_EVIDENCE,
        "CIViC evidence does not meet a treatment-option lane rule.",
        source_ids,
        level or None,
        evidence_type,
        direction,
        significance,
    )


def classify_civic_evidence_source_ref(ref: dict[str, Any]) -> EvidenceLaneDecision:
    """Classify an existing BMA ``evidence_sources`` CIViC reference.

    Reconstruction stores bucket-level source refs, not full raw evidence
    items. Missing type/therapy fields are treated as predictive bucket
    evidence for reporting only; the lane still cannot become standard care.
    """

    persisted_lane = _clean(ref.get("evidence_lane"))
    if persisted_lane:
        try:
            lane = EvidenceLane(persisted_lane)
        except ValueError:
            lane = None
        if lane is not None:
            return _decision(
                lane,
                "BMA source ref already carries an explicit evidence lane.",
                tuple(f"SRC-CIVIC-EID-{eid}" for eid in ref.get("evidence_ids") or []),
                _clean(ref.get("level")).upper() or None,
                _clean(ref.get("evidence_type") or "Predictive"),
                _clean(ref.get("direction")),
                _clean(ref.get("significance")),
            )

    item = {
        "id": ",".join(str(eid) for eid in ref.get("evidence_ids") or []),
        "evidence_level": ref.get("level"),
        "evidence_type": ref.get("evidence_type") or "Predictive",
        "evidence_direction": ref.get("direction"),
        "significance": ref.get("significance"),
        "therapies": ["bucketed therapy"] if ref.get("note") else [],
    }
    return classify_civic_evidence_item(item)


def summarize_lanes(decisions: list[EvidenceLaneDecision]) -> tuple[str, ...]:
    """Return stable unique lane tokens for report metadata."""

    order = {
        EvidenceLane.STANDARD_CARE: 0,
        EvidenceLane.MOLECULAR_EVIDENCE_OPTION: 1,
        EvidenceLane.RESISTANCE_OR_AVOIDANCE_SIGNAL: 2,
        EvidenceLane.TRIAL_RESEARCH_OPTION: 3,
        EvidenceLane.INSUFFICIENT_EVIDENCE: 4,
    }
    lanes = {decision.lane for decision in decisions}
    return tuple(lane.value for lane in sorted(lanes, key=lambda lane: order[lane]))


def standard_care_confirming_source_ids(
    evidence_sources: list[dict[str, Any]] | tuple[dict[str, Any], ...] = (),
    primary_sources: list[str] | tuple[str, ...] = (),
) -> tuple[str, ...]:
    """Return non-CIViC source IDs that can confirm standard-care status.

    This helper is intentionally source-conservative: CIViC, OncoKB legacy
    rows, and generic literature rows do not upgrade a CIViC option to
    standard care. Guideline/regulatory source IDs can.
    """

    out: list[str] = []
    for ref in evidence_sources:
        if not isinstance(ref, dict):
            continue
        source_id = _clean(ref.get("source"))
        if _is_standard_care_confirming_source(source_id):
            out.append(source_id)
    for source_id in primary_sources:
        source_id = _clean(source_id)
        if _is_standard_care_confirming_source(source_id):
            out.append(source_id)
    return tuple(dict.fromkeys(out))


def _decision(
    lane: EvidenceLane,
    reason: str,
    source_ids: tuple[str, ...],
    level: str | None,
    evidence_type: str,
    direction: str,
    significance: str,
) -> EvidenceLaneDecision:
    return EvidenceLaneDecision(
        lane=lane,
        reason=reason,
        source_ids=source_ids,
        evidence_level=level or None,
        evidence_type=evidence_type or None,
        evidence_direction=direction or None,
        significance=significance or None,
    )


def _source_ids(item: dict[str, Any]) -> tuple[str, ...]:
    ids = []
    ev_id = _clean(item.get("id"))
    if ev_id:
        ids.append(f"SRC-CIVIC-EID-{ev_id}")
    citation = _clean(item.get("citation_id"))
    if citation:
        ids.append(citation)
    return tuple(ids)


def _therapies(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(therapy for therapy in (_clean(v) for v in value) if therapy)


def _is_resistance(direction: str, significance: str) -> bool:
    return direction.lower() == "does not support" or "resistance" in significance.lower()


def _is_standard_care_confirming_source(source_id: str) -> bool:
    source = source_id.upper()
    if not source or source.startswith(("SRC-CIVIC", "SRC-ONCOKB")):
        return False
    return any(source.startswith(prefix) for prefix in STANDARD_CARE_CONFIRMING_SOURCE_PREFIXES)


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


__all__ = [
    "EvidenceLane",
    "EvidenceLaneDecision",
    "classify_civic_evidence_item",
    "classify_civic_evidence_source_ref",
    "summarize_lanes",
    "standard_care_confirming_source_ids",
]
