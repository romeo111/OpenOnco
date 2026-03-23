# Re-evaluation Task: HN2-010

## Context
- **Case ID**: HN2-010
- **Cancer type**: Lip Squamous Cell Carcinoma — Locally Advanced (Commissure Involvement)
- **Stage**: T3N1M0 (AJCC Stage III)
- **Molecular profile**: PD-L1 CPS >= 10, UV mutational signature, High tumor mutational burden (~45 mutations/Mb), Dual etiology: chronic UV exposure + tobacco (pipe smoking), EGFR overexpression (typical of cutaneous SCC)
- **Report file**: experiment_reports\HN2-010_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: The most critical gaps in the cancer research report HN2-010 are the lack of data on Neoadjuvant Cemiplimab (Pre-Surgical Immunotherapy) and Concurrent Cisplatin Chemoradiation (Definitive or Adjuvant), which will improve the score by providing more comprehensive information on the effectiveness of these treatments in combination with surgery. Filling these gaps will enable a more complete understanding of the optimal treatment strategies for patients with specific types of cancer, ultimately leading to better patient outcomes and improved scores.

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

Read the full report JSON at `experiment_reports\HN2-010_report.json`.

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
    "cancer_type": "Lip Squamous Cell Carcinoma — Locally Advanced (Commissure Involvement)",
    "stage": "T3N1M0 (AJCC Stage III)",
    "molecular_profile": [
      "PD-L1 CPS >= 10",
      "UV mutational signature",
      "High tumor mutational burden (~45 mutations/Mb)",
      "Dual etiology: chronic UV exposure + tobacco (pipe smoking)",
      "EGFR overexpression (typical of cutaneous SCC)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Surgical Excision with Karapandzic Flap Reconstruction + Selective Neck Dissection",
      "category": "Standard of Care",
      "composite_rating": 8.5,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "NCCN Category 1 recommendation for primary surgical management of locally advanced lip SCC; multiple large institutional series and SEER database analyses support surgery as first-line for T3 lip tumors"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "Complete surgical resection with clear margins is the single most impactful intervention; 5-year OS 60-70% for stage III lip SCC when combined with adjuvant RT; Karapandzic flap achieves 88% good-to-excellent aesthetic outcomes with preserved oral competence"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Standard surgical procedure available at all major head and neck cancer centers; Karapandzic flap is a workhorse reconstruction for commissure-involved defects requiring no microsurgical expertise"
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Surgical morbidity is moderate; microstomia develops in 15.7% requiring commissuroplasty; early complications in 9.8%, late in 17.7%; selective neck dissection adds shoulder/nerve morbidity risk"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability regardless of molecular profile; no biomarker requirement for surgical intervention"
        }
      },
      "mechanism_of_action": "Complete surgical excision of the primary tumor with oncologic margins (6-9 mm for T3 lesions) followed by Karapandzic neurovascular advancement-rotation flap for commissure reconstruction, which preserves orbicularis oris motor innervation, labial artery blood supply, and sensory nerve continuity. Selective neck dissection (levels I-III) addresses the N1 nodal disease.",
      "key_evidence": {
        "study_name": "SEER Database Analysis: Impact of Staging, Histologic Grading, and Racial Background on Lip Cancer Survival (2010-2020)",
        "journal": "PMC / Head and Neck Surgery",
        "year": 2024,
        "sample_size": 8500,
        "os_months": {
          "treatment": 72,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 60,
          "control"
... (truncated — read full file from experiment_reports\HN2-010_report.json)
```
