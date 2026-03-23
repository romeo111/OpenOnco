# Re-evaluation Task: HN3-013

## Context
- **Case ID**: HN3-013
- **Cancer type**: Post-Laryngectomy Stomal Recurrence — Bilateral Paratracheal Nodal Disease
- **Stage**: Recurrent — Peristomal with bilateral paratracheal nodes, 14 months post-TL
- **Molecular profile**: SCC histology, PD-L1 CPS >= 20, Post-total laryngectomy recurrence
- **Report file**: experiment_reports\HN3-013_report.json
- **Current score**: 70/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN3-013 cancer research report include the lack of data on Pembrolizumab + Platinum-Based Chemotherapy (First-Line — CPS >= 20) and Taxane-Based Palliative Chemotherapy (Docetaxel or Paclitaxel), which are essential for providing comprehensive treatment options and improving patient outcomes. Filling these gaps with high-quality data will significantly improve the report's score by providing a more complete understanding of effective treatments for patients with specific cancer types, thereby enhancing the overall credibility and usefulness of the research.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  14/25  |  56.0% |
| tier_coverage                       |   8/10  |  80.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-013_report.json`.

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
    "case_id": "HN3-013",
    "generated_date": "2026-03-23",
    "cancer_type": "Post-Laryngectomy Stomal Recurrence — Bilateral Paratracheal Nodal Disease",
    "stage": "Recurrent — Peristomal with bilateral paratracheal nodes, 14 months post-TL",
    "molecular_profile": [
      "SCC histology",
      "PD-L1 CPS >= 20",
      "Post-total laryngectomy recurrence"
    ],
    "patient_context": "45-year-old male, 14 months post-total laryngectomy, stomal recurrence with bilateral paratracheal lymph node involvement — most feared post-TL complication with very poor prognosis"
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Surgical Re-Excision with Mediastinal Tracheostomy + Manubrium Resection + Pectoralis Major Flap",
      "category": "Standard of Care — Salvage Surgery",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 7,
          "rationale": "Multiple case series and institutional reviews (38-patient manubrial resection series); Iowa Head and Neck Protocol for stomal recurrence; no RCTs due to rarity"
        },
        "survival_benefit": {
          "score": 5,
          "rationale": "1-year OS 80.6%, 5-year OS 55.6% in mediastinal tracheostomy series; however 2-year survival <25% in broader stomal recurrence literature; bilateral paratracheal nodes worsen prognosis significantly; offers best chance of cure among all options"
        },
        "accessibility": {
          "score": 5,
          "rationale": "Requires experienced head and neck surgeon comfortable with mediastinal dissection and manubrial resection; thoracic surgery collaboration often needed; limited to major academic centers"
        },
        "safety_profile": {
          "score": 4,
          "rationale": "Hospital mortality 5.3%; anastomotic leakage 17.6%; long-term stomal stenosis 47.4%; carotid blowout risk; major wound complications; pectoralis flap needed to protect great vessels"
        },
        "biomarker_match": {
          "score": 7,
          "rationale": "Applicable to all peristomal recurrences amenable to R0 resection; PD-L1 status not directly relevant for surgical indication but supports adjuvant immunotherapy"
        }
      },
      "mechanism_of_action": "Radical excision of stomal recurrence including tracheal resection with adequate inferior margins, bilateral paratracheal node dissection, manubrium resection with medial clavicular heads to access superior mediastinum. Anterior mediastinal tracheostomy created below innominate artery level. Pectoralis major myocutaneous flap provides vascularized tissue coverage to protect great vessels and reconstruct soft tissue defect. One-stage procedure when possible.",
      "key_evidence": {
        "study_name": "Manubrial Resection and Anterior Mediastinal Tracheostomy: Friend or Foe?",
        "journal": "The Laryngoscope",
        "year": 2011,
        "sample_size": 38,
        "os_months": {
          "tre
... (truncated — read full file from experiment_reports\HN3-013_report.json)
```
