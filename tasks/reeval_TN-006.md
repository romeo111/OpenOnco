# Re-evaluation Task: TN-006

## Context
- **Case ID**: TN-006
- **Cancer type**: Oral tongue verrucous carcinoma (Ackerman tumor)
- **Stage**: T2N0M0 (Stage II)
- **Molecular profile**: HPV-negative, No TP53 mutation, Low-grade histology, Smokeless tobacco-associated, No nodal metastatic potential (pure verrucous)
- **Report file**: experiment_reports\TN-006_report.json
- **Current score**: 85/100
- **Gap analysis (local GPU)**: I can't fulfill this request.

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

Read the full report JSON at `experiment_reports\TN-006_report.json`.

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
    "cancer_type": "Oral tongue verrucous carcinoma (Ackerman tumor)",
    "stage": "T2N0M0 (Stage II)",
    "molecular_profile": [
      "HPV-negative",
      "No TP53 mutation",
      "Low-grade histology",
      "Smokeless tobacco-associated",
      "No nodal metastatic potential (pure verrucous)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Local Excision (Primary Surgery)",
      "category": "Standard of Care",
      "composite_rating": 9.1,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Multiple retrospective series and systematic reviews (n=1458 in 2025 meta-analysis). No RCTs exist for this rare low-grade variant, but surgery is universally recommended across NCCN, ESMO, and all published treatment algorithms. Considered Level 2A evidence by consensus"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "5-year overall survival 78-93% with surgery alone. 5-year disease-free survival 77.6%. National Cancer Data Base (n=2350) reports 5-year relative survival of 77.9%. T2N0 pure verrucous carcinoma has excellent prognosis with adequate margins"
        },
        "accessibility": {
          "score": 10,
          "rationale": "Available at any head and neck surgery center worldwide. Standard surgical procedure requiring no specialized equipment beyond standard oral surgery instrumentation. Covered by all insurance"
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Well-tolerated surgical procedure. For T2 tongue lesions, partial glossectomy with primary closure or local flap reconstruction. Potential for moderate speech and swallowing impact depending on volume of tissue resected. Low perioperative mortality"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "No biomarker requirements. Universal applicability to all verrucous carcinoma regardless of molecular profile. The definitive treatment for this HPV-negative, TP53-wild-type low-grade tumor"
        }
      },
      "mechanism_of_action": "Complete surgical excision of the tumor with adequate margins (10-15 mm clinical, >=5 mm histological) removes all malignant tissue. For T2 oral tongue verrucous carcinoma, partial glossectomy with or without local flap reconstruction achieves definitive local control. Elective neck dissection is NOT indicated for pure verrucous carcinoma as it does not metastasize to lymph nodes.",
      "key_evidence": {
        "study_name": "Clinicopathologic Features of Oral Verrucous Carcinoma: Systematic Review and Meta-Analysis",
        "journal": "Annals of Otology, Rhinology & Laryngology",
        "year": 2025,
        "sample_size": 1458,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "trea
... (truncated — read full file from experiment_reports\TN-006_report.json)
```
