"""Smoke tests for scripts/oncokb_coverage_report.py.

Not exhaustive — the script is observability infra, not engine code.
We verify it runs cleanly against the real KB + the report shape is sane."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "oncokb_coverage_report.py"


def test_text_report_runs_and_mentions_diseases():
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT)],
        capture_output=True,
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    assert "Total diseases:" in proc.stdout
    assert "tier-1 explicit:" in proc.stdout
    assert "Biomarker references:" in proc.stdout


def test_json_report_parses():
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--json"],
        capture_output=True,
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert "diseases" in data
    assert isinstance(data["diseases"], list)
    assert len(data["diseases"]) > 0

    # Every entry has the expected fields
    sample = data["diseases"][0]
    for k in (
        "disease_id", "name_en", "icd_10", "oncotree_explicit",
        "final_oncotree_code", "pan_tumor_warning",
        "referenced_biomarker_ids", "referenced_biomarkers_with_hint",
        "indications_count",
    ):
        assert k in sample, f"missing field {k}"


def test_warn_flag_succeeds_when_all_diseases_have_oncotree_codes():
    """Currently all 65 KB diseases have explicit oncotree_code (PR-B done).
    --warn should exit 0. If a new disease lands without a code,
    this will surface as a CI warning."""
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--warn"],
        capture_output=True,
        text=True,
        timeout=120,
        env={"PYTHONIOENCODING": "utf-8", **__import__("os").environ},
    )
    assert proc.returncode == 0, (
        f"--warn flagged pan-tumor diseases (exit {proc.returncode}); "
        f"either populate Disease.oncotree_code or extend oncotree_fallback. "
        f"stderr: {proc.stderr}"
    )
