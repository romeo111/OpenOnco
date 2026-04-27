"""Contract tests against synthesized OncoKB response fixtures.

Phase 0 mock-mode deliverable. Locks the proxy parsing layer
(`services/oncokb_proxy/app.py:_call_oncokb`) and the engine client
(`HttpxOncoKBClient.lookup`) against the response shape we expect
from OncoKB.

When real-token curl captures replace the fixtures, these tests
should still pass — if they break, parsing needs adjustment.

Tests are decoupled from network — fixtures are local JSON.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "oncokb_responses"


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


# ── Parsing layer reads fixture → OncoKBResult cleanly ─────────────────


@pytest.mark.parametrize("fixture_path", _list_fixtures(), ids=lambda p: p.name)
def test_proxy_parsing_layer_handles_fixture(fixture_path: Path):
    """Mirror of services/oncokb_proxy/app.py:_call_oncokb post-processing.

    If this breaks, the proxy parsing breaks — same logic, kept in lockstep
    by code review."""
    data = json.loads(fixture_path.read_text(encoding="utf-8"))

    options: list[dict] = []
    for tx in data.get("treatments", []) or []:
        options.append({
            "level": str(tx.get("level") or "").replace("LEVEL_", "") or "?",
            "drugs": [d.get("drugName", "") for d in tx.get("drugs", []) or []],
            "description": tx.get("description") or None,
            "pmids": [str(p) for p in tx.get("pmids", []) or []],
        })

    # Every option must have a level we surface (or filter — Q1)
    for o in options:
        assert o["level"] in {"1", "2", "3A", "3B", "4", "R1", "R2", "?"}
        assert len(o["drugs"]) >= 1, f"option in {fixture_path.name} has no drugs"


# ── HttpxOncoKBClient end-to-end via mocked httpx ───────────────────────


def test_httpx_client_parses_braf_v600e_mel_fixture():
    """Wire HttpxOncoKBClient against a fixture-backed mock."""
    from unittest.mock import patch, MagicMock
    from knowledge_base.engine.oncokb_client import HttpxOncoKBClient
    from knowledge_base.engine.oncokb_types import OncoKBQuery, OncoKBResult

    fixture = json.loads((_FIXTURES / "braf_v600e_mel.json").read_text(encoding="utf-8"))
    # Proxy returns LookupResponse-shaped dict, not raw OncoKB shape — synthesize it
    proxy_resp = {
        "gene": "BRAF",
        "variant": "V600E",
        "oncokb_url": "https://www.oncokb.org/gene/BRAF/V600E",
        "therapeutic_options": [
            {
                "level": tx["level"].replace("LEVEL_", ""),
                "drugs": [d["drugName"] for d in tx["drugs"]],
                "description": tx.get("description"),
                "pmids": tx["pmids"],
            }
            for tx in fixture["treatments"]
        ],
        "cached": False,
        "oncokb_data_version": fixture.get("dataVersion"),
    }

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = proxy_resp

    with patch("httpx.Client") as mock_ctx:
        mock_ctx.return_value.__enter__.return_value.post.return_value = mock_resp
        client = HttpxOncoKBClient("http://mock-proxy", timeout_seconds=1.0)
        result = client.lookup(OncoKBQuery(
            gene="BRAF", variant="V600E", oncotree_code="MEL",
            source_biomarker_id="BIO-BRAF-V600E",
        ))

    assert isinstance(result, OncoKBResult)
    # Multiple Level 1 entries in the BRAF V600E + MEL fixture (vem+cobi, enco+bini, dab+tram)
    assert len(result.therapeutic_options) >= 3
    levels = {o.level for o in result.therapeutic_options}
    assert "1" in levels  # LEVEL_1 stripped to "1"


def test_httpx_client_handles_resistance_levels_in_egfr_t790m():
    """T790M fixture has both Level 1 (osimertinib) and R1 (resistance to
    1st/2nd gen TKIs) — verify both surface through parsing."""
    from unittest.mock import patch, MagicMock
    from knowledge_base.engine.oncokb_client import HttpxOncoKBClient
    from knowledge_base.engine.oncokb_types import OncoKBQuery, OncoKBResult

    fixture = json.loads((_FIXTURES / "egfr_t790m_nsclc.json").read_text(encoding="utf-8"))
    proxy_resp = {
        "gene": "EGFR",
        "variant": "T790M",
        "oncokb_url": "https://www.oncokb.org/gene/EGFR/T790M",
        "therapeutic_options": [
            {
                "level": tx["level"].replace("LEVEL_", ""),
                "drugs": [d["drugName"] for d in tx["drugs"]],
                "description": tx.get("description"),
                "pmids": tx["pmids"],
            }
            for tx in fixture["treatments"]
        ],
        "cached": False,
        "oncokb_data_version": fixture.get("dataVersion"),
    }

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = proxy_resp

    with patch("httpx.Client") as mock_ctx:
        mock_ctx.return_value.__enter__.return_value.post.return_value = mock_resp
        client = HttpxOncoKBClient("http://mock-proxy", timeout_seconds=1.0)
        result = client.lookup(OncoKBQuery(
            gene="EGFR", variant="T790M", oncotree_code="NSCLC",
            source_biomarker_id="BIO-EGFR-T790M",
        ))

    assert isinstance(result, OncoKBResult)
    levels = {o.level for o in result.therapeutic_options}
    assert "1" in levels
    assert "R1" in levels  # critical for resistance-conflict detector


def test_httpx_client_handles_pan_tumor_fixture():
    """TP53 fixture has tumorType=None — pan-tumor query."""
    from unittest.mock import patch, MagicMock
    from knowledge_base.engine.oncokb_client import HttpxOncoKBClient
    from knowledge_base.engine.oncokb_types import OncoKBQuery, OncoKBResult

    fixture = json.loads((_FIXTURES / "tp53_r175h_pan.json").read_text(encoding="utf-8"))
    assert fixture["query"]["tumorType"] is None  # confirms pan-tumor shape

    proxy_resp = {
        "gene": "TP53",
        "variant": "R175H",
        "oncokb_url": "https://www.oncokb.org/gene/TP53/R175H",
        "therapeutic_options": [
            {"level": tx["level"].replace("LEVEL_", ""),
             "drugs": [d["drugName"] for d in tx["drugs"]],
             "description": tx.get("description"),
             "pmids": tx["pmids"]}
            for tx in fixture["treatments"]
        ],
        "cached": False,
        "oncokb_data_version": fixture.get("dataVersion"),
    }
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = proxy_resp

    with patch("httpx.Client") as mock_ctx:
        mock_ctx.return_value.__enter__.return_value.post.return_value = mock_resp
        client = HttpxOncoKBClient("http://mock-proxy", timeout_seconds=1.0)
        result = client.lookup(OncoKBQuery(
            gene="TP53", variant="R175H", oncotree_code=None,
            source_biomarker_id="BIO-TP53-R175H",
        ))

    assert isinstance(result, OncoKBResult)
    assert result.query.oncotree_code is None  # pan-tumor preserved


# ── PROVISIONAL marker — refuse to silently treat as verified ──────────


def test_fixtures_carry_provisional_marker():
    """Every fixture must have the `_provisional: true` flag until
    real-curl captures replace them. Removing the flag without doing
    real-curl verification would silently treat unverified data as
    verified — guard against that."""
    for f in _list_fixtures():
        data = json.loads(f.read_text(encoding="utf-8"))
        assert data.get("_provisional") is True, (
            f"{f.name} missing _provisional flag — if you've replaced with "
            f"real-curl capture, also update Phase 0 evidence doc."
        )
