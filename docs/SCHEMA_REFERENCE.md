# Report JSON Schema Reference

All research reports in the database use this schema.
`cancer_research_scorer.py` and `evaluate.py` validate against it.

---

## Top-Level Structure

```json
{
  "report_metadata":         { ... },
  "treatments":              [ ... ],
  "clinical_trials":         [ ... ],
  "combination_strategies":  [ ... ],
  "supportive_care":         [ ... ],
  "sources":                 [ ... ]
}
```

---

## `report_metadata`

```json
{
  "report_metadata": {
    "generated_date":   "2026-03-23",           // ISO 8601 date string
    "cancer_type":      "Glioblastoma, IDH-wildtype, MGMT-methylated",
    "stage":            "WHO Grade 4 (T2N0M0 equivalent — CNS staging)",
    "molecular_profile": ["IDH-wildtype", "MGMT-methylated", "EGFRvIII-"],
    "case_id":          "GBM-001",              // matches benchmark_cases.json id
    "strategy_version": "seed-1.0"              // strategy.md version used
  }
}
```

| Field | Required | Notes |
|---|---|---|
| `generated_date` | Yes | Date of report generation |
| `cancer_type` | Yes | Specific histological name, not generic |
| `stage` | Yes | AJCC/TNM or disease-specific staging |
| `molecular_profile` | Yes | Array of key molecular markers |
| `case_id` | Recommended | Links report to benchmark case |
| `strategy_version` | Recommended | Tracks which strategy.md version was used |

---

## `treatments`

Array of treatment objects, sorted by `composite_rating` descending.
Minimum 8, maximum 15 entries. Each entry:

```json
{
  "rank": 1,
  "name": "Temozolomide + Radiation (Stupp Protocol)",
  "category": "Standard of Care",
  "intent": "curative",
  "composite_rating": 8.1,

  "rating_breakdown": {
    "evidence_level":   { "score": 9, "rationale": "EORTC 26981 Phase 3 RCT, N=573..." },
    "survival_benefit": { "score": 7, "rationale": "Median OS 14.6 vs 12.1 months (HR 0.63)..." },
    "accessibility":    { "score": 10, "rationale": "FDA approved, globally available..." },
    "safety_profile":   { "score": 6, "rationale": "Myelosuppression, fatigue, nausea..." },
    "biomarker_match":  { "score": 8, "rationale": "MGMT methylation predicts TMZ benefit..." }
  },

  "mechanism_of_action": "Temozolomide alkylates DNA at O6-guanine position...",

  "key_evidence": {
    "study_name":   "EORTC 26981 / NCIC CTG CE.3 (Stupp et al.)",
    "journal":      "New England Journal of Medicine",
    "year":         2005,
    "sample_size":  573,
    "os_months": {
      "treatment":    14.6,
      "control":      12.1,
      "hazard_ratio": 0.63,
      "p_value":      0.001
    },
    "pfs_months": {
      "treatment":    6.9,
      "control":      5.0
    },
    "orr_percent": {
      "treatment":    null,
      "control":      null
    }
  },

  "biomarker_requirements": ["MGMT promoter methylation preferred but not required"],
  "ps_requirement":         "ECOG 0-2",
  "notable_side_effects": [
    "Myelosuppression (grade 3-4 in 7%)",
    "Fatigue (all grades 61%)",
    "Nausea/vomiting (manageable with antiemetics)",
    "LATE: lymphopenia, opportunistic infections (PCP prophylaxis required)"
  ],
  "qol_impact":    "Cognitive effects from whole-brain radiation; IMRT minimizes dose to hippocampus",
  "availability":  "FDA approved, universally available",
  "source_urls": [
    "https://www.nejm.org/doi/full/10.1056/NEJMoa043330"
  ]
}
```

### `intent` values (mandatory)

| Value | Use when |
|---|---|
| `curative` | Definitive therapy for localized disease (Stage I-III, resectable) |
| `adjuvant` | Post-operative treatment to prevent recurrence |
| `neoadjuvant` | Pre-operative treatment to downstage or shrink |
| `palliative` | Stage IV M1, unresectable, or recurrent incurable disease |
| `salvage` | Second/third-line after prior treatment failure |
| `maintenance` | Ongoing treatment to delay progression after response |
| `preventive` | Risk reduction post-curative treatment completion |

### `composite_rating` formula

```
composite = (evidence_level × 0.30)
           + (survival_benefit × 0.30)
           + (accessibility × 0.15)
           + (safety_profile × 0.15)
           + (biomarker_match × 0.10)
```

Round to 1 decimal place. All component scores are integers 1-10.

### Rating anchors — `evidence_level`

| Score | Evidence |
|---|---|
| 10 | Large Phase 3 RCT, top journal, >500 patients |
| 8-9 | Phase 3 RCT, moderate N, clear statistical significance |
| 7 | Phase 2 strong results, or Phase 3 small sample |
| 5-6 | Phase 2 moderate results |
| 4 | Phase 1 promising signals, or Phase 2 mixed |
| 2-3 | Phase 1 only, or case series |
| 1 | Case reports, retrospective data only |

### Rating anchors — `survival_benefit`

| Score | Benefit |
|---|---|
| 10 | >12 months OS improvement over SoC, or curative potential |
| 8-9 | 6-12 months OS improvement, or >50% reduction in death risk |
| 6-7 | 3-6 months OS improvement, or significant PFS gain |
| 4-5 | 1-3 months OS improvement, or moderate PFS improvement |
| 2-3 | Marginal survival benefit, mainly response rate improvement |
| 1 | No demonstrated survival benefit |

### Rating anchors — `accessibility`

| Score | Access |
|---|---|
| 10 | FDA + EMA approved, widely available |
| 8-9 | FDA approved, available at most oncology centers |
| 7 | Available through Phase 3 trial at multiple sites |
| 5-6 | Phase 2 trial, limited sites |
| 3-4 | Phase 1 trial, very limited access |
| 1-2 | Research only, not accessible to patients |

### Rating anchors — `safety_profile`

| Score | Toxicity |
|---|---|
| 10 | Minimal side effects, well-tolerated |
| 7-8 | Manageable with standard supportive care |
| 5-6 | Significant but manageable, may require dose reductions |
| 3-4 | Serious toxicity, requires close monitoring |
| 1-2 | Life-threatening potential, narrow therapeutic window |

### Rating anchors — `biomarker_match`

| Score | Match |
|---|---|
| 10 | No biomarker required (universal applicability) |
| 7-8 | Requires common biomarker (>30% of cases) |
| 5 | Biomarker status unknown or undetermined |
| 3-4 | Requires rare biomarker (<10% of cases) |
| 1-2 | Ultra-rare biomarker or specific combination required |

---

## `clinical_trials`

Array of active/recent clinical trial objects. Minimum 3, target 5-7.

```json
{
  "trial_id":    "NCT04280705",
  "name":        "KEYNOTE-689: Pembrolizumab + SoC vs SoC in Resectable LA-HNSCC",
  "phase":       "Phase 3",
  "status":      "COMPLETED",
  "sponsor":     "Merck Sharp & Dohme",
  "enrollment":  714,
  "primary_endpoint": "Event-free survival (EFS)",
  "key_eligibility": [
    "Resectable locally advanced HNSCC",
    "ECOG PS 0-1",
    "PD-L1 CPS >= 1"
  ],
  "results_summary": "EFS HR 0.66 in CPS>=10 population (p=0.00434). FDA approved June 2025.",
  "countries":   ["US", "EU", "Japan"],
  "site_count":  200,
  "url":         "https://clinicaltrials.gov/study/NCT04280705"
}
```

---

## `combination_strategies`

Array of synergistic treatment combinations. Minimum 4 entries. Include:
- SoC + immunotherapy combination
- Targeted therapy + immunotherapy
- Novel combination from active trials
- Evidence-based supportive add-on

```json
{
  "name":                "Pembrolizumab + Cisplatin + RT (perioperative)",
  "base_therapy":        "Cisplatin + Intensity-Modulated Radiation Therapy",
  "combination_partner": "Pembrolizumab (anti-PD-1)",
  "intent":              "curative",
  "evidence_level":      "Phase 3 RCT (KEYNOTE-689, N=714)",
  "rationale":           "Neoadjuvant pembrolizumab primes anti-tumor T-cell response against tumor neoantigens while tumor is in situ; adjuvant pembrolizumab sustains immune surveillance. PD-1 blockade + cisplatin-mediated immunogenic cell death creates synergistic anti-tumor immunity.",
  "key_data":            "36-month EFS 60% vs 46% in CPS>=10 (HR 0.66). 3-year OS 68% vs 59%.",
  "contraindications":   ["Active autoimmune disease", "ECOG PS >= 3"],
  "source_url":          "https://www.nejm.org/doi/full/10.1056/NEJMoa2415434"
}
```

---

## `supportive_care`

Array of evidence-based supportive approaches. Minimum 4 entries.

```json
{
  "approach":             "Prophylactic swallowing exercises (pre- and during-RT)",
  "evidence":             "DIGEST RCT (Carroll et al., 2008, IJROBP); Hutcheson et al. 2013",
  "benefit":              "Reduces long-term severe dysphagia (OR 0.41, 95% CI 0.18-0.94). Reduces PEG tube dependence at 12 months from 35% to 18%.",
  "recommendation_level": "Level 1 — recommended for all H&N patients receiving RT",
  "qol_instrument":       "MDADI (MD Anderson Dysphagia Inventory)",
  "implementation":       "Structured exercise program starting 2 weeks pre-RT, continuing throughout RT and 6 months post-RT"
}
```

---

## `sources`

Array of all sources cited in the report. Minimum 10, target 15-20.

```json
{
  "title":    "Pembrolizumab plus Chemotherapy in Head and Neck Squamous-Cell Carcinoma",
  "authors":  "Burtness B, et al.",
  "journal":  "New England Journal of Medicine",
  "year":     2019,
  "pmid":     "31679945",
  "url":      "https://www.nejm.org/doi/full/10.1056/NEJMoa1915914",
  "type":     "phase3_rct",
  "accessed": "2026-03-23"
}
```

### Source `type` values

| Value | Description |
|---|---|
| `guideline` | NCCN, ESMO, ASCO guidelines |
| `phase3_rct` | Phase 3 randomized controlled trial |
| `phase2_trial` | Phase 2 trial |
| `phase1_trial` | Phase 1 / dose-escalation trial |
| `meta_analysis` | Systematic review or meta-analysis |
| `network_meta_analysis` | Network meta-analysis (NMA) |
| `regulatory` | FDA/EMA approval announcement |
| `clinical_trial_registry` | ClinicalTrials.gov entry |
| `conference_abstract` | ASCO/ESMO/AACR abstract (preliminary) |
| `review` | Narrative review article |
| `case_series` | Case series or retrospective analysis |

---

## Schema Validation

Run the built-in validator at any time:

```bash
# Validate a single report
python cancer_research_scorer.py research_db/carcinomas/breast/reports/BRE-001_report.json --validate-only

# Score and validate
python evaluate.py research_db/carcinomas/breast/reports/BRE-001_report.json --verbose

# Validate all reports for a cancer type
for f in research_db/carcinomas/breast/reports/*_report.json; do
  echo -n "$f: "
  python evaluate.py "$f" --score-only
done
```

---

## Benchmark Case Schema

```json
{
  "benchmark_metadata": {
    "generated_date": "2026-03-23",
    "site": "breast",
    "demographic": { "age": 50, "sex": "female" },
    "case_count": 10,
    "purpose": "Fixed test set for autoresearch loop — do NOT modify between iterations"
  },
  "cases": [
    {
      "id": "BRE-001",
      "cancer_type": "Triple-negative breast cancer (TNBC), PD-L1 CPS >= 10",
      "stage": "Stage II (T2N1M0)",
      "molecular_markers": ["ER-", "PR-", "HER2-", "PD-L1 CPS 15", "BRCA1 germline+"],
      "patient_context": {
        "age": 50,
        "sex": "female",
        "risk_factors": ["BRCA1 germline mutation", "Ashkenazi Jewish ancestry"],
        "comorbidities": [],
        "performance_status": "ECOG 0"
      },
      "why_this_case_matters": "Tests pembrolizumab + chemo (KEYNOTE-522), olaparib adjuvant (OlympiA), and capecitabine for residual disease (CREATE-X). BRCA1+ enables PARP inhibitor use."
    }
  ]
}
```

### Case ID naming convention

```
{CATEGORY_PREFIX}-{3-digit-number}

Examples:
  HN-001    Head & Neck (original 10 cases)
  HN2-001   Head & Neck batch 2 (20 cases)
  HN3-001   Head & Neck batch 3 (60 complex/rare cases)
  LUN-001   Lung
  BRE-001   Breast
  CRC-001   Colorectal
  PAN-001   Pancreatic
  GAS-001   Gastric
  HCC-001   Hepatocellular
  THY-001   Thyroid
  CER-001   Cervical
  OVA-001   Ovarian
  BLA-001   Bladder
  KID-001   Kidney/Renal
  PRO-001   Prostate
  MEL-001   Melanoma/Skin
  OST-001   Osteosarcoma
  EWI-001   Ewing Sarcoma
  RMS-001   Rhabdomyosarcoma
  LMS-001   Leiomyosarcoma
  LIP-001   Liposarcoma
  CHO-001   Chondrosarcoma
  GIS-001   GIST
  AML-001   AML
  ALL-001   ALL
  CML-001   CML
  CLL-001   CLL
  HCL-001   Hairy Cell Leukemia
  HOD-001   Hodgkin Lymphoma
  DLB-001   DLBCL
  FOL-001   Follicular Lymphoma
  MCL-001   Mantle Cell Lymphoma
  TCL-001   T-Cell Lymphoma
  MZL-001   Marginal Zone Lymphoma
  MM-001    Multiple Myeloma
  WAL-001   Waldenström
  GBM-001   Glioblastoma
  AST-001   IDH-mutant Astrocytoma
  MEN-001   Meningioma
  MED-001   Medulloblastoma
  EPE-001   Ependymoma
  SPC-001   Spinal Cord Tumor
```
