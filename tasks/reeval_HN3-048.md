# Re-evaluation Task: HN3-048

## Context
- **Case ID**: HN3-048
- **Cancer type**: Sinonasal Teratocarcinosarcoma
- **Stage**: T4aN0M0 (Stage IVA, orbital invasion, mixed histological components)
- **Molecular profile**: Mixed epithelial, mesenchymal, and primitive neuroectodermal components, SMARCA4 loss characteristic, Possible beta-catenin activating mutation (Wnt pathway), Orbital invasion without distant metastasis
- **Report file**: experiment_reports\HN3-048_report.json
- **Current score**: 67/100
- **Gap analysis (local GPU)**: The lack of data on Adjuvant Radiation Therapy (IMRT or Proton Beam Therapy) and Histology-Directed Multiagent Chemotherapy (Cisplatin-based regimen) hinders the understanding of effective treatment strategies for patients with HN3-048, which will improve the score by providing more comprehensive insights into radiation therapy and chemotherapy regimens. Additionally, missing data on Endoscopic-Assisted Craniofacial Resection and Orbital Preservation with Induction Chemotherapy will limit the evaluation of minimally invasive surgical options and their potential benefits for patients with this specific cancer type.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |   9/25  |  36.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-048_report.json`.

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
    "cancer_type": "Sinonasal Teratocarcinosarcoma",
    "stage": "T4aN0M0 (Stage IVA, orbital invasion, mixed histological components)",
    "molecular_profile": [
      "Mixed epithelial, mesenchymal, and primitive neuroectodermal components",
      "SMARCA4 loss characteristic",
      "Possible beta-catenin activating mutation (Wnt pathway)",
      "Orbital invasion without distant metastasis"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Craniofacial Resection with Orbital Assessment + Adjuvant Chemoradiation",
      "category": "Standard of Care — Multimodal",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 7,
          "rationale": "Systematic review and survival analysis (PMC 2021) of SNTCS showed surgery + adjuvant therapy provides significant survival advantage over surgery alone (p<0.001). 90% of patients undergo surgery as primary treatment. Multimodal therapy (surgery + RT +/- chemo) is the most common approach in published series. No randomized trials exist due to extreme rarity (<100 reported cases)."
        },
        "survival_benefit": {
          "score": 6,
          "rationale": "Mean 2-year survival rate of 55% for SNTCS overall. Recurrence rate 38% with mean recurrence time 21.3 months. Combined therapy significantly improves survival over surgery alone. For T4a with orbital invasion, prognosis is worse than early-stage. Average survival <2 years. Multimodal approach offers best chance of disease control."
        },
        "accessibility": {
          "score": 6,
          "rationale": "Craniofacial resection requires specialized skull base surgical expertise at tertiary centers. Combined neurosurgical and otolaryngologic team needed. Endoscopic-assisted approaches increasingly available. Adjuvant CRT widely available. Limited to major academic medical centers."
        },
        "safety_profile": {
          "score": 4,
          "rationale": "Major surgery with significant morbidity. Complication rate 25-28% for craniofacial resection. Risks include CSF leak (11%), meningitis, orbital complications, brain injury, wound infection. Skull base reconstruction needed. If orbital exenteration required, permanent visual loss and disfigurement. Sequential CRT adds cumulative toxicity."
        },
        "biomarker_match": {
          "score": 8,
          "rationale": "Surgery is the cornerstone regardless of molecular profile. Mixed histology with multiple components all addressed by complete surgical resection. R0 margins are the primary determinant of outcome. Applicable to all SNTCS variants."
        }
      },
      "mechanism_of_action": "Open or endoscopic-assisted craniofacial resection achieves en bloc removal of the tumor involving the nasal cavity, paranasal sinuses, and anterior skull base. For T4a with orbital invasion, orbital preservation vs exenteration decision depends on 
... (truncated — read full file from experiment_reports\HN3-048_report.json)
```
