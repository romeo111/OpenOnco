# Diagnostic-Phase MDT Specification

**Project:** OpenOnco
**Document:** Diagnostic-Phase MDT — pre-biopsy / pre-histology workup
**Version:** v0.1 (draft)
**Status:** Draft for discussion with Clinical Co-Leads
**Prerequisite documents:** CHARTER.md (especially §1, §2, §15), MDT_ORCHESTRATOR_SPEC.md,
KNOWLEDGE_SCHEMA_SPECIFICATION.md, DATA_STANDARDS.md

---

## Purpose of this document

Addresses a real clinical use case: **initial oncology consultation / tumor
board BEFORE confirmed histology**. The patient presents with a suspicion
(a mass, cytopenias, B-symptoms), biopsy is not yet available — but the
MDT must already convene to:

1. Determine the correct biopsy approach (where, how, which IHC panel)
2. Plan staging studies (PET/CT, bone marrow trephine biopsy)
3. Identify the team composition for the specific suspicion pattern
4. Document open questions that must be resolved **before** any
   therapy discussion

Prior to this commit, OpenOnco required a confirmed `disease_id` for
any Plan generation — i.e., it covered the phase **after** histology.
This spec adds a **second operational mode** covering the phase **before**.

---

## 1. Principles

### 1.1. Two operational modes (mutually exclusive)

| Mode | Trigger | Output | Patient profile shape |
|---|---|---|---|
| **`treatment_planning`** (existing) | `patient.disease.id` OR `patient.disease.icd_o_3_morphology` is present | `Plan` with ≥2 `tracks` (treatment alternatives) + MDT brief | confirmed diagnosis |
| **`diagnostic`** (new) | `patient.disease.suspicion` is present AND `patient.disease.id` is ABSENT | `DiagnosticPlan` (workup steps, mandatory questions, MDT brief) — **no treatment tracks** | suspicion only |

The mode is determined **automatically** from the patient profile — the
client does not specify it explicitly. The CLI flag `--diagnostic` is
optional, for UI/UX convenience (forces diagnostic mode even if a diagnosis
is stated but the reviewer wants to re-confirm the workup).

### 1.2. Hard rule: no treatment Plan without histology

**Enforced mechanically in code, not subjective judgment:**

- `generate_plan(patient)` returns an **error / empty PlanResult** if
  both `patient.disease.id` AND `patient.disease.icd_o_3_morphology`
  are absent
- `generate_diagnostic_brief(patient)` returns an **error** if
  `patient.disease.id` is present (the reviewer should use treatment
  mode for a confirmed diagnosis)
- If a reviewer wants a "simulation" of a treatment Plan for a suspected
  diagnosis — this is a separate action `simulate_plan_for_hypothesis()`
  that does **not** produce a real Plan and explicitly marks the output
  as hypothesis-driven (out of MVP scope)

### 1.3. Why this strengthens the FDA non-device CDS positioning

Diagnostic-phase MDT is **even more clearly** non-device CDS than
treatment planning:

- Workup recommendations are "a list of preventive/diagnostic options"
  (FDA Guidance §IV(3) Example V.A.10) — exactly the carve-out pattern
- There are no **treatment** directives at all → no risk of a
  "specific treatment output" disqualifier
- Open questions and mandatory questions are explicit → HCP independent
  review is based on honest acknowledgment of gaps

→ Addition to **CHARTER §15.2 C7**: "no treatment recommendations
without confirmed histology" — this is a new hard constraint formalized
here.

---

## 2. Patient profile shape (diagnostic mode)

```json
{
  "patient_id": "PZ-DIAG-001",
  "disease": {
    "suspicion": {
      "lineage_hint": "b_cell_lymphoma",
      "tissue_locations": ["lymph_node", "spleen"],
      "icd_o_3_topography": ["C77.2", "C42.2"],
      "presentation": "Splenomegaly + mediastinal lymphadenopathy + cytopenias",
      "working_hypotheses": ["DIS-SPLENIC-MZL", "DIS-DLBCL", "DIS-FOLLICULAR-LYMPHOMA"]
    }
  },
  "demographics": {
    "age": 58,
    "sex": "male",
    "ecog": 1
  },
  "findings": {
    "splenic_mass_cm": 12.0,
    "ldh_ratio_to_uln": 1.4,
    "anc": 1200,
    "platelets": 95000
  },
  "history": {
    "hcv_known_positive": false,
    "prior_malignancy": null
  }
}
```

`suspicion.lineage_hint` — controlled vocabulary expressed as a canonical
tag (see the §3.2 matrix). Other fields are optional; the more complete
the profile, the more precisely the DiagnosticWorkup can be matched and
the fewer OpenQuestions will be raised.

`working_hypotheses` — list of `Disease` IDs that the clinician is
considering. If specified, the orchestrator can perform a **differential**
assessment (showing which tests are needed to distinguish hypothesis A
from hypothesis B). In MVP — informational only, not driving recommendations.

---

## 3. Data entities

### 3.1. `DiagnosticWorkup` (KB content entity)

Curated content, lives under `knowledge_base/hosted/content/workups/`.
Analogous to `Indication` in treatment mode, but **without** regimen/dose.

```yaml
id: WORKUP-SUSPECTED-LYMPHOMA
applicable_to:
  lineage_hints:
    - b_cell_lymphoma
    - t_cell_lymphoma
    - hodgkin_lymphoma
    - lymphoma  # generic fallback
  tissue_locations:
    - lymph_node
    - spleen
    - stomach
    - thyroid
    - salivary_gland
  presentation_keywords:  # optional substrings to widen match
    - lymphadenopathy
    - splenomegaly
    - cytopenia
    - B-symptom

required_tests:
  - TEST-CBC
  - TEST-LFT
  - TEST-LDH
  - TEST-HBV-SEROLOGY
  - TEST-PET-CT

biopsy_approach:
  preferred: "Excisional biopsy of largest accessible lymph node"
  alternatives:
    - "Core needle biopsy if excisional not feasible"
    - "Ultrasound-guided biopsy for deep-seated lesions"
  rationale: >
    Lymph node architecture is critical for lymphoma classification
    (follicular vs diffuse, nodular vs interfollicular). FNA is
    insufficient — it misses the architectural pattern.

required_ihc_panel:
  baseline: ["CD20", "CD3", "CD5", "CD10", "CD23", "BCL2", "BCL6", "Ki67"]
  if_b_cell: ["MUM1", "CyclinD1", "EBER-ISH"]
  if_aggressive: ["MYC", "BCL6 break-apart FISH"]

mandatory_questions_to_resolve:
  - "Is this lymphoma, reactive hyperplasia, or another malignancy?"
  - "If lymphoma — what subtype per WHO Classification?"
  - "Are there signs of transformation / aggressive component?"
  - "Is molecular testing required (translocation, FISH)?"

expected_timeline_days: 14
expected_workup_cost_uah_estimate: 8000  # approximate estimate for the Ukrainian context

triggers_mdt_roles:
  required: [hematologist, pathologist, radiologist]
  recommended: [infectious_disease_hepatology]  # if HBV/HCV not yet ruled out

sources:
  - SRC-NCCN-BCELL-2025
  - SRC-ESMO-MZL-2024

last_reviewed: "2026-04-25"
notes: >
  STUB — for HCV-MZL reference case workup. Expand per-disease as
  KB grows.
```

### 3.2. `DiagnosticPlan` (per-patient artifact, gitignored)

Analogous to the treatment `Plan` (per CHARTER §9.3 — patient-specific,
not in the public KB).

```yaml
id: DPLAN-PZ-DIAG-001-V1
patient_id: PZ-DIAG-001
mode: diagnostic
version: 1
generated_at: "2026-04-25T..."

supersedes: null
superseded_by: null
revision_trigger: null

patient_snapshot: { ...full input... }
suspicion_snapshot:
  lineage_hint: b_cell_lymphoma
  tissue_locations: [lymph_node, spleen]
  presentation: "..."
  working_hypotheses: [DIS-SPLENIC-MZL, DIS-DLBCL]

matched_workup_id: WORKUP-SUSPECTED-LYMPHOMA
workup_steps:
  - step: 1
    category: lab
    test_id: TEST-CBC
    rationale: "Baseline cytopenias, marrow involvement assessment"
  - step: 2
    category: lab
    test_id: TEST-HBV-SEROLOGY
    rationale: "HBV reactivation risk before any anti-CD20"
  - step: 3
    category: imaging
    test_id: TEST-PET-CT
    rationale: "Staging + identify highest-yield biopsy site"
  - step: 4
    category: histology
    biopsy_approach: { ...inline from workup... }
    ihc_panel: { ...inline from workup... }

mandatory_questions:  # from workup, surfaced explicitly
  - "Is this lymphoma, reactive hyperplasia, or another malignancy?"
  - ...

expected_timeline_days: 14

mdt_brief: { ...MDTOrchestrationResult — same shape as treatment mode... }

trace: []  # diagnostic mode has no algorithm decision tree
warnings: []
```

`DiagnosticPlan` instances do **not** go into the public KB. They are
stored outside the repo, analogous to treatment Plans.

### 3.3. Relationship with the MDT Orchestrator

`orchestrate_mdt()` accepts **either** a `PlanResult` **or** a
`DiagnosticPlanResult`. Internally it detects the mode → applies the
appropriate rule set:

- Treatment mode: existing R1-R9 (role based on disease + tracks
  + biomarkers + regimen)
- Diagnostic mode: D1-D6 (role based on tissue_location +
  lineage_hint + workup steps)

The output type is the same `MDTOrchestrationResult` — but with diagnostic
context-specific reasons in `MDTRequiredRole.reason`.

---

## 4. Diagnostic-mode MDT rules (D1-D6)

| # | Trigger | Role | Priority | trigger_type |
|---|---|---|---|---|
| D1 | `suspicion.lineage_hint` contains `lymphoma` | `hematologist` | `required` | `diagnosis_complexity` |
| D2 | Any suspicion → biopsy required | `pathologist` | `required` | `diagnosis_complexity` |
| D3 | `suspicion.tissue_locations` is non-empty OR imaging fields present in findings | `radiologist` | `required` | `diagnosis_complexity` |
| D4 | `suspicion.lineage_hint` ∈ {`solid_tumor_*`, generic carcinoma with surgically relevant location} | `surgical_oncologist` | `recommended` | `treatment_domain` |
| D5 | `suspicion.lineage_hint` contains `lymphoma` AND history contains HCV/HBV (or not yet excluded) | `infectious_disease_hepatology` | `recommended` | `molecular_data` |
| D6 | ECOG ≥ 3 OR `suspicion.presentation` contains B-symptoms + decompensation | `palliative_care` | `recommended` (early goals-of-care) | `palliative_need` |

**Key difference from treatment mode:**
- `clinical_pharmacist` NOT recommended (no regimen yet)
- `radiation_oncologist` NOT recommended (treatment-domain decision deferred)
- `social_worker_case_manager` NOT recommended for non-reimbursed drugs
  (no drugs yet); but recommended if `suspicion.expected_workup_cost_uah_estimate`
  is significant AND the patient has financial constraints (out of MVP scope)

---

## 5. Diagnostic-mode OpenQuestions (DQ1-DQ4)

| # | Trigger | Question | owner_role | blocking |
|---|---|---|---|---|
| DQ1 | `suspicion.lineage_hint` contains `lymphoma` AND `cd20_ihc_status` is absent | "What is the CD20 IHC result after biopsy? This is the basis for anti-CD20 selection." | `pathologist` | true |
| DQ2 | Lymphoma suspicion AND HBV serology absent | "HBV serology before anti-CD20 is mandatory immediately." | `infectious_disease_hepatology` | true |
| DQ3 | Lymphoma suspicion AND imaging staging absent | "Has PET/CT been performed for staging?" | `radiologist` | true |
| DQ4 | Multiple working_hypotheses in suspicion (≥2) | "What is the differential diagnosis plan? What molecular tests are needed to choose between {hypothesis A vs B}?" | `pathologist` | false |

OpenQuestions from treatment mode (Q1-Q6) **do not apply** in diagnostic
mode — there is no Plan with a regimen to which questions can be linked.

---

## 6. Engine API

### 6.1. Diagnostic mode entry point

```python
# knowledge_base/engine/diagnostic.py

def generate_diagnostic_brief(
    patient: dict,
    kb_root: Path | str = "knowledge_base/hosted/content",
    plan_version: int = 1,
    supersedes: str | None = None,
    revision_trigger: str | None = None,
) -> DiagnosticPlanResult:
    """Build a DiagnosticPlan for a patient WITHOUT confirmed histology.

    Hard rules:
    - patient.disease.id present AND .icd_o_3_morphology present →
      raise ValueError ("use generate_plan() for confirmed diagnosis")
    - patient.disease.suspicion absent → return empty result with warning
    """
    ...
```

### 6.2. MDT Orchestrator dispatch

```python
def orchestrate_mdt(
    patient: dict,
    plan_or_diagnostic: PlanResult | DiagnosticPlanResult,
    kb_root: Path | str = "...",
) -> MDTOrchestrationResult:
    """Detects mode by isinstance and applies the correct rule set."""
```

### 6.3. CLI dispatch

```bash
python -m knowledge_base.engine.cli patient.json              # auto-detect
python -m knowledge_base.engine.cli patient.json --diagnostic  # force
python -m knowledge_base.engine.cli patient.json --mdt         # MDT brief on top
```

Auto-detection rule: if patient.disease has `id` or `icd_o_3_morphology`
→ treatment mode. Otherwise if `suspicion` is present → diagnostic mode.
Otherwise → error "patient profile has neither confirmed diagnosis nor
suspicion".

### 6.4. CLI banner — DIAGNOSTIC PHASE

Diagnostic-mode output **must begin** with:

```
=========================================================
  DIAGNOSTIC PHASE — TREATMENT PLAN NOT YET APPLICABLE
  Histology required before any therapy discussion.
=========================================================
```

This is a mechanical guard against automation bias (CHARTER §15.2 C6).

---

## 7. What remains THE SAME for both modes

- `MDTOrchestrationResult` shape (same dataclass)
- `ProvenanceEvent` shape (same provenance.py)
- FDA Criterion 4 fields in output (intended_use, hcp_user_specification, …)
- Source citations
- Audit trail / version chain (supersedes/superseded_by — implementation in §7.1)
- Termination criterion: when histology is confirmed →
  the diagnostic-mode `DiagnosticPlan` becomes `superseded_by` a treatment-mode
  `Plan` (formal transition; the supersedes-link crosses a mode boundary)

### 7.1. Revisions — closing step 5 from the infographic

`knowledge_base/engine/revisions.py` contains
`revise_plan(updated_patient, previous, revision_trigger, kb_root)`,
which returns **`(previous_with_superseded_by_set, new_result)`** — both
sides of the supersedes-chain. The previous result is **not mutated** —
a deep copy is returned with `superseded_by` populated.

**Three legal transitions** (auto-detected from shapes):

| Previous | Updated patient | Transition | New |
|---|---|---|---|
| `DiagnosticPlan` vN | suspicion-only | `diagnostic → diagnostic` | `DiagnosticPlan` v(N+1) |
| `DiagnosticPlan` vN | confirmed `disease.id` | `diagnostic → treatment` | `Plan` v1 (first treatment) |
| `Plan` vN | confirmed `disease.id` | `treatment → treatment` | `Plan` v(N+1) |

**Forbidden transition:**

| `Plan` vN | suspicion-only (no `.id`) | `treatment → diagnostic` | **`ValueError`** — CHARTER §15.2 C7 |

Rationale: if a treatment Plan already exists, reverting to diagnostic
mode is not permitted automatically — this signifies clinical uncertainty
that requires a separate decision (e.g. a new primary suspicion — create
a **separate** new `DiagnosticPlan` with no revision-link).

**Provenance:** the new plan receives a `modified` ProvenanceEvent in
its `trace`: `summary = "Plan revised from PREV_ID (trigger: ...). This
is version N of patient X."` The audit trail always shows **where**
the new version came from.

**CLI:** `--revise PREV.json --revision-trigger "biopsy 2026-05-10 →
DLBCL confirmed"`. PREV.json is the previous `--json-output` from the
prior run.

**Persistence:** as before, plan instances are not in the public KB —
they are stored under `patient_plans/<patient_id>/<plan_id>.json`
(gitignored per CHARTER §9.3). Implementation in
`knowledge_base/engine/persistence.py` (see §7.2).

### 7.2. Persistence layer

`knowledge_base/engine/persistence.py` provides:

| API | Action |
|---|---|
| `save_result(result, root=patient_plans/)` | Serializes `PlanResult` / `DiagnosticPlanResult` to `<root>/<patient_id>/<plan_id>.json`. Returns the path. |
| `load_result(path_or_plan_id, root=patient_plans/)` | Reconstructs result from a file path OR from a plan_id (resolved via glob `<root>/*/<plan_id>.json`). |
| `list_versions(patient_id, root=patient_plans/)` | Returns `[{plan_id, version, mode, supersedes, superseded_by, path}]` sorted: diagnostic → treatment, then by `version`. |
| `update_superseded_by_on_disk(plan_id, new_id, root=patient_plans/)` | In-place mutates `superseded_by` in the saved file. Used by the revisions workflow to synchronize the on-disk chain. |
| `latest_version_path(patient_id, root=patient_plans/)` | Path to the most recent version, or `None`. |

**Hard guarantees:**
- `patient_plans/` is in `.gitignore` by default (CHARTER §9.3).
- `save_result` refuses to write when `patient_id` is absent — it will
  not silently write to `ANONYMOUS/`.
- `update_superseded_by_on_disk` raises `FileNotFoundError` if the
  previous version is not on disk — the caller learns explicitly.
- Format = JSON (not YAML, because PlanResult / DiagnosticPlanResult
  are serialized via dataclass `to_dict()` + Pydantic `model_dump()`,
  which is natively JSON).

**CLI integration:**

```bash
# Generate + auto-save
python -m knowledge_base.engine.cli patient.json --save
# → patient_plans/PZ-001/PLAN-PZ-001-V1.json

# Show all saved versions for a patient
python -m knowledge_base.engine.cli --list-versions PZ-001

# Revise: --revise accepts a plan_id (resolved via persistence layer)
# OR an explicit JSON path. With --save: writes new + updates previous in place.
python -m knowledge_base.engine.cli patient_v2.json \
    --revise PLAN-PZ-001-V1 \
    --revision-trigger "new lab 2026-05-10: FIB-4 worsened" \
    --save
# → patient_plans/PZ-001/PLAN-PZ-001-V2.json (new)
# → patient_plans/PZ-001/PLAN-PZ-001-V1.json (updated: superseded_by=...-V2)
```

**Out of MVP scope:**
- Database backend (SQLite/Postgres) — JSON files are sufficient at current scale
- Encryption-at-rest — patient data but development-only for now;
  add if deployed to cloud
- Network sync / cloud backup — to be considered when > 1 OpenOnco
  installation exists
- Search / cross-patient analytics — separate "Case cohort matching"
  workstream in the roadmap

---

## 8. Extensions (not in MVP)

- `simulate_plan_for_hypothesis(patient, hypothesis_disease_id)` —
  show what the treatment plan would look like IF the diagnosis is
  confirmed as hypothesis Y. Strict marking "HYPOTHETICAL — not for clinical
  decision".
- DiagnosticPlan → treatment Plan transition automation: when a
  pathology report is added and `disease.id` is resolved, automatically
  call generate_plan() with the previous DiagnosticPlan as `supersedes`.
- Cost estimate for the workup basket (NHSU vs out-of-pocket) for
  patient financial planning.
- Timeline tracking: "7 of the expected 14 workup days have elapsed,
  histology still unavailable" → escalation to MDT.

---

## 9. Changes in this document

| Version | Date | Changes |
|---|---|---|
| v0.1 | 2026-04-25 | Initial MVP spec; diagnostic mode with 1 seed workup (lymphoma); D1-D6 + DQ1-DQ4 rules; hard rule "no treatment without histology". |
