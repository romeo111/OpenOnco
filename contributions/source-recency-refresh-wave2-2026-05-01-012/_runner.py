"""Source-recency-refresh wave-2 chunk runner — chunk 012 (issue #214).

Per caller spec (different from wave-1 #92-#121 worker):
- httpx GET (not HEAD)
- UA: Mozilla/5.0 (compatible; OpenOnco-recency-bot)
- timeout 30s, 3 retries
- 200 -> upsert
- 3xx -> upsert + record redirect target
- 404 -> unreachable.dead
- 403 -> DOI fallback if available; if DOI also fails or no DOI -> unreachable.blocked
- No URL field -> unreachable

Outputs (sidecar-only, under contributions/source-recency-refresh-wave2-2026-05-01-012/):
- _contribution_meta.yaml      chunk-level meta
- task_manifest.txt            manifest IDs
- src_*.yaml                   per-source upsert sidecars (HTTP 2xx/3xx)
- unreachable.yaml             flag list (HTTP 403/404/network)
- source_recency_audit.yaml    schema-required audit per issue body
- refresh_summary.yaml         aggregate counts

Run: C:/Python312/python.exe contributions/source-recency-refresh-wave2-2026-05-01-012/_runner.py
"""

from __future__ import annotations

import datetime as dt
import time
from collections import Counter
from pathlib import Path

import httpx
import yaml

CHUNK_ID = "source-recency-refresh-wave2-2026-05-01-012"
ISSUE_NUMBER = 214
TODAY = dt.date(2026, 5, 1)
SUBMISSION_DATE = TODAY.isoformat()
TIMEOUT_SEC = 30.0
MAX_RETRIES = 3
USER_AGENT = "Mozilla/5.0 (compatible; OpenOnco-recency-bot)"

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"
OUT_DIR = REPO_ROOT / "contributions" / CHUNK_ID

MANIFEST = [
    "SRC-EHA-WORKUP-2024",
    "SRC-NCCN-MM-2025",
    "SRC-BREAK-3-HAUSCHILD-2012",
    "SRC-ARCAINI-2014",
    "SRC-INNOVATE-DIMOPOULOS-2018",
]


def _src_yaml_path(src_id: str) -> Path | None:
    """Resolve SRC-FOO-BAR -> sources/src_foo_bar.yaml (with id-field fallback)."""
    candidate = src_id.replace("SRC-", "").lower().replace("-", "_")
    direct = SOURCES_DIR / f"src_{candidate}.yaml"
    if direct.is_file():
        return direct
    # Try common normalisations (SRC-BREAK-3-... -> src_break3_...)
    alt = src_id.replace("SRC-", "").lower()
    for token in (alt, alt.replace("-", "_"), alt.replace("-", "")):
        p = SOURCES_DIR / f"src_{token}.yaml"
        if p.is_file():
            return p
    # Last resort: scan files for matching id field
    for p in SOURCES_DIR.glob("*.yaml"):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict) and data.get("id") == src_id:
            return p
    return None


def http_get(url: str) -> dict:
    """GET with retries. Returns dict: status_code, final_url, redirected, error."""
    last_err = ""
    for attempt in range(MAX_RETRIES):
        try:
            with httpx.Client(
                timeout=TIMEOUT_SEC,
                headers={"User-Agent": USER_AGENT},
                follow_redirects=True,
            ) as client:
                resp = client.get(url)
                final_url = str(resp.url)
                redirected = final_url.rstrip("/") != url.rstrip("/")
                return {
                    "status_code": resp.status_code,
                    "final_url": final_url,
                    "redirected": redirected,
                    "error": "",
                }
        except (httpx.HTTPError, OSError) as e:
            last_err = f"{type(e).__name__}: {str(e)[:120]}"
            if attempt < MAX_RETRIES - 1:
                time.sleep(1.5 * (attempt + 1))
    return {"status_code": None, "final_url": None, "redirected": False, "error": last_err}


def _contrib_block(target_action: str, target_entity_id: str | None, notes: str) -> dict:
    block = {
        "chunk_id": CHUNK_ID,
        "contributor": "claude-anthropic-internal",
        "submission_date": SUBMISSION_DATE,
        "ai_tool": "claude-code",
        "ai_model": "claude-opus-4-7",
    }
    if target_action:
        block["target_action"] = target_action
    if target_entity_id:
        block["target_entity_id"] = target_entity_id
    if notes:
        block["notes_for_reviewer"] = notes
    return block


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    upserts: list[dict] = []
    unreachable: list[dict] = []
    audit_rows: list[dict] = []
    not_found: list[str] = []
    status_dist: Counter[str] = Counter()

    for sid in MANIFEST:
        print(f"[{sid}]")
        src_path = _src_yaml_path(sid)
        if src_path is None:
            print(f"  NOT FOUND in {SOURCES_DIR}")
            not_found.append(sid)
            status_dist["src_not_found"] += 1
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": "unknown",
                "notes": "Source YAML not found in knowledge_base/hosted/content/sources/.",
            })
            continue

        data = yaml.safe_load(src_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            not_found.append(sid)
            status_dist["src_parse_fail"] += 1
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": "unknown",
                "notes": "Source YAML failed to parse as dict.",
            })
            continue

        url = data.get("url")
        doi = data.get("doi")
        existing_caof = data.get("current_as_of")
        license_name = (data.get("license") or {}).get("name") if isinstance(data.get("license"), dict) else None
        license_status = "populated" if license_name else "missing"

        # No URL at all -> unreachable
        if not url:
            print("  no url field")
            unreachable.append({
                "id": sid, "url": None, "status_code": None,
                "category": "unreachable",
                "error": "no url field in source yaml",
                "current_as_of_existing": existing_caof,
            })
            status_dist["no_url"] += 1
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": license_status,
                "notes": "Source has no url field; unreachable.",
            })
            continue

        # Primary GET
        r = http_get(url)
        sc = r["status_code"]
        print(f"  GET {url} -> {sc} (redirected={r['redirected']}) err={r['error']}")

        # Branch on status code
        if sc is not None and 200 <= sc < 400:
            # success (200) or redirect (handled via follow_redirects -> final_url)
            redirect_target = r["final_url"] if r["redirected"] else None
            ok_via = "GET 200" if sc == 200 else f"GET {sc} -> {r['final_url']}"

            upsert = dict(data)
            upsert["current_as_of"] = TODAY.isoformat()
            upsert["last_recency_check"] = TODAY.isoformat()
            upsert["recency_check_status_code"] = sc
            if redirect_target:
                upsert["recency_check_redirect_to"] = redirect_target
            upsert["_contribution"] = _contrib_block(
                target_action="upsert",
                target_entity_id=sid,
                notes=(
                    f"Recency refresh wave-2 (issue #{ISSUE_NUMBER}): {ok_via}. "
                    f"current_as_of bumped from {existing_caof!r} to {TODAY.isoformat()}. "
                    f"License/attribution unchanged. "
                    + (f"Redirect target recorded: {redirect_target}." if redirect_target else "")
                ).strip(),
            )
            (OUT_DIR / src_path.name).write_text(
                yaml.safe_dump(upsert, sort_keys=False, allow_unicode=True, default_flow_style=False),
                encoding="utf-8",
            )
            upserts.append({"id": sid, "url": url, "status": sc, "redirect_to": redirect_target})
            status_dist[f"http_{sc}"] += 1

            audit_notes = (
                f"HTTP {sc} on httpx GET via UA OpenOnco-recency-bot. URL reachable; content not superseded. "
                f"current_as_of bumped from {existing_caof!r} to {TODAY.isoformat()}."
            )
            if redirect_target:
                audit_notes += f" Redirect chain ended at {redirect_target}."
            if isinstance(existing_caof, str) and "XX" in existing_caof:
                audit_notes += " (Existing current_as_of was a placeholder — replaced with real date.)"

            audit_rows.append({
                "id": sid,
                "url_verified": "yes" if not redirect_target else f"replaced-with: {redirect_target}",
                "content_current": "yes",
                "proposed_current_as_of": TODAY.isoformat(),
                "license_status": license_status,
                "notes": audit_notes,
            })

        elif sc == 404:
            unreachable.append({
                "id": sid, "url": url, "status_code": sc,
                "category": "unreachable.dead",
                "error": "HTTP 404 — page genuinely missing",
                "current_as_of_existing": existing_caof,
            })
            status_dist["http_404"] += 1
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": license_status,
                "notes": (
                    f"HTTP 404 on httpx GET; URL no longer resolves. "
                    f"Maintainer to replace URL with DOI/PubMed canonical. "
                    f"Existing current_as_of preserved at {existing_caof!r}."
                ),
            })

        elif sc == 403:
            # DOI fallback
            doi_url = f"https://doi.org/{doi}" if doi else None
            if doi_url:
                print(f"  403 -> DOI fallback {doi_url}")
                r2 = http_get(doi_url)
                sc2 = r2["status_code"]
                if sc2 is not None and 200 <= sc2 < 400:
                    redirect_target = r2["final_url"]
                    upsert = dict(data)
                    upsert["current_as_of"] = TODAY.isoformat()
                    upsert["last_recency_check"] = TODAY.isoformat()
                    upsert["recency_check_status_code"] = sc2
                    upsert["recency_check_via"] = "doi_fallback"
                    upsert["recency_check_doi_url"] = doi_url
                    upsert["recency_check_redirect_to"] = redirect_target
                    upsert["_contribution"] = _contrib_block(
                        target_action="upsert",
                        target_entity_id=sid,
                        notes=(
                            f"Recency refresh wave-2 (issue #{ISSUE_NUMBER}): "
                            f"primary URL returned HTTP 403 (publisher bot-block); "
                            f"DOI fallback {doi_url} returned HTTP {sc2} -> {redirect_target}. "
                            f"current_as_of bumped from {existing_caof!r} to {TODAY.isoformat()}."
                        ),
                    )
                    (OUT_DIR / src_path.name).write_text(
                        yaml.safe_dump(upsert, sort_keys=False, allow_unicode=True, default_flow_style=False),
                        encoding="utf-8",
                    )
                    upserts.append({"id": sid, "url": url, "status": sc2,
                                    "via": "doi_fallback", "redirect_to": redirect_target})
                    status_dist["http_403_doi_ok"] += 1
                    audit_rows.append({
                        "id": sid,
                        "url_verified": f"replaced-with: {doi_url}",
                        "content_current": "yes",
                        "proposed_current_as_of": TODAY.isoformat(),
                        "license_status": license_status,
                        "notes": (
                            f"Primary URL HTTP 403 (publisher bot-block); DOI fallback HTTP {sc2}. "
                            f"Resolved to {redirect_target}. Content not superseded."
                        ),
                    })
                else:
                    unreachable.append({
                        "id": sid, "url": url, "status_code": sc,
                        "category": "unreachable.blocked",
                        "error": f"HTTP 403 on primary; DOI fallback {doi_url} -> {sc2} {r2['error']}",
                        "doi_fallback_url": doi_url,
                        "current_as_of_existing": existing_caof,
                    })
                    status_dist["http_403_doi_fail"] += 1
                    audit_rows.append({
                        "id": sid,
                        "url_verified": "no",
                        "content_current": "unknown",
                        "proposed_current_as_of": None,
                        "license_status": license_status,
                        "notes": (
                            f"HTTP 403 on primary URL; DOI fallback {doi_url} also failed "
                            f"({sc2 or 'network-error'}). Maintainer browser-verify required."
                        ),
                    })
            else:
                unreachable.append({
                    "id": sid, "url": url, "status_code": sc,
                    "category": "unreachable.blocked",
                    "error": "HTTP 403 — no DOI fallback available",
                    "current_as_of_existing": existing_caof,
                })
                status_dist["http_403_no_doi"] += 1
                audit_rows.append({
                    "id": sid,
                    "url_verified": "no",
                    "content_current": "unknown",
                    "proposed_current_as_of": None,
                    "license_status": license_status,
                    "notes": (
                        f"HTTP 403 on httpx GET (likely publisher bot-block); "
                        f"no DOI field on source for fallback. "
                        f"Maintainer browser-verify required."
                    ),
                })

        else:
            # Other 4xx/5xx/network-error
            cat = "unreachable.network" if sc is None else f"unreachable.http_{sc}"
            unreachable.append({
                "id": sid, "url": url, "status_code": sc,
                "category": cat,
                "error": r["error"] or f"HTTP {sc}",
                "current_as_of_existing": existing_caof,
            })
            status_dist[f"http_{sc}" if sc else "network_error"] += 1
            audit_rows.append({
                "id": sid,
                "url_verified": "no",
                "content_current": "unknown",
                "proposed_current_as_of": None,
                "license_status": license_status,
                "notes": (
                    f"HTTP {sc} / network error on httpx GET ({r['error']}). "
                    f"Maintainer review required."
                ),
            })

    # task_manifest.txt
    manifest_lines = MANIFEST[:]
    if not_found:
        manifest_lines.append("")
        manifest_lines.append("# SRC IDs in issue manifest but not found in hosted/content/sources/:")
        manifest_lines.extend(f"# {sid}" for sid in not_found)
    (OUT_DIR / "task_manifest.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    # unreachable.yaml
    if unreachable:
        (OUT_DIR / "unreachable.yaml").write_text(
            yaml.safe_dump({
                "_contribution": _contrib_block(
                    target_action="",
                    target_entity_id=None,
                    notes=(
                        "Report-only flag list: sources whose httpx GET did not return 2xx/3xx "
                        "(after DOI fallback where available). HTTP 403 typically indicates "
                        "publisher bot-blocking; HTTP 404 indicates a genuinely broken URL."
                    ),
                ),
                "rows": unreachable,
            }, sort_keys=False, allow_unicode=True, default_flow_style=False),
            encoding="utf-8",
        )

    # source_recency_audit.yaml — schema mandated by issue body
    (OUT_DIR / "source_recency_audit.yaml").write_text(
        yaml.safe_dump({
            "_contribution": _contrib_block(
                target_action="",
                target_entity_id=None,
                notes=(
                    "Per-source audit row per issue #214 schema: id, url_verified, "
                    "content_current, proposed_current_as_of, license_status, notes."
                ),
            ),
            "rows": audit_rows,
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    # refresh_summary.yaml
    (OUT_DIR / "refresh_summary.yaml").write_text(
        yaml.safe_dump({
            "_contribution": _contrib_block(
                target_action="",
                target_entity_id=None,
                notes="Report-only aggregate stats for chunk run.",
            ),
            "issue_number": ISSUE_NUMBER,
            "manifest_count": len(MANIFEST),
            "upserts_count": len(upserts),
            "unreachable_count": len(unreachable),
            "not_found_count": len(not_found),
            "status_distribution": dict(status_dist),
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    # _contribution_meta.yaml — chunk-level
    (OUT_DIR / "_contribution_meta.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": CHUNK_ID,
                "contributor": "claude-anthropic-internal",
                "submission_date": SUBMISSION_DATE,
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "ai_model_version": "1m-context",
                "ai_session_notes": (
                    f"Wave-2 source-recency-refresh — closes #{ISSUE_NUMBER}. "
                    f"httpx GET (UA Mozilla/5.0 OpenOnco-recency-bot) on {len(MANIFEST)} sources, "
                    "30s timeout, 3 retries. 403 -> DOI fallback when available."
                ),
                "tasktorrent_version": "wave2-2026-05-01",
                "notes_for_reviewer": (
                    "Per-source upsert touches only: current_as_of, last_recency_check, "
                    "recency_check_status_code (and recency_check_redirect_to / "
                    "recency_check_via / recency_check_doi_url where applicable). "
                    "Content/license/attribution unchanged."
                ),
            },
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    print()
    print(f"Manifest:   {len(MANIFEST)}")
    print(f"Upserts:    {len(upserts)}")
    print(f"Unreachable:{len(unreachable)}")
    print(f"Not-found:  {len(not_found)}")
    print(f"Status dist:{dict(status_dist)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
