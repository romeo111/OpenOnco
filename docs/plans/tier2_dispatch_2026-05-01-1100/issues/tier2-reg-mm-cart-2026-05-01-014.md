# [Chunk] tier2-reg-mm-cart-2026-05-01-014

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Tier-2 regimen coverage` from Tier-1 regimens landed; Tier-2 drugs (W8) require regimen wiring toward ~50 new regimens covering W8 drugs across line/disease combinations for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W9 -- MM CAR-T regimens (~5)`. Sequencing: starts after the relevant W8 drug chunk merges; verify drug IDs exist before authoring.

## Manifest IDs (this chunk's allowlist)

- regimen_idecel_mm_3l (KarMMa)
- regimen_ciltacel_mm_3l (CARTITUDE-1)
- regimen_ciltacel_mm_2l (CARTITUDE-4)
- regimen_idecel_lymphodepletion_flu_cy
- regimen_ciltacel_lymphodepletion_flu_cy

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly outside the allowlist.
- KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK -- all entities valid".
- pytest fixture green: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed".
- Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` should only list paths in the allowlist below.
- Sources cited (no invented IDs); flag missing trial Sources in commit body.


## Reference YAML pattern

`git show origin/master:knowledge_base/hosted/content/regimens/reg_tisagenlecleucel_b_all.yaml`

## Sources to cite

- KarMMa
- CARTITUDE-1
- CARTITUDE-4
- FDA labels

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/regimens/regimen_*cel_mm*.yaml
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/tier2-reg-mm-cart-2026-05-01-014 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): tier2-reg-mm-cart-2026-05-01-014

<one-line scope description per roadmap section>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/tier2-reg-mm-cart-2026-05-01-014
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
