# Re-evaluation Task: HN3-005

## Context
- **Case ID**: HN3-005
- **Cancer type**: Soft palate squamous cell carcinoma (oropharyngeal subsite)
- **Stage**: T2N0M0 (Stage II) — 45-year-old male smoker
- **Molecular profile**: PD-L1 CPS 10, EGFR overexpression, HPV/p16 status unknown (likely negative given smoking history and soft palate subsite — HPV prevalence only 28.7% in soft palate SCC), Active tobacco smoker
- **Report file**: experiment_reports\HN3-005_report.json
- **Current score**: 86/100
- **Gap analysis (local GPU)**: The lack of data on Definitive IMRT (70 Gy/35 fractions) + Concurrent Chemotherapy and Proton Beam Therapy (Intensity-Modulated Proton Therapy) with a specified sample size are critical gaps, as they represent key treatment modalities for head and neck cancer that have shown promise in improving outcomes. Addressing these gaps will improve the score by providing more comprehensive evidence on the efficacy of these treatments, which can inform clinical decision-making and ultimately lead to better patient outcomes.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  14/25  |  56.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (56.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-005_report.json`.

Your task: Fill missing evidence fields in `treatments[].key_evidence`.

For each treatment where these are null or missing, search and fill:
- `key_evidence.study_name` — full trial name
- `key_evidence.year` — publication year
- `key_evidence.sample_size` — numeric patient count
- `key_evidence.os_months.treatment` — median OS in treatment arm (months)
- `key_evidence.os_months.control` — median OS in control arm (months)
- `key_evidence.os_months.hazard_ratio` — HR from primary analysis
- `key_evidence.os_months.p_value` — p-value from OS analysis
- `key_evidence.pfs_months.treatment` — median PFS treatment arm
- `key_evidence.pfs_months.control` — median PFS control arm

Rules:
- Only fill with data you can verify from published trials
- Set to null (not omit) if genuinely unavailable after searching
- Do NOT fabricate or estimate numbers

Return the corrected `treatments` array only.

## Output format

Return a valid JSON object containing ONLY the corrected section (e.g., `{"treatments": [...]}` or `{"sources": [...]}`).

Do NOT return the full report — only the corrected array. The runner will merge it back.

After returning the JSON, add one line:
`SCORE_IMPACT: <estimated new score>/100`

## Report JSON (for reference)

```json
{
  "report_metadata": {
    "generated_date": "2026-03-23",
    "cancer_type": "Soft palate squamous cell carcinoma (oropharyngeal subsite)",
    "stage": "T2N0M0 (Stage II) — 45-year-old male smoker",
    "molecular_profile": [
      "PD-L1 CPS 10",
      "EGFR overexpression",
      "HPV/p16 status unknown (likely negative given smoking history and soft palate subsite — HPV prevalence only 28.7% in soft palate SCC)",
      "Active tobacco smoker"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Definitive IMRT (70 Gy/35 fractions) + Concurrent Cisplatin",
      "category": "Standard of Care",
      "composite_rating": 8.0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "NCCN Category 1 recommendation for T2N0M0 oropharyngeal SCC. Concurrent cisplatin-RT established by multiple phase 3 RCTs (Adelstein et al., Intergroup 0126). NCCN Guidelines v2.2025 and v1.2026 endorse definitive CRT as primary option for oropharyngeal cancer. IMRT is standard technique for oropharynx, reducing xerostomia and dysphagia vs 3D-CRT."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "Early-stage soft palate SCC (T1-2 N0-1) treated with definitive RT: 5-year OS 74.5%, PFS 84.7%, DSS 86.8%. Modern IMRT series: 5-year OS 86% (HPV+) and 64% (HPV-). Cisplatin concurrent with RT adds 6-8% absolute OS benefit over RT alone. T2 local control rate approximately 90% with definitive RT."
        },
        "accessibility": {
          "score": 9,
          "rationale": "IMRT and cisplatin universally available at all radiation oncology centers. Standard-of-care regimen covered by all insurance. Cisplatin 100 mg/m2 q3w x3 cycles or 40 mg/m2 weekly — both widely accessible protocols."
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Grade 3+ toxicity in 48% with IMRT. Cisplatin adds nephrotoxicity, ototoxicity, myelosuppression. Mucositis grade 3 in 40-60%. Feeding tube dependence at 2 years only 1%. Xerostomia and dysphagia are key long-term toxicities but IMRT reduces these. Velopharyngeal function generally preserved with RT compared to surgery."
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "No biomarker required — standard of care for all T2N0M0 oropharyngeal SCC. Smokers with presumed HPV-negative disease benefit from full-dose CRT (no de-escalation warranted). EGFR overexpression may enhance radiosensitization."
        }
      },
      "mechanism_of_action": "IMRT delivers conformal high-dose radiation (70 Gy in 35 fractions over 7 weeks) to the primary soft palate tumor and elective bilateral neck nodes while sparing parotid glands, pharyngeal constrictors, and contralateral structures. Cisplatin acts as a radiosensitizer by forming platinum-DNA adducts that inhibit DNA repair, creating lethal synergy with radiation-induced double-strand breaks.",
      "key_evidence": {
        "study_n
... (truncated — read full file from experiment_reports\HN3-005_report.json)
```
