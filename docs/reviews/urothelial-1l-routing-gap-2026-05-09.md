# Urothelial 1L Routing Gap — CI Failure Diagnosis

**Date:** 2026-05-09  
**Test:** `tests/test_curated_chunk_e2e.py::test_curated_case_e2e[patient_urothelial_muc_ev_pembro.json]`  
**Status:** Pre-existing CI failure — diagnosis only. Clinical re-authoring required.

---

## What the fixture expects

`examples/patient_urothelial_muc_ev_pembro.json` represents a 70-year-old male with metastatic urothelial
carcinoma (bladder primary, ECOG 1, CrCl 55 mL/min → cisplatin-ineligible, no neuropathy, no diabetes,
no ocular disease). The finding `ev_pembro_eligible: true` is explicitly set.

Golden: `IND-UROTHELIAL-METASTATIC-1L-EV-PEMBRO` (enfortumab vedotin + pembrolizumab, EV-302/KEYNOTE-A39).

## What the engine produces

The engine routes to `IND-UROTHELIAL-METASTATIC-1L-PLATINUM-CHEMO-AVELUMAB`
(gemcitabine+carboplatin → avelumab maintenance), contradicting the EV-302 standard of care for eligible
patients.

## Root cause: regression introduced in commit 4afe2b451 (2026-05-04)

Commit `c53df2963` (2026-04-30) correctly fixed a free-text condition bug in
`knowledge_base/hosted/content/algorithms/algo_urothelial_metastatic_1l.yaml`, replacing
`{condition: "Patient eligible for EV+pembro..."}` with `{finding: ev_pembro_eligible, value: true}`.
This was verified working.

Commit `4afe2b451` (2026-05-04, "urothelial/prostate algorithm expansions") expanded the decision tree
and silently re-introduced free-text conditions:

```yaml
# Step 1 (current broken state)
evaluate:
  all_of:
    - condition: "No pre-existing severe (Grade ≥2) peripheral neuropathy"
    - condition: "No uncontrolled diabetes mellitus (HbA1c > 10% or recurrent DKA)"
    - condition: "No severe corneal disease or active keratopathy"
```

The engine's `_eval_clause` (redflag_eval.py:107) looks up `condition:` strings as exact-match keys in the
patient findings dict. None of these three strings exist as keys → all evaluate to `None` → `False`.
`all_of` is False → `if_false` fires → step 2 (also a free-text `condition:` clause → also False) →
`if_false` → `IND-UROTHELIAL-METASTATIC-1L-PLATINUM-CHEMO-AVELUMAB`.

## Clinical authoring work required

**CHARTER §6.1 two-reviewer sign-off required before any change to clinical YAML.**

Two valid repair paths:

1. **Restore the composite finding gate** (minimal change): revert step 1 `evaluate` to
   `any_of: [{finding: ev_pembro_eligible, value: true}]`. This requires the patient fixture's
   `ev_pembro_eligible` field to be maintained as the authoritative composite signal. Clinical reviewers
   must confirm the eligibility criteria it represents (no Grade ≥2 neuropathy, no uncontrolled DM,
   no corneal disease) match the authored criteria.

2. **Author structured per-criterion finding clauses** (preferred long-term): replace each free-text
   condition with a structured clause using existing patient-fixture finding keys:
   `neuropathy_grade`, `diabetic_neuropathy`, `ocular_disease`. This eliminates the composite
   `ev_pembro_eligible` shortcut and gates on individual clinical criteria evaluable by the engine.

In both cases, RF entities `RF-UROTHELIAL-EV-INELIGIBLE` (composite) or per-criterion RFs remain
owed per the algorithm's `notes` field.
