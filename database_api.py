#!/usr/bin/env python3
"""
database_api.py — Query Interface for the Cancer AutoResearch Database

Standalone tool that reads directly from the research_db/ folder structure.
Works without the orchestrator server running.

Usage:
    python database_api.py search "glioblastoma"
    python database_api.py search --category cns_tumors --min-score 85
    python database_api.py ask "best treatment for HPV positive oropharyngeal cancer stage III"
    python database_api.py stats
    python database_api.py get-best "triple negative breast cancer"
    python database_api.py compare "lung cancer" "breast cancer"
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


# ── Constants ─────────────────────────────────────────────────────────────────

DB_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "research_db")
EXPERIMENT_REPORTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "experiment_reports")

# Known category names for browsing
KNOWN_CATEGORIES = [
    "carcinomas", "sarcomas", "leukemias", "lymphomas", "myelomas", "cns_tumors"
]

# Keyword synonyms for natural language search
_CANCER_SYNONYMS = {
    "glioblastoma": ["glioblastoma", "gbm", "glioblastoma multiforme", "grade iv glioma"],
    "nsclc": ["non-small cell lung", "nsclc", "adenocarcinoma lung", "squamous lung"],
    "sclc": ["small cell lung", "sclc"],
    "breast": ["breast cancer", "breast carcinoma", "invasive ductal", "invasive lobular"],
    "tnbc": ["triple negative breast", "tnbc", "triple-negative"],
    "crc": ["colorectal", "colon cancer", "rectal cancer", "crc"],
    "hnscc": ["head and neck", "hnscc", "oropharyngeal", "laryngeal", "hypopharyngeal"],
    "opscc": ["oropharyngeal", "opscc", "tonsil", "base of tongue"],
    "aml": ["acute myeloid leukemia", "aml"],
    "all": ["acute lymphoblastic leukemia", "all", "acute lymphocytic"],
    "dlbcl": ["diffuse large b-cell", "dlbcl", "large b-cell lymphoma"],
    "melanoma": ["melanoma", "cutaneous melanoma", "uveal melanoma"],
    "prostate": ["prostate cancer", "prostate adenocarcinoma", "castration resistant"],
    "pancreatic": ["pancreatic cancer", "pancreatic adenocarcinoma", "pdac"],
    "ovarian": ["ovarian cancer", "ovarian carcinoma", "high-grade serous"],
}

# Stop words for tokenization
_STOP_WORDS = {
    "the", "a", "an", "and", "or", "for", "in", "at", "of", "on", "is",
    "are", "was", "were", "to", "with", "by", "from", "this", "that",
    "what", "which", "how", "best", "treatment", "treatments", "cancer",
    "therapy", "therapies", "patient", "patients", "most", "more", "less",
    "its", "my", "your", "our", "their",
}


# ── Report Discovery ──────────────────────────────────────────────────────────

def _find_all_reports() -> List[Dict[str, Any]]:
    """
    Walk the research_db/ folder structure and find all *_report.json files.
    Also checks experiment_reports/ for legacy reports.
    Returns a list of report metadata dicts (without loading full JSON).
    """
    found = []

    def _scan_dir(base_dir: str, category: str) -> None:
        if not os.path.isdir(base_dir):
            return
        for entry in os.scandir(base_dir):
            if entry.is_dir():
                reports_dir = os.path.join(entry.path, "reports")
                if os.path.isdir(reports_dir):
                    for report_file in os.scandir(reports_dir):
                        if report_file.name.endswith("_report.json"):
                            found.append({
                                "path": report_file.path,
                                "cancer_type": entry.name.replace("_", " "),
                                "category": category,
                                "case_id": report_file.name.replace("_report.json", ""),
                                "filename": report_file.name,
                            })
                else:
                    # Recurse one more level (for category/subtype/reports)
                    _scan_dir(entry.path, category)

    for category in KNOWN_CATEGORIES:
        cat_path = os.path.join(DB_ROOT, category)
        _scan_dir(cat_path, category)

    # Also scan legacy experiment_reports/
    if os.path.isdir(EXPERIMENT_REPORTS):
        for fname in os.listdir(EXPERIMENT_REPORTS):
            if fname.endswith("_report.json"):
                case_id = fname.replace("_report.json", "")
                found.append({
                    "path": os.path.join(EXPERIMENT_REPORTS, fname),
                    "cancer_type": _infer_cancer_type_from_case_id(case_id),
                    "category": "carcinomas",
                    "case_id": case_id,
                    "filename": fname,
                })

    return found


def _infer_cancer_type_from_case_id(case_id: str) -> str:
    """Infer a display cancer type from a case ID like HN-001, LUNG-003, etc."""
    prefix = case_id.split("-")[0].upper()
    mapping = {
        "HN": "head and neck",
        "LUNG": "lung",
        "BREAST": "breast",
        "CRC": "colorectal",
        "GBM": "glioblastoma",
        "AML": "aml",
        "DLBCL": "dlbcl",
        "MEL": "melanoma",
        "PANC": "pancreatic",
    }
    return mapping.get(prefix, case_id.replace("-", " ").lower())


def _load_report(path: str) -> Optional[dict]:
    """Load and parse a report JSON file. Returns None on error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError, OSError):
        return None


def _get_report_score(report_data: dict) -> float:
    """Extract quality_score from a report (stored in various places)."""
    # Check quality metadata if present
    meta = report_data.get("quality_metadata", {})
    if meta.get("quality_score"):
        try:
            return float(meta["quality_score"])
        except (TypeError, ValueError):
            pass
    # Try evaluating on the fly
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from evaluate import evaluate_report
        result = evaluate_report(report_data)
        return float(result.get("quality_score", 0.0))
    except Exception:
        return 0.0


# ── ResearchDatabase Class ────────────────────────────────────────────────────

class ResearchDatabase:
    """
    Query interface for the accumulated research_db/ folder structure.
    Standalone — works without the server running.
    """

    def __init__(self, db_root: str = DB_ROOT):
        self.db_root = db_root
        self._index: Optional[dict] = None
        self._report_index: Optional[List[Dict[str, Any]]] = None

    def _get_index(self) -> dict:
        if self._index is None:
            index_path = os.path.join(self.db_root, "INDEX.json")
            try:
                with open(index_path, "r", encoding="utf-8") as f:
                    self._index = json.load(f)
            except Exception:
                self._index = {}
        return self._index

    def _get_report_index(self) -> List[Dict[str, Any]]:
        if self._report_index is None:
            self._report_index = _find_all_reports()
        return self._report_index

    def _refresh(self) -> None:
        """Invalidate cache — re-scan on next access."""
        self._report_index = None

    # ── Search ────────────────────────────────────────────────────────────────

    def search(
        self,
        cancer_type: Optional[str] = None,
        category: Optional[str] = None,
        min_score: float = 0.0,
        intent: Optional[str] = None,
        stage: Optional[str] = None,
        marker: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search the database for matching reports.

        Args:
            cancer_type:  Partial match against cancer type name
            category:     Exact category (carcinomas, sarcomas, etc.)
            min_score:    Minimum quality_score (0-100)
            intent:       Filter by treatment intent in top treatment
                          (curative, palliative, adjuvant, etc.)
            stage:        Partial match against stage in report_metadata
            marker:       Partial match against molecular_profile markers

        Returns:
            List of result dicts sorted by quality_score descending.
        """
        all_reports = self._get_report_index()
        results = []

        for entry in all_reports:
            # Category filter
            if category and entry["category"].lower() != category.lower():
                continue

            # Cancer type filter
            if cancer_type:
                ct_lower = cancer_type.lower()
                entry_ct = entry["cancer_type"].lower()
                if ct_lower not in entry_ct and entry_ct not in ct_lower:
                    # Try synonym matching
                    if not _matches_synonyms(ct_lower, entry_ct):
                        continue

            # Load report for deeper filtering
            report_data = _load_report(entry["path"])
            if not report_data:
                continue

            score = _get_report_score(report_data)
            if score < min_score:
                continue

            # Stage filter
            if stage:
                meta = report_data.get("report_metadata", {})
                report_stage = str(meta.get("stage", "")).lower()
                if stage.lower() not in report_stage:
                    continue

            # Marker filter
            if marker:
                meta = report_data.get("report_metadata", {})
                profile = meta.get("molecular_profile", [])
                profile_str = " ".join(str(p) for p in profile).lower()
                if marker.lower() not in profile_str:
                    continue

            # Intent filter — check top treatment
            if intent:
                treatments = report_data.get("treatments", [])
                top = treatments[0] if treatments else {}
                if str(top.get("intent", "")).lower() != intent.lower():
                    continue

            results.append({
                "case_id": entry["case_id"],
                "cancer_type": entry["cancer_type"],
                "category": entry["category"],
                "quality_score": round(score, 1),
                "path": entry["path"],
                "stage": report_data.get("report_metadata", {}).get("stage", "unknown"),
                "molecular_profile": report_data.get("report_metadata", {}).get(
                    "molecular_profile", []
                ),
                "top_treatment": _top_treatment_name(report_data),
                "treatment_count": len(report_data.get("treatments", [])),
            })

        return sorted(results, key=lambda r: r["quality_score"], reverse=True)

    # ── Get Best Treatment ────────────────────────────────────────────────────

    def get_best_treatment(
        self,
        cancer_type: str,
        stage: Optional[str] = None,
        markers: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get ranked treatment list from the best-scoring report for a cancer type.

        Returns:
            List of treatment dicts from the top-ranked report, or [] if not found.
        """
        results = self.search(cancer_type=cancer_type, stage=stage)
        if not results:
            return []

        best = results[0]
        report_data = _load_report(best["path"])
        if not report_data:
            return []

        treatments = report_data.get("treatments", [])

        # If markers specified, boost marker-matching treatments
        if markers:
            markers_lower = [m.lower() for m in markers]
            def _marker_score(t: dict) -> int:
                reqs = [r.lower() for r in t.get("biomarker_requirements", [])]
                return sum(1 for m in markers_lower if any(m in r for r in reqs))
            # Re-sort: primary by composite_rating, secondary by marker match
            treatments = sorted(
                treatments,
                key=lambda t: (t.get("composite_rating", 0), _marker_score(t)),
                reverse=True,
            )

        return [
            {
                "rank": i + 1,
                "name": t.get("name", "unknown"),
                "category": t.get("category", ""),
                "intent": t.get("intent", ""),
                "composite_rating": t.get("composite_rating", 0),
                "availability": t.get("availability", ""),
                "biomarker_requirements": t.get("biomarker_requirements", []),
                "notable_side_effects": t.get("notable_side_effects", []),
                "source_urls": t.get("source_urls", []),
                "key_evidence": _summarize_evidence(t.get("key_evidence", {})),
            }
            for i, t in enumerate(treatments)
        ]

    # ── Ask (Natural Language Query) ──────────────────────────────────────────

    def ask(self, question: str) -> str:
        """
        Simple keyword-based search + structured answer extraction.

        1. Tokenize the question
        2. Search reports by cancer type keywords
        3. Return top treatment recommendations from the best-scoring matching report
        4. Format as a readable response

        Returns:
            Human-readable answer string.
        """
        if not question.strip():
            return "Please ask a question about a cancer type and its treatments."

        # Tokenize
        tokens = _tokenize(question)
        if not tokens:
            return "Could not parse question. Try: 'best treatment for [cancer type]'"

        # Extract cancer type hint from tokens
        cancer_hint = _extract_cancer_type(tokens, question)
        stage_hint = _extract_stage(question)
        marker_hint = _extract_markers(question)

        if not cancer_hint:
            # Try searching with all content words
            cancer_hint = " ".join(tokens[:3])

        # Search
        results = self.search(cancer_type=cancer_hint, stage=stage_hint)
        if not results:
            # Broaden search
            for token in tokens:
                if token in _STOP_WORDS or len(token) < 4:
                    continue
                results = self.search(cancer_type=token)
                if results:
                    break

        if not results:
            return (
                f"No reports found matching '{question}'.\n"
                f"Available data covers: head and neck, lung, and other cancer types.\n"
                f"Run 'python database_api.py stats' to see current database coverage."
            )

        best = results[0]
        report_data = _load_report(best["path"])
        if not report_data:
            return f"Found report at {best['path']} but could not load it."

        return _format_ask_response(question, best, report_data, stage_hint, marker_hint)

    # ── Stats ─────────────────────────────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        """
        Return database statistics.

        Returns:
            Dict with total_reports, mean_score, coverage, etc.
        """
        all_entries = self._get_report_index()
        if not all_entries:
            return {
                "total_reports": 0,
                "mean_score": 0.0,
                "top_score": 0.0,
                "cancer_types_covered": 0,
                "categories_covered": 0,
                "coverage": {},
            }

        scores = []
        cancer_types: Dict[str, int] = {}
        categories: Dict[str, int] = {}

        for entry in all_entries:
            ct = entry["cancer_type"]
            cat = entry["category"]
            cancer_types[ct] = cancer_types.get(ct, 0) + 1
            categories[cat] = categories.get(cat, 0) + 1
            report_data = _load_report(entry["path"])
            if report_data:
                score = _get_report_score(report_data)
                scores.append(score)

        mean_score = round(sum(scores) / len(scores), 1) if scores else 0.0
        top_score = round(max(scores), 1) if scores else 0.0

        index = self._get_index()
        total_possible = 0
        index_categories = index.get("categories", {})
        for cat_data in index_categories.values():
            for subtype_data in cat_data.get("subtypes", {}).values():
                total_possible += 1  # count each defined subtype

        return {
            "total_reports": len(all_entries),
            "mean_score": mean_score,
            "top_score": top_score,
            "cancer_types_covered": len(cancer_types),
            "categories_covered": len(categories),
            "total_subtypes_defined": total_possible,
            "coverage_pct": round(len(cancer_types) / max(total_possible, 1) * 100, 1),
            "reports_per_cancer_type": dict(sorted(cancer_types.items())),
            "reports_per_category": dict(sorted(categories.items())),
        }

    # ── Compare ───────────────────────────────────────────────────────────────

    def compare(self, cancer_type_a: str, cancer_type_b: str) -> str:
        """
        Side-by-side comparison of two cancer types.
        Returns a formatted comparison string.
        """
        results_a = self.search(cancer_type=cancer_type_a)
        results_b = self.search(cancer_type=cancer_type_b)

        if not results_a and not results_b:
            return f"No reports found for either '{cancer_type_a}' or '{cancer_type_b}'."

        lines = [
            f"{'='*70}",
            f"  COMPARISON: {cancer_type_a.upper()} vs {cancer_type_b.upper()}",
            f"{'='*70}",
        ]

        def _side(label: str, results: List[Dict[str, Any]]) -> List[str]:
            out = [f"\n  --- {label.upper()} ---"]
            if not results:
                out.append(f"  No reports found.")
                return out
            best = results[0]
            out.append(f"  Reports found:    {len(results)}")
            out.append(f"  Best case:        {best['case_id']}")
            out.append(f"  Quality score:    {best['quality_score']}/100")
            out.append(f"  Stage:            {best['stage']}")
            out.append(f"  Top treatment:    {best['top_treatment']}")
            out.append(f"  Treatments in DB: {best['treatment_count']}")

            report_data = _load_report(best["path"])
            if report_data:
                treatments = report_data.get("treatments", [])[:3]
                if treatments:
                    out.append(f"  Top 3 treatments:")
                    for i, t in enumerate(treatments, 1):
                        rating = t.get("composite_rating", "?")
                        intent = t.get("intent", "?")
                        out.append(f"    {i}. {t.get('name', 'unknown')} "
                                   f"(rating {rating}, {intent})")
            return out

        lines.extend(_side(cancer_type_a, results_a))
        lines.extend(_side(cancer_type_b, results_b))
        lines.append(f"\n{'='*70}")
        return "\n".join(lines)


# ── Helper Functions ──────────────────────────────────────────────────────────

def _matches_synonyms(query: str, cancer_type: str) -> bool:
    """Check if query matches any synonym for cancer_type."""
    for canonical, synonyms in _CANCER_SYNONYMS.items():
        if any(s in cancer_type for s in synonyms):
            # This cancer_type matches the synonym group
            if any(s in query for s in synonyms) or canonical in query:
                return True
    return False


def _top_treatment_name(report_data: dict) -> str:
    """Get the name of the top-ranked treatment in a report."""
    treatments = report_data.get("treatments", [])
    if not treatments:
        return "none"
    return treatments[0].get("name", "unknown")


def _summarize_evidence(ev: dict) -> Dict[str, Any]:
    """Summarize key_evidence into a brief dict."""
    if not ev:
        return {}
    summary: Dict[str, Any] = {}
    if ev.get("study_name"):
        summary["study"] = ev["study_name"]
    if ev.get("journal"):
        summary["journal"] = ev["journal"]
    os_data = ev.get("os_months", {})
    if isinstance(os_data, dict) and os_data.get("treatment"):
        trt = os_data.get("treatment")
        ctl = os_data.get("control")
        if trt and ctl:
            summary["os_months"] = f"{trt} vs {ctl} (control)"
        elif trt:
            summary["os_months"] = f"{trt} months"
        hr = os_data.get("hazard_ratio")
        if hr:
            summary["hazard_ratio"] = hr
    return summary


def _tokenize(text: str) -> List[str]:
    """Tokenize a question into meaningful words."""
    words = re.findall(r"[a-zA-Z0-9\+\-]+", text.lower())
    return [w for w in words if w not in _STOP_WORDS and len(w) >= 2]


def _extract_cancer_type(tokens: List[str], original: str) -> str:
    """Try to extract a cancer type phrase from the question."""
    orig_lower = original.lower()

    # Try to find known cancer types in the original question
    cancer_phrases = [
        "glioblastoma", "non-small cell lung", "nsclc", "small cell lung",
        "triple negative breast", "tnbc", "oropharyngeal", "head and neck",
        "hnscc", "colorectal", "pancreatic", "ovarian", "prostate",
        "melanoma", "leukemia", "lymphoma", "myeloma", "sarcoma",
        "bladder", "cervical", "thyroid", "hepatocellular", "gastric",
        "kidney", "renal", "breast",
    ]
    for phrase in cancer_phrases:
        if phrase in orig_lower:
            return phrase

    # Check HPV+ variants
    if "hpv" in orig_lower and "oropharyngeal" in orig_lower:
        return "oropharyngeal"
    if "hpv" in orig_lower and "head" in orig_lower:
        return "head and neck"

    # Fall back to longest content word
    content_tokens = [t for t in tokens if len(t) >= 4]
    return content_tokens[0] if content_tokens else ""


def _extract_stage(question: str) -> Optional[str]:
    """Extract stage hint from question."""
    q = question.upper()
    patterns = [
        r'\bSTAGE\s+(I{1,3}V?[ABC]?|IV[ABC]?)\b',
        r'\bSTAGE\s+(\d)\b',
        r'\b(I{1,3}V?[ABC]?)\b',
        r'\bM1\b', r'\bIVB\b', r'\bIVC\b',
    ]
    for pat in patterns:
        m = re.search(pat, q)
        if m:
            return m.group(0).strip()
    return None


def _extract_markers(question: str) -> List[str]:
    """Extract molecular marker hints from question."""
    q = question.lower()
    markers = []
    marker_keywords = [
        "hpv", "egfr", "kras", "braf", "alk", "ros1", "ret", "ntrk",
        "pd-l1", "her2", "brca", "msi", "mmr", "tmt", "fgfr",
        "erbb2", "met", "nras", "pik3ca", "tp53",
    ]
    for kw in marker_keywords:
        if kw in q:
            markers.append(kw)
    return markers


def _format_ask_response(
    question: str,
    best_result: Dict[str, Any],
    report_data: dict,
    stage_hint: Optional[str],
    marker_hint: List[str],
) -> str:
    """Format a human-readable answer from the best matching report."""
    cancer_type = best_result["cancer_type"].title()
    score = best_result["quality_score"]
    case_id = best_result["case_id"]

    lines = [
        f"",
        f"Question: {question}",
        f"{'='*70}",
        f"",
        f"Based on the best available research report for {cancer_type}:",
        f"  Report ID:     {case_id}",
        f"  Quality score: {score}/100",
    ]

    meta = report_data.get("report_metadata", {})
    report_stage = meta.get("stage", "not specified")
    profile = meta.get("molecular_profile", [])
    if profile:
        lines.append(f"  Molecular:     {', '.join(str(p) for p in profile)}")
    lines.append(f"  Stage:         {report_stage}")
    lines.append(f"")

    # Top treatments
    treatments = report_data.get("treatments", [])
    curative = [t for t in treatments
                if t.get("intent", "").lower() in ("curative", "adjuvant", "neoadjuvant")]
    palliative = [t for t in treatments
                  if t.get("intent", "").lower() in ("palliative", "salvage", "maintenance")]
    other = [t for t in treatments
             if t not in curative and t not in palliative]

    def _format_treatment_list(title: str, tlist: List[dict], max_items: int = 5) -> List[str]:
        if not tlist:
            return []
        result = [f"  {title}:"]
        for i, t in enumerate(tlist[:max_items], 1):
            name = t.get("name", "unknown")
            rating = t.get("composite_rating", "?")
            intent = t.get("intent", "?")
            avail = t.get("availability", "")[:50] if t.get("availability") else ""

            # Evidence summary
            ev = t.get("key_evidence", {})
            os_data = ev.get("os_months", {})
            os_str = ""
            if isinstance(os_data, dict) and os_data.get("treatment"):
                trt = os_data.get("treatment")
                ctl = os_data.get("control")
                if trt and ctl:
                    os_str = f"  [OS: {trt}mo vs {ctl}mo control]"
                elif trt:
                    os_str = f"  [OS: {trt}mo]"

            side_effects = t.get("notable_side_effects", [])
            se_str = (", ".join(str(s) for s in side_effects[:2])
                      if side_effects else "")

            result.append(f"    {i}. {name}")
            result.append(f"       Rating: {rating}/10 | Intent: {intent}")
            if avail:
                result.append(f"       Status: {avail}")
            if os_str:
                result.append(f"       Evidence: {os_str.strip()}")
            if se_str:
                result.append(f"       Side effects: {se_str}")
            urls = t.get("source_urls", [])
            if urls:
                result.append(f"       Source: {urls[0]}")
        return result

    if curative:
        lines.extend(_format_treatment_list("Curative-Intent Options", curative))
        lines.append("")
    if palliative:
        lines.extend(_format_treatment_list("Palliative/Salvage Options", palliative, 3))
        lines.append("")
    if other and not curative and not palliative:
        lines.extend(_format_treatment_list("Treatment Options", other))
        lines.append("")

    # Clinical trials
    trials = report_data.get("clinical_trials", [])
    if trials:
        lines.append(f"  Active Clinical Trials ({len(trials)} found):")
        for t in trials[:3]:
            trial_id = t.get("trial_id", t.get("nct_id", "unknown"))
            title = t.get("title", "unknown")[:60]
            phase = t.get("phase", "?")
            status = t.get("status", "?")
            lines.append(f"    - {trial_id} [{phase}] {title}... ({status})")
        lines.append("")

    # Disclaimer
    lines.extend([
        f"{'─'*70}",
        f"DISCLAIMER: This information is for research and educational purposes",
        f"only. Always consult a qualified oncologist before making treatment",
        f"decisions. Report quality score: {score}/100.",
        f"{'─'*70}",
        f"",
    ])

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def _print_search_results(results: List[Dict[str, Any]]) -> None:
    if not results:
        print("No reports found matching your query.")
        return
    print(f"\nFound {len(results)} report(s):\n")
    print(f"  {'Case ID':<20} {'Cancer Type':<30} {'Score':>6}  {'Stage':<12} {'Top Treatment'}")
    print(f"  {'-'*20} {'-'*30} {'-'*6}  {'-'*12} {'-'*30}")
    for r in results:
        print(
            f"  {r['case_id']:<20} "
            f"{r['cancer_type'][:29]:<30} "
            f"{r['quality_score']:>6.1f}  "
            f"{str(r['stage'])[:11]:<12} "
            f"{str(r['top_treatment'])[:40]}"
        )
    print()


def _print_stats(stats: Dict[str, Any]) -> None:
    print(f"\n{'='*60}")
    print(f"  Cancer AutoResearch Database Statistics")
    print(f"{'='*60}")
    print(f"  Total reports:          {stats['total_reports']}")
    print(f"  Mean quality score:     {stats['mean_score']}/100")
    print(f"  Top quality score:      {stats['top_score']}/100")
    print(f"  Cancer types covered:   {stats['cancer_types_covered']}")
    print(f"  Categories covered:     {stats['categories_covered']}")
    if "total_subtypes_defined" in stats:
        print(f"  Total subtypes defined: {stats['total_subtypes_defined']}")
        print(f"  Database coverage:      {stats['coverage_pct']}%")
    print()
    if stats.get("reports_per_category"):
        print(f"  Reports by Category:")
        for cat, count in stats["reports_per_category"].items():
            print(f"    {cat:<25} {count:>4} reports")
    print()
    if stats.get("reports_per_cancer_type"):
        print(f"  Reports by Cancer Type (top 10):")
        sorted_types = sorted(
            stats["reports_per_cancer_type"].items(),
            key=lambda x: x[1], reverse=True
        )
        for ct, count in sorted_types[:10]:
            print(f"    {ct:<35} {count:>4}")
    print(f"{'='*60}\n")


def _print_best_treatment(cancer_type: str, treatments: List[Dict[str, Any]]) -> None:
    if not treatments:
        print(f"No treatment data found for '{cancer_type}'.")
        return
    print(f"\n{'='*70}")
    print(f"  BEST TREATMENTS: {cancer_type.upper()}")
    print(f"  ({len(treatments)} treatments from highest-scoring report)")
    print(f"{'='*70}\n")
    for t in treatments:
        rank = t.get("rank", "?")
        name = t.get("name", "unknown")
        rating = t.get("composite_rating", "?")
        intent = t.get("intent", "?")
        avail = t.get("availability", "")
        biomarkers = t.get("biomarker_requirements", [])
        se = t.get("notable_side_effects", [])
        ev = t.get("key_evidence", {})
        urls = t.get("source_urls", [])

        print(f"  #{rank}: {name}")
        print(f"       Composite Rating: {rating}/10 | Intent: {intent}")
        if avail:
            print(f"       Availability: {avail[:70]}")
        if biomarkers:
            print(f"       Biomarkers: {', '.join(str(b) for b in biomarkers)}")
        if se:
            print(f"       Side Effects: {', '.join(str(s) for s in se[:3])}")
        if ev.get("study"):
            print(f"       Key Study: {ev['study']}")
        if ev.get("os_months"):
            print(f"       OS: {ev['os_months']}")
        if urls:
            print(f"       Source: {urls[0]}")
        print()
    print(f"{'='*70}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cancer AutoResearch Database Query Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python database_api.py search "glioblastoma"
  python database_api.py search --category cns_tumors --min-score 85
  python database_api.py ask "best treatment for HPV positive oropharyngeal cancer stage III"
  python database_api.py stats
  python database_api.py get-best "triple negative breast cancer"
  python database_api.py compare "lung cancer" "breast cancer"
        """,
    )
    parser.add_argument("--db-root", default=DB_ROOT,
                        help=f"Path to research_db root (default: {DB_ROOT})")

    sub = parser.add_subparsers(dest="command", help="Command")
    sub.required = True

    # search
    p_search = sub.add_parser("search", help="Search reports by cancer type / filters")
    p_search.add_argument("cancer_type", nargs="?", default=None,
                          help="Cancer type to search for (partial match)")
    p_search.add_argument("--category", "-c", default=None,
                          help="Filter by category (carcinomas, sarcomas, etc.)")
    p_search.add_argument("--min-score", type=float, default=0.0,
                          help="Minimum quality score (default: 0)")
    p_search.add_argument("--stage", default=None,
                          help="Filter by stage (partial match)")
    p_search.add_argument("--marker", default=None,
                          help="Filter by molecular marker (partial match)")
    p_search.add_argument("--intent", default=None,
                          help="Filter by treatment intent in top treatment")
    p_search.add_argument("--limit", type=int, default=20,
                          help="Maximum results (default: 20)")

    # ask
    p_ask = sub.add_parser("ask", help="Ask a natural language question")
    p_ask.add_argument("question", nargs="+",
                       help="Question about cancer treatments")

    # stats
    sub.add_parser("stats", help="Database statistics and coverage")

    # get-best
    p_best = sub.add_parser("get-best", help="Get ranked treatments for a cancer type")
    p_best.add_argument("cancer_type", help="Cancer type to look up")
    p_best.add_argument("--stage", default=None, help="Filter by stage")
    p_best.add_argument("--markers", nargs="+", default=None,
                        help="Molecular markers to prioritize")

    # compare
    p_compare = sub.add_parser("compare", help="Compare two cancer types side by side")
    p_compare.add_argument("cancer_type_a", help="First cancer type")
    p_compare.add_argument("cancer_type_b", help="Second cancer type")

    args = parser.parse_args()

    db = ResearchDatabase(db_root=args.db_root)

    if args.command == "search":
        results = db.search(
            cancer_type=args.cancer_type,
            category=args.category,
            min_score=args.min_score,
            intent=args.intent,
            stage=args.stage,
            marker=args.marker,
        )
        if args.limit:
            results = results[: args.limit]
        _print_search_results(results)

    elif args.command == "ask":
        question = " ".join(args.question)
        answer = db.ask(question)
        # Windows console may not support all Unicode — encode safely
        safe_answer = answer.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(
            sys.stdout.encoding or "utf-8"
        )
        print(safe_answer)

    elif args.command == "stats":
        stats = db.stats()
        _print_stats(stats)

    elif args.command == "get-best":
        treatments = db.get_best_treatment(
            cancer_type=args.cancer_type,
            stage=args.stage,
            markers=args.markers,
        )
        _print_best_treatment(args.cancer_type, treatments)

    elif args.command == "compare":
        output = db.compare(args.cancer_type_a, args.cancer_type_b)
        print(output)


if __name__ == "__main__":
    main()
