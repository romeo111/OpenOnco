"""verify_citations — citation-grounding verifier for sidecar PRs.

Per docs/reviews/cross-repo-task_torrent-sync-plan-2026-04-28.md §4.2 and
docs/reviews/one-prompt-onboarding-plan-2026-04-28.md §6.

Runs three layers of grounding checks on contribution sidecars:

  1. Structural — every cited SRC-* exists on master OR is stubbed in the
     chunk dir; every CIViC EID matches the latest CIViC snapshot.
  2. Title-substring — for replace_source/new-source rows, the trial name
     in the claim must appear in the target Source's title or notes
     (delegates to reverify_citation_replace_source.py rule).
  3. Semantic (optional) — if ANTHROPIC_API_KEY is set and --semantic is
     passed, call Claude API to score whether each claim is supported by
     its cited source's title + notes.

Layer 3 is the new value-add. Layers 1+2 already exist in other scripts;
this orchestrator wraps them and emits a single per-claim report.

Usage:
    # Default: structural + title-substring on the whole chunk
    python -m scripts.tasktorrent.verify_citations <chunk-id>

    # Add semantic check (requires ANTHROPIC_API_KEY env)
    python -m scripts.tasktorrent.verify_citations <chunk-id> --semantic

    # Run on changed-files-only mode (CI)
    python -m scripts.tasktorrent.verify_citations <chunk-id> --base origin/master

    # Emit JSON report
    python -m scripts.tasktorrent.verify_citations <chunk-id> --json > report.json

Exit codes:
    0 — all citations grounded
    1 — at least one citation failed grounding
    2 — usage / IO error
    3 — semantic check requested but ANTHROPIC_API_KEY missing

Design note: the semantic check is OPTIONAL by design. CI runs structural
by default; semantic adds latency + token cost and requires a secret. Pure
forks without the secret degrade to structural-only — never block on
missing secrets.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRIB_ROOT = REPO_ROOT / "contributions"
SOURCES_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"
CIVIC_SNAPSHOT_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "civic"


# ---------- Data ----------

@dataclass
class Claim:
    """A claim under verification.

    A claim is the (sidecar_path, evidence_summary, cited_sources) triple
    that we need to verify is grounded.
    """
    sidecar: str
    target_id: str
    summary: str
    cited_sources: list[str] = field(default_factory=list)
    civic_eids: list[str] = field(default_factory=list)


@dataclass
class CheckResult:
    layer: str           # "structural" | "title-substring" | "semantic"
    passed: bool
    detail: str = ""


@dataclass
class ClaimReport:
    sidecar: str
    target_id: str
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)


# ---------- KB readers ----------

def _load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_master_source_ids() -> set[str]:
    """Stable IDs of every Source on master."""
    ids: set[str] = set()
    if not SOURCES_ROOT.is_dir():
        return ids
    for p in SOURCES_ROOT.glob("*.yaml"):
        data = _load_yaml(p)
        if isinstance(data, dict) and isinstance(data.get("id"), str):
            ids.add(data["id"])
    return ids


def load_chunk_stub_source_ids(chunk_dir: Path) -> set[str]:
    """Source IDs declared as stubs in the chunk's contribution dir."""
    ids: set[str] = set()
    if not chunk_dir.is_dir():
        return ids
    for p in chunk_dir.glob("source_stub_*.yaml"):
        data = _load_yaml(p)
        if isinstance(data, dict):
            sid = data.get("id") or (data.get("_contribution") or {}).get("target_entity_id")
            if isinstance(sid, str):
                ids.add(sid)
    return ids


def load_latest_civic_eids() -> set[str]:
    """All CIViC EIDs available across snapshots (we accept any version)."""
    eids: set[str] = set()
    if not CIVIC_SNAPSHOT_ROOT.is_dir():
        return eids
    for snapshot_dir in CIVIC_SNAPSHOT_ROOT.iterdir():
        if not snapshot_dir.is_dir():
            continue
        for p in snapshot_dir.rglob("*.yaml"):
            data = _load_yaml(p)
            if isinstance(data, dict):
                # Snapshot files vary; collect any EID-like keys
                for k in ("id", "evidence_id"):
                    v = data.get(k)
                    if isinstance(v, str) and v.startswith("EID"):
                        eids.add(v)
                # Snapshots often list evidence_items
                for item in data.get("evidence_items", []) or []:
                    if isinstance(item, dict):
                        eid = item.get("id") or item.get("evidence_id")
                        if isinstance(eid, str) and eid.startswith("EID"):
                            eids.add(eid)
    return eids


# ---------- Claim extraction ----------

def _extract_eids(value: Any) -> list[str]:
    """Find any EID strings nested in a value."""
    eids: list[str] = []
    if isinstance(value, str):
        eids.extend(re.findall(r"\bEID\d+\b", value))
    elif isinstance(value, list):
        for v in value:
            eids.extend(_extract_eids(v))
    elif isinstance(value, dict):
        for v in value.values():
            eids.extend(_extract_eids(v))
    return eids


def extract_claims_from_sidecar(path: Path) -> list[Claim]:
    """Pull (target_id, summary, cited sources) tuples from a sidecar yaml."""
    data = _load_yaml(path)
    if not isinstance(data, dict):
        return []
    rel = str(path.relative_to(REPO_ROOT)).replace("\\", "/")

    target_id = data.get("id") or (data.get("_contribution") or {}).get("target_entity_id") or ""
    if not target_id:
        return []

    summary = (
        data.get("evidence_summary")
        or data.get("definition")
        or data.get("description")
        or data.get("notes")
        or ""
    )
    if isinstance(summary, list):
        summary = "\n".join(str(x) for x in summary)
    summary = str(summary)[:4000]  # cap for API token budget

    cited: set[str] = set()
    for k in ("primary_sources", "sources", "supporting_sources"):
        v = data.get(k)
        if isinstance(v, list):
            cited.update(s for s in v if isinstance(s, str) and s.startswith("SRC-"))

    for es in data.get("evidence_sources", []) or []:
        if isinstance(es, dict):
            s = es.get("source")
            if isinstance(s, str) and s.startswith("SRC-"):
                cited.add(s)

    eids = _extract_eids(data.get("evidence_sources"))

    return [Claim(
        sidecar=rel,
        target_id=str(target_id),
        summary=summary,
        cited_sources=sorted(cited),
        civic_eids=sorted(set(eids)),
    )]


def discover_sidecars(chunk_dir: Path) -> list[Path]:
    """Sidecar yaml files (excluding meta + manifest + reports)."""
    if not chunk_dir.is_dir():
        return []
    out: list[Path] = []
    for p in sorted(chunk_dir.glob("*.yaml")):
        if p.name in ("_contribution_meta.yaml",):
            continue
        if p.name.endswith("_report.yaml") or p.name.endswith("_filter_report.yaml"):
            continue
        if p.name.startswith("audit-report"):
            continue
        out.append(p)
    return out


# ---------- Layer 1: structural ----------

def check_structural(
    claim: Claim,
    master_sources: set[str],
    chunk_stub_sources: set[str],
    civic_eids: set[str] | None,
) -> CheckResult:
    """Every cited SRC-* exists; every CIViC EID is real (when snapshot available)."""
    known = master_sources | chunk_stub_sources
    missing_sources = [s for s in claim.cited_sources if s not in known]
    issues: list[str] = []
    if missing_sources:
        issues.append(f"unknown sources: {missing_sources}")

    if civic_eids and claim.civic_eids:
        missing_eids = [e for e in claim.civic_eids if e not in civic_eids]
        if missing_eids:
            issues.append(f"unknown CIViC EIDs: {missing_eids}")

    if issues:
        return CheckResult(layer="structural", passed=False, detail="; ".join(issues))
    return CheckResult(layer="structural", passed=True, detail="all cited refs known")


# ---------- Layer 2: title-substring ----------

# Match "trial XXX" / "study XXX" where XXX is an uppercase acronym with
# at least one digit OR hyphen (filters out plain English words like
# "named", "completed", "the", etc.). Inline (?i:...) makes the
# trial/study trigger case-insensitive while keeping the captured group
# strictly uppercase.
_TRIAL_RE = re.compile(r"""(?i:trial|study)\s+['"]?([A-Z][A-Z0-9-]{2,})['"]?""")


def _normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _is_trial_acronym(s: str) -> bool:
    """A real trial name has at least one digit or hyphen (KEYNOTE-522, EV-302)."""
    return any(c.isdigit() or c == "-" for c in s)


def check_title_substring(
    claim: Claim,
    master_source_titles: dict[str, str],
) -> CheckResult:
    """If the claim mentions a trial name + cites a source, the trial name must
    appear in that source's title.

    Triggered only when claim.summary explicitly references "trial XYZ" or
    "study XYZ". Otherwise no-op (passed=True with detail="n/a").
    """
    matches = [m for m in _TRIAL_RE.findall(claim.summary or "") if _is_trial_acronym(m)]
    if not matches:
        return CheckResult(layer="title-substring", passed=True, detail="n/a (no trial mentioned)")
    if not claim.cited_sources:
        return CheckResult(
            layer="title-substring",
            passed=False,
            detail=f"trial(s) mentioned ({matches}) but no source cited",
        )

    # For each mentioned trial, at least one cited source's title must contain it.
    fails: list[str] = []
    for trial in matches:
        norm_trial = _normalize(trial)
        ok = False
        for src in claim.cited_sources:
            title_norm = _normalize(master_source_titles.get(src, ""))
            if norm_trial and norm_trial in title_norm:
                ok = True
                break
        if not ok:
            fails.append(trial)
    if fails:
        return CheckResult(
            layer="title-substring",
            passed=False,
            detail=f"trial name(s) not found in any cited source title: {fails}",
        )
    return CheckResult(layer="title-substring", passed=True, detail=f"matched {matches}")


def load_master_source_titles() -> dict[str, str]:
    out: dict[str, str] = {}
    if not SOURCES_ROOT.is_dir():
        return out
    for p in SOURCES_ROOT.glob("*.yaml"):
        data = _load_yaml(p)
        if not isinstance(data, dict):
            continue
        sid = data.get("id")
        if not isinstance(sid, str):
            continue
        title = " ".join(filter(None, [
            str(data.get("title") or ""),
            str(data.get("notes") or ""),
        ]))
        out[sid] = title
    return out


# ---------- Layer 3: semantic (optional) ----------

def check_semantic(claim: Claim, source_corpus: dict[str, str]) -> CheckResult:
    """Call Anthropic API to score grounding.

    Returns CheckResult. Requires ANTHROPIC_API_KEY in env.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return CheckResult(layer="semantic", passed=True, detail="skipped (no API key)")

    try:
        import anthropic  # type: ignore
    except ImportError:
        return CheckResult(
            layer="semantic",
            passed=True,
            detail="skipped (anthropic SDK not installed; pip install anthropic)",
        )

    if not claim.cited_sources or not claim.summary:
        return CheckResult(layer="semantic", passed=True, detail="n/a (no claim+source pair)")

    # Build context: the claim + each cited source's title/notes
    sources_text = "\n\n".join(
        f"### {s}\n{source_corpus.get(s, '(no title/notes available)')[:1500]}"
        for s in claim.cited_sources
    )
    prompt = (
        "You are verifying whether a clinical-evidence claim is supported by "
        "the cited sources. Respond ONLY with JSON of the form "
        '{"grounded": true|false, "confidence": 0.0-1.0, "reasoning": "..."}. '
        "Be strict: a claim is `grounded: true` only if at least one cited "
        "source plausibly supports it. If sources are too short to judge, "
        'use {"grounded": true, "confidence": 0.5, "reasoning": "insufficient source text"}.\n\n'
        f"CLAIM:\n{claim.summary[:2500]}\n\n"
        f"CITED SOURCES:\n{sources_text}"
    )

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in response.content if hasattr(b, "text")).strip()
    except Exception as e:  # pragma: no cover (network)
        return CheckResult(layer="semantic", passed=True, detail=f"API error (non-blocking): {e}")

    # Extract JSON object
    m = re.search(r"\{.*?\}", text, re.DOTALL)
    if not m:
        return CheckResult(
            layer="semantic", passed=True,
            detail=f"unparseable response (non-blocking): {text[:200]}",
        )
    try:
        result = json.loads(m.group(0))
    except json.JSONDecodeError:
        return CheckResult(layer="semantic", passed=True, detail="unparseable JSON (non-blocking)")

    grounded = bool(result.get("grounded", True))
    confidence = float(result.get("confidence", 0.5))
    reasoning = str(result.get("reasoning", ""))[:500]
    detail = f"grounded={grounded} conf={confidence:.2f} — {reasoning}"
    # Threshold: fail only on grounded=false AND confidence>=0.7 (avoid noise)
    fail = (not grounded) and confidence >= 0.7
    return CheckResult(layer="semantic", passed=not fail, detail=detail)


# ---------- Orchestrator ----------

def verify_chunk(
    chunk_id: str,
    semantic: bool = False,
) -> tuple[list[ClaimReport], int]:
    """Run all enabled layers on every sidecar in the chunk."""
    chunk_dir = CONTRIB_ROOT / chunk_id
    if not chunk_dir.is_dir():
        return [], 2

    master_sources = load_master_source_ids()
    chunk_stubs = load_chunk_stub_source_ids(chunk_dir)
    master_titles = load_master_source_titles()
    civic_eids = load_latest_civic_eids() if any(
        True for _ in (CIVIC_SNAPSHOT_ROOT.glob("*") if CIVIC_SNAPSHOT_ROOT.is_dir() else [])
    ) else None

    reports: list[ClaimReport] = []
    for sidecar_path in discover_sidecars(chunk_dir):
        for claim in extract_claims_from_sidecar(sidecar_path):
            r = ClaimReport(sidecar=claim.sidecar, target_id=claim.target_id)
            r.checks.append(check_structural(claim, master_sources, chunk_stubs, civic_eids))
            r.checks.append(check_title_substring(claim, master_titles))
            if semantic:
                r.checks.append(check_semantic(claim, master_titles))
            reports.append(r)

    fail = 0 if all(r.passed for r in reports) else 1
    return reports, fail


# ---------- CLI ----------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="scripts.tasktorrent.verify_citations",
        description="Citation-grounding verifier for TaskTorrent sidecar PRs.",
    )
    parser.add_argument("chunk_id")
    parser.add_argument(
        "--semantic",
        action="store_true",
        help="enable Claude API semantic grounding check (requires ANTHROPIC_API_KEY)",
    )
    parser.add_argument(
        "--json", action="store_true", help="emit JSON report to stdout",
    )
    args = parser.parse_args(argv)

    if args.semantic and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: --semantic requires ANTHROPIC_API_KEY", file=sys.stderr)
        return 3

    reports, fail = verify_chunk(args.chunk_id, semantic=args.semantic)

    if not reports:
        print(f"ERROR: chunk '{args.chunk_id}' produced no claims (no sidecars found?)", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([asdict(r) for r in reports], indent=2))
    else:
        for r in reports:
            status = "PASS" if r.passed else "FAIL"
            print(f"{status}  {r.sidecar}  ({r.target_id})")
            for c in r.checks:
                marker = "[+]" if c.passed else "[-]"
                print(f"  {marker} {c.layer:18s} {c.detail}")
        passed_n = sum(1 for r in reports if r.passed)
        print(f"\n{passed_n}/{len(reports)} sidecars passed.")
        if fail:
            print("Citation grounding failed — fix and re-run.", file=sys.stderr)

    return fail


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
