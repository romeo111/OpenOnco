"""Phase B test: live translation of long free-text in rendered Plan.

Verifies that when a translate client is configured AND target_lang
differs from source UA, the render layer routes long UA fields
(do_not_do, RedFlag definitions, MDT role reasons, open-question
question + rationale) through the translation client. Uses a stub
client to avoid network — the production stack (DeepL+LibreTranslate
fallback) is exercised separately in test_translate_client.py.

Also verifies graceful degrade: with NO client configured, render
still produces a usable document; UA text remains in place.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from knowledge_base.engine import generate_plan, orchestrate_mdt, render_plan_html
from knowledge_base.engine.render import _set_translate_client

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


class _StubTranslateClient:
    """In-memory translator that prefixes EN(...) for inspection.
    Records every call for later assertions."""

    name = "stub"

    def __init__(self):
        self.calls: list[tuple] = []

    def translate(self, text: str, target_lang: str, source_lang=None) -> str:
        self.calls.append((text, target_lang, source_lang))
        return f"EN({text[:60]})"


@pytest.fixture(autouse=True)
def _reset_client():
    """Each test starts with no client; teardown resets to env-driven."""
    _set_translate_client(None)
    yield
    _set_translate_client(None)


# ── Graceful degrade (no client configured) ──────────────────────────────


def test_render_uk_target_no_client_calls(monkeypatch):
    """target_lang='uk' = no translation needed; client never invoked
    even if available."""
    monkeypatch.delenv("DEEPL_API_KEY", raising=False)
    monkeypatch.delenv("LIBRETRANSLATE_URL", raising=False)
    stub = _StubTranslateClient()
    _set_translate_client(stub)

    p = _patient("patient_dlbcl_high_ipi.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    render_plan_html(plan, mdt=mdt, target_lang="uk")
    assert stub.calls == [], "uk render should not invoke translator"


def test_render_en_no_client_no_translation_no_crash(monkeypatch):
    """target_lang='en' with NO client configured → render still works,
    no exception. With curated `do_not_do_en` populated on every
    Indication, the EN list renders directly; the UA list is suppressed
    on EN renders."""
    monkeypatch.delenv("DEEPL_API_KEY", raising=False)
    monkeypatch.delenv("LIBRETRANSLATE_URL", raising=False)
    _set_translate_client(None)

    p = _patient("patient_dlbcl_high_ipi.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt, target_lang="en")
    # Document still produced, well-formed
    assert html.startswith("<!DOCTYPE html>")
    assert '<html lang="en">' in html
    # Curated `do_not_do_en` bullets emit instead of UA. The DLBCL
    # indications all carry EN bullets; UA "Не "/"НЕ " stems should
    # no longer appear inside the do_not section. (`_localize_html`
    # post-pass also catches MDT orchestrator UA text registered in
    # `_UI_STRINGS`, so the surrounding HTML is EN too.)
    assert "What NOT to do" in html
    do_not_section = html.split("What NOT to do", 1)[1].split("</section>", 1)[0]
    assert "Не " not in do_not_section and "НЕ " not in do_not_section, (
        "EN render should prefer curated do_not_do_en over UA fallback"
    )


# ── Phase B core: client invoked for long UA fields ──────────────────────


def test_en_render_prefers_do_not_do_en_over_translator():
    """When `do_not_do_en` is curated, EN render uses it directly and
    skips the translate client for those bullets — saves API quota +
    uses authoritative wording (mirrors the bilingual-field policy in
    `test_en_render_uses_bilingual_field_when_available`).

    The DLBCL fixture indications all ship curated `do_not_do_en`, so
    the client should never see a UA "Не "/"НЕ " bullet originating
    from `Indication.do_not_do`."""
    stub = _StubTranslateClient()
    _set_translate_client(stub)

    p = _patient("patient_dlbcl_high_ipi.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None, target_lang="en")

    do_not_calls = [
        c for c in stub.calls
        if "Не " in c[0] or "НЕ " in c[0]
    ]
    assert do_not_calls == [], (
        f"do_not_do bullets should be served from do_not_do_en, not "
        f"translated; client received: {[c[0][:80] for c in do_not_calls]}"
    )
    # Curated EN bullets render in the do_not section
    assert "What NOT to do" in html
    do_not_section = html.split("What NOT to do", 1)[1].split("</section>", 1)[0]
    assert "Do not" in do_not_section or "Do NOT" in do_not_section, (
        "expected curated EN bullets to appear under 'What NOT to do'"
    )


def test_redflag_definitions_skip_translator_when_en_field_present():
    """All RFs in current KB have both `definition` (EN) and
    `definition_ua` — EN render must use the EN field directly without
    invoking the translator. Saves API quota + uses authoritative wording.
    The translation-fallback branch (UA-only definition) is not exercised
    here because no current RF lacks the EN field — but the code path
    exists; future curator-supplied UA-only RF will trigger it."""
    stub = _StubTranslateClient()
    _set_translate_client(stub)

    p = _patient("patient_dlbcl_high_ipi.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    render_plan_html(plan, mdt=None, target_lang="en")

    # No call should contain RedFlag definition_ua text
    rf_text_keywords = ["POLARIX", "ескалований", "Pola-R-CHP замість R-CHOP"]
    rf_calls = [c for c in stub.calls
                if any(k in c[0] for k in rf_text_keywords)]
    assert not rf_calls, (
        f"RedFlag definitions should use EN field directly, not call "
        f"translator; got: {[c[0][:80] for c in rf_calls]}"
    )


def test_en_render_translates_mdt_role_reasons():
    """MDT role.reason fields (UA Ukrainian sentences) route through
    translator on EN render."""
    stub = _StubTranslateClient()
    _set_translate_client(stub)

    p = _patient("patient_dlbcl_high_ipi.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    render_plan_html(plan, mdt=mdt, target_lang="en")

    # Hematologist's reason for required role contains UA "Лімфомний"
    # or "провідна спеціальність" — should be translated
    has_lymphoma_reason = any(
        "Лімфом" in c[0] or "спеціальніст" in c[0]
        for c in stub.calls
    )
    assert has_lymphoma_reason, (
        f"expected MDT role.reason translation; client saw: "
        f"{[c[0][:80] for c in stub.calls[:10]]}"
    )


def test_en_render_uses_bilingual_field_when_available():
    """When a RedFlag has both `definition` (EN) and `definition_ua`,
    EN render should prefer the curated EN definition over translating
    the UA — saves a translator call + uses authoritative wording."""
    stub = _StubTranslateClient()
    _set_translate_client(stub)

    p = _patient("patient_dlbcl_high_ipi.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None, target_lang="en")

    # RF-DLBCL-HIGH-IPI has both `definition` (EN) and `definition_ua`.
    # The EN one mentions "International Prognostic Index" — should
    # appear in HTML directly without going through translator.
    assert "International Prognostic Index" in html, (
        "EN definition field should be used directly when present"
    )


def test_translation_does_not_run_on_uk_render():
    """Default uk render path triggers zero translator calls — no
    accidental cross-language activation."""
    stub = _StubTranslateClient()
    _set_translate_client(stub)

    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    render_plan_html(plan, mdt=mdt, target_lang="uk")
    assert stub.calls == [], (
        f"uk render must not call translator; saw {len(stub.calls)} calls"
    )


def test_translation_failure_falls_back_to_original():
    """If the translator raises, render returns the original text without
    crashing. With curated `do_not_do_en` the translator is no longer in
    the do_not_do path at all; this test now verifies (a) render still
    succeeds end-to-end despite a failing client, and (b) curated EN
    bullets surface unaffected."""
    class _FailingClient:
        name = "failing"

        def translate(self, text, target_lang, source_lang=None):
            raise RuntimeError("simulated network failure")

    _set_translate_client(_FailingClient())

    p = _patient("patient_dlbcl_high_ipi.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None, target_lang="en")

    # Document still produced
    assert html.startswith("<!DOCTYPE html>")
    # Curated EN do_not_do bullets render, untouched by the failing client
    assert "What NOT to do" in html
    do_not_section = html.split("What NOT to do", 1)[1].split("</section>", 1)[0]
    assert "Do not" in do_not_section or "Do NOT" in do_not_section
