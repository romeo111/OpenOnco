# Re-evaluation Task: HN3-016

## Context
- **Case ID**: HN3-016
- **Cancer type**: Diffuse Large B-Cell Lymphoma (DLBCL) of Waldeyer's Ring/Tonsil
- **Stage**: Stage IIE
- **Molecular profile**: CD20+, GCB subtype, Extranodal (Waldeyer's ring/tonsil)
- **Report file**: experiment_reports\HN3-016_report.json
- **Current score**: 73/100
- **Gap analysis (local GPU)**: The lack of data on R-CHOP, Pola-R-CHP, and Tafasitamab + Lenalidomide regimens will hinder the understanding of their efficacy in treating non-Hodgkin lymphoma, as these combinations are considered promising therapeutic options that have shown positive results in clinical trials. Filling these gaps with high-quality data will significantly improve the score by providing a more comprehensive picture of treatment outcomes and guiding clinicians in making informed decisions about patient care.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  14/25  |  56.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-016_report.json`.

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
    "cancer_type": "Diffuse Large B-Cell Lymphoma (DLBCL) of Waldeyer's Ring/Tonsil",
    "stage": "Stage IIE",
    "molecular_profile": [
      "CD20+",
      "GCB subtype",
      "Extranodal (Waldeyer's ring/tonsil)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "R-CHOP (Rituximab, Cyclophosphamide, Doxorubicin, Vincristine, Prednisone)",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Multiple Phase 3 RCTs establish R-CHOP as gold standard for DLBCL; extensive evidence in GCB subtype and Waldeyer's ring presentations"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "GCB subtype 5-year PFS ~76% with R-CHOP; Stage IIE limited-stage carries favorable prognosis; cure rates 60-70% in limited-stage disease"
        },
        "accessibility": {
          "score": 10,
          "rationale": "FDA approved, universally available worldwide, on WHO essential medicines list"
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Well-characterized toxicity profile including myelosuppression, cardiotoxicity from doxorubicin, neuropathy from vincristine; manageable with supportive care"
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "CD20+ expression ensures rituximab target; GCB subtype has superior outcomes with R-CHOP compared to ABC subtype"
        }
      },
      "mechanism_of_action": "Rituximab targets CD20 on B-cells via ADCC and CDC; cyclophosphamide and doxorubicin are cytotoxic alkylating/intercalating agents; vincristine inhibits microtubule formation; prednisone provides anti-inflammatory and lympholytic effects.",
      "key_evidence": {
        "study_name": "GELA LNH-98.5 / MInT Trial",
        "journal": "New England Journal of Medicine / Lancet Oncology",
        "year": 2006,
        "sample_size": 824,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0.64,
          "p_value": 0.001
        },
        "pfs_months": {
          "treatment": 0,
          "control": 0
        },
        "orr_percent": {
          "treatment": 86,
          "control": 68
        }
      },
      "biomarker_requirements": [
        "CD20+"
      ],
      "notable_side_effects": [
        "Myelosuppression",
        "Febrile neutropenia",
        "Cardiotoxicity (doxorubicin)",
        "Peripheral neuropathy",
        "Tumor lysis syndrome",
        "Infusion reactions"
      ],
      "availability": "FDA Approved",
      "source_urls": [
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC6144206/",
        "https://ashpublications.org/blood/article/139/6/822/483215/Limited-stage-diffuse-large-B-cell-lymphoma"
      ]
    },
    {
      "rank": 2,
      "name": "Pola-R-CHP (Polatuzumab Vedotin + Rituximab, 
... (truncated — read full file from experiment_reports\HN3-016_report.json)
```
