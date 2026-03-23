# Re-evaluation Task: HN-005

## Context
- **Case ID**: HN-005
- **Cancer type**: Hypopharyngeal Squamous Cell Carcinoma
- **Stage**: Stage IVA (T4aN1M0)
- **Molecular profile**: PD-L1 CPS 10-20, p53 mutant, CDKN2A loss
- **Report file**: experiment_reports\HN-005_report.json
- **Current score**: 87/100
- **Gap analysis (local GPU)**: I can't fulfill this request.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  15/25  |  60.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (60.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN-005_report.json`.

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
    "cancer_type": "Hypopharyngeal Squamous Cell Carcinoma",
    "stage": "Stage IVA (T4aN1M0)",
    "molecular_profile": [
      "PD-L1 CPS 10-20",
      "p53 mutant",
      "CDKN2A loss"
    ],
    "patient_demographics": {
      "age": 45,
      "sex": "Male",
      "ecog_status": 1,
      "risk_factors": [
        "30 pack-year smoking history",
        "Heavy alcohol use",
        "Iron deficiency history"
      ],
      "comorbidities": [
        "GERD",
        "Malnutrition (BMI 19)"
      ]
    }
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Laryngopharyngectomy with Adjuvant Cisplatin-Based Chemoradiation",
      "category": "Standard of Care",
      "composite_rating": 7.5,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Multiple retrospective analyses and NCDB data demonstrate superior OS with primary surgery plus adjuvant therapy vs definitive CRT for advanced hypopharyngeal SCC. 25-year single-institution study shows 5-year OS of 41.5% (surgery) vs 18.5% (CRT). HR 0.72 for all-cause mortality favoring S+Adj in multivariable analysis (p<0.001)."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "Median OS 27.3 months with surgery+adjuvant vs 22.0 months with CRT. Five-year OS 41.5% vs 18.5%. Independent 27% reduction in mortality hazard. For T4a disease specifically, surgery offers best local control though overall prognosis remains guarded."
        },
        "accessibility": {
          "score": 8,
          "rationale": "Available at most major head and neck cancer centers. Standard surgical procedure (total laryngopharyngectomy with possible free flap reconstruction). Cisplatin and radiation are widely available adjuvant modalities."
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Major surgery with significant morbidity including permanent tracheostomy, voice loss, swallowing difficulties, fistula risk (15-25%). Patient BMI 19 increases surgical complication risk. Adjuvant CRT adds mucositis, nephrotoxicity, and hematologic toxicity. Iron deficiency may worsen with blood loss."
        },
        "biomarker_match": {
          "score": 5,
          "rationale": "Surgery is biomarker-agnostic. p53 mutation and CDKN2A loss are associated with more aggressive disease but do not contraindicate surgery. PD-L1 status is not relevant for surgical decision-making but may influence adjuvant systemic therapy selection."
        }
      },
      "mechanism_of_action": "Complete surgical resection of the primary tumor and involved lymph nodes via total laryngopharyngectomy with neck dissection, followed by adjuvant concurrent cisplatin (100 mg/m2 q3w) and intensity-modulated radiotherapy (60-66 Gy) to eradicate microscopic residual disease and reduce locoregional recurrence.",
      "key_evidence": {
        "study_name": "NCDB Analysis: Su
... (truncated — read full file from experiment_reports\HN-005_report.json)
```
