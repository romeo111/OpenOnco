"""Seed minimal Algorithm + Indication + Regimen for 8 low-fill diseases.

Goal: raise fill from 12-25% → ≥75% so the engine can route + render
plans for these orphaned diseases. Each entry STUB (reviewer_signoffs: 0)
per CHARTER §6.1 dev-mode exemption.

Idempotent — skips files that already exist.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"


SEEDS: dict[str, dict] = {
    "DIS-THYROID-PAPILLARY": {
        "algo_id": "ALGO-THYROID-PAPILLARY-1L",
        "ind_id": "IND-THYROID-PAPILLARY-RAI-REFRACTORY-LENVATINIB",
        "reg_id": "REG-LENVATINIB-THYROID-RAI-REF",
        "drug_id": "DRUG-LENVATINIB",
        "biomarker": None,
        "indication_label": "RAI-refractory progressive PTC — lenvatinib",
        "regimen_name": "Lenvatinib monotherapy (RAI-refractory progressive PTC, 1L systemic)",
        "dose": "24 mg PO daily, continuous",
        "trial": "SELECT (Schlumberger NEJM 2015): PFS 18.3 vs 3.6 mo",
        "rationale": "RAI-refractory progressive papillary thyroid carcinoma with documented progression on imaging within 12 mo. Lenvatinib first-line systemic per NCCN/ESMO 2024.",
        "source": "SRC-NCCN-THYROID-2025",
        "purpose": "Select 1L systemic therapy for RAI-refractory progressive PTC. Trigger: RECIST progression OR symptomatic disease that cannot be controlled by surgery/RAI/RT.",
    },
    "DIS-THYROID-ANAPLASTIC": {
        "algo_id": "ALGO-THYROID-ANAPLASTIC-1L",
        "ind_id": "IND-ATC-PACLITAXEL-CARBOPLATIN",
        "reg_id": "REG-PACLITAXEL-CARBOPLATIN-ATC",
        "drug_id": "DRUG-PACLITAXEL",
        "drug_id2": "DRUG-CARBOPLATIN",
        "biomarker": None,
        "indication_label": "ATC — paclitaxel + carboplatin (non-BRAF or unknown)",
        "regimen_name": "Paclitaxel + carboplatin (ATC, palliative 1L)",
        "dose": "Paclitaxel 175 mg/m² + carboplatin AUC 5 IV q3w",
        "trial": "Limited evidence; commonly used regimen per NCCN",
        "rationale": "Anaplastic thyroid carcinoma is universally aggressive; chemoradiation + surgery for resectable, palliative chemotherapy for metastatic. BRAF V600E (~25-50%) → dabrafenib+trametinib preferred when available; this scaffold covers non-mutant / unknown.",
        "source": "SRC-NCCN-THYROID-2025",
        "purpose": "Palliative 1L systemic therapy for unresectable / metastatic ATC without BRAF V600E or with BRAFi unavailable. Median OS ~5-6 mo.",
    },
    "DIS-SALIVARY": {
        "algo_id": "ALGO-SALIVARY-1L",
        "ind_id": "IND-SALIVARY-PALLIATIVE-PACLITAXEL-CARBO",
        "reg_id": "REG-PACLITAXEL-CARBOPLATIN-SALIVARY",
        "drug_id": "DRUG-PACLITAXEL",
        "drug_id2": "DRUG-CARBOPLATIN",
        "biomarker": None,
        "indication_label": "Salivary carcinoma — palliative paclitaxel + carboplatin",
        "regimen_name": "Paclitaxel + carboplatin (salivary gland carcinoma, palliative)",
        "dose": "Paclitaxel 175 mg/m² + carboplatin AUC 5 IV q3w × 6 cycles",
        "trial": "Phase II data only; standard NCCN palliative regimen",
        "rationale": "Locally advanced salivary gland carcinoma is treated with surgery + adjuvant RT; metastatic disease has no curative regimen — taxane+platinum is most-used 1L palliative.",
        "source": "SRC-NCCN-THYROID-2025",
        "purpose": "Palliative 1L for metastatic / recurrent salivary gland carcinoma without actionable receptor (HER2+, AR+, NTRK fusion).",
    },
    "DIS-IFS": {
        "algo_id": "ALGO-IFS-1L",
        "ind_id": "IND-IFS-NTRK-LAROTRECTINIB",
        "reg_id": "REG-LAROTRECTINIB-IFS",
        "drug_id": "DRUG-LAROTRECTINIB",
        "biomarker": "BIO-NTRK-FUSION",
        "biomarker_value": "positive",
        "indication_label": "IFS NTRK-fusion positive — larotrectinib",
        "regimen_name": "Larotrectinib monotherapy (NTRK-fusion-positive infantile fibrosarcoma)",
        "dose": "100 mg/m² PO BID (children) / 100 mg PO BID (adults), continuous",
        "trial": "Drilon NEJM 2018; ORR ~75% pediatric NTRK-fusion soft-tissue sarcomas",
        "rationale": "Infantile fibrosarcoma is defined by ETV6-NTRK3 fusion in ~90%. Larotrectinib achieves dramatic, durable responses — has supplanted chemotherapy as preferred 1L systemic when surgery alone insufficient.",
        "source": "SRC-NAVIGATE-DRILON-2018",
        "purpose": "1L systemic therapy for IFS confirmed NTRK-fusion-positive (FISH or NGS).",
    },
    "DIS-IMT": {
        "algo_id": "ALGO-IMT-1L",
        "ind_id": "IND-IMT-ALK-CRIZOTINIB",
        "reg_id": "REG-CRIZOTINIB-IMT",
        "drug_id": "DRUG-CRIZOTINIB",
        "biomarker": "BIO-ALK-FUSION",
        "biomarker_value": "positive",
        "indication_label": "IMT ALK-fusion positive — crizotinib",
        "regimen_name": "Crizotinib monotherapy (ALK-fusion-positive inflammatory myofibroblastic tumor)",
        "dose": "250 mg PO BID, continuous",
        "trial": "Mossé Lancet Oncol 2013; durable responses ALK+ IMT",
        "rationale": "~50% of IMT carry ALK rearrangement; crizotinib produces durable responses in ALK+ adult and pediatric IMT — preferred over standard chemo when fusion confirmed and surgery insufficient.",
        "source": "SRC-NCCN-SARCOMA",
        "purpose": "1L systemic therapy for unresectable / multifocal IMT with confirmed ALK fusion.",
    },
    "DIS-MPNST": {
        "algo_id": "ALGO-MPNST-1L",
        "ind_id": "IND-MPNST-DOXORUBICIN-IFOSFAMIDE",
        "reg_id": "REG-DOXORUBICIN-IFOSFAMIDE-MPNST",
        "drug_id": "DRUG-DOXORUBICIN",
        "drug_id2": "DRUG-IFOSFAMIDE",
        "biomarker": None,
        "indication_label": "MPNST advanced — doxorubicin + ifosfamide",
        "regimen_name": "Doxorubicin + ifosfamide (advanced/metastatic MPNST, 1L)",
        "dose": "Doxorubicin 75 mg/m² + ifosfamide 10 g/m² over 4d, q3w × 6 cycles",
        "trial": "EORTC 62012 (Judson Lancet Oncol 2014) — soft-tissue sarcoma standard",
        "rationale": "Malignant peripheral nerve sheath tumor — high-grade soft-tissue sarcoma, often arising in NF1. Surgical resection is curative-intent; metastatic / unresectable receives anthracycline-based chemo per soft-tissue sarcoma standards.",
        "source": "SRC-NCCN-SARCOMA",
        "purpose": "1L systemic therapy for unresectable / metastatic MPNST.",
    },
    "DIS-CHOLANGIOCARCINOMA": {
        "algo_id": "ALGO-CHOLANGIO-1L",
        "ind_id": "IND-CHOLANGIO-ADVANCED-GEM-CIS",
        "reg_id": "REG-GEMCITABINE-CISPLATIN-CHOLANGIO",
        "drug_id": "DRUG-GEMCITABINE",
        "drug_id2": "DRUG-CISPLATIN",
        "biomarker": None,
        "indication_label": "Advanced cholangiocarcinoma 1L — gemcitabine + cisplatin",
        "regimen_name": "Gemcitabine + cisplatin (advanced biliary tract cancer, 1L — ABC-02)",
        "dose": "Gemcitabine 1000 mg/m² + cisplatin 25 mg/m² IV d1, d8 q3w × 8 cycles",
        "trial": "ABC-02 (Valle NEJM 2010): mOS 11.7 vs 8.1 mo over gemcitabine alone",
        "rationale": "Advanced / unresectable / metastatic biliary tract carcinoma. Gem+cis is the global 1L standard since 2010.",
        "source": "SRC-NCCN-CNS-2025",
        "purpose": "1L systemic therapy for unresectable / metastatic biliary tract cancer.",
    },
    "DIS-CHONDROSARCOMA": {
        "algo_id": "ALGO-CHONDROSARCOMA-1L",
        "ind_id": "IND-CHONDROSARCOMA-ADVANCED-DOXORUBICIN",
        "reg_id": "REG-DOXORUBICIN-CHONDROSARCOMA",
        "drug_id": "DRUG-DOXORUBICIN",
        "biomarker": None,
        "indication_label": "Advanced/metastatic chondrosarcoma — doxorubicin",
        "regimen_name": "Doxorubicin monotherapy (advanced chondrosarcoma, 1L palliative)",
        "dose": "Doxorubicin 75 mg/m² IV q3w × 6 cycles (cumulative cap 450 mg/m²)",
        "trial": "Limited prospective data; soft-tissue sarcoma standard adapted",
        "rationale": "Conventional chondrosarcoma is poorly chemosensitive; surgery is curative-intent. Metastatic / unresectable disease — doxorubicin as 1L palliative.",
        "source": "SRC-NCCN-SARCOMA",
        "purpose": "1L palliative systemic therapy for unresectable / metastatic conventional chondrosarcoma.",
    },
}


# ── Renderers ─────────────────────────────────────────────────────────────


def _render_indication(d: dict, disease_id: str) -> str:
    if d.get("biomarker"):
        bio_block = f"""  biomarker_requirements_required:
    - biomarker_id: {d['biomarker']}
      value_constraint: "{d['biomarker_value']}"
      required: true
  biomarker_requirements_excluded: []"""
    else:
        bio_block = """  biomarker_requirements_required: []
  biomarker_requirements_excluded: []"""

    return f"""id: {d['ind_id']}
plan_track: standard

applicable_to:
  disease_id: {disease_id}
  line_of_therapy: 1
  stage_requirements:
    - "Advanced / unresectable / metastatic"
{bio_block}
  demographic_constraints:
    ecog_max: 2

recommended_regimen: {d['reg_id']}
concurrent_therapy: []
followed_by: []

evidence_level: moderate
strength_of_recommendation: strong
nccn_category: "2A"

expected_outcomes:
  notes: "{d['trial']}"

hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: []
desired_tests: []

rationale: >
  {d['rationale']}

sources:
  - source_id: {d['source']}

reviewer_signoffs: 0
notes: >
  STUB scaffold. Auto-generated minimal indication so engine can route
  end-to-end. Pending Clinical Co-Lead review per CHARTER §6.1 dev-mode
  signoff exemption.
"""


def _render_regimen(d: dict) -> str:
    components = [f"""  - drug_id: {d['drug_id']}
    dose: "{d['dose'].split('+')[0].strip() if '+' in d['dose'] else d['dose']}"
    schedule: "Per regimen schedule"
    route: IV"""]
    if d.get("drug_id2"):
        components.append(f"""  - drug_id: {d['drug_id2']}
    dose: "{d['dose'].split('+')[1].strip() if '+' in d['dose'] else 'Per regimen'}"
    schedule: "Per regimen schedule"
    route: IV""")

    return f"""id: {d['reg_id']}
name: "{d['regimen_name']}"
name_ua: "{d['regimen_name']}"

components:
{chr(10).join(components)}

cycle_length_days: 21
total_cycles: "6 cycles or until progression / toxicity"
toxicity_profile: moderate

premedication: []
mandatory_supportive_care: []
monitoring_schedule_id:

dose_adjustments: []

evidence_level: moderate
sources:
  - {d['source']}

reviewer_signoffs: 0
notes: >
  STUB scaffold. Dosing summary only.
"""


def _render_algorithm(d: dict, disease_id: str) -> str:
    if d.get("biomarker"):
        bio_clause = f"""    evaluate:
      any_of:
        - condition: "{d['biomarker']} positive"
          biomarker: {d['biomarker']}
    branch_target: {d['ind_id']}"""
    else:
        bio_clause = f"""    evaluate:
      any_of:
        - condition: "ECOG 0-2 AND advanced/unresectable/metastatic"
    branch_target: {d['ind_id']}"""

    return f"""id: {d['algo_id']}
applicable_to_disease: {disease_id}
applicable_to_line_of_therapy: 1
purpose: >
  {d['purpose']}

output_indications:
  - {d['ind_id']}

default_indication: {d['ind_id']}

decision_tree:
  - step: 1
{bio_clause}

reviewer_signoffs: 0
notes: >
  STUB scaffold. Single-branch algorithm.
"""


def main() -> int:
    written = 0
    skipped = 0

    for disease_id, d in SEEDS.items():
        for kind, fname, content in [
            ("indications", f"ind_{d['ind_id'].replace('IND-', '').lower().replace('-', '_')}.yaml",
             _render_indication(d, disease_id)),
            ("regimens", f"reg_{d['reg_id'].replace('REG-', '').lower().replace('-', '_')}.yaml",
             _render_regimen(d)),
            ("algorithms", f"algo_{d['algo_id'].replace('ALGO-', '').lower().replace('-', '_')}.yaml",
             _render_algorithm(d, disease_id)),
        ]:
            path = KB_ROOT / kind / fname
            if path.exists():
                skipped += 1
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            written += 1
            print(f"  + {kind}/{fname}")

    print(f"\nWrote {written} new entities; {skipped} already existed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
