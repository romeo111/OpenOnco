"""Observe medication-input handling using public synthetic examples only.

Candidate input shapes are probes, not a supported medication API contract.
This audit never changes clinical content or turns observations into approval.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from knowledge_base.engine import generate_plan

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge_base/hosted/content"
CASES = ("ptcl-cd30-positive", "aitl-cd30-positive", "alcl-alk-negative")
PROBES = {
    "absent": {},
    "top_level_medications": {"medications": ["DRUG-BLEOMYCIN"]},
    "top_level_concomitant_drugs": {"concomitant_drugs": ["DRUG-BLEOMYCIN"]},
    "finding_concomitant_drugs": {"findings": {"concomitant_drugs": ["DRUG-BLEOMYCIN"]}},
    "explicit_pair": {"findings": {"concomitant_drugs": ["DRUG-BRENTUXIMAB-VEDOTIN", "DRUG-BLEOMYCIN"]}},
    "named_bleomycin_flag": {"findings": {"bleomycin_concomitant": True}},
    "malformed_medications": {"medications": True},
}


def audit():
    examples = json.loads((ROOT / "docs/examples.json").read_text(encoding="utf-8"))
    rows = []
    for case in CASES:
        original = next(row["json"] for row in examples if row["case_id"] == case)
        for name, patch in PROBES.items():
            profile = copy.deepcopy(original)
            for key, value in patch.items():
                if key == "findings":
                    profile.setdefault(key, {}).update(copy.deepcopy(value))
                else:
                    profile[key] = copy.deepcopy(value)
            before = copy.deepcopy(profile)
            try:
                result = generate_plan(profile, kb_root=KB)
                row = {
                    "case": case, "probe": name, "accepted": True,
                    "regimens": [track.regimen_data.get("id") for track in result.plan.tracks],
                    "selection_withheld": bool(result.plan.knowledge_base_state.get("profile_selection_withheld")),
                    "surfaced_contraindications": sorted({ci.get("id") for track in result.plan.tracks for ci in track.contraindications_data if ci.get("id")}),
                }
            except ValueError as error:
                row = {"case": case, "probe": name, "accepted": False, "error": str(error)}
            if profile != before:
                raise AssertionError("Audit input was mutated")
            rows.append(row)
    files = ["knowledge_base/engine/plan.py", "knowledge_base/engine/profile_input.py",
             "knowledge_base/hosted/content/contraindications/ci_brentuximab_bleomycin.yaml",
             "knowledge_base/hosted/content/indications/ind_tcell_1l_chp_bv.yaml",
             "knowledge_base/hosted/content/indications/ind_aitl_1l_chp_bv.yaml"]
    return {
        "scope": "Source engine only; synthetic public examples; no network or production API calls.",
        "clinical_approval": False,
        "candidate_fields_are_supported_contract": False,
        "primary_source": {"url": "https://labeling.pfizer.com/ShowLabeling.aspx?id=20629", "section": "4", "observed_date": "2026-10-13"},
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest() for name in files},
        "observations": rows,
        "required_next_contract": [
            "Define a typed, explicit concomitant-medication input and unknown/completeness state before claiming screening.",
            "Do not infer an empty medication list from absent input, or combine historical exposure with active concomitant use.",
            "Match authored drug identifiers and proposed regimen components; do not guess aliases or free text.",
            "For a confirmed source-specific prohibited combination, withhold the selected track without automatically selecting a substitute.",
            "Unknown or malformed data must not be described as cleared; surface the incomplete screen in both report modes.",
            "Retain unrelated emergency signals; validate source, questionnaire, browser, API and WASM contracts together.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    exposed = sum("REG-CHP-BV" in row.get("regimens", []) for row in report["observations"] if row["probe"] != "absent")
    print(f"{len(report['observations'])} synthetic observations; BV retained in {exposed} medication probes. No clinical approval.")


if __name__ == "__main__":
    main()
