# Re-evaluation Task: HN2-009

## Context
- **Case ID**: HN2-009
- **Cancer type**: Squamous Cell Carcinoma of the Hard Palate (Oral Cavity SCC)
- **Stage**: T2N0M0 (Stage II, AJCC 8th Edition)
- **Molecular profile**: PD-L1 CPS <1 (negative), EGFR overexpressed, Reverse smoking (chutta) associated, HPV-negative
- **Report file**: experiment_reports\HN2-009_report.json
- **Current score**: 86/100
- **Gap analysis (local GPU)**: The most critical gaps in the cancer research report HN2-009 are the lack of data on Adjuvant Concurrent Chemoradiation (Cisplatin 100 mg/m²) and Proton Beam Radiation Therapy (IMPT) for Palate/Mandible, which will improve the score by providing more comprehensive information on effective treatment regimens and radiation therapy modalities. Filling these gaps with specific data will enhance the report's credibility and provide valuable insights for researchers, clinicians, and patients, ultimately leading to improved cancer treatment outcomes.

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

Read the full report JSON at `experiment_reports\HN2-009_report.json`.

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
    "cancer_type": "Squamous Cell Carcinoma of the Hard Palate (Oral Cavity SCC)",
    "stage": "T2N0M0 (Stage II, AJCC 8th Edition)",
    "molecular_profile": [
      "PD-L1 CPS <1 (negative)",
      "EGFR overexpressed",
      "Reverse smoking (chutta) associated",
      "HPV-negative"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Local Excision / Partial Maxillectomy with Obturator Prosthesis + Elective Neck Dissection (Levels I-III)",
      "category": "Standard of Care",
      "composite_rating": 8.9,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "NCCN Category 1 recommendation for T2N0 oral cavity SCC. Large SEER database study (n=2857) confirms survival benefit of elective neck dissection in T2N0M0 OSCC. Multiple institutional series with long-term follow-up support surgical resection as primary treatment for hard palate SCC"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "T2 hard palate SCC 5-year survival 45-70% with surgery. SEER data: END improves 5-year OS from 56.4% to 66.7% (HR 0.829, p=0.0031) and DSS from 64.5% to 73.6% (HR 0.769, p=0.0069) in T2N0M0 OSCC. Surgery alone yields 71% disease-specific 5-year survival vs 29% with RT alone"
        },
        "accessibility": {
          "score": 10,
          "rationale": "Standard surgical procedure available at all head and neck surgery centers worldwide. Obturator prosthesis fabrication available through maxillofacial prosthodontists. Well-established procedure in India where reverse smoking palate cancers are endemic"
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Surgical morbidity includes oronasal communication requiring obturator or free flap reconstruction, speech hypernasality, swallowing difficulty with solids, potential shoulder dysfunction from neck dissection. Perioperative mortality <2%. Young age (45yo) favors surgical recovery"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Surgery is universally applicable regardless of PD-L1 or EGFR status. No biomarker requirements. Definitive local treatment addresses the primary tumor regardless of molecular profile"
        }
      },
      "mechanism_of_action": "Surgical resection of the primary tumor with negative margins (target >=1cm) via partial or infrastructure maxillectomy. For T2 hard palate lesions (2-4cm), resection typically creates an oronasal defect requiring rehabilitation with an obturator prosthesis (preferred for <50% palatal defect) or free flap reconstruction (preferred for >50% defect). Elective neck dissection (selective, levels I-III) addresses occult cervical metastases present in 15-23% of hard palate SCC even in clinically N0 necks.",
      "key_evidence": {
        "study_name": "SEER Database Analysis: Elective Neck Dissection in T2N0M0 OSCC",
   
... (truncated — read full file from experiment_reports\HN2-009_report.json)
```
