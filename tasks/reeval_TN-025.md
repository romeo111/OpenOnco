# Re-evaluation Task: TN-025

## Context
- **Case ID**: TN-025
- **Cancer type**: Carotid Body Paraganglioma (Shamblin Class III, ICA Encasement)
- **Stage**: Locally advanced — Shamblin III encasing internal carotid artery
- **Molecular profile**: SDHB germline mutation positive, Non-secretory (no catecholamine excess), Neuroendocrine tumor (NOT carcinoma), High malignant potential due to SDHB
- **Report file**: experiment_reports\TN-025_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: The lack of data on Stereotactic Radiosurgery / Fractionated Stereotac and Surgical Resection with Vascular Reconstruction (SVR) will hinder the report's comprehensiveness, as these treatments are crucial for glioblastoma patients and their inclusion is essential to provide a complete picture of treatment options. Filling in these gaps will improve the score by providing more accurate information on effective treatments for this specific type of cancer, allowing for more informed decision-making for patients and researchers alike.

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

Read the full report JSON at `experiment_reports\TN-025_report.json`.

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
    "cancer_type": "Carotid Body Paraganglioma (Shamblin Class III, ICA Encasement)",
    "stage": "Locally advanced — Shamblin III encasing internal carotid artery",
    "molecular_profile": [
      "SDHB germline mutation positive",
      "Non-secretory (no catecholamine excess)",
      "Neuroendocrine tumor (NOT carcinoma)",
      "High malignant potential due to SDHB"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Stereotactic Radiosurgery / Fractionated Stereotactic Radiotherapy (SRS/FSRT)",
      "category": "Standard of Care — Radiation",
      "composite_rating": 8.3,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "Multiple retrospective series and systematic reviews/meta-analyses with >400 patients; 94-100% local control at 5-10 years; no RCT but paraganglioma rarity precludes this"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "Local control rate of 94-100% with tumor stabilization or shrinkage in majority; avoids catastrophic stroke risk of Shamblin III surgery; disease-specific survival exceeds 95% at 10 years"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Widely available at radiation oncology centers with Gamma Knife or LINAC-based SRS/SBRT capability; no FDA approval needed as it is a radiation modality"
        },
        "safety_profile": {
          "score": 9,
          "rationale": "Minimal cranial nerve injury (<5%); no stroke risk; no ICA manipulation; late toxicity rare; avoids 39-63% cranial nerve deficit rate of Shamblin III surgery"
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Effective regardless of SDH mutation status; SDH-related paragangliomas show aggregate 100% local control with SRS in recent series"
        }
      },
      "mechanism_of_action": "Delivers focused high-dose radiation to the tumor in 1-5 fractions, causing DNA double-strand breaks and delayed tumor cell death. Paragangliomas are slow-growing, so local control (tumor stabilization) rather than shrinkage is the primary endpoint. Tumor shrinkage may continue for years after treatment.",
      "key_evidence": {
        "study_name": "Stereotactic radiosurgery for head and neck paragangliomas: systematic review and meta-analysis",
        "journal": "Neurosurgical Review",
        "year": 2020,
        "sample_size": 418,
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
          "treatment": 94,
          "control": 0
        }
      },
      "biomarker_requirements": [
        "None required; effective across all genotypes including SDHB"
      ],
      "notable_side_effects": [
        "Transient cranial ner
... (truncated — read full file from experiment_reports\TN-025_report.json)
```
