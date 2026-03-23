# Re-evaluation Task: HN3-021

## Context
- **Case ID**: HN3-021
- **Cancer type**: Polymorphous Adenocarcinoma of the Hard Palate
- **Stage**: T1N0M0 — Low-grade, early stage
- **Molecular profile**: PRKD1 mutation (E710D hotspot), Low-grade histology, Minor salivary gland origin
- **Report file**: experiment_reports\HN3-021_report.json
- **Current score**: 68/100
- **Gap analysis (local GPU)**: The lack of data on Adjuvant Radiation Therapy (IMRT/Proton) for High-Risk Patients and Re-Excision for Positive or Close Margins are critical gaps that need to be addressed, as they directly impact treatment outcomes and patient survival rates. Filling these gaps with high-quality data will improve the score by providing a more comprehensive understanding of treatment efficacy and informing evidence-based clinical decision-making.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  10/25  |  40.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| combo_supportive_coverage           |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-021_report.json`.

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
    "cancer_type": "Polymorphous Adenocarcinoma of the Hard Palate",
    "stage": "T1N0M0 — Low-grade, early stage",
    "molecular_profile": [
      "PRKD1 mutation (E710D hotspot)",
      "Low-grade histology",
      "Minor salivary gland origin"
    ],
    "patient_demographics": {
      "age": 45,
      "sex": "Male"
    },
    "clinical_context": "Polymorphous adenocarcinoma (PAC) of the hard palate in a 45-year-old male. T1N0M0, low-grade, PRKD1 mutation positive. This is a low-grade salivary gland malignancy with excellent prognosis. Wide excision alone is curative for T1N0 disease with negative margins. Adjuvant radiation therapy is rarely needed for T1 tumors and should be avoided to prevent overtreatment. The PRKD1 E710D hotspot mutation is diagnostic and confirms indolent biology. Perineural invasion is histologically common (60-75%) but does not change the favorable prognosis in low-grade PAC. Palatal obturator prosthesis may be needed if wide excision creates an oroantral communication. 5-year disease-specific survival exceeds 98%. 10-year DSS is 94%. Recurrence rate is 9-19% but typically manageable with re-excision. Lymph node metastasis occurs in only 9-17% of all PAC cases and is essentially absent in T1N0 disease. Chemotherapy has no role in low-grade PAC. The key clinical principle is to avoid overtreatment of this indolent malignancy."
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Wide Local Excision / Partial Palatectomy with Negative Margins",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "ASCO 2021 and ESMO/EURACAN 2022 guidelines both recommend surgical excision as primary treatment for salivary gland malignancies. Multiple large retrospective series (>500 patients combined) confirm excellent outcomes with surgery alone for low-grade PAC. No RCTs exist because cure rates are so high. NCCN Head and Neck guidelines endorse surgery for resectable salivary gland cancers."
        },
        "survival_benefit": {
          "score": 10,
          "rationale": "5-year disease-specific survival 98%, 10-year DSS 94%. For T1N0 low-grade PAC with negative margins, cure rates approach 95-100%. This is a curative procedure. The 45-year-old patient has essentially normal life expectancy after complete excision with clear margins."
        },
        "accessibility": {
          "score": 10,
          "rationale": "Wide excision or partial palatectomy is a standard oral/maxillofacial surgery procedure available at any head and neck surgery center worldwide. No specialized equipment required. Straightforward outpatient or short-stay procedure."
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Minimal surgical morbidity for T1 palatal lesions. May create oroantral communication requiring palatal obturator. Ris
... (truncated — read full file from experiment_reports\HN3-021_report.json)
```
