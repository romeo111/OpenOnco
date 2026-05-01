"""check_ready — categorize open TaskTorrent chunks by prerequisite status.

For Tier-2 dispatch + future waves, chunks are organized into workstreams
that have inter-dependencies (e.g. W9 regimens reference DRUG-X IDs from
W8 drugs; W10 indications reference biomarker_id + recommended_regimen
from W7+W8+W9). A chunk is "ready" when all its prerequisite chunks have
landed (closed via merged PR).

Usage:
    py -3.12 -m scripts.tasktorrent.check_ready
    py -3.12 -m scripts.tasktorrent.check_ready --json     # machine-readable
    py -3.12 -m scripts.tasktorrent.check_ready --ready    # just print ready chunk IDs

Output groups: ready | blocked-on-W7 | blocked-on-W8 | blocked-on-W9 |
                blocked-multiple | meta | unknown.

Exit code 0 always (this is a status report, not a gate). Use --strict
to exit 1 when no chunks are ready (signals "nothing left to dispatch").
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional


# ── Workstream → prerequisite map ─────────────────────────────────────────
#
# Keys are workstream IDs (W7/W8/W9/W10/W11/W12a/W12b/W13/tracker).
# Values are the SET of workstream IDs that must be fully closed before
# this workstream can start. Empty set = no prerequisites (ready immediately).
#
# Source of truth: docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md
# > "Sequencing summary" + per-workstream "after relevant Wn merges" notes.

PREREQS: dict[str, set[str]] = {
    "tracker": set(),  # meta — not really "work", but track for completeness
    "W7": set(),       # bio authoring — independent
    "W8": set(),       # drug authoring — independent
    "W9": {"W8"},      # regimens reference DRUG-X
    "W10": {"W7", "W8", "W9"},  # indications reference bio + reg
    "W11": {"W7"},     # RFs reference biomarkers
    "W12a": set(),     # CIViC backfill — independent (per-BMA work)
    "W12b": set(),     # source recency — independent (per-source work)
    "W13": set(),      # deferred stubs — not auto-dispatched anyway
}


# Map chunk-id PREFIX → workstream id. Order matters: longer prefixes first
# so e.g. "tier2-bio-followup" doesn't accidentally match "tier2-bio".
PREFIX_TO_WORKSTREAM: list[tuple[str, str]] = [
    ("[Tracker]", "tracker"),
    ("bma-civic-backfill-wave2", "W12a"),
    ("source-recency-refresh-wave2", "W12b"),
    ("tier2-bio-", "W7"),
    ("tier2-drug-", "W8"),
    ("tier2-reg-", "W9"),
    ("tier2-ind-", "W10"),
    ("tier2-rf-", "W11"),
    ("tier3-", "W13"),
]


@dataclass
class Chunk:
    number: int
    title: str
    chunk_id: str
    workstream: str
    state: str  # "open" | "closed"
    blocked_by: set[str] = field(default_factory=set)

    @property
    def status(self) -> str:
        if self.state == "closed":
            return "closed"
        if self.workstream == "tracker":
            return "meta"
        if self.workstream == "W13":
            return "deferred"
        if self.blocked_by:
            return f"blocked-on-{'+'.join(sorted(self.blocked_by))}"
        return "ready"


def _classify_workstream(title: str) -> str:
    for prefix, ws in PREFIX_TO_WORKSTREAM:
        if prefix in title or title.startswith(f"[Chunk] {prefix}"):
            return ws
    return "unknown"


def _extract_chunk_id(title: str) -> str:
    """`[Chunk] tier2-bio-heme-2026-05-01-001` → `tier2-bio-heme-2026-05-01-001`."""
    m = re.match(r"^\[(?:Chunk|Tracker)\]\s*(.+?)\s*$", title)
    return (m.group(1) if m else title).strip()


def _gh_issue_list(extra_args: list[str] | None = None) -> list[dict]:
    """Run gh CLI and return list of issues. Raises on gh failure."""
    cmd = [
        "gh", "issue", "list",
        "--label", "chunk-task",
        "--state", "all",
        "--limit", "500",
        "--json", "number,title,state,labels",
    ]
    if extra_args:
        cmd.extend(extra_args)
    out = subprocess.run(
        cmd, check=True, capture_output=True, text=True, encoding="utf-8"
    )
    return json.loads(out.stdout)


def collect_chunks() -> list[Chunk]:
    raw = _gh_issue_list()
    chunks: list[Chunk] = []
    for r in raw:
        title = r.get("title") or ""
        ws = _classify_workstream(title)
        chunks.append(Chunk(
            number=int(r["number"]),
            title=title,
            chunk_id=_extract_chunk_id(title),
            workstream=ws,
            state=str(r.get("state", "")).lower(),
        ))
    return chunks


def compute_blocked_by(chunks: list[Chunk]) -> None:
    """For each open chunk, fill .blocked_by with the workstream IDs whose
    chunks are not all closed yet."""
    closed_by_ws: dict[str, list[Chunk]] = defaultdict(list)
    open_by_ws: dict[str, list[Chunk]] = defaultdict(list)
    for c in chunks:
        (closed_by_ws if c.state == "closed" else open_by_ws)[c.workstream].append(c)

    for c in chunks:
        if c.state != "open":
            continue
        prereqs = PREREQS.get(c.workstream, set())
        for prereq_ws in prereqs:
            # Prereq satisfied iff at least one chunk exists for prereq_ws
            # AND no open chunks remain in that workstream.
            existing = closed_by_ws.get(prereq_ws, []) + open_by_ws.get(prereq_ws, [])
            if not existing:
                # No prereq chunks exist at all — treat as satisfied (e.g.,
                # prereq was deferred / never dispatched). Conservative
                # alternative: treat as blocked. We pick "satisfied" so
                # workstreams without prereq dispatches don't deadlock.
                continue
            if open_by_ws.get(prereq_ws):
                c.blocked_by.add(prereq_ws)


def render_text(chunks: list[Chunk]) -> str:
    by_status: dict[str, list[Chunk]] = defaultdict(list)
    for c in chunks:
        by_status[c.status].append(c)

    lines: list[str] = []
    lines.append("OpenOnco TaskTorrent — chunk readiness report")
    lines.append("")
    open_ct = sum(1 for c in chunks if c.state == "open")
    closed_ct = sum(1 for c in chunks if c.state == "closed")
    ready_ct = len(by_status.get("ready", []))
    lines.append(f"Total chunks queried: {len(chunks)} (open={open_ct}, closed={closed_ct})")
    lines.append(f"Ready to pick up RIGHT NOW: {ready_ct}")
    lines.append("")

    order = ["ready", "meta", "deferred", "closed"]
    blocked_keys = sorted(k for k in by_status if k.startswith("blocked-on-"))
    order.extend(blocked_keys)
    other = [k for k in by_status if k not in order]
    order.extend(sorted(other))

    for status in order:
        bucket = by_status.get(status)
        if not bucket:
            continue
        lines.append(f"## {status} ({len(bucket)})")
        # Group by workstream within bucket
        by_ws: dict[str, list[Chunk]] = defaultdict(list)
        for c in bucket:
            by_ws[c.workstream].append(c)
        for ws in sorted(by_ws):
            cs = sorted(by_ws[ws], key=lambda c: c.number)
            issue_range = f"#{cs[0].number}-#{cs[-1].number}" if len(cs) > 1 else f"#{cs[0].number}"
            lines.append(f"  {ws:<8} {issue_range:<14} ({len(cs)} chunks)")
        lines.append("")

    return "\n".join(lines)


def render_json(chunks: list[Chunk]) -> str:
    payload = {
        "total": len(chunks),
        "open": sum(1 for c in chunks if c.state == "open"),
        "closed": sum(1 for c in chunks if c.state == "closed"),
        "ready_count": sum(1 for c in chunks if c.status == "ready"),
        "by_status": defaultdict(list),
    }
    for c in chunks:
        payload["by_status"][c.status].append({
            "number": c.number,
            "chunk_id": c.chunk_id,
            "workstream": c.workstream,
            "state": c.state,
            "blocked_by": sorted(c.blocked_by) if c.blocked_by else [],
        })
    payload["by_status"] = dict(payload["by_status"])
    return json.dumps(payload, indent=2, ensure_ascii=False)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--json", action="store_true",
                    help="Emit machine-readable JSON instead of text table.")
    ap.add_argument("--ready", action="store_true",
                    help="Print only ready chunk IDs (one per line). Useful for "
                         "piping into a contributor-onboarding workflow.")
    ap.add_argument("--strict", action="store_true",
                    help="Exit 1 if zero chunks are ready. Default: exit 0 always.")
    args = ap.parse_args()

    try:
        chunks = collect_chunks()
    except subprocess.CalledProcessError as e:
        print(f"gh CLI failed: {e.stderr}", file=sys.stderr)
        return 2
    except FileNotFoundError:
        print("gh CLI not found in PATH. Install from https://cli.github.com/", file=sys.stderr)
        return 2

    compute_blocked_by(chunks)

    if args.ready:
        for c in sorted(chunks, key=lambda c: c.number):
            if c.status == "ready":
                print(f"#{c.number}\t{c.chunk_id}")
    elif args.json:
        print(render_json(chunks))
    else:
        print(render_text(chunks))

    if args.strict:
        ready = sum(1 for c in chunks if c.status == "ready")
        return 0 if ready > 0 else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
