"""Build per-track plain-UA rationale bullets from `PlanResult.trace`.

Render-time only. Engine MUST NOT consult these bullets as a treatment-
selection signal (CHARTER §8.3 invariant — same contract as
`_patient_vocabulary.py`, `_emergency_rf.py`, `_ask_doctor.py`).

The track-selection happens in `algorithm_eval.walk_algorithm`, which
records each fired clause + RedFlag in `PlanResult.trace`. This module
re-reads that trace and composes 2-4 plain-UA bullets per track that
explain to the patient why this branch was reached. Sources of bullets:

  1. **Variant actionability** — when the plan has a strong-tier
     biomarker hit (ESCAT IA/IB), surface it as a "бо у вас знайдено
     {gene} {variant}" line. This is the primary biomarker-driven
     rationale.
  2. **Fired RedFlags** — for each RF whose `id` appears in the trace,
     surface the first sentence of `definition_ua` (already plain UA per
     REDFLAG_AUTHORING_GUIDE).
  3. **Track-default fallback** — when no biomarker / RF rationale is
     available, surface a generic "стандарт для вашого діагнозу" line.
  4. **Track-alternative fallback** — when alternative track has no
     specific reason in trace, surface a "це альтернативний варіант,
     обговорити з лікарем" line.

Cap: ≤4 bullets per track. Empty rationale → fallback line.

CHARTER §8.3 boundary: this module reads `trace`, `red_flags`,
`variant_actionability`. It does NOT vote on track selection. The
renderer surfaces whatever bullets this module produces; the engine has
already chosen the tracks and ordered them.
"""

from __future__ import annotations

import html
from typing import Any


# Strong-tier ESCAT labels — these get a more confident bullet wording
# ("найвищий рівень доказів") than mid-tier hits.
_STRONG_TIERS: frozenset[str] = frozenset({"IA", "IB"})
_MID_TIERS: frozenset[str] = frozenset({"IIA", "IIB"})

_REVIEW_PENDING_EN = "Clinical review of this biomarker record is pending. "
_REVIEW_PENDING_UK = "Клінічна перевірка цього запису біомаркера ще не завершена. "


_FALLBACK_DEFAULT_UA = (
    "Цей варіант рекомендовано як стандарт для вашого діагнозу на "
    "основі клінічних рекомендацій."
)
_FALLBACK_ALTERNATIVE_UA = (
    "Це альтернативний варіант — обговоріть з лікарем, чи підходить "
    "він для вас."
)
_FALLBACK_NO_TRACE_UA = (
    "Цей варіант запропоновано на основі стандартів клінічних "
    "рекомендацій для вашого діагнозу. Деталі — у технічній версії звіту."
)

_FALLBACK_DEFAULT_EN = (
    "This option is recommended as a standard for your diagnosis based on clinical guidelines."
)
_FALLBACK_ALTERNATIVE_EN = (
    "This is an alternative option. Discuss with your doctor whether it is suitable for you."
)
_FALLBACK_NO_TRACE_EN = (
    "This option is proposed based on clinical guidelines for your diagnosis. "
    "See the technical report for details."
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


def build_track_rationale(plan_result: Any, track: Any, *, target_lang: str = "uk") -> list[str]:
    """Return up to 4 plain-UA rationale bullets for one track.

    Inputs:
      * `plan_result` — duck-typed `PlanResult`. Reads `.plan`,
        `.kb_resolved`, `.trace` (and tolerates absences).
      * `track` — a `PlanTrack` (or duck-typed equivalent). Reads
        `.is_default`, `.indication_data`, `.regimen_data`.

    Output: list of plain-UA strings (≤4 bullets). When no signal is
    available, returns a single-element list with the
    `_FALLBACK_NO_TRACE_UA` line so the renderer always has something
    to display.

    Order of consideration (each adds at most one bullet, capped at 4):

      1. Strong-tier biomarker hit (ESCAT IA/IB) — biomarker-driven
         tracks usually anchor on this.
      2. Default-track stable-state line — when the track is default and
         no aggressive RF fired.
      3. Up to 2 fired-RF lines — pulled from `_first_sentence_ua` of
         `definition_ua`.
      4. Alternative-track fallback — when the track is alternative and
         no other rationale fits.

    The function is tolerant of partial state: missing `kb_resolved`,
    empty `trace`, `None` indication_data — all fall through to the
    appropriate fallback. The renderer should ALWAYS get a non-empty
    list back."""
    plan = getattr(plan_result, "plan", None)
    english = target_lang == "en"
    bullets: list[str] = []
    is_default = bool(getattr(track, "is_default", False))

    # ── 1. Strong-tier biomarker hit ────────────────────────────────
    hits = []
    if plan is not None:
        hits = list(getattr(plan, "variant_actionability", None) or [])
    strong_hit = next((h for h in hits if _hit_tier(h) in _STRONG_TIERS), None)
    if strong_hit is None:
        strong_hit = next((h for h in hits if _hit_tier(h) in _MID_TIERS), None)
    if strong_hit is not None:
        label = _gene_variant_label(strong_hit)
        tier = _hit_tier(strong_hit)
        if label:
            ready = (strong_hit.get("clinical_use_ready", False)
                     if isinstance(strong_hit, dict)
                     else getattr(strong_hit, "clinical_use_ready", False))
            if not ready:
                bullets.append(
                    (_REVIEW_PENDING_EN + f"The report records {label} with evidence tier {tier}. "
                     "This unreviewed record does not establish that this treatment is appropriate for you."
                     if english else _REVIEW_PENDING_UK + f"У звіті записано {label} з рівнем доказів {tier}. "
                     "Неперевірений запис не підтверджує, що це лікування підходить саме вам.")
                )
            elif tier in _STRONG_TIERS:
                bullets.append(
                    (f"Because {label} was found, it provides strong evidence for choosing this treatment."
                     if english else f"Бо у вас знайдено {label} — це сильний доказовий "
                     f"маркер для вибору саме цього лікування.")
                )
            else:
                bullets.append(
                    (f"Because {label} was found, there is moderate evidence in favour of this option."
                     if english else f"Бо у вас знайдено {label} — є помірні докази на "
                     f"користь цього варіанту.")
                )

    # ── 2. Default-track stable-state line ──────────────────────────
    fired_rf_ids = _fired_rf_ids_from_trace(
        getattr(plan_result, "trace", None)
    )
    if is_default and not fired_rf_ids and len(bullets) < 4:
        bullets.append(
            "The algorithm proposed the standard option; no red flags were recorded as triggered in its trace. "
            "This does not rule out risks or replace assessment by your doctor."
            if english else
            "Алгоритм запропонував стандартний варіант; у його журналі немає спрацьованих сигналів-тривоги. "
            "Це не виключає ризиків і не замінює оцінки лікаря."
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

    # ── 4. Alternative-track fallback ───────────────────────────────
    if not is_default and len(bullets) == 0:
        bullets.append(_FALLBACK_ALTERNATIVE_EN if english else _FALLBACK_ALTERNATIVE_UA)
    elif not bullets:
        bullets.append(_FALLBACK_DEFAULT_EN if english else _FALLBACK_DEFAULT_UA)

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
        pending_prefix = _REVIEW_PENDING_EN if target_lang == "en" else _REVIEW_PENDING_UK
        if bullet.startswith(pending_prefix):
            content = (f'<span class="translation-fallback" data-biomarker-review="pending">'
                       f'{html.escape(pending_prefix.strip())}</span> '
                       + html.escape(bullet[len(pending_prefix):]))
        items.append(f'<li>{content}</li>')
    return f'<ul>{"".join(items)}</ul>'


__all__ = [
    "build_track_rationale",
    "build_track_rationale_html",
]
