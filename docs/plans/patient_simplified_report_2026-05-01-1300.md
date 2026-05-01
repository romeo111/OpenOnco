# Patient-mode iteration 2 — Спрощений звіт для пацієнта

**Stamp:** 2026-05-01-1300 · **Status:** draft, awaiting user review · **Scope:** patient-facing render layer + supporting KB content schema

## TL;DR

Patient mode is **not new**. `render_plan_html(result, mode="patient")` shipped
2026-04-27 as part of the CSD-3 pitch pack
([commit lineage in `docs/plans/csd-pitch/`](csd-pitch/README.md)). The supporting
modules already exist:

| Module | Lines | What it does |
|---|---:|---|
| [`knowledge_base/engine/_patient_vocabulary.py`](../../knowledge_base/engine/_patient_vocabulary.py) | 592 | 372 plain-UA term explanations across 7 categories (drug class, variant type, ESCAT, NSZU, lab, AE, screening) |
| [`knowledge_base/engine/_ask_doctor.py`](../../knowledge_base/engine/_ask_doctor.py) | 211 | 11 question templates with predicates over the Plan |
| [`knowledge_base/engine/_emergency_rf.py`](../../knowledge_base/engine/_emergency_rf.py) | 102 | Filter RFs into emergency tier + `🚨` label |
| [`knowledge_base/engine/render.py:_render_patient_mode`](../../knowledge_base/engine/render.py) | ~60 in 2876 | The renderer entry point |
| [`knowledge_base/engine/render_styles.py:PATIENT_MODE_CSS`](../../knowledge_base/engine/render_styles.py) | ~200 | Embedded CSS shell |
| [`tests/test_patient_render.py`](../../tests/test_patient_render.py) | 526 | 30+ tests across 7 sections (vocab, no-jargon, structure, emergency, ask-doctor, e2e, a11y) |
| [`docs/plans/csd-pitch/02_patient_demo.html`](csd-pitch/02_patient_demo.html) | 1078 | Live demo for CSD partnership pitch |

This plan is **iteration 2**. The user's bar
("без латини, без абревіатур, з поясненням, чому призначено саме це і на що
звертати увагу між візитами; той самий план, дві мови; **лікар може відкрити
пацієнтський звіт, пацієнт може відкрити лікарський**") raises four concrete
gaps that the current renderer does not meet:

**Access model (clarified 2026-05-01).** Both bundles are open to both
audiences. The clinician version is not gated from the patient; the patient
version is not "filtered down" from the clinician — it is a **translation of
the same plan into plain UA**. Any information in the clinician bundle that
affects patient understanding (track count, regimen schedule, fired RedFlags,
CHARTER §6.1 sign-off status, NSZU coverage) MUST be representable in the
patient bundle too — possibly compressed, never silently dropped. This is
called the *information parity rule* below.

1. **Tracks are flattened.** `_render_drugs_plain` walks all tracks but dedupes
   by `seen_drug_ids` — patient sees a single drug pile, never learns that the
   plan offers a Standard alternative *and* an Aggressive alternative. This
   contradicts "той самий план" at a structural level. Load-bearing fix.
2. **No "why this for you."** Drug blocks render the drug-class blurb only.
   Per-patient rationale (which biomarker drove which track, which RedFlag
   blocked the aggressive path, why this regimen vs the alternative) is never
   surfaced. Source already exists: `PlanResult.trace` records each fired
   algorithm clause + `fired_red_flags`.
3. **No "what to watch between visits."** The current emergency banner is
   "go to ER now" — it does not tell a patient at home what mild-to-moderate
   things to track in a diary, what to call the clinic about (vs ER), what
   their normal cycle-day-7 nadir feels like, etc. Different content, different
   urgency tier.

A fourth gap is real but intentionally **deprioritized**:

4. **Latin / abbreviation residue.** Vocabulary entries themselves carry
   "BRAFi", "MEKi", "anti-PD-1", "TKI", "CAR-T". Tests check entity-IDs
   (`BMA-…`, `DRUG-…`) but not residual Latin. Hardening this *first* would
   either block the rationale/watchpoint authoring or get strings that game the
   gate without being readable. Order matters: author the new content, then
   tighten the gate.

## Current contract (from code, not yet in spec)

The patient-mode renderer is governed by these implicit invariants, derived
from existing tests + module docstrings + CHARTER:

- **CHARTER §8.3** — render-only layer; the engine MUST NOT consult patient
  vocabulary, emergency filter, or ask-doctor templates as a treatment-selection
  signal. (Documented at the top of all three helper modules.)
- **No PHI leakage** (CHARTER §9.3) — patient mode renders synthetic +
  de-identified profiles only; the same gitignore guard that protects clinician
  output covers patient bundles.
- **Vocabulary floor ≥ 200 terms** (currently 372).
- **No `BMA-* / DIS-* / ALGO-* / IND-* / REG-* / BIO-* / DRUG-* / RF-*` entity
  IDs in visible text.** (Tests in `test_patient_render.py` Section B.)
- **Mandatory structural anchors:** `.patient-report`, `.what-was-found`,
  `.what-now`, `.emergency-signals`, `.ask-doctor`, `.patient-disclaimer`.
- **A11y floors:** `.patient-report { font-size ≥ 16px; line-height ≥ 1.5 }`.
- **NSZU labels are render-only** — no engine-side coverage filtering.

These invariants are correct but live in test assertions instead of a spec doc.
That gap is what let CSD-3 ship without a per-track presentation, no rationale,
and no between-visit watchpoints — none of those omissions violate any
*explicit* contract.

## Phases

Each phase is sized to land as a single PR, gated on the previous one. The
order is deliberate: spec first so the contract is locked; rendering surface
before content authoring; content authoring queue before gate hardening.

### Phase 1 — `specs/PATIENT_MODE_SPEC.md`

**Goal:** lift the patient-mode contract from test assertions into a spec doc
so future iterations can reason about it.

**Deliverable:** new spec, ≤300 lines, sections:

1. **Scope + invariants** (CHARTER §8.3 render-only; CHARTER §15 not a medical
   device; no PHI; same engine output, two render skins).
2. **Audience model** — 8th-grade reading level Ukrainian; assume the patient
   has a recent diagnosis and an oncologist, not a clinical degree; assume they
   may forward the document to a relative who is also a layperson.
2.5. **Symmetric access + information parity rule.**
   - Both bundles render from the same `PlanResult`. Neither is access-gated.
   - The doctor reading the patient bundle is the verification path: the
     doctor wants to confirm the lay-language version doesn't mislead, omit, or
     soften something material. To support this, every patient-visible
     statement is anchored to the same data the clinician version uses
     (regimen ID, fired RF ID, ESCAT cell ID) via `data-*` attributes — visible
     to nobody by default, retrievable by `View Source` for the doctor's check.
   - The patient reading the clinician bundle is the radical-transparency
     path: the clinician renderer remains as-is (no patient-friendly
     softening); the patient is allowed to look but is not the target audience.
   - **Information parity:** anything material in clinician → representable in
     patient. The clinician version is the *source of truth*; the patient
     version is its *translation*. Differences are translation choices, not
     filtering choices. Specifically: track count, regimen schedule
     (cycle length × cycles), all fired RedFlags (translated to layperson
     wording, urgency-tiered), CHARTER §6.1 sign-off status (badge per track),
     NSZU coverage (per drug), and disclaimer must all surface in both.
   - **Cross-link required:** every clinician bundle includes a "Версія для
     пацієнта →" link in its header; every patient bundle includes a
     "Технічна версія для лікаря →" link (already present in the CSD-3 demo
     scaffold, codified here). When `--render-mode both` is used, the links
     resolve to the sibling file; for single-mode renders, the link is a
     placeholder URL the caller can override (Phase 6 wires the filename
     resolution in CLI).
3. **Required sections** (current 5 + 2 new):
   - `<header>` — diagnosis, date, version stamp.
   - `<section class="what-was-found">` — biomarker findings in plain UA.
   - `<section class="what-now">` — **per-track** drug + regimen blocks.
     **(Schema change vs current: tracks preserved.)**
   - `<section class="why-this-plan">` — **NEW.** Plain-UA rationale per track.
   - `<section class="between-visits">` — **NEW.** What to track at home, when
     to call clinic vs ER, what to expect at common cycle days.
   - `<section class="emergency-signals">` — existing siren banner.
   - `<div class="ask-doctor">` — existing 5-7 questions.
   - `<footer class="patient-disclaimer">` — existing.
4. **Vocabulary contract** — first-use abbreviation expansion rule:
   "ESCAT" → "рівень доказів ESCAT (як міцно доведено, що препарат працює)";
   thereafter just "ESCAT". Expansion table lives in `_patient_vocabulary.py`,
   tracked separately from term-lookup table.
5. **Two-track preservation** — when `len(plan.tracks) > 1`, every per-track
   section MUST render both tracks side-by-side or stacked with explicit "А)
   Стандартний / Б) Альтернативний" labels. Single-track plans render a single
   block without the А/Б prefix.
6. **Source rule for between-visit watchpoints** — content comes from
   `Regimen.between_visit_watchpoints` (new field, Phase 4). Render falls back
   to "поки що не заповнено — обговоріть з лікарем" when unauthored. Render
   never invents watchpoints from drug-class vocabulary.
7. **Two-reviewer signoff scope** (CHARTER §6.1) — applies to:
   `Regimen.between_visit_watchpoints` (Phase 4 content), patient-facing AE
   wording (`AE_PLAIN_UA`), drug-class blurbs that drive the rationale section.
   Does not apply to renderer code or fallback strings.
8. **No-Latin / no-abbrev gate** — Phase 5 deliverable; spec lists the
   allowlist of biology terms that may stay (BRAF, EGFR, KRAS, gene symbols,
   numeric variant labels).

**Validates that:** the contract is explicit before content is authored at
scale.

### Phase 2 — Tracks preserved in `_render_drugs_plain` + new `why-this-plan` shell

**Goal:** structural fix — patient version conveys "two plans" the same way
clinician version does.

**Code changes:**

- [`knowledge_base/engine/render.py:2399`](../../knowledge_base/engine/render.py:2399) `_render_drugs_plain` — split into per-track blocks. Drop the
  global `seen_drug_ids` dedupe; dedupe within a track instead so cross-track
  drug-list comparison stays honest.
- New `_render_why_section(plan_result)` — renders an empty shell `<section
  class="why-this-plan">` with per-track placeholder. Phase 3 fills it.
- `_render_patient_mode` — append `_render_why_section()` between
  `what-now` and `emergency-signals`.
- Add per-track wrapper `<div class="track-card track-card--default">` /
  `track-card--alternative` matching the clinician-side track classes for CSS
  reuse.
- **Cross-link header chip** in both renderers (per Phase 1 §2.5):
  - `_render_patient_mode` — add `<a class="mode-toggle" href="…">Технічна
    версія для лікаря →</a>` in the `<header>` block, alongside title.
  - `render_plan_html` clinician path — add the mirror `<a
    class="mode-toggle" href="…">Версія для пацієнта →</a>` in `doc-header`.
  - Default href is `"#"` (placeholder); CLI in Phase 6 rewrites to the
    sibling filename when `--render-mode both`.
- **Parity hooks** — every patient-visible drug block, RF, and rationale
  bullet emits a `data-source-id="REG-…|RF-…|BMA-…"` attribute. Tags are
  invisible by default; doctors verify via `View Source` or by piping the
  rendered HTML through a grep.

**Tests:** extend `test_patient_render.py`:

- New: `test_patient_html_two_track_plan_shows_both_tracks` — two-track
  fixture (any HCV-MZL or MM patient with both ANTIVIRAL and BR-AGGRESSIVE).
- New: `test_patient_html_single_track_plan_no_a_b_prefix`.
- Update existing `test_patient_html_has_required_sections` to add
  `.why-this-plan` (placeholder OK in Phase 2).
- New: `test_patient_html_has_clinician_cross_link` — patient bundle
  contains `<a class="mode-toggle"` with "Технічна версія для лікаря".
- New: `test_clinician_html_has_patient_cross_link` — clinician bundle
  (mirror) contains `<a class="mode-toggle"` with "Версія для пацієнта".
- New: `test_information_parity_smoke` — for the reference HCV-MZL case,
  every track present in the clinician HTML appears in the patient HTML
  (matched via `data-source-id` REG-* attributes); every fired RF in
  clinician trace surfaces somewhere in the patient body (banner OR
  rationale OR between-visits).

**Done when:** patient demo for the reference HCV-MZL case shows both tracks;
demo doc at `docs/plans/csd-pitch/02_patient_demo.html` regenerated.

### Phase 3 — Rationale from `PlanResult.trace`

**Goal:** fill the `why-this-plan` section from the algorithm trace + fired
RedFlags, not from new authored content.

**Source data** (already populated by the engine, no schema change needed):

- `PlanResult.trace: list[dict]` — each entry is `{"step": str|None,
  "outcome"/"result": str, "branch": str, "fired_red_flags": list[str]}`
  (per [`knowledge_base/engine/algorithm_eval.py:155`](../../knowledge_base/engine/algorithm_eval.py:155)).
- `PlanResult.kb_resolved["red_flags"]` — RedFlag entities, including
  `definition_ua`.
- `PlanResult.kb_resolved["disease"]`, `["algorithm"]` — disease + algorithm
  entities for `applies_when` / decision-clause prose.

**Mapping rule** (renderer-side, no LLM):

For each track, walk the algorithm trace and produce a 2-4 line plain-UA
explanation:

- "Бо у вас знайдено **BRAF V600E**" — when a fired clause references
  `BIO-BRAF-MUTATION` (translate gene+variant via `_explain_patient`).
- "Стандартний варіант рекомендовано, бо ваш стан стабільний (ECOG 1, без
  ускладнень)" — when no aggressive-track RFs fired.
- "Альтернативний варіант **не рекомендовано як стандартний**, бо у вас
  активний гепатит B без профілактики" — when an aggressive-track RF fired.
- "Цей препарат — **bevacizumab** — додано, бо ESCAT-рівень доказів IB для
  вашого діагнозу" — when an actionability cell drove the regimen.

**Code changes:**

- New `knowledge_base/engine/_patient_rationale.py` (~150-200 lines) with
  `build_track_rationale(plan_result, track) -> list[str]`. Pure function,
  consumes `trace` + `kb_resolved`, returns plain-UA bullets.
- Render-side `_render_why_section` calls it once per track.
- Fallback when trace empty or no clauses fire: "Цей варіант запропоновано
  лікарем на основі стандартів NCCN/ESMO для вашого діагнозу. Деталі — у
  технічній версії звіту."

**Tests:**

- `test_patient_rationale_braf_v600e_mcrc` — synthetic fixture, asserts
  "BRAF V600E" appears in rationale text.
- `test_patient_rationale_aggressive_blocked_by_rf` — synthetic HCV-MZL
  patient with HBV-no-prophylaxis RF fired; asserts the aggressive-track
  rationale explains the block in plain UA.
- `test_patient_rationale_no_trace_fallback` — empty trace → fallback string
  rendered.

**Done when:** every existing `tests/test_reference_case_e2e.py` patient renders
non-empty rationale text in both tracks (or single-track patients render a
non-empty single rationale).

### Phase 4 — `Regimen.between_visit_watchpoints` schema + authoring queue

**Goal:** introduce the field, build the renderer side, queue the content
authoring under CHARTER §6.1 two-reviewer signoff.

**Schema change** ([`knowledge_base/schemas/regimen.py`](../../knowledge_base/schemas/regimen.py), if it exists):

```python
class BetweenVisitWatchpoint(BaseModel):
    trigger_ua: str           # plain UA: what the patient might notice
    action_ua: str            # plain UA: what to do (call clinic? ER? log it?)
    urgency: Literal["log_at_next_visit", "call_clinic_same_day", "er_now"]
    cycle_day_window: Optional[str] = None  # e.g. "Day 7-14" — when this is normal vs alarming
    sources: list[str] = []   # SRC-* IDs
```

`Regimen.between_visit_watchpoints: list[BetweenVisitWatchpoint] = []`

Field is optional; existing 244 regimens stay valid.

**Renderer:**

- New `_render_between_visits_section(plan_result)` — per-track block, lists
  watchpoints grouped by urgency tier. `er_now` items overlap with the
  emergency banner; renderer collapses duplicates by `trigger_ua` text.
- Fallback when a track's regimen has no watchpoints authored:
  > "Список того, на що звернути увагу між візитами, для цього курсу ще не
  > узгоджено клінічною командою. Запитайте лікаря на наступному візиті, які
  > симптоми треба занотовувати, а які — приводи дзвонити в клініку."

**Authoring queue** (separate workstream, gated on Phase 4 schema landing):

- ~244 regimens × ~5 watchpoints = ~1000-1500 content items.
- Two-reviewer signoff per regimen (CHARTER §6.1) before render surfaces them
  as authored — until then, the placeholder fallback shows.
- Tracking doc: `docs/plans/patient_watchpoints_authoring_queue_2026-05-01-1300.md`
  (separate plan, written when Phase 4 schema lands).
- Triage by regimen-blast-radius: anti-CD20 / anthracycline / platinum first
  (used in many tracks, well-known AE profile); rare-tumor regimens last.

**Tests:**

- Schema validator covers new field.
- `test_patient_html_watchpoints_section_renders_authored` — fixture regimen
  with 3 watchpoints; asserts urgency grouping + counts.
- `test_patient_html_watchpoints_section_renders_fallback` — regimen with
  empty `between_visit_watchpoints` renders the placeholder string.
- `test_watchpoints_emergency_dedupe` — `er_now` items don't double-render
  in both `between-visits` and `emergency-signals`.

**Done when:** schema validator green; renderer surfaces authored content
when present, fallback when not; queue doc opened.

### Phase 5 — Latin / abbreviation hardening + vocabulary expansion

**Goal:** lock the no-Latin / no-abbreviation gate **after** new content lands,
so the gate checks real prose rather than placeholder strings.

**Vocabulary work** ([`knowledge_base/engine/_patient_vocabulary.py`](../../knowledge_base/engine/_patient_vocabulary.py)):

- New `ABBREVIATION_FIRST_USE_UA: dict[str, str]` — first-use expansion table
  ("ESCAT" → "рівень доказів ESCAT (як міцно доведено, що препарат працює)").
- Audit existing `DRUG_CLASS_PLAIN_UA` for residual Latin acronyms in the
  *explanation strings themselves*: "BRAFi" → "препарат, який блокує мутацію
  BRAF — ключовий driver пухлини" (BRAF stays — gene symbol allowed; the
  trailing "i" suffix abbreviation drops).
- Same audit for `VARIANT_TYPE_PLAIN_UA`, `ESCAT_PLAIN_UA`, `AE_PLAIN_UA`,
  `LAB_PLAIN_UA`, `SCREENING_PLAIN_UA`. Estimate ~50-80 strings to rewrite.

**Allowlist** (terms that may stay in patient body):

- Gene symbols: BRAF, EGFR, KRAS, NRAS, BRCA1, BRCA2, ALK, ROS1, RET, MET,
  HER2, PD-1, PD-L1, KIT, FGFR3, JAK2, BCR-ABL1, MGMT, IDH1/2, FLT3, NPM1,
  TP53, PIK3CA, PTEN, RB1, MYC, BCL2, CDKN2A.
- Variant labels: V600E, V600K, T790M, L858R, G12C, G12D, Q61R, F1174L,
  H1047R, R132H, M918T, exon-14 skipping, fusion (translated as "злиття").
- Tier labels: ESCAT IA/IB/IIA/IIB/IIIA/IIIB/IV/X (with first-use expansion).

Everything else gets a Ukrainian rewrite or a first-use expansion.

**Test gate** (new in `test_patient_render.py`):

- `test_patient_html_no_latin_abbreviations_in_visible_text` — regex scan
  visible text for `\b[A-Z]{2,}[a-z]?\b` (e.g. "TKI", "MEKi", "CAR-T",
  "CRS"); fail unless every hit is on the allowlist OR appears within 80
  chars of its first-use expansion.
- `test_patient_html_no_bare_latin_words` — regex `\b[a-z]{4,}\b` on
  visible text; fail when any Latin word ≥4 chars not on allowlist appears
  (catches "fertility", "chemotherapy" — should be "хіміотерапія" in body
  text). Allowlist exempts brand names (drug names stay as-is per
  `_patient_drug_label`).

**Done when:** both gates pass on the full reference-case suite. Vocabulary
audit log committed alongside the gate.

### Phase 6 — CLI + roadmap entry

**Goal:** make patient mode discoverable from the command line; track in the
roadmap.

**CLI** ([`knowledge_base/engine/cli.py:378`](../../knowledge_base/engine/cli.py:378)):

- New flag: `--render-mode {clinician,patient,both}`, default `clinician`
  (back-compat).
- `--render-mode both` writes two files: `<out>.html` (clinician) +
  `<out>.patient.html` (patient). Same `result`, two render passes.
- When `both` is selected, the CLI passes the sibling filename into each
  render call so the cross-link chip resolves correctly:
  - Clinician bundle's "Версія для пацієнта →" → `<basename>.patient.html`.
  - Patient bundle's "Технічна версія для лікаря →" → `<basename>.html`.
  - For single-mode renders, the chip stays present with `href="#"` so a
    downstream caller (web app, embed) can rewrite it.
- Existing `--render OUT.html` keeps current behaviour (clinician).

**Memory:**

- Add `[ ]` entry under `### Engine + render` in `memory/project_roadmap.md`
  pointing at this plan doc.

**Done when:** `python -m knowledge_base.engine.cli examples/patient_zero_reference_case.json --render out.html --render-mode both` produces both files; roadmap line appended.

## Out of scope for this iteration

- **EN patient bundles.** UA-only per CSD-3 spec. Adding EN multiplies
  vocabulary work 2×; revisit only if a non-Ukrainian deployment is on the
  table.
- **PDF export.** A4 print-friendly CSS already exists; users print from the
  browser. Adding a server-side PDF pipeline is a separate workstream.
- **Email delivery / patient portal.** Out of CHARTER §9.3 scope until
  patient-data hosting is approved.
- **Translation of CHARTER §11 medical disclaimer.** Already in UA; no work.
- **Removing the QR-code panel from `02_patient_demo.html`.** That panel is
  CSD-pitch chrome around the engine output; the renderer itself does not
  emit QR codes. Demo regeneration in Phase 2 keeps the QR scaffold.

## Risks + mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Phase 4 watchpoint authoring stalls (CHARTER §6.1 needs Clinical Co-Lead capacity) | Medium | Patient-mode lands but the section is mostly fallback strings | Schema + renderer ship in Phase 4 PR; content authoring is its own queue with its own pace; render fallback is honest ("ще не заповнено") rather than fabricated |
| Trace-driven rationale (Phase 3) produces wooden, hard-to-read prose for complex algorithms | Medium | Patient sees "Бо у вас знайдено BIO-… and BIO-… and BIO-…" style strings | Rationale renderer caps at 4 bullets per track; longer logic falls back to "Деталі — у технічній версії звіту"; design review of generated text on the 7 reference cases before merge |
| Phase 5 gate too strict — blocks legitimate biology terms | Low | Tests fail on PR that didn't change patient mode | Allowlist explicit + maintained in `_patient_vocabulary.py`; gate failure points at the offending term + suggested fix |
| Two-track preservation breaks single-track render path | Low | Patients with single-track plans see "А) Стандартний" with no "Б)" | Phase 2 includes single-track regression test; rendering branches on `len(plan.tracks)` |
| Information parity rule too strict — forces patient bundle to mirror clinician structure 1:1 | Low | Plain-UA prose gets cluttered with translated technical detail | Parity is on *information*, not on *structure*: a fired RF must appear *somewhere* in patient body, not necessarily in the same shape. Phase 2's `test_information_parity_smoke` only checks set-membership, not formatting. |
| User wants the iteration done sooner than the 6 phases imply | Medium | Plan stalls midway with half-built sections | Phases 1-3 alone close the structural gap (tracks + rationale) — that's a shippable v2.1 even without watchpoints |

## Order of operations + estimate

| Phase | Effort | Blocking |
|---|---|---|
| 1 — Spec doc | 1 session | — |
| 2 — Tracks preserved + `why-this-plan` shell | 1 session | Phase 1 |
| 3 — Rationale from trace | 2 sessions | Phase 2 |
| 4 — Watchpoints schema + renderer + queue doc | 1 session (schema+renderer); queue authoring is multi-month | Phase 1 |
| 5 — Latin/abbrev gate + vocab audit | 1-2 sessions | Phase 3 (so the gate scans real rationale prose) |
| 6 — CLI + roadmap | 0.5 session | Phase 5 |

**v2.1 (shippable without Phase 4 content):** Phases 1+2+3+5+6.
**v2.2 (full bar):** v2.1 + Phase 4 schema + first 50 anchor-regimen
watchpoints authored.

## Open questions for the user

1. **Watchpoint authoring funnel.** Two-reviewer signoff for ~1000-1500
   content items is large. Acceptable to ship Phase 4 as schema-only + 0
   authored watchpoints + permanent fallback, OR is the queue itself part of
   the deliverable? (Plan currently assumes the former.)
2. **EN patient bundle.** Confirm out-of-scope. (Plan currently assumes UA-only.)
3. **Spec home for the contract.** New `specs/PATIENT_MODE_SPEC.md`, or
   appended section in existing `specs/CLINICAL_CONTENT_STANDARDS.md`?
   (Plan currently assumes new file — patient mode is structurally distinct
   from clinical-content-authoring rules.)
4. **Demo regeneration.** Should the Phase 2 PR also regenerate
   `docs/plans/csd-pitch/02_patient_demo.html` so the CSD pitch pack stays
   current, or is the pitch pack frozen?
