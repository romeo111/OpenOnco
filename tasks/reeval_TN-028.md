# Re-evaluation Task: TN-028

## Context
- **Case ID**: TN-028
- **Cancer type**: Carcinoma ex pleomorphic adenoma (CEPA) of the parapharyngeal space
- **Stage**: Stage III (T3N1M0)
- **Molecular profile**: PLAG1 rearrangement, Ki-67 30%, HER2 negative, Malignant transformation of long-standing (20-year) pleomorphic adenoma
- **Report file**: experiment_reports\TN-028_report.json
- **Current score**: 87/100
- **Gap analysis (local GPU)**: The most critical gaps in the TN-028 cancer research report include the lack of data on Larotrectinib for NTRK Fusion-positive patients, which is a crucial treatment option that has shown significant efficacy in clinical trials, and Comprehensive Molecular Profiling (NGS) with matched cases, which would provide valuable insights into the molecular characteristics of the disease. Addressing these gaps will improve the score by providing more comprehensive and accurate data on effective treatments for specific patient populations and subtypes of cancer, respectively.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  13/25  |  52.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| rating_calibration                  |  15/15  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (52.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-028_report.json`.

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
    "cancer_type": "Carcinoma ex pleomorphic adenoma (CEPA) of the parapharyngeal space",
    "stage": "Stage III (T3N1M0)",
    "molecular_profile": [
      "PLAG1 rearrangement",
      "Ki-67 30%",
      "HER2 negative",
      "Malignant transformation of long-standing (20-year) pleomorphic adenoma"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Surgical Excision + Adjuvant Intensity-Modulated Radiation Therapy (IMRT)",
      "category": "Standard of Care",
      "composite_rating": 8.5,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Standard of care supported by NCCN guidelines for salivary gland malignancies and multiple large retrospective series. National Cancer Database analysis (n>7000) confirms adjuvant RT survival benefit. Not Phase 3 RCT due to rarity, but the highest level of evidence available for this tumor type"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "Surgery plus adjuvant RT achieves 5-year local control of 75% vs 49% with surgery alone. 5-year OS for stage III CEPA approximately 50-60% with combined modality treatment. Multi-institutional CEPA cohort shows 5-year OS of 61.7% overall; adjuvant RT significantly improves locoregional control"
        },
        "accessibility": {
          "score": 10,
          "rationale": "Standard of care available at all head and neck cancer centers worldwide. IMRT technology widely available. Parapharyngeal space resection requires experienced skull base surgeon but is performed at tertiary centers"
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Parapharyngeal space surgery carries risk of cranial nerve VII (facial nerve) and X (vagus) injury — the most common surgical complications. Possible first-bite syndrome, Frey syndrome. RT causes xerostomia, mucositis, dysphagia, osteoradionecrosis risk. Dose 60-66 Gy over 6-7 weeks"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability — surgery plus RT is indicated for all CEPA regardless of molecular profile. PLAG1 rearrangement confirms origin from pleomorphic adenoma, supporting diagnosis. Ki-67 30% indicates aggressive biology requiring adjuvant treatment"
        }
      },
      "mechanism_of_action": "Complete surgical resection removes the primary tumor and involved lymph nodes (neck dissection for N1 disease). Adjuvant IMRT delivers 60-66 Gy to the tumor bed and regional lymphatics to eradicate microscopic residual disease. IMRT allows conformal dose delivery while sparing adjacent critical structures including the contralateral parotid, brainstem, and spinal cord.",
      "key_evidence": {
        "study_name": "National Cancer Database Analysis — Adjuvant RT for Salivary Gland Malignancies",
        "journal": "Advances in Radiation Oncology",
        "year": 20
... (truncated — read full file from experiment_reports\TN-028_report.json)
```
