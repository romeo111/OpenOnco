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

    actual = findings.get(finding_key)

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


__all__ = ["evaluate_redflag_trigger"]
