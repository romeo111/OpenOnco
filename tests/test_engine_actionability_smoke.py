"""Smoke test for the variant-actionability lookup wired into
generate_plan. Validates that a synthetic mCRC patient with a BRAF
V600E variant resolves to the BMA-BRAF-V600E-CRC actionability cell
with the expected ESCAT tier.

CSD-1 prep: the partnership pitch demonstrates that an NGS
report → tumor-board brief flow surfaces ESMO-grade clinical context
next to the chosen track. This test is the engine's side of that
integration; downstream CSD-1-tests adds 5 known-case fixtures,
CSD-1-demo packages the BRAF-V600E mCRC pitch HTML.

Phase 1 of the CIViC pivot dropped the per-test `oncokb_level` check —
that field is gone from VariantActionabilityHit. Phase 1.5 will
populate `evidence_sources` for this BMA cell and the assertion
re-tightens to "exactly one CIViC entry at level A".
"""

from __future__ import annotations

from pathlib import Path

from knowledge_base.engine import generate_plan


REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"


def test_braf_v600e_mcrc_actionability_lookup():
    """Synthetic mCRC + BRAF V600E patient → exactly one BMA hit
    (BMA-BRAF-V600E-CRC), ESCAT IB. No warnings on the actionability
    path."""
    patient = {
        "patient_id": "TEST-CRC-BRAF-001",
        "disease": {"id": "DIS-CRC"},
        "line_of_therapy": 1,
        "biomarkers": {"BRAF": "V600E"},
    }

    result = generate_plan(patient, kb_root=KB_ROOT)

    assert result.disease_id == "DIS-CRC"
    assert result.plan is not None, "Plan should be generated for mCRC 1L"
    assert not [w for w in result.warnings if "actionability" in w.lower()], (
        f"actionability lookup should not warn: {result.warnings}"
    )

    hits = result.plan.variant_actionability
    assert len(hits) == 1, f"Expected exactly one BMA hit, got {len(hits)}: {hits}"

    h = hits[0]
    assert h.bma_id == "BMA-BRAF-V600E-CRC"
    assert h.biomarker_id == "BIO-BRAF-V600E"
    assert h.escat_tier == "IB"
    assert "encorafenib" in " ".join(h.recommended_combinations).lower()
    assert h.primary_sources, "primary_sources should be non-empty"
