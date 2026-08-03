"""Safety contracts for ESCAT applicability, readiness, and audit output."""

from __future__ import annotations

from datetime import date

import pytest
import yaml

from knowledge_base.engine._actionability import find_matching_actionability
from knowledge_base.schemas.biomarker_actionability import (
    BiomarkerActionability,
    actionability_release_readiness,
)
from scripts.audit_escat_readiness import audit_escat_readiness


def _ready_bma() -> dict:
    return {
        "id": "BMA-BRAF-V600E-CRC",
        "biomarker_id": "BIO-BRAF-V600E",
        "variant_qualifier": "V600E",
        "disease_id": "DIS-CRC",
        "actionability_scope": "therapeutic_predictive",
        "escat_applicability": "applicable",
        "escat_tier": "IC",
        "escat_evidence_dossier": {
            "assessment_status": "clinically_reviewed",
            "tier_rationale": "Clinician-reviewed, source-linked rationale.",
            "evidence_records": [{
                "source": "SRC-ESMO",
                "therapy_context": "targeted therapy",
                "tumour_context": "colorectal cancer",
                "study_design": "basket_trial",
            }],
        },
        "evidence_sources": [{"source": "SRC-ESMO", "level": "I"}],
        "evidence_summary": "Test context only.",
        "primary_sources": ["SRC-ESMO"],
        "last_verified": "2026-08-03",
        "reviewer_signoffs": [
            {"reviewer_id": "REV-ONE", "timestamp": "2026-08-03T00:00:00Z", "entity_version": "2026-08-03", "scope_match": True},
            {"reviewer_id": "REV-TWO", "timestamp": "2026-08-03T00:00:00Z", "entity_version": "2026-08-03", "scope_match": True},
        ],
    }


@pytest.mark.parametrize("tier", ["IA", "IB", "IC", "IIA", "IIB", "IIIA", "IIIB", "IVA", "IVB", "V", "X"])
def test_full_escat_vocabulary_is_accepted(tier: str):
    data = _ready_bma()
    data["escat_tier"] = tier
    assert BiomarkerActionability.model_validate(data).escat_tier == tier


def test_not_applicable_record_cannot_keep_a_tier():
    data = _ready_bma()
    data.update({
        "actionability_scope": "surveillance",
        "escat_applicability": "not_applicable",
        "escat_non_applicable_reason": "Surveillance marker, not an alteration-drug claim.",
    })
    with pytest.raises(ValueError, match="must not carry escat_tier"):
        BiomarkerActionability.model_validate(data)


def test_release_gate_requires_current_distinct_signoffs():
    data = _ready_bma()
    assert actionability_release_readiness(data).ready is True
    data["reviewer_signoffs"][1]["entity_version"] = "2026-08-02"
    result = actionability_release_readiness(data)
    assert result.ready is False
    assert "fewer than two current" in result.reasons[-1]


def test_variant_matching_exposes_unready_status_without_selecting_tracks():
    data = _ready_bma()
    data.update({"actionability_scope": "unclassified", "escat_applicability": "review_required"})
    hit = find_matching_actionability(
        {"BRAF": "V600E"},
        "DIS-CRC",
        {data["id"]: {"type": "biomarker_actionability", "data": data}},
    )[0]
    assert hit["clinical_use_ready"] is False
    assert hit["escat_tier"] == "IC"


def test_audit_emits_evidence_and_snapshot_queue(tmp_path):
    bma_dir = tmp_path / "bma"
    bio_dir = tmp_path / "bio"
    civic_root = tmp_path / "civic"
    bma_dir.mkdir()
    bio_dir.mkdir()
    (civic_root / "2026-06-01").mkdir(parents=True)
    (bma_dir / "bma.yaml").write_text(yaml.safe_dump({
        "id": "BMA-BRAF-V600K-CRC",
        "biomarker_id": "BIO-BRAF-V600E",
        "variant_qualifier": "V600K",
        "disease_id": "DIS-CRC",
        "escat_tier": "IA",
        "evidence_summary": "Context only.",
        "primary_sources": ["SRC-TEST"],
        "last_verified": "2026-06-01",
    }, sort_keys=False), encoding="utf-8")
    (bio_dir / "bio.yaml").write_text(yaml.safe_dump({
        "id": "BIO-BRAF-V600E",
        "actionability_lookup": {"variant": "V600E"},
    }, sort_keys=False), encoding="utf-8")
    (civic_root / "2026-06-01" / "evidence.yaml").write_text(
        yaml.safe_dump({"evidence_items": []}, sort_keys=False), encoding="utf-8"
    )

    report = audit_escat_readiness(
        bma_dir=bma_dir,
        biomarker_dir=bio_dir,
        civic_root=civic_root,
        manifest=tmp_path / "manifest.txt",
        as_of=date(2026, 8, 3),
        max_snapshot_age_days=45,
    )
    assert report["issues_by_code"]["missing_evidence_sources"] == 1
    assert report["issues_by_code"]["biomarker_taxonomy_mismatch"] == 1
    assert report["issues_by_code"]["civic_snapshot_stale"] == 1
