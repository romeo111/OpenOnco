# ESMO Verification Report — SRC-ESMO-NSCLC-EARLY-2024

**Generated:** 2026-05-04  
**Branch:** feat/esmo-pdf-extract-2026-05-03  
**Mode:** PROTOTYPE — output for clinical review only, NOT auto-applied to KB  
**Legal status:** SOURCE_INGESTION_SPEC §6 red flag #1 pending resolution

## 1. Source metadata

| Field | Value |
|---|---|
| **Source ID** | `SRC-ESMO-NSCLC-EARLY-2024` |
| **Title** | ESMO Clinical Practice Guideline on Early NSCLC + Stage III |
| **DOI** | [10.1016/j.annonc.2025.08.003](https://doi.org/10.1016/j.annonc.2025.08.003) |
| **Version** | 2025 |
| **Hosting mode** | referenced |
| **License** | CC-BY-NC-ND 4.0 (typical for ESMO / Annals of Oncology) |
| **Legal review** | reviewed |
| **PDF URL** | https://www.annalsofoncology.org/article/S0923-7534(25)00923-8/pdf |
| **PDF pages** | 0 |
| **Therapy pages found** | 0 () |

## ⚠️ Extraction error

```
PDF download failed (https://www.annalsofoncology.org/article/S0923-7534(25)00923-8/pdf): HTTP Error 403: Forbidden
```

## 2. Extracted therapy text (ESMO PDF source)

> **Attribution required on any use:** ESMO Clinical Practice Guideline on Early NSCLC + Stage III, v2024 (DOI: 10.1016/j.annonc.2025.08.003)

> **Do not copy-paste into KB** — clinician paraphrase required per SOURCE_INGESTION_SPEC §1.2.

*(No therapy-relevant text extracted.)*

## 3. Current KB indications for this source's diseases

Found **36** indication(s) linked to ['DIS-NSCLC'].


### IND-NSCLC-2L-BRAF-V600E-DAB-TRAM
- **Regimen:** REG-DABRAFENIB-TRAMETINIB-NSCLC  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-BRF113928-PLANCHARD-2016, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Dabrafenib (BRAF inhibitor) + trametinib (MEK inhibitor) for BRAF V600E-mutant metastatic
  NSCLC (~1-2% of NSCLC adenocarcinoma). BRF113928 phase-2 cohort B (pretreated): ORR 63%,
  mPFS 9.7 mo, mOS 18.2 mo. Cohort C (1L) ORR 64%. FDA approval 2017 for any-line BRAF
  V600E+ NSCLC. Pyrexia (~50% any-grade, often recurrent) and LVEF decline are dominant
  clinical management challenges; protocol-driven pyrexia management (hold both, restart
  when afebrile) maintains exposure. V600K, V600D, and non-V600 BRAF mutations are NOT
  reliably responsive to this regimen — confirm V600E specifically. Encorafenib +
  binimetinib (PHAROS, 2023) is alternative — same combination strategy, comparable
  efficacy, slightly less pyrexia.



### IND-NSCLC-2L-DATO-DXD
- **Regimen:** REG-DATO-DXD-NSCLC-2L  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Datopotamab deruxtecan (Dato-DXd, TROP2-directed ADC with topoisomerase-I payload) for 2L+
  nonsquamous metastatic NSCLC after platinum + ICI (or post-osimertinib + platinum for
  EGFR-mut). TROPION-Lung01 phase III (n=604): nonsquamous PFS HR 0.84 (95% CI 0.74-0.95);
  squamous subgroup did not benefit; ITT OS not significant. FDA approval (2025-01)
  restricted to actionable-mutation (EGFR-mutant) post-targeted-therapy + chemotherapy
  subset based on TROPION-Lung05 supporting evidence. Aggressive-track 2L for nonsquamous
  (especially EGFR-mut post-osi + platinum) with adequate pulmonary baseline. ILD is the
  dominant class toxicity — adjudicated ~8% all-grade; lower threshold for permanent
  discontinuation than T-DXd. Patient selection: prefer for nonsquamous histology,
  especially EGFR-mutant; avoi



### IND-NSCLC-2L-DOCETAXEL-RAMUCIRUMAB
- **Regimen:** REG-DOCETAXEL-RAMUCIRUMAB  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** pending_clinical_signoff
- **KB sources cited:** SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Docetaxel + ramucirumab for 2L driver-negative NSCLC after 1L chemo+ICI failure (REVEL
  trial — pre-ICI era but mechanism still applies). Adds modest OS + PFS benefit over
  single-agent docetaxel. In modern post-ICI+chemo failure setting, this represents the
  default cytotoxic 2L. Single-agent docetaxel (without ramucirumab) is the realistic
  fallback in Ukraine where ramucirumab not NSZU- reimbursed. For driver-positive disease
  that progressed on targeted therapy, this Indication does NOT apply — patient receives
  next- generation TKI per molecular subtype.



### IND-NSCLC-2L-EGFR-EX20INS-AMIVANTAMAB
- **Regimen:** REG-AMIVANTAMAB-MONO-NSCLC-EX20INS  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-CHRYSALIS-PARK-2021, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Amivantamab monotherapy for EGFR exon 20 insertion-mutated metastatic NSCLC progressing on
  platinum chemotherapy. EGFR Ex20ins (~10% of EGFR-mut NSCLC) is poorly responsive to
  standard EGFR-TKIs (osimertinib ORR ~10-25%) due to the variable insertion site that
  distorts the ATP-binding pocket. CHRYSALIS phase-1 expansion: ORR 40%, mPFS 8.3 mo, mOS
  22.8 mo — basis for FDA accelerated approval (2021). PAPILLON has subsequently established
  ami+carbo+pem as the 1L SoC for Ex20ins; this 2L mono indication applies when 1L was
  platinum alone (e.g., before PAPILLON results, or in resource-limited settings). DNA-NGS
  (not hotspot PCR) is essential for Ex20ins detection — sites are variable and not all
  assays capture them. SC amivantamab strongly preferred over IV given dramatic IRR
  reduction.



### IND-NSCLC-2L-EGFR-POST-OSI-AMI-LAZ
- **Regimen:** REG-AMIVANTAMAB-LAZERTINIB-NSCLC-2L  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-MARIPOSA2-PASSARO-2024, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Amivantamab (EGFR-MET bispecific antibody) + lazertinib (3rd-gen EGFR-TKI) for EGFR-
  mutated metastatic NSCLC (ex19del / L858R) progressing on 1L osimertinib. MARIPOSA-2
  demonstrated PFS HR ~0.44-0.48 vs platinum doublet alone. The combination targets both the
  on-pathway (T790M / C797S resistance mutations) and the bypass-pathway (MET amplification
  — common osimertinib resistance mechanism) by virtue of amivantamab's dual EGFR + MET
  targeting. Pre-treatment biopsy or ctDNA NGS strongly recommended to characterize
  resistance and exclude small-cell transformation (5-15%, requires platinum-etoposide
  instead). Significant toxicity burden: IRR (mitigated by SC formulation), VTE (DOAC
  prophylaxis mandatory first 4 mo), rash, paronychia. Aggressive-track for fit patients
  with funding pathway.



### IND-NSCLC-2L-HER2-MUT-T-DXD
- **Regimen:** REG-T-DXD-NSCLC  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-DESTINYLUNG02-GOTO-2023, SRC-DESTINYLUNG01-LI-2022, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024, SRC-DESTINY-BREAST03-CORTES-2022

**Current KB rationale:**

  Trastuzumab deruxtecan (T-DXd, HER2-targeted ADC with deruxtecan topoisomerase-I payload)
  for HER2-mutant metastatic NSCLC progressing on 1L. HER2 mutations occur in ~2-4% of NSCLC
  adenocarcinoma — distinct from HER2 amplification (rarer in NSCLC, different testing).
  DESTINY-Lung01 (Li 2022): T-DXd 6.4 mg/kg ORR 55%, mPFS 8.2 mo, mOS 17.8 mo. DESTINY-
  Lung02 (Goto 2023): randomized 5.4 vs 6.4 mg/kg → 5.4 mg/kg ORR 49%, mPFS 9.9 mo, mOS 19.5
  mo, with substantially less pneumonitis. 5.4 mg/kg is the label dose. FDA approval 2022.
  Boxed pneumonitis warning ~12% any-grade (3% G≥3, ~1% fatal) — baseline + serial CT chest
  mandatory; LVEF monitoring required. Drug is registered + reimbursed in UA for breast
  indications (DESTINY-Breast03 / -04); NSCLC indication not on НСЗУ formulary — funding via



### IND-NSCLC-2L-KRAS-G12C-ADAGRASIB
- **Regimen:** REG-ADAGRASIB-NSCLC  |  **Line:** 2  |  **Track:** aggressive
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-KRYSTAL1-JANNE-2022, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Adagrasib (KRAS G12C-selective covalent inhibitor with CNS penetration) for KRAS G12C+
  metastatic NSCLC progressing on 1L platinum ± ICI. KRYSTAL-1 phase-2: ORR 43%, mPFS 6.5
  mo, mOS 12.6 mo, intracranial ORR ~33% (active brain mets) — distinguishing CNS profile
  from sotorasib's modest CNS activity. FDA accelerated approval 2022 for 2L+ KRAS G12C+
  NSCLC. KRYSTAL-12 phase-3 vs docetaxel ongoing for full approval. Aggressive-track
  preferred for patients with active brain metastases. AE profile: high GI burden (diarrhea,
  N/V), QTc prolongation, hepatotoxicity, renal impairment — broader monitoring than
  sotorasib.



### IND-NSCLC-2L-KRAS-G12C-SOTORASIB
- **Regimen:** REG-SOTORASIB-KRAS  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-CODEBREAK200-JOHNSON-2023, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Sotorasib (first-in-class covalent KRAS G12C inhibitor) for KRAS G12C+ metastatic NSCLC
  progressing on 1L platinum ± ICI. CodeBreaK 200 phase-3 vs docetaxel: PFS HR 0.66 (5.6 vs
  4.5 mo), ORR 28% vs 13%; OS not significant (HR 1.01) reflecting post-progression therapy
  crossover and biological limits. FDA approval 2021 (accelerated) / 2024 (full) for 2L+
  KRAS G12C+ NSCLC. Adagrasib (KRYSTAL-1) is alternative — preferred for active brain
  metastases (better CNS penetration: intracranial ORR ~33% vs sotorasib's modest CNS
  activity). Hepatotoxicity is the dose-limiting AE; LFTs q-cycle. Co-mutation profile
  (STK11, KEAP1) modulates response — STK11+KRAS G12C predicts poorer ICI response (separate
  consideration for prior 1L).



### IND-NSCLC-2L-MET-AMP-CAPMATINIB
- **Regimen:** REG-CAPMATINIB-NSCLC  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** moderate  |  **Reviewer sign-offs:** []
- **Review status:** ?
- **KB sources cited:** SRC-GEOMETRY-WOLF-2020, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  High-level MET amplification (MET/CEP7 ≥4.0 OR mean GCN ≥10) is a distinct actionable
  subset from MET ex14 skipping in metastatic NSCLC (~1-5% de-novo, plus acquired post-
  osimertinib resistance in EGFR-mutant disease). Capmatinib (selective MET-TKI) showed
  meaningful response in the GEOMETRY mono-1 high-amp cohort (GCN ≥10: ORR ~40%, mPFS ~5.5
  mo). Tepotinib (VISION cohort B) is alternative with similar efficacy. CRITICAL: FDA
  capmatinib label is for MET ex14 skipping NSCLC only — MET-amp use is OFF-LABEL but
  supported by GEOMETRY mono-1 data and NCCN/ESMO 2024-2025 listing as 2A recommendation.
  Low-level amp (GCN 5-9) NOT actionable as monotherapy — must be high-level. Acquired post-
  osimertinib MET-amp: SAVANNAH (osimertinib + savolitinib) ORR ~49% but not FDA-approved;
  alternative is ami



### IND-NSCLC-2L-MET-EX14-CAPMATINIB
- **Regimen:** REG-CAPMATINIB-NSCLC  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** []
- **Review status:** ?
- **KB sources cited:** SRC-GEOMETRY-WOLF-2020, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Capmatinib (selective MET TKI) for MET exon 14 skipping mutation metastatic NSCLC (~3-4%
  of NSCLC adenocarcinoma; enriched in older, sarcomatoid histology). GEOMETRY mono-1:
  pretreated ORR 41%, mPFS 5.4 mo; TKI-naïve ORR 68%, mPFS 12.4 mo. FDA approval 2020 for
  MET ex14 NSCLC any line. CNS activity demonstrated. Tepotinib (VISION) is alternative
  (once-daily oral; comparable efficacy). Detection requires NGS that captures splice-site
  variants — DNA-only hotspot panels miss many MET ex14 events; RNA-NGS preferred.
  Peripheral edema dominant AE (~70%); diuretics + leg elevation usually manageable.



### IND-NSCLC-2L-MET-EX14-TEPOTINIB
- **Regimen:** REG-TEPOTINIB-NSCLC  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** []
- **Review status:** ?
- **KB sources cited:** SRC-VISION-PAIK-2020, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Tepotinib (selective MET TKI, once-daily oral) for MET exon 14 skipping mutation
  metastatic NSCLC. VISION trial: combined ORR 46% (1L 43%, pretreated 48%); mDOR 11.1 mo.
  FDA approval 2021 (now full) for MET ex14 NSCLC any line. Once-daily dosing convenience
  advantage over capmatinib BID. Peripheral edema dominant AE (~70% — class effect);
  proactive management with diuretics + compression. Comparable efficacy to capmatinib;
  choice driven by tolerability nuances and EAP availability in UA.



### IND-NSCLC-2L-NTRK-LAROTRECTINIB
- **Regimen:** REG-LAROTRECTINIB-PANTUMOR  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** []
- **Review status:** ?
- **KB sources cited:** SRC-NAVIGATE-DRILON-2018, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Larotrectinib (highly selective TRK inhibitor) for NTRK1/2/3 fusion-positive metastatic
  NSCLC. NTRK fusion frequency in NSCLC is ~0.2% — extremely rare but actionable. Pooled
  NAVIGATE / SCOUT / phase-1 analysis: ORR 75% (IRC) across 17 tumor types incl. NSCLC
  subset. Tumor-agnostic FDA approval 2018 — the first solid-tumor approval based on
  biomarker irrespective of histology. Best tolerated TRK inhibitor; entrectinib alternative
  (broader spectrum incl. ROS1 / ALK but more CNS-AE); repotrectinib (TRIDENT-1, also
  approved for NTRK 2024) is next-gen for resistance mutations (G595R / G667C). RNA-NGS
  detection mandatory — pan-TRK IHC is reasonable inexpensive screen but NGS confirmation
  required.



### IND-NSCLC-2L-PD-L1-POST-IO-DOCETAXEL
- **Regimen:** REG-DOCETAXEL-RAMUCIRUMAB  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-REVEL-GARON-2014, SRC-LUMELUNG1-RECK-2014, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Docetaxel + ramucirumab for 2L driver-negative metastatic NSCLC after 1L platinum + ICI
  failure (REVEL trial — pre-ICI era but mechanism still applies). Adds modest OS + PFS
  benefit over single-agent docetaxel. In modern post-ICI+chemo failure setting, this
  represents the default cytotoxic 2L for driver-negative disease. Single-agent docetaxel
  (without ramucirumab) is the realistic fallback in Ukraine where ramucirumab not NSZU-
  reimbursed for NSCLC. Nintedanib + docetaxel (LUME-Lung 1) is alternative for
  adenocarcinoma histology. CRITICAL: comprehensive NGS panel must rule out all actionable
  drivers before cytotoxic — driver-positive disease that progressed on 1L (rare given
  driver-positive ≠ ICI 1L) goes to next-line targeted, not docetaxel.



### IND-NSCLC-2L-RET-FUSION-SELPERCATINIB
- **Regimen:** REG-SELPERCATINIB-NSCLC  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-LIBRETTO001-DRILON-2020, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Selpercatinib (highly selective RET TKI) for RET fusion-positive metastatic NSCLC (~1-2%
  of NSCLC adenocarcinoma). LIBRETTO-001 NSCLC cohorts: pretreated ORR 64% (mPFS 16.5 mo);
  TKI-naïve ORR 85%; intracranial ORR 91% (measurable brain mets). FDA approval 2020 for
  RET-fusion+ NSCLC any line. LIBRETTO-431 phase-3 vs platinum± pembrolizumab confirmed 1L
  superiority (PFS HR 0.46). Pralsetinib (ARROW) is alternative — comparable efficacy,
  slightly different AE profile (more hematologic). Hypertension (~40%) and hepatotoxicity
  are dose-limiting AEs requiring proactive management. RNA-NGS detection mandatory — DNA-
  only panels often miss RET fusions.



### IND-NSCLC-2L-ROS1-POST-CRIZ-ENTRECTINIB
- **Regimen:** REG-ENTRECTINIB-NSCLC  |  **Line:** 2  |  **Track:** standard
- **Evidence level:** high  |  **Reviewer sign-offs:** 0
- **Review status:** ?
- **KB sources cited:** SRC-STARTRK2-DRILON-2020, SRC-NCCN-NSCLC-2025, SRC-ESMO-NSCLC-METASTATIC-2024

**Current KB rationale:**

  Entrectinib (ROS1 / NTRK / ALK TKI with CNS penetration) for ROS1+ metastatic NSCLC
  progressing on crizotinib 1L. Crizotinib has poor CNS penetration; CNS progression is a
  common failure mode and entrectinib's high intracranial activity (~55% intracranial ORR in
  STARTRK-2 integrated analysis) makes it preferred in CNS-positive disease. For systemic-
  only progression or G2032R solvent-front resistance, repotrectinib (TRIDENT-1, separate
  Indication) may be preferred. Lorlatinib also has ROS1 activity but is less specifically
  studied for ROS1 2L. Pre-treatment NGS recommended to characterize resistance mutations
  driving precise next-line choice.



*(… 21 more indications not shown)*

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