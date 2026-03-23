# Re-evaluation Task: HN3-043

## Context
- **Case ID**: HN3-043
- **Cancer type**: Nasopharyngeal Carcinoma with Skull Base Invasion and Cranial Nerve III/VI Palsy
- **Stage**: T4N2M0
- **Molecular profile**: EBV positive, PD-L1 CPS >= 50, High EBV DNA titer
- **Report file**: experiment_reports\HN3-043_report.json
- **Current score**: 68/100
- **Gap analysis (local GPU)**: The lack of data on Toripalimab + Gemcitabine-Cisplatin (JUPITER-02) and Sintilimab + Induction Chemotherapy + Concurrent C are critical gaps, as they represent potential new treatment combinations that could provide valuable insights into improving patient outcomes for HN3-043. Addressing these gaps will improve the score by providing more comprehensive evidence on the efficacy of these novel treatments, which may offer improved survival rates or quality of life for patients with HN3-043.

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
| rating_calibration                  |   0/15  |   0.0% |
| evidence_depth                      |  10/25  |  40.0% |
| clinical_relevance                  |   9/10  |  90.0% |
| source_quality                      |  14/15  |  93.3% |
| structural_integrity                |  15/15  | 100.0% |
| tier_coverage                       |  10/10  | 100.0% |
| combo_supportive_coverage           |  10/10  | 100.0% |

## Target dimension: `rating_calibration` (0.0% of max)

## Your instructions

Read the full report JSON at `experiment_reports\HN3-043_report.json`.

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
    "cancer_type": "Nasopharyngeal Carcinoma with Skull Base Invasion and Cranial Nerve III/VI Palsy",
    "stage": "T4N2M0",
    "molecular_profile": [
      "EBV positive",
      "PD-L1 CPS >= 50",
      "High EBV DNA titer"
    ]
  },
  "treatments": [
    {
      "rank": 1,
      "name": "Induction Gemcitabine-Cisplatin (GP) Followed by Concurrent Chemoradiation (IMRT + Cisplatin)",
      "category": "Standard of Care",
      "composite_rating": 0,
      "rating_breakdown": {
        "evidence_level": {
          "score": 10,
          "rationale": "Phase 3 RCT published in NEJM demonstrated significant improvement in recurrence-free survival with GP induction + CCRT vs CCRT alone in high-risk locoregionally advanced NPC"
        },
        "survival_benefit": {
          "score": 8,
          "rationale": "3-year recurrence-free survival 85.3% vs 76.5%; EBV DNA-guided intensification further stratifies benefit; meta-analysis confirms IC+CCRT benefit for high EBV DNA patients"
        },
        "accessibility": {
          "score": 9,
          "rationale": "Standard regimen worldwide; all components widely available; NCCN category 1 recommendation for stage IVA NPC"
        },
        "safety_profile": {
          "score": 5,
          "rationale": "Significant acute toxicity: grade 3-4 neutropenia, thrombocytopenia, nausea during induction; concurrent cisplatin adds nephrotoxicity, ototoxicity; skull base dosimetry requires careful planning"
        },
        "biomarker_match": {
          "score": 9,
          "rationale": "EBV-positive NPC with high EBV DNA is the population that benefits most from induction chemotherapy intensification; EBV DNA clearance is a validated response biomarker"
        }
      },
      "mechanism_of_action": "Induction GP delivers systemic cytotoxicity to reduce tumor bulk and eliminate micrometastases before definitive chemoradiation. Gemcitabine inhibits DNA synthesis as a nucleoside analog; cisplatin forms DNA crosslinks. Concurrent cisplatin with IMRT provides radiosensitization. EBV DNA kinetics guide treatment adaptation.",
      "key_evidence": {
        "study_name": "Gemcitabine and Cisplatin Induction Chemotherapy in Nasopharyngeal Carcinoma (Phase 3 RCT)",
        "journal": "New England Journal of Medicine",
        "year": 2019,
        "sample_size": 480,
        "os_months": {
          "treatment": 0,
          "control": 0,
          "hazard_ratio": 0.43,
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
        "EBV positive (endemic NPC)"
      ],
      "notable_side_effects": [
        "Neutropenia (grade 3-4)",
        "Thrombocytopenia",
        "Nausea and vomiting",
        "Nephrotoxicity (cisplatin)",
        "Ototoxicity",
   
... (truncated — read full file from experiment_reports\HN3-043_report.json)
```
