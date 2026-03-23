# Re-evaluation Task: HN3-053

## Context
- **Case ID**: HN3-053
- **Cancer type**: Recurrent nasal septum mucosal melanoma
- **Stage**: rT2N0M0 — recurrent 18 months post-resection
- **Molecular profile**: NRAS Q61R mutation, KIT wild-type, PD-L1 40%, Mucosal melanoma subtype, 18 months post-initial resection recurrence
- **Report file**: experiment_reports\HN3-053_report.json
- **Current score**: 73/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN3-053 cancer research report include the lack of data on Nivolumab + Ipilimumab (Neoadjuvant/Definitive) and Salvage Re-excision + Adjuvant Proton Beam Radiation, which are essential for comprehensive understanding of treatment outcomes. Filling these gaps will significantly improve the score by providing more accurate information on effective treatment combinations and radiation therapy modalities, ultimately enhancing the reliability and validity of the report.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  16/25  |  64.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| combo_supportive_coverage           |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-053_report.json`.

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
    "cancer_type": "Recurrent nasal septum mucosal melanoma",
    "stage": "rT2N0M0 — recurrent 18 months post-resection",
    "molecular_profile": [
      "NRAS Q61R mutation",
      "KIT wild-type",
      "PD-L1 40%",
      "Mucosal melanoma subtype",
      "18 months post-initial resection recurrence"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Salvage Re-excision + Adjuvant Nivolumab + Ipilimumab",
      "category": "Immunotherapy",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 7,
          "rationale": "Surgery remains most effective local control for sinonasal mucosal melanoma per multiple retrospective series. Adjuvant nivo+ipi based on CheckMate-067 mucosal melanoma pooled analysis showing ORR 37-43% and 5-year OS 36%. No dedicated phase 3 for adjuvant ICI in mucosal melanoma, but strong extrapolation from cutaneous melanoma adjuvant data."
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "Salvage surgery achieves locoregional control in 60-70% when combined with adjuvant RT. Adding nivo+ipi addresses the 50-80% recurrence and distant failure rate. 5-year OS 36% with nivo+ipi in advanced mucosal melanoma (vs 17% nivo alone, 7% ipi alone). PD-L1 40% predicts above-average immunotherapy response."
        },
        "accessibility": {
          "score": 7,
          "rationale": "Salvage endoscopic resection available at experienced sinonasal surgery centers. Nivolumab and ipilimumab both FDA approved for melanoma. Combination regimen widely available. Off-label for adjuvant mucosal melanoma setting."
        },
        "safety_profile": {
          "score": 4,
          "rationale": "Nivo+ipi combination has grade 3-4 AEs in 40% of mucosal melanoma patients. Immune-related colitis, hepatitis, pneumonitis, endocrinopathies. Salvage surgery adds operative morbidity (septal perforation, nasal obstruction). Combined toxicity is significant."
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "PD-L1 40% is above average for mucosal melanoma (only 44% express PD-L1). Predicts enhanced immunotherapy response. NRAS Q61R does not preclude immunotherapy benefit. Combination nivo+ipi may overcome lower tumor mutational burden typical of mucosal melanoma."
        }
      },
      "mechanism_of_action": "Salvage surgical re-excision provides immediate local disease control, followed by adjuvant nivolumab (anti-PD-1) + ipilimumab (anti-CTLA-4) dual checkpoint blockade. Nivolumab blocks PD-1/PD-L1 interaction while ipilimumab releases CTLA-4-mediated T-cell suppression. Dual blockade produces complementary immune activation — ipilimumab primes T-cell responses while nivolumab sustains anti-tumor immunity. Critical for mucosal melanoma which has lower TMB and fewer neoantigens than cutaneous melanoma.",
      "key_evidence": {
        "study_nam
... (truncated — read full file from experiment_reports\HN3-053_report.json)
```
