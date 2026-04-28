"""Fusion-aware (gene, variant) matcher for CIViC molecular profiles.

CIViC encodes fusion-on-fusion-background resistance mutations in a way
that naive equality matching misses. Specifically:

    gene    = "BCR::ABL1"
    variant = "Fusion AND ABL1 T315I"

Our normalized queries arrive as ``gene="ABL1", variant="T315I"`` (per
``actionability_extract.normalize_variant``), so a direct ``==`` lookup
returns nothing for what is, clinically, the single most important
actionable resistance mutation in CML.

This module is a **pure function** with no I/O and no engine imports.
It receives already-normalized query strings (uppercase HGNC gene,
short HGVS-p variant) and returns a boolean. Future agents can extend
the rule set by adding new branches and tests; never broaden the
matcher to fuzzy/Levenshtein matching — false positives in this layer
would silently surface wrong therapy evidence.

See ``docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`` §2.5
for the encoding quirks this matcher addresses.
"""

from __future__ import annotations

import re

__all__ = ["matches_civic_entry", "split_fusion_components"]


# ── Constants ────────────────────────────────────────────────────────────

# Variant strings that mean "any fusion event" rather than a point mutation.
_PAN_FUSION_VARIANTS = frozenset({"fusion", "fusions", "rearrangement"})

# Token splitter for whole-word substring matching inside the variant string.
# Splits on whitespace and on any non-alphanumeric char (so "T315I_extension"
# becomes ["T315I", "extension"], avoiding the substring trap where "T315"
# would otherwise match "T315I").
_TOKEN_SPLIT_RE = re.compile(r"[^A-Za-z0-9]+")

# Recognise a token as an HGNC-shaped gene symbol: uppercase alphanumeric,
# starts with a letter, length ≥ 2. Used to validate that "EML4-ALK" really
# is a fusion (both halves gene-shaped) and not, e.g., a HGVS variant string
# that happens to contain a hyphen.
_HGNC_TOKEN_RE = re.compile(r"^[A-Z][A-Z0-9]*$")


# ── Helpers ──────────────────────────────────────────────────────────────


def split_fusion_components(civic_gene: str) -> list[str]:
    """Split a CIViC gene field into its component HGNC symbols.

    Examples:
        "BCR::ABL1"     → ["BCR", "ABL1"]
        "EML4-ALK"      → ["EML4", "ALK"]
        "ETV6::NTRK3"   → ["ETV6", "NTRK3"]
        "BRAF"          → ["BRAF"]
        "V::ALK"        → ["V", "ALK"]   (CIViC uses V::ALK for variant ALK fusions)

    Returns ``[civic_gene]`` (single-element list) when the input does not
    look like a fusion. Hyphen-splitting only applies when *both* halves
    are HGNC-shaped, to avoid false-splitting variant strings containing
    a hyphen.
    """

    if not civic_gene:
        return []

    g = civic_gene.strip()
    if not g:
        return []

    # Preferred fusion separator in CIViC.
    if "::" in g:
        parts = [p.strip() for p in g.split("::") if p.strip()]
        return parts if parts else [g]

    # Legacy hyphen separator — only treat as fusion when both halves
    # are HGNC-shaped, otherwise hand back the verbatim symbol.
    if "-" in g:
        parts = [p.strip() for p in g.split("-")]
        if len(parts) == 2 and all(_HGNC_TOKEN_RE.match(p) for p in parts):
            return parts

    return [g]


def _tokenize(text: str) -> set[str]:
    """Split text into a set of alphanumeric tokens for whole-word matching."""
    if not text:
        return set()
    return {t for t in _TOKEN_SPLIT_RE.split(text) if t}


def _has_fusion_token(text: str) -> bool:
    """True if ``text`` contains the literal token 'Fusion' (any case).

    Whole-token match — does not match e.g. 'Fusionoid'.
    """
    if not text:
        return False
    return any(t.lower() == "fusion" for t in _tokenize(text))


# ── Public API ───────────────────────────────────────────────────────────


def matches_civic_entry(
    *,
    query_gene: str,
    query_variant: str,
    civic_gene: str,
    civic_variant: str,
) -> bool:
    """Return True if the (query_gene, query_variant) pair matches the
    CIViC molecular profile (civic_gene, civic_variant).

    All four arguments are required; the matcher is a total function.

    Query inputs are expected to already be normalized:
    - ``query_gene``: uppercase HGNC symbol (e.g. "ABL1")
    - ``query_variant``: short HGVS-p form per ``normalize_variant``
      (e.g. "T315I", "V600E", "Exon 19 deletion") OR one of the
      pan-fusion sentinels {"Fusion", "Fusions", "Rearrangement"}.

    CIViC inputs are verbatim from the molecular_profile entry:
    - ``civic_gene``: may be a single HGNC symbol or a fusion ("BCR::ABL1",
      "EML4-ALK", "V::ALK")
    - ``civic_variant``: may be a point mutation ("T315I"), a structured
      compound ("Fusion AND ABL1 T315I"), a generic fusion descriptor
      ("EML4-ALK Fusion"), etc.

    Matching rules (ordered, first match wins):

    1. **Exact match.** gene and variant both equal.
    2. **Fusion-component + variant-in-profile.** query_gene is one of
       the components of civic_gene (split on ``::`` or hyphen-when-both-
       halves-HGNC), AND query_variant is a whole-word token of
       civic_variant. Catches the BCR::ABL1+T315I pattern.
    3. **Pan-fusion query.** query_variant ∈ {"Fusion","Fusions","Rearrangement"}
       and EITHER civic_gene contains query_gene as a fusion component,
       OR (gene matches and civic_variant contains "Fusion" token).
    4. Otherwise → False.

    The matcher does NOT do fuzzy matching, chemical-effect inference,
    or Levenshtein. If the case is not covered, return False and let
    the caller log a no-match — extend with a new rule + tests instead
    of broadening the existing rules.
    """

    # Defensive: empty inputs → no match. (Don't raise; the matcher is
    # called in a hot loop over thousands of CIViC entries and any one
    # malformed entry shouldn't crash the run.)
    if not query_gene or not query_variant:
        return False
    if not civic_gene:
        return False

    qg = query_gene.strip().upper()
    qv = query_variant.strip()
    cg = civic_gene.strip()
    cv = (civic_variant or "").strip()

    if not qg or not qv or not cg:
        return False

    # ── Rule 1: exact match (case-insensitive on both sides) ──
    # casefold() chosen over .lower() for non-ASCII safety. Phase 3-O
    # surfaced NPM1 W288fs vs CIViC W288FS as a real miss; gene-side made
    # case-insensitive defensively (HGNC symbols are conventionally upper
    # but some CIViC entries arrive in non-canonical case).
    if qg.casefold() == cg.casefold() and qv.casefold() == cv.casefold():
        return True

    # ── Pan-fusion-query path (rule 3) ──
    # Handle separately because it has different gene-match semantics
    # (component-OR-equal) and different variant semantics (any "Fusion"
    # token in cv counts).
    if qv.lower() in _PAN_FUSION_VARIANTS:
        components = split_fusion_components(cg)
        components_upper = {c.upper() for c in components}
        gene_matches = qg in components_upper or qg == cg.upper()
        if gene_matches:
            # If the CIViC gene itself is a fusion symbol, that is by
            # definition a fusion entry — the gene field already encodes
            # the rearrangement.
            if len(components) >= 2:
                return True
            # Single-gene CIViC entry: require an explicit "Fusion" token
            # in the variant string.
            if _has_fusion_token(cv):
                return True
        return False

    # ── Rule 2: fusion-component + variant-in-profile ──
    components = split_fusion_components(cg)
    if len(components) >= 2:
        components_upper = {c.upper() for c in components}
        if qg in components_upper:
            cv_tokens = _tokenize(cv)
            if qv in cv_tokens:
                return True
            # Also tolerate case-insensitive token match for descriptors
            # like "Exon 19 deletion" where capitalisation may drift.
            qv_lower = qv.lower()
            if any(t.lower() == qv_lower for t in cv_tokens):
                return True

    # ── No rule matched ──
    return False
