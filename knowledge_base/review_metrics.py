"""Current content-review metrics; historical counters confer no authority."""
from typing import Any, Mapping

from .schemas._review_readiness import eligible_signoffs
from .schemas._review_scope import entity_disease_ids

REVIEW_TYPES = {
    "indications": "Indication", "algorithms": "Algorithm",
    "regimens": "Regimen", "redflags": "RedFlag",
    "biomarker_actionability": "BiomarkerActionability",
}


def current_review_count(data: Mapping[str, Any], directory: str,
                         reviewers: Mapping[str, Mapping[str, Any]],
                         diseases: Mapping[str, Mapping[str, Any]]) -> int:
    """Use the same revision, authorization, scope and independence gate as reports."""
    kind = REVIEW_TYPES.get(directory)
    if kind is None:
        return 0
    contexts = entity_disease_ids(data, kind)
    # An unknown disease is not a verified scope context.
    if any(disease_id and disease_id not in diseases for disease_id in contexts):
        return 0
    lineage = diseases.get(contexts[0], {}).get("lineage") if len(contexts) == 1 else None
    return len(eligible_signoffs(
        data, reviewers, entity_type=kind, disease_lineage=lineage,
        revision_field="last_verified" if directory == "biomarker_actionability" else "last_reviewed",
    ))


def historical_review_counts(data: Mapping[str, Any]) -> tuple[int, int]:
    """Separate raw structured rows from legacy counters, without claiming validity."""
    raw = data.get("reviewer_signoffs")
    if isinstance(raw, list):
        return sum(isinstance(row, Mapping) for row in raw), 0
    if isinstance(raw, int) and not isinstance(raw, bool):
        return 0, max(0, raw)
    return 0, 0
