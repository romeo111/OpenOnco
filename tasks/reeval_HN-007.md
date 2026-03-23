# Re-evaluation Task: HN-007

## Context
- **Case ID**: HN-007
- **Cancer type**: Papillary Thyroid Carcinoma (PTC)
- **Stage**: Stage II (T3N1aM0, AJCC 8th edition, age <55)
- **Molecular profile**: BRAF V600E positive, RET/PTC rearrangement negative
- **Report file**: experiment_reports\HN-007_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: The most critical gaps in HN-007's cancer research report are the missing data on Radioactive Iodine (RAI) Therapy (I-131) and TSH Suppression Therapy (Levothyroxine), as these treatments are crucial for thyroid cancer management, and filling in this data will provide a more comprehensive understanding of their efficacy. By addressing these gaps, HN-007's score can be improved by providing a clearer picture of the effectiveness of RAI therapy and levothyroxine treatment, which are essential components of thyroid cancer care.

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

Read the full report JSON at `experiment_reports\HN-007_report.json`.

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
    "cancer_type": "Papillary Thyroid Carcinoma (PTC)",
    "stage": "Stage II (T3N1aM0, AJCC 8th edition, age <55)",
    "molecular_profile": [
      "BRAF V600E positive",
      "RET/PTC rearrangement negative"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Total Thyroidectomy + Central Neck Dissection",
      "category": "Standard of Care",
      "composite_rating": 9.7,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Decades of level I evidence and international guideline consensus (ATA 2025, NCCN, ESMO) support total thyroidectomy as definitive treatment for T3N1a PTC"
        },
        "survival_benefit": {
          "score": 10,
          "rationale": "10-year OS >97% and 20-year OS ~90% for PTC after total thyroidectomy; locoregional recurrence ~1% with complete resection; disease-specific survival ~99% at 10 years"
        },
        "accessibility": {
          "score": 10,
          "rationale": "Universally available surgical procedure at all cancer centers worldwide; standard practice for over 50 years"
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Generally safe; risks include transient hypoparathyroidism (up to 50%), permanent hypoparathyroidism (1-3%), recurrent laryngeal nerve injury (2-8%); requires lifelong thyroid hormone replacement"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Applicable to all PTC regardless of molecular profile; BRAF V600E status may support more extensive initial surgery due to associated aggressive features"
        }
      },
      "mechanism_of_action": "Complete surgical excision of the thyroid gland and central compartment lymph nodes removes all macroscopic disease. For T3N1a tumors, total thyroidectomy with central neck dissection provides comprehensive local disease control and enables postoperative RAI therapy and thyroglobulin surveillance.",
      "key_evidence": {
        "study_name": "Long-term Outcomes of 5,897 PTC Patients",
        "journal": "World Journal of Surgery",
        "year": 2018,
        "sample_size": 5897,
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
        }
      },
      "biomarker_requirements": [],
      "notable_side_effects": [
        "Hypoparathyroidism (transient 20-50%, permanent 1-3%)",
        "Recurrent laryngeal nerve injury (2-8%)",
        "Lifelong levothyroxine requirement",
        "Post-surgical hypocalcemia",
        "Voice changes (transient dysphonia ~12-20%)"
      ],
      "availability": "FDA Approved / Universally Available",
      "source_urls": [
        "https://pmc.ncbi.nlm.nih.gov/ar
... (truncated — read full file from experiment_reports\HN-007_report.json)
```
