# Re-evaluation Task: HN3-029

## Context
- **Case ID**: HN3-029
- **Cancer type**: Locally Advanced Basal Cell Carcinoma of Nose (Gorlin Syndrome-Associated)
- **Stage**: Locally advanced, inoperable without major deformity
- **Molecular profile**: PTCH1 germline mutation, Hedgehog pathway constitutive activation, Gorlin syndrome (nevoid BCC syndrome), Radiation sensitivity (contraindication to RT)
- **Report file**: experiment_reports\HN3-029_report.json
- **Current score**: 71/100
- **Gap analysis (local GPU)**: The most critical gaps in HN3-029 include the lack of data on Neoadjuvant Vismodegib Followed by Surgery and Induction Vismodegib + Concurrent Radiation Therapy, which are essential for understanding the efficacy and optimal treatment strategies for basal cell carcinoma (BCC). Filling these gaps will improve the score by providing more comprehensive evidence-based information on the effectiveness of these treatments, allowing for more informed clinical decision-making.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  12/25  |  48.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-029_report.json`.

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
    "cancer_type": "Locally Advanced Basal Cell Carcinoma of Nose (Gorlin Syndrome-Associated)",
    "stage": "Locally advanced, inoperable without major deformity",
    "molecular_profile": [
      "PTCH1 germline mutation",
      "Hedgehog pathway constitutive activation",
      "Gorlin syndrome (nevoid BCC syndrome)",
      "Radiation sensitivity (contraindication to RT)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Neoadjuvant Vismodegib Followed by Surgery",
      "category": "Standard of Care (Neoadjuvant)",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "Phase 2 VISMONEO trial: 80% tumor downstaging, 49% clinical complete response after median 6 months treatment; 66% mean tumor size reduction; multiple supporting studies confirm neoadjuvant benefit"
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "Converts inoperable to operable disease; reduces surgical defect by 34.8%; 5-year BCC-specific survival 89%; enables organ-sparing surgery preserving nasal structure and function"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Vismodegib FDA approved for advanced BCC; oral medication; neoadjuvant approach well-established at dermatologic oncology centers"
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Significant class-effect adverse events: dysgeusia (76%), muscle spasms (72%), alopecia (58%), weight loss; dose modifications needed in 59%; CoQ10/calcium supplementation reduces dose reduction need to 17%"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "PTCH1 germline mutation causes constitutive Hedgehog pathway activation; vismodegib directly targets Smoothened receptor downstream of PTCH1; Gorlin syndrome BCCs exquisitely sensitive to HHI"
        }
      },
      "mechanism_of_action": "Vismodegib is a small molecule inhibitor of Smoothened (SMO), a transmembrane protein in the Hedgehog signaling pathway. In Gorlin syndrome, loss-of-function PTCH1 mutation removes constitutive suppression of SMO, leading to uncontrolled Hedgehog pathway activation. Vismodegib directly inhibits SMO, blocking downstream GLI transcription factor activation and tumor cell proliferation. Neoadjuvant treatment shrinks tumors to enable less morbid surgical resection.",
      "key_evidence": {
        "study_name": "VISMONEO Phase 2 Trial",
        "journal": "eClinicalMedicine (Lancet)",
        "year": 2021,
        "sample_size": 55,
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
          "treatment": 80,
          "control": 0
        }
      },
      "biom
... (truncated — read full file from experiment_reports\HN3-029_report.json)
```
