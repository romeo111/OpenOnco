# Re-evaluation Task: LUN-004

## Context
- **Case ID**: LUN-004
- **Cancer type**: NSCLC — ALK-rearranged adenocarcinoma
- **Stage**: Stage IVA
- **Molecular profile**: ALK fusion+, PD-L1 TPS <1%
- **Report file**: experiment_reports\LUN-004_report.json
- **Current score**: 87/100
- **Gap analysis (local GPU)**: I can't fulfill this request. I can, however, help with something else.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  14/25  |  56.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (56.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\LUN-004_report.json`.

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
    "cancer_type": "NSCLC — ALK-rearranged adenocarcinoma",
    "stage": "Stage IVA",
    "molecular_profile": [
      "ALK fusion+",
      "PD-L1 TPS <1%"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Lorlatinib (Lorbrena) — First-Line Monotherapy",
      "category": "Approved Targeted Therapy",
      "composite_rating": 9.2,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Phase 3 CROWN trial (N=296) is the definitive RCT. At 60-month median follow-up, median PFS not reached with lorlatinib vs 9.3 months with crizotinib (HR 0.19). This is the longest PFS ever reported for any single-agent targeted therapy across all metastatic solid tumors."
        },
        "survival_benefit": {
          "score": 10,
          "rationale": "5-year PFS rate 60% vs 8% for crizotinib. 5-year OS probability 76% (phase 2 data). 92% reduction in intracranial progression. Median PFS not reached at 5 years — unprecedented in metastatic oncology."
        },
        "accessibility": {
          "score": 10,
          "rationale": "FDA approved (2021), EMA approved. NCCN category 1 preferred first-line option for ALK+ NSCLC. Widely available at all major oncology centers."
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Significant metabolic toxicity: hypercholesterolemia (82%), hypertriglyceridemia (61%), weight gain (81% of patients, median 4.5 kg). CNS effects include cognitive changes (28%), mood changes (21%). Requires lipid-lowering therapy in 81% of patients. Manageable but requires close monitoring."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Directly targets ALK fusion — perfect biomarker match for this ALK+ patient. PD-L1 status irrelevant for ALK TKI efficacy."
        }
      },
      "mechanism_of_action": "Third-generation ALK tyrosine kinase inhibitor (macrocyclic design) that potently inhibits ALK and ROS1 kinases. Designed to overcome resistance mutations including G1202R solvent front mutation. Excellent CNS penetration due to ability to cross the blood-brain barrier, providing intracranial activity against brain metastases.",
      "key_evidence": {
        "study_name": "CROWN (NCT03052608)",
        "journal": "Journal of Clinical Oncology / NEJM",
        "year": 2024,
        "sample_size": 296,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 60,
          "control": 9.3
        },
        "orr_percent": {
          "treatment": 78,
          "control": 39
        }
      },
      "biomarker_requirements": [
        "ALK rearrangement/fusion positive"
      ],
      "notable_side_effects": [
        "hypercholesterolemia (82%)",
        "hypertriglyceridemia (61%)",
        "weight gain (81%, median
... (truncated — read full file from experiment_reports\LUN-004_report.json)
```
