# Adding a New Cancer Type — Step-by-Step Guide

This guide walks through adding a completely new cancer type to the database,
from zero to scored research reports ready for the autoresearch loop.

Total time: ~15 minutes setup + research runtime (8-12 min per case).

---

## Prerequisites

- The autoresearch project is set up and `python auto_loop.py --dry-run` runs clean
- You know which cancer type and category you are adding
- You have identified its folder in `research_db/` (see `DATABASE_GUIDE.md`)

---

## Step 1 — Choose & Confirm the Cancer Type

Find the folder in `research_db/{category}/{subtype}/`. If the subtype doesn't
exist yet, create it:

```bash
mkdir -p research_db/sarcomas/synovial_sarcoma/reports
```

Confirm what already exists in `research_db/INDEX.json`:
```bash
python -c "
import json
idx = json.load(open('research_db/INDEX.json'))
# Check if your subtype is listed
print(json.dumps(idx['categories']['sarcomas'], indent=2))
"
```

---

## Step 2 — Generate Benchmark Cases

Benchmark cases are the **fixed test set** for this cancer type. Generate once,
never change between loop iterations (changing the test set invalidates all
previous scores).

### Option A — Use the built-in generator

```bash
# Breast cancer, 50 y.o. female, 10 cases
python generate_cases.py \
  --site "breast" \
  --age 50 --sex female --count 10 \
  --output research_db/carcinomas/breast/benchmark_cases.json

# Glioblastoma, 55 y.o. male, 8 cases
python generate_cases.py \
  --site "glioblastoma" \
  --age 55 --sex male --count 8 \
  --output research_db/cns_tumors/glioblastoma/benchmark_cases.json
```

Currently pre-built templates exist for: `lung`, `breast`, `colorectal`,
`pancreatic`, `head and neck`. All other sites get realistic placeholder cases
that should be manually reviewed and improved.

### Option B — Write cases manually (recommended for rare cancers)

Copy the template below into `research_db/{category}/{subtype}/benchmark_cases.json`
and fill in accurate clinical data. See `SCHEMA_REFERENCE.md` for field definitions.

```json
{
  "benchmark_metadata": {
    "generated_date": "2026-03-23",
    "site": "multiple myeloma",
    "demographic": {"age": 60, "sex": "male"},
    "case_count": 10,
    "purpose": "Fixed test set for autoresearch loop — do NOT modify between iterations"
  },
  "cases": [
    {
      "id": "MM-001",
      "cancer_type": "Multiple myeloma — newly diagnosed transplant-eligible",
      "stage": "ISS Stage II (serum albumin 3.8, beta-2-microglobulin 4.2 mg/L)",
      "molecular_markers": ["t(4;14) — high risk", "del(17p) absent", "FISH normal ploidy"],
      "patient_context": {
        "age": 60,
        "sex": "male",
        "risk_factors": ["family history of plasma cell dyscrasia"],
        "comorbidities": ["hypertension"],
        "performance_status": "ECOG 0"
      },
      "why_this_case_matters": "Tests VRd induction, ASCT, lenalidomide maintenance, and MRD-guided therapy. Standard newly-diagnosed pathway with high-risk cytogenetics (t(4;14))."
    }
  ]
}
```

### Minimum case requirements per cancer type

| Category | Minimum cases | Recommended | Rationale |
|---|---|---|---|
| Carcinomas | 8 | 10-15 | High incidence, many subtypes to cover |
| Sarcomas | 6 | 8-10 | Rare; subtypes are biologically distinct |
| Leukemias | 8 | 10 | Multiple molecular subtypes drive therapy |
| Lymphomas | 8 | 10 | Histological + molecular complexity |
| Myelomas | 6 | 8 | Treatment lines (NDMM, R/R) need coverage |
| CNS Tumors | 6 | 8 | WHO grade + molecular classification critical |

### What makes a good benchmark case?

Each case should test a **distinct clinical question**. Across 10 cases, cover:
- [ ] Early stage (potentially curative) and late stage (palliative)
- [ ] Common molecular subtype AND rare/actionable subtype
- [ ] ECOG 0-1 patient AND ECOG 2+ patient
- [ ] Standard therapy candidate AND trial-eligible patient
- [ ] At least one biomarker-driven case (specific targeted therapy exists)
- [ ] At least one case with prior treatment failure (salvage setting)

---

## Step 3 — Run the First Research Pass

```bash
python run_experiment.py \
  --cases research_db/carcinomas/breast/benchmark_cases.json \
  --strategy strategy.md \
  --reports-dir research_db/carcinomas/breast/reports

# With live data enrichment (adds PubMed abstracts + CT.gov trial data):
python run_experiment.py \
  --cases research_db/carcinomas/breast/benchmark_cases.json \
  --reports-dir research_db/carcinomas/breast/reports \
  --enrich-pubmed
```

This generates prompts for each case. The actual research is executed by Claude
when you open the prompt files and run the cancer research skill.

**Expected output per case:**
- `research_db/carcinomas/breast/reports/{CASE_ID}_prompt.md` — research instructions
- `research_db/carcinomas/breast/reports/{CASE_ID}_report.json` — filled after research

---

## Step 4 — Evaluate Quality

```bash
# Score all reports for this cancer type
python run_experiment.py \
  --cases research_db/carcinomas/breast/benchmark_cases.json \
  --reports-dir research_db/carcinomas/breast/reports

# Score a single report with detail
python evaluate.py research_db/carcinomas/breast/reports/BRE-001_report.json --verbose

# Check complexity classification for all cases
python run_experiment.py \
  --cases research_db/carcinomas/breast/benchmark_cases.json \
  --show-complexity --dry-run
```

**Target score for acceptance: ≥80/100 mean across all cases.**

If mean score is below 80, the reports need revision or the strategy needs tuning
before moving to the autoresearch loop.

---

## Step 5 — Run the Autoresearch Loop

Once a baseline score exists, start the loop to improve strategy.md for this
cancer type:

```bash
# Basic loop — 20 iterations, target 92/100
python auto_loop.py \
  --cases research_db/carcinomas/breast/benchmark_cases.json \
  --target-score 92 \
  --max-iters 20 \
  --parallel 2 \
  --variants 3

# With local LLM semantic mutations (requires ollama):
python auto_loop.py \
  --cases research_db/carcinomas/breast/benchmark_cases.json \
  --target-score 92 \
  --local-llm \
  --auto-focus
```

The loop writes results to `results.tsv` in the working directory. To keep
per-cancer-type results isolated, run from the subtype directory or redirect:

```bash
# Isolated results per cancer type
cd research_db/carcinomas/breast
python ../../../auto_loop.py \
  --cases benchmark_cases.json \
  --reports-dir reports
```

---

## Step 6 — Update the Master Index

After generating reports, update `research_db/INDEX.json`:

```bash
python -c "
import json, os, glob

idx_path = 'research_db/INDEX.json'
idx = json.load(open(idx_path))

# Example: update breast carcinoma entry
reports = glob.glob('research_db/carcinomas/breast/reports/*_report.json')
idx['categories']['carcinomas']['subtypes']['breast'].update({
    'status': 'active',
    'cases': 10,
    'reports': len(reports),
    'benchmark_file': 'benchmark_cases.json',
})
idx['_meta']['last_updated'] = '2026-03-23'

with open(idx_path, 'w') as f:
    json.dump(idx, f, indent=2)
print('Index updated.')
"
```

---

## Category-Specific Clinical Notes

These notes highlight what the research strategy MUST capture for each category.
Include these as `why_this_case_matters` context in benchmark cases.

### Carcinomas
- **Lung (NSCLC)**: Every case needs molecular profiling context (EGFR, ALK, ROS1,
  KRAS G12C, MET, RET, NTRK, BRAF). Targeted therapy availability changes treatment
  completely. PD-L1 TPS % determines immunotherapy first-line eligibility.
- **Breast**: Hormone receptor status (ER/PR) and HER2 define 4 distinct treatment
  paradigms. Include CDK4/6 inhibitors for HR+ and T-DM1/T-DXd for HER2+.
  BRCA1/2 germline status triggers PARP inhibitor eligibility.
- **Colorectal**: MSI-H/dMMR enables immunotherapy (pembrolizumab first-line).
  RAS/BRAF/HER2 status determines chemotherapy backbone and targeted eligibility.
  Left vs right sidedness affects anti-EGFR use.
- **Pancreatic**: BRCA1/2 mutations enable olaparib maintenance. KRAS G12C enables
  sotorasib/adagrasib trials. Germline testing is standard.
- **CNS-adjacent (GBM as carcinoma-adjacent)**: Blood-brain barrier limits drug access.
  MGMT methylation determines temozolomide benefit. EGFRvIII enables antibody-drug
  conjugates in trials.

### Sarcomas
- Sarcomas are **histotype-driven**: treatment for leiomyosarcoma ≠ treatment for
  osteosarcoma. Never aggregate sarcoma cases across histotypes.
- Most sarcomas lack Phase 3 RCT data — Phase 2 single-arm studies are often the
  highest level of evidence. Calibrate ratings accordingly.
- **GIST**: KIT exon 9 vs 11 mutations determine imatinib dosing. PDGFRA D842V
  is imatinib-resistant — requires avapritinib specifically.
- **Ewing**: EWSR1-FLI1 fusion is diagnostic. Pediatric vs adult biology differs.
  VDC/IE chemotherapy is the backbone.
- **Bone sarcomas**: always note limb-salvage vs amputation surgical considerations.
  Rotationplasty and endoprostheses are functional endpoints, not just tumor control.

### Leukemias
- **AML**: Treatment decisions split by: age (fit vs unfit for intensive chemo),
  ELN risk classification (favorable/intermediate/adverse), and specific mutations
  (FLT3 → midostaurin/quizartinib, IDH1 → ivosidenib, IDH2 → enasidenib, APL
  → ATRA+ATO). MRD status post-induction drives consolidation decisions.
- **ALL**: BCR-ABL1 status is first split — Ph+ ALL has completely different
  treatment from Ph- ALL. Blinatumomab, inotuzumab, CAR-T (tisagenlecleucel) are
  standard for R/R B-ALL.
- **CML**: First-line TKI choice (imatinib vs dasatinib vs nilotinib vs asciminib)
  depends on phase, BCR-ABL1 mutation status, and cardiovascular risk. Treatment-
  free remission (TFR) is a realistic endpoint in deep molecular responders.
- Leukemia cases MUST include response criteria: CR, CRi, MRD negativity, CCyR,
  MMR, MR4.5. These are the treatment endpoints, not OS alone.

### Lymphomas
- **Hodgkin**: Highly curable (>80% first-line cure rate). PET-adapted therapy
  (interim PET) drives escalation/de-escalation decisions. Brentuximab vedotin +
  AVD is now standard for stage III-IV.
- **DLBCL**: GCB vs ABC (non-GCB) biology determines prognosis. Double-hit
  (MYC+BCL2 or MYC+BCL6) requires DA-EPOCH-R escalation. Polatuzumab vedotin,
  loncastuximab tesirine, tafasitamab in R/R. CAR-T is standard for chemo-refractory.
- **Follicular**: Watch-and-wait is standard for low-burden FL. FLIPI score drives
  treatment decisions. POD24 (progression within 24 months) is the key adverse
  prognostic marker — these patients need escalated therapy.
- All lymphoma cases need Ann Arbor/Lugano staging, IPI/FLIPI scoring, and
  bulk disease documentation.

### Myelomas
- **Multiple Myeloma**: The backbone has shifted to quadruplet induction
  (daratumumab + VRd or KRd). ASCT eligibility (age <70, ECOG 0-2, organ function)
  splits treatment algorithms. MRD negativity is the treatment goal.
  High-risk cytogenetics: t(4;14), t(14;16), del(17p), gain(1q), del(1p).
  Bispecific antibodies (teclistamab, elranatamab) and CAR-T (cilta-cel, ide-cel)
  are standard for penta-refractory disease.
- Cases must cover: NDMM transplant-eligible, NDMM transplant-ineligible, first
  relapse, late relapse, and high-risk cytogenetics.

### CNS Tumors
- **All CNS tumors**: Blood-brain barrier penetration is a primary consideration
  for all systemic therapies. Document which drugs achieve CNS levels.
- **GBM**: O6-methylguanine-DNA methyltransferase (MGMT) promoter methylation
  determines temozolomide efficacy. IDH-wildtype = GBM per WHO 2021. EGFRvIII
  amplification is a druggable target in trials. Tumor treating fields (TTFields/
  Optune) improves OS in newly-diagnosed GBM.
- **IDH-mutant astrocytoma**: Vorasidenib (IDH1/2 inhibitor) was FDA-approved in
  2024 for grade 2 IDH-mutant glioma — major practice change. Include it.
- **Medulloblastoma**: WNT-activated subgroup has excellent prognosis and can be
  de-escalated. SHH-activated responds to vismodegib/sonidegib. Group 3/4 has
  worst prognosis.
- All CNS cases need: WHO grade (1-4), IDH status, MGMT status, 1p/19q co-deletion
  (oligodendroglioma), H3 K27M (diffuse midline glioma), TERT mutation status.

---

## Common Mistakes to Avoid

| Mistake | Consequence | Fix |
|---|---|---|
| Adding cases mid-loop | Invalidates score comparisons | Always freeze benchmark_cases.json before first loop run |
| Mixing cancer types in one benchmark | Strategy can't optimize for one type | One benchmark_cases.json per specific cancer subtype |
| Not including ECOG 2+ cases | Strategy skews to fit patients only | Always include at least 1-2 ECOG 2+ cases |
| Generic molecular markers | Agent can't find targeted therapy evidence | Use specific mutation names: EGFR L858R, not just "EGFR mutation" |
| No palliative-intent cases | No test of palliative treatment ranking | Include at least 2 Stage IV M1 cases per benchmark set |
| All same histology | Misses subtype-specific biology | Cover at least 3 histological subtypes per benchmark set |
