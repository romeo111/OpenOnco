"""Audit trial-search provenance with synthetic responses and no network calls.

Failures describe reporting defects, never an absence of trials or approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from knowledge_base.engine.experimental_options import enumerate_experimental_options
from knowledge_base.engine.render import _render_experimental_options
from knowledge_base.schemas.experimental_option import ExperimentalOption

ROOT = Path(__file__).resolve().parents[1]


def audit() -> dict:
    observations = []
    for scenario in ("not_configured", "request_failed", "successful_empty", "successful_results"):
        calls = []

        def search(*, _calls=calls, _scenario=scenario, **kwargs):
            _calls.append(kwargs)
            if _scenario == "request_failed":
                raise RuntimeError("synthetic registry failure")
            if _scenario == "successful_results":
                return [{"nct_id": "NCT00000001", "title": "Synthetic audit fixture", "status": "RECRUITING"}]
            return []

        option = enumerate_experimental_options(
            disease_id="DIS-AUDIT", disease_term="Synthetic audit condition",
            search_fn=None if scenario == "not_configured" else search,
            cache=False,
        )
        findings = []
        if scenario in {"not_configured", "request_failed"} and option.last_synced:
            findings.append("unsuccessful_search_has_successful_sync_date")
        observations.append(_observe(scenario, option, len(calls), findings))

    # Legacy empty cache data alone cannot prove a completed search.
    legacy = ExperimentalOption(
        id="EXPER-AUDIT-LEGACY", disease_id="DIS-AUDIT",
        trials=[], last_synced="2000-01-01",
    )
    findings = []
    if "No active trials matched" in _render_experimental_options(legacy, target_lang="en"):
        findings.append("legacy_empty_without_execution_provenance_claims_negative_search")
    observations.append(_observe("legacy_empty_unknown_execution", legacy, 0, findings))
    files = (
        "knowledge_base/engine/experimental_options.py",
        "knowledge_base/engine/render.py",
        "knowledge_base/schemas/experimental_option.py",
    )
    return {
        "scope": "Source engine and EN/UK renderer only; synthetic inputs; no network, production API or patient data.",
        "clinical_approval": False,
        "production_verified": False,
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest() for name in files},
        "observations": observations,
        "finding_count": sum(len(row["findings"]) for row in observations),
        "required_followup": [
            "Persist explicit search execution state, including unknown for legacy cache payloads.",
            "Set successful synchronization date only after a successful registry response; retain the real cached date.",
            "Distinguish not searched, request failed and successfully empty results in English and Ukrainian reports.",
            "A successful empty filtered response describes this query only, never the global absence of trials or patient eligibility.",
            "Verify cache round trips, API and offline bundles before publication; preserve clinical treatment selection.",
        ],
    }


def _observe(scenario, option, calls, findings):
    return {
        "scenario": scenario,
        "injected_search_calls": calls,
        "trial_count": len(option.trials),
        "last_synced": option.last_synced,
        "notes": option.notes,
        "rendered_html": {lang: _render_experimental_options(option, target_lang=lang) for lang in ("en", "uk")},
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(result['observations'])} synthetic scenarios; {result['finding_count']} reporting findings; no network calls.")
    return 1 if result["finding_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
