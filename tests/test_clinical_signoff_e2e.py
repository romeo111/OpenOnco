"""End-to-end tests for the clinical sign-off workflow (CSD-5A).

Covers behaviors that the smoke suite (`test_clinical_signoff_smoke.py`)
does NOT exercise:

  Section A — CLI round-trip on a temporary KB
  Section B — CLI validation gates (unknown reviewer, scope mismatch)
  Section C — Dashboard generation from an audit log
  Section D — Render badges (pending / complete) for sign-off state

Every test uses a temp KB / audit log via monkeypatching so the real
production KB and `knowledge_base/hosted/audit/signoffs.jsonl` are
never modified.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import pytest
import yaml

import scripts.clinical_signoff as cli
import scripts.build_signoff_dashboard as dashboard
from knowledge_base.engine.render import (
    _render_signoff_badge,
    _render_signoff_badge_patient,
)


# ──────────────────────────────────────────────────────────────────────────
# Fixture KB scaffolding
# ──────────────────────────────────────────────────────────────────────────


def _write_yaml(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def _make_temp_kb(tmp_path: Path) -> dict:
    """Build a minimal KB on disk with:
      - 1 heme reviewer (REV-HEME-LEAD)
      - 1 solid reviewer (REV-SOLID-LEAD)
      - 1 heme indication (DLBCL)
      - 1 solid indication (CRC)

    Returns a dict of well-known paths used by the tests.
    """
    kb_root = tmp_path / "content"
    audit_log = tmp_path / "audit" / "signoffs.jsonl"

    # Reviewers — leave entity_types empty so the scope check is purely
    # category-based (the live placeholders use the human-readable
    # "Indication" form which the CLI's dir-name check then flags as a
    # warn-only mismatch; that's a separate CLI quirk we don't probe here).
    _write_yaml(kb_root / "reviewers" / "rev_heme.yaml", {
        "id": "REV-HEME-LEAD-PLACEHOLDER",
        "name": {"preferred": "Heme Lead"},
        "specialty": "Hematology",
        "qualifications": ["board"],
        "sign_off_scope": {
            "disease_categories": ["hematologic", "lymphoid"],
            "entity_types": [],
            "diseases_explicit": [],
            "disease_ids": [],
        },
        "last_active": "2026-04-27",
    })
    _write_yaml(kb_root / "reviewers" / "rev_solid.yaml", {
        "id": "REV-SOLID-LEAD-PLACEHOLDER",
        "name": {"preferred": "Solid Lead"},
        "specialty": "Solid Tumors",
        "qualifications": ["board"],
        "sign_off_scope": {
            "disease_categories": ["solid", "gastrointestinal"],
            "entity_types": [],
            "diseases_explicit": [],
            "disease_ids": [],
        },
        "last_active": "2026-04-27",
    })

    # Diseases (used for category inference / dashboard label lookup)
    _write_yaml(kb_root / "diseases" / "dlbcl_nos.yaml", {
        "id": "DIS-DLBCL-NOS",
        "names": {"preferred": "DLBCL", "ukrainian": "ДВВКЛ"},
        "lineage": "b_cell_lymphoma",
        "codes": {},
    })
    _write_yaml(kb_root / "diseases" / "crc.yaml", {
        "id": "DIS-CRC",
        "names": {"preferred": "Colorectal Cancer", "ukrainian": "КРР"},
        "lineage": "solid_gi",
        "codes": {},
    })

    # Heme indication (DLBCL)
    heme_ind = kb_root / "indications" / "ind_dlbcl_test.yaml"
    _write_yaml(heme_ind, {
        "id": "IND-DLBCL-TEST",
        "applicable_to": {
            "disease_id": "DIS-DLBCL-NOS",
            "line_of_therapy": 1,
        },
        "recommended_regimen": "REG-R-CHOP",
        "evidence_level": "high",
        "last_reviewed": "2026-04-27",
    })

    # Solid indication (CRC)
    solid_ind = kb_root / "indications" / "ind_crc_test.yaml"
    _write_yaml(solid_ind, {
        "id": "IND-CRC-TEST",
        "applicable_to": {
            "disease_id": "DIS-CRC",
            "line_of_therapy": 1,
        },
        "recommended_regimen": "REG-FOLFOX",
        "evidence_level": "high",
        "last_reviewed": "2026-04-27",
    })

    return {
        "kb_root": kb_root,
        "audit_log": audit_log,
        "reviewers_dir": kb_root / "reviewers",
        "heme_ind_path": heme_ind,
        "solid_ind_path": solid_ind,
    }


@pytest.fixture
def temp_kb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict:
    """Provide a fresh temp KB with monkey-patched module constants for
    both the CLI and the dashboard. No test ever touches the real KB or
    audit log."""
    paths = _make_temp_kb(tmp_path)

    # Redirect CLI module-level paths. REPO_ROOT is also redirected so
    # the CLI's relative-path print (used in dry-run output) does not
    # ValueError when our temp paths fall outside the real repo root.
    monkeypatch.setattr(cli, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(cli, "KB_ROOT", paths["kb_root"])
    monkeypatch.setattr(cli, "REVIEWERS_DIR", paths["reviewers_dir"])
    monkeypatch.setattr(cli, "AUDIT_LOG", paths["audit_log"])

    # Redirect dashboard module-level paths
    monkeypatch.setattr(dashboard, "KB_ROOT", paths["kb_root"])
    monkeypatch.setattr(dashboard, "REVIEWERS_DIR", paths["reviewers_dir"])
    monkeypatch.setattr(dashboard, "AUDIT_LOG", paths["audit_log"])

    return paths


def _read_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


# ──────────────────────────────────────────────────────────────────────────
# Section A — CLI round-trip
# ──────────────────────────────────────────────────────────────────────────


def test_approve_single_entity_writes_signoff(temp_kb: dict) -> None:
    rc = cli.main([
        "approve",
        "--reviewer", "REV-HEME-LEAD-PLACEHOLDER",
        "--entity-id", "IND-DLBCL-TEST",
        "--rationale", "NCCN-aligned, evidence reviewed",
    ])
    assert rc == 0

    data = _read_yaml(temp_kb["heme_ind_path"])
    sigs = data.get("reviewer_signoffs_v2") or []
    assert len(sigs) == 1
    s = sigs[0]
    assert s["reviewer_id"] == "REV-HEME-LEAD-PLACEHOLDER"
    assert s["rationale"] == "NCCN-aligned, evidence reviewed"
    assert "signoff_date" in s
    assert s.get("scope_match") is True


def test_approve_writes_audit_log_entry(temp_kb: dict) -> None:
    rc = cli.main([
        "approve",
        "--reviewer", "REV-HEME-LEAD-PLACEHOLDER",
        "--entity-id", "IND-DLBCL-TEST",
        "--rationale", "audit-log probe",
    ])
    assert rc == 0

    audit = temp_kb["audit_log"]
    assert audit.is_file(), "audit log was not created"
    lines = [ln for ln in audit.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 1
    row = json.loads(lines[0])
    assert row["action"] == "approve"
    assert row["reviewer_id"] == "REV-HEME-LEAD-PLACEHOLDER"
    assert row["entity_id"] == "IND-DLBCL-TEST"
    assert row["entity_type"] == "Indication"


def test_approve_dry_run_no_writes(temp_kb: dict) -> None:
    rc = cli.main([
        "approve",
        "--reviewer", "REV-HEME-LEAD-PLACEHOLDER",
        "--entity-id", "IND-DLBCL-TEST",
        "--rationale", "dry run",
        "--dry-run",
    ])
    assert rc == 0

    # YAML untouched
    data = _read_yaml(temp_kb["heme_ind_path"])
    assert not data.get("reviewer_signoffs_v2"), (
        "dry-run must not touch the YAML"
    )
    # Audit log not created (or, if created, empty)
    audit = temp_kb["audit_log"]
    assert not audit.exists() or audit.read_text(encoding="utf-8").strip() == ""


def test_withdraw_removes_signoff_keeps_audit(temp_kb: dict) -> None:
    # 1. Approve
    rc1 = cli.main([
        "approve",
        "--reviewer", "REV-HEME-LEAD-PLACEHOLDER",
        "--entity-id", "IND-DLBCL-TEST",
        "--rationale", "first",
    ])
    assert rc1 == 0

    # 2. Withdraw
    rc2 = cli.main([
        "withdraw",
        "--reviewer", "REV-HEME-LEAD-PLACEHOLDER",
        "--entity-id", "IND-DLBCL-TEST",
        "--rationale", "reconsider",
    ])
    assert rc2 == 0

    # YAML: signoff removed
    data = _read_yaml(temp_kb["heme_ind_path"])
    assert (data.get("reviewer_signoffs_v2") or []) == [], (
        "withdraw must remove the sign-off entry from the YAML"
    )

    # Audit log: both entries preserved
    lines = [
        ln for ln in temp_kb["audit_log"].read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    assert len(lines) == 2
    actions = [json.loads(ln)["action"] for ln in lines]
    assert actions == ["approve", "withdraw"]


def test_approve_duplicate_refused_without_force(temp_kb: dict) -> None:
    # First approve succeeds and writes
    rc1 = cli.main([
        "approve",
        "--reviewer", "REV-HEME-LEAD-PLACEHOLDER",
        "--entity-id", "IND-DLBCL-TEST",
        "--rationale", "first",
    ])
    assert rc1 == 0
    data1 = _read_yaml(temp_kb["heme_ind_path"])
    assert len(data1.get("reviewer_signoffs_v2") or []) == 1

    # Second approve by same reviewer is skipped (no second entry written)
    rc2 = cli.main([
        "approve",
        "--reviewer", "REV-HEME-LEAD-PLACEHOLDER",
        "--entity-id", "IND-DLBCL-TEST",
        "--rationale", "second attempt without force",
    ])
    # CLI returns 0 for skip-without-force (per current behavior); the
    # important guarantee is that nothing was duplicated in the YAML.
    assert rc2 == 0
    data2 = _read_yaml(temp_kb["heme_ind_path"])
    assert len(data2.get("reviewer_signoffs_v2") or []) == 1, (
        "duplicate sign-off must be skipped without --force"
    )

    # With --force, a second entry is appended
    rc3 = cli.main([
        "approve",
        "--reviewer", "REV-HEME-LEAD-PLACEHOLDER",
        "--entity-id", "IND-DLBCL-TEST",
        "--rationale", "force re-affirm",
        "--force",
    ])
    assert rc3 == 0
    data3 = _read_yaml(temp_kb["heme_ind_path"])
    assert len(data3.get("reviewer_signoffs_v2") or []) == 2, (
        "--force should permit a re-affirmation entry"
    )


# ──────────────────────────────────────────────────────────────────────────
# Section B — Validation
# ──────────────────────────────────────────────────────────────────────────


def test_approve_unknown_reviewer_refused(temp_kb: dict) -> None:
    rc = cli.main([
        "approve",
        "--reviewer", "REV-DOES-NOT-EXIST",
        "--entity-id", "IND-DLBCL-TEST",
        "--rationale", "should fail",
    ])
    assert rc != 0, "unknown reviewer must produce non-zero exit"
    # YAML must remain untouched
    data = _read_yaml(temp_kb["heme_ind_path"])
    assert not data.get("reviewer_signoffs_v2")


def test_approve_strict_scope_mismatch_refused(temp_kb: dict) -> None:
    """Heme reviewer + solid-tumor entity + --strict must refuse."""
    rc = cli.main([
        "approve",
        "--reviewer", "REV-HEME-LEAD-PLACEHOLDER",
        "--entity-id", "IND-CRC-TEST",
        "--rationale", "heme reviewer should not sign solid",
        "--strict",
    ])
    # CLI returns 0 with `0 approved` in strict-skip mode; the contract we
    # care about is that the YAML stayed clean.
    data = _read_yaml(temp_kb["solid_ind_path"])
    assert not data.get("reviewer_signoffs_v2"), (
        "scope-mismatched approval must not be persisted under --strict"
    )


def test_approve_strict_scope_mismatch_warning_default(temp_kb: dict) -> None:
    """Same heme-on-solid call WITHOUT --strict must proceed (warn-only)."""
    rc = cli.main([
        "approve",
        "--reviewer", "REV-HEME-LEAD-PLACEHOLDER",
        "--entity-id", "IND-CRC-TEST",
        "--rationale", "warn-only path",
    ])
    assert rc == 0
    data = _read_yaml(temp_kb["solid_ind_path"])
    sigs = data.get("reviewer_signoffs_v2") or []
    assert len(sigs) == 1, "warn-only mode should still write the sign-off"
    assert sigs[0]["scope_match"] is False, (
        "scope_match flag must surface as False on a warn-only mismatch"
    )


# ──────────────────────────────────────────────────────────────────────────
# Section C — Dashboard generation
# ──────────────────────────────────────────────────────────────────────────


def _seed_audit_and_signoffs(temp_kb: dict) -> None:
    """Drive a few approvals so the dashboard has something to summarise."""
    cli.main([
        "approve",
        "--reviewer", "REV-HEME-LEAD-PLACEHOLDER",
        "--entity-id", "IND-DLBCL-TEST",
        "--rationale", "seed-1",
    ])
    cli.main([
        "approve",
        "--reviewer", "REV-SOLID-LEAD-PLACEHOLDER",
        "--entity-id", "IND-CRC-TEST",
        "--rationale", "seed-2",
    ])


def test_dashboard_generated_from_audit_log(
    temp_kb: dict, tmp_path: Path
) -> None:
    _seed_audit_and_signoffs(temp_kb)
    out = tmp_path / "dashboard.md"
    rc = dashboard.main(["--out", str(out)])
    assert rc == 0
    assert out.is_file(), "dashboard markdown not produced"
    text = out.read_text(encoding="utf-8")
    assert "# Clinical Sign-off Status" in text
    assert "## Summary" in text


def test_dashboard_includes_per_entity_type_breakdown(
    temp_kb: dict, tmp_path: Path
) -> None:
    _seed_audit_and_signoffs(temp_kb)
    out = tmp_path / "dashboard.md"
    rc = dashboard.main(["--out", str(out)])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    # Per-entity-type section + the Indication / Algorithm / RedFlag rows
    assert "## Per entity-type" in text
    for label in ("Indication", "Algorithm", "RedFlag"):
        assert label in text, f"dashboard missing {label} row"


def test_dashboard_includes_per_reviewer_activity(
    temp_kb: dict, tmp_path: Path
) -> None:
    _seed_audit_and_signoffs(temp_kb)
    out = tmp_path / "dashboard.md"
    rc = dashboard.main(["--out", str(out)])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    assert "## Per reviewer" in text
    assert "REV-HEME-LEAD-PLACEHOLDER" in text, (
        "dashboard must mention the heme reviewer"
    )
    # Approvals column for heme reviewer should show ≥1
    # (we don't pin to an exact column shape, just verify the row mentions
    # a non-zero approval somewhere in its line)
    heme_rows = [
        ln for ln in text.splitlines()
        if "REV-HEME-LEAD-PLACEHOLDER" in ln and "|" in ln
    ]
    assert heme_rows, "no heme-reviewer table row found"
    assert any(" 1 " in ln or "| 1 |" in ln for ln in heme_rows), (
        f"heme-reviewer row does not show an approval count: {heme_rows!r}"
    )


# ──────────────────────────────────────────────────────────────────────────
# Section D — Render badges
# ──────────────────────────────────────────────────────────────────────────


def test_render_signoff_badge_pending_for_zero_signoffs() -> None:
    html = _render_signoff_badge({
        "id": "IND-X",
        "reviewer_signoffs_v2": [],
    })
    assert "signoff-pending" in html
    assert "Очікує підпису" in html
    # Sanity: not the green state
    assert "signoff-complete" not in html


def test_render_signoff_badge_complete_for_two_plus_signoffs() -> None:
    html = _render_signoff_badge({
        "id": "IND-X",
        "reviewer_signoffs_v2": [
            {"reviewer_id": "REV-HEME-LEAD-PLACEHOLDER",
             "signoff_date": "2026-04-27"},
            {"reviewer_id": "REV-SOLID-LEAD-PLACEHOLDER",
             "signoff_date": "2026-04-27"},
        ],
    })
    assert "signoff-complete" in html
    assert "Клінічно затверджено" in html
    assert "signoff-pending" not in html
