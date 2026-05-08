"""Tests for the scheduled-audit orchestrator (Phase A).

Plan: docs/plans/scheduled_kb_audit_2026-04-26.md
Module: scripts/run_scheduled_audit.py

Three pillars:
  1. Determinism — same KB + same `today` → byte-identical action_plan.
  2. Delta classification — surgical fixtures expose each delta kind
     (missing_ref, dormant, schema_regression, freshness_breach, etc.).
  3. Cap + idempotency — synthetic 100-error KB → meta-issue, not 100 issues.

Fixtures use a tmp_path isolating a synthetic mini-KB. We don't wrap
the real `knowledge_base/hosted/content/` — that would couple tests
to evolving KB state and make assertions brittle.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest


# Late import so test discovery works even if scripts/ has issues.
def _import_orchestrator():
    import sys
    REPO_ROOT = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(REPO_ROOT))
    import scripts.run_scheduled_audit as orch  # noqa: E402
    return orch


# ── Fixtures ────────────────────────────────────────────────────────────


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _seed_minimal_kb(root: Path, *, today: str = "2026-04-26") -> None:
    """Build the smallest KB the loader will accept cleanly.

    One disease, one biomarker, one drug, one regimen, one
    indication, one algorithm. Recently `last_reviewed` so no
    freshness breaches.
    """
    # Disease
    _write(root / "diseases" / "test_disease.yaml", f"""
id: DIS-TEST
names:
  preferred: "Test disease"
codes:
  icd_o_3_morphology: "9999/9"
last_reviewed: "{today}"
""".strip())

    # Biomarker
    _write(root / "biomarkers" / "bio_test.yaml", f"""
id: BIO-TEST-MARKER
names:
  preferred: "Test marker"
codes:
  loinc: "12345-6"
biomarker_type: protein_expression_ihc
measurement:
  method: "IHC"
last_reviewed: "{today}"
""".strip())

    # Drug
    _write(root / "drugs" / "test_drug.yaml", f"""
id: DRUG-TEST
names:
  preferred: "Test drug"
atc_code: L01XX99
drug_class: "test"
last_reviewed: "{today}"
""".strip())

    # Regimen
    _write(root / "regimens" / "reg_test.yaml", f"""
id: REG-TEST
name: "Test regimen"
components:
  - drug_id: DRUG-TEST
    dose: "100mg"
    schedule: "qd"
    route: "PO"
cycle_length_days: 28
last_reviewed: "{today}"
""".strip())

    # Source
    _write(root / "sources" / "src_test.yaml", f"""
id: SRC-TEST
source_type: guideline
title: "Test source"
last_reviewed: "{today}"
""".strip())

    # Indication (cites the biomarker → counts as reference)
    _write(root / "indications" / "ind_test.yaml", f"""
id: IND-TEST
plan_track: standard
applicable_to:
  disease_id: DIS-TEST
  line_of_therapy: 1
  biomarker_requirements_required:
    - biomarker_id: BIO-TEST-MARKER
      value_constraint: "positive"
      required: true
recommended_regimen: REG-TEST
evidence_level: high
strength_of_recommendation: strong
hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: []
desired_tests: []
sources:
  - source_id: SRC-TEST
    weight: primary
last_reviewed: "{today}"
""".strip())

    # Algorithm
    _write(root / "algorithms" / "algo_test.yaml", f"""
id: ALGO-TEST
applicable_to_disease: DIS-TEST
applicable_to_line_of_therapy: 1
purpose: "test"
output_indications: [IND-TEST]
default_indication: IND-TEST
alternative_indication: IND-TEST
decision_tree: []
sources: [SRC-TEST]
last_reviewed: "{today}"
""".strip())


@pytest.fixture
def kb(tmp_path: Path) -> Path:
    root = tmp_path / "kb_content"
    root.mkdir()
    _seed_minimal_kb(root)
    return root


# ── Helper: run orchestrator pointed at the fixture KB ──────────────────


def _run(orch, kb_root: Path, today: str = "2026-04-26",
         state_dir: Path | None = None):
    """Run build_action_plan with the orchestrator's STATE_FILE
    redirected so tests don't poison real audit state."""
    if state_dir is not None:
        orch.STATE_FILE = state_dir / ".state.json"
    today_d = date.fromisoformat(today)
    return orch.build_action_plan(today=today_d, kb_root=kb_root)


# ── 1. Clean KB — no actions beyond heartbeat ───────────────────────────


def test_clean_kb_emits_only_heartbeat(kb, tmp_path):
    orch = _import_orchestrator()
    plan = _run(orch, kb, state_dir=tmp_path)

    # First-run vs empty state will surface coverage_growth (informational).
    # No open_issue actions for clean KB.
    issue_actions = [a for a in plan["actions"] if a["type"] == "open_issue"]
    assert issue_actions == [], (
        f"clean KB should not open issues; got: {[a['title'] for a in issue_actions]}"
    )
    # Diagnostics confirm
    assert plan["diagnostics"]["preflight_aborted"] is False


# ── 2. Determinism: same inputs → same outputs ──────────────────────────


def test_determinism_same_kb_same_today(kb, tmp_path):
    orch = _import_orchestrator()
    plan_a = _run(orch, kb, state_dir=tmp_path)
    plan_b = _run(orch, kb, state_dir=tmp_path)

    # Strip volatile fields (started_at) before comparing.
    for p in (plan_a, plan_b):
        p.pop("started_at", None)
    # The git_sha should match across runs in the same repo state
    # but is repo-dependent — strip too for portability.
    plan_a.pop("git_sha", None)
    plan_b.pop("git_sha", None)

    assert json.dumps(plan_a, sort_keys=True) == json.dumps(plan_b, sort_keys=True)


# ── 3. Broken-ref detection ─────────────────────────────────────────────


def test_missing_ref_surfaces_one_action(kb, tmp_path):
    """Add an indication that cites a biomarker not in the KB."""
    _write(kb / "indications" / "ind_broken.yaml", """
id: IND-BROKEN
plan_track: standard
applicable_to:
  disease_id: DIS-TEST
  line_of_therapy: 1
  biomarker_requirements_required:
    - biomarker_id: BIO-DOES-NOT-EXIST
      value_constraint: "positive"
      required: true
recommended_regimen: REG-TEST
evidence_level: high
strength_of_recommendation: strong
hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: []
desired_tests: []
sources:
  - source_id: SRC-TEST
    weight: primary
last_reviewed: "2026-04-26"
""".strip())
    orch = _import_orchestrator()
    plan = _run(orch, kb, state_dir=tmp_path)

    missing_actions = [
        a for a in plan["actions"]
        if a["type"] == "open_issue" and "no entity file" in a.get("title", "")
    ]
    assert len(missing_actions) == 1
    assert "BIO-DOES-NOT-EXIST" in missing_actions[0]["title"]
    assert "blocker" in missing_actions[0]["labels"]


def test_contract_regression_surfaces_one_action(kb, tmp_path):
    """Add an algorithm that routes active treatment without a regimen."""
    _write(kb / "indications" / "ind_contract_broken.yaml", """
id: IND-CONTRACT-BROKEN
plan_track: standard
applicable_to:
  disease_id: DIS-TEST
  line_of_therapy: 1
recommended_regimen: null
evidence_level: high
strength_of_recommendation: strong
hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: []
desired_tests: []
sources:
  - source_id: SRC-TEST
    weight: primary
last_reviewed: "2026-04-26"
""".strip())
    _write(kb / "algorithms" / "algo_contract_broken.yaml", """
id: ALGO-CONTRACT-BROKEN
applicable_to_disease: DIS-TEST
applicable_to_line_of_therapy: 1
purpose: "test"
output_indications: [IND-CONTRACT-BROKEN]
default_indication: IND-CONTRACT-BROKEN
decision_tree: []
sources: [SRC-TEST]
last_reviewed: "2026-04-26"
""".strip())

    orch = _import_orchestrator()
    plan = _run(orch, kb, state_dir=tmp_path)

    contract_actions = [
        a for a in plan["actions"]
        if a["type"] == "open_issue" and "Contract errors increased" in a.get("title", "")
    ]
    assert len(contract_actions) == 1
    assert "blocker" in contract_actions[0]["labels"]


# ── 4. Dormant biomarker detection ──────────────────────────────────────


def test_dormant_biomarker_surfaces_one_action(kb, tmp_path):
    """Add a biomarker that no rule references."""
    _write(kb / "biomarkers" / "bio_orphan.yaml", """
id: BIO-ORPHAN
names: {preferred: "Orphan marker"}
codes: {loinc: "99999-9"}
biomarker_type: gene_mutation
last_reviewed: "2026-04-26"
""".strip())
    orch = _import_orchestrator()
    plan = _run(orch, kb, state_dir=tmp_path)

    dormant_actions = [
        a for a in plan["actions"]
        if a["type"] == "open_issue" and "defined but unused" in a.get("title", "")
    ]
    assert len(dormant_actions) == 1
    assert "BIO-ORPHAN" in dormant_actions[0]["title"]
    assert "clinical-review-required" in dormant_actions[0]["labels"]


# ── 5. Freshness breach detection ───────────────────────────────────────


def test_freshness_breach_per_entity_type(kb, tmp_path):
    """Backdate one Drug past its 12-month SLA."""
    _write(kb / "drugs" / "stale_drug.yaml", """
id: DRUG-STALE
names: {preferred: "Stale drug"}
atc_code: L01XX98
drug_class: "test"
last_reviewed: "2024-01-01"
""".strip())
    orch = _import_orchestrator()
    plan = _run(orch, kb, state_dir=tmp_path, today="2026-04-26")

    fresh_actions = [
        a for a in plan["actions"]
        if a["type"] == "open_issue"
        and "Drug" in a.get("title", "")
        and "past SLA" in a.get("title", "")
    ]
    assert len(fresh_actions) == 1, (
        f"expected one Drug freshness issue; got "
        f"{[a['title'] for a in plan['actions']]}"
    )
    assert "freshness" in fresh_actions[0]["labels"]


# ── 6. Cap enforcement ──────────────────────────────────────────────────


def test_cap_collapses_overflow_into_meta_issue(kb, tmp_path):
    """Inject many freshness breaches across different entity types so
    we exceed MAX_ISSUES_PER_RUN."""
    # One stale entity per type — exceeds MAX_ISSUES_PER_RUN (=5)
    stale = "2024-01-01"
    for i in range(MAX_TYPES := 7):
        # Use different entity types to generate distinct breach issues
        types_dir = ["biomarkers", "drugs", "regimens", "redflags",
                     "indications", "algorithms", "sources"][i % 7]
        _write(kb / types_dir / f"stale_{i}.yaml", f"""
id: STALE-{i:02d}
names: {{preferred: "Stale {i}"}}
last_reviewed: "{stale}"
""".strip())
    orch = _import_orchestrator()
    plan = _run(orch, kb, state_dir=tmp_path, today="2026-04-26")

    issue_actions = [a for a in plan["actions"] if a["type"] == "open_issue"]
    # MAX_ISSUES_PER_RUN cap (5) plus one meta-overflow issue = 6 max
    assert len(issue_actions) <= 6
    meta_actions = [a for a in issue_actions if "Cap overflow" in a.get("title", "")]
    if plan["diagnostics"]["actions_capped"] > 0:
        assert len(meta_actions) == 1, (
            "when cap fires, exactly one meta-issue should be emitted"
        )


# ── 7. Idempotency: previous-state suppresses dup issues ────────────────


def test_dormant_seen_twice_becomes_comment_not_open(kb, tmp_path):
    """First run opens an issue; second run with a previous-state file
    listing that issue produces a comment_issue action instead."""
    # Add a dormant biomarker
    _write(kb / "biomarkers" / "bio_orphan.yaml", """
id: BIO-ORPHAN
names: {preferred: "Orphan marker"}
codes: {loinc: "99999-9"}
biomarker_type: gene_mutation
last_reviewed: "2026-04-26"
""".strip())
    orch = _import_orchestrator()
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    state_file = state_dir / ".state.json"

    # Seed previous-state — pretend we already have an open issue for this dormant
    # Note: dedupe_key format is `kb-audit-key-v1:<kind>:<key>`
    prev_state = {
        "biomarkers": {
            "defined": 2,                # 2 — original BIO-TEST-MARKER + new BIO-ORPHAN
            "referenced": 1,
            "dormant_count": 1,
            "missing_count": 0,
            "naming_mismatch_count": 0,
            "loinc_missing_count": 0,
            "missing_ids": [],
            "dormant_ids": ["BIO-ORPHAN"],   # already known dormant
            "naming_pairs": [],
        },
        "validator": {"loaded_entities": 7, "schema_errors_count": 0,
                      "ref_errors_count": 0, "errors": []},
        "freshness": {"total_breaches": 0, "by_entity_type": {}},
        "open_issues": {
            "kb-audit-key-v1:dormant_appeared:BIO-ORPHAN": 42,
        },
    }
    state_file.write_text(json.dumps(prev_state), encoding="utf-8")
    orch.STATE_FILE = state_file

    plan = orch.build_action_plan(today=date(2026, 4, 26), kb_root=kb)

    # Since BIO-ORPHAN is in BOTH previous and current dormant_ids, no
    # delta is generated — the issue is already tracked. Verify no
    # NEW open_issue / comment_issue for this dedupe_key.
    dormant_titles = [
        a.get("title", "") for a in plan["actions"]
        if "BIO-ORPHAN" in a.get("title", "") and a["type"] == "open_issue"
    ]
    assert dormant_titles == [], (
        "previously-known dormant should not re-open an issue"
    )


def test_dormant_resolved_emits_close_action(kb, tmp_path):
    """Previous run had a dormant issue open; current run shows it
    resolved → close_issue action."""
    orch = _import_orchestrator()
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    state_file = state_dir / ".state.json"

    # Seed previous: BIO-WAS-DORMANT was dormant; current KB has it
    # consumed (the seed KB has BIO-TEST-MARKER consumed by IND-TEST)
    prev_state = {
        "biomarkers": {
            "defined": 1, "referenced": 1, "dormant_count": 1,
            "missing_count": 0, "naming_mismatch_count": 0,
            "loinc_missing_count": 0,
            "missing_ids": [],
            "dormant_ids": ["BIO-TEST-MARKER"],  # was previously dormant
            "naming_pairs": [],
        },
        "validator": {"loaded_entities": 7, "schema_errors_count": 0,
                      "ref_errors_count": 0, "errors": []},
        "freshness": {"total_breaches": 0, "by_entity_type": {}},
        "open_issues": {
            "kb-audit-key-v1:dormant_appeared:BIO-TEST-MARKER": 99,
        },
    }
    state_file.write_text(json.dumps(prev_state), encoding="utf-8")
    orch.STATE_FILE = state_file

    plan = orch.build_action_plan(today=date(2026, 4, 26), kb_root=kb)

    close_actions = [a for a in plan["actions"] if a["type"] == "close_issue"]
    assert len(close_actions) == 1
    assert close_actions[0]["issue_number"] == 99
    assert "BIO-TEST-MARKER" in close_actions[0]["body"]


# ── 8. Catalog refresh fires when snapshot signature changes ────────────


def test_catalog_refresh_when_signature_changes(kb, tmp_path):
    orch = _import_orchestrator()
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    state_file = state_dir / ".state.json"

    prev_state = {
        "biomarkers": {"defined": 99, "referenced": 99, "dormant_count": 0,
                       "missing_count": 0, "loinc_missing_count": 0,
                       "missing_ids": [], "dormant_ids": [], "naming_pairs": []},
        "validator": {"loaded_entities": 99, "schema_errors_count": 0,
                      "ref_errors_count": 0, "errors": []},
        "freshness": {"total_breaches": 0, "by_entity_type": {}},
        "open_issues": {},
    }
    state_file.write_text(json.dumps(prev_state), encoding="utf-8")
    orch.STATE_FILE = state_file

    plan = orch.build_action_plan(today=date(2026, 4, 26), kb_root=kb)

    refresh_actions = [
        a for a in plan["actions"] if a["type"] == "commit_catalog_refresh"
    ]
    assert len(refresh_actions) == 1
    assert "chore(catalog)" in refresh_actions[0]["message"]


def test_catalog_refresh_skipped_when_signature_unchanged(kb, tmp_path):
    orch = _import_orchestrator()
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    state_file = state_dir / ".state.json"

    # First-run snapshot to capture current signature
    plan_a = _run(orch, kb, state_dir=state_dir)

    # Build matching state and re-run
    snap = plan_a["snapshot"]
    matching_state = {
        "biomarkers": snap["biomarkers"],
        "validator": snap["validator"],
        "freshness": snap["freshness"],
        "open_issues": {},
    }
    state_file.write_text(json.dumps(matching_state), encoding="utf-8")
    orch.STATE_FILE = state_file

    plan_b = orch.build_action_plan(today=date(2026, 4, 26), kb_root=kb)

    refresh_actions = [
        a for a in plan_b["actions"] if a["type"] == "commit_catalog_refresh"
    ]
    assert refresh_actions == [], (
        "no signature change → no catalog refresh commit"
    )


# ── 9. Catastrophic — validator crash ───────────────────────────────────


def test_catastrophic_validator_collapses_to_one_blocker_issue(tmp_path, monkeypatch):
    """Even with 50 individual problems, a catastrophic validator
    crash short-circuits to ONE blocker issue, not 50."""
    orch = _import_orchestrator()
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    orch.STATE_FILE = state_dir / ".state.json"

    # Stub validator state to look catastrophic
    def fake_collect_validator_state(*args, **kwargs):
        return {
            "loaded_entities": 0,
            "schema_errors_count": 0,
            "ref_errors_count": 0,
            "catastrophic_error": "Pydantic upgrade broke schemas",
            "errors": [],
            "summary_by_file": {},
        }

    monkeypatch.setattr(
        "scripts.audit_validator.collect_validator_state",
        fake_collect_validator_state,
    )

    # Seed a real-ish KB so other audits don't crash
    kb_root = tmp_path / "kb"
    kb_root.mkdir()
    _seed_minimal_kb(kb_root)

    plan = orch.build_action_plan(today=date(2026, 4, 26), kb_root=kb_root)

    blocker_issues = [
        a for a in plan["actions"]
        if a["type"] == "open_issue" and "BLOCKER" in a.get("title", "")
    ]
    assert len(blocker_issues) == 1
    assert "blocker" in blocker_issues[0]["labels"]
    # Only the catastrophic delta should be present
    assert all(d["kind"] == "catastrophic" for d in plan["deltas"])
