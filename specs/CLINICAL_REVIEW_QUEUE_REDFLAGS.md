# Clinical Review Queue — RedFlags

**To:** OpenOnco clinical reviewer (hemato-oncologist).
**Context:** following a technical round of work on red-flag branching
(2026-04-25), items remain that **only a clinician can close** — because
CHARTER §8.3 prohibits LLMs from generating clinical recommendations without
human confirmation.

**What has already been done** (for context):
- RedFlag schema extended (`severity`, `priority`, `branch_targets`, `draft`).
- Engine supports multi-flag combos + deterministic conflict resolver.
- 21 active + 3 universal RFs have golden-fixture pos+neg tests (48 fixtures, 56 pytest-passing).
- 75 scaffolds generated for 15 diseases with zero coverage (all marked `draft: true`).
- CI validator blocks merges of non-draft RFs that lack sources / have invalid `clinical_direction` / have orphan `relevant_diseases`.
- Author guide: `specs/REDFLAG_AUTHORING_GUIDE.md` — read before editing.

**Total estimate**: ~110-160 hours of work across 4 queues (A → B → C → D).
A and B have the highest ROI (compliance + least effort).

---

## TL;DR — execution order

1. **A.** 18 RFs have only 1 source — add ≥1 additional Tier-1/2.
   *~9 hours content lookup*. Open targets per CLINICAL_CONTENT_STANDARDS §6.1.
2. **B.** 1 RF (RF-HBV-COINFECTION) remains orphaned — clinical decision:
   add a 3rd Indication to ALGO-HCV-MZL-1L OR reclassify as investigate
   + deprecate (a universal analogue already exists). *~2-4 hours*.
3. **C.** 75 scaffold stubs (15 diseases × 5 categories) — fill in the real
   trigger predicate, ≥2 sources, decision_tree wiring in the corresponding
   Algorithm. *~1-2 hours per RF — ~100-150 hours total*.
4. **D.** Sanity-review the 48 golden fixtures: do pos/neg cases cover
   realistic clinical scenarios?
   *~5-10 minutes per fixture — ~5-8 hours total*.
5. **E.** *(optional)* Review the 6 `investigate`-only RFs — do any of them
   actually need to shift? *~3-5 hours*.

Each task is a separate PR with two-reviewer sign-off (CHARTER §6.1).
Tasks **A**, **B**, and **D** can be done in parallel; **C** is disease-by-disease.

---

## A. Citation backfill — 18 single-cited RFs

CLINICAL_CONTENT_STANDARDS §6.1 requires **≥2 independent Tier-1/2 sources**
for clinical content. Each of the 18 RFs below currently has only 1 — the
task is to add ≥1 more.

**Action per item:**
1. Open the YAML.
2. Find a second Tier-1/2 source (ESMO guideline, ASCO, peer-reviewed
   Phase-3 RCT, FDA label) that supports the same clinical concept.
3. If the Source entity does not yet exist in `knowledge_base/hosted/content/sources/` —
   add it first per SOURCE_INGESTION_SPEC §8.
4. Add the ID to the `sources:` block.
5. Update `last_reviewed: "<today's date>"`.
6. PR + 2-reviewer merge.

**Acceptance:** `python -m knowledge_base.validation.loader` returns 0
contract warnings about "<2 sources" for this RF.

| # | RedFlag | YAML | Current source | What to add (hint) |
|---|---------|------|----------------|-------------------|
| 1 | RF-AGGRESSIVE-HISTOLOGY-TRANSFORMATION | rf_aggressive_histology_transformation.yaml | NCCN B-cell 2025 | ESMO MZL guideline 2024 (transformation criteria) |
| 2 | RF-AITL-AUTOIMMUNE-CYTOPENIA | rf_aitl_autoimmune_cytopenia.yaml | NCCN B-cell 2025 | ESMO PTCL guideline; where AIHA/ITP are described as AITL features |
| 3 | RF-AITL-EBV-DRIVEN-B-CELL | rf_aitl_ebv_driven_b_cell.yaml | NCCN B-cell 2025 | ESMO PTCL; WHO 5th-edition lymphoid classification |
| 4 | RF-AITL-HYPOGAMMA | rf_aitl_hypogamma.yaml | NCCN B-cell 2025 | ESMO PTCL; recurrent infection + IVIG indication |
| 5 | RF-BURKITT-HIGH-RISK | rf_burkitt_high_risk.yaml | NCCN B-cell 2025 | ESMO Burkitt 2024; CALGB-style risk stratification |
| 6 | RF-CHL-ADVANCED-STAGE | rf_chl_advanced_stage.yaml | NCCN B-cell 2025 | ESMO Hodgkin 2024 (Lugano staging III/IV → ABVD/escBEACOPP) |
| 7 | RF-CLL-HIGH-RISK | rf_cll_high_risk.yaml | NCCN B-cell 2025 | iwCLL 2018 guidelines (TP53/del17p definition) + ESMO CLL |
| 8 | RF-DLBCL-CNS-RISK | rf_dlbcl_cns_risk.yaml | NCCN B-cell 2025 | CNS-IPI primary publication (Schmitz et al. JCO 2016); ESMO DLBCL |
| 9 | RF-DLBCL-HIGH-IPI | rf_dlbcl_high_ipi.yaml | NCCN B-cell 2025 | POLARIX trial (Tilly et al. NEJM 2022); ESMO DLBCL |
| 10 | RF-FL-HIGH-TUMOR-BURDEN-GELF | rf_fl_high_tumor_burden_gelf.yaml | NCCN B-cell 2025 | GELF criteria primary publication (Brice et al. JCO 1997); ESMO FL |
| 11 | RF-FL-TRANSFORMATION-SUSPECT | rf_fl_transformation_suspect.yaml | NCCN B-cell 2025 | ESMO FL; histologic transformation review |
| 12 | RF-MCL-BLASTOID-OR-TP53 | rf_mcl_blastoid_or_tp53.yaml | NCCN B-cell 2025 | TRIANGLE trial; ESMO MCL 2024 |
| 13 | RF-MF-LARGE-CELL-TRANSFORMATION | rf_mf_large_cell_transformation.yaml | NCCN B-cell 2025 | ESMO MF/SS; large-cell transformation criteria |
| 14 | RF-MF-SEZARY-LEUKEMIC | rf_mf_sezary_leukemic.yaml | NCCN B-cell 2025 | ISCL/EORTC staging (Olsen et al. Blood 2007) |
| 15 | RF-MM-HIGH-RISK-CYTOGENETICS | rf_mm_high_risk_cytogenetics.yaml | NCCN MM 2025 | mSMART 3.0; IMWG R-ISS; ESMO MM |
| 16 | RF-MM-RENAL-DYSFUNCTION | rf_mm_renal_dysfunction.yaml | NCCN MM 2025 | IMWG renal failure consensus; ESMO MM |
| 17 | RF-TCELL-CD30-POSITIVE | rf_tcell_cd30_positive.yaml | NCCN B-cell 2025 | ECHELON-2 trial (Horwitz et al. Lancet 2019); ESMO PTCL |
| 18 | RF-WM-HYPERVISCOSITY | rf_wm_hyperviscosity.yaml | NCCN B-cell 2025 | IWWM consensus; ESMO WM |

**Total: ~9 hours** (≈30 min per RF: find the source, verify, add).

---

## B. Wiring orphan RFs

**Status (as of 2026-04-25):** of the 3 original orphans, **2 are already wired**
(see `docs/plans/archive/rf_wiring_audit_2026-04-25.md`). **1 open**
clinical-decision item remains:

| RF | Algorithm | Status |
|----|-----------|--------|
| RF-DECOMP-CIRRHOSIS | ALGO-HCV-MZL-1L | ✅ wired at step 1 |
| RF-TCELL-CD30-POSITIVE | ALGO-ALCL-1L | ✅ wired at step 1 |
| RF-HBV-COINFECTION | ALGO-HCV-MZL-1L | ⏳ **clinical decision needed** |

### B.1 — RF-HBV-COINFECTION (open question)

- **Trigger:** `hbsag=positive OR anti_hbc_total=positive`
- **Current `clinical_direction:`** `hold`
- **Problem:** ALGO-HCV-MZL-1L has 2 arms (ANTIVIRAL vs BR-AGGRESSIVE);
  neither is semantically "hold for HBV-prophylaxis." The `hold` direction
  does not fit the current architecture of this algorithm.

**Two options for the clinician to choose from:**

- **Option 1 — add a 3rd Indication.** Create a new Indication
  `IND-HCV-MZL-1L-HBV-PROPHYLAXIS-FIRST` that activates entecavir/TDF
  prophylaxis BEFORE continuing rituximab-based therapy. The decision_tree
  then adds a step: HBsAg+ → this new Indication; otherwise — existing flow.

- **Option 2 — reclassify as investigate** + remove `ALGO-HCV-MZL-1L` from
  `shifts_algorithm`. The RF remains a surveillance flag (an annotation in the
  Plan about the need for HBV prophylaxis); the regimen is chosen without change;
  premedication is added through a `supportive_care` entity.

  *This is the suggested option*, because **universal RF-UNIVERSAL-HBV-REACTIVATION-RISK**
  already exists with the same trigger and `clinical_direction: investigate` —
  the disease-specific RF-HBV-COINFECTION would then become redundant and can
  be **deprecated** (removed, leaving only the universal RF).

- **File:** `knowledge_base/hosted/content/redflags/rf_hbv_coinfection.yaml`
- **After the decision:** remove `("RF-HBV-COINFECTION", "ALGO-HCV-MZL-1L")` from
  the whitelist in `tests/test_redflag_fixtures.py::_KNOWN_ORPHANS`.

**Total B: ~2-4 hours** (one decision + either wiring, or YAML edit + tests).

---

## C. Fill in 75 scaffolds for 15 zero-coverage diseases

Each of these 15 diseases now has 5 RF stubs (one per category from
REDFLAG_AUTHORING_GUIDE §2). All are marked `draft: true` and CI warns
about them but does not block merges.

**Workflow per RF:**
1. Open the stub YAML.
2. Replace the placeholder `definition` and `definition_ua` with a disease-specific
   clinical statement (1 sentence describing what it captures).
3. Replace the placeholder `trigger.any_of[*].finding` with a real machine-evaluable
   predicate from a cited guideline. If the canonical `finding` key does not yet
   exist in DATA_STANDARDS — either choose a canonical one, or add it in §4.2.
4. Replace `SRC-TODO` with ≥2 real Tier-1/2 source IDs. Create a Source entity
   if one does not yet exist (SOURCE_INGESTION_SPEC §8).
5. Add a step in `<algorithm_id>.decision_tree` that references this RF and routes
   to a specific (existing or new) Indication.
6. Fill in `shifts_algorithm: [<algorithm_id>]`.
7. Set `last_reviewed: "<date>"`, `draft: false`.
8. Add a golden fixture in `tests/fixtures/redflags/<rf_id>/{positive,negative}.yaml`.
9. PR + 2-reviewer merge.

**Acceptance per RF:**
- `python -m knowledge_base.validation.loader` is clean.
- `pytest tests/test_redflag_fixtures.py` is clean.
- `python scripts/redflag_coverage.py` shows this RF in the appropriate matrix cell.

### List of diseases, each = 5 stubs

Categories in each disease: **organ-dysfunction**, **infection-screening**,
**high-risk-biology**, **transformation-progression**, **frailty-age**.
If a category is clinically not relevant — replace the stub with a `notes:` explanation.

| # | Disease | Algorithm | Files | Priority |
|---|---------|-----------|-------|----------|
| 1 | **PMBCL** | ALGO-PMBCL-1L | rf_pmbcl_*.yaml | **HIGH** — DA-EPOCH-R vs R-CHOP depends on bulky/PET2 |
| 2 | **PCNSL** | ALGO-PCNSL-1L | rf_pcnsl_*.yaml | **HIGH** — CrCl, age, MTX-eligibility — foundation of 1L |
| 3 | **B-ALL** | ALGO-B-ALL-1L | rf_b_all_*.yaml | **HIGH** — Ph+, MRD, age cutoff (pediatric vs adult) |
| 4 | **T-ALL** | ALGO-T-ALL-1L | rf_t_all_*.yaml | **HIGH** — CNS, ETP-ALL, age |
| 5 | **PTLD** | ALGO-PTLD-1L | rf_ptld_*.yaml | HIGH — EBV-status, IS-reduction, transplant-type |
| 6 | **HGBL-DH/-TH** | ALGO-HGBL-DH-1L | rf_hgbl_dh_*.yaml | HIGH — double/triple-hit; CNS prophylaxis |
| 7 | **NK/T-cell nasal** | ALGO-NK-T-NASAL-1L | rf_nk_t_nasal_*.yaml | HIGH — SMILE vs DDGP, asparaginase tolerance, EBV |
| 8 | **HCL** | ALGO-HCL-1L | rf_hcl_*.yaml | MEDIUM — cladribine vs vemurafenib (BRAF+) |
| 9 | **EATL** | ALGO-EATL-1L | rf_eatl_*.yaml | MEDIUM — rare, but without RFs the product is incomplete |
| 10 | **HSTCL** | ALGO-HSTCL-1L | rf_hstcl_*.yaml | MEDIUM |
| 11 | **ATLL** | ALGO-ATLL-1L | rf_atll_*.yaml | MEDIUM — IFN+AZT vs aggressive |
| 12 | **T-PLL** | ALGO-T-PLL-1L | rf_t_pll_*.yaml | MEDIUM — alemtuzumab eligibility |
| 13 | **Splenic MZL** | ALGO-SMZL-1L | rf_smzl_*.yaml | MEDIUM — HCV-status, autoimmune cytopenia |
| 14 | **Nodal MZL** | ALGO-NMZL-1L | rf_nmzl_*.yaml | LOW |
| 15 | **NLPBL** | ALGO-NLPBL-1L | rf_nlpbl_*.yaml | LOW — distinct from cHL |

Suggested sequence: High → Medium → Low.

**Special questions requiring a clinical decision per disease:**

- **PMBCL frailty stub:** PMBCL patients are usually young. Should the
  frailty RF be kept, or replaced with `notes:` explaining it is rarely relevant?
- **PCNSL infection-screening:** PCNSL does not use anti-CD20 in 1L, so
  HBV/HCV screening is less urgent. Should this be replaced with CMV/JC
  reactivation for rituximab-based regimens?
- **B-ALL/T-ALL frailty:** pediatric pathways do not use age cutoff in the
  usual sense. Explain in `notes:`.
- **PTLD organ-dysfunction:** transplant patients have organ-failure as a
  baseline — the RF is meaningful only for **trend changes**
  (worsening allograft function), not a static baseline.
- **HCL infection-screening:** purine analogs → opportunistic infections
  (PCP, Listeria) — is this screen-before-treatment or monitor-during-treatment?
- **NK/T-nasal frailty:** SMILE is very intensive — frailty cutoff is important.

**Total C: ~100-150 hours** (≈1-2 hours per RF × 75 RFs).

---

## D. Sanity-check 48 golden fixtures

The 48 fixtures (24 RFs × pos+neg) were generated automatically from the
trigger structure. Each includes: the minimum fields to trigger (positive)
or all fields false (negative). This is engine-correct, but **clinically
these are not always realistic patient profiles**.

**Action per fixture (~5-10 min):**
1. Open `tests/fixtures/redflags/<RF-ID>/positive.yaml` and `negative.yaml`.
2. Do the `findings` look like a **real patient profile**, not an "artificial" one?
3. If not — add 2-3 additional findings to make the scenario plausible
   (e.g., in RF-DLBCL-HIGH-IPI/positive, add LDH, ECOG, age, stage —
   so that `ipi_score: 3` makes sense in context).
4. Add a `notes:` field with a short comment describing the scenario.

Acceptance: subjectively — a clinician reads the fixture and thinks "yes,
I've seen a patient like this in the clinic."

**24 RFs with fixtures:**

```
RF-AGGRESSIVE-HISTOLOGY-TRANSFORMATION   RF-DLBCL-CNS-RISK              RF-MM-HIGH-RISK-CYTOGENETICS
RF-AITL-AUTOIMMUNE-CYTOPENIA             RF-DLBCL-HIGH-IPI              RF-MM-RENAL-DYSFUNCTION
RF-AITL-EBV-DRIVEN-B-CELL                RF-FL-HIGH-TUMOR-BURDEN-GELF   RF-TCELL-CD30-POSITIVE
RF-AITL-HYPOGAMMA                        RF-FL-TRANSFORMATION-SUSPECT   RF-WM-HYPERVISCOSITY
RF-BULKY-DISEASE                         RF-HBV-COINFECTION             RF-UNIVERSAL-HBV-REACTIVATION-RISK
RF-BURKITT-HIGH-RISK                     RF-MCL-BLASTOID-OR-TP53        RF-UNIVERSAL-INFUSION-REACTION-FIRST-CYCLE
RF-CHL-ADVANCED-STAGE                    RF-MF-LARGE-CELL-TRANSFORMATION  RF-UNIVERSAL-TLS-RISK
RF-CLL-HIGH-RISK                         RF-MF-SEZARY-LEUKEMIC          RF-DECOMP-CIRRHOSIS
```

**Total D: ~5-8 hours**.

---

## E. (Optional) Review the 6 `investigate`-only RFs

Currently 6 RFs have `clinical_direction: investigate` (i.e., surveillance-only,
no shift). Decision for the specialist:

| RF | Should it shift? |
|----|-----------------|
| RF-DLBCL-CNS-RISK | Yes, probably — IT-prophylaxis branch (R-CHOP+IT-MTX) |
| RF-MM-RENAL-DYSFUNCTION | Yes, probably — bortezomib-based instead of lenalidomide-based |
| RF-WM-HYPERVISCOSITY | Yes — plasmapheresis + rapid BTKi/anti-CD20 |
| RF-AITL-AUTOIMMUNE-CYTOPENIA | Possibly — IVIG ± steroids before induction |
| RF-AITL-EBV-DRIVEN-B-CELL | Possibly — add a rituximab arm |
| RF-AITL-HYPOGAMMA | Investigate — IVIG as supportive care, not a shift |
| RF-UNIVERSAL-INFUSION-REACTION-FIRST-CYCLE | Investigate (premedication, not a shift) |

If a decision is made "yes, shift" for any item → rework to
`intensify`/`de-escalate`/`hold` + wire into the decision_tree.

**Total E: ~3-5 hours**.

---

## Total effort

| Queue | Description | Estimate |
|-------|-------------|----------|
| A | Citation backfill (18 RFs) | ~9 hrs |
| B | Resolve 1 remaining orphan (RF-HBV-COINFECTION) | ~2-4 hrs |
| C | Fill in 75 scaffolds | ~100-150 hrs |
| D | Sanity-check 48 fixtures | ~5-8 hrs |
| E | Re-classify 6 investigate-flags | ~3-5 hrs |
| **Total** | | **~120-175 hrs** |

Realistically — **3-6 weeks of part-time work** with two-reviewer merge on each PR.

---

## Running locally

```bash
# Validate KB after every edit
python -m knowledge_base.validation.loader knowledge_base/hosted/content

# RF-specific tests
python -m pytest tests/test_redflag_fixtures.py -v

# Coverage report — confirm coverage is growing
python scripts/redflag_coverage.py
```

---

## Contacts / questions

- Schema questions: `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` §9
- Authoring guide: `specs/REDFLAG_AUTHORING_GUIDE.md`
- Source ingestion: `specs/SOURCE_INGESTION_SPEC.md` §8
- Citation standards: `specs/CLINICAL_CONTENT_STANDARDS.md` §6.1
- Engine code: `knowledge_base/engine/redflag_eval.py`,
  `knowledge_base/engine/algorithm_eval.py`
