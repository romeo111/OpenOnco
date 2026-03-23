# Re-evaluation Task: HN2-013

## Context
- **Case ID**: HN2-013
- **Cancer type**: Merkel Cell Carcinoma (MCC) of the Head and Neck
- **Stage**: T2N1bM0 with in-transit metastases
- **Molecular profile**: MCPyV-positive (Merkel cell polyomavirus), PD-L1 50% (high expression), Neuroendocrine differentiation, Concurrent CLL on ibrutinib (BTK inhibitor)
- **Report file**: experiment_reports\HN2-013_report.json
- **Current score**: 84/100
- **Gap analysis (local GPU)**: The lack of data on Adjuvant Pembrolizumab (Post-Resection Immunotherapy) and Definitive Radiation Therapy Alone (Non-Surgical Postoperative Treatment) are critical gaps that need to be addressed, as they represent key areas for improving the treatment outcomes and survival rates for patients with cancer. Filling these knowledge gaps will significantly improve the score by providing more comprehensive evidence-based information on the effectiveness of these treatments in specific patient populations.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  12/25  |  48.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (48.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-013_report.json`.

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
    "cancer_type": "Merkel Cell Carcinoma (MCC) of the Head and Neck",
    "stage": "T2N1bM0 with in-transit metastases",
    "molecular_profile": [
      "MCPyV-positive (Merkel cell polyomavirus)",
      "PD-L1 50% (high expression)",
      "Neuroendocrine differentiation",
      "Concurrent CLL on ibrutinib (BTK inhibitor)"
    ],
    "patient_demographics": {
      "age": 45,
      "sex": "Male",
      "comorbidities": [
        "Chronic Lymphocytic Leukemia (CLL) on ibrutinib",
        "Immunosuppression secondary to CLL and BTK inhibitor therapy"
      ]
    },
    "special_considerations": [
      "Dual malignancy coordination required between MCC and CLL management teams",
      "CLL-associated immunosuppression significantly worsens MCC outcomes (ORR 20% vs 61.5% in non-immunosuppressed, HR 4.09 for progression)",
      "Ibrutinib may paradoxically enhance checkpoint inhibitor efficacy via ITK inhibition and Th1/Th2 rebalancing",
      "MCPyV-positive status generally predicts favorable immunotherapy response but CLL immunosuppression may attenuate this benefit",
      "PD-L1 50% expression supports checkpoint inhibitor candidacy",
      "In-transit metastases require consideration of regional therapies (RT, intralesional approaches)",
      "Head/neck location necessitates careful radiation planning to spare critical structures"
    ],
    "disclaimer": "MEDICAL DISCLAIMER: This document is generated for research and educational purposes only. It is NOT medical advice. All treatment decisions must be made in consultation with a qualified oncology team including both dermatologic/surgical oncology and hematology/oncology specialists who can evaluate the patient's individual circumstances. Never start, stop, or change treatment based solely on this document."
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Pembrolizumab (Keytruda) - First-Line Anti-PD-1 Monotherapy",
      "category": "Immunotherapy - Standard of Care",
      "composite_rating": 8.1,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Phase III KEYNOTE-913 (n=55) and Phase II KEYNOTE-017 (n=50) provide robust evidence. ORR 49-56% first-line with durable responses (median DOR 39.8 months). FDA approved December 2018 for recurrent locally advanced or metastatic MCC."
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "Median OS 24.3 months in KEYNOTE-913. 2-year PFS 39%, 2-year OS 51%. MCPyV+ patients had ORR of 59-62% in KEYNOTE-017. However, CLL immunosuppression dramatically reduces response (ORR drops to ~20% in CLL patients per Seattle registry data), tempering expected benefit."
        },
        "accessibility": {
          "score": 10,
          "rationale": "FDA approved for first-line recurrent locally advanced or metastatic MCC. Widely available at oncology centers. Well-established dosing protocol (200mg 
... (truncated — read full file from experiment_reports\HN2-013_report.json)
```
