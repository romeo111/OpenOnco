# Re-evaluation Task: HN3-006

## Context
- **Case ID**: HN3-006
- **Cancer type**: Posterior Pharyngeal Wall Squamous Cell Carcinoma (Oropharyngeal Origin)
- **Stage**: T3N1M0 (Stage III, AJCC 8th Edition p16-negative)
- **Molecular profile**: TP53 mutation, PD-L1 CPS 15, HPV/p16-negative, Tobacco and alcohol associated
- **Report file**: experiment_reports\HN3-006_report.json
- **Current score**: 75/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN3-006 cancer research report include the lack of data on Cisplatin-Based Concurrent Chemoradiation and Pembrolizumab + Cisplatin/5-FU (KEYNOTE-048 Regime), which are crucial for understanding effective treatment regimens and improving patient outcomes. Filling these gaps will significantly enhance the score by providing valuable insights into the efficacy of concurrent chemoradiation and immunotherapy combinations, ultimately informing more personalized and effective treatment strategies.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  16/25  |  64.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-006_report.json`.

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
    "cancer_type": "Posterior Pharyngeal Wall Squamous Cell Carcinoma (Oropharyngeal Origin)",
    "stage": "T3N1M0 (Stage III, AJCC 8th Edition p16-negative)",
    "molecular_profile": [
      "TP53 mutation",
      "PD-L1 CPS 15",
      "HPV/p16-negative",
      "Tobacco and alcohol associated"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Definitive Cisplatin-Based Concurrent Chemoradiation (CRT)",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Multiple phase III RCTs (MACH-NC meta-analysis) demonstrate OS benefit of concurrent cisplatin with RT in locally advanced HNSCC; NCCN Category 1 recommendation for T3N1 disease"
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "5-year OS approximately 24-43% for posterior wall subsite; absolute survival benefit of 6-8% with addition of cisplatin to RT; median OS ~40 months for locally advanced p16-negative OPSCC"
        },
        "accessibility": {
          "score": 10,
          "rationale": "Universally available standard of care; cisplatin and radiation widely accessible globally"
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Significant toxicities including nephrotoxicity, ototoxicity, mucositis, severe dysphagia given posterior wall location; grade 3-4 AEs in ~70% of patients"
        },
        "biomarker_match": {
          "score": 7,
          "rationale": "Standard approach regardless of biomarkers; TP53 mutation may confer partial resistance but cisplatin-RT remains standard; PD-L1 status not relevant for definitive CRT"
        }
      },
      "mechanism_of_action": "Cisplatin forms platinum-DNA adducts causing interstrand crosslinks, inhibiting DNA repair and replication. Acts as a radiosensitizer by inhibiting DNA damage repair pathways, enhancing radiation-induced cell death through synergistic double-strand break accumulation.",
      "key_evidence": {
        "study_name": "MACH-NC Meta-Analysis Update",
        "journal": "Radiotherapy and Oncology",
        "year": 2009,
        "sample_size": 17346,
        "os_months": {
          "treatment": 40,
          "control": 34,
          "hazard_ratio": 0.81,
          "p_value": 0.001
        },
        "pfs_months": {
          "treatment": 30,
          "control": 22
        },
        "orr_percent": {
          "treatment": 0,
          "control": 0
        }
      },
      "biomarker_requirements": [],
      "notable_side_effects": [
        "Nephrotoxicity",
        "Ototoxicity",
        "Severe mucositis",
        "Dysphagia (especially problematic for posterior wall tumors)",
        "Myelosuppression",
        "Nausea/vomiting"
      ],
      "availability": "FDA Approved / Global Standard of Care",
      "source_urls": [
        "https://pubmed.ncb
... (truncated — read full file from experiment_reports\HN3-006_report.json)
```
