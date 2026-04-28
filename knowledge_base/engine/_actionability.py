"""Variant actionability lookup — match patient biomarkers to
BiomarkerActionability cells (ESCAT) for a given disease.

Render-time metadata only. The engine MUST NOT consult these tier
assignments as a treatment-selection signal — that would replicate the
LLM-ranks-treatments anti-pattern (CHARTER §8.3). Tracks come from the
declarative Algorithm; this module surfaces parallel ESCAT
context next to the chosen track for tumor-board discussion.

Patient `biomarkers` may take several shapes (the ingestion path varies):

    {"BRAF": "V600E"}                   # gene-name → variant string
    {"BIO-BRAF-V600E": True}            # BIO-id flag (already-resolved)
    {"BIO-BRAF-V600E": "positive"}      # BIO-id with positive value
    {"EGFR": {"variant": "T790M", ...}} # nested dict (NGS report ingest)

Matching rules (case-insensitive throughout):

  1. **Biomarker key match.** A patient key matches a BMA cell when:
     - patient key equals the cell.biomarker_id exactly, or
     - the patient key (uppercased gene stem like "BRAF") appears as a
       token inside cell.biomarker_id (e.g. "BIO-BRAF-V600E"), or
     - cell.biomarker_id (after stripping the "BIO-" prefix) starts with
       the patient gene stem.

  2. **Disease match.** Cell.disease_id must equal patient.disease_id
     (BMA cells are tumor-specific by construction).

  3. **Variant qualifier match.** Given the patient's variant value
     (`patient_variant`):
     - If `cell.variant_qualifier` is None / empty: match (gene-level
       cell — any pathogenic alteration of that gene applies).
     - Otherwise: case-insensitive substring match in either direction
       (patient_variant in qualifier OR qualifier in patient_variant).
       This handles "p.V600E" vs "V600E" vs "V600E (somatic)" gracefully.

The matcher is deliberately lenient — false positives surface as a row
in the actionability table for HCP review; false negatives silently drop
clinically relevant context. Lenient matching, with the cell's full
evidence_summary in the rendered table, gives the HCP enough to
disambiguate.
"""

from __future__ import annotations

from typing import Any, Optional


def _normalize_gene_stem(key: str) -> str:
    """Extract the gene-symbol stem from a patient biomarker key.

    Examples:
        "BRAF"            → "BRAF"
        "braf"            → "BRAF"
        "BIO-BRAF-V600E"  → "BRAF"
        "BIO-EGFR-T790M"  → "EGFR"
    """
    if not key:
        return ""
    raw = str(key).strip().upper()
    if raw.startswith("BIO-"):
        raw = raw[4:]
    # First hyphen-segment is the gene symbol in BIO-* convention.
    return raw.split("-", 1)[0]


def _extract_variant(value: Any) -> Optional[str]:
    """Pull a variant string out of a heterogeneous patient biomarker value.

    Returns None when the value is a falsy/negative flag (so the caller
    can skip the lookup entirely)."""
    if value is None or value is False:
        return None
    if value is True:
        return ""  # gene-level positive — match any cell for this gene
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return None
        if s.lower() in {"negative", "neg", "absent", "wildtype", "wild-type", "wt", "false", "0"}:
            return None
        # "positive"/"present" with no specific variant → gene-level
        if s.lower() in {"positive", "pos", "present", "mutated", "mut", "amplified", "high"}:
            return ""
        return s
    if isinstance(value, dict):
        for k in ("variant", "qualifier", "hgvs", "hgvs_protein", "value"):
            v = value.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
        # status-only nested dict
        st = value.get("status")
        if isinstance(st, str):
            return _extract_variant(st)
        return ""
    # numeric / other → coerce
    return str(value)


def _biomarker_keys_match(patient_key: str, cell_biomarker_id: str) -> bool:
    """Does this patient biomarker key correspond to this BMA cell's biomarker?"""
    if not patient_key or not cell_biomarker_id:
        return False
    pk = str(patient_key).strip().upper()
    bid = str(cell_biomarker_id).strip().upper()
    if pk == bid:
        return True
    stem = _normalize_gene_stem(pk)
    bid_stripped = bid[4:] if bid.startswith("BIO-") else bid
    if not stem:
        return False
    # Token match: BIO-BRAF-V600E contains "BRAF" segment
    bid_tokens = bid_stripped.split("-")
    if stem in bid_tokens:
        return True
    # Patient key like "BIO-BRAF-V600E" already-resolved
    pk_stripped = pk[4:] if pk.startswith("BIO-") else pk
    if pk_stripped == bid_stripped:
        return True
    return False


def _variant_matches(patient_variant: Optional[str], cell_qualifier: Optional[str]) -> bool:
    """Variant-qualifier matching, case-insensitive substring (both directions).

    - cell_qualifier None/empty → gene-level cell, matches any variant
    - patient_variant empty string → gene-level positive, matches any cell
    - else: case-insensitive substring in either direction
    """
    if not cell_qualifier:
        return True  # gene-level cell
    if patient_variant is None:
        return False
    if patient_variant == "":
        return True  # patient gene-level positive matches any specific cell
    pv = patient_variant.strip().lower()
    cq = cell_qualifier.strip().lower()
    if not pv:
        return True
    if pv == cq:
        return True
    return pv in cq or cq in pv


def find_matching_actionability(
    patient_biomarkers: dict,
    disease_id: str,
    entities_by_id: dict,
) -> list[dict]:
    """Return a list of variant_actionability hit dicts for the patient profile.

    Each hit dict carries the fields needed by both the Plan JSON
    (VariantActionabilityHit schema) and the render layer.
    Order: BMA-id ascending — stable, deterministic for tests.
    """
    if not patient_biomarkers or not disease_id:
        return []

    # Pre-filter the KB to BMA cells for this disease only — the
    # entity store is global and we don't want to scan it once per
    # biomarker key.
    bma_cells: list[dict] = []
    for eid, info in entities_by_id.items():
        if info.get("type") != "biomarker_actionability":
            continue
        data = info.get("data") or {}
        if data.get("disease_id") != disease_id:
            continue
        bma_cells.append(data)

    if not bma_cells:
        return []

    hits: dict[str, dict] = {}  # dedup by bma_id
    for patient_key, raw_value in patient_biomarkers.items():
        patient_variant = _extract_variant(raw_value)
        if patient_variant is None:
            continue  # negative / absent / unparseable → skip
        for cell in bma_cells:
            cell_bid = cell.get("biomarker_id") or ""
            if not _biomarker_keys_match(patient_key, cell_bid):
                continue
            if not _variant_matches(patient_variant, cell.get("variant_qualifier")):
                continue
            bma_id = cell.get("id")
            if not bma_id or bma_id in hits:
                continue
            # `evidence_sources` (Phase 1.5+) carries per-source level
            # attestations. Default empty for back-compat with legacy
            # YAML still using `oncokb_level`; Phase 1.5 migrates the
            # latter into `evidence_sources` entries.
            hits[bma_id] = {
                "bma_id": bma_id,
                "biomarker_id": cell_bid,
                "variant_qualifier": cell.get("variant_qualifier"),
                "escat_tier": cell.get("escat_tier"),
                "evidence_sources": list(cell.get("evidence_sources") or []),
                "evidence_summary": (cell.get("evidence_summary") or "").strip(),
                "recommended_combinations": list(cell.get("recommended_combinations") or []),
                "primary_sources": list(cell.get("primary_sources") or []),
            }

    return [hits[k] for k in sorted(hits.keys())]


__all__ = [
    "find_matching_actionability",
    "_biomarker_keys_match",
    "_variant_matches",
    "_extract_variant",
    "_normalize_gene_stem",
]
