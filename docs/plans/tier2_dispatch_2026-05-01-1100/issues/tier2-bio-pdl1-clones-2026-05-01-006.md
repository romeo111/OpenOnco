# [Chunk] tier2-bio-pdl1-clones-2026-05-01-006

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Tier-2 biomarker coverage` from current biomarker count 125 toward full second-wave coverage (28 new biomarkers across W7a-W7f) for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W7f -- PD-L1 IHC clones (4 bio)`.

## Manifest IDs (this chunk's allowlist)

- bio_pdl1_22c3_clone (Dako 22C3 -- pembrolizumab indications)
- bio_pdl1_sp142_clone (Ventana SP142 -- atezolizumab TNBC, urothelial)
- bio_pdl1_sp263_clone (Ventana SP263 -- durvalumab)
- bio_pdl1_28_8_clone (Dako 28-8 -- nivolumab)

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly outside the allowlist.
- KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK -- all entities valid".
- pytest fixture green: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed".
- Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` should only list paths in the allowlist below.
- Sources cited (no invented IDs); flag missing trial Sources in commit body.


## Reference YAML pattern

`git show origin/master:knowledge_base/hosted/content/biomarkers/bio_pdl1_cps.yaml`

## Sources to cite

- KEYNOTE-024/189/407 (22C3)
- IMpower150/IMpassion130 (SP142)
- PACIFIC/CASPIAN (SP263)
- CheckMate-067/214 (28-8)
- Blueprint PD-L1 Assay Comparison Project (J Thorac Oncol 2017/2018)

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/biomarkers/bio_pdl1_22c3_clone.yaml
knowledge_base/hosted/content/biomarkers/bio_pdl1_sp142_clone.yaml
knowledge_base/hosted/content/biomarkers/bio_pdl1_sp263_clone.yaml
knowledge_base/hosted/content/biomarkers/bio_pdl1_28_8_clone.yaml
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/tier2-bio-pdl1-clones-2026-05-01-006 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): tier2-bio-pdl1-clones-2026-05-01-006

<one-line scope description per roadmap section>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/tier2-bio-pdl1-clones-2026-05-01-006
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
