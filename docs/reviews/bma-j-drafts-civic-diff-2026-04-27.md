# J-agent BMA drafts vs CIViC side-by-side diff — 2026-04-27

**Mode:** read-only audit (Phase 3-O). No YAML edits. Single output: this file.
**Branch:** `feat/civic-primary` at `e31ebd1` (Phase 3-N — BMA evidence reconstruction via CIViC) or descendant.
**Inputs:**
- 23 BMAs marked `drafted_by: claude_extraction` under `knowledge_base/hosted/content/biomarker_actionability/`
- CIViC snapshot `knowledge_base/hosted/civic/2026-04-25/evidence.yaml` (4,842 evidence items, CC0-1.0)
- `SnapshotCIViCClient` (`knowledge_base/engine/snapshot_civic_client.py`) — fusion-aware lookup via `civic_variant_matcher`
- Cross-referenced: [`docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`](./oncokb-public-civic-coverage-2026-04-27.md)

---

## 1. Executive summary

**Total J-drafts found:** 23 (matches the prior audit's 23).

**Categorization:**

| Category | Count | Notes |
|---|---:|---|
| CONFIRMED-WITH-DRUGS | 4 | Promote to merged after clinical re-read of drug list. |
| CONFIRMED-LEVEL-ONLY | 1 | Level alignment but CIViC drugs differ from BMA recs — review needed. |
| DOWNGRADE | 0 | Legacy 1/2 not supportable from CIViC (only C/D). |
| CONTRADICTED | 0 | CIViC has resistance evidence for a recommended drug with no offsetting support. |
| NO-EVIDENCE | 2 | actionability_lookup present, but CIViC has no therapeutic-option hit on the (gene, variant). |
| NO-LOOKUP | 16 | Biomarker has `skip_reason` or no `actionability_lookup` (IHC / methylation / composite / multi-allele). |
| **Total** | **23** | |

**CIViC-confirmable at variant level (any kind):** 5 of 23.

### Comparison with prior audit's 6-of-23 prediction

The 2026-04-27 OncoKB-public + CIViC coverage audit at §5 enumerated **6 BMAs** as 'CIViC-confirmed at variant level + therapies':

| BMA in prior audit | This audit's category |
|---|---|
| BMA-BRAF-V600E-CHOLANGIO | CONFIRMED-WITH-DRUGS |
| BMA-BRAF-V600E-THYROID-ANAPLASTIC | CONFIRMED-WITH-DRUGS |
| BMA-JAK2-V617F-ET | CONFIRMED-LEVEL-ONLY |
| BMA-JAK2-V617F-PMF | CONFIRMED-WITH-DRUGS |
| BMA-JAK2-V617F-PV | CONFIRMED-WITH-DRUGS |
| BMA-NPM1-AML | **NO-EVIDENCE** (variant-case mismatch — see §5) |

This audit confirms **5 of 6** prior predictions. The disagreement is BMA-NPM1-AML: the prior audit counted 3 NPM1 W288fs items (B:1, D:1, E:1) with 2 having therapies. This audit's `SnapshotCIViCClient.lookup` returns 0 therapeutic options for `(NPM1, W288fs)`. **Root cause:** `civic_variant_matcher.matches_civic_entry` Rule 1 does a case-sensitive `==` between the query variant (`W288fs`, mixed-case from `actionability_lookup`) and the CIViC variant string (`W288FS`, uppercase). The fusion-component path tolerates case (Rule 2), and the descriptor path tokenizes case-insensitively, but Rule 1 does not. **This is a genuine matcher bug, not a CIViC gap** — the prior audit found the items via case-insensitive lookup. See §6.1.

### Phase 3-N (commit e31ebd1) coverage of these J-drafts

- **5 of 23** J-drafts received fresh `SRC-CIVIC` evidence_sources entries from Phase 3-N reconstruction.
- **18 of 23** still carry only the legacy `SRC-ONCOKB` entry. Of these, all are in NO-LOOKUP / NO-EVIDENCE — Phase 3-N correctly skipped them because their CIViC lookup returned no therapeutic options.
- Phase 4 render rule (skip evidence_sources entries with source=SRC-ONCOKB) means **the 18 J-drafts without a Phase-3-N SRC-CIVIC entry will surface zero evidence** in the rendered HCP layer once the render pivots. They need either guideline citations (NCCN/ESMO directly) or matcher fixes to unblock CIViC coverage.

---

## 2. Per-draft table

Drug-overlap column shows `<n supportive> sup / <n resistance> res` — count of drugs in `recommended_combinations` that appear in CIViC supportive vs resistance evidence respectively.

| BMA-ID | biomarker | (gene, variant) | legacy SRC-ONCOKB level | CIViC levels found | drug overlap | category | recommended action | Phase-3-N added SRC-CIVIC? |
|---|---|---|---|---|---|---|---|---|
| BMA-BRAF-V600E-CHOLANGIO | BIO-BRAF-V600E | (BRAF, V600E) | 1 | A:5, B:40, C:16, D:12 | 2 sup / 2 res | CONFIRMED-WITH-DRUGS | PROMOTE | yes (14) |
| BMA-BRAF-V600E-THYROID-ANAPLASTIC | BIO-BRAF-V600E | (BRAF, V600E) | 1 | A:5, B:40, C:16, D:12 | 2 sup / 2 res | CONFIRMED-WITH-DRUGS | PROMOTE | yes (14) |
| BMA-JAK2-V617F-PMF | BIO-JAK2 | (JAK2, V617F) | 1 | B:1, D:1 | 1 sup / 0 res | CONFIRMED-WITH-DRUGS | PROMOTE | yes (4) |
| BMA-JAK2-V617F-PV | BIO-JAK2 | (JAK2, V617F) | 1 | B:1, D:1 | 1 sup / 0 res | CONFIRMED-WITH-DRUGS | PROMOTE | yes (4) |
| BMA-JAK2-V617F-ET | BIO-JAK2 | (JAK2, V617F) | 1 | B:1, D:1 | 0 sup / 0 res | CONFIRMED-LEVEL-ONLY | PROMOTE w/ drug-set review | yes (4) |
| BMA-EZH2-Y641-FL | BIO-EZH2-Y641 | (EZH2, Y641N) | 1 | — | 0 sup / 0 res | NO-EVIDENCE | ARCHIVE / re-extract from real source | no (0) |
| BMA-NPM1-AML | BIO-NPM1 | (NPM1, W288fs) | 1 | — | 0 sup / 0 res | NO-EVIDENCE | ARCHIVE / re-extract from real source | no (0) |
| BMA-CALR-ET | BIO-CALR | — (no lookup) | 1 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-CALR-PMF | BIO-CALR | — (no lookup) | 1 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-CD30-ALCL | BIO-CD30-IHC | — (no lookup) | 1 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-CD30-CHL | BIO-CD30-IHC | — (no lookup) | 1 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-CXCR4-WHIM-WM | BIO-CXCR4-WHIM | — (no lookup) | 3A | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-ESR1-MUT-BREAST | BIO-ESR1 | — (no lookup) | 1 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-HER2-AMP-CRC | BIO-HER2-SOLID | — (no lookup) | 2 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-HER2-AMP-ESOPHAGEAL | BIO-HER2-SOLID | — (no lookup) | 1 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-HER2-AMP-GASTRIC | BIO-HER2-SOLID | — (no lookup) | 1 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-HRD-STATUS-BREAST | BIO-HRD-STATUS | — (no lookup) | 1 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-HRD-STATUS-OVARIAN | BIO-HRD-STATUS | — (no lookup) | 1 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-HRD-STATUS-PDAC | BIO-HRD-STATUS | — (no lookup) | 1 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-HRD-STATUS-PROSTATE | BIO-HRD-STATUS | — (no lookup) | 1 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-IDH1-R132-CHOLANGIO | BIO-IDH-MUTATION | — (no lookup) | 1 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-IGHV-UNMUTATED-CLL | BIO-IGHV-MUTATIONAL-STATUS | — (no lookup) | 2 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |
| BMA-MGMT-METHYLATION-GBM | BIO-MGMT-METHYLATION | — (no lookup) | 2 | — | 0 sup / 0 res | NO-LOOKUP | Cite NCCN/ESMO directly (out of CIViC scope) | no (0) |

---

## 3. Detailed analysis by category

### 3.1 CONFIRMED-WITH-DRUGS — 4 BMA(s)

_CIViC has options at compatible level (A/B for legacy 1/2; C for 3A/3B; D for 4) AND drug overlap with recommended_combinations._

#### BMA-BRAF-V600E-CHOLANGIO  (`bma_braf_v600e_cholangio.yaml`)

- **biomarker:** `BIO-BRAF-V600E` — type `gene_mutation`
- **disease:** `DIS-CHOLANGIOCARCINOMA`
- **ESCAT tier:** IA
- **actionability_lookup:** gene=`BRAF`, variant=`V600E`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-HEPATOBILIARY, SRC-ONCOKB
- **recommended_combinations:**
  - dabrafenib + trametinib (2L+ BRAF V600E cholangio per SRC-NCCN-HEPATOBILIARY)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 73
  - levels: A:5, B:40, C:16, D:12
  - all drugs surfaced: Trametinib, Mirdametinib, Panitumumab, Sorafenib, Dabrafenib, Pictilisib Bismesylate, PLX4720, Nutlin-3 (+18)
  - supportive drugs: Panitumumab, Sorafenib, Trametinib, Dabrafenib, Pictilisib Bismesylate, PLX4720, Nutlin-3, Capecitabine (+14)
  - resistance/Does-Not-Support drugs: Trametinib, Mirdametinib, Cetuximab, Panitumumab, MEK Inhibitor RO4987655, Vemurafenib, Dabrafenib, Oxaliplatin (+4)
  - top options (level-ranked, up to 3):
    - **A** | Predictive — Supports — Sensitivity/Response (Combination) → Dabrafenib, Trametinib
    - **A** | Predictive — Supports — Sensitivity/Response (Combination) → Cetuximab, Encorafenib
    - **A** | Predictive — Supports — Sensitivity/Response (Combination) → Trametinib, Dabrafenib
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: Trametinib, Dabrafenib
  - resistance matches: Trametinib, Dabrafenib
- **Phase-3-N added SRC-CIVIC?** yes — 14 SRC-CIVIC entries

#### BMA-BRAF-V600E-THYROID-ANAPLASTIC  (`bma_braf_v600e_thyroid_anaplastic.yaml`)

- **biomarker:** `BIO-BRAF-V600E` — type `gene_mutation`
- **disease:** `DIS-THYROID-ANAPLASTIC`
- **ESCAT tier:** IA
- **actionability_lookup:** gene=`BRAF`, variant=`V600E`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-THYROID-2025, SRC-ONCOKB
- **recommended_combinations:**
  - dabrafenib + trametinib (1L V600E ATC per SRC-NCCN-THYROID-2025)
  - neoadjuvant dabrafenib + trametinib → surgery → adjuvant systemic ± RT (initially unresectable, per SRC-NCCN-THYROID-2025)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 73
  - levels: A:5, B:40, C:16, D:12
  - all drugs surfaced: Trametinib, Mirdametinib, Panitumumab, Sorafenib, Dabrafenib, Pictilisib Bismesylate, PLX4720, Nutlin-3 (+18)
  - supportive drugs: Panitumumab, Sorafenib, Trametinib, Dabrafenib, Pictilisib Bismesylate, PLX4720, Nutlin-3, Capecitabine (+14)
  - resistance/Does-Not-Support drugs: Trametinib, Mirdametinib, Cetuximab, Panitumumab, MEK Inhibitor RO4987655, Vemurafenib, Dabrafenib, Oxaliplatin (+4)
  - top options (level-ranked, up to 3):
    - **A** | Predictive — Supports — Sensitivity/Response (Combination) → Dabrafenib, Trametinib
    - **A** | Predictive — Supports — Sensitivity/Response (Combination) → Cetuximab, Encorafenib
    - **A** | Predictive — Supports — Sensitivity/Response (Combination) → Trametinib, Dabrafenib
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: Trametinib, Dabrafenib
  - resistance matches: Trametinib, Dabrafenib
- **Phase-3-N added SRC-CIVIC?** yes — 14 SRC-CIVIC entries

#### BMA-JAK2-V617F-PMF  (`bma_jak2_v617f_pmf.yaml`)

- **biomarker:** `BIO-JAK2` — type `gene_mutation`
- **disease:** `DIS-PMF`
- **ESCAT tier:** IA
- **actionability_lookup:** gene=`JAK2`, variant=`V617F`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015, SRC-COMFORT-I-VERSTOVSEK-2012, SRC-JAKARTA2-HARRISON-2017, SRC-MOMENTUM-VERSTOVSEK-2023, SRC-DIPSS-PLUS-GANGAT-2011, SRC-ONCOKB
- **recommended_combinations:**
  - ruxolitinib monotherapy (intermediate-2 / high-risk per SRC-COMFORT-I-VERSTOVSEK-2012, SRC-NCCN-MPN-2025)
  - fedratinib monotherapy (post-ruxolitinib failure per SRC-JAKARTA2-HARRISON-2017)
  - momelotinib monotherapy (MF + anemia per SRC-MOMENTUM-VERSTOVSEK-2023)
  - allogeneic HCT (transplant-eligible higher-risk per SRC-NCCN-MPN-2025, SRC-DIPSS-PLUS-GANGAT-2011)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 2
  - levels: B:1, D:1
  - all drugs surfaced: Peginterferon Alfa-2b, Fedratinib
  - supportive drugs: Peginterferon Alfa-2b, Fedratinib
  - top options (level-ranked, up to 3):
    - **B** | Predictive — Supports — Sensitivity/Response → Peginterferon Alfa-2b
    - **D** | Predictive — Supports — Sensitivity/Response → Fedratinib
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: Fedratinib
- **Phase-3-N added SRC-CIVIC?** yes — 4 SRC-CIVIC entries

#### BMA-JAK2-V617F-PV  (`bma_jak2_v617f_pv.yaml`)

- **biomarker:** `BIO-JAK2` — type `gene_mutation`
- **disease:** `DIS-PV`
- **ESCAT tier:** IA
- **actionability_lookup:** gene=`JAK2`, variant=`V617F`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015, SRC-RESPONSE-VANNUCCHI-2015, SRC-PROUD-PV-GISSLINGER-2020, SRC-ONCOKB
- **recommended_combinations:**
  - phlebotomy + low-dose aspirin (low-risk PV per SRC-NCCN-MPN-2025)
  - hydroxyurea (high-risk 1L cytoreduction per SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015)
  - ropeginterferon alfa-2b (high-risk; preferred for younger patients per SRC-PROUD-PV-GISSLINGER-2020)
  - ruxolitinib (post-hydroxyurea resistance/intolerance per SRC-RESPONSE-VANNUCCHI-2015)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 2
  - levels: B:1, D:1
  - all drugs surfaced: Peginterferon Alfa-2b, Fedratinib
  - supportive drugs: Peginterferon Alfa-2b, Fedratinib
  - top options (level-ranked, up to 3):
    - **B** | Predictive — Supports — Sensitivity/Response → Peginterferon Alfa-2b
    - **D** | Predictive — Supports — Sensitivity/Response → Fedratinib
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: Peginterferon Alfa-2b
- **Phase-3-N added SRC-CIVIC?** yes — 4 SRC-CIVIC entries

### 3.2 CONFIRMED-LEVEL-ONLY — 1 BMA(s)

_CIViC level matches but no drug overlap with recommended_combinations (CIViC therapies differ from BMA recommendations)._

#### BMA-JAK2-V617F-ET  (`bma_jak2_v617f_et.yaml`)

- **biomarker:** `BIO-JAK2` — type `gene_mutation`
- **disease:** `DIS-ET`
- **ESCAT tier:** IA
- **actionability_lookup:** gene=`JAK2`, variant=`V617F`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015, SRC-PT1-HARRISON-2005, SRC-ONCOKB
- **recommended_combinations:**
  - low-dose aspirin (low-risk per SRC-NCCN-MPN-2025)
  - hydroxyurea + aspirin (high-risk 1L per SRC-PT1-HARRISON-2005)
  - interferon-alpha (preferred for younger high-risk per SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015)
  - anagrelide (HU-resistant/intolerant 2L)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 2
  - levels: B:1, D:1
  - all drugs surfaced: Peginterferon Alfa-2b, Fedratinib
  - supportive drugs: Peginterferon Alfa-2b, Fedratinib
  - top options (level-ranked, up to 3):
    - **B** | Predictive — Supports — Sensitivity/Response → Peginterferon Alfa-2b
    - **D** | Predictive — Supports — Sensitivity/Response → Fedratinib
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** yes — 4 SRC-CIVIC entries

### 3.5 NO-EVIDENCE — 2 BMA(s)

_Biomarker has actionability_lookup, but the CIViC 2026-04-25 snapshot has no therapeutic-option entries for the (gene, variant) pair._

#### BMA-EZH2-Y641-FL  (`bma_ezh2_y641_fl.yaml`)

- **biomarker:** `BIO-EZH2-Y641` — type `gene_mutation`
- **disease:** `DIS-FL`
- **ESCAT tier:** IB
- **actionability_lookup:** gene=`EZH2`, variant=`Y641N`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-BCELL-2025, SRC-ESMO-FL-2024, SRC-ONCOKB
- **recommended_combinations:**
  - tazemetostat monotherapy (R/R EZH2-mutated FL after ≥2 prior systemic therapies per SRC-NCCN-BCELL-2025, SRC-ESMO-FL-2024)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-NPM1-AML  (`bma_npm1_aml.yaml`)

- **biomarker:** `BIO-NPM1` — type `gene_mutation`
- **disease:** `DIS-AML`
- **ESCAT tier:** IA
- **actionability_lookup:** gene=`NPM1`, variant=`W288fs`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-ELN-AML-2022, SRC-NCCN-AML-2025, SRC-ESMO-AML-2020, SRC-QUAZAR-WEI-2020, SRC-VIALE-A-DINARDO-2020, SRC-ONCOKB
- **recommended_combinations:**
  - 7+3 induction → consolidation (fit, NPM1-mut without FLT3-ITD, intermediate/favorable per SRC-ELN-AML-2022)
  - oral azacitidine maintenance post-CR (per SRC-QUAZAR-WEI-2020)
  - venetoclax + azacitidine (unfit per SRC-VIALE-A-DINARDO-2020)
  - MRD-guided allogeneic HCT (NPM1-MRD persistence post-2 cycles per SRC-ELN-AML-2022)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

### 3.6 NO-LOOKUP — 16 BMA(s)

_Biomarker has skip_reason or no actionability_lookup (IHC, methylation, composite signature, multi-allele, etc.) — variant-level CIViC lookup not applicable._

#### BMA-CALR-ET  (`bma_calr_et.yaml`)

- **biomarker:** `BIO-CALR` — type `gene_mutation`
- **disease:** `DIS-ET`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `multi_allele_mvp`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015, SRC-PT1-HARRISON-2005, SRC-ONCOKB
- **recommended_combinations:**
  - observation (very-low-risk CALR-mutated per SRC-ESMO-MPN-2015)
  - low-dose aspirin (low-risk per SRC-NCCN-MPN-2025)
  - hydroxyurea + aspirin (high-risk 1L per SRC-PT1-HARRISON-2005)
  - interferon-alpha (preferred for younger high-risk per SRC-NCCN-MPN-2025)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-CALR-PMF  (`bma_calr_pmf.yaml`)

- **biomarker:** `BIO-CALR` — type `gene_mutation`
- **disease:** `DIS-PMF`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `multi_allele_mvp`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015, SRC-COMFORT-I-VERSTOVSEK-2012, SRC-JAKARTA2-HARRISON-2017, SRC-MOMENTUM-VERSTOVSEK-2023, SRC-DIPSS-PLUS-GANGAT-2011, SRC-ONCOKB
- **recommended_combinations:**
  - ruxolitinib monotherapy (intermediate-2 / high-risk per SRC-COMFORT-I-VERSTOVSEK-2012)
  - fedratinib monotherapy (post-ruxolitinib failure per SRC-JAKARTA2-HARRISON-2017)
  - momelotinib monotherapy (MF + anemia per SRC-MOMENTUM-VERSTOVSEK-2023)
  - allogeneic HCT (transplant-eligible higher-risk per SRC-NCCN-MPN-2025, SRC-DIPSS-PLUS-GANGAT-2011)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-CD30-ALCL  (`bma_cd30_alcl.yaml`)

- **biomarker:** `BIO-CD30-IHC` — type `protein_expression_ihc`
- **disease:** `DIS-ALCL`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `ihc_no_variant`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-BCELL-2025, SRC-ESMO-PTCL-2024, SRC-ONCOKB
- **recommended_combinations:**
  - BV + CHP — 1L sALCL per SRC-NCCN-BCELL-2025, SRC-ESMO-PTCL-2024
  - BV monotherapy — R/R sALCL salvage per SRC-NCCN-BCELL-2025
  - consolidative autologous HCT in CR1 (high-risk subgroups per SRC-NCCN-BCELL-2025)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-CD30-CHL  (`bma_cd30_chl.yaml`)

- **biomarker:** `BIO-CD30-IHC` — type `protein_expression_ihc`
- **disease:** `DIS-CHL`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `ihc_no_variant`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-BCELL-2025, SRC-ESMO-HODGKIN-2024, SRC-ONCOKB
- **recommended_combinations:**
  - A+AVD (brentuximab vedotin + AVD) — 1L stage III/IV cHL per SRC-NCCN-BCELL-2025, SRC-ESMO-HODGKIN-2024
  - brentuximab vedotin + nivolumab — R/R cHL pre-/post-autoHCT per SRC-NCCN-BCELL-2025
  - brentuximab vedotin consolidation post-autoHCT — high-risk R/R cHL per SRC-NCCN-BCELL-2025
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-CXCR4-WHIM-WM  (`bma_cxcr4_whim_wm.yaml`)

- **biomarker:** `BIO-CXCR4-WHIM` — type `gene_mutation`
- **disease:** `DIS-WM`
- **ESCAT tier:** IB
- **actionability_lookup:** —
- **skip_reason:** `multi_allele_mvp`
- **legacy SRC-ONCOKB level (J's claim):** `3A`
- **primary_sources:** SRC-NCCN-BCELL-2025, SRC-ESMO-WM-2024, SRC-ONCOKB
- **recommended_combinations:**
  - bendamustine + rituximab (1L CXCR4-mutated WM per SRC-NCCN-BCELL-2025, SRC-ESMO-WM-2024)
  - bortezomib + dexamethasone + rituximab (BDR, 1L CXCR4-mutated alternative per SRC-NCCN-BCELL-2025)
  - zanubrutinib monotherapy (1L CXCR4-mutated alternative — preserved efficacy vs ibrutinib in CXCR4-mut subgroup of ASPEN trial per SRC-NCCN-BCELL-2025)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-ESR1-MUT-BREAST  (`bma_esr1_mut_breast.yaml`)

- **biomarker:** `BIO-ESR1` — type `gene_mutation`
- **disease:** `DIS-BREAST`
- **ESCAT tier:** IB
- **actionability_lookup:** —
- **skip_reason:** `multi_allele_mvp`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-BREAST-2025, SRC-ESMO-BREAST-METASTATIC-2024, SRC-ONCOKB
- **recommended_combinations:**
  - elacestrant monotherapy (ESR1-mut HR+/HER2- post-AI ± CDK4/6i per SRC-NCCN-BREAST-2025, SRC-ESMO-BREAST-METASTATIC-2024)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-HER2-AMP-CRC  (`bma_her2_amp_crc.yaml`)

- **biomarker:** `BIO-HER2-SOLID` — type `protein_expression_ihc`
- **disease:** `DIS-CRC`
- **ESCAT tier:** IB
- **actionability_lookup:** —
- **skip_reason:** `ihc_no_variant`
- **legacy SRC-ONCOKB level (J's claim):** `2`
- **primary_sources:** SRC-NCCN-COLON-2025, SRC-ESMO-COLON-2024, SRC-ONCOKB
- **recommended_combinations:**
  - tucatinib + trastuzumab (2L+ HER2+ RAS-WT mCRC per SRC-NCCN-COLON-2025)
  - trastuzumab deruxtecan (2L+ HER2+ mCRC per SRC-NCCN-COLON-2025)
  - trastuzumab + lapatinib (alternative per HERACLES, listed in SRC-NCCN-COLON-2025)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-HER2-AMP-ESOPHAGEAL  (`bma_her2_amp_esophageal.yaml`)

- **biomarker:** `BIO-HER2-SOLID` — type `protein_expression_ihc`
- **disease:** `DIS-ESOPHAGEAL`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `ihc_no_variant`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-ESOPHAGEAL-2025, SRC-ESMO-ESOPHAGEAL-2024, SRC-ONCOKB
- **recommended_combinations:**
  - trastuzumab + fluoropyrimidine + platinum (1L per SRC-NCCN-ESOPHAGEAL-2025, SRC-ESMO-ESOPHAGEAL-2024)
  - pembrolizumab + trastuzumab + fluoropyrimidine + platinum (1L HER2+ PD-L1 CPS≥1 GEJ adenocarcinoma per SRC-NCCN-ESOPHAGEAL-2025)
  - trastuzumab deruxtecan (2L+ per SRC-NCCN-ESOPHAGEAL-2025)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-HER2-AMP-GASTRIC  (`bma_her2_amp_gastric.yaml`)

- **biomarker:** `BIO-HER2-SOLID` — type `protein_expression_ihc`
- **disease:** `DIS-GASTRIC`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `ihc_no_variant`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-GASTRIC-2025, SRC-ESMO-GASTRIC-2024, SRC-ONCOKB
- **recommended_combinations:**
  - trastuzumab + fluoropyrimidine + platinum (1L per SRC-NCCN-GASTRIC-2025, SRC-ESMO-GASTRIC-2024)
  - pembrolizumab + trastuzumab + fluoropyrimidine + platinum (1L HER2+ PD-L1 CPS ≥1 per SRC-NCCN-GASTRIC-2025)
  - trastuzumab deruxtecan (2L+ post-trastuzumab progression per SRC-NCCN-GASTRIC-2025)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-HRD-STATUS-BREAST  (`bma_hrd_status_breast.yaml`)

- **biomarker:** `BIO-HRD-STATUS` — type `gene_mutation`
- **disease:** `DIS-BREAST`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `tumor_agnostic`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-BREAST-2025, SRC-ESMO-BREAST-EARLY-2024, SRC-ESMO-BREAST-METASTATIC-2024, SRC-ONCOKB
- **recommended_combinations:**
  - olaparib monotherapy (gBRCAm HER2-negative metastatic per SRC-NCCN-BREAST-2025, SRC-ESMO-BREAST-METASTATIC-2024)
  - talazoparib monotherapy (gBRCAm HER2-negative metastatic per SRC-NCCN-BREAST-2025)
  - olaparib 1y adjuvant (gBRCAm high-risk early breast post-(neo)adjuvant chemo per SRC-NCCN-BREAST-2025, SRC-ESMO-BREAST-EARLY-2024)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-HRD-STATUS-OVARIAN  (`bma_hrd_status_ovarian.yaml`)

- **biomarker:** `BIO-HRD-STATUS` — type `gene_mutation`
- **disease:** `DIS-OVARIAN`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `tumor_agnostic`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-OVARIAN-2025, SRC-ESMO-OVARIAN-2024, SRC-ONCOKB
- **recommended_combinations:**
  - olaparib monotherapy maintenance (1L BRCA1/2-mut per SRC-NCCN-OVARIAN-2025, SRC-ESMO-OVARIAN-2024)
  - olaparib + bevacizumab maintenance (1L HRD-positive non-BRCA per SRC-NCCN-OVARIAN-2025)
  - niraparib monotherapy maintenance (1L per SRC-NCCN-OVARIAN-2025, all-comers benefit, HRD-positive strongest)
  - rucaparib monotherapy (2L maintenance / treatment per SRC-NCCN-OVARIAN-2025)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-HRD-STATUS-PDAC  (`bma_hrd_status_pdac.yaml`)

- **biomarker:** `BIO-HRD-STATUS` — type `gene_mutation`
- **disease:** `DIS-PDAC`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `tumor_agnostic`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-PANCREATIC-2025, SRC-ESMO-PANCREATIC-2024, SRC-ONCOKB
- **recommended_combinations:**
  - FOLFIRINOX (or modified) 1L for fit gBRCAm PDAC (preferred per SRC-NCCN-PANCREATIC-2025, SRC-ESMO-PANCREATIC-2024)
  - gemcitabine + cisplatin 1L (alternative platinum-based for non-FOLFIRINOX-eligible gBRCAm per SRC-NCCN-PANCREATIC-2025)
  - olaparib monotherapy maintenance (post-platinum response gBRCAm per SRC-NCCN-PANCREATIC-2025, SRC-ESMO-PANCREATIC-2024)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-HRD-STATUS-PROSTATE  (`bma_hrd_status_prostate.yaml`)

- **biomarker:** `BIO-HRD-STATUS` — type `gene_mutation`
- **disease:** `DIS-PROSTATE`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `tumor_agnostic`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-PROSTATE-2025, SRC-ESMO-PROSTATE-2024, SRC-EAU-PROSTATE-2024, SRC-ONCOKB
- **recommended_combinations:**
  - olaparib monotherapy (HRR-mutated mCRPC 2L+ per SRC-NCCN-PROSTATE-2025, SRC-ESMO-PROSTATE-2024)
  - olaparib + abiraterone + prednisone (BRCA-mutated 1L mCRPC per SRC-NCCN-PROSTATE-2025)
  - niraparib + abiraterone + prednisone (BRCA-mutated 1L mCRPC per SRC-NCCN-PROSTATE-2025)
  - talazoparib + enzalutamide (HRR-mutated 1L mCRPC per SRC-NCCN-PROSTATE-2025)
  - rucaparib monotherapy (BRCA1/2 mCRPC per SRC-NCCN-PROSTATE-2025)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-IDH1-R132-CHOLANGIO  (`bma_idh1_r132_cholangio.yaml`)

- **biomarker:** `BIO-IDH-MUTATION` — type `gene_mutation`
- **disease:** `DIS-CHOLANGIOCARCINOMA`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `multi_allele_mvp`
- **legacy SRC-ONCOKB level (J's claim):** `1`
- **primary_sources:** SRC-NCCN-HEPATOBILIARY, SRC-ONCOKB
- **recommended_combinations:**
  - ivosidenib monotherapy (2L+ IDH1 R132-mutated cholangio per SRC-NCCN-HEPATOBILIARY)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-IGHV-UNMUTATED-CLL  (`bma_ighv_unmutated_cll.yaml`)

- **biomarker:** `BIO-IGHV-MUTATIONAL-STATUS` — type `gene_mutation`
- **disease:** `DIS-CLL`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `multi_allele_mvp`
- **legacy SRC-ONCOKB level (J's claim):** `2`
- **primary_sources:** SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024, SRC-MOZ-UA-CLL-2022, SRC-ONCOKB
- **recommended_combinations:**
  - ibrutinib continuous monotherapy (1L IGHV-unmutated per SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024)
  - acalabrutinib ± obinutuzumab (1L IGHV-unmutated per SRC-NCCN-BCELL-2025)
  - zanubrutinib continuous monotherapy (1L IGHV-unmutated per SRC-NCCN-BCELL-2025)
  - venetoclax + obinutuzumab fixed-duration 12 mo (1L IGHV-unmutated per SRC-NCCN-BCELL-2025, SRC-ESMO-CLL-2024)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

#### BMA-MGMT-METHYLATION-GBM  (`bma_mgmt_methylation_gbm.yaml`)

- **biomarker:** `BIO-MGMT-METHYLATION` — type `methylation`
- **disease:** `DIS-GBM`
- **ESCAT tier:** IA
- **actionability_lookup:** —
- **skip_reason:** `tumor_agnostic`
- **legacy SRC-ONCOKB level (J's claim):** `2`
- **primary_sources:** SRC-NCCN-CNS-2025, SRC-EANO-GBM-2024, SRC-ONCOKB
- **recommended_combinations:**
  - Stupp protocol: concurrent RT + temozolomide → 6 cycles adjuvant TMZ (1L MGMT-methylated GBM per SRC-NCCN-CNS-2025, SRC-EANO-GBM-2024)
  - hypofractionated RT + TMZ (elderly ≥65y MGMT-methylated per SRC-EANO-GBM-2024)
  - lomustine + TMZ + RT (alternative MGMT-methylated 1L per CeTeG/NOA-09 — listed as option in SRC-EANO-GBM-2024)
- **CIViC fresh lookup (snapshot 2026-04-25):**
  - n therapeutic options: 0
  - levels: —
  - all drugs surfaced: —
  - supportive drugs: —
- **drug overlap (recommended_combinations vs CIViC):**
  - supportive matches: —
- **Phase-3-N added SRC-CIVIC?** no — only legacy SRC-ONCOKB present
  - **Phase-4 render-skip warning:** once render skips `source=SRC-ONCOKB`, this BMA will surface NO evidence_sources to HCP. Mitigation: cite NCCN/ESMO entry from `primary_sources` directly via render fallback, or rebuild BMA from a real source.

---

## 4. Recommendations

### 4.1 PROMOTE to merged status

BMAs where CIViC confirms both level (loose A/B↔1/2 mapping) AND at least one recommended drug. Single Clinical Co-Lead read-through of the CIViC supportive drug list against the BMA's recommended_combinations is sufficient (no full clinical signoff required because the rule engine rule itself is unchanged):

- `BMA-BRAF-V600E-CHOLANGIO` — biomarker `BIO-BRAF-V600E`, CIViC levels A:5, B:40, C:16, D:12, supportive overlap: Trametinib, Dabrafenib
- `BMA-BRAF-V600E-THYROID-ANAPLASTIC` — biomarker `BIO-BRAF-V600E`, CIViC levels A:5, B:40, C:16, D:12, supportive overlap: Trametinib, Dabrafenib
- `BMA-JAK2-V617F-PMF` — biomarker `BIO-JAK2`, CIViC levels B:1, D:1, supportive overlap: Fedratinib
- `BMA-JAK2-V617F-PV` — biomarker `BIO-JAK2`, CIViC levels B:1, D:1, supportive overlap: Peginterferon Alfa-2b

**Promote conditionally** (level matches, but CIViC drug list and BMA `recommended_combinations` are disjoint — clinical read of why CIViC's supportive drugs are not in our recs):

- `BMA-JAK2-V617F-ET` — CIViC drugs Peginterferon Alfa-2b, Fedratinib; BMA recs low-dose aspirin (low-risk per SRC-NCCN-MPN-2025), hydroxyurea + aspirin (high-risk 1L per SRC-PT1-HARRISON-2005), interferon-alpha (preferred for younger high-risk per SRC-NCCN-MPN-2025, SRC-ESMO-MPN-2015), anagrelide (HU-resistant/intolerant 2L).

### 4.2 REASSESS by Clinical Co-Lead

BMAs where CIViC contradicts the legacy claim or the level cannot be supported:

_(none — no DOWNGRADE / CONTRADICTED categorizations after refined drug-overlap analysis. The BRAF V600E cases briefly flagged as CONTRADICTED on a coarser pass were re-classified to CONFIRMED-WITH-DRUGS once supportive-vs-resistance overlap was disambiguated; the resistance evidence applies to monotherapy or a different indication, not the BMA's recommended combination.)_

### 4.3 ARCHIVE / re-extract from real source

BMAs where the variant-level lookup returned nothing in CIViC. The legacy `oncokb_level: "1"` claim came from training-data priors and cannot be cross-checked against any redistributable source. Either archive the BMA or re-extract from NCCN/ESMO with explicit citations.

- `BMA-EZH2-Y641-FL` — `BIO-EZH2-Y641` (lookup `{'gene': 'EZH2', 'variant': 'Y641N'}`). Prior audit Table §4 expected coverage; this audit found 0 therapeutic options. See §6.1 for the matcher case-sensitivity issue affecting NPM1.
- `BMA-NPM1-AML` — `BIO-NPM1` (lookup `{'gene': 'NPM1', 'variant': 'W288fs'}`). Prior audit Table §4 expected coverage; this audit found 0 therapeutic options. See §6.1 for the matcher case-sensitivity issue affecting NPM1.

### 4.4 Out-of-scope-for-CIViC (NO-LOOKUP)

16 BMAs reference biomarkers that CIViC's variant-keyed schema cannot encode (IHC / methylation / composite signature / multi-allele indels). These are **not OncoKB problems either** — see prior audit §1, §5. They need direct NCCN/ESMO citations in `primary_sources`, with the level set by clinical judgment under two-reviewer signoff (CHARTER §6.1).

**ihc_no_variant:**
- `BMA-CD30-ALCL` — `BIO-CD30-IHC` (legacy level `1`)
- `BMA-CD30-CHL` — `BIO-CD30-IHC` (legacy level `1`)
- `BMA-HER2-AMP-CRC` — `BIO-HER2-SOLID` (legacy level `2`)
- `BMA-HER2-AMP-ESOPHAGEAL` — `BIO-HER2-SOLID` (legacy level `1`)
- `BMA-HER2-AMP-GASTRIC` — `BIO-HER2-SOLID` (legacy level `1`)

**multi_allele_mvp:**
- `BMA-CALR-ET` — `BIO-CALR` (legacy level `1`)
- `BMA-CALR-PMF` — `BIO-CALR` (legacy level `1`)
- `BMA-CXCR4-WHIM-WM` — `BIO-CXCR4-WHIM` (legacy level `3A`)
- `BMA-ESR1-MUT-BREAST` — `BIO-ESR1` (legacy level `1`)
- `BMA-IDH1-R132-CHOLANGIO` — `BIO-IDH-MUTATION` (legacy level `1`)
- `BMA-IGHV-UNMUTATED-CLL` — `BIO-IGHV-MUTATIONAL-STATUS` (legacy level `2`)

**tumor_agnostic:**
- `BMA-HRD-STATUS-BREAST` — `BIO-HRD-STATUS` (legacy level `1`)
- `BMA-HRD-STATUS-OVARIAN` — `BIO-HRD-STATUS` (legacy level `1`)
- `BMA-HRD-STATUS-PDAC` — `BIO-HRD-STATUS` (legacy level `1`)
- `BMA-HRD-STATUS-PROSTATE` — `BIO-HRD-STATUS` (legacy level `1`)
- `BMA-MGMT-METHYLATION-GBM` — `BIO-MGMT-METHYLATION` (legacy level `2`)

### 4.5 Source-ingest TODOs (which guidelines would unblock confirmation)

To convert NO-LOOKUP and NO-EVIDENCE BMAs from training-data priors to citation-grounded evidence, ingest these primary sources (each is referenced by ≥1 BMA already):

- **`SRC-NCCN-BCELL-2025`** — would unblock 5 BMA(s): BMA-CD30-ALCL, BMA-CD30-CHL, BMA-CXCR4-WHIM-WM, BMA-EZH2-Y641-FL, BMA-IGHV-UNMUTATED-CLL
- **`SRC-NCCN-MPN-2025`** — would unblock 2 BMA(s): BMA-CALR-ET, BMA-CALR-PMF
- **`SRC-ESMO-MPN-2015`** — would unblock 2 BMA(s): BMA-CALR-ET, BMA-CALR-PMF
- **`SRC-NCCN-BREAST-2025`** — would unblock 2 BMA(s): BMA-ESR1-MUT-BREAST, BMA-HRD-STATUS-BREAST
- **`SRC-ESMO-BREAST-METASTATIC-2024`** — would unblock 2 BMA(s): BMA-ESR1-MUT-BREAST, BMA-HRD-STATUS-BREAST
- **`SRC-PT1-HARRISON-2005`** — would unblock 1 BMA(s): BMA-CALR-ET
- **`SRC-COMFORT-I-VERSTOVSEK-2012`** — would unblock 1 BMA(s): BMA-CALR-PMF
- **`SRC-JAKARTA2-HARRISON-2017`** — would unblock 1 BMA(s): BMA-CALR-PMF
- **`SRC-MOMENTUM-VERSTOVSEK-2023`** — would unblock 1 BMA(s): BMA-CALR-PMF
- **`SRC-DIPSS-PLUS-GANGAT-2011`** — would unblock 1 BMA(s): BMA-CALR-PMF
- **`SRC-ESMO-PTCL-2024`** — would unblock 1 BMA(s): BMA-CD30-ALCL
- **`SRC-ESMO-HODGKIN-2024`** — would unblock 1 BMA(s): BMA-CD30-CHL
- **`SRC-ESMO-WM-2024`** — would unblock 1 BMA(s): BMA-CXCR4-WHIM-WM
- **`SRC-ESMO-FL-2024`** — would unblock 1 BMA(s): BMA-EZH2-Y641-FL
- **`SRC-NCCN-COLON-2025`** — would unblock 1 BMA(s): BMA-HER2-AMP-CRC
- **`SRC-ESMO-COLON-2024`** — would unblock 1 BMA(s): BMA-HER2-AMP-CRC
- **`SRC-NCCN-ESOPHAGEAL-2025`** — would unblock 1 BMA(s): BMA-HER2-AMP-ESOPHAGEAL
- **`SRC-ESMO-ESOPHAGEAL-2024`** — would unblock 1 BMA(s): BMA-HER2-AMP-ESOPHAGEAL
- **`SRC-NCCN-GASTRIC-2025`** — would unblock 1 BMA(s): BMA-HER2-AMP-GASTRIC
- **`SRC-ESMO-GASTRIC-2024`** — would unblock 1 BMA(s): BMA-HER2-AMP-GASTRIC
- **`SRC-ESMO-BREAST-EARLY-2024`** — would unblock 1 BMA(s): BMA-HRD-STATUS-BREAST
- **`SRC-NCCN-OVARIAN-2025`** — would unblock 1 BMA(s): BMA-HRD-STATUS-OVARIAN
- **`SRC-ESMO-OVARIAN-2024`** — would unblock 1 BMA(s): BMA-HRD-STATUS-OVARIAN
- **`SRC-NCCN-PANCREATIC-2025`** — would unblock 1 BMA(s): BMA-HRD-STATUS-PDAC
- **`SRC-ESMO-PANCREATIC-2024`** — would unblock 1 BMA(s): BMA-HRD-STATUS-PDAC
- **`SRC-NCCN-PROSTATE-2025`** — would unblock 1 BMA(s): BMA-HRD-STATUS-PROSTATE
- **`SRC-ESMO-PROSTATE-2024`** — would unblock 1 BMA(s): BMA-HRD-STATUS-PROSTATE
- **`SRC-EAU-PROSTATE-2024`** — would unblock 1 BMA(s): BMA-HRD-STATUS-PROSTATE
- **`SRC-NCCN-HEPATOBILIARY`** — would unblock 1 BMA(s): BMA-IDH1-R132-CHOLANGIO
- **`SRC-ESMO-CLL-2024`** — would unblock 1 BMA(s): BMA-IGHV-UNMUTATED-CLL
- **`SRC-MOZ-UA-CLL-2022`** — would unblock 1 BMA(s): BMA-IGHV-UNMUTATED-CLL
- **`SRC-NCCN-CNS-2025`** — would unblock 1 BMA(s): BMA-MGMT-METHYLATION-GBM
- **`SRC-EANO-GBM-2024`** — would unblock 1 BMA(s): BMA-MGMT-METHYLATION-GBM
- **`SRC-ELN-AML-2022`** — would unblock 1 BMA(s): BMA-NPM1-AML
- **`SRC-NCCN-AML-2025`** — would unblock 1 BMA(s): BMA-NPM1-AML
- **`SRC-ESMO-AML-2020`** — would unblock 1 BMA(s): BMA-NPM1-AML
- **`SRC-QUAZAR-WEI-2020`** — would unblock 1 BMA(s): BMA-NPM1-AML
- **`SRC-VIALE-A-DINARDO-2020`** — would unblock 1 BMA(s): BMA-NPM1-AML

Plus targeted single-paper additions (already referenced via SRC-* IDs in the BMA `notes`):
- `SRC-INDIGO-MELLINGHOFF-2023` (vorasidenib in IDH-mut grade-2 glioma) — referenced by IDH1-R132 cholangio family
- `SRC-EZH2-FL-MORSCHHAUSER-2020` (tazemetostat in r/r EZH2-mutated FL) — referenced by EZH2-Y641-FL
- `SRC-MK3475-689` and `SRC-CHECKMATE-577` for MGMT/HER2 esophageal context (already partially cited in BMA notes)

---

## 5. Findings on Phase-3-N coverage

Cross-tab of categorization vs Phase-3-N SRC-CIVIC entry presence:

| Category | got SRC-CIVIC from N | only legacy SRC-ONCOKB |
|---|---:|---:|
| CONFIRMED-WITH-DRUGS | 4 | 0 |
| CONFIRMED-LEVEL-ONLY | 1 | 0 |
| NO-EVIDENCE | 0 | 2 |
| NO-LOOKUP | 0 | 16 |

- Phase 3-N successfully attached SRC-CIVIC entries to **all 5 CIViC-confirmed BMAs** (BRAF V600E ×2, JAK2 V617F ×3).
- Phase 3-N (correctly) skipped all 18 BMAs in NO-LOOKUP / NO-EVIDENCE, since CIViC has no therapeutic options to attach. No false attachments observed.
- **Render warning:** with the Phase-4 render rule that skips `source=SRC-ONCOKB`, those 18 BMAs will display zero `evidence_sources` rows. Their factual content (NCCN/ESMO citations, drug labels) lives in `primary_sources` and `regulatory_approval` and must reach the render layer through those paths instead.

---

## 6. Top-3 most-actionable findings

**Finding 6.1 — `civic_variant_matcher.matches_civic_entry` Rule 1 is case-sensitive, missing NPM1 W288fs.**  
Query `(NPM1, W288fs)` returns 0 therapeutic options against a snapshot that contains 2 W288FS items with therapies (CIViC IDs 152 `[NSC348884]`, 153 `[Etoposide, Daunorubicin, Cytarabine]`). Cause: `qv == cv` at `knowledge_base/engine/civic_variant_matcher.py:171` compares `"W288fs" == "W288FS"` → False. Rule 2 (fusion-component) and the descriptor path (Rule 2 fallback) are case-insensitive, so the bug only bites single-gene exact-match queries where the CIViC variant string differs in case from the normalized query. **Recommended fix:** change Rule 1 to `qg == cg.upper() and qv.casefold() == cv.casefold()`. Add a regression test for `(NPM1, W288fs)` and `(NPM1, w288fs)` returning ≥1 therapeutic option. This single fix would convert NPM1-AML from NO-EVIDENCE to CONFIRMED-WITH-DRUGS (or LEVEL-ONLY — its CIViC drugs are NSC348884 / Etoposide / Daunorubicin / Cytarabine, none of which match the BMA's `7+3 / venetoclax+aza` recs; LEVEL-ONLY classification more likely).

**Finding 6.2 — 18 of 23 J-drafts cannot be cross-checked against any redistributable variant-level source, by construction.**  
All 18 NO-LOOKUP/NO-EVIDENCE BMAs reference biomarkers that are either non-variant (IHC, methylation, composite signature) or multi-allele (CALR exon 9 indels, IDH1/2 family). This matches the prior audit's §5 conclusion that public-only is NOT viable for the BMA layer as J-authored, and OncoKB itself does not cover these at variant level either. **Action item:** for each, replace the `oncokb_level: "1"` claim — which currently has no traceable source — with explicit NCCN/ESMO citations in `primary_sources` plus `escat_tier` set by clinical judgment under two-reviewer signoff. Highest-priority targets are CD30-IHC ×2 (the brentuximab indication is FDA-approved and well-documented in NCCN) and HRD-STATUS ×4 (PARPi indications are FDA-approved, again well-documented in NCCN/ESMO).

**Finding 6.3 — Phase-3-N + Phase-4 render-skip create a 'silent zero evidence' bucket of 18 BMAs.**  
Phase 4's render rule (skip `evidence_sources` entries with `source=SRC-ONCOKB`) is correct per the OncoKB ToS audit, but it leaves 18 J-drafts with zero `evidence_sources` rows visible to the HCP. Their citation-bearing content is in `primary_sources` (NCCN, ESMO) and `regulatory_approval` (FDA, EMA) which the current render template may not surface as 'evidence' rows. **Recommended:** before flipping the Phase-4 render rule on, add a render fallback that promotes `primary_sources` (filtered to non-stub Source entities) into the rendered evidence section when `evidence_sources` is empty after the SRC-ONCOKB skip. This is read-only logic in the template; no schema change needed.

---

## Appendix A. Methodology notes

- **CIViC level → legacy OncoKB tier** (loose comparison used for level-match): A/B ↔ 1/2; C ↔ 3A/3B; D ↔ 4. (Same as prior audit §6.1; conservative principle: CONFIRMED requires a CIViC level at or above the legacy claim.)
- **Drug overlap** is computed by case-insensitive substring of the CIViC drug name into each entry of `recommended_combinations` (after non-alphanumeric normalization). 'Trametinib' matches 'dabrafenib + trametinib (2L+ ...)'. INN-only — does not currently expand brand names or ATC codes; a future pass should normalize via `RxNorm` or the project's `Drug` entity index.
- **CONTRADICTED** is asserted only when a recommended drug appears in CIViC resistance/Does-Not-Support evidence AND does NOT also appear in supportive evidence at the same (gene, variant). For BRAF V600E, both Trametinib and Dabrafenib appear in supportive (combination) AND resistance (monotherapy in CRC); the resistance evidence is informational for the BMA, not contradictory, so neither was flagged.
- **No YAML files were modified.** This audit is read-only per the Phase-3-O brief.

## Appendix B. Files touched

- `docs/reviews/bma-j-drafts-civic-diff-2026-04-27.md` — this file (only write).

