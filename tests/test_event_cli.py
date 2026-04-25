"""Tests for the clinician event CLI (knowledge_base/engine/event_cli.py).

Verifies:
1. `add` command writes a valid event and prints the path
2. `list` command emits human and --json output
3. Validation errors return non-zero
4. --event-id auto-generation produces a usable id
5. --skip-if-exists is honoured
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent


def _run(*args: str, cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "knowledge_base.engine.event_cli", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _add_minimal(root: Path, pid: str, event_id: str | None = None, **extra: str) -> subprocess.CompletedProcess:
    args = [
        "--root", str(root),
        "add", pid,
        "--event-type", "confirmed",
        "--target-type", "regimen",
        "--target-id", "REG-VRD",
        "--summary", "Confirmed at MDT",
    ]
    if event_id:
        args += ["--event-id", event_id]
    for k, v in extra.items():
        args += [f"--{k.replace('_', '-')}", v]
    return _run(*args)


def test_add_writes_event_file(tmp_path):
    r = _add_minimal(tmp_path, "patient-cli-1", event_id="ev-1")
    assert r.returncode == 0, r.stderr
    log = tmp_path / "patient-cli-1" / "events.jsonl"
    assert log.is_file()
    line = log.read_text(encoding="utf-8").strip()
    payload = json.loads(line)
    assert payload["event_id"] == "ev-1"
    assert payload["event_type"] == "confirmed"
    assert payload["target_id"] == "REG-VRD"


def test_add_auto_event_id(tmp_path):
    r = _add_minimal(tmp_path, "patient-cli-auto")
    assert r.returncode == 0, r.stderr
    assert "Appended ev-" in r.stdout
    log = tmp_path / "patient-cli-auto" / "events.jsonl"
    payload = json.loads(log.read_text(encoding="utf-8").strip())
    assert payload["event_id"].startswith("ev-")


def test_add_json_output(tmp_path):
    r = _run(
        "--root", str(tmp_path),
        "add", "patient-cli-json",
        "--event-type", "approved",
        "--target-type", "plan_section",
        "--target-id", "TRACK-AGGRESSIVE",
        "--summary", "Approved by co-lead",
        "--actor-id", "dr.x",
        "--evidence", "ESMO-MM-2023", "NCCN-MM-2024",
        "--json",
    )
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["event"]["evidence_refs"] == ["ESMO-MM-2023", "NCCN-MM-2024"]
    assert out["event"]["actor_id"] == "dr.x"


def test_add_invalid_event_type_returns_nonzero(tmp_path):
    r = _run(
        "--root", str(tmp_path),
        "add", "patient-cli-bad",
        "--event-type", "exploded",
        "--target-type", "regimen",
        "--target-id", "REG-X",
        "--summary", "x",
    )
    assert r.returncode != 0
    assert "exploded" in r.stderr or "invalid choice" in r.stderr


def test_list_empty(tmp_path):
    r = _run("--root", str(tmp_path), "list", "no-such-patient")
    assert r.returncode == 0
    assert "no events" in r.stdout


def test_list_after_add_human(tmp_path):
    pid = "patient-cli-list"
    _add_minimal(tmp_path, pid, event_id="ev-1")
    _add_minimal(tmp_path, pid, event_id="ev-2", summary="Second action")
    r = _run("--root", str(tmp_path), "list", pid)
    assert r.returncode == 0, r.stderr
    assert "ev-1" in r.stdout
    assert "ev-2" in r.stdout
    assert "Events for patient-cli-list (2)" in r.stdout


def test_list_after_add_json(tmp_path):
    pid = "patient-cli-listjson"
    _add_minimal(tmp_path, pid, event_id="ev-1")
    _add_minimal(tmp_path, pid, event_id="ev-2")
    r = _run("--root", str(tmp_path), "list", pid, "--json")
    assert r.returncode == 0, r.stderr
    payload = json.loads(r.stdout)
    assert [e["event_id"] for e in payload] == ["ev-1", "ev-2"]


def test_skip_if_exists_idempotent(tmp_path):
    pid = "patient-cli-skip"
    _add_minimal(tmp_path, pid, event_id="ev-once")
    r = _run(
        "--root", str(tmp_path),
        "add", pid,
        "--event-type", "confirmed",
        "--target-type", "regimen",
        "--target-id", "REG-VRD",
        "--summary", "duplicate attempt",
        "--event-id", "ev-once",
        "--skip-if-exists",
    )
    assert r.returncode == 0, r.stderr
    log = tmp_path / pid / "events.jsonl"
    lines = [ln for ln in log.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 1
