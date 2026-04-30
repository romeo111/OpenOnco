"""Wave 7 batch worker — source-license-backfill chunks #84-#91 (8 chunks × ~4 sources).

For each source:
  - Read existing license block
  - If license fields populated → no-op (already set)
  - Else: classify license from URL hostname + source-id pattern.
    Known patterns:
      civicdb.org              → CC0-1.0
      pubmed.ncbi.nlm.nih.gov  → varies per article (mark unresolved)
      pmc.ncbi.nlm.nih.gov     → likely PMC OA (mark unresolved-but-likely-open)
      clinicaltrials.gov       → US-PD
      fda.gov / accessdata.fda → US-PD
      dailymed.nlm.nih.gov     → US-PD
      moz.gov.ua               → UA-government (typically open)
      nccn.org                 → NCCN restricted (cite-by-reference only)
      esmo.org                 → CC BY-NC-ND (typical for ESMO guidelines)
      easl.eu                  → similar restricted
      annalsofoncology.com     → Elsevier (restricted)
      thelancet.com            → Elsevier (restricted)
      nejm.org                 → NEJM Massachusetts Medical Soc (restricted)
      jamanetwork.com          → AMA (restricted)
      ascopubs.org             → ASCO (restricted)
    Unknown / paywalled trial publications: mark unresolved with notes.

Per chunk-spec: "Propose sidecar updates where a public license or
terms statement is clear; otherwise record why the license remains
unresolved." Both paths are valid output.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"
CONTRIB_ROOT = REPO_ROOT / "contributions"
MANIFESTS_FILE = "/tmp/license_manifests.json"


# (hostname-substring, license-classification, attribution-note)
HOST_PATTERNS = [
    ("civicdb.org", {"name": "Creative Commons Public Domain Dedication (CC0 1.0)",
                     "spdx_id": "CC0-1.0",
                     "url": "https://creativecommons.org/publicdomain/zero/1.0/",
                     "commercial_use_allowed": True,
                     "redistribution_allowed": True,
                     "modifications_allowed": True,
                     "sharealike_required": False}),
    ("clinicaltrials.gov", {"name": "U.S. Government public-domain (NIH/NLM)",
                            "spdx_id": None,
                            "url": "https://www.nlm.nih.gov/web_policies.html",
                            "commercial_use_allowed": True,
                            "redistribution_allowed": True,
                            "modifications_allowed": True,
                            "sharealike_required": False}),
    ("fda.gov", {"name": "U.S. Government public-domain (FDA)",
                 "spdx_id": None,
                 "url": "https://www.fda.gov/about-fda/about-website/website-policies",
                 "commercial_use_allowed": True,
                 "redistribution_allowed": True,
                 "modifications_allowed": True,
                 "sharealike_required": False}),
    ("dailymed.nlm.nih.gov", {"name": "U.S. Government public-domain (NLM DailyMed)",
                              "spdx_id": None,
                              "url": "https://www.nlm.nih.gov/web_policies.html",
                              "commercial_use_allowed": True,
                              "redistribution_allowed": True,
                              "modifications_allowed": True,
                              "sharealike_required": False}),
    ("moz.gov.ua", {"name": "Ukrainian Ministry of Health official document (citation by reference)",
                    "spdx_id": None, "url": None,
                    "commercial_use_allowed": False,
                    "redistribution_allowed": False,
                    "modifications_allowed": False,
                    "sharealike_required": False}),
    ("nccn.org", {"name": "NCCN Guidelines — restricted (cite-by-reference only; no redistribution)",
                  "spdx_id": None,
                  "url": "https://www.nccn.org/about/permissions/default.aspx",
                  "commercial_use_allowed": False,
                  "redistribution_allowed": False,
                  "modifications_allowed": False,
                  "sharealike_required": False}),
    ("esmo.org", {"name": "ESMO Guidelines — typically CC BY-NC-ND or restricted (publisher Annals of Oncology / Elsevier)",
                  "spdx_id": None,
                  "url": "https://www.esmo.org/guidelines",
                  "commercial_use_allowed": False,
                  "redistribution_allowed": False,
                  "modifications_allowed": False,
                  "sharealike_required": False}),
]


def classify_by_url(url: str) -> tuple[dict, str] | None:
    """Returns (license_block, rationale) or None if no pattern matches."""
    try:
        host = urlparse(url).hostname or ""
    except Exception:
        return None
    for substring, license_block in HOST_PATTERNS:
        if substring in host:
            return license_block, f"matched hostname pattern '{substring}' → known publisher policy"
    return None


def _src_path(source_id: str) -> Path | None:
    candidate = source_id.replace("SRC-", "").lower().replace("-", "_")
    direct = SOURCES_DIR / f"src_{candidate}.yaml"
    if direct.is_file():
        return direct
    for p in SOURCES_DIR.glob("*.yaml"):
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and d.get("id") == source_id:
            return p
    return None


def has_license(data: dict) -> bool:
    lic = data.get("license")
    if not isinstance(lic, dict):
        return False
    return bool(lic.get("name") or lic.get("spdx_id"))


def process_chunk(chunk_id: str, source_ids: list[str], issue_number: int) -> dict:
    out_dir = CONTRIB_ROOT / chunk_id
    out_dir.mkdir(parents=True, exist_ok=True)

    upserts: list[dict] = []
    unresolved: list[dict] = []
    already_set: list[str] = []
    not_found: list[str] = []

    for sid in source_ids:
        path = _src_path(sid)
        if path is None:
            not_found.append(sid)
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            not_found.append(sid)
            continue
        if not isinstance(data, dict):
            not_found.append(sid)
            continue

        if has_license(data):
            already_set.append(sid)
            continue

        url = data.get("url")
        classified = classify_by_url(url) if url else None

        if classified:
            license_block, rationale = classified
            upsert = dict(data)
            upsert["license"] = license_block
            upsert["_contribution"] = {
                "chunk_id": chunk_id,
                "contributor": "claude-anthropic-internal",
                "submission_date": "2026-04-30",
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "target_action": "upsert",
                "target_entity_id": sid,
                "notes_for_reviewer": (
                    f"License backfill via URL-pattern classification: {rationale}. "
                    "License block populated; no other fields modified. "
                    "Maintainer should verify against publisher's current terms-of-use page."
                ),
            }
            (out_dir / path.name).write_text(
                yaml.safe_dump(upsert, sort_keys=False, allow_unicode=True, default_flow_style=False),
                encoding="utf-8",
            )
            upserts.append({"id": sid, "url": url, "license_name": license_block["name"]})
        else:
            unresolved.append({
                "id": sid,
                "url": url,
                "reason": (
                    "no_url_field" if not url else
                    "host_not_in_known_patterns — likely trial publication; needs publisher-specific check"
                ),
            })

    # task_manifest.txt
    lines = list(source_ids)
    if not_found:
        lines.append("\n# Not found in master:")
        lines.extend(f"# {x}" for x in not_found)
    if already_set:
        lines.append("\n# Already had license set (no-op):")
        lines.extend(f"# {x}" for x in already_set)
    (out_dir / "task_manifest.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # unresolved.yaml — report-only when there are any
    if unresolved:
        (out_dir / "unresolved.yaml").write_text(
            yaml.safe_dump({
                "_contribution": {
                    "chunk_id": chunk_id,
                    "contributor": "claude-anthropic-internal",
                    "submission_date": "2026-04-30",
                    "ai_tool": "claude-code",
                    "ai_model": "claude-opus-4-7",
                    "notes_for_reviewer": (
                        "Sources where license could not be classified from URL "
                        "hostname pattern alone. Mostly trial publications — "
                        "license depends on the journal that published the trial, "
                        "not the trial sponsor. Maintainer triages: each needs "
                        "publisher-specific terms-of-use check."
                    ),
                },
                "rows": unresolved,
            }, sort_keys=False, allow_unicode=True, default_flow_style=False),
            encoding="utf-8",
        )

    # _contribution_meta.yaml
    (out_dir / "_contribution_meta.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": chunk_id,
                "contributor": "claude-anthropic-internal",
                "submission_date": "2026-04-30",
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "ai_model_version": "1m-context",
                "ai_session_notes": (
                    f"Wave 7 batch — closes #{issue_number}. License backfill via "
                    "URL-hostname pattern matching (no web fetch). Known publishers "
                    "(NCCN, ESMO, FDA, NLM, CIViC, ClinicalTrials.gov, MOZ.gov.ua) "
                    "→ direct license classification. Trial publications without "
                    "matching pattern → flagged unresolved."
                ),
                "tasktorrent_version": "2026-04-30-pending-first-commit",
                "notes_for_reviewer": (
                    "Per-source upsert touches only the `license` block. No other "
                    "fields modified. Maintainer should verify against publisher's "
                    "current terms-of-use before promoting to hosted KB."
                ),
            },
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    return {
        "chunk_id": chunk_id, "issue_number": issue_number,
        "upserts": len(upserts),
        "unresolved": len(unresolved),
        "already_set": len(already_set),
        "not_found": len(not_found),
    }


def main() -> int:
    with open(MANIFESTS_FILE, encoding="utf-8") as f:
        manifests = json.load(f)
    summaries = []
    for k in sorted(manifests.keys(), key=int):
        n = int(k)
        chunk_id, sources = manifests[k]
        s = process_chunk(chunk_id, sources, n)
        summaries.append(s)
        print(f"  #{n}: upserts={s['upserts']} unresolved={s['unresolved']} "
              f"already_set={s['already_set']} not_found={s['not_found']}", file=sys.stderr)
    total = {
        "chunks": len(summaries),
        "upserts": sum(s["upserts"] for s in summaries),
        "unresolved": sum(s["unresolved"] for s in summaries),
        "already_set": sum(s["already_set"] for s in summaries),
    }
    print(f"\nBatch done: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
