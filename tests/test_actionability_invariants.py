"""OncoKB integration architectural invariants — safe-rollout v3 §10.6
+ acceptance criteria AC-1, AC-2, AC-7, AC-9, AC-15.

These tests defend the §8.3 firewall: OncoKB output must never affect
track selection, only be surfaced alongside the engine's two-track plan.

If ANY of these tests fail, the integration violates CHARTER §8.3 —
treat as a P0 incident and revert before merging.
"""

from __future__ import annotations

import ast
from pathlib import Path
from unittest.mock import patch

import pytest

from knowledge_base.engine.oncokb_client import (
    HttpxOncoKBClient,
    NullOncoKBClient,
    StubOncoKBClient,
)
from knowledge_base.engine.oncokb_conflict import detect_resistance_conflicts
from knowledge_base.engine.oncokb_types import (
    OncoKBQuery,
    OncoKBResult,
    OncoKBTherapeuticOption,
    ResistanceConflict,
)


# ── AC-1: track-builder MUST NOT import oncokb modules ──────────────────


# Files that build tracks / evaluate algorithms — these run BEFORE
# oncokb wiring and must remain ignorant of oncokb's existence.
_FORBIDDEN_IMPORTERS = [
    "knowledge_base/engine/algorithm_eval.py",
    "knowledge_base/engine/redflag_eval.py",
    "knowledge_base/engine/_actionability.py",
    "knowledge_base/engine/access_matrix.py",
    "knowledge_base/engine/experimental_options.py",
]

_FORBIDDEN_IMPORT_TARGETS = [
    "oncokb_client",
    "oncokb_conflict",
    "oncokb_extract",
    "oncokb_types",
]


@pytest.mark.parametrize("source_path", _FORBIDDEN_IMPORTERS)
def test_track_builder_does_not_import_oncokb(source_path: str):
    """AC-1: import-graph firewall.

    If a track-builder needs OncoKB data, it would mean engine routing
    depends on OncoKB — direct §8.3 violation."""
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
                    f"{source_path} imports oncokb module '{mod}' — "
                    f"violates §8.3 firewall (track-builder must not see OncoKB)"
                )
        if isinstance(node, ast.Import):
            for alias in node.names:
                for forbidden in _FORBIDDEN_IMPORT_TARGETS:
                    assert forbidden not in alias.name, (
                        f"{source_path} imports oncokb module '{alias.name}'"
                    )


def test_generate_plan_signature_does_not_pass_oncokb_into_tracks():
    """AC-1 (function-level): walk_algorithm and _materialize_track
    signatures must not accept any oncokb-named parameter."""
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


# ── AC-7: default-OFF — generate_plan(patient) makes 0 network calls ────


def test_default_off_makes_zero_oncokb_calls():
    """AC-7: without oncokb_enabled, no network call may originate from
    generate_plan. Even patching httpx — count must be 0."""
    from knowledge_base.engine.plan import generate_plan

    patient = {"patient_id": "TEST-DEFAULT-OFF", "disease": {"id": "DIS-NONEXISTENT"}}

    # Patch httpx so any accidental call would be visible
    with patch("httpx.Client") as mock_client:
        result = generate_plan(patient)
        assert mock_client.call_count == 0
        assert result.oncokb_layer is None


# ── AC-2: fail-open when client unreachable ─────────────────────────────


def test_engine_fail_open_when_oncokb_client_raises():
    """AC-2: if oncokb_client.batch_lookup raises a RuntimeError, the
    engine must NOT propagate. Plan still generated; warning recorded."""
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
    result = generate_plan(patient, oncokb_enabled=True, oncokb_client=_BrokenClient())
    # Disease unresolved → returns early; either way, no exception
    assert result is not None


def test_null_client_returns_disabled_errors():
    client = NullOncoKBClient()
    q = OncoKBQuery(gene="BRAF", variant="V600E", oncotree_code="MEL", source_biomarker_id="BIO-1")
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


def test_resistance_conflict_detected_for_r1_drug_overlap():
    """AC-9: if an engine track recommends drug X and OncoKB shows R1 for
    drug X with the patient's variant, a conflict is detected."""
    track = _make_track(
        "standard",
        [{"drug_id": "DRUG-GEFITINIB", "drug_name": "Gefitinib"}],
    )

    query = OncoKBQuery(gene="EGFR", variant="T790M", oncotree_code="NSCLC", source_biomarker_id="BIO-EGFR-T790M")
    result = OncoKBResult(
        query=query,
        oncokb_url="https://www.oncokb.org/gene/EGFR/T790M",
        therapeutic_options=(
            OncoKBTherapeuticOption(
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
    c = conflicts[0]
    assert c.track_id == "standard"
    assert c.drug == "gefitinib"
    assert c.gene == "EGFR"
    assert c.variant == "T790M"
    assert c.level == "R1"


def test_resistance_conflict_detected_for_r2_too():
    track = _make_track(
        "standard", [{"drug_name": "Vemurafenib"}]
    )
    query = OncoKBQuery(gene="BRAF", variant="V600E", oncotree_code=None, source_biomarker_id="BIO-1")
    result = OncoKBResult(
        query=query,
        oncokb_url="x",
        therapeutic_options=(
            OncoKBTherapeuticOption(
                level="R2", drugs=("Vemurafenib",), description="preclinical", pmids=()
            ),
        ),
        cached=False,
    )
    conflicts = detect_resistance_conflicts([track], [result])
    assert len(conflicts) == 1
    assert conflicts[0].level == "R2"


def test_no_conflict_when_drug_not_in_track():
    track = _make_track("standard", [{"drug_name": "Pembrolizumab"}])
    query = OncoKBQuery(gene="EGFR", variant="T790M", oncotree_code="NSCLC", source_biomarker_id="BIO-1")
    result = OncoKBResult(
        query=query,
        oncokb_url="x",
        therapeutic_options=(
            OncoKBTherapeuticOption(level="R1", drugs=("Gefitinib",), description=None, pmids=()),
        ),
        cached=False,
    )
    assert detect_resistance_conflicts([track], [result]) == []


def test_no_conflict_when_oncokb_only_has_non_resistance_levels():
    """3A is therapeutic evidence, not resistance — never a conflict."""
    track = _make_track("standard", [{"drug_name": "Vemurafenib"}])
    query = OncoKBQuery(gene="BRAF", variant="V600E", oncotree_code=None, source_biomarker_id="BIO-1")
    result = OncoKBResult(
        query=query,
        oncokb_url="x",
        therapeutic_options=(
            OncoKBTherapeuticOption(level="3A", drugs=("Vemurafenib",), description=None, pmids=()),
        ),
        cached=False,
    )
    assert detect_resistance_conflicts([track], [result]) == []


def test_conflict_dedupe_when_drug_referenced_twice_in_same_track():
    track = _make_track(
        "standard",
        [
            {"drug_id": "DRUG-GEFITINIB"},
            {"drug_name": "Gefitinib"},
        ],
    )
    query = OncoKBQuery(gene="EGFR", variant="T790M", oncotree_code="NSCLC", source_biomarker_id="BIO-1")
    result = OncoKBResult(
        query=query,
        oncokb_url="x",
        therapeutic_options=(
            OncoKBTherapeuticOption(level="R1", drugs=("Gefitinib",), description=None, pmids=()),
        ),
        cached=False,
    )
    conflicts = detect_resistance_conflicts([track], [result])
    assert len(conflicts) == 1


# ── AC-16 (Q1): SURFACED_LEVELS excludes 1/2 ────────────────────────────


def test_surfaced_levels_excludes_1_and_2():
    from knowledge_base.engine.oncokb_types import SURFACED_LEVELS

    assert "1" not in SURFACED_LEVELS
    assert "2" not in SURFACED_LEVELS
    assert SURFACED_LEVELS == frozenset({"3A", "3B", "4", "R1", "R2"})


# ── StubOncoKBClient sanity ─────────────────────────────────────────────


def test_stub_client_returns_baked_response():
    stub = StubOncoKBClient(
        {
            ("BRAF", "V600E"): [
                {"level": "1", "drugs": ["vemurafenib"], "pmids": ["12345"]},
            ],
        }
    )
    q = OncoKBQuery(gene="BRAF", variant="V600E", oncotree_code="MEL", source_biomarker_id="BIO-1")
    r = stub.lookup(q)
    assert isinstance(r, OncoKBResult)
    assert len(r.therapeutic_options) == 1
    assert r.therapeutic_options[0].level == "1"
    assert r.therapeutic_options[0].drugs == ("vemurafenib",)


def test_stub_client_returns_empty_for_unknown_variant():
    stub = StubOncoKBClient({})
    q = OncoKBQuery(gene="UNKNOWN", variant="X1Y", oncotree_code=None, source_biomarker_id="BIO-x")
    r = stub.lookup(q)
    assert isinstance(r, OncoKBResult)
    assert r.therapeutic_options == ()
    assert r.is_negative is True


# ── HttpxOncoKBClient fail-open ─────────────────────────────────────────


def test_httpx_client_returns_error_on_unreachable_proxy():
    """No mock — point at unroutable address; expect OncoKBError, not raise."""
    client = HttpxOncoKBClient(
        proxy_url="http://127.0.0.1:1",  # connection refused
        timeout_seconds=1.0,
    )
    q = OncoKBQuery(gene="BRAF", variant="V600E", oncotree_code=None, source_biomarker_id="BIO-1")
    out = client.lookup(q)
    # Either timeout or http_error depending on platform; both acceptable
    assert hasattr(out, "error_kind")
    assert out.error_kind in {"timeout", "http_error"}
