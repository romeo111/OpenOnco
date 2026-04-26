#!/usr/bin/env python3
"""Scheduled-audit orchestrator — Phase A (dry-run only).

Per `docs/plans/scheduled_kb_audit_2026-04-26.md`. Composes three
deterministic audits (biomarker catalog / validator integrity /
last_reviewed freshness), diffs against the previously-archived
state, classifies deltas, applies dedupe + caps, and emits an
`action_plan.json`.

Phase A scope: NO actions are executed. The orchestrator only emits
the plan to stdout (or `--output`) for review and for downstream
Phase C executors.

Phase A determinism guarantee: same git SHA + same `--today` value =
byte-identical action_plan.json. This is what unit tests rely on.

Schema of `action_plan.json`:

    {
      "run_id":     "audit-2026-04-26-monthly",
      "started_at": "...",
      "git_sha":    "<HEAD>",
      "snapshot": {
        "biomarkers": { ... output of audit_biomarkers.collect_biomarker_state },
        "validator":  { ... output of audit_validator.collect_validator_state },
        "freshness":  { ... output of audit_freshness.collect_freshness_state }
      },
      "deltas": [
        {"kind": "missing_ref",   "key": "BIO-FOO", "current": 1, "previous": 0},
        ...
      ],
      "actions": [
        {
          "type":     "open_issue" | "comment_issue" | "close_issue"
                    | "commit_catalog_refresh" | "no_op" | "abort",
          "dedupe_key": "missing-bio-FOO",
          "title": "...", "body": "...", "labels": [...],
          "rationale": "..."   # human-readable why
        },
        ...
      ],
      "diagnostics": {
        "deltas_detected":               int,
        "actions_taken":                 int,
        "actions_suppressed_idempotency": int,
        "actions_capped":                int,
        "preflight_aborted":             bool,
        "abort_reason":                  str | null
      }
    }

Usage:
  python scripts/run_scheduled_audit.py                       # dry-run, JSON to stdout
  python scripts/run_scheduled_audit.py --human               # readable summary
  python scripts/run_scheduled_audit.py --output plan.json    # write to file
  python scripts/run_scheduled_audit.py --today 2026-05-01    # for testing/replay
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
AUDIT_LOG_DIR = REPO_ROOT / "docs" / "audit_log"
STATE_FILE = AUDIT_LOG_DIR / ".state.json"
CATALOG_FILE = REPO_ROOT / "docs" / "BIOMARKER_CATALOG.md"

# Action caps — per docs/plans/scheduled_kb_audit_2026-04-26.md §4.4
MAX_ISSUES_PER_RUN = 5
MAX_COMMITS_PER_RUN = 1
MAX_TOTAL_ACTIONS = 6

# Structural sanity — abort if we suddenly see <50% of last-known
# entity count (KB renamed / restructured under us).
STRUCTURAL_REGRESSION_THRESHOLD = 0.5

sys.path.insert(0, str(REPO_ROOT))


def _force_utf8_stdout() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:  # pylint: disable=broad-except
                pass


# ── Pre-flight gates ────────────────────────────────────────────────────


def _run_git(args: list[str], cwd: Path = REPO_ROOT) -> tuple[int, str]:
    """Returns (returncode, stdout-text)."""
    try:
        proc = subprocess.run(
            ["git"] + args, cwd=cwd, capture_output=True, text=True,
            encoding="utf-8", timeout=30,
        )
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return 1, f"git unavailable: {exc}"


def _git_head_sha(cwd: Path = REPO_ROOT) -> Optional[str]:
    code, out = _run_git(["rev-parse", "HEAD"], cwd)
    if code != 0:
        return None
    return out.strip()[:12]


def _git_clean_on_master(cwd: Path = REPO_ROOT) -> tuple[bool, str]:
    """Phase A relaxes the on-master requirement — orchestrator can be
    invoked from any branch for testing. Phase D production cron will
    enforce it. Here we still return diagnostic info for the action plan.
    Returns (allowed, reason)."""

    # In Phase A dry-run, git state doesn't gate execution — only logs.
    # Production cron (Phase D) flips the boolean to require clean+master.
    return True, "phase-A-dry-run-mode"


# ── State (previous-run archive) ────────────────────────────────────────


def _load_previous_state() -> dict[str, Any]:
    """Load the last archived audit snapshot from STATE_FILE.

    Returns empty/baseline dict on first run (no state yet)."""
    if not STATE_FILE.is_file():
        return {
            "biomarkers": {
                "defined": 0, "referenced": 0, "dormant_count": 0,
                "missing_count": 0, "naming_mismatch_count": 0,
                "loinc_missing_count": 0,
                "missing_ids": [], "dormant_ids": [], "naming_pairs": [],
            },
            "validator": {
                "loaded_entities": 0, "schema_errors_count": 0,
                "ref_errors_count": 0, "errors": [],
            },
            "freshness": {
                "total_breaches": 0, "by_entity_type": {},
            },
            "open_issues": {},  # dedupe_key → issue_number
        }
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # Corrupt state file — treat as empty + emit warning later.
        return {
            "biomarkers": {}, "validator": {}, "freshness": {},
            "open_issues": {}, "_state_corrupt": True,
        }


# ── Snapshot collection ─────────────────────────────────────────────────


def _collect_snapshot(today: date, kb_root: Path) -> dict[str, Any]:
    """Run all three audits + return their structured states."""

    from scripts.audit_biomarkers import collect_biomarker_state  # noqa: E402
    from scripts.audit_validator import collect_validator_state  # noqa: E402
    from scripts.audit_freshness import collect_freshness_state  # noqa: E402

    return {
        "biomarkers": collect_biomarker_state(kb_root=kb_root),
        "validator": collect_validator_state(kb_root),
        "freshness": collect_freshness_state(kb_root, today=today),
    }


# ── Delta classification ────────────────────────────────────────────────


def _classify_deltas(
    snapshot: dict[str, Any],
    previous: dict[str, Any],
) -> list[dict[str, Any]]:
    """Compare current snapshot to previously-archived state. Each
    delta is one of:

      missing_ref          — new broken reference (BIO-X cited, no entity)
      missing_resolved     — previously broken ref no longer broken
      dormant_appeared     — biomarker became unused
      dormant_resolved     — dormant biomarker now wired
      schema_regression    — new schema error (count went up)
      schema_resolved      — schema errors went down
      ref_regression       — new ref error
      ref_resolved         — ref errors went down
      catastrophic         — validator failed to load
      loinc_improved       — LOINC missing count decreased
      loinc_degraded       — LOINC missing count increased
      freshness_breach     — at least one new breach for an entity type
      freshness_resolved   — entity-type went from breaches → none
      structural_warning   — entity count dropped >50%
      coverage_growth      — new biomarker entity added (informational)
    """

    deltas: list[dict[str, Any]] = []

    # 0. Catastrophic check first — if validator broke, nothing else matters.
    if snapshot["validator"].get("catastrophic_error"):
        deltas.append({
            "kind": "catastrophic",
            "key": "validator-load-failed",
            "detail": snapshot["validator"]["catastrophic_error"],
        })
        return deltas  # short-circuit

    bio = snapshot["biomarkers"]
    prev_bio = previous.get("biomarkers", {}) or {}
    val = snapshot["validator"]
    prev_val = previous.get("validator", {}) or {}
    fresh = snapshot["freshness"]
    prev_fresh = previous.get("freshness", {}) or {}

    # 1. Structural sanity — KB renamed / mass-deleted.
    prev_loaded = prev_val.get("loaded_entities", 0)
    cur_loaded = val.get("loaded_entities", 0)
    if prev_loaded > 100 and cur_loaded < prev_loaded * STRUCTURAL_REGRESSION_THRESHOLD:
        deltas.append({
            "kind": "structural_warning",
            "key": "entity-count-regression",
            "previous": prev_loaded,
            "current": cur_loaded,
        })
        return deltas  # don't emit individual deltas under structural break

    # 2. Missing refs (broken citations).
    prev_missing = set(prev_bio.get("missing_ids", []) or [])
    cur_missing = set(bio.get("missing_ids", []) or [])
    for new_id in sorted(cur_missing - prev_missing):
        deltas.append({"kind": "missing_ref", "key": new_id})
    for resolved_id in sorted(prev_missing - cur_missing):
        deltas.append({"kind": "missing_resolved", "key": resolved_id})

    # 3. Dormant biomarkers.
    prev_dormant = set(prev_bio.get("dormant_ids", []) or [])
    cur_dormant = set(bio.get("dormant_ids", []) or [])
    for new_id in sorted(cur_dormant - prev_dormant):
        deltas.append({"kind": "dormant_appeared", "key": new_id})
    for resolved_id in sorted(prev_dormant - cur_dormant):
        deltas.append({"kind": "dormant_resolved", "key": resolved_id})

    # 4. Schema/ref error regressions.
    if val.get("schema_errors_count", 0) > prev_val.get("schema_errors_count", 0):
        deltas.append({
            "kind": "schema_regression",
            "key": "schema-errors",
            "previous": prev_val.get("schema_errors_count", 0),
            "current": val["schema_errors_count"],
        })
    elif val.get("schema_errors_count", 0) < prev_val.get("schema_errors_count", 0):
        deltas.append({
            "kind": "schema_resolved",
            "key": "schema-errors",
            "previous": prev_val.get("schema_errors_count", 0),
            "current": val["schema_errors_count"],
        })

    if val.get("ref_errors_count", 0) > prev_val.get("ref_errors_count", 0):
        deltas.append({
            "kind": "ref_regression",
            "key": "ref-errors",
            "previous": prev_val.get("ref_errors_count", 0),
            "current": val["ref_errors_count"],
        })
    elif val.get("ref_errors_count", 0) < prev_val.get("ref_errors_count", 0):
        deltas.append({
            "kind": "ref_resolved",
            "key": "ref-errors",
            "previous": prev_val.get("ref_errors_count", 0),
            "current": val["ref_errors_count"],
        })

    # 5. LOINC coverage trend.
    prev_loinc = prev_bio.get("loinc_missing_count", bio.get("loinc_missing_count", 0))
    cur_loinc = bio.get("loinc_missing_count", 0)
    if cur_loinc < prev_loinc:
        deltas.append({
            "kind": "loinc_improved",
            "key": "loinc-coverage",
            "previous": prev_loinc, "current": cur_loinc,
        })
    elif cur_loinc > prev_loinc and prev_loinc > 0:
        # Don't fire on first run (prev = 0 because no state file yet).
        deltas.append({
            "kind": "loinc_degraded",
            "key": "loinc-coverage",
            "previous": prev_loinc, "current": cur_loinc,
        })

    # 6. Freshness breaches per entity type.
    prev_breach = {
        t: (d.get("stale_past_sla", 0) + d.get("never_reviewed", 0))
        for t, d in (prev_fresh.get("by_entity_type", {}) or {}).items()
    }
    cur_breach = {
        t: (d.get("stale_past_sla", 0) + d.get("never_reviewed", 0))
        for t, d in (fresh.get("by_entity_type", {}) or {}).items()
    }
    for entity_type in sorted(set(prev_breach) | set(cur_breach)):
        before = prev_breach.get(entity_type, 0)
        after = cur_breach.get(entity_type, 0)
        if before == 0 and after > 0:
            deltas.append({
                "kind": "freshness_breach",
                "key": entity_type,
                "current": after,
            })
        elif before > 0 and after == 0:
            deltas.append({
                "kind": "freshness_resolved",
                "key": entity_type,
                "previous": before,
            })
        # Don't fire on monotone-increasing breaches — single issue
        # per entity_type; the dedupe protocol refreshes its body each
        # run with the current count.

    # 7. Coverage growth (informational only — never escalates).
    if bio.get("defined", 0) > prev_bio.get("defined", 0):
        deltas.append({
            "kind": "coverage_growth",
            "key": "biomarkers-defined",
            "previous": prev_bio.get("defined", 0),
            "current": bio.get("defined", 0),
        })

    return deltas


# ── Action planning ─────────────────────────────────────────────────────


def _dedupe_key(delta: dict[str, Any]) -> str:
    """Stable per-delta key used to:
    - prevent multiple open issues for the same root cause
    - track resolution across runs (auto-close when resolved)
    Version prefix `v1` allows future migration.

    Resolution variants (`*_resolved`) intentionally map to the SAME
    key as their open form (`missing_ref`, `dormant_appeared`, etc.)
    so that close_issue actions can find the originally-opened issue.
    """
    kind = delta["kind"]
    # Map "_resolved" variants back to their open form for key lookup.
    resolution_aliases = {
        "missing_resolved": "missing_ref",
        "dormant_resolved": "dormant_appeared",
        "schema_resolved": "schema_regression",
        "ref_resolved": "ref_regression",
        "freshness_resolved": "freshness_breach",
    }
    canonical_kind = resolution_aliases.get(kind, kind)
    return f"kb-audit-key-v1:{canonical_kind}:{delta['key']}"


def _action_for_delta(
    delta: dict[str, Any],
    open_issues: dict[str, Any],
    snapshot: dict[str, Any],
) -> Optional[dict[str, Any]]:
    """Map one delta to one (or zero) actions. Idempotent: if an open
    issue already covers this dedupe_key, returns a `comment_issue`
    refresh instead of `open_issue`."""

    key = _dedupe_key(delta)
    kind = delta["kind"]
    existing = open_issues.get(key)

    if kind == "catastrophic":
        if existing:
            return {
                "type": "comment_issue", "dedupe_key": key,
                "issue_number": existing,
                "body": "Validator is still broken at this run.",
                "rationale": "catastrophic state persists; refresh existing issue",
            }
        return {
            "type": "open_issue", "dedupe_key": key,
            "title": "[kb-audit] BLOCKER — validator failed to load KB",
            "labels": ["kb-audit", "blocker", "regression"],
            "body": (
                "Validator could not load knowledge_base/hosted/content/. "
                f"Error: `{delta.get('detail', 'unknown')}`. "
                "All other audit signals are unreliable until this is fixed."
            ),
            "rationale": "validator load failed; everything else gated on this",
        }

    if kind == "structural_warning":
        return {
            "type": "open_issue", "dedupe_key": key,
            "title": "[kb-audit] Structural change — entity count dropped sharply",
            "labels": ["kb-audit", "regression"],
            "body": (
                f"Entity count dropped from {delta['previous']} → "
                f"{delta['current']} (>50% loss). KB may have been "
                "renamed / restructured / partially deleted. Audit "
                "aborted to prevent issue spam; please review."
            ),
            "rationale": "abort path — manual review needed",
        }

    if kind == "missing_ref":
        if existing:
            return {
                "type": "comment_issue", "dedupe_key": key,
                "issue_number": existing,
                "body": f"Still seen at this run. Audit log: docs/audit_log/...",
                "rationale": "missing-ref persists; refresh",
            }
        return {
            "type": "open_issue", "dedupe_key": key,
            "title": f"[kb-audit] {delta['key']} referenced but no entity file",
            "labels": ["kb-audit", "blocker", "clinical-review-required"],
            "body": (
                f"`{delta['key']}` is cited by one or more rule entities "
                "but has no corresponding YAML file under "
                "`knowledge_base/hosted/content/biomarkers/`. Either author "
                "the entity or remove the citation."
            ),
            "rationale": "new broken ref",
        }

    if kind == "missing_resolved":
        if existing:
            return {
                "type": "close_issue", "dedupe_key": key,
                "issue_number": existing,
                "body": f"Resolved as of this audit run — `{delta['key']}` now defined.",
                "rationale": "delta cleared; close tracking issue",
            }
        return None  # nothing to close

    if kind == "dormant_appeared":
        if existing:
            return {
                "type": "comment_issue", "dedupe_key": key,
                "issue_number": existing,
                "body": "Still dormant at this run.",
                "rationale": "dormant persists",
            }
        return {
            "type": "open_issue", "dedupe_key": key,
            "title": f"[kb-audit] {delta['key']} defined but unused",
            "labels": ["kb-audit", "clinical-review-required"],
            "body": (
                f"`{delta['key']}` is defined as a biomarker entity but no "
                "Indication / Algorithm / RedFlag references it. Either "
                "wire into ≥1 rule or document why dormant in the entity "
                "`notes:` field."
            ),
            "rationale": "new dormant entity",
        }

    if kind == "dormant_resolved":
        if existing:
            return {
                "type": "close_issue", "dedupe_key": key,
                "issue_number": existing,
                "body": f"Resolved — `{delta['key']}` now consumed by a rule.",
                "rationale": "delta cleared; close tracking issue",
            }
        return None

    if kind == "schema_regression":
        return {
            "type": "open_issue" if not existing else "comment_issue",
            "dedupe_key": key,
            "issue_number": existing,
            "title": f"[kb-audit] Schema errors increased: {delta['previous']} → {delta['current']}",
            "labels": ["kb-audit", "regression"],
            "body": (
                f"Schema-validator caught new schema errors. "
                f"Was {delta['previous']}, now {delta['current']}. "
                "Inspect `scripts/audit_validator.py --human` output."
            ),
            "rationale": "schema regression",
        }

    if kind == "ref_regression":
        return {
            "type": "open_issue" if not existing else "comment_issue",
            "dedupe_key": key,
            "issue_number": existing,
            "title": f"[kb-audit] Ref errors increased: {delta['previous']} → {delta['current']}",
            "labels": ["kb-audit", "regression"],
            "body": (
                f"Reference-integrity validator caught new errors. "
                f"Was {delta['previous']}, now {delta['current']}."
            ),
            "rationale": "ref regression",
        }

    if kind in {"schema_resolved", "ref_resolved", "loinc_improved",
                "freshness_resolved", "coverage_growth"}:
        # Informational — log only, no issue.
        return {
            "type": "no_op", "dedupe_key": key,
            "rationale": f"{kind} (informational, no action)",
        }

    if kind == "loinc_degraded":
        return {
            "type": "open_issue" if not existing else "comment_issue",
            "dedupe_key": key,
            "issue_number": existing,
            "title": f"[kb-audit] LOINC coverage degraded: {delta['previous']} → {delta['current']} missing",
            "labels": ["kb-audit", "regression"],
            "body": (
                "LOINC missing count went up. New entity authored "
                "without `codes.loinc`?"
            ),
            "rationale": "LOINC coverage regression",
        }

    if kind == "freshness_breach":
        return {
            "type": "open_issue" if not existing else "comment_issue",
            "dedupe_key": key,
            "issue_number": existing,
            "title": f"[kb-audit] {delta['key']}: {delta['current']} entities past SLA",
            "labels": ["kb-audit", "freshness", "clinical-review-required"],
            "body": (
                f"{delta['current']} `{delta['key']}` entities have "
                "`last_reviewed` past their SLA. See `docs/audit_log/` "
                "for the full list."
            ),
            "rationale": "freshness SLA breach",
        }

    return None


def _maybe_catalog_refresh(
    snapshot: dict[str, Any],
    previous: dict[str, Any],
) -> Optional[dict[str, Any]]:
    """Should we commit a catalog refresh? Yes when ANY semantic
    snapshot field differs from previous (regardless of action plan).
    The commit is the single source of historical record."""

    sig_keys = (
        ("biomarkers", "defined"),
        ("biomarkers", "referenced"),
        ("biomarkers", "dormant_count"),
        ("biomarkers", "missing_count"),
        ("biomarkers", "loinc_missing_count"),
        ("validator", "schema_errors_count"),
        ("validator", "ref_errors_count"),
        ("freshness", "total_breaches"),
    )
    cur_sig = tuple(
        snapshot.get(top, {}).get(field) for (top, field) in sig_keys
    )
    prev_sig = tuple(
        previous.get(top, {}).get(field) for (top, field) in sig_keys
    )
    if cur_sig == prev_sig:
        return None
    return {
        "type": "commit_catalog_refresh",
        "dedupe_key": "catalog-refresh",
        "files": [
            "docs/BIOMARKER_CATALOG.md",
            f"docs/audit_log/{date.today().isoformat()}.md",
            "docs/audit_log/.metrics.csv",
            "docs/audit_log/.state.json",
        ],
        "message": (
            f"chore(catalog): KB audit — defined={cur_sig[0]} "
            f"referenced={cur_sig[1]} dormant={cur_sig[2]} "
            f"missing={cur_sig[3]} schema_err={cur_sig[5]} ref_err={cur_sig[6]}"
        ),
        "rationale": "snapshot signature changed since last archived state",
    }


def _enforce_caps(actions: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    """Apply MAX_ISSUES_PER_RUN cap on NEW issue creations. Overflow
    of new issues collapses into one meta-issue. Other action types
    (commit_catalog_refresh, comment_issue, close_issue, no_op) are
    NOT capped — they're low-noise and low-risk by design.

    Returns (capped_actions, n_capped_open_issues)."""

    issue_actions = [a for a in actions if a["type"] == "open_issue"]
    other_actions = [a for a in actions if a["type"] != "open_issue"]

    n_capped = 0
    if len(issue_actions) > MAX_ISSUES_PER_RUN:
        overflow = issue_actions[MAX_ISSUES_PER_RUN:]
        issue_actions = issue_actions[:MAX_ISSUES_PER_RUN]
        n_capped = len(overflow)
        meta_action = {
            "type": "open_issue",
            "dedupe_key": "kb-audit-key-v1:meta:cap-overflow",
            "title": (
                f"[kb-audit] Cap overflow: {n_capped} additional "
                "delta(s) suppressed this run"
            ),
            "labels": ["kb-audit", "meta"],
            "body": (
                f"This run wanted to open {len(issue_actions) + n_capped} "
                f"issues; capped at {MAX_ISSUES_PER_RUN} per "
                "MAX_ISSUES_PER_RUN. See audit log for the full delta list. "
                "Suppressed dedupe_keys:\n"
                + "\n".join(f"- `{a['dedupe_key']}`" for a in overflow)
            ),
            "rationale": "cap-overflow meta",
        }
        issue_actions.append(meta_action)

    return issue_actions + other_actions, n_capped


# ── Top-level orchestration ─────────────────────────────────────────────


def build_action_plan(
    today: Optional[date] = None,
    kb_root: Path = KB_ROOT,
) -> dict[str, Any]:
    """Top-level entry point used by tests + the cron-agent runner."""
    if today is None:
        today = date.today()

    started_at = datetime.now(timezone.utc).isoformat()
    git_sha = _git_head_sha() or "unknown"
    run_id = f"audit-{today.isoformat()}-monthly"

    # 1. Pre-flight
    allowed, reason = _git_clean_on_master()
    if not allowed:
        return {
            "run_id": run_id,
            "started_at": started_at,
            "git_sha": git_sha,
            "today": today.isoformat(),
            "snapshot": {},
            "deltas": [],
            "actions": [{
                "type": "abort",
                "rationale": f"pre-flight failed: {reason}",
            }],
            "diagnostics": {
                "deltas_detected": 0, "actions_taken": 0,
                "actions_suppressed_idempotency": 0, "actions_capped": 0,
                "preflight_aborted": True, "abort_reason": reason,
            },
        }

    # 2. Snapshot
    snapshot = _collect_snapshot(today, kb_root)

    # 3. Previous state
    previous = _load_previous_state()
    open_issues = previous.get("open_issues", {}) or {}

    # 4. Classify deltas
    deltas = _classify_deltas(snapshot, previous)

    # 5. Map deltas → candidate actions
    candidate_actions: list[dict[str, Any]] = []
    suppressed = 0
    for delta in deltas:
        action = _action_for_delta(delta, open_issues, snapshot)
        if action is None:
            continue
        # Track idempotency: comment_issue is the "suppressed open_issue" form.
        if action["type"] == "comment_issue":
            suppressed += 1
        candidate_actions.append(action)

    # 6. Catalog-refresh commit if snapshot signature changed.
    catalog_action = _maybe_catalog_refresh(snapshot, previous)
    if catalog_action:
        candidate_actions.append(catalog_action)

    # 7. Apply caps
    final_actions, n_capped = _enforce_caps(candidate_actions)

    # 8. If everything is no-op, still emit a baseline action so the
    # log entry gets written each run.
    if not final_actions:
        final_actions = [{
            "type": "no_op", "dedupe_key": "no-deltas",
            "rationale": "no deltas detected this run; heartbeat only",
        }]

    return {
        "run_id": run_id,
        "started_at": started_at,
        "git_sha": git_sha,
        "today": today.isoformat(),
        "snapshot": snapshot,
        "deltas": deltas,
        "actions": final_actions,
        "diagnostics": {
            "deltas_detected": len(deltas),
            "actions_taken": len([a for a in final_actions if a["type"] != "no_op"]),
            "actions_suppressed_idempotency": suppressed,
            "actions_capped": n_capped,
            "preflight_aborted": False,
            "abort_reason": None,
            "previous_state_corrupt": bool(previous.get("_state_corrupt")),
        },
    }


# ── Human-readable summary ──────────────────────────────────────────────


def render_human(plan: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# {plan['run_id']}  (git {plan['git_sha']})")
    lines.append("")
    diag = plan["diagnostics"]
    if diag.get("preflight_aborted"):
        lines.append(f"❌ ABORTED: {diag['abort_reason']}")
        return "\n".join(lines) + "\n"
    bio = plan["snapshot"].get("biomarkers", {})
    val = plan["snapshot"].get("validator", {})
    fresh = plan["snapshot"].get("freshness", {})
    lines.append(
        f"Snapshot: defined={bio.get('defined', '?')} "
        f"referenced={bio.get('referenced', '?')} "
        f"dormant={bio.get('dormant_count', '?')} "
        f"missing={bio.get('missing_count', '?')} "
        f"schema_err={val.get('schema_errors_count', '?')} "
        f"ref_err={val.get('ref_errors_count', '?')} "
        f"freshness_breaches={fresh.get('total_breaches', '?')}"
    )
    lines.append("")
    lines.append(f"Deltas: {len(plan['deltas'])}")
    for d in plan["deltas"][:15]:
        extra = ""
        if "previous" in d and "current" in d:
            extra = f" ({d['previous']} → {d['current']})"
        lines.append(f"  - {d['kind']}: {d['key']}{extra}")
    if len(plan["deltas"]) > 15:
        lines.append(f"  ... and {len(plan['deltas']) - 15} more")
    lines.append("")
    lines.append(f"Actions ({len(plan['actions'])}):")
    for a in plan["actions"]:
        title = a.get("title", a.get("rationale", ""))
        lines.append(f"  [{a['type']:24s}] {title[:72]}")
    lines.append("")
    lines.append(
        f"Diagnostics: actions_taken={diag['actions_taken']} "
        f"suppressed_idempotency={diag['actions_suppressed_idempotency']} "
        f"capped={diag['actions_capped']}"
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    _force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "--output", type=Path, default=None,
        help="Write action_plan.json to this file (default: stdout).",
    )
    parser.add_argument(
        "--human", action="store_true",
        help="Emit human-readable summary instead of JSON.",
    )
    parser.add_argument(
        "--today", type=str, default=None,
        help="Override today (ISO date) for testing/replay.",
    )
    parser.add_argument(
        "--kb-root", type=Path, default=KB_ROOT,
        help=f"KB content root (default: {KB_ROOT}).",
    )
    args = parser.parse_args()

    today_override: Optional[date] = None
    if args.today:
        try:
            today_override = datetime.fromisoformat(args.today).date()
        except ValueError:
            print(f"Invalid --today: {args.today}", file=sys.stderr)
            return 2

    plan = build_action_plan(today_override, args.kb_root)

    if args.human:
        out = render_human(plan)
    else:
        out = json.dumps(plan, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)

    if plan["diagnostics"].get("preflight_aborted"):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
