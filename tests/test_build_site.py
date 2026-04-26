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
    # Hero copy
    assert "oncology" in html.lower() or "онколог" in html.lower()


def test_capabilities_shows_numerical_metrics(site_dir: Path):
    """Project metrics live on /capabilities.html (moved off the landing
    in commit `25b0340` so the landing stays focused on the MDT story).

    The rich-card layout with per-metric textual explanations is the
    canonical place to show what's in the KB."""
    html = (site_dir / "capabilities.html").read_text(encoding="utf-8")
    assert 'class="num-grid num-grid--rich"' in html
    for label in ("Хвороби в KB", "Лікарі-скіли", "Режими лікування",
                  "Препарати", "Тести", "Workups", "Red flags",
                  "Джерела", "Специфікації"):
        assert label in html, f"missing capabilities metric label: {label}"
    # Removed labels per user direction
    for removed in ("Показання (Indications)", "Supportive care"):
        assert removed not in html, f"label '{removed}' should be removed"
    # Each rich card has a text explanation block
    assert html.count('class="num-text"') >= 8


def test_landing_drops_watson_comparison(site_dir: Path):
    """Per user direction: Watson comparison block removed — keep landing
    focused on what we DO, not what we're not."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "Watson Oncology" not in html
    assert 'class="cmp"' not in html
    assert 'class="approach"' not in html


def test_landing_problem_block_is_single_prose(site_dir: Path):
    """The 'why this is needed' block is prose paragraphs (`how-lead`)
    inside the unified `<section class="how">`, not a 2-column grid.
    Renamed from `problem-text` to `how-lead` in commit `25b0340` when
    the problem and how-it-works blocks merged."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert 'class="how-lead"' in html
    assert 'class="problem-grid"' not in html


def test_landing_how_section_uses_dataflow_stages(site_dir: Path):
    """The 'Як це працює' section uses a 4-stage dataflow block
    (INPUT → VERIFY → BIOMARKERS → OUTPUT) — replaced the older
    MDT infographic embed when the landing was redesigned."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert 'class="dataflow"' in html
    for stage in ("01 · INPUT", "02 · VERIFY", "03 · BIOMARKERS", "04 · OUTPUT"):
        assert stage in html, f"missing dataflow stage label: {stage}"
    # Old text-list step format removed
    assert '<ol class="steps">' not in html


def test_top_bar_drops_tester_pill(site_dir: Path):
    """Per user direction: 'Тестувальник · OSS preview' pill removed from header."""
    for page in ("index.html", "gallery.html", "try.html"):
        html = (site_dir / page).read_text(encoding="utf-8")
        assert "Тестувальник · OSS preview" not in html, (
            f"tester pill still in {page} header"
        )


def test_landing_drops_charter_eyebrow(site_dir: Path):
    """Per user direction: 'клінічний контент під CHARTER §6.1 dual-review'
    eyebrow removed from hero — too noisy for first-time visitor."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "клінічний контент під CHARTER" not in html
    assert 'class="eyebrow"' not in html


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
    # Bundle must be small enough for fast first-page load.
    # ~260KB at initial implementation (2026-Q1, ~200 entities); ~605KB
    # after the redflag-quality plan (2026-04-25); ~1MB after GI solid-
    # tumor batch + parallel hematology / thoracic / breast / prostate
    # expansions (2026-04-26 — 43+ diseases, 723+ entities); ~1.5MB after
    # heme 2L+ algorithms + drug curation (2026-04-27 — 1124 entities);
    # ~1.78MB after CSD-1..4 expansion (2026-04-26 — 1899 entities).
    # CSD-5B introduces a core+per-disease lazy-load split that will
    # eventually bring the on-load core back under ~1.5 MB; until /try.html
    # is wired to the new bundle index, we still ship the monolithic zip
    # as a fallback, so the ceiling here is bumped to 3 MB to absorb
    # ongoing KB growth without churning the test.
    # Pyodide first-load (≈10 MB) dominates UX latency, so the ceiling is
    # sized for headroom.
    assert zip_path.stat().st_size < 3_000_000, (
        f"engine bundle exceeds 3MB compressed: {zip_path.stat().st_size}"
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


# ── Language switcher + EN mirror ─────────────────────────────────────────


def test_en_mirror_built_alongside_ua(site_dir: Path):
    """Every public page has an /en/ counterpart so the language toggle
    can navigate between them without 404."""
    for page in ("index.html", "gallery.html", "try.html"):
        assert (site_dir / "en" / page).exists(), f"missing en/{page}"
    assert (site_dir / "en").is_dir()
    assert (site_dir / "en" / "cases").is_dir()
    # Every UA case has an EN counterpart at /en/cases/
    for c in CASES:
        assert (site_dir / "en" / "cases" / f"{c.case_id}.html").exists(), (
            f"missing en/cases/{c.case_id}.html"
        )


def test_lang_switch_present_on_every_top_level_page(site_dir: Path):
    """Toggle in the top bar lets the user flip UA↔EN on landing/gallery/try."""
    for page in ("index.html", "gallery.html", "try.html"):
        ua = (site_dir / page).read_text(encoding="utf-8")
        en = (site_dir / "en" / page).read_text(encoding="utf-8")
        # Toggle markup
        assert 'class="lang-switch"' in ua
        assert 'class="lang-switch"' in en
        # UA points to /en/<page>
        assert '/en/' in ua, f"UA {page} missing pointer to /en/"
        # EN points back to root (UA)
        # Either '/' (landing) or '/<page>' for gallery/try
        en_to_ua_target = "/" if page == "index.html" else f"/{page}"
        assert f'href="{en_to_ua_target}"' in en, (
            f"EN {page} lang-switch should link back to {en_to_ua_target}"
        )


def test_lang_switch_present_on_case_pages(site_dir: Path):
    """Per-case pages also carry a UA↔EN mini-toggle — toggle on a case
    must navigate to that same case in the other language."""
    sample_id = CASES[0].case_id
    ua_case = (site_dir / "cases" / f"{sample_id}.html").read_text(encoding="utf-8")
    en_case = (site_dir / "en" / "cases" / f"{sample_id}.html").read_text(encoding="utf-8")
    assert f"/en/cases/{sample_id}.html" in ua_case, "UA case missing EN twin link"
    assert f"/cases/{sample_id}.html" in en_case, "EN case missing UA twin link"


def test_try_cta_is_separate_action_button(site_dir: Path):
    """'Try it' is a high-conviction action, not a reading link. It must
    render as a distinct CTA button class — not a plain top-nav link."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert 'class="btn-cta-try"' in html, "Try CTA button missing from top bar"
    # Top reading-nav must not include the try link as a plain entry —
    # CTA lives in the right cluster, separated visually
    assert 'class="top-right"' in html


def test_en_pages_load_stylesheet_via_root_relative_path(site_dir: Path):
    """Regression: /en/index.html that links to a relative `style.css`
    resolves to /en/style.css and renders unstyled. Every page that lives
    at non-root depth must use a root-relative `/style.css` link."""
    for page in ("en/index.html", "en/gallery.html", "en/try.html"):
        html = (site_dir / page).read_text(encoding="utf-8")
        assert 'href="/style.css"' in html, (
            f"{page} must load /style.css via root-relative path"
        )
        # The broken pattern (relative without leading slash) must not appear
        # on the head <link>
        assert '<link href="style.css"' not in html, (
            f"{page} has a broken relative style.css link"
        )


def test_lang_switch_shows_flag_for_active_mode(site_dir: Path):
    """User direction: small flag indicates the active language. Uses
    CSS-painted mini flags (Windows doesn't render flag emoji, so emoji
    would fall back to letter pairs 'UA'/'GB' next to the labels)."""
    ua = (site_dir / "index.html").read_text(encoding="utf-8")
    en = (site_dir / "en" / "index.html").read_text(encoding="utf-8")
    # Both flag classes must appear on every top-level page (one current,
    # one in the toggle target)
    for page_html, name in ((ua, "UA index"), (en, "EN index")):
        assert "flag-ua" in page_html, f"{name} missing flag-ua class"
        assert "flag-en" in page_html, f"{name} missing flag-en class"
        assert 'class="lang-flag' in page_html, f"{name} missing lang-flag wrapper"


def test_en_landing_links_use_en_paths(site_dir: Path):
    """Top-bar links on /en/ pages must stay within /en/ scope (so the
    user keeps reading in English unless they explicitly toggle UA)."""
    en_index = (site_dir / "en" / "index.html").read_text(encoding="utf-8")
    # Gallery + Try links route through /en/ for EN nav
    assert "/en/gallery.html" in en_index
    assert "/en/try.html" in en_index
    # html lang attr is en
    assert '<html lang="en">' in en_index


# ── Privacy guard ─────────────────────────────────────────────────────────


def test_no_real_patient_initials_leak_into_site(site_dir: Path):
    forbidden = ["В.Д.В.", "V.D.V.", "В. Д. В.", "V. D. V."]
    for path in site_dir.rglob("*.html"):
        html = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in html, f"leaked '{token}' in {path.name}"
