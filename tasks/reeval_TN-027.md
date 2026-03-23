# Re-evaluation Task: TN-027

## Context
- **Case ID**: TN-027
- **Cancer type**: Poorly Differentiated Thyroid Carcinoma (PDTC)
- **Stage**: T4aN1bM0 (AJCC 8th Edition Stage II, age <55)
- **Molecular profile**: RAS mutation (driver oncogene), TERT promoter mutation (poor prognostic marker), Partially RAI-avid, Turin criteria-defined PDTC, Tracheal compression (T4a)
- **Report file**: experiment_reports\TN-027_report.json
- **Current score**: 87/100
- **Gap analysis (local GPU)**: The most critical gaps in the TN-027 cancer research report are the lack of data on Lenvatinib (Lenvima) and Sorafenib (Nexavar), as these treatments have shown promise in treating thyroid cancer, particularly for advanced stages, and filling this gap will provide more comprehensive insights into their efficacy. Additionally, the absence of data on Larotrectinib or Entrectinib for NTRK Fusion-Positive Tumors and Selpercatinib for RET Fusion-Positive Thyroid Cancer will limit the understanding of targeted therapies in specific subtypes, which is crucial for personalized treatment approaches.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  14/25  |  56.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (56.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-027_report.json`.

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
    "cancer_type": "Poorly Differentiated Thyroid Carcinoma (PDTC)",
    "stage": "T4aN1bM0 (AJCC 8th Edition Stage II, age <55)",
    "molecular_profile": [
      "RAS mutation (driver oncogene)",
      "TERT promoter mutation (poor prognostic marker)",
      "Partially RAI-avid",
      "Turin criteria-defined PDTC",
      "Tracheal compression (T4a)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Total Thyroidectomy with Central/Lateral Neck Dissection and Tracheal Decompression",
      "category": "Standard of Care",
      "composite_rating": 8.3,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Supported by NCCN, ATA 2025, and ESMO guidelines as mandatory first-line for T4a PDTC. Multiple retrospective series with >500 patients confirm improved locoregional control. Total thyroidectomy with compartment-oriented lymph node dissection is universally recommended for PDTC."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "Complete surgical resection achieves 5-year locoregional control of 81%. T4a PTC series show 5-year disease-specific survival of 96% with complete resection. For PDTC specifically, R0 resection significantly improves OS compared to R1/R2 (HR 0.45). Tracheal decompression addresses the immediate life-threatening airway compromise."
        },
        "accessibility": {
          "score": 9,
          "rationale": "Available at all tertiary referral centers and most community hospitals with endocrine surgery expertise. Should be performed at high-volume thyroid surgery center given T4a status with tracheal involvement requiring potential shave excision or window resection."
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Well-established surgical procedure. Key risks include recurrent laryngeal nerve injury (2-5% permanent), hypoparathyroidism (1-3% permanent), and wound complications. Tracheal shave/window resection adds airway-related risk but is manageable at experienced centers."
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Universal applicability regardless of molecular profile. Surgery is the essential first step enabling subsequent RAI therapy, particularly important given partial RAI-avidity. Provides tissue for molecular confirmation of RAS/TERT status."
        }
      },
      "mechanism_of_action": "Surgical extirpation of primary tumor with en-bloc removal of involved lymph nodes. Total thyroidectomy removes all thyroid tissue to enable subsequent RAI ablation. Tracheal decompression via shave excision or window resection relieves airway compromise. Central and bilateral lateral neck dissection (levels II-V) addresses N1b nodal metastases.",
      "key_evidence": {
        "study_name": "Surgical Management and Outcomes of T4a Papillary Thyroid Carcinoma",
        "journal
... (truncated — read full file from experiment_reports\TN-027_report.json)
```
