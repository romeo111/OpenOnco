from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from scripts.build_kb_wiki import build_kb_wiki


KB_ROOT = Path("knowledge_base/hosted/content")
OUT_ROOT = Path("build/test-kb-wiki")


@pytest.fixture(scope="module")
def wiki_dir() -> Path:
    shutil.rmtree(OUT_ROOT, ignore_errors=True)
    build_kb_wiki(KB_ROOT, OUT_ROOT)
    try:
        yield OUT_ROOT
    finally:
        shutil.rmtree(OUT_ROOT, ignore_errors=True)


@pytest.fixture(scope="module")
def wiki_payload(wiki_dir: Path) -> dict:
    return json.loads((wiki_dir / "kb_search_index.json").read_text(encoding="utf-8"))


def test_kb_wiki_builds_search_index_and_entity_pages(wiki_dir: Path, wiki_payload: dict):
    counts = wiki_payload["counts"]

    assert len(wiki_payload["entries"]) > 1000
    assert counts["Disease"] >= 70
    assert counts["Drugs"] >= 200
    assert counts["Biomarkers"] >= 100
    assert counts["Red flags"] >= 400
    assert counts["Actionability"] >= 400

    assert (wiki_dir / "kb.html").exists()
    assert (wiki_dir / "ukr" / "kb.html").exists()
    assert (wiki_dir / "kb_search_index.json").exists()
    assert (wiki_dir / "ukr" / "kb_search_index.json").exists()
    assert (wiki_dir / "kb" / "drugs" / "drug-rituximab.html").exists()
    assert (wiki_dir / "ukr" / "kb" / "drugs" / "drug-rituximab.html").exists()
    assert (wiki_dir / "kb" / "biomarkers" / "bio-egfr-l858r.html").exists()
    assert (
        wiki_dir
        / "kb"
        / "redflags"
        / "rf-aggressive-histology-transformation.html"
    ).exists()
    assert (
        wiki_dir
        / "kb"
        / "biomarker_actionability"
        / "bma-egfr-l858r-nsclc.html"
    ).exists()

    kb_home = (wiki_dir / "kb.html").read_text(encoding="utf-8")
    assert 'class="kb-info-box"' in kb_home
    assert 'id="kbSearchBtn"' in kb_home
    assert "<h1>Onco Wiki</h1>" in kb_home
    assert 'href="/diseases.html">Diseases</a>' not in kb_home
    assert "Source-grounded browser" in kb_home
    assert 'data-kind="Disease"' in kb_home
    assert ">Search</button>" in kb_home

    uk_kb_home = (wiki_dir / "ukr" / "kb.html").read_text(encoding="utf-8")
    assert 'lang="uk"' in uk_kb_home
    assert "<h1>Onco Wiki</h1>" in uk_kb_home
    assert 'href="/ukr/diseases.html">Хвороби</a>' not in uk_kb_home
    assert "Браузер, прив’язаний до джерел" in uk_kb_home
    assert ">Шукати</button>" in uk_kb_home
    assert "FAQ для клініцистів" in uk_kb_home


def test_kb_search_index_exposes_provenance_and_reverse_refs(wiki_payload: dict):
    entries = {entry["id"]: entry for entry in wiki_payload["entries"]}

    nsclc = entries["DIS-NSCLC"]
    assert nsclc["kind"] == "Disease"
    assert nsclc["kind_key"] == "diseases"
    assert nsclc["url"] == "/diseases.html#DIS-NSCLC"
    assert "non-small cell lung cancer" in nsclc["search_text"]
    assert "regimen" in nsclc["search_text"]
    assert "verified" in nsclc["subtitle"]

    rituximab = entries["DRUG-RITUXIMAB"]
    assert rituximab["kind"] == "Drug"
    assert "SRC-" in " ".join(rituximab["sources"])
    assert rituximab["used_by_count"] > 0
    assert "rituximab" in rituximab["search_text"]

    egfr = entries["BIO-EGFR-L858R"]
    assert egfr["kind"] == "Biomarker"
    assert "egfr" in egfr["search_text"]
    assert "SRC-NCCN-NSCLC-2025" in egfr["sources"]


def test_redflag_page_shows_origin_logic_and_usage(wiki_dir: Path):
    page = (
        wiki_dir
        / "kb"
        / "redflags"
        / "rf-aggressive-histology-transformation.html"
    ).read_text(encoding="utf-8")

    assert "Red Flag Origin" in page
    assert "Trigger Logic" in page
    assert "RF-AGGRESSIVE-HISTOLOGY-TRANSFORMATION" in page
    assert "SRC-NCCN-BCELL-2025" in page
    assert "Used By" in page
    assert "ALGO-HCV-MZL-1L" in page

    uk_page = (
        wiki_dir
        / "ukr"
        / "kb"
        / "redflags"
        / "rf-aggressive-histology-transformation.html"
    ).read_text(encoding="utf-8")
    assert "Походження тривожної ознаки" in uk_page
    assert "Логіка спрацьовування" in uk_page
    assert "Де використовується" in uk_page
