# Re-evaluation Task: HN3-018

## Context
- **Case ID**: HN3-018
- **Cancer type**: Hodgkin Lymphoma, Cervical Stage IIA (Classical, Nodular Sclerosis)
- **Stage**: Stage IIA (Early Stage)
- **Molecular profile**: CD30+, Nodular sclerosis subtype, CD15+, Reed-Sternberg cells, 9p24.1 amplification (PD-L1/PD-L2)
- **Report file**: experiment_reports\HN3-018_report.json
- **Current score**: 71/100
- **Gap analysis (local GPU)**: The most critical gaps in HN3-018's research report include the lack of data on PET-adapted ABVD alone (RT Omission Strategy) and BrECADD (Brentuximab Vedotin + Etoposide, Cyclophosphamide), which are crucial for understanding the efficacy of these regimens in early-stage Hodgkin lymphoma. Filling these gaps will improve the score by providing more comprehensive insights into the effectiveness of these treatments, allowing for more informed decision-making and potentially leading to improved patient outcomes.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  13/25  |  52.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-018_report.json`.

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
    "cancer_type": "Hodgkin Lymphoma, Cervical Stage IIA (Classical, Nodular Sclerosis)",
    "stage": "Stage IIA (Early Stage)",
    "molecular_profile": [
      "CD30+",
      "Nodular sclerosis subtype",
      "CD15+",
      "Reed-Sternberg cells",
      "9p24.1 amplification (PD-L1/PD-L2)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "2x ABVD + 20 Gy Involved-Site RT (GHSG HD10 Protocol)",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "GHSG HD10 Phase 3 RCT with 1370 patients; international standard of care for early-stage favorable HL; long-term follow-up (median 79-91 months) confirms excellent outcomes"
        },
        "survival_benefit": {
          "score": 10,
          "rationale": "5-year OS 96.6%, 5-year PFS 91.2%; highly curable disease; cure rate >90% with combined modality therapy; minimal difference from more intensive 4x ABVD approach"
        },
        "accessibility": {
          "score": 10,
          "rationale": "ABVD universally available worldwide; 20 Gy ISRT widely deliverable; WHO essential medicines; lowest cost frontline option; only 2 cycles minimizes treatment burden"
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Only 2 cycles of ABVD limits cumulative toxicity; 20 Gy ISRT has minimal late effects (2.9% vs 8.7% at 30 Gy); ABVD has lowest gonadotoxicity of HL regimens; no bleomycin-free option but 2 cycles limit pulmonary risk"
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "Standard approach for all classical HL subtypes including nodular sclerosis; CD30 expression not required for ABVD efficacy but confirms classical HL diagnosis"
        }
      },
      "mechanism_of_action": "ABVD: Doxorubicin (DNA intercalator/topoisomerase II inhibitor), Bleomycin (DNA strand breaks via free radicals), Vinblastine (microtubule inhibitor), Dacarbazine (alkylating agent). Combined with 20 Gy involved-site radiation therapy to consolidate local disease control. Two cycles deliver sufficient chemotherapy intensity for favorable-risk disease.",
      "key_evidence": {
        "study_name": "GHSG HD10",
        "journal": "New England Journal of Medicine",
        "year": 2010,
        "sample_size": 1370,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0.61
        },
        "pfs_months": {
          "treatment": 0,
          "control": 0
        },
        "orr_percent": {
          "treatment": 96,
          "control": 96
        }
      },
      "biomarker_requirements": [],
      "notable_side_effects": [
        "Nausea/vomiting",
        "Myelosuppression",
        "Bleomycin pulmonary toxicity (low risk with 2 cycles)",
        "Alopecia",
        "Transient azoospermia
... (truncated — read full file from experiment_reports\HN3-018_report.json)
```
