# Re-evaluation Task: HN3-042

## Context
- **Case ID**: HN3-042
- **Cancer type**: Dermatofibrosarcoma Protuberans (DFSP) of the Neck with Fibrosarcomatous Transformation
- **Stage**: Locally Advanced (8 cm)
- **Molecular profile**: COL1A1-PDGFB fusion positive, Fibrosarcomatous areas (FS-DFSP), CD34 positive
- **Report file**: experiment_reports\HN3-042_report.json
- **Current score**: 64/100
- **Gap analysis (local GPU)**: The most critical gaps in the cancer research report HN3-042 are the lack of data on Imatinib Maintenance/Definitive Therapy (Unresectable disease) and Sunitinib (Second-Line TKI after Imatinib Resistance), as these are crucial components of treatment protocols for specific patient populations, and filling these gaps will provide more comprehensive insights into effective treatment strategies. Addressing these gaps will improve the score by providing a more complete understanding of treatment outcomes and allowing researchers to draw more informed conclusions about the efficacy of various therapies.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  10/25  |  40.0% |
| tier_coverage                       |   8/10  |  80.0% |
| clinical_relevance                  |   8/10  |  80.0% |
| combo_supportive_coverage           |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-042_report.json`.

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
    "cancer_type": "Dermatofibrosarcoma Protuberans (DFSP) of the Neck with Fibrosarcomatous Transformation",
    "stage": "Locally Advanced (8 cm)",
    "molecular_profile": [
      "COL1A1-PDGFB fusion positive",
      "Fibrosarcomatous areas (FS-DFSP)",
      "CD34 positive"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Neoadjuvant Imatinib (800 mg daily) Followed by Surgical Resection",
      "category": "Standard of Care / Approved Targeted Therapy",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "Phase II DeCOG trial and systematic review: 55.2% PR, 5.2% CR, median 31.5% tumor shrinkage; FDA/EMA-approved for DFSP with COL1A1-PDGFB fusion"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "Enables tissue-sparing surgery for 8cm neck tumor; converts borderline resectable to resectable; 40% of unresectable patients achieved R0 resection after imatinib"
        },
        "accessibility": {
          "score": 9,
          "rationale": "FDA-approved specifically for DFSP at 800 mg daily; widely available oral medication; NCCN 2025 guidelines recommend for borderline resectable disease"
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Well-tolerated; 25% grade 3/4 events in DeCOG trial; common AEs: edema, nausea, fatigue, rash; manageable toxicity profile"
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "COL1A1-PDGFB fusion directly drives PDGFR-beta autocrine signaling that imatinib specifically inhibits; this is the exact molecular target"
        }
      },
      "mechanism_of_action": "Imatinib is a selective tyrosine kinase inhibitor that blocks PDGFR-beta signaling driven by the COL1A1-PDGFB fusion oncoprotein. The fusion creates an autocrine loop of PDGF-BB production that constitutively activates PDGFR-beta; imatinib directly inhibits this receptor, halting tumor cell proliferation and inducing tumor shrinkage to facilitate surgical resection.",
      "key_evidence": {
        "study_name": "Neoadjuvant Imatinib in Advanced Primary or Locally Recurrent DFSP: Multicenter Phase II DeCOG Trial",
        "journal": "Clinical Cancer Research",
        "year": 2014,
        "sample_size": 16,
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
          "treatment": 57.1,
          "control": 0
        }
      },
      "biomarker_requirements": [
        "COL1A1-PDGFB fusion (t(17;22) translocation)",
        "PDGFR-beta expression"
      ],
      "notable_side_effects": [
        "Periorbital/peripheral edema",
        "Nausea",
        "Fatigue",
        "Rash",
        "Muscle cramp
... (truncated — read full file from experiment_reports\HN3-042_report.json)
```
