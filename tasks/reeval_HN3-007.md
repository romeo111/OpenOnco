# Re-evaluation Task: HN3-007

## Context
- **Case ID**: HN3-007
- **Cancer type**: Nasopharyngeal Carcinoma WHO Type I (Keratinizing Squamous Cell Carcinoma), EBV-Negative
- **Stage**: T3N2M0 (Stage III/IVA, AJCC 8th Edition)
- **Molecular profile**: PIK3CA mutation, EBV-negative (EBER-negative), Keratinizing histology (WHO Type I), Smoking-related etiology
- **Report file**: experiment_reports\HN3-007_report.json
- **Current score**: 70/100
- **Gap analysis (local GPU)**: The lack of sample size information for Concurrent Cisplatin-IMRT (Definitive Chemoradiation) and Induction TPF (Docetaxel/Cisplatin/5-FU) Followed by C is critical as it hinders the ability to accurately assess treatment efficacy and patient outcomes, which will improve the score by providing more reliable data. Additionally, filling in the intent information for Toripalimab + Gemcitabine-Cisplatin (JUPITER-02 Re), Induction Chemoimmunotherapy (Camrelizumab/Toripalimab), and Alpelisib + Cetuximab Combination will provide a more comprehensive understanding of treatment strategies, leading to improved score.

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

Read the full report JSON at `experiment_reports\HN3-007_report.json`.

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
    "cancer_type": "Nasopharyngeal Carcinoma WHO Type I (Keratinizing Squamous Cell Carcinoma), EBV-Negative",
    "stage": "T3N2M0 (Stage III/IVA, AJCC 8th Edition)",
    "molecular_profile": [
      "PIK3CA mutation",
      "EBV-negative (EBER-negative)",
      "Keratinizing histology (WHO Type I)",
      "Smoking-related etiology"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Induction Gemcitabine-Cisplatin (GP) Followed by Concurrent Cisplatin-IMRT",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Phase III RCT (Zhang et al., NEJM 2019) demonstrated significant OS benefit for GP induction + CCRT vs CCRT alone in LA-NPC; NCCN Category 1 recommendation for T3N2 disease"
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "5-year OS 87.9% vs 78.8% with induction GP+CCRT vs CCRT alone (HR 0.51); however keratinizing histology has substantially worse outcomes (5-year survival 37-46%) compared to the predominantly non-keratinizing trial population"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Gemcitabine and cisplatin widely available globally; IMRT technology standard at most radiation centers; established standard of care"
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Grade 3-4 neutropenia and thrombocytopenia common during induction; cumulative cisplatin toxicity; late toxicities comparable between arms at 11.3% vs 11.4%"
        },
        "biomarker_match": {
          "score": 5,
          "rationale": "Trial population was predominantly EBV-positive non-keratinizing NPC; extrapolation to EBV-negative keratinizing subtype uncertain; PIK3CA mutation may confer partial resistance to platinum; keratinizing histology less radiosensitive"
        }
      },
      "mechanism_of_action": "Gemcitabine is a nucleoside analog inhibiting DNA synthesis; cisplatin forms DNA crosslinks. Induction reduces tumor burden and addresses micrometastatic disease before definitive IMRT with concurrent cisplatin radiosensitization. Sequential approach targets both systemic and local disease.",
      "key_evidence": {
        "study_name": "Zhang et al. GP Induction NPC Phase III",
        "journal": "New England Journal of Medicine",
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
          "treatment": 92,
          "control": 76
        }
      },
      "biomarker_requirements": [],
      "notable_side_effects": [
        "Neutropenia",
        "Thrombocytopenia",
        "Nephrotoxicity",
        "Ototoxi
... (truncated — read full file from experiment_reports\HN3-007_report.json)
```
