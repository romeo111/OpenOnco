"""Tests for Phase C action executors (scripts/audit_executors.py).

All tests inject a mock `runner` so subprocess never actually fires.
The whitelist enforcement tests are the most important — they assert
that the cron CANNOT make non-doc commits even if a malformed action
plan tries.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest


def _import_executors():
    import sys
    REPO_ROOT = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(REPO_ROOT))
    import scripts.audit_executors as ex  # noqa: E402
    return ex


# ── Helpers ─────────────────────────────────────────────────────────────


def _make_runner(*responses):
    """Build a fake `_run` that returns each response in order.
    Each response: (returncode, stdout, stderr)."""
    iterator = iter(responses)

    def runner(cmd, cwd=None, timeout=60, check_disallowed=True):
        try:
            return next(iterator)
        except StopIteration:
            # Default: success with empty output
            return (0, "", "")
    return runner


def _seq_runner():
    """Records calls; returns success with empty output by default."""
    calls = []

    def runner(cmd, cwd=None, timeout=60, check_disallowed=True):
        calls.append(list(cmd))
        return (0, "", "")
    runner.calls = calls
    return runner


# ── Whitelist: commit-message prefix ────────────────────────────────────


def test_commit_message_must_start_with_chore_catalog():
    ex = _import_executors()
    bad_action = {
        "type": "commit_catalog_refresh",
        "files": ["docs/audit_log/2026-04-26.md"],
        "message": "feat(engine): bypass safety",
        "dedupe_key": "x",
    }
    result = ex.execute_commit_catalog_refresh(
        bad_action, runner=_seq_runner(),
    )
    assert result.success is False
    assert "chore(catalog):" in result.error


def test_chore_catalog_message_accepted():
    ex = _import_executors()
    # No paths under whitelist + no diff → returns success "skipped_empty"
    runner = _make_runner(
        (0, "", ""),                # add: no-op (file doesn't exist, skipped)
        (0, "", ""),                # diff --cached --quiet returns 0 (no changes)
    )
    action = {
        "type": "commit_catalog_refresh",
        "files": [],
        "message": "chore(catalog): test",
        "dedupe_key": "x",
    }
    result = ex.execute_commit_catalog_refresh(action, runner=runner)
    assert result.success is True


# ── Whitelist: git-add path ─────────────────────────────────────────────


def test_git_add_outside_whitelist_refused():
    ex = _import_executors()
    bad_action = {
        "type": "commit_catalog_refresh",
        "files": ["knowledge_base/hosted/content/biomarkers/bio_evil.yaml"],
        "message": "chore(catalog): valid prefix but bad path",
        "dedupe_key": "x",
    }
    result = ex.execute_commit_catalog_refresh(
        bad_action, runner=_seq_runner(),
    )
    assert result.success is False
    assert "whitelist" in result.error.lower()


def test_git_add_audit_log_path_allowed():
    ex = _import_executors()
    # Verify the whitelist accepts the canonical audit log dir
    paths = ["docs/audit_log/2026-04-26.md", "docs/BIOMARKER_CATALOG.md"]
    # Should not raise
    ex._check_add_paths(paths)


def test_git_add_normalizes_backslash_paths():
    """Windows path separators must be normalized; the audit log
    dir-prefix check should match either way."""
    ex = _import_executors()
    ex._check_add_paths(["docs\\audit_log\\2026-04-26.md"])


# ── Whitelist: disallowed flags ─────────────────────────────────────────


@pytest.mark.parametrize("flag", ["--force", "-f", "--no-verify", "--amend"])
def test_disallowed_flags_refused(flag):
    ex = _import_executors()
    with pytest.raises(ex.ExecutorError):
        ex._check_no_disallowed_flags(["git", "push", flag])


# ── commit_catalog_refresh: empty diff is success ───────────────────────


def test_commit_catalog_refresh_skipped_when_no_changes(tmp_path):
    ex = _import_executors()
    # Pretend file exists so add succeeds, but diff --cached --quiet exits 0
    (tmp_path / "fake_file.md").write_text("x", encoding="utf-8")
    runner = _make_runner(
        (0, "", ""),                # git add
        (0, "", ""),                # diff --quiet: no changes
    )
    action = {
        "type": "commit_catalog_refresh",
        "files": ["docs/audit_log/2026-04-26.md"],
        "message": "chore(catalog): test",
        "dedupe_key": "x",
    }
    result = ex.execute_commit_catalog_refresh(
        action, runner=runner, cwd=tmp_path,
    )
    assert result.success is True
    assert result.metadata.get("skipped_empty") is True


def test_commit_catalog_refresh_succeeds_with_changes(tmp_path):
    ex = _import_executors()
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "audit_log").mkdir()
    (tmp_path / "docs" / "audit_log" / "2026-04-26.md").write_text("x", encoding="utf-8")
    runner = _make_runner(
        (0, "", ""),                # git add
        (1, "", ""),                # diff --quiet: HAS changes (exit 1)
        (0, "[master abc] chore(catalog): test", ""),  # git commit
    )
    action = {
        "type": "commit_catalog_refresh",
        "files": ["docs/audit_log/2026-04-26.md"],
        "message": "chore(catalog): test",
        "dedupe_key": "x",
    }
    result = ex.execute_commit_catalog_refresh(
        action, runner=runner, cwd=tmp_path,
    )
    assert result.success is True
    assert result.metadata.get("skipped_empty") is not True


# ── open_issue: idempotency via dedupe-key search ───────────────────────


def test_open_issue_returns_existing_when_dedupe_marker_matches():
    ex = _import_executors()
    dedupe_key = "kb-audit-key-v1:missing_ref:BIO-FOO"
    marker = ex._BODY_DEDUPE_MARKER.format(key=dedupe_key)
    runner = _make_runner(
        # gh issue list returns one match — body must contain the marker
        # so the post-search verification accepts it.
        (0, json.dumps([{"number": 42, "body": f"some body\n\n{marker}"}]), ""),
    )
    action = {
        "type": "open_issue",
        "title": "[kb-audit] BIO-FOO missing",
        "body": "...",
        "labels": ["kb-audit"],
        "dedupe_key": dedupe_key,
    }
    result = ex.execute_open_issue(action, runner=runner)
    assert result.success is True
    assert result.issue_number == 42
    assert result.metadata.get("already_existed") is True


def test_open_issue_creates_when_no_existing():
    ex = _import_executors()
    runner = _make_runner(
        (0, "[]", ""),               # list: no matches
        (0, "https://github.com/o/r/issues/77", ""),  # create returns URL
    )
    action = {
        "type": "open_issue",
        "title": "[kb-audit] BIO-NEW missing",
        "body": "...",
        "labels": ["kb-audit", "blocker"],
        "dedupe_key": "kb-audit-key-v1:missing_ref:BIO-NEW",
    }
    result = ex.execute_open_issue(action, runner=runner)
    assert result.success is True
    assert result.issue_number == 77


def test_open_issue_defers_to_pending_on_persistent_failure():
    ex = _import_executors()
    runner = _make_runner(
        (0, "[]", ""),               # list: no matches
        (1, "", "API not reachable"),  # create fails (non-rate-limit)
    )
    action = {
        "type": "open_issue",
        "title": "[kb-audit] x",
        "body": "...",
        "labels": [],
        "dedupe_key": "kb-audit-key-v1:x:y",
    }
    result = ex.execute_open_issue(action, runner=runner, max_retries=1)
    assert result.success is False
    assert result.deferred_to_pending is True


# ── close_issue: best-effort on missing ─────────────────────────────────


def test_close_issue_succeeds_with_explicit_number():
    ex = _import_executors()
    runner = _make_runner(
        (0, "", ""),                 # gh issue comment (best-effort)
        (0, "issue closed", ""),     # gh issue close
    )
    action = {
        "type": "close_issue",
        "issue_number": 42,
        "body": "resolved",
        "dedupe_key": "kb-audit-key-v1:dormant_appeared:BIO-OLD",
    }
    result = ex.execute_close_issue(action, runner=runner)
    assert result.success is True
    assert result.issue_number == 42


def test_close_issue_noop_when_no_matching_open():
    ex = _import_executors()
    runner = _make_runner(
        (0, "[]", ""),  # list (gh issue list) returns empty
    )
    action = {
        "type": "close_issue",
        # no issue_number → fallback to dedupe lookup
        "body": "resolved",
        "dedupe_key": "kb-audit-key-v1:dormant_appeared:BIO-MISSING",
    }
    result = ex.execute_close_issue(action, runner=runner)
    # Treat as success — already-closed-or-never-opened is idempotent
    assert result.success is True
    assert result.metadata.get("no_op") is True


def test_open_issue_filters_out_unallowed_labels():
    """Defensive: even if the action plan asks for a label not in
    ALLOWED_LABELS, the executor strips it before calling gh-CLI.
    Prevents 'label not found' failures from polluting the queue."""
    ex = _import_executors()
    captured: list = []

    def runner(cmd, cwd=None, timeout=60, check_disallowed=True):
        captured.append(list(cmd))
        if "list" in cmd:
            return (0, "[]", "")  # no existing
        if "create" in cmd:
            return (0, "https://github.com/o/r/issues/9", "")
        return (0, "", "")

    action = {
        "type": "open_issue",
        "title": "[kb-audit] test",
        "body": "...",
        "labels": ["kb-audit", "regression", "made-up-label", "evil-label"],
        "dedupe_key": "kb-audit-key-v1:x:y",
    }
    ex.execute_open_issue(action, runner=runner)
    create_call = next(c for c in captured if "create" in c)
    # Allowed labels present:
    assert "kb-audit" in create_call
    assert "regression" in create_call
    # Unallowed labels stripped:
    assert "made-up-label" not in create_call
    assert "evil-label" not in create_call


def test_open_issue_embeds_dedupe_marker_in_body():
    """The body sent to gh-CLI must contain the HTML-comment marker so
    the next run's _find_existing_issue can locate this issue."""
    ex = _import_executors()
    captured_body: list[str] = []

    def runner(cmd, cwd=None, timeout=60, check_disallowed=True):
        if "list" in cmd:
            return (0, "[]", "")
        if "create" in cmd:
            # Find the --body arg
            i = cmd.index("--body")
            captured_body.append(cmd[i + 1])
            return (0, "https://github.com/o/r/issues/9", "")
        return (0, "", "")

    action = {
        "type": "open_issue",
        "title": "[kb-audit] test",
        "body": "user-facing body",
        "labels": ["kb-audit"],
        "dedupe_key": "kb-audit-key-v1:test:Z",
    }
    ex.execute_open_issue(action, runner=runner)
    assert len(captured_body) == 1
    body = captured_body[0]
    assert "user-facing body" in body
    assert "<!-- audit-dedupe: kb-audit-key-v1:test:Z -->" in body


# ── Pending queue ───────────────────────────────────────────────────────


def test_save_and_load_pending_round_trip(tmp_path):
    ex = _import_executors()
    deferred = [
        {"type": "open_issue", "title": "x", "dedupe_key": "k1"},
        {"type": "comment_issue", "issue_number": 5, "dedupe_key": "k2"},
    ]
    ex.save_pending("audit-2026-04-26-monthly", deferred, tmp_path)
    loaded = ex.load_pending(tmp_path)
    assert len(loaded) == 2
    # Each loaded action gets a `_pending_source` provenance marker
    assert all("_pending_source" in a for a in loaded)


def test_pending_queue_caps_at_max_pending_runs(tmp_path):
    ex = _import_executors()
    # Save more than MAX_PENDING_RUNS
    for i in range(ex.MAX_PENDING_RUNS + 3):
        ex.save_pending(f"run-{i:03d}", [{"type": "open_issue", "title": "x", "dedupe_key": str(i)}], tmp_path)
    files = list(tmp_path.glob("*.json"))
    assert len(files) <= ex.MAX_PENDING_RUNS


def test_save_pending_noop_for_empty_list(tmp_path):
    ex = _import_executors()
    result = ex.save_pending("run-x", [], tmp_path)
    assert result is None
    assert list(tmp_path.glob("*.json")) == []


# ── execute_plan: dispatch + push ───────────────────────────────────────


def test_execute_plan_pushes_after_successful_commit(tmp_path):
    ex = _import_executors()
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "audit_log").mkdir()
    (tmp_path / "docs" / "audit_log" / "2026-04-26.md").write_text("x", encoding="utf-8")
    runner = _make_runner(
        (0, "", ""),                 # git add
        (1, "", ""),                 # diff --quiet: HAS changes
        (0, "[master abc] msg", ""), # commit
        (0, "Everything up-to-date", ""),  # push
    )
    plan = {
        "run_id": "audit-2026-04-26-monthly",
        "actions": [{
            "type": "commit_catalog_refresh",
            "files": ["docs/audit_log/2026-04-26.md"],
            "message": "chore(catalog): test",
            "dedupe_key": "x",
        }],
    }
    out = ex.execute_plan(plan, runner=runner, cwd=tmp_path)
    assert out["push_result"] is not None
    assert out["push_result"]["success"] is True


def test_execute_plan_skips_push_when_no_commit(tmp_path):
    ex = _import_executors()
    runner = _make_runner((0, "[]", ""))  # for any list call
    plan = {
        "run_id": "audit-2026-04-26-monthly",
        "actions": [{
            "type": "no_op", "dedupe_key": "x", "rationale": "nothing"},
        ],
    }
    out = ex.execute_plan(plan, runner=runner, cwd=tmp_path)
    assert out["push_result"] is None


def test_execute_plan_returns_issue_numbers_for_state_update(tmp_path):
    ex = _import_executors()
    runner = _make_runner(
        (0, "[]", ""),                                  # list (no existing)
        (0, "https://github.com/o/r/issues/55", ""),    # create
    )
    plan = {
        "run_id": "audit-2026-04-26-monthly",
        "actions": [{
            "type": "open_issue",
            "title": "[kb-audit] new issue",
            "body": "...",
            "labels": [],
            "dedupe_key": "kb-audit-key-v1:foo:bar",
        }],
    }
    out = ex.execute_plan(plan, runner=runner, cwd=tmp_path)
    assert out["issue_numbers"]["kb-audit-key-v1:foo:bar"] == 55


# ── Disallowed-flag enforcement at execute layer ────────────────────────


def test_executor_runner_refuses_force_flag_via_check():
    ex = _import_executors()
    # `_run` enforces by default; verify the check fires
    with pytest.raises(ex.ExecutorError):
        ex._run(["git", "push", "--force", "origin", "master"])


# ── Top-level dispatch ─────────────────────────────────────────────────


def test_dispatch_routes_to_correct_executor():
    ex = _import_executors()
    no_op_action = {"type": "no_op", "dedupe_key": "x", "rationale": "test"}
    result = ex.execute_action(no_op_action, runner=_seq_runner())
    assert result.success is True
    assert result.metadata.get("no_op") is True


def test_dispatch_unknown_type_does_not_crash():
    ex = _import_executors()
    weird_action = {"type": "future_action_v2", "dedupe_key": "x"}
    result = ex.execute_action(weird_action, runner=_seq_runner())
    assert result.success is False
    assert "unknown action type" in result.error
