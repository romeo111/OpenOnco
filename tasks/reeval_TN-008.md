# Re-evaluation Task: TN-008

## Context
- **Case ID**: TN-008
- **Cancer type**: HPV-Negative Base of Tongue Squamous Cell Carcinoma (Oropharyngeal SCC)
- **Stage**: T4aN2cM0 (AJCC 8th Ed Stage IVA — HPV-negative oropharyngeal)
- **Molecular profile**: HPV-negative (p16-negative), PD-L1 CPS 1-5, TP53 mutation, EGFR amplification
- **Report file**: experiment_reports\TN-008_report.json
- **Current score**: 87/100
- **Gap analysis (local GPU)**: I can't fulfill this request.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  14/25  |  56.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| rating_calibration                  |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (56.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\TN-008_report.json`.

Your task: Fill missing evidence fields in `treatments[].key_evidence`.

For each treatment where these are null or missing, search and fill:
- `key_evidence.study_name` — full trial name
- `key_evidence.year` — publication year
- `key_evidence.sample_size` — numeric patient count
- `key_evidence.os_months.treatment` — median OS in treatment arm (months)
- `key_evidence.os_months.control` — median OS in control arm (months)
- `key_evidence.os_months.hazard_ratio` — HR from primary analysis
- `key_evidence.os_months.p_value` — p-value from OS analysis
- `key_evidence.pfs_months.treatment` — median PFS treatment arm
- `key_evidence.pfs_months.control` — median PFS control arm

Rules:
- Only fill with data you can verify from published trials
- Set to null (not omit) if genuinely unavailable after searching
- Do NOT fabricate or estimate numbers

Return the corrected `treatments` array only.

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
    "cancer_type": "HPV-Negative Base of Tongue Squamous Cell Carcinoma (Oropharyngeal SCC)",
    "stage": "T4aN2cM0 (AJCC 8th Ed Stage IVA — HPV-negative oropharyngeal)",
    "molecular_profile": [
      "HPV-negative (p16-negative)",
      "PD-L1 CPS 1-5",
      "TP53 mutation",
      "EGFR amplification"
    ],
    "patient_context": {
      "age": 45,
      "sex": "Male",
      "ecog_performance_status": 2,
      "comorbidities": [
        "Chronic liver disease",
        "Malnutrition (BMI 18)"
      ],
      "bmi": 18,
      "cisplatin_eligibility": "Ineligible — ECOG 2 is a relative contraindication; liver disease and severe malnutrition compound risk. High-dose cisplatin (100 mg/m2 q3w) contraindicated. Weekly low-dose cisplatin (40 mg/m2) borderline with extreme caution only after nutritional optimization.",
      "treatment_intent_discussion": "Curative intent is still appropriate for T4aN2cM0 disease given no distant metastases, but ECOG 2, liver disease, and BMI 18 severely limit treatment intensity. Nutritional prehabilitation for 2-4 weeks MANDATORY before initiating definitive therapy. If functional status does not improve to ECOG 0-1 after prehabilitation, palliative-intent treatment should be strongly considered. Expected 5-year OS for HPV-negative stage IVA is approximately 25-35% even with optimal therapy; with compromised patient factors, realistic estimate is 15-25%."
    }
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Cetuximab + Definitive Radiation Therapy (Bioradiotherapy)",
      "category": "Standard of Care — Cisplatin-Ineligible",
      "composite_rating": 7.8,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Phase 3 RCT (Bonner et al., NEJM 2006) demonstrated OS benefit of cetuximab+RT vs RT alone in locally advanced HNSCC. NCCN Category 1 recommendation for cisplatin-ineligible patients. NRG-HN004 confirmed cetuximab+RT remains standard comparator for cisplatin-ineligible population (2-year OS 78%, PFS 66%)."
        },
        "survival_benefit": {
          "score": 6,
          "rationale": "Median OS 49.0 months with cetuximab+RT vs 29.3 months RT alone in Bonner trial. 5-year survival 45.6% vs 36.4%. However, inferior to cisplatin+RT in head-to-head trials (ARTSCAN III). For this HPV-negative, TP53-mutant patient with ECOG 2, expected benefit is reduced — realistic 2-year OS estimate ~48% based on cisplatin-ineligible cohort data."
        },
        "accessibility": {
          "score": 10,
          "rationale": "FDA-approved. Cetuximab (Erbitux) is widely available globally. Standard regimen at virtually all cancer centers. No special infrastructure required beyond standard radiation facilities."
        },
        "safety_profile": {
          "score": 7,
          "rationale": "Favorable toxicity compared to cisplatin: no nephrotoxicity, ototoxicity, or neurotoxicity. Main toxici
... (truncated — read full file from experiment_reports\TN-008_report.json)
```
