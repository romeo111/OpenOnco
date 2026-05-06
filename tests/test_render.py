"""Tests for the HTML render layer.

Verifies:
1. Treatment Plan render — well-formed HTML, contains expected sections
2. Diagnostic Brief render — diagnostic banner mandatory + workup steps + mandatory questions visible
3. Revision Note render — transition + previous/new IDs + inline new content
4. Embedded CSS only (single-file output, no external <link> for CSS)
5. FDA disclosure present in every output
6. Cyrillic content renders without encoding issues
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from knowledge_base.engine import (
    generate_diagnostic_brief,
    generate_plan,
    orchestrate_mdt,
    render_diagnostic_brief_html,
    render_plan_html,
    render_revision_note_html,
    revise_plan,
)

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


# ── Treatment plan render ─────────────────────────────────────────────────


def test_treatment_plan_html_well_formed():
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt)

    assert html.startswith("<!DOCTYPE html>")
    assert "<html lang=\"uk\">" in html
    assert "<title>" in html and "</title>" in html
    assert "</body>" in html and "</html>" in html
    # CSS embedded, not external (single-file output)
    assert "<style>" in html
    # No external CSS link references (only Google Fonts is allowed)
    css_links = re.findall(r'<link[^>]*rel="stylesheet"[^>]*>', html)
    for link in css_links:
        assert "fonts.googleapis.com" in link, (
            f"non-fonts external CSS link found: {link}"
        )


def test_treatment_plan_shows_both_tracks():
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None)

    assert plan.default_indication_id in html
    assert plan.alternative_indication_id in html
    # Default badge visible somewhere
    assert "DEFAULT" in html or "★" in html


def test_treatment_plan_includes_fda_disclosure():
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None)
    assert "fda-disclosure" in html
    assert "CHARTER §15" in html
    assert "medical-disclaimer" in html


def test_treatment_plan_renders_mdt_when_provided():
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt)
    assert "MDT brief" in html
    assert "hematologist" in html or "Гематолог" in html


# ── Pre-treatment "Where to order" column ─────────────────────────────────


def _ovarian_brca_plan():
    """Fixture that exercises TEST-GERMLINE-BRCA-PANEL → CSD M089."""
    fixture = json.loads(
        (REPO_ROOT / "tests" / "fixtures" / "cases" / "csd_4_ovarian_brca1_plat_sens_2l.json")
        .read_text(encoding="utf-8")
    )
    return generate_plan(fixture, kb_root=KB_ROOT)


def test_pretreatment_table_has_where_to_order_column_uk_and_en():
    plan = _ovarian_brca_plan()
    html_uk = render_plan_html(plan, target_lang="uk")
    html_en = render_plan_html(plan, target_lang="en")
    assert "Де замовити" in html_uk
    assert "Where to order" in html_en


def test_pretreatment_renders_verified_csd_product_code_with_link():
    """A test entity with `lab_availability_ua.product_code` set must surface
    as a clickable chip pointing at the lab's public catalog."""
    plan = _ovarian_brca_plan()
    html = render_plan_html(plan, target_lang="uk")
    assert "TEST-GERMLINE-BRCA-PANEL" in html
    assert "M089" in html
    assert 'class="lab-chip"' in html
    assert "csdlab.ua" in html
    # External link hardening
    assert 'target="_blank"' in html
    assert 'rel="noopener"' in html


def test_pretreatment_renders_category_only_chip_with_tbc_marker():
    """A test entity with `lab_availability_ua` but no product_code must
    render as a soft chip indicating the category is confirmed but the
    specific code is TBC."""
    fixture = json.loads(
        (REPO_ROOT / "tests" / "fixtures" / "cases" / "csd_4_nsclc_egfr_post_osi_2l.json")
        .read_text(encoding="utf-8")
    )
    plan = generate_plan(fixture, kb_root=KB_ROOT)
    html_uk = render_plan_html(plan, target_lang="uk")
    html_en = render_plan_html(plan, target_lang="en")
    # PD-L1 IHC is category-only confirmed
    assert "TEST-PDL1-IHC" in html_uk
    assert "код TBC" in html_uk
    assert "code TBC" in html_en
    # The check-mark is the visual indicator for category-only confirmation
    assert "✓" in html_uk


# ── Diagnostic brief render ───────────────────────────────────────────────


def test_diagnostic_brief_html_contains_mandatory_banner():
    """CHARTER §15.2 C7 — diagnostic banner must be visible above the fold."""
    p = _patient("patient_diagnostic_lymphoma_suspect.json")
    diag = generate_diagnostic_brief(p, kb_root=KB_ROOT)
    html = render_diagnostic_brief_html(diag, mdt=None)
    assert "DIAGNOSTIC PHASE" in html
    assert "TREATMENT PLAN NOT YET APPLICABLE" in html
    assert "banner--diagnostic" in html


def test_diagnostic_brief_shows_workup_steps_and_questions():
    p = _patient("patient_diagnostic_lymphoma_suspect.json")
    diag = generate_diagnostic_brief(p, kb_root=KB_ROOT)
    html = render_diagnostic_brief_html(diag, mdt=None)

    # Workup steps section
    assert "Workup steps" in html
    # IHC + biopsy described inline
    assert "CD20" in html  # IHC baseline marker
    # Mandatory questions section visible
    assert "Питання що мають бути закриті" in html


def test_diagnostic_brief_has_matched_workup_in_output():
    p = _patient("patient_diagnostic_lymphoma_suspect.json")
    diag = generate_diagnostic_brief(p, kb_root=KB_ROOT)
    html = render_diagnostic_brief_html(diag, mdt=None)
    assert "WORKUP-SUSPECTED-LYMPHOMA" in html


# ── Revision note render ─────────────────────────────────────────────────


def test_revision_note_shows_transition_and_ids():
    susp = _patient("patient_diagnostic_lymphoma_suspect.json")
    confirmed = _patient("patient_diagnostic_lymphoma_confirmed.json")

    diag_v1 = generate_diagnostic_brief(susp, kb_root=KB_ROOT)
    revised_prev, plan_v1 = revise_plan(
        confirmed, diag_v1, "biopsy 2026-05-10: HCV-MZL confirmed", kb_root=KB_ROOT,
    )
    html = render_revision_note_html(revised_prev, plan_v1, "diagnostic→treatment", mdt=None)

    assert "Revision Note" in html
    assert "diagnostic→treatment" in html
    assert diag_v1.diagnostic_plan.id in html
    assert plan_v1.plan.id in html
    # Trigger surfaced
    assert "biopsy 2026-05-10" in html


# ── Cyrillic / unicode safety ─────────────────────────────────────────────


def test_cyrillic_content_renders_without_loss():
    p = _patient("patient_diagnostic_lymphoma_suspect.json")
    diag = generate_diagnostic_brief(p, kb_root=KB_ROOT)
    html = render_diagnostic_brief_html(diag, mdt=None)
    # The mandatory_questions text is in Ukrainian — must be preserved intact
    assert "лімфома" in html.lower() or "лімфому" in html.lower()
    # Encoding declared
    assert 'charset="UTF-8"' in html


# ── No patient PII leaked from the reference HTML files ──────────────────


def test_render_does_not_leak_reference_patient_initials():
    """The infograph reference HTML files contain real patient initials
    (V.D.V.). We borrow only the visual idiom, never the patient text.
    Smoke check that the rendered output of a synthetic patient contains
    no string that looks like the reference patient ID."""
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None)
    # Latin and Cyrillic forms of the reference patient initials
    assert "V.D.V" not in html
    assert "В.Д.В" not in html


# ── MDT brief prioritizes discussion questions over audit metadata ────────


def test_mdt_brief_hides_skill_version_per_role():
    """Activated roles should stay clinically focused. Skill versions are
    audit metadata and belong in the collapsed catalog footer."""
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt)

    assert "skill-meta" not in html
    assert "q-list--featured" in html
    assert html.index('<ul class="q-list q-list--featured"') < html.index('<ul class="role-list"')


def test_mdt_brief_includes_collapsed_skill_catalog_with_activation_markers():
    """Skill catalog footer must list all registered skills with versions,
    but it should be collapsed so discussion questions remain the focus."""
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt)

    assert "skill-catalog" in html
    assert '<details class="skill-catalog">' in html
    # Every catalog row still carries a version for audit when expanded.
    from knowledge_base.engine.mdt_orchestrator import _SKILL_REGISTRY
    for sid, s in _SKILL_REGISTRY.items():
        assert sid in html, f"skill_id '{sid}' missing from rendered catalog"
    # Activation marker must mention the count
    import re
    m = re.search(r"<summary>.*\((\d+)/(\d+)", html)
    assert m, "skill catalog header missing activation count"
    activated, total = int(m.group(1)), int(m.group(2))
    assert total == len(_SKILL_REGISTRY)
    assert 1 <= activated <= total


def test_role_block_uses_skill_framing_in_ukrainian():
    """User explicitly requested 'віртуальні спеціалісти' framing instead
    of generic 'roles'."""
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt)
    assert "Скіли" in html or "віртуальні спеціалісти" in html.lower()


# ── i18n: target_lang switch (auto-translate render output) ───────────────


def test_render_default_target_lang_is_ukrainian():
    """Backward compat: default render produces UA HTML."""
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None)
    assert '<html lang="uk">' in html
    assert "Що НЕ робити" in html
    assert "Етіологічний драйвер" in html


def test_render_target_lang_en_localizes_ui_strings():
    """target_lang='en' post-processes the UA render to swap UI labels."""
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt, target_lang="en")
    # html lang attribute flipped
    assert '<html lang="en">' in html
    assert '<html lang="uk">' not in html
    # Section headers translated
    assert "What NOT to do" in html
    assert "Etiological driver" in html
    assert "Skills (required) — mandatory virtual specialists" in html
    assert "Skills (recommended) — for consideration" in html
    # UA section headers absent
    assert "Що НЕ робити" not in html
    assert "Етіологічний драйвер" not in html
    assert "Скіли (required)" not in html
    # Common UA pairs translated
    assert "Hard contraindications" in html  # was already EN
    # Disclaimer translated to EN
    assert "informational resource" in html or "tumor-board discussion" in html
    assert "Цей документ — інформаційний ресурс" not in html


def test_render_diagnostic_brief_target_lang_en():
    """Diagnostic-mode render also accepts target_lang."""
    from knowledge_base.engine import generate_diagnostic_brief
    p = _patient("patient_diagnostic_lymphoma_suspect.json")
    res = generate_diagnostic_brief(p, kb_root=KB_ROOT)
    html = render_diagnostic_brief_html(res, target_lang="en")
    assert '<html lang="en">' in html


def test_render_target_lang_unknown_falls_back_to_uk():
    """Unsupported target_lang doesn't break — falls back to UA."""
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None, target_lang="ja")
    # No translation map for 'ja' → all UA strings remain, but lang attr flipped
    assert "Що НЕ робити" in html


def test_render_target_lang_preserves_entity_ids_and_doses():
    """Entity IDs / doses must survive the localization pass unchanged
    (they're in the substitution corpus only as values, never as keys).

    Note: regimen IDs (REG-*) are not surfaced in the rendered HTML —
    only regimen NAMES are — so we check IDs that actually appear in
    the document (disease, indication, source IDs)."""
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=None, target_lang="en")
    for token in ("DIS-HCV-MZL", "IND-HCV-MZL-1L-ANTIVIRAL", "SRC-NCCN-BCELL-2025"):
        assert token in html, f"localization swallowed entity ID '{token}'"


def test_treatment_plan_renders_biomarker_coverage_in_mdt():
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt, target_lang="en")

    assert "Biomarker coverage:" in html
    assert "biomarker_coverage" not in html


def test_treatment_plan_renders_doctor_facing_data_quality_actions():
    p = _patient("patient_zero_indolent.json")
    findings = dict(p.get("findings") or {})
    findings.pop("hbsag", None)
    p = {**p, "findings": findings}
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt, target_lang="en")

    assert "Incomplete for MDT sign-off" in html
    assert "Missing data for doctor action" in html
    assert "HBsAg" in html
    assert "Order or document HBsAg" in html


def test_treatment_plan_renders_ukrainian_data_quality_actions():
    p = _patient("patient_zero_indolent.json")
    findings = dict(p.get("findings") or {})
    findings.pop("hbsag", None)
    p = {**p, "findings": findings}
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt, target_lang="uk")

    assert "Якість даних" in html
    assert "Неповно для підписання MDT" in html
    assert "Відсутні дані для дії лікаря" in html
    assert "Призначити або задокументувати HBsAg" in html
    assert "Missing data for doctor action" not in html


def test_treatment_plan_renders_mdt_talk_tree():
    p = _patient("patient_zero_indolent.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt)

    assert "MDT talk tree" in html
    assert "<th>Owner</th>" in html
    assert "<th>Action</th>" in html
