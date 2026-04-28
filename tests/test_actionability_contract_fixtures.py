"""Contract tests against synthesized OncoKB-shape response fixtures.

Renamed from test_oncokb_contract_fixtures.py during the CIViC pivot.
The fixtures themselves stayed — they document the OncoKB IndicatorQueryResp
shape and remain useful for parser testing if a Phase 4 OncoKB-shape
reader ever needs validation. They lived under tests/fixtures/oncokb_responses/
and now live under tests/fixtures/actionability_responses/.

The Phase 1 pivot removed `HttpxOncoKBClient` and the proxy that fed it
(license conflict with CHARTER §2). Tests that exercised that client
end-to-end are skipped at the module level. The fixture-shape invariants
(every fixture is a valid IndicatorQueryResp; treatments[] have canonical
fields; provisional flag is set) still run — they're pure-data assertions
and survive the pivot.

Phase 2 will reuse the parsing-layer test once a CIViC-shape reader
lands; the OncoKB-shape parser test is preserved here for documentation
of what a Phase 4 OncoKB-compatible reader (if ever added) would have
to handle.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


_FIXTURES = (
    Path(__file__).resolve().parent / "fixtures" / "actionability_responses"
)


# ── Fixture inventory ──────────────────────────────────────────────────


def _list_fixtures() -> list[Path]:
    return sorted(_FIXTURES.glob("*.json"))


def test_fixtures_directory_populated():
    files = _list_fixtures()
    assert len(files) >= 12, f"expected >=12 fixtures, got {len(files)}"


# ── Shape invariants — every fixture must be parseable ─────────────────


@pytest.mark.parametrize("fixture_path", _list_fixtures(), ids=lambda p: p.name)
def test_fixture_loads_as_indicator_query_resp(fixture_path: Path):
    data = json.loads(fixture_path.read_text(encoding="utf-8"))

    # Top-level required fields per OncoKB IndicatorQueryResp shape
    for key in (
        "query", "geneExist", "variantExist", "oncogenic",
        "mutationEffect", "treatments", "dataVersion",
    ):
        assert key in data, f"{fixture_path.name}: missing top-level field '{key}'"

    # query has hugoSymbol + alteration (tumorType may be None for pan-tumor)
    assert "hugoSymbol" in data["query"]
    assert "alteration" in data["query"]


@pytest.mark.parametrize("fixture_path", _list_fixtures(), ids=lambda p: p.name)
def test_fixture_treatments_have_canonical_shape(fixture_path: Path):
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    for tx in data["treatments"]:
        # Annotator code accesses these four fields
        assert "level" in tx, "treatment missing 'level'"
        assert "drugs" in tx, "treatment missing 'drugs'"
        assert "pmids" in tx, "treatment missing 'pmids'"
        assert "abstracts" in tx, "treatment missing 'abstracts'"

        # Level format: must be LEVEL_X (X in {1, 2, 3A, 3B, 4, R1, R2})
        assert tx["level"].startswith("LEVEL_"), f"unexpected level format: {tx['level']!r}"
        suffix = tx["level"][len("LEVEL_"):]
        assert suffix in {"1", "2", "3A", "3B", "4", "R1", "R2"}, (
            f"unknown level suffix: {suffix!r}"
        )

        # Drugs must be objects with drugName (NOT flat strings)
        for drug in tx["drugs"]:
            assert isinstance(drug, dict), "drug entry must be object, not string"
            assert "drugName" in drug, "drug missing drugName"

        # PMIDs flat list of strings (or empty)
        assert isinstance(tx["pmids"], list)
        for p in tx["pmids"]:
            assert isinstance(p, str), f"pmid must be string, got {type(p).__name__}"


# ── Parsing layer reads fixture cleanly (parser shape contract) ────────


@pytest.mark.parametrize("fixture_path", _list_fixtures(), ids=lambda p: p.name)
def test_proxy_parsing_layer_handles_fixture(fixture_path: Path):
    """Mirror of the OncoKB-shape parsing logic. Pure-data test,
    independent of any client implementation."""
    data = json.loads(fixture_path.read_text(encoding="utf-8"))

    options: list[dict] = []
    for tx in data.get("treatments", []) or []:
        options.append({
            "level": str(tx.get("level") or "").replace("LEVEL_", "") or "?",
            "drugs": [d.get("drugName", "") for d in tx.get("drugs", []) or []],
            "description": tx.get("description") or None,
            "pmids": [str(p) for p in tx.get("pmids", []) or []],
        })

    # Every option must have a level + drugs
    for o in options:
        assert o["level"] in {"1", "2", "3A", "3B", "4", "R1", "R2", "?"}
        assert len(o["drugs"]) >= 1, f"option in {fixture_path.name} has no drugs"


# ── PROVISIONAL marker — refuse to silently treat as verified ──────────


def test_fixtures_carry_provisional_marker():
    """Every fixture must have the `_provisional: true` flag. The CIViC
    pivot removed the path that would have replaced these with real-curl
    captures; the flag stays as a documentation marker that this data is
    synthesized from API docs, not captured."""
    for f in _list_fixtures():
        data = json.loads(f.read_text(encoding="utf-8"))
        assert data.get("_provisional") is True, (
            f"{f.name} missing _provisional flag — these fixtures are "
            f"synthesized from OncoKB API docs and should stay flagged."
        )


# ── Httpx client end-to-end — skipped (HttpxOncoKBClient removed) ──────


@pytest.mark.skip(reason="phase-1: HttpxOncoKBClient removed during CIViC pivot. "
                         "Phase 2 will add CIViC-shape parser tests here.")
def test_httpx_client_parses_braf_v600e_mel_fixture():
    pass


@pytest.mark.skip(reason="phase-1: HttpxOncoKBClient removed during CIViC pivot.")
def test_httpx_client_handles_resistance_levels_in_egfr_t790m():
    pass


@pytest.mark.skip(reason="phase-1: HttpxOncoKBClient removed during CIViC pivot.")
def test_httpx_client_handles_pan_tumor_fixture():
    pass
