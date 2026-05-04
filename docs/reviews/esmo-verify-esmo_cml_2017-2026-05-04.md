# ESMO Verification Report — SRC-ESMO-CML-2017

**Generated:** 2026-05-04  
**Branch:** feat/esmo-pdf-extract-2026-05-03  
**Mode:** PROTOTYPE — output for clinical review only, NOT auto-applied to KB  
**Legal status:** SOURCE_INGESTION_SPEC §6 red flag #1 pending resolution

## 1. Source metadata

| Field | Value |
|---|---|
| **Source ID** | `SRC-ESMO-CML-2017` |
| **Title** | Chronic myeloid leukaemia: ESMO Clinical Practice Guidelines for diagnosis, treatment and follow-up |
| **DOI** | [10.1093/annonc/mdx219](https://doi.org/10.1093/annonc/mdx219) |
| **Version** | 2017 |
| **Hosting mode** | referenced |
| **License** | ESMO (CC-BY-NC-ND) |
| **Legal review** | reviewed |
| **PDF URL** | (not resolved) |
| **PDF pages** | 0 |
| **Therapy pages found** | 0 () |

## ⚠️ Extraction error

```
No open-access PDF found via Unpaywall and no direct_pdf_url provided.
```

## 2. Extracted therapy text (ESMO PDF source)

> **Attribution required on any use:** Hochhaus et al., Annals of Oncology 2017; ESMO CML guideline (DOI: 10.1093/annonc/mdx219)

> **Do not copy-paste into KB** — clinician paraphrase required per SOURCE_INGESTION_SPEC §1.2.

*(No therapy-relevant text extracted.)*

## 3. Current KB indications for this source's diseases

Found **5** indication(s) linked to ['DIS-CML'].


### IND-CML-1L-2GEN-TKI
- **Regimen:** REG-2GEN-TKI-CML  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-MPN-2025, SRC-ELN-CML-2020, SRC-ESMO-CML-2017

**Current KB rationale:**

  Aggressive 1L for CML chronic phase: high-risk by ELTS / Sokal / EUTOS, younger patients
  with TFR ambition, OR low-risk patients preferring deeper / faster molecular response.
  2nd-generation TKI selected by comorbidity matrix per ELN 2020:
    - Default low-CV-risk: dasatinib OR nilotinib
    - CV disease / DM / hyperlipidemia → AVOID nilotinib + ponatinib → bosutinib or
  dasatinib
    - Pulmonary disease → AVOID dasatinib → nilotinib or bosutinib
    - GI disease → AVOID bosutinib → dasatinib or nilotinib
    - Pancreatitis history → AVOID nilotinib → dasatinib or bosutinib
  Faster early molecular response vs imatinib (DASISION, ENESTnd, BFORE) but no consistent
  OS benefit. Higher rate of TFR-eligibility (~30-40% achieve sustained DMR enabling TKI
  stop attempt).



### IND-CML-1L-IMATINIB
- **Regimen:** REG-IMATINIB-CML  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-MPN-2025, SRC-ELN-CML-2020, SRC-IRIS-OBRIEN-2003

**Current KB rationale:**

  Standard 1L for CML chronic phase: low-risk by ELTS / Sokal / EUTOS, elderly, comorbid
  (especially CV disease precluding nilotinib / ponatinib, or pulmonary disease precluding
  dasatinib), or where cost / access is limiting. Imatinib 400 mg PO daily with food. IRIS
  established 10-y OS ~83%. ELN 2020 milestones: BCR-ABL1 IS ≤10% at 3 mo, ≤1% at 6 mo,
  ≤0.1% (MMR) at 12 mo. PCR monitoring q3mo for first year, then q3-6mo. Switch to 2nd-gen
  TKI on suboptimal / failure. TFR attempt eligible after ≥3 years on TKI + sustained DMR
  (MR4.5) ≥2 years per ELN.



### IND-CML-2L-PONATINIB-T315I
- **Regimen:** REG-PONATINIB-CML  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-MPN-2025, SRC-PACE-CORTES-2013, SRC-ELN-CML-2020

**Current KB rationale:**

  Ponatinib is the only widely-available pan-BCR-ABL1 TKI active against T315I gatekeeper
  mutation. PACE phase-2 in r/r Ph+ leukemias post-multi-TKI or T315I+: 56% MCyR / 34% MMR
  in CML-CP; 70% MCyR in T315I-positive CML-CP. CRITICAL: substantial vascular toxicity
  (boxed warning — arterial occlusive events MI, stroke, PAOD, mortality). Mandatory
  baseline + ongoing CV-risk-factor management (BP, lipids, fasting glucose, smoking
  cessation). OPTIC trial validated response-adjusted dose reduction (45 mg → 15 mg PO daily
  upon achievement of MMR) reducing vascular events ~50% with maintained efficacy. Asciminib
  at higher dose (200 mg BID) is alternative for T315I — but ponatinib has broader real-
  world experience. Major Ukraine access barrier: not registered.



### IND-CML-3L-ASCIMINIB
- **Regimen:** REG-ASCIMINIB-CML  |  **Line:** 3  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-MPN-2025, SRC-ASCEMBL-REA-2021, SRC-ELN-CML-2020

**Current KB rationale:**

  Asciminib (STAMP — Specifically Targeting the ABL Myristoyl Pocket) is the first-in-class
  allosteric BCR-ABL1 inhibitor — binds the myristoyl pocket distinct from the ATP-binding
  site targeted by all classical TKIs. Mechanism avoids most ATP-site resistance mutations.
  ASCEMBL phase-3: asciminib 40 mg BID vs bosutinib 500 mg daily in CML-CP after ≥2 prior
  TKIs; MMR at 24 weeks 25.5% vs 13.2% (p=0.029). Superior tolerability vs bosutinib. Low
  cardiovascular toxicity (vs ponatinib). T315I mutation requires higher dose (200 mg BID) —
  addressed in a separate algorithm branch with ponatinib as the alternative. Mandatory
  kinase-domain mutation screening before switching per ELN 2020. Major Ukraine access
  barrier: not registered.



### IND-CML-ADVANCED-ALLOHCT
- **Regimen:** REG-ALLOHCT-CML-ADVANCED  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** moderate  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-MPN-2025, SRC-ELN-CML-2020

**Current KB rationale:**

  AlloHCT remains the only curative option for CML in blast crisis, accelerated phase, or
  after multi-TKI failure when ponatinib/asciminib access is limited. Outcomes are dominated
  by disease status at transplant — optimal control (≥CCyR, ideally MMR) pre-HCT
  substantially improves survival vs active blast crisis. Donor selection: HLA-matched
  sibling preferred; matched unrelated and haploidentical / cord acceptable for fit younger
  with no sibling. Conditioning: myeloablative for fit younger (Bu/Cy or Cy/TBI); reduced-
  intensity (Flu/Mel) for older / comorbid (HCT-CI ≥3, age >55). Post-HCT TKI maintenance
  (typically dasatinib or imatinib) for ≥2 years per institution reduces relapse. Major
  Ukraine access barrier: limited transplant centers, donor registry coverage limited;
  international referr



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