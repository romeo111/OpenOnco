"""Trial outlook scoring — per-trial structured signals.

v1 ships two heuristic signals over the parsed ctgov dict, no KB lookup,
no probabilistic modeling, no verbal verdict:

  - `biomarker_stratification`: was the patient's biomarker term mentioned
    in the trial's inclusion criteria? (enriched / open_label / unclear)
  - `design_flags`: phase1-only, small N, surrogate-only endpoints,
    single-country.

Both are derivable from the dict produced by
`knowledge_base.clients.ctgov_client._parse_study`, so scoring is pure
and testable without network.

Architectural invariant (CHARTER §8.3 + plan §3.2): the engine never reads
the resulting `TrialOutlook` back as a selection signal. Render uses it to
display structured tags next to each trial; that is the only consumer.

Mechanism-precedent scoring (matching trial interventions to KB Drug/BMA
evidence tiers) is a deliberate follow-up — it requires drug-name
disambiguation against `Drug.names` and is the noisiest signal of the four
proposed in the design discussion. Ship the cheap signals first.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Optional

from knowledge_base.schemas.experimental_option import (
    BiomarkerStratification,
    DesignFlag,
    TrialOutlook,
)


# ── Biomarker stratification ─────────────────────────────────────────────


def _normalize(text: str) -> str:
    return text.lower().strip()


# Tokens we strip from a biomarker term before matching — the trial text
# rarely echoes the exact phrase ("EGFR mutation" vs "EGFR-mutant" vs
# "activating EGFR alteration"), so we match on the gene/keyword core.
_BM_STOPWORDS = {
    "mutation", "mutations", "mutant", "mutated",
    "amplification", "amplified",
    "fusion", "fusions", "rearrangement", "rearranged",
    "expression", "expressing", "positive", "negative",
    "alteration", "alterations", "variant", "variants",
}


def _biomarker_tokens(biomarker_term: str) -> list[str]:
    """Split a biomarker term into matchable tokens.

    "EGFR mutation" -> ["egfr"]
    "BRAF V600E" -> ["braf", "v600e"]
    "HER2-positive" -> ["her2"]
    """
    cleaned = re.sub(r"[^a-z0-9 ]", " ", _normalize(biomarker_term))
    parts = [p for p in cleaned.split() if p and p not in _BM_STOPWORDS]
    return parts


def _detect_biomarker_stratification(
    inclusion_summary: Optional[str],
    exclusion_summary: Optional[str],
    biomarker_term: Optional[str],
) -> tuple[BiomarkerStratification, Optional[str]]:
    """Return (stratification, explanatory_note).

    Three buckets:
      - "enriched"  : every biomarker token appears in inclusion text
      - "open_label": biomarker term empty, or no token in inclusion text
      - "unclear"   : biomarker tokens appear only in exclusion text, or
                      partial inclusion match (some tokens but not all)
    """
    if not biomarker_term:
        return ("open_label", None)

    tokens = _biomarker_tokens(biomarker_term)
    if not tokens:
        return ("open_label", None)

    incl = _normalize(inclusion_summary or "")
    excl = _normalize(exclusion_summary or "")

    incl_hits = [t for t in tokens if t in incl]
    excl_hits = [t for t in tokens if t in excl]

    if len(incl_hits) == len(tokens):
        return (
            "enriched",
            f"inclusion criteria reference {biomarker_term}",
        )

    if incl_hits and len(incl_hits) < len(tokens):
        return (
            "unclear",
            f"partial biomarker match in inclusion ({', '.join(incl_hits)})",
        )

    if excl_hits and not incl_hits:
        return (
            "unclear",
            f"biomarker mentioned only in exclusion ({', '.join(excl_hits)})",
        )

    return ("open_label", None)


# ── Design flags ─────────────────────────────────────────────────────────


def _phase_set(phase: Optional[str]) -> set[str]:
    if not phase:
        return set()
    # ctgov_client renders multi-phase as "PHASE2 / PHASE3"; tolerate any
    # separator and normalize.
    return {p.strip().upper() for p in re.split(r"[/,;]+", phase) if p.strip()}


def _has_overall_survival(primary_outcomes: list[str]) -> bool:
    blob = _normalize(" ".join(primary_outcomes or []))
    # "OS" alone is too noisy (it appears inside other tokens); require a
    # word boundary or the spelled-out phrase.
    return bool(
        re.search(r"\boverall survival\b", blob)
        or re.search(r"\bos\b", blob)
    )


def _has_surrogate_endpoint(primary_outcomes: list[str]) -> bool:
    blob = _normalize(" ".join(primary_outcomes or []))
    return any(
        marker in blob
        for marker in (
            "progression-free",
            "progression free",
            "pfs",
            "objective response",
            "overall response",
            "orr",
            "response rate",
            "disease-free",
            "disease free",
            "dfs",
        )
    )


def _detect_design_flags(study: dict) -> tuple[list[DesignFlag], list[str]]:
    """Return (flags, parallel_notes). One note per flag, same index."""
    flags: list[DesignFlag] = []
    notes: list[str] = []

    phases = _phase_set(study.get("phase"))
    if phases == {"PHASE1"}:
        flags.append("phase1_only")
        notes.append("phase 1 only — early safety/PK signal, not efficacy")

    enrollment = study.get("enrollment") or 0
    try:
        enrollment_n = int(enrollment)
    except (TypeError, ValueError):
        enrollment_n = 0
    if 0 < enrollment_n < 50:
        flags.append("small_enrollment")
        notes.append(f"target enrollment N={enrollment_n} (<50)")

    primary_outcomes = study.get("primary_outcomes") or []
    if isinstance(primary_outcomes, str):
        primary_outcomes = [primary_outcomes]
    if (
        primary_outcomes
        and _has_surrogate_endpoint(primary_outcomes)
        and not _has_overall_survival(primary_outcomes)
    ):
        flags.append("surrogate_endpoint_only")
        notes.append("primary endpoint is a surrogate (PFS/ORR), no OS")

    countries = study.get("countries") or []
    if isinstance(countries, list) and len(countries) == 1:
        flags.append("single_country")
        notes.append(f"single-country trial ({countries[0]})")

    return (flags, notes)


# ── Public entry point ───────────────────────────────────────────────────


def score_trial(
    study: dict,
    *,
    biomarker_term: Optional[str] = None,
    inclusion_summary: Optional[str] = None,
    exclusion_summary: Optional[str] = None,
    last_scored: Optional[str] = None,
) -> TrialOutlook:
    """Score one parsed-ctgov study dict.

    Args:
        study:               dict from `ctgov_client._parse_study` (or the
                             stub form used in tests). Reads `phase`,
                             `enrollment`, `primary_outcomes`, `countries`.
        biomarker_term:      patient's biomarker phrase, e.g. "EGFR mutation".
                             Empty/None -> "open_label" stratification.
        inclusion_summary:   eligibility-inclusion text (already split by
                             `experimental_options._split_eligibility`).
                             Falls back to study["eligibility_criteria"]
                             when absent so callers can pass the raw study.
        exclusion_summary:   eligibility-exclusion text, same fallback.
        last_scored:         ISO date string. Defaults to today (UTC).

    Returns:
        `TrialOutlook` with stratification + design flags + notes.
    """
    if inclusion_summary is None and exclusion_summary is None:
        # Caller didn't pre-split — fall back to the raw eligibility blob
        # for both buckets. Stratification still works (it OR's the two).
        raw = study.get("eligibility_criteria") or study.get("eligibility_summary") or ""
        inclusion_summary = raw
        exclusion_summary = ""

    stratification, strat_note = _detect_biomarker_stratification(
        inclusion_summary, exclusion_summary, biomarker_term
    )
    flags, flag_notes = _detect_design_flags(study)

    notes: list[str] = []
    if strat_note:
        notes.append(strat_note)
    notes.extend(flag_notes)

    return TrialOutlook(
        biomarker_stratification=stratification,
        design_flags=flags,
        notes=notes,
        last_scored=last_scored or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    )


__all__ = ["score_trial"]
