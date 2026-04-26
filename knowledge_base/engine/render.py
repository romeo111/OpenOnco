"""HTML render layer — Plan / DiagnosticPlan / Revision → single-file
A4-printable HTML document.

Design language adapted from the project's reference patient deliverables
(infograph/*план лікування.html — gitignored, not the source of patient
data; only the visual idiom is borrowed): green medical palette, DM Serif
Display headings, Source Sans 3 body, badges + alerts + cards.
Layout adapted for A4 print + browser preview (no scroll-snap, single
flow column). UI patterns avoid automation bias per CHARTER §15.2 C6
(both tracks shown side-by-side, alternative is not buried, every
recommendation cites sources).

Three render entry points (one per document type):

- render_plan_html(plan_result, mdt=None) — treatment Plan with tracks
- render_diagnostic_brief_html(diag_result, mdt=None) — Workup Brief
- render_revision_note_html(prev, new, transition) — Revision Note

Each returns a complete single-file HTML string (CSS embedded). Caller
decides where to write it.

Per CHARTER §15.2 C7 — diagnostic banner mandatory in DiagnosticBrief,
treatment-Plan-not-applicable disclaimer surfaced above the fold.
"""

from __future__ import annotations

import functools
import html
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

import yaml

from ._ask_doctor import select_questions as _select_ask_doctor_questions
from ._emergency_rf import filter_emergency_rfs, patient_emergency_label
from ._nszu import lookup_nszu_status, nszu_label
from ._patient_vocabulary import (
    NSZU_PATIENT_LABEL,
    ESCAT_TIER_PATIENT_LABEL,
    explain as _explain_patient,
)
from .diagnostic import _DIAGNOSTIC_BANNER, DiagnosticPlanResult
from .mdt_orchestrator import MDTOrchestrationResult
from .plan import PlanResult
from .render_styles import PATIENT_MODE_CSS as _PATIENT_CSS
from .render_styles import STYLESHEET as _CSS




# ── Helpers ───────────────────────────────────────────────────────────────


def _h(s) -> str:
    """Escape for HTML output."""
    if s is None:
        return ""
    return html.escape(str(s))


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# ── Sign-off badge (CHARTER §6.1) ─────────────────────────────────────────
#
# Indications carry `reviewer_signoffs_v2: list[ReviewerSignoff]` after the
# `scripts/clinical_signoff.py` CLI is run. The plan render surfaces the
# coverage state as a coloured badge so the clinician sees at a glance
# whether the recommendation has the two Clinical Co-Lead approvals
# CHARTER §6.1 requires.
#
# Reviewer display names come from `knowledge_base/hosted/content/reviewers/`
# and are cached for the process lifetime.


@functools.lru_cache(maxsize=1)
def _load_reviewer_labels() -> dict[str, str]:
    """REV-* → display_name. Cached. Returns empty dict on failure."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    rev_dir = repo_root / "knowledge_base" / "hosted" / "content" / "reviewers"
    if not rev_dir.is_dir():
        return {}
    out: dict[str, str] = {}
    for p in sorted(rev_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and data.get("id"):
            out[data["id"]] = str(data.get("display_name") or data["id"])
    return out


def _signoff_label(reviewer_id: str) -> str:
    """REV-* → display_name with REV-id fallback."""
    return _load_reviewer_labels().get(reviewer_id, reviewer_id)


def _render_signoff_badge(entity_data: Optional[dict]) -> str:
    """Render a clinician-mode sign-off badge for an Indication / Algorithm /
    Regimen / RedFlag / BiomarkerActionability dict.

    States:
      - 0 sign-offs   → red    (Очікує підпису Clinical Co-Lead)
      - 1 sign-off    → yellow (Підписано (1/2): {reviewer})
      - ≥2 sign-offs  → green  (Клінічно затверджено: {r1}, {r2})

    Returns empty string when entity_data is None.
    """
    if not isinstance(entity_data, dict):
        return ""
    sigs = entity_data.get("reviewer_signoffs_v2") or []
    sigs = [s for s in sigs if isinstance(s, dict) and s.get("reviewer_id")]
    n = len(sigs)
    if n == 0:
        return (
            '<span class="signoff-badge signoff-pending">'
            '⚠ Очікує підпису Clinical Co-Lead</span>'
        )
    if n == 1:
        rid = sigs[0]["reviewer_id"]
        return (
            '<span class="signoff-badge signoff-partial">'
            f'🟡 Підписано (1/2): {_h(_signoff_label(rid))}'
            '</span>'
        )
    names = ", ".join(_signoff_label(s["reviewer_id"]) for s in sigs[:3])
    if n > 3:
        names += f" + {n - 3}"
    return (
        '<span class="signoff-badge signoff-complete">'
        f'✓ Клінічно затверджено: {_h(names)}'
        '</span>'
    )


def _render_signoff_badge_patient(entity_data: Optional[dict]) -> str:
    """Patient-mode sign-off — simpler vocabulary, no reviewer names."""
    if not isinstance(entity_data, dict):
        return ""
    sigs = entity_data.get("reviewer_signoffs_v2") or []
    sigs = [s for s in sigs if isinstance(s, dict) and s.get("reviewer_id")]
    n = len(sigs)
    if n >= 2:
        return (
            '<span class="patient-badge patient-good signoff-complete">'
            'Затверджено лікарями</span>'
        )
    if n == 1:
        return (
            '<span class="patient-badge patient-warn signoff-partial">'
            'Очікує перевірки лікарями (1 з 2)</span>'
        )
    return (
        '<span class="patient-badge patient-emergency signoff-pending">'
        'Очікує перевірки лікарями</span>'
    )


# ── i18n: live translation client for long free-text ─────────────────────
#
# Phase B of auto-translate render: long free-text from KB (Indication
# notes, do_not_do bullets, RedFlag definitions, MDT role reasons) goes
# through a configured translate client (DeepL Free + LibreTranslate
# fallback + glossary protection + on-disk cache).
#
# Graceful degrade: if neither DEEPL_API_KEY nor LIBRETRANSLATE_URL is
# set in the environment, `_translate_kb_text` returns the original UA
# text unchanged. Render still produces a usable document, just with
# UA-only KB content embedded.
#
# Per CHARTER §8.3 every cached translation is marked
# `machine_translated: true` for clinician review.

_TRANSLATE_CLIENT = None
_TRANSLATE_CLIENT_INIT = False


def _get_translate_client():
    """Lazy-load the translate client once per process. Returns None if
    no upstream is configured — caller falls back to original text."""
    global _TRANSLATE_CLIENT, _TRANSLATE_CLIENT_INIT
    if _TRANSLATE_CLIENT_INIT:
        return _TRANSLATE_CLIENT
    _TRANSLATE_CLIENT_INIT = True
    import os
    if not (os.environ.get("DEEPL_API_KEY") or os.environ.get("LIBRETRANSLATE_URL")):
        _TRANSLATE_CLIENT = None
        return None
    try:
        from knowledge_base.clients.translate_client import build_full_stack
        _TRANSLATE_CLIENT = build_full_stack()
    except Exception:
        _TRANSLATE_CLIENT = None
    return _TRANSLATE_CLIENT


def _set_translate_client(client) -> None:
    """Test hook — inject a stub client. Pass None to clear + force
    re-init from env on next call."""
    global _TRANSLATE_CLIENT, _TRANSLATE_CLIENT_INIT
    _TRANSLATE_CLIENT = client
    _TRANSLATE_CLIENT_INIT = client is not None


def _translate_kb_text(text: str, target_lang: str, source_lang: str = "uk") -> str:
    """Translate a UA free-text fragment to target_lang via the configured
    client. Returns the original text if:
    - target_lang is the source language (no translation needed)
    - text is empty or whitespace-only
    - no translate client configured (graceful degrade)
    - the client raises (network failure, quota, etc.)
    """
    if not text or not text.strip():
        return text
    if target_lang == source_lang or not target_lang:
        return text
    client = _get_translate_client()
    if client is None:
        return text
    try:
        return client.translate(text, target_lang=target_lang, source_lang=source_lang)
    except Exception:
        return text


def _h_t(text, target_lang: str = "uk", source_lang: str = "uk") -> str:
    """HTML-escape AND translate (where applicable). Drop-in replacement
    for `_h(...)` at sites that emit long UA free-text from the KB.
    Translation happens BEFORE escaping — the cached translation is in
    natural language, escape is just transport."""
    if text is None:
        return ""
    return html.escape(_translate_kb_text(str(text), target_lang, source_lang))


# ── i18n: UI label dictionary (UA + EN) ───────────────────────────────────
#
# Used by render to switch static section headers / banners / disclaimers
# between UA and EN. Long free-text from KB is handled by
# `_translate_kb_text` (live translation, configured via env vars).
# For `target_lang` outside {uk, en}, falls back to UA on UI labels;
# free-text still translated by the client if it supports the language.

_UI_STRINGS: dict[str, dict[str, str]] = {
    # Section headers
    "treatment_options":           {"uk": "Варіанти лікування", "en": "Treatment options"},
    "etiological_driver":          {"uk": "Етіологічний драйвер", "en": "Etiological driver"},
    "etiological_driver_label":    {"uk": "Etiological driver · etiologically_driven archetype",
                                    "en": "Etiological driver · etiologically_driven archetype"},
    "pretreatment":                {"uk": "Pre-treatment investigations",
                                    "en": "Pre-treatment investigations"},
    "pretreatment_sub":            {"uk": "Дослідження перед стартом терапії · критичні / стандарт / бажано · поєднані по треках",
                                    "en": "Investigations before treatment start · critical / standard / desired · merged across tracks"},
    "redflags_pro_contra":         {"uk": "Red flags — PRO / CONTRA aggressive",
                                    "en": "Red flags — PRO / CONTRA aggressive"},
    "what_not":                    {"uk": "Що НЕ робити", "en": "What NOT to do"},
    "what_not_sub":                {"uk": "Прямі прохібітивні правила, кожне з обґрунтуванням у regimen / supportive care / contraindication",
                                    "en": "Explicit prohibitive rules, each grounded in a regimen / supportive care / contraindication entity"},
    "monitoring":                  {"uk": "Monitoring schedule", "en": "Monitoring schedule"},
    "monitoring_sub":              {"uk": "Графік моніторингу за фазами лікування",
                                    "en": "Monitoring schedule by treatment phase"},
    "timeline":                    {"uk": "Timeline", "en": "Timeline"},
    "timeline_sub":                {"uk": "Хронологія лікування — derived from regimen + monitoring schedule",
                                    "en": "Treatment timeline — derived from regimen + monitoring schedule"},
    "skills_required":             {"uk": "Скіли (required) — обов'язкові віртуальні спеціалісти",
                                    "en": "Skills (required) — mandatory virtual specialists"},
    "skills_recommended":          {"uk": "Скіли (recommended) — рекомендовані для розгляду",
                                    "en": "Skills (recommended) — for consideration"},
    "skills_optional":             {"uk": "Скіли (optional) — опціональні",
                                    "en": "Skills (optional)"},
    "mdt_brief":                   {"uk": "MDT brief", "en": "MDT brief"},
    "open_questions":              {"uk": "Open questions", "en": "Open questions"},
    "data_quality":                {"uk": "Data quality", "en": "Data quality"},
    "blocking":                    {"uk": "BLOCKING", "en": "BLOCKING"},
    "sources_cited":               {"uk": "Sources cited", "en": "Sources cited"},
    # Track labels (matches plan.py track id semantics)
    "track_standard":              {"uk": "Стандартний план", "en": "Standard plan"},
    "track_aggressive":            {"uk": "Агресивний план", "en": "Aggressive plan"},
    "track_surveillance":          {"uk": "Активне спостереження (watch-and-wait)",
                                    "en": "Active surveillance (watch-and-wait)"},
    "track_palliative":            {"uk": "Паліативний план", "en": "Palliative plan"},
    "track_trial":                 {"uk": "План у рамках клінічного дослідження", "en": "Clinical-trial-only plan"},
    # Document headers
    "doc_label_plan":              {"uk": "OpenOnco · Treatment Plan", "en": "OpenOnco · Treatment Plan"},
    "doc_title_plan_prefix":       {"uk": "План лікування", "en": "Treatment plan"},
    "doc_label_brief":             {"uk": "OpenOnco · Workup Brief · DIAGNOSTIC PHASE",
                                    "en": "OpenOnco · Workup Brief · DIAGNOSTIC PHASE"},
    "doc_title_brief":             {"uk": "Brief підготовки до тумор-борду", "en": "Pre-tumor-board workup brief"},
    "doc_label_revision":          {"uk": "OpenOnco · Revision Note", "en": "OpenOnco · Revision Note"},
    "doc_title_revision":          {"uk": "Перегляд плану", "en": "Plan revision"},
    # Banners and labels
    "diagnostic_banner_strong":    {"uk": "⚠ DIAGNOSTIC PHASE — TREATMENT PLAN NOT YET APPLICABLE",
                                    "en": "⚠ DIAGNOSTIC PHASE — TREATMENT PLAN NOT YET APPLICABLE"},
    "patient_label":               {"uk": "Patient", "en": "Patient"},
    "default_badge":                {"uk": "★ DEFAULT", "en": "★ DEFAULT"},
    "indication_label":            {"uk": "Indication", "en": "Indication"},
    "regimen_label":               {"uk": "Regimen", "en": "Regimen"},
    "supportive_label":            {"uk": "Supportive care", "en": "Supportive care"},
    "ci_label":                    {"uk": "Hard contraindications", "en": "Hard contraindications"},
    "reason_label":                {"uk": "Reason", "en": "Reason"},
    # Skill catalog
    "skill_catalog_prefix":        {"uk": "Skill catalog", "en": "Skill catalog"},
    "skill_catalog_active_in":     {"uk": "активовано в цьому плані", "en": "activated in this plan"},
    "skill_catalog_legend":        {"uk": "Усі зареєстровані віртуальні спеціалісти. ✓ — активовано для цього кейсу; ○ — не активовано (доступні для інших клінічних сценаріїв).",
                                    "en": "All registered virtual specialists. ✓ — activated for this case; ○ — not activated (available for other clinical scenarios)."},
    "th_specialist":               {"uk": "Спеціаліст", "en": "Specialist"},
    "th_skill_id":                 {"uk": "skill_id", "en": "skill_id"},
    "th_version":                  {"uk": "Версія", "en": "Version"},
    "th_last_reviewed":            {"uk": "Last reviewed", "en": "Last reviewed"},
    "th_signoffs":                 {"uk": "Sign-offs", "en": "Sign-offs"},
    "th_domain":                   {"uk": "Domain", "en": "Domain"},
    "th_id":                       {"uk": "ID", "en": "ID"},
    "th_name":                     {"uk": "Назва", "en": "Name"},
    "th_priority":                 {"uk": "Пріоритет", "en": "Priority"},
    "th_category":                 {"uk": "Категорія", "en": "Category"},
    "th_needed_for":               {"uk": "Потрібно для", "en": "Needed for"},
    "th_phase":                    {"uk": "Фаза", "en": "Phase"},
    "th_window":                   {"uk": "Вікно", "en": "Window"},
    "th_tests":                    {"uk": "Тести", "en": "Tests"},
    "th_checkpoints":              {"uk": "Контрольні точки", "en": "Checkpoints"},
    "scope_all_tracks":            {"uk": "усі треки", "en": "all tracks"},
    "scope_desired_prefix":        {"uk": "бажано", "en": "desired"},
    # Priority labels
    "priority_critical":           {"uk": "Критично", "en": "Critical"},
    "priority_standard":           {"uk": "Стандарт", "en": "Standard"},
    "priority_desired":            {"uk": "Бажано", "en": "Desired"},
    "priority_calculation_based":  {"uk": "Розрахунок", "en": "Calculation"},
    # PRO/CONTRA columns
    "pro_aggressive":              {"uk": "PRO-AGGRESSIVE", "en": "PRO-AGGRESSIVE"},
    "pro_aggressive_sub":          {"uk": "Тригери що штовхають до агресивного треку",
                                    "en": "Triggers that push toward the aggressive track"},
    "contra_aggressive":           {"uk": "CONTRA-AGGRESSIVE", "en": "CONTRA-AGGRESSIVE"},
    "contra_aggressive_sub":       {"uk": "Жорсткі протипоказання до ескалації",
                                    "en": "Hard contraindications to escalation"},
    # Timeline phase names
    "tl_baseline":                 {"uk": "Baseline", "en": "Baseline"},
    "tl_induction":                {"uk": "Induction", "en": "Induction"},
    "tl_response":                 {"uk": "Response assessment", "en": "Response assessment"},
    "tl_maintenance":              {"uk": "Maintenance", "en": "Maintenance"},
    "tl_followup":                 {"uk": "Follow-up", "en": "Follow-up"},
    # Disclaimers
    "medical_disclaimer":          {
        "uk": "Цей документ — інформаційний ресурс для підтримки обговорення в "
              "тумор-борді (per CHARTER §11). Не система, що приймає клінічні рішення. "
              "Усі рекомендації потребують перевірки лікуючим лікарем.",
        "en": "This document is an informational resource supporting tumor-board "
              "discussion (per CHARTER §11). It is not a system that makes clinical "
              "decisions. Every recommendation must be verified by the treating physician.",
    },
    "fda_disclosure_label":        {"uk": "Per FDA non-device CDS positioning (CHARTER §15):",
                                    "en": "Per FDA non-device CDS positioning (CHARTER §15):"},
    # Variant actionability (ESCAT / OncoKB)
    "actionability_heading":       {"uk": "Клінічна значущість мутацій (ESCAT / OncoKB)",
                                    "en": "Clinical significance of mutations (ESCAT / OncoKB)"},
    "actionability_sub":           {"uk": "Контекст для тумор-борду — інженер не використовує ці тіри для вибору треку",
                                    "en": "Tumor-board context — the engine does not use these tiers to rank tracks"},
    "actionability_th_biomarker":  {"uk": "Біомаркер", "en": "Biomarker"},
    "actionability_th_variant":    {"uk": "Варіант", "en": "Variant"},
    "actionability_th_escat":      {"uk": "ESCAT", "en": "ESCAT"},
    "actionability_th_oncokb":     {"uk": "OncoKB", "en": "OncoKB"},
    "actionability_th_action":     {"uk": "Клінічна дія", "en": "Clinical significance"},
    "actionability_th_combos":     {"uk": "Препарати", "en": "Drugs"},
    "actionability_th_sources":    {"uk": "Джерела", "en": "Sources"},
    "actionability_empty":         {"uk": "Не знайдено клінічно значущих варіантів у цьому профілі.",
                                    "en": "No clinically actionable variants matched in this profile."},
    "actionability_gene_level":    {"uk": "(гено-рівень)", "en": "(gene-level)"},
}


def _t(key: str, target_lang: str = "uk") -> str:
    """Look up a UI label in the desired language. Falls back to UA if
    the key is missing in the target language. Falls back to the key
    itself if the key is missing entirely (defensive — surfaces missing
    translations clearly in the rendered output)."""
    entry = _UI_STRINGS.get(key)
    if entry is None:
        return key
    return entry.get(target_lang) or entry.get("uk") or key


def _track_label(track_id: str, target_lang: str = "uk") -> str:
    """Map a track_id to its localized display label."""
    return _t(f"track_{track_id}", target_lang) or track_id


def _localize_html(html_text: str, target_lang: str) -> str:
    """Post-process a fully-rendered UA HTML document into another language
    by targeted UI-label substitution. The render layer always produces UA
    first; if the caller asks for `target_lang != "uk"`, we do longest-first
    string replacements over the known UI labels in `_UI_STRINGS` plus a
    handful of common phrases used inside f-strings.

    Free-text KB content (Indication.rationale, Indication.notes, RedFlag
    definitions, etc.) is NOT translated here — that's the next iteration
    via `knowledge_base.clients.translate_client`. Only UI labels.

    Also flips `<html lang="uk">` to `<html lang="en">` for proper a11y.
    """
    if target_lang == "uk" or not target_lang:
        return html_text

    # Build the substitution map: UA-side string → target-lang string, only
    # when both sides exist and differ. Include both the raw and the
    # HTML-escaped form (the render layer pipes most strings through _h()
    # which encodes apostrophes as `&#x27;` etc.) — without the escaped
    # variant a UA literal like "обов'язкові" would never match. Longest-
    # first to avoid collisions ("Стандартний план" before "Стандарт").
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for entry in _UI_STRINGS.values():
        ua = entry.get("uk")
        out = entry.get(target_lang)
        if not ua or not out or ua == out:
            continue
        for src, dst in (
            (ua, out),
            (html.escape(ua, quote=True), html.escape(out, quote=True)),
        ):
            if src in seen or src == dst:
                continue
            pairs.append((src, dst))
            seen.add(src)
    pairs.sort(key=lambda p: len(p[0]), reverse=True)

    out_html = html_text
    for src, dst in pairs:
        out_html = out_html.replace(src, dst)

    # Doc-language attribute
    out_html = out_html.replace('<html lang="uk">', f'<html lang="{target_lang}">')
    return out_html


def _doc_shell(title: str, body: str, target_lang: str = "uk") -> str:
    """Wrap rendered body in a complete HTML document with embedded CSS."""
    lang_attr = "en" if target_lang == "en" else "uk"
    return (
        "<!DOCTYPE html>\n"
        f'<html lang="{lang_attr}">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"<title>{_h(title)}</title>\n"
        '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900'
        '&family=Source+Sans+3:wght@300;400;500;600;700'
        '&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">\n'
        f"<style>{_CSS}</style>\n"
        "</head>\n<body>\n"
        f'<div class="page">{body}</div>\n'
        "</body>\n</html>\n"
    )


def _render_mdt_section(mdt: Optional[MDTOrchestrationResult],
                        target_lang: str = "uk") -> str:
    if mdt is None:
        return ""
    parts: list[str] = []

    def _skill_meta_html(r) -> str:
        """One-line metadata strip showing skill version + last-reviewed
        date + sign-off status — so a clinician verifying changes can see
        at a glance which version of which skill produced this row."""
        s = r.skill
        if s is None:
            return ""
        status_cls = "pill--reviewed" if s.review_status == "reviewed" else "pill--stub"
        status_label = "REVIEWED" if s.review_status == "reviewed" else "STUB"
        lead = _h(s.clinical_lead) if s.clinical_lead else "TBD"
        return (
            '<div class="skill-meta">'
            f'<span class="pill">skill: <code>{_h(s.skill_id)}</code></span>'
            f'<span class="pill">v{_h(s.version)}</span>'
            f'<span class="pill">reviewed {_h(s.last_reviewed)}</span>'
            f'<span class="pill {status_cls}">{status_label}</span>'
            f'<span class="pill">sign-offs: {s.signoffs}</span>'
            f'<span class="pill">lead: {lead}</span>'
            "</div>"
        )

    def _role_block(label: str, badge_cls: str, roles) -> str:
        if not roles:
            return ""
        items = []
        for r in roles:
            qs = (
                f'<div class="role-questions">Owns: {_h(", ".join(r.linked_questions))}</div>'
                if r.linked_questions else ""
            )
            items.append(
                f"<li>"
                f'<span class="role-name">{_h(r.role_name)}</span> '
                f'<span class="badge {badge_cls}">{_h(r.priority)}</span>'
                f'<div class="role-reason">{_h_t(r.reason, target_lang)}</div>'
                f"{qs}"
                f"{_skill_meta_html(r)}"
                f"</li>"
            )
        return (
            f"<h3>{_h(label)} ({len(roles)})</h3>"
            f'<ul class="role-list">{"".join(items)}</ul>'
        )

    parts.append(_role_block(
        "Скіли (required) — обов'язкові віртуальні спеціалісти",
        "badge--required", mdt.required_roles))
    parts.append(_role_block(
        "Скіли (recommended) — рекомендовані для розгляду",
        "badge--recommended", mdt.recommended_roles))
    parts.append(_role_block(
        "Скіли (optional) — опціональні",
        "badge--optional", mdt.optional_roles))

    qs = mdt.open_questions
    if qs:
        blocking = sum(1 for q in qs if q.blocking)
        items = []
        for q in qs:
            cls = " blocking" if q.blocking else ""
            tag = '<span class="badge badge--blocking">BLOCKING</span> ' if q.blocking else ""
            items.append(
                f'<li class="{cls.strip()}">'
                f'<div class="q-id">{tag}{_h(q.id)}</div>'
                f'<div class="q-text">{_h_t(q.question, target_lang)}</div>'
                f'<div class="q-rationale">{_h_t(q.rationale, target_lang)}</div>'
                f'<div class="q-owner">→ {_h(q.owner_role)}</div>'
                f"</li>"
            )
        parts.append(
            f"<h3>Open questions ({len(qs)}, {blocking} blocking)</h3>"
            f'<ul class="q-list">{"".join(items)}</ul>'
        )

    dq = mdt.data_quality_summary or {}
    crit = dq.get("missing_critical_fields") or []
    rec = dq.get("missing_recommended_fields") or []
    unevaluated = dq.get("unevaluated_red_flags") or []
    if crit or rec or unevaluated:
        parts.append("<h3>Data quality</h3><ul>")
        if crit:
            parts.append(f"<li>Missing critical: {_h(', '.join(crit))}</li>")
        if rec:
            parts.append(f"<li>Missing recommended: {_h(', '.join(rec))}</li>")
        if unevaluated:
            parts.append(f"<li>Unevaluated RedFlags: {_h(', '.join(unevaluated))}</li>")
        parts.append("</ul>")

    # Skill catalog — full list of registered skills with activation marker
    activated_ids = {s.skill_id for s in mdt.activated_skills}
    catalog_rows = []
    # Pull the full registry via the dict surfaced through to_dict()
    full = mdt.to_dict().get("skill_catalog", [])
    for s in full:
        sid = s["skill_id"]
        is_active = sid in activated_ids
        cls = "activated" if is_active else "dormant"
        catalog_rows.append(
            f'<tr class="{cls}">'
            f'<td>{_h(s["name"])}</td>'
            f'<td><code>{_h(sid)}</code></td>'
            f'<td class="ver">v{_h(s["version"])}</td>'
            f'<td>{_h(s["last_reviewed"])}</td>'
            f'<td>{s["signoffs"]}</td>'
            f'<td>{_h(s.get("domain") or "—")}</td>'
            "</tr>"
        )
    parts.append(
        '<div class="skill-catalog">'
        f'<h3>Skill catalog ({len(activated_ids)}/{len(full)} активовано в цьому плані)</h3>'
        '<div class="section-sub">Усі зареєстровані віртуальні спеціалісти. '
        '✓ — активовано для цього кейсу; ○ — не активовано (доступні для інших клінічних сценаріїв).</div>'
        '<table><thead><tr>'
        '<th>Спеціаліст</th><th>skill_id</th><th>Версія</th>'
        '<th>Last reviewed</th><th>Sign-offs</th><th>Domain</th>'
        "</tr></thead><tbody>"
        f'{"".join(catalog_rows)}'
        "</tbody></table>"
        "</div>"
    )

    return f'<section><h2>MDT brief</h2><div class="mdt">{"".join(parts)}</div></section>'


def _render_fda_disclosure(text: str) -> str:
    return (
        f'<div class="fda-disclosure">'
        f"<strong>Per FDA non-device CDS positioning (CHARTER §15):</strong> "
        f"{_h(text)}"
        f"</div>"
    )


def _render_version_chain(plan_id, version, supersedes, superseded_by, generated_at) -> str:
    parts = [f"plan_id: {_h(plan_id)} | version: {_h(version)} | generated: {_h(generated_at)}"]
    if supersedes:
        parts.append(f"supersedes: {_h(supersedes)}")
    if superseded_by:
        parts.append(f"superseded_by: {_h(superseded_by)}")
    return f'<div class="version-chain">{" | ".join(parts)}</div>'


_MEDICAL_DISCLAIMER = (
    "Цей документ — інформаційний ресурс для підтримки обговорення в "
    "тумор-борді (per CHARTER §11). Не система, що приймає клінічні рішення. "
    "Усі рекомендації потребують перевірки лікуючим лікарем."
)


# ── Section helpers (treatment Plan) ──────────────────────────────────────


def _render_etiological_driver(disease: Optional[dict]) -> str:
    """Etiologically-driven archetype gets a featured card explaining WHY
    a particular driver (HCV, H. pylori, EBV, etc.) shapes treatment.
    Returns empty string for non-etiologically_driven diseases."""
    if not disease:
        return ""
    archetype = disease.get("archetype")
    if archetype != "etiologically_driven":
        return ""
    factors = disease.get("etiological_factors") or []
    name = (disease.get("names") or {}).get("ukrainian") or (
        disease.get("names") or {}).get("preferred") or disease.get("id", "")
    factor_items = "".join(f"<li>{_h(f)}</li>" for f in factors) or "<li>—</li>"
    return (
        '<section>'
        '<h2>Етіологічний драйвер</h2>'
        '<div class="etiology-card">'
        '<div class="label">Etiological driver · etiologically_driven archetype</div>'
        f'<div class="archetype">{_h(name)}</div>'
        f'<ul>{factor_items}</ul>'
        '</div>'
        '</section>'
    )


_PRIORITY_LABEL_UA = {
    "critical": "Критично",
    "standard": "Стандарт",
    "desired": "Бажано",
    "calculation_based": "Розрахунок",
}
_PRIORITY_BADGE_CLS = {
    "critical": "badge--required",
    "standard": "badge--recommended",
    "desired": "badge--optional",
    "calculation_based": "badge--optional",
}
_PRIORITY_RANK = {"critical": 0, "standard": 1, "desired": 2, "calculation_based": 3}


def _render_pretreatment_investigations(plan, kb_resolved: dict) -> str:
    """Pre-treatment investigations table: union of required + desired tests
    across all tracks, sorted by priority_class. Each row shows test name,
    priority badge, category, and which tracks need it.
    Per REFERENCE_CASE_SPECIFICATION §3.5."""
    tests_lookup = (kb_resolved or {}).get("tests") or {}
    if not tests_lookup:
        return ""

    # Collect: test_id → {required_by: set[track_id], desired_by: set[track_id]}
    test_use: dict[str, dict] = {}
    for t in plan.tracks:
        ind = t.indication_data or {}
        for tid in ind.get("required_tests") or []:
            test_use.setdefault(tid, {"required_by": set(), "desired_by": set()})
            test_use[tid]["required_by"].add(t.track_id)
        for tid in ind.get("desired_tests") or []:
            test_use.setdefault(tid, {"required_by": set(), "desired_by": set()})
            test_use[tid]["desired_by"].add(t.track_id)
    if not test_use:
        return ""

    rows = []
    for tid, use in sorted(
        test_use.items(),
        key=lambda kv: (
            _PRIORITY_RANK.get((tests_lookup.get(kv[0]) or {}).get("priority_class", "standard"), 1),
            kv[0],
        ),
    ):
        test = tests_lookup.get(tid) or {}
        names = test.get("names") or {}
        name = names.get("ukrainian") or names.get("preferred") or tid
        priority = test.get("priority_class") or "standard"
        category = test.get("category") or "—"
        # If required by every track → "all"; else list which tracks
        all_track_ids = {t.track_id for t in plan.tracks}
        if use["required_by"] == all_track_ids:
            scope = "усі треки"
        elif use["required_by"]:
            scope = ", ".join(sorted(use["required_by"]))
        else:
            scope = "бажано (" + ", ".join(sorted(use["desired_by"])) + ")"
        priority_badge = (
            f'<span class="badge {_PRIORITY_BADGE_CLS.get(priority, "badge--optional")}">'
            f'{_h(_PRIORITY_LABEL_UA.get(priority, priority))}</span>'
        )
        rows.append(
            f'<tr><td>{_h(tid)}</td><td>{_h(name)}</td>'
            f'<td>{priority_badge}</td>'
            f'<td>{_h(category)}</td><td>{_h(scope)}</td></tr>'
        )

    return (
        '<section>'
        '<h2>Pre-treatment investigations</h2>'
        '<div class="section-sub">Дослідження перед стартом терапії · '
        'критичні / стандарт / бажано · поєднані по треках</div>'
        '<table class="tbl">'
        '<thead><tr><th>ID</th><th>Назва</th><th>Пріоритет</th>'
        '<th>Категорія</th><th>Потрібно для</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        '</table>'
        '</section>'
    )


def _render_branch_explanation(
    plan_result, kb_resolved: dict, target_lang: str = "uk"
) -> str:
    """Surface the actually-fired RedFlags from the engine trace.

    For each step that resolved a branch (`outcome=True` and `result` set),
    list the RFs that fired in that step and which one won the conflict-
    resolution tiebreak (`winner_red_flag` set by walk_algorithm in P2).

    This is the "Why this branch was chosen" answer — distinct from the
    PRO/CONTRA section above, which lists *possible* triggers. This one
    lists what actually drove the chosen branch on this specific patient.
    """
    rf_lookup = (kb_resolved or {}).get("red_flags") or {}
    src_lookup = (kb_resolved or {}).get("sources") or {}
    trace = getattr(plan_result, "trace", None) or []

    explained_steps: list[str] = []
    for step in trace:
        fired = step.get("fired_red_flags") or []
        if not fired:
            continue
        winner = step.get("winner_red_flag")
        branch = step.get("branch") or {}
        step_id = step.get("step")
        result_target = branch.get("result") or branch.get("next_step")

        rf_items: list[str] = []
        for rid in fired:
            rf = rf_lookup.get(rid) or {}
            defn = (
                rf.get("definition_ua")
                if target_lang == "uk" and rf.get("definition_ua")
                else rf.get("definition") or "—"
            )
            srcs = rf.get("sources") or []
            src_chips = "".join(
                f'<span class="src-chip">{_h(sid)}</span>'
                for sid in srcs
            )
            winner_mark = (
                ' <span class="rf-winner-tag">★ winner</span>'
                if rid == winner else ""
            )
            rf_items.append(
                f'<li><strong>{_h(rid)}</strong>{winner_mark}: '
                f'{_h(defn)} {src_chips}</li>'
            )

        head = (
            f"Step {step_id} → branch <code>{_h(str(result_target))}</code>"
            if result_target
            else f"Step {step_id}"
        )
        explained_steps.append(
            f'<div class="branch-step">'
            f'<div class="branch-step-head">{head}</div>'
            f'<ul>{"".join(rf_items)}</ul>'
            f'</div>'
        )

    if not explained_steps:
        return ""

    title = "Чому обрано саме цей трек" if target_lang == "uk" else "Why this branch was chosen"
    sub = (
        "Тригери з профілю пацієнта, що активувалися та визначили вибір."
        if target_lang == "uk"
        else "Triggers from the patient profile that fired and drove the chosen branch."
    )
    return (
        '<section class="branch-explanation">'
        f'<h2>{title}</h2>'
        f'<div class="section-sub">{sub}</div>'
        f'{"".join(explained_steps)}'
        '</section>'
    )


def _render_red_flags_pro_contra(plan, kb_resolved: dict, target_lang: str = "uk") -> str:
    """RedFlag PRO/CONTRA categorization for the aggressive escalation:

    - PRO-AGGRESSIVE: red flags that, when present, push the engine toward
      the aggressive track. Source: indication.red_flags_triggering_alternative
      on the STANDARD track + algorithm.decision_tree any_of red_flag clauses
      that resolve to the aggressive indication.
    - CONTRA-AGGRESSIVE: hard contraindications attached to the AGGRESSIVE
      track's indication / regimen — reasons NOT to escalate.

    Per REFERENCE_CASE_SPECIFICATION §3.8.
    """
    rf_lookup = (kb_resolved or {}).get("red_flags") or {}
    if not plan.tracks:
        return ""

    # PRO: union of red_flags_triggering_alternative across non-aggressive tracks
    pro_ids: set[str] = set()
    for t in plan.tracks:
        if t.track_id == "aggressive":
            continue
        ind = t.indication_data or {}
        pro_ids.update(ind.get("red_flags_triggering_alternative") or [])
    # Also pick up red flags from algorithm decision tree pointing to aggressive
    algo = (kb_resolved or {}).get("algorithm") or {}
    aggr_ind_ids = {
        t.indication_id for t in plan.tracks if t.track_id == "aggressive"
    }
    for step in algo.get("decision_tree") or []:
        if_true = (step.get("if_true") or {}).get("result")
        if if_true in aggr_ind_ids:
            ev = step.get("evaluate") or {}
            for clause in (ev.get("any_of") or []) + (ev.get("all_of") or []):
                if isinstance(clause, dict) and clause.get("red_flag"):
                    pro_ids.add(clause["red_flag"])

    # CONTRA: hard contraindications on aggressive track
    contra_items: list[dict] = []
    for t in plan.tracks:
        if t.track_id != "aggressive":
            continue
        for c in t.contraindications_data or []:
            contra_items.append(c)

    if not pro_ids and not contra_items:
        return ""

    def _rf_li(rid: str) -> str:
        rf = rf_lookup.get(rid) or {}
        # Prefer the bilingual EN field if target_lang=en — saves a translate
        # call when curator already provided an English definition. Fall back
        # to translating the UA field if only UA is present.
        if target_lang == "en" and rf.get("definition"):
            defn = rf["definition"]
            return f'<li>{_h(defn)}<span class="rf-id">{_h(rid)}</span></li>'
        defn = rf.get("definition_ua") or rf.get("definition") or "—"
        return f'<li>{_h_t(defn, target_lang)}<span class="rf-id">{_h(rid)}</span></li>'

    def _ci_li(c: dict) -> str:
        cid = c.get("id", "?")
        if target_lang == "en" and c.get("description"):
            descr = c["description"]
            return f'<li>{_h(descr)}<span class="rf-id">{_h(cid)}</span></li>'
        descr = c.get("description_ua") or c.get("description") or "—"
        return f'<li>{_h_t(descr, target_lang)}<span class="rf-id">{_h(cid)}</span></li>'

    pro_html = (
        '<div class="pc-col pc-col--pro">'
        '<h3>PRO-AGGRESSIVE</h3>'
        '<div class="section-sub">Тригери що штовхають до агресивного треку</div>'
        f'<ul>{"".join(_rf_li(r) for r in sorted(pro_ids)) or "<li>—</li>"}</ul>'
        '</div>'
    )
    contra_html = (
        '<div class="pc-col pc-col--contra">'
        '<h3>CONTRA-AGGRESSIVE</h3>'
        '<div class="section-sub">Жорсткі протипоказання до ескалації</div>'
        f'<ul>{"".join(_ci_li(c) for c in contra_items) or "<li>—</li>"}</ul>'
        '</div>'
    )
    return (
        '<section>'
        '<h2>Red flags — PRO / CONTRA aggressive</h2>'
        f'<div class="pro-contra">{pro_html}{contra_html}</div>'
        '</section>'
    )


def _render_what_not_to_do(plan, target_lang: str = "uk") -> str:
    """Explicitly prohibitive 'do_not_do' list per track.
    Per REFERENCE_CASE_SPECIFICATION §1.3 critical.

    Each bullet is UA free-text from Indication.do_not_do — translated
    via the configured client when target_lang != source."""
    blocks = []
    for t in plan.tracks:
        ind = t.indication_data or {}
        items = ind.get("do_not_do") or []
        if not items:
            continue
        li = "".join(f"<li>{_h_t(x, target_lang)}</li>" for x in items)
        blocks.append(
            '<div class="do-not">'
            f'<div class="track-name">{_h(t.label)} ({_h(t.indication_id)})</div>'
            f'<ul>{li}</ul>'
            '</div>'
        )
    if not blocks:
        return ""
    return (
        '<section>'
        '<h2>Що НЕ робити</h2>'
        '<div class="section-sub">Прямі прохібітивні правила, кожне з обґрунтуванням у regimen / supportive care / contraindication</div>'
        f'{"".join(blocks)}'
        '</section>'
    )


def _render_monitoring_phases(plan) -> str:
    """Monitoring schedule phases as a per-track table.
    Per REFERENCE_CASE_SPECIFICATION §1.3 critical."""
    blocks = []
    seen_monitoring_ids: set[str] = set()
    for t in plan.tracks:
        mon = t.monitoring_data
        if not mon:
            continue
        mid = mon.get("id") or ""
        if mid in seen_monitoring_ids:
            continue  # dedupe — both tracks may share the same monitoring schedule
        seen_monitoring_ids.add(mid)
        phases = mon.get("phases") or []
        if not phases:
            continue
        rows = []
        for ph in phases:
            tests = ", ".join(ph.get("tests") or []) or "—"
            checks = ph.get("checkpoints") or []
            checks_html = (
                "<ul style='padding-left:16px;margin:0;'>"
                + "".join(f"<li>{_h(c)}</li>" for c in checks)
                + "</ul>"
            ) if checks else "—"
            rows.append(
                f'<tr><td><strong>{_h(ph.get("name", "?"))}</strong></td>'
                f'<td>{_h(ph.get("window", "—"))}</td>'
                f'<td style="font-family:var(--font-mono);font-size:11px;">{_h(tests)}</td>'
                f'<td>{checks_html}</td></tr>'
            )
        blocks.append(
            f'<h3>{_h(t.label)} · {_h(mid)}</h3>'
            '<table class="tbl">'
            '<thead><tr><th>Фаза</th><th>Вікно</th>'
            '<th>Тести</th><th>Контрольні точки</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody>'
            '</table>'
        )
    if not blocks:
        return ""
    return (
        '<section>'
        '<h2>Monitoring schedule</h2>'
        '<div class="section-sub">Графік моніторингу за фазами лікування</div>'
        f'{"".join(blocks)}'
        '</section>'
    )


def _render_timeline(plan) -> str:
    """Horizontal timeline strip composed from Regimen.cycle_length_days +
    total_cycles + MonitoringSchedule.phases. CSS-only, no SVG/JS.
    Per REFERENCE_CASE_SPECIFICATION §1.3 should-have."""
    if not plan.tracks:
        return ""

    blocks = []
    seen: set[tuple] = set()
    for t in plan.tracks:
        reg = t.regimen_data or {}
        mon = t.monitoring_data or {}
        key = (reg.get("id"), mon.get("id"))
        if key in seen or key == (None, None):
            continue
        seen.add(key)

        phases_html: list[str] = []

        # Baseline phase from monitoring (always first if present)
        mon_phases = mon.get("phases") or []
        baseline = next((p for p in mon_phases if p.get("name") == "baseline"), None)
        if baseline:
            phases_html.append(
                '<div class="tl-phase tl-phase--baseline">'
                '<div class="name">Baseline</div>'
                f'<div class="window">{_h(baseline.get("window", "—"))}</div>'
                '</div>'
            )

        # Induction phase from regimen cycle metadata
        cycle_len = reg.get("cycle_length_days")
        total_cycles = reg.get("total_cycles") or "—"
        if cycle_len:
            cycles_str = str(total_cycles).strip()
            window = (
                f"{cycle_len}-day cycles × {cycles_str}"
                if cycles_str and cycles_str != "—"
                else f"{cycle_len}-day cycles"
            )
            phases_html.append(
                '<div class="tl-phase tl-phase--induction">'
                f'<div class="name">Induction · {_h(reg.get("name", "—")[:30])}</div>'
                f'<div class="window">{_h(window)}</div>'
                '</div>'
            )

        # Response assessment phase from monitoring
        ra = next((p for p in mon_phases if "response" in (p.get("name", "").lower())), None)
        if ra:
            phases_html.append(
                '<div class="tl-phase tl-phase--response">'
                '<div class="name">Response assessment</div>'
                f'<div class="window">{_h(ra.get("window", "—"))}</div>'
                '</div>'
            )

        # Maintenance phase if present
        maint = next((p for p in mon_phases if "maint" in (p.get("name", "").lower())), None)
        if maint:
            phases_html.append(
                '<div class="tl-phase tl-phase--maintenance">'
                '<div class="name">Maintenance</div>'
                f'<div class="window">{_h(maint.get("window", "—"))}</div>'
                '</div>'
            )

        # Follow-up phase if present
        fu = next(
            (p for p in mon_phases if "follow" in (p.get("name", "").lower())),
            None,
        )
        if fu:
            phases_html.append(
                '<div class="tl-phase tl-phase--followup">'
                '<div class="name">Follow-up</div>'
                f'<div class="window">{_h(fu.get("window", "—"))}</div>'
                '</div>'
            )

        if phases_html:
            blocks.append(
                f'<h3>{_h(t.label)}</h3>'
                f'<div class="timeline">{"".join(phases_html)}</div>'
            )

    if not blocks:
        return ""
    return (
        '<section>'
        '<h2>Timeline</h2>'
        '<div class="section-sub">Хронологія лікування — derived from regimen + monitoring schedule</div>'
        f'{"".join(blocks)}'
        '</section>'
    )


# ── Experimental-options track (Phase C) ─────────────────────────────────


def _render_experimental_options(option) -> str:
    """Render the clinical-trial track surfaced after engine selection.

    `option` is an `ExperimentalOption` (or None when no `search_fn` was
    wired). Output is render-time-only metadata — engine never reads
    these fields back (CHARTER §8.3 + plan §3.2 invariant).

    When option is None: emit a small placeholder so clinicians know the
    track exists but ctgov sync hasn't run. When option is present but
    has zero open trials, emit an empty-state message instead of a table.
    """

    if option is None:
        return (
            '<section class="experimental-track experimental-track--unset">'
            '<h2>Експериментальні опції (клінічні дослідження)</h2>'
            '<div class="section-sub">Третій трек плану — open-enrollment trials з ClinicalTrials.gov.</div>'
            '<p class="empty-state">'
            '🔬 Дані недоступні — синхронізація з ClinicalTrials.gov не виконана. '
            'Передайте <code>experimental_search_fn</code> у <code>generate_plan()</code> '
            'або синхронізуйте офлайн (per ua-ingestion plan §3.3).'
            '</p>'
            '</section>'
        )

    trials = option.trials or []
    last_synced = option.last_synced or ""

    if not trials:
        msg = option.notes or "Жодного активного трайла для цього сценарію в ctgov не знайдено."
        return (
            '<section class="experimental-track experimental-track--empty">'
            '<h2>Експериментальні опції (клінічні дослідження)</h2>'
            f'<div class="section-sub">Останнє оновлення: {_h(last_synced)} · ctgov.</div>'
            f'<p class="empty-state">{_h(msg)}</p>'
            '</section>'
        )

    rows = []
    for t in trials:
        ua_badge = ""
        if t.sites_ua:
            ua_badge = '<span class="badge badge--ua" title="Site present in Ukraine">UA</span>'
        elig = t.inclusion_summary or ""
        elig_short = (elig[:140] + "…") if len(elig) > 140 else elig
        rows.append(
            "<tr>"
            f'<td class="trial-nct"><a href="https://clinicaltrials.gov/study/{_h(t.nct_id)}" '
            f'target="_blank" rel="noopener">{_h(t.nct_id)}</a></td>'
            f'<td class="trial-title">{_h(t.title)}</td>'
            f'<td class="trial-phase">{_h(t.phase or "—")}</td>'
            f'<td class="trial-status">{_h(t.status)}</td>'
            f'<td class="trial-sponsor">{_h(t.sponsor or "—")}</td>'
            f'<td class="trial-ua">{ua_badge or "—"}</td>'
            f'<td class="trial-elig">{_h(elig_short)}</td>'
            "</tr>"
        )

    return (
        '<section class="experimental-track">'
        '<h2>Експериментальні опції (клінічні дослідження)</h2>'
        '<div class="section-sub">'
        f'Третій трек плану — open-enrollment trials з ClinicalTrials.gov. '
        f'Останнє оновлення: {_h(last_synced)}. '
        f'<em>Render-time metadata; engine selection не змінюється цим блоком (CHARTER §8.3).</em>'
        '</div>'
        '<table class="trials-table">'
        '<thead><tr>'
        '<th>NCT</th><th>Назва</th><th>Фаза</th><th>Статус</th>'
        '<th>Спонсор</th><th>UA</th><th>Включення (фрагмент)</th>'
        '</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        '</table>'
        '<p class="trial-disclaimer">'
        'Перевіряти статус набору безпосередньо у дослідницькому центрі. '
        'Дані ctgov можуть відставати від поточного статусу UA-сайтів.'
        '</p>'
        '</section>'
    )


# ── Access Matrix (Phase D) ──────────────────────────────────────────────


def _fmt_uah_range(lo, hi, per_unit) -> str:
    """Format `(min, max)` UAH cost range as a short readable string.
    Returns "—" when both bounds are absent (no cost data on any
    component). The `per_unit` suffix is appended in plain text."""
    if lo is None and hi is None:
        return "—"
    suffix = f"/{_h(per_unit)}" if per_unit else ""
    if lo is not None and hi is not None and lo != hi:
        return f"₴{int(lo):,}–{int(hi):,}{suffix}".replace(",", " ")
    val = lo if lo is not None else hi
    return f"₴{int(val):,}{suffix}".replace(",", " ")


def _avail_badge(value, *, true_label: str, false_label: str) -> str:
    """Tri-state status cell — True/False/None each render distinctly so
    the matrix never silently coalesces 'unknown' into 'no'."""
    if value is True:
        return f'<span class="badge badge--ok">✓ {_h(true_label)}</span>'
    if value is False:
        return f'<span class="badge badge--no">✗ {_h(false_label)}</span>'
    return '<span class="badge badge--unknown">— невідомо</span>'


def _render_access_matrix(matrix) -> str:
    """Render the per-Plan Access Matrix block (ua-ingestion plan §4).

    The matrix surfaces UA-availability metadata — registered, reimbursed,
    cost orientation, primary access pathway — for every track presented
    in the Plan, including any clinical-trial rows from the experimental
    track. Render-only; the engine never reads any field on `matrix`
    back as a selection signal (CHARTER §8.3, plan §0 invariant).

    Default-collapsed via <details>; auto-expanded when at least one row
    indicates a non-reimbursed component (so clinicians see the funding
    gap without an extra click). `matrix is None` (older Plans, or
    aggregator failure) renders nothing — the section is opt-in.
    """
    if matrix is None or not matrix.rows:
        return ""

    # Auto-expand when any track has non-reimbursed component or stale cost
    auto_open = any(
        (r.reimbursed_nszu is False) or r.cost_is_stale or (r.registered_in_ua is False)
        for r in matrix.rows
    )
    open_attr = " open" if auto_open else ""

    rows_html: list[str] = []
    for r in matrix.rows:
        track_class = "track-trial" if r.track_id.startswith("trial:") else f"track-{_h(r.track_id)}"
        regimen_label = _h(r.regimen_name or r.regimen_id or "—")
        if r.regimen_name and r.regimen_id:
            regimen_label = f"<strong>{_h(r.regimen_name)}</strong> <span class='regimen-id'>({_h(r.regimen_id)})</span>"

        cost_cell_parts: list[str] = []
        # Reimbursed bucket first (НСЗУ tariff), self-pay second (retail)
        reimb_cell = _fmt_uah_range(r.cost_reimbursed_min, r.cost_reimbursed_max, r.cost_per_unit)
        if reimb_cell != "—":
            cost_cell_parts.append(f"<div class='cost-row'><span class='cost-label'>НСЗУ:</span> {reimb_cell}</div>")
        sp_cell = _fmt_uah_range(r.cost_self_pay_min, r.cost_self_pay_max, r.cost_per_unit)
        if sp_cell != "—":
            cost_cell_parts.append(f"<div class='cost-row'><span class='cost-label'>self-pay:</span> {sp_cell}</div>")
        if not cost_cell_parts:
            if r.track_id.startswith("trial:"):
                cost_cell_parts.append("<span class='cost-trial'>0 для пацієнта (sponsor pays)</span>")
            else:
                cost_cell_parts.append("<span class='cost-unknown'>₴-? — verify pathway</span>")

        # Pathway cell
        if r.primary_pathway_id:
            path_cell = f'<a href="#path-{_h(r.primary_pathway_id)}">{_h(r.primary_pathway_id)}</a>'
            if r.pathway_alternative_ids:
                path_cell += f' <span class="alt-paths">(+{len(r.pathway_alternative_ids)})</span>'
        elif r.track_id.startswith("trial:"):
            path_cell = "Trial sponsor"
        elif r.reimbursed_nszu:
            path_cell = "НСЗУ formulary"
        else:
            path_cell = "<em>not recorded</em>"

        # Notes cell — collapse to one line, full list on hover
        notes_cell = ""
        if r.notes:
            head = r.notes[0]
            tail = ""
            if len(r.notes) > 1:
                tail_attr = _h(" · ".join(r.notes[1:]))
                tail = f' <span class="more-notes" title="{tail_attr}">+{len(r.notes) - 1}</span>'
            cls = "notes-stale" if r.cost_is_stale else "notes"
            notes_cell = f'<div class="{cls}">{_h(head)}{tail}</div>'

        rows_html.append(
            f'<tr class="{track_class}">'
            f'<td class="track-cell"><strong>{_h(r.track_label)}</strong>'
            f'<div class="regimen-name">{regimen_label}</div>{notes_cell}</td>'
            f'<td>{_avail_badge(r.registered_in_ua, true_label="зареєстровано", false_label="не зареєстровано")}</td>'
            f'<td>{_avail_badge(r.reimbursed_nszu, true_label="покривається", false_label="out-of-pocket")}</td>'
            f'<td class="cost-cell">{"".join(cost_cell_parts)}</td>'
            f'<td class="pathway-cell">{path_cell}</td>'
            f'</tr>'
        )

    plan_notes = ""
    if matrix.notes:
        items = "".join(f"<li>{_h(n)}</li>" for n in matrix.notes)
        plan_notes = f'<ul class="matrix-plan-notes">{items}</ul>'

    return (
        f'<section class="access-matrix">'
        f'<details{open_attr}>'
        f'<summary><h2>Доступність опцій в Україні</h2>'
        f'<span class="section-sub">Per-track UA registration · НСЗУ · cost · access pathway. '
        f'Render-time metadata; engine selection не залежить від цих полів (CHARTER §8.3).</span></summary>'
        f'{plan_notes}'
        f'<table class="access-matrix-table">'
        f'<thead><tr>'
        f'<th>Опція</th><th>Реєстрація UA</th><th>НСЗУ</th>'
        f'<th>Cost orientation</th><th>Access pathway</th>'
        f'</tr></thead>'
        f'<tbody>{"".join(rows_html)}</tbody>'
        f'</table>'
        f'<p class="matrix-disclaimer">'
        f'Інформація про ціни — orientation. Перевіряти у конкретній аптеці / foundation / трайл-сайті. '
        f'Status updated: {_h((matrix.generated_at or "")[:10])}.'
        f'</p>'
        f'</details>'
        f'</section>'
    )


# ── NSZU availability badges (per-drug) ─────────────────────────────────


_NSZU_DRUGS_LABEL = {
    "uk": "Препарати + НСЗУ",
    "en": "Drugs + NSZU",
}


def _render_nszu_badge(drug_entity, patient_disease_id, disease_names, target_lang="uk") -> str:
    """One drug → one `<span class="nszu-badge nszu-{status}">…</span>`.

    `drug_entity` is the dict-shape Drug record from the loader. When
    None (e.g. a drug_id referenced by a regimen but not present in the
    KB), renders an explicit `not-registered` badge so the row never
    silently drops a component."""
    badge = lookup_nszu_status(
        drug_entity or {},
        patient_disease_id,
        disease_names=disease_names,
    )
    cls = f"nszu-badge nszu-{badge.status}"
    label = nszu_label(badge.status, target_lang)
    tip = badge.notes_excerpt or badge.indication_match or ""
    title_attr = f' title="{_h(tip)}"' if tip else ""
    return f'<span class="{cls}"{title_attr}>{_h(label)}</span>'


def _render_track_drug_list(
    track,
    drugs_lookup: dict,
    patient_disease_id: str,
    disease_names: dict,
    target_lang: str = "uk",
) -> str:
    """Render the regimen's drug components as a `<dt>/<dd>` block with
    an NSZU availability badge per drug. Returns empty string when the
    track has no regimen / no components — keeps the dl tidy."""
    reg = track.regimen_data or {}
    components = reg.get("components") or []
    if not components:
        return ""
    rows: list[str] = []
    for comp in components:
        if not isinstance(comp, dict):
            continue
        drug_id = comp.get("drug_id")
        if not drug_id:
            continue
        drug = drugs_lookup.get(drug_id)
        # Drug display name — prefer ukrainian when rendering UA, else preferred
        names = (drug or {}).get("names") or {}
        if (target_lang or "uk").lower().startswith("en"):
            name = names.get("english") or names.get("preferred") or drug_id
        else:
            name = names.get("ukrainian") or names.get("preferred") or drug_id
        dose_bits: list[str] = []
        for k in ("dose", "schedule", "route"):
            v = comp.get(k)
            if v:
                dose_bits.append(str(v))
        dose_str = " · ".join(dose_bits)
        nszu = _render_nszu_badge(drug, patient_disease_id, disease_names, target_lang)
        meta = (
            f'<span class="drug-name">{_h(name)}</span>'
            f' <span class="drug-id">({_h(drug_id)})</span>'
        )
        if dose_str:
            meta += f' <span class="drug-dose">{_h(dose_str)}</span>'
        rows.append(f'<li class="drug-row">{meta} {nszu}</li>')
    if not rows:
        return ""
    label = _NSZU_DRUGS_LABEL.get(
        "en" if (target_lang or "uk").lower().startswith("en") else "uk",
        _NSZU_DRUGS_LABEL["uk"],
    )
    return f'<dt>{_h(label)}</dt><dd><ul class="drug-list">{"".join(rows)}</ul></dd>'


# ── Variant actionability (ESCAT / OncoKB) ──────────────────────────────


def _escat_class(tier: Optional[str]) -> str:
    """ESCAT tier → CSS class. Falls back to escat-X for unknown values."""
    if not tier:
        return "escat-X"
    valid = {"IA", "IB", "IIA", "IIB", "IIIA", "IIIB", "IV", "X"}
    t = str(tier).strip().upper()
    return f"escat-{t}" if t in valid else "escat-X"


def _oncokb_class(level: Optional[str]) -> str:
    """OncoKB level → CSS class. Falls back to oncokb-4 for unknown values."""
    if not level:
        return "oncokb-4"
    valid = {"1", "2", "3A", "3B", "4", "R1", "R2"}
    raw = str(level).strip().upper()
    return f"oncokb-{raw}" if raw in valid else "oncokb-4"


def _render_variant_actionability(plan, target_lang: str = "uk") -> str:
    """Render the ESCAT / OncoKB tier-badges section.

    Inserted between the diagnostic profile (patient strip + etiological
    driver) and the treatment-plan tracks. When the patient has no
    matching BMA cells, render a single placeholder row — the section
    is always present so HCPs see that the lookup ran.
    """
    hits = list(getattr(plan, "variant_actionability", None) or [])

    th = (
        "<thead><tr>"
        f"<th>{_h(_t('actionability_th_biomarker', target_lang))}</th>"
        f"<th>{_h(_t('actionability_th_variant', target_lang))}</th>"
        f"<th>{_h(_t('actionability_th_escat', target_lang))}</th>"
        f"<th>{_h(_t('actionability_th_oncokb', target_lang))}</th>"
        f"<th>{_h(_t('actionability_th_action', target_lang))}</th>"
        f"<th>{_h(_t('actionability_th_combos', target_lang))}</th>"
        f"<th>{_h(_t('actionability_th_sources', target_lang))}</th>"
        "</tr></thead>"
    )

    rows: list[str] = []
    if not hits:
        rows.append(
            f'<tr class="empty-row"><td colspan="7">'
            f'{_h(_t("actionability_empty", target_lang))}'
            f'</td></tr>'
        )
    else:
        for h in hits:
            biomarker = _h(h.biomarker_id or "")
            qualifier = h.variant_qualifier
            variant_cell = (
                _h(qualifier)
                if qualifier
                else f'<span style="color:var(--gray-500)">{_h(_t("actionability_gene_level", target_lang))}</span>'
            )
            escat_cls = _escat_class(h.escat_tier)
            oncokb_cls = _oncokb_class(h.oncokb_level)
            escat_label = _h(h.escat_tier or "X")
            oncokb_label = _h(h.oncokb_level or "4")
            summary = _h_t(h.evidence_summary or "", target_lang)
            combos = (
                "<br>".join(_h(c) for c in (h.recommended_combinations or []))
                or '<span style="color:var(--gray-500)">—</span>'
            )
            sources = (
                "".join(f"<li>{_h(s)}</li>" for s in (h.primary_sources or []))
                or '<li style="color:var(--gray-500)">—</li>'
            )
            rows.append(
                "<tr>"
                f'<td><span class="gene">{biomarker}</span></td>'
                f'<td><span class="variant">{variant_cell}</span></td>'
                f'<td><span class="tier-badge {escat_cls}">{escat_label}</span></td>'
                f'<td><span class="tier-badge {oncokb_cls}">{oncokb_label}</span></td>'
                f'<td class="summary">{summary}</td>'
                f'<td class="combos">{combos}</td>'
                f'<td><ul class="src-list">{sources}</ul></td>'
                "</tr>"
            )

    return (
        '<section class="variant-actionability">'
        f'<h2>{_h(_t("actionability_heading", target_lang))}</h2>'
        f'<div class="section-sub">{_h(_t("actionability_sub", target_lang))}</div>'
        f'<table class="actionability-table">{th}<tbody>{"".join(rows)}</tbody></table>'
        '</section>'
    )


# ── Treatment Plan render ─────────────────────────────────────────────────


def render_plan_html(
    plan_result: PlanResult,
    mdt: Optional[MDTOrchestrationResult] = None,
    *,
    target_lang: str = "uk",
    mode: str = "clinician",
) -> str:
    """Render a PlanResult as a single-file HTML document.

    `mode="clinician"` (default) emits the full tumor-board brief with
    technical IDs, ESCAT tiers, MDT block, FDA disclosure, etc.

    `mode="patient"` emits a stripped-down plain-Ukrainian patient-facing
    bundle: technical IDs (BMA-*, ALGO-*, BIO-*, IND-*, REG-*, RF-*) are
    removed from user-visible text and replaced with vocabulary lookups
    from `_patient_vocabulary`. Emergency RedFlags surface as a banner
    via `_emergency_rf`; an 'ask your doctor' section is generated via
    `_ask_doctor`. CHARTER §8.3 invariant — patient-mode never changes
    the engine's track selection."""
    if (mode or "").lower() == "patient":
        return _render_patient_mode(plan_result, target_lang)

    plan = plan_result.plan
    if plan is None:
        return _doc_shell("OpenOnco — empty plan", "<p>Empty PlanResult; nothing to render.</p>")

    fda = plan.fda_compliance

    # Header
    body: list[str] = []
    body.append(
        '<div class="doc-header">'
        '<div class="doc-label">OpenOnco · Treatment Plan</div>'
        f'<div class="doc-title">План лікування — {_h(plan_result.disease_id)}</div>'
        f'<div class="doc-sub">{_h(plan.id)} · v{_h(plan.version)} · {_h(plan.generated_at[:10])}</div>'
        '</div>'
    )

    # Patient strip
    body.append(
        '<div class="patient-strip">'
        '<div class="label">Patient</div>'
        f'<div class="value">{_h(plan.patient_id)} · Algorithm: {_h(plan_result.algorithm_id)}</div>'
        '</div>'
    )

    # Etiological driver — only for etiologically_driven archetype
    body.append(_render_etiological_driver(
        (plan_result.kb_resolved or {}).get("disease")
    ))

    # Variant actionability (ESCAT / OncoKB) — inserted between the
    # diagnostic profile and the treatment-plan tracks. Render-time
    # context only; engine never re-reads tier values to rank tracks.
    body.append(_render_variant_actionability(plan, target_lang))

    # Tracks
    drugs_lookup = (plan_result.kb_resolved or {}).get("drugs") or {}
    disease_data = (plan_result.kb_resolved or {}).get("disease") or {}
    disease_names = (disease_data.get("names") if isinstance(disease_data, dict) else None) or {}
    track_html = []
    for t in plan.tracks:
        track_class = f"track track--{(t.track_id or 'standard')}"
        if t.is_default:
            badge = '<span class="track-default-badge">★ DEFAULT</span>'
        else:
            badge = ""
        regimen_str = (t.regimen_data or {}).get("name", "—") if t.regimen_data else "—"
        sup = (
            f'<dt>Supportive care</dt><dd>{_h(", ".join(s.get("id", "?") for s in t.supportive_care_data))}</dd>'
            if t.supportive_care_data else ""
        )
        ci = (
            f'<dt>Hard contraindications</dt><dd>{_h(", ".join(c.get("id", "?") for c in t.contraindications_data))}</dd>'
            if t.contraindications_data else ""
        )
        # Drug components with NSZU availability badges (render-time only;
        # engine never reads these — same contract as ESCAT/OncoKB tiers).
        drugs_dd = _render_track_drug_list(
            t, drugs_lookup, plan_result.disease_id or "", disease_names, target_lang
        )
        signoff_badge = _render_signoff_badge(t.indication_data)
        track_html.append(
            f'<div class="{track_class}">'
            f'<div class="track-head"><div class="track-name">{_h(t.label)}</div>{badge}</div>'
            f'<div class="track-signoff">{signoff_badge}</div>'
            f'<dl>'
            f'<dt>Indication</dt><dd>{_h(t.indication_id)}</dd>'
            f'<dt>Regimen</dt><dd>{_h(regimen_str)}</dd>'
            f'{drugs_dd}'
            f'{sup}'
            f'{ci}'
            f'<dt>Reason</dt><dd>{_h(t.selection_reason)}</dd>'
            f'</dl>'
            f'</div>'
        )
    body.append(
        f'<section><h2>Treatment options ({len(plan.tracks)} tracks)</h2>'
        f'<div class="tracks">{"".join(track_html)}</div></section>'
    )

    # Why this branch was chosen — actual fired RFs from the trace,
    # with the conflict-resolution winner tagged. Distinct from the
    # PRO/CONTRA section, which lists possible triggers in the abstract.
    body.append(_render_branch_explanation(plan_result, plan_result.kb_resolved, target_lang))

    # Pre-treatment investigations · RedFlag PRO/CONTRA · What NOT to do ·
    # Monitoring phases · Timeline (REFERENCE_CASE_SPECIFICATION §1.3)
    body.append(_render_pretreatment_investigations(plan, plan_result.kb_resolved))
    body.append(_render_red_flags_pro_contra(plan, plan_result.kb_resolved, target_lang))
    body.append(_render_what_not_to_do(plan, target_lang))

    # Phase 4: OncoKB precision-medicine layer (HCP-only; surface-only).
    # Per safe-rollout v3 §4.1: section sits AFTER tracks + supportive-care,
    # BEFORE monitoring. CHARTER §8.3 invariant — engine never reads this.
    # Phase 4.1: pass kb_resolved.drugs so the render layer can source FDA-
    # approval truth from our Drug entities (OncoKB doesn't carry fdaApproved
    # on treatments[] — see oncokb_api_evidence.md A3-bis).
    oncokb_layer = getattr(plan_result, "oncokb_layer", None)
    if oncokb_layer is not None:
        try:
            from .render_oncokb import render_oncokb_section
            body.append(render_oncokb_section(
                oncokb_layer,
                mode="clinician",
                target_lang=target_lang,
                drugs_lookup=(plan_result.kb_resolved or {}).get("drugs"),
            ))
        except Exception as exc:
            # Fail-open: missing oncokb section is preferable to a broken plan
            body.append(f"<!-- oncokb section error: {exc} -->")

    body.append(_render_monitoring_phases(plan))
    body.append(_render_timeline(plan))

    # MDT brief inline
    body.append(_render_mdt_section(mdt, target_lang))

    # Sources
    if fda.data_sources_summary:
        items = "".join(f"<li>{_h(s)}</li>" for s in fda.data_sources_summary)
        body.append(f"<section><h2>Sources cited</h2><ul class='sources'>{items}</ul></section>")

    # Experimental options (Phase C — clinical-trial track)
    body.append(_render_experimental_options(plan_result.experimental_options))

    # Access Matrix (Phase D — UA-availability per track)
    body.append(_render_access_matrix(plan.access_matrix))

    # Footer
    body.append('<div class="doc-footer">')
    body.append(_render_version_chain(
        plan.id, plan.version, plan.supersedes, plan.superseded_by, plan.generated_at,
    ))
    body.append(_render_fda_disclosure(fda.intended_use))
    if fda.automation_bias_warning:
        body.append(_render_fda_disclosure(fda.automation_bias_warning))
    body.append(f'<div class="medical-disclaimer">{_h(_MEDICAL_DISCLAIMER)}</div>')
    body.append('</div>')

    out = _doc_shell(f"План лікування — {plan_result.disease_id}", "".join(body))
    return _localize_html(out, target_lang)


# ── Patient-mode render ───────────────────────────────────────────────────
#
# Plain-Ukrainian patient-facing bundle. Technical entity IDs (BMA-*,
# ALGO-*, BIO-*, IND-*, REG-*, RF-*) are NEVER rendered as visible text
# in patient mode (they may appear in HTML attributes for testing /
# debugging, e.g. `data-bma-id="..."`, but never in `<p>` / `<li>` /
# `<td>` content). All clinician-vocabulary terms route through
# `_patient_vocabulary.explain()`.


def _patient_doc_shell(title: str, body: str) -> str:
    """Patient-mode HTML shell — embeds STYLESHEET + PATIENT_MODE_CSS so
    the bundle is a single self-contained document. Distinct from
    `_doc_shell` because patient mode wraps the body in
    `<div class="patient-report">` rather than `<div class="page">` and
    doesn't ship the Google Fonts <link> (patient bundles favour system
    fonts for offline-readability)."""
    return (
        "<!DOCTYPE html>\n"
        '<html lang="uk">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"<title>{_h(title)}</title>\n"
        f"<style>{_CSS}{_PATIENT_CSS}</style>\n"
        "</head>\n<body>\n"
        f'<div class="patient-report">{body}</div>\n'
        "</body>\n</html>\n"
    )


def _patient_disease_label(plan_result: PlanResult) -> str:
    """Plain-UA disease label, never the DIS- ID. Falls back to a generic
    label so user-visible text never contains a technical ID."""
    disease_data = (plan_result.kb_resolved or {}).get("disease") or {}
    names = disease_data.get("names") if isinstance(disease_data, dict) else None
    if isinstance(names, dict):
        for key in ("ukrainian", "preferred", "english"):
            v = names.get(key)
            if v:
                return str(v)
    return "ваш діагноз"


def _patient_drug_label(drug_dict: dict, drug_id: str) -> str:
    """Plain-UA drug label, never the DRUG- ID."""
    if isinstance(drug_dict, dict):
        names = drug_dict.get("names") or {}
        if isinstance(names, dict):
            for key in ("ukrainian", "preferred", "english"):
                v = names.get(key)
                if v:
                    return str(v)
        nm = drug_dict.get("name")
        if nm:
            return str(nm)
    # Last-resort fallback: humanize the ID. We deliberately strip the
    # `DRUG-` prefix so no raw entity ID leaks into rendered text.
    raw = (drug_id or "").strip()
    if raw.upper().startswith("DRUG-"):
        raw = raw[5:]
    return raw.replace("-", " ").replace("_", " ").lower() or "препарат"


def _render_findings_plain(plan_result: PlanResult) -> str:
    """Plain-UA rendering of the variant_actionability hits.

    Each hit becomes a friendly statement: 'У вас знайдено [variant
    explanation]. Це означає: [ESCAT tier patient label].' Technical
    IDs (BMA-*, BIO-*) are stripped — only gene + variant fragment
    survive (e.g. "BRAF V600E"), which is patient-facing biology, not
    a KB ID."""
    plan = plan_result.plan
    hits = list((plan and plan.variant_actionability) or [])
    if not hits:
        return (
            '<p>За результатами наявних аналізів значущих молекулярних мішеней '
            "поки не виявлено. Це не означає, що лікування неможливе — стандартна терапія "
            "залишається повністю чинною. Якщо у вас ще не було молекулярного тестування "
            "пухлини, обговоріть це з лікарем.</p>"
        )

    parts: list[str] = ['<ul class="findings-list">']
    for h in hits:
        # Strip BIO- prefix from the biomarker label — keep only gene-name
        # fragment (BRAF, EGFR, etc.) which is patient-readable biology,
        # not an internal KB ID.
        bio = (h.biomarker_id or "").strip()
        gene = bio[4:].split("-", 1)[0] if bio.upper().startswith("BIO-") else bio.split("-", 1)[0]
        variant = (h.variant_qualifier or "").strip() or ""
        # Variant explanation from vocabulary (e.g. V600E → "конкретна
        # заміна валіну на глутамат…"). Falls back to the literal variant
        # string when vocabulary has no entry.
        v_expl = _explain_patient(variant) or _explain_patient(gene) or ""
        tier = (h.escat_tier or "").strip().upper()
        tier_label = ESCAT_TIER_PATIENT_LABEL.get(tier, "")
        # Compose a short human paragraph. We render gene + variant
        # together (e.g. "BRAF V600E") because that's biology a patient
        # can search for; ESCAT tier is wrapped in a friendly label.
        gene_variant = f"{gene} {variant}".strip() if variant else gene
        bits = [f"<li><strong>{_h(gene_variant)}</strong>"]
        if v_expl:
            bits.append(f" — {_h(v_expl)}")
        if tier_label:
            bits.append(f'. <span class="patient-badge patient-info">{_h(tier_label)}</span>')
        else:
            bits.append(".")
        bits.append("</li>")
        parts.append("".join(bits))
    parts.append("</ul>")
    return "".join(parts)


def _render_drugs_plain(plan_result: PlanResult) -> str:
    """Plain-UA rendering of recommended drugs across all tracks.

    Each drug renders as a `<div class="drug-explanation">` block with
    drug name + lay-language explanation (`drug.notes_patient` if
    present, else `_explain_patient(drug.drug_class)`, else a generic
    fallback) + NSZU patient badge."""
    plan = plan_result.plan
    if plan is None or not plan.tracks:
        return (
            "<p>Конкретний список препаратів буде сформовано лікарем "
            "після перегляду усіх ваших аналізів.</p>"
        )

    drugs_lookup = (plan_result.kb_resolved or {}).get("drugs") or {}
    disease_data = (plan_result.kb_resolved or {}).get("disease") or {}
    disease_names = disease_data.get("names") if isinstance(disease_data, dict) else None
    seen_drug_ids: set[str] = set()
    blocks: list[str] = []

    for t in plan.tracks:
        regimen = t.regimen_data or {}
        components = regimen.get("components") or []
        for comp in components:
            if not isinstance(comp, dict):
                continue
            drug_id = comp.get("drug_id") or ""
            if not drug_id or drug_id in seen_drug_ids:
                continue
            seen_drug_ids.add(drug_id)

            drug = drugs_lookup.get(drug_id) or {}
            label = _patient_drug_label(drug, drug_id)
            drug_class = (drug.get("drug_class") or "") if isinstance(drug, dict) else ""

            # Lay-language explanation: prefer notes_patient (drug-author'd
            # patient-facing blurb) → drug_class vocabulary entry → generic.
            lay = ""
            if isinstance(drug, dict):
                lay = (drug.get("notes_patient") or "").strip()
            if not lay and drug_class:
                lay = _explain_patient(drug_class) or ""
            if not lay:
                lay = "препарат для лікування вашого захворювання — деталі обговоріть з лікарем"

            # NSZU badge — patient-friendly label, render only when we can
            # resolve coverage. Falls back silently when drug entity is
            # missing (don't fabricate a badge).
            badge_html = ""
            if isinstance(drug, dict) and drug:
                try:
                    badge = lookup_nszu_status(
                        drug,
                        plan_result.disease_id or "",
                        disease_names=disease_names if isinstance(disease_names, dict) else None,
                    )
                    p_label = NSZU_PATIENT_LABEL.get(badge.status, "")
                    if p_label:
                        cls = f"patient-nszu patient-nszu-{badge.status}"
                        badge_html = (
                            f'<div class="{cls}" data-nszu-status="{_h(badge.status)}">'
                            f"{_h(p_label)}</div>"
                        )
                except Exception:
                    badge_html = ""

            blocks.append(
                '<div class="drug-explanation">'
                f"<h3>{_h(label)}</h3>"
                f'<p class="lay-language">{_h(lay)}</p>'
                f"{badge_html}"
                "</div>"
            )

    if not blocks:
        return (
            "<p>Конкретний список препаратів буде сформовано лікарем "
            "після перегляду усіх ваших аналізів.</p>"
        )
    return "".join(blocks)


def _render_emergency_section(plan_result: PlanResult) -> str:
    """Filter the plan's red flags and render emergency-tier ones as a
    `<section class="emergency-signals">` with one banner item per RF.
    Renders an empty-state placeholder when no emergency RFs apply, so
    the section is always present in the bundle (assertable structural
    contract for downstream tests)."""
    rf_lookup = (plan_result.kb_resolved or {}).get("red_flags") or {}
    emergencies = filter_emergency_rfs(list(rf_lookup.values()))
    if not emergencies:
        return (
            '<section class="emergency-signals">'
            "<h2>Сигнали, що вимагають негайної уваги</h2>"
            '<p class="patient-badge patient-good">'
            "Наразі немає термінових сигналів — продовжуйте планові візити."
            "</p>"
            "</section>"
        )
    items: list[str] = []
    for rf in emergencies:
        # data-rf-id keeps the engine ID accessible to debug tooling /
        # tests, but the visible text is generated solely from the
        # patient_emergency_label() output.
        rf_id = (rf.get("id") or "") if isinstance(rf, dict) else ""
        label = patient_emergency_label(rf)
        items.append(
            f'<li data-rf-id="{_h(rf_id)}">{_h(label)}</li>'
        )
    return (
        '<section class="emergency-signals">'
        "<h2>Сигнали, що вимагають негайної уваги</h2>"
        '<p>Якщо у вас з\'явилися ці симптоми — зверніться у лікарню '
        "негайно, не чекайте планового візиту:</p>"
        f'<ul class="emergency-list">{"".join(items)}</ul>'
        "</section>"
    )


def _render_ask_doctor_section(plan_result: PlanResult) -> str:
    """Build the 'про що варто запитати лікаря' block.

    Pulls a plan dict (model_dump) and decorates it with derived flags
    that the predicates in `_ask_doctor.py` look for (recommended_drugs,
    plan_tracks, etc.). The decoration keeps the predicates simple
    while still surfacing oop-drug / multi-track / germline-variant
    contingent questions."""
    plan = plan_result.plan
    plan_dict: dict = plan.model_dump() if plan is not None else {}

    # Decorate with the derived fields the predicates expect. We don't
    # mutate the persisted Plan — `model_dump()` returns a fresh dict.
    drugs_lookup = (plan_result.kb_resolved or {}).get("drugs") or {}
    disease_data = (plan_result.kb_resolved or {}).get("disease") or {}
    disease_names = disease_data.get("names") if isinstance(disease_data, dict) else None

    recommended: list[dict] = []
    seen: set[str] = set()
    if plan is not None:
        for t in plan.tracks:
            regimen = t.regimen_data or {}
            for comp in regimen.get("components") or []:
                if not isinstance(comp, dict):
                    continue
                did = comp.get("drug_id") or ""
                if not did or did in seen:
                    continue
                seen.add(did)
                drug = drugs_lookup.get(did) or {}
                nszu_status: str = ""
                if isinstance(drug, dict) and drug:
                    try:
                        b = lookup_nszu_status(
                            drug,
                            plan_result.disease_id or "",
                            disease_names=disease_names if isinstance(disease_names, dict) else None,
                        )
                        nszu_status = b.status
                    except Exception:
                        nszu_status = ""
                recommended.append({
                    "drug_id": did,
                    "name": _patient_drug_label(drug, did),
                    "drug_class": (drug.get("drug_class") if isinstance(drug, dict) else None),
                    "nszu_status": nszu_status,
                })

    plan_dict["recommended_drugs"] = recommended
    plan_dict["plan_tracks"] = list(plan_dict.get("tracks") or [])

    questions = _select_ask_doctor_questions(plan_dict, target_count=6)
    if not questions:
        return ""
    items = "".join(f"<li>{_h(q['question_ua'])}</li>" for q in questions)
    return (
        '<div class="ask-doctor">'
        "<h2>Про що варто запитати лікаря</h2>"
        f"<ul>{items}</ul>"
        "</div>"
    )


_PATIENT_DISCLAIMER_HTML = (
    "<p>Цей звіт — інформаційний інструмент, не медичний прилад. Усі рішення "
    "про лікування приймає ваш онколог. Звіт оновлюється, коли з'являються "
    "нові аналізи. Не змінюйте призначене лікування на основі лише цього звіту.</p>"
    "<p>Якщо у вас виникли термінові симптоми, перелічені вище — звертайтесь у "
    "лікарню негайно, не чекайте планового візиту.</p>"
    "<p>Питання про сам інструмент: "
    '<a href="https://github.com/romeo111/OpenOnco/issues">github.com/romeo111/OpenOnco</a></p>'
)


def _render_patient_mode(plan_result: PlanResult, target_lang: str) -> str:
    """Render a Plan as a plain-Ukrainian patient-facing single-file HTML.

    `target_lang` is currently honoured only for the document `<html lang>`
    attribute — the body stays Ukrainian per the patient-mode spec. EN
    patient bundles are out of scope for the current iteration (see
    CSD-3 plan)."""
    plan = plan_result.plan
    if plan is None:
        return _patient_doc_shell(
            "Ваш персональний онкологічний план",
            '<p>Поки що недостатньо даних для побудови плану. '
            'Зверніться до вашого онколога для уточнення.</p>',
        )

    disease_label = _patient_disease_label(plan_result)
    body_parts: list[str] = []

    # Header
    body_parts.append(
        "<header>"
        "<h1>Ваш персональний план</h1>"
        '<p class="patient-subhead">Що показав аналіз і що це означає для вас</p>'
        f'<p><strong>Діагноз:</strong> {_h(disease_label)}</p>'
        "</header>"
    )

    body_parts.append(
        '<section class="what-was-found">'
        "<h2>Що знайдено в результаті</h2>"
        f"{_render_findings_plain(plan_result)}"
        "</section>"
    )

    # Sign-off badge for the default track's Indication (patient-mode).
    # Surfaces clinician-review status in plain UA so the patient sees
    # whether the plan has been verified by a physician (CHARTER §6.1).
    default_track = next(
        (t for t in (plan.tracks or []) if getattr(t, "is_default", False)),
        (plan.tracks[0] if plan.tracks else None),
    )
    signoff_html_patient = (
        _render_signoff_badge_patient(getattr(default_track, "indication_data", None))
        if default_track else ""
    )
    body_parts.append(
        '<section class="what-now">'
        "<h2>Що це означає для лікування</h2>"
        f'{("<p>" + signoff_html_patient + "</p>") if signoff_html_patient else ""}'
        f"{_render_drugs_plain(plan_result)}"
        "</section>"
    )

    body_parts.append(_render_emergency_section(plan_result))
    body_parts.append(_render_ask_doctor_section(plan_result))

    body_parts.append(
        f'<footer class="patient-disclaimer">{_PATIENT_DISCLAIMER_HTML}</footer>'
    )

    return _patient_doc_shell(
        "Ваш персональний онкологічний план",
        "".join(body_parts),
    )


# ── Diagnostic Brief render ───────────────────────────────────────────────


def render_diagnostic_brief_html(
    diag_result: DiagnosticPlanResult,
    mdt: Optional[MDTOrchestrationResult] = None,
    *,
    target_lang: str = "uk",
) -> str:
    dp = diag_result.diagnostic_plan
    if dp is None:
        return _doc_shell("OpenOnco — empty diagnostic brief", "<p>Empty DiagnosticPlanResult.</p>")

    body: list[str] = []

    # Header
    body.append(
        '<div class="doc-header">'
        '<div class="doc-label">OpenOnco · Workup Brief · DIAGNOSTIC PHASE</div>'
        '<div class="doc-title">Brief підготовки до тумор-борду</div>'
        f'<div class="doc-sub">{_h(dp.id)} · v{_h(dp.version)} · {_h(dp.generated_at[:10])}</div>'
        '</div>'
    )

    # MANDATORY diagnostic banner (CHARTER §15.2 C7)
    body.append(
        '<div class="banner banner--diagnostic">'
        '<strong>⚠ DIAGNOSTIC PHASE — TREATMENT PLAN NOT YET APPLICABLE</strong>'
        f'{_h(_DIAGNOSTIC_BANNER)}'
        '</div>'
    )

    # Patient + suspicion strip
    susp = diag_result.suspicion or dp.suspicion_snapshot
    susp_html = ""
    if susp:
        tissues = ", ".join(susp.tissue_locations) if susp.tissue_locations else "—"
        hyps = ", ".join(susp.working_hypotheses) if susp.working_hypotheses else "—"
        susp_html = (
            '<div class="patient-strip">'
            '<div class="label">Patient</div>'
            f'<div class="value">{_h(dp.patient_id)} · suspicion lineage: {_h(susp.lineage_hint)}</div>'
            f'<div class="value" style="margin-top:6px;font-size:13px;color:var(--gray-700);">'
            f'Tissues: {_h(tissues)} · Hypotheses: {_h(hyps)}</div>'
        )
        if susp.presentation:
            susp_html += f'<div class="value" style="margin-top:6px;font-size:13px;color:var(--gray-700);">{_h(susp.presentation)}</div>'
        susp_html += "</div>"
    body.append(susp_html)

    # Matched workup
    body.append(
        f'<div class="banner banner--info">'
        f'<strong>Matched workup:</strong> {_h(diag_result.matched_workup_id)} · '
        f'<strong>Очікуваний термін:</strong> ~{_h(dp.expected_timeline_days)} днів'
        '</div>'
    )

    # Workup steps
    steps_html = []
    for s in dp.workup_steps:
        cat_badge = f'<span class="badge badge--{_h(s.category)}">{_h(s.category)}</span> '
        descr = s.description or s.test_id or "?"
        rationale = (
            f'<div class="step-rationale">{_h(s.rationale)}</div>' if s.rationale else ""
        )
        biopsy = ""
        if s.biopsy_approach:
            biopsy = (
                f'<div class="step-rationale" style="margin-top:6px;">'
                f'<strong>Biopsy preferred:</strong> {_h(s.biopsy_approach.preferred)}'
                f'</div>'
            )
        ihc = ""
        if s.ihc_panel and s.ihc_panel.baseline:
            ihc = (
                f'<div class="step-rationale" style="margin-top:4px;">'
                f'<strong>IHC baseline:</strong> {_h(", ".join(s.ihc_panel.baseline))}'
                f'</div>'
            )
        steps_html.append(
            f'<li>'
            f'<span class="step-num">{_h(s.step)}</span>'
            f'<span class="step-name">{cat_badge}{_h(descr)}</span>'
            f'{rationale}'
            f'{biopsy}'
            f'{ihc}'
            f'</li>'
        )
    body.append(
        f'<section><h2>Workup steps ({len(dp.workup_steps)})</h2>'
        f'<ul class="steps">{"".join(steps_html)}</ul></section>'
    )

    # Mandatory questions
    if dp.mandatory_questions:
        items = "".join(f"<li>{_h(q)}</li>" for q in dp.mandatory_questions)
        body.append(
            f'<section><h2>Питання що мають бути закриті ({len(dp.mandatory_questions)})</h2>'
            f'<ul style="padding-left:20px;font-size:14px;line-height:1.7;color:var(--gray-700);">{items}</ul></section>'
        )

    # MDT brief
    body.append(_render_mdt_section(mdt, target_lang))

    # Footer
    body.append('<div class="doc-footer">')
    body.append(_render_version_chain(
        dp.id, dp.version, dp.supersedes, dp.superseded_by, dp.generated_at,
    ))
    body.append(_render_fda_disclosure(dp.intended_use))
    body.append(_render_fda_disclosure(dp.automation_bias_warning))
    body.append(f'<div class="medical-disclaimer">{_h(_MEDICAL_DISCLAIMER)}</div>')
    body.append('</div>')

    out = _doc_shell("OpenOnco · Workup Brief", "".join(body))
    return _localize_html(out, target_lang)


# ── Revision Note render ──────────────────────────────────────────────────


def render_revision_note_html(
    previous: Union[PlanResult, DiagnosticPlanResult],
    new_result: Union[PlanResult, DiagnosticPlanResult],
    transition: str,
    mdt: Optional[MDTOrchestrationResult] = None,
    *,
    target_lang: str = "uk",
) -> str:
    """Renders a revision note: shows transition + prev/new IDs, then
    renders the new result inline (so reviewer sees the latest state)."""

    prev_id = (
        previous.diagnostic_plan.id if isinstance(previous, DiagnosticPlanResult)
        and previous.diagnostic_plan
        else (previous.plan.id if isinstance(previous, PlanResult) and previous.plan else "?")
    )
    new_id = (
        new_result.diagnostic_plan.id if isinstance(new_result, DiagnosticPlanResult)
        and new_result.diagnostic_plan
        else (new_result.plan.id if isinstance(new_result, PlanResult) and new_result.plan else "?")
    )
    new_trigger = ""
    if isinstance(new_result, PlanResult) and new_result.plan:
        new_trigger = new_result.plan.revision_trigger or ""
    elif isinstance(new_result, DiagnosticPlanResult) and new_result.diagnostic_plan:
        new_trigger = new_result.diagnostic_plan.revision_trigger or ""

    body: list[str] = []
    body.append(
        '<div class="doc-header">'
        '<div class="doc-label">OpenOnco · Revision Note</div>'
        '<div class="doc-title">Перегляд плану</div>'
        f'<div class="doc-sub">Transition: {_h(transition)} · {_h(_now_iso())}</div>'
        '</div>'
    )

    body.append(
        '<div class="banner banner--info">'
        f'<strong>Previous:</strong> {_h(prev_id)} → <strong>New:</strong> {_h(new_id)}<br>'
        f'<strong>Trigger:</strong> {_h(new_trigger or "(not specified)")}'
        '</div>'
    )

    # Inline render of the NEW result (delegate). The inner render handles
    # localization itself; here we render in UA and let the outer wrap
    # localize the entire revision-note HTML in one pass.
    if isinstance(new_result, DiagnosticPlanResult):
        inner = render_diagnostic_brief_html(new_result, mdt=mdt, target_lang="uk")
    else:
        inner = render_plan_html(new_result, mdt=mdt, target_lang="uk")
    start = inner.find('<div class="page">')
    end = inner.rfind('</div>\n</body>')
    if start >= 0 and end >= 0:
        body.append(inner[start + len('<div class="page">'):end])
    else:
        body.append(inner)

    out = _doc_shell("OpenOnco · Revision Note", "".join(body))
    return _localize_html(out, target_lang)


# ── Polymorphic dispatch ──────────────────────────────────────────────────


def render(
    result: Union[PlanResult, DiagnosticPlanResult],
    mdt: Optional[MDTOrchestrationResult] = None,
    *,
    target_lang: str = "uk",
) -> str:
    """Auto-dispatch by result type."""
    if isinstance(result, DiagnosticPlanResult):
        return render_diagnostic_brief_html(result, mdt=mdt, target_lang=target_lang)
    return render_plan_html(result, mdt=mdt, target_lang=target_lang)


__all__ = [
    "render",
    "render_diagnostic_brief_html",
    "render_plan_html",
    "render_revision_note_html",
]
