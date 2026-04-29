"""Wave 7 batch worker — source-recency-refresh chunks 92-121 (30 chunks × 5 sources each = 150 sources).

For each chunk:
  - Read its manifest from the GitHub issue body (cached to /tmp/recency_manifests.json)
  - For each SRC-* in the manifest:
      * Real HTTP HEAD via stdlib urllib
      * On 2xx/3xx: produce upsert sidecar bumping current_as_of + adding
        last_recency_check + recency_check_status_code
      * On non-2xx: produce flag-only entry in unreachable.yaml for the chunk
  - Each chunk gets its own contributions/<chunk-id>/ dir with:
      _contribution_meta.yaml, task_manifest.txt, src_*.yaml upserts,
      unreachable.yaml (if any), refresh_summary.yaml

This is bundled as a single PR per maintainer pragmatic decision (30
chunks would otherwise be 30 individual PRs). Each chunk's directory
is independently reviewable / mergeable.
"""

from __future__ import annotations

import datetime as dt
import json
import socket
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"
CONTRIB_ROOT = REPO_ROOT / "contributions"
TODAY = dt.date(2026, 4, 29)
TIMEOUT_SEC = 8

MANIFESTS_FILE = "/tmp/recency_manifests.json"


def _date_from_value(v):
    if isinstance(v, dt.date):
        return v
    if isinstance(v, str):
        try:
            return dt.date.fromisoformat(v[:10])
        except ValueError:
            return None
    return None


def http_head(url: str) -> tuple[int | None, str]:
    socket.setdefaulttimeout(TIMEOUT_SEC)
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "TaskTorrent-RecencyCheck/0.4 (+https://romeo111.github.io/task_torrent/)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
            return resp.getcode() or 0, ""
    except urllib.error.HTTPError as e:
        if e.code == 405:
            return _http_get(url)
        return e.code, str(e.reason)[:100]
    except (urllib.error.URLError, socket.timeout, OSError) as e:
        return None, str(e)[:100]


def _http_get(url: str) -> tuple[int | None, str]:
    socket.setdefaulttimeout(TIMEOUT_SEC)
    req = urllib.request.Request(
        url, headers={"User-Agent": "TaskTorrent-RecencyCheck/0.4"},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
            return resp.getcode() or 0, "via GET"
    except urllib.error.HTTPError as e:
        return e.code, f"via GET: {e.reason}"[:100]
    except (urllib.error.URLError, socket.timeout, OSError) as e:
        return None, f"via GET: {e}"[:100]


def _src_yaml_path(src_id: str) -> Path | None:
    """Map SRC-FOO-BAR → file path."""
    # Try direct slug
    candidate = src_id.replace("SRC-", "").lower().replace("-", "_")
    direct = SOURCES_DIR / f"src_{candidate}.yaml"
    if direct.is_file():
        return direct
    # Otherwise scan files for the id field
    for p in SOURCES_DIR.glob("*.yaml"):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict) and data.get("id") == src_id:
            return p
    return None


def process_chunk(chunk_id: str, source_ids: list[str], issue_number: int) -> dict:
    out_dir = CONTRIB_ROOT / chunk_id
    out_dir.mkdir(parents=True, exist_ok=True)

    upserts: list[dict] = []
    unreachable: list[dict] = []
    not_found: list[str] = []
    status_dist: Counter[str] = Counter()

    for sid in source_ids:
        src_path = _src_yaml_path(sid)
        if src_path is None:
            not_found.append(sid)
            status_dist["src_not_found"] += 1
            continue
        try:
            data = yaml.safe_load(src_path.read_text(encoding="utf-8"))
        except Exception:
            not_found.append(sid)
            status_dist["src_parse_fail"] += 1
            continue
        if not isinstance(data, dict):
            not_found.append(sid)
            continue
        url = data.get("url")
        if not url:
            unreachable.append({"id": sid, "url": None, "status_code": None,
                                "error": "no url field in source yaml"})
            status_dist["no_url"] += 1
            continue

        status, err = http_head(url)
        bucket = (
            "ok" if status and 200 <= status < 400 else
            f"http_{status}" if status else "network_error"
        )
        status_dist[bucket] += 1

        if status and 200 <= status < 400:
            upsert = dict(data)
            upsert["current_as_of"] = TODAY.isoformat()
            upsert["last_recency_check"] = TODAY.isoformat()
            upsert["recency_check_status_code"] = status
            upsert["_contribution"] = {
                "chunk_id": chunk_id,
                "contributor": "claude-anthropic-internal",
                "submission_date": "2026-04-29",
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "target_action": "upsert",
                "target_entity_id": sid,
                "notes_for_reviewer": (
                    f"Recency refresh: HTTP {status} on HEAD. URL reachable. "
                    f"current_as_of bumped from {data.get('current_as_of', '(unset)')} "
                    f"to {TODAY.isoformat()}. No content fields modified."
                ),
            }
            (out_dir / src_path.name).write_text(
                yaml.safe_dump(upsert, sort_keys=False, allow_unicode=True, default_flow_style=False),
                encoding="utf-8",
            )
            upserts.append({"id": sid, "url": url, "status": status})
        else:
            unreachable.append({
                "id": sid, "url": url, "status_code": status, "error": err,
                "current_as_of_existing": data.get("current_as_of"),
            })

    # task_manifest.txt
    manifest_lines = source_ids[:]
    if not_found:
        manifest_lines.append("")
        manifest_lines.append("# SRC IDs in issue manifest but not found in hosted/content/sources/:")
        manifest_lines.extend(f"# {sid}" for sid in not_found)
    (out_dir / "task_manifest.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    # unreachable.yaml (report-only, NO target_action — non-entity-prefix file)
    if unreachable:
        (out_dir / "unreachable.yaml").write_text(
            yaml.safe_dump({
                "_contribution": {
                    "chunk_id": chunk_id,
                    "contributor": "claude-anthropic-internal",
                    "submission_date": "2026-04-29",
                    "ai_tool": "claude-code",
                    "ai_model": "claude-opus-4-7",
                    "notes_for_reviewer": (
                        "Report-only flag list: sources whose URL HEAD did not return 2xx/3xx. "
                        "Most HTTP 403 are publisher bot-blocking (real browser would succeed); "
                        "HTTP 404 are genuinely broken — maintainer browser-verify before next action."
                    ),
                },
                "rows": unreachable,
            }, sort_keys=False, allow_unicode=True, default_flow_style=False),
            encoding="utf-8",
        )

    # refresh_summary.yaml (report-only)
    (out_dir / "refresh_summary.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": chunk_id,
                "contributor": "claude-anthropic-internal",
                "submission_date": "2026-04-29",
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "notes_for_reviewer": "Report-only aggregate stats.",
            },
            "issue_number": issue_number,
            "manifest_count": len(source_ids),
            "upserts_count": len(upserts),
            "unreachable_count": len(unreachable),
            "not_found_count": len(not_found),
            "status_distribution": dict(status_dist),
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    # _contribution_meta.yaml (chunk-level)
    (out_dir / "_contribution_meta.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": chunk_id,
                "contributor": "claude-anthropic-internal",
                "submission_date": "2026-04-29",
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "ai_model_version": "1m-context",
                "ai_session_notes": (
                    f"Wave 7 batch — closes #{issue_number}. Real HTTP HEAD checks on "
                    f"{len(source_ids)} sources from chunk manifest via stdlib urllib. "
                    "Worker shared across chunks 92-121 (see "
                    "contributions/_wave7_recency_batch/_batch_worker.py)."
                ),
                "tasktorrent_version": "2026-04-29-pending-first-commit",
                "notes_for_reviewer": (
                    "Per-source upsert touches only: current_as_of, last_recency_check, "
                    "recency_check_status_code. Content/license/attribution unchanged."
                ),
            },
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    return {
        "chunk_id": chunk_id, "issue_number": issue_number,
        "upserts": len(upserts), "unreachable": len(unreachable),
        "not_found": len(not_found), "status_dist": dict(status_dist),
    }


def main() -> int:
    with open(MANIFESTS_FILE, encoding="utf-8") as f:
        manifests = json.load(f)
    summaries = []
    for issue_num_str in sorted(manifests.keys(), key=int):
        n = int(issue_num_str)
        chunk_id, sources = manifests[issue_num_str]
        print(f"  Processing #{n} {chunk_id} ({len(sources)} sources)...", file=sys.stderr)
        s = process_chunk(chunk_id, sources, n)
        summaries.append(s)
        print(f"    {s['upserts']} upserts, {s['unreachable']} unreachable, {s['not_found']} not-found",
              file=sys.stderr)
    # Cross-chunk batch summary
    total = {
        "total_chunks": len(summaries),
        "total_upserts": sum(s["upserts"] for s in summaries),
        "total_unreachable": sum(s["unreachable"] for s in summaries),
        "total_not_found": sum(s["not_found"] for s in summaries),
        "per_chunk": summaries,
    }
    Path("/tmp/wave7_recency_summary.json").write_text(json.dumps(total, indent=2), encoding="utf-8")
    print(f"\nBatch done: {total['total_chunks']} chunks · "
          f"{total['total_upserts']} upserts · {total['total_unreachable']} unreachable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
