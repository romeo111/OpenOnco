"""`applicable_to_disease_state` is a declared, closed-registry field.

It is a live routing key read by `engine/plan.py::_find_algorithm`, but it
used to be an *undeclared* extra field on the Algorithm model — `Base` sets
`extra="allow"`, so any value, including a typo, loaded silently.

That is not a cosmetic gap. The loader catches ValidationError and skips the
file, so an unregistered value drops the whole algorithm out of
`entities_by_id` — invisible to `_find_algorithm`. Because absence of the key
means "state-agnostic catch-all", losing the catch-all that way drops unstaged
patients into the legacy fallback, which picks by insertion order. For cervical
line 1 that swaps a palliative default for a curative-intent one. See
docs/reviews/disease-state-routing-policy-2026-07-18.md.

These tests pin the field as declared and enumerated so such a typo is a
load-time error.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from knowledge_base.schemas.algorithm import DISEASE_STATE_VALUES, Algorithm


def _algo(**overrides) -> dict:
    data = {
        "id": "ALGO-TEST-1L",
        "applicable_to_disease": "DIS-TEST",
        "applicable_to_line_of_therapy": 1,
        "output_indications": ["IND-TEST"],
    }
    data.update(overrides)
    return data


def test_field_is_declared_not_an_extra():
    assert "applicable_to_disease_state" in Algorithm.model_fields


def test_absent_state_means_catch_all_none():
    algo = Algorithm(**_algo())
    assert algo.applicable_to_disease_state is None


@pytest.mark.parametrize("value", sorted(DISEASE_STATE_VALUES))
def test_every_registered_value_is_accepted(value):
    algo = Algorithm(**_algo(applicable_to_disease_state=value))
    assert algo.applicable_to_disease_state == value


@pytest.mark.parametrize(
    "typo",
    [
        "metastaic",  # transposition
        "locally-advanced",  # hyphen instead of underscore
        "Metastatic",  # wrong case
        "mcrpc",  # wrong case, would still route (matcher lowercases)
        "",  # empty string
        "palliative",  # plausible but unregistered
    ],
)
def test_unregistered_value_is_rejected(typo):
    with pytest.raises(ValidationError):
        Algorithm(**_algo(applicable_to_disease_state=typo))


def test_registry_has_no_case_insensitive_collisions():
    """`_find_algorithm` lowercases both sides before comparing, so two
    registry values differing only in case would be indistinguishable at
    routing time even though the schema treats them as distinct."""
    lowered = [v.lower() for v in DISEASE_STATE_VALUES]
    assert len(set(lowered)) == len(lowered)


def test_every_value_in_the_live_kb_is_registered():
    """Guards the other direction: the registry must not fall behind the KB.

    A value present in a shipped algorithm but missing from the Literal
    would make the KB fail to load.
    """
    from pathlib import Path

    import yaml

    algo_dir = (
        Path(__file__).parent.parent
        / "knowledge_base"
        / "hosted"
        / "content"
        / "algorithms"
    )
    unregistered = {}
    for path in sorted(algo_dir.glob("*.yaml")):
        with path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        state = data.get("applicable_to_disease_state")
        if state is not None and state not in DISEASE_STATE_VALUES:
            unregistered[path.name] = state
    assert not unregistered, f"unregistered disease_state values: {unregistered}"
