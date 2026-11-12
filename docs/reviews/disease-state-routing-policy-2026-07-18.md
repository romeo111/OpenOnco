# Unstaged Patients and Algorithm Routing — Clinical Policy Decision Required

**Date:** 2026-07-18
**Status:** DECISION REQUIRED — CHARTER §6.1 (two of three Clinical Co-Leads)
**Plus:** one live patient-facing defect on `master`, §0 — not a policy question
**Engine/schema half:** done, ungated (this branch)
**Prior work:** `docs/plans/stateless_disease_state_routing_2026-07-18-1620.md`,
commit `510576ae0c` (ambiguity warning, on `claude/gallery-examples-outdated-eb7f06`)

All figures below were re-derived on this branch and independently
re-verified; §8 records where they differ from the earlier plan and why.

---

## 0. Live defect on `master` — fix before deciding anything

`examples/patient_cervical_locally_advanced.json` records
`findings.stage: "FIGO IIIB"` and **no `disease_state`**. It is in the public
showcase set (`scripts/site_cases.py:109`, `badge="Treatment Plan"`), and its
card promises *"cisplatin-based CCRT + brachytherapy; pembrolizumab maintenance
(KEYNOTE-A18)"*.

What the engine actually produces for it, on this branch and on `master`:

```
algorithm_id : ALGO-CERVICAL-METASTATIC-1L
warnings     : []
```

The built page `docs/cases/cervical-locally-advanced.html` — on `master` —
serves `REG-PEMBRO-PACLI-CARBO-BEV-CERVICAL`, palliative systemic therapy, to a
**FIGO IIIB (curable, locally advanced)** patient, under a heading promising
curative chemoradiation. No warning fires, because the selected algorithm is the
state-agnostic catch-all.

**This is already fixed on `claude/gallery-examples-outdated-eb7f06`** (that
branch sets `disease_state: locally_advanced`), and deliberately *not*
duplicated here — two branches editing one example file is the coordination bug
CLAUDE.md warns about. It needs merging, not re-fixing. Until it merges, the
public site contradicts itself on a curable presentation.

Note this is a *derivation*, not a staging call: the clinician-recorded stage is
already in the file. See Option D.

---

## 1. How routing works today

`engine/plan.py::_find_algorithm` resolves in three tiers:

```
state_matched    algorithm state == patient state       → wins
state_agnostic   algorithm declares no state            → next
state_specific   legacy fallback                        → last resort
```

Two precisions that matter for costing the options:

- **The third tier fires only when the patient has no `disease_state` at all**
  (`None`, or empty/whitespace, which is normalised to `None` at `plan.py:180`).
  A patient who *has* a state matching no algorithm, in a group with no
  catch-all, gets `None` — not a fallback.
- **Ties are broken by `entities_by_id` insertion order at every tier**, not
  only the legacy one. That order is `sorted()` over **full `Path` objects**
  (`validation/loader.py:339`), within each entity directory. For `algorithms/`
  this currently coincides with alphabetical *filename* order only because the
  directory is flat (189 files, no subdirectories) and every filename is
  lowercase. The coincidence is incidental — `redflags/` already diverges via
  its `universal/` subfolder — so read the tables below as "loader insertion
  order", which today happens to be filename order.

The consequence that drives everything else: **omitting
`applicable_to_disease_state` is not "unspecified"**. It makes that algorithm
the catch-all that wins for every unstaged patient.

---

## 2. The KB already runs two different de facto policies

Nine (disease, line) groups are state-ambiguous. They split into two shapes that
behave differently:

| Shape | Groups | Unstaged patient gets | Chosen by |
|---|---|---|---|
| **Catch-all** — one algorithm omits the key | NSCLC, gastric, melanoma, PDAC, cervical (all L1) | the catch-all | KB authoring |
| **All-state-specific** — every algorithm declares a state | CRC L1, esophageal L1, prostate L1, breast L2 | legacy fallback | **loader insertion order** |

Across the **930** `examples/*.json` on this branch, **86 stateless profiles
land in a state-ambiguous group — 61 via a catch-all, 25 via the fallback.**

**The 61 (catch-all), by disease:** NSCLC 17, gastric 13, melanoma 12, PDAC 12,
cervical 7 — every one routed to that disease's `*-METASTATIC-1L`.

**The 25 (insertion-order fallback):**

| Disease | n | Routed to | What that algorithm actually is |
|---|---|---|---|
| CRC L1 | 10 | `ALGO-CRC-ADJUVANT` | adjuvant post-R0 stage II–III — **curative**, assumes resection done |
| Prostate L1 | 8 | `ALGO-PROSTATE-MCRPC-1L` | castration-**resistant** — the *most advanced*, palliative state; assumes prior ADT progression. The passed-over sibling (mHSPC) is the earlier one |
| Esophageal L1 | 6 | `ALGO-ESOPH-DEFINITIVE-1L` | definitive CRT for cT4b / medically inoperable M0 — **curative**, locally advanced |
| Breast L2 | 1 | `ALGO-BREAST-HER2-POS-2L` | 2L metastatic palliative; the discriminating axis here is **receptor subtype, not stage** |

**The failure is arbitrary intent in both directions, not a uniform curative
bias.** Two of the four overtreat (curative intent for a possibly-metastatic
patient); one undertreats by presuming castration resistance that may not have
occurred; one assigns therapy on the wrong axis entirely. Any framing of policy
A as "move the four off curative defaults" is wrong for half of them.

**The sharpest case:** `examples/variant_breast_relapsed_2l.json` records
`BIO-BRCA-GERMLINE: positive`, no receptor status, no `disease_state`. It is
routed to the HER2-positive algorithm by insertion order. Both emitted
indications declare a hard required `BIO-HER2-SOLID` biomarker the patient does
not have, and the engine does not enforce that at track emission — so a
HER2-targeted regimen is proposed for a patient with no HER2 result.

### Why this matters to the decision

The earlier plan asked whether the five catch-all diseases represent a
deliberate house convention. The evidence says **the KB is already internally
inconsistent**: 61 profiles follow policy A, 25 already follow policy B by
insertion order. Whatever is chosen, four groups need changing regardless — the
status quo is not a coherent position that can simply be ratified.

**Adjacent, no profile reaches it today:** three further multi-member groups at
line 0 — `(DIS-CRC, 0)` n=11, `(DIS-BREAST, 0)` n=7,
`(DIS-SOFT-TISSUE-SARCOMA, 0)` n=3 — are *uniformly* state-agnostic, so they are
not state-ambiguous by the definition above, but they too resolve to
`state_agnostic[0]` = the alphabetically-first file. These are risk/prevention
models (Gail, Tyrer-Cuzick, PREMM5, Chompret). No current profile has
`line_of_therapy: 0`. Recorded so it is not rediscovered as a new finding.

---

## 3. Today, all 86 are silent to a clinician

`render.py` surfaces `plan_result.warnings` **only** on the `plan is None`
branch. So:

- the **61** catch-all profiles emit no engine warning at all; and
- the **25** fallback profiles do emit the load-order warning at
  `plan.py:908-915` — but it reaches developers and tests, **not** anyone
  reading a rendered plan.

(For completeness: **32** profiles trigger that engine warning overall — the 25
above plus 7 in *single-algorithm* state-specific groups: CRC L2 ×5,
prostate L2 ×1, soft-tissue sarcoma L2 ×1. Those 7 are outside the ambiguity
scope of this memo.)

Commit `510576ae0c` on the gallery branch widens the warning to cover the
ambiguous-choice case. It does not change routing, and it does not make anything
visible to a clinician.

---

## 4. The options

| | Policy | Effect on the 86 | Cost |
|---|---|---|---|
| **A** | Default to palliative | 25 change | An unstaged **curable** patient gets a palliative plan. Undertreatment. |
| **B** | Default to curative-intent | 61 change | An unstaged **incurable** patient gets curative chemoradiation / surgery-assuming adjuvant regimens. Overtreatment and toxicity without benefit. |
| **C** | Refuse to route | see below — **not** simply "all 86" | Largest visible regression. Asserts nothing clinically. |
| **D** | Derive state from the recorded stage | 16 become derived rather than guessed; **2 routings correct**, 14 confirmed | Does not answer the question for the remaining 70. Not mutually exclusive with A/B/C. |

### Option C — the blast radius depends on which branch is cut

The earlier framing ("a change to `_find_algorithm`'s legacy fallback") and the
outcome ("all 86 produce no plan") are **not the same change**:

| What is cut | Profiles that stop routing |
|---|---|
| Legacy fallback only (`plan.py:205-206`) | **25.** The other 61 keep routing to the catch-all exactly as today, still with no warning. |
| Legacy fallback + an **ambiguity-aware** guard on the catch-all | **86** — the intended reading. |
| Legacy fallback + naive suppression of `state_agnostic` (`plan.py:200-201`) | **763.** 677 further stateless profiles in *unambiguous* groups lose routing too (`auto_aml.json` → `ALGO-AML-1L`, `auto_dlbcl_nos.json` → `ALGO-DLBCL-1L`, …). |

Only the middle row costs 86. The engine work is the ambiguity-aware guard, and
it is meaningfully more than deleting two lines.

**There is also no "disease_state required" error today.** What
`plan.py:902-907` emits is a warning reading `No Algorithm found for
disease=DIS-CERVICAL, line_of_therapy=1` — the state suffix is empty precisely
*because* `disease_state` is `None`, so the message never mentions it. It is
textually indistinguishable from a genuine KB coverage gap. Making C produce an
actionable message is additional scope.

### Option D — read the stage the record already contains

**16 of the 86 are not actually unstaged.** They carry a clinician-recorded
`findings.stage` that the router never reads:

- **14 are stage IV** → derived state `metastatic` → **routing unchanged**, but
  explicit and verifiable instead of guessed.
- **2 are stage III and currently mis-routed**, and both self-correct:

```
patient_cervical_locally_advanced.json   ALGO-CERVICAL-METASTATIC-1L → ALGO-CERVICAL-LOCALLY-ADVANCED-1L
patient_melanoma_adjuvant_pembro_stage_iii.json  ALGO-MELANOMA-METASTATIC-1L → ALGO-MELANOMA-ADJUVANT-1L
```

The first of those is the live public defect in §0.

Deriving `disease_state` from a stage a clinician already recorded is **not** an
LLM staging call, so CHARTER §8.3 does not block it — that constraint is what
rules out inventing stages for the six stubs (§7), and it does not apply here.
A declarative stage→state mapping in the KB would be §6.1 clinical content and
must be authored per disease (FIGO for cervical, AJCC for melanoma, etc.), not
inferred generically.

D removes guessing for 16 and fixes 2 wrong plans at low blast radius, but it
does **not** answer what happens to the other 70. It is a complement to A/B/C,
not a substitute.

### Do not reach B by accident

Adding `applicable_to_disease_state: metastatic` to
`algo_cervical_metastatic_1l.yaml` looks like the obvious fix. **It is not.** It
does not make stateless patients unroutable; it drops them into the legacy
fallback. Verified by patching the entity in memory and re-routing
`examples/auto_cervical.json`:

```
BEFORE (KB as-is)     -> ALGO-CERVICAL-METASTATIC-1L       (palliative)
AFTER  (obvious fix)  -> ALGO-CERVICAL-LOCALLY-ADVANCED-1L (curative CRT)
```

Two qualifications, both verified:

- The flip is **warning-flagged, not fully silent** — after the edit the
  selected algorithm declares a state, so `plan.py:908-915` fires. Per §3 that
  warning still reaches no clinician, and a complete curative-CRT plan is
  returned regardless. (The *current* state is genuinely silent.)
- The same edit makes patients with `disease_state: recurrent` or `persistent`
  **unroutable** — states the metastatic algorithm's own decision tree
  explicitly covers.

---

## 5. What changed on this branch (ungated)

`applicable_to_disease_state` was a **live routing key that no schema
declared**. `Base` sets `extra="allow"`, so any value — including a typo —
loaded silently.

It is now declared on the `Algorithm` model as a closed `Literal` of the 15
values in use (`knowledge_base/schemas/algorithm.py`,
`tests/test_algorithm_disease_state_registry.py`). Full KB loads with 0 schema
errors; routing is unchanged for all 930 profiles.

**Why a typo mattered, stated correctly.** The loader catches `ValidationError`
and `continue`s (`loader.py:361-363`), so an unregistered value now **drops the
whole algorithm out of `entities_by_id`** — which `_find_algorithm` iterates.
Concretely, typoing `TNBC` → `TNBc` flips breast L2 TNBC routing to `None`.
Before this change the same typo left the algorithm loaded but permanently
unmatchable, and — in a catch-all group — removed the catch-all, producing
exactly the silent palliative→curative flip above. Either way a typo changed
patient routing; now it fails at load instead. Routing is unchanged today
because all in-use values are registered, not because a Literal is structurally
incapable of affecting routing.

### Flagged, not fixed — the key spans two axes

The 15 values are not one taxonomy: stage/intent (`adjuvant`, `advanced`,
`locally_advanced`, `metastatic`, `resectable`, `resectable_perioperative`,
`unresectable_definitive`); disease-prefixed compounds
(`pdac_lapc_unresectable`, `pdac_resectable_or_borderline`,
`rectal_locally_advanced_tnt`) that re-encode the disease already named in
`applicable_to_disease`; hormone-sensitivity states (`mCRPC`, `mHSPC`); and
**receptor subtype, which is not a disease state at all** (`TNBC`,
`HER2-positive`, `HR-positive_HER2-negative`).

The field is in practice a general "which of several same-disease-and-line
algorithms applies" discriminator, and its name describes only the first group.
Normalising the values would move patients between algorithms → §6.1. Left
alone.

---

## 6. Out of scope, raised for reviewers

- **KEYNOTE-A18 not modelled.** FDA approved pembrolizumab + chemoradiation for
  FIGO 2014 stage III–IVA cervical cancer in January 2024.
  `algo_cervical_locally_advanced_1l.yaml` models cisplatin-CRT only — while the
  §0 public card already advertises KEYNOTE-A18.
- **Required-biomarker enforcement.** The breast case in §2 shows indications
  with a hard required biomarker being emitted for a patient lacking it.
  Independent of this policy question.
- **The FIGO split itself is correct.** ESMO-family guidance confirms IB3–IVA →
  definitive chemoradiation, IVB/recurrent → palliative systemic. Both cervical
  algorithms' prose scope statements already match. NCCN was unreachable
  (registration-walled).

---

## 7. The six stateless cervical stubs stay unstaged

`auto_cervical.json` and `variant_cervical_{high_risk,frail,organ_dysf,
infection_hbv,biomarker_act}.json` contain **no** stage field of any kind.
Assigning one would be an LLM making a staging call — CHARTER §8.3. They are
badged "Auto-stub"/"Variant" in `scripts/site_cases.py` and none is in the
public gallery.

This is why Option D is scoped to *deriving* from a recorded stage: it covers
`patient_cervical_locally_advanced.json` (FIGO IIIB on file) and leaves these
six untouched. The seventh cervical profile is not one of the six.

---

## 8. Measurement notes

- **Denominator.** 930 `examples/*.json` on this branch. The plan's "808" was
  stale; the 86 numerator is unaffected.
- **Scope.** The plan reported 92 affected across 10 diseases (including 1
  soft-tissue sarcoma); this branch measures **86 across 9**. The difference is
  branch drift — the plan was measured on
  `claude/gallery-examples-outdated-eb7f06`, which carries example-file changes
  (`84ae3a11e0`) not present here. `ALGO-STS-ADVANCED-2L` is the only algorithm
  for its disease and line here, so sarcoma is unambiguous on this branch.
  Re-measure once the branches converge; the shape of the finding is unaffected.
- **Test suite.** 8 failures / 4050 errors are **pre-existing** — identical
  counts on untouched `f5ba1435bb` (build-size, bundle, and one curated e2e
  test). This branch adds 26 passing tests and changes nothing else.

## Reproduction

```bash
C:/Python312/python.exe -m pytest tests/test_algorithm_disease_state_registry.py \
                                  tests/test_engine_find_algorithm.py -q
```

Group/profile sweeps are reproducible from `_find_algorithm` plus
`load_content`; the tables above record their outputs.
