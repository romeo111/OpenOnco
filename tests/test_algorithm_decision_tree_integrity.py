"""Tests for the Algorithm decision-tree integrity checks in loader.py.

Covers _check_algorithm_decision_tree_integrity (errors E1-E5, warnings
W1-W2) both against the real KB (no NEW algorithm contract errors) and with
small synthetic algorithm dicts that make each rule fire in isolation.
"""

from __future__ import annotations

from pathlib import Path

from knowledge_base.validation.loader import (
    LoadResult,
    _check_algorithm_decision_tree_integrity,
    load_content,
)

KB_ROOT = Path(__file__).parent.parent / "knowledge_base" / "hosted" / "content"


# --------------------------------------------------------------------------
# (a) Real KB: the new algorithm checks must add ZERO contract errors.
# --------------------------------------------------------------------------

def _algorithm_error_messages(result: LoadResult) -> list[str]:
    """Contract-error messages that name an algorithm decision-tree defect.

    The decision-tree check is the only producer of these substrings, so
    filtering on them isolates E1-E5 from the pre-existing routing / redflag /
    precedence contract errors."""
    needles = (
        "duplicate decision_tree step id",
        "is not a step id in decision_tree",
        "is not listed in output_indications",
        "does not resolve to a known Indication entity",
    )
    out: list[str] = []
    for _path, msg in result.contract_errors:
        if any(n in msg for n in needles):
            out.append(msg)
    return out


def test_real_kb_has_no_new_algorithm_contract_errors():
    result = load_content(KB_ROOT)
    algo_errors = _algorithm_error_messages(result)
    assert algo_errors == [], (
        "New algorithm decision-tree checks (E1-E5) fired on current content:\n"
        + "\n".join(algo_errors)
    )


# --------------------------------------------------------------------------
# Synthetic-input helpers.
# --------------------------------------------------------------------------

def _make_result(algo: dict, *, indications: list[str] | None = None) -> LoadResult:
    """Build a minimal LoadResult with one algorithm plus the given Indication
    entity ids, then run only the decision-tree integrity check."""
    result = LoadResult()
    result.entities_by_id["ALGO-TEST"] = {
        "type": "algorithms",
        "data": algo,
        "path": Path("algo_test.yaml"),
    }
    for ind_id in indications or []:
        result.entities_by_id[ind_id] = {
            "type": "indications",
            "data": {"id": ind_id},
            "path": Path(f"{ind_id}.yaml"),
        }
    _check_algorithm_decision_tree_integrity(result)
    return result


def _error_msgs(result: LoadResult) -> str:
    return "\n".join(m for _p, m in result.contract_errors)


def _warning_msgs(result: LoadResult) -> str:
    return "\n".join(m for _p, m in result.contract_warnings)


# --------------------------------------------------------------------------
# (b) Focused unit tests — one per check.
# --------------------------------------------------------------------------

def test_clean_algorithm_produces_no_errors_or_warnings():
    algo = {
        "id": "ALGO-TEST",
        "output_indications": ["IND-A", "IND-B"],
        "default_indication": "IND-A",
        "alternative_indication": "IND-B",
        "decision_tree": [
            {"step": 1, "if_true": {"result": "IND-A"},
             "if_false": {"next_step": 2}},
            {"step": 2, "if_true": {"result": "IND-B"},
             "if_false": {"result": "IND-A"}},
        ],
    }
    result = _make_result(algo, indications=["IND-A", "IND-B"])
    assert result.contract_errors == [], _error_msgs(result)
    assert result.contract_warnings == [], _warning_msgs(result)


def test_e1_duplicate_step_ids_octal_collision():
    # YAML would parse "01" -> int 1, colliding with an explicit 1. Simulate the
    # post-parse dict directly: two entries both keyed to int 1.
    algo = {
        "id": "ALGO-TEST",
        "output_indications": ["IND-A"],
        "decision_tree": [
            {"step": 1, "if_true": {"result": "IND-A"},
             "if_false": {"result": "IND-A"}},
            {"step": 1, "if_true": {"result": "IND-A"},
             "if_false": {"result": "IND-A"}},
        ],
    }
    result = _make_result(algo, indications=["IND-A"])
    msgs = _error_msgs(result)
    assert "duplicate decision_tree step id" in msgs, msgs
    # Reported once per colliding id.
    assert msgs.count("duplicate decision_tree step id") == 1, msgs


def test_e2_dangling_next_step():
    algo = {
        "id": "ALGO-TEST",
        "output_indications": ["IND-A"],
        "decision_tree": [
            {"step": 1, "if_true": {"result": "IND-A"},
             "if_false": {"next_step": 99}},  # no step 99
        ],
    }
    result = _make_result(algo, indications=["IND-A"])
    msgs = _error_msgs(result)
    assert "next_step=99 is not a step id in decision_tree" in msgs, msgs


def test_e3_result_not_in_output_indications():
    algo = {
        "id": "ALGO-TEST",
        "output_indications": ["IND-A"],
        "decision_tree": [
            {"step": 1, "if_true": {"result": "IND-B"},  # exists but not advertised
             "if_false": {"result": "IND-A"}},
        ],
    }
    result = _make_result(algo, indications=["IND-A", "IND-B"])
    msgs = _error_msgs(result)
    assert "result='IND-B' is not listed in output_indications" in msgs, msgs
    # IND-B is a real entity, so E5 must NOT fire for it.
    assert "does not resolve to a known Indication entity" not in msgs, msgs


def test_e4_default_and_alternative_not_in_output_indications():
    algo = {
        "id": "ALGO-TEST",
        "output_indications": ["IND-A"],
        "default_indication": "IND-X",       # not advertised
        "alternative_indication": "IND-Y",   # not advertised
        "decision_tree": [
            {"step": 1, "if_true": {"result": "IND-A"},
             "if_false": {"result": "IND-A"}},
        ],
    }
    result = _make_result(algo, indications=["IND-A", "IND-X", "IND-Y"])
    msgs = _error_msgs(result)
    assert "default_indication='IND-X' is not listed in output_indications" in msgs, msgs
    assert "alternative_indication='IND-Y' is not listed in output_indications" in msgs, msgs


def test_e5_result_references_nonexistent_indication():
    algo = {
        "id": "ALGO-TEST",
        "output_indications": ["IND-GHOST"],
        "decision_tree": [
            {"step": 1, "if_true": {"result": "IND-GHOST"},  # advertised but no entity
             "if_false": {"result": "IND-GHOST"}},
        ],
    }
    # No IND-GHOST entity registered -> E5 fires (E3 does not, since it IS in output).
    result = _make_result(algo, indications=[])
    msgs = _error_msgs(result)
    assert "result='IND-GHOST' does not resolve to a known Indication entity" in msgs, msgs
    assert "is not listed in output_indications" not in msgs, msgs


def test_w1_unreachable_step_is_warning_only():
    algo = {
        "id": "ALGO-TEST",
        "output_indications": ["IND-A", "IND-B"],
        "decision_tree": [
            {"step": 1, "if_true": {"result": "IND-A"},
             "if_false": {"result": "IND-B"}},   # both terminal — step 2 never targeted
            {"step": 2, "if_true": {"result": "IND-A"},
             "if_false": {"result": "IND-B"}},
        ],
    }
    result = _make_result(algo, indications=["IND-A", "IND-B"])
    assert result.contract_errors == [], _error_msgs(result)
    warns = _warning_msgs(result)
    assert "decision_tree step 2 is unreachable" in warns, warns


def test_w2_falsy_result_terminal_is_warning_only():
    algo = {
        "id": "ALGO-TEST",
        "output_indications": ["IND-A"],
        "decision_tree": [
            {"step": 1, "if_true": {"result": "IND-A"},
             "if_false": {"result": None}},       # falsy -> W2
            {"step": 2, "if_true": {"result": False},  # falsy -> W2
             "if_false": {"next_step": 1}},
        ],
    }
    result = _make_result(algo, indications=["IND-A"])
    assert result.contract_errors == [], _error_msgs(result)
    warns = _warning_msgs(result)
    assert "if_false.result is None (falsy)" in warns, warns
    assert "if_true.result is False (falsy)" in warns, warns
