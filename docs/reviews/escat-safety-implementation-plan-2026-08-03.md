# ESCAT actionability safety implementation plan — 2026-08-03

## Decision

The existing BMA collection is useful as an auditable research/context layer,
but it is not yet safe to present as clinically reviewed ESCAT actionability.
No tier may be inferred, upgraded, or rewritten by a script or language model.
Clinical co-leads must adjudicate each claim against its tumour and therapy
context, then provide two independent, current sign-offs.

The framework reference is Mateo et al., 2018, *Annals of Oncology*
([open full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC6158764/)).
The implementation follows CHARTER §6 and §8: ESCAT is context for review,
never a treatment-track ranking or selection input.

## Baseline observed on 2026-08-03

The reproducible audit at `--as-of 2026-08-03` scanned 475 BMA records.
It found 0 records meeting the clinical-use gate, 40 records absent from the
older 435-record ESCAT manifest, and a latest hosted CIViC snapshot dated
2026-04-25 (100 days old; operating limit 45 days). These are workflow and
provenance findings, not clinical determinations that any individual tier is
wrong.

## Implemented controls

1. **Full, explicit vocabulary.** The schema supports `IA`, `IB`, `IC`,
   `IIA`, `IIB`, `IIIA`, `IIIB`, `IVA`, `IVB`, `V`, and `X`. Historic broad
   `IV` remains loadable only to support migration and is an audit finding.
2. **Applicability before tier.** Every BMA has an `actionability_scope` and
   `escat_applicability`; non-therapeutic records can be explicitly
   `not_applicable` with a reason instead of being forced into ESCAT.
3. **Evidence dossier.** An applicable record needs clinician-authored tier
   rationale and source/therapy/tumour/study-design evidence records.
4. **Version-pinned dual review.** Two distinct in-scope reviewer sign-offs
   must match the BMA's `last_verified`. Editing that field invalidates the
   gate until the evidence is reviewed again.
5. **Safe presentation.** Unready rows stay visible for audit/tumour-board
   discussion, but the renderer marks them as pending clinical review. The
   engine continues not to use them for track selection.
6. **Deterministic audit and refresh.** `scripts/audit_escat_readiness.py`
   produces JSON/Markdown queues for evidence gaps, stale CIViC data,
   taxonomy/evidence-ID mismatches, legacy tier IV, stale approvals, and
   omitted manifest rows. The monthly CIViC workflow attaches this queue to
   its review PR.

## Clinical remediation queue

Clinical co-leads process BMA records in this order:

1. **Critical:** IA/IB records without per-source evidence or without a
   current clinical-use gate; verify source, tumour, alteration, drug, and
   endpoint before any status is changed.
2. **Major:** taxonomy/evidence-ID mismatch flags, broad legacy IV, BMA
   records added after the prior manifest, and snapshot staleness.
3. **Minor:** assign an evidence lane (`standard_care`, molecular option,
   resistance/avoidance, trial/research, or insufficient evidence) for each
   evidence source.

For every candidate record the reviewer chooses exactly one of:

- `applicable` + `therapeutic_predictive` + a complete evidence dossier;
- `not_applicable` + documented reason; or
- `review_required` while evidence/taxonomy remains unresolved.

The audit's mismatch flags are deliberately conservative. They are prompts
to compare BMA qualifier, `BIO-*` lookup, and CIViC EID rather than evidence
that a clinical claim should be changed automatically.

## Release criteria

A BMA may be marked clinically ready only when all conditions hold:

| Requirement | Machine check | Human responsibility |
|---|---|---|
| Therapeutic-predictive scope and explicit applicability | Schema + release gate | Co-lead classifies the claim |
| Complete ESCAT evidence dossier | Schema + release gate | Co-lead writes rationale from permitted sources |
| Correct alteration/tumour/EID linkage | Audit warning | Co-lead reconciles primary source context |
| Two current in-scope approvals | Release gate | Two distinct authorized reviewers sign off |
| Fresh CIViC snapshot | Monthly audit | Reviewer assesses any drift in the PR |

## Operational commands

```powershell
py -3.12 -m scripts.audit_escat_readiness `
  --as-of 2026-08-03 `
  --markdown-output docs/reviews/escat-readiness-2026-08-03.md `
  --json-output docs/reviews/escat-readiness-2026-08-03.json
```

After a reviewer changes evidence, set `last_verified` to the reviewed
revision, then collect fresh approvals through `scripts/clinical_signoff.py`.
The sign-off command now pins BMA approval to `last_verified`, not to an
unrelated `last_reviewed` fallback.

## Non-goals and guardrails

- Do not bulk rewrite `escat_tier`, clinical summaries, or treatment claims
  from CIViC level, an LLM, or audit output.
- Do not present evidence-source levels as an ESCAT conversion.
- Do not allow ESCAT readiness to affect declarative algorithm track choice.
- Do not merge a CIViC refresh solely because the technical workflow passed;
  required clinical review remains mandatory.
