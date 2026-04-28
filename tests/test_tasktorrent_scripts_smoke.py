"""Smoke tests for the bash-based onboarding scripts.

These don't replace shell-level tests (bats/shellcheck) but verify:
  - Syntax via `bash -n`
  - Exit codes + dry-run output for known-good inputs
  - Pre-flight error paths (auto_pr rejects wrong-branch / missing sidecar)

Skipped when bash is unavailable.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts" / "tasktorrent"
SCRIPTS = ["auto_claim.sh", "auto_pr.sh", "bootstrap_contributor.sh"]

if not shutil.which("bash"):
    pytest.skip("bash not on PATH", allow_module_level=True)


def run_bash(args: list[str], cwd: Path | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    """Invoke bash <script> <args> with default cwd at repo root."""
    full_env = dict(os.environ)
    if env:
        full_env.update(env)
    return subprocess.run(
        ["bash", *args],
        capture_output=True,
        text=True,
        cwd=cwd or SCRIPTS_DIR.parent.parent,
        env=full_env,
        timeout=30,
    )


# ---------- Syntax check ----------

@pytest.mark.parametrize("script", SCRIPTS)
def test_script_syntax_valid(script: str) -> None:
    res = subprocess.run(
        ["bash", "-n", str(SCRIPTS_DIR / script)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert res.returncode == 0, f"bash -n failed for {script}: {res.stderr}"


# ---------- auto_claim.sh ----------

def test_auto_claim_no_chunk_id_fails() -> None:
    res = run_bash([str(SCRIPTS_DIR / "auto_claim.sh")])
    assert res.returncode == 1
    assert "chunk-id is required" in res.stderr


def test_auto_claim_invalid_method_fails() -> None:
    res = run_bash(
        [str(SCRIPTS_DIR / "auto_claim.sh"), "test-chunk",
         "--method", "open-bidding", "--issue", "1", "--dry-run"]
    )
    assert res.returncode == 1
    assert "invalid --method" in res.stderr


def test_auto_claim_formal_issue_dry_run() -> None:
    res = run_bash(
        [str(SCRIPTS_DIR / "auto_claim.sh"), "test-chunk",
         "--method", "formal-issue", "--issue", "999", "--dry-run"]
    )
    assert res.returncode == 0
    assert "DRY-RUN" in res.stdout
    assert "+ gh issue comment 999" in res.stdout
    assert "I'd like to take this chunk" in res.stdout


def test_auto_claim_trusted_agent_dry_run() -> None:
    res = run_bash(
        [str(SCRIPTS_DIR / "auto_claim.sh"), "test-chunk",
         "--method", "trusted-agent-wip-branch-first", "--dry-run"]
    )
    assert res.returncode == 0
    assert "+ git checkout -b tasktorrent/test-chunk" in res.stdout
    assert "+ git commit --allow-empty" in res.stdout
    assert "+ git push -u origin tasktorrent/test-chunk" in res.stdout


def test_auto_claim_formal_issue_requires_issue_number() -> None:
    """Without --issue and without resolvable repo issues, formal-issue must fail."""
    # Use a repo unlikely to have a chunk-task issue matching "definitely-fake-chunk"
    res = run_bash(
        [str(SCRIPTS_DIR / "auto_claim.sh"), "definitely-fake-chunk",
         "--method", "formal-issue",
         "--repo", "romeo111/OpenOnco",
         "--dry-run"]
    )
    assert res.returncode == 1
    assert "formal-issue claim requires --issue" in res.stderr


# ---------- auto_pr.sh ----------

def test_auto_pr_no_chunk_id_fails() -> None:
    res = run_bash([str(SCRIPTS_DIR / "auto_pr.sh")])
    assert res.returncode == 1


def test_auto_pr_pre_flight_wrong_branch_fails() -> None:
    """We're on feat/tasktorrent-next-chunk-cli, not on tasktorrent/test-chunk."""
    res = run_bash(
        [str(SCRIPTS_DIR / "auto_pr.sh"), "test-chunk", "--dry-run"]
    )
    assert res.returncode == 3
    assert "pre-flight failed" in res.stderr


# ---------- bootstrap_contributor.sh ----------

def test_bootstrap_dry_run_with_no_clone() -> None:
    res = run_bash(
        [str(SCRIPTS_DIR / "bootstrap_contributor.sh"), "--no-clone", "--dry-run"]
    )
    # Possible outcomes:
    #   0 — dry-run completed
    #   1 — local Python missing
    #   2 — gh not authenticated (CI without gh login may hit this)
    assert res.returncode in (0, 1, 2)
    assert "TaskTorrent contributor bootstrap" in res.stdout


def test_bootstrap_unknown_arg_fails() -> None:
    res = run_bash(
        [str(SCRIPTS_DIR / "bootstrap_contributor.sh"), "--bogus-flag"]
    )
    assert res.returncode == 1
