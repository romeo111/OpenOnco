# Re-evaluation Task: HN3-022

## Context
- **Case ID**: HN3-022
- **Cancer type**: Myoepithelial Carcinoma of the Parotid Gland
- **Stage**: T3N1M0 — Locally advanced with nodal involvement
- **Molecular profile**: EWSR1 rearrangement, Ki-67 25% (high proliferative index), Sarcoma-like fusion gene
- **Report file**: experiment_reports\HN3-022_report.json
- **Current score**: 68/100
- **Gap analysis (local GPU)**: The most critical gaps in the cancer research report HN3-022 are the lack of data on Adjuvant Radiation Therapy (IMRT) — Post-Surgical and Comprehensive Molecular Profiling (NGS) for Basket, which are essential components of modern cancer treatment protocols that require up-to-date information to accurately assess treatment efficacy. Filling these gaps will improve the score by providing a more comprehensive understanding of the effectiveness of IMRT in reducing post-surgical recurrence and enabling the identification of specific molecular profiles that can guide targeted therapy decisions.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  12/25  |  48.0% |
| tier_coverage                       |   8/10  |  80.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| combo_supportive_coverage           |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| source_quality                      |  15/15  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-022_report.json`.

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
    "cancer_type": "Myoepithelial Carcinoma of the Parotid Gland",
    "stage": "T3N1M0 — Locally advanced with nodal involvement",
    "molecular_profile": [
      "EWSR1 rearrangement",
      "Ki-67 25% (high proliferative index)",
      "Sarcoma-like fusion gene"
    ],
    "patient_demographics": {
      "age": 45,
      "sex": "Male"
    },
    "clinical_context": "Myoepithelial carcinoma (malignant myoepithelioma) of the parotid gland in a 45-year-old male. T3N1M0 with EWSR1 rearrangement and Ki-67 of 25%, indicating high-grade biology. This is a rare salivary gland malignancy (<2% of all salivary gland tumors) with sarcoma-like gene fusions. Limited evidence base due to extreme rarity. Should be classified as high-grade malignancy. Treatment involves radical parotidectomy with neck dissection followed by adjuvant radiation therapy. Chemotherapy is empiric — doxorubicin/ifosfamide sarcoma-type regimens may be considered given the EWSR1 fusion and sarcoma-like biology. Ki-67 of 25% correlates with worse prognosis and supports aggressive multimodality treatment. 5-year OS approximately 70%. High rates of distant metastasis (22-33%) and local recurrence (30-41%). Molecular profiling should be pursued for potential basket trial enrollment."
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Radical Parotidectomy with Ipsilateral Neck Dissection",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "ASCO 2021 and ESMO/EURACAN 2022 guidelines recommend surgical resection as primary treatment for resectable salivary gland malignancies. Multiple retrospective series confirm surgery as mainstay of therapy. For T3N1 disease, radical parotidectomy with neck dissection is standard. No RCTs exist due to disease rarity."
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "5-year OS approximately 70% for myoepithelial carcinoma overall. Complete resection with negative margins provides the best chance of cure. T3N1 with high Ki-67 confers worse prognosis than early-stage disease. pN+ status is an independent predictor of decreased survival."
        },
        "accessibility": {
          "score": 9,
          "rationale": "Standard head and neck surgical procedure available at all major surgical centers. Requires experienced head and neck surgeon for facial nerve management and comprehensive neck dissection. Widely available."
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Facial nerve sacrifice may be necessary for T3 disease with nerve involvement. Risk of permanent facial palsy. Other risks include Frey syndrome, shoulder dysfunction (if spinal accessory nerve affected during neck dissection), wound infection, seroma, hematoma."
        },
        "biomarker_match": {
          "score": 10,
     
... (truncated — read full file from experiment_reports\HN3-022_report.json)
```
