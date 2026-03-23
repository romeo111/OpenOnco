# Re-evaluation Task: TN-010

## Context
- **Case ID**: TN-010
- **Cancer type**: Oral Tongue Mucoepidermoid Carcinoma (Minor Salivary Gland Origin, High-Grade)
- **Stage**: T2N0M0 (Stage II)
- **Molecular profile**: CRTC1-MAML2 fusion negative (high-grade aggressive), HER2 IHC 2+ (FISH confirmation pending — T-DXd candidate if amplified), Androgen receptor negative, Minor salivary gland origin — NOT squamous cell carcinoma
- **Report file**: experiment_reports\TN-010_report.json
- **Current score**: 83/100
- **Gap analysis (local GPU)**: The most critical gaps in the TN-010 cancer research report are the lack of data on Wide Local Excision with Adequate Margins + Elective Surgery and Adjuvant Postoperative Radiation Therapy (60-66 Gy), as these are crucial components of standard treatment protocols for certain types of cancer. Filling in this data will improve the score by providing a more comprehensive understanding of the effectiveness of these treatments, allowing researchers to make more informed decisions about patient care and potentially leading to improved outcomes.

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

Read the full report JSON at `experiment_reports\TN-010_report.json`.

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
    "cancer_type": "Oral Tongue Mucoepidermoid Carcinoma (Minor Salivary Gland Origin, High-Grade)",
    "stage": "T2N0M0 (Stage II)",
    "molecular_profile": [
      "CRTC1-MAML2 fusion negative (high-grade aggressive)",
      "HER2 IHC 2+ (FISH confirmation pending — T-DXd candidate if amplified)",
      "Androgen receptor negative",
      "Minor salivary gland origin — NOT squamous cell carcinoma"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Local Excision with Adequate Margins + Elective Neck Dissection (Levels I-IV)",
      "category": "Standard of Care",
      "composite_rating": 8.6,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "NCCN and ASCO guidelines (2025) strongly recommend primary surgical resection with wide margins for resectable salivary gland malignancies. Extensive retrospective data supports surgery as the definitive treatment for T2N0 high-grade MEC."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "Complete surgical resection with clear margins is the single most important prognostic factor. 5-year OS for adequately resected high-grade MEC ranges 50-67%. Negative margins convert a poor prognosis to a manageable one."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Widely available at any head and neck surgical center. Standard procedure for oral tongue tumors. No special equipment or biomarker requirements."
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Surgical morbidity includes potential speech and swallowing impairment, tongue mobility restriction, and neck dissection complications (shoulder dysfunction, nerve injury). Manageable with rehabilitation."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability — surgery is indicated regardless of molecular profile. The procedure addresses the primary tumor independent of fusion status, HER2, or AR status."
        }
      },
      "mechanism_of_action": "Complete surgical excision removes the primary tumor with adequate margins (ideally >5mm). Elective neck dissection addresses the 30-50% risk of occult nodal metastasis in high-grade MEC, even in clinically N0 disease. NCCN recommends levels II-IV dissection for high-grade tumors.",
      "key_evidence": {
        "study_name": "NCCN Head and Neck Cancer Guidelines v2.2025 / ASCO Salivary Gland Malignancy Guideline",
        "journal": "Journal of Clinical Oncology / JNCCN",
        "year": 2025,
        "sample_size": 0,
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
       
... (truncated — read full file from experiment_reports\TN-010_report.json)
```
