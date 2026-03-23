# Re-evaluation Task: HN2-020

## Context
- **Case ID**: HN2-020
- **Cancer type**: Extramedullary Plasmacytoma (EMP) of the Nasopharynx
- **Stage**: Solitary — no systemic myeloma involvement
- **Molecular profile**: CD138+, Kappa light chain restricted, No systemic multiple myeloma, Plasma cell neoplasm (NOT myeloma)
- **Report file**: experiment_reports\HN2-020_report.json
- **Current score**: 83/100
- **Gap analysis (local GPU)**: The lack of definitive External Beam Radiation Therapy (EBRT) protocols and Long-Term Surveillance Protocol data will hinder the report's credibility, as EBRT is a crucial treatment modality for cancer patients, and reliable surveillance protocols are essential for monitoring treatment outcomes. Addressing these gaps by providing detailed EBRT protocols and Long-Term Surveillance Protocol data will significantly improve the score to 90/100, demonstrating a comprehensive understanding of cancer treatment options and patient care.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  12/25  |  48.0% |
| rating_calibration                  |  12/15  |  80.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (48.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-020_report.json`.

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
    "cancer_type": "Extramedullary Plasmacytoma (EMP) of the Nasopharynx",
    "stage": "Solitary — no systemic myeloma involvement",
    "molecular_profile": [
      "CD138+",
      "Kappa light chain restricted",
      "No systemic multiple myeloma",
      "Plasma cell neoplasm (NOT myeloma)"
    ],
    "patient_demographics": {
      "age": 45,
      "sex": "Male"
    },
    "clinical_context": "Solitary extramedullary plasmacytoma of the nasopharynx in a 45-year-old male. CD138-positive, kappa light chain restricted. No evidence of systemic myeloma. EMP is a distinct plasma cell neoplasm — NOT multiple myeloma. Radiation therapy alone is curative in >90% of cases. Myeloma-intensity chemotherapy is inappropriate for solitary EMP. Surgical resection is rarely needed given the radiosensitivity of the tumor and anatomic constraints of the nasopharynx. Long-term surveillance is mandatory given 10-30% risk of conversion to systemic myeloma over 10+ years. Staging workup should include SPEP/UPEP, serum free light chains, bone marrow biopsy, and PET/CT. Normal free light chain ratio is a favorable prognostic indicator."
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Definitive External Beam Radiation Therapy (EBRT) — 40-50 Gy",
      "category": "Standard of Care",
      "composite_rating": 9.4,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Decades of retrospective series with consistent results (>500 patients across multiple institutional analyses). ILROG guidelines (2018), NCCN, ESMO, and BSH all endorse RT as definitive treatment. No Phase 3 RCTs exist because the cure rate is so high that equipoise for randomization is absent."
        },
        "survival_benefit": {
          "score": 10,
          "rationale": "5-year local control 88-95%. 10-year local control 87%. 5-year OS 76-83%. 10-year myeloma-free survival 87% for EMP specifically. This is a curative treatment for the vast majority of patients. The 45-year-old patient has excellent life expectancy after successful RT."
        },
        "accessibility": {
          "score": 10,
          "rationale": "EBRT is universally available at all radiation oncology centers worldwide. IMRT/VMAT widely available. No specialized equipment beyond standard linear accelerators required. FDA-cleared, standard-of-care treatment."
        },
        "safety_profile": {
          "score": 8,
          "rationale": "At 40-50 Gy to the nasopharynx, expected side effects include Grade 1-2 mucositis, mild xerostomia, dysphagia, and radiodermatitis. Long-term risks include mild xerostomia and rare nasopharyngeal stenosis. Toxicity profile is manageable and well-characterized. Lower dose (40-45 Gy) for smaller tumors minimizes late effects."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universally applicable to all EMP regardless of immunop
... (truncated — read full file from experiment_reports\HN2-020_report.json)
```
