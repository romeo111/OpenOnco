"""Smoke test for the static-site builder (scripts/build_site.py).

Builds the full site into a tmp dir and asserts the structural contract:

- public landing (no auth gate) with hero + numerical metrics + Watson cmp
- public gallery with all CASE entries
- try.html wired to Pyodide + example loader
- per-case files keep back-link + feedback link, no auth gate
- no real-patient data leaks
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from scripts.build_site import CASES, build_site


@pytest.fixture(scope="module")
def site_dir(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("docs")
    build_site(out)
    return out


# ── Static assets ─────────────────────────────────────────────────────────


def test_static_assets_present(site_dir: Path):
    for f in (".nojekyll", "CNAME", "style.css", "index.html", "gallery.html",
              "try.html", "openonco-engine.zip", "examples.json"):
        assert (site_dir / f).exists(), f"missing {f}"


def test_cname_binds_custom_domain(site_dir: Path):
    """GitHub Pages reads docs/CNAME on every deploy. Build must rewrite it
    every run so --clean cycles never break the apex domain binding."""
    cname = (site_dir / "CNAME").read_text(encoding="utf-8").strip()
    assert cname == "openonco.info"


# ── Landing page (index.html) ─────────────────────────────────────────────


def test_landing_is_public_with_hero_and_ctas(site_dir: Path):
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    # No auth gate — public landing per user direction
    assert "openOncoUser" not in html, "auth gate must be removed from landing"
    # Hero structure
    assert 'class="hero"' in html
    # Both CTAs
    assert 'href="try.html"' in html
    assert 'href="gallery.html"' in html
    # Hero copy in Ukrainian
    assert "tumor-board" in html.lower()


def test_landing_shows_numerical_metrics(site_dir: Path):
    """Goal 1: project metrics must be prominent on the landing."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert 'class="num-grid"' in html
    # Headline numbers labels
    for label in ("Хвороби в KB", "Показання", "Режими", "Препарати",
                  "Тести", "Workups", "Red flags", "Supportive care",
                  "Джерела", "Специфікації"):
        assert label in html, f"missing landing metric label: {label}"


def test_landing_includes_watson_comparison(site_dir: Path):
    """The 'how we differ from Watson' table from REFERENCE_CASE_SPECIFICATION §8.3
    is the trust-establishing block — must appear on the public landing."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "Watson Oncology" in html
    assert "OpenOnco" in html
    assert "Black box" in html or "чорних скриньок" in html.lower()


# ── Gallery page ──────────────────────────────────────────────────────────


def test_gallery_is_public_with_all_cases(site_dir: Path):
    html = (site_dir / "gallery.html").read_text(encoding="utf-8")
    assert "openOncoUser" not in html, "auth gate must be removed from gallery"
    assert html.count('class="case-card"') == len(CASES)
    for c in CASES:
        assert f"cases/{c.case_id}.html" in html
    # Stats widget embedded
    assert "oo-widget" in html
    # Feedback path
    assert "tester-feedback" in html


# ── Try page (Pyodide demo) ───────────────────────────────────────────────


def test_try_page_wires_pyodide_and_form(site_dir: Path):
    """Goal 2: visitor enters virtual patient JSON, engine runs in browser."""
    html = (site_dir / "try.html").read_text(encoding="utf-8")
    # Pyodide loaded from CDN
    assert "cdn.jsdelivr.net/pyodide" in html
    assert "loadPyodide" in html
    # micropip installs the runtime deps
    assert "pydantic" in html and "pyyaml" in html
    # Form elements
    assert 'id="patientJson"' in html
    assert 'id="exampleSelect"' in html
    assert 'id="runBtn"' in html
    # Result rendered into iframe (so embedded styles don't conflict)
    assert 'id="resultFrame"' in html
    # Engine bundle URL
    assert "openonco-engine.zip" in html
    # Example dropdown source
    assert "examples.json" in html


# ── Engine bundle (Pyodide-loadable zip) ──────────────────────────────────


def test_engine_bundle_contains_runtime_modules(site_dir: Path):
    zip_path = site_dir / "openonco-engine.zip"
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    # Required engine + schema + validation + content for generate_plan to run
    must_have = {
        "knowledge_base/__init__.py",
        "knowledge_base/engine/__init__.py",
        "knowledge_base/engine/plan.py",
        "knowledge_base/engine/render.py",
        "knowledge_base/schemas/__init__.py",
        "knowledge_base/validation/loader.py",
    }
    missing = must_have - names
    assert not missing, f"engine bundle missing required modules: {missing}"
    # KB content YAML files present (sample probe)
    yaml_files = [n for n in names if n.startswith("knowledge_base/hosted/content/") and n.endswith(".yaml")]
    assert len(yaml_files) >= 50, f"engine bundle too few KB YAML files: {len(yaml_files)}"


def test_engine_bundle_excludes_heavy_unused_subtrees(site_dir: Path):
    """code_systems/ + civic/ + ctcae/ are not loaded by the engine at runtime
    (validation.loader scans hosted/content/ only). Excluding them keeps the
    Pyodide download under ~250KB compressed."""
    zip_path = site_dir / "openonco-engine.zip"
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
    forbidden_prefixes = (
        "knowledge_base/hosted/code_systems/",
        "knowledge_base/hosted/civic/",
        "knowledge_base/hosted/ctcae/",
        "knowledge_base/clients/",
        "knowledge_base/ingestion/",
    )
    for n in names:
        for pfx in forbidden_prefixes:
            assert not n.startswith(pfx), f"unexpected file in bundle: {n}"
    # Bundle must be small enough for fast first-page load
    assert zip_path.stat().st_size < 300_000, (
        f"engine bundle exceeds 300KB compressed: {zip_path.stat().st_size}"
    )


# ── Examples payload ──────────────────────────────────────────────────────


def test_examples_payload_matches_cases(site_dir: Path):
    payload = json.loads((site_dir / "examples.json").read_text(encoding="utf-8"))
    case_ids_payload = {e["case_id"] for e in payload}
    case_ids_expected = {c.case_id for c in CASES}
    assert case_ids_payload == case_ids_expected
    # Each entry has a parseable patient JSON
    for entry in payload:
        assert isinstance(entry["json"], dict)
        # Engine-required top-level fields exist for non-diagnostic patients
        # (diagnostic patients have a different shape)


# ── Per-case files ────────────────────────────────────────────────────────


def test_case_files_have_back_link_and_no_auth(site_dir: Path):
    for c in CASES:
        path = site_dir / "cases" / f"{c.case_id}.html"
        assert path.exists(), f"case file missing: {path.name}"
        html = path.read_text(encoding="utf-8")
        assert html.startswith("<!DOCTYPE html>")
        assert "</html>" in html
        assert "openOncoUser" not in html, f"{c.case_id} retains auth gate"
        assert "Назад до галереї" in html
        assert "tester-feedback" in html


# ── Privacy guard ─────────────────────────────────────────────────────────


def test_no_real_patient_initials_leak_into_site(site_dir: Path):
    forbidden = ["В.Д.В.", "V.D.V.", "В. Д. В.", "V. D. V."]
    for path in site_dir.rglob("*.html"):
        html = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in html, f"leaked '{token}' in {path.name}"
