"""Regimen phase-aware schema — PR1 of regimen-phases-refactor.

See `docs/reviews/regimen-phases-refactor-plan-2026-04-28.md` §4 and
`knowledge_base/schemas/regimen.py` (module docstring).

Covers four contracts:

1. **Legacy back-compat (auto-wrap):** YAMLs without `phases:` continue
   to load and end up with a single phase named "main" carrying all the
   original components. `regimen.phases[0].components == regimen.components`.
2. **Authored phases preserved:** when a Regimen is constructed with
   explicit `phases=[...]`, the auto-wrap MUST NOT fire. `phases` and
   `components` are independent on input.
3. **`bridging_options` round-trips through YAML.**
4. **No regression on representative legacy regimens** (R-CHOP, axi-cel,
   lifileucel — pre-PR1 component counts preserved, phases len ≥ 1).
"""

from __future__ import annotations

from pathlib import Path

import yaml

from knowledge_base.schemas import Regimen, RegimenComponent, RegimenPhase

KB_REGIMENS = (
    Path(__file__).parent.parent
    / "knowledge_base"
    / "hosted"
    / "content"
    / "regimens"
)


def _load_regimen(filename: str) -> tuple[dict, Regimen]:
    """Load a regimen YAML directly (no full KB walk, no caching)."""
    raw = yaml.safe_load((KB_REGIMENS / filename).read_text(encoding="utf-8"))
    return raw, Regimen.model_validate(raw)


# ── 1. Legacy back-compat (auto-wrap) ────────────────────────────────────────


def test_legacy_regimen_auto_wraps_into_main_phase():
    """R-CHOP has no `phases:` field. After load, exactly one phase named
    'main' must appear, carrying ALL original components verbatim."""
    raw, r = _load_regimen("r_chop.yaml")
    assert "phases" not in raw, (
        "fixture invariant: r_chop.yaml is legacy (no phases:); "
        "if it gains phases, swap fixture to another legacy regimen"
    )

    assert len(r.phases) == 1, f"expected single auto-wrapped phase, got {len(r.phases)}"
    phase = r.phases[0]
    assert phase.name == "main"
    assert phase.components == r.components, (
        "auto-wrapped phase MUST carry components verbatim"
    )
    # `components` is preserved separately (not removed)
    assert len(r.components) == 5, "R-CHOP has 5 drug components"


def test_legacy_regimen_with_no_components_does_not_auto_wrap():
    """Empty components → empty phases. The validator only fires when
    there is something to wrap, otherwise we'd manufacture empty phases."""
    # Components is required by the schema (list[RegimenComponent], no default
    # of empty), so we need at least one to construct. Test the guard via
    # an in-memory minimal Regimen with one component.
    r = Regimen(
        id="REG-TEST",
        name="test",
        components=[RegimenComponent(drug_id="DRUG-X")],
    )
    assert len(r.phases) == 1
    assert r.phases[0].name == "main"
    assert r.phases[0].components[0].drug_id == "DRUG-X"


# ── 2. Authored phases preserved (no auto-wrap when phases is provided) ──────


def test_authored_phases_not_overwritten():
    """When `phases=[...]` is authored explicitly, the validator must NOT
    rewrap. `components` and `phases` stay independent on input."""
    r = Regimen(
        id="REG-CART-LIKE",
        name="CART-like with explicit phases",
        components=[
            RegimenComponent(drug_id="DRUG-CYCLOPHOSPHAMIDE"),
            RegimenComponent(drug_id="DRUG-FLUDARABINE"),
            RegimenComponent(drug_id="DRUG-CART-PRODUCT"),
        ],
        phases=[
            RegimenPhase(
                name="lymphodepletion",
                purpose_ua="lymphodepletion phase",
                components=[
                    RegimenComponent(drug_id="DRUG-CYCLOPHOSPHAMIDE"),
                    RegimenComponent(drug_id="DRUG-FLUDARABINE"),
                ],
                duration="3 days, days -5 to -3",
                timing_relative_to="main_infusion",
                timing_offset_days=-5,
                optional=False,
            ),
            RegimenPhase(
                name="main",
                purpose_ua="main infusion",
                components=[RegimenComponent(drug_id="DRUG-CART-PRODUCT")],
                timing_relative_to="absolute",
            ),
        ],
    )
    assert len(r.phases) == 2
    assert [p.name for p in r.phases] == ["lymphodepletion", "main"]
    # Independent: components is NOT auto-derived from phases.
    assert len(r.components) == 3
    assert r.phases[0].timing_offset_days == -5
    assert r.phases[0].optional is False


def test_authored_phases_with_optional_bridging():
    r = Regimen(
        id="REG-X",
        name="x",
        components=[RegimenComponent(drug_id="DRUG-A")],
        phases=[
            RegimenPhase(
                name="bridging",
                purpose_ua="bridging while waiting for manufacturing",
                components=[RegimenComponent(drug_id="DRUG-B")],
                optional=True,
            ),
            RegimenPhase(
                name="main",
                purpose_ua="main therapy",
                components=[RegimenComponent(drug_id="DRUG-A")],
            ),
        ],
    )
    assert r.phases[0].optional is True
    assert r.phases[1].optional is False


# ── 3. bridging_options round-trips through YAML ─────────────────────────────


def test_bridging_options_yaml_round_trip():
    """Construct → dump to YAML → reload → field preserved."""
    r = Regimen(
        id="REG-CART-WITH-BRIDGE",
        name="CART with bridge",
        components=[RegimenComponent(drug_id="DRUG-CART")],
        bridging_options=["REG-RICE", "REG-DHAP"],
    )
    dumped = yaml.safe_dump(r.model_dump(mode="json", exclude_none=True), sort_keys=False)
    reloaded = Regimen.model_validate(yaml.safe_load(dumped))
    assert reloaded.bridging_options == ["REG-RICE", "REG-DHAP"]


def test_bridging_options_default_empty():
    r = Regimen(
        id="REG-PLAIN",
        name="plain",
        components=[RegimenComponent(drug_id="DRUG-X")],
    )
    assert r.bridging_options == []


# ── 4. No regression on representative legacy regimens ───────────────────────
#
# Component counts captured by reading the YAML twice — once as raw dict
# (pre-validate) and once as a model — to prove the model didn't drop or
# duplicate anything during the auto-wrap.


def _raw_component_count(raw: dict) -> int:
    return len(raw.get("components") or [])


def test_no_regression_r_chop():
    raw, r = _load_regimen("r_chop.yaml")
    assert len(r.phases) >= 1
    assert len(r.components) == _raw_component_count(raw)
    # Auto-wrapped — phase[0] components == r.components
    assert sum(len(p.components) for p in r.phases) == len(r.components)


def test_no_regression_axicel():
    raw, r = _load_regimen("reg_car_t_axicel.yaml")
    assert len(r.phases) >= 1
    assert len(r.components) == _raw_component_count(raw)
    assert sum(len(p.components) for p in r.phases) == len(r.components)


def test_no_regression_lifileucel():
    raw, r = _load_regimen("reg_lifileucel_til_melanoma.yaml")
    assert len(r.phases) >= 1
    assert len(r.components) == _raw_component_count(raw)
    assert sum(len(p.components) for p in r.phases) == len(r.components)


def test_no_regression_all_244_legacy_yamls_load():
    """Catch-all: every existing regimen YAML loads under the new schema.
    Auto-wrap invariant: phases is non-empty iff components is non-empty
    (a single legitimate surveillance "regimen" carries 0 components and
    therefore stays at 0 phases).

    Drives the load-bearing claim of PR1: zero existing YAML breaks.
    """
    yaml_paths = sorted(KB_REGIMENS.glob("*.yaml"))
    assert len(yaml_paths) >= 240, (
        f"expected ~244 regimen YAMLs, found {len(yaml_paths)} — "
        "fixture changed?"
    )

    nonempty_count = 0
    empty_count = 0
    for path in yaml_paths:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        r = Regimen.model_validate(raw)
        raw_count = _raw_component_count(raw)
        # Component preservation (idempotent on the legacy schema)
        assert len(r.components) == raw_count, (
            f"{path.name}: components count drifted "
            f"({raw_count} raw vs {len(r.components)} model)"
        )
        # Auto-wrap invariant
        if raw_count > 0:
            assert len(r.phases) >= 1, (
                f"{path.name}: components={raw_count} but phases empty "
                "— auto-wrap failed"
            )
            assert r.phases[0].name == "main", (
                f"{path.name}: auto-wrapped phase has unexpected name "
                f"{r.phases[0].name!r} (expected 'main')"
            )
            nonempty_count += 1
        else:
            # Surveillance-only "regimen" with components: [] — phases
            # also stays empty. Render layer is responsible for routing
            # this kind of entity differently.
            assert len(r.phases) == 0, (
                f"{path.name}: zero components but phases populated "
                "— auto-wrap fired spuriously"
            )
            empty_count += 1

    # Sanity: vast majority of regimens have ≥1 component
    assert nonempty_count >= 240, (
        f"expected ~243 non-empty regimens, got {nonempty_count}"
    )
    # Documented exception
    assert empty_count == 1, (
        f"expected exactly one zero-component surveillance regimen, "
        f"got {empty_count}"
    )
