# Re-evaluation Task: TN-030

## Context
- **Case ID**: TN-030
- **Cancer type**: Nodal Marginal Zone Lymphoma (NMZL) of the Neck
- **Stage**: Stage II (bilateral cervical nodes)
- **Molecular profile**: CD20+, BCL2+, t(11;18) negative, Sjogren's syndrome-associated
- **Report file**: experiment_reports\TN-030_report.json
- **Current score**: 84/100
- **Gap analysis (local GPU)**: The lack of data on Rituximab Monotherapy and Rituximab + ISRT Combined Modality Therapy will hinder the understanding of treatment efficacy and optimal dosing, which is crucial for improving patient outcomes and increasing the overall score. Additionally, the absence of sample sizes for Active Surveillance (Watch-and-Wait) and Bendamustine plus Rituximab (BR) therapies will limit the ability to assess their safety and effectiveness, further impacting the report's credibility and accuracy.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  11/25  |  44.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (44.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-030_report.json`.

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
    "cancer_type": "Nodal Marginal Zone Lymphoma (NMZL) of the Neck",
    "stage": "Stage II (bilateral cervical nodes)",
    "molecular_profile": [
      "CD20+",
      "BCL2+",
      "t(11;18) negative",
      "Sjogren's syndrome-associated"
    ],
    "patient_demographics": {
      "age": 45,
      "sex": "Male",
      "comorbidities": [
        "Sjogren's syndrome"
      ]
    }
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Involved-Site Radiation Therapy (ISRT) 24-30 Gy",
      "category": "Standard of Care",
      "composite_rating": 8.9,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "NCCN Category 2A recommendation for localized (Stage I-II) nodal MZL. Extensive retrospective data with consistent results across multiple institutions. ILROG guidelines standardize the approach. 5-year DFS 74%, OS 97% in localized MZL."
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "Exceptional outcomes for localized disease: 5-year OS 97%, 5-year DFS 74%, CR rate 99% (87/88 patients). In-field recurrence rate extremely low at 2.4% at 5 years and 4.7% at 10 years. For Stage II bilateral cervical nodes, curative intent is realistic."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Widely available at all radiation oncology centers. Standard of care for localized MZL per NCCN, ESMO, and BSH guidelines. No special equipment beyond standard linear accelerator required."
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Low-dose ISRT (24 Gy) is well-tolerated with minimal acute toxicity. Cervical radiation may cause temporary mucositis, xerostomia (concerning given existing Sjogren's dryness), and fatigue. Long-term risks include secondary malignancy but are low at these doses."
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Radiation is effective regardless of biomarker profile. t(11;18) negative status is associated with better local control. Localized bilateral cervical disease is amenable to involved-site technique. Stage II is within curative RT range."
        }
      },
      "mechanism_of_action": "Ionizing radiation induces DNA double-strand breaks in lymphoma cells, leading to apoptosis and cell death. ISRT targets the involved nodal regions with a margin for microscopic disease while minimizing exposure to uninvolved tissue. Low-dose (24 Gy) is sufficient for indolent lymphomas due to their high radiosensitivity.",
      "key_evidence": {
        "study_name": "ILROG ISRT Guidelines / Multi-institutional retrospective series",
        "journal": "International Journal of Radiation Oncology, Biology, Physics",
        "year": 2020,
        "sample_size": 88,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
          "p_value
... (truncated — read full file from experiment_reports\TN-030_report.json)
```
