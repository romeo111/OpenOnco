# ESMO Verification Report — SRC-ESMO-BTC-2023

**Generated:** 2026-05-04  
**Branch:** feat/esmo-pdf-extract-2026-05-03  
**Mode:** PROTOTYPE — output for clinical review only, NOT auto-applied to KB  
**Legal status:** SOURCE_INGESTION_SPEC §6 red flag #1 pending resolution

## 1. Source metadata

| Field | Value |
|---|---|
| **Source ID** | `SRC-ESMO-BTC-2023` |
| **Title** | Biliary tract cancer: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up |
| **DOI** | [10.1016/j.annonc.2022.10.506](https://doi.org/10.1016/j.annonc.2022.10.506) |
| **Version** | 2023 |
| **Hosting mode** | referenced |
| **License** | Elsevier (Annals of Oncology) - ESMO clinical practice guidelines open access |
| **Legal review** | pending |
| **PDF URL** | https://hal.science/hal-03888631/document |
| **PDF pages** | 48 |
| **Therapy pages found** | 23 (3, 5, 6, 7, 8, 9, 10, 11, 12, 15…) |

## 2. Extracted therapy text (ESMO PDF source)

> **Attribution required on any use:** Vogel A, Bridgewater J, Edeline J, et al. Biliary tract cancer: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. Ann Oncol. 2023;34(2):127-140. (DOI: 10.1016/j.annonc.2022.10.506)

> **Do not copy-paste into KB** — clinician paraphrase required per SOURCE_INGESTION_SPEC §1.2.

```text
_[Page 3]_

Running header: ESMO Clinical Practice Guideline for biliary tract cancer
Word count: 10 478 (excluding title page, acknowledgements, funding and disclosure
sections); References: 113; Tables: 1; Figures: 1; Supplementary material: 1.
Key words: cholangiocarcinoma, gallbladder cancer, diagnosis, treatment, follow-up,
precision medicine
f
Highlights: o
o
• This ESMO Clinical Practice Guideline provides kery recommendations for managing
p
biliary tract cancer.
-
• The guideline covers clinical and pathologeical diagnosis, staging and risk
r
assessment, treatment and follow-up.
P
• A treatment and management algorithm for locoregional and advanced/metastatic
l
disease is provided. a
n
• ESCAT scores are given to describe the evidence level for genomic alterations as
r
biomarkers for using utargeted therapies.
• Recommendationos are based on available scientific data and the authors’ collective
J
expert opinion.

---

_[Page 5]_

Estimates of the relative incidence of the BTCs recognised by the new International
Classification of Diseases (ICD) 11th revision (ICD11) (iCCA, pCCA, dCCA and GBC)
have previously been biased by geography and type of study, as well as changes and
inaccuracies in ICD coding. iCCAs occur less commonly in east Asia where fluke-
related cancers increase the relative proportion of pCCA.11 iCCAs are more common in
studies of advanced disease compared with adjuvant series due to the greater number
of actionable alterations, availability of tissue for molecular diagnosis and potentially
improved prognosis.12-14 Finally, the changes in ICD and poor classification have further
increased uncertainty.15 Although CCA rates in Asia overall havfe remained static, the
o
incidence of iCCA has been steadily increasing in most oWestern countries, while the
incidence of d/pCCA has remained stable or decreaserd.16-18 These trends may be
p
explained by cross referencing of pCCA to iCCA by previous versions of the ICD,19
-
e
improved diagnostics, changing migration patterns in the West20 and the increasing
r
burden of chronic liver disease.21 P
The incidence of GBC is low in western Europe and the USA (1.6-2.0 cases per 100 000
l
a
population) and is decreasing, probably due to the increase in routine
n
cholecystectomy.22 Neverthe
r
less, incidence remains high in some regions (e.g. southern
u
Chile, northern India, Poland, south Pakistan and Japan).23
o
Risk factors for CCJA, which vary between regions, share chronic inflammation of the
biliary epithelium as a key feature.18,24 Patients with primary sclerosing cholangitis (PSC)
in Western countries and those with hepatobiliary flukes or hepatolithiasis in Asian
countries are at increased risk of pCCA. Guidelines for surveillance of patients with PSC
are available. In the absence of clear evidence regarding the optimal monitoring
strategy, annual imaging with magnetic resonance imaging (MRI) or magnetic
resonance cholangiopancreatography (MRCP) or ultrasound followed by investigation

… *(truncated)*
```

## 3. Current KB indications for this source's diseases

*(No indications found in KB for the diseases listed in `relates_to_diseases`. Either the disease IDs are missing from the source YAML, or the indications have not been authored yet.)*

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