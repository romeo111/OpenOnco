# RedFlag fixture coverage — baseline 2026-04-27

## Pre-pass inventory

Walked `knowledge_base/hosted/content/redflags/` and cross-checked
`tests/fixtures/redflags/RF-X/{positive,negative}.yaml`.

| Bucket                     | Count |
|----------------------------|-------|
| Total RF YAML files        |   282 |
| Non-draft RFs              |   280 |
| Draft RFs                  |     2 |
| RFs with both fixtures     |   279 |
| RFs with only positive     |     0 |
| RFs with only negative     |     0 |
| RFs with no fixtures       |     3 |

The 3 RFs missing both fixtures:
- `RF-CML-COMORBIDITY-COMPLEX` (draft)
- `RF-DLBCL-TRANSFORMATION-PROGRESSION` (draft)
- `RF-PROSTATE-PSA-PROGRESSION` (non-draft, no fixtures)

CLAUDE.md `Current state` already records that RedFlag quality phases
1-7 are done with golden fixtures auto-generated and 220 RF-tests
green; this pass closes the long tail (drafts + the prostate PSA RF
that landed after the prior sweep).

## Plan

1. Run `scripts/generate_redflag_fixtures.py --include-drafts` to
   skeleton-generate the 6 missing fixtures (3 RFs x 2).
2. Manually rewrite all 6 with realistic clinical scenarios + comments
   (auto-gen positives only fire the first `any_of` clause, which is
   over-minimal for clinical review).
3. Run `pytest tests/test_redflag_fixtures.py` — target green for the
   data-driven fixture tests.

## Pre-existing test failures (not caused by this pass)

`test_no_orphan_red_flag_decl` and `test_investigate_flags_do_not_shift`
fail today against the current RF/Algorithm content. These are
structural integrity issues in the RF YAMLs themselves (e.g.,
`RF-CML-COMORBIDITY-COMPLEX` has `clinical_direction=investigate` AND
declares `shifts_algorithm`), not fixture issues. Resolving them
requires editing the RFs or Algorithms, which is out of scope for this
pass per the task constraints ("Don't modify RFs themselves, schemas,
or any code. Only generate / edit fixtures").

Pre-existing orphans flagged:
- `RF-HCV-MZL-FRAILTY-AGE` -> `ALGO-HCV-MZL-1L`
- `RF-OVARIAN-INFECTION-SCREENING` -> `ALGO-OVARIAN-ADVANCED-1L`
- `RF-OVARIAN-TRANSFORMATION-PROGRESSION` -> `ALGO-OVARIAN-ADVANCED-1L`
- `RF-CML-COMORBIDITY-COMPLEX` (investigate-shifts conflict)

These should be tracked as RF/Algorithm content TODOs in the
clinical-review queue, not as test-fixture work.
