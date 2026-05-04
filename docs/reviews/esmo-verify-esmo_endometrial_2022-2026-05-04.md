# ESMO Verification Report — SRC-ESMO-ENDOMETRIAL-2022

**Generated:** 2026-05-04  
**Branch:** feat/esmo-pdf-extract-2026-05-03  
**Mode:** PROTOTYPE — output for clinical review only, NOT auto-applied to KB  
**Legal status:** SOURCE_INGESTION_SPEC §6 red flag #1 pending resolution

## 1. Source metadata

| Field | Value |
|---|---|
| **Source ID** | `SRC-ESMO-ENDOMETRIAL-2022` |
| **Title** | ESMO-ESGO-ESTRO Endometrial Consensus |
| **DOI** | [10.1016/j.annonc.2022.05.009](https://doi.org/10.1016/j.annonc.2022.05.009) |
| **Version** | 2022 |
| **Hosting mode** | referenced |
| **License** | CC-BY-NC-ND 4.0 |
| **Legal review** | reviewed |
| **PDF URL** | http://www.annalsofoncology.org/article/S0923753422012078/pdf |
| **PDF pages** | 0 |
| **Therapy pages found** | 0 () |

## ⚠️ Extraction error

```
PDF download failed (http://www.annalsofoncology.org/article/S0923753422012078/pdf): HTTP Error 403: Forbidden
```

## 2. Extracted therapy text (ESMO PDF source)

> **Attribution required on any use:** ESMO-ESGO-ESTRO Endometrial Consensus, v2022 (DOI: 10.1016/j.annonc.2022.05.009)

> **Do not copy-paste into KB** — clinician paraphrase required per SOURCE_INGESTION_SPEC §1.2.

*(No therapy-relevant text extracted.)*

## 3. Current KB indications for this source's diseases

Found **5** indication(s) linked to ['DIS-ENDOMETRIAL'].


### IND-ENDOMETRIAL-2L-DOSTARLIMAB-DMMR
- **Regimen:** REG-DOSTARLIMAB-MONO-ENDOM  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 2
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-UTERINE-2025, SRC-ESMO-ENDOMETRIAL-2022

**Current KB rationale:**

  Dostarlimab monotherapy is NCCN cat 1 for 2L+ recurrent/metastatic dMMR endometrial
  carcinoma after 1L platinum-based chemotherapy failure (in patients who did NOT receive
  ICI in 1L). GARNET trial established durable responses (ORR 45%, DoR >16 mo).
  Pembrolizumab monotherapy is the labeled equivalent (KEYNOTE-158 pan-tumor MSI-H). This
  indication applies primarily to historical-era patients whose 1L predated ICI standard of
  care (RUBY/NRG-GY018 era ~2023+); newer dMMR patients who already received ICI in 1L
  should receive pembro+lenva or chemo re-challenge in 2L instead. Dramatically lower
  toxicity than pembro+lenva — preferred when single-agent ICI is appropriate clinical
  choice. Lynch syndrome screening mandatory for all dMMR endometrial.



### IND-ENDOMETRIAL-2L-PEMBRO-LENVA-PMMR
- **Regimen:** REG-PEMBRO-LENVATINIB-ENDOM  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 2
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-UTERINE-2025, SRC-ESMO-ENDOMETRIAL-2022

**Current KB rationale:**

  Pembrolizumab + lenvatinib is the NCCN cat 1 preferred 2L for advanced/ recurrent pMMR
  endometrial carcinoma after 1L platinum-based chemo failure. KEYNOTE-775 established OS +
  PFS + ORR benefit over investigator's-choice chemo (doxo or pacli). Indication applies
  primarily to pMMR patients (the majority of 2L population since dMMR patients now receive
  ICI in 1L per RUBY/NRG-GY018). Toxicity is substantial — proactive hypertension management
  + dose-reduction algorithm + anti-diarrheal supportive care needed. dMMR patients who did
  not receive ICI in 1L should preferentially receive single-agent ICI (dostarlimab GARNET
  or pembro KEYNOTE-158) rather than the heavier pembro+lenva combination.



### IND-ENDOMETRIAL-ADVANCED-1L-DOSTARLIMAB-CHEMO
- **Regimen:** REG-DOSTARLIMAB-CARBO-PACLI-ENDOM  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-UTERINE-2025

**Current KB rationale:**

  *(empty)*



### IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO
- **Regimen:** REG-PEMBRO-CARBO-PACLI-ENDOM  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-UTERINE-2025

**Current KB rationale:**

  *(empty)*



### IND-ENDOMETRIAL-STAGE-I-POLE-OBSERVATION
- **Regimen:** None  |  **Line:** 1  |  **Track:** surveillance
- **Evidence level:** high  |  **Reviewer sign-offs:** []
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-UTERINE-2025, SRC-ESMO-ENDOMETRIAL-2022, SRC-ESGO-ENDOMETRIAL-2025

**Current KB rationale:**

  PORTEC-3 / TransPORTEC pooled analyses demonstrated that Stage I endometrial carcinoma
  harboring a pathogenic POLE exonuclease-domain (POLE-EDM) mutation has near-100%
  recurrence-free survival regardless of histologic grade, and adjuvant chemoradiation
  provides NO incremental benefit. POLD1-EDM is rarer but mechanistically equivalent and
  grouped with POLE in TCGA / ESGO-ESTRO integrated risk classification. Following total
  hysterectomy + bilateral salpingo-oophorectomy, observation alone is the standard
  recommendation per NCCN Uterine 2025 and ESGO-ESTRO-ESP 2025 guidelines. Avoids
  unnecessary toxicity and cost in a population with excellent biology. Lynch screening
  still appropriate if any MMR/MSI features co-occur; germline counseling for POLD1 cases
  (PPAP differential).



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