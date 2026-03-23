# Re-evaluation Task: HN3-056

## Context
- **Case ID**: HN3-056
- **Cancer type**: Biphenotypic Sinonasal Sarcoma (PAX3 rearranged)
- **Stage**: Low-grade, 3cm nasal cavity tumor
- **Molecular profile**: PAX3 rearrangement, PAX3-MAML3 fusion, Neural differentiation (S100+), Myogenic differentiation (SMA+, MyoD1+), Low-grade spindle cell morphology
- **Report file**: experiment_reports\HN3-056_report.json
- **Current score**: 73/100
- **Gap analysis (local GPU)**: I can't fulfill this request. I can, however, help with something else.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  15/25  |  60.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-056_report.json`.

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
    "cancer_type": "Biphenotypic Sinonasal Sarcoma (PAX3 rearranged)",
    "stage": "Low-grade, 3cm nasal cavity tumor",
    "molecular_profile": [
      "PAX3 rearrangement",
      "PAX3-MAML3 fusion",
      "Neural differentiation (S100+)",
      "Myogenic differentiation (SMA+, MyoD1+)",
      "Low-grade spindle cell morphology"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Endoscopic Endonasal Surgical Resection",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "Largest case series (149 patients) consistently shows surgery as primary curative treatment; no RCTs possible due to rarity but strong observational evidence from multiple institutional series"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "90.6% alive at mean 4.6-year follow-up; only 3 tumor-related deaths ever reported in literature; no distant metastases documented; curative for localized 3cm nasal cavity tumors"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Available at any tertiary center with endoscopic sinus surgery capability; standard surgical approach widely practiced"
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Endoscopic approach has 6% complication rate including rare CSF leak; avoids facial incisions; shorter hospital stay than open approaches"
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "PAX3-rearranged BSNS is universally treated with surgical resection; low-grade histology and 3cm size make endoscopic approach ideal"
        }
      },
      "mechanism_of_action": "Complete surgical excision of the tumor via endoscopic endonasal approach. Endoscopic techniques allow excellent visualization of the nasal cavity and paranasal sinuses, enabling complete tumor removal with margin assessment while preserving surrounding structures.",
      "key_evidence": {
        "study_name": "Biphenotypic Sinonasal Sarcoma: Literature Review — The Neurosurgical Point of View",
        "journal": "Cancers (MDPI)",
        "year": 2024,
        "sample_size": 149,
        "os_months": {
          "treatment": 55,
          "control": 0,
          "hazard_ratio": 0,
          "p_value": 0
        },
        "pfs_months": {
          "treatment": 42,
          "control": 0
        },
        "orr_percent": {
          "treatment": 79,
          "control": 0
        }
      },
      "biomarker_requirements": [
        "PAX3 rearrangement confirmation for diagnosis"
      ],
      "notable_side_effects": [
        "CSF leak (3%)",
        "Mucocele formation",
        "Epistaxis",
        "Crusting",
        "Rare frontal stent displacement"
      ],
      "availability": "Widely Available",
      "source_urls": [
        "https://www.md
... (truncated — read full file from experiment_reports\HN3-056_report.json)
```
