# BMA combinatorial coverage extraction — 2026-04-27

**Authoring agent:** Claude Code (extraction only; per CHARTER §8.3, LLM is
NOT the clinical decision-maker)
**Drafted by tag:** `claude_extraction`
**Review status (every draft):** `pending_clinical_signoff`
**Two clinical co-leads must adjudicate before any of these go live**

This document records BMA cells drafted in this round, cells skipped because
no in-repo source documents the actionability, and cells where in-repo
sources show evidence-based disagreement that should NOT be resolved by an
LLM.

---

## 1. Drafts created (23)

All drafts:
- cite ≥1 in-repo `SRC-*` Source entity
- copy regulatory approvals from FDA / EMA labels (text only — no
  invented wording)
- carry the existing schema's required ESCAT and OncoKB level fields
  (snapshot version `v3.20-2026-04`)
- are marked `review_status: pending_clinical_signoff` and
  `drafted_by: claude_extraction`
- list `last_verified: "2026-04-27"`

Per the prompt, fusions and ITDs were excluded (Phase 7 / agent B3 owns
those on the BIO side). Drafts intentionally focused on hotspot mutations,
status-flag biomarkers (HRD, IGHV, MGMT methylation, IHC) where actionability
is established by an in-repo NCCN/ESMO source.

| BMA id | Biomarker | Disease | ESCAT | OncoKB | Primary in-repo sources |
|---|---|---|---|---|---|
| BMA-JAK2-V617F-PV | BIO-JAK2 | DIS-PV | IA | 1 | NCCN-MPN-2025, ESMO-MPN-2015, RESPONSE-VANNUCCHI-2015, PROUD-PV-GISSLINGER-2020, ONCOKB |
| BMA-JAK2-V617F-ET | BIO-JAK2 | DIS-ET | IA | 1 | NCCN-MPN-2025, ESMO-MPN-2015, PT1-HARRISON-2005, ONCOKB |
| BMA-JAK2-V617F-PMF | BIO-JAK2 | DIS-PMF | IA | 1 | NCCN-MPN-2025, ESMO-MPN-2015, COMFORT-I-VERSTOVSEK-2012, JAKARTA2-HARRISON-2017, MOMENTUM-VERSTOVSEK-2023, DIPSS-PLUS-GANGAT-2011, ONCOKB |
| BMA-CALR-ET | BIO-CALR | DIS-ET | IA | 1 | NCCN-MPN-2025, ESMO-MPN-2015, PT1-HARRISON-2005, ONCOKB |
| BMA-CALR-PMF | BIO-CALR | DIS-PMF | IA | 1 | NCCN-MPN-2025, ESMO-MPN-2015, COMFORT-I-VERSTOVSEK-2012, JAKARTA2-HARRISON-2017, MOMENTUM-VERSTOVSEK-2023, DIPSS-PLUS-GANGAT-2011, ONCOKB |
| BMA-NPM1-AML | BIO-NPM1 | DIS-AML | IA | 1 | ELN-AML-2022, NCCN-AML-2025, ESMO-AML-2020, QUAZAR-WEI-2020, VIALE-A-DINARDO-2020, ONCOKB |
| BMA-BRAF-V600E-THYROID-ANAPLASTIC | BIO-BRAF-V600E | DIS-THYROID-ANAPLASTIC | IA | 1 | NCCN-THYROID-2025, ONCOKB |
| BMA-BRAF-V600E-CHOLANGIO | BIO-BRAF-V600E | DIS-CHOLANGIOCARCINOMA | IA | 1 | NCCN-HEPATOBILIARY, ONCOKB |
| BMA-IDH1-R132-CHOLANGIO | BIO-IDH-MUTATION | DIS-CHOLANGIOCARCINOMA | IA | 1 | NCCN-HEPATOBILIARY, ONCOKB |
| BMA-HER2-AMP-GASTRIC | BIO-HER2-SOLID | DIS-GASTRIC | IA | 1 | NCCN-GASTRIC-2025, ESMO-GASTRIC-2024, ONCOKB |
| BMA-HER2-AMP-CRC | BIO-HER2-SOLID | DIS-CRC | IB | 2 | NCCN-COLON-2025, ESMO-COLON-2024, ONCOKB |
| BMA-HER2-AMP-ESOPHAGEAL | BIO-HER2-SOLID | DIS-ESOPHAGEAL | IA | 1 | NCCN-ESOPHAGEAL-2025, ESMO-ESOPHAGEAL-2024, ONCOKB |
| BMA-MGMT-METHYLATION-GBM | BIO-MGMT-METHYLATION | DIS-GBM | IA | 2 | NCCN-CNS-2025, EANO-GBM-2024, ONCOKB |
| BMA-HRD-STATUS-OVARIAN | BIO-HRD-STATUS | DIS-OVARIAN | IA | 1 | NCCN-OVARIAN-2025, ESMO-OVARIAN-2024, ONCOKB |
| BMA-HRD-STATUS-PROSTATE | BIO-HRD-STATUS | DIS-PROSTATE | IA | 1 | NCCN-PROSTATE-2025, ESMO-PROSTATE-2024, EAU-PROSTATE-2024, ONCOKB |
| BMA-HRD-STATUS-BREAST | BIO-HRD-STATUS | DIS-BREAST | IA | 1 | NCCN-BREAST-2025, ESMO-BREAST-EARLY-2024, ESMO-BREAST-METASTATIC-2024, ONCOKB |
| BMA-HRD-STATUS-PDAC | BIO-HRD-STATUS | DIS-PDAC | IA | 1 | NCCN-PANCREATIC-2025, ESMO-PANCREATIC-2024, ONCOKB |
| BMA-CD30-CHL | BIO-CD30-IHC | DIS-CHL | IA | 1 | NCCN-BCELL-2025, ESMO-HODGKIN-2024, ONCOKB |
| BMA-CD30-ALCL | BIO-CD30-IHC | DIS-ALCL | IA | 1 | NCCN-BCELL-2025, ESMO-PTCL-2024, ONCOKB |
| BMA-CXCR4-WHIM-WM | BIO-CXCR4-WHIM | DIS-WM | IB | 3A | NCCN-BCELL-2025, ESMO-WM-2024, ONCOKB |
| BMA-EZH2-Y641-FL | BIO-EZH2-Y641 | DIS-FL | IB | 1 | NCCN-BCELL-2025, ESMO-FL-2024, ONCOKB |
| BMA-IGHV-UNMUTATED-CLL | BIO-IGHV-MUTATIONAL-STATUS | DIS-CLL | IA | 2 | NCCN-BCELL-2025, ESMO-CLL-2024, MOZ-UA-CLL-2022, ONCOKB |
| BMA-ESR1-MUT-BREAST | BIO-ESR1 | DIS-BREAST | IB | 1 | NCCN-BREAST-2025, ESMO-BREAST-METASTATIC-2024, ONCOKB |

### Coverage delta

- Biomarkers gaining BMA coverage in this round: 11
  (BIO-JAK2, BIO-CALR, BIO-NPM1, BIO-HER2-SOLID, BIO-MGMT-METHYLATION,
  BIO-HRD-STATUS, BIO-CD30-IHC, BIO-CXCR4-WHIM, BIO-EZH2-Y641,
  BIO-IGHV-MUTATIONAL-STATUS, BIO-ESR1)
- Existing biomarkers gaining new disease cells in this round: 2
  (BIO-BRAF-V600E × THYROID-ANAPLASTIC + CHOLANGIO; BIO-IDH-MUTATION ×
  CHOLANGIO)
- Diseases gaining first-ever BMA coverage in this round: 5
  (DIS-PV, DIS-ET, DIS-PMF, DIS-CHL, DIS-THYROID-ANAPLASTIC)

---

## 2. Documented evidence-based disagreements (do NOT resolve without
clinical co-leads)

The drafts call out three places where in-repo NCCN vs ESMO (or NCCN vs EANO,
or NCCN vs EAU) take different positions. These are flagged inside the YAML
`notes:` block and re-listed here so co-lead reviewers can see them quickly.

| Cell | Disagreement | Sources in conflict |
|---|---|---|
| BMA-MGMT-METHYLATION-GBM | NCCN does not withhold TMZ from MGMT-unmethylated GBM; EANO 2024 lists RT-alone as acceptable for unmethylated elderly — different intensity threshold for the same biomarker class. | SRC-NCCN-CNS-2025 vs SRC-EANO-GBM-2024 |
| BMA-HRD-STATUS-OVARIAN | NCCN lists niraparib maintenance for HRD-negative all-comers; ESMO-Ovarian-2024 explicitly de-prioritizes PARP-i in HRD-negative platinum-sensitive recurrence. | SRC-NCCN-OVARIAN-2025 vs SRC-ESMO-OVARIAN-2024 |
| BMA-HRD-STATUS-PROSTATE | EAU-Prostate-2024 is more conservative on non-BRCA HRR PARP-i indications than NCCN. | SRC-EAU-PROSTATE-2024 vs SRC-NCCN-PROSTATE-2025 |

Per CLINICAL_CONTENT_STANDARDS §1.2 and §5.3, these are NOT to be resolved
by the drafting agent; both positions are kept verbatim in the cell.

---

## 3. Cells deliberately NOT drafted in this round

### 3.1. Biomarker entities that are non-actionable / informational only

Skipped because the in-repo BIO-* entity itself flags non-actionability
(`oncokb_skip_reason: ihc_no_variant`, `tumor_agnostic`, `fusion_mvp`, etc.)
and no in-repo NCCN/ESMO source ties the biomarker to a treatment selection.

| Biomarker | Reason for skip |
|---|---|
| BIO-AFP, BIO-PSA, BIO-PSMA-PET, BIO-GLEASON-ISUP | Disease-monitoring / staging biomarkers — not treatment-selection per BIO-* notes |
| BIO-DLBCL-IPI, BIO-FL-FLIPI, BIO-MCL-MIPI | Risk scores; not biomarker-actionability cells |
| BIO-DLBCL-COO-HANS | COO is a stratifier; no FDA-approved COO-targeted regimen in repo sources |
| BIO-CD20-IHC, BIO-CD5-IHC, BIO-CD23-IHC, BIO-CD52-IHC, BIO-CD79B-IHC | Phenotype confirmation; rituximab/anti-CD20 is universal in B-NHL — not a per-cell BMA pattern |
| BIO-ESTROGEN-RECEPTOR, BIO-PROGESTERONE-RECEPTOR | Standard endocrine-therapy gatekeepers, but BMA-style pairing not used in repo (managed via Indication, not BMA) |
| BIO-KI67-PROLIFERATION-INDEX | Proliferation index, not a target |
| BIO-HBV-STATUS, BIO-HCV-STATUS, BIO-HCV-RNA, BIO-HIV-STATUS, BIO-HPV-STATUS, BIO-HTLV-1, BIO-EBV-STATUS, BIO-EBV-DNA | Infectious-disease / co-morbidity flags, not actionability cells (managed via Indication / RedFlag) |
| BIO-VHL-STATUS | Belzutifan in VHL syndrome is highly contextual; insufficient sources in repo |
| BIO-HRAS, BIO-AKT1, BIO-CDKN2A, BIO-PTEN, BIO-SF3B1 | Actionable in select tumors (HNSCC, breast, etc.) but no in-repo SRC-* clearly documents — flagged as **blocked-on-source** below |
| BIO-PDL1-CPS, BIO-PDL1-EXPRESSION, BIO-PDL1-TPS | PD-L1 is a per-tumor companion-diagnostic for many ICIs; cells could be drafted but each requires careful per-tumor cutoff extraction. Deferred to a dedicated PD-L1 phase. |
| BIO-MSI-STATUS | Largely overlaps BIO-DMMR-IHC actionability cells already covered. Drafting per-tumor MSI-STATUS cells would mostly duplicate existing DMMR cells. Deferred until clinical co-leads decide the canonical biomarker for MSI-H actionability. |
| BIO-TMB-HIGH | Tumor-agnostic FDA approval; per-tumor cells need careful extraction of cutoff per disease (KEYNOTE-158). Deferred. |
| BIO-RHOA-G17V | "Informational, not algorithm-driving" per the BIO-* notes. |
| BIO-MM-CYTOGENETICS-HR | Composite biomarker that includes translocations — fusions are out of scope per prompt. |
| BIO-FLT3-D835 (× R/R AML expansions), BIO-FLT3-ITD (× more diseases) | Existing coverage adequate; further expansion is fusion/ITD-adjacent and deferred to Phase 7 per prompt. |

### 3.2. Cells with clear actionability but blocked on missing in-repo source

These are cells where a clinically-canonical FDA-approved biomarker-targeted
regimen exists, but no in-repo `SRC-*` Source entity explicitly documents the
indication. Drafting them would require inventing source attribution, which
the prompt forbids. They are listed as "ingest source XYZ" follow-ups for
the source-ingestion roadmap.

| Cell | Standard regimen | Source(s) needed |
|---|---|---|
| BIO-HRAS × DIS-HNSCC | tipifarnib (FDA orphan, not approved) | NCCN-HNSCC-2025 already in repo, but no language extracted; need verbatim ingestion before drafting |
| BIO-AKT1 (E17K) × DIS-BREAST | capivasertib + fulvestrant (CAPItello-291) | SRC-CAPITELLO-291 / NCCN-BREAST-2025 phrasing — need section extraction |
| BIO-FGFR2 × DIS-CHOLANGIOCARCINOMA (mutation, distinct from existing fusion BMA) | not a primary actionability call; resistance context | Trial source SRC-FOENIX-CCA2-MUTATION-COHORT not in repo |
| BIO-IDH-MUTATION × DIS-GLIOMA-LOW-GRADE | vorasidenib (INDIGO Lancet 2023; FDA approved 2024) | SRC-INDIGO-MELLINGHOFF-2023, SRC-NCCN-CNS-2025 explicit IDH section |
| BIO-PIK3CA × DIS-HNSCC, × DIS-CERVICAL (alpelisib repurposing) | not yet FDA approved beyond breast | SRC-NCCN-HNSCC-2025 / SRC-NCCN-CERVICAL-2025 explicit text needed |
| BIO-MET × DIS-PDAC, × DIS-CRC | crizotinib / capmatinib in MET-amplified rare cohorts | Trial sources SRC-PROFILE-1001 not in repo |
| BIO-KIT × DIS-THYMOMA, × thymic carcinoma | imatinib in KIT-mutant thymic | No DIS-THYMUS / no THYMIC source in repo |
| BIO-HER2-SOLID × DIS-CERVICAL, × DIS-ENDOMETRIAL, × DIS-OVARIAN | tumor-agnostic T-DXd 2024 approval | NCCN per-disease text not yet extracted explicitly for HER2 |
| BIO-NPM1 × menin-inhibitor R/R AML | revumenib FDA approval 2024 (KMT2A-rearranged AML); NPM1 indication pending | SRC-AUGMENT-101 / SRC-FDA-REVUMENIB not in repo |
| BIO-EZH2-Y641 × DIS-DLBCL-NOS | no FDA approval; combination trials ongoing | not actionable yet |
| BIO-MGMT-METHYLATION × DIS-GLIOMA-LOW-GRADE | predictive in some grade III subgroups | SRC-CATNON / dedicated source |
| Pan-tumor BIO-TMB-HIGH × NSCLC, × CRC, × ENDOMETRIAL, etc. | pembrolizumab tumor-agnostic per KEYNOTE-158 | SRC-KEYNOTE-158, SRC-FDA-PEMBROLIZUMAB-TMB not in repo |
| BIO-MSI-STATUS × pan-tumor | pembrolizumab tumor-agnostic | Use SRC-KEYNOTE-158 / SRC-KEYNOTE-177 once ingested; until then DMMR-IHC cells stand in. |
| BIO-FGFR3 × DIS-NSCLC squamous, × DIS-RCC | erdafitinib selectable; FDA approval is urothelial-only currently | Need SRC-FGFR-CHRONIC-PAN-TUMOR-EXTENSION |

These are high-priority for the source-ingestion sprint. Best yield will come
from ingesting:
1. SRC-NCCN-HEPATOBILIARY (currently STUB) — full table
2. SRC-NCCN-MPN-2025 (currently STUB)
3. ROAR / COMBI / COLUMBUS BRAF trial sources
4. SOLO-1 / PAOLA-1 / PRIMA / PROfound / MAGNITUDE / PROpel / TALAPRO-2 PARP trials
5. ECHELON-1 / ECHELON-2 / AETHERA brentuximab trials
6. KEYNOTE-158 / KEYNOTE-177 ICI tumor-agnostic trials
7. EMERALD elacestrant trial
8. ToGA / KEYNOTE-811 / DESTINY-Gastric01 HER2 gastric trials
9. INDIGO vorasidenib (would unblock BIO-IDH × glioma-low-grade)

### 3.3. Diseases still without ANY BMA after this round

After this round (5 new diseases gained first BMA), these diseases remain
without any BMA:

`DIS-APL`, `DIS-ATLL`, `DIS-CHONDROSARCOMA`, `DIS-EATL`, `DIS-GLIOMA-LOW-GRADE`,
`DIS-HNSCC`, `DIS-HSTCL`, `DIS-IMT`, `DIS-MF-SEZARY`, `DIS-MPNST`,
`DIS-NK-T-NASAL`, `DIS-PMBCL`, `DIS-PTCL-NOS`, `DIS-T-PLL`

Notes on these:
- `DIS-APL` — PML-RARA defines the disease; there is no `BIO-PML-RARA`
  entity (treated via diagnostic Indication / Algorithm path). Drafting a
  BMA would require a new BIO-* — out of scope here.
- `DIS-IMT` — ALK fusion is the actionable feature; fusion-side coverage
  blocked by Phase 7 fusions exclusion.
- `DIS-CHONDROSARCOMA` — IDH1/2 mutation is actionable (ivosidenib
  AGILE-extension cohorts), but no in-repo NCCN-SARCOMA / ESMO-SARCOMA
  source exists.
- `DIS-MF-SEZARY` — HDAC inhibitors / mogamulizumab are CCR4-driven; a
  BIO-CCR4 entity would be needed.
- `DIS-NK-T-NASAL` — EBV-driven, mostly histology + Ann Arbor staging
  rather than actionable somatic markers; no per-tumor BMA cell justified
  in MVP.

---

## 4. Validator status

```
$ py -3.12 -m knowledge_base.validation.loader knowledge_base/hosted/content
Loaded 1910 entities.
  biomarker_actionability: 399  (was 376; +23 from this round)
  ...
OK — all entities valid, all references resolve.
```

Schema-error / contract-warning baseline pre-existed this round (3 schema
errors in `indications/` and 3 RedFlag draft warnings) and is unchanged by
this work. No new errors introduced by the 23 BMA drafts.

---

## 5. Reviewer checklist (per CLINICAL_CONTENT_STANDARDS §6.2)

Two clinical co-leads (per CHARTER §6.1) are required to adjudicate before
these can become live KB content. Quick checklist for each draft:

- [ ] Does `evidence_summary` accurately paraphrase the cited source?
- [ ] Are FDA / EMA approval years and indications correctly stated?
- [ ] Is `escat_tier` defensible against ESCAT v2 (Mateo 2018, updates)?
- [ ] Is `oncokb_level` consistent with the OncoKB snapshot v3.20-2026-04?
- [ ] Are `recommended_combinations` literally present in cited NCCN/ESMO
      tables (not LLM-generated)?
- [ ] Are `contraindicated_monotherapy` flags mechanism-level, not
      generated from training-data priors?
- [ ] For the 3 disagreements flagged in §2, is the resolution language in
      `notes:` honest (does NOT pick a winner)?

Adjudication recorded by changing `review_status` from
`pending_clinical_signoff` to `signed_off_2reviewer` plus `reviewers: [...]`
once two co-leads have agreed.
