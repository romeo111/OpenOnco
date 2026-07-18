# Track materialization ignores `biomarker_requirements_required`

**Created:** 2026-07-18-1615
**Status:** proposed, NOT started — deliberately not fixed
**Gate:** engine half ungated; the KB half is CHARTER §6.1 clinical content
**Origin:** gallery audit on `claude/gallery-examples-outdated-eb7f06`

> **Read this before touching `_track_filter.py`.** The obvious one-line fix
> deletes real treatment options from 35% of example profiles and breaches a
> CHARTER safety invariant. This plan exists because the fix is *not* small.

---

## 1. The defect

An EGFR-T790M lung-cancer patient is shown **15 treatment tracks**, including
targeted therapies for drivers they demonstrably do not have — and two the
profile explicitly records as **negative**.

Reproduced with `generate_plan()` on
`examples/patient_showcase_nsclc_egfr_t790m_2l.json` (the profile records
`"EGFR": "T790M"`, `"ALK": "negative"`, `"ROS1": "negative"`):

```
aggressive  IND-NSCLC-2L-EGFR-POST-OSI-AMI-LAZ      default=True
standard    IND-NSCLC-2L-EGFR-EX20INS-AMIVANTAMAB   ← exon-20 drug, patient has T790M
aggressive  IND-NSCLC-ALK-2L-LORLATINIB             ← patient is ALK-negative
standard    IND-NSCLC-2L-ROS1-POST-CRIZ-ENTRECTINIB ← patient is ROS1-negative
aggressive  IND-NSCLC-2L-ROS1-REPOTRECTINIB
standard    IND-NSCLC-2L-KRAS-G12C-SOTORASIB
aggressive  IND-NSCLC-2L-KRAS-G12C-ADAGRASIB
standard    IND-NSCLC-2L-MET-EX14-CAPMATINIB
standard    IND-NSCLC-2L-MET-EX14-TEPOTINIB
standard    IND-NSCLC-2L-MET-AMP-CAPMATINIB
standard    IND-NSCLC-2L-BRAF-V600E-DAB-TRAM
standard    IND-NSCLC-2L-RET-FUSION-SELPERCATINIB
standard    IND-NSCLC-2L-NTRK-LAROTRECTINIB
standard    IND-NSCLC-2L-HER2-MUT-T-DXD
standard    IND-NSCLC-2L-PD-L1-POST-IO-DOCETAXEL
```

Zero warnings. These are fully materialized clinical tracks with drug names —
not actionability-table rows.

### Root cause

`biomarker_requirements_required` and `value_constraint` are **never consulted
during track materialization**. There is no required-biomarker gate to be
lenient or strict about. The only biomarker filter is the *exclusion* path:

`knowledge_base/engine/plan.py` track loop:
```python
patient_biomarkers = patient.get("biomarkers") or {}
tracks: list[PlanTrack] = []
for ind_id in current_candidate_ids:
    ind = _resolve(entities, ind_id)
    if ind and is_track_excluded(ind, patient_biomarkers):
```

`knowledge_base/engine/_track_filter.py`:
```python
excluded = applicable.get("biomarker_requirements_excluded") or []
if not excluded:
    return False          # no exclusions → never drop
```

Both offending indications declare `biomarker_requirements_excluded: []`, so
`is_track_excluded` short-circuits before any comparison. `grep
biomarker_requirements_required knowledge_base/engine/` returns hits only in
`mdt_orchestrator.py` (downstream reporting) — never in the gating path.

**There are three structurally identical call sites, not one.** A fix that
touches only the first leaves two paths unguarded:

| Site | Path |
|---|---|
| `plan.py` current-line track loop | the one above |
| `plan.py` sequencing track loop | same exclusion-only gate; `continue`s silently |
| `plan.py` `_find_prevention_indications` | PreventionPlan path, same defect |

---

## 2. Why the obvious fix is wrong

Both candidate policies were simulated across all 781 example profiles that
produce a plan.

**Lenient gate** (drop only on explicit contradiction — the policy
`_track_filter.py` documents in its own module docstring): drops **0 of 15**
spurious tracks. The patient has no EGFR/ROS1/KRAS/MET/BRAF/RET/NTRK/HER2 keys
*at all*, so there is nothing to contradict. Zero benefit.

**Strict gate** (missing required biomarker → drop the track): fixes this case
correctly (15 → 2), but across the corpus removes **747 of 2320 tracks**:

- 258 profiles (33%) lose ≥1 track
- **96 profiles fall to ZERO tracks**
- **175 profiles fall to ONE track**

That is **271 profiles (35%) breaching `specs/CHARTER.md` §15 C4** — *"Always
≥2 tracks, never a single binding directive."* That invariant is the project's
FDA-non-device positioning, not a style preference. A strict gate as a
standalone change converts a cosmetic bug into a regulatory-posture breach.

---

## 3. Two further defects in the comparison layer

`_track_filter.py`'s existing matcher is **not** a red herring — it is broken in
both directions on real KB data. Its 12 unit tests pass only because they use
short clean tokens ("MSI-H", "V600E"); the KB actually stores multi-clause
English prose.

**False positive — punctuation collision.** For an EGFR-Ex20ins patient,
`IND-NSCLC-2L-EGFR-POST-OSI-AMI-LAZ` is dropped because the token-intersection
fallback finds exactly one shared token between the patient value and the
indication's constraint: the **em-dash `—`**. Deleting the em-dash flips the
result. A treatment option is withheld because two prose strings share a dash.

**False negative.** `ind_nsclc_2l_pdl1_post_io_docetaxel.yaml` authors
`biomarker_id: BIO-ALK-FUSION` with `value_constraint: "ALK-rearranged excluded
— targeted therapy preferred"`. For a patient recorded `BIO-ALK-FUSION:
"positive"` this returns False — the `pv_is_presence` branch skips it. The KB
author's explicit clinical intent silently never fires.

### Scale of the prose problem

Of 831 indications: **238** declare `biomarker_requirements_required`, carrying
**333 constraints**, of which **208 are free text longer than 40 characters**.
Those strings are not machine-comparable in their current form.

---

## 4. Recommended shape of a real fix

Three coordinated parts. Do not ship part 2 alone.

1. **Normalize the constraint vocabulary** (KB, §6.1-gated). Give
   `BiomarkerRequirement` a structured form — `presence:
   Literal["positive","negative","unknown"]` plus an optional free-text
   `qualifier` — and migrate the 333 constraints. `project_roadmap`'s
   "Engine bugs / fixes" section already proposes exactly this as its P3 item;
   this plan is the evidence that P3 is the load-bearing step, not an optional
   cleanup.
2. **Add the required-biomarker gate** to all three call sites (engine,
   ungated), reading the structured field — never the prose.
3. **Guarantee a fallback track.** Before enabling the gate, ensure every
   algorithm yields a driver-negative/default option so no profile can fall
   below two tracks. Re-run the 781-profile simulation and require **zero**
   profiles at <2 tracks before merge.

Also repair the em-dash tokenization and the `pv_is_presence` skip in
`_track_filter.py` (engine, ungated) — but note that repairing them *changes
which tracks appear*, so it needs the same corpus-wide before/after diff.

### Sequencing

```
P0  structured BiomarkerRequirement schema + migration   (§6.1)
P1  _track_filter comparison repairs + corpus diff       (engine)
P2  required gate at all 3 call sites, behind a flag     (engine)
P3  fallback-track audit; flip the flag on               (engine + §6.1 review)
```

---

## 5. Non-goals

- **Do not** "just add a required check" to the current-line loop. That is the
  strict gate simulated above: 96 profiles to zero tracks.
- **Do not** hand-edit individual `value_constraint` strings to dodge the
  em-dash bug. 208 of them are long prose; patching one moves the problem.
- **Do not** treat this as the T790M fix. The T790M default-track defect has
  its own plan (`docs/plans/nsclc_t790m_osimertinib_2l_2026-07-18-1550.md`) and
  a different root cause — a missing indication. An engine-only fix here does
  **not** resolve it.

---

## 6. Verification protocol

Any change must produce, before/after:

1. Track-count distribution across all 781 plan-producing profiles; **zero**
   profiles may drop below 2 tracks.
2. Full pytest, diffed against baseline. As of 2026-07-18 the suite has a known
   pre-existing failure set (e.g.
   `test_curated_chunk_e2e[patient_hnscc_cps_high_pembro_mono.json]`, stale
   after the CPS≥20 wiring in `e07f108c6a`) — diff, never read absolute counts.
3. KB validator: 0 reference and 0 contract errors.
4. Explicit re-check of the T790M profile and an ALK-positive profile, to show
   the gate removes wrong tracks without removing right ones.

---

## 7. Suggested branch

```
fix/track-biomarker-gating-2026-07-18-1615
```

Never commit to `master`; never `git add -A`; never `--no-verify`.
