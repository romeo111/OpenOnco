"""Generate the 'what to ask your doctor' section for patient-mode rendering.

Render-time only. The engine MUST NOT consult these question templates
as a treatment-selection signal (CHARTER §8.3 invariant — same contract
as `_actionability.py`, `_nszu.py`, `_emergency_rf.py`). Tracks come
from the declarative Algorithm; this helper just decorates the rendered
patient bundle with 5-7 plain-UA questions that a layperson can take
into a clinic visit.

Each template is a triple of:

  * `id` — stable identifier (used by tests + the renderer's must-include set).
  * `predicate` — pure function over the plan dict; True when the question
    is relevant for this specific plan. Always-relevant questions return
    True unconditionally.
  * `question_ua` — the Ukrainian question text shown to the patient.

Selection order (in `select_questions`):

  1. Apply each predicate against the plan. Drop irrelevant templates.
  2. Always include the four 'must-have' questions when relevant
     (second_opinion, duration, side_effects, support).
  3. Fill remaining slots from the optional pool until `target_count`
     is reached.

The plan dict is duck-typed — predicates `.get(...)` everything and
default to safe values, so a partial plan (no recommended_drugs, no
variant_actionability, etc.) still produces the must-have core.
"""

from __future__ import annotations

from typing import Any, Callable, TypedDict


class QuestionTemplate(TypedDict):
    id: str
    predicate: Callable[[dict], bool]
    question_ua: str


def _drugs(plan: dict) -> list[dict]:
    return list(plan.get("recommended_drugs") or [])


def _variants(plan: dict) -> list[dict]:
    return list(plan.get("variant_actionability") or [])


def _has_oop_drug(plan: dict) -> bool:
    return any(
        (d.get("nszu_status") in ("oop", "not-registered"))
        for d in _drugs(plan)
    )


def _has_strict_oop_drug(plan: dict) -> bool:
    return any((d.get("nszu_status") == "oop") for d in _drugs(plan))


def _has_high_tox_drug(plan: dict) -> bool:
    return any(
        (d.get("drug_class") or d.get("class") or "").lower()
        in ("anthracycline", "platinum", "platinum agent", "alkylating", "alkylating agent")
        for d in _drugs(plan)
    )


def _has_basket_eligible_variant(plan: dict) -> bool:
    return any(
        str(va.get("escat_tier") or "").upper().startswith("III")
        for va in _variants(plan)
    )


def _patient_under_50(plan: dict) -> bool:
    age = plan.get("patient_age")
    if age is None:
        # Try to read from snapshot
        snap = plan.get("patient_snapshot") or {}
        demos = snap.get("demographics") or {}
        age = demos.get("age")
    try:
        return age is not None and int(age) < 50
    except (TypeError, ValueError):
        return False


def _has_germline_variant(plan: dict) -> bool:
    for va in _variants(plan):
        q = (va.get("variant_qualifier") or "").lower()
        if "germline" in q:
            return True
    return False


def _multiple_tracks(plan: dict) -> bool:
    return len(plan.get("plan_tracks") or plan.get("tracks") or []) > 1


# 11 question templates — author'd against the specs in
# specs/CLINICAL_CONTENT_STANDARDS.md §6 (patient-information leaflet
# tone) and the questions ESMO patient guides recommend asking before
# treatment start. Wording is Ukrainian, 8th-grade reading level.
QUESTION_TEMPLATES: list[QuestionTemplate] = [
    {
        "id": "second_opinion",
        "predicate": lambda plan: True,
        "question_ua": "Чи варто отримати другу думку молекулярного онколога перед початком лікування?",
    },
    {
        "id": "regional_access",
        "predicate": lambda plan: _has_oop_drug(plan),
        "question_ua": "Чи доступний цей препарат у моєму регіоні? Якщо ні — як можна його отримати?",
    },
    {
        "id": "duration",
        "predicate": lambda plan: True,
        "question_ua": "Скільки циклів триватиме лікування? Як ми зрозуміємо, що воно працює?",
    },
    {
        "id": "side_effects",
        "predicate": lambda plan: True,
        "question_ua": "Які побічні ефекти найбільш імовірні саме для мене? Які я можу запобігти?",
    },
    {
        "id": "dose_reduction",
        "predicate": lambda plan: _has_high_tox_drug(plan),
        "question_ua": "Чи можна почати з нижчої дози і поступово підвищувати?",
    },
    {
        "id": "trials",
        "predicate": lambda plan: _has_basket_eligible_variant(plan),
        "question_ua": "Чи є клінічні випробування, у яких я міг би взяти участь?",
    },
    {
        "id": "fertility",
        "predicate": lambda plan: _patient_under_50(plan),
        "question_ua": "Як це лікування вплине на мою фертильність? Чи треба заморозити репродуктивні клітини?",
    },
    {
        "id": "insurance",
        "predicate": lambda plan: _has_strict_oop_drug(plan),
        "question_ua": "Чи покриває моя страховка частину витрат? Чи є благодійні фонди для допомоги?",
    },
    {
        "id": "second_track",
        "predicate": lambda plan: _multiple_tracks(plan),
        "question_ua": "Чому ви рекомендуєте саме цей план, а не альтернативний?",
    },
    {
        "id": "support",
        "predicate": lambda plan: True,
        "question_ua": "Чи є групи підтримки або психолог для онкологічних пацієнтів, які я можу відвідувати?",
    },
    {
        "id": "family_screening",
        "predicate": lambda plan: _has_germline_variant(plan),
        "question_ua": "Якщо мутація успадкована (germline), чи треба перевірити моїх дітей/братів/сестер?",
    },
]


_MUST_INCLUDE_IDS = {"second_opinion", "duration", "side_effects", "support"}


def select_questions(plan: Any, target_count: int = 6) -> list[dict]:
    """Pick 5-7 plan-relevant questions for the patient bundle.

    `plan` may be a dict, a Pydantic Plan model, or any object exposing
    `.get(...)`. The four always-relevant 'must-have' questions are
    inserted first; remaining slots are filled from the disease/plan-
    contingent pool until `target_count` is reached.

    Returns a list of the underlying template dicts (caller renders the
    `question_ua` field)."""
    if plan is None:
        plan_dict: dict = {}
    elif isinstance(plan, dict):
        plan_dict = plan
    elif hasattr(plan, "model_dump"):
        plan_dict = plan.model_dump()
    elif hasattr(plan, "__dict__"):
        plan_dict = dict(plan.__dict__)
    else:
        plan_dict = {}

    relevant: list[QuestionTemplate] = []
    for q in QUESTION_TEMPLATES:
        try:
            if q["predicate"](plan_dict):
                relevant.append(q)
        except Exception:
            # Predicates are pure data lookups — but defensive against
            # unusual plan shapes (CSD-3-tests synthetic fixtures).
            continue

    must = [q for q in relevant if q["id"] in _MUST_INCLUDE_IDS]
    optional = [q for q in relevant if q["id"] not in _MUST_INCLUDE_IDS]
    selected: list[QuestionTemplate] = list(must)
    for q in optional:
        if len(selected) >= target_count:
            break
        selected.append(q)
    return [dict(q) for q in selected[:target_count]]


__all__ = [
    "QUESTION_TEMPLATES",
    "select_questions",
]
