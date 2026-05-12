#!/usr/bin/env python3
"""Integrate Phase-1 UA-translation agent branches into a single integration branch.

Workflow per branch (in agent order ua-01..ua-14):
  1. git fetch origin <branch>
  2. git merge --no-ff --no-commit origin/<branch>
     - if conflict → abort, write report row "conflict", continue with next
     - if clean → commit with summary message
  3. After each merge, run UA quality validator + KB loader on touched dirs
     - record before/after error counts
  4. After all 14 → final report.

Allowlists were disjoint by design (audit-driven partition), so conflicts
should be rare. When they occur, the script does NOT improvise resolution
— it aborts that merge and continues; the orchestrator decides per-case.

Use `--dry-run` to preview each merge without committing.
Use `--skip <branch-name>` to defer a specific branch.
Use `--branch <name>` (repeatable) to override the auto-discovery list.

Run from repo root, on the integration branch you want to receive the
merges.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PYTHON = "C:/Python312/python.exe"

# Agent → entity-type mapping for targeted validation post-merge.
AGENT_SCOPES: dict[str, list[str]] = {
    "ua-01": ["diseases"],
    "ua-02": ["biomarkers"],
    "ua-03": ["biomarker_actionability"],
    "ua-04": ["biomarker_actionability"],
    "ua-05": ["biomarker_actionability"],
    "ua-06": ["indications"],
    "ua-07": ["indications"],
    "ua-08": ["indications"],
    "ua-09": ["redflags"],
    "ua-10": ["redflags"],
    "ua-11": ["regimens"],
    "ua-12": ["regimens"],
    "ua-13": ["algorithms"],
    "ua-14": ["drugs", "procedures", "radiation_courses"],
}


def run(cmd: list[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=REPO,
        text=True,
        capture_output=capture,
        check=check,
    )


def git(*args: str, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return run(["git", *args], check=check, capture=capture)


def discover_branches() -> list[tuple[str, str]]:
    """Find remote branches that look like agent-pushed worktree branches.

    Returns list of (agent_id, branch_ref) pairs in ua-01..ua-14 order.
    Falls back to interactive entry if discovery fails.
    """
    git("fetch", "origin", "--prune")
    out = git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin").stdout
    candidates = [
        line.strip()
        for line in out.splitlines()
        if "worktree-agent-" in line or "feat/ua-fullquality" in line
    ]
    return [("auto", b) for b in candidates]


def quality_counts(scope_dirs: list[str]) -> dict[str, int]:
    """Run ua_quality on the given KB subdirs; parse summary line."""
    paths = [str(REPO / "knowledge_base" / "hosted" / "content" / d) for d in scope_dirs]
    proc = run([PYTHON, "-m", "knowledge_base.validation.ua_quality", "--summary-only", *paths],
               check=False)
    out = proc.stdout + proc.stderr
    # Last summary line: "UA quality: <N> files checked, <E> errors, <W> warnings."
    errors = warnings = files = 0
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("UA quality:"):
            try:
                parts = line.split()
                files = int(parts[2])
                errors = int(parts[5])
                warnings = int(parts[7])
            except (IndexError, ValueError):
                pass
    return {"files": files, "errors": errors, "warnings": warnings}


def loader_ok() -> bool:
    proc = run([PYTHON, "-m", "knowledge_base.validation.loader",
                "knowledge_base/hosted/content"], check=False)
    return proc.returncode == 0


def merge_one(branch: str, agent_id: str, dry_run: bool) -> dict:
    """Try to merge one branch. Return result row."""
    row = {
        "branch": branch,
        "agent": agent_id,
        "scope": AGENT_SCOPES.get(agent_id, []),
        "status": "",
        "files_changed": 0,
        "ua_errors_before": None,
        "ua_errors_after": None,
        "loader_ok_after": None,
        "note": "",
    }
    scope = AGENT_SCOPES.get(agent_id, ["diseases"])
    pre = quality_counts(scope)
    row["ua_errors_before"] = pre["errors"]

    proc = git("merge", "--no-ff", "--no-commit",
               f"origin/{branch}" if not branch.startswith("origin/") else branch,
               check=False)
    if proc.returncode != 0:
        row["status"] = "conflict"
        row["note"] = (proc.stdout + proc.stderr).strip()[:200]
        git("merge", "--abort", check=False)
        return row

    diff = git("diff", "--cached", "--name-only").stdout
    row["files_changed"] = len([l for l in diff.splitlines() if l.strip()])

    if dry_run:
        git("merge", "--abort", check=False)
        row["status"] = "dry-run-clean"
        return row

    # Commit the merge.
    msg = f"Merge agent {agent_id} branch {branch} into integration"
    git("commit", "-m", msg, check=True)

    post = quality_counts(scope)
    row["ua_errors_after"] = post["errors"]
    row["loader_ok_after"] = loader_ok()
    row["status"] = "merged"
    return row


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--branch", action="append", default=[],
                    help="Explicit branch to merge (repeatable). agent_id must be supplied via --agent-map.")
    ap.add_argument("--agent-map", action="append", default=[],
                    help="branch=agent-id pair, e.g. worktree-agent-aaab85c84f3246a66=ua-01")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", type=Path,
                    default=REPO / "docs" / "reviews" / f"ua-phase1-integration-{dt.date.today().isoformat()}.json")
    args = ap.parse_args()

    # Build (agent_id, branch) list.
    pairs: list[tuple[str, str]] = []
    if args.branch:
        amap = dict(p.split("=", 1) for p in args.agent_map)
        for b in args.branch:
            pairs.append((amap.get(b, "unknown"), b))
    else:
        # Discovery mode — list candidates so user can re-run with --branch.
        candidates = discover_branches()
        print("Discovered candidate branches (re-run with explicit --branch / --agent-map):")
        for _, b in candidates:
            print(f"  {b}")
        return 0

    print(f"Merging {len(pairs)} branches (dry-run={args.dry_run})\n")
    results = []
    for agent_id, branch in pairs:
        print(f"\n=== {agent_id} ← {branch} ===")
        row = merge_one(branch, agent_id, args.dry_run)
        results.append(row)
        delta = ""
        if row["ua_errors_before"] is not None and row["ua_errors_after"] is not None:
            delta = f" ({row['ua_errors_before']} → {row['ua_errors_after']} errors)"
        print(f"  status: {row['status']}  files: {row['files_changed']}{delta}")
        if row["note"]:
            print(f"  note: {row['note']}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\nReport: {args.out.relative_to(REPO)}")
    print(f"Merged: {sum(1 for r in results if r['status'] == 'merged')} / {len(results)}")
    print(f"Conflicts: {sum(1 for r in results if r['status'] == 'conflict')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
