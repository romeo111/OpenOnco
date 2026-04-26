#!/usr/bin/env python3
"""Phase C action executors — git + gh-CLI side effects.

Per `docs/plans/scheduled_kb_audit_2026-04-26.md` §4.1 + §6.

Each executor takes one action dict (output of `run_scheduled_audit
.build_action_plan`) and performs one side effect via `subprocess`.

**Safety properties enforced here, not in the cron-agent prompt:**

  1. **Commit-message whitelist.** Only `chore(catalog):` prefix is
     allowed. Any other commit message is rejected. Engine/render
     changes go through manual sessions; the cron is doc-only.

  2. **Git-add path whitelist.** Only paths under `docs/audit_log/`
     and the canonical `docs/BIOMARKER_CATALOG.md` are stageable.
     Anything else → refuse.

  3. **No force push, no skip hooks, no recursive sub-agents.**
     The execute helpers refuse `--force`, `--no-verify`, `--amend`.

  4. **Pending-actions retry queue.** When `gh` fails (rate limit,
     network), the action is appended to
     `docs/audit_log/.pending/<run-id>.json`. Next run picks up
     pending before processing fresh deltas. Bounded queue (drop
     oldest if >10 — outage of >10 months means bigger problems).

  5. **Idempotent gh ops.** Open issue uses dedupe-key search before
     create; comment uses issue_number; close uses issue_number.

The orchestrator (`run_scheduled_audit.py`) gates execution behind
`--execute`. By default it stays in `--dry-run` mode — no executor
ever runs unless the operator opts in. Phase D (cron) sets `--execute`.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
PENDING_DIR = REPO_ROOT / "docs" / "audit_log" / ".pending"
MAX_PENDING_RUNS = 10

# Whitelist constants — these are the load-bearing safety surface.
ALLOWED_COMMIT_PREFIXES: tuple[str, ...] = ("chore(catalog):",)
ALLOWED_ADD_PATH_PREFIXES: tuple[str, ...] = (
    "docs/audit_log/",
    "docs/BIOMARKER_CATALOG.md",
)
DISALLOWED_GIT_FLAGS: tuple[str, ...] = (
    "--force", "-f",
    "--no-verify",
    "--amend",
    "--no-gpg-sign",
)


class ExecutorError(Exception):
    """Raised when an executor refuses an action (whitelist violation,
    bad input). Distinct from subprocess failures (network, rate limit)."""


@dataclass
class ExecutionResult:
    """Outcome of executing one action."""
    action_type: str
    dedupe_key: Optional[str]
    success: bool
    output: str = ""
    error: str = ""
    deferred_to_pending: bool = False
    issue_number: Optional[int] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_type": self.action_type,
            "dedupe_key": self.dedupe_key,
            "success": self.success,
            "output": self.output[:500],
            "error": self.error[:500],
            "deferred_to_pending": self.deferred_to_pending,
            "issue_number": self.issue_number,
            "metadata": self.metadata,
        }


# ── Whitelist enforcement ───────────────────────────────────────────────


def _check_commit_message(message: str) -> None:
    if not any(message.strip().startswith(p) for p in ALLOWED_COMMIT_PREFIXES):
        raise ExecutorError(
            f"Refusing commit — message must start with one of "
            f"{ALLOWED_COMMIT_PREFIXES!r}; got: {message[:60]!r}"
        )


def _check_add_paths(paths: list[str]) -> None:
    for p in paths:
        norm = p.replace("\\", "/").lstrip("./")
        if not any(norm.startswith(prefix) for prefix in ALLOWED_ADD_PATH_PREFIXES):
            raise ExecutorError(
                f"Refusing git-add — path {p!r} not in whitelist "
                f"{ALLOWED_ADD_PATH_PREFIXES!r}"
            )


def _check_no_disallowed_flags(args: list[str]) -> None:
    for arg in args:
        if arg in DISALLOWED_GIT_FLAGS:
            raise ExecutorError(f"Refusing git command — disallowed flag {arg}")


# ── Subprocess helpers ──────────────────────────────────────────────────


def _run(
    cmd: list[str],
    cwd: Path = REPO_ROOT,
    timeout: int = 60,
    check_disallowed: bool = True,
) -> tuple[int, str, str]:
    """Returns (exit_code, stdout, stderr)."""
    if check_disallowed:
        _check_no_disallowed_flags(cmd)
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True,
            encoding="utf-8", timeout=timeout,
        )
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except FileNotFoundError as exc:
        return 127, "", f"command not found: {exc}"
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s"


# ── Executor: commit_catalog_refresh ────────────────────────────────────


def execute_commit_catalog_refresh(
    action: dict[str, Any],
    *,
    cwd: Path = REPO_ROOT,
    runner=_run,
) -> ExecutionResult:
    """Stage whitelisted files + create one chore(catalog) commit.

    Does NOT push. Push is a separate executor (Phase D wires it
    explicitly so the cron can decide ordering w.r.t. multi-action runs).
    """
    files = action.get("files", []) or []
    message = action.get("message", "").strip()

    try:
        _check_commit_message(message)
        _check_add_paths(files)
    except ExecutorError as exc:
        return ExecutionResult(
            action_type=action["type"], dedupe_key=action.get("dedupe_key"),
            success=False, error=str(exc),
        )

    # Stage explicitly named files only — never `git add -A` or `.`.
    for path in files:
        full = (cwd / path).resolve()
        if not full.exists():
            # File was supposed to be written before this executor ran
            # (audit log + state file are written by Phase B writers
            # earlier in the runner pipeline). If a path is missing,
            # skip it rather than fail the whole commit.
            continue
        code, _, err = runner(["git", "add", "--", str(full)], cwd=cwd)
        if code != 0:
            return ExecutionResult(
                action_type=action["type"], dedupe_key=action.get("dedupe_key"),
                success=False, error=f"git add {path}: {err}",
            )

    # Are there actually changes staged? Empty commits are pointless.
    code, out, _ = runner(["git", "diff", "--cached", "--quiet"], cwd=cwd)
    # `git diff --cached --quiet` returns 0 = no changes, 1 = changes.
    if code == 0:
        return ExecutionResult(
            action_type=action["type"], dedupe_key=action.get("dedupe_key"),
            success=True, output="no staged changes; commit skipped",
            metadata={"skipped_empty": True},
        )

    code, out, err = runner(
        ["git", "commit", "-m", message], cwd=cwd,
    )
    if code != 0:
        return ExecutionResult(
            action_type=action["type"], dedupe_key=action.get("dedupe_key"),
            success=False, error=f"git commit: {err}",
        )

    return ExecutionResult(
        action_type=action["type"], dedupe_key=action.get("dedupe_key"),
        success=True, output=out,
    )


def execute_push(
    *,
    cwd: Path = REPO_ROOT,
    runner=_run,
    branch: str = "master",
) -> ExecutionResult:
    """Push current branch to origin. Refuses --force.

    Returns success=True even when nothing to push (idempotent)."""
    code, out, err = runner(["git", "push", "origin", branch], cwd=cwd)
    if code != 0:
        return ExecutionResult(
            action_type="push", dedupe_key=None, success=False,
            error=f"git push: {err}",
        )
    return ExecutionResult(
        action_type="push", dedupe_key=None, success=True, output=out + err,
    )


# ── Executors: GitHub issue ops ─────────────────────────────────────────


_BODY_DEDUPE_MARKER = "<!-- audit-dedupe: {key} -->"
# Six curated labels are pre-created in the repo by maintainer. The
# cron only attaches labels from this set — never creates new labels.
ALLOWED_LABELS: frozenset[str] = frozenset({
    "kb-audit",
    "kb-audit-meta",
    "blocker",
    "regression",
    "freshness",
    "clinical-review-required",
})


def _filter_labels(labels: list[str]) -> list[str]:
    """Drop labels not in the allow-list. Keeps the curated label set
    stable; new labels need maintainer signoff (per CHARTER §6.1
    spirit — config changes go through review, not cron drift)."""
    return [l for l in labels if l in ALLOWED_LABELS]


def _body_with_dedupe_marker(body: str, dedupe_key: str) -> str:
    """Embed an HTML-comment marker so a future run can find this
    issue via `gh issue list --search ...`. The marker doesn't render
    in the GitHub UI."""
    marker = _BODY_DEDUPE_MARKER.format(key=dedupe_key)
    return f"{body}\n\n{marker}"


def _find_existing_issue(
    dedupe_key: str,
    runner=_run,
    cwd: Path = REPO_ROOT,
) -> Optional[int]:
    """Return open issue number whose body contains the dedupe marker
    for `dedupe_key`, or None.

    Implementation: `gh issue list --search "<marker> in:body"`.
    Fast — GitHub's search index covers body text within seconds of
    issue create. We narrow to the kb-audit label so cross-label
    title collisions don't false-match."""
    marker = _BODY_DEDUPE_MARKER.format(key=dedupe_key)
    code, out, _ = runner(
        ["gh", "issue", "list",
         "--state", "open",
         "--label", "kb-audit",
         "--search", f'"{marker}"',
         "--json", "number,body",
         "--limit", "10"],
        cwd=cwd,
    )
    if code != 0:
        return None
    try:
        rows = json.loads(out)
    except json.JSONDecodeError:
        return None
    # Verify match: gh-CLI's search is best-effort; double-check the
    # body actually contains the marker (avoids false positives from
    # search-index lag).
    for row in rows:
        if marker in (row.get("body") or ""):
            return row.get("number")
    return None


def execute_open_issue(
    action: dict[str, Any],
    *,
    cwd: Path = REPO_ROOT,
    runner=_run,
    max_retries: int = 3,
    retry_delay_s: float = 2.0,
) -> ExecutionResult:
    """Create one issue via gh-CLI, attaching a dedupe-key label so
    next run can find + comment instead of creating a duplicate.

    On rate-limit / network failure: retries up to `max_retries`, then
    defers to pending queue (Phase C §10.6)."""
    title = action.get("title", "").strip()
    body_raw = action.get("body", "")
    dedupe_key = action.get("dedupe_key", "") or ""
    # Embed dedupe marker in body (HTML comment, doesn't render).
    body = _body_with_dedupe_marker(body_raw, dedupe_key) if dedupe_key else body_raw
    # Drop any labels not in the curated allowlist — defensive against
    # malformed action plans referencing labels that don't exist.
    labels = _filter_labels(list(action.get("labels", [])))
    # Always carry the base "kb-audit" label so dedupe search can scope.
    if "kb-audit" not in labels:
        labels.append("kb-audit")

    if not title:
        return ExecutionResult(
            action_type=action["type"], dedupe_key=action.get("dedupe_key"),
            success=False, error="title required",
        )

    # Idempotency: if an open issue with our dedupe marker already
    # exists, treat as success (we shouldn't have been called, but
    # defensive).
    existing = _find_existing_issue(dedupe_key, runner, cwd) if dedupe_key else None
    if existing:
        return ExecutionResult(
            action_type=action["type"], dedupe_key=action.get("dedupe_key"),
            success=True, output=f"existing issue #{existing}",
            issue_number=existing,
            metadata={"already_existed": True},
        )

    cmd = ["gh", "issue", "create", "--title", title, "--body", body]
    for lbl in labels:
        cmd.extend(["--label", lbl])

    last_err = ""
    for attempt in range(max_retries):
        code, out, err = runner(cmd, cwd=cwd)
        if code == 0:
            # gh prints the issue URL on success; extract the number.
            num = _parse_issue_number(out)
            return ExecutionResult(
                action_type=action["type"], dedupe_key=action.get("dedupe_key"),
                success=True, output=out, issue_number=num,
            )
        last_err = err
        if "rate limit" in err.lower() or "503" in err or "504" in err:
            time.sleep(retry_delay_s * (attempt + 1))
            continue
        # Non-transient error → defer
        break

    return ExecutionResult(
        action_type=action["type"], dedupe_key=action.get("dedupe_key"),
        success=False, error=f"gh issue create: {last_err}",
        deferred_to_pending=True,
    )


_ISSUE_URL_RE = re.compile(r"/issues/(\d+)")


def _parse_issue_number(stdout: str) -> Optional[int]:
    """gh-CLI prints `https://github.com/owner/repo/issues/N` on success."""
    m = _ISSUE_URL_RE.search(stdout)
    return int(m.group(1)) if m else None


def execute_comment_issue(
    action: dict[str, Any],
    *,
    cwd: Path = REPO_ROOT,
    runner=_run,
) -> ExecutionResult:
    """Post a comment on an existing issue."""
    issue_number = action.get("issue_number")
    body = action.get("body", "")

    if not issue_number:
        # Try to recover via dedupe_key lookup (handles None placeholder
        # from previous-run state)
        issue_number = _find_existing_issue(
            action.get("dedupe_key", ""), runner, cwd,
        )
        if not issue_number:
            return ExecutionResult(
                action_type=action["type"], dedupe_key=action.get("dedupe_key"),
                success=False, error="no issue_number and no matching open issue",
            )

    code, out, err = runner(
        ["gh", "issue", "comment", str(issue_number), "--body", body],
        cwd=cwd,
    )
    if code != 0:
        return ExecutionResult(
            action_type=action["type"], dedupe_key=action.get("dedupe_key"),
            success=False, error=f"gh issue comment: {err}",
            deferred_to_pending=True,
        )
    return ExecutionResult(
        action_type=action["type"], dedupe_key=action.get("dedupe_key"),
        success=True, output=out, issue_number=issue_number,
    )


def execute_close_issue(
    action: dict[str, Any],
    *,
    cwd: Path = REPO_ROOT,
    runner=_run,
) -> ExecutionResult:
    """Post a final comment + close the issue.

    Two gh calls because comments-on-close are best-effort: if the
    comment fails we still try the close, but log both."""
    issue_number = action.get("issue_number")
    body = action.get("body", "")

    if not issue_number:
        issue_number = _find_existing_issue(
            action.get("dedupe_key", ""), runner, cwd,
        )
        if not issue_number:
            return ExecutionResult(
                action_type=action["type"], dedupe_key=action.get("dedupe_key"),
                success=True, output="no matching open issue (already closed?)",
                metadata={"no_op": True},
            )

    # Best-effort: post the resolution comment first
    if body:
        runner(
            ["gh", "issue", "comment", str(issue_number), "--body", body],
            cwd=cwd,
        )

    code, out, err = runner(
        ["gh", "issue", "close", str(issue_number)],
        cwd=cwd,
    )
    if code != 0:
        return ExecutionResult(
            action_type=action["type"], dedupe_key=action.get("dedupe_key"),
            success=False, error=f"gh issue close: {err}",
            deferred_to_pending=True,
        )
    return ExecutionResult(
        action_type=action["type"], dedupe_key=action.get("dedupe_key"),
        success=True, output=out, issue_number=issue_number,
    )


# ── Pending queue (gh-outage recovery) ──────────────────────────────────


def save_pending(
    run_id: str,
    deferred: list[dict[str, Any]],
    pending_dir: Path = PENDING_DIR,
) -> Optional[Path]:
    """Persist deferred actions for next-run recovery. Caps queue at
    MAX_PENDING_RUNS (oldest dropped). No-op if `deferred` is empty."""
    if not deferred:
        return None
    pending_dir.mkdir(parents=True, exist_ok=True)
    target = pending_dir / f"{run_id}.json"
    target.write_text(
        json.dumps({"run_id": run_id, "actions": deferred}, indent=2),
        encoding="utf-8",
    )
    _trim_pending_queue(pending_dir)
    return target


def _trim_pending_queue(pending_dir: Path) -> None:
    files = sorted(pending_dir.glob("*.json"), key=lambda p: p.stat().st_mtime)
    if len(files) > MAX_PENDING_RUNS:
        for old in files[:-MAX_PENDING_RUNS]:
            try:
                old.unlink()
            except OSError:
                pass


def load_pending(pending_dir: Path = PENDING_DIR) -> list[dict[str, Any]]:
    """Load all pending actions (oldest first). Caller is responsible
    for removing / re-deferring after processing."""
    out: list[dict[str, Any]] = []
    if not pending_dir.is_dir():
        return out
    for p in sorted(pending_dir.glob("*.json"), key=lambda p: p.stat().st_mtime):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for action in data.get("actions", []):
            action["_pending_source"] = p.name
            out.append(action)
    return out


def clear_pending_file(name: str, pending_dir: Path = PENDING_DIR) -> None:
    target = pending_dir / name
    try:
        target.unlink()
    except OSError:
        pass


# ── Top-level dispatch ──────────────────────────────────────────────────


def execute_action(
    action: dict[str, Any],
    *,
    cwd: Path = REPO_ROOT,
    runner=_run,
) -> ExecutionResult:
    """Dispatch one action to the right executor. Unknown types
    return a no-op success result so unknown action_plan v2 fields
    don't crash the runner mid-flight."""

    atype = action.get("type")
    if atype == "commit_catalog_refresh":
        return execute_commit_catalog_refresh(action, cwd=cwd, runner=runner)
    if atype == "open_issue":
        return execute_open_issue(action, cwd=cwd, runner=runner)
    if atype == "comment_issue":
        return execute_comment_issue(action, cwd=cwd, runner=runner)
    if atype == "close_issue":
        return execute_close_issue(action, cwd=cwd, runner=runner)
    if atype in {"no_op", "abort"}:
        return ExecutionResult(
            action_type=atype or "unknown",
            dedupe_key=action.get("dedupe_key"),
            success=True, output=f"no-op: {action.get('rationale', '')}",
            metadata={"no_op": True},
        )
    # Unknown type — defensive no-op (don't crash; surface via metadata)
    return ExecutionResult(
        action_type=atype or "unknown",
        dedupe_key=action.get("dedupe_key"),
        success=False, error=f"unknown action type: {atype}",
    )


def execute_plan(
    plan: dict[str, Any],
    *,
    cwd: Path = REPO_ROOT,
    runner=_run,
    push_after_commit: bool = True,
) -> dict[str, Any]:
    """Execute every action in plan["actions"]. Returns:

      {
        "results": [<ExecutionResult.to_dict() per action>],
        "pending_saved": bool,
        "issue_numbers": {dedupe_key: issue_number},  # for state update
      }

    Non-transactional: each action runs independently. Failures defer
    to pending queue; successes are recorded so the runner can update
    state file with real issue numbers."""

    results: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    issue_numbers: dict[str, int] = {}
    saw_commit = False

    for action in plan.get("actions", []):
        result = execute_action(action, cwd=cwd, runner=runner)
        results.append(result.to_dict())
        if result.deferred_to_pending:
            deferred.append(action)
        if result.success and result.issue_number is not None:
            key = action.get("dedupe_key")
            if key:
                issue_numbers[key] = result.issue_number
        if (action.get("type") == "commit_catalog_refresh"
                and result.success
                and not result.metadata.get("skipped_empty")):
            saw_commit = True

    pending_saved = False
    if deferred:
        save_pending(plan.get("run_id", "unknown"), deferred)
        pending_saved = True

    # If we made a commit, push it (unless caller opted out).
    push_result: Optional[dict[str, Any]] = None
    if saw_commit and push_after_commit:
        push = execute_push(cwd=cwd, runner=runner)
        push_result = push.to_dict()
        results.append(push_result)

    return {
        "results": results,
        "pending_saved": pending_saved,
        "issue_numbers": issue_numbers,
        "push_result": push_result,
    }
