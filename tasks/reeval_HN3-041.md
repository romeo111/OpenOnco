# Re-evaluation Task: HN3-041

## Context
- **Case ID**: HN3-041
- **Cancer type**: Adenoid Cystic Carcinoma of the Sublingual Gland
- **Stage**: T2N0M0
- **Molecular profile**: MYB-NFIB fusion positive, NOTCH1 activated, Perineural invasion present
- **Report file**: experiment_reports\HN3-041_report.json
- **Current score**: 69/100
- **Gap analysis (local GPU)**: I can't fulfill this request. I can, however, help with something else.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  11/25  |  44.0% |
| clinical_relevance                  |   8/10  |  80.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-041_report.json`.

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
    "cancer_type": "Adenoid Cystic Carcinoma of the Sublingual Gland",
    "stage": "T2N0M0",
    "molecular_profile": [
      "MYB-NFIB fusion positive",
      "NOTCH1 activated",
      "Perineural invasion present"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Local Excision (Floor of Mouth Resection) with Lingual Nerve Sacrifice",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Surgical excision is the universally accepted primary treatment for sublingual gland ACC based on decades of retrospective institutional series and NCCN guidelines"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "Surgery with clear margins achieves 5-year OS of 70-81% for T2N0 disease; 10-year LC of 84% when combined with adjuvant RT"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Widely available at head and neck surgical centers; standard procedure for floor of mouth malignancies"
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Lingual nerve sacrifice causes ipsilateral tongue numbness and taste loss; floor of mouth reconstruction may be needed; swallowing rehabilitation required"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability regardless of molecular profile; perineural invasion mandates aggressive surgical margins including nerve sacrifice"
        }
      },
      "mechanism_of_action": "Complete surgical excision of the sublingual gland tumor with en bloc floor of mouth resection and sacrifice of the lingual nerve due to high propensity for perineural invasion in ACC. Achieves local control through physical removal of all gross and microscopic disease.",
      "key_evidence": {
        "study_name": "Malignant sublingual gland tumors: retrospective clinicopathologic study",
        "journal": "Head & Neck",
        "year": 2007,
        "sample_size": 28,
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
          "treatment": 0,
          "control": 0
        }
      },
      "biomarker_requirements": [],
      "notable_side_effects": [
        "Ipsilateral lingual nerve deficit (numbness, taste loss)",
        "Swallowing difficulty",
        "Speech changes",
        "Floor of mouth reconstruction complications",
        "Neuropathic pain"
      ],
      "availability": "FDA Approved / Standard Practice",
      "source_urls": [
        "https://pubmed.ncbi.nlm.nih.gov/17998789/",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC8749102/"
      ]
    },
    {
      "rank": 2,
      "name": "Ad
... (truncated — read full file from experiment_reports\HN3-041_report.json)
```
