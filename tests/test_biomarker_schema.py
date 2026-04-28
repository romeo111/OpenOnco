"""Biomarker schema — actionability-wiring fields.

Renamed/updated during the CIViC pivot (see
docs/reviews/oncokb-public-civic-coverage-2026-04-27.md). Covers the
three optional fields:

  - `actionability_lookup` (was `oncokb_lookup`): explicit (gene, variant) hint
  - `oncokb_skip_reason`: stable machine-readable exclusion token
    (field name preserved — tokens are source-agnostic)
  - `external_ids`: cross-refs to HGNC / OncoKB / CIViC / ClinGen

Phase 1.5 will migrate the YAML field name from `oncokb_lookup` →
`actionability_lookup`; the schema field has already been renamed.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from knowledge_base.schemas import Biomarker
from knowledge_base.schemas.biomarker import (
    ActionabilityLookupHint,
    BiomarkerExternalIDs,
)


def _make(**overrides):
    """Minimal valid Biomarker for the tests below."""
    base = dict(
        id="BIO-TEST",
        names={"preferred": "Test biomarker"},
    )
    base.update(overrides)
    return Biomarker.model_validate(base)


# ── Valid: each new field on its own ──────────────────────────────────────────


def test_biomarker_with_actionability_lookup_only():
    b = _make(
        actionability_lookup={"gene": "BRAF", "variant": "V600E"},
    )
    assert isinstance(b.actionability_lookup, ActionabilityLookupHint)
    assert b.actionability_lookup.gene == "BRAF"
    assert b.actionability_lookup.variant == "V600E"
    assert b.oncokb_skip_reason is None


def test_biomarker_with_oncokb_skip_reason_only():
    b = _make(oncokb_skip_reason="ihc_no_variant")
    assert b.oncokb_skip_reason == "ihc_no_variant"
    assert b.actionability_lookup is None


def test_biomarker_with_neither_lookup_nor_skip_reason():
    """Current state of all 85 bio_*.yaml files — must remain valid."""
    b = _make()
    assert b.actionability_lookup is None
    assert b.oncokb_skip_reason is None
    assert b.external_ids is None


# ── Variant string flexibility (schema only type-checks; engine normalizes) ──


@pytest.mark.parametrize(
    "variant",
    [
        "V600E",            # short HGVS-p
        "L858R",
        "G12C",
        "Exon 19 deletion",  # structured descriptor
        "E746_A750del",      # multi-residue deletion
        "W288fs",            # frameshift
    ],
)
def test_actionability_lookup_accepts_canonical_variant_strings(variant):
    b = _make(actionability_lookup={"gene": "EGFR", "variant": variant})
    assert b.actionability_lookup.variant == variant


# ── Mutual exclusion ──────────────────────────────────────────────────────────


def test_both_actionability_lookup_and_skip_reason_rejected():
    with pytest.raises(ValidationError) as exc:
        _make(
            actionability_lookup={"gene": "BRAF", "variant": "V600E"},
            oncokb_skip_reason="fusion_mvp",
        )
    msg = str(exc.value)
    assert "actionability_lookup" in msg and "oncokb_skip_reason" in msg


# ── Skip-reason enum guard ────────────────────────────────────────────────────


def test_invalid_oncokb_skip_reason_rejected():
    with pytest.raises(ValidationError):
        _make(oncokb_skip_reason="not_a_real_reason")


@pytest.mark.parametrize(
    "reason",
    [
        "ihc_no_variant",
        "score",
        "clinical_composite",
        "serological",
        "viral_load",
        "tumor_marker",
        "imaging",
        "germline_no_somatic",
        "fusion_mvp",
        "itd_mvp",
        "multi_allele_mvp",
        "tumor_agnostic",
    ],
)
def test_all_documented_skip_reasons_accepted(reason):
    """Stable tokens — downstream code greps these strings, so the
    schema enum and the documented set must stay in lockstep."""
    b = _make(oncokb_skip_reason=reason)
    assert b.oncokb_skip_reason == reason


# ── external_ids partial keys ─────────────────────────────────────────────────


def test_external_ids_with_partial_keys():
    b = _make(
        external_ids={
            "hgnc_symbol": "BRAF",
            "oncokb_url": "https://oncokb.org/gene/BRAF/V600E",
        }
    )
    assert isinstance(b.external_ids, BiomarkerExternalIDs)
    assert b.external_ids.hgnc_symbol == "BRAF"
    assert b.external_ids.oncokb_url == "https://oncokb.org/gene/BRAF/V600E"
    # Other keys remain None
    assert b.external_ids.civic_id is None
    assert b.external_ids.clingen_id is None
    assert b.external_ids.hgvs_protein is None


def test_external_ids_with_all_keys():
    b = _make(
        external_ids={
            "hgnc_symbol": "EGFR",
            "hgnc_id": "HGNC:3236",
            "oncokb_url": "https://oncokb.org/gene/EGFR/L858R",
            "civic_id": "33",
            "civic_url": "https://civicdb.org/links/variants/33",
            "clingen_id": "CA123456",
            "hgvs_protein": "NP_005219.2:p.Leu858Arg",
            "hgvs_coding": "NM_005228.5:c.2573T>G",
        }
    )
    assert b.external_ids.hgnc_id == "HGNC:3236"
    assert b.external_ids.civic_id == "33"
    assert b.external_ids.hgvs_coding == "NM_005228.5:c.2573T>G"


def test_external_ids_coexists_with_oncokb_lookup():
    """external_ids is independent of the lookup/skip XOR."""
    b = _make(
        oncokb_lookup={"gene": "BRAF", "variant": "V600E"},
        external_ids={"hgnc_symbol": "BRAF"},
    )
    assert b.oncokb_lookup is not None
    assert b.external_ids.hgnc_symbol == "BRAF"


def test_external_ids_coexists_with_skip_reason():
    b = _make(
        oncokb_skip_reason="ihc_no_variant",
        external_ids={"hgnc_symbol": "MKI67"},
    )
    assert b.oncokb_skip_reason == "ihc_no_variant"
    assert b.external_ids.hgnc_symbol == "MKI67"
