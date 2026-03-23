# Re-evaluation Task: HN3-003

## Context
- **Case ID**: HN3-003
- **Cancer type**: HPV-positive tonsillar squamous cell carcinoma (oropharyngeal)
- **Stage**: T2N1M0, AJCC 8th Edition Stage I (p16-positive)
- **Molecular profile**: HPV-positive (p16+), PD-L1 CPS >= 20, Non-smoker, 45-year-old male
- **Report file**: experiment_reports\HN3-003_report.json
- **Current score**: 84/100
- **Gap analysis (local GPU)**: The lack of data on Definitive Concurrent Chemoradiation with IMRT and TORS with Neck Dissection, as well as Definitive CRT with Proton Therapy, hinders the ability to accurately assess treatment outcomes for patients with head and neck cancer, which will improve the score by providing more comprehensive evidence-based recommendations. Additionally, missing data on Tonsillectomy with Ipsilateral Neck Dissection and Definitive Radiation Alone with IMRT will limit the understanding of optimal treatment strategies for specific patient subgroups, further reducing the overall score.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  11/25  |  44.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (44.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-003_report.json`.

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
    "cancer_type": "HPV-positive tonsillar squamous cell carcinoma (oropharyngeal)",
    "stage": "T2N1M0, AJCC 8th Edition Stage I (p16-positive)",
    "molecular_profile": [
      "HPV-positive (p16+)",
      "PD-L1 CPS >= 20",
      "Non-smoker",
      "45-year-old male"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Definitive Concurrent Chemoradiation (70 Gy IMRT + Cisplatin)",
      "category": "Standard of Care",
      "composite_rating": 9.2,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Phase 3 RCT evidence from NRG-HN005, RTOG 1016, De-ESCALaTE, and multiple landmark trials. NRG-HN005 control arm achieved unprecedented 98.1% 2-year PFS and 99% 2-year OS in this exact population. NCCN Category 1 recommendation. Decades of level 1 evidence supporting 70 Gy with concurrent cisplatin."
        },
        "survival_benefit": {
          "score": 10,
          "rationale": "HPV+ T2N1M0 Stage I patients have >90% 5-year OS with standard CRT. NRG-HN005 showed 98.1% 2-year PFS and 99% 2-year OS — the highest ever recorded in a phase 3 trial for this population. De-escalation attempts (NRG-HN005 arms B/C) failed to meet non-inferiority, confirming standard CRT remains optimal."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Universally available at all radiation oncology centers. Cisplatin is a generic, widely accessible platinum agent. IMRT is standard equipment at virtually all treatment facilities. No specialized technology or trial enrollment required."
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Significant acute toxicity: grade 3-4 mucositis (40-60%), dysphagia requiring feeding tube (25-40%), cisplatin-related nephrotoxicity, ototoxicity (33% hearing impairment per RTOG 1016), nausea/emesis. Long-term xerostomia and dysphagia persist beyond 2 years. In a 45-year-old, decades of survivorship with these toxicities is a major concern."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability — no biomarker requirement. HPV+ status confirms excellent prognosis with this approach. Non-smoking status further enhances favorable outcomes per NRG-HN005 inclusion criteria."
        }
      },
      "mechanism_of_action": "70 Gy delivered in 35 fractions (2 Gy/fx) via IMRT over 7 weeks with concurrent cisplatin (100 mg/m2 on days 1 and 22, or 40 mg/m2 weekly). Radiation induces DNA double-strand breaks in tumor cells; cisplatin forms platinum-DNA adducts that inhibit DNA repair and enhance radiosensitivity. HPV+ tumors are intrinsically radiosensitive due to functional p53 and intact apoptotic pathways.",
      "key_evidence": {
        "study_name": "NRG-HN005 (Control Arm)",
        "journal": "Presented at ASTRO 2024, published 2025",
        "year": 2025,
        "sample_size": 38
... (truncated — read full file from experiment_reports\HN3-003_report.json)
```
