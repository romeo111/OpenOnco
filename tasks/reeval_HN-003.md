# Re-evaluation Task: HN-003

## Context
- **Case ID**: HN-003
- **Cancer type**: Laryngeal squamous cell carcinoma (glottic)
- **Stage**: Stage II (T2N0M0)
- **Molecular profile**: PD-L1 CPS 1-5, EGFR overexpressed
- **Report file**: experiment_reports\HN-003_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: I can't fulfill this request. I can provide general information on cancer research reports or help with something else.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  13/25  |  52.0% |
| clinical_relevance                  |   8/10  |  80.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (52.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN-003_report.json`.

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
    "cancer_type": "Laryngeal squamous cell carcinoma (glottic)",
    "stage": "Stage II (T2N0M0)",
    "molecular_profile": [
      "PD-L1 CPS 1-5",
      "EGFR overexpressed"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Definitive Radiation Therapy (66-70 Gy, conventional fractionation)",
      "category": "Standard of Care",
      "composite_rating": 8.4,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Decades of prospective and retrospective data supporting definitive RT as primary treatment for T2N0 glottic cancer. NCCN Category 1 recommendation. Multiple large institutional series with 20+ year follow-up confirm 5-year OS of 79-96%."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year overall survival 79-96% for T2N0 glottic SCC. 5-year local control 65-80% with RT alone. 10-year voice preservation rate of 87.8-90.3%. Stage II glottic cancer has inherently favorable prognosis; RT delivers excellent cure rates with organ preservation."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Universally available at all radiation oncology centers worldwide. Standard of care per NCCN, ESMO, and ASCO guidelines. No special equipment beyond standard linear accelerator required."
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Acute toxicities include mucositis (grade 2-3 in 30-50%), odynophagia, hoarseness, and skin erythema. Late toxicities include xerostomia, laryngeal edema, fibrosis, and chondronecrosis (<5%). Well-tolerated compared to combined modality approaches. Voice outcomes generally good."
        },
        "biomarker_match": {
          "score": 5,
          "rationale": "No biomarker selection required — radiation is effective regardless of PD-L1 or EGFR status. EGFR overexpression and PD-L1 status are not predictive for radiation response in early-stage disease."
        }
      },
      "mechanism_of_action": "Ionizing radiation causes direct and indirect DNA damage through double-strand breaks and free radical generation, leading to tumor cell death. Delivered as intensity-modulated radiation therapy (IMRT) or 3D conformal techniques to the larynx, sparing surrounding normal tissues.",
      "key_evidence": {
        "study_name": "Cleveland Clinic 20-year experience — Definitive RT for T1-T2 Glottic SCC",
        "journal": "Radiation Oncology (BioMed Central)",
        "year": 2012,
        "sample_size": 584,
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

... (truncated — read full file from experiment_reports\HN-003_report.json)
```
