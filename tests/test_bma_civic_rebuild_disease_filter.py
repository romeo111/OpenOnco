from __future__ import annotations

from pathlib import Path

import yaml

from knowledge_base.engine.actionability_types import (
    ActionabilityQuery,
    ActionabilityResult,
)
from scripts import reconstruct_bma_evidence_via_civic as rebuild


class _Client:
    def lookup(self, query: ActionabilityQuery):
        return ActionabilityResult(
            query=query,
            source_url="https://civicdb.org/",
            therapeutic_options=(),
            cached=True,
        )


def _civic_item(evidence_id: int, disease: str) -> dict:
    return {
        "id": evidence_id,
        "gene": "BRAF",
        "variant": "V600E",
        "disease": disease,
        "evidence_level": "A",
        "evidence_type": "Predictive",
        "evidence_direction": "Supports",
        "significance": "Sensitivity/Response",
        "therapies": ["Cetuximab"],
    }


def test_process_bma_filters_civic_matches_by_bma_disease():
    scratch_dir = Path(__file__).resolve().parents[1] / ".tmp"
    scratch_dir.mkdir(exist_ok=True)
    bma_path = scratch_dir / "test-bma-disease-filter.yaml"
    bma_path.write_text(
        yaml.safe_dump(
            {
                "id": "BMA-BRAF-V600E-CRC",
                "biomarker_id": "BIO-BRAF-V600E",
                "disease_id": "DIS-CRC",
                "escat_tier": "IA",
                "evidence_sources": [],
                "actionability_review_required": False,
                "evidence_summary": "Test.",
                "primary_sources": ["SRC-NCCN-CRC-2026"],
                "last_verified": "2026-05-06",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    try:
        outcome = rebuild.process_bma(
            bma_path,
            {"BIO-BRAF-V600E": ("BRAF", "V600E")},
            {
                "DIS-CRC": {
                    "id": "DIS-CRC",
                    "names": {"english": "Colorectal carcinoma", "synonyms": []},
                }
            },
            [
                _civic_item(101, "Melanoma"),
                _civic_item(202, "Colorectal Cancer"),
            ],
            _Client(),
            dry_run=False,
        )

        data = yaml.safe_load(bma_path.read_text(encoding="utf-8"))
        civic_refs = [
            ref for ref in data["evidence_sources"] if ref["source"] == "SRC-CIVIC"
        ]

        assert outcome.civic_entries_added == 1
        assert len(civic_refs) == 1
        assert civic_refs[0]["evidence_ids"] == ["202"]
        assert civic_refs[0]["evidence_lane"] == "standard_care"
    finally:
        if bma_path.exists():
            bma_path.unlink()


def test_process_bma_reports_skip_when_only_other_disease_matches():
    scratch_dir = Path(__file__).resolve().parents[1] / ".tmp"
    scratch_dir.mkdir(exist_ok=True)
    bma_path = scratch_dir / "test-bma-disease-skip.yaml"
    bma_path.write_text(
        yaml.safe_dump(
            {
                "id": "BMA-BRAF-V600E-CRC",
                "biomarker_id": "BIO-BRAF-V600E",
                "disease_id": "DIS-CRC",
                "escat_tier": "IA",
                "evidence_sources": [],
                "actionability_review_required": False,
                "evidence_summary": "Test.",
                "primary_sources": ["SRC-NCCN-CRC-2026"],
                "last_verified": "2026-05-06",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    try:
        outcome = rebuild.process_bma(
            bma_path,
            {"BIO-BRAF-V600E": ("BRAF", "V600E")},
            {
                "DIS-CRC": {
                    "id": "DIS-CRC",
                    "names": {"english": "Colorectal carcinoma", "synonyms": []},
                }
            },
            [_civic_item(101, "Melanoma")],
            _Client(),
            dry_run=True,
        )

        assert outcome.skip_reason == "civic_no_disease_matched_evidence"
        assert outcome.civic_entries_added == 0
    finally:
        if bma_path.exists():
            bma_path.unlink()
