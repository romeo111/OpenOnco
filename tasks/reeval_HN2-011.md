# Re-evaluation Task: HN2-011

## Context
- **Case ID**: HN2-011
- **Cancer type**: Parotid Acinic Cell Carcinoma with High-Grade Transformation
- **Stage**: T3N1M0 (Stage III/IVA)
- **Molecular profile**: NR4A3 rearrangement (confirmatory for acinic cell carcinoma origin), Ki-67 proliferative index 40% (consistent with high-grade transformation), High-grade transformation (dedifferentiation) component, Facial nerve involvement (perineural invasion), Prior parotid surgery 8 years ago (scarred operative field)
- **Report file**: experiment_reports\HN2-011_report.json
- **Current score**: 86/100
- **Gap analysis (local GPU)**: The most critical gaps in the cancer research report HN2-011 include the lack of data on Adjuvant Intensity-Modulated Radiation Therapy (IMRT) and Proton Beam Radiation Therapy, which are crucial for understanding the effectiveness of radiation therapy in treating parotid gland cancers. Filling these gaps will improve the score by providing more comprehensive information on treatment options and outcomes, allowing researchers to better understand the role of IMRT and proton beam radiation therapy in improving patient survival rates and quality of life.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  13/25  |  52.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (52.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-011_report.json`.

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
    "cancer_type": "Parotid Acinic Cell Carcinoma with High-Grade Transformation",
    "stage": "T3N1M0 (Stage III/IVA)",
    "molecular_profile": [
      "NR4A3 rearrangement (confirmatory for acinic cell carcinoma origin)",
      "Ki-67 proliferative index 40% (consistent with high-grade transformation)",
      "High-grade transformation (dedifferentiation) component",
      "Facial nerve involvement (perineural invasion)",
      "Prior parotid surgery 8 years ago (scarred operative field)"
    ],
    "patient_demographics": {
      "age": 45,
      "sex": "Male",
      "relevant_history": "Prior parotid surgery 8 years ago; recurrent/transformed disease in previously operated field"
    }
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Radical Revision Parotidectomy with Facial Nerve Sacrifice and Ipsilateral Neck Dissection",
      "category": "Standard of Care — Surgery",
      "composite_rating": 7.4,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "NCCN, ASCO, and ESMO guidelines uniformly recommend complete surgical resection as primary treatment for salivary gland malignancies. For T3N1 high-grade tumors, total parotidectomy with sacrifice of involved facial nerve branches and formal neck dissection (levels I-V or selective levels I-III) is standard. Evidence from large retrospective series (REFCOR study, n=187; PMC4838973, n=25 HGT cases) consistently supports aggressive surgery."
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "Surgery is the cornerstone of curative intent. In the PMC4838973 series, 3/25 (12%) HGT patients achieved long-term disease-free survival (mean 7.3 years), all through complete surgical excision. 5-year OS after salvage parotidectomy for recurrent disease reported at 66.7% in one series. However, 86% of HGT patients recur despite aggressive surgery, and median survival remains 2.2 years for HGT-AcCC."
        },
        "accessibility": {
          "score": 9,
          "rationale": "Widely available at head and neck surgical centers. Re-operation in scarred field requires experienced head and neck surgeon, ideally at high-volume center with microsurgical capability for nerve grafting. Simultaneously available at most academic medical centers."
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Re-operation in previously operated parotid field carries increased risk: distorted anatomy, fibrosis, higher facial nerve injury rate, increased bleeding risk, wound complications, Frey syndrome. Facial nerve sacrifice results in complete ipsilateral facial paralysis (House-Brackmann VI). Additional morbidity from neck dissection includes shoulder dysfunction, lymphedema, chyle leak."
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "NR4A3 rearrangement confirms acinic cell origin, supporti
... (truncated — read full file from experiment_reports\HN2-011_report.json)
```
