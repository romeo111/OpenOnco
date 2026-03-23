# Re-evaluation Task: HN3-014

## Context
- **Case ID**: HN3-014
- **Cancer type**: Nasal Cavity Squamous Cell Carcinoma with Ethmoid Extension — Occupational (Nickel)
- **Stage**: T3N0M0 (Stage III)
- **Molecular profile**: SCC histology, Nickel refinery occupational exposure, Ethmoid sinus extension, No nodal involvement
- **Report file**: experiment_reports\HN3-014_report.json
- **Current score**: 66/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN3-014 cancer research report are the lack of data on Definitive Radiation Therapy Alone (Non-Surgical C) and Induction Chemotherapy (TPF) Followed by Surgery, which will be addressed to improve the score as these treatments provide crucial information on non-surgical and neoadjuvant approaches. Fixing these gaps will enhance the report's credibility and provide valuable insights into treatment options for patients with head and neck cancer, ultimately leading to a higher score of 100/100.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |   9/25  |  36.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| combo_supportive_coverage           |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-014_report.json`.

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
    "case_id": "HN3-014",
    "generated_date": "2026-03-23",
    "cancer_type": "Nasal Cavity Squamous Cell Carcinoma with Ethmoid Extension — Occupational (Nickel)",
    "stage": "T3N0M0 (Stage III)",
    "molecular_profile": [
      "SCC histology",
      "Nickel refinery occupational exposure",
      "Ethmoid sinus extension",
      "No nodal involvement"
    ],
    "patient_context": "45-year-old male nickel refinery worker with occupational nasal cavity SCC, T3 with ethmoid extension, distinct from maxillary sinus SCC"
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Endoscopic Medial Maxillectomy + Ethmoidectomy + Adjuvant Radiation Therapy",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 8,
          "rationale": "Multiple retrospective studies and pooled analyses (1,404 cases) demonstrating equivalent or superior outcomes to open approaches; NCCN-recommended endoscopic approach for appropriate sinonasal cancers"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year OS 78% with negative margins in definitive resection group; 5-year OS 93% with negative margins specifically; local recurrence 17.8% endoscopic vs 38.5% open; nasal cavity primary has better prognosis (77% 5-year survival) than maxillary sinus (62%)"
        },
        "accessibility": {
          "score": 7,
          "rationale": "Requires experienced endoscopic skull base surgeon; available at major academic centers and tertiary ENT departments; specialized equipment needed"
        },
        "safety_profile": {
          "score": 8,
          "rationale": "Lower morbidity than open craniofacial resection; no facial incision; shorter hospital stay; faster healing; preserves facial cosmesis; avoids craniotomy in most T3 cases"
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Ideal for nasal cavity primary with ethmoid extension (T3N0); endoscopic approach well-suited for laterally based tumors requiring medial maxillectomy; occupational etiology does not change surgical approach"
        }
      },
      "mechanism_of_action": "Transnasal endoscopic resection of the lateral nasal wall (medial maxillectomy) with complete ethmoidectomy for tumor extending into ethmoid sinuses. Boundaries include nasal floor inferiorly, cribriform plate/fovea ethmoidalis superiorly, anterior maxillary wall anteriorly, and posterior ethmoid posteriorly. Frozen section margin analysis during surgery. Adjuvant RT (60-66 Gy) to tumor bed addresses microscopic residual disease risk.",
      "key_evidence": {
        "study_name": "Endoscopic surgery for SCC in nasal cavity and ethmoid sinus: retrospective observational study",
        "journal": "Auris Nasus Larynx",
        "year": 2024,
        "sample_size": 27,
        "os_months": {
          "treatment": 0,
          "control": 0,
      
... (truncated — read full file from experiment_reports\HN3-014_report.json)
```
