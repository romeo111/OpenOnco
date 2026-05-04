# ESMO Verification Report — SRC-ESMO-AML-2020

**Generated:** 2026-05-04  
**Branch:** feat/esmo-pdf-extract-2026-05-03  
**Mode:** PROTOTYPE — output for clinical review only, NOT auto-applied to KB  
**Legal status:** SOURCE_INGESTION_SPEC §6 red flag #1 pending resolution

## 1. Source metadata

| Field | Value |
|---|---|
| **Source ID** | `SRC-ESMO-AML-2020` |
| **Title** | Acute myeloid leukaemia in adult patients: ESMO Clinical Practice Guidelines for diagnosis, treatment and follow-up |
| **DOI** | [10.1016/j.annonc.2020.02.018](https://doi.org/10.1016/j.annonc.2020.02.018) |
| **Version** | 2020 |
| **Hosting mode** | referenced |
| **License** | ESMO (CC-BY-NC-ND) |
| **Legal review** | reviewed |
| **PDF URL** | http://www.annalsofoncology.org/article/S0923753420360798/pdf |
| **PDF pages** | 0 |
| **Therapy pages found** | 0 () |

## ⚠️ Extraction error

```
PDF download failed (http://www.annalsofoncology.org/article/S0923753420360798/pdf): HTTP Error 403: Forbidden
```

## 2. Extracted therapy text (ESMO PDF source)

> **Attribution required on any use:** Heuser et al., Annals of Oncology 2020; ESMO AML guideline (DOI: 10.1016/j.annonc.2020.02.018)

> **Do not copy-paste into KB** — clinician paraphrase required per SOURCE_INGESTION_SPEC §1.2.

*(No therapy-relevant text extracted.)*

## 3. Current KB indications for this source's diseases

Found **19** indication(s) linked to ['DIS-AML', 'DIS-APL'].


### IND-AML-1L-7-3
- **Regimen:** REG-AML-7-3  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-ELN-AML-2022, SRC-RATIFY-STONE-2017

**Current KB rationale:**

  Aggressive 1L for fit AML patients (typically age <70-75, ECOG ≤2, HCT-CI ≤3, no severe
  organ dysfunction). 7+3 induction (cytarabine 100-200 mg/m² CIVI d1-7 + daunorubicin 60-90
  mg/m² d1-3 or idarubicin 12 mg/m² d1-3); add midostaurin d8-21 if FLT3-ITD/TKD+ per
  RATIFY. Day-14 BM check; re-induction if blasts persist. Consolidation HiDAC 3 g/m² q12h
  d1, 3, 5 × 3-4 cycles for younger fit; alloHCT in CR1 for adverse-risk per ELN 2022 +
  donor availability.



### IND-AML-1L-7-3-GO-CBF
- **Regimen:** REG-AML-7-3-GO  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** []
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-ELN-AML-2022, SRC-ALFA-0701-CASTAIGNE-2012

**Current KB rationale:**

  Fractionated gemtuzumab ozogamicin (3 mg/m² days 1, 4, 7) added to standard 7+3 induction
  is Category 1 1L for fit CD33+ AML with CBF / favorable / intermediate cytogenetics (NCCN
  preferred). ALFA-0701 (Castaigne Lancet 2012): 2-yr EFS 40.8% vs 17.1% (HR 0.58); 2-yr OS
  53.2% vs 41.9% (HR 0.69). Hills meta-analysis 2014: GO reduces 5-yr mortality ~20% in
  favorable-risk (HR 0.47) + intermediate-risk (HR 0.84); NO benefit in adverse-risk (HR
  1.03). CBF AML — inv(16)/CBFB::MYH11, t(8;21)/RUNX1::RUNX1T1 — derives greatest benefit.
  Daunorubicin 60 mg/m² (not 90) with concurrent GO due to additive cardiotoxicity. NOT for
  adverse-risk (complex karyotype, TP53-mutant, monosomy 7) — standard 7+3 alone + alloHCT-
  bridge is the appropriate path for that subset. Hepatic VOD/SOS is dominant safety concer



### IND-AML-1L-CPX351-SECONDARY
- **Regimen:** REG-CPX351-AML  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-LANCET-CPX351-2018, SRC-ELN-AML-2022

**Current KB rationale:**

  CPX-351 (Vyxeos) liposomal cytarabine + daunorubicin in 5:1 synergistic ratio is FDA-
  approved for newly-dx therapy-related AML (t-AML) and AML with myelodysplasia-related
  changes (AML-MRC) in fit older patients (60-75). Pivotal phase-3 (Lancet et al., JCO
  2018): median OS 9.56 vs 5.95 mo for standard 7+3 (HR 0.69), 5-y OS 18% vs 8%. Higher
  CR/CRi (47.7% vs 33.3%) → more patients bridged to alloHCT (34% vs 25%) drives the
  survival benefit. CRITICAL labeling: dosing is "units/m²" not "mg/m²" — fatal dosing
  errors when liposomal product mistaken for free cytarabine + daunorubicin. ECHO +
  cumulative anthracycline tracking mandatory. Prolonged cytopenia recovery (often beyond
  day 35) — G-CSF + transfusion + infection prophylaxis. Ukraine: not registered,
  international referral required.



### IND-AML-1L-QUIZARTINIB-FLT3ITD
- **Regimen:** REG-QUIZARTINIB-7-3  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-QUANTUM-FIRST-ERBA-2023, SRC-ELN-AML-2022

**Current KB rationale:**

  Quizartinib + standard 7+3 induction + HiDAC consolidation + 3-year maintenance for newly-
  dx FLT3-ITD+ AML age 18-75. Pivotal QuANTUM-First (Erba et al., Lancet 2023) phase-3 RCT:
  median OS 31.9 vs 15.1 mo (HR 0.78, p=0.032) vs placebo+chemo. Approved FDA July 2023.
  Quizartinib is Type-II FLT3 inhibitor — covers FLT3-ITD ONLY, NOT FLT3-TKD (D835/I836);
  for FLT3-TKD or combined ITD+TKD, midostaurin (RATIFY) remains the option. QTc
  prolongation requires ACTIVE management: baseline + serial ECG, K+ ≥4.0 / Mg++ ≥2.0 BEFORE
  initiation, AVOID concomitant QT-prolonging drugs, dose-reduce 50% with strong CYP3A4
  inhibitors (azoles). AlloHCT in CR1 still recommended for high FLT3-allelic-burden /
  NPM1-wild-type per ELN 2022. Ukraine: not registered, major access barrier.



### IND-AML-1L-VEN-AZA
- **Regimen:** REG-VEN-AZA-AML  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-VIALE-A-DINARDO-2020, SRC-ELN-AML-2022

**Current KB rationale:**

  Standard 1L for AML patients NOT fit for intensive 7+3 induction (typically age ≥75, or
  ≥65 with HCT-CI ≥3, or ECOG ≥2 with multiple comorbidities). Venetoclax + azacitidine per
  VIALE-A: median OS 14.7 vs 9.6 mo with aza alone. TLS prophylaxis with allopurinol +
  hydration MANDATORY for first ramp cycle (3-day accelerated ramp: 100 → 200 → 400 mg).
  Long cytopenia windows are expected — G-CSF for febrile neutropenia, antimicrobial
  prophylaxis, attenuated venetoclax duration in subsequent cycles per institutional
  protocol.



### IND-AML-2L-GILTERITINIB-FLT3
- **Regimen:** REG-GILTERITINIB-AML  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-ADMIRAL-PERL-2019, SRC-ELN-AML-2022

**Current KB rationale:**

  Gilteritinib monotherapy is standard 2L+ for R/R FLT3-mutated AML per ADMIRAL phase-3
  trial: median OS 9.3 vs 5.6 mo (HR 0.64) vs investigator-choice salvage chemo. CRITICAL:
  re-test FLT3 status at relapse — clonal evolution can lose FLT3-mutated clone (~25% of
  relapses lose detectable FLT3) or acquire resistance mutations (FLT3-F691L gatekeeper).
  Gilteritinib covers BOTH FLT3-ITD AND FLT3-TKD (D835/I836) — distinct from quizartinib.
  Bridge to alloHCT for fit responders — gilteritinib alone NOT curative. Continue
  gilteritinib post-HCT as maintenance (MORPHO trial emerging data). Differentiation
  syndrome + QTc prolongation manageable but require active monitoring. Major Ukraine access
  barrier: not registered, international referral or compassionate-use only.



### IND-AML-2L-IDH2-ENASIDENIB
- **Regimen:** REG-ENASIDENIB-AML  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** moderate  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-ELN-AML-2022, SRC-ESMO-AML-2020

**Current KB rationale:**

  Enasidenib monotherapy is FDA-approved (Aug 2017) for R/R IDH2- mutated AML, on the basis
  of AG221-AML-001 phase 1/2: ORR 38%, CR 19%, median OS 9.3 mo. Mechanism: selective
  allosteric inhibitor of mutant IDH2 (R140Q, R172K) — reduces neomorphic 2-hydroxyglutarate
  oncometabolite, restoring TET2-dependent demethylation and inducing terminal
  differentiation of leukemic blasts. CRITICAL: re-test IDH2 status at relapse (subclonal
  loss possible). Bridge to alloHCT for fit responders — enasidenib alone NOT curative.
  Continue ≥6 cycles before declaring non-response (median time to first response ~1.9 mo).
  Differentiation syndrome (~14%) requires immediate dexamethasone + cytoreduction;
  hyperbilirubinemia (~80% any grade, UGT1A1 inhibition) usually asymptomatic. Major Ukraine
  access barrier: not r



### IND-AML-2L-KMT2A-REVUMENIB
- **Regimen:** REG-REVUMENIB-AML  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** moderate  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-ELN-AML-2022

**Current KB rationale:**

  Revumenib monotherapy is FDA-approved (Nov 2024) for R/R KMT2A- rearranged acute leukemia
  after ≥1 prior line of therapy, on the basis of AUGMENT-101 phase 1/2 trial — KMT2A-r AML
  cohort: ORR ~63%, CR/CRh ~23%. Mechanism: small-molecule inhibitor of menin- KMT2A
  protein-protein interaction; KMT2A-fusion proteins are dependent on menin recruitment to
  drive HOXA / MEIS1 transcription. CRITICAL: confirm KMT2A rearrangement at relapse (rare
  but possible loss). Bridge to alloHCT for fit responders — revumenib alone NOT curative.
  Differentiation syndrome (~16%) requires immediate dexamethasone + cytoreduction; QTc
  prolongation requires baseline + serial ECG with electrolyte correction. Major Ukraine
  access barrier: not registered, international referral or compassionate-use (Syndax EAP)
  only. Tr



### IND-AML-CR1-ORAL-AZA-MAINTENANCE
- **Regimen:** REG-ORAL-AZA-QUAZAR-MAINTENANCE  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-QUAZAR-WEI-2020, SRC-NCCN-AML-2025, SRC-ELN-AML-2022

**Current KB rationale:**

  Standard-track CR1 maintenance for AML patients ≥55 years not proceeding to alloHCT (the
  dominant scenario for older / unfit patients). QUAZAR AML-001 (Wei 2020): oral azacitidine
  300 mg PO daily × 14 d / 28-d cycle vs placebo improved median OS (24.7 vs 14.8 mo; HR
  0.69, p<0.001) and RFS (10.2 vs 4.8 mo; HR 0.65) — irrespective of post-induction
  consolidation status. FDA-approved Sep 2020 as Onureg. CRITICAL: only the oral CC-486
  formulation (Onureg) qualifies; SC/IV azacitidine is NOT bioequivalent and must NOT be
  substituted for QUAZAR maintenance. UA access barrier: Onureg not registered in Ukraine —
  engine should flag funding pathway as required step before activating this indication.



### IND-AML-PEDIATRIC-AAML1031
- **Regimen:** REG-AML-7-3  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-ELN-AML-2022

**Current KB rationale:**

  Pediatric AML (age ≤18) is treated per Children's Oncology Group AAML1031 (now AAML1831)
  protocol, which is distinct from adult 7+3-based therapy in dose density, supportive care,
  and risk stratification. Backbone: cytarabine 100 mg/m² CIVI × 7 days + daunorubicin 50
  mg/m² IV × 3 days induction (similar to 7+3 but with intensified consolidation).
  Consolidation with high-dose cytarabine (HiDAC 3 g/m² q12h × 6 doses × 2-3 cycles) — the
  cornerstone of pediatric AML cure. Risk stratification: low-risk (NPM1+/FLT3-ITD-, CEBPA
  biallelic, inv(16), t(8;21)) → chemotherapy alone; high-risk (FLT3-ITD high allelic ratio,
  KMT2A rearranged, complex karyotype, monosomy 7, TP53) → matched-related-donor or matched-
  unrelated-donor alloHCT in CR1. Gemtuzumab ozogamicin (GO) is added to induction for low-
  ris



### IND-AML-RR-IDH1-OLUTASIDENIB
- **Regimen:** REG-OLUTASIDENIB-AML-RR-IDH1  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** moderate  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-ELN-AML-2022, SRC-ESMO-AML-2020

**Current KB rationale:**

  Olutasidenib monotherapy is FDA-approved (Dec 2022) for R/R IDH1- mutated AML, on the
  basis of Study 2102-HEM-101 phase 1/2 single-arm trial — R/R AML efficacy cohort (n=153):
  CR + CRh rate 35% (95% CI 27-43); among CR + CRh responders, median DoR 25.9 mo, median
  time to CR + CRh 1.9 mo, 56-day mortality 8%. Transfusion independence achieved in 56% of
  baseline-dependent patients. Mechanism: selective small-molecule inhibitor of mutant IDH1
  (R132 variants) — reduces neomorphic 2-hydroxyglutarate (2-HG) oncometabolite, restoring
  TET2-dependent demethylation and inducing terminal differentiation of leukemic blasts.
  Compared to ivosidenib: olutasidenib has higher in vitro selectivity for mIDH1 R132 over
  WT-IDH1/IDH2; less prominent QT signal; distinguishing hepatotoxicity boxed warning
  (drug-i



### IND-EMERG-CINV-HIGH-EMETOGENIC
- **Regimen:** None  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-CTCAE-V5

**Current KB rationale:**

  For high-emetogenic chemotherapy (HEC), the 4-drug antiemetic regimen — NK1 receptor
  antagonist (aprepitant 125 mg PO d1, 80 mg PO d2-3 OR fosaprepitant 150 mg IV d1) + 5HT3
  receptor antagonist (palonosetron 0.25 mg IV d1 — preferred over ondansetron for delayed
  CINV) + dexamethasone 12 mg PO/IV d1 then 8 mg PO d2-4 + olanzapine 10 mg PO d1-4 — is
  NCCN/MASCC/ASCO Cat 1 standard. Olanzapine addition (Navari 2016 NEJM, Hashimoto 2020
  Lancet Oncol) substantially improves complete response (no vomiting + no rescue): ~80-90%
  with 4-drug vs ~65-70% with 3-drug. Acute CINV (0-24h) primarily mediated by 5HT3 release;
  delayed CINV (>24h) primarily by NK1/substance P + dexamethasone. Olanzapine adds dopamine
  D2 + serotonin 5HT2A blockade. AC regimen (doxorubicin + cyclophosphamide) is now
  classified



### IND-EMERG-FEBRILE-NEUTROPENIA-EMPIRICAL
- **Regimen:** None  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-NCCN-BCELL-2025

**Current KB rationale:**

  Febrile neutropenia (FN) is a medical emergency. Definition: single oral T ≥38.3°C OR
  sustained T ≥38.0°C ×1h, AND ANC <500/μL (or expected to fall <500/μL within 48h).
  Empirical broad-spectrum antibiotic must be initiated within 60 minutes of presentation
  per IDSA, NCCN, ASCO, MASCC guidelines — antibiotic delay >60 min correlates with
  increased mortality (Rosa 2014 J Clin Oncol). Default empirical regimen: piperacillin-
  tazobactam 4.5 g IV q6h (covers most gram-positive + gram-negative + Pseudomonas) OR
  cefepime 2 g IV q8h (similar coverage) OR meropenem 1 g IV q8h (if prior carbapenem-
  sparing reasonable; broader for ESBL/AmpC concerns). ADD vancomycin 15-20 mg/kg IV q12h
  IF: clinical suspicion of catheter-related infection, mucositis grade ≥3, hemodynamic
  instability, prior MRSA coloniza



### IND-EMERG-NEUTROPENIC-FEVER-PROPHYLAXIS
- **Regimen:** None  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-NCCN-BCELL-2025

**Current KB rationale:**

  G-CSF (filgrastim 5 μg/kg SC daily OR pegfilgrastim 6 mg SC fixed dose × 1) primary
  prophylaxis is recommended (NCCN/ASCO/EORTC) for chemotherapy regimens with predicted FN
  rate ≥20% (e.g., AML 7+3 induction, dose-dense AC-T, R-CHOEP, HD-MTX-based protocols,
  FOLFIRINOX in high-risk patients). For 10-20% predicted FN risk, G-CSF added if individual
  risk factors present (age >65, prior FN, advanced disease, bone marrow involvement,
  comorbidities, hepatic/renal dysfunction). FLUOROQUINOLONE antibacterial prophylaxis
  (levofloxacin 500 mg PO daily OR ciprofloxacin 500 mg PO BID) recommended per IDSA for
  predicted prolonged profound neutropenia (ANC <100/μL ≥7 days OR ANC <500/μL ≥10 days) —
  typical scenarios: AML induction/consolidation, allogeneic HSCT, lymphoma HD-MTX,
  autologous HSCT mobiliz



### IND-EMERG-TLS-PROPHYLAXIS-RASBURICASE
- **Regimen:** None  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-NCCN-BCELL-2025

**Current KB rationale:**

  Tumor lysis syndrome (TLS) prophylaxis with rasburicase 0.2 mg/kg IV daily × 1-5 days + IV
  hydration (2.5-3 L/m²/day) + concomitant allopurinol 300-600 mg PO daily is mandatory
  before cytotoxic / cytoreductive therapy in high-risk patients. Rasburicase (recombinant
  urate oxidase) cleaves uric acid → allantoin (renally cleared) — far more effective than
  allopurinol (which only inhibits new uric acid formation, does not break down preformed
  pool). Cairo-Bishop classification defines TLS risk: high-risk = Burkitt + AML with WBC
  >100K + B-ALL high risk + lymphoblastic lymphoma + bulky high-grade lymphoma with LDH >2×
  ULN. Rasburicase reduces TLS-related AKI from ~10-20% to <2% in high-risk cohorts.
  CONTRAINDICATIONS: G6PD deficiency (severe haemolysis risk — screen Asian / African /
  Mediterran



*(… 4 more indications not shown)*

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