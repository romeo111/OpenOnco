# Re-evaluation Task: HN3-019

## Context
- **Case ID**: HN3-019
- **Cancer type**: Salivary Duct Carcinoma of Parotid Gland
- **Stage**: T4aN2M0 (Locally Advanced, Facial Nerve Invaded)
- **Molecular profile**: AR+ (Androgen Receptor Positive), HER2 3+ (Overexpression), Facial nerve invasion
- **Report file**: experiment_reports\HN3-019_report.json
- **Current score**: 71/100
- **Gap analysis (local GPU)**: The most critical gaps in HN3-019's research report include the lack of data on Adjuvant Radiation Therapy (60-66 Gy) Post-Surgery, which is a crucial aspect of post-operative care for patients with head and neck cancer, and Trastuzumab Deruxtecan (T-DXd / Enhertu) — Tumor-A, a promising HER2-targeted treatment that has shown significant efficacy in other cancers. Addressing these gaps will improve the score by providing more comprehensive information on effective post-operative treatments and targeted therapies for patients with head and neck cancer.

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

Read the full report JSON at `experiment_reports\HN3-019_report.json`.

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
    "cancer_type": "Salivary Duct Carcinoma of Parotid Gland",
    "stage": "T4aN2M0 (Locally Advanced, Facial Nerve Invaded)",
    "molecular_profile": [
      "AR+ (Androgen Receptor Positive)",
      "HER2 3+ (Overexpression)",
      "Facial nerve invasion"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Radical Parotidectomy + Neck Dissection + Facial Nerve Sacrifice with Immediate Reanimation",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "NCCN/ASCO guidelines mandate radical surgery for T4a salivary duct carcinoma with facial nerve invasion; multi-institutional analyses of 141+ patients validate approach; standard of care worldwide"
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "3-year OS ~70.5% and DFS ~38.2% for SDC overall; R0 resection is strongest predictor of survival; T4aN2 has poor DFS but surgery remains only curative-intent option; facial nerve sacrifice required for invaded nerve"
        },
        "accessibility": {
          "score": 8,
          "rationale": "Available at head and neck surgery centers; requires experienced parotid surgeon for nerve reanimation; immediate facial reanimation preferred at time of sacrifice"
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Facial nerve sacrifice causes permanent facial paralysis; immediate reanimation improves functional outcomes; Frey syndrome, wound complications, shoulder dysfunction from neck dissection; nerve grafting from sural or great auricular nerve"
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Surgery indicated regardless of molecular profile for resectable T4a disease; R0 resection enables adjuvant targeted therapy based on AR+ and HER2+ status"
        }
      },
      "mechanism_of_action": "Radical parotidectomy with total removal of parotid gland and sacrificed facial nerve segments involved by tumor. Comprehensive neck dissection (levels I-V) addresses N2 nodal disease. Immediate facial reanimation using nerve grafts (sural nerve, great auricular nerve) or sling procedures restores facial symmetry and eye closure.",
      "key_evidence": {
        "study_name": "Multi-Institutional SDC Analysis",
        "journal": "Head & Neck / Oral Oncology",
        "year": 2016,
        "sample_size": 141,
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
        "Permanent facial paralysis (requires reanimation)",
        "Frey syndrome
... (truncated — read full file from experiment_reports\HN3-019_report.json)
```
