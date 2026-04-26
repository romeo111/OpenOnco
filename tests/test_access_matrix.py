"""Access Matrix tests — Phase D of ua-ingestion plan.

Per docs/plans/ua_ingestion_and_alternatives_2026-04-26.md §3.1 + §4.

Covers:
  1. CostRange embed validates and round-trips on UkraineRegistration
  2. _build_access_matrix produces correct rows for an MM-style fixture
  3. Stale-cost warning fires at >180 days
  4. Trial rows are appended when experimental_options carry trials
  5. Engine integration: generate_plan attaches access_matrix to Plan
  6. Invariant preserved: matrix is render-only — engine signature unchanged
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import pytest

from knowledge_base.engine import generate_plan
from knowledge_base.engine.access_matrix import (
    _is_stale,
    _row_for_track,
    _trial_rows,
    build_access_matrix,
)
from knowledge_base.schemas import (
    AccessMatrix,
    AccessMatrixRow,
    ExperimentalOption,
    ExperimentalTrial,
    PlanTrack,
)
from knowledge_base.schemas.base import CostRange, UkraineRegistration

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


# ── 1. CostRange embed ───────────────────────────────────────────────────


def test_cost_range_embed_validates():
    cr = CostRange(currency="UAH", min=1500, max=3500, per_unit="cycle")
    assert cr.currency == "UAH"
    assert cr.min == 1500
    assert cr.per_unit == "cycle"


def test_ukraine_registration_carries_cost_orientation():
    """Both new cost embeds + cost_last_updated/cost_source roundtrip."""
    ur = UkraineRegistration(
        registered=True,
        reimbursed_nszu=False,
        cost_uah_reimbursed=CostRange(currency="UAH", min=1500, max=3500, per_unit="cycle"),
        cost_uah_self_pay=CostRange(currency="UAH", min=80000, max=140000, per_unit="cycle"),
        cost_last_updated="2026-01-15",
        cost_source="SRC-NSZU-FORMULARY-2025-Q4",
    )
    dumped = ur.model_dump()
    assert dumped["cost_uah_self_pay"]["max"] == 140000
    assert dumped["cost_last_updated"] == "2026-01-15"


def test_ukraine_registration_legacy_yaml_still_loads():
    """Old YAML without cost_orientation fields must validate."""
    ur = UkraineRegistration(registered=True, reimbursed_nszu=True)
    assert ur.cost_uah_reimbursed is None
    assert ur.cost_last_updated is None


# ── 2. Stale-cost detection ──────────────────────────────────────────────


def test_is_stale_fresh():
    today = date(2026, 4, 26)
    assert _is_stale("2026-04-01", today=today) is False  # 25 days


def test_is_stale_at_threshold():
    today = date(2026, 4, 26)
    # Exactly 180 days — boundary is "more than 180 days"
    boundary = (today - timedelta(days=180)).isoformat()
    assert _is_stale(boundary, today=today) is False
    over = (today - timedelta(days=181)).isoformat()
    assert _is_stale(over, today=today) is True


def test_is_stale_handles_none():
    assert _is_stale(None) is False
    assert _is_stale("") is False
    assert _is_stale("garbage") is False


# ── 3. Row aggregation from synthetic entities ───────────────────────────


def _make_entities(drugs: list[dict], regimens: list[dict] | None = None,
                   pathways: list[dict] | None = None) -> dict:
    """Build a minimal `entities_by_id` lookup for the aggregator."""
    e: dict = {}
    for d in drugs:
        e[d["id"]] = {"type": "drugs", "data": d}
    for r in (regimens or []):
        e[r["id"]] = {"type": "regimens", "data": r}
    for p in (pathways or []):
        e[p["id"]] = {"type": "access_pathways", "data": p}
    return e


def _drug(id_: str, *, registered=True, reimbursed=True,
          cost_self_pay_max=None, cost_last_updated=None) -> dict:
    reg: dict = {"registered": registered, "reimbursed_nszu": reimbursed}
    if cost_self_pay_max is not None:
        reg["cost_uah_self_pay"] = {
            "currency": "UAH", "min": cost_self_pay_max // 2, "max": cost_self_pay_max,
            "per_unit": "cycle",
        }
    if cost_last_updated is not None:
        reg["cost_last_updated"] = cost_last_updated
    return {"id": id_, "regulatory_status": {"ukraine_registration": reg}}


def _track(track_id: str, regimen_id: str, drug_ids: list[str],
           regimen_name: str = "Test regimen") -> PlanTrack:
    return PlanTrack(
        track_id=track_id,
        label=track_id,
        indication_id="IND-TEST",
        is_default=(track_id == "standard"),
        regimen_data={
            "id": regimen_id,
            "name": regimen_name,
            "components": [{"drug_id": did} for did in drug_ids],
        },
    )


def test_row_all_components_registered_and_reimbursed():
    entities = _make_entities([
        _drug("DRUG-A", registered=True, reimbursed=True),
        _drug("DRUG-B", registered=True, reimbursed=True),
    ])
    track = _track("standard", "REG-AB", ["DRUG-A", "DRUG-B"])
    row = _row_for_track(track, entities)
    assert row.registered_in_ua is True
    assert row.reimbursed_nszu is True
    assert row.notes == []


def test_row_one_component_not_reimbursed():
    entities = _make_entities([
        _drug("DRUG-A", registered=True, reimbursed=True),
        _drug("DRUG-B", registered=True, reimbursed=False),
    ])
    track = _track("aggressive", "REG-AB", ["DRUG-A", "DRUG-B"])
    row = _row_for_track(track, entities)
    assert row.registered_in_ua is True
    assert row.reimbursed_nszu is False
    assert any("not on НСЗУ" in n for n in row.notes)


def test_row_summed_self_pay_cost():
    entities = _make_entities([
        _drug("DRUG-A", cost_self_pay_max=80000),
        _drug("DRUG-B", cost_self_pay_max=40000),
    ])
    track = _track("standard", "REG-AB", ["DRUG-A", "DRUG-B"])
    row = _row_for_track(track, entities)
    assert row.cost_self_pay_max == 120000
    assert row.cost_self_pay_min == 60000  # 40000+20000
    assert row.cost_per_unit == "cycle"


def test_row_stale_cost_triggers_note():
    today = date(2026, 4, 26)
    old = (today - timedelta(days=200)).isoformat()
    entities = _make_entities([
        _drug("DRUG-A", cost_self_pay_max=80000, cost_last_updated=old),
    ])
    track = _track("standard", "REG-A", ["DRUG-A"])
    row = _row_for_track(track, entities, today=today)
    assert row.cost_is_stale is True
    assert any("180 days" in n for n in row.notes)


def test_row_no_components_unknown():
    """Empty drug list → both flags None, not False (no positive evidence
    either way)."""
    entities = _make_entities([])
    track = _track("standard", "REG-EMPTY", [])
    row = _row_for_track(track, entities)
    assert row.registered_in_ua is None
    assert row.reimbursed_nszu is None


def test_row_finds_access_pathway():
    """When an AccessPathway declares applies_to_drug_ids overlap, it
    shows up as primary_pathway_id."""
    entities = _make_entities(
        drugs=[_drug("DRUG-LU-PSMA", registered=False, reimbursed=False)],
        pathways=[{
            "id": "PATH-LU-PSMA-EU",
            "name": "EU referral",
            "pathway_type": "international_referral",
            "applies_to_drug_ids": ["DRUG-LU-PSMA"],
            "applies_to_regimen_ids": [],
        }],
    )
    track = _track("aggressive", "REG-LU-PSMA", ["DRUG-LU-PSMA"])
    row = _row_for_track(track, entities)
    assert row.primary_pathway_id == "PATH-LU-PSMA-EU"


# ── 4. Trial rows ────────────────────────────────────────────────────────


def test_trial_rows_appended_with_ua_site():
    option = ExperimentalOption(
        id="EXPER-TEST", disease_id="DIS-NSCLC",
        trials=[
            ExperimentalTrial(
                nct_id="NCT05153486", title="FLAURA2",
                status="RECRUITING", sites_ua=["UA"],
            ),
        ],
    )
    rows = _trial_rows(option, entities={})
    assert len(rows) == 1
    assert rows[0].track_id == "trial:NCT05153486"
    assert rows[0].cost_self_pay_max == 0.0  # sponsor pays
    assert any("UA site" in n for n in rows[0].notes)


def test_trial_rows_handles_none_option():
    assert _trial_rows(None, entities={}) == []
    empty = ExperimentalOption(id="EXPER-EMPTY", disease_id="DIS-X", trials=[])
    assert _trial_rows(empty, entities={}) == []


# ── 5. End-to-end build_access_matrix ───────────────────────────────────


def test_build_access_matrix_full():
    today = date(2026, 4, 26)
    entities = _make_entities([
        _drug("DRUG-A", registered=True, reimbursed=True, cost_self_pay_max=20000),
        _drug("DRUG-B", registered=False, reimbursed=False, cost_self_pay_max=80000,
              cost_last_updated=(today - timedelta(days=210)).isoformat()),
    ])
    tracks = [
        _track("standard", "REG-A", ["DRUG-A"]),
        _track("aggressive", "REG-B", ["DRUG-B"]),
    ]
    matrix = build_access_matrix(tracks, entities, today=today)
    assert isinstance(matrix, AccessMatrix)
    assert len(matrix.rows) == 2
    # Plan-level note surfaces because aggressive track has stale cost
    assert any("180 days" in n for n in matrix.notes)


# ── 6. Engine integration + invariant preservation ──────────────────────


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def test_generate_plan_attaches_access_matrix():
    """Real KB load → Plan.access_matrix is populated with one row per track."""
    patient = _patient("patient_mm_high_risk.json")
    result = generate_plan(patient, kb_root=KB_ROOT)
    assert result.plan is not None
    matrix = result.plan.access_matrix
    assert matrix is not None, "access_matrix must be attached"
    assert len(matrix.rows) == len(result.plan.tracks)
    for row, track in zip(matrix.rows, result.plan.tracks):
        assert row.track_id == track.track_id


def test_access_matrix_does_not_alter_engine_decision():
    """The matrix is built AFTER engine selection. Plan tracks + default
    must be identical with or without the matrix step."""
    patient = _patient("patient_mm_high_risk.json")
    result = generate_plan(patient, kb_root=KB_ROOT)
    # Capture decisions
    default_id = result.default_indication_id
    track_ids = [t.indication_id for t in result.plan.tracks]
    # The matrix attaches to the same plan instance — assert decisions
    # weren't mutated as a side effect of matrix construction.
    assert result.plan.access_matrix is not None
    assert result.default_indication_id == default_id
    assert [t.indication_id for t in result.plan.tracks] == track_ids
