# Re-evaluation Task: TN-012

## Context
- **Case ID**: TN-012
- **Cancer type**: Synchronous Oral Tongue SCC (T2N1M0) with Second Primary Floor of Mouth SCC (T1N0M0) — Field Cancerization
- **Stage**: Tongue: T2N1M0 (Stage III) + Floor of Mouth: T1N0M0 (Stage I) — Synchronous Second Primary
- **Molecular profile**: PD-L1 CPS 10-20, TP53 mutation, Field cancerization, 40-pack-year smoking history, Alcohol use history
- **Report file**: experiment_reports\TN-012_report.json
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

Read the full report JSON at `experiment_reports\TN-012_report.json`.

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
    "cancer_type": "Synchronous Oral Tongue SCC (T2N1M0) with Second Primary Floor of Mouth SCC (T1N0M0) — Field Cancerization",
    "stage": "Tongue: T2N1M0 (Stage III) + Floor of Mouth: T1N0M0 (Stage I) — Synchronous Second Primary",
    "molecular_profile": [
      "PD-L1 CPS 10-20",
      "TP53 mutation",
      "Field cancerization",
      "40-pack-year smoking history",
      "Alcohol use history"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Composite Surgical Resection (Partial Glossectomy + FOM Excision) with Ipsilateral Selective Neck Dissection and Free Flap Reconstruction",
      "category": "Standard of Care",
      "composite_rating": 8.5,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "NCCN Category 1 recommendation for surgical resection of resectable oral cavity SCC. Surgery is the preferred primary modality for oral cavity cancers. Level I evidence from multiple RCTs and institutional series confirming 5-year OS of 80-85% for T1-2N0-1 disease."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year OS of 84.4% for T1-2N0-1 tongue SCC with adequate surgical margins. Composite resection of synchronous primaries can achieve curative intent for both lesions. En bloc resection with 1 cm margins and adequate neck dissection (>=30 nodes) independently predicts improved DFS and LRFS."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Universally available at all head and neck cancer centers. Standard surgical procedure performed by head and neck surgical oncologists worldwide. No biomarker or drug access barriers."
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Composite resection of two oral cavity subsites carries significant functional morbidity including speech and swallowing impairment. Free flap reconstruction required for defect coverage. Early postoperative complications include flap failure (2-5%), wound infection, and fistula. Most patients recover near-baseline function at 12 months with rehabilitation."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability — no biomarker requirements. Applicable to all oral cavity SCC regardless of molecular profile. Histopathological assessment guides adjuvant therapy decisions."
        }
      },
      "mechanism_of_action": "En bloc surgical excision of both primary tumors with adequate margins (>=1 cm) to achieve R0 resection. Ipsilateral selective neck dissection (levels I-IV) addresses the N1 disease of the tongue primary. Composite resection allows unified surgical field to address field cancerization. Free flap reconstruction (anterolateral thigh or radial forearm) restores oral competence.",
      "key_evidence": {
        "study_name": "Prognostic factors in surgically treated tongu
... (truncated — read full file from experiment_reports\TN-012_report.json)
```
