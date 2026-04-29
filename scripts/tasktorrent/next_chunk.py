"""next_chunk — find the next claimable TaskTorrent chunk and emit JSON.

Discovery contract (per docs/reviews/one-prompt-onboarding-plan-2026-04-28.md §4):

    GET /repos/<owner>/<repo>/issues
        ?labels=chunk-task,status-active
        &assignee=none
        &state=open

The oldest unassigned issue wins (FIFO; oldest-first encourages stale-claim
release before new claims pile on).

Issue body parsing handles the structured headings emitted by
.github/ISSUE_TEMPLATE/tasktorrent-chunk-task.md:

    ## Chunk Spec               → first https://… URL
    ## Chunk ID                 → first inline `code` token
    ## Branch Naming Convention → first inline `code` token
    ## Sidecar Output Path      → first fenced codeblock body (one line)
    ## Claim Method             → first inline `code` token; must be one of
                                  formal-issue / trusted-agent-wip-branch-first
    ## Drop Estimate            → text + numeric extraction (Drops/tokens)
    ## Required Skill           → first inline `code` token
    ## Task Manifest            → first fenced codeblock or bullet list
    ## Topic Labels             → list of inline `code` tokens
    ## Acceptance Criteria (machine-checkable) → checklist count

Output (JSON to stdout):

    {
      "issue_number": 26,
      "issue_url": "https://github.com/owner/repo/issues/26",
      "chunk_id": "trial-source-ingest-pubmed",
      "spec_url": "https://github.com/.../chunks/openonco/<id>.md",
      "branch": "tasktorrent/trial-source-ingest-pubmed",
      "sidecar_dir": "contributions/trial-source-ingest-pubmed/",
      "claim_method": "formal-issue",
      "drop_estimate": "~3 Drops (~300k tokens)",
      "drop_estimate_tokens": 300000,
      "required_skill": "citation-verification",
      "topic_labels": ["source-ingest", "metadata-classification"],
      "manifest_preview": ["CROSS", "PARADIGM", ...],
      "acceptance_criteria_machine_count": 12,
      "agent_prompt_url_guess": "https://github.com/owner/repo/blob/master/docs/contributing/AGENT_PROMPT_<id>.md"
    }

Exit codes:
    0 — success, JSON emitted
    1 — parse error or issue lookup failed
    2 — no claimable chunks (`{"status": "no_chunks_available"}` to stdout)
    3 — gh CLI unavailable

Usage:
    python -m scripts.tasktorrent.next_chunk
    python -m scripts.tasktorrent.next_chunk --repo owner/repo
    python -m scripts.tasktorrent.next_chunk --json-only      # silent on stderr
    python -m scripts.tasktorrent.next_chunk --offline FILE   # parse a saved JSON dump (testing)
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_REPO = "romeo111/OpenOnco"
VALID_CLAIM_METHODS = {"formal-issue", "trusted-agent-wip-branch-first"}

SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
URL_RE = re.compile(r"https?://\S+")
FENCE_RE = re.compile(r"```[a-zA-Z]*\s*\n(.*?)\n```", re.DOTALL)
DROPS_NUM_RE = re.compile(r"~?(\d+)\s*Drops?", re.IGNORECASE)
TOKENS_NUM_RE = re.compile(r"~?(\d+)\s*[kK]\s*tokens", re.IGNORECASE)


@dataclass
class ChunkInfo:
    issue_number: int
    issue_url: str
    chunk_id: str | None = None
    spec_url: str | None = None
    branch: str | None = None
    sidecar_dir: str | None = None
    claim_method: str | None = None
    drop_estimate: str | None = None
    drop_estimate_tokens: int | None = None
    required_skill: str | None = None
    topic_labels: list[str] = field(default_factory=list)
    manifest_preview: list[str] = field(default_factory=list)
    acceptance_criteria_machine_count: int = 0
    agent_prompt_url_guess: str | None = None
    parse_warnings: list[str] = field(default_factory=list)


# ---------- Section parsing ----------

def parse_sections(body: str) -> dict[str, str]:
    """Split issue body into {heading: body} keyed by `## ` headings."""
    sections: dict[str, str] = {}
    matches = list(SECTION_RE.finditer(body))
    for i, m in enumerate(matches):
        heading = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sections[heading] = body[start:end].strip()
    return sections


def first_inline_code(text: str) -> str | None:
    m = INLINE_CODE_RE.search(text)
    return m.group(1).strip() if m else None


def first_url(text: str) -> str | None:
    m = URL_RE.search(text)
    if not m:
        return None
    url = m.group(0)
    # strip trailing punctuation that's not part of a real URL
    return url.rstrip(".,;)]")


def first_fenced_block(text: str) -> str | None:
    m = FENCE_RE.search(text)
    return m.group(1).strip() if m else None


def all_inline_codes(text: str) -> list[str]:
    return [c.strip() for c in INLINE_CODE_RE.findall(text)]


def parse_drop_estimate(text: str) -> tuple[str, int | None]:
    """Return (raw_text_first_line, numeric_token_estimate_or_None).

    Token estimate priority: explicit tokens > drops × 100k.
    """
    first_line = text.split("\n", 1)[0].strip() if text else ""
    tokens: int | None = None
    tm = TOKENS_NUM_RE.search(text)
    if tm:
        tokens = int(tm.group(1)) * 1000
    else:
        dm = DROPS_NUM_RE.search(text)
        if dm:
            tokens = int(dm.group(1)) * 100000
    return first_line, tokens


def parse_manifest(text: str) -> list[str]:
    """Extract manifest entries; prefer fenced block, fall back to bullet list."""
    block = first_fenced_block(text)
    if block:
        items = re.split(r"[,\n]", block)
        return [i.strip() for i in items if i.strip() and not i.strip().startswith("#")]
    bullets = re.findall(r"^\s*[-*]\s+(.+?)\s*$", text, re.MULTILINE)
    return [b.strip("`") for b in bullets if b]


def count_machine_acceptance(text: str) -> int:
    return len(re.findall(r"^\s*-\s*\[\s?\]\s+", text, re.MULTILINE))


# ---------- Issue body → ChunkInfo ----------

def parse_issue(issue: dict) -> ChunkInfo:
    info = ChunkInfo(
        issue_number=issue["number"],
        issue_url=issue.get("url", issue.get("html_url", "")),
    )
    body = issue.get("body") or ""
    sections = parse_sections(body)

    if "Chunk Spec" in sections:
        info.spec_url = first_url(sections["Chunk Spec"])
    if "Chunk ID" in sections:
        info.chunk_id = first_inline_code(sections["Chunk ID"])
    if "Branch Naming Convention" in sections:
        info.branch = first_inline_code(sections["Branch Naming Convention"])
    elif "Branch Naming" in sections:
        info.branch = first_inline_code(sections["Branch Naming"])
    if "Sidecar Output Path" in sections:
        block = first_fenced_block(sections["Sidecar Output Path"])
        info.sidecar_dir = block.strip() if block else None

    if "Claim Method" in sections:
        cm = first_inline_code(sections["Claim Method"])
        if cm and cm in VALID_CLAIM_METHODS:
            info.claim_method = cm
        else:
            info.parse_warnings.append(
                f"Claim Method `{cm}` not in {sorted(VALID_CLAIM_METHODS)}"
            )

    if "Drop Estimate" in sections:
        info.drop_estimate, info.drop_estimate_tokens = parse_drop_estimate(
            sections["Drop Estimate"]
        )

    if "Required Skill" in sections:
        info.required_skill = first_inline_code(sections["Required Skill"])
    if "Topic Labels" in sections:
        info.topic_labels = all_inline_codes(sections["Topic Labels"])
    if "Task Manifest" in sections:
        info.manifest_preview = parse_manifest(sections["Task Manifest"])[:20]

    machine_section = sections.get("Acceptance Criteria (machine-checkable)") or ""
    info.acceptance_criteria_machine_count = count_machine_acceptance(machine_section)

    # Required-section sanity
    for req in ("Chunk Spec", "Chunk ID", "Claim Method"):
        if req not in sections:
            info.parse_warnings.append(f"missing required section: {req}")

    if info.chunk_id and info.issue_url:
        m = re.match(r"https?://[^/]+/([^/]+)/([^/]+)/", info.issue_url)
        if m:
            owner, repo = m.group(1), m.group(2)
            info.agent_prompt_url_guess = (
                f"https://github.com/{owner}/{repo}/blob/master/"
                f"docs/contributing/AGENT_PROMPT_{info.chunk_id}.md"
            )
    return info


# ---------- gh CLI integration ----------

def gh_available() -> bool:
    return shutil.which("gh") is not None


def fetch_open_chunks(repo: str) -> list[dict]:
    """Query GitHub for open status-active chunk-task issues with no assignee."""
    cmd = [
        "gh", "issue", "list",
        "--repo", repo,
        "--label", "chunk-task,status-active",
        "--state", "open",
        "--limit", "50",
        "--json", "number,title,body,assignees,labels,createdAt,url",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if res.returncode != 0:
        raise RuntimeError(f"gh issue list failed: {res.stderr.strip()}")
    issues = json.loads(res.stdout or "[]")
    # Filter to unassigned only — gh doesn't have a `--no-assignee` flag
    unassigned = [i for i in issues if not i.get("assignees")]
    # Oldest first (FIFO); avoid `-r` to keep the script simple
    unassigned.sort(key=lambda i: i.get("createdAt", ""))
    return unassigned


# ---------- CLI ----------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="scripts.tasktorrent.next_chunk",
        description="Find the next claimable TaskTorrent chunk and emit JSON.",
    )
    parser.add_argument("--repo", default=DEFAULT_REPO, help=f"GitHub repo (default: {DEFAULT_REPO})")
    parser.add_argument("--json-only", action="store_true", help="suppress stderr human-readable output")
    parser.add_argument(
        "--offline",
        type=Path,
        default=None,
        help="path to a JSON file containing a list of issue dicts (for testing)",
    )
    args = parser.parse_args(argv)

    if args.offline:
        try:
            issues = json.loads(args.offline.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"ERROR: cannot read offline file: {e}", file=sys.stderr)
            return 1
        if not isinstance(issues, list):
            print("ERROR: offline file must contain a list of issue dicts", file=sys.stderr)
            return 1
        unassigned = [i for i in issues if not i.get("assignees")]
        unassigned.sort(key=lambda i: i.get("createdAt", ""))
    else:
        if not gh_available():
            print("ERROR: gh CLI not on PATH; install from https://cli.github.com/", file=sys.stderr)
            return 3
        try:
            unassigned = fetch_open_chunks(args.repo)
        except (RuntimeError, subprocess.TimeoutExpired) as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1

    if not unassigned:
        print(json.dumps({"status": "no_chunks_available"}))
        return 2

    pick = unassigned[0]
    info = parse_issue(pick)

    out = asdict(info)
    out["status"] = "ok"
    print(json.dumps(out, indent=2))

    if not args.json_only:
        rest = len(unassigned) - 1
        if rest > 0:
            print(f"\n{rest} more claimable chunk(s) in queue.", file=sys.stderr)
        if info.parse_warnings:
            print(f"WARNINGS: {info.parse_warnings}", file=sys.stderr)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
