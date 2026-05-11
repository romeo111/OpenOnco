"""Smoke test for the static-site builder (scripts/build_site.py).

Builds the full site into a tmp dir and asserts the structural contract:

- public landing (no auth gate) with hero + numerical metrics + Watson cmp
- public gallery with all publishable CASE entries
- try.html wired to Pyodide + example loader
- per-case files keep back-link + feedback link, no auth gate
- no real-patient data leaks
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest
import yaml

from scripts.build_site import (
    CASES,
    GALLERY_EXCLUDED_CASE_IDS,
    GALLERY_FEATURED_CASE_IDS,
    _public_example_entries,
    build_site,
    _example_sort_key,
    _render_top_bar,
    render_diseases,
)


@pytest.fixture(scope="module")
def site_dir(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("docs")
    build_site(out)
    return out


# ── Static assets ─────────────────────────────────────────────────────────


def test_static_assets_present(site_dir: Path):
    # CSD-9C dropped monolithic openonco-engine.zip — replaced by core + per-disease + index.
    for f in (".nojekyll", "CNAME", "style.css", "index.html", "gallery.html",
              "try.html", "ask.html", "openonco-engine-core.zip", "openonco-engine-index.json",
              "examples.json", "manifest.webmanifest", "kb.html", "kb_search_index.json",
              "ukr/kb.html", "ukr/kb_search_index.json",
              "clinical-gaps.html", "ukr/clinical-gaps.html",
              "audits/clinical_gap_audit.md", "audits/clinical_gap_audit.json"):
        assert (site_dir / f).exists(), f"missing {f}"


def test_ukrainian_diseases_page_localized_and_clean():
    html = render_diseases(None, target_lang="uk")
    assert 'id="DIS-NSCLC"' in html

    assert "Недрібноклітинний рак легені" in html
    assert "Біомарк." in html
    assert "Преп." in html
    assert "Показ." in html
    assert "Трив. озн." in html
    assert "STUB" not in html
    assert "Hand-authored" not in html
    assert "Clinical Co-Lead" not in html
    assert "Сер. верифікація" not in html
    assert html.index("Позначення в таблиці") < html.index("Покриття за хворобами")


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
    # Hero structure (v2 redesign: class="home-hero", commit after 48eb804e)
    assert 'class="home-hero"' in html
    # Primary CTA in hero (root-relative path since EN-default flip — commit 48eb804e)
    assert 'href="/try.html"' in html
    # Hero copy
    assert "oncology" in html.lower() or "онколог" in html.lower()


def test_capabilities_shows_numerical_metrics(site_dir: Path):
    """Project metrics live on /capabilities.html (moved off the landing
    in commit `25b0340` so the landing stays focused on the MDT story).

    The rich-card layout with per-metric textual explanations is the
    canonical place to show what's in the KB.

    UA labels live on /ukr/capabilities.html since the EN-default flip
    (commit 48eb804e) — the root /capabilities.html now renders English."""
    html = (site_dir / "ukr" / "capabilities.html").read_text(encoding="utf-8")
    assert 'class="num-grid num-grid--rich"' in html
    for label in ("Хвороби в KB", "Лікарі-скіли", "Режими лікування",
                  "Препарати", "Тести", "Workups", "Red flags",
                  "Джерела"):
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
    """Landing v2 redesign: the 'why this is needed' prose (`how-lead`) was
    removed from the home page to keep the first viewport focused on the product.
    The source-band (`home-source-band`) is the canonical non-hero section,
    replacing the old how/problem blocks. No 2-column problem-grid either."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert 'class="home-source-band"' in html
    assert 'class="problem-grid"' not in html
    assert 'class="how-lead"' not in html


def test_landing_how_section_uses_dataflow_stages(site_dir: Path):
    """Landing v2 redesign: the dataflow (INPUT → VERIFY → BIOMARKERS → OUTPUT)
    was removed from the home page. The landing is now a focused home-main layout
    with hero + source-band. Old step/dataflow/MDT embeds must be absent."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert 'class="home-main"' in html
    assert 'class="dataflow"' not in html
    assert '<ol class="steps">' not in html


def test_top_bar_drops_tester_pill(site_dir: Path):
    """Per user direction: 'Тестувальник · OSS preview' pill removed from header."""
    for page in ("index.html", "gallery.html", "try.html", "ask.html"):
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


def test_gallery_is_public_with_publishable_cases(site_dir: Path):
    html = (site_dir / "gallery.html").read_text(encoding="utf-8")
    assert "openOncoUser" not in html, "auth gate must be removed from gallery"
    public_cases = [
        c for c in CASES
        if c.case_id not in GALLERY_EXCLUDED_CASE_IDS
        and (
            not GALLERY_FEATURED_CASE_IDS
            or c.case_id in GALLERY_FEATURED_CASE_IDS
        )
    ]
    assert html.count('class="case-card"') == len(public_cases)
    assert "Curated showcase" in html
    assert 'class="dt-quality"' in html
    assert "No treatment plan generated" not in html
    for c in public_cases:
        assert f"cases/{c.case_id}.html" in html
    for c in CASES:
        if c.case_id in GALLERY_EXCLUDED_CASE_IDS:
            assert f"cases/{c.case_id}.html" not in html
    # Stats widget intentionally dropped from /gallery.html in commit 6234fe9b
    # (UA-leak cleanup on the EN gallery surface).
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
    # Engine bundle URL (CSD-9C lazy-load: core + per-disease modules)
    assert "openonco-engine-core.zip" in html
    assert "openonco-engine-index.json" in html
    # Example dropdown source
    assert "examples.json" in html


def test_try_page_has_pwa_manifest_and_build_status(site_dir: Path):
    html = (site_dir / "try.html").read_text(encoding="utf-8")
    ua_html = (site_dir / "ukr" / "try.html").read_text(encoding="utf-8")
    manifest = json.loads((site_dir / "manifest.webmanifest").read_text(encoding="utf-8"))

    assert 'rel="manifest" href="/manifest.webmanifest"' in html
    assert 'name="theme-color" content="#0a2e1a"' in html
    assert 'id="buildCard"' in html
    assert 'id="coreVersion"' in html
    assert 'id="diseaseVersion"' in html
    assert 'id="cacheState"' in html
    assert 'id="offlineState"' in html
    assert 'id="offlineModulesState"' in html
    assert 'id="offlineCacheFill"' in html
    assert "cacheAllBundlesForOffline" in html
    assert "scheduleOfflineCacheWarmup" in html
    assert "fetchJsonWithTimeout" in html
    assert 'id="questReadiness"' in html
    assert 'id="readinessCriticalText"' in html
    assert 'class="try-actions quest-cta quest-actions-top"' in html
    assert html.index('id="questReadiness"') < html.index('id="runBtn"') < html.index('class="quest-grid"')
    assert html.index('id="runBtn"') < html.index('id="buildCard"')
    assert "function updateWorkflowControls()" in html
    assert "actionLocked" in html
    assert ".status-top[hidden] { display: none; }" in (site_dir / "style.css").read_text(encoding="utf-8")
    assert "statusTopText.textContent = ''" in html
    assert 'class="quest-impact-card"' not in html
    assert 'rel="manifest" href="/manifest.webmanifest"' in ua_html

    assert manifest["start_url"] == "/try.html"
    assert manifest["display"] == "standalone"
    assert manifest["theme_color"] == "#0a2e1a"
    assert any(icon["src"] == "/logo.svg" for icon in manifest["icons"])


def test_ask_page_wires_clinical_question_endpoint(site_dir: Path):
    """Optional ChatGPT adapter: free-text case goes to a server endpoint,
    not directly to OpenAI from the browser."""
    html = (site_dir / "ask.html").read_text(encoding="utf-8")
    uk_html = (site_dir / "ukr" / "ask.html").read_text(encoding="utf-8")
    assert 'id="caseText"' in html
    assert 'id="endpointInput"' in html
    assert 'id="askBtn"' in html
    assert "/api/clinical-question" in html
    assert "OPENONCO_CLINICAL_QUESTION_ENDPOINT" in html
    assert "openonco-ask-user-id-v1" in html
    assert "MAX_QUESTIONS = 3" in html
    assert 'id="askExamples"' in html
    assert 'id="planGeneratorLink"' in html
    assert "CompressionStream" in html
    assert "try.html#p=" in html
    assert "engine_summary.ok === true" in html
    assert "questions_used" in html
    assert "OPENAI_API_KEY" not in html
    assert "api.openai.com" not in html
    for ask_html in (html, uk_html):
        assert 'property="og:image"' not in ask_html
        assert 'name="twitter:image"' not in ask_html
        assert 'name="twitter:card" content="summary"' in ask_html
        assert 'name="twitter:card" content="summary_large_image"' not in ask_html


# ── Engine bundle (Pyodide-loadable zip) ──────────────────────────────────


def test_engine_bundle_contains_runtime_modules(site_dir: Path):
    # CSD-9C: core bundle replaces monolithic openonco-engine.zip
    zip_path = site_dir / "openonco-engine-core.zip"
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
    (validation.loader scans hosted/content/ only). CSD-9C dropped monolithic;
    same exclusion contract now applies to core bundle."""
    zip_path = site_dir / "openonco-engine-core.zip"
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
    # ~1.78MB after CSD-1..4 expansion (2026-04-26 — 1899 entities);
    # ~3.88MB after CIViC pivot + solid-tumor expansion to 65 diseases
    # (2026-04-27 — 1810 entities, +CIViC snapshot data, +ESCAT actionability
    # records, +CSD-5/6/7 redflag-matrix and drug curation). CSD-5B core+per-
    # disease lazy-load split exists but the monolithic fallback zip is what
    # this test validates; ceiling bumped to 4MB to absorb ongoing growth.
    # Pyodide first-load (≈10 MB) dominates UX latency, so the ceiling is
    # sized for headroom.
    assert zip_path.stat().st_size < 4_000_000, (
        f"engine bundle exceeds 4MB compressed: {zip_path.stat().st_size}"
    )


# ── Examples payload ──────────────────────────────────────────────────────


def test_examples_payload_matches_cases(site_dir: Path):
    payload = json.loads((site_dir / "examples.json").read_text(encoding="utf-8"))
    case_ids_payload = {e["case_id"] for e in payload}
    case_ids_expected = {c.case_id for c in _public_example_entries()}
    assert case_ids_payload == case_ids_expected
    assert not (case_ids_payload & GALLERY_EXCLUDED_CASE_IDS)
    assert not any((e.get("case_id") or "").startswith(("auto-", "variant-")) for e in payload)
    assert not any("Auto-stub" in (e.get("label_en") or e.get("label") or "") for e in payload)
    assert not any("KB fill" in (e.get("label_en") or "") for e in payload)
    # Each entry has a parseable patient JSON
    for entry in payload:
        assert isinstance(entry["json"], dict)
        assert isinstance(entry.get("quality_rank"), int)
        assert entry.get("quality_label")
        assert entry.get("quality_label_en")
        assert entry.get("quality_class")
        assert "Auto-stub" not in entry.get("label", "")
        assert "Auto-stub" not in entry.get("label_en", "")
        # Engine-required top-level fields exist for non-diagnostic patients
        # (diagnostic patients have a different shape)


def test_examples_are_quality_ranked_in_try_picker(site_dir: Path):
    payload = json.loads((site_dir / "examples.json").read_text(encoding="utf-8"))
    nsclc = [entry for entry in payload if entry.get("disease_id") == "DIS-NSCLC"]
    assert nsclc, "NSCLC examples should be available for try.html"
    assert nsclc == sorted(nsclc, key=_example_sort_key)
    assert nsclc[0]["quality_tier"] == "showcase"
    try_html = (site_dir / "try.html").read_text(encoding="utf-8")
    assert '"quality_rank":' in try_html
    assert "function exampleDisplayLabel(ex)" in try_html
    assert "quality_rank" in try_html
    assert "Curated showcase" in try_html


def test_try_examples_are_curated_and_filter_by_disease_id(site_dir: Path):
    """Try-page examples are curated. Missing examples are better than
    surfacing old low-fill auto-stubs as if they were clinical examples.
    """
    examples = json.loads((site_dir / "examples.json").read_text(encoding="utf-8"))
    questionnaires = json.loads((site_dir / "questionnaires.json").read_text(encoding="utf-8"))

    example_disease_ids = {
        entry.get("disease_id")
        for entry in examples
        if entry.get("disease_id")
    }
    questionnaire_disease_ids = {
        q.get("disease_id")
        for q in questionnaires
        if q.get("disease_id")
    }
    hosted_disease_ids = {
        (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("id")
        for path in Path("knowledge_base/hosted/content/diseases").glob("*.yaml")
    }
    hosted_disease_ids.discard(None)

    assert hosted_disease_ids <= questionnaire_disease_ids
    assert example_disease_ids <= questionnaire_disease_ids
    for entry in examples:
        did = entry.get("disease_id")
        if did not in questionnaire_disease_ids:
            continue
        profile = entry.get("json") or {}
        profile_did = (
            (profile.get("disease") or {}).get("id")
            or profile.get("disease_id")
        )
        assert profile_did == did, entry["case_id"]

    html = (site_dir / "try.html").read_text(encoding="utf-8")
    assert '"disease_id":' in html
    assert "return ex.disease_id === wantDiseaseId" in html
    assert "ICD-O morphology is not unique enough" in html


def test_try_questionnaire_dropdown_titles_are_public_and_localized(site_dir: Path):
    en_html = (site_dir / "try.html").read_text(encoding="utf-8")
    uk_html = (site_dir / "ukr" / "try.html").read_text(encoding="utf-8")

    assert '"title_en": "Invasive breast cancer — first line"' in en_html
    assert '"title_en": "HCV-associated Marginal Zone Lymphoma — first line"' in en_html
    assert '"icd_10": "C50"' in en_html
    assert "ICD-10 ${icd10}" in en_html
    assert "openonco-manifests-v3" in en_html
    assert "getItem('openonco-manifests-v3')" in en_html
    assert "removeItem('openonco-manifests-v1')" in en_html
    assert "removeItem('openonco-manifests-v2')" in en_html
    assert "auto-generated STUB" not in en_html
    assert "q.title_uk || q.title_en || q.title" in uk_html
    assert '"title_uk": "Інвазивний рак молочної залози — перша лінія"' in uk_html
    assert '"icd_10": "C50"' in uk_html
    assert "auto-generated STUB" not in uk_html

    qsrc = Path("knowledge_base/hosted/content/questionnaires")
    assert not any(
        "auto-generated STUB" in line
        for path in qsrc.glob("*.yaml")
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("title:")
    )


# ── Per-case files ────────────────────────────────────────────────────────


def test_case_files_have_back_link_and_no_auth(site_dir: Path):
    # Root /cases/ now renders EN since the EN-default flip (commit 48eb804e);
    # UA back-link "Назад до галереї" lives at /ukr/cases/<id>.html.
    for c in CASES:
        path = site_dir / "cases" / f"{c.case_id}.html"
        if c.case_id in GALLERY_EXCLUDED_CASE_IDS:
            assert not path.exists(), f"excluded case file leaked: {path.name}"
            continue
        assert path.exists(), f"case file missing: {path.name}"
        html = path.read_text(encoding="utf-8")
        assert html.startswith("<!DOCTYPE html>")
        assert "</html>" in html
        assert "openOncoUser" not in html, f"{c.case_id} retains auth gate"
        assert "Back to gallery" in html
        assert "tester-feedback" in html


# ── Language switcher + UA mirror ─────────────────────────────────────────
# Site layout flipped in commit 48eb804e: EN is now default at root, UA
# moved to /ukr/. These tests preserve the original "secondary mirror
# exists / lang switch points to twin" semantics with the path direction
# reversed.


def test_en_mirror_built_alongside_ua(site_dir: Path):
    """Every public page has a /ukr/ counterpart so the language toggle
    can navigate between them without 404."""
    for page in ("index.html", "gallery.html", "try.html", "ask.html"):
        assert (site_dir / "ukr" / page).exists(), f"missing ukr/{page}"
    assert (site_dir / "ukr").is_dir()
    assert (site_dir / "ukr" / "cases").is_dir()
    # Every EN case has a UA counterpart at /ukr/cases/
    for c in CASES:
        path = site_dir / "ukr" / "cases" / f"{c.case_id}.html"
        if c.case_id in GALLERY_EXCLUDED_CASE_IDS:
            assert not path.exists(), f"excluded UA case file leaked: {path.name}"
            continue
        assert path.exists(), (
            f"missing ukr/cases/{c.case_id}.html"
        )


def test_lang_switch_present_on_every_top_level_page(site_dir: Path):
    """Toggle in the top bar lets the user flip EN↔UA on landing/gallery/try."""
    for page in ("index.html", "gallery.html", "try.html", "ask.html"):
        en = (site_dir / page).read_text(encoding="utf-8")
        ua = (site_dir / "ukr" / page).read_text(encoding="utf-8")
        # Toggle markup
        assert 'class="lang-switch"' in en
        assert 'class="lang-switch"' in ua
        # EN points to /ukr/<page>
        assert '/ukr/' in en, f"EN {page} missing pointer to /ukr/"
        # UA points back to root (EN)
        # Either '/' (landing) or '/<page>' for gallery/try
        ua_to_en_target = "/" if page == "index.html" else f"/{page}"
        assert f'href="{ua_to_en_target}"' in ua, (
            f"UA {page} lang-switch should link back to {ua_to_en_target}"
        )


def test_lang_switch_present_on_case_pages(site_dir: Path):
    """Per-case pages also carry an EN↔UA mini-toggle — toggle on a case
    must navigate to that same case in the other language."""
    sample_id = CASES[0].case_id
    en_case = (site_dir / "cases" / f"{sample_id}.html").read_text(encoding="utf-8")
    ua_case = (site_dir / "ukr" / "cases" / f"{sample_id}.html").read_text(encoding="utf-8")
    assert f"/ukr/cases/{sample_id}.html" in en_case, "EN case missing UA twin link"
    assert f"/cases/{sample_id}.html" in ua_case, "UA case missing EN twin link"


def test_try_cta_is_separate_action_button(site_dir: Path):
    """The plan builder is a high-conviction action, not a reading link. It must
    render as a distinct CTA button class — not a plain top-nav link."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert 'class="btn-cta-top btn-cta-try"' in html, "Plan Builder CTA missing from top bar"
    assert "Plan Builder" in html
    assert "Try it" not in html
    # Top reading-nav must not include the try link as a plain entry —
    # CTA lives in the right cluster, separated visually
    assert 'class="top-right"' in html
    assert 'class="top-cta-group"' in html


def test_home_hero_avoids_duplicate_top_actions(site_dir: Path):
    """The top bar owns the three product actions; the home hero keeps one
    primary next step so the first viewport stays focused."""
    html = (site_dir / "ukr" / "index.html").read_text(encoding="utf-8")
    hero = html.split('<section class="home-hero">', 1)[1].split("</section>", 1)[0]
    assert hero.count('class="btn ') == 1
    assert 'href="/ukr/try.html"' in hero
    assert 'href="/ukr/kb.html"' not in hero
    assert 'href="/ukr/ask.html"' not in hero
    assert 'class="home-source-band"' in html


def test_top_bar_wraps_before_tablet_width(site_dir: Path):
    """Header must wrap before common 768px tablet widths because the right
    cluster now includes language switch plus three CTA buttons."""
    css = (site_dir / "style.css").read_text(encoding="utf-8")
    assert "@media (max-width: 900px)" in css


def test_try_page_uses_plan_builder_language(site_dir: Path):
    html = (site_dir / "try.html").read_text(encoding="utf-8")
    ua_html = (site_dir / "ukr" / "try.html").read_text(encoding="utf-8")
    assert "<h1>Plan Builder</h1>" in html
    assert "Try it with a virtual patient" not in html
    assert "<h1>План лікування</h1>" in ua_html
    assert "Спробувати з віртуальним пацієнтом" not in ua_html


def test_top_nav_uses_single_onco_wiki_entry():
    """Diseases stay addressable by URL, but Wiki is a top action, not a nav duplicate."""
    for html, wiki_label, board_label in (
        (_render_top_bar(active="home", target_lang="en"), "Onco Wiki", "Tumor Board"),
        (_render_top_bar(active="diseases", target_lang="en"), "Onco Wiki", "Tumor Board"),
        (_render_top_bar(active="home", target_lang="uk"), "Онко-вікі", "Туморборд"),
        (_render_top_bar(active="diseases", target_lang="uk"), "Онко-вікі", "Туморборд"),
    ):
        nav = html.split('<nav class="top-nav">', 1)[1].split("</nav>", 1)[0]
        actions = html.split('<div class="top-cta-group">', 1)[1].split("</div>", 1)[0]
        assert wiki_label in actions
        assert board_label in actions
        assert wiki_label not in nav
        assert board_label not in nav
        assert "KB Search" not in nav
        assert 'href="/diseases.html"' not in nav
        assert 'href="/ukr/diseases.html"' not in nav


def test_en_pages_load_stylesheet_via_root_relative_path(site_dir: Path):
    """Regression: a non-root page that links to relative `style.css`
    resolves to a sibling-relative path and renders unstyled. Every page
    that lives at non-root depth must use a root-relative `/style.css` link.

    The non-root tier is now /ukr/ (commit 48eb804e flipped EN to root)."""
    for page in ("ukr/index.html", "ukr/gallery.html", "ukr/try.html"):
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
    would fall back to letter pairs 'UA'/'GB' next to the labels).

    Root index is EN since commit 48eb804e; UA mirror at /ukr/index.html."""
    en = (site_dir / "index.html").read_text(encoding="utf-8")
    ua = (site_dir / "ukr" / "index.html").read_text(encoding="utf-8")
    # Both flag classes must appear on every top-level page (one current,
    # one in the toggle target)
    for page_html, name in ((en, "EN index"), (ua, "UA index")):
        assert "flag-ua" in page_html, f"{name} missing flag-ua class"
        assert "flag-en" in page_html, f"{name} missing flag-en class"
        assert 'class="lang-flag' in page_html, f"{name} missing lang-flag wrapper"


def test_en_landing_links_use_en_paths(site_dir: Path):
    """Top-bar links on /ukr/ pages must stay within /ukr/ scope (so the
    user keeps reading in Ukrainian unless they explicitly toggle EN).

    Direction flipped in commit 48eb804e: UA is now the secondary tier.
    Landing v2 redesign removed Gallery from the nav; Try is the primary CTA."""
    ua_index = (site_dir / "ukr" / "index.html").read_text(encoding="utf-8")
    # Try link routes through /ukr/ for UA nav
    assert "/ukr/try.html" in ua_index
    # html lang attr is uk
    assert '<html lang="uk">' in ua_index


# ── Privacy guard ─────────────────────────────────────────────────────────


def test_no_real_patient_initials_leak_into_site(site_dir: Path):
    forbidden = ["В.Д.В.", "V.D.V.", "В. Д. В.", "V. D. V."]
    for path in site_dir.rglob("*.html"):
        html = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in html, f"leaked '{token}' in {path.name}"
