"""Patient explanations from recorded algorithm paths.

Render-time only; never an input to treatment selection (CHARTER §8.3).
Plan-wide biomarker records are informational context outside track
explanations. A track receives fired-signal context only when the final
recorded algorithm result identifies that exact indication. Missing or
unlinked paths remain explicitly unassessed. The clinical plan is immutable.
"""

from __future__ import annotations

import html
from typing import Any


# Evidence tiers used to summarize report-wide findings, never selection.
_STRONG_TIERS: frozenset[str] = frozenset({"IA", "IB"})
_MID_TIERS: frozenset[str] = frozenset({"IIA", "IIB"})

_REVIEW_PENDING_EN = "Clinical review of this biomarker record is pending. "
_REVIEW_PENDING_UK = "Клінічна перевірка цього запису біомаркера ще не завершена. "


_FALLBACK_NO_TRACE_UA = (
    "У звіті не записано обґрунтування цього варіанта. Попросіть лікаря перевірити технічний звіт."
)

_FALLBACK_NO_TRACE_EN = (
    "The report does not record an explanation for this option. Ask your doctor to review the technical report."
)
RATIONALE_TRANSLATION_STATUS = {"en": "draft_pending_review"}


def _first_sentence_ua(text: str) -> str:
    """Return the first sentence of `text` (split on `. `), trimmed.

    Falls back to the full text when no period is found. Keeps any
    closing punctuation off the result so the renderer can append its
    own period."""
    if not text:
        return ""
    s = text.strip()
    cut = s.split(". ", 1)[0].strip()
    # Strip a trailing period since the renderer template appends one.
    return cut.rstrip(".").strip()


def _strip_bio_prefix(biomarker_id: str) -> str:
    """Strip a leading `BIO-` from a biomarker ID and split on the first
    `-` so the gene fragment (e.g. `BRAF` from `BIO-BRAF-MUTATION`) is
    returned as the patient-readable label."""
    if not biomarker_id:
        return ""
    s = biomarker_id.strip()
    if s.upper().startswith("BIO-"):
        s = s[4:]
    return s.split("-", 1)[0]


def _gene_variant_label(hit: Any) -> str:
    """Compose a `BRAF V600E`-style label from a variant_actionability
    hit, falling back to the gene alone when no variant qualifier is
    present. Accepts either a Pydantic model or a dict."""
    bio = ""
    variant = ""
    if hasattr(hit, "biomarker_id"):
        bio = (getattr(hit, "biomarker_id", "") or "").strip()
        variant = (getattr(hit, "variant_qualifier", "") or "").strip()
    elif isinstance(hit, dict):
        bio = str(hit.get("biomarker_id", "") or "").strip()
        variant = str(hit.get("variant_qualifier", "") or "").strip()
    gene = _strip_bio_prefix(bio)
    if variant:
        return f"{gene} {variant}".strip()
    return gene


def _hit_tier(hit: Any) -> str:
    if hasattr(hit, "escat_tier"):
        return str(getattr(hit, "escat_tier", "") or "").strip().upper()
    if isinstance(hit, dict):
        return str(hit.get("escat_tier", "") or "").strip().upper()
    return ""


def _fired_rf_ids_from_trace(trace: Any) -> list[str]:
    """Collect unique fired RedFlag IDs from a `PlanResult.trace`,
    preserving the first-occurrence order so the bullet sequence is
    deterministic."""
    seen: set[str] = set()
    ordered: list[str] = []
    if not trace:
        return ordered
    for entry in trace:
        if not isinstance(entry, dict):
            continue
        for rf_id in entry.get("fired_red_flags") or []:
            if rf_id and rf_id not in seen:
                seen.add(rf_id)
                ordered.append(rf_id)
    return ordered


def _rf_definition_ua(rf_dict: Any) -> str:
    """Pull a clean first-sentence Ukrainian definition from a RedFlag
    dict. Falls back to English `definition` when `definition_ua` is
    absent (clinician text — patient still benefits from seeing the
    fired condition)."""
    if not isinstance(rf_dict, dict):
        return ""
    text = rf_dict.get("definition_ua") or rf_dict.get("definition") or ""
    return _first_sentence_ua(str(text))


def build_plan_findings_context(plan_result: Any, *, target_lang: str = "uk") -> list[str]:
    """Informational biomarker context, never a track-selection rationale."""
    plan = getattr(plan_result, "plan", None)
    hits = list(getattr(plan, "variant_actionability", None) or []) if plan else []
    hit = next((h for h in hits if _hit_tier(h) in _STRONG_TIERS), None)
    if hit is None:
        hit = next((h for h in hits if _hit_tier(h) in _MID_TIERS), None)
    if hit is None or not _gene_variant_label(hit):
        return []
    ready = hit.get("clinical_use_ready", False) if isinstance(hit, dict) else getattr(hit, "clinical_use_ready", False)
    label, tier = _gene_variant_label(hit), _hit_tier(hit)
    if target_lang == "en":
        return [("" if ready else _REVIEW_PENDING_EN)
                + f"The report records {label} with evidence tier {tier}."]
    return [("" if ready else _REVIEW_PENDING_UK)
            + f"У звіті записано {label} з рівнем доказів {tier}."]


def build_plan_findings_context_html(plan_result: Any, *, target_lang: str = "uk") -> str:
    bullets = build_plan_findings_context(plan_result, target_lang=target_lang)
    if not bullets:
        return ""
    heading = ("Report-wide finding — not a reason for selecting an option."
               if target_lang == "en" else "Загальна знахідка у звіті — не причина вибору окремого варіанта.")
    prefix = _REVIEW_PENDING_EN if target_lang == "en" else _REVIEW_PENDING_UK
    items = []
    for bullet in bullets:
        content = html.escape(bullet)
        if bullet.startswith(prefix):
            content = (f'<span class="translation-fallback" data-biomarker-review="pending">'
                       f'{html.escape(prefix.strip())}</span> ' + html.escape(bullet[len(prefix):]))
        items.append(f"<li>{content}</li>")
    return ('<div class="why-findings-context" data-rationale-scope="plan-findings">'
            f'<p>{html.escape(heading)}</p><ul>{"".join(items)}</ul></div>')


def build_plan_signal_context_html(plan_result: Any, *, target_lang: str = "uk") -> str:
    """Keep all recorded signal observations accessible outside track reasons.

    Retain original field text and its declared language. This is not a
    severity filter, a treatment-selection input or a clinical endorsement.
    """
    ids = _fired_rf_ids_from_trace(getattr(plan_result, "trace", None))
    if not ids:
        return ""
    resolved = getattr(plan_result, "kb_resolved", None) or {}
    lookup = resolved.get("red_flags", {}) if isinstance(resolved, dict) else {}
    english = target_lang == "en"
    heading = ("Signals recorded in this report — not reasons for selecting every option."
               if english else "Сигнали, записані у звіті, — не причини вибору кожного варіанта.")
    caption = "Recorded signal (original source text):" if english else "Записаний сигнал (оригінальний текст джерела):"
    missing = ("A signal was recorded, but its explanation is unavailable. See the technical report."
               if english else "Сигнал записано, але його пояснення недоступне. Дивіться технічний звіт.")
    items = []
    for rf_id in ids:
        record = lookup.get(rf_id) if isinstance(lookup, dict) else None
        text, language = "", "und"
        if isinstance(record, dict):
            fields = (("definition", "en"), ("definition_ua", "uk")) if english else (("definition_ua", "uk"), ("definition", "en"))
            for field, declared in fields:
                if record.get(field):
                    text, language = _first_sentence_ua(str(record[field])) + ".", declared
                    break
        content = (html.escape(caption) + " "
                   + f'<span lang="{language}" data-original-source>{html.escape(text)}</span>'
                   if text else html.escape(missing))
        items.append(f'<li data-source-id="{html.escape(str(rf_id), quote=True)}">{content}</li>')
    return ('<div class="why-signals-context" data-rationale-scope="plan-signals">'
            f'<p>{html.escape(heading)}</p><ul>{"".join(items)}</ul></div>')


def build_track_rationale(plan_result: Any, track: Any, *, target_lang: str = "uk") -> list[str]:
    """Return at most four escaped-later bullets for a recorded track path.

    No gene, evidence tier, default flag or medicine-name matching is used
    to infer selection. Legacy traces without a selected indication cannot
    substantiate a track-specific explanation.
    """
    english = target_lang == "en"
    bullets: list[str] = []

    # A plan-wide biomarker record is not evidence of why any track was
    # selected. It is rendered once, outside per-track explanations.
    trace = getattr(plan_result, "trace", None) or []
    indication_id = getattr(track, "indication_id", None)
    last = trace[-1] if isinstance(trace, list) and trace else None
    branch = last.get("branch") if isinstance(last, dict) else None
    selected = (branch.get("result") if isinstance(branch, dict) and "result" in branch
                else last.get("result") if isinstance(last, dict) else None)
    linked = bool(indication_id and selected == indication_id)
    if not linked:
        notice = ("This report does not record an algorithm path selecting this option. "
                  "Ask your doctor to review the technical report and its suitability for you."
                  if english else
                  "У цьому звіті не записано шлях алгоритму, що обрав цей варіант. "
                  "Попросіть лікаря перевірити технічний звіт і відповідність цього варіанта вашій ситуації.")
        return [notice]

    bullets.append(
        "The recorded algorithm path selected this option. This does not establish its suitability for you."
        if english else
        "Записаний шлях алгоритму обрав цей варіант. Це не підтверджує, що він підходить саме вам."
    )
    fired_rf_ids = _fired_rf_ids_from_trace(trace)
    if not fired_rf_ids:
        bullets.append(
            "No red flags were recorded as triggered on that path. This does not rule out risks or replace assessment by your doctor."
            if english else
            "На цьому шляху не записано спрацьованих сигналів-тривоги. Це не виключає ризиків і не замінює оцінки лікаря."
        )

    # ── 3. Fired-RF lines ───────────────────────────────────────────
    rf_lookup = {}
    kb_resolved = getattr(plan_result, "kb_resolved", None) or {}
    if isinstance(kb_resolved, dict):
        rf_lookup = kb_resolved.get("red_flags") or {}

    rf_lines_added = 0
    for rf_id in fired_rf_ids:
        if len(bullets) >= 4 or rf_lines_added >= 2:
            break
        rf_dict = rf_lookup.get(rf_id) if isinstance(rf_lookup, dict) else None
        text = _rf_definition_ua(rf_dict)
        original = False
        if english and isinstance(rf_dict, dict):
            translated = rf_dict.get("definition")
            if translated:
                text = _first_sentence_ua(str(translated))
            else:
                original = True
        if text:
            if english:
                qualifier = " (original Ukrainian text; translation unavailable)" if original else ""
                bullets.append(f"The algorithm recorded{qualifier}: {text}.")
            else:
                bullets.append(f"У вас зафіксовано: {text}.")
            rf_lines_added += 1

    return bullets[:4]


def build_track_rationale_html(plan_result: Any, track: Any, *, target_lang: str = "uk") -> str:
    """Render `build_track_rationale` output as a `<ul>` of `<li>`
    bullets. When the rationale is empty (defensive — should never
    happen), emits the no-trace fallback paragraph instead.

    HTML escapes each bullet so KB content with `<` / `&` / `"` cannot
    break the document or smuggle markup. Renderer composes this output
    directly into the patient bundle."""
    bullets = build_track_rationale(plan_result, track, target_lang=target_lang)
    if not bullets:
        fallback = _FALLBACK_NO_TRACE_EN if target_lang == "en" else _FALLBACK_NO_TRACE_UA
        return f'<p class="why-fallback">{html.escape(fallback)}</p>'
    items = []
    # This prefix is emitted only for a missing English definition and a
    # retained definition_ua field. It identifies provenance, not a language guess.
    original_prefix = 'The algorithm recorded (original Ukrainian text; translation unavailable): '
    for bullet in bullets:
        content = html.escape(bullet)
        if target_lang == 'en' and bullet.startswith(original_prefix):
            content = (html.escape(original_prefix)
                       + f'<span lang="uk" data-original-source>{html.escape(bullet[len(original_prefix):])}</span>')
        items.append(f'<li>{content}</li>')
    return f'<ul>{"".join(items)}</ul>'


__all__ = [
    "build_plan_findings_context",
    "build_plan_findings_context_html",
    "build_plan_signal_context_html",
    "build_track_rationale",
    "build_track_rationale_html",
]
