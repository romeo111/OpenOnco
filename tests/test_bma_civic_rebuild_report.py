from __future__ import annotations

from pathlib import Path

from scripts import reconstruct_bma_evidence_via_civic as rebuild


def test_rebuild_report_includes_lane_column(monkeypatch):
    scratch_dir = Path(__file__).resolve().parents[1] / ".tmp"
    scratch_dir.mkdir(exist_ok=True)
    report_path = scratch_dir / "test-bma-civic-rebuild.md"
    monkeypatch.setattr(rebuild, "REPORT_PATH", report_path)

    try:
        rebuild.write_report(
            [
                rebuild.BMAOutcome(
                    bma_id="BMA-BRAF-V600E-MELANOMA",
                    biomarker_id="BIO-BRAF-V600E",
                    gene="BRAF",
                    variant="V600E",
                    disease_id="DIS-MELANOMA",
                    skip_reason=None,
                    civic_entries_added=0,
                    civic_entries_total=1,
                    civic_levels_present=("A",),
                    has_resistance=False,
                    legacy_oncokb_level=None,
                    review_required=True,
                    file_modified=False,
                    lanes_present=("molecular_evidence_option",),
                )
            ],
            dry_run=True,
        )

        markdown = report_path.read_text(encoding="utf-8")
        assert (
            "| BMA-ID | biomarker | (gene, variant) | CIViC entries (total) | "
            "added this run | levels | lanes | resistance | review_required |"
        ) in markdown
        assert "molecular_evidence_option" in markdown
    finally:
        if report_path.exists():
            report_path.unlink()
