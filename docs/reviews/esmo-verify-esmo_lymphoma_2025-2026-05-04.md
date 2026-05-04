# ESMO Verification Report — SRC-ESMO-LYMPHOMA-2025

**Generated:** 2026-05-04  
**Branch:** feat/esmo-pdf-extract-2026-05-03  
**Mode:** PROTOTYPE — output for clinical review only, NOT auto-applied to KB  
**Legal status:** SOURCE_INGESTION_SPEC §6 red flag #1 pending resolution

## 1. Source metadata

| Field | Value |
|---|---|
| **Source ID** | `SRC-ESMO-LYMPHOMA-2025` |
| **Title** | Lymphomas: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up |
| **DOI** | [10.1016/j.annonc.2025.07.014](https://doi.org/10.1016/j.annonc.2025.07.014) |
| **Version** | 2025 |
| **Hosting mode** | referenced |
| **License** | CC-BY-NC-ND 4.0 (Annals of Oncology / ESMO) |
| **Legal review** | reviewed |
| **PDF URL** | (not resolved) |
| **PDF pages** | 0 |
| **Therapy pages found** | 0 () |

## ⚠️ Extraction error

```
No open-access PDF found via Unpaywall and no direct_pdf_url provided.
```

## 2. Extracted therapy text (ESMO PDF source)

> **Attribution required on any use:** Lymphomas: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. Annals of Oncology 2025. DOI: 10.1016/j.annonc.2025.07.014 (DOI: 10.1016/j.annonc.2025.07.014)

> **Do not copy-paste into KB** — clinician paraphrase required per SOURCE_INGESTION_SPEC §1.2.

*(No therapy-relevant text extracted.)*

## 3. Current KB indications for this source's diseases

Found **49** indication(s) linked to ['DIS-DLBCL-NOS', 'DIS-PMBCL', 'DIS-HGBL-DH', 'DIS-FL', 'DIS-MCL', 'DIS-HCV-MZL', 'DIS-HODGKIN', 'DIS-PTCL-NOS', 'DIS-AITL', 'DIS-ALCL-ALK-POS', 'DIS-ALCL-ALK-NEG', 'DIS-BURKITT'].


### IND-DLBCL-1L-POLA-R-CHP
- **Regimen:** REG-POLA-R-CHP  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024

**Current KB rationale:**

  Aggressive-track default for newly-diagnosed DLBCL NOS with IPI ≥2 (RF-DLBCL-HIGH-IPI
  fired). Replaces vincristine in R-CHOP with polatuzumab vedotin (anti-CD79b ADC with MMAE
  payload). POLARIX trial (NEJM 2022) showed ~6.5% absolute PFS improvement at 2 years vs
  R-CHOP. Toxicity profile comparable; peripheral neuropathy slightly higher with
  polatuzumab but vincristine removed. Major access constraint in Ukraine: polatuzumab not
  НСЗУ-reimbursed. Funding pathway (clinical trial / charitable / out-of-pocket) MUST be
  verified before plan finalized.



### IND-DLBCL-1L-RCHOP
- **Regimen:** REG-R-CHOP  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024

**Current KB rationale:**

  Long-standing 1L standard for newly-diagnosed DLBCL NOS, used for the past 20+ years
  across NCCN, ESMO, EHA. ~60% overall cure rate; outcomes highly dependent on IPI. Replaced
  PreCHOP regimens after the rituximab era (RCT data from late 1990s/early 2000s). Default
  for low-IPI (0-1) patients; for IPI ≥2, modern evidence (POLARIX 2022) favors Pola-R-CHP
  if accessible (see IND-DLBCL-1L-POLA-R-CHP).



### IND-DLBCL-1L-RCHOP-ISRT-EARLY
- **Regimen:** REG-R-CHOP  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024

**Current KB rationale:**

  De-escalated regimen for newly-diagnosed early-stage (I-II) non-bulky DLBCL: 4 cycles
  R-CHOP followed by 30 Gy involved-site radiotherapy (ISRT), or 6 cycles R-CHOP without RT
  in PET-negative responders (LYSA-LNH 02-03, SWOG S1001, FLYER trial conceptually). 4-cycle
  schedule with response-adapted RT yields equivalent 5-year PFS/OS to historical 6-cycle
  approaches with substantially less anthracycline exposure + reduced infusion days. ISRT
  field encompasses pre-chemo gross disease; modern 30 Gy dose carries low late-effect
  burden.



### IND-DLBCL-2L-LISOCEL
- **Regimen:** REGIMEN-LISOCEL-DLBCL-2L  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024

**Current KB rationale:**

  Lisocabtagene maraleucel (liso-cel; Breyanzi) is a CD19-targeted CAR-T with defined 1:1
  CD4:CD8 cell composition and 4-1BB costimulation, approved for primary-refractory LBCL or
  relapse <12 months from completion of first-line therapy in transplant-intended 2L setting
  (TRANSFORM phase 3 RCT). TRANSFORM (Kamdar et al., Lancet 2022; long-term update Abramson
  et al., Blood 2023): liso-cel superior to standard-of-care salvage chemo + autoSCT —
  median EFS 10.1 vs 2.3 mo (HR ~0.36), CR ~74% vs ~43%, ORR ~86%, PFS substantially
  extended; OS trend favourable but crossover-confounded. Boxed warnings: CRS, ICANS,
  secondary T-cell malignancy (FDA 2024 class label). Eligibility narrower than 3L liso-cel
  (TRANSCEND): primary-refractory or early-relapse + transplant-intent. CRS profile
  favourable (G≥3 ~



### IND-DLBCL-2L-POLA-R-BENDAMUSTINE
- **Regimen:** REG-POLA-R-BENDAMUSTINE  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024

**Current KB rationale:**

  Polatuzumab + rituximab + bendamustine (Pola-BR) for r/r DLBCL after 1L R-CHOP failure in
  patients NOT eligible for autoSCT (age >70, comorbidity, ECOG ≥2, or autoSCT-failed). Per
  GO29365 trial, Pola-BR more than doubled CR rate vs BR alone (40% vs 18%) with substantial
  PFS + OS gains. Position: standard-track 2L for transplant-ineligible cohort; transplant-
  eligible patients still go to salvage chemo (R-DHAP / R-ICE) → autoSCT first per NCCN.
  Major UA access barrier: polatuzumab not НСЗУ-reimbursed.



### IND-DLBCL-3L-AXICEL-CART
- **Regimen:** REG-CAR-T-AXICEL  |  **Line:** 3  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024, SRC-ZUMA-1-NEELAPU-2017, SRC-ZUMA-7-LOCKE-2022

**Current KB rationale:**

  Axicabtagene ciloleucel (axi-cel) for relapsed/refractory DLBCL after ≥2 prior systemic
  lines (3L+ per ZUMA-1 registration). Anti-CD19 CD28-costimulated CAR-T with single
  infusion after fludarabine-cyclo lymphodepletion. ~40% achieve durable remission at 5
  years — only curative option in this otherwise grim setting (historical 2L+ refractory mOS
  ~6 months pre-CAR-T). For primary-refractory or early-relapse (<12 mo from 1L), ZUMA-7
  supports moving CAR-T to 2L (separate Indication, future). Absolute access barrier in
  Ukraine: not registered, no domestic manufacturing — international referral required.



### IND-DLBCL-3L-EPCORITAMAB
- **Regimen:** REGIMEN-EPCORITAMAB-MONO-DLBCL-3L  |  **Line:** 3  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024

**Current KB rationale:**

  Epcoritamab (Epkinly / Tepkinly) is a subcutaneous CD20×CD3 bispecific T-cell engager for
  relapsed/refractory DLBCL after ≥2 prior systemic lines, including patients ineligible for
  or relapsed after CD19 CAR-T. EPCORE NHL-1 (Thieblemont et al., J Clin Oncol 2023; n=157,
  ~39% prior CAR-T): ORR ~63%, CR ~39%, median DOR ~12 months, median PFS ~4.4 mo. Step-up
  dosing (0.16 → 0.8 → 48 mg) + cycle-1 corticosteroid prophylaxis reduce CRS to
  predominantly Grade 1-2 (any-grade ~50%, G≥3 ~3%); ICANS ~6% any-grade. SC route +
  ambulatory schedule favourable vs IV bispecifics for outpatient-heavy practices.
  Continuous indefinite dosing is the principal sequencing trade-off vs fixed-duration
  glofitamab. Ukraine context: not registered, no NSZU pathway; international clinical trial
  / compassionate use o



### IND-DLBCL-3L-GLOFITAMAB
- **Regimen:** REGIMEN-GLOFITAMAB-MONO-DLBCL-3L  |  **Line:** 3  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024

**Current KB rationale:**

  Glofitamab (Columvi) is an IV CD20×CD3 bispecific T-cell engager with 2:1 CD20-bivalent /
  CD3-monovalent format and fixed 12-cycle duration for relapsed/refractory DLBCL after ≥2
  prior systemic lines, including patients ineligible for or relapsed after CD19 CAR-T.
  NP30179 pivotal phase 2 (Dickinson et al., NEJM 2022; n=155, ~33% prior CAR-T): ORR ~52%,
  CR ~39%, median CR DOR not reached, 12-month PFS among CR responders ~71%, OS at 12 months
  ~50%. Obinutuzumab 1000 mg IV pretreatment day -7 + cycle-1 step-up dosing (2.5 → 10 → 30
  mg) + corticosteroid premedication suppress CRS to predominantly Grade 1-2 (any-grade
  ~63%, G≥3 ~4%); ICANS ~8% any-grade. Distinguishing feature vs epcoritamab is fixed
  12-cycle duration (~8.5 months from cycle 1 day 1) vs continuous indefinite dosing —
  improves



### IND-DLBCL-3L-LISO-CEL-CART
- **Regimen:** None  |  **Line:** 3  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024, SRC-ZUMA-1-NEELAPU-2017, SRC-ZUMA-7-LOCKE-2022

**Current KB rationale:**

  Lisocabtagene maraleucel (liso-cel; Breyanzi) is a CD19-targeted CAR-T cell therapy with
  the best safety profile of the three FDA-approved CAR-T products for r/r DLBCL (axi-cel,
  tisa-cel, liso-cel). TRANSCEND NHL-001 (Abramson 2020 Lancet): ORR 73%, CR 53%, mPFS 6.8
  mo overall, 22.8 mo in CR responders. CRS Grade ≥3 ~2% (vs ~13% axi-cel) and ICANS Grade
  ≥3 ~10% (vs ~28% axi-cel) make liso-cel preferred in older / frail / cardiac comorbid
  patients. TRANSFORM (Kamdar 2022 Lancet) and PILOT (Sehgal 2022 Lancet Oncol) extended use
  to 2L for HSCT-ineligible / primary refractory or early relapse. Step-up dosing not
  required (single infusion); fludarabine + cyclophosphamide lymphodepletion 5-3 days pre-
  infusion. Hospital observation 7-14 days. Universal hypogammaglobulinemia → IVIG. PJP +
  HSV/VZV



### IND-DLBCL-3L-LONCASTUXIMAB
- **Regimen:** REG-LONCASTUXIMAB-TESIRINE  |  **Line:** 3  |  **Track:** standard
- **Evidence level:** moderate  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024, SRC-LOTIS-2-CAIMI-2021

**Current KB rationale:**

  Loncastuximab tesirine (Zynlonta) is a CD19-directed antibody-drug conjugate (ADC) with
  PBD warhead approved for r/r DLBCL after ≥2 prior systemic therapies. LOTIS-2 (Caimi 2021
  Lancet Oncol): single-arm phase 2; ORR 48%, CR 24%, mPFS 4.9 mo, mOS 9.5 mo, in heavily
  pretreated patients (median 3 prior lines, ~30% prior CAR-T). Ideal for patients NOT
  candidates for CAR-T (frailty, manufacturing window prohibitive, prior CD19 CAR-T failure
  with CD19-positive relapse, comorbidity precluding lymphodepletion). Off-the-shelf +
  outpatient feasible — major operational advantage over CAR-T. Bispecifics (epcoritamab,
  glofitamab) are competing 3L+ options with comparable ORR (~60%) but require step-up
  dosing + inpatient observation. Loncastuximab toxicities: peripheral edema (~50%),
  thrombocytopenia (



### IND-DLBCL-RENAL-FAILURE-MOD-RCHOP
- **Regimen:** REG-R-CHOP  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** low  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024

**Current KB rationale:**

  In DLBCL patients with severe renal impairment (CrCl <30 mL/min), R-CHOP modifications:
  (1) CYCLOPHOSPHAMIDE: reduce dose by 25% for CrCl 10-30 mL/min; consider 50% reduction or
  omission for CrCl <10 / dialysis; cyclophosphamide active metabolite (acrolein)
  accumulates with haemorrhagic cystitis risk — IV mesna + aggressive hydration mandatory.
  (2) DOXORUBICIN: no formal renal adjustment but consider 25% reduction for combined
  hepatic + renal dysfunction; cardiotoxicity risk amplified in fluid-overloaded CKD. (3)
  VINCRISTINE: no renal adjustment needed; cap dose at 2 mg total (standard practice). (4)
  PREDNISONE: no renal adjustment. (5) RITUXIMAB: no renal adjustment; HBV/HCV screen
  mandatory. CNS prophylaxis (HD-MTX intercalated) is challenging in CKD — methotrexate is
  renally cleared wit



### IND-EMERG-INFUSION-REACTION-IRR
- **Regimen:** None  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-CTCAE-V5

**Current KB rationale:**

  Infusion-related reactions (IRRs) are common with monoclonal antibodies, particularly
  first doses of CD20-targeted (rituximab, obinutuzumab — IRR rate ~50-77%), CD38
  (daratumumab — ~46%), EGFR (cetuximab — ~3% severe), HER2 (trastuzumab — ~30% mild),
  bispecifics (mosunetuzumab, glofitamab — CRS overlap). CTCAE v5 grading: G1 transient
  flushing/rash/fever; G2 requires intervention/interruption but rapid response; G3
  prolonged, recurrent symptoms requiring hospitalization; G4 life-threatening (anaphylaxis,
  ARDS); G5 death. ALGORITHM: G1 — slow infusion 50%; G2 — STOP infusion + IV
  diphenhydramine 25-50 mg + IV hydrocortisone 100 mg (or methylprednisolone 40-80 mg) +
  acetaminophen 650-1000 mg PO/IV + supportive (oxygen, fluids); resume at 50% rate after
  symptoms resolve; G3 — STOP + above + b



### IND-PMBCL-1L-DA-EPOCH-R
- **Regimen:** REG-DA-EPOCH-R  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024

**Current KB rationale:**

  DA-EPOCH-R — preferred 1L per NCCN (Cat 1) на основі NCI single-arm study (Dunleavy 2013,
  ~95% PFS). Уникає необхідності consolidation RT у більшості пацієнтів (PET-negative після
  induction). Краще ніж R-CHOP+RT для bulky mediastinal disease, особливо в young жінок,
  яким хочемо уникнути mediastinal RT (carcinogenesis ризик молочної залози).



### IND-PMBCL-1L-RCHOP-RT
- **Regimen:** REG-R-CHOP  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** moderate  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024

**Current KB rationale:**

  R-CHOP × 6 + consolidation involved-site mediastinal RT — historic standard. Менш бажаний
  за DA-EPOCH-R, але acceptable коли DA-EPOCH-R недоступний (центр без infusional досвіду).
  RT додає late toxicity (breast cancer, cardiac, secondary malignancies).



### IND-PMBCL-2L-RICE-AUTOSCT
- **Regimen:** REG-R-ICE-PMBCL  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** moderate  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-DLBCL-2024

**Current KB rationale:**

  R-ICE × 2-3 cycles → response assessment (PET) → BEAM-conditioned autoSCT for
  chemosensitive r/r PMBCL is standard 2L per NCCN and ESMO. ~50-60% achieve durable
  remission post-autoSCT. For chemorefractory disease: CAR-T (axi-cel/liso-cel) or
  pembrolizumab (KEYNOTE-170, ORR ~45% in r/r PMBCL). PMBCL biology overlaps with classic
  Hodgkin (PD-L1 amplification 9p24.1) — checkpoint inhibitor response notable.



*(… 34 more indications not shown)*

## 4. Clinician verification checklist

For each item below, the reviewing clinician should check the extracted text against the current KB indication rationale and mark ✅ / ❌ / ➕.

- [ ] First-line regimen(s) in PDF match `recommended_regimen` in KB indication(s)

- [ ] Expected outcomes (ORR, CR, PFS, OS) in PDF match KB `expected_outcomes` block

- [ ] Hard contraindications in PDF match KB `hard_contraindications` list

- [ ] Any regimens in PDF **not yet** in KB (gap → new indication needed) — mark ➕

- [ ] Any regimens in KB that PDF **does not support** (possible hallucination) — mark ❌

- [ ] ESMO evidence level / recommendation grade captured correctly in KB

- [ ] `rationale` field accurately paraphrases PDF (not a verbatim copy)

- [ ] All `sources` in the indication cite this source ID where appropriate

- [ ] `reviewer_signoffs` incremented after this review

- [ ] If discrepancies found: open a draft PR updating the indication(s), citing this report

## 5. Notes / findings

*(Clinician fills in here — discrepancies, missing regimens, outdated claims, etc.)*

---