# Re-evaluation Task: HN2-016

## Context
- **Case ID**: HN2-016
- **Cancer type**: External Auditory Canal Squamous Cell Carcinoma (EAC SCC)
- **Stage**: T3N0M0 (Modified Pittsburgh Stage III) — Middle Ear Involvement
- **Molecular profile**: SCC histology, Chronic otitis media-associated (30-year history), Prior mastoidectomy consideration, PD-L1 CPS status unknown — testing recommended, EGFR expression likely (common in HNSCC)
- **Report file**: experiment_reports\HN2-016_report.json
- **Current score**: 86/100
- **Gap analysis (local GPU)**: The most critical gaps in the HN2-016 cancer research report are the lack of data on Perioperative Pembrolizumab (Neoadjuvant + Adjuvant) and Proton Beam Therapy (Adjuvant or Definitive), as these treatments have shown promise in improving outcomes for patients with head and neck cancer, particularly in terms of reducing recurrence rates and improving overall survival. Filling these gaps will improve the score by providing more comprehensive evidence on the effectiveness of these innovative treatments, which can inform treatment decisions and potentially lead to better patient outcomes.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  14/25  |  56.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (56.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-016_report.json`.

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
    "cancer_type": "External Auditory Canal Squamous Cell Carcinoma (EAC SCC)",
    "stage": "T3N0M0 (Modified Pittsburgh Stage III) — Middle Ear Involvement",
    "molecular_profile": [
      "SCC histology",
      "Chronic otitis media-associated (30-year history)",
      "Prior mastoidectomy consideration",
      "PD-L1 CPS status unknown — testing recommended",
      "EGFR expression likely (common in HNSCC)"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Lateral Temporal Bone Resection (LTBR) + Adjuvant IMRT (60-66 Gy)",
      "category": "Standard of Care",
      "composite_rating": 7.1,
      "rating_breakdown": {
        "evidence_level": {
          "score": 7,
          "rationale": "No Phase 3 RCTs exist for this ultra-rare cancer (~1/million incidence). Evidence derives from multiple retrospective institutional series and systematic reviews/meta-analyses with consistent results across centers. The largest meta-analysis included 752 patients. Modified Pittsburgh staging validated across institutions."
        },
        "survival_benefit": {
          "score": 7,
          "rationale": "For T3N0M0 EAC SCC, LTBR + adjuvant RT yields 5-year OS of 50-67% and 5-year DSS of 87.5% in Stage III. Clear surgical margins are the strongest predictor of survival. Adjuvant RT improves outcomes significantly (p=0.02 for SCC patients). 5-year LRC of 66.2% with adjuvant RT."
        },
        "accessibility": {
          "score": 7,
          "rationale": "Available at major academic medical centers with skull base surgery programs. Requires specialized otologic/neurotologic surgical expertise. IMRT widely available. Prior mastoidectomy may complicate the surgical approach but does not preclude LTBR in experienced hands."
        },
        "safety_profile": {
          "score": 6,
          "rationale": "LTBR involves en bloc resection of the ear canal, tympanic membrane, malleus, and incus. Expected ipsilateral conductive hearing loss. Facial nerve preservation possible if not involved (T3 stage). Prior mastoidectomy alters anatomy and increases surgical complexity. RT side effects include fibrosis, osteoradionecrosis risk. IMRT reduces late toxicity vs 3D-CRT (8.7% vs 38.1% grade 2+ fibrosis)."
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "Universal applicability — no biomarker requirements. Standard of care for all T3 EAC SCC regardless of molecular profile. Applicable to chronic otitis media-associated cases."
        }
      },
      "mechanism_of_action": "En bloc surgical excision of the external auditory canal with surrounding temporal bone (lateral compartment), removing the bony and cartilaginous canal, tympanic membrane, malleus, and incus while preserving the stapes, facial nerve, and inner ear structures. Adjuvant intensity-modulated radiotherapy delivers 60-66 Gy to the tumor bed to eradicate microscopic residual dis
... (truncated — read full file from experiment_reports\HN2-016_report.json)
```
