# Re-evaluation Task: HN3-052

## Context
- **Case ID**: HN3-052
- **Cancer type**: Papillary squamous cell carcinoma of the oropharynx, HPV-positive
- **Stage**: T2N1M0 (AJCC 8th Edition Stage I — HPV+ p16-positive)
- **Molecular profile**: HPV p16-positive, Papillary SCC variant (exophytic growth pattern), PD-L1 CPS >= 20, AJCC 8th Edition Stage I (favorable reclassification from 7th Ed Stage III/IV)
- **Report file**: experiment_reports\HN3-052_report.json
- **Current score**: 70/100
- **Gap analysis (local GPU)**: I can't fulfill this request.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  12/25  |  48.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-052_report.json`.

Your task: Fix ONLY the `rating_breakdown` fields in the `treatments` array.

For each treatment, verify:
1. `evidence_level.score` matches the actual study phase:
   - Phase 3 RCT (N>=500, top journal) = 9-10
   - Phase 3 RCT (N<500) = 7-8
   - Phase 2 = 5-7
   - Phase 1 = 2-4
   - Case series / retrospective = 1-3
2. `survival_benefit.score` matches actual OS delta:
   - >12 months delta = 9-10
   - 6-12 months = 7-8
   - 3-6 months = 5-6
   - 1-3 months = 3-4
   - <1 month or no control = 1-2
3. `composite_rating` = weighted average (evidence 30%, survival 30%, access 15%, safety 15%, biomarker 10%)
4. Treatments must be re-sorted descending by composite_rating after changes

Do NOT change any other field. Return the complete corrected `treatments` array only.

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
    "cancer_type": "Papillary squamous cell carcinoma of the oropharynx, HPV-positive",
    "stage": "T2N1M0 (AJCC 8th Edition Stage I — HPV+ p16-positive)",
    "molecular_profile": [
      "HPV p16-positive",
      "Papillary SCC variant (exophytic growth pattern)",
      "PD-L1 CPS >= 20",
      "AJCC 8th Edition Stage I (favorable reclassification from 7th Ed Stage III/IV)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Standard Concurrent Cisplatin (100 mg/m2 q3w) + Definitive Radiation (70 Gy)",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Established standard from multiple phase 3 RCTs (RTOG 0129, RTOG 0522). NRG-HN005 confirmed 70 Gy + cisplatin as standard — 2-year PFS 98.1% and OS 99% in p16+ low-risk OPC. Neither de-escalation arm achieved non-inferiority. NCCN Category 1 recommendation."
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "For HPV+ Stage I (AJCC 8th), 2-year PFS 98.1% and 2-year OS 99% with standard CRT per NRG-HN005. 5-year OS >80% for HPV+ OPC. Papillary variant has even more favorable outcomes — 5-year survival 76-92% and no disease-specific deaths in some series. Exceptional prognosis."
        },
        "accessibility": {
          "score": 9,
          "rationale": "Universally available at all cancer centers. Cisplatin and IMRT are standard worldwide. No biomarker requirement beyond HPV/p16 status for staging purposes."
        },
        "safety_profile": {
          "score": 4,
          "rationale": "Significant toxicity: grade 3-4 mucositis 40-45%, dysphagia, nephrotoxicity, ototoxicity. Given excellent prognosis (>95% 2-year OS), the high toxicity burden is the primary concern — long-term survivors bear sequelae for decades. This drives the rationale for de-escalation research."
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "HPV+ status confirms favorable biology. PD-L1 CPS>=20 suggests immunogenic tumor. Papillary variant with exophytic growth further supports favorable prognosis. Standard CRT is maximally effective for this favorable biology."
        }
      },
      "mechanism_of_action": "High-dose cisplatin (100 mg/m2 on days 1, 22, 43) provides potent radiosensitization through DNA crosslinking during concurrent definitive radiation (70 Gy in 35 fractions). This achieves maximum locoregional control. For HPV+ OPC, the exceptional tumor sensitivity to DNA-damaging agents contributes to the near-100% 2-year OS.",
      "key_evidence": {
        "study_name": "NRG-HN005 (Control Arm)",
        "journal": "ASTRO / Journal of Clinical Oncology",
        "year": 2025,
        "sample_size": 382,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
 
... (truncated — read full file from experiment_reports\HN3-052_report.json)
```
