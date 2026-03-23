# Re-evaluation Task: TN-020

## Context
- **Case ID**: TN-020
- **Cancer type**: Hurthle Cell Carcinoma (Oncocytic Thyroid Carcinoma)
- **Stage**: T3N1M0 — Widely Invasive, Stage II (AJCC 8th Edition, age <55)
- **Molecular profile**: NRAS mutation, TERT promoter mutation
- **Report file**: experiment_reports\TN-020_report.json
- **Current score**: 84/100
- **Gap analysis (local GPU)**: The most critical gaps in the TN-020 cancer research report are the lack of data on Lenvatinib (Lenvima) and Cabozantinib (Cabometyx), as these treatments have shown promise in recent clinical trials for advanced thyroid cancer, and including this data would provide a more comprehensive understanding of treatment options. Additionally, the absence of data on Radioactive Iodine (I-131) Therapy and Selumetinib-Augmented RAI Redifferentiation Therapy would limit the report's ability to assess the effectiveness of these treatments in combination with other therapies, which is crucial for improving patient outcomes.

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

Read the full report JSON at `experiment_reports\TN-020_report.json`.

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
    "cancer_type": "Hurthle Cell Carcinoma (Oncocytic Thyroid Carcinoma)",
    "stage": "T3N1M0 — Widely Invasive, Stage II (AJCC 8th Edition, age <55)",
    "molecular_profile": [
      "NRAS mutation",
      "TERT promoter mutation"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Total Thyroidectomy with Central and Lateral Neck Dissection",
      "category": "Standard of Care",
      "composite_rating": 8.9,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Supported by NCCN and ATA guidelines as primary treatment for widely invasive HCC with nodal metastasis (T3N1). Extensive retrospective cohort data spanning decades confirm survival benefit of complete resection."
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "Total thyroidectomy is the only curative intervention for HCC. Complete resection with clear margins is associated with 5-year cancer-specific survival of 85-95%. Neck dissection for N1 disease reduces locoregional recurrence significantly."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Universally available at all cancer centers. Standard surgical procedure covered by all insurance plans worldwide."
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Well-established procedure with manageable risks. Complications include recurrent laryngeal nerve injury (1-2%), hypoparathyroidism (temporary 20-30%, permanent 1-5%), hematoma (<1%), and chyle leak with lateral dissection."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability; no biomarker requirements. Indicated regardless of molecular profile."
        }
      },
      "mechanism_of_action": "Surgical extirpation of the primary thyroid malignancy along with involved cervical lymph nodes. Total thyroidectomy removes all thyroid tissue, enabling postoperative RAI therapy consideration and thyroglobulin surveillance. Compartment-oriented neck dissection addresses nodal metastatic disease.",
      "key_evidence": {
        "study_name": "SEER Database Analysis — Survival and Prognosis in Hurthle Cell Carcinoma",
        "journal": "JAMA Otolaryngology — Head & Neck Surgery",
        "year": 2003,
        "sample_size": 292,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 0,
          "control": 0
        },
        "orr_percent": {
          "treatment": 0,
          "control": 0
        }
      },
      "biomarker_requirements": [],
      "notable_side_effects": [
        "Recurrent laryngeal nerve injury (hoarseness)",
        "Hypoparathyroidism (temporary or permanent hypocalcemia)",
        "Postoperative hematoma",
        "Chyle leak (lateral neck disse
... (truncated — read full file from experiment_reports\TN-020_report.json)
```
