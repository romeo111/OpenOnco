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
    BROKEN_CASE_IDS,
    CASES,
    GALLERY_EXCLUDED_CASE_IDS,
    GALLERY_FEATURED_CASE_IDS,
    _public_case_entries,
    _public_example_entries,
    build_one_case_patient,
    build_site,
    _example_sort_key,
    _render_top_bar,
    render_diseases,
)
from knowledge_base.engine import is_diagnostic_profile


@pytest.fixture(scope="module")
def site_dir(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("docs")
    build_site(out)
    return out


# ── Static assets ─────────────────────────────────────────────────────────


def test_static_assets_present(site_dir: Path):
    # CSD-9C dropped monolithic openonco-engine.zip — replaced by core + per-disease + index.
    for f in (".nojekyll", "CNAME", "style.css", "index.html", "gallery.html",
              "try.html", "prevent.html", "ask.html",
              "openonco-engine-core.zip", "openonco-engine-index.json",
              "examples.json", "manifest.webmanifest", "kb.html", "kb_search_index.json",
              "ukr/prevent.html",
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
    """Landing v3 (role-router redesign): the old 'why this is needed' prose
    (`how-lead`) and 2-column problem-grid stay gone. The canonical non-hero
    sections are now the role doors (`home-doors`) plus the how-it-works steps;
    the old source-band prose was folded into the trust line."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert 'class="home-doors"' in html
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
    for page in ("index.html", "gallery.html", "try.html", "prevent.html", "ask.html"):
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


def test_loading_example_keeps_personalize_button_reachable(site_dir: Path):
    """Loading an example preloads its plan without opening a modal over
    the banner that unlocks the prefilled fields."""
    for path in (site_dir / "try.html", site_dir / "ukr" / "try.html"):
        html = path.read_text(encoding="utf-8")
        loader = html.split("async function loadExamplePlan", 1)[1].split(
            "function clearPlanState", 1
        )[0]
        assert "resultFrame.src =" in loader, f"{path}: example plan is not preloaded"
        assert "openPlanModal" not in loader, f"{path}: modal blocks personalize button"


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


def test_prevent_page_is_consumer_diagnostic_flow(site_dir: Path):
    """The prevention page is a real consumer-facing risk and early-signal
    workflow, not a clinician-only JSON form."""
    html = (site_dir / "prevent.html").read_text(encoding="utf-8")
    uk_html = (site_dir / "ukr" / "prevent.html").read_text(encoding="utf-8")

    for page_html in (html, uk_html):
        assert 'class="risk-page consumer-risk-assessment"' in page_html
        assert 'id="riskForm"' in page_html
        assert 'id="familyCancerRows"' in page_html
        assert 'id="pedigreeMap"' in page_html
        assert 'name="fit_result"' in page_html
        assert 'name="breast_imaging"' in page_html
        assert 'id="profileJson"' in page_html
        assert "consumer_prevention_and_early_detection_check" in page_html
        assert "CompressionStream" in page_html
        assert "openTryBtn.href = TRY_HREF + '#p='" in page_html
        assert "Color Health" in page_html
        assert "CancerIQ" in page_html
        assert "Freenome" in page_html
        assert "GRAIL Galleri" in page_html
        assert "Prenuvo" in page_html
        assert "USPSTF" in page_html
        assert "not a diagnosis" in page_html or "не діагноз" in page_html

    assert "Check risk, family history, screenings" in html
    assert "Перевірте ризик, родовід, скринінги" in uk_html


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
    # disease lazy-load split is now canonical. The core reached 4.13 MB after
    # the 2026-08 structured-drug/source expansion; keep a narrow 4.25 MB
    # ceiling so further growth must be deliberately sharded.
    # Pyodide first-load (≈10 MB) dominates UX latency, so the ceiling is
    # sized for headroom.
    assert zip_path.stat().st_size < 4_250_000, (
        f"engine bundle exceeds 4.25MB compressed: {zip_path.stat().st_size}"
    )


# ── Examples payload ──────────────────────────────────────────────────────


def test_try_page_has_example_search_input(site_dir: Path):
    """A search input must be available near the examples picker so
    users can find examples across diseases (not just the active one)."""
    for path in (site_dir / "try.html", site_dir / "ukr" / "try.html"):
        html = path.read_text(encoding="utf-8")
        assert 'id="exampleSearch"' in html, f"{path}: missing exampleSearch input"
        assert 'id="exampleSearchCount"' in html, f"{path}: missing search count chip"
        assert 'id="exampleSearchClear"' in html, f"{path}: missing clear button"
        assert "function exampleSearchBlob" in html, f"{path}: missing JS search helper"
        assert "function exampleSearchMatches" in html, f"{path}: missing match helper"


def test_examples_manifest_carries_searchable_fields(site_dir: Path):
    """The inlined EXAMPLES_MANIFEST on /try.html must include the
    enriched search tokens — disease names, biomarker ids, regimen
    name, line of therapy — otherwise the search bar would find nothing."""
    html = (site_dir / "try.html").read_text(encoding="utf-8")
    # Locate the inline manifest JS array.
    import re as _re
    m = _re.search(r"const EXAMPLES_MANIFEST = (\[.*?\]);\nconst PAGE_LANG", html, _re.S)
    assert m, "EXAMPLES_MANIFEST inline literal not found"
    manifest = json.loads(m.group(1))
    assert manifest, "EXAMPLES_MANIFEST is empty"
    # Spot-check every required field is present on at least 50% of entries
    # (every entry should have these — diagnostic-only profiles may lack a
    # regimen/line, which is fine).
    keys_required = {
        "case_id", "label", "label_en", "summary", "summary_en",
        "disease_id", "disease_name_en", "disease_name_ua",
        "biomarker_ids", "category",
    }
    sample = manifest[0]
    for k in keys_required:
        assert k in sample, f"manifest entry missing key: {k}"
    # At least some entries carry line_of_therapy + regimen_name (verified ones).
    assert any(e.get("regimen_name") for e in manifest), \
        "no manifest entry has regimen_name — search by FOLFOX/CHOEP/etc will fail"
    assert any(e.get("line_of_therapy") is not None for e in manifest), \
        "no manifest entry has line_of_therapy — search by '2L' will fail"


def test_verified_examples_reach_public_payload(site_dir: Path):
    """Verified-treatment-example case ids must show up in docs/examples.json."""
    payload = json.loads((site_dir / "examples.json").read_text(encoding="utf-8"))
    verified = [e for e in payload if (e.get("case_id") or "").startswith("verified-")]
    # At least 10 — generator runs may produce more or fewer, but a near-zero
    # count signals the auto-block wasn't picked up by the build.
    assert len(verified) >= 10, (
        f"only {len(verified)} verified examples in payload — site_cases "
        f"auto-block may be missing or unreadable"
    )
    for entry in verified:
        assert entry.get("quality_label_en"), entry["case_id"]
        # Every verified patient JSON carries the target indication.
        assert entry["json"].get("_target_indication_id"), entry["case_id"]


def test_examples_payload_matches_cases(site_dir: Path):
    payload = json.loads((site_dir / "examples.json").read_text(encoding="utf-8"))
    case_ids_payload = {e["case_id"] for e in payload}
    case_ids_expected = {c.case_id for c in _public_example_entries()}
    assert case_ids_payload == case_ids_expected
    # The picker is intentionally more permissive than the curated gallery:
    # it must still exclude every broken case, but it MAY include
    # GALLERY_ONLY_HIDDEN_CASE_IDS (HCC/RCC patient cases, etc.) so that
    # every supported disease has at least one usable load-example entry.
    assert not (case_ids_payload & BROKEN_CASE_IDS)
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
        assert entry.get("scenario_type")
        assert entry.get("verification_required") is True
        assert "Auto-stub" not in entry.get("label", "")
        assert "Auto-stub" not in entry.get("label_en", "")
        # Engine-required top-level fields exist for non-diagnostic patients
        # (diagnostic patients have a different shape)


def test_examples_payload_flags_patient_mode(site_dir: Path):
    """PATIENT_MODE_SPEC §3: patient mode is treatment-only.

    Every example in examples.json must carry a `has_patient_mode` flag.
    The flag is True iff the example is treatment-shape (not diagnostic),
    so the try-page modal knows whether to enable the audience toggle.
    """
    payload = json.loads((site_dir / "examples.json").read_text(encoding="utf-8"))
    for entry in payload:
        assert "has_patient_mode" in entry, (
            f"Example {entry.get('case_id')} missing has_patient_mode flag"
        )
        # Verify the flag matches the engine's diagnostic-profile detector
        ex_json = entry.get("json", {})
        expected = not is_diagnostic_profile(ex_json)
        assert entry["has_patient_mode"] == expected, (
            f"Example {entry.get('case_id')}: has_patient_mode="
            f"{entry['has_patient_mode']} but is_diagnostic_profile="
            f"{is_diagnostic_profile(ex_json)}"
        )


def test_curated_treatment_examples_have_patient_twin(site_dir: Path):
    """Every treatment-shape curated example has a patient twin built at
    /cases/<id>.patient.html (UA-only per PATIENT_MODE_SPEC §3 — a single
    file serves both EN and UA visitors)."""
    payload = json.loads((site_dir / "examples.json").read_text(encoding="utf-8"))
    treatment_ids = [
        e["case_id"] for e in payload if e.get("has_patient_mode")
    ]
    assert treatment_ids, "expected at least one treatment-shape example"
    missing = [
        cid for cid in treatment_ids
        if not (site_dir / "cases" / f"{cid}.patient.html").exists()
    ]
    assert not missing, f"Missing patient twins: {missing[:5]}"
    # Patient twins for diagnostic examples MUST NOT exist (would mislead)
    diagnostic_ids = [
        e["case_id"] for e in payload if not e.get("has_patient_mode")
    ]
    stray = [
        cid for cid in diagnostic_ids
        if (site_dir / "cases" / f"{cid}.patient.html").exists()
    ]
    assert not stray, f"Patient twin generated for diagnostic example: {stray}"


def test_patient_twin_has_required_anchors(site_dir: Path):
    """PATIENT_MODE_SPEC §3 anchors must be present in the patient HTML so
    downstream tests + accessibility tooling can locate the major sections.
    """
    # Pick a known-curated treatment example
    payload = json.loads((site_dir / "examples.json").read_text(encoding="utf-8"))
    pick = next(
        (e for e in payload
         if e.get("has_patient_mode") and e["case_id"] == "aitl-cd30-negative"),
        None,
    )
    assert pick is not None, "expected aitl-cd30-negative in curated examples"
    twin = site_dir / "cases" / f"{pick['case_id']}.patient.html"
    assert twin.exists()
    body = twin.read_text(encoding="utf-8")
    for anchor in (
        'class="patient-report"',
        'class="what-was-found"',
        'class="what-now"',
        'class="emergency-signals"',
        'class="ask-doctor"',
        'class="patient-disclaimer"',
    ):
        assert anchor in body, f"Patient twin missing anchor: {anchor}"
    # Sibling chip back to the UA clinician twin so deep-linked patient
    # pages round-trip to the doctor view
    assert "/ukr/cases/aitl-cd30-negative.html" in body


def test_try_html_wires_patient_mode_for_examples(site_dir: Path):
    """The audience toggle in /try.html must be wired for example-source
    plans (not just engine-generated ones). The wiring is a build-time
    JS constant (EXAMPLE_PATIENT_MODE_BY_ID) plus an updated mode-switch
    handler that loads /cases/<id>.patient.html in the iframe.
    """
    for path in (site_dir / "try.html", site_dir / "ukr" / "try.html"):
        body = path.read_text(encoding="utf-8")
        assert "EXAMPLE_PATIENT_MODE_BY_ID" in body, (
            f"{path} missing EXAMPLE_PATIENT_MODE_BY_ID lookup"
        )
        assert "activeExampleHasPatient" in body, (
            f"{path} missing activeExampleHasPatient state"
        )
        assert ".patient.html" in body, (
            f"{path} mode-switch never loads a patient twin"
        )


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
    assert "patient_view_available" in try_html
    assert ".patient.html" in try_html
    capabilities_html = (site_dir / "capabilities.html").read_text(encoding="utf-8")
    assert f"{len(_public_example_entries())} public examples" in capabilities_html
    assert "586 cases" not in capabilities_html
    assert "verified variant profiles" not in capabilities_html


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

    # A questionnaire is an optional authoring aid, not the definition of
    # whether a disease or molecular evidence example can be published.
    # Diagnostic, prevention, and molecular examples without a disease-
    # specific questionnaire fall back to their supplied JSON profile in the
    # try page. Treatment scenarios must retain a questionnaire match.
    no_questionnaire_examples = [
        entry for entry in examples
        if entry.get("disease_id") not in questionnaire_disease_ids
    ]
    assert no_questionnaire_examples
    assert all(
        entry.get("scenario_type") in {"diagnostic", "prevention", "molecular"}
        for entry in no_questionnaire_examples
    )
    assert all(entry.get("questionnaire_available") is False for entry in no_questionnaire_examples)
    assert all(
        entry.get("questionnaire_available") is True
        for entry in examples
        if entry.get("disease_id") in questionnaire_disease_ids
    )
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


def test_questionnaire_bundle_exposes_explicit_clinician_confirmation_gates(site_dir: Path):
    questionnaires = json.loads((site_dir / "questionnaires.json").read_text(encoding="utf-8"))
    aml = next(q for q in questionnaires if q["id"] == "QUEST-AML-1L-STUB")
    confirmation_group = next(
        group for group in aml["groups"] if group["title"] == "Clinician / MDT confirmations"
    )
    assert confirmation_group["questions"]
    assert all(
        question["field"].startswith("clinician_confirmations.CC-")
        and question["type"] == "boolean"
        and "never inferred" in question["helper"]
        and "default_value" not in question
        for question in confirmation_group["questions"]
    )


# ── Per-case files ────────────────────────────────────────────────────────


def test_case_files_have_back_link_and_no_auth(site_dir: Path):
    # Root /cases/ now renders EN since the EN-default flip (commit 48eb804e);
    # UA back-link "Назад до галереї" lives at /ukr/cases/<id>.html.
    for c in _public_case_entries():
        path = site_dir / "cases" / f"{c.case_id}.html"
        assert path.exists(), f"case file missing: {path.name}"
        html = path.read_text(encoding="utf-8")
        assert html.startswith("<!DOCTYPE html>")
        assert "</html>" in html
        assert "openOncoUser" not in html, f"{c.case_id} retains auth gate"
        assert "Back to gallery" in html
        assert "tester-feedback" in html
        assert "Do not self-treat" in html
        if c.scenario_type != "diagnostic":
            assert (site_dir / "cases" / f"{c.case_id}.patient.html").exists()

    for c in CASES:
        if c.visibility != "public":
            assert not (site_dir / "cases" / f"{c.case_id}.html").exists()


# ── Language switcher + UA mirror ─────────────────────────────────────────
# Site layout flipped in commit 48eb804e: EN is now default at root, UA
# moved to /ukr/. These tests preserve the original "secondary mirror
# exists / lang switch points to twin" semantics with the path direction
# reversed.


def test_en_mirror_built_alongside_ua(site_dir: Path):
    """Every public page has a /ukr/ counterpart so the language toggle
    can navigate between them without 404."""
    for page in ("index.html", "gallery.html", "try.html", "prevent.html", "ask.html"):
        assert (site_dir / "ukr" / page).exists(), f"missing ukr/{page}"
    assert (site_dir / "ukr").is_dir()
    assert (site_dir / "ukr" / "cases").is_dir()
    # Every EN case has a UA counterpart at /ukr/cases/
    for c in _public_case_entries():
        path = site_dir / "ukr" / "cases" / f"{c.case_id}.html"
        assert path.exists(), (
            f"missing ukr/cases/{c.case_id}.html"
        )
        if c.scenario_type != "diagnostic":
            assert (site_dir / "ukr" / "cases" / f"{c.case_id}.patient.html").exists()


def test_lang_switch_present_on_every_top_level_page(site_dir: Path):
    """Toggle in the top bar lets the user flip EN↔UA on landing/gallery/try."""
    for page in ("index.html", "gallery.html", "try.html", "prevent.html", "ask.html"):
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
    """Role-router redesign: the top bar owns the product actions and the hero
    is copy-only — the role doors immediately below it carry the primary next
    steps, so the hero never duplicates the top-bar actions."""
    html = (site_dir / "ukr" / "index.html").read_text(encoding="utf-8")
    hero = html.split('<section class="home-hero">', 1)[1].split("</section>", 1)[0]
    # Hero carries no inline CTAs of its own; the doors section owns them.
    assert hero.count('class="btn ') == 0
    assert 'href="/ukr/try.html"' not in hero
    assert 'href="/ukr/kb.html"' not in hero
    assert 'href="/ukr/ask.html"' not in hero
    # The role doors are the canonical primary-action surface.
    assert 'class="home-doors"' in html
    assert 'door-card--doctor' in html
    assert 'door-card--patient' in html


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


# ── IP → language auto-selection ──────────────────────────────────────────
# openonco.info is a static site, so language auto-selection by IP runs
# client-side: a head script redirects English pages to their /ukr/ twin only
# when the visitor's IP resolves to Ukraine. Default is English everywhere.


def test_geo_lang_redirect_injected_on_every_page(site_dir: Path):
    """Every built page (EN root, UA mirror, case pages) carries the geo
    language-redirect script in its <head>, and it is injected exactly once."""
    for page in ("index.html", "ukr/index.html", "gallery.html",
                 "ukr/gallery.html", "kb.html", "ukr/kb.html"):
        html = (site_dir / page).read_text(encoding="utf-8")
        assert html.count("<!-- openonco-geo-lang:start -->") == 1, (
            f"{page} missing/duplicated geo-lang block"
        )
        assert "<!-- openonco-geo-lang:end -->" in html
        # Script lives inside <head>, after the charset meta (charset stays first).
        start = html.index("<!-- openonco-geo-lang:start -->")
        assert html.lower().index("<head") < start < html.lower().index("</head")
        assert html.lower().index("charset") < start


def test_geo_lang_redirect_behaviour_markers(site_dir: Path):
    """Guard the core behavioural contract of the redirect script so a future
    refactor cannot silently drop a safety rail."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    block = html.split("<!-- openonco-geo-lang:start -->", 1)[1].split(
        "<!-- openonco-geo-lang:end -->", 1
    )[0]
    # Ukraine is the only country that flips to Ukrainian.
    assert "cc==='UA'?'uk':'en'" in block
    # Manual choice is remembered and read back so it overrides the IP guess.
    assert "localStorage.setItem('oo_lang'" in block
    assert "localStorage.getItem('oo_lang')" in block
    # Iframed previews (try.html result frame) are skipped.
    assert "window.top!==window.self" in block
    # Bots are not redirected (keeps both language trees crawlable).
    assert "Googlebot" not in block  # matched generically, not by name
    assert "/bot|crawl|spider" in block
    # No API key is embedded (static public site) and referrers are not leaked.
    assert "referrerPolicy:'no-referrer'" in block
    assert "api_key" not in block.lower() and "apikey" not in block.lower()
    # Legacy /en/ redirect stubs bail (no /ukr/en/ twin exists).
    assert "/^\\/en(\\/|$)/" in block
    # A slow async lookup must not yank a visitor who has started interacting.
    assert "if(!touched)go(want(code))" in block
    # Third-party surface minimized: GeoJS + ipapi.co only (ipwho.is dropped);
    # exactly two https geo endpoints in the fallback chain.
    assert "get.geojs.io" in block and "ipapi.co" in block
    assert "ipwho.is" not in block
    assert block.count("https://") == 2


def test_geo_lang_redirect_skips_redirect_stubs_and_404():
    """inject_geo_lang_redirect must never place (and must strip) the script on
    redirect stubs (legacy /en/ tree carries <meta http-equiv=refresh> and has
    no /ukr/en/ twin) or on 404.html (served for arbitrary missing paths, so a
    mirror hop only 404s again)."""
    from scripts.site_head import GEO_LANG_START, inject_geo_lang_redirect

    normal = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
              "<title>x</title></head><body></body></html>")
    stub = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta http-equiv="refresh" content="0; url=/">'
            "</head><body></body></html>")

    # normal content page gets the block
    injected = inject_geo_lang_redirect(normal, path="index.html")
    assert GEO_LANG_START in injected

    # redirect stub never gets it (regardless of path)
    assert GEO_LANG_START not in inject_geo_lang_redirect(stub)
    assert GEO_LANG_START not in inject_geo_lang_redirect(stub, path="en/index.html")

    # 404 page (detected by path) never gets it
    assert GEO_LANG_START not in inject_geo_lang_redirect(normal, path="404.html")

    # already-injected page that is a stub -> block stripped back out (idempotent)
    stubbed = injected.replace(
        '<meta charset="utf-8">',
        '<meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/">',
    )
    assert GEO_LANG_START not in inject_geo_lang_redirect(stubbed, path="en/index.html")


def test_geo_lang_does_not_break_charset_or_seo(site_dir: Path):
    """The injection must not displace the SEO block or the charset meta."""
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "<!-- openonco-seo:start -->" in html
    # charset < geo-lang < seo-block ordering keeps charset within the first bytes
    assert (
        html.lower().index("charset")
        < html.index("<!-- openonco-geo-lang:start -->")
        < html.index("<!-- openonco-seo:start -->")
    )


# ── Privacy guard ─────────────────────────────────────────────────────────


def test_no_real_patient_initials_leak_into_site(site_dir: Path):
    forbidden = ["В.Д.В.", "V.D.V.", "В. Д. В.", "V. D. V."]
    for path in site_dir.rglob("*.html"):
        html = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in html, f"leaked '{token}' in {path.name}"
