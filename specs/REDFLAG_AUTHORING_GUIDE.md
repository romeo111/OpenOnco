# REDFLAG_AUTHORING_GUIDE — How to Add a RedFlag

**Status:** v0.1 (P0). **Owner:** Clinical Co-Leads (per CHARTER §6.1).
**Prerequisite reading:** `KNOWLEDGE_SCHEMA_SPECIFICATION.md` §9 (RedFlag),
`CLINICAL_CONTENT_STANDARDS.md` §2/§4/§6, `CHARTER.md` §6 / §8.3.

This document is an operational guide for content authors and CI gates. It
describes **what a RedFlag is, the minimum requirements every new RedFlag must meet,
and how it is wired into `Algorithm.decision_tree`**.

---

## 1. What a RedFlag is (and what it is not)

A **RedFlag** is a machine-evaluable clinical finding that, when triggered in a
patient's profile, **shifts the Indication selected** within an existing Algorithm.
A RedFlag **does not prescribe treatment by itself**.
A RedFlag is an **input** to the decision_tree, not an output (CHARTER §8.3).

### RedFlag IS

- A binary `True / False` predicate, computed from patient `findings`
  (lab thresholds, biomarker presence, imaging dimension, composite score).
- Bound to ≥1 disease (`relevant_diseases`) or marked as
  universal (`relevant_diseases: ["*"]`) — if applicable across
  many diseases (HBV-reactivation, TLS-risk, etc.).
- Has a `clinical_direction` — **the semantic of how it shifts the Algorithm**:
  `intensify | de-escalate | hold | investigate`.
- Cited by ≥2 Tier-1/2 sources (CLINICAL_CONTENT_STANDARDS §6.1).
  Tier-1: NCCN, ESMO, ASCO, FDA labels, regulatory documents. Tier-2:
  published Phase-3 RCTs, Cochrane reviews, meta-analyses.

### RedFlag IS NOT

- ❌ A regimen / dose / schedule. Those belong to Regimen / Indication.
- ❌ "This patient is high-risk → give aggressive treatment" — that is
  an LLM prescribing treatment. Instead: a RedFlag fires on
  cytogenetics → the Algorithm selects an alternative Indication.
- ❌ A free-text condition without a machine predicate. Every trigger must
  reference a `findings.<key>` with a threshold/value/comparator.
- ❌ A hard-coded duplicate for every disease. If a flag applies
  across all diseases (HBV, TLS), mark `relevant_diseases: ["*"]` and place it in
  `redflags/universal/`.

---

## 2. 5-type matrix (minimum per disease)

Every disease in the KB must have **≥5 RedFlags**, one from each
category (where clinically relevant):

| # | Type | What it catches | Default `clinical_direction` |
|---|-----|----------|------------------------------|
| 1 | **organ-dysfunction** | CrCl <30, Child-Pugh B/C, LVEF <50%, bilirubin >3×ULN, pulmonary diffusion <60% | `de-escalate` or `hold` |
| 2 | **infection-screening** | HBsAg+, anti-HCV+, HIV+, latent TB (for anti-CD20, BTKi, autoSCT) | `hold` (until treated) or `investigate` |
| 3 | **high-risk-biology** | TP53 / del(17p), MYC-rearrangement, double-/triple-hit, blastoid morphology, Ph-like, Ki67 >30% | `intensify` |
| 4 | **transformation-progression** | rapid progression on therapy, new bulky mass, new extranodal localization | `intensify` |
| 5 | **frailty / age** | ECOG ≥3 OR (age ≥75 + ≥2 comorbidities + albumin <3.5) | `de-escalate` |

If a category is clinically irrelevant for a disease (e.g.,
infection-screening for PCNSL prior to anti-CD20 is not required) — add
`<rf>.notes:` with a justification instead of a placeholder stub.

---

## 3. YAML template

```yaml
# knowledge_base/hosted/content/redflags/rf_<disease>_<category>_<short>.yaml
id: RF-<DISEASE>-<CATEGORY>-<SHORT>          # uppercase, kebab; e.g., RF-PMBCL-BULKY-MEDIASTINAL
definition: "<one-line EN, machine-extractable trigger spelled out>"
definition_ua: "<one-line UA — translation, not invention>"

# trigger MUST be machine-evaluable. Refer to canonical findings names
# (see DATA_STANDARDS.md §4.2 for list of standardized finding keys).
trigger:
  type: lab_value | imaging_finding | biomarker | composite_score | symptom_composite
  any_of:                                     # OR clauses
    - finding: "<key>"
      threshold: <number>
      comparator: ">=" | ">" | "<=" | "<" | "==" | "!="
    - finding: "<key>"
      value: <bool|string>
  # all_of:  AND clauses (use one or both of any_of/all_of)
  # none_of: must-not-fire clauses

clinical_direction: intensify | de-escalate | hold | investigate

severity: critical | major | minor          # default: major. Used for
                                            # conflict-resolution tie-break
                                            # (engine prefers higher severity
                                            # when directions clash).
priority: 100                                # lower wins in tie-break;
                                            # default 100. Bump to <50 only
                                            # for true override flags.

relevant_diseases:
  - DIS-<CODE>                              # ≥1 disease ID (or ["*"] universal)
shifts_algorithm:
  - ALGO-<CODE>                             # Algorithm IDs whose decision_tree
                                            # references this RedFlag

# Optional: pin which decision_tree step.id this RedFlag drives, for
# coverage-tooling. Engine still walks tree as authored.
branch_targets:
  ALGO-<CODE>: "step-1"

sources:                                    # ≥2 Tier-1/2 sources required
  - SRC-NCCN-BCELL-2025
  - SRC-ESMO-DLBCL-2024

last_reviewed: "YYYY-MM-DD"                # ISO date of last clinical review
draft: false                                # set true only while authoring is
                                           # in progress; CI blocks merge of
                                           # non-draft entries without ≥1 source.
notes: >
  Free-text clinical context: why the flag matters, where it is borderline,
  practical access constraints in Ukraine (NSZU reimbursement,
  drug availability), reference to specific trials.
```

---

## 4. Wiring into Algorithm.decision_tree

A RedFlag is activated when an `Algorithm.decision_tree` step references
it in an `evaluate:` block:

```yaml
# knowledge_base/hosted/content/algorithms/algo_<disease>_<line>.yaml
id: ALGO-PMBCL-1L
applicable_to_disease: DIS-PMBCL
default_indication: IND-PMBCL-1L-RCHOP-RT

decision_tree:
  - step: 1
    evaluate:
      any_of:
        - red_flag: RF-PMBCL-BULKY-MEDIASTINAL   # single-flag branch
    if_true:
      result: IND-PMBCL-1L-DA-EPOCH-R            # different indication
    if_false:
      next_step: 2

  - step: 2
    evaluate:
      red_flags_all_of:                          # multi-flag combo (P2)
        - RF-PMBCL-RT-INELIGIBLE
        - RF-PMBCL-PARTIAL-RESPONSE-PET
    if_true:
      result: IND-PMBCL-1L-DA-EPOCH-R-NORT
    if_false:
      result: IND-PMBCL-1L-RCHOP-RT
```

**Wiring rules:**

1. Every `shifts_algorithm: [ALGO-X]` reference must have a **reciprocal**
   reference — `ALGO-X.decision_tree` must contain this RedFlag in some step.
   Otherwise CI flags the RedFlag as an orphan.
2. If `clinical_direction: investigate` — `shifts_algorithm` must
   be empty (investigate-flags do not shift the selection; they only
   surface annotations in the Plan / MDT brief).
3. Multi-flag combos (`red_flags_all_of: [...]`, `red_flags_any_of: [...]`)
   — supported by the engine from P2. Use for situations such as
   "DLBCL with HIGH-IPI **and** double-hit → DA-EPOCH-R + IT prophylaxis".

---

## 5. Conflict resolution (how the engine resolves multiple simultaneous triggers)

When multiple RedFlags with different `clinical_direction` values fire
in the same step, the engine applies the following deterministic order:

1. **Direction precedence** (highest wins): `hold` > `intensify` > `de-escalate` > `investigate`
2. **Severity** (highest wins): `critical` > `major` > `minor`
3. **Priority** (lowest number wins): default 100; bump to <50 for
   true override flags

The engine places the winner in `trace[*].fired_red_flags[0]` and logs
the full list as `trace[*].fired_red_flags[1:]`. **Do not rely
on implicit ordering** — if you want a specific flag to always win
its conflict, set `priority: <50`.

---

## 6. Citation requirements (CHARTER §6.1, CLINICAL_CONTENT_STANDARDS §6.1)

- **Minimum 2 independent Tier-1 or Tier-2 sources** for every non-draft
  RedFlag. CI warns if <2 and errors if 0.
- **Tier-1**: NCCN (current version), ESMO (current), ASCO, WHO, FDA labels.
- **Tier-2**: published Phase-3 RCTs, Cochrane reviews, meta-analyses from peer-reviewed journals.
- Source IDs must exist in `knowledge_base/hosted/content/sources/`.
  If the required source is not there — first add the Source entity per
  SOURCE_INGESTION_SPEC §8.

---

## 7. Authoring checklist (review all items before opening a PR)

- [ ] YAML validates against the Pydantic schema (run `python -m knowledge_base.validation.loader`)
- [ ] `id` is unique in the KB
- [ ] Both `definition` and `definition_ua` are filled in
- [ ] `trigger` is 100% machine-evaluable (`finding` + `threshold|value`)
- [ ] `clinical_direction` is assigned (and consistent with `shifts_algorithm`)
- [ ] `relevant_diseases` references existing `DIS-*` IDs or `["*"]`
- [ ] ≥2 sources (Tier-1/2) with valid `SRC-*` IDs
- [ ] Algorithm ALGO-X in `shifts_algorithm` actually references this RF in its decision_tree
- [ ] If `investigate` → `shifts_algorithm: []`
- [ ] `last_reviewed` is set to the date of the clinical review
- [ ] `draft: false` (or `true` if still under review)
- [ ] Two-reviewer sign-off in the PR (CHARTER §6.1)

---

## 8. Most common mistakes

| Symptom | Cause | Fix |
|---------|---------|------|
| RF fires but Plan does not change | `shifts_algorithm` is empty / Algorithm does not reference the RF | Add `red_flag: RF-X` to a decision_tree step |
| Multiple RFs fire, the wrong one is selected | Conflict resolution: inspect the trace; check priority/severity | Adjust `priority: <N>` on the flag that should win |
| CI error "X not found in any loaded entity" | `relevant_diseases` / `sources` / `shifts_algorithm` references a non-existent ID | Create the missing entity or fix the ID |
| Pydantic ValidationError on load | `clinical_direction` not from the enum, or `severity` not from the enum | Use only `intensify/de-escalate/hold/investigate` and `critical/major/minor` |

---

## 9. Test battery (P3)

For each newly authored RedFlag — a minimum of 2 golden fixtures in
`knowledge_base/tests/fixtures/redflags/<rf_id>/`:

```
positive.json  # virtual patient who SHOULD trigger this RF
negative.json  # virtual patient who SHOULD NOT
expected.yaml: # expected fired_red_flags + selected_indication for each
  positive:
    fires: true
    selected_indication: IND-...
  negative:
    fires: false
    selected_indication: IND-...   # whatever the algorithm's default branch yields
```

The CI runner will execute `walk_algorithm` on each fixture and fail
the test if `fired_red_flags` or `selected_indication` diverges from the expected value.
This provides both a coverage metric ("X% of RFs have golden tests")
and regression protection when the engine or RF structure changes.
