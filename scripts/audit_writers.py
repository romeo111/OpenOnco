#!/usr/bin/env python3
"""Phase B writers: persist state, render audit log, append metrics row.

Per `docs/plans/scheduled_kb_audit_2026-04-26.md` §2.4 + §5 + §7.2.

Three pure(-ish) functions consumed by `run_scheduled_audit.py`:

  - write_state_file(plan, path)
        Serializes the snapshot + updated `open_issues` map. The map
        gates idempotency on the next run — without it, every run
        treats every delta as fresh.

  - render_audit_log_md(plan) → str
        Per-run markdown report. Stable schema across runs so
        clinicians + readers can scan time-series at-a-glance.

  - append_metrics_csv(plan, path)
        One row per run. CSV chosen over JSON-array so external
        tools (pandas, sheets, ad-hoc grep) can consume directly.

All three are deterministic given a fixed action_plan input — same
plan dict produces same outputs. Tests rely on this.
"""

from __future__ import annotations

import csv
import json
from io import StringIO
from pathlib import Path
from typing import Any

# Stable column order for `.metrics.csv`. Adding a column = bump version
# (or treat as a follow-up migration; pandas tolerates new columns).
METRICS_CSV_COLUMNS: tuple[str, ...] = (
    "date",                  # plan["today"]
    "run_id",
    "git_sha",
    "duration_s",            # populated by runner; "" in dry-run
    "biomarkers_defined",
    "biomarkers_referenced",
    "biomarkers_dormant",
    "biomarkers_missing",
    "loinc_missing",
    "schema_errors",
    "ref_errors",
    "contract_errors",
    "freshness_breaches",
    "deltas_detected",
    "actions_taken",
    "actions_capped",
)


# ── State file ──────────────────────────────────────────────────────────


def _updated_open_issues(plan: dict[str, Any]) -> dict[str, int]:
    """Compute the new open_issues map from previous map + this run's
    actions.

    Rules:
      - `open_issue` action: add entry (issue_number is unknown until
        the executor runs gh-CLI; in dry-run we record None as a
        placeholder; Phase C executors update with real number).
      - `comment_issue`: keep existing entry as-is (issue stays open).
      - `close_issue`: remove the entry.
      - All other action types: no change.

    The map is keyed by `dedupe_key` (the v1-prefixed full key). When
    Phase C executes, it patches placeholder Nones with real numbers
    by re-saving state after each gh-CLI call.
    """
    # Reconstruct previous map from the plan's snapshot — but the plan
    # itself doesn't carry it explicitly. Caller passes via wrapper.
    # We accept the map as input via the helper above; handled in
    # write_state_file().
    raise NotImplementedError("call _apply_action_effects directly")


def _apply_action_effects(
    previous_open: dict[str, int],
    actions: list[dict[str, Any]],
) -> dict[str, int]:
    """Pure transform: previous open_issues + actions → new open_issues."""

    out = dict(previous_open)
    for action in actions:
        kind = action.get("type")
        key = action.get("dedupe_key")
        if not key:
            continue
        if kind == "open_issue":
            # Issue number unknown in dry-run; preserve None placeholder
            # so Phase C executors can detect "needs gh create".
            if key not in out:
                out[key] = None  # type: ignore[assignment]
        elif kind == "close_issue":
            out.pop(key, None)
        elif kind == "comment_issue":
            # Keep existing entry — comment doesn't change open/close.
            pass
        # commit_catalog_refresh / no_op / abort: no map change.
    return out


def build_state_payload(
    plan: dict[str, Any],
    previous_open_issues: dict[str, Any],
) -> dict[str, Any]:
    """Compose the JSON payload the runner writes to `.state.json`.

    Schema (kept narrow — anything bigger lives in audit log MD):
      {
        "biomarkers": {<canonical biomarker snapshot subset>},
        "validator":  {<canonical validator snapshot subset>},
        "freshness":  {<canonical freshness snapshot subset>},
        "open_issues": {dedupe_key: issue_number|null},
        "last_run_id": "...",
        "last_run_today": "YYYY-MM-DD",
        "last_run_git_sha": "...",
      }

    Snapshot subsets are the same fields read by `_classify_deltas` —
    this is what diff-detection compares against next month.
    """
    snap = plan.get("snapshot", {}) or {}
    bio = snap.get("biomarkers", {}) or {}
    val = snap.get("validator", {}) or {}
    fresh = snap.get("freshness", {}) or {}

    bio_subset = {
        "defined": bio.get("defined", 0),
        "referenced": bio.get("referenced", 0),
        "dormant_count": bio.get("dormant_count", 0),
        "missing_count": bio.get("missing_count", 0),
        "naming_mismatch_count": bio.get("naming_mismatch_count", 0),
        "loinc_missing_count": bio.get("loinc_missing_count", 0),
        "missing_ids": list(bio.get("missing_ids", []) or []),
        "dormant_ids": list(bio.get("dormant_ids", []) or []),
        "naming_pairs": [list(p) for p in (bio.get("naming_pairs", []) or [])],
    }
    val_subset = {
        "loaded_entities": val.get("loaded_entities", 0),
        "schema_errors_count": val.get("schema_errors_count", 0),
        "ref_errors_count": val.get("ref_errors_count", 0),
        "contract_errors_count": val.get("contract_errors_count", 0),
        "errors": [],   # full error list lives in audit log MD, not state
    }
    fresh_subset = {
        "total_breaches": fresh.get("total_breaches", 0),
        "by_entity_type": {
            t: {
                "stale_past_sla": d.get("stale_past_sla", 0),
                "never_reviewed": d.get("never_reviewed", 0),
            }
            for t, d in (fresh.get("by_entity_type", {}) or {}).items()
        },
    }

    return {
        "biomarkers": bio_subset,
        "validator": val_subset,
        "freshness": fresh_subset,
        "open_issues": _apply_action_effects(
            previous_open_issues, plan.get("actions", []),
        ),
        "last_run_id": plan.get("run_id", ""),
        "last_run_today": plan.get("today", ""),
        "last_run_git_sha": plan.get("git_sha", ""),
    }


def write_state_file(
    plan: dict[str, Any],
    path: Path,
    previous_open_issues: dict[str, Any],
) -> None:
    """Serialize state payload to `path` (atomic write via tmpfile)."""
    payload = build_state_payload(plan, previous_open_issues)
    data = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(data, encoding="utf-8")
    tmp.replace(path)


# ── Audit log markdown ──────────────────────────────────────────────────


def render_audit_log_md(plan: dict[str, Any]) -> str:
    """Render one per-run markdown log per spec §2.4. Stable schema:
       header / snapshot table / actions / suppressed."""

    lines: list[str] = []
    run_id = plan.get("run_id", "unknown")
    today = plan.get("today", "")
    git_sha = plan.get("git_sha", "unknown")
    diag = plan.get("diagnostics", {}) or {}
    snap = plan.get("snapshot", {}) or {}
    bio = snap.get("biomarkers", {}) or {}
    val = snap.get("validator", {}) or {}
    fresh = snap.get("freshness", {}) or {}

    # Header
    lines.append(f"# KB audit — {today} (monthly)")
    lines.append("")
    lines.append(f"**Run id:** {run_id}")
    lines.append(f"**Git SHA:** {git_sha}")
    lines.append(f"**Started:** {plan.get('started_at', '')}")
    lines.append("")

    if diag.get("preflight_aborted"):
        lines.append(f"## ❌ ABORTED")
        lines.append("")
        lines.append(f"Reason: {diag.get('abort_reason', 'unknown')}")
        lines.append("")
        return "\n".join(lines) + "\n"

    # Snapshot summary
    lines.append("## Snapshot")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Defined biomarkers | {bio.get('defined', 0)} |")
    lines.append(f"| Referenced | {bio.get('referenced', 0)} |")
    lines.append(f"| Dormant | {bio.get('dormant_count', 0)} |")
    lines.append(f"| Broken refs (missing) | {bio.get('missing_count', 0)} |")
    lines.append(f"| LOINC missing | {bio.get('loinc_missing_count', 0)} |")
    lines.append(f"| Schema errors | {val.get('schema_errors_count', 0)} |")
    lines.append(f"| Ref errors | {val.get('ref_errors_count', 0)} |")
    lines.append(f"| Contract errors | {val.get('contract_errors_count', 0)} |")
    lines.append(f"| Freshness breaches | {fresh.get('total_breaches', 0)} |")
    lines.append("")

    # Deltas detected
    deltas = plan.get("deltas", []) or []
    lines.append(f"## Deltas detected ({len(deltas)})")
    lines.append("")
    if not deltas:
        lines.append("_No deltas this run — nothing changed since last archived state._")
    else:
        for d in deltas:
            extra = ""
            if "previous" in d and "current" in d:
                extra = f" ({d['previous']} → {d['current']})"
            lines.append(f"- **{d['kind']}** `{d['key']}`{extra}")
    lines.append("")

    # Actions taken
    actions = plan.get("actions", []) or []
    n_real = sum(1 for a in actions if a["type"] != "no_op")
    lines.append(f"## Actions ({n_real} taken / {len(actions)} total)")
    lines.append("")
    for a in actions:
        atype = a["type"]
        title = a.get("title") or a.get("rationale", "")
        marker = "•" if atype == "no_op" else "→"
        lines.append(f"- {marker} `{atype}` — {title}")
    lines.append("")

    # Diagnostics tail
    lines.append("## Diagnostics")
    lines.append("")
    lines.append(f"- Deltas detected: {diag.get('deltas_detected', 0)}")
    lines.append(f"- Actions executed: {diag.get('actions_taken', 0)}")
    lines.append(f"- Suppressed by idempotency: {diag.get('actions_suppressed_idempotency', 0)}")
    lines.append(f"- Capped (overflow): {diag.get('actions_capped', 0)}")
    if diag.get("previous_state_corrupt"):
        lines.append("- ⚠ Previous state file was corrupt; treated as empty.")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_audit_log(plan: dict[str, Any], dir_path: Path) -> Path:
    """Write the per-run audit log markdown. Returns the path written.

    Filename collision (same `today` re-run): suffix `-2`, `-3`, ...
    Caller can rely on a stable naming for the first run of a date.
    """
    today = plan.get("today", "unknown")
    base = dir_path / f"{today}.md"
    target = base
    n = 2
    while target.exists():
        target = dir_path / f"{today}-{n}.md"
        n += 1
    dir_path.mkdir(parents=True, exist_ok=True)
    target.write_text(render_audit_log_md(plan), encoding="utf-8")
    return target


# ── Metrics CSV ─────────────────────────────────────────────────────────


def metrics_row(plan: dict[str, Any]) -> dict[str, Any]:
    """Build one CSV row from an action plan. All values stringified —
    csv module handles quoting."""
    snap = plan.get("snapshot", {}) or {}
    bio = snap.get("biomarkers", {}) or {}
    val = snap.get("validator", {}) or {}
    fresh = snap.get("freshness", {}) or {}
    diag = plan.get("diagnostics", {}) or {}

    return {
        "date": plan.get("today", ""),
        "run_id": plan.get("run_id", ""),
        "git_sha": plan.get("git_sha", ""),
        "duration_s": plan.get("duration_s", ""),
        "biomarkers_defined": bio.get("defined", 0),
        "biomarkers_referenced": bio.get("referenced", 0),
        "biomarkers_dormant": bio.get("dormant_count", 0),
        "biomarkers_missing": bio.get("missing_count", 0),
        "loinc_missing": bio.get("loinc_missing_count", 0),
        "schema_errors": val.get("schema_errors_count", 0),
        "ref_errors": val.get("ref_errors_count", 0),
        "contract_errors": val.get("contract_errors_count", 0),
        "freshness_breaches": fresh.get("total_breaches", 0),
        "deltas_detected": diag.get("deltas_detected", 0),
        "actions_taken": diag.get("actions_taken", 0),
        "actions_capped": diag.get("actions_capped", 0),
    }


def append_metrics_csv(plan: dict[str, Any], path: Path) -> None:
    """Append one row to the metrics CSV. Writes header on first write.

    Idempotency: caller is responsible for deduping (e.g., not running
    twice in same minute). Each row has run_id which is date-keyed.
    """
    row = metrics_row(plan)

    file_exists = path.is_file()
    path.parent.mkdir(parents=True, exist_ok=True)

    # Use StringIO so we can validate before touching disk
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=METRICS_CSV_COLUMNS)
    if not file_exists:
        writer.writeheader()
    writer.writerow(row)

    with path.open("a", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


# ── Combined "persist this plan" entry point ────────────────────────────


def persist_plan_outputs(
    plan: dict[str, Any],
    audit_log_dir: Path,
    state_file: Path,
    metrics_csv: Path,
    previous_open_issues: dict[str, Any],
) -> dict[str, Path]:
    """Write all three artifacts. Used by the runner and by tests.

    Returns paths actually written (audit log path may include suffix
    on collision)."""
    log_path = write_audit_log(plan, audit_log_dir)
    write_state_file(plan, state_file, previous_open_issues)
    append_metrics_csv(plan, metrics_csv)
    return {
        "audit_log": log_path,
        "state_file": state_file,
        "metrics_csv": metrics_csv,
    }
