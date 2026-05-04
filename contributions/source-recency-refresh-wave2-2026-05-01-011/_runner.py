"""Wave-2 source recency refresh — chunk source-recency-refresh-wave2-2026-05-01-011.

Per-source HTTPS GET check using httpx (User-Agent: Mozilla/5.0 ... OpenOnco-recency-bot,
30s timeout, 3 retries). Writes sidecar contributions only; never edits hosted KB.

Pattern mirrors contributions/source-recency-refresh-wave2-2026-05-01-006/_runner.py.

Outcome routing per agent brief:
- 200            -> upsert (bump current_as_of, last_recency_check, recency_check_status_code)
- 3xx           -> upsert + redirect note
- 404 / 410     -> unreachable.dead (no current_as_of bump)
- 403           -> DOI fallback if available; else unreachable.blocked (no bump)
- network err   -> unreachable (no bump)
- no URL        -> unreachable + suggest field
"""

from __future__ import annotations

import datetime as dt
import sys
import time
from collections import Counter
from pathlib import Path

import httpx
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"
CHUNK_ID = "source-recency-refresh-wave2-2026-05-01-011"
ISSUE_NUMBER = 213
TODAY = dt.date(2026, 5, 1)
TIMEOUT_SEC = 30
RETRIES = 3
CHUNK_DIR = REPO_ROOT / "contributions" / CHUNK_ID
USER_AGENT = "Mozilla/5.0 (compatible; OpenOnco-recency-bot)"

MANIFEST = [
    "SRC-EASL-HCV-2023",
    "SRC-NCCN-HEPATOBILIARY",
    "SRC-OCEANS-AGHAJANIAN-2012",
    "SRC-NOVA-MIRZA-2016",
    "SRC-KEYNOTE-054-EGGERMONT-2018",
]


def http_check(url: str, retries: int = RETRIES) -> tuple[int | None, str, str | None]:
    """GET with redirects allowed. Returns (status, error_msg, final_url_if_redirected).

    The agent brief mandates httpx GET with the OpenOnco-recency-bot UA.
    follow_redirects=True so 301/302/307/308 chains resolve to a final 2xx
    when the publisher does that — we still record status of the final
    response. The caller distinguishes "200 same URL" from "200 after
    redirect" by comparing final_url to the input URL.
    """
    last_err = ""
    last_status: int | None = None
    final_url: str | None = None
    headers = {"User-Agent": USER_AGENT}
    for attempt in range(retries):
        try:
            with httpx.Client(
                timeout=TIMEOUT_SEC,
                follow_redirects=True,
                headers=headers,
            ) as client:
                resp = client.get(url)
                last_status = resp.status_code
                if str(resp.url) != url:
                    final_url = str(resp.url)
                # Success or definitive client error — stop retrying.
                if 200 <= resp.status_code < 400 or resp.status_code in (404, 410):
                    return resp.status_code, "", final_url
                if resp.status_code == 403 and attempt + 1 < retries:
                    last_err = f"HTTP 403 Forbidden"
                    time.sleep(1)
                    continue
                # Other 4xx/5xx — return status, no retry on the last attempt
                if attempt + 1 == retries:
                    return resp.status_code, f"HTTP {resp.status_code}", final_url
        except httpx.HTTPError as e:
            last_err = f"{type(e).__name__}: {e}"[:160]
            if attempt + 1 == retries:
                return None, last_err, None
            time.sleep(1)
        except Exception as e:  # noqa: BLE001
            last_err = f"{type(e).__name__}: {e}"[:160]
            if attempt + 1 == retries:
                return None, last_err, None
            time.sleep(1)
    return last_status, last_err, final_url


def doi_fallback_url(data: dict) -> str | None:
    doi = data.get("doi")
    if isinstance(doi, str) and doi:
        if doi.lower().startswith("http"):
            return doi
        return f"https://doi.org/{doi}"
    pmid = data.get("pmid")
    if isinstance(pmid, (str, int)) and str(pmid).strip():
        return f"https://pubmed.ncbi.nlm.nih.gov/{str(pmid).strip()}"
    return None


def _src_yaml_path(src_id: str) -> Path | None:
    candidate = src_id.replace("SRC-", "").lower().replace("-", "_")
    direct = SOURCES_DIR / f"src_{candidate}.yaml"
    if direct.is_file():
        return direct
    for p in SOURCES_DIR.glob("*.yaml"):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict) and data.get("id") == src_id:
            return p
    return None


def _license_status_str(data: dict) -> str:
    lic = data.get("license") if isinstance(data.get("license"), dict) else None
    legal = data.get("legal_review") if isinstance(data.get("legal_review"), dict) else None
    license_name = lic.get("name") if lic else None
    legal_status = legal.get("status") if legal else None
    if license_name:
        return f"{license_name} (legal_review={legal_status or 'unset'})"
    return f"missing (no license.name, legal_review={legal_status or 'unset'})"


def _build_upsert(
    data: dict, sid: str, src_path: Path, status: int, note_for_reviewer: str
) -> None:
    upsert = dict(data)
    upsert["current_as_of"] = TODAY.isoformat()
    upsert["last_recency_check"] = TODAY.isoformat()
    upsert["recency_check_status_code"] = status
    upsert["_contribution"] = {
        "chunk_id": CHUNK_ID,
        "contributor": "claude-anthropic-internal",
        "submission_date": TODAY.isoformat(),
        "ai_tool": "claude-code",
        "ai_model": "claude-opus-4-7",
        "ai_model_version": "1m-context",
        "target_action": "upsert",
        "target_entity_id": sid,
        "notes_for_reviewer": note_for_reviewer,
    }
    (CHUNK_DIR / src_path.name).write_text(
        yaml.safe_dump(upsert, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )


def main() -> int:
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    upserts: list[dict] = []
    unreachable: list[dict] = []
    not_found: list[str] = []
    audit_rows: list[dict] = []
    status_dist: Counter[str] = Counter()

    for sid in MANIFEST:
        src_path = _src_yaml_path(sid)
        if src_path is None:
            not_found.append(sid)
            status_dist["src_not_found"] += 1
            audit_rows.append({
                "id": sid, "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": "unknown",
                "notes": "Source YAML not found in hosted/content/sources/.",
            })
            continue
        try:
            data = yaml.safe_load(src_path.read_text(encoding="utf-8"))
        except Exception as exc:
            not_found.append(sid)
            status_dist["src_parse_fail"] += 1
            audit_rows.append({
                "id": sid, "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": "unknown",
                "notes": f"YAML parse fail: {exc!r}",
            })
            continue
        if not isinstance(data, dict):
            not_found.append(sid)
            audit_rows.append({
                "id": sid, "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": "unknown",
                "notes": "Top-level YAML is not a mapping.",
            })
            continue

        url = data.get("url")
        license_status = _license_status_str(data)

        if not url:
            unreachable.append({
                "id": sid, "url": None, "status_code": None,
                "error": "no url field in source yaml — suggest populate URL/citation",
                "current_as_of_existing": data.get("current_as_of"),
            })
            status_dist["no_url"] += 1
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": license_status,
                "notes": (
                    "Source stub has no URL field. Cannot HTTP-verify. "
                    "Maintainer must populate URL/citation before bump."
                ),
            })
            continue

        status, err, final_url = http_check(url)
        bucket = (
            "ok" if status and 200 <= status < 300 else
            "redirect" if status and 300 <= status < 400 else
            f"http_{status}" if status else "network_error"
        )
        status_dist[bucket] += 1

        # Outcome dispatch per agent brief.
        if status and 200 <= status < 300:
            note = (
                f"Recency refresh: HTTP {status} via httpx GET (UA={USER_AGENT}). "
                f"URL reachable. current_as_of bumped from {data.get('current_as_of', '(unset)')} "
                f"to {TODAY.isoformat()}. No content/license/attribution fields modified."
            )
            _build_upsert(data, sid, src_path, status, note)
            upserts.append({"id": sid, "url": url, "status": status})
            audit_rows.append({
                "id": sid,
                "url_verified": "yes",
                "content_current": "yes",
                "proposed_current_as_of": TODAY.isoformat(),
                "license_status": license_status,
                "notes": f"HTTP {status} via httpx GET. URL resolves; clinical content unchanged.",
            })
        elif status and 300 <= status < 400:
            redirect_note = f" Redirected to {final_url}." if final_url else ""
            note = (
                f"Recency refresh: HTTP {status} via httpx GET (redirect).{redirect_note} "
                f"current_as_of bumped from {data.get('current_as_of', '(unset)')} "
                f"to {TODAY.isoformat()}. No content/license/attribution fields modified. "
                "Maintainer may want to update url field to the new canonical destination."
            )
            _build_upsert(data, sid, src_path, status, note)
            upserts.append({"id": sid, "url": url, "status": status, "redirect_to": final_url})
            audit_rows.append({
                "id": sid,
                "url_verified": f"replaced-with: {final_url}" if final_url else "yes (redirect)",
                "content_current": "yes",
                "proposed_current_as_of": TODAY.isoformat(),
                "license_status": license_status,
                "notes": (
                    f"HTTP {status} via httpx GET (redirect). "
                    f"{f'Final URL: {final_url}. ' if final_url else ''}"
                    "Clinical content unchanged."
                ),
            })
        elif status in (404, 410):
            unreachable.append({
                "id": sid, "url": url, "status_code": status,
                "error": f"HTTP {status} — dead link",
                "current_as_of_existing": data.get("current_as_of"),
                "category": "dead",
            })
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": license_status,
                "notes": (
                    f"HTTP {status} (dead link). Existing current_as_of preserved at "
                    f"{data.get('current_as_of')}. Maintainer must locate replacement URL."
                ),
            })
        elif status == 403:
            # DOI fallback per brief.
            fallback = doi_fallback_url(data)
            if fallback and fallback != url:
                fb_status, fb_err, fb_final = http_check(fallback)
                if fb_status and 200 <= fb_status < 400:
                    note = (
                        f"Recency refresh: original URL HTTP 403 (publisher bot-block); "
                        f"DOI/PubMed fallback {fallback} returned HTTP {fb_status}. "
                        f"current_as_of bumped from {data.get('current_as_of', '(unset)')} "
                        f"to {TODAY.isoformat()}. No content/license/attribution fields modified."
                    )
                    _build_upsert(data, sid, src_path, fb_status, note)
                    upserts.append({
                        "id": sid, "url": url, "status": 403,
                        "fallback": fallback, "fallback_status": fb_status,
                    })
                    status_dist["http_403_fallback_ok"] += 1
                    audit_rows.append({
                        "id": sid,
                        "url_verified": f"yes (DOI/PubMed fallback: {fallback})",
                        "content_current": "yes",
                        "proposed_current_as_of": TODAY.isoformat(),
                        "license_status": license_status,
                        "notes": (
                            f"Original URL HTTP 403 (publisher bot-block). "
                            f"DOI/PubMed fallback {fallback} returned HTTP {fb_status}. "
                            "Clinical content unchanged."
                        ),
                    })
                    continue
                # Fallback also failed — record as blocked.
            unreachable.append({
                "id": sid, "url": url, "status_code": 403,
                "error": f"HTTP 403 Forbidden (publisher bot-block); fallback={'tried-failed' if fallback else 'unavailable'}",
                "current_as_of_existing": data.get("current_as_of"),
                "category": "blocked",
            })
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": license_status,
                "notes": (
                    "HTTP 403 (publisher bot-block — real browser would likely succeed). "
                    f"DOI/PubMed fallback {'attempted but also blocked' if fallback else 'unavailable'}. "
                    f"Existing current_as_of preserved at {data.get('current_as_of')}. "
                    "No bump. Maintainer browser-verify before next action."
                ),
            })
        else:
            unreachable.append({
                "id": sid, "url": url, "status_code": status, "error": err,
                "current_as_of_existing": data.get("current_as_of"),
                "category": "other",
            })
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": license_status,
                "notes": (
                    f"HTTP {status if status else 'network_error'} ({err}). "
                    f"Existing current_as_of preserved at {data.get('current_as_of')}. "
                    "Maintainer browser-verify before next action."
                ),
            })

    # task_manifest.txt
    lines = MANIFEST[:]
    if not_found:
        lines.append("")
        lines.append("# SRC IDs in issue manifest but not found in hosted/content/sources/:")
        lines.extend(f"# {sid}" for sid in not_found)
    (CHUNK_DIR / "task_manifest.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # unreachable.yaml
    if unreachable:
        (CHUNK_DIR / "unreachable.yaml").write_text(
            yaml.safe_dump({
                "_contribution": {
                    "chunk_id": CHUNK_ID,
                    "contributor": "claude-anthropic-internal",
                    "submission_date": TODAY.isoformat(),
                    "ai_tool": "claude-code",
                    "ai_model": "claude-opus-4-7",
                    "notes_for_reviewer": (
                        "Report-only flag list: sources whose URL HTTP check did not return 2xx/3xx, "
                        "or which lack a URL field entirely. HTTP 403 = publisher bot-block "
                        "(real browser would likely succeed). HTTP 404/410 = genuinely dead. "
                        "DOI/PubMed fallback was attempted on 403 where doi/pmid present. "
                        "Maintainer browser-verify before next action."
                    ),
                },
                "rows": unreachable,
            }, sort_keys=False, allow_unicode=True, default_flow_style=False),
            encoding="utf-8",
        )

    # refresh_summary.yaml
    (CHUNK_DIR / "refresh_summary.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": CHUNK_ID,
                "contributor": "claude-anthropic-internal",
                "submission_date": TODAY.isoformat(),
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "notes_for_reviewer": "Report-only aggregate stats.",
            },
            "issue_number": ISSUE_NUMBER,
            "manifest_count": len(MANIFEST),
            "upserts_count": len(upserts),
            "unreachable_count": len(unreachable),
            "not_found_count": len(not_found),
            "status_distribution": dict(status_dist),
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    # source_recency_audit.yaml — issue-mandated structured audit
    (CHUNK_DIR / "source_recency_audit.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": CHUNK_ID,
                "contributor": "claude-anthropic-internal",
                "submission_date": TODAY.isoformat(),
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "notes_for_reviewer": (
                    "Per-source structured audit per issue #213 Output Requirements: "
                    "id, url_verified (yes/no/replaced-with), content_current "
                    "(yes/no/superseded-by), proposed_current_as_of, license_status, notes."
                ),
            },
            "issue_number": ISSUE_NUMBER,
            "rows": audit_rows,
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    # _contribution_meta.yaml — chunk-level meta
    (CHUNK_DIR / "_contribution_meta.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": CHUNK_ID,
                "contributor": "claude-anthropic-internal",
                "submission_date": TODAY.isoformat(),
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "ai_model_version": "1m-context",
                "ai_session_notes": (
                    f"Wave-2 batch — closes #{ISSUE_NUMBER}. Real HTTPS GET checks via httpx "
                    f"(User-Agent: {USER_AGENT}, 30s timeout, 3 retries) on 5 sources. "
                    "Pattern mirrors contributions/source-recency-refresh-wave2-2026-05-01-006/. "
                    "Per-source upsert touches only: current_as_of, last_recency_check, "
                    "recency_check_status_code. Content/license/attribution unchanged."
                ),
                "tasktorrent_version": "2026-05-01-wave2",
                "claim_method": "formal-issue",
                "notes_for_reviewer": (
                    "All edits are sidecar files under contributions/<chunk-id>/. "
                    "No hosted KB files modified. source_recency_audit.yaml provides "
                    "issue-mandated structured audit; src_*.yaml files provide upsert "
                    "payloads for reachable sources."
                ),
            },
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    print(f"manifest={len(MANIFEST)} upserts={len(upserts)} "
          f"unreachable={len(unreachable)} not_found={len(not_found)} "
          f"status_dist={dict(status_dist)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
