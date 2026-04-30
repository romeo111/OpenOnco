# [Chunk] tier2-reg-gi-emerging-2026-05-01-018

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Tier-2 regimen coverage` from Tier-1 regimens landed; Tier-2 drugs (W8) require regimen wiring toward ~50 new regimens covering W8 drugs across line/disease combinations for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W9 -- GI emerging regimens (~5)`. Sequencing: starts after the relevant W8 drug chunk merges; verify drug IDs exist before authoring.

## Manifest IDs (this chunk's allowlist)

- regimen_futibatinib_cholangio_2l (FOENIX-CCA2)
- regimen_infigratinib_cholangio_2l (CBGJ398X2204) -- verify drug still marketed
- regimen_fruquintinib_crc_3l (FRESCO-2)
- regimen_erdafitinib_urothelial_2l (THOR)
- regimen_olutasidenib_aml_rr_idh1 (Study 2102-HEM-101)

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly outside the allowlist.
- KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK -- all entities valid".
- pytest fixture green: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed".
- Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` should only list paths in the allowlist below.
- Sources cited (no invented IDs); flag missing trial Sources in commit body.


## Reference YAML pattern

`git show origin/master:knowledge_base/hosted/content/regimens/regimen_pemigatinib_cholangio.yaml`

## Sources to cite

- FOENIX-CCA2
- FRESCO-2
- THOR
- Study 2102-HEM-101

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/regimens/regimen_*cholangio*.yaml + regimen_fruquintinib_*.yaml + regimen_erdafitinib_*.yaml + regimen_olutasidenib_*.yaml
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/tier2-reg-gi-emerging-2026-05-01-018 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): tier2-reg-gi-emerging-2026-05-01-018

<one-line scope description per roadmap section>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/tier2-reg-gi-emerging-2026-05-01-018
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
