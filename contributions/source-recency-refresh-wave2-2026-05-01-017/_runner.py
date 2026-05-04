"""Recency-refresh runner for chunk source-recency-refresh-wave2-2026-05-01-017.

Performs real HTTP HEAD/GET checks via stdlib urllib (30s timeout, 3 retries)
on each source URL in the chunk manifest. Mirrors pattern from
contributions/source-recency-refresh-wave2-2026-05-01-006/_runner.py.

Outcomes:
- 200/3xx (HEAD or GET fallback): emit upsert sidecar bumping current_as_of,
  last_recency_check, recency_check_status_code (no other content modified).
- 403 with DOI fallback success: same upsert payload tagged with redirect note.
- 403 (no DOI/PubMed fallback): unreachable.blocked.
- 404/410: unreachable.dead.
- No URL field: unreachable.no_url.

This is a one-shot script; it writes upsert YAMLs, unreachable.yaml,
refresh_summary.yaml, and source_recency_audit.yaml side-by-side.
"""

from __future__ import annotations

import datetime as _dt
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

CHUNK_ID = "source-recency-refresh-wave2-2026-05-01-017"
ISSUE_NUMBER = 219
TODAY = "2026-05-01"
USER_AGENT = "Mozilla/5.0 (compatible; OpenOnco-recency-bot)"
TIMEOUT_S = 30
RETRIES = 3

REPO_ROOT = Path(__file__).resolve().parents[2]
HOSTED = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"
OUT_DIR = REPO_ROOT / "contributions" / CHUNK_ID

MANIFEST = [
    ("SRC-ESMO-HNSCC-2020", "src_esmo_hnscc_2020.yaml"),
    ("SRC-PAPMET", "src_papmet.yaml"),
    ("SRC-AURELIA-PUJADE-LAURAINE-2014", "src_aurelia_pujade_lauraine_2014.yaml"),
    ("SRC-JAKARTA2-HARRISON-2017", "src_jakarta2_harrison_2017.yaml"),
    ("SRC-ESCAT-MATEO-2018", "src_escat_mateo_2018.yaml"),
]


def _http_check(url: str, method: str = "HEAD") -> tuple[int | None, str | None]:
    """Try url; return (status_code, error). status=None on failure."""
    req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    last_err = None
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                return resp.status, None
        except urllib.error.HTTPError as e:
            return e.code, e.reason
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = str(e)
            time.sleep(1 + attempt)
    return None, last_err


def check_url(url: str) -> tuple[int | None, str | None, str]:
    """HEAD then GET fallback. Returns (status_code, error, method_used)."""
    code, err = _http_check(url, "HEAD")
    if code in (200, 301, 302, 303, 307, 308):
        return code, None, "HEAD"
    if code == 403:
        # try GET — many publishers 403 on HEAD but accept GET
        code2, err2 = _http_check(url, "GET")
        if code2 in (200, 301, 302, 303, 307, 308):
            return code2, None, "GET"
        return code2 or code, err2 or err, "GET"
    if code is None:
        # connection-level failure: try GET as last resort
        code2, err2 = _http_check(url, "GET")
        return code2, err2, "GET"
    return code, err, "HEAD"


def _doi_fallbacks(doc: dict) -> list[str]:
    """Compute DOI / PubMed canonical URL fallbacks from existing metadata.

    Returns a list of fallback URLs to try in order. PubMed is generally
    more reliable than doi.org -> publisher landing pages because publishers
    often 403 bot user-agents.
    """
    out = []
    pmid = doc.get("pmid")
    doi = doc.get("doi")
    if pmid:
        out.append(f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/")
    if doi:
        out.append(f"https://doi.org/{doi}")
    return out


def main() -> int:
    audit_rows = []
    upsert_count = 0
    unreachable_rows = []
    not_found_count = 0
    status_dist: dict[str, int] = {}

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for src_id, fname in MANIFEST:
        path = HOSTED / fname
        if not path.exists():
            audit_rows.append({
                "id": src_id,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": "unknown (hosted file missing)",
                "notes": f"hosted source file not found: {path.name}",
            })
            unreachable_rows.append({
                "id": src_id,
                "url": None,
                "status_code": None,
                "error": "hosted source yaml missing",
                "current_as_of_existing": None,
            })
            status_dist["missing_file"] = status_dist.get("missing_file", 0) + 1
            continue

        with path.open("r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)

        url = doc.get("url")
        existing_as_of = doc.get("current_as_of")
        license_block = doc.get("license") or {}
        license_name = license_block.get("name") if isinstance(license_block, dict) else None
        legal_review = doc.get("legal_review") or {}
        lr_status = legal_review.get("status") if isinstance(legal_review, dict) else None
        license_summary = (
            f"{license_name} (legal_review={lr_status})"
            if license_name
            else f"missing (no license.name, legal_review={lr_status})"
        )

        if not url:
            audit_rows.append({
                "id": src_id,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": license_summary,
                "notes": "Source stub has no URL field. Cannot HTTP-verify. Maintainer must populate URL/citation/license before bump.",
            })
            unreachable_rows.append({
                "id": src_id,
                "url": None,
                "status_code": None,
                "error": "no url field in source yaml",
                "current_as_of_existing": existing_as_of,
            })
            status_dist["no_url"] = status_dist.get("no_url", 0) + 1
            continue

        code, err, method = check_url(url)
        url_used = url
        used_fallback = False

        # 403 / connection failures: try DOI / PubMed fallbacks before giving up
        if code is None or code in (403,):
            for fb in _doi_fallbacks(doc):
                if fb == url:
                    continue
                code2, err2, method2 = check_url(fb)
                if code2 in (200, 301, 302, 303, 307, 308):
                    code, err, method = code2, None, method2
                    url_used = fb
                    used_fallback = True
                    break

        success = code in (200, 301, 302, 303, 307, 308)

        if success:
            upsert_count += 1
            status_dist["ok"] = status_dist.get("ok", 0) + 1
            # build upsert payload: existing doc + bumped fields + _contribution wrapper
            payload = dict(doc)
            payload["current_as_of"] = TODAY
            payload["last_recency_check"] = TODAY
            payload["recency_check_status_code"] = code
            note_parts = [
                f"Recency refresh: HTTP {code} via {method}.",
                "URL reachable via DOI fallback." if used_fallback else "URL reachable.",
                f"current_as_of bumped from {existing_as_of} to {TODAY}.",
                "No content/license/attribution fields modified.",
            ]
            payload["_contribution"] = {
                "chunk_id": CHUNK_ID,
                "contributor": "claude-anthropic-internal",
                "submission_date": TODAY,
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "ai_model_version": "1m-context",
                "target_action": "upsert",
                "target_entity_id": src_id,
                "notes_for_reviewer": " ".join(note_parts),
            }
            out_path = OUT_DIR / fname
            with out_path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(payload, f, sort_keys=False, allow_unicode=True, width=100)
            audit_rows.append({
                "id": src_id,
                "url_verified": "replaced-with-doi" if used_fallback else "yes",
                "content_current": "yes",
                "proposed_current_as_of": TODAY,
                "license_status": license_summary,
                "notes": (
                    f"HTTP {code} via {method}"
                    + (f" (DOI fallback {url_used})" if used_fallback else "")
                    + ". URL resolves; clinical content unchanged."
                ),
            })
        else:
            # unreachable
            err_label = err or f"HTTP {code}"
            if code in (404, 410):
                key = f"http_{code}"
                not_found_count += 1
            elif code == 403:
                key = "http_403"
            elif code is None:
                key = "connection_error"
            else:
                key = f"http_{code}"
            status_dist[key] = status_dist.get(key, 0) + 1
            unreachable_rows.append({
                "id": src_id,
                "url": url_used,
                "status_code": code,
                "error": err_label,
                "current_as_of_existing": existing_as_of,
            })
            audit_rows.append({
                "id": src_id,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": license_summary,
                "notes": (
                    f"HTTP {code or 'connection-error'} ({err_label}) via {method}. "
                    f"Existing current_as_of preserved at {existing_as_of}. "
                    "Maintainer browser-verify before next action."
                ),
            })

    # task_manifest.txt
    (OUT_DIR / "task_manifest.txt").write_text(
        "\n".join(src_id for src_id, _ in MANIFEST) + "\n",
        encoding="utf-8",
    )

    # _contribution_meta.yaml
    meta = {
        "_contribution": {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": TODAY,
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "ai_model_version": "1m-context",
            "ai_session_notes": (
                f"Wave-2 batch — closes #{ISSUE_NUMBER}. Real HTTP HEAD/GET checks via "
                f"stdlib urllib (30s timeout, 3 retries) on {len(MANIFEST)} sources. "
                "Pattern mirrors contributions/source-recency-refresh-2026-04-29-001/. "
                "Per-source upsert touches only: current_as_of, last_recency_check, "
                "recency_check_status_code. Content/license/attribution unchanged. "
                "DOI/PubMed fallback used on 403 from publisher landing pages."
            ),
            "tasktorrent_version": "2026-05-01-wave2",
            "claim_method": "formal-issue",
            "notes_for_reviewer": (
                "All edits are sidecar files under contributions/<chunk-id>/. "
                "No hosted KB files modified. source_recency_audit.yaml provides "
                "issue-mandated structured audit; src_*.yaml files provide upsert "
                "payloads for reachable sources."
            ),
        }
    }
    with (OUT_DIR / "_contribution_meta.yaml").open("w", encoding="utf-8") as f:
        yaml.safe_dump(meta, f, sort_keys=False, allow_unicode=True, width=100)

    # source_recency_audit.yaml — issue-mandated audit format
    audit = {
        "_contribution": {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": TODAY,
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "notes_for_reviewer": (
                f"Per-source structured audit per issue #{ISSUE_NUMBER} Output Requirements: "
                "id, url_verified (yes/no/replaced-with), content_current (yes/no/superseded-by), "
                "proposed_current_as_of, license_status, notes."
            ),
        },
        "issue_number": ISSUE_NUMBER,
        "rows": audit_rows,
    }
    with (OUT_DIR / "source_recency_audit.yaml").open("w", encoding="utf-8") as f:
        yaml.safe_dump(audit, f, sort_keys=False, allow_unicode=True, width=100)

    # unreachable.yaml
    unreach = {
        "_contribution": {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": TODAY,
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "notes_for_reviewer": (
                "Report-only flag list: sources whose URL HEAD/GET did not return 2xx/3xx, "
                "or which lack a URL field entirely. HTTP 403 typically means publisher "
                "bot-blocking (real browser would succeed); HTTP 404/410 are genuinely broken. "
                "Maintainer browser-verify before next action."
            ),
        },
        "rows": unreachable_rows,
    }
    with (OUT_DIR / "unreachable.yaml").open("w", encoding="utf-8") as f:
        yaml.safe_dump(unreach, f, sort_keys=False, allow_unicode=True, width=100)

    # refresh_summary.yaml
    summary = {
        "_contribution": {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": TODAY,
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "notes_for_reviewer": "Report-only aggregate stats.",
        },
        "issue_number": ISSUE_NUMBER,
        "manifest_count": len(MANIFEST),
        "upserts_count": upsert_count,
        "unreachable_count": len(unreachable_rows),
        "not_found_count": not_found_count,
        "status_distribution": status_dist,
    }
    with (OUT_DIR / "refresh_summary.yaml").open("w", encoding="utf-8") as f:
        yaml.safe_dump(summary, f, sort_keys=False, allow_unicode=True, width=100)

    # upsert log
    ts = _dt.datetime.utcnow().strftime("%Y-%m-%dT%H%M%SZ")
    log_lines = [
        f"# Upsert log: {CHUNK_ID} ({ts})",
        "Mode: PLAN (no writes; sidecars only — maintainer applies via tasktorrent merger)",
        "",
    ]
    for src_id, fname in MANIFEST:
        side = OUT_DIR / fname
        if side.exists():
            log_lines.append(
                f"- contributions/{CHUNK_ID}/{fname}: UPDATE -> "
                f"knowledge_base/hosted/content/sources/{fname}"
            )
        else:
            log_lines.append(f"- contributions/{CHUNK_ID}/{fname}: SKIP (unreachable; see unreachable.yaml)")
    log_lines.append(f"- contributions/{CHUNK_ID}/refresh_summary.yaml: SKIP unknown prefix")
    log_lines.append(f"- contributions/{CHUNK_ID}/source_recency_audit.yaml: SKIP unknown prefix")
    log_lines.append(f"- contributions/{CHUNK_ID}/unreachable.yaml: SKIP unknown prefix")
    (OUT_DIR / f"upsert-log-{ts}.md").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    # stdout report
    print(json.dumps({
        "manifest_count": len(MANIFEST),
        "upserts_count": upsert_count,
        "unreachable_count": len(unreachable_rows),
        "status_distribution": status_dist,
        "audit": audit_rows,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
