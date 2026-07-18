# Sex/disease incoherence in generated example profiles

**Created:** 2026-07-18-1625
**Status:** DONE in this branch
**Gate:** none — tooling + synthetic data, no KB content touched
**Origin:** gallery audit on `claude/gallery-examples-outdated-eb7f06`

---

## 1. The defect

24 synthetic patient profiles declared an anatomically impossible sex:

- 22 female-only cancers marked male — 6 cervical, 8 endometrial, 8 ovarian
- 2 prostate profiles marked female

All 24 were machine-generated. The 199 hand-curated `patient_*.json` profiles
were clean.

### Root cause

Four generators hardcoded a constant `sex` with no disease awareness — three
defaulted to `"male"`, one to `"female"`, which is precisely why the
gynaecological cancers came out male and the prostate BMA cases came out female:

| Generator | Was |
|---|---|
| `scripts/generate_auto_examples.py` | `"sex": "male"` |
| `scripts/generate_variant_examples.py` | `"sex": "male"` |
| `scripts/generate_verified_treatment_examples.py` | `"sex": "male"` |
| `scripts/generate_bma_examples.py` | `"sex": "female"` |

`generate_verified_treatment_examples.py` derives age and ECOG from the
indication's demographic constraints but never touched sex.

### Severity: credibility, not safety

`sex` is **inert in the engine**. Verified three ways: no reference to it
anywhere under `knowledge_base/engine/`; every mention in KB YAML is prose
rather than a structured constraint; and flipping sex on a profile produces a
byte-identical plan apart from the echoed input field.

So this was never a clinical misroute. But a male cervical-cancer patient in a
public example destroys credibility with exactly the clinicians the project is
asking to review it — 22 of the 24 are published and in the sitemap.

---

## 2. What was done

**`scripts/example_demographics.py`** (new) — a single `sex_for_disease()`
helper plus `is_sex_incoherent()` for auditing. All four generators now derive
sex from `disease.id` instead of a constant. The 24 existing profiles were
backfilled.

Verified: plans are byte-identical before and after (`algorithm_id`,
`default_indication_id`, and full track list unchanged on a sample spanning all
four affected diseases), confirming the inertness claim rather than assuming it.

### Deliberately scoped narrowly

Only **anatomically sex-specific** diseases are pinned:

```
female: DIS-CERVICAL, DIS-ENDOMETRIAL, DIS-OVARIAN,
        DIS-SERTOLI-LEYDIG-OVARIAN, DIS-VULVAR-VAGINAL-SCC
male:   DIS-PROSTATE, DIS-TESTICULAR-GCT, DIS-PENILE-SCC
```

**Breast is deliberately excluded from that list.** Male breast cancer is real
and the KB models it explicitly (`diseases/breast_cancer.yaml`: *"Male breast
cancer follows the same algorithm with gender-specific notes"*). Breast gets a
*preferred default* of female for epidemiological plausibility, but existing
male breast profiles are valid and were not rewritten. Sex is a property of the
patient, not the tumor; over-constraining it would make real patients
unrepresentable.

Noted but not changed: 8 of 30 breast profiles are male. None is individually
wrong, but a 27% male rate is epidemiologically implausible and is an artifact
of the same hardcoded default. Now that generators default breast to female,
new profiles will be plausible; if male breast coverage is wanted it should be
one explicitly-labelled intentional profile rather than 8 incidental ones.

---

## 3. What was deliberately NOT changed

**The questionnaires.** All 78 offer both "Male" and "Female" regardless of
disease, so the cervical questionnaire offers "Male". This was investigated and
rejected as a fix, for four reasons:

1. **It would be a clinical regression.** Restricting breast to female would
   contradict the KB's own disease definition and make ~1% of breast cancers
   unrepresentable. A transgender man with a cervix can develop cervical
   cancer; a transgender woman can develop prostate cancer. Hard-restricting an
   enum on a field with no plan effect makes those patients unrepresentable.
2. **It is a documented design decision, not an oversight.**
   `quest_hcv_mzl_1l.yaml` states `helper: "Does not affect the HCV-MZL 1L
   algorithm. Collected for the render layer."` and `quest_mm_1l.yaml` uses sex
   for a pregnancy-contraindication display label that *requires* both options.
3. **The convention predates the generator.** 3 of the 78 questionnaires are
   hand-authored and carry the same both-sexes block; the generator copied the
   house convention rather than introducing it.
4. **The deferral path is a no-op anyway.** `generate_stub_questionnaires.py`
   skips files that already exist, so "fix the generator, regenerate later"
   would change nothing without deleting files first — which would discard any
   clinician edits made meanwhile.

Questionnaires also live under `knowledge_base/hosted/content/`, so changing
them is §6.1-gated regardless.

---

## 4. Follow-up worth considering

A cheap guard against regression: add `is_sex_incoherent()` to the example-audit
scripts or a test, so a future generator change cannot silently reintroduce a
male ovarian-cancer profile. Not done here to keep this change tooling-only.
