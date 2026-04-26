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
    ONCOKB_PLAIN_UA,
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
        # ONCOKB_PLAIN_UA
        "1", "R1",
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
      * `<section class="emergency-signals">` — emergency banner
      * `<div class="ask-doctor"…>` — question list
      * `<footer class="patient-disclaimer">` — disclaimer
    """
    required = [
        '<div class="patient-report">',
        '<section class="what-was-found">',
        '<section class="what-now">',
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
    has_drug_section = '<div class="drug-explanation">' in html
    has_nszu_badge = "патієнт-nszu" in html.lower() or "програмою НСЗУ" in visible
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
        "ONCOKB_PLAIN_UA": ONCOKB_PLAIN_UA,
        "NSZU_PLAIN_UA": NSZU_PLAIN_UA,
        "LAB_PLAIN_UA": LAB_PLAIN_UA,
        "AE_PLAIN_UA": AE_PLAIN_UA,
        "SCREENING_PLAIN_UA": SCREENING_PLAIN_UA,
    }
    for name, t in tables.items():
        assert len(t) > 0, f"Vocabulary table {name} unexpectedly empty"
