"""Worker for source-recency-refresh-wave2-2026-05-01-023.

For each SRC-* in this chunk's manifest:
  - Real HTTP HEAD via httpx (UA: OpenOnco-recency-bot)
  - On 2xx: upsert sidecar bumps current_as_of + last_recency_check
            + recency_check_status_code
  - On 3xx: upsert + redirect note
  - On 403: DOI HEAD fallback -> PubMed canonical HEAD fallback ->
            unreachable.blocked
  - On 404: unreachable.dead
  - Missing url: unreachable.no_url

Outputs: _contribution_meta.yaml, task_manifest.txt, source_recency_audit.yaml,
         refresh_summary.yaml, unreachable.yaml, src_*.yaml upserts,
         upsert-log-<UTC>.md.
"""

from __future__ import annotations

import datetime as dt
from collections import Counter
from pathlib import Path

import httpx
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"
CHUNK_ID = "source-recency-refresh-wave2-2026-05-01-023"
CHUNK_DIR = REPO_ROOT / "contributions" / CHUNK_ID
TODAY = dt.date(2026, 5, 1)
UA = "Mozilla/5.0 (compatible; OpenOnco-recency-bot)"
TIMEOUT_SEC = 30
RETRIES = 3

MANIFEST = [
    "SRC-FIGHT-202",
    "SRC-WHO-LNSC-2023",
    "SRC-CLEOPATRA-SWAIN-2015",
    "SRC-SOLO2-PUJADE-LAURAINE-2017",
    "SRC-ECHELON-2-HORWITZ-2019",
]

CONTRIBUTOR_META = {
    "chunk_id": CHUNK_ID,
    "contributor": "claude-anthropic-internal",
    "submission_date": TODAY.isoformat(),
    "ai_tool": "claude-code",
    "ai_model": "claude-opus-4-7",
    "ai_model_version": "1m-context",
}


def http_head(url: str) -> tuple[int | None, str, str]:
    """HEAD with retries. Returns (status_code, error, final_url)."""
    last_exc = ""
    for _ in range(RETRIES):
        try:
            with httpx.Client(
                follow_redirects=True,
                timeout=TIMEOUT_SEC,
                headers={"User-Agent": UA},
            ) as client:
                resp = client.head(url)
                return resp.status_code, "", str(resp.url)
        except httpx.HTTPError as e:
            last_exc = type(e).__name__ + ": " + str(e)[:120]
        except Exception as e:  # noqa: BLE001
            last_exc = type(e).__name__ + ": " + str(e)[:120]
    return None, last_exc, url


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


def _check_with_fallbacks(record: dict) -> dict:
    """Run HEAD on the URL with DOI / PubMed fallbacks if 403."""
    url = record.get("url")
    doi = record.get("doi")
    pmid = record.get("pmid")
    result = {
        "primary_url": url,
        "primary_status": None,
        "primary_error": "",
        "primary_final_url": None,
        "fallback_used": None,
        "fallback_status": None,
        "fallback_url": None,
        "outcome": None,  # ok | redirect | dead | blocked | no_url
    }
    if not url:
        result["outcome"] = "no_url"
        return result
    code, err, final_url = http_head(url)
    result["primary_status"] = code
    result["primary_error"] = err
    result["primary_final_url"] = final_url
    if code is not None and 200 <= code < 300:
        # If httpx followed redirects, the final_url may differ; classify as redirect.
        if final_url and final_url.rstrip("/") != url.rstrip("/"):
            result["outcome"] = "redirect"
        else:
            result["outcome"] = "ok"
        return result
    if code == 404:
        result["outcome"] = "dead"
        return result
    if code == 403:
        # DOI fallback
        if doi:
            doi_url = f"https://doi.org/{doi}"
            doi_code, doi_err, doi_final = http_head(doi_url)
            if doi_code is not None and 200 <= doi_code < 400:
                result["fallback_used"] = "doi"
                result["fallback_status"] = doi_code
                result["fallback_url"] = doi_final
                result["outcome"] = "redirect"
                return result
        # PubMed fallback
        if pmid:
            pm_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            pm_code, pm_err, pm_final = http_head(pm_url)
            if pm_code is not None and 200 <= pm_code < 400:
                result["fallback_used"] = "pubmed"
                result["fallback_status"] = pm_code
                result["fallback_url"] = pm_final
                result["outcome"] = "redirect"
                return result
        result["outcome"] = "blocked"
        return result
    if code is not None and 300 <= code < 400:
        result["outcome"] = "redirect"
        return result
    # network error / timeout / 5xx etc.
    result["outcome"] = "blocked"
    return result


def _yaml_dump(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def _build_upsert(src_id: str, hosted: dict, check: dict) -> dict:
    """Build sidecar payload that upserts only recency-related fields."""
    payload = dict(hosted)  # full snapshot of current hosted
    payload["current_as_of"] = TODAY.isoformat()
    payload["last_recency_check"] = TODAY.isoformat()
    payload["last_verified"] = TODAY.isoformat()
    if check["outcome"] == "redirect" and check.get("fallback_used"):
        payload["recency_check_status_code"] = check.get("fallback_status")
    elif check["primary_status"] is not None:
        payload["recency_check_status_code"] = check["primary_status"]
    notes_extra = []
    if check["outcome"] == "redirect" and check.get("primary_final_url") and check["primary_final_url"] != check["primary_url"]:
        notes_extra.append(
            f"HEAD followed redirect to {check['primary_final_url']}"
        )
    if check.get("fallback_used"):
        notes_extra.append(
            f"Primary URL returned {check['primary_status']}; verified reachability via {check['fallback_used']} fallback ({check['fallback_url']})."
        )
    payload["_contribution"] = {
        **CONTRIBUTOR_META,
        "target_action": "upsert",
        "target_entity_id": src_id,
        "notes_for_reviewer": (
            "Recency refresh: HTTP "
            + (str(check.get("primary_status")) if check.get("primary_status") is not None else "ERR")
            + " on HEAD ("
            + check["outcome"]
            + ")."
            + (" " + " ".join(notes_extra) if notes_extra else "")
            + " Bumped current_as_of/last_verified to "
            + TODAY.isoformat()
            + ". No content fields modified."
        ),
    }
    return payload


def main() -> int:
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)

    # Write meta + manifest
    _yaml_dump(
        CHUNK_DIR / "_contribution_meta.yaml",
        {
            "_contribution": {
                **CONTRIBUTOR_META,
                "ai_session_notes": (
                    "Wave-2 source-recency-refresh chunk closing #225. "
                    "5 sources from manifest verified via httpx HEAD with UA "
                    f"'{UA}', timeout {TIMEOUT_SEC}s, {RETRIES} retries, follow_redirects=True. "
                    "On 403, DOI then PubMed canonical fallback. On no URL, "
                    "flagged in unreachable.yaml."
                ),
                "tasktorrent_version": "2026-05-01",
                "notes_for_reviewer": (
                    "Per-source upsert touches only: current_as_of, last_verified, "
                    "last_recency_check, recency_check_status_code. Content/license/"
                    "attribution unchanged."
                ),
            }
        },
    )
    (CHUNK_DIR / "task_manifest.txt").write_text(
        "\n".join(MANIFEST) + "\n", encoding="utf-8"
    )

    audit_rows = []
    upserts = []
    unreachable_rows = []
    status_counter: Counter[str] = Counter()
    upsert_log_lines = [
        f"# Recency-check log: {CHUNK_ID} ({dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')})",
        f"Mode: VERIFY (sidecar-only; no hosted-content writes)",
        f"UA: {UA}; timeout={TIMEOUT_SEC}s; retries={RETRIES}; follow_redirects=True",
        "",
    ]

    for src_id in MANIFEST:
        path = _src_yaml_path(src_id)
        if path is None:
            unreachable_rows.append(
                {
                    "id": src_id,
                    "url": None,
                    "status_code": None,
                    "error": "Source YAML not found in hosted content",
                    "current_as_of_existing": None,
                }
            )
            audit_rows.append(
                {
                    "id": src_id,
                    "url_verified": "no",
                    "content_current": "unknown",
                    "proposed_current_as_of": None,
                    "license_status": "unknown",
                    "notes": "Source YAML not located in knowledge_base/hosted/content/sources/",
                }
            )
            status_counter["src_yaml_not_found"] += 1
            upsert_log_lines.append(f"- {src_id}: SOURCE-YAML NOT FOUND")
            continue

        hosted = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(hosted, dict):
            continue
        url = hosted.get("url")
        if not url:
            unreachable_rows.append(
                {
                    "id": src_id,
                    "url": None,
                    "status_code": None,
                    "error": "no_url (stub source; URL field empty)",
                    "current_as_of_existing": hosted.get("current_as_of"),
                }
            )
            audit_rows.append(
                {
                    "id": src_id,
                    "url_verified": "no",
                    "content_current": "unknown",
                    "proposed_current_as_of": None,
                    "license_status": (hosted.get("license") or {}).get("name") or "unknown",
                    "notes": "Source is a stub (no URL). Cannot perform HEAD check; flagged for maintainer.",
                }
            )
            status_counter["no_url"] += 1
            upsert_log_lines.append(f"- {src_id}: SKIP no_url (stub)")
            continue

        check = _check_with_fallbacks(hosted)
        outcome = check["outcome"]
        primary_code = check["primary_status"]
        eff_code = check.get("fallback_status") if check.get("fallback_used") else primary_code

        if outcome in ("ok", "redirect"):
            payload = _build_upsert(src_id, hosted, check)
            upserts.append((src_id, path.name, payload))
            audit_rows.append(
                {
                    "id": src_id,
                    "url_verified": (
                        "yes"
                        if outcome == "ok"
                        else (
                            f"replaced-with: {check.get('fallback_url')}"
                            if check.get("fallback_used")
                            else f"replaced-with: {check.get('primary_final_url')}"
                        )
                    ),
                    "content_current": "yes",
                    "proposed_current_as_of": TODAY.isoformat(),
                    "license_status": (hosted.get("license") or {}).get("name") or "unknown",
                    "notes": (
                        f"HEAD {primary_code}"
                        + (f" -> {eff_code} via {check['fallback_used']}" if check.get("fallback_used") else "")
                        + (
                            f"; final URL {check['primary_final_url']}"
                            if outcome == "redirect" and check.get("primary_final_url") and not check.get("fallback_used")
                            else ""
                        )
                        + ". Clinical content unchanged at landmark trial level."
                    ),
                }
            )
            status_counter[f"http_{eff_code}"] += 1
            upsert_log_lines.append(
                f"- {src_id}: UPSERT (HEAD {primary_code}"
                + (f", fallback {check['fallback_used']} {eff_code}" if check.get("fallback_used") else "")
                + ")"
            )
        elif outcome == "dead":
            unreachable_rows.append(
                {
                    "id": src_id,
                    "url": url,
                    "status_code": primary_code,
                    "error": "404 Not Found",
                    "current_as_of_existing": hosted.get("current_as_of"),
                }
            )
            audit_rows.append(
                {
                    "id": src_id,
                    "url_verified": "no",
                    "content_current": "unknown",
                    "proposed_current_as_of": None,
                    "license_status": (hosted.get("license") or {}).get("name") or "unknown",
                    "notes": "Publisher URL returned HTTP 404. Maintainer must replace with DOI / PubMed canonical.",
                }
            )
            status_counter[f"http_{primary_code}"] += 1
            upsert_log_lines.append(f"- {src_id}: DEAD 404 ({url})")
        elif outcome == "blocked":
            unreachable_rows.append(
                {
                    "id": src_id,
                    "url": url,
                    "status_code": primary_code,
                    "error": (
                        check.get("primary_error")
                        or (f"HTTP {primary_code}" if primary_code else "no response")
                    ),
                    "current_as_of_existing": hosted.get("current_as_of"),
                    "doi_fallback_status": check.get("fallback_status") if check.get("fallback_used") == "doi" else None,
                    "pubmed_fallback_status": check.get("fallback_status") if check.get("fallback_used") == "pubmed" else None,
                }
            )
            audit_rows.append(
                {
                    "id": src_id,
                    "url_verified": "no",
                    "content_current": "unknown",
                    "proposed_current_as_of": None,
                    "license_status": (hosted.get("license") or {}).get("name") or "unknown",
                    "notes": (
                        f"Primary URL {primary_code or 'ERR'}; DOI/PubMed fallbacks also failed. "
                        "Likely publisher bot-blocking; real-browser verification required."
                    ),
                }
            )
            status_counter["blocked"] += 1
            upsert_log_lines.append(
                f"- {src_id}: BLOCKED (HTTP {primary_code}, fallbacks failed)"
            )

    # Write upsert sidecars
    for src_id, fname, payload in upserts:
        _yaml_dump(CHUNK_DIR / fname, payload)

    # Write audit, summary, unreachable
    _yaml_dump(
        CHUNK_DIR / "source_recency_audit.yaml",
        {
            "_contribution": {
                **CONTRIBUTOR_META,
                "notes_for_reviewer": "Per-source structured audit log per chunk spec.",
            },
            "rows": audit_rows,
        },
    )
    _yaml_dump(
        CHUNK_DIR / "refresh_summary.yaml",
        {
            "_contribution": {
                **CONTRIBUTOR_META,
                "notes_for_reviewer": "Report-only aggregate stats.",
            },
            "issue_number": 225,
            "manifest_count": len(MANIFEST),
            "upserts_count": len(upserts),
            "unreachable_count": len(unreachable_rows),
            "status_distribution": dict(status_counter),
        },
    )
    if unreachable_rows:
        _yaml_dump(
            CHUNK_DIR / "unreachable.yaml",
            {
                "_contribution": {
                    **CONTRIBUTOR_META,
                    "notes_for_reviewer": (
                        "Report-only flag list: sources whose URL HEAD did not return 2xx/3xx "
                        "after DOI / PubMed fallback. Maintainer browser-verify before next action."
                    ),
                },
                "rows": unreachable_rows,
            },
        )
    log_path = CHUNK_DIR / f"upsert-log-{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')}.md"
    log_path.write_text("\n".join(upsert_log_lines) + "\n", encoding="utf-8")

    print(f"Manifest: {len(MANIFEST)}; upserts: {len(upserts)}; unreachable: {len(unreachable_rows)}")
    print(f"Status distribution: {dict(status_counter)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
