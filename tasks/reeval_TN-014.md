# Re-evaluation Task: TN-014

## Context
- **Case ID**: TN-014
- **Cancer type**: Oral Tongue Squamous Cell Carcinoma — Superficial Spreading Pattern
- **Stage**: T2N0M0 (Stage II)
- **Molecular profile**: PIK3CA mutated, SOX2 amplified, PD-L1 CPS <1
- **Report file**: experiment_reports\TN-014_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: The most critical gaps in the TN-014 cancer research report include the lack of data on Sentinel Lymph Node Biopsy (SLNB) — Alternative to, which is essential for accurately staging oral cavity cancers, and the absence of information on Cetuximab + Platinum + 5-FU (EXTREME Regimen), a potentially effective salvage regimen for recurrent or metastatic disease. Addressing these gaps will significantly improve the score by providing more comprehensive data on treatment outcomes and options for patients with specific types of oral cavity cancers, ultimately enhancing the overall quality and relevance of the research report.

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

Read the full report JSON at `experiment_reports\TN-014_report.json`.

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
    "cancer_type": "Oral Tongue Squamous Cell Carcinoma — Superficial Spreading Pattern",
    "stage": "T2N0M0 (Stage II)",
    "molecular_profile": [
      "PIK3CA mutated",
      "SOX2 amplified",
      "PD-L1 CPS <1"
    ],
    "patient_context": {
      "age": 45,
      "sex": "Male",
      "comorbidities": [
        "Rheumatoid arthritis on methotrexate (immunosuppressed)",
        "Oral lichen planus (premalignant field)"
      ],
      "tumor_characteristics": {
        "surface_extent": "8cm superficial spreading",
        "depth_of_invasion": "Superficial",
        "pattern": "Superficial spreading"
      }
    }
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Excision (Partial Glossectomy) with Free Flap Reconstruction + Elective Neck Dissection",
      "category": "Standard of Care",
      "composite_rating": 8.2,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "NCCN Category 1 recommendation for T2N0 oral cavity cancer. Surgery is the primary modality for resectable oral tongue SCC based on decades of Phase 3 data and guideline consensus. 5-year OS of 80-89% for T1-T2N0 disease."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year OS 80.8%, DFS 80.2% for T1-2N0-1 oral tongue SCC. Curative intent with high local control. Free flap reconstruction achieves wider margins (mean 7.88mm vs 5.68mm without flap) and lower recurrence rates. Elective neck dissection reduces occult metastasis risk (20-30% rate in N0 oral tongue)."
        },
        "accessibility": {
          "score": 9,
          "rationale": "Standard surgical procedure available at all major head and neck cancer centers worldwide. No regulatory barriers. Requires experienced microvascular surgeon for free flap reconstruction of the 8cm defect."
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Major surgery with significant functional morbidity for 8cm superficial resection. Free flap surgery carries risks of flap failure (2-5%), fistula, donor site morbidity. Speech and swallowing impairment expected but most recover near baseline at 1 year. Methotrexate management perioperatively is a consideration — evidence supports continuation to prevent RA flare, though some surgeons prefer 1-week hold."
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Surgery is universally applicable regardless of molecular profile. PIK3CA/SOX2 status does not contraindicate surgery. Superficial spreading pattern may actually favor surgical approach as depth of invasion is limited despite wide surface involvement."
        }
      },
      "mechanism_of_action": "Complete surgical excision of the primary tumor with adequate margins (target >5mm). For 8cm superficial spreading lesion, partial glossectomy with radial forearm or anterolateral thigh free flap re
... (truncated — read full file from experiment_reports\TN-014_report.json)
```
