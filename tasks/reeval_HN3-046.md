# Re-evaluation Task: HN3-046

## Context
- **Case ID**: HN3-046
- **Cancer type**: Oral Cavity Squamous Cell Carcinoma with Massive N3b Lymphadenopathy
- **Stage**: T2N3bM0 (Stage IVB, AJCC 8th edition)
- **Molecular profile**: PD-L1 CPS 30, EGFR amplified, Skin-involving matted lymph nodes, N3b nodal burden (clinically matted, skin invasion)
- **Report file**: experiment_reports\HN3-046_report.json
- **Current score**: 72/100
- **Gap analysis (local GPU)**: The lack of data on Radical Surgery — Wide Excision + Modified Radical and Neoadjuvant Chemoradiation (INVERT Trial Regimen) are critical gaps that need to be addressed, as they directly impact the comprehensiveness of the report's findings on treatment outcomes for patients with cancer. Filling these gaps will improve the score by providing a more complete picture of the efficacy and safety of various treatments, allowing for more accurate conclusions about patient outcomes and guiding future research directions.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  13/25  |  52.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-046_report.json`.

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
    "cancer_type": "Oral Cavity Squamous Cell Carcinoma with Massive N3b Lymphadenopathy",
    "stage": "T2N3bM0 (Stage IVB, AJCC 8th edition)",
    "molecular_profile": [
      "PD-L1 CPS 30",
      "EGFR amplified",
      "Skin-involving matted lymph nodes",
      "N3b nodal burden (clinically matted, skin invasion)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Perioperative Pembrolizumab (KEYNOTE-689 Regimen) with Surgery and Adjuvant CRT",
      "category": "Standard of Care — Immunotherapy + Surgery",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "KEYNOTE-689 phase 3 RCT (NEJM 2025) demonstrated EFS HR 0.66 (p=0.004) in CPS>=10 population. FDA approved June 2025 for resectable LA HNSCC with PD-L1 CPS>=1. This patient's CPS 30 places them squarely in the most responsive subgroup. First perioperative immunotherapy approval in HNSCC."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "3-year EFS 59.8% vs 45.9% in CPS>=10 cohort. Median EFS 51.8 months vs 30.4 months. DMFS also improved (HR 0.71). However, N3b massive burden may attenuate benefit compared to trial population which was predominantly N0-N2. Still represents meaningful improvement over standard surgery + adjuvant CRT alone."
        },
        "accessibility": {
          "score": 9,
          "rationale": "FDA approved June 2025 for this indication. Pembrolizumab is widely available at major cancer centers. Covered by most insurance plans. Requires PD-L1 CPS>=1 which this patient meets (CPS 30)."
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Grade >=3 AEs 44.6% vs 42.9% in control arm — modest incremental toxicity. Immune-related AEs manageable. Neoadjuvant pembrolizumab did not impair surgical completion rates. Risk of immune-mediated hypothyroidism, hepatitis, pneumonitis. No new safety signals identified."
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "PD-L1 CPS 30 is well above the CPS>=1 threshold for FDA approval and CPS>=10 for maximum benefit. Higher CPS correlates with greater immunotherapy benefit. EGFR amplification does not preclude immunotherapy response in HNSCC."
        }
      },
      "mechanism_of_action": "Pembrolizumab is an anti-PD-1 monoclonal antibody that blocks PD-1/PD-L1 interaction, restoring T-cell-mediated antitumor immunity. Given as 2 neoadjuvant cycles before surgery, then continued as adjuvant with radiation +/- cisplatin, followed by single-agent maintenance for up to 15 cycles total.",
      "key_evidence": {
        "study_name": "KEYNOTE-689",
        "journal": "New England Journal of Medicine",
        "year": 2025,
        "sample_size": 714,
        "os_months": {
          "treatment": 51.8,
          "control": 30.4,
          "hazard_ratio": 0.73,
          "p_
... (truncated — read full file from experiment_reports\HN3-046_report.json)
```
