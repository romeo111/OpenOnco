# [Chunk] tier2-bio-prostate-2026-05-01-003

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Tier-2 biomarker coverage` from current biomarker count 125 toward full second-wave coverage (28 new biomarkers across W7a-W7f) for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W7c -- Prostate (3 bio)`.

## Manifest IDs (this chunk's allowlist)

- bio_ar_amplification (distinct from AR-V7 splice variant; ARSI-resistance complement)
- bio_tmprss2_erg_fusion (prognostic, not Tx-modifying)
- bio_dmmr_prostate (small-pop pembro eligibility -- verify if existing bio_dmmr_solid covers; if so, drop and document)

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly outside the allowlist.
- KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK -- all entities valid".
- pytest fixture green: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed".
- Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` should only list paths in the allowlist below.
- Sources cited (no invented IDs); flag missing trial Sources in commit body.


## Reference YAML pattern

`git show origin/master:knowledge_base/hosted/content/biomarkers/bio_ar_v7.yaml`

## Sources to cite

- KEYNOTE-199 (pembro mCRPC)
- PROPHECY trial (AR-V7)
- TMPRSS2-ERG prognostic literature (PubMed)

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/biomarkers/bio_ar_amplification.yaml
knowledge_base/hosted/content/biomarkers/bio_tmprss2_erg_fusion.yaml
knowledge_base/hosted/content/biomarkers/bio_dmmr_prostate.yaml
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/tier2-bio-prostate-2026-05-01-003 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): tier2-bio-prostate-2026-05-01-003

<one-line scope description per roadmap section>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/tier2-bio-prostate-2026-05-01-003
```

Self-push authorized per CLAUDE.md commit `3a60901b`.

## Stop conditions

- KB validator regresses.
- pytest fixture drops below 62 passed.
- Edits land outside the allowlist.
- Required source ID does not exist in KB -- flag in commit body, do not invent.
- Two chunks editing the same file (coordination bug, escalate).

## Never

`git add -A`, `--no-verify`, force-push, branch deletion, edits to existing YAML beyond the allowlist.
