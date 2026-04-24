"""Algorithm decision-tree walker.

Algorithm.decision_tree is a list of steps. Each step:

    - step: 1
      evaluate:
        any_of:  [ {red_flag: RF-X}, {red_flag: RF-Y}, <nested clause> ]
        all_of:  [ ... ]
      if_true:
        result: IND-X         # select this Indication
        # or
        next_step: N
      if_false:
        result: IND-Y
        # or
        next_step: N

Evaluation starts at step 1 (or the first in list). Traversal ends when
a step resolves to `result`. If all steps fall through with no resolution,
return the Algorithm's `default_indication`.

`trace` records each step's outcome — the structured audit of why a
particular Indication was selected.
"""

from __future__ import annotations

from typing import Any

from .redflag_eval import _eval_clause as _eval_plain_clause


def _eval_step_clause(clause: dict, findings: dict[str, Any], redflag_lookup: dict[str, dict]) -> bool:
    """Evaluate a single clause that may reference {red_flag: RF-X}."""
    if not isinstance(clause, dict):
        return False

    if "red_flag" in clause:
        rf_id = clause["red_flag"]
        rf = redflag_lookup.get(rf_id)
        if rf is None:
            # Unknown RedFlag — treat as not-triggered (safer default)
            return False
        from .redflag_eval import evaluate_redflag_trigger

        return evaluate_redflag_trigger(rf.get("trigger") or {}, findings)

    # Nested group
    if "all_of" in clause:
        return all(_eval_step_clause(c, findings, redflag_lookup) for c in clause["all_of"])
    if "any_of" in clause:
        return any(_eval_step_clause(c, findings, redflag_lookup) for c in clause["any_of"])
    if "none_of" in clause:
        return not any(_eval_step_clause(c, findings, redflag_lookup) for c in clause["none_of"])

    # Fall through to plain-clause evaluator (threshold / value / condition)
    return _eval_plain_clause(clause, findings)


def _eval_step_evaluate(evaluate: dict, findings: dict[str, Any], redflag_lookup: dict[str, dict]) -> bool:
    """Evaluate the `evaluate:` block of a decision-tree step."""
    if not isinstance(evaluate, dict):
        return False

    parts: list[bool] = []
    if "all_of" in evaluate:
        parts.append(all(_eval_step_clause(c, findings, redflag_lookup) for c in evaluate["all_of"]))
    if "any_of" in evaluate:
        parts.append(any(_eval_step_clause(c, findings, redflag_lookup) for c in evaluate["any_of"]))
    if "none_of" in evaluate:
        parts.append(not any(_eval_step_clause(c, findings, redflag_lookup) for c in evaluate["none_of"]))

    if not parts:
        # No boolean group — treat the whole evaluate dict as one clause
        return _eval_step_clause(evaluate, findings, redflag_lookup)

    return all(parts)


def walk_algorithm(
    algorithm: dict,
    findings: dict[str, Any],
    redflag_lookup: dict[str, dict],
) -> tuple[str, list[dict]]:
    """Walk the decision tree, return (selected_indication_id, trace).

    `trace` is a list of per-step records: [{step, outcome, branch, ...}]
    """

    trace: list[dict] = []
    steps = {s.get("step", i + 1): s for i, s in enumerate(algorithm.get("decision_tree") or [])}
    if not steps:
        # No decision tree — fall back to default_indication
        default = algorithm.get("default_indication")
        trace.append({"step": None, "note": "no decision_tree; using default_indication", "result": default})
        return default, trace

    current_key = next(iter(steps))  # start at first step (by insertion order)
    visited: set = set()

    while current_key is not None:
        if current_key in visited:
            trace.append({"step": current_key, "note": "cycle detected, breaking"})
            break
        visited.add(current_key)

        step = steps.get(current_key)
        if step is None:
            trace.append({"step": current_key, "note": "step id not found, breaking"})
            break

        outcome = _eval_step_evaluate(step.get("evaluate") or {}, findings, redflag_lookup)
        branch = step.get("if_true") if outcome else step.get("if_false")
        trace.append({
            "step": current_key,
            "outcome": outcome,
            "branch": branch,
        })

        if not branch:
            break
        if "result" in branch:
            return branch["result"], trace
        if "next_step" in branch:
            current_key = branch["next_step"]
            continue
        break

    # Fell through — fall back to default_indication
    default = algorithm.get("default_indication")
    trace.append({"step": None, "note": "decision tree fell through; using default_indication", "result": default})
    return default, trace


__all__ = ["walk_algorithm"]
