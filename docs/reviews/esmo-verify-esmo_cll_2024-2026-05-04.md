# ESMO Verification Report — SRC-ESMO-CLL-2024

**Generated:** 2026-05-04  
**Branch:** feat/esmo-pdf-extract-2026-05-03  
**Mode:** PROTOTYPE — output for clinical review only, NOT auto-applied to KB  
**Legal status:** SOURCE_INGESTION_SPEC §6 red flag #1 pending resolution

## 1. Source metadata

| Field | Value |
|---|---|
| **Source ID** | `SRC-ESMO-CLL-2024` |
| **Title** | ESMO Clinical Practice Guideline on Chronic Lymphocytic Leukaemia |
| **DOI** | [10.1016/j.annonc.2024.06.016](https://doi.org/10.1016/j.annonc.2024.06.016) |
| **Version** | 2024 |
| **Hosting mode** | referenced |
| **License** | CC-BY-NC-ND 4.0 (typical for ESMO / Annals of Oncology) |
| **Legal review** | reviewed |
| **PDF URL** | http://www.annalsofoncology.org/article/S0923753424007476/pdf |
| **PDF pages** | 0 |
| **Therapy pages found** | 0 () |

## ⚠️ Extraction error

```
PDF download failed (http://www.annalsofoncology.org/article/S0923753424007476/pdf): HTTP Error 403: Forbidden
```

## 2. Extracted therapy text (ESMO PDF source)

> **Attribution required on any use:** ESMO Clinical Practice Guideline: Chronic Lymphocytic Leukaemia, 2024 (DOI: 10.1016/j.annonc.2024.06.016)

> **Do not copy-paste into KB** — clinician paraphrase required per SOURCE_INGESTION_SPEC §1.2.

*(No therapy-relevant text extracted.)*

## 3. Current KB indications for this source's diseases

Found **7** indication(s) linked to ['DIS-CLL'].


### IND-CLL-1L-BTKI
- **Regimen:** REG-ACALABRUTINIB-CONTINUOUS  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024, SRC-CLL14-FISCHER-2019, SRC-ELEVATE-TN-SHARMAN-2020

**Current KB rationale:**

  Standard 1L for CLL: BTKi continuous (acalabrutinib preferred over ibrutinib per ELEVATE-
  TN — superior tolerability, fewer cardiac / hypertension events). Continuous therapy until
  progression or intolerance. Suitable for most patients regardless of risk status, but
  high-risk (TP53/del 17p/IGHV-unmutated) may benefit equally or more from fixed-duration
  VenO (CLL14 evidence).



### IND-CLL-1L-VENO
- **Regimen:** REG-VENETOCLAX-OBINUTUZUMAB  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024, SRC-CLL14-FISCHER-2019

**Current KB rationale:**

  Aggressive-track 1L for CLL — fixed-duration venetoclax + obinutuzumab (12 months) per
  CLL14 evidence. Particularly valuable for high-risk (RF-CLL-HIGH-RISK fired) where
  chemoimmuno is contraindicated and continuous BTKi may have suboptimal long-term outcomes.
  Key advantages: finite duration, deep MRD-negative responses, no continuous drug exposure;
  key risks: TLS during ramp, infusion reactions to obinutuzumab, neutropenia.



### IND-CLL-1L-ZANUBRUTINIB
- **Regimen:** REG-ZANUBRUTINIB-CONTINUOUS  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024

**Current KB rationale:**

  Zanubrutinib continuous monotherapy is a preferred 1L BTKi for CLL, alongside
  acalabrutinib. Both second-generation BTKis are preferred over ibrutinib due to superior
  cardiac safety + comparable or superior PFS. ALPINE trial (r/r CLL): zanubrutinib superior
  to ibrutinib in PFS (HR 0.65) AND atrial fibrillation rate (5.2% vs 13.3%). SEQUOIA trial
  (1L CLL): zanubrutinib superior to BR. Continuous therapy until progression / intolerance.
  Suitable for most patients regardless of risk; high-risk (TP53/del 17p) particularly
  benefits as chemoimmuno is contraindicated.



### IND-CLL-2L-VENR-MURANO
- **Regimen:** REG-VENETOCLAX-RITUXIMAB  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024, SRC-CLL14-FISCHER-2019

**Current KB rationale:**

  Venetoclax + rituximab (VenR) for 24 months is the preferred 2L+ fixed-duration regimen
  for r/r CLL after 1L BTKi or chemoimmuno progression. MURANO trial: substantial PFS + OS
  benefit over BR with durable MRD-negative responses (~62% MRD-negative at end of
  treatment). Distinct from VenO (1L CLL14, 12 mo + obinutuzumab anti-CD20) — VenR is 24 mo
  + rituximab, designed for r/r setting. Particularly valuable for patients who are
  BCL2-naive and need fixed-duration time-off- treatment. Choice of VenR vs continued BTKi
  at progression depends on prior 1L exposure: if 1L was BTKi → VenR is the rational switch;
  if 1L was chemoimmuno → either VenR or BTKi acceptable.



### IND-CLL-3L-LISOCEL
- **Regimen:** None  |  **Line:** 3  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024

**Current KB rationale:**

  Lisocabtagene maraleucel (liso-cel; Breyanzi) received FDA accelerated approval (March
  2024) for relapsed/refractory CLL/SLL after ≥2 prior systemic lines including a BTK
  inhibitor and a BCL-2 inhibitor — the first CAR-T product approved for CLL. Defined 1:1
  CD4:CD8 cell composition with 4-1BB costimulation. TRANSCEND CLL-004 (Siddiqi et al.,
  Lancet 2023; updated J Clin Oncol 2024): primary cohort of double-exposed CLL (progression
  on cBTKi + BCL-2i, n≈87 evaluable) — ORR ~47%, CR + CRi ~18% with deep MRD-negative
  responses, median PFS ~12 months overall but durable in CR + uMRD subset. CRS profile
  predominantly low-grade (any ~85%, G≥3 ~9%); ICANS any ~30%, G≥3 ~20% (higher than MCL /
  DLBCL liso-cel — CLL-specific neurotox signal). Fills critical unmet need in double-
  exposed CLL where rem



### IND-CLL-3L-PIRTOBRUTINIB
- **Regimen:** REG-PIRTOBRUTINIB  |  **Line:** 3  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024

**Current KB rationale:**

  Pirtobrutinib (non-covalent reversible BTKi) for r/r CLL after ≥2 prior lines including a
  covalent BTKi. Distinct binding mechanism (C481-independent) overcomes BTK-C481-S/R
  mutations that confer resistance to ibrutinib / acalabrutinib / zanubrutinib. BRUIN trial:
  ORR 73% in heavily pretreated population (median 3 prior lines, ~50% with prior BCL2i too)
  — including ~71% ORR in confirmed BTK-C481- mutated subset. Particularly active in
  TP53-mutated CLL where conventional chemoimmunotherapy fails. Cardiac safety better than
  ibrutinib (afib ~3% vs ~7-15%). Major UA access barrier: not registered.



### IND-CLL-ELDERLY-O-CHL
- **Regimen:** None  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024, SRC-CLL14-FISCHER-2019

**Current KB rationale:**

  Obinutuzumab + chlorambucil (O-Chl) is the historical chemoimmunotherapy gold standard for
  elderly / comorbid CLL patients per CLL11 trial (Goede 2014 NEJM): O-Chl vs Rituximab +
  Chlorambucil (R-Chl) showed mPFS 26.7 vs 16.3 mo (HR 0.40), CR 21% vs 7%, MRD-negativity
  38% vs 4%, with comparable safety. 6-year update (Goede 2018 ASH) confirmed sustained OS
  benefit. iwCLL criteria define treatment indication; iwCLL-2018 response criteria define
  endpoints. Modern paradigm has shifted: most NCCN/ESMO Cat 1 1L for CLL are now BTKi
  continuous (acalabrutinib, zanubrutinib) or venetoclax + obinutuzumab fixed-duration
  (CLL14). O-Chl remains a valid option for very-frail patients (CIRS >6, severe comorbidity
  precluding BTKi/venetoclax) OR resource-limited settings. STUB regimen — no dedicated REG-
  O-C



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