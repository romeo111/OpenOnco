# Re-evaluation Task: HN-004

## Context
- **Case ID**: HN-004
- **Cancer type**: Nasopharyngeal carcinoma (NPC), WHO Type II/III, EBV-associated, nonkeratinizing
- **Stage**: Stage III (T3N1M0)
- **Molecular profile**: EBV-positive, PD-L1 CPS >=50, High plasma EBV DNA, WHO Type II/III (nonkeratinizing)
- **Report file**: experiment_reports\HN-004_report.json
- **Current score**: 87/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN-004 cancer research report are the lack of data on the efficacy of Toripalimab combined with Gemcitabine/Cisplatin for first-line treatment, which is a crucial area to address as it may impact the overall effectiveness of the therapy. Additionally, the absence of sample size information for Plasma EBV DNA-Guided Adaptive Therapy (Risk Stratification) will hinder the ability to accurately assess its potential benefits and limitations, thereby limiting the report's score improvement.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  13/25  |  52.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| rating_calibration                  |  15/15  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (52.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN-004_report.json`.

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
    "cancer_type": "Nasopharyngeal carcinoma (NPC), WHO Type II/III, EBV-associated, nonkeratinizing",
    "stage": "Stage III (T3N1M0)",
    "molecular_profile": [
      "EBV-positive",
      "PD-L1 CPS >=50",
      "High plasma EBV DNA",
      "WHO Type II/III (nonkeratinizing)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Gemcitabine/Cisplatin Induction Chemotherapy + Concurrent Cisplatin-IMRT (GP-IC + CCRT)",
      "category": "Standard of Care",
      "composite_rating": 8.9,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Phase 3 RCT (NEJM 2019, n=480) with 69.8-month follow-up. NCCN Category 1 recommendation. Gemcitabine/cisplatin is the preferred induction regimen per guidelines. Final OS analysis published in JCO 2022 confirms sustained benefit."
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "5-year OS 87.9% vs 78.8% (HR 0.51, 95% CI 0.34-0.78, P=0.001). 5-year recurrence-free survival also significantly improved. For stage III T3N1M0 patients with complete response to induction, 5-year OS approaches 100%."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Gemcitabine and cisplatin are generic, globally available chemotherapeutics. IMRT is standard radiation technology available at all major cancer centers. Universal access worldwide."
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Grade 3-4 neutropenia in ~50% during induction. Cisplatin-related nephrotoxicity, ototoxicity, nausea. Late toxicity comparable between arms (grade 3+: 11.3% vs 11.4%). Mucositis during concurrent phase is significant."
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Standard for all locoregionally advanced NPC regardless of biomarkers. EBV+ status and WHO Type II/III are the defining features of endemic NPC for which this regimen was developed. Plasma EBV DNA clearance during induction correlates with response."
        }
      },
      "mechanism_of_action": "Gemcitabine (nucleoside analog) inhibits DNA synthesis and cisplatin forms DNA crosslinks, providing synergistic cytotoxicity during induction. Concurrent cisplatin radiosensitizes tumor cells during IMRT, which delivers conformal radiation to the nasopharynx and involved nodes while sparing parotid glands.",
      "key_evidence": {
        "study_name": "Gemcitabine/Cisplatin Induction Phase III (Zhang et al.)",
        "journal": "New England Journal of Medicine / Journal of Clinical Oncology",
        "year": 2019,
        "sample_size": 480,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0.51,
          "p_value": 0.001
        },
        "pfs_months": {
          "treatment": 0,
          "control": 0
        },
        "orr_percent": {
          "treatment": 94,

... (truncated — read full file from experiment_reports\HN-004_report.json)
```
