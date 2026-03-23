# Re-evaluation Task: HN2-014

## Context
- **Case ID**: HN2-014
- **Cancer type**: Skull Base Chordoma (Clivus, Brainstem Extension, Basilar Artery Encasement)
- **Stage**: Locally Advanced — Clivus origin with brainstem extension and basilar artery encasement
- **Molecular profile**: Brachyury/TBXT-positive (pathognomonic), PDGFR-expressing, EGFR-expressing, p16/CDKN2A loss likely
- **Report file**: experiment_reports\HN2-014_report.json
- **Current score**: 83/100
- **Gap analysis (local GPU)**: The most critical gaps in the cancer research report HN2-014 are the lack of data on Afatinib (Irreversible EGFR/HER2 Inhibitor) and Imatinib + Everolimus (PDGFR + mTOR Dual Inhibitor), which will improve the score by providing more comprehensive information on targeted therapies for specific cancer types. Filling these gaps with high-quality data will enable a more accurate assessment of treatment efficacy and safety, ultimately leading to better patient outcomes and improved research credibility.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| evidence_depth                      |  11/25  |  44.0% |
| rating_calibration                  |  13/15  |  86.7% |
| clinical_relevance                  |   9/10  |  90.0% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| source_quality                      |  15/15  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `evidence_depth` (44.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN2-014_report.json`.

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
    "cancer_type": "Skull Base Chordoma (Clivus, Brainstem Extension, Basilar Artery Encasement)",
    "stage": "Locally Advanced — Clivus origin with brainstem extension and basilar artery encasement",
    "molecular_profile": [
      "Brachyury/TBXT-positive (pathognomonic)",
      "PDGFR-expressing",
      "EGFR-expressing",
      "p16/CDKN2A loss likely"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Maximal Safe Endoscopic Endonasal Resection + Adjuvant Proton Beam Therapy (>70 GyRBE)",
      "category": "Standard of Care",
      "composite_rating": 8.2,
      "rating_breakdown": {
        "evidence_level": {
          "score": 9,
          "rationale": "Gold standard multimodal approach supported by decades of institutional series from MGH, PSI, and Loma Linda; dose-escalated proton therapy data from 112-patient series demonstrates robust outcomes. Proton therapy is the established standard for skull base chordoma."
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "5-year OS 78%, disease-specific survival 83%, 5-year local control 74% with subtotal resection. For GTR patients, 5-year LC reaches 95% and DSS 100%. Median dose 73.8 GyRBE delivers meaningful disease control in this otherwise lethal tumor."
        },
        "accessibility": {
          "score": 7,
          "rationale": "Proton therapy available at ~40 centers in the US and growing internationally. Endoscopic endonasal surgery for clivus chordoma requires specialized skull base neurosurgery centers. Both modalities are standard-of-care and insurance-covered."
        },
        "safety_profile": {
          "score": 7,
          "rationale": "No acute grade >=3 radiation toxicity reported. Late effects include hypopituitarism (17%), temporal lobe necrosis grade 3 (5%), vision loss (<3%). Surgical risks include CSF leak (11.8%), meningitis (23.5%), cranial nerve palsy (11.8%). Basilar encasement increases surgical risk."
        },
        "biomarker_match": {
          "score": 10,
          "rationale": "Universal applicability to all chordomas regardless of molecular profile. Brachyury/TBXT positivity confirms chordoma diagnosis. No biomarker restriction for surgery + proton therapy."
        }
      },
      "mechanism_of_action": "Maximal safe surgical debulking via endoscopic endonasal transsphenoidal approach provides direct midline access to clivus tumors, reducing tumor burden while preserving neurovascular structures. Adjuvant proton beam therapy at doses >70 GyRBE exploits the Bragg peak for precise dose deposition to residual tumor with steep dose falloff protecting brainstem, optic pathways, and temporal lobes. The high linear energy transfer at the Bragg peak end yields enhanced relative biological effectiveness against radiation-resistant chordoma cells.",
      "key_evidence": {
        "study_name": "Clinical Outcomes Following Dose-Escalated Pr
... (truncated — read full file from experiment_reports\HN2-014_report.json)
```
