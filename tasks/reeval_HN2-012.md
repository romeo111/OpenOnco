# Re-evaluation Task: HN2-012

## Context
- **Case ID**: HN2-012
- **Cancer type**: Submandibular Gland Adenoid Cystic Carcinoma
- **Stage**: T3N0M0 (AJCC Stage III)
- **Molecular profile**: MYB-NFIB fusion positive, Perineural invasion along lingual nerve (V3), NOTCH1 wild-type
- **Report file**: experiment_reports\HN2-012_report.json
- **Current score**: 87/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN2-012 cancer research report include the lack of data on Adjuvant Proton Beam Therapy with Perineural Pathway and Lenvatinib (Lenvima) for Recurrent/Metastatic Disease, which will improve the score by providing more comprehensive information on innovative treatments for head and neck cancers. Filling these gaps will enable a more thorough evaluation of treatment efficacy and potential outcomes, ultimately enhancing the overall credibility and reliability of the report.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  15/25  |  60.0% |
| clinical_relevance                  |   8/10  |  80.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (60.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-012_report.json`.

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
    "cancer_type": "Submandibular Gland Adenoid Cystic Carcinoma",
    "stage": "T3N0M0 (AJCC Stage III)",
    "molecular_profile": [
      "MYB-NFIB fusion positive",
      "Perineural invasion along lingual nerve (V3)",
      "NOTCH1 wild-type"
    ],
    "patient_demographics": {
      "age": 45,
      "sex": "Male"
    },
    "case_id": "HN2-012",
    "disclaimer": "This document is generated for research and educational purposes only. It is NOT medical advice. All treatment decisions must be made in consultation with a qualified oncology team who can evaluate the patient's individual circumstances. Never start, stop, or change treatment based solely on this document."
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Radical Surgical Resection with Lingual Nerve Tracing and Negative Margin Clearance",
      "category": "Standard of Care",
      "composite_rating": 8.5,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Surgery is the cornerstone of ACC management per NCCN v1.2026 and ASCO salivary gland guidelines. Level I evidence from multiple large retrospective series (>1000 patients cumulative) confirming radical surgery with margin-negative resection as primary treatment."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "Complete resection with negative margins associated with 5-year OS of 82-90%. For T3 disease, R0 resection yields 5-year local-regional control of 70-80%. However, the perineural invasion along the lingual nerve mandates nerve tracing at surgery back toward foramen ovale to ensure complete extirpation."
        },
        "accessibility": {
          "score": 9,
          "rationale": "Available at all major head and neck surgical centers. Requires experienced head and neck surgeon capable of skull base approaches for nerve tracing along V3 pathway."
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Expected morbidity includes lingual nerve sacrifice with tongue numbness/taste loss on affected side, possible marginal mandibular nerve injury. Hypoglossal nerve (XII) at risk given submandibular location. Functional rehabilitation feasible with speech therapy."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability regardless of molecular profile. MYB-NFIB fusion status does not alter surgical approach. All T3N0M0 ACC patients are surgical candidates."
        }
      },
      "mechanism_of_action": "Complete surgical excision of the primary tumor with en-bloc resection of the submandibular gland, floor of mouth contents, and tracing of the lingual nerve (V3 branch) proximally toward the skull base to achieve negative neural margins. In ACC with perineural invasion along a named nerve, intraoperative frozen section of the proximal nerve stump is critical to confirm clearance
... (truncated — read full file from experiment_reports\HN2-012_report.json)
```
