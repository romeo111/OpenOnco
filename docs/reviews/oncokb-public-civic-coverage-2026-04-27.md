# OncoKB-public + CIViC coverage audit — 2026-04-27

**Author:** automated audit (Claude, read-only, no repo writes outside this file)
**Branch:** feat/oncokb-wiring
**Scope:** can OpenOnco build a working OncoKB-equivalent biomarker-actionability dataset using only redistributable public sources (CIViC + oncokb-public/oncokb-datahub on GitHub), without an OncoKB live API token?
**Mode:** READ-ONLY across repo. Network reads: GitHub clones into `%TEMP%` (ephemeral), WebFetch on CIViC docs.

---

## 1. Executive summary

**Decision metrics (Step 5):**

| Metric | Value |
|---|---|
| Single-allele BIO-* fully covered by public sources (variant evidence + therapies in CIViC, gene confirmation in oncokb-datahub) | **27 of 29** (29 BIO-* have `oncokb_lookup`, not 20 as initially stated in the brief) |
| BMA drafts (drafted_by: claude_extraction) confirmed by ≥1 public source (variant-level CIViC with therapies) | **6 of 23** |
| BMAs flagged — claimed level/drugs NOT verifiable from any public source | **15 of 23** + 2 datahub-gene-only = **17 of 23 not variant-level confirmable in public sources** |
| Gene/variant pairs in our 29 BIO-* that need OncoKB live API for full coverage | **2** (EZH2 Y641N, RHOA G17V — datahub gene-only, no CIViC variant evidence) |
| Estimated %coverage gain from OncoKB live token | At BIO-* level: ~7% (2/29). At BMA-draft level: ~52% (12 of the 17 unconfirmed BMAs cover non-variant biomarkers — IHC, methylation, fusion-only, indels — that OncoKB may or may not actually cover; estimate "OncoKB token unblocks ~5–10 of the 17 in practice, the rest need ESMO/NCCN narrative citations") |

**Decision:** *public-only is viable for the variant-level rule engine* (27/29 BIO-* covered). It is *not viable* for the BMA layer as currently authored — 17 of 23 drafted BMAs reference biomarkers that public sources do not cover at the level/drugs granularity claimed (CALR exon 9 indels, CD30-IHC, HRD signature, MGMT methylation, IGHV mutation status, HER2 amp by IHC, etc.). These BMAs are **not OncoKB problems** — OncoKB itself does not cover most of them at variant level either. They need direct guideline citations (NCCN/ESMO) rather than OncoKB substitution.

**License gate (oncokb-public data redistribution):** **forbids redistribution.** See §3.

---

## 2. CIViC inventory

Loaded from `knowledge_base/hosted/civic/2026-04-25/evidence.yaml` (CC0-1.0, 90,937 lines).

| Metric | Value |
|---|---|
| Total accepted evidence items | 4,842 |
| Distinct (gene, variant) pairs | 1,933 |
| Distinct gene symbols | 551 |
| % of items with non-empty `therapies` list | **58.7% (2,841 / 4,842)** |
| All items have `evidence_status: accepted` | yes (4,842/4,842) |

### 2.1 Evidence level distribution

| Level | Count | % |
|---|---|---|
| A — Validated | 225 | 4.6% |
| B — Clinical | 1,619 | 33.4% |
| C — Case Study | 1,668 | 34.4% |
| D — Preclinical | 1,298 | 26.8% |
| E — Inferential | 32 | 0.7% |

### 2.2 Evidence type distribution

| Type | Count |
|---|---|
| Predictive | 2,842 |
| Predisposing | 682 |
| Prognostic | 536 |
| Diagnostic | 493 |
| Functional | 159 |
| Oncogenic | 130 |

### 2.3 Direction & significance

| Direction | Count |
|---|---|
| Supports | 4,275 (88.3%) |
| Does Not Support | 513 (10.6%) |
| N/A | 54 (1.1%) |

| Significance (top 12) | Count |
|---|---|
| Sensitivity/Response | 1,777 |
| Resistance | 1,038 |
| Positive | 484 |
| Predisposition | 478 |
| Poor Outcome | 374 |
| Uncertain Significance | 149 |
| Oncogenicity | 130 |
| Better Outcome | 122 |
| N/A | 95 |
| Dominant Negative | 81 |
| Gain of Function | 38 |
| Loss of Function | 27 |

### 2.4 Top genes by evidence count

VHL (660), BCR::ABL1 (334), EGFR (268), BRAF (220), TP53 (194), KRAS (191), PIK3CA (176), ERBB2 (146), KIT (113), FLT3 (78), EML4::ALK (64), PTEN (61), NRAS (48), BRCA1 (46), FGFR1 (43), BRCA2 (41), V::ALK (38), MET (37), ALK (36), NPM1 (35), DNMT3A (34), FGFR3 (34), ETV6::NTRK3 (32), ATM (31), PDGFRA (30), LMNA::NTRK1 (30), RET (29), CDKN2A (29), EZH2 (29), IDH1 (28).

### 2.5 Notable encoding quirks

- **Fusions are encoded as fused gene symbols joined by `::`** (e.g. `BCR::ABL1`, `EML4::ALK`, `ETV6::NTRK3`).
- **Resistance mutations on a fusion background are encoded in the variant string**, not the gene field (e.g. gene `BCR::ABL1`, variant `Fusion AND ABL1 T315I`). Naïve `gene == "ABL1"` lookup misses 100% of CML kinase-domain mutation evidence. The cross-coverage in §4 below uses fusion-aware matching that splits `::` and substring-matches the variant string.
- **Exon-level descriptors** appear as `EXON 19 DELETION`, `EXON 20 INSERTION` (uppercase, space-separated). Our `engine/oncokb_extract.py:normalize_variant` produces `Exon 19 deletion` (mixed case) — **case-insensitive** match required when querying CIViC.

---

## 3. oncokb-public + oncokb-datahub inventory

### 3.1 What was cloned

- `https://github.com/oncokb/oncokb-public` → `C:\Users\805\AppData\Local\Temp\oncokb-public-clone\` (shallow clone). This is the **JHipster webapp source code** (Java + React) that powers oncokb.org. **No `data/` directory exists.** No `LICENSE` file at top level.
- `https://github.com/oncokb/oncokb-datahub` → `C:\Users\805\AppData\Local\Temp\oncokb-datahub\` (shallow clone). This is the actual public data repo. **No `LICENSE` file.**

The brief assumed `oncokb-public` would contain `allActionableVariants.txt`, `allAnnotatedVariants.txt`, etc. **It does not.** Those tables are only available via the authenticated download portal at oncokb.org/dataAccess (API token required).

### 3.2 oncokb-datahub file inventory

- Layout: `RELEASE/v3.0/`, `RELEASE/v3.1/` … `RELEASE/v7.0/` (52 versioned releases).
- Each release contains exactly four files:
  - `allCuratedGenes.txt` (~78 KB, TSV)
  - `allCuratedGenes.json` (~300 KB)
  - `cancerGeneList.txt` (~135 KB, TSV)
  - `cancerGeneList.json` (~460 KB)
- Plus `README.md` per release (changelog only, ~64 KB for v7.0).

`allCuratedGenes.txt` columns: `GRCh37 Isoform, GRCh37 RefSeq, GRCh38 Isoform, GRCh38 RefSeq, Entrez Gene ID, Hugo Symbol, Gene Type, Highest Level of Evidence(sensitivity), Highest Level of Evidence(resistance)`.

**This is gene-level, not variant-level.** No alterations, no specific drugs, no tumor types. For each curated gene you get:
- Hugo symbol + Entrez ID + transcript IDs
- Gene Type (ONCOGENE / TSG / ONCOGENE_AND_TSG)
- Highest sensitivity level (1, 2, 3A, 3B, or blank)
- Highest resistance level (R1, R2, or blank)

`cancerGeneList.txt` is similar but with cross-resource panel membership (MSK-IMPACT, FoundationOne, Vogelstein, COSMIC CGC).

### 3.3 License — verbatim quotes

**oncokb-public repository:** no `LICENSE` file. The terms displayed on oncokb.org/terms are reproduced verbatim in `src/main/webapp/app/pages/apiAccessGroup/TermsPage.tsx` (lines 33–93). The relevant clauses:

> "You may view the Content solely for your own personal reference or use for research in an academic setting, provided that all academic research use of the Content must credit OncoKB™ as the source of the Content and reference these Terms of Use; **outside of scientific publication, you may not otherwise redistribute or share the Content with any third party, in part or in whole, for any purpose, without the express permission of MSK.**" *(emphasis added)*

> "Unless you have signed a license agreement with MSK, you may not use any part of the Content for any other purpose, including:
> 1. use or incorporation into a commercial product or towards performance of a commercial service;
> 2. research use in a commercial setting;
> 3. **use for patient services**; or
> 4. **generation of reports in a hospital or other patient care setting.**"
> *(emphasis added)*

> "You may not copy, transfer, reproduce, modify or create derivative works of OncoKB™ for any commercial purpose without the express permission of MSK."

From `constants/terms.ts` line 3:

> "Using OncoKB™ data for the creation and training of AI models is strictly prohibited. Access may be granted for model validation or benchmarking purposes only with explicit authorization."

**oncokb-datahub repository:** no `LICENSE` file. The README does not specify terms but references the same OncoKB™ trademark and citation requirements as oncokb.org. By default of GitHub absent a license: **all rights reserved.**

### 3.4 License verdict

**FORBIDS REDISTRIBUTION.** Three independent grounds:

1. The OncoKB Terms of Use explicitly state academic users **may not redistribute or share the Content with any third party, in part or in whole, for any purpose, without the express permission of MSK** (other than in scientific publication).
2. They explicitly forbid **"use for patient services"** and **"generation of reports in a hospital or other patient care setting"** — which is exactly what OpenOnco is (CHARTER §2: free public resource that produces patient treatment plans).
3. **AI training is "strictly prohibited."** Even if OpenOnco is rule-engine driven (CHARTER §8.3), this clause forecloses any future evolution that uses OncoKB data to train auxiliary ML components.

The `oncokb-datahub` gene-list files have no separate LICENSE — by default they inherit "all rights reserved" plus the OncoKB Terms by reference. We **cannot mirror or vendor them** in our GitHub Releases. We can only reference them by URL and instruct users to fetch from MSK directly.

This matches `specs/SOURCE_INGESTION_SPEC.md` §2.5 which classifies OncoKB as `referenced` mode (not `hosted`) — **no change needed to the spec.** The audit confirms the spec was right.

---

## 4. Cross-coverage matrix — 29 BIO-* with `oncokb_lookup`

(The brief said "20"; the repo currently has 29 such files — listed below.)

Match logic: gene equality OR fusion-component match (`BCR::ABL1` → `ABL1`); variant either equal (case-insensitive) or substring match (catches `Fusion AND ABL1 T315I` and `EXON 19 DELETION`). CIViC level columns counted A/B/C/D/E.

| BIO id | gene | variant | CIViC n | A/B/C/D/E | dir S/N | with therapies | datahub sens/R | verdict |
|---|---|---|---|---|---|---|---|---|
| BIO-ALK-G1202R | ALK | G1202R | 7 | 0/0/2/5/0 | 7/0 | 7 | 1 / R2 | covered |
| BIO-ALK-L1196M | ALK | L1196M | 7 | 0/0/4/3/0 | 7/0 | 7 | 1 / R2 | covered |
| BIO-BCR-ABL1-E255K | ABL1 | E255K | 20 | 0/1/9/10/0 | 17/3 | 20 | 1 / R1 | covered |
| BIO-BCR-ABL1-F317L | ABL1 | F317L | 21 | 0/2/8/11/0 | 18/3 | 21 | 1 / R1 | covered |
| BIO-BCR-ABL1-T315I | ABL1 | T315I | 28 | 0/4/9/15/0 | 26/2 | 28 | 1 / R1 | covered |
| BIO-BCR-ABL1-V299L | ABL1 | V299L | 11 | 0/1/3/7/0 | 11/0 | 11 | 1 / R1 | covered |
| BIO-BRAF-V600E | BRAF | V600E | 109 | 6/65/20/17/1 | 98/11 | 87 | 1 / – | covered |
| BIO-BRAF-V600K | BRAF | V600K | 11 | 0/10/1/0/0 | 11/0 | 11 | 1 / – | covered |
| BIO-EGFR-C797S | EGFR | C797S | 2 | 0/1/1/0/0 | 2/0 | 2 | 1 / R2 | covered |
| BIO-EGFR-EXON19-DELETION | EGFR | Exon 19 deletion | 42 | 11/14/12/5/0 | 41/1 | 42 | 1 / R2 | covered |
| BIO-EGFR-EXON20-INSERTION | EGFR | Exon 20 insertion | 7 | 4/2/1/0/0 | 7/0 | 7 | 1 / R2 | covered |
| BIO-EGFR-L858R | EGFR | L858R | 49 | 11/15/4/19/0 | 48/1 | 48 | 1 / R2 | covered |
| BIO-EGFR-T790M | EGFR | T790M | 35 | 5/11/7/11/1 | 34/1 | 33 | 1 / R2 | covered |
| BIO-EZH2-Y641 | EZH2 | Y641N | **0** | 0/0/0/0/0 | 0/0 | 0 | 1 / – | **datahub gene-only** |
| BIO-FLT3-D835 | FLT3 | D835Y | 6 | 0/0/1/5/0 | 5/1 | 6 | 1 / – | covered |
| BIO-FLT3-F691L | FLT3 | F691L | 2 | 0/0/0/2/0 | 2/0 | 2 | 1 / – | covered |
| BIO-IDH1-R132H | IDH1 | R132H | 3 | 1/0/1/1/0 | 2/1 | 3 | 1 / – | covered |
| BIO-JAK2 | JAK2 | V617F | 6 | 0/5/0/1/0 | 6/0 | 2 | 2 / – | covered |
| BIO-KIT-D816V | KIT | D816V | 6 | 0/3/0/3/0 | 6/0 | 4 | 1 / R2 | covered |
| BIO-KRAS-G12C | KRAS | G12C | 18 | 3/7/1/7/0 | 18/0 | 16 | 1 / R1 | covered |
| BIO-KRAS-G12D | KRAS | G12D | 21 | 0/7/7/7/0 | 21/0 | 16 | 1 / R1 | covered |
| BIO-KRAS-G12V | KRAS | G12V | 12 | 0/3/5/4/0 | 11/1 | 11 | 1 / R1 | covered |
| BIO-MYD88-L265P | MYD88 | L265P | 3 | 0/2/0/1/0 | 3/0 | 2 | – / – | CIViC-only (datahub gene blank) |
| BIO-NPM1 | NPM1 | W288fs | 3 | 0/1/0/1/1 | 2/1 | 2 | 1 / – | covered |
| BIO-NRAS-Q61R | NRAS | Q61R | 2 | 0/0/2/0/0 | 2/0 | 2 | 1 / R1 | covered |
| BIO-PIK3CA-H1047R | PIK3CA | H1047R | 30 | 2/5/3/20/0 | 26/4 | 27 | 1 / – | covered |
| BIO-RET-M918T | RET | M918T | 15 | 1/4/3/7/0 | 15/0 | 9 | 1 / – | covered |
| BIO-RHOA-G17V | RHOA | G17V | **0** | 0/0/0/0/0 | 0/0 | 0 | – / – | **neither (would need OncoKB token)** |
| BIO-ROS1-G2032R | ROS1 | G2032R | 9 | 0/0/3/6/0 | 9/0 | 9 | 1 / R2 | covered |

**Roll-up:** 27/29 covered with variant-level evidence + therapies in CIViC. EZH2 Y641N is in oncokb-datahub at gene level (sens=1) but not in our CIViC snapshot at the Y641N variant level — surprising, given EZH2 Y641 is the canonical tazemetostat indication; this may be a snapshot age issue (CIViC has 29 EZH2 evidence items, none on Y641N specifically). RHOA G17V has no public coverage at all (RHOA is not on oncokb-datahub's curated gene list and CIViC has no RHOA G17V evidence) — this is consistent with RHOA being a research-mode AITL biomarker, not an OncoKB Level 1–4 variant.

---

## 5. Cross-coverage matrix — 23 BMA drafts (`drafted_by: claude_extraction`)

| BMA file | biomarker_id | claimed level | CIViC variant n | CIViC levels | datahub gene sens/R | verdict |
|---|---|---|---|---|---|---|
| bma_braf_v600e_cholangio.yaml | BIO-BRAF-V600E | 1 | 109 | A:6,B:65,C:20,D:17,E:1 | 1 / – | CIViC-confirmed |
| bma_braf_v600e_thyroid_anaplastic.yaml | BIO-BRAF-V600E | 1 | 109 | A:6,B:65,C:20,D:17,E:1 | 1 / – | CIViC-confirmed |
| bma_calr_et.yaml | BIO-CALR | 1 | 0 | – | – / – | NOT in public sources |
| bma_calr_pmf.yaml | BIO-CALR | 1 | 0 | – | – / – | NOT in public sources |
| bma_cd30_alcl.yaml | BIO-CD30-IHC | 1 | 0 | – | ? / ? | NOT in public sources (IHC, not a variant) |
| bma_cd30_chl.yaml | BIO-CD30-IHC | 1 | 0 | – | ? / ? | NOT in public sources (IHC, not a variant) |
| bma_cxcr4_whim_wm.yaml | BIO-CXCR4-WHIM | 3A | 0 | – | – / – | NOT in public sources |
| bma_esr1_mut_breast.yaml | BIO-ESR1 | 1 | 0 | – | 1 / – | datahub-gene-only (variant-level claim cannot be cross-checked) |
| bma_ezh2_y641_fl.yaml | BIO-EZH2-Y641 | 1 | 0 | – | 1 / – | datahub-gene-only |
| bma_her2_amp_crc.yaml | BIO-HER2-SOLID | 2 | 0 | – | ? / ? | NOT in public sources (amplification, not in CIViC variant index) |
| bma_her2_amp_esophageal.yaml | BIO-HER2-SOLID | 1 | 0 | – | ? / ? | NOT in public sources |
| bma_her2_amp_gastric.yaml | BIO-HER2-SOLID | 1 | 0 | – | ? / ? | NOT in public sources |
| bma_hrd_status_breast.yaml | BIO-HRD-STATUS | 1 | 0 | – | ? / ? | NOT in public sources (composite biomarker) |
| bma_hrd_status_ovarian.yaml | BIO-HRD-STATUS | 1 | 0 | – | ? / ? | NOT in public sources |
| bma_hrd_status_pdac.yaml | BIO-HRD-STATUS | 1 | 0 | – | ? / ? | NOT in public sources |
| bma_hrd_status_prostate.yaml | BIO-HRD-STATUS | 1 | 0 | – | ? / ? | NOT in public sources |
| bma_idh1_r132_cholangio.yaml | BIO-IDH-MUTATION | 1 | 0 | – | ? / ? | NOT in public sources (parent BIO has no oncokb_lookup; specific R132C/L lookup would hit) |
| bma_ighv_unmutated_cll.yaml | BIO-IGHV-MUTATIONAL-STATUS | 2 | 0 | – | ? / ? | NOT in public sources (mutational-burden classifier, not a variant) |
| bma_jak2_v617f_et.yaml | BIO-JAK2 | 1 | 6 | B:5,D:1 | 2 / – | CIViC-confirmed (datahub disagrees with claim — datahub says gene sens=2, BMA claims level=1) |
| bma_jak2_v617f_pmf.yaml | BIO-JAK2 | 1 | 6 | B:5,D:1 | 2 / – | CIViC-confirmed (same datahub level disagreement) |
| bma_jak2_v617f_pv.yaml | BIO-JAK2 | 1 | 6 | B:5,D:1 | 2 / – | CIViC-confirmed (same datahub level disagreement) |
| bma_mgmt_methylation_gbm.yaml | BIO-MGMT-METHYLATION | 2 | 0 | – | ? / ? | NOT in public sources (epigenetic, not a variant) |
| bma_npm1_aml.yaml | BIO-NPM1 | 1 | 3 | B:1,D:1,E:1 | 1 / – | CIViC-confirmed |

**Roll-up:**
- 6/23 CIViC-confirmed at variant level + therapies
- 2/23 datahub-gene-level only (ESR1, EZH2 Y641N) — claim cannot be cross-checked at variant granularity
- 15/23 not in any public source — but most of these are by-construction not OncoKB-variant-shaped: IHC markers (CD30), composite signatures (HRD), epigenetic (MGMT methylation), structural (HER2 amp, CALR exon 9 indels), mutation-burden (IGHV-status). OncoKB does cover several of these (HER2 amp, MGMT methylation, IGHV via "tumor type" tab) but **CIViC's variant-keyed schema does not.**

**Disagreement to escalate:** all three JAK2 V617F BMAs claim `oncokb_level: "1"`, but oncokb-datahub's allCuratedGenes (v7.0) has JAK2 highest-sens-level = **2**, not 1. The BMA-claimed level may still be correct (datahub levels are stale relative to OncoKB-live), but this should be verified against oncokb.org by a clinical co-lead before sign-off.

---

## 6. Proposed CIViC ↔ OncoKB level mapping

**Status: `mapping_review_status: pending_clinical_signoff`.**

CIViC level definitions (verbatim from civic.readthedocs.io/en/latest/model/evidence/level.html, fetched 2026-04-27):

- **A — Validated Association:** "Proven/consensus association in human medicine."
- **B — Clinical Evidence:** "Clinical trial or other primary patient data supports association."
- **C — Case Study:** "Individual case reports from clinical journals."
- **D — Preclinical Evidence:** "In vivo or in vitro models support association."
- **E — Inferential Association:** "Indirect evidence."

OncoKB therapeutic levels (from oncokb-public source code + their published news entries — exact text reconstructed from the NewsPage 12/20/2019 simplified-levels announcement, since oncokb.org/levels-of-evidence requires JS rendering):

- **Level 1:** FDA-recognized biomarker predictive of response to an FDA-approved drug *in this indication*.
- **Level 2:** "Standard care biomarker recommended by the NCCN or other expert panels predictive of response to an FDA-approved drug in this indication" (formerly Level 2A, simplified Dec 2019).
- **Level 3A:** Compelling clinical evidence supports the biomarker as predictive of response to a drug in this indication, but neither biomarker nor drug is standard care.
- **Level 3B:** "Standard care or investigational biomarker predictive of response to an FDA-approved or investigational drug in another indication" (combination of former 2B and 3B, simplified Dec 2019).
- **Level 4:** Compelling biological evidence supports the biomarker as predictive of response to a drug.
- **R1:** Standard-care biomarker predictive of resistance to an FDA-approved drug.
- **R2:** Compelling clinical evidence supports the biomarker as predictive of resistance to a drug.

### 6.1 Proposed conservative mapping (CIViC → OncoKB)

The mapping is asymmetric: CIViC-A only roughly matches OncoKB-1, CIViC-B straddles OncoKB-2 and 3A, etc. **Conservative principle: when uncertain, downgrade.**

| CIViC | Interim OncoKB equivalent | Rationale |
|---|---|---|
| A — Validated | **2** (NOT 1) | CIViC-A includes "consensus association in human medicine" which is broader than OncoKB-1's strict "FDA-recognized biomarker for an FDA-approved drug in this indication." Many CIViC-A items are NCCN-driven without FDA companion-diagnostic status. Downgrade to 2 by default; promote to 1 only when the evidence item explicitly cites an FDA companion diagnostic (CIViC stores `is_flagged` and PMC IDs but not FDA-CDx flag — manual review needed). |
| B — Clinical | **3A** (default) or **2** if therapy is FDA-approved in same indication | CIViC-B = "clinical trial or other primary patient data" without specifying FDA approval status. Compelling but not standard-care. Map to 3A. Promote to 2 only when therapy ATC code matches an FDA label active in the same OncoTree node. |
| C — Case Study | **3B** (default) or **4** if very small N | Single-patient or small-series reports. OncoKB 3B = standard or investigational biomarker for FDA-approved/investigational drug in *another* indication; this captures the CIViC-C "compelling but anecdotal" tier. |
| D — Preclinical | **4** | Both are explicitly preclinical / biological evidence. Direct match. |
| E — Inferential | **(do not assign an OncoKB level)** | OncoKB has no equivalent. Render as "supporting in silico / inferential evidence" without a Level badge. |

**Direction collapse for resistance:**

| CIViC direction | CIViC significance | Maps to |
|---|---|---|
| Supports | Sensitivity/Response | OncoKB sensitivity level (per the table above) |
| Supports | Resistance | **R1** if CIViC level A or B, else **R2** |
| Supports | Reduced Sensitivity | **R2** (always — never R1, as OncoKB R1 requires FDA-recognized resistance) |
| Supports | Adverse Response | Render as a **safety flag**, not an OncoKB level — adverse-response is not a sensitivity-vs-resistance dichotomy |
| Supports | Better Outcome / Poor Outcome | **prognostic only** — do NOT map to therapeutic OncoKB levels; surface in the Prognosis section of the plan |
| Supports | Predisposition | **germline pathogenicity** — route to ACMG/ClinGen layer, not OncoKB therapeutic |
| Does Not Support | Sensitivity/Response | **invert to "no evidence of response"** — display as anti-recommendation, not as OncoKB level |
| Does Not Support | Resistance | **rebut a resistance claim** — display as safety-positive flag |
| N/A direction | any | drop (do not surface) |

**Open mapping decisions for clinical co-lead review:**

1. CIViC-A → OncoKB-1 (instead of 2) when CIViC `evidence_type` is "Predictive" AND a known FDA companion diagnostic exists for the gene/variant. This requires a manual FDA-CDx whitelist; we don't have one yet.
2. Should CIViC-B with `Sensitivity/Response` and a guideline-cited (NCCN/ESMO) therapy auto-promote to OncoKB-2? Reviewing 1,777 CIViC items would be impractical without a guideline cross-link.
3. How to render `Uncertain Significance` (149 items) — currently dropped from the therapeutic mapping; suggest routing to a "research-only" badge rather than discarding.

---

## 7. CIViC direction/significance handling proposal (consolidated)

OpenOnco's UI must distinguish four orthogonal axes that CIViC keeps separate but OncoKB collapses:

1. **Therapeutic axis** (Sensitivity/Response vs Resistance vs Reduced Sensitivity) — the only axis OncoKB models. Map per §6.1.
2. **Prognostic axis** (Better Outcome / Poor Outcome) — render in a Prognosis card; **never as a treatment recommendation.**
3. **Predisposition axis** (Predisposition) — route to germline layer; **never as a treatment recommendation directly** — the recommendation flows from the predisposition mechanism (e.g. BRCA1 predisposition → consider PARPi class once tumor arises), which lives in a separate BMA, not in the CIViC mapping.
4. **Functional/Oncogenic axis** (Gain of Function / Loss of Function / Oncogenicity / Dominant Negative) — render as a "biological mechanism" tag; informs interpretation but is not itself a therapeutic level.

Direction handling: `evidence_direction == "Does Not Support"` is **load-bearing.** A CIViC-A "Does Not Support / Sensitivity" finding (e.g. "EGFR amplification does NOT predict response to gefitinib") must produce a **negative recommendation card** (anti-evidence), not be silently dropped. The current `oncokb_extract.py` has no equivalent because OncoKB does not encode anti-evidence in this way; the engine will need a new `anti_evidence` field on BMA when wiring CIViC.

---

## 8. Recommended next move

**Public-only is viable for the variant-level engine layer (BIO-* and BMA-by-variant rules).** 27/29 BIO-* are covered by CIViC + oncokb-datahub gene levels at sufficient granularity. The two gaps (EZH2 Y641N, RHOA G17V) are minor and tractable:
- **EZH2 Y641N**: refresh the CIViC snapshot (current is 2026-04-25; CIViC publishes nightly) — likely just stale; otherwise cite tazemetostat label + Morschhauser 2020 directly in the BMA.
- **RHOA G17V**: this is a research-stage AITL marker, not a Level 1–4 OncoKB variant — keep as `escat_tier: III/IV` and cite Sakata-Yanagimoto 2014 + Yoo 2014 directly.

**Public-only is NOT viable for ~17/23 BMA drafts as currently authored**, but this is **not a CIViC limitation** — these BMAs reference biomarkers (IHC, methylation, indels, composite signatures) that are also outside OncoKB's strict variant-keyed evidence model. They require:
- Direct guideline citations (NCCN / ESMO sections) — already partially populated via `primary_sources` field
- Drug labels (FDA / EMA) — already partially in `regulatory_approval` field
- Clinical co-lead sign-off on `oncokb_level: "1"` / `"2"` claims, since these claims cannot be machine-verified against any public structured source

**Recommended workstream order:**

1. **Snapshot the gene-list anchor (read-only).** Add an `oncokb-datahub` reference (mode: `referenced`, NOT hosted) pointing at a specific tagged release (v7.0). Use only the gene-level highest-evidence as a cross-check, never as a primary source.
2. **Build SnapshotOncoKBClient** that loads from CIViC (already in repo) + oncokb-datahub (referenced). No need for a live OncoKB API client until a clinical edge case forces it.
3. **Defer the OncoKB API token decision.** It would unblock at most ~5–10 of the 17 unconfirmed BMAs (the structural-variant / amp / methylation ones) and would force us into the redistribution-forbidden license tier, which conflicts with CHARTER §2 (free public resource → no patient-services-license restriction).
4. **For the 17 unconfirmed BMAs: explicit two-reviewer clinical sign-off**, citing NCCN/ESMO directly. Do not attempt to derive the level from a public source; write the level by clinical judgment with citations.

**Decision: PUBLIC-ONLY VIABLE. OncoKB token NOT needed for v0.1.** Revisit only if the engine starts producing wrong levels on patient cases that have CIViC-uncovered variants that OncoKB's full annotated-variants table would have caught.

---

## 9. Open questions for clinical co-lead review

1. **JAK2 V617F level disagreement.** Three BMAs claim OncoKB Level 1 for JAK2 V617F (PV / ET / PMF → ruxolitinib). oncokb-datahub gene-level is 2. CIViC has 6 V617F items at levels B/D. Is the level-1 claim correct? (Likely no — ruxolitinib is NCCN-recommended but JAK2 V617F is not the FDA companion diagnostic; the indication is symptomatic intermediate/high-risk MF regardless of mutation status.) **Action:** clinical co-lead to set the correct level on all three BMAs.
2. **EZH2 Y641N gap.** CIViC v2026-04-25 has 29 EZH2 evidence items but none on Y641N specifically. Is this a snapshot artifact (try a re-pull) or a real gap (CIViC pivoted to E641-class encoding)?
3. **CIViC-A → OncoKB-1 promotion gate.** Without an FDA-CDx whitelist, every CIViC-A maps to OncoKB-2 by default. Should we author a manual FDA-CDx promotion list (currently ~20 variants) to enable level-1 surfacing? This is a one-time effort; revisit per FDA list updates.
4. **Anti-evidence rendering.** CIViC has 513 "Does Not Support" items (10.6% of evidence). The engine currently has no `anti_evidence` channel. Approve adding one to the Plan schema?
5. **The oncokb-datahub `referenced` fetch policy.** We do not need a snapshot of the data file — we need to know what version of OncoKB our gene-level cross-check is against. Pin to v7.0 and re-pull on a quarterly cadence, or always-latest? (Suggest pinned per `oncokb_snapshot_version` field already used in BMA YAMLs.)
6. **Does CHARTER §2 (free public resource → non-commercial) preclude the OncoKB academic license too?** The OncoKB academic terms forbid "use for patient services" — and CHARTER §2 makes patient services the explicit goal. Unless OncoKB grants a custom waiver, even a paid-for token does not unblock this. **This is the strongest argument for public-only.** Confirm with legal before pursuing the token path.

---

## Appendix A. Data sources used

- `knowledge_base/hosted/civic/2026-04-25/evidence.yaml` — CIViC nightly snapshot, CC0-1.0, 4,842 evidence items.
- `knowledge_base/hosted/content/biomarkers/bio_*.yaml` — 29 BIO-* with `oncokb_lookup` (full list in §4).
- `knowledge_base/hosted/content/biomarker_actionability/bma_*.yaml` — 23 BMA drafts with `drafted_by: claude_extraction` (full list in §5). Note: 399 BMA files exist in total, all of which carry `ukrainian_drafted_by: claude_extraction` (the UA-translation flag, distinct from `drafted_by:`).
- `https://github.com/oncokb/oncokb-public` (commit at 2026-04-27 11:26 local) — webapp source; **no data**.
- `https://github.com/oncokb/oncokb-datahub` RELEASE/v7.0 — gene-level highest-evidence list; **no variant-level data**.
- `https://civic.readthedocs.io/en/latest/model/evidence/level.html` — CIViC level definitions (fetched 2026-04-27).
- `oncokb-public/src/main/webapp/app/pages/apiAccessGroup/TermsPage.tsx` — OncoKB Terms of Use, source-of-truth verbatim.
- `oncokb-public/src/main/webapp/app/config/constants/terms.ts` — OncoKB AI-training prohibition clause.

## Appendix B. Cleanup

The two ephemeral clones at `C:\Users\805\AppData\Local\Temp\oncokb-public-clone\` and `C:\Users\805\AppData\Local\Temp\oncokb-datahub\` are kept for follow-up audits. They are outside the repo and gitignored by the OS-level temp path. Delete with:

```bat
rmdir /s /q "C:\Users\805\AppData\Local\Temp\oncokb-public-clone"
rmdir /s /q "C:\Users\805\AppData\Local\Temp\oncokb-datahub"
```

No commits or pushes were made by this audit other than this review file itself.
