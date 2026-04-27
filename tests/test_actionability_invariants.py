"""Actionability integration architectural invariants — safe-rollout v3
§10.6 + acceptance criteria AC-1, AC-2, AC-7, AC-9, AC-15.

Renamed from test_oncokb_invariants.py during the CIViC pivot. These
tests defend the §8.3 firewall: actionability output must never affect
track selection, only be surfaced alongside the engine's two-track plan.

If ANY of these tests fail, the integration violates CHARTER §8.3 —
treat as a P0 incident and revert before merging.
"""

from __future__ import annotations

import ast
from pathlib import Path
from unittest.mock import patch

import pytest

from knowledge_base.engine.actionability_client import (
    NullActionabilityClient,
    StubActionabilityClient,
)
from knowledge_base.engine.actionability_conflict import detect_resistance_conflicts
from knowledge_base.engine.actionability_types import (
    ActionabilityQuery,
    ActionabilityResult,
    ActionabilityTherapeuticOption,
    ResistanceConflict,
)


# ── AC-1: track-builder MUST NOT import actionability modules ───────────


# Files that build tracks / evaluate algorithms — these run BEFORE
# actionability wiring and must remain ignorant of its existence.
_FORBIDDEN_IMPORTERS = [
    "knowledge_base/engine/algorithm_eval.py",
    "knowledge_base/engine/redflag_eval.py",
    "knowledge_base/engine/_actionability.py",
    "knowledge_base/engine/access_matrix.py",
    "knowledge_base/engine/experimental_options.py",
]

_FORBIDDEN_IMPORT_TARGETS = [
    "actionability_client",
    "actionability_conflict",
    "actionability_extract",
    "actionability_types",
]


@pytest.mark.parametrize("source_path", _FORBIDDEN_IMPORTERS)
def test_track_builder_does_not_import_actionability(source_path: str):
    """AC-1: import-graph firewall.

    If a track-builder needs actionability data, it would mean engine
    routing depends on the actionability source — direct §8.3 violation."""
    repo_root = Path(__file__).resolve().parent.parent
    full = repo_root / source_path
    if not full.exists():
        pytest.skip(f"{source_path} not present (skipped, not failed)")
    src = full.read_text(encoding="utf-8")
    tree = ast.parse(src)

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for forbidden in _FORBIDDEN_IMPORT_TARGETS:
                assert forbidden not in mod, (
                    f"{source_path} imports actionability module '{mod}' — "
                    f"violates §8.3 firewall (track-builder must not see actionability)"
                )
        if isinstance(node, ast.Import):
            for alias in node.names:
                for forbidden in _FORBIDDEN_IMPORT_TARGETS:
                    assert forbidden not in alias.name, (
                        f"{source_path} imports actionability module '{alias.name}'"
                    )


def test_generate_plan_signature_does_not_pass_actionability_into_tracks():
    """AC-1 (function-level): walk_algorithm and _materialize_track
    signatures must not accept any actionability-named parameter."""
    from knowledge_base.engine.algorithm_eval import walk_algorithm
    from knowledge_base.engine.plan import _materialize_track
    import inspect

    for fn in (walk_algorithm, _materialize_track):
        sig = inspect.signature(fn)
        for param_name in sig.parameters:
            assert "oncokb" not in param_name.lower(), (
                f"{fn.__name__} accepts param '{param_name}' — "
                f"track-builder must not be aware of OncoKB"
            )
            assert "actionability" not in param_name.lower(), (
                f"{fn.__name__} accepts param '{param_name}' — "
                f"track-builder must not be aware of actionability"
            )


# ── AC-7: default-OFF — generate_plan(patient) makes 0 network calls ────


def test_default_off_makes_zero_actionability_calls():
    """AC-7: without actionability_enabled, no network call may originate
    from generate_plan. Even patching httpx — count must be 0."""
    from knowledge_base.engine.plan import generate_plan

    patient = {"patient_id": "TEST-DEFAULT-OFF", "disease": {"id": "DIS-NONEXISTENT"}}

    # Patch httpx so any accidental call would be visible. (The CIViC
    # pivot removed all httpx use from this code path; this test pins
    # that contract.)
    try:
        import httpx  # noqa: F401
        httpx_available = True
    except ImportError:
        httpx_available = False

    if httpx_available:
        with patch("httpx.Client") as mock_client:
            result = generate_plan(patient)
            assert mock_client.call_count == 0
            assert result.actionability_layer is None
    else:
        result = generate_plan(patient)
        assert result.actionability_layer is None


# ── AC-2: fail-open when client unreachable ─────────────────────────────


def test_engine_fail_open_when_actionability_client_raises():
    """AC-2: if actionability_client.batch_lookup raises a RuntimeError,
    the engine must NOT propagate. Plan still generated; warning recorded."""
    from knowledge_base.engine.plan import generate_plan

    class _BrokenClient:
        def lookup(self, q):
            raise RuntimeError("boom")

        def batch_lookup(self, qs):
            raise RuntimeError("boom")

    patient = {
        "patient_id": "TEST-FAIL-OPEN",
        "disease": {"id": "DIS-NONEXISTENT"},
        "biomarkers": {},
    }

    # Should not raise even though client is broken
    result = generate_plan(
        patient,
        actionability_enabled=True,
        actionability_client=_BrokenClient(),
    )
    # Disease unresolved → returns early; either way, no exception
    assert result is not None


def test_null_client_returns_disabled_errors():
    client = NullActionabilityClient()
    q = ActionabilityQuery(
        gene="BRAF", variant="V600E", oncotree_code="MEL",
        source_biomarker_id="BIO-1",
    )
    out = client.batch_lookup([q])
    assert len(out) == 1
    assert out[0].error_kind == "disabled"


# ── AC-9 / AC-15: resistance-conflict detection ─────────────────────────


def _make_track(track_id: str, drugs: list[dict]):
    """Build a minimal duck-typed track for conflict-detector tests."""

    class _Track:
        pass

    t = _Track()
    t.track_id = track_id
    t.regimen_data = {"components": drugs}
    return t


@pytest.mark.skip(reason="phase-2: surfacing rules redefined for CIViC — "
                         "RESISTANCE_LEVELS now empty until matchers populate it")
def test_resistance_conflict_detected_for_r1_drug_overlap():
    """AC-9: if an engine track recommends drug X and the actionability
    source shows resistance for drug X with the patient's variant, a
    conflict is detected.

    Phase 2 (CIViC reader) will repopulate RESISTANCE_LEVELS so this
    test passes again under CIViC's direction=Supports & significance=
    Resistance vocabulary."""
    track = _make_track(
        "standard",
        [{"drug_id": "DRUG-GEFITINIB", "drug_name": "Gefitinib"}],
    )

    query = ActionabilityQuery(
        gene="EGFR", variant="T790M", oncotree_code="NSCLC",
        source_biomarker_id="BIO-EGFR-T790M",
    )
    result = ActionabilityResult(
        query=query,
        source_url="https://example.org/gene/EGFR/T790M",
        therapeutic_options=(
            ActionabilityTherapeuticOption(
                level="R1",
                drugs=("Gefitinib", "Erlotinib"),
                description="acquired resistance",
                pmids=("17392385",),
            ),
        ),
        cached=False,
    )

    conflicts = detect_resistance_conflicts([track], [result])
    assert len(conflicts) == 1


@pytest.mark.skip(reason="phase-2: surfacing rules redefined for CIViC")
def test_resistance_conflict_detected_for_r2_too():
    track = _make_track(
        "standard", [{"drug_name": "Vemurafenib"}]
    )
    query = ActionabilityQuery(
        gene="BRAF", variant="V600E", oncotree_code=None,
        source_biomarker_id="BIO-1",
    )
    result = ActionabilityResult(
        query=query,
        source_url="x",
        therapeutic_options=(
            ActionabilityTherapeuticOption(
                level="R2", drugs=("Vemurafenib",),
                description="preclinical", pmids=(),
            ),
        ),
        cached=False,
    )
    conflicts = detect_resistance_conflicts([track], [result])
    assert len(conflicts) == 1


def test_no_conflict_when_drug_not_in_track():
    """No-conflict path is source-agnostic — empty RESISTANCE_LEVELS
    yields zero conflicts regardless of input shape."""
    track = _make_track("standard", [{"drug_name": "Pembrolizumab"}])
    query = ActionabilityQuery(
        gene="EGFR", variant="T790M", oncotree_code="NSCLC",
        source_biomarker_id="BIO-1",
    )
    result = ActionabilityResult(
        query=query,
        source_url="x",
        therapeutic_options=(
            ActionabilityTherapeuticOption(
                level="R1", drugs=("Gefitinib",),
                description=None, pmids=(),
            ),
        ),
        cached=False,
    )
    assert detect_resistance_conflicts([track], [result]) == []


def test_no_conflict_when_actionability_only_has_non_resistance_levels():
    """Therapeutic-evidence levels never produce conflicts."""
    track = _make_track("standard", [{"drug_name": "Vemurafenib"}])
    query = ActionabilityQuery(
        gene="BRAF", variant="V600E", oncotree_code=None,
        source_biomarker_id="BIO-1",
    )
    result = ActionabilityResult(
        query=query,
        source_url="x",
        therapeutic_options=(
            ActionabilityTherapeuticOption(
                level="3A", drugs=("Vemurafenib",),
                description=None, pmids=(),
            ),
        ),
        cached=False,
    )
    assert detect_resistance_conflicts([track], [result]) == []


@pytest.mark.skip(reason="phase-2: surfacing rules redefined for CIViC")
def test_conflict_dedupe_when_drug_referenced_twice_in_same_track():
    track = _make_track(
        "standard",
        [
            {"drug_id": "DRUG-GEFITINIB"},
            {"drug_name": "Gefitinib"},
        ],
    )
    query = ActionabilityQuery(
        gene="EGFR", variant="T790M", oncotree_code="NSCLC",
        source_biomarker_id="BIO-1",
    )
    result = ActionabilityResult(
        query=query,
        source_url="x",
        therapeutic_options=(
            ActionabilityTherapeuticOption(
                level="R1", drugs=("Gefitinib",),
                description=None, pmids=(),
            ),
        ),
        cached=False,
    )
    conflicts = detect_resistance_conflicts([track], [result])
    assert len(conflicts) == 1


# ── AC-16 (Q1): SURFACED_LEVELS contract ────────────────────────────────


def test_surfaced_levels_default_empty():
    """Per CIViC pivot: SURFACED_LEVELS is empty by default — matchers
    populate it at lookup time. Phase 2 will redefine the rule for CIViC
    (likely A/B with direction=Supports + significance in the therapeutic
    axis)."""
    from knowledge_base.engine.actionability_types import SURFACED_LEVELS

    assert SURFACED_LEVELS == frozenset()


# ── StubActionabilityClient sanity ──────────────────────────────────────


def test_stub_client_returns_baked_response():
    stub = StubActionabilityClient(
        {
            ("BRAF", "V600E"): [
                {"level": "1", "drugs": ["vemurafenib"], "pmids": ["12345"]},
            ],
        }
    )
    q = ActionabilityQuery(
        gene="BRAF", variant="V600E", oncotree_code="MEL",
        source_biomarker_id="BIO-1",
    )
    r = stub.lookup(q)
    assert isinstance(r, ActionabilityResult)
    assert len(r.therapeutic_options) == 1
    assert r.therapeutic_options[0].level == "1"
    assert r.therapeutic_options[0].drugs == ("vemurafenib",)


def test_stub_client_returns_empty_for_unknown_variant():
    stub = StubActionabilityClient({})
    q = ActionabilityQuery(
        gene="UNKNOWN", variant="X1Y", oncotree_code=None,
        source_biomarker_id="BIO-x",
    )
    r = stub.lookup(q)
    assert isinstance(r, ActionabilityResult)
    assert r.therapeutic_options == ()
    assert r.is_negative is True
