# Re-evaluation Task: HN2-004

## Context
- **Case ID**: HN2-004
- **Cancer type**: Sinonasal undifferentiated carcinoma (SNUC), IDH2-mutant subtype
- **Stage**: Stage IVA (T4aN1M0)
- **Molecular profile**: IDH2 mutation (R172 hotspot), Ki-67 80%, WHO 2022: IDH2-mutated sinonasal carcinoma
- **Report file**: experiment_reports\HN2-004_report.json
- **Current score**: 81/100
- **Gap analysis (local GPU)**: The lack of data on Proton Beam Therapy (Post-Surgical or Definitive) with a sample size is a critical gap, as it hinders the understanding of its efficacy in improving patient outcomes, which would significantly boost the score. Additionally, filling in the intent behind Neoadjuvant Pembrolizumab + Chemotherapy (Curative) and Enasidenib (IDH2 Inhibitor, 100 mg Daily) — Target will provide valuable insights into innovative treatment approaches for cancer patients, further enhancing the report's credibility.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  10/25  |  40.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (40.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-004_report.json`.

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
    "cancer_type": "Sinonasal undifferentiated carcinoma (SNUC), IDH2-mutant subtype",
    "stage": "Stage IVA (T4aN1M0)",
    "molecular_profile": [
      "IDH2 mutation (R172 hotspot)",
      "Ki-67 80%",
      "WHO 2022: IDH2-mutated sinonasal carcinoma"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Induction Cisplatin/Etoposide followed by Definitive Chemoradiation (Response-Adapted)",
      "category": "Standard of Care",
      "composite_rating": 7.7,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "Large retrospective series (Amit et al., 95 patients at MD Anderson) with consistent results across multiple institutions. Not Phase 3 RCT but the largest SNUC-specific evidence base available for this ultra-rare tumor"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year OS 81% for IC responders receiving CRT (Amit 2019). 5-year DSS 81% in responders. Overall cohort 5-year OS 56%. IPD meta-analysis shows 72.6% 5-year OS with IC vs 44.5% without (Burggraf 2024)"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Cisplatin and etoposide universally available at all cancer centers. IMRT widely available. No special infrastructure required beyond standard oncology"
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Grade 3/4 hematologic toxicity 34% (neutropenia 20%, thrombocytopenia 11%). Grade 3/4 non-hematologic 26%. Hearing impairment 25%. Significant mucositis with concurrent CRT. Manageable with supportive care"
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Applies to all SNUC regardless of IDH2 status. IC response-adapted approach particularly valuable as Ki-67 80% suggests chemosensitivity to platinum/etoposide given high proliferative index"
        }
      },
      "mechanism_of_action": "Cisplatin forms DNA crosslinks causing replication arrest and apoptosis. Etoposide inhibits topoisomerase II, blocking DNA unwinding. Sequential approach uses IC response to guide definitive therapy: responders receive CRT (cisplatin + 70 Gy IMRT), non-responders undergo salvage surgery + adjuvant RT.",
      "key_evidence": {
        "study_name": "Amit et al. Induction Chemotherapy Response as a Guide for Treatment Optimization in SNUC",
        "journal": "Journal of Clinical Oncology",
        "year": 2019,
        "sample_size": 95,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0.0001
        },
        "pfs_months": {
          "treatment": 0,
          "control": 0
        },
        "orr_percent": {
          "treatment": 67,
          "control": 0
        }
      },
      "biomarker_requirements": [],
      "notable_side_effects": [
        "Grade 3/4 neutropenia (20%)",
        "Thrombocytop
... (truncated — read full file from experiment_reports\HN2-004_report.json)
```
