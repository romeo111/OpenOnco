#!/usr/bin/env python3
"""Phase D entrypoint — the script CronCreate invokes once a month.

Per `docs/plans/scheduled_kb_audit_2026-04-26.md` §8 Phase D + §4.

Composition (in order):

  1. Acquire run lock (`.claude/scheduled_tasks.lock`); detect + take
     over stale lock (>1h old).
  2. Check kill switch (`docs/audit_log/CRON_DISABLED.md`); abort
     if present.
  3. Pre-flight gates: clean working tree, on `master`, in sync with
     `origin/master`. If any fails → log + abort gracefully.
  4. Build action plan (Phase A).
  5. Persist artifacts: state file + audit log MD + metrics CSV (Phase B).
  6. Execute actions (Phase C): commit_catalog_refresh / open_issue /
     comment_issue / close_issue. Push if any commit landed.
  7. Update state file with real issue numbers from gh-CLI responses.
  8. Release lock.

Every abort path writes an audit log entry — silence is never the
indicator. Even a fully no-op month produces one MD file so the
heartbeat-check meta-cron can verify the runner is alive.

Usage:
  python scripts/cron_kb_audit_runner.py            # production run
  python scripts/cron_kb_audit_runner.py --dry-run  # plan only, no I/O
  python scripts/cron_kb_audit_runner.py --no-execute  # persist but skip executors
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Dedicated lock for this cron runner. Does NOT share with Claude Code's
# parent scheduling system (which uses `.claude/scheduled_tasks.lock` —
# different schema, different lifecycle, accidentally clobbering it
# would corrupt state for the parent system).
LOCK_FILE = REPO_ROOT / ".claude" / "kb_audit_cron.lock"
LOCK_STALE_AFTER_S = 60 * 60   # 1 hour
KILL_SWITCH = REPO_ROOT / "docs" / "audit_log" / "CRON_DISABLED.md"
AUDIT_LOG_DIR = REPO_ROOT / "docs" / "audit_log"
STATE_FILE = AUDIT_LOG_DIR / ".state.json"
METRICS_CSV = AUDIT_LOG_DIR / ".metrics.csv"


def _force_utf8_stdout() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:  # pylint: disable=broad-except
                pass


def _log(msg: str) -> None:
    """Stderr log (cron captures stderr separately from action_plan stdout)."""
    print(f"[cron-audit] {msg}", file=sys.stderr)


# ── Run lock ────────────────────────────────────────────────────────────


def acquire_lock() -> tuple[bool, str]:
    """Acquire LOCK_FILE. If a stale lock (>LOCK_STALE_AFTER_S) exists,
    take it over. Returns (acquired, message)."""
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)

    if LOCK_FILE.is_file():
        try:
            existing = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
            acquired_ms = existing.get("acquiredAt", 0)
            age_s = time.time() - (acquired_ms / 1000.0)
        except (json.JSONDecodeError, OSError):
            age_s = LOCK_STALE_AFTER_S + 1   # treat as stale
        if age_s < LOCK_STALE_AFTER_S:
            return False, (
                f"lock held by another process (age={int(age_s)}s); "
                "refusing to run"
            )
        _log(f"stale lock detected (age={int(age_s)}s); taking over")

    payload = {
        "sessionId": f"cron-audit-{datetime.now(timezone.utc).isoformat()}",
        "pid": os.getpid(),
        "acquiredAt": int(time.time() * 1000),
        "purpose": "scheduled-kb-audit",
    }
    LOCK_FILE.write_text(json.dumps(payload), encoding="utf-8")
    return True, "lock acquired"


def release_lock() -> None:
    if LOCK_FILE.is_file():
        try:
            LOCK_FILE.unlink()
        except OSError:
            pass


# ── Kill switch ─────────────────────────────────────────────────────────


def kill_switch_active() -> bool:
    return KILL_SWITCH.is_file()


# ── Pre-flight git gates ────────────────────────────────────────────────


def preflight_check(cwd: Path = REPO_ROOT) -> tuple[bool, str]:
    """Returns (ok, reason). Production cron mode requires:
       - clean working tree
       - on `master` branch
       - in sync with `origin/master`
    """
    from scripts.audit_executors import _run

    code, out, _ = _run(["git", "status", "--porcelain"], cwd=cwd)
    if code != 0:
        return False, "git status failed"
    if out.strip():
        return False, f"working tree not clean ({len(out.splitlines())} files modified)"

    code, out, _ = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
    branch = out.strip()
    if branch != "master":
        return False, f"not on master (on {branch!r})"

    # Fetch + check parity (don't fail on offline — log warning)
    code, _, _ = _run(["git", "fetch", "origin", "master"], cwd=cwd, timeout=30)
    if code != 0:
        return True, "preflight pass (fetch failed; offline mode)"

    code, out, _ = _run(
        ["git", "rev-list", "--count", "HEAD..origin/master"], cwd=cwd,
    )
    if code == 0 and out.strip().isdigit() and int(out.strip()) > 0:
        return False, f"local behind origin/master by {out.strip()} commits"

    return True, "preflight ok"


# ── Main pipeline ───────────────────────────────────────────────────────


def run(
    *,
    dry_run: bool = False,
    no_execute: bool = False,
    today_override: Optional[date] = None,
    cwd: Path = REPO_ROOT,
) -> int:
    """Main pipeline. Returns process exit code:
       0 — success (or graceful no-op abort)
       1 — error during plan/persist/execute
       2 — refused to run (lock contention, kill switch)
    """
    _force_utf8_stdout()
    started = time.time()

    # 1. Lock
    acquired, lock_msg = acquire_lock()
    if not acquired:
        _log(lock_msg)
        return 2

    try:
        # 2. Kill switch
        if kill_switch_active():
            _log(f"kill switch active ({KILL_SWITCH}); writing log + aborting")
            _write_disabled_log_entry()
            return 2

        # 3. Pre-flight (only enforced when we'll actually fire git/gh ops).
        # Pre-flight gates the executor side effects, not the persist
        # writers; `--no-execute` writes log/state/CSV without git/gh, so
        # an unclean tree shouldn't gate it.
        if not dry_run and not no_execute:
            ok, reason = preflight_check(cwd)
            if not ok:
                _log(f"preflight failed: {reason}")
                _write_aborted_log_entry(reason)
                return 0  # graceful — this isn't an error, just not our turn

        # 4. Build plan
        from scripts.run_scheduled_audit import build_action_plan, _load_previous_state
        plan = build_action_plan(today=today_override)
        plan["duration_s"] = round(time.time() - started, 2)

        # 5. Persist (Phase B writers)
        from scripts.audit_writers import persist_plan_outputs
        previous_open = (_load_previous_state() or {}).get("open_issues", {}) or {}
        if not dry_run:
            paths = persist_plan_outputs(
                plan,
                audit_log_dir=AUDIT_LOG_DIR,
                state_file=STATE_FILE,
                metrics_csv=METRICS_CSV,
                previous_open_issues=previous_open,
            )
            _log(f"persisted: log={paths['audit_log'].name}")

        # 6. Execute (Phase C)
        if dry_run or no_execute:
            _log("execution skipped (dry-run / no-execute)")
        else:
            from scripts.audit_executors import execute_plan
            outcome = execute_plan(plan, cwd=cwd)
            _log(
                f"executed {len(outcome['results'])} actions; "
                f"pending_saved={outcome['pending_saved']}; "
                f"new_issues={len(outcome['issue_numbers'])}"
            )
            # 7. Patch state file with real issue numbers
            if outcome["issue_numbers"]:
                _patch_state_file_issue_numbers(outcome["issue_numbers"])

        return 0
    except Exception as exc:  # pylint: disable=broad-except
        _log(f"unhandled exception: {type(exc).__name__}: {exc}")
        # Don't write a partial log; the abort log entry is best-effort.
        try:
            _write_aborted_log_entry(f"unhandled: {exc}")
        except Exception:  # pylint: disable=broad-except
            pass
        return 1
    finally:
        release_lock()


def _write_disabled_log_entry() -> None:
    """Brief log entry stating that the kill switch is active."""
    today = date.today().isoformat()
    AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)
    target = AUDIT_LOG_DIR / f"{today}-disabled.md"
    # Use as_posix() instead of relative_to — the latter raises when
    # KILL_SWITCH is outside the repo (test scenarios).
    try:
        kill_switch_str = str(KILL_SWITCH.relative_to(REPO_ROOT))
    except ValueError:
        kill_switch_str = KILL_SWITCH.as_posix()
    target.write_text(
        f"# KB audit — {today} (DISABLED)\n\n"
        f"Kill switch active at `{kill_switch_str}`. "
        "Cron took no actions this run.\n",
        encoding="utf-8",
    )


def _write_aborted_log_entry(reason: str) -> None:
    today = date.today().isoformat()
    AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)
    target = AUDIT_LOG_DIR / f"{today}-aborted.md"
    n = 2
    while target.exists():
        target = AUDIT_LOG_DIR / f"{today}-aborted-{n}.md"
        n += 1
    target.write_text(
        f"# KB audit — {today} (ABORTED)\n\n"
        f"Pre-flight check failed: {reason}\n\n"
        "No actions taken; no state file modified. The next scheduled "
        "run will retry.\n",
        encoding="utf-8",
    )


def _patch_state_file_issue_numbers(numbers: dict[str, int]) -> None:
    """After Phase C executors return real issue numbers, update
    .state.json's open_issues map. The state file was already written
    by Phase B with None placeholders."""
    if not STATE_FILE.is_file():
        return
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    open_issues = data.get("open_issues", {}) or {}
    for key, num in numbers.items():
        open_issues[key] = num
    data["open_issues"] = open_issues
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    tmp.replace(STATE_FILE)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scheduled KB audit cron runner (production entrypoint)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Build plan, but do not write or execute anything.",
    )
    parser.add_argument(
        "--no-execute", action="store_true",
        help="Persist audit log + state, but skip git/gh actions.",
    )
    parser.add_argument(
        "--today", type=str, default=None,
        help="Override today (ISO date) for testing/replay.",
    )
    args = parser.parse_args()

    today_override: Optional[date] = None
    if args.today:
        today_override = datetime.fromisoformat(args.today).date()

    return run(
        dry_run=args.dry_run,
        no_execute=args.no_execute,
        today_override=today_override,
    )


if __name__ == "__main__":
    sys.exit(main())
