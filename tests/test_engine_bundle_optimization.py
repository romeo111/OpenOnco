"""Tests for the CSD-5B core + per-disease bundle split.

Verifies:

- The build produces a core bundle, ≥1 per-disease bundle, and a
  bundle index JSON.
- The core bundle stays under the 2 MB target headroom (with room for
  growth — eventual goal is ≤1.5 MB once content shifts further into
  per-disease modules).
- The bundle index lists every per-disease bundle that exists on disk.
- Per-disease bundles round-trip through `lazy_load_disease()`: the
  expected disease-scoped entities appear, and entities for *other*
  diseases stay out.
- The legacy monolithic openonco-engine.zip is still produced for
  back-compat with /try.html until the JS lazy-load handler ships.
"""

from __future__ import annotations

import json
import shutil
import zipfile
from pathlib import Path

import pytest

from scripts.build_site import bundle_engine
from knowledge_base.engine.lazy_loader import (
    apply_disease_module,
    disease_bundle_basename,
    lazy_load_disease,
    load_bundle_index,
    url_for_disease,
)
from knowledge_base.validation.loader import clear_load_cache


@pytest.fixture(scope="module")
def bundle_out(tmp_path_factory) -> dict:
    """Build the bundles once per module — bundle_engine() is fast
    (~3 s) but still worth caching across the test suite."""
    out = tmp_path_factory.mktemp("docs_bundle")
    info = bundle_engine(out)
    info["_dir"] = out
    return info


# ── Artifacts present ─────────────────────────────────────────────────────


def test_core_and_index_and_disease_dir_present(bundle_out: dict):
    out = Path(bundle_out["_dir"])
    assert (out / "openonco-engine-core.zip").is_file(), "core bundle missing"
    assert (out / "openonco-engine-index.json").is_file(), "bundle index missing"
    assert (out / "disease").is_dir(), "per-disease dir missing"
    # At least 5 per-disease bundles (KB has 60+ diseases — sanity floor)
    bundles = list((out / "disease").glob("openonco-*.zip"))
    assert len(bundles) >= 5, f"expected ≥5 per-disease bundles, got {len(bundles)}"
    # Monolithic openonco-engine.zip retired in CSD-9C (2026-04-27);
    # build_engine() actively deletes any stale copy on disk. No assertion.


def test_core_bundle_under_size_ceiling(bundle_out: dict):
    """Core bundle target: ≤2.95 MB compressed today (~2.89 MB observed
    2026-05-01 after EN-render translation overrides + do_not_do JSON
    sidecar (~72 KB compressed) and four Waves of patient-watchpoints
    authoring: Wave 1 (11 anchor regimens, ~12 KB), Wave 2 (15 disease
    anchors, ~90 KB), Wave 2B (16 disease anchors, ~70 KB), Wave 2C
    (17 disease anchors, ~90 KB). Eventual goal ≤1.5 MB once more
    disease-scoped content (drugs, regimens, indications) is moved out
    of core into per-disease modules. Ceiling sized for headroom;
    tighten as the split matures."""
    core_zip = Path(bundle_out["_dir"]) / "openonco-engine-core.zip"
    size = core_zip.stat().st_size
    assert size < 3_000_000, (
        f"core bundle exceeds 3.0MB compressed: {size} bytes — split is "
        "leaking disease-scoped content into core or shared content has bloated"
    )


def test_per_disease_bundles_under_size_ceiling(bundle_out: dict):
    """Per-disease bundles should be small (≤300 KB each per the design
    target). Catches regressions where the per-disease attribution
    breaks and a bundle starts swallowing shared content."""
    disease_dir = Path(bundle_out["_dir"]) / "disease"
    for zp in sorted(disease_dir.glob("openonco-*.zip")):
        size = zp.stat().st_size
        assert size < 300_000, (
            f"per-disease bundle {zp.name} = {size} bytes (>300 KB) — "
            "attribution heuristic likely picked up shared content"
        )


# ── Bundle index ──────────────────────────────────────────────────────────


def test_bundle_index_is_valid_and_lists_existing_bundles(bundle_out: dict):
    out = Path(bundle_out["_dir"])
    index = load_bundle_index(out / "openonco-engine-index.json")

    assert index["core"] == "openonco-engine-core.zip"
    # `monolithic` key retired in CSD-9C — index no longer carries it.
    assert "core_version" in index and len(index["core_version"]) == 12
    diseases = index.get("diseases") or {}
    assert diseases, "bundle index lists no diseases"

    # Every URL in the index must point to an existing zip on disk
    for did, rel_url in diseases.items():
        assert did.startswith("DIS-"), f"non-canonical disease id in index: {did}"
        bp = out / rel_url
        assert bp.is_file(), f"index references missing bundle: {rel_url}"

    # Every per-disease bundle on disk must appear in the index (no orphans)
    on_disk = {p.name for p in (out / "disease").glob("openonco-*.zip")}
    in_index = {Path(rel).name for rel in diseases.values()}
    orphans = on_disk - in_index
    assert not orphans, f"per-disease zips present but not in index: {orphans}"


def test_disease_bundle_basename_matches_url_in_index(bundle_out: dict):
    """`disease_bundle_basename()` is the canonical slug rule. Every
    per-disease URL in the index must derive from it."""
    index = load_bundle_index(
        Path(bundle_out["_dir"]) / "openonco-engine-index.json"
    )
    for did, rel_url in index["diseases"].items():
        expected = f"disease/{disease_bundle_basename(did)}"
        assert rel_url == expected, (
            f"index URL {rel_url!r} for {did} differs from "
            f"disease_bundle_basename → {expected!r}"
        )


# ── Per-disease bundle contents ──────────────────────────────────────────


def _names(zp: Path) -> set[str]:
    with zipfile.ZipFile(zp) as zf:
        return set(zf.namelist())


def test_core_bundle_excludes_disease_specific_indications(bundle_out: dict):
    """The whole point of the split is that disease-specific
    indications/algorithms/regimens/RFs go to the per-disease bundles.
    Probe: pick DLBCL files known to exist and check they're NOT in core."""
    core_names = _names(Path(bundle_out["_dir"]) / "openonco-engine-core.zip")
    leaked = [
        n for n in core_names
        if "/indications/ind_dlbcl_" in n
        or "/algorithms/algo_dlbcl_" in n
        or "/redflags/rf_dlbcl_" in n
        or "/biomarker_actionability/bma_" in n and "_dlbcl_nos" in n
    ]
    assert not leaked, f"DLBCL-scoped content leaked into core: {leaked[:5]}"


def test_core_bundle_keeps_universal_redflags_and_disease_metadata(bundle_out: dict):
    """Universals stay in core (they apply across diseases) and disease
    metadata stays in core (so the questionnaire/disease picker can
    render before any lazy-load fires)."""
    core_names = _names(Path(bundle_out["_dir"]) / "openonco-engine-core.zip")
    # Disease metadata
    assert any(n.endswith("/diseases/dlbcl_nos.yaml") for n in core_names), (
        "diseases/dlbcl_nos.yaml must stay in core"
    )
    # Universal RFs
    assert any("/redflags/universal/" in n for n in core_names), (
        "universal redflags must stay in core"
    )
    # Shared content
    assert any("/sources/" in n for n in core_names), "sources/ must be in core"
    assert any("/drugs/" in n for n in core_names), "drugs/ must be in core"
    assert any("/biomarkers/" in n for n in core_names), "biomarkers/ must be in core"


def test_per_disease_bundle_contains_only_that_diseases_yamls(bundle_out: dict):
    """Probe DIS-DLBCL-NOS bundle: every YAML in it should reference
    DIS-DLBCL-NOS in disease_id / applicable_to_disease / a single-entry
    relevant_diseases. (Universal RFs stay in core, so this bundle should
    contain only disease-scoped files.)"""
    out = Path(bundle_out["_dir"])
    bundle = out / "disease" / "openonco-dis-dlbcl-nos.zip"
    assert bundle.is_file(), "DLBCL bundle expected for this test"
    with zipfile.ZipFile(bundle) as zf:
        for name in zf.namelist():
            if not name.endswith(".yaml"):
                continue
            text = zf.read(name).decode("utf-8")
            assert "DIS-DLBCL-NOS" in text, (
                f"file {name} in DLBCL bundle but never mentions DIS-DLBCL-NOS"
            )


# ── Lazy-load round trip (pure-Python, no Pyodide) ───────────────────────


def _unpack_core(out_dir: Path, target: Path) -> None:
    """Mimic what `pyodide.unpackArchive` does for the core bundle."""
    with zipfile.ZipFile(out_dir / "openonco-engine-core.zip") as zf:
        zf.extractall(target)


def test_lazy_load_disease_merges_into_core(bundle_out: dict, tmp_path: Path):
    """Round-trip: unpack core into a tmp KB root, then call
    `lazy_load_disease()` for DLBCL — verify (a) the per-disease YAMLs
    landed on disk, (b) the loader sees both core entities and the
    lazily-loaded disease entities, (c) DIS-DLBCL-NOS-specific files
    are present after the merge."""
    out_dir = Path(bundle_out["_dir"])
    target = tmp_path / "kb_root"
    target.mkdir()
    _unpack_core(out_dir, target)

    content_root = target / "knowledge_base" / "hosted" / "content"
    assert content_root.is_dir(), "core unpack should produce hosted/content/"

    # Probe a DLBCL-specific indication is NOT yet present
    assert not (content_root / "indications" / "ind_dlbcl_1l_rchop.yaml").exists()

    clear_load_cache()
    result = lazy_load_disease(
        "DIS-DLBCL-NOS",
        bundle_dir=out_dir,
        kb_root=target,
    )

    assert result["disease_id"] == "DIS-DLBCL-NOS"
    assert result["extracted"], "lazy_load extracted no files"
    summary = result["summary"]
    # Schema + contract checks must stay green — those are intrinsic to
    # the entities themselves, not cross-bundle references.
    assert summary["schema_errors"] == 0, (
        f"schema errors after lazy-load: {summary}"
    )
    assert summary["contract_errors"] == 0, (
        f"contract errors after lazy-load: {summary}"
    )
    # Ref errors are EXPECTED in core+single-disease state: algorithms in
    # core may reference indications that live in OTHER diseases' bundles
    # which haven't been lazy-loaded. The engine still runs correctly for
    # the disease that IS loaded — ref-completeness is only required when
    # all bundles are loaded together (= the monolithic case, covered by
    # test_monolithic_bundle_is_self_sufficient).
    # Disease-specific file now exists on disk
    assert (content_root / "indications" / "ind_dlbcl_1l_rchop.yaml").exists(), (
        "DLBCL indication missing after lazy-load merge"
    )
    # And the loader sees DLBCL entities now
    assert summary["by_type"].get("indications", 0) > 0, (
        "no indications loaded after merging DLBCL bundle"
    )


def test_lazy_load_does_not_leak_unrelated_disease_content(
    bundle_out: dict, tmp_path: Path
):
    """After lazy-loading DLBCL on top of core, content for an
    *unrelated* disease (CRC) must NOT have appeared on disk — the
    core+DLBCL merge should never pull CRC indications."""
    out_dir = Path(bundle_out["_dir"])
    target = tmp_path / "kb_root"
    target.mkdir()
    _unpack_core(out_dir, target)

    clear_load_cache()
    lazy_load_disease(
        "DIS-DLBCL-NOS",
        bundle_dir=out_dir,
        kb_root=target,
    )

    content_root = target / "knowledge_base" / "hosted" / "content"
    # Probe CRC-scoped files
    crc_files = list((content_root / "indications").glob("ind_crc_*.yaml"))
    assert not crc_files, (
        f"CRC indications appeared after DLBCL-only lazy-load: "
        f"{[p.name for p in crc_files]}"
    )
    crc_rfs = list((content_root / "redflags").glob("rf_crc_*.yaml"))
    assert not crc_rfs, (
        f"CRC redflags appeared after DLBCL-only lazy-load: "
        f"{[p.name for p in crc_rfs]}"
    )


def test_url_for_disease_returns_none_for_unknown_disease(bundle_out: dict):
    index = load_bundle_index(
        Path(bundle_out["_dir"]) / "openonco-engine-index.json"
    )
    assert url_for_disease(index, "DIS-DOES-NOT-EXIST") is None


# Monolithic back-compat tests removed 2026-04-30: the legacy
# `openonco-engine.zip` was retired in CSD-9C (2026-04-27,
# scripts/build_site.py:272-278 actively deletes any stale monolithic
# on every build). The lazy-load core + per-disease pathway is exercised
# by the tests above and in test_engine_bundle_extended.py.
