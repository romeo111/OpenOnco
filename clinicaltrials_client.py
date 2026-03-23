#!/usr/bin/env python3
"""
clinicaltrials_client.py — ClinicalTrials.gov v2 API Client

Uses the official REST API (no key required, ~10 req/s limit).
More reliable than web-searching for trial info: returns structured,
authoritative data including real-time recruiting status, eligibility
criteria, NCT numbers, and site counts.

API docs: https://clinicaltrials.gov/data-api/api

Usage:
    python clinicaltrials_client.py search "oropharyngeal cancer pembrolizumab"
    python clinicaltrials_client.py search "HNSCC" --status RECRUITING --phase PHASE3
    python clinicaltrials_client.py get NCT01706829
    python clinicaltrials_client.py enrich experiment_reports/HN-001_report.json
    python clinicaltrials_client.py enrich experiment_reports/HN-001_report.json --output enriched.json
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
from typing import Optional

CT_BASE = "https://clinicaltrials.gov/api/v2"

# Fields to request for each study (CT.gov v2 FieldPath names)
_FIELDS = ",".join([
    "NCTId", "BriefTitle", "OfficialTitle", "OverallStatus",
    "Phase", "EnrollmentCount",
    "StartDate", "PrimaryCompletionDate",
    "Condition", "BriefSummary",
    "EligibilityCriteria", "MinimumAge", "MaximumAge", "Sex",
    "LeadSponsorName",
    "LocationCountry",
    "PrimaryOutcomeMeasure",
])

# Map our status shorthand → CT.gov enum values
_STATUS_MAP = {
    "recruiting":    "RECRUITING",
    "active":        "ACTIVE_NOT_RECRUITING",
    "completed":     "COMPLETED",
    "all":           None,  # no filter
}

# Map phase shorthand → CT.gov values
_PHASE_MAP = {
    "1":      "PHASE1",
    "2":      "PHASE2",
    "3":      "PHASE3",
    "phase1": "PHASE1",
    "phase2": "PHASE2",
    "phase3": "PHASE3",
}


# ── Core API Functions ─────────────────────────────────────────────────────────

def _get(url: str, timeout: int = 15) -> Optional[dict]:
    """GET a URL and return parsed JSON, or None on failure."""
    try:
        req  = urllib.request.Request(url, headers={"User-Agent": "CancerAutoResearch/1.0"})
        resp = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"  [ctgov] HTTP {e.code}: {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  [ctgov] request failed: {e}", file=sys.stderr)
        return None


def search_trials(
    condition: str,
    intervention: str = "",
    status: str = "recruiting",
    phase: str = "",
    max_results: int = 10,
) -> list:
    """
    Search ClinicalTrials.gov for studies matching condition + intervention.

    Args:
        condition:    Cancer type / disease query (e.g., "oropharyngeal cancer")
        intervention: Drug or treatment name (e.g., "pembrolizumab")
        status:       "recruiting" | "active" | "completed" | "all"
        phase:        "1" | "2" | "3" | "" (all phases)
        max_results:  Max studies to return

    Returns:
        List of study summary dicts.
    """
    params: dict = {
        "query.cond":  condition,
        "fields":      _FIELDS,
        "pageSize":    str(min(max_results, 25)),
        "format":      "json",
    }
    if intervention:
        params["query.intr"] = intervention

    status_enum = _STATUS_MAP.get(status.lower())
    if status_enum:
        params["filter.overallStatus"] = status_enum

    # Phase filtering: CT.gov v2 doesn't have a simple filter.phase param;
    # we filter client-side from results instead.
    _requested_phase = _PHASE_MAP.get(phase.lower().replace(" ", ""))

    url = f"{CT_BASE}/studies?" + urllib.parse.urlencode(params)
    data = _get(url)
    if not data:
        return []

    studies = data.get("studies", [])
    parsed = [_parse_study(s) for s in studies]
    # Client-side phase filter — CT.gov returns e.g. "PHASE2 / PHASE3"
    if _requested_phase:
        parsed = [s for s in parsed if _requested_phase in s.get("phase", "").upper()]
    return parsed


def get_trial(nct_id: str) -> Optional[dict]:
    """
    Fetch a single trial by NCT number.
    Returns parsed study dict or None.
    """
    url  = f"{CT_BASE}/studies/{nct_id}?fields={_FIELDS}&format=json"
    data = _get(url)
    if not data:
        return None
    return _parse_study(data)


def _parse_study(raw: dict) -> dict:
    """
    Parse a CT.gov v2 study response into a clean flat dict.
    The v2 API returns fields directly when a fields= list is provided,
    but falls back to protocolSection nesting for full-record requests.
    """
    # When fields= is used, response is a flat dict at top level.
    # For full record (/studies/{id}), it's nested under protocolSection.
    proto = raw.get("protocolSection", raw)

    def _get(*paths):
        """Walk multiple fallback paths in proto or raw."""
        for path in paths:
            node = proto
            for key in path.split("."):
                if isinstance(node, dict):
                    node = node.get(key)
                else:
                    node = None
                    break
            if node is not None:
                return node
        return None

    nct_id = _get("identificationModule.nctId") or raw.get("NCTId", "")
    title  = _get("identificationModule.briefTitle") or raw.get("BriefTitle", "")
    off_title = _get("identificationModule.officialTitle") or raw.get("OfficialTitle", "")
    status = _get("statusModule.overallStatus") or raw.get("OverallStatus", "")
    summary = _get("descriptionModule.briefSummary") or raw.get("BriefSummary", "")

    # Phase — stored as list in protocolSection, string in flat fields
    phase_raw = _get("designModule.phases") or raw.get("Phase", [])
    if isinstance(phase_raw, list):
        phase = " / ".join(phase_raw) if phase_raw else "N/A"
    else:
        phase = str(phase_raw) if phase_raw else "N/A"

    # Enrollment
    enroll_info = _get("designModule.enrollmentInfo") or {}
    enrollment  = enroll_info.get("count", 0) if isinstance(enroll_info, dict) else (raw.get("EnrollmentCount") or 0)

    # Dates
    start_date  = (_get("statusModule.startDateStruct.date") or raw.get("StartDate", ""))
    comp_date   = (_get("statusModule.primaryCompletionDateStruct.date") or raw.get("PrimaryCompletionDate", ""))

    # Eligibility
    elig_mod    = _get("eligibilityModule") or {}
    elig_text   = elig_mod.get("eligibilityCriteria", "") if isinstance(elig_mod, dict) else raw.get("EligibilityCriteria", "")
    min_age     = elig_mod.get("minimumAge", "") if isinstance(elig_mod, dict) else raw.get("MinimumAge", "")
    max_age     = elig_mod.get("maximumAge", "") if isinstance(elig_mod, dict) else raw.get("MaximumAge", "")
    sex         = elig_mod.get("sex", "ALL") if isinstance(elig_mod, dict) else raw.get("Sex", "ALL")

    # Sponsor
    sponsor_mod = _get("sponsorCollaboratorsModule.leadSponsor") or {}
    sponsor     = sponsor_mod.get("name", "") if isinstance(sponsor_mod, dict) else raw.get("LeadSponsorName", "")

    # Countries (flat field is a list; protocolSection is nested)
    countries_raw = raw.get("LocationCountry") or []
    if not countries_raw:
        locs = _get("contactsLocationsModule.locations") or []
        countries_raw = list({loc.get("country", "") for loc in locs if loc.get("country")})
    countries = countries_raw if isinstance(countries_raw, list) else [countries_raw]

    # Primary outcomes
    outcomes_raw = raw.get("PrimaryOutcomeMeasure") or []
    if not outcomes_raw:
        outcomes_raw = [o.get("measure", "") for o in (_get("outcomesModule.primaryOutcomes") or [])]
    primary_outcomes = outcomes_raw if isinstance(outcomes_raw, list) else [outcomes_raw]

    elig_summary = (elig_text[:500] + "...") if len(str(elig_text)) > 500 else elig_text

    return {
        "nct_id":             nct_id,
        "title":              title,
        "official_title":     off_title,
        "status":             status,
        "phase":              phase,
        "enrollment":         enrollment,
        "start_date":         start_date,
        "completion_date":    comp_date,
        "brief_summary":      summary,
        "primary_outcomes":   primary_outcomes,
        "eligibility_summary": elig_summary,
        "age_range":          f"{min_age}–{max_age}" if (min_age or max_age) else "",
        "sex":                sex,
        "sponsor":            sponsor,
        "countries":          [c for c in countries if c],
        "site_count":         len(countries),
        "url":                f"https://clinicaltrials.gov/study/{nct_id}" if nct_id else "",
    }


# ── Report Enrichment ──────────────────────────────────────────────────────────

def enrich_report_with_trials(
    report_path: str,
    max_trials_per_case: int = 5,
    verbose: bool = True,
) -> int:
    """
    For each clinical trial entry in a report that lacks a clinicaltrials.gov URL,
    attempt to find the matching NCT record and fill in structured data.

    Also appends newly found recruiting trials relevant to the cancer type.

    Returns number of trials enriched/added.
    """
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    cancer_type = report.get("report_metadata", {}).get("cancer_type", "")
    if not cancer_type:
        print("  [ctgov] no cancer_type in report_metadata", file=sys.stderr)
        return 0

    enriched = 0
    existing_trials = report.get("clinical_trials", [])
    existing_ncts = {
        re.search(r"NCT\d+", str(t)).group()
        for t in existing_trials
        if re.search(r"NCT\d+", str(t))
    }

    # 1. Enrich existing trial entries that have NCT IDs but missing data
    for trial in existing_trials:
        trial_str = json.dumps(trial)
        nct_match = re.search(r"NCT\d+", trial_str)
        if not nct_match:
            continue
        nct_id = nct_match.group()
        if trial.get("_ctgov_enriched"):
            continue
        ct_data = get_trial(nct_id)
        if ct_data:
            trial["status"]      = ct_data["status"]
            trial["phase"]       = ct_data["phase"]
            trial["enrollment"]  = ct_data["enrollment"]
            trial["countries"]   = ct_data["countries"]
            trial["site_count"]  = ct_data["site_count"]
            trial["url"]         = ct_data["url"]
            trial["_ctgov_enriched"] = True
            enriched += 1
            if verbose:
                print(f"  [ctgov] enriched {nct_id}: {ct_data['status']} ({ct_data['site_count']} sites)")
            time.sleep(0.15)  # ~10 req/s limit

    # 2. Find additional recruiting Phase 3 trials not yet in the report
    new_trials = search_trials(
        condition=cancer_type,
        status="recruiting",
        phase="3",
        max_results=max_trials_per_case,
    )
    for ct in new_trials:
        if ct["nct_id"] in existing_ncts:
            continue
        trial_entry = {
            "trial_id":   ct["nct_id"],
            "name":       ct["title"],
            "phase":      ct["phase"],
            "status":     ct["status"],
            "enrollment": ct["enrollment"],
            "sponsor":    ct["sponsor"],
            "countries":  ct["countries"],
            "site_count": ct["site_count"],
            "summary":    ct["brief_summary"][:300],
            "url":        ct["url"],
            "_ctgov_enriched": True,
            "_source": "clinicaltrials_client",
        }
        existing_trials.append(trial_entry)
        existing_ncts.add(ct["nct_id"])
        enriched += 1
        if verbose:
            print(f"  [ctgov] added {ct['nct_id']}: {ct['title'][:60]}")

    if enriched > 0:
        report["clinical_trials"] = existing_trials
        tmp = report_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        os.replace(tmp, report_path)

    return enriched


def search_and_format(
    condition: str,
    intervention: str = "",
    status: str = "recruiting",
    phase: str = "3",
    max_results: int = 10,
) -> str:
    """Return a formatted text summary of trial search results."""
    trials = search_trials(condition, intervention, status, phase, max_results)
    if not trials:
        return f"No {status} Phase {phase} trials found for: {condition} {intervention}"

    lines = [f"ClinicalTrials.gov — {len(trials)} results for '{condition}'"
             + (f" + '{intervention}'" if intervention else "")]
    lines.append("=" * 70)
    for t in trials:
        lines.append(f"\n{t['nct_id']}  [{t['status']}]  Phase: {t['phase']}")
        lines.append(f"  Title:    {t['title']}")
        lines.append(f"  Sponsor:  {t['sponsor']}")
        lines.append(f"  Sites:    {t['site_count']} ({', '.join(t['countries'][:5])})")
        if t["enrollment"]:
            lines.append(f"  Target N: {t['enrollment']}")
        if t["primary_outcomes"]:
            lines.append(f"  Primary:  {t['primary_outcomes'][0][:80]}")
        lines.append(f"  URL:      {t['url']}")
    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="ClinicalTrials.gov v2 API client for cancer autoresearch"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    p_s = sub.add_parser("search", help="Search trials by condition + intervention")
    p_s.add_argument("condition", help="Disease/condition query (e.g., 'oropharyngeal cancer')")
    p_s.add_argument("--intervention", "-i", default="", help="Drug/treatment name")
    p_s.add_argument("--status", default="recruiting",
                     choices=["recruiting", "active", "completed", "all"])
    p_s.add_argument("--phase", default="3", help="Trial phase: 1, 2, 3, or '' for all")
    p_s.add_argument("--n", type=int, default=10, help="Max results (default: 10)")
    p_s.add_argument("--json", action="store_true", help="Output as JSON")

    # get
    p_g = sub.add_parser("get", help="Get a single trial by NCT ID")
    p_g.add_argument("nct_id", help="NCT number (e.g., NCT01706829)")
    p_g.add_argument("--json", action="store_true", help="Output as JSON")

    # enrich
    p_e = sub.add_parser("enrich", help="Enrich a report JSON with CT.gov data")
    p_e.add_argument("report", help="Path to report JSON file")
    p_e.add_argument("--output", "-o", default=None,
                     help="Write enriched report to this path (default: overwrite input)")
    p_e.add_argument("--max-trials", type=int, default=5,
                     help="Max new trials to add per report (default: 5)")

    args = parser.parse_args()

    if args.command == "search":
        if getattr(args, "json", False):
            results = search_trials(args.condition, args.intervention,
                                    args.status, args.phase, args.n)
            print(json.dumps(results, indent=2))
        else:
            print(search_and_format(args.condition, args.intervention,
                                    args.status, args.phase, args.n))

    elif args.command == "get":
        trial = get_trial(args.nct_id)
        if not trial:
            print(f"Trial {args.nct_id} not found", file=sys.stderr)
            sys.exit(1)
        if getattr(args, "json", False):
            print(json.dumps(trial, indent=2))
        else:
            for k, v in trial.items():
                if v:
                    print(f"{k:<22} {v}")

    elif args.command == "enrich":
        report_path = args.report
        if args.output and args.output != report_path:
            import shutil
            shutil.copy2(report_path, args.output)
            report_path = args.output

        n = enrich_report_with_trials(report_path, args.max_trials, verbose=True)
        print(f"\nEnriched {n} trials in {report_path}")


if __name__ == "__main__":
    main()
