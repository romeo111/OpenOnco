"""Filter algorithm output_indications by biomarker exclusion.

Lenient mode: only drop tracks where the patient profile EXPLICITLY
violates an Indication's `applicable_to.biomarker_requirements_excluded`.
Missing or unknown biomarkers do NOT drop a track — patient profiles are
typically incomplete (some biomarkers not yet tested), and strict
filtering would over-prune and hide options the clinician should see.

This is a render-time / track-materialization filter, not a clinical
selection signal. It removes tracks that are clinically inapplicable
because the patient explicitly carries an excluded marker
(e.g. KRAS-G12C-specific track + patient with BRAF V600E + KRAS WT
should not see the KRAS-G12C track if KRAS-WT is on the exclusion list).

Schema reference (see `schemas/indication.py`):

    applicable_to:
      biomarker_requirements_excluded:
        - biomarker_id: BIO-MSI-STATUS
          value_constraint: "MSI-H"        # free-form text
        - biomarker_id: BIO-BRAF-V600E
          value_constraint: "positive"

The matcher uses lenient gene-stem extraction (BIO-EGFR-T790M → EGFR)
to bridge patient biomarker dicts that may key by gene name or by full
BIO-id. `_actionability._normalize_gene_stem` covers the same convention.
"""

from __future__ import annotations

from typing import Any

from ._actionability import _extract_variant, _normalize_gene_stem


_NEGATIVE_TOKENS = {
    "negative",
    "neg",
    "absent",
    "wildtype",
    "wild-type",
    "wt",
    "false",
    "0",
    "",
}


def is_track_excluded(indication_data: dict, patient_biomarkers: dict) -> bool:
    """Return True if the patient profile EXPLICITLY violates this
    indication's `biomarker_requirements_excluded` list.

    Lenient: missing biomarkers do not drop the track.

    Args:
        indication_data: parsed Indication YAML dict (top-level — we read
            its `applicable_to` subdict). Tolerates `None`/non-dict.
        patient_biomarkers: patient.biomarkers dict (gene name or
            BIO-id → value/status). Tolerates `None`.
    """
    if not isinstance(indication_data, dict):
        return False
    if not patient_biomarkers:
        return False

    applicable = indication_data.get("applicable_to") or {}
    excluded = applicable.get("biomarker_requirements_excluded") or []
    if not excluded:
        return False  # no exclusions → never drop

    for excl in excluded:
        if isinstance(excl, dict):
            bio_id = excl.get("biomarker_id")
        elif isinstance(excl, str):
            bio_id = excl
        else:
            continue
        if not bio_id:
            continue

        gene_stem = _normalize_gene_stem(bio_id)

        # Find the patient's value, trying multiple key shapes
        patient_value = _lookup_patient_value(
            patient_biomarkers, bio_id, gene_stem
        )
        if patient_value is None:
            continue  # missing → don't drop (lenient)

        if _matches_excluded_value(patient_value, excl):
            return True

    return False


def _lookup_patient_value(
    patient_biomarkers: dict, bio_id: str, gene_stem: str
) -> Any:
    """Find a patient's value for a biomarker by trying multiple key shapes.

    Returns None when the patient has not reported anything for this
    biomarker (lenient — caller will skip).

    Tries (case-insensitively):
      - exact bio_id match (`BIO-MSI-STATUS`)
      - bio_id with `BIO-` prefix stripped (`MSI-STATUS`)
      - the gene stem alone (`MSI`)
    """
    if bio_id in patient_biomarkers:
        return patient_biomarkers[bio_id]
    if gene_stem and gene_stem in patient_biomarkers:
        return patient_biomarkers[gene_stem]

    # Build candidate keys (uppercase, normalized) for case-insensitive scan.
    candidates = {bio_id.upper(), (gene_stem or "").upper()}
    bio_stripped = bio_id.upper()
    if bio_stripped.startswith("BIO-"):
        bio_stripped = bio_stripped[4:]
    candidates.add(bio_stripped)
    candidates.discard("")

    for k, v in patient_biomarkers.items():
        if not isinstance(k, str):
            continue
        ku = k.strip().upper()
        if ku in candidates:
            return v
        # Patient may use BIO- prefix too — strip and re-compare
        ku_stripped = ku[4:] if ku.startswith("BIO-") else ku
        if ku_stripped in candidates:
            return v
    return None


def _matches_excluded_value(patient_value: Any, exclusion_spec: Any) -> bool:
    """Return True iff the patient's reported value matches the
    exclusion spec.

    `exclusion_spec` can be:
      - a plain string biomarker_id (any non-negative value excludes), or
      - a dict with `biomarker_id` and optional `value_constraint`,
        `value`, or `values`.

    The match for free-form `value_constraint` text is a case-insensitive
    substring check both directions (mirrors `_actionability._variant_matches`),
    so "MSI-H" in spec matches patient_value "MSI-H" or "MSI-High".
    """
    # Normalize patient value to a comparable string (or detect negative)
    variant = _extract_variant(patient_value)
    if variant is None:
        # Patient explicitly negative / wildtype → not an exclusion match
        return False

    if isinstance(exclusion_spec, str):
        # Plain biomarker_id only — any positive presence excludes.
        return True

    if not isinstance(exclusion_spec, dict):
        return False

    # Collect candidate "exclusion values" from the spec
    expected_values: list[str] = []
    for key in ("value_constraint", "value"):
        v = exclusion_spec.get(key)
        if isinstance(v, str) and v.strip():
            expected_values.append(v)
    raw_values = exclusion_spec.get("values")
    if isinstance(raw_values, list):
        for v in raw_values:
            if isinstance(v, str) and v.strip():
                expected_values.append(v)

    if not expected_values:
        # No specific value qualifier — any positive presence excludes.
        return True

    pv = (variant or "").strip().lower()
    if not pv:
        # Patient is gene-level positive (no specific variant string), but
        # the exclusion is qualified by a value_constraint. The patient has
        # not reported the qualifying condition, so don't drop the track —
        # consistent with the file's "missing biomarkers do not drop a
        # track" stance. The clinician decides on the more nuanced data.
        return False

    for expected in expected_values:
        ev = expected.strip().lower()
        if not ev:
            continue
        if ev in pv or pv in ev:
            return True
        # Token-level match for things like "MSI-H" vs "MSI-High"
        ev_tokens = {t for t in ev.replace(",", " ").split() if t}
        pv_tokens = {t for t in pv.replace(",", " ").split() if t}
        if ev_tokens and pv_tokens and ev_tokens & pv_tokens:
            return True

    return False


__all__ = ["is_track_excluded"]
