# Re-evaluation Task: HN3-026

## Context
- **Case ID**: HN3-026
- **Cancer type**: Cribriform-Morular Variant of Papillary Thyroid Carcinoma (FAP-Associated)
- **Stage**: T2N0M0, bilateral multifocal
- **Molecular profile**: APC germline mutation, BRAF wild-type, Estrogen receptor positive, Progesterone receptor positive, WNT/beta-catenin pathway activated, FAP-associated
- **Report file**: experiment_reports\HN3-026_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: The most critical gaps in the cancer research report HN3-026 are the lack of data on Active Surveillance with Thyroglobulin Monitoring, which is a crucial aspect of thyroid cancer management, and the absence of information on Lenvatinib plus Pembrolizumab Combination, a potentially effective treatment for advanced thyroid cancer. Filling these gaps will improve the score by providing more comprehensive evidence-based recommendations for thyroid cancer treatment, particularly for patients with RET fusion-positive tumors.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  12/25  |  48.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (48.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-026_report.json`.

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
    "cancer_type": "Cribriform-Morular Variant of Papillary Thyroid Carcinoma (FAP-Associated)",
    "stage": "T2N0M0, bilateral multifocal",
    "molecular_profile": [
      "APC germline mutation",
      "BRAF wild-type",
      "Estrogen receptor positive",
      "Progesterone receptor positive",
      "WNT/beta-catenin pathway activated",
      "FAP-associated"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Total Thyroidectomy with TSH Suppression Therapy",
      "category": "Standard of Care",
      "composite_rating": 9.1,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Well-established as definitive treatment for FAP-associated CMV-PTC in multiple retrospective studies; total thyroidectomy recommended over lobectomy due to bilateral multifocal disease and high risk of de novo tumors in remnant tissue"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "Over 98% overall survival and >90% disease-free survival at 10 years after total thyroidectomy; curative in majority of cases"
        },
        "accessibility": {
          "score": 10,
          "rationale": "Universally available standard surgical procedure; patient has already had prior colectomy for FAP, so surgical infrastructure is established"
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Well-tolerated procedure with manageable risks including hypoparathyroidism and recurrent laryngeal nerve injury; lifelong levothyroxine replacement required"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Directly addresses the bilateral multifocal nature of FAP-associated CMV-PTC; APC mutation drives multifocal disease requiring complete thyroidectomy"
        }
      },
      "mechanism_of_action": "Complete surgical removal of thyroid gland eliminates all tumor foci and prevents de novo tumor development in remaining thyroid tissue. Followed by TSH suppression with levothyroxine to reduce growth stimulus to any residual thyroid cancer cells via TSH receptor signaling.",
      "key_evidence": {
        "study_name": "CMV-PTC Treatment Experience - FAP vs Sporadic",
        "journal": "Endocrine Journal",
        "year": 2011,
        "sample_size": 30,
        "os_months": {
          "treatment": 120,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 120,
          "control": 0
        },
        "orr_percent": {
          "treatment": 98,
          "control": 0
        }
      },
      "biomarker_requirements": [
        "APC germline mutation confirmed"
      ],
      "notable_side_effects": [
        "Permanent hypothyroidism requiring lifelong levothyroxine",
        "Risk of hypoparathyroidism",
        "Recurrent laryngeal nerve injury risk",
        "Surgical co
... (truncated — read full file from experiment_reports\HN3-026_report.json)
```
