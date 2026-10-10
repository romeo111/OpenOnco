"""Synthetic probes of existing DLBCL rules, not clinical recommendations.

Expected routes are engineering contracts against the checked-in algorithm.
Clinical correctness, thresholds and source applicability require human review.
"""

from copy import deepcopy
import json
from pathlib import Path


STANDARD = "IND-DLBCL-1L-RCHOP"
INTENSIFIED = "IND-DLBCL-1L-POLA-R-CHP"


def scenarios() -> list[dict]:
    cases = []

    def add(case_id, title, changes=None, *, base="low", expected=STANDARD,
            category="routing", remove=(), flag=None):
        cases.append({"id": case_id, "title": title, "base": base,
                      "category": category, "changes": changes or {},
                      "remove": list(remove), "expected_default": expected,
                      "expected_flag": flag, "mode": "treatment"})

    for score in (0, 1, 2, 5):
        add(f"ipi-{score}", f"IPI score {score}", {"findings.ipi_score": score},
            expected=STANDARD if score < 2 else INTENSIFIED)
    for ecog in (2, 3, 4):
        add(f"ecog-{ecog}", f"IPI 4 with ECOG {ecog}", {"demographics.ecog": ecog},
            base="high", expected=INTENSIFIED if ecog == 2 else STANDARD if ecog == 3 else None,
            category="fitness", flag="RF-DLBCL-FRAILTY-AGE" if ecog >= 3 else None)
    for field, values, label in (
        ("lvef_percent", (49, 50), "LVEF"),
        ("creatinine_clearance_ml_min", (29, 30), "CrCl"),
        ("bilirubin_ratio_to_uln", (2.9, 3), "Bilirubin / ULN"),
        ("dlco_percent", (59, 60), "DLCO"),
    ):
        for value in values:
            triggered = value >= 3 if field == "bilirubin_ratio_to_uln" else value == values[0]
            add(f"{field}-{str(value).replace('.', '-')}", f"IPI 4 with {label} {value}",
                {f"findings.{field}": value}, base="high", category="organ function",
                expected=STANDARD if triggered else INTENSIFIED,
                flag="RF-DLBCL-ORGAN-DYSFUNCTION" if triggered else None)
    for field in ("hbsag", "anti_hbc_total"):
        add(f"{field}-positive", f"{field} positive", {f"findings.{field}": "positive",
            "biomarkers.BIO-HBV-STATUS": "positive"}, category="infection")
    for path in ("findings.ipi_score", "demographics.ecog", "findings.hbsag", "findings.lvef_percent"):
        add(f"missing-{path.split('.')[-1]}", f"Missing {path}", remove=(path,), category="missing data")
    add("cd20-unknown", "CD20 result unknown", {"biomarkers.BIO-CD20-IHC": "unknown",
        "findings.cd20_ihc_status": "unknown"}, category="missing data")
    add("cd20-negative", "CD20 result negative", {"biomarkers.BIO-CD20-IHC": "negative",
        "findings.cd20_ihc_status": "negative"}, category="eligibility")
    add("ipi-conflict", "IPI 1 conflicts with high_ipi=true", {"findings.high_ipi": True},
        expected=INTENSIFIED, category="conflicting data")
    add("unknown-disease", "Unresolvable disease identifier", {"disease.id": "DIS-REVIEW-UNKNOWN"},
        remove=("disease.icd_o_3_morphology",), expected=None, category="scope")
    add("unsupported-line", "Unmodeled line of therapy 99", {"line_of_therapy": 99},
        expected=None, category="scope")
    return cases


def _set(profile: dict, path: str, value) -> None:
    keys = path.split(".")
    target = profile
    for key in keys[:-1]:
        target = target.setdefault(key, {})
    target[keys[-1]] = value


def make_profile(case: dict, examples_dir: Path) -> dict:
    """Use only checked-in public synthetic seeds; never accept patient files."""
    filename = "patient_dlbcl_high_ipi.json" if case["base"] == "high" else "patient_dlbcl_low_ipi.json"
    seed = json.loads((examples_dir / filename).read_text(encoding="utf-8"))
    # Exclude the narrative record: a mutated score must not retain a conflicting
    # copied narrative / IPI-component table from the original example.
    profile = {key: deepcopy(seed[key]) for key in
               ("disease", "line_of_therapy", "biomarkers", "demographics", "findings")}
    profile["patient_id"] = f"SYNTHETIC-REVIEW-{case['id'].upper()}"
    profile["comment"] = "Synthetic engineering review probe; not a real patient or a prescription."
    findings = profile["findings"]
    for key in ("high_ipi", "Standard-risk IPI (0-1)", "ECOG ≤ 2"):
        findings.pop(key, None)
    findings.update({"biopsy_confirmed": True, "cd20_ihc_status": "positive",
                     "hbsag": "negative", "anti_hbc_total": "negative",
                     "creatinine_clearance_ml_min": 90,
                     "bilirubin_ratio_to_uln": 1, "dlco_percent": 85})
    profile["biomarkers"].update({"BIO-HBV-STATUS": "negative", "BIO-HCV-STATUS": "negative",
                                  "BIO-HIV-STATUS": "negative"})
    for path, value in case["changes"].items():
        _set(profile, path, value)
    for path in case["remove"]:
        keys = path.split(".")
        target = profile
        for key in keys[:-1]:
            target = target.get(key, {})
        target.pop(keys[-1], None)
    return profile
