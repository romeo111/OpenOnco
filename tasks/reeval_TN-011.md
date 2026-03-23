# Re-evaluation Task: TN-011

## Context
- **Case ID**: TN-011
- **Cancer type**: Oral tongue mucosal melanoma
- **Stage**: T3N0M0, 4mm thickness
- **Molecular profile**: BRAF wild-type, NRAS Q61K mutated, KIT amplified (not mutated), PD-L1 TPS 30%
- **Report file**: experiment_reports\TN-011_report.json
- **Current score**: 86/100
- **Gap analysis (local GPU)**: The most critical gaps in TN-011's research report are the lack of data on Adjuvant Postoperative Radiation Therapy (IMRT/Proton) and Temozolomide (Cytotoxic Chemotherapy), as these treatments are crucial for improving outcomes in surgical excision of brain tumors. Addressing these gaps will improve the score by providing more comprehensive evidence on the effectiveness of radiation therapy and chemotherapy in combination with surgery, which is essential for optimizing treatment strategies for patients with brain cancer.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  14/25  |  56.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (56.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-011_report.json`.

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
    "cancer_type": "Oral tongue mucosal melanoma",
    "stage": "T3N0M0, 4mm thickness",
    "molecular_profile": [
      "BRAF wild-type",
      "NRAS Q61K mutated",
      "KIT amplified (not mutated)",
      "PD-L1 TPS 30%"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Surgical Excision with Negative Margins",
      "category": "Standard of Care",
      "composite_rating": 7.9,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "Multiple large retrospective series and NCCN/ESMO guidelines establish surgery as first-line curative intent. No RCTs possible given rarity, but consistent Level 2A evidence from institutional series of 100-160+ patients showing surgery is the only curative modality"
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "Complete resection with negative margins is the strongest predictor of survival. 5-year OS 20-35% in resectable disease vs <10% without surgery. T3N0M0 with 4mm thickness has moderate risk; clear margins improve local control by 40-50% vs positive margins"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Available at all tertiary head and neck surgical centers. Requires experienced head and neck or oromaxillofacial surgeon. Oral tongue location permits adequate access though reconstruction may be needed for large defects"
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Operative morbidity includes speech/swallowing impairment depending on excision extent, wound healing complications, and flap failure risk if reconstruction needed. Generally well-tolerated in 45-year-old with good performance status"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability — surgery does not depend on molecular profile. Appropriate for all mucosal melanoma patients with resectable disease regardless of BRAF/NRAS/KIT status"
        }
      },
      "mechanism_of_action": "Complete surgical excision removes the primary tumor with wide margins (target >=1cm where anatomically feasible) to eliminate all malignant cells. In oral tongue location, may require partial glossectomy with or without free flap reconstruction depending on defect size.",
      "key_evidence": {
        "study_name": "Long-term treatment outcomes of mucosal melanoma of the head and neck: 161 cases (Jethanamest et al.)",
        "journal": "Annals of Surgical Oncology",
        "year": 2017,
        "sample_size": 161,
        "os_months": {
          "treatment": 25,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 14,
          "control": 0
        },
        "orr_percent": {
          "treatment": 0,
          "control": 0
        }
      },
      "biomarker_requirements": [],

... (truncated — read full file from experiment_reports\TN-011_report.json)
```
