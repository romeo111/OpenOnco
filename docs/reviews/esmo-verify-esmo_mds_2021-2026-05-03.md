# ESMO Verification Report — SRC-ESMO-MDS-2021

**Generated:** 2026-05-03  
**Branch:** feat/esmo-pdf-extract-2026-05-03  
**Mode:** PROTOTYPE — output for clinical review only, NOT auto-applied to KB  
**Legal status:** SOURCE_INGESTION_SPEC §6 red flag #1 pending resolution

## 1. Source metadata

| Field | Value |
|---|---|
| **Source ID** | `SRC-ESMO-MDS-2021` |
| **Title** | Myelodysplastic syndromes: ESMO Clinical Practice Guidelines for diagnosis, treatment and follow-up |
| **DOI** | [10.1016/j.annonc.2020.11.002](https://doi.org/10.1016/j.annonc.2020.11.002) |
| **Version** | 2021 |
| **Hosting mode** | referenced |
| **License** | ESMO (CC-BY-NC-ND) |
| **Legal review** | reviewed |
| **PDF URL** | http://www.annalsofoncology.org/article/S0923753420431291/pdf |
| **PDF pages** | 0 |
| **Therapy pages found** | 0 () |

## ⚠️ Extraction error

```
PDF download failed (http://www.annalsofoncology.org/article/S0923753420431291/pdf): HTTP Error 403: Forbidden
```

## 2. Extracted therapy text (ESMO PDF source)

> **Attribution required on any use:** Fenaux et al., Annals of Oncology 2021; ESMO MDS guideline (DOI: 10.1016/j.annonc.2020.11.002)

> **Do not copy-paste into KB** — clinician paraphrase required per SOURCE_INGESTION_SPEC §1.2.

*(No therapy-relevant text extracted.)*

## 3. Current KB indications for this source's diseases

Found **7** indication(s) linked to ['DIS-MDS-LR', 'DIS-MDS-HR'].


### IND-MDS-LR-1L-ESA
- **Regimen:** REG-ESA-MDS-LR  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** moderate  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-ESMO-MDS-2021

**Current KB rationale:**

  Standard 1L for symptomatic anemia in MDS-LR (IPSS-R Very Low / Low / Intermediate).
  Patient selection: endogenous EPO ≤500 mU/mL + RBC TD ≤2U/month → response rate ~50-60%.
  Epoetin alfa 60,000 IU SC weekly OR darbepoetin 150-300 μg SC weekly. Add G-CSF in non-
  responders if RS-MDS subtype. Target Hb 10-12 g/dL (do NOT exceed; boxed mortality / VTE
  warning). Switch to luspatercept (RS-MDS / 1L COMMANDS) or lenalidomide (del 5q) or HMA
  escalation on failure.



### IND-MDS-LR-1L-LUSPATERCEPT
- **Regimen:** REG-LUSPATERCEPT-MDS-LR  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-ESMO-MDS-2021, SRC-COMMANDS-FENAUX-2020

**Current KB rationale:**

  Aggressive 1L for MDS-LR symptomatic anemia in jurisdictions with luspatercept access —
  superior 1L over ESA per COMMANDS trial (~58% TI vs 31% ESA at 12 wk; benefit greatest in
  SF3B1+ / RS-MDS but extends to non-RS too). Originally established as 2L (MEDALIST: RS-MDS
  post-ESA failure). Luspatercept 1.0 mg/kg SC q3wk titrating to 1.75 mg/kg if no response
  after 2 doses. Reassess at 24 weeks. In Ukraine NOT registered — practical 1L remains ESA.



### IND-MDS-LR-2L-IMETELSTAT
- **Regimen:** REG-IMETELSTAT-MDS-LR  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-IMERGE-PLATZBECKER-2024, SRC-ESMO-MDS-2021, SRC-IPSS-M-BERNARD-2022

**Current KB rationale:**

  Imetelstat is a first-in-class telomerase inhibitor approved June 2024 for transfusion-
  dependent LR-MDS post-ESA failure (IMerge phase-3: Platzbecker et al., Lancet 2024).
  8-week RBC TI 39.8% vs 15.0% placebo (p<0.001); sustained 24-week TI 28% vs 3.3%; median
  TI duration ~52 weeks. Active in non-del(5q) setting where lenalidomide is not indicated.
  Cytopenia (severe thrombocytopenia + neutropenia) is the dominant toxicity — active
  management with transfusion + G-CSF + dose modification mandatory. Baseline + serial LFT
  (hepatotoxicity Grade ≥3 observed). Major Ukraine access barrier: not registered. Consider
  sequential lenalidomide → imetelstat in del(5q) post- lenalidomide failure (data
  extrapolation; not formally studied).



### IND-MDS-LR-LENALIDOMIDE-DEL5Q
- **Regimen:** REG-LENALIDOMIDE-MDS-DEL5Q  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-MDS-004-FENAUX-2011, SRC-ESMO-MDS-2021

**Current KB rationale:**

  Lenalidomide is Cat 1 standard for transfusion-dependent del(5q) LR-MDS. Pivotal MDS-003
  (Houston phase-2) + MDS-004 (phase-3 RCT, Fenaux et al., Blood 2011) — at 10 mg PO
  d1-21/28d: ~56% achieve RBC TI vs 5.9% placebo at 26 weeks; ~20-25% achieve cytogenetic CR
  with loss of del(5q) clone. Median TI duration >2 years. Mechanism: cereblon-mediated
  selective degradation of casein kinase 1A1 (CK1α), encoded within the 5q33.1 commonly-
  deleted region — del(5q) cells haploinsufficient → uniquely sensitive. CRITICAL:
  lenalidomide is teratogenic — REMS / Revlimid Risk Management Programme mandatory;
  pregnancy testing weekly first month, then monthly. VTE prophylaxis (aspirin 81-325 mg PO
  daily; LMWH for higher-risk) mandatory. Avoid concurrent ESA (additive VTE risk). MUST
  screen TP53 — TP53-mutat



### IND-MDS-HR-1L-AZA
- **Regimen:** REG-AZA-MDS-HR  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-ESMO-MDS-2021, SRC-IPSS-M-BERNARD-2022

**Current KB rationale:**

  Standard 1L for MDS-HR (IPSS-R high / very high; IPSS-M High / Very High; MDS-IB1/IB2).
  Azacitidine 75 mg/m² SC days 1-7 q28d (AZA-001: median OS 24.5 vs 15.0 mo, HR 0.58).
  Continue ≥6 cycles before declaring failure (response often delayed to cycles 4-6).
  Concurrent alloHCT donor search if eligible (RF-MDS-TRANSPLANT- ELIGIBLE) — do NOT defer
  donor search to HMA failure (search takes 3-6 months). Decitabine 20 mg/m² × 5 d q28d is
  functionally equivalent alternative; choice often local.



### IND-MDS-HR-1L-VEN-AZA
- **Regimen:** REG-VEN-AZA-AML  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** low  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-VIALE-A-DINARDO-2020

**Current KB rationale:**

  Aggressive 1L for MDS-HR with high blast burden (MDS-IB2, blasts 10-19%) where intensified
  disease control is desired pre-alloHCT bridging. Off-label use of ven+aza schedule
  (extrapolated from VIALE-A AML). NOT yet phase-3 confirmed for HR-MDS specifically; active
  trials (VERONA) ongoing. Toxicity (cumulative cytopenias) is substantial; selection biased
  toward fit patients who could tolerate alloHCT downstream. TLS prophylaxis MANDATORY for
  first ramp cycle.



### IND-MDS-HR-ALLOHCT
- **Regimen:** REG-ALLOHCT-MDS-HR  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** moderate  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-AML-2025, SRC-ESMO-MDS-2021, SRC-IPSS-M-BERNARD-2022

**Current KB rationale:**

  AlloHCT is the ONLY curative option for MDS-HR — mandatory consideration in ALL
  transplant-eligible patients (typically age <70-75, adequate organ function, ECOG ≤2,
  suitable donor, caregiver support). 5-y OS post-HCT 40-50% vs 10-15% with non-transplant
  therapy. Donor search initiated CONCURRENTLY with HMA induction — donor identification can
  take 3-6 months and HMA-failure rapid-pivot needed. HMA bridging during search improves
  disease control before transplant. Conditioning intensity tailored to age + comorbidity
  (myeloablative for fit young; reduced-intensity for older / comorbid). TP53-mutated MDS-HR
  has worse outcomes (~20-30% 3-y OS) but HCT still the only curative pathway; consider
  clinical trial enrollment + post-HCT azacitidine maintenance. CRITICAL: do NOT defer donor
  search to



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