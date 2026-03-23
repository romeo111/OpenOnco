# Re-evaluation Task: HN3-034

## Context
- **Case ID**: HN3-034
- **Cancer type**: Adult Nasopharyngeal Rhabdomyosarcoma, Alveolar Type
- **Stage**: T2bN1M0 (Clinical Group III, Parameningeal site)
- **Molecular profile**: PAX3-FOXO1 fusion positive, Alveolar histology, FGFR4 overexpression (PAX3-FOXO1 driven), Potential CDK4 amplification
- **Report file**: experiment_reports\HN3-034_report.json
- **Current score**: 69/100
- **Gap analysis (local GPU)**: The most critical gaps in the cancer research report HN3-034 include the lack of data on Futibatinib (Irreversible FGFR1-4 Inhibitor) with a sample size, which is crucial for evaluating its efficacy and safety, and the absence of information on KDM4 Inhibitor (Epigenetic Targeted Therapy), which could provide valuable insights into its potential as an epigenetic targeted therapy. Fixing these gaps will improve the score by providing concrete data to support or refute the effectiveness of these promising treatments, allowing for more informed decision-making in cancer research and treatment.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  12/25  |  48.0% |
| clinical_relevance                  |   8/10  |  80.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-034_report.json`.

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
    "cancer_type": "Adult Nasopharyngeal Rhabdomyosarcoma, Alveolar Type",
    "stage": "T2bN1M0 (Clinical Group III, Parameningeal site)",
    "molecular_profile": [
      "PAX3-FOXO1 fusion positive",
      "Alveolar histology",
      "FGFR4 overexpression (PAX3-FOXO1 driven)",
      "Potential CDK4 amplification"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "VAC Chemotherapy (Vincristine + Actinomycin D + Cyclophosphamide) + Radiation Therapy",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "VAC is the established standard of care since the 1970s per COG and EpSSG protocols; Phase III RCT data (EpSSG RMS 2005); adapted from pediatric protocols for adult use"
        },
        "survival_benefit": {
          "score": 5,
          "rationale": "Adult RMS has 5-year OS ~27-30% vs 61% in pediatric cases; median OS ~20 months with VAC for localized adult RMS; PAX3-FOXO1+ alveolar has worse prognosis (~8% 4-year OS for metastatic)"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Standard chemotherapy agents widely available; radiation therapy universally available; well-established treatment protocols"
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Significant toxicity: myelosuppression, nausea, hepatotoxicity (actinomycin D), hemorrhagic cystitis (cyclophosphamide), peripheral neuropathy (vincristine); adults tolerate dose intensity less well than children"
        },
        "biomarker_match": {
          "score": 7,
          "rationale": "Standard treatment regardless of fusion status; PAX3-FOXO1+ cases receive risk-adapted intensification but same backbone agents"
        }
      },
      "mechanism_of_action": "Vincristine disrupts microtubule formation causing mitotic arrest. Actinomycin D intercalates DNA and inhibits RNA synthesis. Cyclophosphamide is an alkylating agent cross-linking DNA. Combined with intensity-modulated radiation therapy (IMRT) to the nasopharyngeal primary and involved nodes for local control.",
      "key_evidence": {
        "study_name": "EpSSG RMS 2005 Phase III trial and COG protocols for RMS",
        "journal": "The Lancet Oncology / Journal of Clinical Oncology",
        "year": 2018,
        "sample_size": 484,
        "os_months": {
          "treatment": 20,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 14,
          "control": 0
        },
        "orr_percent": {
          "treatment": 70,
          "control": 0
        }
      },
      "biomarker_requirements": [],
      "notable_side_effects": [
        "Myelosuppression",
        "Peripheral neuropathy",
        "Hepatotoxicity",
        "Hemorrhagic cystitis",
        "Nausea/vomiting",
       
... (truncated — read full file from experiment_reports\HN3-034_report.json)
```
