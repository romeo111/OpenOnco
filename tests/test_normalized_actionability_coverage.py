from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.normalized_actionability_coverage import build_fill_backlog, build_report


_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "normalized_actionability_coverage.py"


def test_build_report_collapses_nsclc_variant_families():
    rows = {row.disease_id: row for row in build_report()}
    nsclc = rows["DIS-NSCLC"]
    assert nsclc.bma_total > nsclc.normalized_family_count
    assert nsclc.bma_variant_inflation_ratio is not None
    assert nsclc.bma_variant_inflation_ratio > 1.0
    assert nsclc.unique_drug_count > 0
    assert nsclc.indications > 0


def test_json_cli_parses_and_exposes_normalized_fields():
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--json"],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert "diseases" in data
    nsclc = next(row for row in data["diseases"] if row["disease_id"] == "DIS-NSCLC")
    assert nsclc["bma_total"] > nsclc["normalized_family_count"]
    assert "bma_variant_inflation_ratio" in nsclc
    assert "standard_family_count" in nsclc


def test_markdown_cli_mentions_variant_inflation():
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT)],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    assert "Normalized Actionability Coverage" in proc.stdout
    assert "Variant Inflation Flags" in proc.stdout
    assert "DIS-NSCLC" in proc.stdout


def test_fill_backlog_freezes_nsclc_and_prioritizes_active_gaps():
    backlog = build_fill_backlog(build_report())
    by_id = {row.disease_id: row for row in backlog}
    nsclc = by_id["DIS-NSCLC"]
    assert nsclc.tier == "freeze_expand"
    assert nsclc.workflow_lane == "freeze_expand"
    assert nsclc.score == 0
    assert "Freeze expansion" in nsclc.recommended_chunk
    endometrial = by_id["DIS-ENDOMETRIAL"]
    assert endometrial.workflow_lane == "fill_first"
    assert endometrial.review_readiness_pct == 44.0
    gbm = by_id["DIS-GBM"]
    assert gbm.current_regimens == 1
    assert gbm.regimen_gap == 7
    assert "missing_regimen_records" in gbm.quality_flags
    esophageal = by_id["DIS-ESOPHAGEAL"]
    assert esophageal.review_readiness_pct == 100.0
    assert esophageal.workflow_lane == "fill_first"
    assert esophageal.score == 0
    assert "missing_regimen_records" in esophageal.quality_flags
    assert "linked regimen records" in esophageal.recommended_chunk
    assert any(row.score > 0 for row in backlog)
    assert any(row.workflow_lane == "review_ready" for row in backlog)


def test_rank_fill_next_cli_outputs_backlog():
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--rank-fill-next"],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    assert "Normalized Coverage Fill Backlog" in proc.stdout
    assert "Highest Priority Fill Chunks" in proc.stdout
    assert "Freeze Expansion" in proc.stdout


def test_rank_fill_next_json_cli_parses():
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--rank-fill-next", "--json"],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert "fill_backlog" in data
    nsclc = next(row for row in data["fill_backlog"] if row["disease_id"] == "DIS-NSCLC")
    assert nsclc["tier"] == "freeze_expand"
    assert "workflow_lane" in nsclc
    assert "review_readiness_pct" in nsclc


def test_rank_fill_next_can_filter_review_ready_lane():
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--rank-fill-next",
            "--workflow-lane",
            "review_ready",
            "--top",
            "5",
            "--compact-json",
        ],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["fill_backlog"]
    assert all(row["workflow_lane"] == "review_ready" for row in data["fill_backlog"])
    assert all(row["review_readiness_pct"] >= 80.0 for row in data["fill_backlog"])
    assert all("missing_regimen_records" not in row["flags"] for row in data["fill_backlog"])


def test_top_disease_compact_json_filters_to_one_disease():
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--rank-fill-next",
            "--disease",
            "DIS-ENDOMETRIAL",
            "--compact-json",
        ],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert len(data["fill_backlog"]) == 1
    row = data["fill_backlog"][0]
    assert row["disease_id"] == "DIS-ENDOMETRIAL"
    assert "gaps" in row
    assert "current" in row
    assert "recommended_chunk" not in row


def test_tier_filter_and_top_limit():
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--rank-fill-next",
            "--tier",
            "major_solid",
            "--top",
            "2",
            "--json",
        ],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert len(data["fill_backlog"]) == 2
    assert {row["tier"] for row in data["fill_backlog"]} == {"major_solid"}


def test_chunk_specs_cli_is_compact_and_non_authoring():
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--chunk-specs", "--top", "2"],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    assert "Generated Normalized Fill Chunk Specs" in proc.stdout
    assert proc.stdout.count("## Chunk") == 2
    assert "Do not author clinical claims" in proc.stdout
    assert "--compact-json" in proc.stdout
    assert "--inventory-disease" in proc.stdout


def test_inventory_disease_compact_json_lists_linked_files_and_no_stale_sources_after_cleanup():
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--inventory-disease",
            "DIS-ENDOMETRIAL",
            "--compact-json",
        ],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert len(data["inventories"]) == 1
    inventory = data["inventories"][0]
    assert inventory["disease_id"] == "DIS-ENDOMETRIAL"
    assert inventory["counts"]["bma"] > 0
    assert inventory["counts"]["ind"] > 0
    assert inventory["counts"]["reg"] > 0
    assert inventory["stale_source_ids"] == []
    assert inventory["bma_review_blockers"]["pending_clinical_signoff_count"] == inventory["counts"]["bma"]
    assert "bma_metadata_consistency" in inventory
    dmmr_family = next(item for item in inventory["bma_families"] if item["biomarker_id"] == "BIO-DMMR-IHC")
    assert dmmr_family["count"] == 9
    queue_ids = {item["queue_id"] for item in inventory["bma_review_queue"]}
    assert {"soc_dmmr_family", "intermediate_family_audit", "low_tier_tail"} <= queue_ids


def test_inventory_queue_filters_to_soc_dmmr_family():
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--inventory-disease",
            "DIS-ENDOMETRIAL",
            "--inventory-queue",
            "soc_dmmr_family",
            "--compact-json",
        ],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    inventory = data["inventories"][0]
    assert inventory["counts"]["bma"] == 9
    assert len(inventory["bma_review_queue"]) == 1
    assert inventory["bma_review_queue"][0]["queue_id"] == "soc_dmmr_family"
    assert {item["biomarker_id"] for item in inventory["bma_families"]} == {"BIO-DMMR-IHC"}


def test_inventory_queue_intermediate_family_is_metadata_clean_after_normalization():
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--inventory-disease",
            "DIS-ENDOMETRIAL",
            "--inventory-queue",
            "intermediate_family_audit",
            "--compact-json",
        ],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    inventory = data["inventories"][0]
    consistency = inventory["bma_metadata_consistency"]
    assert inventory["counts"]["bma"] == 3
    assert consistency["missing_contraindicated_monotherapy_count"] == 0
    assert consistency["guideline_evidence_order_mismatch_count"] == 0
    assert consistency["metadata_ready_count"] == 3


def test_review_packet_compact_json_for_soc_dmmr_family():
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--review-packet",
            "--inventory-disease",
            "DIS-ENDOMETRIAL",
            "--inventory-queue",
            "soc_dmmr_family",
            "--compact-json",
        ],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert len(data["review_packets"]) == 1
    packet = data["review_packets"][0]
    assert packet["queue"]["queue_id"] == "soc_dmmr_family"
    assert packet["counts"]["bma"] == 9
    assert packet["metadata_consistency"]["metadata_ready_count"] == 9
    assert packet["shared_primary_sources"] == ["SRC-ESGO-ENDOMETRIAL-2025", "SRC-NCCN-UTERINE-2025"]
    assert len(packet["records"]) == 9
    assert all("primary_sources" in item for item in packet["records"])


def test_hnscc_inventory_regimen_wiring_is_clean_after_source_backfill():
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--inventory-disease",
            "DIS-HNSCC",
            "--compact-json",
        ],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    inventory = data["inventories"][0]
    consistency = inventory["regimen_wiring_consistency"]
    assert consistency["missing_regimen_record_count"] == 0
    assert consistency["regimens_missing_sources_count"] == 0
    assert "REG-NIVOLUMAB-MONO" in consistency["wired_regimen_ids"]
    assert "REG-PEMBROLIZUMAB-MONO" in consistency["wired_regimen_ids"]


def test_rcc_and_hcc_inventories_regimen_wiring_are_clean_after_source_backfill():
    for disease_id, expected_regimen in (
        ("DIS-RCC", "REG-PEMBROLIZUMAB-MONO"),
        ("DIS-HCC", "REG-CABOZANTINIB-HCC"),
    ):
        proc = subprocess.run(
            [
                sys.executable,
                str(_SCRIPT),
                "--inventory-disease",
                disease_id,
                "--compact-json",
            ],
            capture_output=True,
            encoding="utf-8",
            text=True,
            timeout=120,
            env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
        )
        assert proc.returncode == 0, proc.stderr
        data = json.loads(proc.stdout)
        inventory = data["inventories"][0]
        consistency = inventory["regimen_wiring_consistency"]
        assert consistency["missing_regimen_record_count"] == 0
        assert consistency["regimens_missing_sources_count"] == 0
        assert expected_regimen in consistency["wired_regimen_ids"]


def test_gbm_inventory_exposes_missing_regimen_records():
    proc = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            "--inventory-disease",
            "DIS-GBM",
            "--compact-json",
        ],
        capture_output=True,
        encoding="utf-8",
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    inventory = data["inventories"][0]
    consistency = inventory["regimen_wiring_consistency"]
    assert consistency["missing_regimen_record_count"] == 3
    assert set(consistency["missing_regimen_record_ids"]) == {
        "REG-BEVACIZUMAB-GBM",
        "REG-HYPOFRACTIONATED-RT-GBM",
        "REG-TMZ-MONO",
    }
