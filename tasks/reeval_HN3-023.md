# Re-evaluation Task: HN3-023

## Context
- **Case ID**: HN3-023
- **Cancer type**: Parotid Lymphoepithelial Carcinoma, EBV-Associated
- **Stage**: T3N1M0 — Locally advanced with nodal involvement
- **Molecular profile**: EBV-positive (EBER+), PD-L1 CPS >=50 (high expression), Epstein-Barr virus driven
- **Report file**: experiment_reports\HN3-023_report.json
- **Current score**: 69/100
- **Gap analysis (local GPU)**: The lack of sample size data for Definitive Chemoradiation (Without Surgery) — NPC- and Ipilimumab + Nivolumab (Dual Checkpoint Blockade) will hinder the ability to accurately assess treatment efficacy, leading to a significant decrease in the overall score. Providing this critical information will enable researchers to better understand treatment outcomes, allowing for more informed decision-making and ultimately improving the score by providing a more comprehensive understanding of cancer research findings.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  10/25  |  40.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-023_report.json`.

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
    "cancer_type": "Parotid Lymphoepithelial Carcinoma, EBV-Associated",
    "stage": "T3N1M0 — Locally advanced with nodal involvement",
    "molecular_profile": [
      "EBV-positive (EBER+)",
      "PD-L1 CPS >=50 (high expression)",
      "Epstein-Barr virus driven"
    ],
    "patient_demographics": {
      "age": 45,
      "sex": "Male"
    },
    "clinical_context": "EBV-associated lymphoepithelial carcinoma (LEC) of the parotid gland in a 45-year-old male. T3N1M0, PD-L1 CPS >=50, EBV-positive. This rare salivary gland cancer is histologically identical to undifferentiated nasopharyngeal carcinoma (NPC) and shares its EBV-driven biology. Treatment parallels NPC protocols: cisplatin-based chemoradiation is highly effective as LEC is exquisitely radiosensitive. PD-L1 CPS >=50 makes this patient an excellent candidate for checkpoint inhibitor therapy — toripalimab is now FDA-approved for NPC. EBV promotes PD-L1 overexpression via LMP1-mediated pathways. Ethnic predisposition exists in Southeast Asian, Inuit, and North African populations (LEC accounts for 92% of salivary gland cancers in Inuit populations). 5-year OS is excellent at 90-97%. Multimodality treatment with surgery, adjuvant chemoradiation, and potential checkpoint inhibitor integration represents optimal management."
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Total Parotidectomy + Neck Dissection Followed by Adjuvant Cisplatin-Based Chemoradiation",
      "category": "Standard of Care — Multimodality",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "ASCO and ESMO guidelines recommend surgery + adjuvant RT for resectable salivary gland cancers. Multiple retrospective series confirm excellent outcomes with multimodality treatment for LEC (5-year OS 90-97%). NPC-analogous treatment protocols are well-established. NCDB analysis confirms survival benefit of adjuvant RT in high-risk salivary gland cancers (HR 0.76)."
        },
        "survival_benefit": {
          "score": 9,
          "rationale": "5-year OS 90-97%. 10-year OS 90.8%. LEC is exquisitely radiosensitive — combination multimodality therapy yields excellent outcomes whether lymph node metastases are present or not. Concurrent cisplatin enhances radiosensitivity. Surgery achieves gross disease removal; chemoradiation eliminates microscopic residual disease."
        },
        "accessibility": {
          "score": 9,
          "rationale": "Standard surgical procedure (parotidectomy + neck dissection) available at all head and neck surgical centers. IMRT widely available. Cisplatin is generic and universally accessible. Well-established treatment protocol."
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Combined toxicity of surgery (facial nerve risk, shoulder dysfunction) and chemoradiation (mucositis, xerostomia, nephrotox
... (truncated — read full file from experiment_reports\HN3-023_report.json)
```
