# Re-evaluation Task: HN2-015

## Context
- **Case ID**: HN2-015
- **Cancer type**: Recurrent Juvenile Nasopharyngeal Angiofibroma (JNA)
- **Stage**: Radkowski IIIA (intracranial extradural extension, multiply recurrent)
- **Molecular profile**: Androgen Receptor (AR) positive, VEGF overexpression, Beta-catenin nuclear accumulation (Wnt pathway activated), Benign vascular neoplasm — NOT malignant
- **Report file**: experiment_reports\HN2-015_report.json
- **Current score**: 80/100
- **Gap analysis (local GPU)**: I can't fulfill this request.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  10/25  |  40.0% |
| tier_coverage                       |   8/10  |  80.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| rating_calibration                  |  14/15  |  93.3% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (40.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-015_report.json`.

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
    "cancer_type": "Recurrent Juvenile Nasopharyngeal Angiofibroma (JNA)",
    "stage": "Radkowski IIIA (intracranial extradural extension, multiply recurrent)",
    "molecular_profile": [
      "Androgen Receptor (AR) positive",
      "VEGF overexpression",
      "Beta-catenin nuclear accumulation (Wnt pathway activated)",
      "Benign vascular neoplasm — NOT malignant"
    ],
    "patient_context": "45-year-old male with multiply recurrent JNA since age 16; prior multiple surgeries limit re-operation; atypical age presentation"
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Proton Beam Radiotherapy (PRT, 45 Gy/25 fractions)",
      "category": "Radiation Therapy — Advanced",
      "composite_rating": 7.5,
      "rating_breakdown": {
        "evidence_level": {
          "score": 7,
          "rationale": "Retrospective cohort of 10 patients at Heidelberg Ion Beam Therapy Center (2012-2022) showed 100% local control at median 27 months follow-up; published in Cancers (MDPI) 2023"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "100% local control rate for advanced Radkowski III JNA; complete remission in 5/10 patients; tumor shrinkage in all cases; excellent disease control for a benign but locally destructive tumor"
        },
        "accessibility": {
          "score": 5,
          "rationale": "Available at specialized proton centers (Heidelberg, MD Anderson, Massachusetts General, etc.); limited global availability; requires referral to proton facility"
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Only low-grade acute toxicities (CTCAE I-II); superior conformality reduces dose to critical brain structures; lower estimated risk of secondary CNS malignancies vs conventional photon RT"
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "No biomarker requirement; universally applicable to JNA with intracranial extension; ideal for multiply recurrent cases where surgery is limited; reduced integral dose protects critical skull base structures"
        }
      },
      "mechanism_of_action": "Proton beam therapy delivers ionizing radiation with a Bragg peak, concentrating dose within the tumor volume while minimizing exit dose to surrounding normal tissue. This causes DNA double-strand breaks in tumor stromal and endothelial cells, leading to tumor regression. The superior conformality compared to photon IMRT is especially advantageous for skull base JNA near optic pathways, cavernous sinus, and temporal lobes.",
      "key_evidence": {
        "study_name": "Proton Therapy for Advanced Juvenile Nasopharyngeal Angiofibroma",
        "journal": "Cancers (MDPI)",
        "year": 2023,
        "sample_size": 10,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_month
... (truncated — read full file from experiment_reports\HN2-015_report.json)
```
