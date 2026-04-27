# Rejection-Comment Templates

Standard maintainer responses for failed chunk PRs. Copy-paste, fill the
`<placeholder>` parts, post as PR comment, close PR with the
`status-rejected` label.

The goal is consistency: a contributor who sees a familiar template
knows what to fix without negotiating. Use the closest-matching template;
do not invent ad-hoc rejection prose.

---

## R-001 — Out-of-manifest entity

```
Thanks for the submission. The PR is rejected because one or more sidecars
target entities outside the chunk's task_manifest.txt:

<list offending sidecar paths and target_entity_ids>

The chunk-issue's manifest is the canonical scope. To re-submit:
1. Drop the out-of-manifest sidecars OR open a new chunk-task issue
   covering them.
2. Re-run `python -m scripts.tasktorrent.validate_contributions <chunk-id>`
   locally to confirm clean.
3. Force-push to this same branch.
```

---

## R-002 — Banned source used

```
Rejected. One or more sidecars reference a banned source:

<list offending paths and SRC-* IDs>

Allowed sources are listed in
https://github.com/romeo111/task_torrent/blob/main/docs/openonco-pilot-workflow.md#source-allowlist .
OncoKB / SNOMED CT / MedDRA cannot appear in contributor-authored sidecars.
For OncoKB-specific claims that lack CIViC coverage, mark
`actionability_review_required: true` and explain in
`_contribution.notes_for_reviewer` rather than citing the banned source.

Re-submit after removing banned-source references.
```

---

## R-003 — Missing or invalid AI metadata

```
Rejected. One or more sidecars are missing required AI-tool / AI-model
metadata in the `_contribution` wrapper:

<list paths>

Both `ai_tool` and `ai_model` are required. See
https://github.com/romeo111/task_torrent/blob/main/docs/openonco-pilot-workflow.md#ai-tool--model-metadata-required-non-blocking-on-acceptreject
for the rationale and allowed values.

Add the fields and re-submit.
```

---

## R-004 — Pydantic validation failure

```
Rejected. One or more sidecar payloads fail schema validation after
`_contribution:` strip:

<paste validator output>

The schema definitions in
https://github.com/romeo111/cancer-autoresearch/tree/master/knowledge_base/schemas/
are authoritative. Field names, types, enum values must match exactly.

Re-submit after fixing the schema errors.
```

---

## R-005 — Recommendation wording

```
Rejected. One or more fields use treatment-recommendation language that
violates CHARTER §8.3 (LLMs are not the clinical decision-maker):

<list paths and offending excerpts>

Allowed: "evidence supports", "guidelines list", "source attests",
"in cited trial".
Banned: "best", "preferred", "first choice", "patients should",
"we recommend", "treatment of choice".

Replace with neutral evidence wording and re-submit.
```

---

## R-006 — Invented or unresolvable SRC-*

```
Rejected. One or more `SRC-*` references do not exist in
`knowledge_base/hosted/content/sources/` and no corresponding
`source_stub_<id>.yaml` is included in the chunk directory:

<list>

Either:
- Use an existing SRC-* (resolve via `grep -rln '^id: SRC-' knowledge_base/hosted/content/sources/`)
- File a `source_stub_<id>.yaml` in this chunk dir, with full license
  classification per
  https://github.com/romeo111/cancer-autoresearch/blob/master/specs/SOURCE_INGESTION_SPEC.md §8

Re-submit.
```

---

## R-007 — Computational re-verify mismatch

```
Rejected. The maintainer-run re-verification script disagreed with the
contributor's output:

<paste mismatch summary, e.g. CIViC EID claimed not in snapshot, hosted
field changed outside the procedure's allowlist>

The chunk's "Computation" section in
https://github.com/romeo111/task_torrent/blob/main/chunks/openonco/<chunk-id>.md
is the canonical procedure. Mismatches usually mean: (a) the contributor's
AI tool diverged from the procedure (e.g. invented an EID, edited a
forbidden field), or (b) the snapshot version differed.

Re-run the procedure, re-submit. If you believe the disagreement is on
the maintainer side, comment with the specific row(s) and we'll investigate.
```

---

## R-008 — Sample re-verify below threshold

```
Rejected. Sample human re-verification on N% of the output showed
agreement below the chunk's trust threshold:

<state threshold and observed rate, e.g. "trust threshold 90%, observed 72%">

A different model or different contributor should re-execute. Common causes:
- Topic-adjacent source treated as direct support (citation verification)
- Severity tags misapplied (rec-wording audit)
- ESCAT tier overclaim (BMA drafting)

Comment if you'd like the specific failing rows; otherwise close this PR
and let another contributor pick up the chunk.
```

---

## R-009 — Multi-chunk PR

```
Rejected. This PR touches files in multiple chunk directories:

<list affected chunk ids>

TaskTorrent rule: one chunk = one PR. Split into separate PRs, one per
chunk, and re-submit.
```

---

## R-010 — Edits outside `contributions/<chunk-id>/`

```
Rejected. The PR modifies files outside `contributions/<chunk-id>/`:

<list paths>

Contributor edits are confined to the chunk's sidecar directory. If the
chunk genuinely requires changes to schemas, validators, or hosted
content, those are maintainer-only changes and need a separate PR.

Drop the out-of-scope edits and re-submit.
```

---

## R-011 — `git add -A` evidence

```
Rejected. The PR includes files that look like accidental sweep-ins
(stray .pyc, .DS_Store, editor temp files, untracked output of other
sessions):

<list files>

Per repo policy, do not use `git add -A` or `git add .`. Stage explicit
paths. Drop the unintended files and re-submit.
```

---

## R-012 — Pre-commit / `--no-verify` evidence

```
Rejected. Commits in this PR appear to bypass pre-commit hooks (e.g.
black formatting, ruff lint, schema check were skipped). Per repo policy,
`--no-verify` is not permitted.

Re-run the commit through pre-commit (`pre-commit run --all-files`),
fix anything it flags, and re-submit.
```

---

## How to compose a rejection comment

1. Pick the closest template by failure mode.
2. Fill `<placeholders>` with specifics from the failed CI run or your
   review.
3. Post as a PR comment.
4. Apply labels `status-rejected` and remove `status-in-review`.
5. Close the PR (keep branch — contributor force-pushes if they fix).
6. If the chunk is `status-active`, do NOT free the active slot until
   the contributor confirms they are dropping the work or 14 days pass
   without re-submission.
