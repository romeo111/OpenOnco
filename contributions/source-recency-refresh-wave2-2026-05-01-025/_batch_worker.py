"""Wave-2 worker — source-recency-refresh-wave2-2026-05-01-025 (issue #227).

Per chunk brief:
  - httpx HEAD (NOT GET), UA Mozilla/5.0 (compatible; OpenOnco-recency-bot),
    30s timeout, 3 retries, follow_redirects=True.
  - 200/3xx: upsert (current_as_of bumped, last_recency_check + status_code added).
  - 404: dead → unreachable.dead.
  - 403: try DOI HEAD fallback → PubMed canonical HEAD fallback → unreachable.blocked.
  - No URL: unreachable.no_url.

Outputs to contributions/<chunk-id>/:
  _contribution_meta.yaml, task_manifest.txt,
  src_*.yaml upserts, unreachable.yaml, refresh_summary.yaml,
  upsert-log-<utc-stamp>.md (audit).
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
CONTRIB_ROOT = REPO_ROOT / "contributions"
CHUNK_ID = "source-recency-refresh-wave2-2026-05-01-025"
ISSUE_NUMBER = 227
TODAY = dt.date(2026, 5, 1)
TIMEOUT_SEC = 30
RETRIES = 3
USER_AGENT = "Mozilla/5.0 (compatible; OpenOnco-recency-bot)"

MANIFEST = [
    "SRC-FOENIX-CCA2",
    "SRC-PT1-HARRISON-2005",
    "SRC-RECOURSE-MAYER-2015",
    "SRC-CHECKMATE-238-WEBER-2017",
]


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


def _http_head(client: httpx.Client, url: str) -> tuple[int | None, str]:
    """HEAD with retries. Returns (status_code, error_message)."""
    last_err = ""
    for attempt in range(RETRIES):
        try:
            r = client.head(url)
            return r.status_code, ""
        except httpx.HTTPError as e:
            last_err = f"{type(e).__name__}: {str(e)[:120]}"
            if attempt < RETRIES - 1:
                time.sleep(1.0 * (attempt + 1))
    return None, last_err


def _resolve_url(client: httpx.Client, primary_url: str | None, doi: str | None,
                 pmid: str | None) -> tuple[int | None, str, str, str, list[dict]]:
    """Try primary → DOI → PubMed cascade.

    Returns (final_status, final_url_used, source_label, error_msg, trail).
    source_label ∈ {"primary", "doi_fallback", "pubmed_fallback", "no_url"}.
    trail records each attempt as {"url", "label", "code", "error"}.
    """
    trail: list[dict] = []

    def _try(url: str, label: str) -> tuple[int | None, str]:
        code, err = _http_head(client, url)
        trail.append({"url": url, "label": label, "code": code, "error": err})
        return code, err

    if primary_url:
        code, err = _try(primary_url, "primary")
        if code is not None and 200 <= code < 400:
            return code, primary_url, "primary", err, trail
        if code == 403:
            if doi:
                doi_url = f"https://doi.org/{doi}"
                doi_code, doi_err = _try(doi_url, "doi_fallback")
                if doi_code is not None and 200 <= doi_code < 400:
                    return doi_code, doi_url, "doi_fallback", doi_err, trail
            if pmid:
                pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}"
                pm_code, pm_err = _try(pubmed_url, "pubmed_fallback")
                if pm_code is not None and 200 <= pm_code < 400:
                    return pm_code, pubmed_url, "pubmed_fallback", pm_err, trail
            return code, primary_url, "primary", err, trail
        return code, primary_url, "primary", err, trail
    # No primary URL: try DOI then PubMed
    if doi:
        doi_url = f"https://doi.org/{doi}"
        doi_code, doi_err = _try(doi_url, "doi_fallback")
        if doi_code is not None and 200 <= doi_code < 400:
            return doi_code, doi_url, "doi_fallback", doi_err, trail
        if pmid:
            pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}"
            pm_code, pm_err = _try(pubmed_url, "pubmed_fallback")
            if pm_code is not None and 200 <= pm_code < 400:
                return pm_code, pubmed_url, "pubmed_fallback", pm_err, trail
        return doi_code, doi_url, "doi_fallback", doi_err, trail
    if pmid:
        pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}"
        pm_code, pm_err = _try(pubmed_url, "pubmed_fallback")
        return pm_code, pubmed_url, "pubmed_fallback", pm_err, trail
    return None, "", "no_url", "no_url_no_doi_no_pmid", trail


def main() -> int:
    out_dir = CONTRIB_ROOT / CHUNK_ID
    out_dir.mkdir(parents=True, exist_ok=True)

    upserts: list[tuple[str, dict, dict, dict]] = []  # (src_id, original, payload, meta)
    unreachable: list[dict] = []
    not_found: list[str] = []
    status_dist: Counter[str] = Counter()
    audit_lines: list[str] = []
    today_iso = TODAY.isoformat()
    stamp_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

    headers = {"User-Agent": USER_AGENT}
    with httpx.Client(timeout=TIMEOUT_SEC, follow_redirects=True, headers=headers) as client:
        for sid in MANIFEST:
            src_path = _src_yaml_path(sid)
            if src_path is None:
                not_found.append(sid)
                status_dist["src_not_found"] += 1
                audit_lines.append(f"- {sid}: SRC FILE NOT FOUND in hosted/")
                continue

            try:
                data = yaml.safe_load(src_path.read_text(encoding="utf-8"))
            except Exception as e:
                not_found.append(sid)
                status_dist["src_parse_error"] += 1
                audit_lines.append(f"- {sid}: parse error {e}")
                continue

            url = data.get("url")
            doi = data.get("doi")
            pmid = data.get("pmid")
            if isinstance(pmid, (int, float)):
                pmid = str(int(pmid))

            code, used_url, source_label, err, trail = _resolve_url(client, url, doi, pmid)

            existing_caof = data.get("current_as_of")
            existing_caof_str = (
                existing_caof.isoformat() if isinstance(existing_caof, dt.date) else
                (existing_caof if isinstance(existing_caof, str) else None)
            )

            if code is not None and 200 <= code < 400:
                # Upsert: bump current_as_of, add last_recency_check + status_code
                payload = dict(data)
                payload["current_as_of"] = today_iso
                payload["last_recency_check"] = today_iso
                payload["recency_check_status_code"] = int(code)
                # Optionally record cascade fallback as note in upsert metadata
                fallback_note = ""
                if source_label != "primary":
                    payload["url"] = used_url
                    fallback_note = (
                        f" Primary URL returned 403; succeeded via {source_label} "
                        f"({used_url}); url field updated to canonical resolver."
                    )
                meta = {
                    "chunk_id": CHUNK_ID,
                    "contributor": "claude-anthropic-internal",
                    "submission_date": today_iso,
                    "ai_tool": "claude-code",
                    "ai_model": "claude-opus-4-7",
                    "ai_model_version": "1m-context",
                    "target_action": "upsert",
                    "target_entity_id": sid,
                    "notes_for_reviewer": (
                        f"Recency refresh wave-2: HTTP {code} on HEAD via {source_label}. "
                        f"current_as_of bumped from {existing_caof_str} to {today_iso}. "
                        f"No content fields modified.{fallback_note}"
                    ),
                }
                upserts.append((sid, data, payload, meta))
                status_dist[f"http_{code}_{source_label}"] += 1
                audit_lines.append(
                    f"- {sid}: HTTP {code} via {source_label} → upsert (caof {existing_caof_str} → {today_iso})"
                )
            else:
                # Unreachable record. Classify reason.
                if code == 404:
                    reason = "dead"
                elif code == 403:
                    reason = "blocked"
                elif source_label == "no_url" and not url and not doi and not pmid:
                    reason = "no_url"
                else:
                    reason = "unreachable"
                unreachable.append({
                    "id": sid,
                    "url": used_url or url or "",
                    "status_code": code,
                    "fallback_attempted": source_label,
                    "cascade_trail": trail,
                    "error": err,
                    "reason": reason,
                    "current_as_of_existing": existing_caof_str,
                })
                status_dist[f"unreachable_{reason}"] += 1
                audit_lines.append(
                    f"- {sid}: HTTP {code} via {source_label} → UNREACHABLE.{reason}"
                )

    # Write contribution meta
    contrib_meta = {
        "_contribution": {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": today_iso,
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "ai_model_version": "1m-context",
            "ai_session_notes": (
                f"Wave-2 batch — closes #{ISSUE_NUMBER}. httpx HEAD checks per chunk brief "
                f"(UA={USER_AGENT}, timeout={TIMEOUT_SEC}s, retries={RETRIES}, "
                f"follow_redirects=True). DOI/PubMed cascade for 403."
            ),
            "tasktorrent_version": "2026-05-01",
            "notes_for_reviewer": (
                "Per-source upsert touches only: current_as_of, last_recency_check, "
                "recency_check_status_code. url updated only on DOI/PubMed fallback. "
                "Content/license/attribution unchanged."
            ),
        },
    }
    (out_dir / "_contribution_meta.yaml").write_text(
        yaml.safe_dump(contrib_meta, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    # Manifest
    (out_dir / "task_manifest.txt").write_text(
        "\n".join(MANIFEST) + "\n", encoding="utf-8",
    )

    # Per-source upsert sidecars
    for sid, _orig, payload, meta in upserts:
        slug = sid.replace("SRC-", "").lower().replace("-", "_")
        out_path = out_dir / f"src_{slug}.yaml"
        wrapped = dict(payload)
        wrapped["_contribution"] = meta
        out_path.write_text(
            yaml.safe_dump(wrapped, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

    # unreachable.yaml (always emit, even if empty — keeps shape stable)
    unreachable_doc = {
        "_contribution": {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": today_iso,
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "notes_for_reviewer": (
                "Report-only flag list. dead=HTTP 404 (URL gone). "
                "blocked=HTTP 403 across primary+DOI+PubMed cascade (likely publisher "
                "bot-block; real browser would succeed). no_url=record has no resolvable "
                "URL/DOI/PMID. unreachable=other network/HTTP error."
            ),
        },
        "rows": unreachable,
    }
    (out_dir / "unreachable.yaml").write_text(
        yaml.safe_dump(unreachable_doc, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    # refresh_summary.yaml
    summary = {
        "_contribution": {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": today_iso,
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
    }
    (out_dir / "refresh_summary.yaml").write_text(
        yaml.safe_dump(summary, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    # Audit log
    audit_path = out_dir / f"recency-audit-{stamp_utc}.md"
    audit_path.write_text(
        f"# Recency audit: {CHUNK_ID} ({stamp_utc})\n\n"
        f"Issue: #{ISSUE_NUMBER}\nManifest size: {len(MANIFEST)}\n"
        f"Upserts: {len(upserts)}\nUnreachable: {len(unreachable)}\n"
        f"Not found in hosted/: {len(not_found)}\n\n"
        f"## Per-source outcomes\n\n" + "\n".join(audit_lines) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(upserts)} upserts, {len(unreachable)} unreachable, "
          f"{len(not_found)} not-found to {out_dir}")
    print(f"Status distribution: {dict(status_dist)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
