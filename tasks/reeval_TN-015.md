# Re-evaluation Task: TN-015

## Context
- **Case ID**: TN-015
- **Cancer type**: Oral Tongue Squamous Cell Carcinoma in Renal Transplant Recipient
- **Stage**: T1N0M0 (Stage I)
- **Molecular profile**: PD-L1 CPS 30, TMB-high (>=10 mut/Mb), Immunosuppressed: tacrolimus/mycophenolate, Renal transplant recipient
- **Report file**: experiment_reports\TN-015_report.json
- **Current score**: 84/100
- **Gap analysis (local GPU)**: I can't fulfill this request.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  12/25  |  48.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (48.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-015_report.json`.

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
    "cancer_type": "Oral Tongue Squamous Cell Carcinoma in Renal Transplant Recipient",
    "stage": "T1N0M0 (Stage I)",
    "molecular_profile": [
      "PD-L1 CPS 30",
      "TMB-high (>=10 mut/Mb)",
      "Immunosuppressed: tacrolimus/mycophenolate",
      "Renal transplant recipient"
    ],
    "special_considerations": "CRITICAL DILEMMA: PD-L1 high (CPS 30) and TMB-high biomarker profile strongly predicts checkpoint inhibitor responsiveness, but PD-1/PD-L1 inhibitors cause allograft rejection in 37-50% of kidney transplant recipients with >60% of rejections progressing to graft failure. Treatment strategy must balance oncologic efficacy against graft preservation. Surgery is primary curative modality for T1N0M0. Immunosuppression modification (mTOR inhibitor switch) offers dual anti-rejection and anti-tumor benefit."
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Partial Glossectomy with Sentinel Lymph Node Biopsy or Elective Neck Dissection",
      "category": "Standard of Care — Surgery",
      "composite_rating": 9.4,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Level 1 evidence from multiple Phase 3 RCTs and NCCN/ESMO guidelines universally recommend surgery as primary treatment for T1N0M0 oral tongue SCC. Five-year OS of 97.1% for Stage I in general population."
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "Curative intent surgery for T1N0M0 achieves 5-year OS of 89-97%. Partial glossectomy preserves tongue function. SLNB or elective neck dissection for DOI >4mm reduces regional recurrence from 24% to <6%."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Universally available at all major medical centers. Standard of care worldwide. No drug access barriers."
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Well-tolerated surgical procedure. Does not require modification of immunosuppression. SLNB has lower morbidity than full neck dissection. Minimal impact on transplant graft function."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Surgery is universally applicable regardless of biomarker status. Curative for early-stage disease independent of PD-L1 or TMB status."
        }
      },
      "mechanism_of_action": "Complete surgical excision of the primary tumor with adequate margins (>5mm). Sentinel lymph node biopsy identifies occult nodal metastasis in ~25% of cN0 cases. Elective neck dissection (levels I-III) recommended if depth of invasion >4mm per NCCN guidelines. Achieves cure through physical removal of all malignant tissue.",
      "key_evidence": {
        "study_name": "NCCN Guidelines Head and Neck Cancers v2.2025 / SENT Trial (Sentinel European Node Trial)",
        "journal": "Journal of the National Comprehensive Cancer Network / European 
... (truncated — read full file from experiment_reports\TN-015_report.json)
```
