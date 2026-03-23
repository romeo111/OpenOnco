#!/usr/bin/env python3
"""
generate_cases.py — Input Calibration Generator

Generates benchmark test cases for cancer research autoresearch loop.
Each case is a realistic patient scenario with cancer type, stage,
molecular markers, and patient context.

Usage:
    python generate_cases.py --site "throat and neck" --age 45 --sex male --count 10
    python generate_cases.py --site "lung" --age 60 --sex female --count 8
    python generate_cases.py --output my_cases.json --site "breast" --age 55 --sex female
"""

import json
import argparse
import sys
from datetime import datetime

# ── Head & Neck / Throat Cancer Case Library ─────────────────────────────────
# Ordered by epidemiological probability for a 45 y.o. male

HEAD_NECK_CASES = [
    {
        "id": "HN-001",
        "cancer_type": "HPV-positive oropharyngeal squamous cell carcinoma",
        "stage": "Stage III (T2N1M0)",
        "molecular_markers": ["HPV p16+", "PD-L1 CPS ≥20"],
        "patient_context": {
            "age": 45,
            "sex": "male",
            "risk_factors": ["prior HPV exposure", "non-smoker", "social alcohol use"],
            "comorbidities": [],
            "performance_status": "ECOG 0"
        },
        "why_this_case_matters": "Most common H&N cancer in younger males. Tests whether strategy captures de-escalation trials (lower chemoRT) and immunotherapy integration for favorable-prognosis HPV+ disease."
    },
    {
        "id": "HN-002",
        "cancer_type": "HPV-negative oropharyngeal squamous cell carcinoma",
        "stage": "Stage IVA (T3N2bM0)",
        "molecular_markers": ["HPV p16-", "PD-L1 CPS 5-10", "TP53 mutated"],
        "patient_context": {
            "age": 45,
            "sex": "male",
            "risk_factors": ["20 pack-year smoking history", "heavy alcohol use"],
            "comorbidities": ["mild COPD"],
            "performance_status": "ECOG 1"
        },
        "why_this_case_matters": "Aggressive HPV-negative disease with poor prognosis. Tests strategy's ability to find intensification approaches, novel immunotherapy combos, and accurate survival data for unfavorable biology."
    },
    {
        "id": "HN-003",
        "cancer_type": "Laryngeal squamous cell carcinoma (glottic)",
        "stage": "Stage II (T2N0M0)",
        "molecular_markers": ["PD-L1 CPS 1-5", "EGFR overexpressed"],
        "patient_context": {
            "age": 45,
            "sex": "male",
            "risk_factors": ["25 pack-year smoking history"],
            "comorbidities": ["hypertension"],
            "performance_status": "ECOG 0"
        },
        "why_this_case_matters": "Organ preservation is critical — tests whether strategy captures radiation vs. surgery trade-offs, voice preservation protocols, and cetuximab role in larynx-sparing approaches."
    },
    {
        "id": "HN-004",
        "cancer_type": "Nasopharyngeal carcinoma (WHO Type II/III, EBV-associated)",
        "stage": "Stage III (T3N1M0)",
        "molecular_markers": ["EBV+", "PD-L1 CPS ≥50", "high plasma EBV DNA"],
        "patient_context": {
            "age": 45,
            "sex": "male",
            "risk_factors": ["Southeast Asian descent", "family history of NPC"],
            "comorbidities": [],
            "performance_status": "ECOG 0"
        },
        "why_this_case_matters": "Distinct biology from other H&N cancers (EBV-driven). Tests strategy's ability to differentiate NPC-specific protocols, gemcitabine/cisplatin induction, and emerging EBV-targeted immunotherapies."
    },
    {
        "id": "HN-005",
        "cancer_type": "Hypopharyngeal squamous cell carcinoma",
        "stage": "Stage IVA (T4aN1M0)",
        "molecular_markers": ["PD-L1 CPS 10-20", "p53 mutant", "CDKN2A loss"],
        "patient_context": {
            "age": 45,
            "sex": "male",
            "risk_factors": ["30 pack-year smoking", "heavy alcohol use", "iron deficiency history"],
            "comorbidities": ["gastroesophageal reflux", "malnutrition (BMI 19)"],
            "performance_status": "ECOG 1"
        },
        "why_this_case_matters": "Worst prognosis among H&N sites. Tests strategy's handling of locally advanced disease where surgery is disfiguring, nutritional support is critical, and clinical trials may offer best hope."
    },
    {
        "id": "HN-006",
        "cancer_type": "Oral cavity squamous cell carcinoma (tongue)",
        "stage": "Stage II (T2N0M0)",
        "molecular_markers": ["PD-L1 CPS <1", "NOTCH1 mutated"],
        "patient_context": {
            "age": 45,
            "sex": "male",
            "risk_factors": ["betel nut/tobacco chewing history", "poor dental hygiene"],
            "comorbidities": ["type 2 diabetes"],
            "performance_status": "ECOG 0"
        },
        "why_this_case_matters": "Surgery-first cancer — tests whether strategy correctly prioritizes surgical resection over chemoRT, addresses margin considerations, and handles PD-L1-low cases where immunotherapy benefit is uncertain."
    },
    {
        "id": "HN-007",
        "cancer_type": "Thyroid cancer — papillary thyroid carcinoma (PTC)",
        "stage": "Stage II (T3N1aM0, per AJCC 8th for age <55)",
        "molecular_markers": ["BRAF V600E+", "RET/PTC rearrangement negative"],
        "patient_context": {
            "age": 45,
            "sex": "male",
            "risk_factors": ["childhood radiation exposure to neck", "family history of thyroid nodules"],
            "comorbidities": [],
            "performance_status": "ECOG 0"
        },
        "why_this_case_matters": "Excellent prognosis — tests strategy's calibration of ratings for highly curable cancers. Should identify total thyroidectomy + RAI, active surveillance debates, and BRAF-targeted options for refractory disease."
    },
    {
        "id": "HN-008",
        "cancer_type": "Salivary gland cancer — mucoepidermoid carcinoma (high-grade)",
        "stage": "Stage III (T3N1M0)",
        "molecular_markers": ["CRTC1-MAML2 fusion negative (high-grade indicator)", "HER2 amplified", "AR positive"],
        "patient_context": {
            "age": 45,
            "sex": "male",
            "risk_factors": ["prior radiation to face/neck region"],
            "comorbidities": [],
            "performance_status": "ECOG 0"
        },
        "why_this_case_matters": "Rare cancer with limited trial data — tests strategy's ability to find actionable targets (HER2, AR) in rare tumors and identify basket trials accepting salivary gland histologies."
    },
    {
        "id": "HN-009",
        "cancer_type": "Recurrent/metastatic head and neck squamous cell carcinoma (R/M HNSCC)",
        "stage": "Stage IVC (recurrence with lung metastases)",
        "molecular_markers": ["PD-L1 CPS ≥20", "TMB-high (≥10 mut/Mb)", "PIK3CA mutated"],
        "patient_context": {
            "age": 45,
            "sex": "male",
            "risk_factors": ["prior chemoRT for stage III oropharyngeal SCC 2 years ago"],
            "comorbidities": ["cisplatin-induced hearing loss", "chronic kidney disease stage 2"],
            "performance_status": "ECOG 1"
        },
        "why_this_case_matters": "The KEYNOTE-048 paradigm — tests whether strategy correctly applies pembrolizumab ± chemo as first-line, addresses platinum-ineligible options, and finds second-line trials for checkpoint-refractory disease."
    },
    {
        "id": "HN-010",
        "cancer_type": "Anaplastic thyroid carcinoma (ATC)",
        "stage": "Stage IVB (T4bN1bM0)",
        "molecular_markers": ["BRAF V600E+", "TP53 mutated", "TERT promoter mutated", "PD-L1 high"],
        "patient_context": {
            "age": 45,
            "sex": "male",
            "risk_factors": ["long-standing multinodular goiter", "possible de-differentiation from PTC"],
            "comorbidities": ["airway compression symptoms"],
            "performance_status": "ECOG 2"
        },
        "why_this_case_matters": "Worst-prognosis thyroid cancer (median survival ~5 months). Tests strategy's handling of ultra-aggressive disease — should find dabrafenib/trametinib (BRAF+), emerging immunotherapy combos, and clinical trials as primary approach."
    }
]

# ── Generic Case Generation for Other Sites ──────────────────────────────────

GENERIC_TEMPLATES = {
    "lung": [
        {"cancer_type": "Non-small cell lung cancer — adenocarcinoma", "markers": ["EGFR exon 19 del", "PD-L1 TPS ≥50%"]},
        {"cancer_type": "Non-small cell lung cancer — squamous cell", "markers": ["PD-L1 TPS 1-49%", "FGFR1 amplified"]},
        {"cancer_type": "Small cell lung cancer — extensive stage", "markers": ["RB1 loss", "TP53 mutated"]},
        {"cancer_type": "NSCLC — ALK-rearranged adenocarcinoma", "markers": ["ALK fusion+", "PD-L1 TPS <1%"]},
        {"cancer_type": "NSCLC — KRAS G12C mutant adenocarcinoma", "markers": ["KRAS G12C", "STK11 co-mutation"]},
        {"cancer_type": "NSCLC — ROS1-rearranged adenocarcinoma", "markers": ["ROS1 fusion+"]},
        {"cancer_type": "NSCLC — MET exon 14 skipping", "markers": ["MET ex14 skip", "MET amplification"]},
        {"cancer_type": "NSCLC — RET fusion-positive adenocarcinoma", "markers": ["RET fusion+"]},
        {"cancer_type": "NSCLC — EGFR exon 20 insertion", "markers": ["EGFR ex20ins"]},
        {"cancer_type": "Large cell neuroendocrine carcinoma of the lung", "markers": ["RB1 loss", "high Ki-67"]},
    ],
    "breast": [
        {"cancer_type": "Invasive ductal carcinoma — HR+/HER2-", "markers": ["ER+", "PR+", "HER2-", "Ki-67 low"]},
        {"cancer_type": "Triple-negative breast cancer (TNBC)", "markers": ["ER-", "PR-", "HER2-", "PD-L1 CPS ≥10"]},
        {"cancer_type": "HER2-positive breast cancer", "markers": ["HER2 amplified", "ER-", "PR-"]},
        {"cancer_type": "HR+/HER2- with PIK3CA mutation", "markers": ["ER+", "PIK3CA H1047R"]},
        {"cancer_type": "TNBC with BRCA1 germline mutation", "markers": ["BRCA1+", "HRD-high"]},
        {"cancer_type": "HER2-low breast cancer", "markers": ["HER2 IHC 1+", "ER+"]},
        {"cancer_type": "Inflammatory breast cancer", "markers": ["HER2+", "high Ki-67"]},
        {"cancer_type": "Lobular breast cancer — metastatic", "markers": ["ER+", "CDH1 loss", "ESR1 mutated"]},
        {"cancer_type": "TNBC — androgen receptor positive", "markers": ["AR+", "ER-", "PR-", "HER2-"]},
        {"cancer_type": "HR+/HER2- with ESR1 mutation (endocrine-resistant)", "markers": ["ESR1 D538G", "ER+"]},
    ],
    "colorectal": [
        {"cancer_type": "Colorectal adenocarcinoma — MSI-H/dMMR", "markers": ["MSI-H", "MLH1 loss"]},
        {"cancer_type": "Colorectal adenocarcinoma — KRAS G12C mutant", "markers": ["KRAS G12C", "MSS"]},
        {"cancer_type": "Colorectal adenocarcinoma — BRAF V600E", "markers": ["BRAF V600E", "MSS"]},
        {"cancer_type": "Colorectal adenocarcinoma — RAS/BRAF wild-type, left-sided", "markers": ["RAS WT", "BRAF WT"]},
        {"cancer_type": "Colorectal adenocarcinoma — HER2 amplified", "markers": ["HER2 amplified", "RAS WT"]},
        {"cancer_type": "Rectal adenocarcinoma — locally advanced, dMMR", "markers": ["dMMR", "PD-L1+"]},
        {"cancer_type": "Colorectal adenocarcinoma — NTRK fusion", "markers": ["NTRK fusion+"]},
        {"cancer_type": "Colorectal adenocarcinoma — MSS with high TMB", "markers": ["MSS", "TMB ≥10"]},
        {"cancer_type": "Anal squamous cell carcinoma", "markers": ["HPV+", "PD-L1+"]},
        {"cancer_type": "Appendiceal adenocarcinoma — peritoneal dissemination", "markers": ["KRAS mutated", "GNAS mutated"]},
    ],
    "pancreatic": [
        {"cancer_type": "Pancreatic ductal adenocarcinoma — resectable", "markers": ["KRAS G12D", "TP53 mutated"]},
        {"cancer_type": "Pancreatic ductal adenocarcinoma — locally advanced", "markers": ["KRAS G12V", "SMAD4 loss"]},
        {"cancer_type": "Pancreatic ductal adenocarcinoma — metastatic", "markers": ["KRAS G12D", "BRCA2 germline"]},
        {"cancer_type": "Pancreatic ductal adenocarcinoma — KRAS wild-type", "markers": ["KRAS WT", "NRG1 fusion"]},
        {"cancer_type": "Pancreatic neuroendocrine tumor (pNET) — grade 2", "markers": ["MEN1 mutated", "Ki-67 5-10%"]},
    ],
}

STAGES_DISTRIBUTION = [
    ("Stage I", 0.10),
    ("Stage II", 0.25),
    ("Stage III", 0.35),
    ("Stage IVA", 0.20),
    ("Stage IVB", 0.10),
]

RISK_FACTORS_MALE = [
    ["smoking history"],
    ["heavy alcohol use"],
    ["occupational chemical exposure"],
    ["obesity (BMI 32)"],
    ["family history of cancer"],
    ["sedentary lifestyle"],
    ["hypertension"],
    ["type 2 diabetes"],
    [],
    ["prior radiation exposure"],
]

COMORBIDITIES_45 = [
    [],
    ["hypertension"],
    ["type 2 diabetes"],
    ["mild COPD"],
    ["gastroesophageal reflux"],
    ["hyperlipidemia"],
    [],
    ["chronic kidney disease stage 2"],
    ["anxiety/depression"],
    [],
]


def generate_head_neck_cases(age: int, sex: str, count: int) -> list:
    """Generate curated head & neck cancer benchmark cases."""
    cases = HEAD_NECK_CASES[:count]
    # Adjust age in patient context
    result = []
    for case in cases:
        c = json.loads(json.dumps(case))  # deep copy
        c["patient_context"]["age"] = age
        c["patient_context"]["sex"] = sex
        result.append(c)
    return result


def generate_generic_cases(site: str, age: int, sex: str, count: int) -> list:
    """Generate cases from generic templates for non-curated sites."""
    templates = GENERIC_TEMPLATES.get(site.lower(), [])
    if not templates:
        print(f"Warning: No pre-built templates for site '{site}'. "
              f"Generating placeholder cases.", file=sys.stderr)
        return generate_placeholder_cases(site, age, sex, count)

    cases = []
    for i, tmpl in enumerate(templates[:count]):
        stage_idx = i % len(STAGES_DISTRIBUTION)
        stage = STAGES_DISTRIBUTION[stage_idx][0]
        risk = RISK_FACTORS_MALE[i % len(RISK_FACTORS_MALE)] if sex == "male" else []
        comorbid = COMORBIDITIES_45[i % len(COMORBIDITIES_45)]

        cases.append({
            "id": f"{site[:3].upper()}-{i+1:03d}",
            "cancer_type": tmpl["cancer_type"],
            "stage": stage,
            "molecular_markers": tmpl["markers"],
            "patient_context": {
                "age": age,
                "sex": sex,
                "risk_factors": risk,
                "comorbidities": comorbid,
                "performance_status": "ECOG 0" if i % 3 != 2 else "ECOG 1"
            },
            "why_this_case_matters": f"Tests strategy coverage for {tmpl['cancer_type']} with markers {', '.join(tmpl['markers'])}."
        })
    return cases


def generate_placeholder_cases(site: str, age: int, sex: str, count: int) -> list:
    """Generate minimal placeholder cases for unknown sites."""
    cases = []
    for i in range(count):
        stage_idx = i % len(STAGES_DISTRIBUTION)
        cases.append({
            "id": f"{site[:3].upper()}-{i+1:03d}",
            "cancer_type": f"{site} cancer — subtype {i+1}",
            "stage": STAGES_DISTRIBUTION[stage_idx][0],
            "molecular_markers": ["unknown — requires genomic profiling"],
            "patient_context": {
                "age": age,
                "sex": sex,
                "risk_factors": [],
                "comorbidities": [],
                "performance_status": "ECOG 0"
            },
            "why_this_case_matters": f"Placeholder case #{i+1} for {site} — replace with clinically accurate data."
        })
    return cases


def is_head_neck_site(site: str) -> bool:
    """Check if the site string refers to head & neck cancers."""
    site_lower = site.lower()
    keywords = ["throat", "neck", "head and neck", "head & neck", "h&n",
                "oropharyn", "laryn", "nasopharyn", "hypopharyn",
                "oral", "salivary", "thyroid", "tonsil"]
    return any(kw in site_lower for kw in keywords)


def generate_cases(site: str, age: int, sex: str, count: int) -> dict:
    """Main generation function. Returns the benchmark JSON structure."""
    if is_head_neck_site(site):
        cases = generate_head_neck_cases(age, sex, count)
    else:
        cases = generate_generic_cases(site, age, sex, count)

    return {
        "benchmark_metadata": {
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "site": site,
            "demographic": {"age": age, "sex": sex},
            "case_count": len(cases),
            "purpose": "Fixed test set for autoresearch loop — do NOT modify between iterations"
        },
        "cases": cases
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate benchmark cancer cases for autoresearch loop"
    )
    parser.add_argument("--site", required=True,
                        help='Cancer site, e.g. "throat and neck", "lung", "breast"')
    parser.add_argument("--age", type=int, required=True,
                        help="Patient age for all cases")
    parser.add_argument("--sex", required=True, choices=["male", "female"],
                        help="Patient sex for all cases")
    parser.add_argument("--count", type=int, default=10,
                        help="Number of benchmark cases (default: 10)")
    parser.add_argument("--output", "-o", default="benchmark_cases.json",
                        help="Output file path (default: benchmark_cases.json)")
    args = parser.parse_args()

    benchmark = generate_cases(args.site, args.age, args.sex, args.count)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(benchmark, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(benchmark['cases'])} benchmark cases for: {args.site}")
    print(f"Demographic: {args.age} y.o. {args.sex}")
    print(f"Saved to: {args.output}")
    print()
    for case in benchmark["cases"]:
        case_id = case['id']
        cancer = case['cancer_type']
        stage = case['stage']
        markers = ', '.join(case['molecular_markers'])
        try:
            print(f"  [{case_id}] {cancer}")
            print(f"         {stage} | Markers: {markers}")
        except UnicodeEncodeError:
            print(f"  [{case_id}] {cancer.encode('ascii', 'replace').decode()}")
            print(f"         {stage} | Markers: {markers.encode('ascii', 'replace').decode()}")
        print()


if __name__ == "__main__":
    main()
