"""RedFlag trigger evaluation.

A RedFlag.trigger looks like (simplified):

    type: symptom_composite | imaging_finding | lab_value | ...
    any_of:   [ <clause>, ... ]   # OR
    all_of:   [ <clause>, ... ]   # AND
    none_of:  [ <clause>, ... ]   # NAND (none must match)

Each clause is one of:
    {finding: "X", threshold: N, comparator: ">="}
    {finding: "X", value: True}
    {finding: "X", value: "some_string"}
    {all_of: [...]}  / {any_of: [...]}  (nested)
    {condition: "<free text>"}  — treated as a named condition lookup

`patient_findings` is a flat dict: {finding_name: value}. Values can be
numeric, boolean, or string.

This evaluator is intentionally tight:
- Unknown findings default to False (trigger doesn't fire if data absent).
- Unknown comparators raise.
- Free-text conditions are looked up in `patient_findings` by the exact
  condition string; if absent, treated as False.
"""

from __future__ import annotations

from typing import Any


_COMPARATORS = {
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
}


# RedFlag triggers and patient questionnaires evolved separately, so the
# same clinical concept ended up with different field names. Rather than
# rewrite hundreds of YAMLs, we resolve aliases at lookup time. A RF
# referencing `age_years` finds the value the questionnaire stored under
# `age` (and vice versa). Each entry maps a name → set of equivalents
# (any of which the engine will accept as the source of truth). Audit
# 2026-04-27 showed these 8 aliases close ~150 of 1396 unevaluated-RF
# hits across 65 questionnaires — biggest single lever short of new
# questionnaire content.
FINDING_ALIASES: dict[str, tuple[str, ...]] = {
    "age": ("age_years",),
    "age_years": ("age",),
    "ecog": ("ecog_status", "ecog_performance_status"),
    "ecog_status": ("ecog", "ecog_performance_status"),
    "ecog_performance_status": ("ecog", "ecog_status"),
    "comorbidity_count": ("comorbidities_count",),
    "comorbidities_count": ("comorbidity_count",),
    "severe_neuropathy_grade": ("peripheral_neuropathy_grade",),
    "peripheral_neuropathy_grade": ("severe_neuropathy_grade",),
    "ldh_ratio_to_uln": ("ldh_ulnratio",),
    "ldh_ulnratio": ("ldh_ratio_to_uln",),
    "bilirubin_uln_x": ("bilirubin_ratio_to_uln",),
    "bilirubin_ratio_to_uln": ("bilirubin_uln_x",),
    "hcv_status": ("hcv_rna", "anti_hcv", "BIO-HCV-RNA", "BIO-HCV-STATUS"),
    "hcv_rna": ("hcv_status", "anti_hcv", "BIO-HCV-RNA"),
    "anti_hcv": ("hcv_status", "hcv_rna", "BIO-HCV-STATUS"),
    "her2_status": ("BIO-HER2-SOLID", "BIO-HER2"),
    "BIO-HER2-SOLID": ("her2_status",),
    "hiv_status": ("hiv_serology", "BIO-HIV"),
    "hiv_serology": ("hiv_status", "BIO-HIV"),
    "tp53_mutation": ("BIO-TP53-MUTATION", "tp53_mut"),
    "BIO-TP53-MUTATION": ("tp53_mutation", "tp53_mut"),
    "bilirubin_uln_x": ("bilirubin_ratio_to_uln", "total_bilirubin_ulnratio"),
    "bilirubin_ratio_to_uln": ("bilirubin_uln_x", "total_bilirubin_ulnratio"),
    "total_bilirubin_ulnratio": ("bilirubin_uln_x", "bilirubin_ratio_to_uln"),
}


def _resolve_finding(findings: dict[str, Any], key: str) -> Any:
    """Read a finding by name, falling back to known aliases. Returns the
    raw value (None if absent). Used by both trigger evaluation and the
    data-quality `unevaluated_red_flags` calculation so they stay
    consistent — if a RF can fire on a value, it's also marked evaluable."""
    v = findings.get(key)
    if v not in (None, ""):
        return v
    for alias in FINDING_ALIASES.get(key, ()):
        v = findings.get(alias)
        if v not in (None, ""):
            return v
    return None


def _eval_clause(clause: dict, findings: dict[str, Any]) -> bool:
    if not isinstance(clause, dict):
        return False

    # Nested boolean groups
    if "all_of" in clause:
        return all(_eval_clause(c, findings) for c in clause["all_of"])
    if "any_of" in clause:
        return any(_eval_clause(c, findings) for c in clause["any_of"])
    if "none_of" in clause:
        return not any(_eval_clause(c, findings) for c in clause["none_of"])

    finding_key = clause.get("finding") or clause.get("condition")
    if finding_key is None:
        return False

    actual = _resolve_finding(findings, finding_key)

    if "threshold" in clause:
        if actual is None:
            return False
        comparator = clause.get("comparator", ">=")
        fn = _COMPARATORS.get(comparator)
        if fn is None:
            raise ValueError(f"Unknown comparator: {comparator}")
        try:
            return bool(fn(actual, clause["threshold"]))
        except TypeError:
            return False

    if "value" in clause:
        return actual == clause["value"]

    # Named condition with no threshold / value — truthy lookup
    return bool(actual)


def evaluate_redflag_trigger(trigger: dict, findings: dict[str, Any]) -> bool:
    """Evaluate a RedFlag.trigger dict against patient findings."""
    if not isinstance(trigger, dict):
        return False

    results: list[bool] = []

    if "all_of" in trigger:
        results.append(all(_eval_clause(c, findings) for c in trigger["all_of"]))
    if "any_of" in trigger:
        results.append(any(_eval_clause(c, findings) for c in trigger["any_of"]))
    if "none_of" in trigger:
        results.append(not any(_eval_clause(c, findings) for c in trigger["none_of"]))

    if not results:
        # No boolean group at top level — interpret the trigger itself as a single clause
        return _eval_clause(trigger, findings)

    # Multiple groups at top level are AND-combined
    return all(results)


# ── Conflict resolution (P2) ─────────────────────────────────────────────
# When two or more RedFlags fire in the same Algorithm step with conflicting
# clinical_directions, resolve deterministically. Spec: REDFLAG_AUTHORING_GUIDE §5.

_DIRECTION_PRECEDENCE = {
    "hold": 0,           # highest priority — contraindication wins
    "intensify": 1,
    "de-escalate": 2,
    "investigate": 3,    # lowest — surveillance only
}

_SEVERITY_PRECEDENCE = {
    "critical": 0,
    "major": 1,
    "minor": 2,
}


def resolve_redflag_conflict(
    fired_ids: list[str],
    redflag_lookup: dict[str, dict],
) -> tuple[str | None, list[str]]:
    """Pick the winning RedFlag from a list of fired ones.

    Returns (winner_id, ordered_full_list). winner_id is None iff fired_ids
    is empty. ordered_full_list is the full input sorted by the same
    precedence (winner first), useful for trace logging.

    Order: clinical_direction precedence > severity > priority (lower = wins) > id.
    """
    if not fired_ids:
        return None, []

    def sort_key(rf_id: str) -> tuple:
        rf = redflag_lookup.get(rf_id) or {}
        direction = rf.get("clinical_direction", "investigate")
        severity = rf.get("severity", "major")
        priority = rf.get("priority", 100)
        return (
            _DIRECTION_PRECEDENCE.get(direction, 99),
            _SEVERITY_PRECEDENCE.get(severity, 99),
            priority,
            rf_id,
        )

    ordered = sorted(fired_ids, key=sort_key)
    return ordered[0], ordered


def is_redflag_applicable(redflag: dict, disease_id: str | None) -> bool:
    """Whether a RedFlag applies in the given disease context.

    Universal RFs use ``relevant_diseases: ["*"]``; concrete RFs list
    explicit disease IDs. RFs with empty ``relevant_diseases`` are treated
    as applicable everywhere (legacy compatibility).
    """
    rel = redflag.get("relevant_diseases") or []
    if not rel:
        return True
    if "*" in rel:
        return True
    return disease_id in rel if disease_id is not None else False


__all__ = [
    "evaluate_redflag_trigger",
    "resolve_redflag_conflict",
    "is_redflag_applicable",
    "FINDING_ALIASES",
    "_resolve_finding",
]
