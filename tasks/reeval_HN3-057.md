# Re-evaluation Task: HN3-057

## Context
- **Case ID**: HN3-057
- **Cancer type**: HPV-Positive Oropharyngeal Squamous Cell Carcinoma
- **Stage**: T4aN3bM0 (AJCC 8th Edition Stage III for p16+ OPSCC)
- **Molecular profile**: HPV-positive (p16+), SMAD4 loss, PIK3CA mutation, Never-smoker, Unfavorable risk despite HPV positivity
- **Report file**: experiment_reports\HN3-057_report.json
- **Current score**: 72/100
- **Gap analysis (local GPU)**: The most critical gaps in HN3-057 include the lack of definitive data on Neoadjuvant + Adjuvant Pembrolizumab with Standard treatment, which is a crucial area for improvement as it directly impacts the efficacy and survival rates of patients with head and neck cancer. Addressing this gap by providing more comprehensive data will significantly improve the score, as it will provide valuable insights into the effectiveness of pembrolizumab in combination with standard treatments, ultimately informing clinical practice and treatment guidelines.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  14/25  |  56.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-057_report.json`.

Your task: Fix ONLY the `rating_breakdown` fields in the `treatments` array.

For each treatment, verify:
1. `evidence_level.score` matches the actual study phase:
   - Phase 3 RCT (N>=500, top journal) = 9-10
   - Phase 3 RCT (N<500) = 7-8
   - Phase 2 = 5-7
   - Phase 1 = 2-4
   - Case series / retrospective = 1-3
2. `survival_benefit.score` matches actual OS delta:
   - >12 months delta = 9-10
   - 6-12 months = 7-8
   - 3-6 months = 5-6
   - 1-3 months = 3-4
   - <1 month or no control = 1-2
3. `composite_rating` = weighted average (evidence 30%, survival 30%, access 15%, safety 15%, biomarker 10%)
4. Treatments must be re-sorted descending by composite_rating after changes

Do NOT change any other field. Return the complete corrected `treatments` array only.

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
    "cancer_type": "HPV-Positive Oropharyngeal Squamous Cell Carcinoma",
    "stage": "T4aN3bM0 (AJCC 8th Edition Stage III for p16+ OPSCC)",
    "molecular_profile": [
      "HPV-positive (p16+)",
      "SMAD4 loss",
      "PIK3CA mutation",
      "Never-smoker",
      "Unfavorable risk despite HPV positivity"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Definitive Cisplatin-based Concurrent Chemoradiation (70 Gy + Cisplatin 100mg/m2 q3w)",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Multiple Phase 3 RCTs (RTOG 1016, De-ESCALaTE) confirm cisplatin-CRT as gold standard for HPV+ OPSCC; NCCN Category 1 recommendation; strongest level of evidence"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "5-year OS 84.6% with cisplatin-CRT in HPV+ OPSCC (RTOG 1016); for unfavorable T4aN3b disease, 3-year OS approximately 70-75%; de-escalation NOT appropriate for this high-volume disease"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Widely available at all radiation oncology centers; cisplatin is a generic, inexpensive agent; standard treatment infrastructure"
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Significant acute toxicity including grade 3+ mucositis (40-50%), nephrotoxicity, ototoxicity, myelosuppression; cumulative dose of 200mg/m2 target; requires aggressive supportive care"
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Standard for all HPV+ OPSCC; SMAD4 loss does not alter indication for cisplatin-CRT; PIK3CA mutation does not change primary treatment recommendation"
        }
      },
      "mechanism_of_action": "Cisplatin forms DNA adducts and cross-links that inhibit DNA replication and repair, acting as a potent radiosensitizer. Combined with 70 Gy intensity-modulated radiation therapy (IMRT) in 35 fractions, this provides definitive locoregional tumor control through synergistic cytotoxicity.",
      "key_evidence": {
        "study_name": "NRG Oncology RTOG 1016",
        "journal": "The Lancet",
        "year": 2018,
        "sample_size": 849,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0.68,
          "p_value": 0.004
        },
        "pfs_months": {
          "treatment": 0,
          "control": 0
        },
        "orr_percent": {
          "treatment": 85,
          "control": 78
        }
      },
      "biomarker_requirements": [
        "p16 positivity (HPV association)"
      ],
      "notable_side_effects": [
        "Severe mucositis (grade 3-4 in 40-50%)",
        "Nephrotoxicity",
        "Ototoxicity",
        "Myelosuppression",
        "Dysphagia",
        "Xerostomia",
        "Nausea/vomiting"
      ],
   
... (truncated — read full file from experiment_reports\HN3-057_report.json)
```
