# Re-evaluation Task: TN-029

## Context
- **Case ID**: TN-029
- **Cancer type**: High-Risk Cutaneous Squamous Cell Carcinoma (cSCC) of the Neck with In-Transit Metastases in Renal Transplant Recipient
- **Stage**: T3N2bM0 with in-transit metastases
- **Molecular profile**: UV-signature mutational profile, TMB ultra-high (expected >20 mut/Mb), PD-L1 likely high expression, EGFR overexpression (common in cSCC), TP53 and NOTCH1 mutations expected, Immunosuppressed (renal transplant, on calcineurin inhibitor-based regimen)
- **Report file**: experiment_reports\TN-029_report.json
- **Current score**: 83/100
- **Gap analysis (local GPU)**: The most critical gaps in the TN-029 cancer research report are the lack of data on Wide Local Excision + Lymph Node Dissection + Adjuvant therapy, which is a crucial treatment approach for certain types of cancer, and the absence of sample sizes for Immunosuppression Reduction / Minimization Strategy, which could provide valuable insights into reducing side effects while maintaining efficacy. Fixing these gaps will improve the score by providing more comprehensive data on effective treatments and strategies, allowing researchers to better understand cancer outcomes and develop more targeted therapies.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  11/25  |  44.0% |
| clinical_relevance                  |   8/10  |  80.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (44.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-029_report.json`.

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
    "cancer_type": "High-Risk Cutaneous Squamous Cell Carcinoma (cSCC) of the Neck with In-Transit Metastases in Renal Transplant Recipient",
    "stage": "T3N2bM0 with in-transit metastases",
    "molecular_profile": [
      "UV-signature mutational profile",
      "TMB ultra-high (expected >20 mut/Mb)",
      "PD-L1 likely high expression",
      "EGFR overexpression (common in cSCC)",
      "TP53 and NOTCH1 mutations expected",
      "Immunosuppressed (renal transplant, on calcineurin inhibitor-based regimen)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Local Excision + Lymph Node Dissection + Adjuvant Radiation Therapy",
      "category": "Standard of Care",
      "composite_rating": 8.3,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "NCCN Category 2A recommendation for high-risk cSCC with nodal involvement. Surgery with adjuvant RT is the backbone standard of care with decades of evidence. ASTRO clinical practice guidelines endorse adjuvant RT for high-risk features including in-transit metastases."
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "1-year disease-specific survival for regional disease is approximately 89%. Adjuvant RT reduces locoregional recurrence rates to <15%. However, transplant patients have higher recurrence rates than immunocompetent patients even with aggressive local therapy."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Surgery and radiation therapy are universally available at all cancer centers. No drug approvals or trial enrollment required."
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Surgical morbidity of neck dissection is well-characterized (wound healing concerns in immunosuppressed patients). Adjuvant RT (50-60 Gy in 20-30 fractions) causes manageable acute dermatitis, dysphagia risk depending on field. No graft rejection risk."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "No biomarker requirements. Universally applicable to all cSCC patients regardless of molecular profile or transplant status."
        }
      },
      "mechanism_of_action": "Surgical excision with clear margins removes the primary tumor and involved lymph nodes. Adjuvant radiation therapy delivers targeted ionizing radiation (typically 50-66 Gy in conventional fractionation or 50 Gy in 20 hypofractionated fractions) to the tumor bed and regional nodal basin to eradicate microscopic residual disease and reduce locoregional recurrence.",
      "key_evidence": {
        "study_name": "ASTRO Clinical Practice Guideline for Definitive and Postoperative RT for BCC/SCC",
        "journal": "Practical Radiation Oncology",
        "year": 2020,
        "sample_size": 0,
        "os_months": {
          "treatment": 0,
          "control": 0,
    
... (truncated — read full file from experiment_reports\TN-029_report.json)
```
