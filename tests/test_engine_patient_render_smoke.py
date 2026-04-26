"""Smoke test for patient-mode HTML rendering wired into render_plan_html.

Validates that `render_plan_html(plan_result, mode="patient")` produces a
single-file HTML bundle with the structural contract that downstream
CSD-3-tests + CSD-3-demo rely on:

  * Top-level `<div class="patient-report">` wrapper.
  * No technical entity IDs (BMA-*, ALGO-*, BIO-*, IND-*, REG-*, RF-*)
    appear in user-visible text. (They MAY appear inside HTML attributes
    such as `data-rf-id="..."` for debugging hooks.)
  * Emergency-signals section present (banner with `🚨` items when
    emergency RFs match, or the empty-state placeholder otherwise).
  * Ask-doctor section present with at least 5 questions.
  * Validator stays ok=True (patient-mode rendering is render-only and
    must not regress KB integrity).
"""

from __future__ import annotations

import re
from pathlib import Path

from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.validation.loader import load_content


REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"

# Strip text inside `<...>` opening/closing tag brackets so we only check
# user-visible body text for technical IDs. Technical IDs inside HTML
# attributes (e.g. `data-rf-id="RF-FOO"`) are allowed — they're a debug
# hook for tests.
_TAG_PATTERN = re.compile(r"<[^>]*>")
_ID_PREFIX_PATTERN = re.compile(r"\b(BMA|ALGO|BIO|IND|REG|RF)-[A-Z0-9_-]+\b")


def _visible_text(html: str) -> str:
    """Strip HTML tags + script/style blocks, leaving the visible body
    text that a patient would actually read."""
    # Drop entire <style>...</style> + <script>...</script> blocks first.
    no_style = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    no_script = re.sub(r"<script[^>]*>.*?</script>", "", no_style, flags=re.DOTALL)
    return _TAG_PATTERN.sub(" ", no_script)


def test_patient_mode_smoke_braf_v600e_mcrc():
    """Synthetic mCRC + BRAF V600E patient → patient-mode HTML satisfies
    the structural contract above."""
    patient = {
        "patient_id": "TEST-PATIENT-MODE-001",
        "disease": {"id": "DIS-CRC"},
        "line_of_therapy": 1,
        "biomarkers": {"BRAF": "V600E"},
        "demographics": {"age": 58, "ecog": 1},
    }

    result = generate_plan(patient, kb_root=KB_ROOT)
    assert result.plan is not None, "Plan should be generated for mCRC 1L"

    html = render_plan_html(result, mode="patient")

    # Document wrapper
    assert '<div class="patient-report">' in html, (
        "Patient-mode HTML must wrap content in <div class='patient-report'>"
    )

    # No technical entity IDs in visible text
    visible = _visible_text(html)
    leaks = _ID_PREFIX_PATTERN.findall(visible)
    assert not leaks, f"Technical entity IDs leaked into visible patient-mode text: {leaks[:10]}"

    # Emergency signals section is always present (either banner or empty-state)
    assert "emergency-signals" in html or "Наразі немає" in html, (
        "Emergency signals section (or empty-state) must be present"
    )

    # Ask-doctor block + ≥5 questions
    assert '<div class="ask-doctor"' in html, (
        "Ask-doctor section must be rendered"
    )
    # Count <li> items inside the ask-doctor block specifically.
    ask_match = re.search(
        r'<div class="ask-doctor".*?</div>', html, flags=re.DOTALL
    )
    assert ask_match, "Ask-doctor block should be parseable"
    li_count = len(re.findall(r"<li[\s>]", ask_match.group(0)))
    assert li_count >= 5, f"Expected >=5 questions in ask-doctor, got {li_count}"

    # Validator should stay ok=True regardless of render-mode work
    load = load_content(KB_ROOT)
    err_count = (
        len(load.schema_errors) + len(load.ref_errors) + len(load.contract_errors)
    )
    assert load.ok, f"KB validator should remain ok=True; errors={err_count}"


def test_patient_mode_emergency_banner_when_critical_rf_present():
    """When the kb_resolved red_flags map contains a critical RF, the
    emergency banner should render with a 🚨 marker (not the empty
    placeholder)."""
    patient = {
        "patient_id": "TEST-PATIENT-MODE-EMER-001",
        "disease": {"id": "DIS-CRC"},
        "line_of_therapy": 1,
        "biomarkers": {"BRAF": "V600E"},
    }
    result = generate_plan(patient, kb_root=KB_ROOT)
    assert result.plan is not None

    # Synthesize a critical RF on the resolved KB snapshot — the patient
    # renderer reads result.kb_resolved['red_flags'], which is a render-
    # time scratchpad and not persisted on disk.
    result.kb_resolved.setdefault("red_flags", {})["RF-TEST-EMERGENCY"] = {
        "id": "RF-TEST-EMERGENCY",
        "severity": "critical",
        "clinical_direction": "hold",
        "definition_ua": "Тяжка фебрильна нейтропенія — звертайтесь у відділення невідкладної допомоги негайно",
        "definition": "Severe febrile neutropenia — go to the ER immediately",
    }

    html = render_plan_html(result, mode="patient")
    assert "🚨" in html, "Emergency banner must contain the 🚨 marker"
    # The visible text should carry the patient-friendly first sentence
    assert "фебрильна нейтропенія" in html.lower() or "звертайтесь" in html.lower()


def test_patient_mode_falls_back_when_plan_is_none():
    """Defensive: an empty PlanResult should still produce a valid
    patient-mode HTML shell, not crash."""
    from knowledge_base.engine.plan import PlanResult

    result = PlanResult(patient_id="TEST", disease_id=None, algorithm_id=None)
    html = render_plan_html(result, mode="patient")
    assert '<div class="patient-report">' in html
    assert "Ваш персональний" in html
