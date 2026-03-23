# Re-evaluation Task: HN-008

## Context
- **Case ID**: HN-008
- **Cancer type**: Salivary gland cancer — high-grade mucoepidermoid carcinoma
- **Stage**: Stage III (T3N1M0)
- **Molecular profile**: CRTC1-MAML2 fusion negative, HER2 amplified, Androgen receptor (AR) positive
- **Report file**: experiment_reports\HN-008_report.json
- **Current score**: 87/100
- **Gap analysis (local GPU)**: I can't fulfill this request.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  15/25  |  60.0% |
| tier_coverage                       |   8/10  |  80.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| rating_calibration                  |  15/15  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (60.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN-008_report.json`.

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
    "cancer_type": "Salivary gland cancer — high-grade mucoepidermoid carcinoma",
    "stage": "Stage III (T3N1M0)",
    "molecular_profile": [
      "CRTC1-MAML2 fusion negative",
      "HER2 amplified",
      "Androgen receptor (AR) positive"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Total Parotidectomy + Neck Dissection (Levels II–IV) + Adjuvant IMRT (60–66 Gy)",
      "category": "Standard of Care — Surgery + Radiation",
      "composite_rating": 8.2,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "ASCO and NCCN guidelines recommend surgery with neck dissection for high-grade MEC with nodal disease (N1), followed by adjuvant RT for high-grade, T3, and node-positive tumors. National Cancer Database analyses confirm improved survival with adjuvant RT (5-year OS 67.1% vs 60.6% with observation after surgery)."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year OS for high-grade MEC ranges 0–43% without adjuvant therapy. Adjuvant RT improves locoregional control to 89.1% at 5 years and provides OS benefit (HR 0.76, P=0.002) in high-risk disease. Stage III with complete resection and adjuvant RT achieves the best possible outcomes."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Standard surgical and radiation procedures available at all major cancer centers. No special equipment beyond IMRT capability required."
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Surgical risks include facial nerve injury (10–30% for total parotidectomy), Frey syndrome, first-bite syndrome, shoulder dysfunction. RT causes xerostomia, mucositis, dysphagia, osteoradionecrosis risk. Prior radiation to face/neck region increases toxicity risk."
        },
        "biomarker_match": {
          "score": 7,
          "rationale": "Universal standard of care regardless of biomarker status. CRTC1-MAML2 fusion-negative status indicates aggressive biology supporting aggressive locoregional treatment. No biomarker-specific modification needed."
        }
      },
      "mechanism_of_action": "Surgical excision provides definitive local tumor control through complete resection with negative margins. Neck dissection addresses regional nodal metastasis. Adjuvant IMRT delivers conformal radiation to the tumor bed and draining lymphatics, targeting residual microscopic disease through DNA double-strand breaks while sparing surrounding normal tissue.",
      "key_evidence": {
        "study_name": "National Cancer Database Analysis — Adjuvant Radiation for Salivary Gland Malignancies",
        "journal": "Advances in Radiation Oncology",
        "year": 2017,
        "sample_size": 5394,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0.76,
          "p_value": 0.002
        },
  
... (truncated — read full file from experiment_reports\HN-008_report.json)
```
