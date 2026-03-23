# Re-evaluation Task: HN3-012

## Context
- **Case ID**: HN3-012
- **Cancer type**: Glottic Squamous Cell Carcinoma T4a with Thyroid Cartilage Invasion
- **Stage**: T4aN2M0 (Stage IVA)
- **Molecular profile**: SCC histology, PD-L1 CPS 15, Thyroid cartilage invasion
- **Report file**: experiment_reports\HN3-012_report.json
- **Current score**: 70/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN3-012 cancer research report include the lack of data on Perioperative Pembrolizumab + Total Laryngectomy and Induction Chemoimmunotherapy (TPF + Anti-PD-1) for Squamous Cell Carcinoma, which will improve the score by providing more comprehensive information on the efficacy of immunotherapies in combination with surgery. Filling these gaps will enable researchers to better understand the optimal treatment strategies for patients with laryngeal cancer, ultimately leading to improved patient outcomes and a higher score.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  12/25  |  48.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-012_report.json`.

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
    "case_id": "HN3-012",
    "generated_date": "2026-03-23",
    "cancer_type": "Glottic Squamous Cell Carcinoma T4a with Thyroid Cartilage Invasion",
    "stage": "T4aN2M0 (Stage IVA)",
    "molecular_profile": [
      "SCC histology",
      "PD-L1 CPS 15",
      "Thyroid cartilage invasion"
    ],
    "patient_context": "45-year-old male with COPD, requires careful consideration of pulmonary function for treatment selection"
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Total Laryngectomy + Bilateral Neck Dissection + Adjuvant RT/CRT + Primary TEP",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "NCCN Category 1 recommendation for T4a laryngeal cancer; multiple population-based studies and systematic reviews demonstrating superior survival over organ preservation for T4a disease"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year OS 60% for T4a with TL; median OS 87.2 months vs 31.3 months for larynx-preservation; 2-year OS 81.3% and DFS 78%; N2 disease reduces 5-year OS to approximately 30-40%"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Available at all head and neck surgery centers; standard insurance coverage; well-established surgical technique"
        },
        "safety_profile": {
          "score": 6,
          "rationale": "Major surgery requiring permanent stoma; loss of natural voice (mitigated by TEP); dysphagia risk; pharyngocutaneous fistula risk 15-25%; COPD increases perioperative pulmonary complications"
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Standard approach regardless of PD-L1 status; thyroid cartilage invasion is the primary indication for TL over organ preservation"
        }
      },
      "mechanism_of_action": "Complete surgical removal of the larynx including thyroid cartilage, epiglottis, hyoid bone, and pre-epiglottic/paraglottic spaces. Bilateral selective neck dissection (levels II-IV) addresses N2 nodal disease. Primary tracheoesophageal puncture (TEP) with voice prosthesis placement at time of laryngectomy enables post-operative alaryngeal voice. Adjuvant RT (60 Gy) or CRT (with cisplatin) based on pathologic risk features.",
      "key_evidence": {
        "study_name": "T4a laryngeal cancer survival: retrospective institutional analysis and systematic review",
        "journal": "Journal of Surgical Oncology",
        "year": 2014,
        "sample_size": 148,
        "os_months": {
          "treatment": 87.2,
          "control": 31.3,
          "hazard_ratio": 0,
          "p_value": 0.001
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
      "biomarker_requirements": [
        "Confi
... (truncated — read full file from experiment_reports\HN3-012_report.json)
```
