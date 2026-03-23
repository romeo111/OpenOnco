# Re-evaluation Task: HN3-008

## Context
- **Case ID**: HN3-008
- **Cancer type**: Recurrent/Metastatic Nasopharyngeal Carcinoma, EBV-Positive, Post-Definitive CRT
- **Stage**: rT2rN0M1 (Recurrent with liver metastases)
- **Molecular profile**: EBV-positive, Rising EBV DNA, PD-L1 CPS >= 20, Prior cisplatin exposure with neuropathy and hearing loss, Liver metastases
- **Report file**: experiment_reports\HN3-008_report.json
- **Current score**: 72/100
- **Gap analysis (local GPU)**: The lack of data on Toripalimab + Gemcitabine-Cisplatin (JUPITER-02) and Camrelizumab + Apatinib (Chemo-Free IO + Anti-VEGF) regimens will hinder the understanding of their efficacy in treating cancer patients, as these combinations are being explored for potential synergistic effects. Filling these gaps with high-quality data will significantly improve the score by providing a more comprehensive understanding of the clinical outcomes and safety profiles of these innovative treatments.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  14/25  |  56.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-008_report.json`.

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
    "cancer_type": "Recurrent/Metastatic Nasopharyngeal Carcinoma, EBV-Positive, Post-Definitive CRT",
    "stage": "rT2rN0M1 (Recurrent with liver metastases)",
    "molecular_profile": [
      "EBV-positive",
      "Rising EBV DNA",
      "PD-L1 CPS >= 20",
      "Prior cisplatin exposure with neuropathy and hearing loss",
      "Liver metastases"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Toripalimab + Gemcitabine-Cisplatin (JUPITER-02 Regimen)",
      "category": "Immunotherapy / Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "JUPITER-02 phase III RCT with 6-year follow-up; FDA approved October 2023; NCCN preferred first-line for R/M NPC; median OS 64.8 vs 33.7 months; strongest evidence in R/M NPC"
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "Median OS 64.8 vs 33.7 months (HR 0.62); median PFS 21.4 vs 8.2 months (HR 0.52); 3-year OS 64.5% vs 49.2%; unprecedented long-term survival benefit in metastatic NPC"
        },
        "accessibility": {
          "score": 9,
          "rationale": "FDA approved; toripalimab (Loqtorzi) commercially available; NCCN preferred regimen; approved in 40+ countries; established insurance coverage"
        },
        "safety_profile": {
          "score": 4,
          "rationale": "Patient has pre-existing cisplatin neuropathy and hearing loss; further cisplatin would worsen both; immune-related AEs 54.1%; grade 3+ irAEs 9.6%; cisplatin component problematic for this patient"
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "EBV-positive NPC is the target population; rising EBV DNA indicates active disease amenable to treatment; CPS>=20 highly favorable for checkpoint inhibitor response"
        }
      },
      "mechanism_of_action": "Toripalimab blocks PD-1/PD-L1 interaction restoring anti-tumor T-cell immunity against EBV-driven tumor cells. Combined with gemcitabine-cisplatin, achieves synergistic killing through immunogenic cell death and checkpoint blockade. EBV antigens serve as targets for enhanced immune recognition.",
      "key_evidence": {
        "study_name": "JUPITER-02 (6-Year Follow-Up)",
        "journal": "JAMA / ESMO Asia 2025",
        "year": 2025,
        "sample_size": 289,
        "os_months": {
          "treatment": 64.8,
          "control": 33.7,
          "hazard_ratio": 0.62,
          "p_value": 0.008
        },
        "pfs_months": {
          "treatment": 21.4,
          "control": 8.2
        },
        "orr_percent": {
          "treatment": 77,
          "control": 66
        }
      },
      "biomarker_requirements": [
        "R/M NPC diagnosis"
      ],
      "notable_side_effects": [
        "Immune-related AEs (54.1%)",
        "Nephrotoxicity from cisplatin",
        "Ototoxicity (CONCERN: pre-existing he
... (truncated — read full file from experiment_reports\HN3-008_report.json)
```
