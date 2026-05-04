# ESMO Verification Report — SRC-ESMO-MELANOMA-2024

**Generated:** 2026-05-04  
**Branch:** feat/esmo-pdf-extract-2026-05-03  
**Mode:** PROTOTYPE — output for clinical review only, NOT auto-applied to KB  
**Legal status:** SOURCE_INGESTION_SPEC §6 red flag #1 pending resolution

## 1. Source metadata

| Field | Value |
|---|---|
| **Source ID** | `SRC-ESMO-MELANOMA-2024` |
| **Title** | ESMO Cutaneous Melanoma |
| **DOI** | [10.1016/j.annonc.2024.11.006](https://doi.org/10.1016/j.annonc.2024.11.006) |
| **Version** | 2024 |
| **Hosting mode** | referenced |
| **License** | CC-BY-NC-ND 4.0 |
| **Legal review** | reviewed |
| **PDF URL** | https://scholarlypublications.universiteitleiden.nl/access/item%3A4301150/view |
| **PDF pages** | 22 |
| **Therapy pages found** | 13 (3, 4, 5, 8, 9, 10, 11, 12, 13, 14…) |

## 2. Extracted therapy text (ESMO PDF source)

> **Attribution required on any use:** ESMO Cutaneous Melanoma, v2024 (DOI: 10.1016/j.annonc.2024.11.006)

> **Do not copy-paste into KB** — clinician paraphrase required per SOURCE_INGESTION_SPEC §1.2.

```text
_[Page 3]_

T.Amaralet al. Annals of Oncology
Supplementary Figure S1, available at https://doi.org/10. thicknessinmillimetres(Breslow,measuredtothenear-
1016/j.annonc.2024.11.006. est0.1mm),presenceofulceration,microsatellites,lym-
phovascular invasion, neurotropism/perineural invasion,
Molecular characterisation tumour-infiltrating lymphocytes (TILs), presence of
regression and presence or absence of tumour at the
Testing for actionable mutations is recommended for pa-
deep and peripheral edges of the biopsy [II, A]. Mitotic
tients with resectable or unresectable stage III or IV mela-
rate should also be reported [III, B].
noma. Mutation testing should be considered for high-risk,
(cid:3) Areportonthewideexcisionshouldalsobemadeavail-
clinical stage IIB-IIC melanoma, but is not routinely rec-
able for complete pathological characterisation [II, A].
ommended for stage I or IIA disease. Mutation testing of
(cid:3) Testing foractionable mutations is recommended in pa-
BRAF V600 is mandatory, whereas testing for other BRAF
tientswithresectableorunresectablestageIIIorIVmel-
mutations is optional. A full list of BRAF mutations byclass
anoma [I, A] and should be considered in clinical stage
isprovidedinSupplementaryTableS4,availableathttps://
IIB-IIC [V, C] but not for stage I or IIA disease [V, D].
doi.org/10.1016/j.annonc.2024.11.006. Testing can be
B BRAFV600testingismandatory[I,A;ESCATscore:I-A].
offered for NRAS and c-KITmutations; testing for NTRK al-
terations is recommended in the absence of BRAF or RAS
mutations [see ESMO Scale for Clinical Actionability of
STAGING AND RISK ASSESSMENT
molecular Targets (ESCAT) for further detailsdSupple-
mentary Table S5, available at https://doi.org/10.1016/j. Details on the staging and risk assessment of cutaneous
annonc.2024.11.006]. Mutation analysis using next- melanoma are provided in the Supplementary Material
generation sequencing can be offered for unresectable Section 4 and Table S2, available at https://doi.org/10.
melanoma. Mutation analysis must be carried out in 1016/j.annonc.2024.11.006.
accredited (certified) institutes that have careful quality
controls and appropriate bioinformatic knowledge. Recommendations
The main melanoma subtypes are associated with
(cid:3) Stagingshould be accordingto the eighth edition ofthe
different mutational landscapes,1 as shown in
American Joint Committee on Cancer (AJCC) TNM
Supplementary Table S6, available at https://doi.org/10.
(tumourenodeemetastasis)stagingsystem(AJCC8)[II,A].
1016/j.annonc.2024.11.006. In addition to the mutational
(cid:3) Sentinel lymph node biopsy (SLNB) is not routinely rec-
status, reporting programmed death-ligand 1 (PD-L1)
ommendedforpatientswithamelanomaofAJCC8stage
expression by immunohistochemistry is recommended for
pT1a (e.g.with a tumour thickness <0.8 mm and no ul-
all unresectable stage III and IV melanoma, since the Eu-
ceration) [II, E].
ropean Medicines Agency (EMA) has approved the admin-
(cid:3) SLNB is not usually reco

… *(truncated)*
```

## 3. Current KB indications for this source's diseases

Found **11** indication(s) linked to ['DIS-MELANOMA'].


### IND-MELANOMA-2L-KIT-IMATINIB
- **Regimen:** REG-IMATINIB-KIT-MELANOMA  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** moderate  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-CARVAJAL-KIT-MELANOMA-2013, SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024

**Current KB rationale:**

  ~15-20% of mucosal and acral melanomas carry actionable KIT mutations (exon 11 L576P, exon
  13 K642E most common). Carvajal 2011 (JAMA, NCT00470470) established imatinib 400 mg PO
  BID produces ORR 23% with durable responses (>1 year) in this subset. KIT amplification
  alone is NOT predictive — actionable point mutation required. ESCAT IIA per ESMO.
  Position: niche but high-value option for the small KIT-mutant subset, prioritized early
  in 2L+ algorithm because it is oral, low-toxicity, and available (imatinib generic widely
  accessible in UA). Off-label in melanoma (Glivec licensed in UA for CML/GIST/Ph+ALL); MDT
  documentation required.



### IND-MELANOMA-2L-POST-BRAFI-IPI-NIVO
- **Regimen:** REG-NIVO-IPI-MELANOMA  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-CHECKMATE-067-LARKIN-2019, SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024

**Current KB rationale:**

  For patients who received 1L BRAFi+MEKi (typically driven by visceral crisis or active
  brain metastases requiring rapid response in a BRAF V600+ patient), 2L is anti-PD-1-based
  IO. The ipi+nivo doublet is the most active IO option (CheckMate-067: 5-y OS 52% in 1L;
  benefit retained but attenuated post-BRAFi). Acceptable 2L alternative when patient is fit
  (ECOG ≤1) and can tolerate combo Grade 3-4 irAE rates ~50%. For frailer patients, anti-
  PD-1 monotherapy or rela+nivo (if accessible) are reasonable de-escalations. DREAMseq
  supports the IO-after-targeted sequence retains meaningful activity.



### IND-MELANOMA-2L-POST-IO-BRAFI-MEKI
- **Regimen:** REG-ENCORAFENIB-BINIMETINIB-MELANOMA  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-COLUMBUS-DUMMETT-2018, SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024

**Current KB rationale:**

  For BRAF V600E/K-mutant metastatic melanoma after progression on 1L anti-PD-1
  immunotherapy, BRAFi+MEKi doublet is the standard 2L per NCCN/ESMO. COLUMBUS established
  encorafenib + binimetinib as the most tolerable doublet (less pyrexia than dabrafenib +
  trametinib, less photosensitivity than vemurafenib). DREAMseq confirmed the IO-first →
  BRAFi+MEKi-second sequence is superior to the reverse for BRAF-mutant patients. Dabrafenib
  + trametinib (REG-DABRAFENIB-TRAMETINIB-NSCLC) is an interchangeable cat 1 alternative for
  institutions where binimetinib is unavailable.



### IND-MELANOMA-2L-RELATLIMAB-NIVOLUMAB
- **Regimen:** REG-RELATLIMAB-NIVOLUMAB-MELANOMA  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-RELATIVITY-047-TAWBI-2022, SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024

**Current KB rationale:**

  Relatlimab + nivolumab (Opdualag fixed-dose) is the first anti-LAG-3 + anti-PD-1
  combination, FDA-approved 2022 in 1L metastatic melanoma per RELATIVITY-047 (mPFS 10.1 vs
  4.6 mo vs nivo mono). Key differentiator vs ipi+nivo: Grade 3-4 treatment-related AE 18.9%
  vs ~50%. Position in our 2L+ algorithm: IO-naive alternative (the patient received 1L
  BRAFi+MEKi and so has not yet exhausted PD-1/LAG-3 axis), particularly attractive when
  ipi-grade irAE risk is unacceptable. Trial was 1L; off-label positioning at 2L requires
  MDT documentation. Note: if RELATIVITY was used at 1L (IO-naive cohort), this Indication
  does NOT apply at 2L — patient should move to BRAFi+MEKi (if BRAF V600+) or alternative
  salvage.



### IND-MELANOMA-3L-LIFILEUCEL
- **Regimen:** REG-LIFILEUCEL-TIL-MELANOMA  |  **Line:** 3  |  **Track:** aggressive
- **Evidence level:** moderate  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-C14401-CHESNEY-2024, SRC-NCCN-MELANOMA-2025

**Current KB rationale:**

  Lifileucel (autologous TIL therapy, Amtagvi) is the first cellular therapy approved for
  any solid tumor (FDA 2024-02-16, accelerated). C-144-01 pooled cohorts demonstrated ORR
  31.4% with mOS 13.9 mo in patients who had exhausted anti-PD-1 (and BRAFi+MEKi if BRAF
  V600+) — a population with otherwise grim prognosis (historical mOS ~6-8 mo). Single-
  infusion treatment intent. Specialty-center pathway: tumor procurement → ~22-day central
  manufacturing → cy/flu lymphodepletion → TIL infusion → up to 6 doses bolus IL-2 → 4-week
  recovery. Treatment-related mortality ~7% — strict patient selection required (ECOG ≤1,
  organ function adequate for IL-2). Ukraine access pathway: international referral only.



### IND-MELANOMA-3L-POST-LIFILEUCEL
- **Regimen:** None  |  **Line:** 4  |  **Track:** palliative
- **Evidence level:** very_low  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024

**Current KB rationale:**

  Patients with advanced melanoma who progress through nivolumab + ipilimumab 1L, BRAF/MEK
  targeted 2L (if BRAF-mutant), AND lifileucel TIL therapy 3L (FDA-approved Feb 2024 for
  post-ICI metastatic melanoma; ORR ~31%, mPFS 4.1 mo) face a 4L+ setting with no
  established standard. Best supportive care + clinical trial enrollment is the dominant
  recommendation. Empirical single-agent chemotherapy (dacarbazine, temozolomide,
  paclitaxel, carboplatin/paclitaxel) has historical ORR <15% with mPFS 1.5-3 mo. ICI re-
  challenge (PD-1 monotherapy or CTLA-4 add-back) has anecdotal evidence; bispecifics on
  trial (tebentafusp for HLA-A*02:01 uveal melanoma — NOT applicable for cutaneous melanoma
  4L+). Brain metastases common at this stage; SRS + dexamethasone palliation often the
  focus. Hospice referral dis



### IND-MELANOMA-ADJUVANT-PEMBRO-STAGE-III
- **Regimen:** REG-PEMBRO-ADJUVANT-MELANOMA  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** []
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024, SRC-KEYNOTE-054-EGGERMONT-2018, SRC-CHECKMATE-238-WEBER-2017

**Current KB rationale:**

  Adjuvant pembrolizumab × 12 months is Category 1 standard-track adjuvant therapy for
  resected stage III cutaneous melanoma per KEYNOTE-054 / EORTC-1325 (Eggermont NEJM 2018;
  5-yr update Lancet Oncol 2021). 5-yr RFS 55.4% vs 38.3% with placebo (HR 0.61); benefit
  consistent across PD-L1+ and PD-L1- subgroups, BRAF-mutant and BRAF-WT, and across stage
  III sub-stages. Adjuvant nivolumab (CheckMate-238) is interchangeable alternative with
  comparable efficacy. BRAF-mutant patients have additional option of adjuvant dabrafenib +
  trametinib (COMBI-AD; 5-yr RFS 52% vs 36%) — clinical choice driven by toxicity profile,
  prior IO exposure, patient preference; head-to-head data lacking. Start within 12 weeks of
  definitive surgery; complete 18 cycles unless recurrence / intolerance.



### IND-MELANOMA-BRAF-METASTATIC-1L-DABRA-TRAME
- **Regimen:** REG-DABRAFENIB-TRAMETINIB-NSCLC  |  **Line:** 1  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024, SRC-COMBI-D-LONG-2014

**Current KB rationale:**

  *(empty)*



### IND-MELANOMA-METASTATIC-1L-NIVO-IPI
- **Regimen:** REG-NIVO-IPI-MELANOMA  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024, SRC-CHECKMATE-067-LARKIN-2019

**Current KB rationale:**

  *(empty)*



### IND-MELANOMA-METASTATIC-1L-PEMBRO-MONO
- **Regimen:** REG-PEMBRO-MONO-MELANOMA  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** []
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024, SRC-KEYNOTE-006-ROBERT-2015

**Current KB rationale:**

  Pembrolizumab monotherapy is a Category 1 preferred 1L for advanced / metastatic melanoma
  (KEYNOTE-006). PD-L1-agnostic — used regardless of CPS / TPS. Particularly preferred over
  ipi+nivo combination when combination irAE profile (~55% grade 3-4) is unacceptable: irAE-
  frail patients (autoimmune comorbidity, prior solid-organ transplant contraindication
  aside, age ≥75, ECOG 2). Lower G3-4 irAE rate (~17%) with comparable single-agent IO
  efficacy. BRAF-mutated patients have the alternative of BRAFi+MEKi (dabrafenib+trametinib)
  — choice driven by tumor burden, LDH, symptomatic disease, and patient/ clinician
  preference; IO is generally preferred for durable response potential. Combination ipi+nivo
  remains preferred where tolerable (younger fit, low autoimmune risk, brain mets).



### IND-MELANOMA-NIVO-MAINT
- **Regimen:** None  |  **Line:** 1  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024, SRC-CHECKMATE-067-LARKIN-2019

**Current KB rationale:**

  After 4 cycles of nivolumab + ipilimumab combination induction (4 doses q3w) per
  CheckMate-067, patients transition to nivolumab monotherapy maintenance (240 mg q2w or 480
  mg q4w) until progression, unacceptable toxicity, or maximum 2 years. CheckMate-067
  (Larkin 2015 NEJM, Wolchok 2017/2019/2022 updates): 5-yr OS 52% combination vs 44% nivo
  mono vs 26% ipi mono; 6.5-yr OS plateau ~49%; mOS NR for combination arm vs 36.9 mo nivo
  mono. Approximately 50-60% of patients have durable disease control beyond treatment
  cessation. PD-L1 status does NOT clinically modify combination choice in advanced melanoma
  (unlike NSCLC). Brain metastases (CheckMate-204) respond well — combination with nivo+ipi
  is preferred over mono. STUB regimen — no dedicated REG- entity for nivo maintenance post-
  CheckMate-0



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