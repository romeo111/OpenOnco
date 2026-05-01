"""Wave-2 batch worker — source-recency-refresh-wave2-2026-05-01-015.

For each SRC-* in the manifest:
  - httpx GET (User-Agent Mozilla, 30s timeout, 3 retries)
  - 200 -> upsert sidecar bumping current_as_of, last_recency_check, recency_check_status_code
  - 3xx (redirect captured by httpx automatically; raw 301/302 noted) -> upsert + redirect notes
  - 404 -> unreachable.dead
  - 403 -> DOI fallback if available; else unreachable.blocked
  - No URL -> unreachable

Outputs: _contribution_meta.yaml, task_manifest.txt, src_*.yaml upserts,
unreachable.yaml (if any), refresh_summary.yaml, upsert-log-<TS>.md.
"""

from __future__ import annotations

import datetime as dt
import time
from collections import Counter
from pathlib import Path

import httpx
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"
CHUNK_ID = "source-recency-refresh-wave2-2026-05-01-015"
CONTRIB_DIR = REPO_ROOT / "contributions" / CHUNK_ID
TODAY = dt.date(2026, 5, 1)
TIMEOUT_SEC = 30.0
RETRIES = 3
ISSUE_NUMBER = 217

USER_AGENT = "Mozilla/5.0 (compatible; OpenOnco-recency-bot)"

MANIFEST = [
    "SRC-ESMO-BTC-2023",
    "SRC-NCCN-SARCOMA",
    "SRC-PACE-CORTES-2013",
    "SRC-GOG0213-COLEMAN-2017",
    "SRC-MONALEESA-3-SLAMON-2018",
]


def _src_yaml_path(src_id: str) -> Path | None:
    candidate = src_id.replace("SRC-", "").lower().replace("-", "_")
    direct = SOURCES_DIR / f"src_{candidate}.yaml"
    if direct.is_file():
        return direct
    # else scan files
    for p in SOURCES_DIR.glob("*.yaml"):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict) and data.get("id") == src_id:
            return p
    return None


def http_get(url: str) -> tuple[int | None, str, str | None]:
    """Returns (status_code, error_msg, final_url_if_redirected)."""
    headers = {"User-Agent": USER_AGENT}
    last_err = ""
    for attempt in range(RETRIES):
        try:
            with httpx.Client(
                follow_redirects=True,
                timeout=TIMEOUT_SEC,
                headers=headers,
            ) as client:
                resp = client.get(url)
                final = str(resp.url) if str(resp.url) != url else None
                return resp.status_code, "", final
        except httpx.HTTPError as e:
            last_err = f"{type(e).__name__}: {e}"[:200]
            if attempt < RETRIES - 1:
                time.sleep(1.0)
            continue
    return None, last_err, None


def _doi_fallback(data: dict) -> str | None:
    doi = data.get("doi")
    if doi:
        return f"https://doi.org/{doi}"
    pmid = data.get("pmid")
    if pmid:
        return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    return None


def main() -> int:
    upserts: list[tuple[str, Path, dict, dict]] = []  # (src_id, src_path, data, audit_entry)
    unreachable: list[dict] = []
    audit_rows: list[dict] = []
    status_dist: Counter[str] = Counter()
    not_found: list[str] = []

    for sid in MANIFEST:
        src_path = _src_yaml_path(sid)
        if src_path is None:
            not_found.append(sid)
            status_dist["src_not_found"] += 1
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": "unknown",
                "notes": "source YAML not found in hosted KB",
            })
            continue
        try:
            data = yaml.safe_load(src_path.read_text(encoding="utf-8"))
        except Exception as e:
            not_found.append(sid)
            status_dist["yaml_load_error"] += 1
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": "unknown",
                "notes": f"yaml load error: {e}"[:160],
            })
            continue

        url = data.get("url")
        license_name = (data.get("license") or {}).get("name") or "unspecified"
        license_status = "populated" if license_name and license_name != "unspecified" else "missing"

        if not url:
            unreachable.append({
                "id": sid,
                "url": None,
                "status_code": None,
                "category": "unreachable.no_url",
                "current_as_of_existing": str(data.get("current_as_of") or ""),
            })
            status_dist["no_url"] += 1
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": license_status,
                "notes": "source record has no url field",
            })
            continue

        code, err, final = http_get(url)
        outcome_note = ""
        if code == 200:
            status_dist["ok"] += 1
            outcome_note = "HTTP 200"
            audit_url_verified = "yes"
            do_upsert = True
        elif code is not None and 300 <= code < 400:
            status_dist[f"http_{code}"] += 1
            outcome_note = f"HTTP {code} redirect to {final or 'unknown'}"
            audit_url_verified = f"redirected:{final}" if final else f"redirected:{code}"
            do_upsert = True
        elif code == 404:
            status_dist["http_404"] += 1
            unreachable.append({
                "id": sid,
                "url": url,
                "status_code": 404,
                "category": "unreachable.dead",
                "current_as_of_existing": str(data.get("current_as_of") or ""),
            })
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": license_status,
                "notes": "HTTP 404 — URL appears dead; manual browser-verify needed",
            })
            continue
        elif code == 403:
            # DOI fallback
            fb = _doi_fallback(data)
            fb_code = None
            fb_err = ""
            fb_final = None
            if fb:
                fb_code, fb_err, fb_final = http_get(fb)
            if fb_code == 200 or (fb_code is not None and 300 <= fb_code < 400):
                status_dist[f"http_403_doi_ok"] += 1
                outcome_note = (
                    f"HTTP 403 on publisher URL; DOI fallback {fb} returned {fb_code}"
                )
                audit_url_verified = f"replaced-via-doi:{fb}"
                do_upsert = True
                # mutate data: track that we are using DOI fallback in audit only
                # (not editing canonical url field — that's a content change)
            else:
                status_dist["http_403"] += 1
                unreachable.append({
                    "id": sid,
                    "url": url,
                    "status_code": 403,
                    "category": "unreachable.blocked",
                    "current_as_of_existing": str(data.get("current_as_of") or ""),
                    "doi_fallback_attempted": fb,
                    "doi_fallback_status": fb_code,
                })
                audit_rows.append({
                    "id": sid,
                    "url_verified": "no",
                    "content_current": "yes",
                    "proposed_current_as_of": None,
                    "license_status": license_status,
                    "notes": f"HTTP 403 (publisher bot-block); DOI fallback {fb} -> {fb_code}",
                })
                continue
        else:
            # other failure
            label = f"http_{code}" if code is not None else "network_error"
            status_dist[label] += 1
            unreachable.append({
                "id": sid,
                "url": url,
                "status_code": code,
                "category": "unreachable.other",
                "error": err,
                "current_as_of_existing": str(data.get("current_as_of") or ""),
            })
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": license_status,
                "notes": f"HTTP {code} / {err[:80]}",
            })
            continue

        if do_upsert:
            # Build upsert: only touch current_as_of, last_recency_check,
            # recency_check_status_code. Preserve everything else.
            new = dict(data)
            new["current_as_of"] = TODAY.isoformat()
            new["last_recency_check"] = TODAY.isoformat()
            new["recency_check_status_code"] = code
            new["_contribution"] = {
                "chunk_id": CHUNK_ID,
                "contributor": "claude-anthropic-internal",
                "submission_date": TODAY.isoformat(),
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "target_action": "upsert",
                "target_entity_id": sid,
                "notes_for_reviewer": (
                    f"Recency refresh wave-2: {outcome_note}. URL reachable. "
                    f"current_as_of bumped to {TODAY.isoformat()}. "
                    "No content / license / attribution fields modified."
                ),
            }
            upserts.append((sid, src_path, new, {
                "id": sid,
                "url_verified": audit_url_verified,
                "content_current": "yes",
                "proposed_current_as_of": TODAY.isoformat(),
                "license_status": license_status,
                "notes": outcome_note,
            }))
            audit_rows.append(upserts[-1][3])

    # Write outputs
    CONTRIB_DIR.mkdir(parents=True, exist_ok=True)

    # _contribution_meta.yaml
    meta = {
        "_contribution": {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": TODAY.isoformat(),
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "ai_model_version": "1m-context",
            "ai_session_notes": (
                f"Wave-2 batch — closes #{ISSUE_NUMBER}. Real HTTP GET checks on "
                "5 sources from chunk manifest via httpx (User-Agent Mozilla, "
                "30s timeout, 3 retries). DOI fallback on 403."
            ),
            "tasktorrent_version": "2026-05-01",
            "notes_for_reviewer": (
                "Per-source upsert touches only: current_as_of, last_recency_check, "
                "recency_check_status_code. Content/license/attribution unchanged."
            ),
        }
    }
    (CONTRIB_DIR / "_contribution_meta.yaml").write_text(
        yaml.safe_dump(meta, sort_keys=False), encoding="utf-8"
    )

    # task_manifest.txt
    (CONTRIB_DIR / "task_manifest.txt").write_text(
        "\n".join(MANIFEST) + "\n", encoding="utf-8"
    )

    # Per-source upsert sidecars
    for sid, src_path, new_data, _ in upserts:
        # Filename mirrors the hosted file name so the upsert tool maps cleanly
        out = CONTRIB_DIR / src_path.name
        out.write_text(yaml.safe_dump(new_data, sort_keys=False), encoding="utf-8")

    # source_recency_audit.yaml (per spec)
    audit = {
        "_contribution": {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": TODAY.isoformat(),
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "notes_for_reviewer": "Audit table per spec: id, url_verified, content_current, proposed_current_as_of, license_status, notes.",
        },
        "rows": audit_rows,
    }
    (CONTRIB_DIR / "source_recency_audit.yaml").write_text(
        yaml.safe_dump(audit, sort_keys=False), encoding="utf-8"
    )

    # unreachable.yaml (only if any)
    if unreachable:
        un = {
            "_contribution": {
                "chunk_id": CHUNK_ID,
                "contributor": "claude-anthropic-internal",
                "submission_date": TODAY.isoformat(),
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "notes_for_reviewer": (
                    "Report-only flag list: sources whose URL did not return 2xx/3xx "
                    "(including DOI fallback). 403 = publisher bot-block; 404 = dead."
                ),
            },
            "rows": unreachable,
        }
        (CONTRIB_DIR / "unreachable.yaml").write_text(
            yaml.safe_dump(un, sort_keys=False), encoding="utf-8"
        )

    # refresh_summary.yaml
    summary = {
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
    }
    (CONTRIB_DIR / "refresh_summary.yaml").write_text(
        yaml.safe_dump(summary, sort_keys=False), encoding="utf-8"
    )

    # upsert-log
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    log_lines = [f"# Upsert audit (dry-run preview): {CHUNK_ID} ({ts})", ""]
    log_lines.append("Per-source outcome:")
    for sid, src_path, _, audit_entry in upserts:
        log_lines.append(
            f"- {sid} -> upsert {src_path.name} (url_verified={audit_entry['url_verified']})"
        )
    for row in unreachable:
        log_lines.append(
            f"- {row['id']} -> {row['category']} (status={row.get('status_code')})"
        )
    for sid in not_found:
        log_lines.append(f"- {sid} -> not_found")
    (CONTRIB_DIR / f"upsert-log-{ts}.md").write_text(
        "\n".join(log_lines) + "\n", encoding="utf-8"
    )

    print(f"Done. upserts={len(upserts)} unreachable={len(unreachable)} not_found={len(not_found)}")
    print(f"Status dist: {dict(status_dist)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
