# Re-evaluation Task: HN3-032

## Context
- **Case ID**: HN3-032
- **Cancer type**: Sinonasal Hemangiopericytoma / Solitary Fibrous Tumor (Glomangiopericytoma)
- **Stage**: Low-grade, low mitotic index, 4cm nasal cavity
- **Molecular profile**: NAB2-STAT6 fusion positive, STAT6 nuclear expression, Low mitotic activity
- **Report file**: experiment_reports\HN3-032_report.json
- **Current score**: 65/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN3-032 cancer research report are the lack of data on Adjuvant Radiation Therapy for positive margins and Pazopanib treatment for recurrent/unresectable Soft Tissue Fibroma (SFT), as these interventions are crucial for improving patient outcomes and survival rates. Filling these gaps will significantly improve the score by providing more comprehensive evidence-based information on effective treatments for SFT, which is essential for advancing cancer research and clinical practice.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  11/25  |  44.0% |
| clinical_relevance                  |   7/10  |  70.0% |
| combo_supportive_coverage           |   8/10  |  80.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-032_report.json`.

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
    "cancer_type": "Sinonasal Hemangiopericytoma / Solitary Fibrous Tumor (Glomangiopericytoma)",
    "stage": "Low-grade, low mitotic index, 4cm nasal cavity",
    "molecular_profile": [
      "NAB2-STAT6 fusion positive",
      "STAT6 nuclear expression",
      "Low mitotic activity"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Endoscopic Surgical Resection",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "Multiple systematic reviews and case series confirm endoscopic resection as gold standard for sinonasal HPC/SFT; no significant difference in recurrence vs open approaches"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "Complete excision is curative in vast majority; 5-year OS 88% and DFS 74%; 97% disease-specific survival; this is a low-grade tumor with excellent prognosis when fully excised"
        },
        "accessibility": {
          "score": 10,
          "rationale": "Available at any otolaryngology center with endoscopic sinus surgery capability; standard surgical technique"
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Endoscopic approach is minimally invasive with low morbidity; main risk is intraoperative hemorrhage given vascular nature; lower complication rate than open approaches"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability; standard treatment regardless of molecular profile"
        }
      },
      "mechanism_of_action": "Complete endoscopic endonasal surgical removal of the tumor from the nasal cavity and paranasal sinuses with adequate margins. The endoscopic approach allows excellent visualization and precise dissection while preserving normal sinonasal anatomy.",
      "key_evidence": {
        "study_name": "Systematic review of treatment and prognosis of sinonasal hemangiopericytoma",
        "journal": "Head & Neck",
        "year": 2012,
        "sample_size": 194,
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
        "Intraoperative hemorrhage",
        "Epistaxis",
        "Nasal crusting",
        "Synechiae formation",
        "Rarely CSF leak"
      ],
      "availability": "Widely available standard procedure",
      "source_urls": [
        "https://pubmed.ncbi.nlm.nih.gov/22733718/",
        "https://pubmed.ncbi.nlm.nih.gov/22049019/"
      ]
    },
    {
      "rank": 2,
      "name": "Preoperative Embolization + Endoscopic Resection",

... (truncated — read full file from experiment_reports\HN3-032_report.json)
```
