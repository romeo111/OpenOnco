"""NSZU availability lookup — map a Drug entity's
`regulatory_status.ukraine_registration` block to a per-drug, per-disease
availability badge for the render layer.

Render-time metadata only. The engine MUST NOT consult this badge as a
treatment-selection signal (CHARTER §8.3, plan §0 invariant — same
contract as ESCAT/OncoKB tier badges in `_actionability.py`). Tracks come
from the declarative Algorithm; this module surfaces NSZU coverage
context next to each recommended drug for clinician + patient
orientation.

Status taxonomy (Ukrainian-first labels, EN translations rendered by the
caller):

  * `covered`         — drug.registered=True AND drug.reimbursed_nszu=True
                        AND patient_disease_id matches one of the
                        drug's `reimbursement_indications` strings.
  * `partial`         — registered=True AND reimbursed_nszu=True but no
                        indication matched the patient's disease (NSZU
                        covers other indications of this drug, not this
                        one).
  * `oop`             — registered=True AND reimbursed_nszu=False (drug
                        is legally available in UA but pricing is fully
                        out-of-pocket / not on any НСЗУ pakage).
  * `not-registered`  — registered=False (no РП — has to be imported via
                        named-patient / cross-border / EAP / trial).

Indication-match rules (case-insensitive throughout):

  1. The patient's `disease_id` is split on '-' to extract the disease
     stem (e.g. `DIS-DLBCL-NOS` → `DLBCL`, `DIS-OVARIAN` → `OVARIAN`).
  2. We also try the full id minus the `DIS-` prefix (`DLBCL-NOS`).
  3. We also pull the patient's disease's `names.ukrainian` and
     `names.preferred` strings when supplied via the `disease_names`
     argument — those are matched as substrings against each
     `reimbursement_indications` entry.
  4. A match is declared if any of the patient-disease tokens appears
     (case-insensitive substring) inside any indication string.

Matching is deliberately lenient — `reimbursement_indications` strings
are authored in free Ukrainian by clinical reviewers (e.g.
"Дифузна великоклітинна B-клітинна лімфома (R-CHOP)" for DLBCL). A
false positive surfaces a green "covered" badge that the HCP can verify
against the drug's notes; a false negative surfaces "partial" which
prompts clinician review via the badge tooltip. The cost of a false
"covered" is lower than the cost of dropping a real coverage signal,
because the tooltip carries the verbatim drug.notes excerpt for HCP
review.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


NszuStatus = Literal["covered", "partial", "oop", "not-registered"]


class NszuBadge(BaseModel):
    """One drug's NSZU availability rendered as a badge.

    Attached per-drug-recommendation in the rendered Plan; never read
    back by the engine (render-time only)."""

    drug_id: str
    status: NszuStatus
    indication_match: Optional[str] = None  # the matched reimbursement_indications entry, if any
    label: str  # human-readable Ukrainian summary (e.g. "✓ НСЗУ покриває")
    notes_excerpt: str = ""  # short excerpt from drug.notes for tooltip / detail

    # Disease tokens we tried to match against — useful for tests + debugging
    matched_against: list[str] = Field(default_factory=list)


# ── Localized labels ─────────────────────────────────────────────────────

_LABELS_UA: dict[str, str] = {
    "covered": "✓ НСЗУ покриває",
    "partial": "⚠ НСЗУ — не для цього показання",
    "oop": "⚠ Поза НСЗУ — за свій кошт",
    "not-registered": "✗ Не зареєстровано в UA",
}

_LABELS_EN: dict[str, str] = {
    "covered": "✓ NSZU covered",
    "partial": "⚠ NSZU — not for this indication",
    "oop": "⚠ Out-of-pocket",
    "not-registered": "✗ Not registered in UA",
}


def nszu_label(status: NszuStatus, target_lang: str = "uk") -> str:
    """Localized label for one of the four NSZU status values.

    Falls back to UA when target_lang is unrecognised (mirrors `_t` in
    render.py). Caller is responsible for HTML-escaping."""
    if (target_lang or "uk").lower().startswith("en"):
        return _LABELS_EN.get(status, status)
    return _LABELS_UA.get(status, status)


# ── Disease-token derivation ─────────────────────────────────────────────


_NAME_STOPWORDS = {
    # English connectors / qualifiers — too generic to safely substring-match
    "the", "and", "or", "of", "in", "with", "for", "type", "cell", "cells",
    "subtype", "predominant", "high", "low", "grade", "high-grade", "low-grade",
    "nos", "carcinoma", "cancer", "tumor", "tumour", "disease", "lymphoma",
    "leukemia", "leukaemia", "myeloma",
    # Ukrainian — same idea, very generic; would over-match across diseases
    "та", "або", "і", "з", "для", "тип", "підтип", "карцинома", "рак",
    "пухлина", "хвороба", "лімфома", "лейкоз", "лейкемія", "мієлома",
}


def _name_words(text: Optional[str]) -> list[str]:
    """Extract non-stopword content tokens from a free-text disease name.

    "Ovarian carcinoma (high-grade serous predominant)"
        → ["ovarian", "serous"]
    "Карцинома яєчників (переважно high-grade серозна)"
        → ["яєчників", "серозна"]
    "Diffuse Large B-Cell Lymphoma, NOS"
        → ["diffuse", "large", "b-cell"]

    Tokens shorter than 4 chars are dropped along with any in
    `_NAME_STOPWORDS`. Punctuation (parentheses, commas, semicolons) is
    treated as separator. Hyphens are kept inside tokens (so "B-cell"
    survives as one token)."""
    if not text:
        return []
    s = str(text).lower()
    # Replace punctuation we want to treat as separator with space
    for ch in "(),;:/[]{}\"'.!?":
        s = s.replace(ch, " ")
    out: list[str] = []
    for raw in s.split():
        tok = raw.strip().strip("-")
        if len(tok) < 4:
            continue
        if tok in _NAME_STOPWORDS:
            continue
        if tok not in out:
            out.append(tok)
    return out


def _disease_tokens(
    disease_id: str,
    disease_names: Optional[dict] = None,
) -> list[str]:
    """Build the list of tokens we'll search for inside each
    `reimbursement_indications` entry.

    `disease_id`     : e.g. `DIS-DLBCL-NOS` — the canonical KB id.
    `disease_names`  : optional `{"preferred": str, "ukrainian": str, …}`
                        from the resolved Disease entity. When passed,
                        both whole names AND content words extracted from
                        them are added as substring tokens — they often
                        match free-text indication strings authored in
                        Ukrainian by clinicians (e.g. "яєчників" matches
                        "рак яєчників BRCA1/2-мутований").

    Tokens are normalized to lowercase and de-duped (preserving order).
    Empty / None inputs are silently skipped."""
    tokens: list[str] = []

    def _add(t: Optional[str]) -> None:
        if not t:
            return
        norm = str(t).strip().lower()
        if norm and norm not in tokens:
            tokens.append(norm)

    if disease_id:
        did = str(disease_id).strip()
        # Full id (lower-case)
        _add(did)
        # Strip "DIS-" prefix
        if did.upper().startswith("DIS-"):
            _add(did[4:])
        # First segment after DIS- — the disease stem (e.g. DLBCL, OVARIAN)
        parts = did.upper().split("-")
        if len(parts) >= 2 and parts[0] == "DIS":
            _add(parts[1])
        elif parts:
            _add(parts[0])

    if disease_names:
        for key in ("ukrainian", "preferred", "english"):
            full = disease_names.get(key)
            _add(full)
            # Also break the name into content words — handles the very
            # common case where the indication string uses one specific
            # noun (e.g. "яєчників") rather than the full disease name.
            for w in _name_words(full):
                _add(w)

    return tokens


def _indication_match(
    reimbursement_indications: list[str],
    tokens: list[str],
) -> Optional[str]:
    """Return the first reimbursement_indications entry whose lowercase
    text contains any of the patient-disease tokens. None when no
    indication matches.

    Substring search in one direction only: token in indication. The
    indication strings are full clinical phrases (e.g. "Фолікулярна
    лімфома (R-CHOP / R-Bendamustine; підтримка R)") so we want to
    confirm the patient's disease name appears inside that phrase, not
    the other way round."""
    if not reimbursement_indications or not tokens:
        return None
    for entry in reimbursement_indications:
        if not entry:
            continue
        haystack = str(entry).strip().lower()
        if not haystack:
            continue
        for tok in tokens:
            # Skip very short tokens — would over-match (e.g. "fl" matches
            # everything). Three chars is the practical floor for KB ids.
            if len(tok) < 3:
                continue
            if tok in haystack:
                return entry
    return None


def _notes_excerpt(notes: Optional[str], max_len: int = 240) -> str:
    """First-paragraph excerpt of drug.notes for the badge tooltip.

    Notes can be multi-paragraph free text; we take the first non-empty
    paragraph and truncate at `max_len` chars on a word boundary."""
    if not notes:
        return ""
    text = str(notes).strip()
    if not text:
        return ""
    # First paragraph
    para = text.split("\n\n", 1)[0].replace("\n", " ").strip()
    if len(para) <= max_len:
        return para
    cut = para[:max_len]
    # Back off to last space so we don't break a word
    sp = cut.rfind(" ")
    if sp > max_len - 40:
        cut = cut[:sp]
    return cut.rstrip(",.;: ") + "…"


# ── Public lookup ────────────────────────────────────────────────────────


def lookup_nszu_status(
    drug_entity: dict,
    patient_disease_id: str,
    *,
    disease_names: Optional[dict] = None,
) -> NszuBadge:
    """Map a Drug entity to its NSZU availability badge for one disease.

    `drug_entity` is the dict-shape Drug entity (loader's
    `entities_by_id[drug_id].data` payload, NOT the Pydantic model).
    Tolerates the entity having no `regulatory_status` block at all —
    falls through to `not-registered` so the render still produces a
    badge.

    `patient_disease_id` : the patient's resolved disease id, e.g.
    `DIS-DLBCL-NOS`. May be empty — in that case the indication match
    cannot run and a `reimbursed_nszu=True` drug renders as `partial`.

    `disease_names` (kwarg) : optional dict with `preferred` / `ukrainian`
    keys from the Disease entity, used to broaden the substring match
    into Ukrainian free-text indication strings."""

    drug_id = str((drug_entity or {}).get("id") or "")
    notes = (drug_entity or {}).get("notes") or ""
    reg_status = (drug_entity or {}).get("regulatory_status") or {}
    ua_reg = reg_status.get("ukraine_registration") or {}

    registered = bool(ua_reg.get("registered"))
    reimbursed = bool(ua_reg.get("reimbursed_nszu"))
    indications = list(ua_reg.get("reimbursement_indications") or [])

    # Tokens derived from the patient's disease — used only when
    # registered+reimbursed (the only branch where the indication match
    # matters).
    tokens = _disease_tokens(patient_disease_id, disease_names)

    if not registered:
        status: NszuStatus = "not-registered"
        match: Optional[str] = None
    elif not reimbursed:
        status = "oop"
        match = None
    else:
        match = _indication_match(indications, tokens)
        status = "covered" if match else "partial"

    return NszuBadge(
        drug_id=drug_id,
        status=status,
        indication_match=match,
        label=_LABELS_UA[status],
        notes_excerpt=_notes_excerpt(notes),
        matched_against=tokens,
    )


__all__ = [
    "NszuBadge",
    "NszuStatus",
    "lookup_nszu_status",
    "nszu_label",
    "_disease_tokens",
    "_indication_match",
    "_notes_excerpt",
]
