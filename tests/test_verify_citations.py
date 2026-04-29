"""Tests for scripts.tasktorrent.verify_citations.

Uses a tmp_path-based fake KB so we don't depend on real master content.
"""

from __future__ import annotations

import json
import os
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from scripts.tasktorrent import verify_citations as vc


# ---------- Fixtures ----------

@pytest.fixture
def fake_kb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Build a minimal fake KB structure rooted at tmp_path.

    Returns (repo_root, contrib_root, sources_root).
    """
    repo = tmp_path
    contrib = repo / "contributions"
    sources = repo / "knowledge_base" / "hosted" / "content" / "sources"
    civic = repo / "knowledge_base" / "hosted" / "civic"
    contrib.mkdir(parents=True)
    sources.mkdir(parents=True)
    civic.mkdir(parents=True)

    # Master source: SRC-NCCN with a title that mentions KEYNOTE-522
    (sources / "src_nccn_breast.yaml").write_text(
        yaml.safe_dump({
            "id": "SRC-NCCN-BREAST",
            "title": "NCCN Breast Cancer Guidelines (KEYNOTE-522 + monarchE)",
            "notes": "v3.2025",
        }),
        encoding="utf-8",
    )
    # Master source without trial mentions
    (sources / "src_civic.yaml").write_text(
        yaml.safe_dump({
            "id": "SRC-CIVIC",
            "title": "CIViC — Clinical Interpretations of Variants in Cancer",
            "notes": "snapshot",
        }),
        encoding="utf-8",
    )

    # CIViC snapshot with a couple of EIDs
    snap_dir = civic / "2026-04-25"
    snap_dir.mkdir()
    (snap_dir / "evidence.yaml").write_text(
        yaml.safe_dump({
            "evidence_items": [
                {"id": "EID1409"},
                {"id": "EID3017"},
            ]
        }),
        encoding="utf-8",
    )

    # Repoint module-level constants
    monkeypatch.setattr(vc, "REPO_ROOT", repo)
    monkeypatch.setattr(vc, "CONTRIB_ROOT", contrib)
    monkeypatch.setattr(vc, "SOURCES_ROOT", sources)
    monkeypatch.setattr(vc, "CIVIC_SNAPSHOT_ROOT", civic)

    return repo, contrib, sources


def _write_sidecar(chunk_dir: Path, name: str, payload: dict) -> Path:
    p = chunk_dir / name
    p.write_text(yaml.safe_dump(payload), encoding="utf-8")
    return p


# ---------- Layer 1: structural ----------

def test_structural_passes_with_known_sources(fake_kb) -> None:
    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    _write_sidecar(chunk, "bma_x.yaml", {
        "id": "BMA-X",
        "evidence_summary": "evidence text",
        "primary_sources": ["SRC-NCCN-BREAST"],
        "evidence_sources": [
            {"source": "SRC-CIVIC", "evidence_ids": ["EID1409"]},
        ],
    })
    reports, code = vc.verify_chunk("test-chunk")
    assert code == 0
    assert reports[0].passed
    structural = next(c for c in reports[0].checks if c.layer == "structural")
    assert structural.passed


def test_structural_fails_with_unknown_source(fake_kb) -> None:
    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    _write_sidecar(chunk, "bma_x.yaml", {
        "id": "BMA-X",
        "evidence_summary": "ev",
        "primary_sources": ["SRC-DOES-NOT-EXIST"],
    })
    reports, code = vc.verify_chunk("test-chunk")
    assert code == 1
    assert not reports[0].passed
    structural = next(c for c in reports[0].checks if c.layer == "structural")
    assert "unknown sources" in structural.detail


def test_structural_accepts_chunk_stub_source(fake_kb) -> None:
    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    # Stub provides the otherwise-unknown source
    _write_sidecar(chunk, "source_stub_src_keynote_522.yaml", {
        "id": "SRC-KEYNOTE-522-SCHMID-2024",
        "title": "KEYNOTE-522: pembrolizumab + chemo in TNBC",
    })
    _write_sidecar(chunk, "bma_x.yaml", {
        "id": "BMA-X",
        "evidence_summary": "ev",
        "primary_sources": ["SRC-KEYNOTE-522-SCHMID-2024"],
    })
    reports, code = vc.verify_chunk("test-chunk")
    assert code == 0


def test_structural_fails_on_unknown_eid(fake_kb) -> None:
    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    _write_sidecar(chunk, "bma_x.yaml", {
        "id": "BMA-X",
        "evidence_summary": "ev",
        "primary_sources": ["SRC-CIVIC"],
        "evidence_sources": [
            {"source": "SRC-CIVIC", "evidence_ids": ["EID99999999"]},
        ],
    })
    reports, code = vc.verify_chunk("test-chunk")
    assert code == 1
    structural = next(c for c in reports[0].checks if c.layer == "structural")
    assert "unknown CIViC EIDs" in structural.detail


# ---------- Layer 2: title-substring ----------

def test_title_substring_n_a_when_no_trial_mentioned(fake_kb) -> None:
    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    _write_sidecar(chunk, "bma_x.yaml", {
        "id": "BMA-X",
        "evidence_summary": "Generic evidence about a biomarker, no trial named.",
        "primary_sources": ["SRC-NCCN-BREAST"],
    })
    reports, _ = vc.verify_chunk("test-chunk")
    title = next(c for c in reports[0].checks if c.layer == "title-substring")
    assert title.passed
    assert "n/a" in title.detail


def test_title_substring_passes_when_trial_in_source_title(fake_kb) -> None:
    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    _write_sidecar(chunk, "bma_x.yaml", {
        "id": "BMA-X",
        "evidence_summary": "Per trial KEYNOTE-522 the regimen is supported.",
        "primary_sources": ["SRC-NCCN-BREAST"],  # title mentions KEYNOTE-522
    })
    reports, _ = vc.verify_chunk("test-chunk")
    title = next(c for c in reports[0].checks if c.layer == "title-substring")
    assert title.passed


def test_title_substring_fails_when_trial_not_in_source(fake_kb) -> None:
    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    _write_sidecar(chunk, "bma_x.yaml", {
        "id": "BMA-X",
        "evidence_summary": "Per trial COMPLETELY-MADE-UP-XYZ.",
        "primary_sources": ["SRC-NCCN-BREAST"],
    })
    reports, code = vc.verify_chunk("test-chunk")
    assert code == 1
    title = next(c for c in reports[0].checks if c.layer == "title-substring")
    assert not title.passed
    assert "not found" in title.detail


# ---------- Layer 3: semantic ----------

def test_semantic_skipped_without_api_key(fake_kb, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    _write_sidecar(chunk, "bma_x.yaml", {
        "id": "BMA-X",
        "evidence_summary": "ev",
        "primary_sources": ["SRC-NCCN-BREAST"],
    })
    reports, _ = vc.verify_chunk("test-chunk", semantic=True)
    sem = next(c for c in reports[0].checks if c.layer == "semantic")
    assert sem.passed
    assert "skipped" in sem.detail


def test_semantic_skipped_when_sdk_missing(fake_kb, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-key-for-test")
    # Simulate ImportError on `import anthropic`
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "anthropic":
            raise ImportError("anthropic not installed")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    _write_sidecar(chunk, "bma_x.yaml", {
        "id": "BMA-X",
        "evidence_summary": "ev",
        "primary_sources": ["SRC-NCCN-BREAST"],
    })
    reports, _ = vc.verify_chunk("test-chunk", semantic=True)
    sem = next(c for c in reports[0].checks if c.layer == "semantic")
    assert sem.passed  # missing SDK is non-blocking
    assert "anthropic SDK" in sem.detail


def test_semantic_n_a_when_no_summary(fake_kb, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-key")
    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    _write_sidecar(chunk, "bma_x.yaml", {
        "id": "BMA-X",
        "primary_sources": ["SRC-NCCN-BREAST"],
        # no evidence_summary, no description, no notes → empty summary
        # (intentionally minimal)
    })
    reports, _ = vc.verify_chunk("test-chunk", semantic=True)
    sem = next(c for c in reports[0].checks if c.layer == "semantic")
    assert sem.passed


# ---------- CLI ----------

def test_cli_missing_chunk_returns_2(fake_kb, capsys) -> None:
    rc = vc.main(["nonexistent-chunk"])
    assert rc == 2


def test_cli_semantic_flag_without_key_returns_3(fake_kb, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    rc = vc.main(["test-chunk", "--semantic"])
    assert rc == 3


def test_cli_emits_json_when_flagged(fake_kb, capsys) -> None:
    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    _write_sidecar(chunk, "bma_x.yaml", {
        "id": "BMA-X",
        "evidence_summary": "ev",
        "primary_sources": ["SRC-NCCN-BREAST"],
    })
    rc = vc.main(["test-chunk", "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    parsed = json.loads(out)
    assert isinstance(parsed, list) and len(parsed) == 1
    assert parsed[0]["target_id"] == "BMA-X"


def test_cli_human_output_includes_summary_line(fake_kb, capsys) -> None:
    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    _write_sidecar(chunk, "bma_x.yaml", {
        "id": "BMA-X",
        "evidence_summary": "ev",
        "primary_sources": ["SRC-NCCN-BREAST"],
    })
    rc = vc.main(["test-chunk"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "1/1 sidecars passed" in out


# ---------- Helpers ----------

def test_extract_eids_handles_nested() -> None:
    data = {
        "evidence_sources": [
            {"source": "SRC-CIVIC", "evidence_ids": ["EID1409", "EID3017"]},
            {"source": "SRC-CIVIC", "note": "References EID9851 in passing"},
        ]
    }
    eids = vc._extract_eids(data["evidence_sources"])
    assert set(eids) == {"EID1409", "EID3017", "EID9851"}


def test_normalize_strips_separators() -> None:
    assert vc._normalize("KEYNOTE-522") == "keynote522"
    assert vc._normalize("EV-302") == "ev302"


def test_discover_sidecars_excludes_meta_and_reports(fake_kb) -> None:
    repo, contrib, _ = fake_kb
    chunk = contrib / "test-chunk"; chunk.mkdir()
    (chunk / "_contribution_meta.yaml").write_text("x: 1", encoding="utf-8")
    (chunk / "false_positive_report.yaml").write_text("x: 1", encoding="utf-8")
    (chunk / "audit-report.yaml").write_text("x: 1", encoding="utf-8")
    (chunk / "bma_a.yaml").write_text("id: BMA-A", encoding="utf-8")
    (chunk / "bma_b.yaml").write_text("id: BMA-B", encoding="utf-8")
    found = vc.discover_sidecars(chunk)
    names = sorted(p.name for p in found)
    assert names == ["bma_a.yaml", "bma_b.yaml"]
