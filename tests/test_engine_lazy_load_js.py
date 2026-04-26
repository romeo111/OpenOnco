"""CSD-6E: /try.html JS lazy-load wiring.

Asserts that the rendered try.html contains the bundle lazy-load
infrastructure (helpers + index reference + service-worker register)
and that the bundle index actually ships an `icd_to_disease_id` map
the JS can resolve against. Also covers the EN mirror at /en/try.html
and the standalone `docs/sw.js`.

These are structural smoke tests — they don't load Pyodide. They guard
against the regression "someone refactored render_try() and accidentally
deleted the lazy-load helpers, sending us back to the 1.8 MB monolithic
fetch on every visit".
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_site import build_site


@pytest.fixture(scope="module")
def site_dir(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("docs_lazy")
    build_site(out)
    return out


# ── try.html JS structure ─────────────────────────────────────────────────


@pytest.mark.parametrize("page", ["try.html", "en/try.html"])
def test_try_html_contains_lazy_load_helpers(site_dir: Path, page: str):
    html = (site_dir / page).read_text(encoding="utf-8")
    # Every helper added in CSD-6E must be present so the on-load path
    # uses the core bundle, not the monolithic one.
    for needle in (
        "loadBundleIndex",
        "loadCoreBundle",
        "loadDiseaseModule",
        "resolveDiseaseId",
        "openonco-engine-index.json",
        "openonco-engine-core.zip",
        "loadedDiseases",
        "localStorage",
        "apply_disease_module",
    ):
        assert needle in html, f"{page} missing lazy-load token: {needle}"


@pytest.mark.parametrize("page", ["try.html", "en/try.html"])
def test_try_html_keeps_monolithic_fallback(site_dir: Path, page: str):
    """The monolithic bundle is the safety net when the index 404s
    (old deploys, ad-blockers). render_try() must still reference it."""
    html = (site_dir / page).read_text(encoding="utf-8")
    assert "openonco-engine.zip" in html, (
        f"{page} dropped monolithic fallback — old clients will break"
    )
    assert "FALLBACK_MONOLITHIC_URL" in html


@pytest.mark.parametrize("page", ["try.html", "en/try.html"])
def test_try_html_registers_service_worker(site_dir: Path, page: str):
    html = (site_dir / page).read_text(encoding="utf-8")
    assert "serviceWorker" in html and "navigator.serviceWorker.register" in html
    assert "/sw.js" in html


@pytest.mark.parametrize("page", ["try.html", "en/try.html"])
def test_try_html_calls_disease_module_in_run_engine(site_dir: Path, page: str):
    """The Generate path must call loadDiseaseModule() with the resolved
    disease_id — otherwise the per-disease zips ship to the browser but
    are never actually fetched."""
    html = (site_dir / page).read_text(encoding="utf-8")
    assert "await loadDiseaseModule(did)" in html


# ── Bundle index payload shape ────────────────────────────────────────────


def test_bundle_index_ships_icd_to_disease_id(site_dir: Path):
    idx = json.loads(
        (site_dir / "openonco-engine-index.json").read_text(encoding="utf-8")
    )
    assert "icd_to_disease_id" in idx, "index missing icd_to_disease_id map"
    icd = idx["icd_to_disease_id"]
    assert isinstance(icd, dict) and len(icd) > 10, (
        "icd_to_disease_id looks suspiciously small — disease YAMLs may "
        "have lost their codes.icd_o_3_morphology fields"
    )
    # Every value must be a known disease in the same index, otherwise
    # the JS resolver will request a 404 URL.
    diseases = set(idx.get("diseases", {}).keys())
    for code, did in icd.items():
        assert isinstance(code, str) and code, "blank ICD code in map"
        assert did in diseases or did.startswith("DIS-"), (
            f"icd_to_disease_id[{code}] = {did!r} is not in diseases map"
        )


# ── Service worker file ───────────────────────────────────────────────────


def test_service_worker_written_and_versioned(site_dir: Path):
    sw = site_dir / "sw.js"
    assert sw.is_file(), "docs/sw.js not written by build_site"
    text = sw.read_text(encoding="utf-8")
    # Cache name must be stamped with the core_version so a KB push
    # rotates the cache key.
    idx = json.loads(
        (site_dir / "openonco-engine-index.json").read_text(encoding="utf-8")
    )
    core_version = idx.get("core_version", "")
    assert core_version, "core_version missing from index"
    assert core_version in text, (
        "sw.js cache name not stamped with core_version — KB pushes won't "
        "invalidate stale bundles in the SW cache"
    )
    # Must intercept the engine artifacts and only those.
    for pat in (
        "openonco-engine-core.zip",
        "openonco-engine.zip",
        "openonco-engine-index.json",
        "/disease/openonco-",
    ):
        assert pat in text, f"sw.js doesn't mention {pat}"
