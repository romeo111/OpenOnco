# RF Wiring Audit — 2026-04-25

**Owner:** Phase 1 of redflag-quality plan. Status: closed (1 deferred).

## TL;DR

96 RedFlag entities total. Before this audit:
- 78 of 96 declared `shifts_algorithm: [ALGO-X]` but were **not actually
  referenced** by ALGO-X's `decision_tree`. They fired in evaluator but had
  zero effect on Plan output.

After this audit:
- 81 RFs have `shifts_algorithm: []` (scaffold-pending or metadata-only).
- 14 RFs are correctly wired.
- **1 RF remains orphan** — see [Deferred](#deferred).

## What changed

### 1. Two real wiring fixes

| RF | Was | Now |
|----|-----|-----|
| `RF-DECOMP-CIRRHOSIS` | claimed `ALGO-HCV-MZL-1L`, not in tree | wired as new `step: 1` (Child-Pugh B/C → de-escalate to ANTIVIRAL) |
| `RF-TCELL-CD30-POSITIVE` (× ALCL only) | wired in PTCL/AITL/MF-SEZARY, but ALGO-ALCL-1L used a free-text condition `"CD30+ (universal in systemic ALCL)"` | replaced free-text condition with `red_flag: RF-TCELL-CD30-POSITIVE` for consistency |

ALGO-HCV-MZL-1L decision_tree now: decomp-cirrhosis check → bulky/transformation
check → indolent HCV+ check. Three steps instead of two.

### 2. Scaffold cleanup (75 RFs)

`scripts/scaffold_redflags.py` was pre-filling `shifts_algorithm: [ALGO-X]`
for every generated scaffold. That created the illusion of 75 wired RFs that
were actually placeholder content with `definition: "TODO: ..."`,
`sources: [SRC-TODO]`, and trigger-placeholder findings. Wiring scaffolds
into algorithms would have meant production decision-trees branching on
fictional clinical content.

Action taken:
- All 75 scaffold YAMLs had `shifts_algorithm` cleared to `[]`, with an
  inline comment naming this audit and citing
  `REDFLAG_AUTHORING_GUIDE` §4 wiring rule 1.
- The scaffold script (`scripts/scaffold_redflags.py`) was patched so future
  scaffolds emit `shifts_algorithm: []` with a clinician-author TODO.

The clinician who clears `draft: false` on a scaffold must:
1. Add a step in the named algorithm's `decision_tree` that references the RF.
2. Set `shifts_algorithm: [ALGO-X]` to match.
3. Replace `definition`, `definition_ua`, `trigger`, `sources`, `last_reviewed`.

Per spec §7 authoring checklist, all six TODOs must be done before merge.

## Deferred

### `RF-HBV-COINFECTION` (× ALGO-HCV-MZL-1L)

`clinical_direction: hold` is clinically correct (NCCN: anti-CD20 must be
held until HBV prophylaxis is started). But the current 2-arm
ALGO-HCV-MZL-1L (`ANTIVIRAL` vs `BR-AGGRESSIVE`) does not model a
"hold-and-start-prophylaxis" branch — both arms presume the patient is
ready for therapy.

Three resolution paths, ranked by clinical fidelity:

1. **Add a third Indication** `IND-HCV-MZL-1L-HOLD-FOR-HBV-PROPHYLAXIS`
   that defers chemo, mandates entecavir/TDF prophylaxis, and re-enters
   the algorithm after seroconversion stabilization. **Highest fidelity,
   most authoring work.** Requires source citations + two-reviewer signoff.
2. **Reclassify RF as `investigate`** with empty `shifts_algorithm`. The
   `notes` already say "Triggers SUP-HBV-PROPHYLAXIS as a mandatory parallel
   intervention" — this is the supportive-care mechanism, parallel to
   indication choice. **Loses the "hold" semantics but matches what the
   engine actually does today.**
3. **Wire into ALGO-HCV-MZL-1L step 1** routing HBsAg+ → ANTIVIRAL (gives
   HBV-prophylaxis-friendly path while indication is being held). **Bends
   the meaning of ANTIVIRAL** but is the smallest engine-side change.

This is a clinical co-lead decision per CHARTER §6.1. Recommendation: path
(1) is correct long-term; path (2) is the safe interim if authoring
bandwidth is tight.

## Metrics

|  | Before | After |
|---|---|---|
| Orphan RFs | 78 / 96 | 1 / 96 |
| Wired RFs | 12 / 96 | 14 / 96 |
| Metadata-only / scaffold-pending | 6 / 96 | 81 / 96 |
| Drafts | 75 / 96 | 75 / 96 (unchanged — Phase 4 work) |
| Single-source (<2 sources) | 93 / 96 | 93 / 96 (unchanged — Phase 4 work) |

Phase 1 acceptance criterion (G1: 0 orphans) achieved modulo the 1 deferred
clinical decision. Add CI gate per Phase 7 to prevent regression.
