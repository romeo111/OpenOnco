"""Filter RedFlags into emergency-tier (call doctor immediately) for patient mode.

Render-time only — never read by the engine as a treatment-selection signal
(CHARTER §8.3 invariant — same contract as `_actionability.py` and `_nszu.py`).
The engine still walks the algorithm tree as authored. This helper just
selects which red flags warrant a 'call your doctor immediately' call-out
in the patient-facing report.

Three orthogonal signals identify a red flag as emergency-tier:

  1. `severity == "critical"` — KB-authored severity per
     REDFLAG_AUTHORING_GUIDE; critical = imminent risk to life or organ.
  2. `clinical_direction == "hold"` — algorithm halts treatment selection
     pending stabilization (e.g. RF-APL-EMERGENCY-DIC, RF-AML-EMERGENCY-TLS-LEUKOSTASIS).
  3. Keyword presence in `definition_ua` / `definition` — backstop for
     RFs that author the danger in prose rather than via severity flag
     (e.g. universal infusion-reaction or HBV-reactivation RFs).

Lenient by design: a false positive surfaces an extra emergency line in
the patient banner — no clinical risk. A false negative could drop a real
emergency from the banner — much worse.
"""

from __future__ import annotations

from typing import Iterable


# Keywords (Ukrainian + canonical English clinical terms) that signal an
# emergency situation requiring same-day medical attention. Matched as
# case-insensitive substrings against `definition_ua` + `definition`.
EMERGENCY_RF_KEYWORDS_UA: list[str] = [
    "лихоманка", "сепсис", "TLS", "tumor lysis", "DIC", "ДВЗ",
    "коагуляція", "кровотеча", "тромбоз", "анафілаксія", "анафілактич",
    "інфузійна реакція", "инфузійна реакція",
    "легенева недостатність", "печінкова недостатність", "ниркова недостатність",
    "нейтропенія тяжка", "фебрильна нейтропенія", "febrile neutropenia",
    "encephalopathy", "encephalitis", "енцефалопат", "енцефаліт",
    "leukostasis", "лейкостаз", "hyperleukocytosis", "гіперлейкоцитоз",
    "differentiation syndrome", "синдром диференціювання",
    "myocarditis", "міокардит", "pneumonitis", "пневмоніт",
    "колапс", "shock", "шок",
]


def is_emergency_rf(rf_dict: dict) -> bool:
    """True if the RF is emergency-tier for patient-facing rendering.

    Emergency = severity is `critical` OR clinical direction is `hold`
    OR an emergency keyword appears in the definition text. See module
    docstring for rationale on the lenient OR-of-three strategy."""
    if not isinstance(rf_dict, dict):
        return False
    severity = str(rf_dict.get("severity") or "").strip().lower()
    direction = str(rf_dict.get("clinical_direction") or "").strip().lower()
    if severity == "critical" or direction == "hold":
        return True
    text = (
        str(rf_dict.get("definition_ua") or "") + " "
        + str(rf_dict.get("definition") or "")
    ).lower()
    for kw in EMERGENCY_RF_KEYWORDS_UA:
        if kw.lower() in text:
            return True
    return False


def filter_emergency_rfs(rf_findings: Iterable[dict]) -> list[dict]:
    """Filter a collection of RedFlag dicts to the emergency-tier subset.

    Stable order: caller-supplied iteration order is preserved so the
    rendered banner is deterministic across renders."""
    return [rf for rf in (rf_findings or []) if is_emergency_rf(rf)]


def patient_emergency_label(rf_dict: dict) -> str:
    """One-line patient-readable emergency action statement.

    Uses `definition_ua` (Ukrainian) when set, else falls back to
    `definition` (English). Truncates to the first sentence and prepends
    a siren emoji so the banner reads as an action prompt rather than a
    technical RF dump."""
    text = ""
    if isinstance(rf_dict, dict):
        text = str(rf_dict.get("definition_ua") or rf_dict.get("definition") or "")
    text = text.strip()
    if not text:
        return "🚨 Зверніться до лікаря негайно"
    # Take first sentence (split on period); trim trailing whitespace.
    first_sentence = text.split(".")[0].strip()
    # Don't keep an empty fragment if the text starts with a period.
    if not first_sentence:
        first_sentence = text
    return f"🚨 {first_sentence}"


__all__ = [
    "EMERGENCY_RF_KEYWORDS_UA",
    "is_emergency_rf",
    "filter_emergency_rfs",
    "patient_emergency_label",
]
