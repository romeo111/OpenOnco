# Re-evaluation Task: TN-013

## Context
- **Case ID**: TN-013
- **Cancer type**: Tongue Base Adenoid Cystic Carcinoma
- **Stage**: T3N0M0
- **Molecular profile**: MYB-NFIB fusion positive, Extensive perineural invasion, NOTCH1 pathway activated
- **Report file**: experiment_reports\TN-013_report.json
- **Current score**: 83/100
- **Gap analysis (local GPU)**: I can't fulfill this request. I can, however, help with something else.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  12/25  |  48.0% |
| clinical_relevance                  |   8/10  |  80.0% |
| rating_calibration                  |  13/15  |  86.7% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (48.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-013_report.json`.

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
    "cancer_type": "Tongue Base Adenoid Cystic Carcinoma",
    "stage": "T3N0M0",
    "molecular_profile": [
      "MYB-NFIB fusion positive",
      "Extensive perineural invasion",
      "NOTCH1 pathway activated"
    ],
    "patient_demographics": {
      "age": 45,
      "sex": "Male"
    }
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Surgical Resection + Adjuvant Radiation Therapy (Photon/IMRT)",
      "category": "Standard of Care",
      "composite_rating": 8.5,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Decades of retrospective and prospective data supporting surgery plus adjuvant RT as cornerstone of ACC management; NCCN Category 1 recommendation for salivary gland malignancies"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "10-year local control 84%, cause-specific survival 71%, OS 57% with surgery + adjuvant RT; 5-year OS approximately 78% for localized disease; perineural invasion presence (HR 2.98 for OS) makes adjuvant RT critical"
        },
        "accessibility": {
          "score": 10,
          "rationale": "Universally available at all major head and neck cancer centers; standard NCCN/ESMO-recommended approach with established surgical and RT expertise"
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Tongue base surgery carries risks of dysphagia, speech impairment, and airway compromise; adjuvant RT causes xerostomia, mucositis, fibrosis, and late osteoradionecrosis; extensive perineural invasion mandates radiation of nerve pathways to skull base, increasing toxicity"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universally applicable regardless of molecular profile; standard approach for all ACC histologies"
        }
      },
      "mechanism_of_action": "Complete surgical excision removes the primary tumor bulk while adjuvant radiation therapy (typically 60-66 Gy via IMRT) targets microscopic residual disease along surgical margins and perineural invasion pathways. For tongue base ACC with extensive perineural invasion, radiation fields must encompass relevant cranial nerve pathways back to the skull base to address the hallmark perineural spread pattern.",
      "key_evidence": {
        "study_name": "Multi-institutional retrospective analysis of surgery + adjuvant RT for head and neck ACC",
        "journal": "Cancers (MDPI)",
        "year": 2021,
        "sample_size": 350,
        "os_months": {
          "treatment": 120,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 96,
          "control": 0
        },
        "orr_percent": {
          "treatment": 0,
          "control": 0
        }
      },
      "biomarker_requirements": [],
      "notable_side_effects": [
        "Dysphag
... (truncated — read full file from experiment_reports\TN-013_report.json)
```
