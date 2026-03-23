# Re-evaluation Task: HN3-047

## Context
- **Case ID**: HN3-047
- **Cancer type**: Parotid Collision Tumor — Warthin Tumor with Incidental Low-Grade Mucoepidermoid Carcinoma
- **Stage**: T1N0M0 (Stage I, AJCC 8th edition)
- **Molecular profile**: CRTC1-MAML2 fusion positive, Low-grade mucoepidermoid carcinoma, Incidental finding within Warthin tumor
- **Report file**: experiment_reports\HN3-047_report.json
- **Current score**: 66/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN3-047 cancer research report are the lack of sample size data for Partial Parotidectomy Alone (If Initial Margins Adjuvant) and Active Surveillance with Serial Imaging (If Margin Status Unknown), which will improve the score by providing more accurate and reliable data on treatment outcomes. Fixing these gaps will enable researchers to better understand the efficacy and safety of these treatments, ultimately leading to more informed decision-making and improved patient care.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |   9/25  |  36.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| combo_supportive_coverage           |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-047_report.json`.

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
    "cancer_type": "Parotid Collision Tumor — Warthin Tumor with Incidental Low-Grade Mucoepidermoid Carcinoma",
    "stage": "T1N0M0 (Stage I, AJCC 8th edition)",
    "molecular_profile": [
      "CRTC1-MAML2 fusion positive",
      "Low-grade mucoepidermoid carcinoma",
      "Incidental finding within Warthin tumor"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Completion Superficial Parotidectomy with Facial Nerve Preservation",
      "category": "Standard of Care — Surgery",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "ASCO Guideline (JCO 2021) recommends complete surgical excision as primary treatment for resectable salivary gland cancers. NCCN 2025 guidelines support superficial parotidectomy for T1-2 low-grade parotid cancers. Mayo Clinic 20-year experience (JAMA Otolaryngology) confirmed excellent outcomes for low-grade MEC with adequate resection. 100% locoregional control at 74 months."
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "5-year survival rate for low-grade MEC is 98.8%. T1N0M0 low-grade MEC with CRTC1-MAML2 fusion has the most favorable prognosis in all salivary gland malignancies. Near-curative with surgery alone. Recurrence rate after complete excision is extremely low (<2%)."
        },
        "accessibility": {
          "score": 9,
          "rationale": "Standard procedure at any head and neck surgical center. If initial surgery was partial parotidectomy for Warthin tumor, completion superficial parotidectomy ensures adequate margins. Well-established technique with intraoperative facial nerve monitoring widely available."
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Facial nerve preservation achievable in vast majority of low-grade T1 tumors. Temporary facial nerve weakness in 10-30%, permanent dysfunction in <5%. Frey syndrome (gustatory sweating) 5-15%. Scar morbidity. Lower morbidity than total parotidectomy. Re-operation in previously dissected field may increase nerve injury risk slightly."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Surgery is universally applicable. CRTC1-MAML2 fusion positivity confirms low-grade biology and excellent surgical curability. Molecular profile supports conservative surgical approach without need for aggressive resection."
        }
      },
      "mechanism_of_action": "Complete superficial parotidectomy removes all parotid tissue lateral to the facial nerve plane, ensuring complete excision of any residual MEC after initial partial parotidectomy for Warthin tumor. Facial nerve is identified and preserved. Provides adequate margins for T1 low-grade MEC while definitively treating the Warthin tumor component.",
      "key_evidence": {
        "study_name": "Oncological Efficacy of Partial Parotid
... (truncated — read full file from experiment_reports\HN3-047_report.json)
```
