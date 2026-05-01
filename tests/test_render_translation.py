"""Phase B / C tests: translation of long free-text in rendered Plan.

Resolution order (per `_translation_overrides.lookup`):
1. Inline `OVERRIDES_UK_TO_EN` — engine-emitted code-side strings
   (MDT role reasons, open questions, rationale).
2. `_do_not_do_en.json` sidecar — KB free-text (do_not_do bullets).
3. Escalation-suffix split for mutated reason strings.
4. Live translate client (DeepL / LibreTranslate) for anything else.
5. Original UA text — graceful degrade when no client is available.

These tests verify each path: strings covered by overrides translate
deterministically without a client; strings outside overrides reach
the client when configured and fall back to UA otherwise.
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


def test_render_en_no_client_overrides_still_translate(monkeypatch):
    """target_lang='en' with NO client configured → render still works
    AND the deterministic override pipeline still translates engine-
    emitted strings + KB do_not_do bullets covered by the JSON sidecar.
    Strings outside the overrides fall back to UA (graceful degrade).
    """
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
    # Override-translated MDT reason present (from inline OVERRIDES_UK_TO_EN)
    assert "Lymphoma diagnosis" in html or "Confirm lymphoma histology" in html, (
        "expected EN MDT reason from inline overrides"
    )
    # Override-translated do_not_do bullet present (from JSON sidecar)
    assert "Do not " in html or "Do NOT " in html, (
        "expected EN do_not_do bullets from sidecar overrides"
    )


# ── Phase B core: client invoked for long UA fields ──────────────────────


def test_en_render_translates_do_not_do_bullets():
    """do_not_do bullets render in EN. Strings present in the JSON
    sidecar are served deterministically (never reach the client);
    strings missing from the sidecar fall through to the live client.
    With every current bullet covered by the sidecar, the client should
    see at most a handful of misses (e.g. drift between KB and sidecar)."""
    stub = _StubTranslateClient()
    _set_translate_client(stub)

    p = _patient("patient_dlbcl_high_ipi.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None, target_lang="en")

    # No raw UA do_not_do bullets in the HTML — overrides covered them
    assert "Не починати" not in html
    assert "Не призначати" not in html
    # Several EN-translated bullets are present
    en_bullets = html.count("Do not ") + html.count("Do NOT ")
    assert en_bullets >= 3, (
        f"expected ≥3 EN do_not_do bullets; got {en_bullets}"
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
    """MDT role.reason fields (engine-emitted UA strings) translate
    deterministically via inline overrides — no client invocation
    needed. Verifies the EN reason text appears in the rendered HTML."""
    p = _patient("patient_dlbcl_high_ipi.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt, target_lang="en")

    # Hematologist reason from inline overrides; UA original removed.
    assert "Lymphoma diagnosis" in html, (
        "expected EN MDT role reason from inline overrides"
    )
    assert "Лімфомний діагноз" not in html, (
        "raw UA reason leaked to EN render"
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
    """If a string is missing from overrides AND the live client raises,
    `_translate_kb_text` returns the original text — never crashes.
    Verifies graceful degrade at the unit level (HTML render is mostly
    covered by overrides today, so we exercise the helper directly)."""
    from knowledge_base.engine.render import _translate_kb_text

    class _FailingClient:
        name = "failing"

        def translate(self, text, target_lang, source_lang=None):
            raise RuntimeError("simulated network failure")

    _set_translate_client(_FailingClient())

    # A UA string we know is NOT in overrides — falls through to the
    # failing client, which raises, and we return the original text.
    needle = "Випадковий рядок який точно не в овверайдах для тесту fallback."
    assert _translate_kb_text(needle, "en") == needle

    # Render still produces a document end-to-end
    p = _patient("patient_dlbcl_high_ipi.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None, target_lang="en")
    assert html.startswith("<!DOCTYPE html>")
