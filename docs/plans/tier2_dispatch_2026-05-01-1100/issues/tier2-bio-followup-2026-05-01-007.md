# [Chunk] tier2-bio-followup-2026-05-01-007

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Tier-2 biomarker coverage` from current biomarker count 125 toward full second-wave coverage (28 new biomarkers across W7a-W7f) for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W7 followup -- placeholder for any biomarkers split out during chunk authoring`. Optional / overflow chunk -- only opens if W7b authoring decides to split Lynch into 4 entities. Otherwise close as duplicate.

## Manifest IDs (this chunk's allowlist)

- (Reserved -- if W7b Lynch is split into 4 individual entities, additional bio_msi_lynch_*.yaml files land here)
- (Reserved for any W7 biomarker that requires separate authoring after schema review)

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly outside the allowlist.
- KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK -- all entities valid".
- pytest fixture green: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed".
- Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` should only list paths in the allowlist below.
- Sources cited (no invented IDs); flag missing trial Sources in commit body.


## Reference YAML pattern

`git show origin/master:knowledge_base/hosted/content/biomarkers/bio_brca_germline.yaml`

## Sources to cite

- NCCN Lynch Syndrome guidelines
- PubMed consensus on Lynch gene-specific cancer risk

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/biomarkers/bio_lynch_mlh1_germline.yaml
knowledge_base/hosted/content/biomarkers/bio_lynch_msh2_germline.yaml
knowledge_base/hosted/content/biomarkers/bio_lynch_msh6_germline.yaml
knowledge_base/hosted/content/biomarkers/bio_lynch_pms2_germline.yaml
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/tier2-bio-followup-2026-05-01-007 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): tier2-bio-followup-2026-05-01-007

<one-line scope description per roadmap section>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/tier2-bio-followup-2026-05-01-007
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
