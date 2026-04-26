"""OncoKB integration — variant normalization + biomarker → query extractor.

Pure module. NO I/O. NO mережа. Deterministic.

Per oncokb_integration_safe_rollout_v3.md §4 + §5:
  - Conservative normalization: when uncertain, SKIP (not guess).
  - Biomarkers without `oncokb_lookup` hint are skipped silently.
  - Extractor is the architectural firewall: it cannot import or be
    imported by the engine's track-builder (verified by import-graph
    test in Phase 3b).

Pending Phase 0 verification (A6): the exact form OncoKB accepts for
`alteration` URL parameter. Current assumption: short HGVS-p like
"V600E" or structured like "Exon 19 deletion". If A6 reveals it
prefers prefixed form ("p.V600E"), update OUTPUT_FORMAT here without
changing the public API.
"""

from __future__ import annotations

import re
from typing import Optional

from .oncokb_types import NormalizedVariant, OncoKBQuery


# ── Amino-acid 3-letter → 1-letter table ────────────────────────────────


_AA_3_TO_1: dict[str, str] = {
    "Ala": "A", "Arg": "R", "Asn": "N", "Asp": "D", "Cys": "C",
    "Gln": "Q", "Glu": "E", "Gly": "G", "His": "H", "Ile": "I",
    "Leu": "L", "Lys": "K", "Met": "M", "Phe": "F", "Pro": "P",
    "Ser": "S", "Thr": "T", "Trp": "W", "Tyr": "Y", "Val": "V",
    "Ter": "*", "Sec": "U", "Pyl": "O",
}


# ── Patterns ─────────────────────────────────────────────────────────────


# Short HGVS-p like "V600E", "L858R", "G12C"; optional "p." prefix
_RE_HGVS_P_SHORT = re.compile(
    r"^(?:p\.)?([A-Z\*])(\d+)([A-Z\*])$"
)

# 3-letter HGVS-p like "p.Val600Glu" or "Val600Glu"
_RE_HGVS_P_3LETTER = re.compile(
    r"^(?:p\.)?([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2}|\*|Ter)$"
)

# Structured exon deletion like "del E746_A750" or "E746_A750del"
_RE_EXON_DEL_STRUCTURED = re.compile(
    r"^(?:del\s+)?([A-Z]\d+_[A-Z]\d+)(?:del)?$"
)

# Exon-level descriptors recognised by OncoKB (e.g. "Exon 19 deletion",
# "Exon 20 insertion"). Whitelist — case-insensitive match.
_EXON_DESCRIPTORS = {
    "exon 19 deletion": "Exon 19 deletion",
    "exon 19 del": "Exon 19 deletion",
    "ex19del": "Exon 19 deletion",
    "exon 20 insertion": "Exon 20 insertion",
    "exon 20 ins": "Exon 20 insertion",
    "ex20ins": "Exon 20 insertion",
}

# Frameshift like "W288fs" — pass through (OncoKB recognises HGVS frameshift)
_RE_FRAMESHIFT = re.compile(r"^(?:p\.)?([A-Z])(\d+)fs(\*\d+)?$")

# HGVS-c — explicit skip (we never guess transcript-mapping)
_RE_HGVS_C = re.compile(r"^c\.")

# Boolean / generic flags — skip
_BOOLEAN_VALUES = {"true", "false", "yes", "no", "positive", "negative", "present"}


# ── Public API ───────────────────────────────────────────────────────────


def normalize_variant(raw: str, gene: str) -> Optional[NormalizedVariant]:
    """Normalize a variant string to OncoKB-canonical form.

    Returns None when normalization is unsafe (HGVS-c without transcript,
    fusion, boolean flag, unrecognised format). Caller MUST treat None
    as "skip OncoKB lookup for this biomarker" — never as "no evidence".

    Conservative by design: a false skip is recoverable (clinician can
    consult OncoKB manually); a false canonicalization is not (clinician
    receives wrong evidence with no warning).
    """

    if not raw or not gene:
        return None

    raw_stripped = raw.strip()
    gene_upper = gene.strip().upper()

    if not raw_stripped or not gene_upper:
        return None

    lower = raw_stripped.lower()

    # Boolean / generic flags
    if lower in _BOOLEAN_VALUES:
        return None

    # HGVS-c — explicit skip
    if _RE_HGVS_C.match(raw_stripped):
        return None

    # Fusion — skip in MVP (per oncokb_data_scope.md). Heuristic: hyphen
    # between two uppercase tokens (e.g. "EML4-ALK", "BCR-ABL1").
    if "-" in raw_stripped:
        parts = raw_stripped.split("-")
        if len(parts) == 2 and all(p.replace("1", "").replace("2", "").isalpha() and p.isupper() for p in parts):
            return None

    # ITD-style descriptors (e.g. "FLT3-ITD") — also skip in MVP.
    if "itd" in lower or "tandem duplication" in lower:
        return None

    # Exon-level whitelist
    if lower in _EXON_DESCRIPTORS:
        return NormalizedVariant(
            gene=gene_upper,
            oncokb_query_string=_EXON_DESCRIPTORS[lower],
            raw=raw_stripped,
        )

    # Structured exon deletion (e.g. "E746_A750del")
    m = _RE_EXON_DEL_STRUCTURED.match(raw_stripped)
    if m:
        canonical = f"{m.group(1)}del"
        return NormalizedVariant(
            gene=gene_upper,
            oncokb_query_string=canonical,
            raw=raw_stripped,
        )

    # Frameshift
    m = _RE_FRAMESHIFT.match(raw_stripped)
    if m:
        canonical = f"{m.group(1)}{m.group(2)}fs"
        if m.group(3):
            canonical += m.group(3)
        return NormalizedVariant(
            gene=gene_upper,
            oncokb_query_string=canonical,
            raw=raw_stripped,
        )

    # HGVS-p 3-letter — convert to short
    m = _RE_HGVS_P_3LETTER.match(raw_stripped)
    if m:
        ref3, pos, alt3 = m.group(1), m.group(2), m.group(3)
        ref1 = _AA_3_TO_1.get(ref3)
        # Handle "Ter" stop codon at alt position
        if alt3 == "Ter":
            alt1 = "*"
        else:
            alt1 = _AA_3_TO_1.get(alt3)
        if ref1 and alt1:
            return NormalizedVariant(
                gene=gene_upper,
                oncokb_query_string=f"{ref1}{pos}{alt1}",
                raw=raw_stripped,
            )
        # Unknown amino-acid token — skip (don't guess)
        return None

    # HGVS-p short (V600E etc.)
    m = _RE_HGVS_P_SHORT.match(raw_stripped)
    if m:
        ref, pos, alt = m.group(1), m.group(2), m.group(3)
        return NormalizedVariant(
            gene=gene_upper,
            oncokb_query_string=f"{ref}{pos}{alt}",
            raw=raw_stripped,
        )

    # Anything else — skip (never guess)
    return None


def extract_oncokb_queries(
    biomarker_hints: list[tuple[str, str, str]],
    *,
    oncotree_code: Optional[str] = None,
) -> list[OncoKBQuery]:
    """Build OncoKB queries from a list of (biomarker_id, gene, variant) hints.

    Pure function. Deterministic ordering: sorted by gene then biomarker_id
    so that test snapshots and provenance events are stable.

    `oncotree_code` is applied uniformly. The caller resolves it from
    Disease.oncotree_code or via fallback table; passing None is valid
    and triggers OncoKB pan-tumor mode (Q4 — render shows warning badge).

    Skipped biomarkers (variant fails normalization) are dropped silently
    — caller may want to log via the Plan warnings list separately."""

    queries: list[OncoKBQuery] = []
    seen_keys: set[tuple[str, str, str]] = set()

    sorted_hints = sorted(biomarker_hints, key=lambda h: (h[1].upper(), h[0]))

    for biomarker_id, gene, variant in sorted_hints:
        nv = normalize_variant(variant, gene)
        if nv is None:
            continue

        key = (nv.gene, nv.oncokb_query_string, oncotree_code or "")
        if key in seen_keys:
            # De-dupe: same biomarker referenced by 2+ patient findings
            continue
        seen_keys.add(key)

        queries.append(
            OncoKBQuery(
                gene=nv.gene,
                variant=nv.oncokb_query_string,
                oncotree_code=oncotree_code,
                source_biomarker_id=biomarker_id,
            )
        )

    return queries


__all__ = [
    "normalize_variant",
    "extract_oncokb_queries",
]
