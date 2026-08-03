"""Deterministic, reviewer-queue audit for BiomarkerActionability ESCAT data.

This tool validates provenance and release-readiness metadata.  It never
assigns an ESCAT tier, changes a BMA, or makes a treatment decision.  Its
output is deliberately a queue for the two-reviewer clinical workflow.

Run with ``py -3.12 -m scripts.audit_escat_readiness --help``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from knowledge_base.schemas.biomarker_actionability import actionability_release_readiness


DEFAULT_BMA_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarker_actionability"
DEFAULT_BIOMARKER_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarkers"
DEFAULT_CIVIC_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "civic"
DEFAULT_MANIFEST = REPO_ROOT / "contributions" / "escat-tier-audit-full-2026-04-29-0030" / "task_manifest.txt"
STRONG_TIERS = frozenset({"IA", "IB"})
VARIANT_TOKEN = re.compile(r"\b[A-Z]\d{1,4}(?:[A-Z*]|DEL|INS)\b", re.IGNORECASE)
SEVERITY_ORDER = {"critical": 0, "major": 1, "minor": 2}


def load_yaml(path: Path) -> dict[str, Any] | None:
    """Read one mapping-shaped YAML document, returning None when malformed."""

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    return data if isinstance(data, dict) else None


def _iso_date(value: str | None) -> date | None:
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def find_latest_snapshot(civic_root: Path) -> tuple[Path | None, date | None]:
    """Return the newest YYYY-MM-DD CIViC snapshot directory and its date."""

    candidates: list[tuple[date, Path]] = []
    if civic_root.is_dir():
        for path in civic_root.iterdir():
            snapshot_date = _iso_date(path.name) if path.is_dir() else None
            if snapshot_date:
                candidates.append((snapshot_date, path))
    if not candidates:
        return None, None
    snapshot_date, path = max(candidates)
    return path, snapshot_date


def _variant_tokens(value: Any) -> set[str]:
    return {match.upper() for match in VARIANT_TOKEN.findall(str(value or ""))}


def _normalize_evidence_id(value: Any) -> str | None:
    match = re.search(r"(?:EID)?[-:]?(\d+)$", str(value or ""), flags=re.IGNORECASE)
    return match.group(1) if match else None


def _load_biomarker_lookup(biomarker_dir: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    if not biomarker_dir.is_dir():
        return out
    for path in sorted(biomarker_dir.rglob("*.yaml")):
        data = load_yaml(path)
        if data and data.get("id"):
            out[str(data["id"])] = data.get("actionability_lookup") or {}
    return out


def _load_civic_evidence(snapshot_dir: Path | None) -> dict[str, dict[str, Any]]:
    if not snapshot_dir:
        return {}
    data = load_yaml(snapshot_dir / "evidence.yaml") or {}
    evidence = data.get("evidence_items") or []
    return {
        str(item["id"]): item
        for item in evidence
        if isinstance(item, dict) and item.get("id") is not None
    }


def _load_manifest_ids(manifest: Path | None) -> set[str]:
    if not manifest or not manifest.is_file():
        return set()
    return {
        line.strip()
        for line in manifest.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("BMA-")
    }


def _issue(
    issues: list[dict[str, str]], severity: str, code: str, bma_id: str, detail: str
) -> None:
    issues.append({"severity": severity, "code": code, "bma_id": bma_id, "detail": detail})


def audit_escat_readiness(
    *,
    bma_dir: Path = DEFAULT_BMA_DIR,
    biomarker_dir: Path = DEFAULT_BIOMARKER_DIR,
    civic_root: Path = DEFAULT_CIVIC_ROOT,
    manifest: Path | None = DEFAULT_MANIFEST,
    as_of: date | None = None,
    max_snapshot_age_days: int = 45,
) -> dict[str, Any]:
    """Build an audit report without mutating KB content.

    The checks identify missing provenance, stale snapshots and potential
    taxonomy conflicts. A potential conflict is a review signal only; the
    tool never says that a source or an existing tier is clinically wrong.
    """

    as_of = as_of or date.today()
    issues: list[dict[str, str]] = []
    bmas: list[dict[str, Any]] = []
    for path in sorted(bma_dir.rglob("*.yaml")):
        data = load_yaml(path)
        if data and data.get("id"):
            data = dict(data)
            data["__path"] = path.relative_to(REPO_ROOT).as_posix() if path.is_relative_to(REPO_ROOT) else str(path)
            bmas.append(data)

    lookup_by_id = _load_biomarker_lookup(biomarker_dir)
    snapshot_dir, snapshot_date = find_latest_snapshot(civic_root)
    civic_by_id = _load_civic_evidence(snapshot_dir)
    manifest_ids = _load_manifest_ids(manifest)

    snapshot_age_days = (as_of - snapshot_date).days if snapshot_date else None
    if snapshot_age_days is not None and snapshot_age_days > max_snapshot_age_days:
        _issue(
            issues,
            "major",
            "civic_snapshot_stale",
            "CIVIC-SNAPSHOT",
            f"Latest snapshot {snapshot_date.isoformat()} is {snapshot_age_days} days old (limit {max_snapshot_age_days}).",
        )

    for bma in bmas:
        bma_id = str(bma["id"])
        tier = str(bma.get("escat_tier") or "").upper()
        readiness = actionability_release_readiness(bma)
        if not readiness.ready:
            severity = "critical" if tier in STRONG_TIERS else "major"
            _issue(issues, severity, "release_not_ready", bma_id, "; ".join(readiness.reasons))

        if tier == "IV":
            _issue(issues, "major", "legacy_broad_tier_iv", bma_id, "Legacy broad tier IV must be resolved to IVA or IVB during clinical review.")

        evidence_sources = bma.get("evidence_sources") or []
        if not evidence_sources:
            severity = "critical" if tier in STRONG_TIERS else "major"
            _issue(issues, severity, "missing_evidence_sources", bma_id, "BMA has no per-source evidence records.")
        missing_lanes: list[str] = []
        civic_variant_mismatches: list[str] = []
        for source in evidence_sources:
            if not isinstance(source, dict):
                _issue(issues, "major", "invalid_evidence_source", bma_id, "Evidence-source entry is not a mapping.")
                continue
            if not source.get("evidence_lane"):
                missing_lanes.append(str(source.get("source") or "unknown source"))
            if str(source.get("source") or "").upper() != "SRC-CIVIC":
                continue
            for raw_eid in source.get("evidence_ids") or []:
                eid = _normalize_evidence_id(raw_eid)
                item = civic_by_id.get(eid or "")
                if not eid or item is None:
                    _issue(issues, "major", "civic_evidence_id_missing", bma_id, f"CIViC evidence ID {raw_eid!r} is absent from the loaded snapshot.")
                    continue
                qualifier_tokens = _variant_tokens(bma.get("variant_qualifier"))
                civic_tokens = _variant_tokens(item.get("variant"))
                if qualifier_tokens and civic_tokens and not qualifier_tokens.intersection(civic_tokens):
                    civic_variant_mismatches.append(
                        f"EID{eid} ({', '.join(sorted(civic_tokens))})"
                    )

        if missing_lanes:
            source_counts = Counter(missing_lanes)
            summary = ", ".join(
                f"{source} ×{count}" if count > 1 else source
                for source, count in sorted(source_counts.items())
            )
            _issue(
                issues,
                "minor",
                "missing_evidence_lane",
                bma_id,
                f"{len(missing_lanes)} evidence entries lack evidence_lane ({summary}).",
            )
        if civic_variant_mismatches:
            examples = ", ".join(civic_variant_mismatches[:5])
            extra = len(civic_variant_mismatches) - 5
            suffix = f"; +{extra} more" if extra > 0 else ""
            _issue(
                issues,
                "major",
                "civic_variant_mismatch",
                bma_id,
                "Qualifier tokens "
                f"{sorted(_variant_tokens(bma.get('variant_qualifier')))} do not overlap "
                f"{len(civic_variant_mismatches)} CIViC EID variant(s): {examples}{suffix}.",
            )

        lookup = lookup_by_id.get(str(bma.get("biomarker_id") or ""), {})
        lookup_tokens = _variant_tokens(lookup.get("variant"))
        qualifier_tokens = _variant_tokens(bma.get("variant_qualifier"))
        if lookup_tokens and qualifier_tokens and not lookup_tokens.intersection(qualifier_tokens):
            _issue(
                issues,
                "major",
                "biomarker_taxonomy_mismatch",
                bma_id,
                f"BIO lookup tokens {sorted(lookup_tokens)} do not overlap BMA qualifier tokens {sorted(qualifier_tokens)}.",
            )

        if manifest_ids and bma_id not in manifest_ids:
            _issue(issues, "major", "unplanned_bma", bma_id, "BMA is absent from the supplied ESCAT audit manifest.")

    issues.sort(key=lambda x: (SEVERITY_ORDER[x["severity"]], x["code"], x["bma_id"], x["detail"]))
    issue_by_severity = Counter(issue["severity"] for issue in issues)
    issue_by_code = Counter(issue["code"] for issue in issues)
    return {
        "audit_name": "escat_readiness",
        "as_of": as_of.isoformat(),
        "bma_count": len(bmas),
        "latest_civic_snapshot": snapshot_date.isoformat() if snapshot_date else None,
        "snapshot_age_days": snapshot_age_days,
        "max_snapshot_age_days": max_snapshot_age_days,
        "manifest_path": str(manifest) if manifest else None,
        "manifest_count": len(manifest_ids),
        "release_ready_count": sum(actionability_release_readiness(bma).ready for bma in bmas),
        "issues_by_severity": dict(sorted(issue_by_severity.items())),
        "issues_by_code": dict(sorted(issue_by_code.items())),
        "strong_tier_missing_evidence": sum(
            str(bma.get("escat_tier") or "").upper() in STRONG_TIERS and not bma.get("evidence_sources")
            for bma in bmas
        ),
        "unplanned_bma_count": sum(bma["id"] not in manifest_ids for bma in bmas) if manifest_ids else 0,
        "issues": issues,
    }


def render_markdown(report: dict[str, Any], limit_per_severity: int = 20) -> str:
    """Render a compact reviewer-facing queue from an audit report."""

    lines = [
        "# ESCAT readiness audit",
        "",
        f"Generated: `{report['as_of']}`. This is a deterministic data-quality queue, not an automated clinical assessment or tier reassignment.",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| BMA records scanned | {report['bma_count']} |",
        f"| Clinically ready under release gate | {report['release_ready_count']} |",
        f"| Latest CIViC snapshot | {report['latest_civic_snapshot'] or 'none'} |",
        f"| Snapshot age (days) | {report['snapshot_age_days'] if report['snapshot_age_days'] is not None else 'n/a'} |",
        f"| Strong-tier records missing evidence sources | {report['strong_tier_missing_evidence']} |",
        f"| BMAs absent from historical manifest | {report['unplanned_bma_count']} |",
        "",
        "## Issue counts",
        "",
    ]
    for severity in ("critical", "major", "minor"):
        lines.append(f"- {severity}: {report['issues_by_severity'].get(severity, 0)}")
    lines.extend(["", "## Reviewer queue", ""])
    for severity in ("critical", "major", "minor"):
        rows = [issue for issue in report["issues"] if issue["severity"] == severity]
        if not rows:
            continue
        lines.extend([f"### {severity.title()}", ""])
        for issue in rows[:limit_per_severity]:
            lines.append(f"- `{issue['code']}` — `{issue['bma_id']}`: {issue['detail']}")
        if len(rows) > limit_per_severity:
            lines.append(f"- … {len(rows) - limit_per_severity} additional {severity} findings are in the JSON artifact.")
        lines.append("")
    lines.extend([
        "## Required handling",
        "",
        "1. Clinical co-leads classify scope and ESCAT applicability; they do not accept an inferred tier.",
        "2. Reconcile taxonomy/evidence-ID warnings against primary sources and the relevant tumour context.",
        "3. Record a clinician-authored dossier, then collect two independent sign-offs pinned to `last_verified`.",
        "4. Re-run this audit before release; treatment-track selection remains independent of ESCAT.",
        "",
    ])
    return "\n".join(lines)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bma-dir", type=Path, default=DEFAULT_BMA_DIR)
    parser.add_argument("--biomarker-dir", type=Path, default=DEFAULT_BIOMARKER_DIR)
    parser.add_argument("--civic-root", type=Path, default=DEFAULT_CIVIC_ROOT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    parser.add_argument("--max-snapshot-age-days", type=int, default=45)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when critical findings exist.")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    report = audit_escat_readiness(
        bma_dir=args.bma_dir,
        biomarker_dir=args.biomarker_dir,
        civic_root=args.civic_root,
        manifest=args.manifest,
        as_of=args.as_of,
        max_snapshot_age_days=args.max_snapshot_age_days,
    )
    if args.json_output:
        _write(args.json_output, json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    if args.markdown_output:
        _write(args.markdown_output, render_markdown(report))
    print(json.dumps({key: value for key, value in report.items() if key != "issues"}, ensure_ascii=False))
    return 1 if args.strict and report["issues_by_severity"].get("critical") else 0


if __name__ == "__main__":
    raise SystemExit(main())
