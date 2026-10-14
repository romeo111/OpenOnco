"""Observe medication-input handling using public synthetic examples only.

Legacy input shapes are probes, not supported medication API fields.
The canonical concomitant_medications contract is assessed for REG-CHP-BV only.
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
    "canonical_partial_bleomycin": {"concomitant_medications": {"status": "partial", "drug_ids": ["DRUG-BLEOMYCIN"]}},
    "canonical_complete_bleomycin": {"concomitant_medications": {"status": "complete", "drug_ids": ["DRUG-BLEOMYCIN"]}},
    "canonical_complete_empty": {"concomitant_medications": {"status": "complete", "drug_ids": []}},
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
                    "selection_withheld": bool(result.plan.knowledge_base_state.get("medication_selection_withheld")),
                    "medication_screens": result.plan.knowledge_base_state.get("medication_screens", []),
                    "surfaced_contraindications": sorted({ci.get("id") for track in result.plan.tracks for ci in track.contraindications_data if ci.get("id")}),
                }
            except ValueError as error:
                row = {"case": case, "probe": name, "accepted": False, "error": str(error)}
            if profile != before:
                raise AssertionError("Audit input was mutated")
            rows.append(row)
    files = ["knowledge_base/engine/medication_input.py", "knowledge_base/engine/medication_screen.py", "knowledge_base/engine/render.py", "knowledge_base/engine/plan.py", "knowledge_base/engine/profile_input.py",
             "knowledge_base/hosted/content/contraindications/ci_brentuximab_bleomycin.yaml",
             "knowledge_base/hosted/content/indications/ind_tcell_1l_chp_bv.yaml",
             "knowledge_base/hosted/content/indications/ind_aitl_1l_chp_bv.yaml"]
    return {
        "scope": "Source engine only; synthetic public examples; no network or production API calls.",
        "clinical_approval": False,
        "legacy_probe_fields_are_supported_contract": False,
        "canonical_contract": "concomitant_medications: {status: unknown|partial|complete, drug_ids: exact catalog IDs}",
        "primary_source": {"url": "https://labeling.pfizer.com/ShowLabeling.aspx?id=20629", "section": "4", "observed_date": "2026-10-14"},
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest() for name in files},
        "observations": rows,
        "remaining_limits": [
            "Only REG-CHP-BV and the explicit authored BV/bleomycin reference are assessed; other regimens/interactions remain unevaluated.",
            "Canonical JSON input is supported and retained by form/draft round trips; no medication picker or free-text extraction is claimed.",
            "Caller-reported completeness is not independently verified medication reconciliation or individual eligibility approval.",
            "Clinical/language review and production publication remain pending; this audit runs the draft source engine, not production API.",
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
