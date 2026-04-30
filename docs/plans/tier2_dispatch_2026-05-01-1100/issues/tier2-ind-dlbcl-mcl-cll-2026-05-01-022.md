# [Chunk] tier2-ind-dlbcl-mcl-cll-2026-05-01-022

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Tier-2 indication coverage` from Tier-1 indications landed via PR #166; Tier-2 drugs+regimens require indication wiring toward ~50 new indications routing W7 biomarkers + W8 drugs + W9 regimens for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W10 -- DLBCL/MCL/CLL indications (~8)`. Sequencing: starts after relevant W7+W8+W9 chunks merge; each indication >=2 source citations (Q4 axis).

## Manifest IDs (this chunk's allowlist)

- IND-DLBCL-3L-EPCORITAMAB
- IND-DLBCL-3L-GLOFITAMAB
- IND-DLBCL-3L-LISOCEL
- IND-DLBCL-2L-LISOCEL (TRANSFORM)
- IND-MCL-3L-LISOCEL
- IND-MCL-3L-PIRTOBRUTINIB-EXISTING (verify if present, else add)
- IND-CLL-3L-LISOCEL (TRANSCEND-CLL-004)
- IND-FL-3L-MOSUNETUZUMAB (verify existing; if so, drop and document)

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly outside the allowlist.
- KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK -- all entities valid".
- pytest fixture green: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed".
- Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` should only list paths in the allowlist below.
- Sources cited (no invented IDs); flag missing trial Sources in commit body.


## Reference YAML pattern

`git show origin/master:knowledge_base/hosted/content/indications/ind_dlbcl_3l_axicel_cart.yaml`

## Sources to cite

- EPCORE NHL-1
- NP30179
- TRANSCEND-NHL-001
- TRANSFORM
- TRANSCEND-CLL-004

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/indications/indication_(dlbcl|mcl|cll|fl)_*.yaml (subset)
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/tier2-ind-dlbcl-mcl-cll-2026-05-01-022 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): tier2-ind-dlbcl-mcl-cll-2026-05-01-022

<one-line scope description per roadmap section>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/tier2-ind-dlbcl-mcl-cll-2026-05-01-022
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
