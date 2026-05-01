# Patient-Mode Render Specification

**Project:** OpenOnco
**Document:** Patient-mode render layer — simplified report for the patient
**Version:** v0.1 (draft)
**Status:** Draft for discussion with Clinical Co-Leads
**Prerequisite documents:** CHARTER.md (especially §2, §8.3, §9.3, §11, §15),
KNOWLEDGE_SCHEMA_SPECIFICATION.md, CLINICAL_CONTENT_STANDARDS.md,
DATA_STANDARDS.md
**Implementation plan:** `docs/plans/patient_simplified_report_2026-05-01-1300.md`

---

## Purpose of this document

OpenOnco generates a treatment plan in two rendering modes:

1. **Clinician mode** (existing) — full tumor-board brief: tracks
   side-by-side, contraindications, sources, ESCAT/CIViC tier, FDA
   metadata, CHARTER §6.1 sign-off badges.
2. **Patient mode** (existing from 2026-04-27 — CSD-3) — a concise report
   in plain language for the patient.

This spec formalizes the **patient-mode render contract**: invariants,
data sources, translation rules, required sections, contract tests,
and — critically — the **symmetric access model**: the clinician can
open the patient report; the patient can open the clinician report.

Prior to this spec, patient-mode invariants lived in test assertions in
[`tests/test_patient_render.py`](../tests/test_patient_render.py); this
document makes them explicit and adds rules that the current implementation
does not yet satisfy (per-track presentation, rationale-from-trace, between-visit
watchpoints, no-Latin gate).

---

## 1. Principles

### 1.1. CHARTER §8.3 invariant: render-only

Patient mode does not influence treatment selection. Specifically:

- `_patient_vocabulary.py`, `_ask_doctor.py`, `_emergency_rf.py`,
  `_patient_rationale.py` — **render-only** layer. The engine MUST NOT
  consult these modules as a treatment-selection signal.
- Engine output (`PlanResult`) — **the single source of truth** for both
  bundles. The patient version is a **translation**, not a **filter**.
- If the patient bundle shows fewer details than the clinician version, that is
  a translation choice (compression for readability), not a filter choice.

### 1.2. Symmetric access (clarified 2026-05-01)

**Both bundles are open to both audiences.**

- **The clinician reads the patient report** — a verification path. The clinician wants
  to confirm that the lay-language version is not misleading, does not omit
  or soften anything material.
- **The patient reads the clinician report** — a radical-transparency path.
  The patient has the right to view the canonical version; lay-friendly
  formatting of the clinician bundle is not required.

The patient bundle is a **translation** of the clinician bundle, **not a filter**.
Any information in the clinician version that affects patient
understanding MUST be representable in the patient version. This principle
is called the *information parity rule* (§3.4).

### 1.3. Not a medical device (CHARTER §15, §11)

The patient bundle is an informational instrument. The footer disclaimer is mandatory
(see §3.6). The bundle is not intended to replace a consultation with an oncologist.

### 1.4. PHI restrictions (CHARTER §9.3)

The patient bundle is rendered from the same synthetic / de-identified profiles
as the clinician version — the same gitignore guard applies. Real-patient bundles
do not end up on GitHub.

---

## 2. Audience model

### 2.1. Reading level

Ukrainian grade 8, ESMO patient-guide tone. Assumptions about the reader:

- Has a recently established diagnosis and an oncologist managing their treatment.
- Has no medical education.
- May forward the document to a relative / friend for a second opinion.
- Will print on A4 or read on a phone.
- May show it to another doctor (so technical anchors — `data-*`
  attributes — must remain for verification).

### 2.2. What the patient bundle does NOT do

- Does not suggest dosages (doses are the clinician's responsibility).
- Does not make promises about outcomes (no "you will be cured").
- Does not express a judgment about appropriateness (not "this option is better").
- Does not render technical entity IDs in visible text (RF-, BMA-, IND-
  remain in `data-*` attributes for debugging).

---

## 3. Bundle structure

### 3.1. Required sections

The patient bundle MUST contain the following anchor sections in this order:

| # | Selector | What is rendered |
|---|---|---|
| 1 | `<header>` | Title, diagnosis (Ukrainian name), date, plan version, cross-link to the clinician version |
| 2 | `<section class="what-was-found">` | Molecular / laboratory findings in plain language |
| 3 | `<section class="what-now">` | **Per-track**: recommended drugs, regimen, NSZU coverage, sign-off status |
| 4 | `<section class="why-this-plan">` | **NEW.** Per-track explanation: why this specific option is recommended for you |
| 5 | `<section class="between-visits">` | **NEW.** What to watch for between visits; when to call the clinic, when to go to hospital |
| 6 | `<section class="emergency-signals">` | Symptoms requiring immediate emergency contact |
| 7 | `<div class="ask-doctor">` | 5-7 questions to ask the doctor at the next visit |
| 8 | `<footer class="patient-disclaimer">` | Disclaimer + link to GitHub issues |

Cross-link `<a class="mode-toggle">` — in `<header>` (§3.5).

### 3.2. Per-track presentation

When `len(plan.tracks) > 1`:

- `what-now`, `why-this-plan`, `between-visits` are rendered **once per track**.
- Tracks are marked `track-card track-card--default` /
  `track-card track-card--alternative` (CSS reuse from clinician).
- Visible prefix: "A) Standard option" / "B) Alternative option".
  Ukrainian letter prefix, not Latin.

When `len(plan.tracks) == 1`:

- The same block without the A/B prefix.
- `why-this-plan` is still rendered (the single track has its own "why").

### 3.3. Why-this-plan: rationale from trace

Source: `PlanResult.trace` + `PlanResult.kb_resolved["red_flags"]` +
`PlanResult.kb_resolved["disease"]`. No LLM. No additional authoring.

Renderer (`_patient_rationale.py`):

- Walk the algorithm trace for each track.
- Per fired clause, produce 2-4 lines of plain Ukrainian explanation:
  - "Because **BRAF V600E** was found in your results" — biomarker-driven clause.
  - "The standard option is recommended because your condition is stable (ECOG 1)"
    — no aggressive RF fired.
  - "The alternative option **is not recommended as the standard**, because you have
    active hepatitis B without prophylaxis" — aggressive RF fired.
- Cap: ≤4 bullets per track. Longer logic falls back to "Details — in
  the technical version of the report".
- Empty trace fallback: "This option was proposed based on NCCN/ESMO standards
  for your diagnosis. Details — in the technical version of the report."

### 3.4. Between-visits: source rule

Source: `Regimen.between_visit_watchpoints` (new field, drafted in
spec extension §4 below).

- If the field is present and non-empty — render a list grouped by
  `urgency` tier.
- If empty or absent — fallback string:
  > "The list of things to watch for between visits for this course
  > has not yet been approved by the clinical team. Ask your doctor at the next
  > visit which symptoms to record and which are reasons to call
  > the clinic."

**The renderer NEVER fabricates watchpoints** from drug-class vocabulary or
inferences. If the field is empty — use the fallback. This invariant protects against
hallucinated medical advice.

### 3.5. Cross-link chip

In the patient bundle `<header>`:

```html
<a class="mode-toggle" href="<sibling>">Technical version for the clinician →</a>
```

In the clinician bundle `doc-header`:

```html
<a class="mode-toggle" href="<sibling>">Patient version →</a>
```

`href` rewrite rules:

- With `--render-mode both`, the CLI rewrites `href` to the sibling filename
  (`<basename>.html` ↔ `<basename>.patient.html`).
- With single-mode rendering, `href="#"` (placeholder) — the caller (web app,
  embed) rewrites it independently.

### 3.6. Footer disclaimer (regulatory boilerplate)

Mandatory minimum copy:

> This report is an informational instrument, not a medical device. All treatment
> decisions are made by your oncologist. The report is updated when new test results
> become available. Do not change your prescribed treatment based on this report alone.

---

## 4. Information parity rule

**Principle:** anything material in the clinician bundle MUST surface in the patient
bundle. Compression is acceptable; silent omission is not.

| Clinician surface | Patient surface |
|---|---|
| Track count + track labels | A/B prefix in per-track sections (§3.2) |
| Regimen schedule (cycle × cycles) | Plain Ukrainian description in `what-now` ("4 cycles of 21 days, each — IV infusion") |
| Fired RedFlags | Each fired RF surfaces ≥1: emergency banner / rationale / between-visits |
| CHARTER §6.1 sign-off badge per track | Patient sign-off panel (CSD-3 demo already has this) |
| NSZU coverage per drug | NSZU patient label badge (already exists) |
| ESCAT / CIViC tier | `ESCAT_TIER_PATIENT_LABEL` (already exists) |
| Source citations (PMIDs, DOIs) | Summary line "Based on N clinical guidelines" — pointer to clinician version for detail |
| FDA disclosure footer | Adapted in patient disclaimer (§3.6) |

### 4.1. Verification anchors (`data-*` attributes)

Each patient-visible block emits a `data-source-id="REG-…|RF-…|BMA-…"`
attribute. Invisible by default; the doctor verifies via View Source or
by piping the HTML through grep:

```html
<div class="drug-explanation" data-source-id="REG-FOLFOX">
  <h3>Oxaliplatin</h3>
  ...
</div>
```

This is a verification tool, not a UI element. CSS does not rely on these
attributes.

---

## 5. Vocabulary contract

### 5.1. Lookup tables

All located in [`knowledge_base/engine/_patient_vocabulary.py`](../knowledge_base/engine/_patient_vocabulary.py):

- `DRUG_CLASS_PLAIN_UA` — drug-class blurb.
- `VARIANT_TYPE_PLAIN_UA` — V600E, T790M, MSI-H, etc.
- `ESCAT_PLAIN_UA` + `ESCAT_TIER_PATIENT_LABEL` — evidence level.
- `NSZU_PLAIN_UA` + `NSZU_PATIENT_LABEL` — coverage labels.
- `LAB_PLAIN_UA` — ANC, LVEF, eGFR.
- `AE_PLAIN_UA` — adverse effects.
- `SCREENING_PLAIN_UA` — pre-treatment workup.

**Floor:** ≥200 unique entries (currently 372). Test gate:
`test_vocabulary_has_min_200_terms`.

### 5.2. First-use abbreviation expansion

A separate table `ABBREVIATION_FIRST_USE_UA` (new field, Phase 5):

```python
{
    "ESCAT": "ESCAT evidence level (how strongly it is proven that the drug works)",
    "FDA": "US Food and Drug Administration (FDA)",
    "NSZU": "National Health Service of Ukraine (NSZU)",
    ...
}
```

The renderer expands the first occurrence per bundle; subsequent occurrences —
bare abbreviation.

### 5.3. Allowlist for terms that remain untranslated

Permitted to remain in visible text without translation:

- **Gene symbols:** BRAF, EGFR, KRAS, NRAS, BRCA1, BRCA2, ALK, ROS1, RET,
  MET, HER2, PD-1, PD-L1, KIT, FGFR3, JAK2, BCR-ABL1, MGMT, IDH1, IDH2,
  FLT3, NPM1, TP53, PIK3CA, PTEN, RB1, MYC, BCL2, CDKN2A.
- **Variant labels:** V600E, V600K, T790M, L858R, G12C, G12D, Q61R,
  F1174L, H1047R, R132H, M918T, exon-14, fusion.
- **Tier labels:** ESCAT IA / IB / IIA / IIB / IIIA / IIIB / IV / X
  (with first-use expansion).
- **Drug names:** as per the international nonproprietary name (INN).
  Cyrillic transliteration is preferred; Latin is acceptable if no INN
  transliteration exists.

Everything else — either Ukrainian translation or first-use expansion.

### 5.4. No-Latin / no-abbreviation gate

Phase 5 deliverable. Test gates:

- `test_patient_html_no_latin_abbreviations_in_visible_text` — regex
  `\b[A-Z]{2,}[a-z]?\b` on visible text; fail unless on allowlist OR
  expansion within 80 chars.
- `test_patient_html_no_bare_latin_words` — regex `\b[a-z]{4,}\b`
  identifies Latin words ≥4 chars, fail if not on allowlist (allows drug
  brand names returned by `_patient_drug_label`).

---

## 6. Two-reviewer signoff (CHARTER §6.1) scope

Patient mode touches clinical content in two places:

| Content | Two-reviewer required? |
|---|---|
| `Regimen.between_visit_watchpoints` (Phase 4) | YES — this is a new clinical assertion |
| `AE_PLAIN_UA` patient-facing AE wording | YES — affects patient understanding of side effects |
| Drug-class blurbs in `DRUG_CLASS_PLAIN_UA` | YES — clinically loaded statements ("blocks BRAF — the tumor driver") |
| Renderer code (`_render_patient_mode`, `_patient_rationale`) | NO — render layer, no new clinical content |
| Fallback strings ("The list ... has not yet been approved") | NO — UI copy |
| Question templates in `_ask_doctor.py` | NO — render layer; question wording is UI copy |

---

## 7. Test contract

`tests/test_patient_render.py` (existing) + extensions per phase.

### 7.1. Inherited (Sections A-G from CSD-3)

- Vocabulary floor ≥200 (Section A).
- No entity IDs in visible body (Section B): BMA-, DIS-, ALGO-, IND-,
  REG-, BIO-, DRUG-, RF-.
- Required structural anchors (Section C).
- Emergency RF filter (Section D).
- Ask-doctor selection (Section E).
- End-to-end synthetic mCRC + BRAF V600E (Section F).
- A11y: font-size ≥16px, line-height ≥1.5 (Section G).

### 7.2. New (per phase)

**Phase 2 (tracks + cross-link):**

- `test_patient_html_two_track_plan_shows_both_tracks`.
- `test_patient_html_single_track_plan_no_a_b_prefix`.
- `test_patient_html_has_clinician_cross_link`.
- `test_clinician_html_has_patient_cross_link`.
- `test_information_parity_smoke` — each track in clinician → in patient
  via `data-source-id`; each fired RF → emergency / rationale /
  between-visits.

**Phase 3 (rationale):**

- `test_patient_rationale_braf_v600e_mcrc`.
- `test_patient_rationale_aggressive_blocked_by_rf`.
- `test_patient_rationale_no_trace_fallback`.

**Phase 4 (watchpoints — schema only in this iteration):**

- `test_patient_html_watchpoints_section_renders_authored`.
- `test_patient_html_watchpoints_section_renders_fallback`.
- `test_watchpoints_emergency_dedupe`.

**Phase 5 (Latin gate):**

- `test_patient_html_no_latin_abbreviations_in_visible_text`.
- `test_patient_html_no_bare_latin_words`.

---

## 8. CLI integration

```
python -m knowledge_base.engine.cli patient.json --render out.html
python -m knowledge_base.engine.cli patient.json --render out.html --render-mode patient
python -m knowledge_base.engine.cli patient.json --render out.html --render-mode both
```

- `--render-mode {clinician,patient,both}`, default `clinician`
  (back-compat).
- `both` writes `<out>.html` (clinician) + `<out>.patient.html` (patient).
- Cross-link `href` resolves to the sibling filename when `both` is selected.

---

## 9. Out of scope for v0.1

- **English patient bundles** — Ukrainian only. Deploying in other languages requires 2×
  vocabulary work; revisit if this appears on the horizon.
- **PDF export** — A4 print-friendly CSS already exists; users print from the browser.
- **Email delivery / patient portal** — outside CHARTER §9.3 as long as there is no
  approved patient-data hosting.
- **Dynamic QR code generation** — the QR currently lives in the CSD-3 demo as a
  static asset; the renderer does not emit a QR code.

---

## 10. Open questions

1. **`Regimen.between_visit_watchpoints` schema** — what is the spectrum of urgency
   tiers? Proposed: `log_at_next_visit`, `call_clinic_same_day`,
   `er_now`. Acceptable?
2. **Source citations** in the patient bundle — a summary line "Based on
   N guidelines" or a separate expandable block with the full list?
3. **Sign-off panel** — the CSD-3 demo shows a per-track pill ("🟢 Signed off by
   two clinicians" / "🟡 one more review needed" / "🔴 not yet reviewed").
   Keep as is or use different visual language?
