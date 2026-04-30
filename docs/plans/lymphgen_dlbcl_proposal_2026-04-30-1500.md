# DLBCL LymphGen subtype classifier — proposal (deferred) — 2026-04-30-1500

**Status:** deferred / parked. Not on v0.1 or v0.2 roadmap. Document exists so the idea isn't lost.
**Parent:** `docs/plans/biomarker_expansion_roadmap_2026-04-30-1500.md` workstream W6.
**Background discussion:** chat session on 2026-04-30 (specialist-gap audit of `knowledge_base/hosted/content/biomarkers/`).

## What it is

LymphGen is the Schmitz/Wright (NIH, NEJM 2018 → Cancer Cell 2020) molecular classifier for DLBCL based on 7 genetic subtypes:

| Subtype | Genetic core | COO overlap | Therapeutic signal (research-tier) |
|---|---|---|---|
| **MCD** | MYD88 L265P + CD79B mutation | ABC / non-GCB | BTKi-sensitive (PHOENIX MCD subset) |
| **BN2** | BCL6 fusion + NOTCH2 mutation | mixed | partial BTKi sensitivity |
| **N1** | NOTCH1 mutation | ABC | BTKi-responsive |
| **EZB** (MYC+ / MYC−) | EZH2 Y641 + BCL2 translocation | GCB | tazemetostat / venetoclax in trials |
| **ST2** | TP53 inactivation, aneuploid | "secondary" | poor prognosis baseline |
| **A53** | aneuploid + TP53 (older pts) | ABC | poor; salvage focus |
| **Other** | unclassified | mixed | Hans-default |

## Why it's not in v0.1 / v0.2

### 1. NCCN/ESMO 1L therapy doesn't yet stratify by LymphGen

Standard 1L for DLBCL-NOS is **R-CHOP** or **pola-R-CHP** (POLARIX) for all-comers, with COO modifications using **Hans algorithm (GCB vs non-GCB)** — not LymphGen.

POLARIX subgroup analysis showed ABC benefit of pola-R-CHP. PHOENIX (R-CHOP + ibrutinib) failed overall but showed signal in MCD/N1 subset. Both are **post-hoc** signals, not prospective stratification recommendations.

### 2. No FDA-approved LymphGen-targeted therapy

Adding the classifier without legal therapeutic options gives:
- Information for the MDT brief
- Zero new routing through the algorithm
- Potential confusion if clinicians expect actionable Tx-recommendation downstream

### 3. Engine architecture gap

LymphGen subtype is a **composite classifier** that requires multi-gene + copy-number + priority resolution:

- **MCD vs ST2 priority** when both MYD88L265P and TP53-inactivation present
- **EZB-MYC+ vs HGBL-DH overlap** when MYC + BCL2 + EZH2 all positive
- **Aneuploidy proxy** — A53 / ST2 stratification needs CN data we don't currently model

Current engine RF triggers are flat-finding lookups (`finding: <key> value: <X>`), not multi-step classifier pipelines. LymphGen would require either:

- **(a) Pre-compute upstream:** patient JSON imports the already-classified `lymphgen_subtype: "MCD"` from a lab pipeline. Engine just reads it. Pushes work to data-entry.
- **(b) Composite RF clauses:** `all_of: [MYD88-L265P, CD79B-mutation]` → RF-DLBCL-MCD-LIKE. Works for single subtypes; weak at overlap resolution.
- **(c) New engine layer:** classifier-step between findings and algorithm evaluation. PROD-level architectural change.

### 4. Existing `dlbcl_coo_hans` covers the actionable subset

Hans IHC (CD10 / BCL6 / MUM1) already segments DLBCL into GCB / non-GCB, which is what NCCN routes by today. Adding LymphGen on top duplicates effort without clinical-decision payoff.

## Trigger conditions for revisiting this proposal

Any of these would justify implementation:

1. **FDA approval of a LymphGen-subtype-targeted therapy.** Most likely candidates over next 1-2 years:
   - tazemetostat (EZH2i) for EZB-subtype 2L+ DLBCL (currently FL-only)
   - venetoclax + standard induction for EZB or BN2
   - ibrutinib for MCD specifically (post-PHOENIX subgroup confirmation)
2. **NCCN or ESMO formalizes LymphGen as a recommended stratifier** in any DLBCL setting.
3. **Engine extension** to support composite biomarker classifiers (not just for LymphGen — would also enable HRD scoring methodology distinction, AML CEBPA-biallelic, MDS IPSS-M scoring, prostate AR-V7 ARSI-resistance detection).
4. **Strong clinical co-lead request** with concrete use-case (e.g., a DLBCL-focused tumor-board protocol that depends on LymphGen subtype to triage CAR-T eligibility ordering).

## What partial implementation would look like (if deferred trigger fires)

If only condition (1) fires for a single subtype (e.g., EZB-targeted tazemetostat):

- Add **EZH2 Y641 + BCL2 translocation + MYC rearrangement** as a composite RF (option (b) above) firing `RF-DLBCL-EZB-LIKE-EZH2-INHIBITOR-CANDIDATE`
- Wire that RF into a NEW `IND-DLBCL-2L-EZB-EZH2I-TAZEMETOSTAT` indication
- Algorithm extension in `algo_dlbcl_2l.yaml`
- Do NOT add full LymphGen classifier yet — narrow the work to the subtype that has therapy

If condition (3) fires (engine layer):

- Major refactor of `knowledge_base/engine/redflag_eval.py` + `algorithm_eval.py` to support classifier nodes
- Add `classifiers/` directory under `knowledge_base/hosted/content/`
- Add `DIS-DLBCL-NOS.molecular_subtypes` block (analog to `DIS-NSCLC.molecular_subtypes`)
- Add 7 subtype entities + classification rules
- Wire algorithm to consult classifier output

## Standalone biomarkers that ARE worth adding now (independently of LymphGen)

Several individual genes underlying LymphGen subtypes have value as standalone biomarkers even without classifier integration:

- **CD79B mutation** — currently only `cd79b_ihc` exists in KB; the gene-mutation form is the LymphGen-relevant one (W3 Tier 2 candidate)
- **NOTCH2 mutation** — LymphGen BN2; W3 candidate
- **BCL6 fusion** — `bcl6_rearrangement` exists; ensure FISH+NGS distinction (W3 candidate)
- **EZH2 Y641** — already in KB ✓ (used for FL tazemetostat)
- **MYD88 L265P** — already in KB ✓ (used for WM)
- **TP53 mutation** — already in KB ✓
- **MYC rearrangement / double-hit** — already in KB ✓

So the genetic substrate for LymphGen is roughly 70-80% present in KB already. The missing piece is the **classifier-level entity** + **engine support for composite scoring**. That's where the architectural cost sits, not in the gene-level biomarkers.

## Open questions parked here

1. Should we add a `bio_dlbcl_lymphgen_subtype` entity NOW as a placeholder (subtype string field, no engine evaluation), so patient JSONs can carry pre-computed classifier results from a future lab pipeline? Pros: future-proofs data model. Cons: adds entity that engine can't yet act on.
2. If we do (1), what's the canonical vocabulary? `MCD | BN2 | N1 | EZB-MYC+ | EZB-MYC- | ST2 | A53 | Other` — NIH 2020 paper's naming.
3. How does this interact with the future `kb_data_quality_plan_2026-04-29.md` Q1 evidence requirement? CIViC has individual gene/variant entries (MYD88 L265P, etc.) but not LymphGen-subtype entries. So Q1 evidence for a LymphGen entity would be guideline-level (NIH papers), not CIViC.

## Maintainer note

Re-read this document at every v0.x → v(0.x+1) milestone planning meeting. Check trigger conditions. If still deferred, update "as of YYYY-MM-DD" status. If triggered, fork into an implementation plan.
