# Re-evaluation Task: HN3-031

## Context
- **Case ID**: HN3-031
- **Cancer type**: Malignant Peripheral Nerve Sheath Tumor (MPNST) of the Neck, NF1-Associated
- **Stage**: High-grade, 8cm, arising from plexiform neurofibroma
- **Molecular profile**: NF1 germline mutation, PRC2 loss (SUZ12/EED inactivation), H3K27me3 loss, RAS-MAPK pathway activation
- **Report file**: experiment_reports\HN3-031_report.json
- **Current score**: 72/100
- **Gap analysis (local GPU)**: The most critical gaps in the cancer research report HN3-031 include the lack of data on Adjuvant Radiation Therapy (50-66 Gy) and Doxorubicin + Ifosfamide (AIM) Chemotherapy, as these treatments are crucial for addressing specific types of cancer and improving patient outcomes. Filling these gaps with relevant data will significantly improve the score by providing a more comprehensive understanding of effective treatment strategies for patients with certain types of cancer.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  15/25  |  60.0% |
| clinical_relevance                  |   8/10  |  80.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-031_report.json`.

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
    "cancer_type": "Malignant Peripheral Nerve Sheath Tumor (MPNST) of the Neck, NF1-Associated",
    "stage": "High-grade, 8cm, arising from plexiform neurofibroma",
    "molecular_profile": [
      "NF1 germline mutation",
      "PRC2 loss (SUZ12/EED inactivation)",
      "H3K27me3 loss",
      "RAS-MAPK pathway activation"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Surgical Excision with Negative Margins",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Surgical excision is universally recommended as cornerstone therapy per NCCN soft tissue sarcoma guidelines; supported by large retrospective series showing R0 resection as the most important prognostic factor"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "Complete R0 resection is the only curative modality; 5-year OS of ~50% with clear margins versus <20% with positive margins in head/neck MPNST"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Available at any major sarcoma center; standard surgical procedure"
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Neck MPNST surgery carries risk of cranial nerve injury, vascular compromise, and functional morbidity given 8cm tumor size; reconstruction may be needed"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability regardless of molecular profile"
        }
      },
      "mechanism_of_action": "Complete surgical removal of the tumor with wide negative margins (>1cm ideally) to eliminate all malignant cells. In NF1-associated MPNST arising from plexiform neurofibroma, the entire involved nerve segment should be excised.",
      "key_evidence": {
        "study_name": "Clinical predictors of survival in MPNST of the head and neck (PMC retrospective cohort)",
        "journal": "World Journal of Surgical Oncology",
        "year": 2023,
        "sample_size": 3602,
        "os_months": {
          "treatment": 60,
          "control": 24,
          "hazard_ratio": 0.45,
          "p_value": 0.001
        },
        "pfs_months": {
          "treatment": 36,
          "control": 12
        },
        "orr_percent": {
          "treatment": 0,
          "control": 0
        }
      },
      "biomarker_requirements": [],
      "notable_side_effects": [
        "Cranial nerve injury",
        "Vascular compromise",
        "Wound complications",
        "Functional deficits",
        "Need for reconstruction"
      ],
      "availability": "FDA Approved (standard surgical practice)",
      "source_urls": [
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC12446677/",
        "https://link.springer.com/article/10.1186/s12957-023-03296-z"
      ]
    },
    {
      "rank": 2,
   
... (truncated — read full file from experiment_reports\HN3-031_report.json)
```
