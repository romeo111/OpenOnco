# ESMO Verification Report — SRC-ESMO-RCC-2024

**Generated:** 2026-05-04  
**Branch:** feat/esmo-pdf-extract-2026-05-03  
**Mode:** PROTOTYPE — output for clinical review only, NOT auto-applied to KB  
**Legal status:** SOURCE_INGESTION_SPEC §6 red flag #1 pending resolution

## 1. Source metadata

| Field | Value |
|---|---|
| **Source ID** | `SRC-ESMO-RCC-2024` |
| **Title** | ESMO Renal Cell Carcinoma |
| **DOI** | [10.1016/j.annonc.2024.05.537](https://doi.org/10.1016/j.annonc.2024.05.537) |
| **Version** | 2024 |
| **Hosting mode** | referenced |
| **License** | CC-BY-NC-ND 4.0 |
| **Legal review** | reviewed |
| **PDF URL** | (not resolved) |
| **PDF pages** | 0 |
| **Therapy pages found** | 0 () |

## ⚠️ Extraction error

```
No open-access PDF found via Unpaywall and no direct_pdf_url provided.
```

## 2. Extracted therapy text (ESMO PDF source)

> **Attribution required on any use:** ESMO Renal Cell Carcinoma, v2024 (DOI: 10.1016/j.annonc.2024.05.537)

> **Do not copy-paste into KB** — clinician paraphrase required per SOURCE_INGESTION_SPEC §1.2.

*(No therapy-relevant text extracted.)*

## 3. Current KB indications for this source's diseases

Found **4** indication(s) linked to ['DIS-RCC'].


### IND-RCC-METASTATIC-1L-NIVO-IPI
- **Regimen:** REG-NIVO-IPI-RCC  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024

**Current KB rationale:**

  *(empty)*



### IND-RCC-METASTATIC-1L-PEMBRO-AXI
- **Regimen:** REG-PEMBRO-AXI-RCC  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024

**Current KB rationale:**

  *(empty)*



### IND-RCC-METASTATIC-2L-BELZUTIFAN
- **Regimen:** REG-BELZUTIFAN-MONO  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024

**Current KB rationale:**

  *(empty)*



### IND-RCC-VHL-DISEASE-BELZUTIFAN
- **Regimen:** REG-BELZUTIFAN-MONO  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024

**Current KB rationale:**

  *(empty)*



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