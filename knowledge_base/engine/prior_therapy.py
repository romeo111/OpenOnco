"""Derive scalar prior-therapy findings from `findings.prior_lines`.

Why this module exists
----------------------
Prior therapy is authored as `findings.prior_lines` — a list, either of
dicts (`{"line": 1, "regimen": "erlotinib", ...}`) or of free-text strings
(`"CHOEP x6"`). It survives `plan._flatten_findings` as a raw list, and the
RedFlag clause evaluator (`redflag_eval._resolve_finding`) reads flat scalar
keys only. So no `finding:` clause can express "the prior line was
osimertinib", and any RedFlag written against prior-therapy scalars is inert.

`rf_universal_prior_egfri_progression.yaml` is exactly that: it triggers on
`prior_egfri_progression` / `prior_egfri_received` / `best_response_to_egfri`,
which 0 of the 36 `prior_lines`-carrying example profiles set, and which
appear nowhere else in the knowledge base.

This module derives those scalars from the authored lists, normalised
against the `drugs/` catalogue rather than by hard-coding drug names in the
engine.

Absence vs recorded-false
-------------------------
Derivation is skipped entirely when `prior_lines` is absent, is not a list,
or holds no text-bearing entry. A patient with no recorded prior therapy
stays *unknown* rather than becoming a recorded `false` — the failure mode
that got a conversion reverted in PR #632. `prior_therapy_recorded` marks
the difference explicitly.

Derived values never override authored ones: `_flatten_findings` merges them
with `setdefault`, so an explicit `prior_osimertinib: false` in a profile
wins over anything inferred here.

Fail-safe direction
-------------------
A derived `false` is the safe direction. Every consumer gates on a *positive*
(`prior_egfri_received: true`, `prior_osimertinib: true`), so a drug name this
module fails to recognise causes a patient to miss a targeted track — never
to be routed onto one they do not qualify for. Unrecognised text is surfaced
in `prior_therapy_unmatched_lines` so the data-quality gap stays visible.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

# `EGFR` as a standalone token. This is a lookbehind rather than `\b`
# because `\b` also matches inside **V**EGFR: of the 18 catalogue
# `drug_class` strings containing the substring "EGFR", 10 are VEGFR
# multi-kinase inhibitors (axitinib, lenvatinib, sorafenib, regorafenib, …)
# and are not EGFR-directed. Word-boundary matching leaves the 8 that are:
# afatinib, amivantamab, cetuximab, dacomitinib, erlotinib, gefitinib,
# lazertinib, osimertinib.
_EGFR_CLASS_RE = re.compile(r"(?<![A-Za-z])EGFR", re.IGNORECASE)

# Progression recorded in free text — "PD at 16 mo", "PD with acquired
# T790M", "relapse at 22 mo". The trailing `-` guard stops `PD-L1` from
# reading as progressive disease.
_PROGRESSION_RE = re.compile(
    r"(?<![A-Za-z0-9-])PD(?![A-Za-z0-9-])|progress|relaps|refractor",
    re.IGNORECASE,
)

# Drug names shorter than this are not indexed. Nothing real is lost — the
# shortest brand names in the catalogue are 4 characters (Ifex, Ofev, Omez,
# Tums) — but it guards against a stray 1-2 character `names` value matching
# everywhere.
_MIN_NAME_LEN = 4


@dataclass(frozen=True)
class DrugIndex:
    """Drug-name lookup built from the `drugs/` catalogue.

    `by_name` maps a lowercased name (preferred, english, or brand) to the
    drug ids claiming it. It is a set because 7 catalogue names are shared
    by two ids each — all benign prevention/indication variants such as
    `DRUG-LETROZOLE` / `DRUG-LETROZOLE-CHEMOPREVENTION`.
    """

    by_name: dict[str, frozenset[str]]
    egfr_directed: frozenset[str]
    pattern: re.Pattern[str] | None

    def match_drug_ids(self, text: str) -> set[str]:
        """Return every drug id named in `text`. Case-insensitive, matched
        on whole tokens so `erlotinib` is not found inside a longer word."""
        if not text or self.pattern is None:
            return set()
        found: set[str] = set()
        for hit in self.pattern.findall(text.lower()):
            found |= self.by_name.get(hit, frozenset())
        return found


def build_drug_index(entities: dict) -> DrugIndex:
    """Build a `DrugIndex` from loaded KB entities.

    Reads only entities of type `drugs`; no file I/O. Cheap enough to call
    per plan generation (the catalogue is ~321 entries already in memory).
    """
    by_name: dict[str, set[str]] = {}
    egfr_directed: set[str] = set()

    for info in entities.values():
        if not isinstance(info, dict) or info.get("type") != "drugs":
            continue
        data = info.get("data") or {}
        drug_id = data.get("id")
        if not drug_id:
            continue

        names = data.get("names") or {}
        candidates = [names.get("preferred"), names.get("english")]
        candidates.extend(names.get("brand_names") or [])
        for raw in candidates:
            if not isinstance(raw, str):
                continue
            token = raw.strip().lower()
            if len(token) < _MIN_NAME_LEN:
                continue
            by_name.setdefault(token, set()).add(drug_id)

        if _EGFR_CLASS_RE.search(str(data.get("drug_class") or "")):
            egfr_directed.add(drug_id)

    pattern = None
    if by_name:
        # Longest-first so "axicabtagene ciloleucel" wins over any prefix.
        alternatives = sorted((re.escape(n) for n in by_name), key=len, reverse=True)
        pattern = re.compile(
            r"(?<![a-z0-9])(?:" + "|".join(alternatives) + r")(?![a-z0-9])"
        )

    return DrugIndex(
        by_name={k: frozenset(v) for k, v in by_name.items()},
        egfr_directed=frozenset(egfr_directed),
        pattern=pattern,
    )


def _entry_text(entry: Any) -> tuple[str, Any, Any] | None:
    """Normalise one `prior_lines` entry to (searchable text, best_response,
    outcome). Returns None for an entry carrying no usable text.

    Both authored shapes are handled: 17 example profiles use list-of-dicts,
    18 use list-of-strings.
    """
    if isinstance(entry, str):
        text = entry.strip()
        return (text, None, None) if text else None

    if isinstance(entry, dict):
        parts = [
            str(entry[key])
            for key in ("regimen", "drug_class")
            if entry.get(key) is not None
        ]
        text = " ".join(parts).strip()
        if not text:
            return None
        return (text, entry.get("best_response"), entry.get("outcome"))

    return None


def derive_prior_therapy_findings(
    findings: dict[str, Any], index: DrugIndex
) -> dict[str, Any]:
    """Derive scalar prior-therapy findings from `findings.prior_lines`.

    Returns an empty dict — meaning "nothing is known" — when `prior_lines`
    is absent, is not a list, or holds no text-bearing entry. Notably one
    example profile records `prior_lines` as an integer *count*
    (`patient_melanoma_nivo_relatlimab.json`: `"prior_lines": 1`), which
    names no drug; deriving `prior_osimertinib: false` from it would assert
    something the profile does not say.
    """
    raw = findings.get("prior_lines")
    if not isinstance(raw, list):
        return {}

    entries = [parsed for parsed in (_entry_text(e) for e in raw) if parsed]
    if not entries:
        return {}

    all_drug_ids: set[str] = set()
    unmatched: list[str] = []
    egfri_received = False
    egfri_progression = False
    best_response_to_egfri: Any = None

    for text, best_response, outcome in entries:
        matched = index.match_drug_ids(text)
        all_drug_ids |= matched
        if not matched:
            unmatched.append(text)

        if not (matched & index.egfr_directed):
            continue

        egfri_received = True
        if best_response_to_egfri is None and best_response is not None:
            best_response_to_egfri = best_response
        if str(best_response).strip().upper() == "PD":
            egfri_progression = True
        elif _PROGRESSION_RE.search(f"{text} {outcome or ''}"):
            egfri_progression = True

    derived: dict[str, Any] = {
        "prior_therapy_recorded": True,
        "prior_drug_ids": sorted(all_drug_ids),
        "prior_egfri_received": egfri_received,
        "prior_egfri_progression": egfri_progression,
        "prior_osimertinib": "DRUG-OSIMERTINIB" in all_drug_ids,
    }
    if best_response_to_egfri is not None:
        derived["best_response_to_egfri"] = best_response_to_egfri
    if unmatched:
        derived["prior_therapy_unmatched_lines"] = unmatched
    return derived
