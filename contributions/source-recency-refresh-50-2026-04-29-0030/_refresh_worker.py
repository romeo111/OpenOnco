"""Worker for chunk #33 — source-recency-refresh-50.

Picks 50 sources weighted by (a) staleness (current_as_of age) and
(b) citation count from BMA + IND + RF entities. Performs a real
HTTP HEAD check on each Source.url (via stdlib urllib — no extra deps).

For each verified-reachable source: writes upsert sidecar that updates
`current_as_of` to today and adds `last_recency_check` timestamp +
`recency_check_status_code`. Sources with non-2xx/3xx responses are
flagged in `unreachable.yaml` for maintainer review (no current_as_of
update without confirmed reachability).

Output: contributions/source-recency-refresh-50-2026-04-29-0030/
  src_<id>.yaml             — one per verified source (target_action: upsert)
  unreachable.yaml          — flagged sources, if any
  refresh_summary.yaml      — aggregate stats
  task_manifest.txt
  _contribution_meta.yaml
"""

from __future__ import annotations

import datetime as dt
import socket
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"
OUT_DIR = REPO_ROOT / "contributions" / "source-recency-refresh-50-2026-04-29-0030"
TODAY = dt.date(2026, 4, 29)
TIMEOUT_SEC = 8


def _date_from_value(v) -> dt.date | None:
    if isinstance(v, dt.date):
        return v
    if isinstance(v, str):
        try:
            return dt.date.fromisoformat(v[:10])
        except ValueError:
            return None
    return None


def count_citations(source_id: str) -> int:
    """Count how many other entities reference this source-id by stable-id."""
    n = 0
    for sub in ("biomarker_actionability", "indications", "redflags"):
        d = REPO_ROOT / "knowledge_base" / "hosted" / "content" / sub
        if not d.is_dir():
            continue
        for p in d.glob("*.yaml"):
            try:
                text = p.read_text(encoding="utf-8")
            except OSError:
                continue
            if source_id in text:
                n += 1
    return n


def select_50() -> list[tuple[str, dict, Path]]:
    """Returns [(source_id, parsed_yaml, path), ...] sorted by priority."""
    candidates = []
    for path in sorted(SOURCES_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        sid = data.get("id")
        url = data.get("url")
        if not sid or not url:
            continue
        cao = _date_from_value(data.get("current_as_of"))
        age_days = (TODAY - cao).days if cao else 9999
        if age_days < 365:
            continue  # only refresh stale-by-date sources
        candidates.append((sid, data, path, age_days))

    # Score = age_days + 30 * citation_count
    scored = []
    for sid, data, path, age in candidates:
        citations = count_citations(sid)
        score = age + 30 * citations
        scored.append((score, sid, data, path, citations))
    scored.sort(key=lambda t: -t[0])
    return [(sid, data, path) for _, sid, data, path, _ in scored[:50]]


def http_head(url: str) -> tuple[int | None, str]:
    """Returns (status_code, error_msg). status None on error."""
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
        # Some sites reject HEAD but accept GET — surface 405 distinctly
        if e.code == 405:
            return _http_get_fallback(url)
        return e.code, str(e.reason)[:120]
    except (urllib.error.URLError, socket.timeout, OSError) as e:
        return None, str(e)[:120]


def _http_get_fallback(url: str) -> tuple[int | None, str]:
    socket.setdefaulttimeout(TIMEOUT_SEC)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "TaskTorrent-RecencyCheck/0.4"},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
            return resp.getcode() or 0, "via GET"
    except urllib.error.HTTPError as e:
        return e.code, f"via GET: {e.reason}"[:120]
    except (urllib.error.URLError, socket.timeout, OSError) as e:
        return None, f"via GET: {e}"[:120]


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    selected = select_50()
    print(f"  Selected {len(selected)} sources for refresh check")

    upserts: list[dict] = []
    unreachable: list[dict] = []
    status_dist: Counter[str] = Counter()

    for i, (sid, src_data, src_path) in enumerate(selected, 1):
        url = src_data.get("url")
        status, err = http_head(url)
        bucket = (
            "ok" if status and 200 <= status < 400 else
            f"http_{status}" if status else
            "network_error"
        )
        status_dist[bucket] += 1
        print(f"  [{i:2d}/{len(selected)}] {sid:50s} {bucket}", file=sys.stderr)

        if status and 200 <= status < 400:
            # Build upsert sidecar — only modify recency-related fields
            upsert = dict(src_data)
            upsert["current_as_of"] = TODAY.isoformat()
            upsert["last_recency_check"] = TODAY.isoformat()
            upsert["recency_check_status_code"] = status
            upsert["_contribution"] = {
                "target_action": "upsert",
                "target_entity_id": sid,
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "notes_for_reviewer": (
                    f"Recency refresh: HTTP {status} on HEAD. URL reachable. "
                    f"current_as_of bumped from {src_data.get('current_as_of', '(unset)')} "
                    f"to {TODAY.isoformat()}. No content fields modified."
                ),
            }
            out_name = src_path.name
            (OUT_DIR / out_name).write_text(
                yaml.safe_dump(upsert, sort_keys=False, allow_unicode=True, default_flow_style=False),
                encoding="utf-8",
            )
            upserts.append({"id": sid, "url": url, "status": status})
        else:
            unreachable.append({
                "id": sid,
                "url": url,
                "status_code": status,
                "error": err,
                "current_as_of_existing": src_data.get("current_as_of"),
            })

    # Write unreachable list
    if unreachable:
        (OUT_DIR / "unreachable.yaml").write_text(
            yaml.safe_dump({
                "_contribution_kind": "unreachable-list",
                "chunk_id": "source-recency-refresh-50-2026-04-29-0030",
                "summary": f"{len(unreachable)} sources failed HEAD check; "
                           "current_as_of NOT bumped. Maintainer review needed.",
                "rows": unreachable,
            }, sort_keys=False, allow_unicode=True, default_flow_style=False),
            encoding="utf-8",
        )

    # Aggregate summary
    summary = {
        "_contribution_kind": "refresh-summary",
        "chunk_id": "source-recency-refresh-50-2026-04-29-0030",
        "selected_count": len(selected),
        "upserts_count": len(upserts),
        "unreachable_count": len(unreachable),
        "status_distribution": dict(status_dist),
        "today": TODAY.isoformat(),
    }
    (OUT_DIR / "refresh_summary.yaml").write_text(
        yaml.safe_dump(summary, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    # Manifest = list of source IDs touched
    manifest = "\n".join(s["id"] for s in upserts) + "\n"
    if unreachable:
        manifest += "\n# unreachable (no upsert):\n"
        manifest += "\n".join(f"# {u['id']}" for u in unreachable) + "\n"
    (OUT_DIR / "task_manifest.txt").write_text(manifest, encoding="utf-8")

    print(f"\n  Done. {len(upserts)} upserts, {len(unreachable)} unreachable.")
    print(f"  Status distribution: {dict(status_dist)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
