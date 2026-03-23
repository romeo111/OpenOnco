# Re-evaluation Task: HN3-017

## Context
- **Case ID**: HN3-017
- **Cancer type**: Burkitt Lymphoma of the Jaw (Sporadic)
- **Stage**: MYC rearranged, Ki-67 ~100%
- **Molecular profile**: MYC rearrangement t(8;14), Ki-67 ~100%, Sporadic subtype, CD20+, CD10+, BCL6+
- **Report file**: experiment_reports\HN3-017_report.json
- **Current score**: 70/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN3-017 cancer research report include the lack of data on TLS Prophylaxis Protocol (Rasburicase + Aggressive treatment) and CNS Prophylaxis (Intrathecal Methotrexate + Cytarabine), which are essential components of comprehensive cancer treatment protocols, and filling these gaps will significantly improve the score by providing more accurate and complete information. Additionally, including data on Axicabtagene Ciloleucel / Lisocabtagene Maraleucel and Glofitamab (CD20xCD3 Bispecific Antibody) treatments will enhance the report's credibility and provide a more comprehensive understanding of cancer treatment options.

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

Read the full report JSON at `experiment_reports\HN3-017_report.json`.

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
    "cancer_type": "Burkitt Lymphoma of the Jaw (Sporadic)",
    "stage": "MYC rearranged, Ki-67 ~100%",
    "molecular_profile": [
      "MYC rearrangement t(8;14)",
      "Ki-67 ~100%",
      "Sporadic subtype",
      "CD20+",
      "CD10+",
      "BCL6+"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "DA-EPOCH-R (Dose-Adjusted Etoposide, Prednisone, Vincristine, Cyclophosphamide, Doxorubicin + Rituximab)",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "NCI 9177 multicenter Phase 2 trial with 113 patients; HOVON/SAKK Phase 3 trial confirming non-inferiority to R-CODOX-M/IVAC; published in NEJM"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "4-year EFS 84.5%, 4-year OS 87.0%; low-risk patients achieve 100% 4-year EFS; cures most adult BL patients irrespective of HIV status"
        },
        "accessibility": {
          "score": 9,
          "rationale": "All components FDA approved; available at hematology centers worldwide; dose-adjusted protocol allows safer outpatient administration in some cycles"
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Significantly fewer infectious complications, transfusions, and hospitalization days compared to R-CODOX-M/IVAC; dose adjustment mechanism improves safety; still requires intensive monitoring"
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "Rituximab targets CD20 universally expressed in Burkitt lymphoma; MYC-driven proliferation addressed by continuous infusion schedule; effective in MYC-rearranged tumors"
        }
      },
      "mechanism_of_action": "Continuous infusion chemotherapy with dose adjustment based on neutrophil nadir targets MYC-driven rapidly proliferating cells throughout cell cycle. Etoposide inhibits topoisomerase II; doxorubicin intercalates DNA; cyclophosphamide alkylates DNA; vincristine disrupts microtubules; rituximab provides anti-CD20 immunotherapy. Dose adjustment optimizes between efficacy and toxicity.",
      "key_evidence": {
        "study_name": "NCI 9177 / HOVON-127",
        "journal": "New England Journal of Medicine / Lancet Haematology",
        "year": 2020,
        "sample_size": 113,
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
          "treatment": 87,
          "control": 0
        }
      },
      "biomarker_requirements": [
        "CD20+",
        "MYC rearrangement confirmed"
      ],
      "notable_side_effects": [
        "Myelosuppression",
        "Febrile neutropenia",
        "Tumor lysis syndrome",
        "Mucositis",
        "Neuropat
... (truncated — read full file from experiment_reports\HN3-017_report.json)
```
