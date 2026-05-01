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


def build_track_rationale(plan_result: Any, track: Any) -> list[str]:
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
            if tier in _STRONG_TIERS:
                bullets.append(
                    f"Бо у вас знайдено {label} — це сильний доказовий "
                    f"маркер для вибору саме цього лікування."
                )
            else:
                bullets.append(
                    f"Бо у вас знайдено {label} — є помірні докази на "
                    f"користь цього варіанту."
                )

    # ── 2. Default-track stable-state line ──────────────────────────
    fired_rf_ids = _fired_rf_ids_from_trace(
        getattr(plan_result, "trace", None)
    )
    if is_default and not fired_rf_ids and len(bullets) < 4:
        bullets.append(
            "Стандартний варіант рекомендовано, бо немає сигналів "
            "(redflags), що вимагали б іншого підходу."
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
        if text:
            bullets.append(f"У вас зафіксовано: {text}.")
            rf_lines_added += 1

    # ── 4. Alternative-track fallback ───────────────────────────────
    if not is_default and len(bullets) == 0:
        bullets.append(_FALLBACK_ALTERNATIVE_UA)
    elif not bullets:
        bullets.append(_FALLBACK_DEFAULT_UA)

    return bullets[:4]


def build_track_rationale_html(plan_result: Any, track: Any) -> str:
    """Render `build_track_rationale` output as a `<ul>` of `<li>`
    bullets. When the rationale is empty (defensive — should never
    happen), emits the no-trace fallback paragraph instead.

    HTML escapes each bullet so KB content with `<` / `&` / `"` cannot
    break the document or smuggle markup. Renderer composes this output
    directly into the patient bundle."""
    bullets = build_track_rationale(plan_result, track)
    if not bullets:
        return f'<p class="why-fallback">{html.escape(_FALLBACK_NO_TRACE_UA)}</p>'
    items = "".join(f"<li>{html.escape(b)}</li>" for b in bullets)
    return f"<ul>{items}</ul>"


__all__ = [
    "build_track_rationale",
    "build_track_rationale_html",
]
