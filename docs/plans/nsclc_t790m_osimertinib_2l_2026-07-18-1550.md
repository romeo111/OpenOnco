# NSCLC T790M → osimertinib 2L — indication authoring + prior-therapy discriminator

**Created:** 2026-07-18-1550
**Status:** proposed, not started
**Gate:** CHARTER §6.1 — clinical content, two Clinical Co-Lead sign-offs required before merge
**Origin:** surfaced by the gallery audit on `claude/gallery-examples-outdated-eb7f06`
(commit `ed3bffd9eb`); the flagship showcase case renders a clinically wrong plan.

---

## 1. The defect

`showcase-nsclc-egfr-t790m-2l` describes a patient who progressed on **erlotinib**
(1st-generation EGFR-TKI) with acquired T790M. They are **osimertinib-naive**:

```json
// examples/patient_showcase_nsclc_egfr_t790m_2l.json → findings.prior_lines
[{"line": 1, "regimen": "erlotinib", "duration_months": 18,
  "best_response": "PR", "outcome": "PD with acquired T790M"}]
```

The engine routes them to `IND-NSCLC-2L-EGFR-POST-OSI-AMI-LAZ` as the ★DEFAULT
track. That indication's own gate
(`knowledge_base/hosted/content/indications/ind_nsclc_2l_egfr_post_osi_ami_laz.yaml`)
requires the opposite patient:

```yaml
molecular_subtype: EGFR_MUTATED_POST_OSIMERTINIB
stage_requirements:
  - "Disease progression on osimertinib 1L (FLAURA / FLAURA2 sequencing)"
```

**Osimertinib appears in none of the 15 rendered tracks.** The page shows the
correct answer in its biomarker table and a different answer in its plan.

Blast radius is not limited to the demo: this is a knowledge-base gap, so the
same plan is generated fresh for any T790M patient entering through `/try.html`.

### What the KB already says

The position "T790M after 1G/2G TKI → osimertinib 2L" is **already asserted in
the knowledge base in four places**. This work ratifies and wires an existing
position; it does not introduce a new clinical claim.

| Location | Assertion |
|---|---|
| `biomarker_actionability/bma_egfr_t790m_nsclc.yaml` | `escat_tier: IA`; "Osimertinib (3rd-gen) is active against T790M and is standard 2L (AURA3, Mok et al. 2017)"; `regulatory_approval.fda: osimertinib — T790M-positive NSCLC after EGFR-TKI progression (FDA approved 2015/2017)` |
| `redflags/rf_nsclc_egfr_t790m_actionable.yaml` | "drives 2L switch to osimertinib (AURA3 — mPFS 10.1 vs 4.4 mo with platinum-pem)"; `severity: critical` |
| `algorithms/algo_nsclc_metastatic_2l.yaml` (notes) | "EGFR sub-branches (**deferred** — separate Indications when authored): … T790M-positive post-1G/2G TKI → osimertinib 2L" |
| `algorithms/algo_nsclc_metastatic_2l.yaml` (WIRING GAPS) | "Resistance-mutation-driven precise sub-branches (T790M, C797S, G2032R, G595R) **deferred to dedicated future Indications**" |

Step 3 of the algorithm also documents the shortcut explicitly:

```yaml
# EGFR activating (ex19del / L858R / T790M / C797S) post-osimertinib 1L
# → ami+laz (MARIPOSA-2). T790M acquired on 1G/2G TKI also routes here.
```

So the misroute is a **known, documented, deliberately deferred simplification**,
not an oversight. This plan closes it.

### Building blocks that already exist

Nothing new needs to be invented at the drug or evidence layer:

- `drugs/osimertinib.yaml` — drug entity ✔
- `regimens/reg_osimertinib_nsclc.yaml` — osimertinib regimen ✔
- `sources/src_aura3_mok_2017.yaml` — `SRC-AURA3-MOK-2017`, NEJM, PMID 27959700,
  DOI 10.1056/NEJMoa1612674, `evidence_tier: 2`, `currency_status: current` ✔
- `RF-NSCLC-EGFR-T790M-ACTIONABLE` — already fires correctly and already declares
  `shifts_algorithm: [ALGO-NSCLC-METASTATIC-2L]` ✔

`SRC-AURA3-MOK-2017` is currently cited by **zero indications** (only biomarkers,
the BMA, and two red flags reference it).

---

## 2. The actual blocker: there is no prior-therapy discriminator

This is the part that makes the task non-trivial, and it must be solved before
the indication can be wired.

To route correctly the engine must distinguish **osimertinib-naive T790M**
(→ osimertinib) from **progression on osimertinib 1L** (→ ami+laz). Today it
cannot. Flattening the showcase profile yields:

```
egfr_t790m                 = True          ← RF fires correctly
prior_lines                = [{'line': 1, 'regimen': 'erlotinib', ...}]   ← raw list
prior_egfri_received       = <ABSENT>
prior_egfri_progression    = <ABSENT>
best_response_to_egfri     = <ABSENT>
prior_osimertinib          = <ABSENT>
```

`prior_lines` survives flattening as a **list of dicts**. The clause evaluator
resolves flat scalar keys only, so no `finding:` clause can express "the prior
line was osimertinib".

### This is a systemic gap, not a one-case gap

`redflags/universal/rf_universal_prior_egfri_progression.yaml`
(`RF-PRIOR-EGFRI-PROGRESSION`, `relevant_diseases: ["*"]`) triggers on exactly
those absent scalars:

```yaml
any_of:
  - finding: "prior_egfri_progression"
    value: true
  - all_of:
      - finding: "prior_egfri_received"
        value: true
      - finding: "best_response_to_egfri"
        value: "PD"
```

Measured across the repo:

- **36** example profiles carry `findings.prior_lines`
- **0** example profiles carry any of those three scalar keys
- the **only** file in the whole KB mentioning them is that red flag itself

→ **`RF-PRIOR-EGFRI-PROGRESSION` is inert KB-wide — it can never fire.** Any
prior-therapy red flag written against scalar keys has the same problem, because
prior therapy is authored as `prior_lines` lists.

---

## 3. Options for the discriminator

| | Approach | Pros | Cons |
|---|---|---|---|
| **A** | Author explicit scalar findings (`prior_osimertinib: false`) into affected example profiles + the NSCLC questionnaire | No engine change; smallest diff | Every profile must carry the field; silently wrong for any profile that omits it (absence ≠ recorded-false — the failure mode that got a conversion reverted in PR #632); leaves the universal RF inert |
| **B** | Derive scalars from `findings.prior_lines` in `_flatten_findings` (e.g. `prior_regimens: [...]`, `prior_egfri_received`, `prior_osimertinib`) | Fixes the systemic gap; revives `RF-PRIOR-EGFRI-PROGRESSION` for all 36 profiles; no per-profile authoring | Engine change → wider blast radius; needs drug-name normalisation (free-text `regimen` strings); must be regression-tested across the full suite |
| **C** | B for derivation + A for the questionnaire so live users supply it directly | Correct for both synthetic and real patients | Largest scope |

**Recommendation: C, staged as B → A.** Do B first behind full-suite
verification, since it is the only option that also fixes the inert universal red
flag; then add the questionnaire field so real `/try.html` users produce the same
findings. Do **not** start with the indication — without a discriminator it
cannot be gated correctly.

⚠️ **`prior_lines[].regimen` is free text.** Derivation must normalise against
the `drugs/` catalogue rather than substring-match; "osimertinib" vs
"osimertinib + chemo" vs "Tagrisso" must not silently diverge. Enumerate the
distinct values across all 36 profiles before writing the normaliser.

---

## 4. Work breakdown

### Phase 0 — reproduce and baseline (no changes)
1. `generate_plan()` on `examples/patient_showcase_nsclc_egfr_t790m_2l.json`;
   record all 15 tracks, the ★DEFAULT, and the fired red flags.
2. Run the full pytest suite and **record the baseline failure set**. As of
   2026-07-18 `tests/test_build_site.py` has 3 pre-existing failures
   (`test_capabilities_shows_numerical_metrics`,
   `test_engine_bundle_excludes_heavy_unused_subtrees`,
   `test_try_examples_are_curated_and_filter_by_disease_id`) — confirmed present
   at `c3c9db8a0b` by running them in a detached worktree. Do not attribute
   these to your change; diff before/after rather than reading absolute counts.

### Phase 1 — discriminator (engine, no clinical gate)
3. Extend `_flatten_findings` in `knowledge_base/engine/plan.py` to derive scalar
   prior-therapy findings from `findings.prior_lines`, normalised against the
   drug catalogue.
4. Unit tests: prior line present / absent / multiple lines / unknown drug name /
   `prior_lines` missing entirely. **Absence must remain distinguishable from
   recorded-false.**
5. Confirm `RF-PRIOR-EGFRI-PROGRESSION` now fires where clinically appropriate,
   and audit the 36 `prior_lines` profiles for plans that change as a result.
   **Any plan that changes is a finding to review, not automatically a win.**

### Phase 2 — indication (clinical content → §6.1)
6. Author `IND-NSCLC-2L-EGFR-T790M-OSIMERTINIB` per
   `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md`, modelled on the field shape of
   `ind_nsclc_2l_egfr_post_osi_ami_laz.yaml`. Reuse `reg_osimertinib_nsclc.yaml`;
   cite `SRC-AURA3-MOK-2017` plus `SRC-NCCN-NSCLC-2025` /
   `SRC-ESMO-NSCLC-METASTATIC-2024`. Mark `draft: true`,
   `reviewer_signoffs: 0`.
7. **Do not author dosing from memory.** Take it from the existing regimen entity
   or an explicit cited source; if it cannot be sourced, leave it unstated (the
   discipline applied to I-131 MIBG in PR #633).

### Phase 3 — algorithm wiring (clinical content → §6.1)
8. Add `IND-NSCLC-2L-EGFR-T790M-OSIMERTINIB` to `output_indications` in
   `algo_nsclc_metastatic_2l.yaml`. **This is mandatory** — `plan.py` builds
   tracks only from `output_indications`; an indication reachable in the tree but
   missing from that list is silently dropped (the class of bug fixed at scale in
   PR #629).
9. Split step 3 so osimertinib-naive T790M routes to the new indication and
   post-osimertinib continues to ami+laz. Update the step comment, which
   currently documents the old shortcut.
10. Remove the now-closed item from the algorithm's "EGFR sub-branches
    (deferred)" and "WIRING GAPS" notes, in both `notes` and `notes_ua`.

### Phase 4 — verification
11. `generate_plan()` on the showcase profile: the ★DEFAULT must be the new
    osimertinib indication; `IND-NSCLC-2L-EGFR-EX20INS-AMIVANTAMAB` must no
    longer appear (wrong variant — exon 20 insertion for a T790M patient).
12. Construct a **post-osimertinib** T790M profile and confirm it still routes to
    ami+laz. Guarding against over-correction is as important as the fix.
13. KB validator: 0 reference and 0 contract errors.
14. Full pytest, diffed against the Phase 0 baseline. Zero new failures.
15. Rebuild the site; confirm `docs/cases/showcase-nsclc-egfr-t790m-2l.html` and
    its `/ukr/` twin render the corrected plan.
16. Update the gallery card text in `scripts/site_cases.py` if the summary no
    longer matches the produced plan.

### Phase 5 — sign-off
17. Two Clinical Co-Lead approvals per CHARTER §6.1 before merge. Phase 1 alone
    (engine + tests) may land independently — it is not clinical content — but it
    must not be merged with Phases 2-3 in a single commit.

---

## 5. Explicit non-goals

- **Do not** touch the `value_constraint` matcher. The gallery audit flagged it
  separately (an `EGFR_EX20INS` indication being served to a T790M patient) and
  it has blast radius across all indication matching. Scope it on its own.
  See `project_roadmap` "Engine bugs / fixes" — its P3 item proposes typing
  `BiomarkerRequirement` as `presence` + `qualifier`, which would close that class.
- **Do not** widen this into the 128-dead-step prose-condition backlog.
- **Do not** author C797S, G2032R or G595R sub-branches. Same deferred family,
  separate evidence, separate review.
- **Do not** self-merge Phases 2-3 under the §6.1 dev-mode exemption. The
  exemption covers not flagging §6.1 as unmet during v0.1; it is not a licence
  for an agent to select a regimen (CLAUDE.md: LLMs do "not: choosing regimens,
  generating dosing, interpreting biomarkers for treatment selection").

---

## 6. Open questions for the reviewers

1. **Sequencing preference.** With osimertinib now standard 1L (FLAURA), how
   should the KB treat a patient who received a 1G/2G TKI in 1L in 2026 — a
   legacy pathway to model faithfully, or one to flag as non-standard prior care?
   The BMA calls T790M "rarely encountered de novo since osimertinib has moved to
   1L"; the algorithm calls the pathway "increasingly rare".
2. **Platinum-pemetrexed comparator.** AURA3 randomised against platinum-pem.
   Should that be authored as the alternative track, or is a single track
   sufficient?
3. **Citation integrity.** `rf_nsclc_egfr_t790m_actionable.yaml` quotes AURA3
   efficacy in its `definition` ("mPFS 10.1 vs 4.4 mo") but its `sources:` list
   is `SRC-NCCN-NSCLC-2025`, `SRC-ESMO-NSCLC-METASTATIC-2024`,
   `SRC-FLAURA-SORIA-2018` — **`SRC-AURA3-MOK-2017` is absent.** Adding it looks
   like a straightforward citation fix under CLINICAL_CONTENT_STANDARDS; confirm.
4. **Scope of Phase 1.** Reviving `RF-PRIOR-EGFRI-PROGRESSION` across 36 profiles
   may change plans beyond NSCLC (it is `relevant_diseases: ["*"]`, and CRC
   anti-EGFR mAbs are in its definition). Land Phase 1 repo-wide, or gate the
   derived findings to NSCLC first and widen later?

---

## 7. Suggested branch

```
fix/nsclc-t790m-osimertinib-2l-2026-07-18-1550
```

Per the repo's chunk-naming convention (`YYYY-MM-DD-HHMM` + short scope).
Never commit to `master`; never `git add -A`; never `--no-verify`.
