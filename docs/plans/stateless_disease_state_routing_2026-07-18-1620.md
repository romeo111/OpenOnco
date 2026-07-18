# Unstaged patients silently routed to palliative algorithms

**Created:** 2026-07-18-1620
**Status:** engine half DONE; KB policy question OPEN
**Gate:** the KB half is CHARTER §6.1 clinical content
**Origin:** gallery audit on `claude/gallery-examples-outdated-eb7f06`

---

## 1. The defect

A patient profile with no `disease_state` can be routed to a **palliative**
first-line algorithm while a **curative-intent** algorithm exists for the same
disease and line — with no warning of any kind.

`knowledge_base/engine/plan.py` `_find_algorithm` resolution order:

```
state_matched   (algo state == patient state)   → wins
state_agnostic  (algo declares no state)        → next
state_specific  (legacy fallback, load-order)   → last resort
```

For cervical line 1 the KB has two algorithms:

| Algorithm | `applicable_to_disease_state` | Intent |
|---|---|---|
| `ALGO-CERVICAL-LOCALLY-ADVANCED-1L` | `locally_advanced` | curative chemoradiation |
| `ALGO-CERVICAL-METASTATIC-1L` | *(absent)* | palliative systemic |

The palliative one declares no state, so it is the **state-agnostic catch-all**
and wins for any patient who has not recorded a stage.

Confirmed by running the engine on all six stateless cervical stubs
(`examples/auto_cervical.json`, `examples/variant_cervical_{high_risk,frail,
organ_dysf,infection_hbv,biomarker_act}.json`): every one produced
`ALGO-CERVICAL-METASTATIC-1L` → a single
`IND-CERVICAL-METASTATIC-1L-PEMBRO-CHEMO-BEV` track, **with zero warnings**.

The pre-existing warning at `plan.py` only fires when the *selected* algorithm
declares a state — which is exactly the case that does not happen here. The
misroute was structurally invisible.

### Scope is not cervical

Measured across all 808 example profiles: **92 profiles across 10 diseases**
select an algorithm while the state choice is ambiguous — NSCLC (17), CRC (15),
gastric (13), melanoma (12), PDAC (12), prostate (9), cervical (6), esophageal
(6), soft-tissue sarcoma (1), breast (1). Cervical is a symptom, not the bug.

---

## 2. What was already fixed (engine, ungated)

**Done in this branch.** `_algorithm_state_choice_is_ambiguous()` added to
`plan.py`; the missing-`disease_state` warning now also fires when more than one
algorithm serves (disease, line) with differing state scopes.

- **Routing is unchanged.** Every profile selects exactly the same algorithm as
  before. Verified by re-running the six cervical stubs plus a plan-fingerprint
  diff.
- **No public noise.** `render.py` emits `plan_result.warnings` only on the
  `plan is None` branch, so profiles that produce a plan surface the warning to
  developers and tests, not to site visitors.
- Net effect: 92 profiles that were silently ambiguous now say so.

This does **not** fix the routing. It converts a silent wrong default into a
visible one, which is the most that can be done without a clinical decision.

Also fixed separately: `examples/patient_cervical_locally_advanced.json` (the
one gallery-featured cervical case) now sets `disease_state: locally_advanced`
and routes correctly to `ALGO-CERVICAL-LOCALLY-ADVANCED-1L`.

---

## 3. The open question — for the Clinical Co-Leads

**What should happen to a patient whose disease state is unknown?**

Three candidate policies:

| | Policy | Consequence |
|---|---|---|
| **A** | Default to palliative (status quo) | An unstaged curable patient gets a palliative plan. Silent until now. |
| **B** | Default to curative-intent | An unstaged incurable patient gets a curative plan. Arguably worse. |
| **C** | Refuse to guess — no algorithm, explicit "state required" error | No plan until the clinician supplies a stage. Safest, most disruptive. |

**Do not reach policy B by accident.** The tempting fix — adding
`applicable_to_disease_state: metastatic` to `algo_cervical_metastatic_1l.yaml`
— does *not* leave stateless patients unroutable. It drops them through
`plan.py`'s legacy fallback, which returns the first state-specific algorithm
**by alphabetical filename order** — i.e. `ALGO-CERVICAL-LOCALLY-ADVANCED-1L`.
A stateless patient would then silently receive a **curative-intent
cisplatin-chemoradiation** default, chosen by filename sort. That is policy B,
arrived at by accident, and it is a worse failure mode than what we have.

If the answer is C, the correct change is to `plan.py`'s legacy fallback
(refuse rather than guess) — **engine work, not gated**, and it must be
evaluated against all 92 affected profiles, not just cervical.

### Apply the answer across all five, not just cervical

Five diseases share the state-agnostic-metastatic-catch-all shape. Their
consistency is itself evidence this may be a deliberate house convention rather
than five independent oversights — no documentation of the intent was found
either way. Patching cervical alone would make the KB internally inconsistent.

---

## 4. The staging split is correct — no KB change needed there

Checked against ESMO-family guidance (NCCN was unreachable — it requires
registration):

- **Locally advanced = FIGO 2018 IB3–IVA** → definitive cisplatin-based
  chemoradiation + brachytherapy
- **FIGO IVB / recurrent** → palliative systemic therapy

The KB matches: `algo_cervical_metastatic_1l.yaml` scopes itself to "FIGO IVB,
or recurrent not amenable to curative-intent surgery/RT", and its step-1 comment
redirects "Locally advanced (FIGO IB3-IVA, curative intent)" elsewhere. Both
algorithms' prose scope statements are already correct and reviewed
(`last_reviewed: 2026-05-04` / `2026-04-26`).

**Separate gap noted for reviewers, not part of this plan:** FDA approved
pembrolizumab + chemoradiation for FIGO 2014 stage III–IVA in January 2024
(KEYNOTE-A18). `algo_cervical_locally_advanced_1l.yaml` models cisplatin-CRT
only and does not yet include it.

---

## 5. Do not assign stages to the six stubs

None of the six stateless cervical files contains any basis for inferring a
stage — no `findings.stage`, no staging-adjacent field. Assigning one would be
an LLM making a staging call, which CHARTER §8.3 forbids.

They are mechanical template output, as evidenced by all six having declared a
female-only cancer in a male patient (fixed separately in this branch — see
`docs/plans/example_profile_sex_integrity_2026-07-18-1625.md`).

Mitigating context: all six are already badged "Auto-stub"/"Variant" in
`scripts/site_cases.py` with summaries stating they are synthetic and not for
clinical decisions, and none is in the public gallery.

Two defensible options that avoid a clinical assertion, once the policy question
above is answered:

- Leave the stage absent and treat the new routing warning as the intended
  visible-failure signal (current state).
- Exclude auto-stub/variant profiles from public surfaces for diseases whose
  line-1 routing is state-ambiguous.

---

## 6. Secondary finding — the routing key is unvalidated

`applicable_to_disease_state` is a live routing key read by `_find_algorithm`,
but it is an undeclared extra field on the Algorithm model: no schema entry, no
enum, no validator. A typo silently makes an algorithm unroutable rather than
failing loudly. Distinct values in use today are inconsistent in exactly the way
an unvalidated free-text key invites.

Declaring it on the Algorithm schema with an enum is **engine/schema work, not
gated clinical content**, and is worth doing regardless of which policy wins.

---

## 7. Suggested branch

```
fix/disease-state-routing-policy-2026-07-18-1620
```

Never commit to `master`; never `git add -A`; never `--no-verify`.
