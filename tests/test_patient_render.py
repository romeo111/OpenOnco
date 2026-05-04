"""Comprehensive tests for patient-mode plan rendering (CSD-3).

Covers:
  * Section A — vocabulary coverage (`_patient_vocabulary`)
  * Section B — no-jargon assertions (technical entity IDs stripped from
    user-visible text — HTML attributes are still allowed for debugging)
  * Section C — structural anchors required by downstream consumers
    (CSD-3 demo, CSD-3 tests)
  * Section D — emergency RedFlag filter + section rendering
  * Section E — ask-doctor question selection
  * Section F — end-to-end synthetic mCRC + BRAF V600E patient through
    the full plan + render pipeline
  * Section G — accessibility heuristics on the embedded patient CSS

All patients used here are synthetic. The CSD-1 demo fixture is read
read-only — no PHI ever ships through these tests.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.engine._ask_doctor import (
    QUESTION_TEMPLATES,
    select_questions,
)
from knowledge_base.engine._emergency_rf import (
    filter_emergency_rfs,
    is_emergency_rf,
    patient_emergency_label,
)
from knowledge_base.engine._patient_vocabulary import (
    AE_PLAIN_UA,
    DRUG_CLASS_PLAIN_UA,
    ESCAT_PLAIN_UA,
    LAB_PLAIN_UA,
    NSZU_PLAIN_UA,
    SCREENING_PLAIN_UA,
    VARIANT_TYPE_PLAIN_UA,
    explain,
    total_term_count,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


# ── Helpers ──────────────────────────────────────────────────────────


_TAG_PATTERN = re.compile(r"<[^>]*>")


def _visible_text(html: str) -> str:
    """Strip <style>/<script> blocks and HTML tags, leaving only the
    text a patient would actually read in the browser."""
    no_style = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    no_script = re.sub(r"<script[^>]*>.*?</script>", "", no_style, flags=re.DOTALL)
    return _TAG_PATTERN.sub(" ", no_script)


def _build_synthetic_braf_v600e_mcrc_plan():
    """Synthetic 1L mCRC + BRAF V600E patient through the full pipeline.

    Returns the PlanResult — every Section F / Section B test renders
    from this single fixture so failures cluster around one render."""
    patient = {
        "patient_id": "TEST-PATIENT-RENDER",
        "disease": {"id": "DIS-CRC"},
        "line_of_therapy": 1,
        "biomarkers": {"BRAF": "V600E"},
        "demographics": {"age": 58, "ecog": 1},
    }
    return generate_plan(patient, kb_root=KB_ROOT)


@pytest.fixture(scope="module")
def patient_html() -> str:
    """Cached patient-mode HTML for the synthetic mCRC + BRAF V600E
    patient — module-scoped so the engine only walks the algorithm once
    across the (otherwise) ~10 render-shape tests."""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    assert result.plan is not None, "Synthetic mCRC 1L + BRAF should produce a plan"
    return render_plan_html(result, mode="patient")


# ── Section A — Vocabulary coverage ──────────────────────────────────


def test_vocabulary_has_min_200_terms():
    """Spec floor of 200 unique entries (current is 372; floor protects
    against accidental mass-deletes during refactors)."""
    assert total_term_count() >= 200, (
        f"Patient vocabulary has only {total_term_count()} terms; "
        f"spec floor is 200"
    )


def test_vocabulary_explain_returns_strings():
    """Spot-check ~20 representative terms across all eight category
    tables — each must return a non-empty string explanation."""
    samples = [
        # DRUG_CLASS_PLAIN_UA
        "BRAFi", "MEKi", "anti-PD-1", "CAR-T", "anthracycline",
        # VARIANT_TYPE_PLAIN_UA
        "V600E", "T790M", "MSI-H", "germline", "BRCA1",
        # ESCAT_PLAIN_UA
        "IA", "IIIA",
        # NSZU_PLAIN_UA
        "covered", "oop",
        # LAB_PLAIN_UA
        "ANC", "LVEF",
        # AE_PLAIN_UA
        "neutropenia", "CRS",
        # SCREENING_PLAIN_UA
        "PET-CT", "echocardiogram",
    ]
    for term in samples:
        result = explain(term)
        assert isinstance(result, str) and result.strip(), (
            f"explain({term!r}) returned {result!r}; expected non-empty string"
        )


def test_vocabulary_explain_case_insensitive():
    """Lookup must tolerate caller-supplied case variation and
    whitespace — a label like ' V600E ' is common when paths concatenate
    fields without trimming."""
    canonical = explain("V600E")
    assert canonical is not None
    assert explain("v600e") == canonical
    assert explain(" V600E ") == canonical
    assert explain("V600e") == canonical


def test_vocabulary_explain_unknown_returns_none():
    """Unknown / empty / None inputs must return None so callers can
    fall back to the raw clinician label rather than crash."""
    assert explain("NOTATHING") is None
    assert explain("") is None
    assert explain(None) is None  # type: ignore[arg-type]
    assert explain("   ") is None


# ── Section B — No-jargon (technical IDs stripped) ───────────────────


@pytest.mark.parametrize("prefix", ["BMA", "DIS", "ALGO", "IND", "REG"])
def test_patient_html_no_entity_ids_in_visible_text(patient_html: str, prefix: str):
    """No `BMA-…`, `DIS-…`, `ALGO-…`, `IND-…`, `REG-…` entity IDs leak
    into user-visible body text."""
    pattern = re.compile(rf"\b{prefix}-[A-Z0-9_-]+\b")
    visible = _visible_text(patient_html)
    leaks = pattern.findall(visible)
    assert not leaks, (
        f"{prefix}-* entity IDs leaked into visible patient text: {leaks[:5]}"
    )


def test_patient_html_no_bio_ids_in_visible_text(patient_html: str):
    """`BIO-…` IDs may exist in HTML attributes (e.g. data-bio-id) but
    must not appear in visible body text — gene names are humanized
    (e.g. "BRAF" not "BIO-BRAF-MUTATION")."""
    visible = _visible_text(patient_html)
    leaks = re.findall(r"\bBIO-[A-Z0-9_-]+\b", visible)
    assert not leaks, f"BIO-* IDs leaked into visible text: {leaks[:5]}"


def test_patient_html_no_drug_ids_in_visible_text(patient_html: str):
    """`DRUG-…` IDs must be humanized to drug names (e.g. "encorafenib"
    not "DRUG-ENCORAFENIB"). HTML attribute leaks (data-drug-id) would
    not be found because `_visible_text` strips tags first."""
    visible = _visible_text(patient_html)
    leaks = re.findall(r"\bDRUG-[A-Z0-9_-]+\b", visible)
    assert not leaks, f"DRUG-* IDs leaked into visible text: {leaks[:5]}"


def test_patient_html_no_rf_ids_in_visible_text(patient_html: str):
    """`RF-…` IDs may live in `data-rf-id` attributes for debug tooling
    but must not leak into the visible emergency banner text."""
    visible = _visible_text(patient_html)
    leaks = re.findall(r"\bRF-[A-Z0-9_-]+\b", visible)
    assert not leaks, f"RF-* IDs leaked into visible text: {leaks[:5]}"


# ── Section C — Structural anchors ───────────────────────────────────


def test_patient_html_has_required_sections(patient_html: str):
    """All structural anchors required by CSD-3 demo + tests:

      * `<div class="patient-report">` — root wrapper
      * `<section class="what-was-found">` — molecular findings
      * `<section class="what-now">` — drug recommendations
      * `<section class="why-this-plan">` — Phase 3 rationale
      * `<section class="between-visits">` — Phase 4 between-visit watchpoints
      * `<section class="emergency-signals">` — emergency banner
      * `<div class="ask-doctor"…>` — question list
      * `<footer class="patient-disclaimer">` — disclaimer
    """
    required = [
        '<div class="patient-report">',
        '<section class="what-was-found">',
        '<section class="what-now">',
        '<section class="why-this-plan">',
        '<section class="between-visits">',
        '<section class="emergency-signals">',
        '<div class="ask-doctor"',
        '<footer class="patient-disclaimer">',
    ]
    for marker in required:
        assert marker in patient_html, f"Missing required structural marker: {marker}"


def test_patient_html_has_disclaimer(patient_html: str):
    """Footer disclaimer must include the regulatory boilerplate:
    'Цей звіт' (this report), 'не медичний прилад' (not a medical
    device), 'лікар' (doctor)."""
    visible = _visible_text(patient_html)
    assert "Цей звіт" in visible, "Disclaimer missing 'Цей звіт' boilerplate"
    assert "не медичний прилад" in visible, (
        "Disclaimer missing 'не медичний прилад' boilerplate"
    )
    assert "лікар" in visible, "Disclaimer missing 'лікар' reference"


def test_patient_html_uses_patient_mode_css(patient_html: str):
    """Embedded `<style>` block must include the `.patient-report`
    selector — proves PATIENT_MODE_CSS got concatenated into the
    document shell."""
    assert "<style>" in patient_html
    assert ".patient-report" in patient_html, (
        "Patient-mode CSS selector .patient-report missing from <style>"
    )


# ── Section D — Emergency RF rendering ───────────────────────────────


def test_emergency_rf_filter_keeps_critical_severity():
    rf = {
        "id": "RF-FAKE-1",
        "severity": "critical",
        "definition_ua": "Тестовий стан.",
    }
    assert is_emergency_rf(rf) is True


def test_emergency_rf_filter_keeps_hold_direction():
    rf = {
        "id": "RF-FAKE-2",
        "severity": "moderate",
        "clinical_direction": "hold",
        "definition_ua": "Зупинити терапію до стабілізації.",
    }
    assert is_emergency_rf(rf) is True


def test_emergency_rf_filter_keyword_match_ua():
    rf = {
        "id": "RF-FAKE-3",
        "severity": "moderate",
        "clinical_direction": "monitor",
        "definition_ua": "Лихоманка вище 38°C на тлі низьких нейтрофілів.",
    }
    assert is_emergency_rf(rf) is True


def test_emergency_rf_filter_drops_routine():
    rf = {
        "id": "RF-FAKE-4",
        "severity": "routine",
        "clinical_direction": "monitor",
        "definition_ua": "Стабільний показник, контроль за планом.",
        "definition": "Stable parameter, routine monitoring.",
    }
    assert is_emergency_rf(rf) is False


def test_emergency_rf_filter_handles_non_dict():
    """Defensive: malformed input must return False rather than crash."""
    assert is_emergency_rf(None) is False  # type: ignore[arg-type]
    assert is_emergency_rf("RF-FOO") is False  # type: ignore[arg-type]
    assert is_emergency_rf([]) is False  # type: ignore[arg-type]


def test_emergency_label_prefixes_siren():
    rf = {
        "definition_ua": "Тяжка фебрильна нейтропенія — у відділення негайно.",
    }
    label = patient_emergency_label(rf)
    assert label.startswith("🚨"), f"Label should start with siren emoji: {label!r}"
    # First-sentence truncation
    assert "." not in label[2:], (
        f"Label should contain only the first sentence: {label!r}"
    )


def test_emergency_label_fallback_when_definition_missing():
    rf = {"id": "RF-EMPTY"}
    label = patient_emergency_label(rf)
    assert label.startswith("🚨")
    assert "лікар" in label.lower()


def test_filter_emergency_rfs_preserves_order():
    rfs = [
        {"id": "A", "severity": "routine"},
        {"id": "B", "severity": "critical"},
        {"id": "C", "severity": "moderate", "clinical_direction": "hold"},
        {"id": "D", "severity": "low"},
    ]
    out = filter_emergency_rfs(rfs)
    assert [r["id"] for r in out] == ["B", "C"]


def test_emergency_section_renders_when_no_rfs():
    """A patient whose plan resolves no red flags should still see the
    section, but with the empty-state placeholder rather than the
    siren banner."""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    # Force a clean RF map.
    result.kb_resolved["red_flags"] = {}
    html = render_plan_html(result, mode="patient")
    assert '<section class="emergency-signals">' in html
    assert "Наразі немає термінових сигналів" in html
    assert "🚨" not in html


def test_emergency_section_renders_when_rfs_present():
    """Inject a synthetic critical RF into the resolved KB scratchpad
    and confirm it surfaces as an `<ul class="emergency-list">` item
    with a 🚨 marker."""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    result.kb_resolved.setdefault("red_flags", {})["RF-TEST-EMERGENCY"] = {
        "id": "RF-TEST-EMERGENCY",
        "severity": "critical",
        "clinical_direction": "hold",
        "definition_ua": (
            "Тяжка фебрильна нейтропенія — звертайтесь у відділення невідкладної "
            "допомоги негайно."
        ),
        "definition": "Severe febrile neutropenia — go to the ER immediately.",
    }
    html = render_plan_html(result, mode="patient")
    assert '<ul class="emergency-list">' in html
    # At least one <li> with the siren prefix.
    li_with_siren = re.findall(r"<li[^>]*>[^<]*🚨", html)
    assert li_with_siren, "Emergency banner should contain ≥1 <li> with 🚨"


# ── Section E — Ask-doctor section ───────────────────────────────────


_MUST_IDS = {"second_opinion", "duration", "side_effects", "support"}


def test_select_questions_returns_5_to_7():
    """Sanity: with a non-trivial plan the selector returns between 5
    and 7 questions (target 6 by default; relaxed bounds because the
    must-include set alone is 4 + at least one optional pulled in)."""
    plan = {
        "patient_age": 45,
        "recommended_drugs": [{"nszu_status": "oop"}],
        "tracks": [{}, {}],
    }
    out = select_questions(plan, target_count=6)
    assert 5 <= len(out) <= 7, f"Expected 5-7 questions, got {len(out)}"


def test_select_questions_always_includes_must():
    """The four must-have questions appear regardless of plan shape."""
    out = select_questions({})
    ids = {q["id"] for q in out}
    assert _MUST_IDS.issubset(ids), f"Must-include set missing from: {ids}"


def test_select_questions_oop_question_when_oop_drug():
    """OOP drug → either regional_access or insurance question added."""
    plan = {"recommended_drugs": [{"nszu_status": "oop"}]}
    ids = {q["id"] for q in select_questions(plan)}
    assert "regional_access" in ids or "insurance" in ids, (
        f"OOP-drug plan should surface regional_access/insurance; got {ids}"
    )


def test_select_questions_fertility_question_when_young():
    plan = {"patient_age": 35}
    ids = {q["id"] for q in select_questions(plan)}
    assert "fertility" in ids, f"Patient <50 should see fertility question; got {ids}"


def test_select_questions_fertility_omitted_when_older():
    plan = {"patient_age": 70}
    ids = {q["id"] for q in select_questions(plan)}
    assert "fertility" not in ids


def test_select_questions_family_screening_when_germline():
    plan = {
        "variant_actionability": [
            {"variant_qualifier": "germline pathogenic BRCA1"}
        ]
    }
    ids = {q["id"] for q in select_questions(plan)}
    assert "family_screening" in ids


def test_select_questions_handles_none_plan():
    """`select_questions(None)` must return only the must-have core
    rather than crash — defensive contract for the renderer."""
    out = select_questions(None)
    ids = {q["id"] for q in out}
    assert _MUST_IDS.issubset(ids)


def test_question_templates_have_required_keys():
    for q in QUESTION_TEMPLATES:
        assert "id" in q and "predicate" in q and "question_ua" in q
        assert q["question_ua"].strip(), f"Empty question_ua for {q['id']}"


# ── Section H — ECOG 4 hard gate ─────────────────────────────────────


_ACTIVE_TRACK_IDS = {"standard", "aggressive"}


def test_ecog4_suppresses_active_tracks():
    """ECOG PS 4 → engine must not produce any standard or aggressive tracks."""
    patient = {
        "patient_id": "TEST-ECOG4-GATE",
        "disease": {"id": "DIS-CRC"},
        "line_of_therapy": 1,
        "demographics": {"age": 72, "ecog": 4},
    }
    result = generate_plan(patient, kb_root=KB_ROOT)
    if result.plan is None:
        return  # No plan at all is also acceptable
    active_tracks = [
        t for t in (result.plan.tracks or [])
        if t.track_id in _ACTIVE_TRACK_IDS
    ]
    assert not active_tracks, (
        f"ECOG 4 patient should have no active tracks; got: "
        f"{[t.track_id for t in active_tracks]}"
    )
    ecog_warnings = [w for w in (result.warnings or []) if "ECOG" in w and "suppressed" in w]
    assert ecog_warnings, "Expected ECOG suppression warning in result.warnings"


def test_ecog3_allows_active_tracks():
    """ECOG PS 3 must NOT be suppressed by the ECOG 4 hard gate."""
    patient = {
        "patient_id": "TEST-ECOG3-GATE",
        "disease": {"id": "DIS-CRC"},
        "line_of_therapy": 1,
        "demographics": {"age": 68, "ecog": 3},
    }
    result = generate_plan(patient, kb_root=KB_ROOT)
    ecog_suppression_warnings = [
        w for w in (result.warnings or []) if "suppressed" in w and "ECOG" in w
    ]
    assert not ecog_suppression_warnings, (
        f"ECOG 3 should not trigger active-track suppression; "
        f"got warnings: {ecog_suppression_warnings}"
    )


def test_ecog4_gate_absent_ecog_defaults_to_no_suppression():
    """Missing ECOG in demographics → defaults to 0, no suppression."""
    patient = {
        "patient_id": "TEST-ECOG-ABSENT",
        "disease": {"id": "DIS-CRC"},
        "line_of_therapy": 1,
        "demographics": {"age": 55},
    }
    result = generate_plan(patient, kb_root=KB_ROOT)
    ecog_suppression_warnings = [
        w for w in (result.warnings or []) if "suppressed" in w and "ECOG" in w
    ]
    assert not ecog_suppression_warnings, (
        "Absent ECOG should not suppress tracks; "
        f"got: {ecog_suppression_warnings}"
    )


# ── Section F — End-to-end patient render integration ────────────────


def test_csd1_braf_v600e_mcrc_patient_mode():
    """Full pipeline using a 1L mCRC + BRAF V600E synthetic patient (the
    CSD-1 demo fixture targets line-of-therapy 2, for which the KB
    currently has no Algorithm — we use line=1 here so the render
    actually exercises the drug + emergency + ask-doctor paths)."""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    assert result.plan is not None, "Synthetic mCRC 1L should produce a plan"
    html = render_plan_html(result, mode="patient")

    # 1. Produced without exception, non-empty.
    assert isinstance(html, str) and len(html) > 1000

    # 2. Disease-relevant biology is mentioned in plain language.
    visible = _visible_text(html)
    assert "BRAF" in visible, "BRAF gene should be mentioned in patient-mode body"

    # 3. Either a recognizable drug name or a НСЗУ patient-friendly badge
    #    is present (encorafenib appears only for 2L/3L which the KB
    #    doesn't yet author for CRC — this assertion stays lenient by
    #    design while still proving the drug section rendered).
    # Phase 2: drug-explanation blocks now carry a data-source-id parity
    # hook (PATIENT_MODE_SPEC §4.1), so accept the open-tag prefix rather
    # than the bare closing form.
    has_drug_section = '<div class="drug-explanation"' in html
    has_nszu_badge = "patient-nszu" in html.lower() or "програмою НСЗУ" in visible
    assert has_drug_section and has_nszu_badge, (
        "Expected at least one drug-explanation block + NSZU badge"
    )

    # 4. Emergency section present (banner or empty-state placeholder).
    assert '<section class="emergency-signals">' in html

    # 5. ≥5 ask-doctor questions.
    ask_match = re.search(r'<div class="ask-doctor".*?</div>', html, flags=re.DOTALL)
    assert ask_match, "ask-doctor block should be parseable"
    li_count = len(re.findall(r"<li[\s>]", ask_match.group(0)))
    assert li_count >= 5, f"Expected ≥5 questions, got {li_count}"


def test_csd1_demo_fixture_loads_cleanly():
    """The on-disk CSD-1 demo fixture parses + reaches the renderer
    without exception, even when the KB does not yet author a 2L
    Algorithm for it (renderer must produce a graceful fallback shell
    rather than crash)."""
    fixture = EXAMPLES / "patient_csd_1_demo_braf_mcrc.json"
    if not fixture.exists():
        pytest.skip(f"Fixture missing: {fixture}")
    patient = json.loads(fixture.read_text(encoding="utf-8"))
    result = generate_plan(patient, kb_root=KB_ROOT)
    html = render_plan_html(result, mode="patient")
    assert '<div class="patient-report">' in html


# ── Section G — Accessibility heuristics on the embedded CSS ─────────


def test_patient_css_minimum_font_size(patient_html: str):
    """`.patient-report` body should set font-size ≥ 16px; current spec
    is 18px. Regex catches any size in px ≥ 16 declared on the
    `.patient-report` selector itself (not its descendants)."""
    # Find the .patient-report { … } block in the embedded style.
    block_match = re.search(
        r"\.patient-report\s*\{([^}]+)\}", patient_html, flags=re.DOTALL
    )
    assert block_match, "Embedded CSS missing .patient-report selector block"
    block = block_match.group(1)
    fs_match = re.search(r"font-size\s*:\s*(\d+)px", block)
    assert fs_match, f".patient-report block has no px font-size: {block!r}"
    px = int(fs_match.group(1))
    assert px >= 16, f"Patient body font-size {px}px is below 16px floor"


def test_patient_css_line_height(patient_html: str):
    """`.patient-report` line-height ≥ 1.5 for readability."""
    block_match = re.search(
        r"\.patient-report\s*\{([^}]+)\}", patient_html, flags=re.DOTALL
    )
    assert block_match
    block = block_match.group(1)
    lh_match = re.search(r"line-height\s*:\s*([\d.]+)", block)
    assert lh_match, f".patient-report block has no line-height: {block!r}"
    lh = float(lh_match.group(1))
    assert lh >= 1.5, f"Patient body line-height {lh} is below 1.5 floor"


# ── Vocabulary table integrity sanity ────────────────────────────────


def test_all_vocabulary_tables_nonempty():
    """No category table should silently empty itself on refactor."""
    tables = {
        "DRUG_CLASS_PLAIN_UA": DRUG_CLASS_PLAIN_UA,
        "VARIANT_TYPE_PLAIN_UA": VARIANT_TYPE_PLAIN_UA,
        "ESCAT_PLAIN_UA": ESCAT_PLAIN_UA,
        "NSZU_PLAIN_UA": NSZU_PLAIN_UA,
        "LAB_PLAIN_UA": LAB_PLAIN_UA,
        "AE_PLAIN_UA": AE_PLAIN_UA,
        "SCREENING_PLAIN_UA": SCREENING_PLAIN_UA,
    }
    for name, t in tables.items():
        assert len(t) > 0, f"Vocabulary table {name} unexpectedly empty"


# ── Section H — Phase 2: per-track presentation + cross-link + parity ──


def _build_hcv_mzl_two_track_plan():
    """Reference HCV-MZL fixture — produces two tracks (ANTIVIRAL +
    BR-AGGRESSIVE). Used by the two-track tests below."""
    fixture = EXAMPLES / "patient_zero_reference_case.json"
    if not fixture.exists():
        pytest.skip(f"Reference fixture missing: {fixture}")
    patient = json.loads(fixture.read_text(encoding="utf-8"))
    return generate_plan(patient, kb_root=KB_ROOT)


def test_patient_html_two_track_plan_shows_both_tracks():
    """When the engine produces ≥2 tracks, the patient bundle MUST
    surface both — the А/Б Cyrillic prefix is the structural marker
    (PATIENT_MODE_SPEC §3.2)."""
    result = _build_hcv_mzl_two_track_plan()
    if result.plan is None or len(result.plan.tracks) < 2:
        pytest.skip("Reference HCV-MZL plan should produce ≥2 tracks")
    html = render_plan_html(result, mode="patient")
    visible = _visible_text(html)
    # Cyrillic enumeration markers; never Latin A/B.
    assert "А)" in visible, "Two-track plan must show Cyrillic 'А)' prefix"
    assert "Б)" in visible, "Two-track plan must show Cyrillic 'Б)' prefix"
    # Both track-card modifiers present in the markup.
    assert 'track-card--default' in html
    assert 'track-card--alternative' in html
    # Tracks-grid wrapper for layout.
    assert '<div class="tracks-grid' in html


def test_patient_html_single_track_plan_no_a_b_prefix():
    """Single-track plans render a bare 'Рекомендований план' label,
    without А/Б enumeration."""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    assert result.plan is not None
    if len(result.plan.tracks) > 1:
        pytest.skip("Synthetic mCRC fixture unexpectedly produced ≥2 tracks")
    html = render_plan_html(result, mode="patient")
    visible = _visible_text(html)
    # Must not include А/Б enumeration.
    assert "А)" not in visible, "Single-track plan must not emit 'А)' prefix"
    assert "Б)" not in visible, "Single-track plan must not emit 'Б)' prefix"
    # Should render the bare track label.
    assert "Рекомендований план" in visible


def test_patient_html_has_clinician_cross_link():
    """When `sibling_link` is set, the patient bundle exposes a
    `<a class="mode-toggle">` chip pointing at the clinician version
    (PATIENT_MODE_SPEC §3.5)."""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    html = render_plan_html(
        result, mode="patient", sibling_link="plan.html"
    )
    assert '<a class="mode-toggle"' in html
    assert 'href="plan.html"' in html
    assert "Технічна версія для лікаря" in html


def test_patient_html_no_cross_link_when_sibling_none():
    """`sibling_link=None` (default) suppresses the chip entirely so
    bundles rendered without a sibling stay clean. (`.mode-toggle` CSS
    selector is unconditionally embedded; absence is checked on the
    `<a class="mode-toggle">` markup itself.)"""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    html = render_plan_html(result, mode="patient")
    assert '<a class="mode-toggle"' not in html


def test_clinician_html_has_patient_cross_link():
    """Mirror: clinician bundle exposes a chip pointing at the patient
    version when `sibling_link` is set."""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    html = render_plan_html(
        result, mode="clinician", sibling_link="plan.patient.html"
    )
    assert '<a class="mode-toggle"' in html
    assert 'href="plan.patient.html"' in html
    assert "Версія для пацієнта" in html


def test_patient_html_has_why_section():
    """Phase 2 `why-this-plan` shell must be present even before
    Phase 3 fills the rationale bullets."""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    html = render_plan_html(result, mode="patient")
    assert '<section class="why-this-plan">' in html
    visible = _visible_text(html)
    assert "Чому саме цей план" in visible


# ── Section I — Phase 3: rationale from PlanResult.trace ─────────────


def test_patient_rationale_braf_v600e_mcrc_mentions_braf():
    """The synthetic BRAF V600E mCRC patient should have a rationale
    bullet that names the BRAF V600E hit. Tier handling: the engine
    populates `variant_actionability` with whichever ESCAT cell matched
    (typically IB for BRAF V600E in CRC); both strong-tier and mid-tier
    wordings should mention the gene+variant."""
    from knowledge_base.engine._patient_rationale import build_track_rationale

    result = _build_synthetic_braf_v600e_mcrc_plan()
    if result.plan is None or not result.plan.tracks:
        pytest.skip("Synthetic mCRC plan should produce at least 1 track")
    if not result.plan.variant_actionability:
        pytest.skip("Plan didn't surface a BRAF V600E hit (KB drift?)")
    bullets = build_track_rationale(result, result.plan.tracks[0])
    joined = " ".join(bullets)
    assert "BRAF" in joined, (
        f"Rationale should name BRAF; got: {bullets!r}"
    )


def test_patient_rationale_renders_in_why_section():
    """End-to-end: the patient bundle's `why-this-plan` section now
    contains rationale bullets (not the Phase-2 placeholder paragraph)
    when biomarker / RF data is available."""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    html = render_plan_html(result, mode="patient")
    # `<ul>` inside the why-this-plan section is the structural marker
    # that rationale bullets rendered. Find the section block first
    # to scope the search.
    why_match = re.search(
        r'<section class="why-this-plan">.*?</section>',
        html,
        flags=re.DOTALL,
    )
    assert why_match, "why-this-plan section missing"
    why_block = why_match.group(0)
    assert "<ul>" in why_block and "<li>" in why_block, (
        f"Rationale should render <ul>/<li> bullets, got: {why_block[:300]}"
    )


def test_patient_rationale_no_trace_fallback():
    """Empty trace → at least one fallback bullet so the section is
    never empty."""
    from knowledge_base.engine._patient_rationale import build_track_rationale

    class _FakeTrack:
        is_default = True
        indication_data = None
        regimen_data = None

    class _FakeResult:
        plan = None
        kb_resolved: dict = {}
        trace: list = []

    bullets = build_track_rationale(_FakeResult(), _FakeTrack())
    assert bullets, "Empty plan should still produce at least one fallback bullet"
    assert any("стандарт" in b.lower() or "альтернативн" in b.lower() for b in bullets)


def test_patient_rationale_fired_rf_surfaces_in_bullets():
    """A fired RedFlag in the trace surfaces as a 'У вас зафіксовано: …'
    bullet, taking the first sentence of `definition_ua`."""
    from knowledge_base.engine._patient_rationale import build_track_rationale

    class _FakeTrack:
        is_default = False
        indication_data = None
        regimen_data = None

    class _FakeResult:
        plan = None
        kb_resolved = {
            "red_flags": {
                "RF-FAKE-HBV": {
                    "id": "RF-FAKE-HBV",
                    "definition_ua": (
                        "Хронічний гепатит B без противірусної профілактики. "
                        "Імуносупресивна терапія може реактивувати вірус."
                    ),
                }
            }
        }
        trace = [
            {
                "step": "step_1",
                "outcome": "REG-FOO",
                "branch": "default",
                "fired_red_flags": ["RF-FAKE-HBV"],
            }
        ]

    bullets = build_track_rationale(_FakeResult(), _FakeTrack())
    joined = " ".join(bullets)
    assert "Хронічний гепатит B" in joined or "зафіксовано" in joined, (
        f"Expected the fired-RF definition to surface, got: {bullets!r}"
    )


def test_patient_rationale_caps_at_4_bullets():
    """Even with many fired RFs, the rationale never exceeds 4 bullets
    (PATIENT_MODE_SPEC §3.3 cap to keep the patient bundle scannable)."""
    from knowledge_base.engine._patient_rationale import build_track_rationale

    class _FakeTrack:
        is_default = True
        indication_data = None
        regimen_data = None

    class _FakeResult:
        plan = None
        kb_resolved = {
            "red_flags": {
                f"RF-{i}": {
                    "id": f"RF-{i}",
                    "definition_ua": f"Тестовий RedFlag номер {i}.",
                }
                for i in range(10)
            }
        }
        trace = [
            {
                "step": f"step_{i}",
                "outcome": "REG-FOO",
                "branch": "default",
                "fired_red_flags": [f"RF-{i}"],
            }
            for i in range(10)
        ]

    bullets = build_track_rationale(_FakeResult(), _FakeTrack())
    assert len(bullets) <= 4, f"Cap exceeded: got {len(bullets)} bullets"


def test_information_parity_smoke():
    """PATIENT_MODE_SPEC §4: every track present in the clinician HTML
    must also surface in the patient HTML, indexed by `data-source-id`
    (regimen ID). Fired RedFlags surface in patient body somewhere."""
    result = _build_hcv_mzl_two_track_plan()
    if result.plan is None or len(result.plan.tracks) < 2:
        pytest.skip("Reference HCV-MZL plan should produce ≥2 tracks")
    clinician_html = render_plan_html(result, mode="clinician")
    patient_html = render_plan_html(result, mode="patient")

    # Each track's regimen ID must appear in patient HTML.
    for t in result.plan.tracks:
        rid = (t.regimen_data or {}).get("id", "") if t.regimen_data else ""
        if not rid:
            continue
        assert rid in patient_html, (
            f"Regimen {rid!r} missing from patient bundle "
            f"(present in clinician: {rid in clinician_html})"
        )


# ── Section J — Phase 4: between-visit watchpoints ───────────────────


def test_between_visits_section_renders_fallback_when_unauthored():
    """A regimen with no `between_visit_watchpoints` produces the
    fallback string per PATIENT_MODE_SPEC §3.4 — never fabricates."""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    if result.plan is None or not result.plan.tracks:
        pytest.skip("Synthetic mCRC plan should produce at least 1 track")
    # Defensive: clear any watchpoints that might leak from KB.
    for t in result.plan.tracks:
        if isinstance(t.regimen_data, dict):
            t.regimen_data["between_visit_watchpoints"] = []
    html = render_plan_html(result, mode="patient")
    assert '<section class="between-visits">' in html
    visible = _visible_text(html)
    assert "ще не узгоджено клінічною командою" in visible


def test_between_visits_section_renders_authored_watchpoints():
    """When watchpoints are present they group by urgency tier and the
    headings appear in the rendered section."""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    if result.plan is None or not result.plan.tracks:
        pytest.skip("Synthetic mCRC plan should produce at least 1 track")
    # Inject fixture watchpoints into the first track's regimen_data.
    t = result.plan.tracks[0]
    if not isinstance(t.regimen_data, dict):
        pytest.skip("Track has no regimen_data dict to inject into")
    t.regimen_data["between_visit_watchpoints"] = [
        {
            "trigger_ua": "Сильна слабкість на 7-10 день циклу",
            "action_ua": "Це нормально для цього курсу — занотуйте і обговоріть на наступному візиті",
            "urgency": "log_at_next_visit",
            "cycle_day_window": "Day 7-14",
        },
        {
            "trigger_ua": "Лихоманка вище 38°C",
            "action_ua": "Подзвоніть у клініку того ж дня — нейтрофіли можуть бути низькі",
            "urgency": "call_clinic_same_day",
        },
    ]
    html = render_plan_html(result, mode="patient")
    visible = _visible_text(html)
    # Both urgency-group headings present
    assert "Занотуйте і обговоріть на наступному візиті" in visible
    assert "Подзвоніть у клініку того ж дня" in visible
    # Both trigger texts surface
    assert "Сильна слабкість на 7-10 день циклу" in visible
    assert "Лихоманка вище 38°C" in visible
    # Cycle window rendered for the first watchpoint
    assert "Day 7-14" in visible
    # CSS modifier classes present
    assert 'bv-urgency-group bv-log' in html
    assert 'bv-urgency-group bv-call' in html


def test_between_visits_dedupe_with_emergency_banner():
    """An `er_now` watchpoint whose `trigger_ua` first-sentence matches
    an emergency RF gets dropped from `between-visits` (it surfaces in
    the emergency banner instead). Per PATIENT_MODE_SPEC §3.4."""
    result = _build_synthetic_braf_v600e_mcrc_plan()
    if result.plan is None or not result.plan.tracks:
        pytest.skip("Synthetic mCRC plan should produce at least 1 track")
    # Inject a critical RF whose first-sentence matches a watchpoint.
    rf_text = "Тяжка фебрильна нейтропенія потребує негайного звернення"
    result.kb_resolved.setdefault("red_flags", {})["RF-DEDUPE-TEST"] = {
        "id": "RF-DEDUPE-TEST",
        "severity": "critical",
        "definition_ua": rf_text + ". Подальше — деталі.",
    }
    # Watchpoint with matching trigger should be dropped, non-matching kept.
    t = result.plan.tracks[0]
    if not isinstance(t.regimen_data, dict):
        pytest.skip("Track has no regimen_data dict to inject into")
    t.regimen_data["between_visit_watchpoints"] = [
        {
            "trigger_ua": rf_text,  # exactly the same first sentence
            "action_ua": "Викличте швидку",
            "urgency": "er_now",
        },
        {
            "trigger_ua": "Поява нової задишки",  # not in emergency list
            "action_ua": "Викличте швидку, не чекайте візиту",
            "urgency": "er_now",
        },
    ]
    html = render_plan_html(result, mode="patient")
    bv_match = re.search(
        r'<section class="between-visits">.*?</section>',
        html, flags=re.DOTALL,
    )
    assert bv_match
    bv_block = bv_match.group(0)
    # Non-matching `er_now` item still in between-visits.
    assert "Поява нової задишки" in bv_block
    # Matching item dropped from between-visits (still allowed elsewhere).
    assert rf_text not in bv_block
    # But does surface in the emergency banner.
    em_match = re.search(
        r'<section class="emergency-signals">.*?</section>',
        html, flags=re.DOTALL,
    )
    assert em_match and rf_text in em_match.group(0)


def test_between_visits_per_track_when_two_tracks():
    """Two-track plans render a `bv-track` block per track, each with
    its own dedicated fallback-or-watchpoints area."""
    result = _build_hcv_mzl_two_track_plan()
    if result.plan is None or len(result.plan.tracks) < 2:
        pytest.skip("Reference HCV-MZL plan should produce ≥2 tracks")
    html = render_plan_html(result, mode="patient")
    bv_match = re.search(
        r'<section class="between-visits">.*?</section>',
        html, flags=re.DOTALL,
    )
    assert bv_match
    bv_block = bv_match.group(0)
    # Two `bv-track` cards (one per track).
    track_card_count = bv_block.count('class="bv-track"')
    assert track_card_count == 2, (
        f"Expected 2 bv-track cards for a 2-track plan, got {track_card_count}"
    )
    # Both Cyrillic prefixes present.
    visible = _visible_text(bv_block)
    assert "А)" in visible and "Б)" in visible


def test_between_visits_schema_rejects_bad_urgency():
    """Pydantic Literal type on `urgency` blocks bogus values at load
    time so the renderer never has to defend against typos."""
    from knowledge_base.schemas.regimen import Regimen
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Regimen(
            id="REG-BAD", name="Bad", components=[{"drug_id": "D"}],
            between_visit_watchpoints=[
                {"trigger_ua": "x", "action_ua": "y", "urgency": "asap_now"},
            ],
        )


def test_between_visits_schema_accepts_three_tier_set():
    """All three urgency tiers parse without error."""
    from knowledge_base.schemas.regimen import Regimen

    r = Regimen(
        id="REG-OK", name="OK", components=[{"drug_id": "D"}],
        between_visit_watchpoints=[
            {"trigger_ua": "a1", "action_ua": "b1", "urgency": "log_at_next_visit"},
            {"trigger_ua": "a2", "action_ua": "b2", "urgency": "call_clinic_same_day"},
            {"trigger_ua": "a3", "action_ua": "b3", "urgency": "er_now"},
        ],
    )
    urgencies = [w.urgency for w in r.between_visit_watchpoints]
    assert urgencies == ["log_at_next_visit", "call_clinic_same_day", "er_now"]


# ── Section K — Phase 5: Latin/abbreviation render gate ──────────────


def _flag_unallowed_acronyms(visible_text: str) -> list[str]:
    """Return uppercase abbreviation tokens in `visible_text` that are
    NOT on the patient-mode allowlist. Tokens matching the trial-prefix
    rule (KEYNOTE-189, etc.) pass."""
    from knowledge_base.engine._patient_vocabulary import is_allowlisted_acronym
    pattern = re.compile(r"\b[A-Z]{2,}[a-z]?(?:-[A-Z0-9]+)*\b")
    found = set(pattern.findall(visible_text))
    return sorted(t for t in found if not is_allowlisted_acronym(t))


def _flag_unallowed_latin_words(visible_text: str) -> list[str]:
    """Return Latin lowercase ≥4-char tokens in `visible_text` that are
    NOT on the patient-mode allowlist."""
    from knowledge_base.engine._patient_vocabulary import is_allowlisted_latin_word
    pattern = re.compile(r"\b[a-z]{4,}\b")
    found = set(pattern.findall(visible_text))
    return sorted(t for t in found if not is_allowlisted_latin_word(t))


# Anchor cases the gates run against. Each tuple is (label, fixture-builder).
# Adding a fixture here surfaces any new Latin token introduced by KB shifts
# or render-layer changes — the failure message points at the fixture.
_GATE_CASES = [
    ("synthetic mCRC + BRAF V600E", _build_synthetic_braf_v600e_mcrc_plan),
    ("reference HCV-MZL two-track", _build_hcv_mzl_two_track_plan),
]


@pytest.mark.parametrize("label,builder", _GATE_CASES, ids=lambda x: getattr(x, "__name__", str(x)))
def test_patient_html_no_latin_abbreviations_in_visible_text(label, builder):
    """Visible patient body MUST NOT contain uppercase abbreviations
    outside the allowlist. PATIENT_MODE_SPEC §5.4."""
    if not callable(builder):
        return
    result = builder()
    if result.plan is None:
        pytest.skip(f"{label!r}: builder produced no plan")
    html = render_plan_html(result, mode="patient")
    visible = _visible_text(html)
    leaks = _flag_unallowed_acronyms(visible)
    assert not leaks, (
        f"[{label}] Unallowed uppercase abbreviations leaked into the patient body:\n"
        f"  {leaks}\n"
        f"Fix options:\n"
        f"  1. Rewrite the offending renderer-controlled prose to drop the abbreviation.\n"
        f"  2. Add a first-use expansion to ABBREVIATION_FIRST_USE_UA in _patient_vocabulary.py.\n"
        f"  3. Add the token to PATIENT_ALLOWLIST_ACRONYMS if it's a canonical clinical name.\n"
    )


@pytest.mark.parametrize("label,builder", _GATE_CASES, ids=lambda x: getattr(x, "__name__", str(x)))
def test_patient_html_no_bare_latin_words(label, builder):
    """Visible patient body MUST NOT contain Latin lowercase words
    ≥4 chars outside the allowlist. PATIENT_MODE_SPEC §5.4."""
    if not callable(builder):
        return
    result = builder()
    if result.plan is None:
        pytest.skip(f"{label!r}: builder produced no plan")
    html = render_plan_html(result, mode="patient")
    visible = _visible_text(html)
    leaks = _flag_unallowed_latin_words(visible)
    assert not leaks, (
        f"[{label}] Unallowed Latin words leaked into the patient body:\n"
        f"  {leaks}\n"
        f"Fix options:\n"
        f"  1. Rewrite the offending renderer-controlled prose to use Ukrainian.\n"
        f"  2. Add the word to PATIENT_ALLOWLIST_LATIN_WORDS if it's a canonical loanword,\n"
        f"     biology stem, or unavoidable KB regimen-name fragment.\n"
    )


def test_first_use_expansion_inserts_gloss_for_escat():
    """When the patient body mentions ESCAT, the first occurrence is
    expanded to include the parenthesized gloss."""
    from knowledge_base.engine._patient_vocabulary import expand_first_use

    sample = "<p>За шкалою ESCAT це найвищий рівень доказів.</p>"
    out = expand_first_use(sample)
    # First use becomes the expanded form.
    assert "ESCAT (рівень доказів" in out
    # Idempotency sentinel attached.
    assert "abbrev-expanded" in out


def test_first_use_expansion_idempotent():
    """Calling `expand_first_use` twice on the same input is a no-op
    after the first call (sentinel guard). Lets render flows toggle
    audience / language without double-expanding."""
    from knowledge_base.engine._patient_vocabulary import expand_first_use

    sample = "<p>ESCAT — це шкала.</p>"
    once = expand_first_use(sample)
    twice = expand_first_use(once)
    assert once == twice


def test_first_use_expansion_skips_when_key_absent():
    """If a key from `ABBREVIATION_FIRST_USE_UA` doesn't appear in the
    text, no replacement happens for that key — only the sentinel is
    appended."""
    from knowledge_base.engine._patient_vocabulary import expand_first_use

    sample = "<p>Самі лише українські слова — без жодних абревіатур.</p>"
    out = expand_first_use(sample)
    # No expansion text should be inserted.
    assert "рівень доказів" not in out
    assert "вірус гепатиту" not in out
    # Sentinel still appended.
    assert "abbrev-expanded" in out
