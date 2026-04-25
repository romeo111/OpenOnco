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

Each trace entry records:
- step, outcome, branch (legacy fields, kept for backward compat)
- fired_red_flags: list of RedFlag IDs whose triggers evaluated True
  inside this step. Used by the MDT Orchestrator to emit per-RedFlag
  provenance events and to drive priority escalation
  (specs/MDT_ORCHESTRATOR_SPEC.md §3, §6.2).
"""

from __future__ import annotations

from typing import Any

from .redflag_eval import _eval_clause as _eval_plain_clause


def _eval_step_clause(
    clause: dict, findings: dict[str, Any], redflag_lookup: dict[str, dict]
) -> tuple[bool, list[str]]:
    """Evaluate a single clause that may reference {red_flag: RF-X}.

    Returns (outcome, fired_red_flag_ids). fired_red_flag_ids contains the
    RedFlag IDs that contributed to a True outcome. Empty for False
    outcome or for non-red_flag clauses.
    """
    if not isinstance(clause, dict):
        return False, []

    if "red_flag" in clause:
        rf_id = clause["red_flag"]
        rf = redflag_lookup.get(rf_id)
        if rf is None:
            # Unknown RedFlag — treat as not-triggered (safer default)
            return False, []
        from .redflag_eval import evaluate_redflag_trigger

        outcome = evaluate_redflag_trigger(rf.get("trigger") or {}, findings)
        return outcome, ([rf_id] if outcome else [])

    if "all_of" in clause:
        results = [_eval_step_clause(c, findings, redflag_lookup) for c in clause["all_of"]]
        outcome = all(r[0] for r in results)
        fired = [rf for ok, rfs in results if ok for rf in rfs] if outcome else []
        return outcome, fired

    if "any_of" in clause:
        results = [_eval_step_clause(c, findings, redflag_lookup) for c in clause["any_of"]]
        outcome = any(r[0] for r in results)
        fired = [rf for ok, rfs in results if ok for rf in rfs]
        return outcome, fired

    if "none_of" in clause:
        results = [_eval_step_clause(c, findings, redflag_lookup) for c in clause["none_of"]]
        outcome = not any(r[0] for r in results)
        # Nothing fires under none_of — by definition we want absence
        return outcome, []

    # Plain-clause evaluator (threshold / value / condition)
    return _eval_plain_clause(clause, findings), []


def _eval_step_evaluate(
    evaluate: dict, findings: dict[str, Any], redflag_lookup: dict[str, dict]
) -> tuple[bool, list[str]]:
    """Evaluate the `evaluate:` block of a decision-tree step. Returns
    (outcome, fired_red_flag_ids)."""
    if not isinstance(evaluate, dict):
        return False, []

    parts: list[bool] = []
    fired: list[str] = []
    if "all_of" in evaluate:
        sub = [_eval_step_clause(c, findings, redflag_lookup) for c in evaluate["all_of"]]
        ok = all(r[0] for r in sub)
        parts.append(ok)
        if ok:
            for r_ok, r_fired in sub:
                fired.extend(r_fired)
    if "any_of" in evaluate:
        sub = [_eval_step_clause(c, findings, redflag_lookup) for c in evaluate["any_of"]]
        ok = any(r[0] for r in sub)
        parts.append(ok)
        for r_ok, r_fired in sub:
            if r_ok:
                fired.extend(r_fired)
    if "none_of" in evaluate:
        sub = [_eval_step_clause(c, findings, redflag_lookup) for c in evaluate["none_of"]]
        ok = not any(r[0] for r in sub)
        parts.append(ok)
        # nothing fires under none_of

    if not parts:
        # No boolean group — treat the whole evaluate dict as one clause
        return _eval_step_clause(evaluate, findings, redflag_lookup)

    outcome = all(parts)
    seen: set[str] = set()
    unique_fired: list[str] = []
    for rf in fired:
        if rf not in seen:
            unique_fired.append(rf)
            seen.add(rf)
    return outcome, unique_fired


def walk_algorithm(
    algorithm: dict,
    findings: dict[str, Any],
    redflag_lookup: dict[str, dict],
) -> tuple[str, list[dict]]:
    """Walk the decision tree, return (selected_indication_id, trace).

    `trace` is a list of per-step records:
        {step, outcome, branch, fired_red_flags}
    """

    trace: list[dict] = []
    steps = {s.get("step", i + 1): s for i, s in enumerate(algorithm.get("decision_tree") or [])}
    if not steps:
        default = algorithm.get("default_indication")
        trace.append({
            "step": None,
            "note": "no decision_tree; using default_indication",
            "result": default,
            "fired_red_flags": [],
        })
        return default, trace

    current_key = next(iter(steps))
    visited: set = set()

    while current_key is not None:
        if current_key in visited:
            trace.append({
                "step": current_key,
                "note": "cycle detected, breaking",
                "fired_red_flags": [],
            })
            break
        visited.add(current_key)

        step = steps.get(current_key)
        if step is None:
            trace.append({
                "step": current_key,
                "note": "step id not found, breaking",
                "fired_red_flags": [],
            })
            break

        outcome, fired = _eval_step_evaluate(
            step.get("evaluate") or {}, findings, redflag_lookup
        )
        branch = step.get("if_true") if outcome else step.get("if_false")
        trace.append({
            "step": current_key,
            "outcome": outcome,
            "branch": branch,
            "fired_red_flags": fired,
        })

        if not branch:
            break
        if "result" in branch:
            return branch["result"], trace
        if "next_step" in branch:
            current_key = branch["next_step"]
            continue
        break

    default = algorithm.get("default_indication")
    trace.append({
        "step": None,
        "note": "decision tree fell through; using default_indication",
        "result": default,
        "fired_red_flags": [],
    })
    return default, trace


__all__ = ["walk_algorithm"]
