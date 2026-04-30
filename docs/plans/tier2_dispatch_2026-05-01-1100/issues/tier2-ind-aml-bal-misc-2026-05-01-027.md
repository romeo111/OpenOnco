# [Chunk] tier2-ind-aml-bal-misc-2026-05-01-027

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Tier-2 indication coverage` from Tier-1 indications landed via PR #166; Tier-2 drugs+regimens require indication wiring toward ~50 new indications routing W7 biomarkers + W8 drugs + W9 regimens for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W10 -- AML / B-ALL / SCLC / GIST indications (~8)`. Sequencing: starts after relevant W7+W8+W9 chunks merge; each indication >=2 source citations (Q4 axis).

## Manifest IDs (this chunk's allowlist)

- IND-AML-RR-IDH1-OLUTASIDENIB (Study 2102-HEM-101)
- IND-BALL-ADULT-RR-BLINATUMOMAB (TOWER)
- IND-BALL-ADULT-RR-INOTUZUMAB (INO-VATE ALL)
- IND-BALL-PED-CD19-TISACEL (existing -- verify)
- IND-SCLC-RR-LURBINECTEDIN (ATLANTIS)
- IND-GIST-4L-RIPRETINIB (INVICTUS)
- IND-MELANOMA-ADJ-1L-PEMBRO-EXISTING (KEYNOTE-054; verify; if not present add)
- IND-HNSCC-RM-1L-EXTREME-EXISTING (verify; if not present add)

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly outside the allowlist.
- KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK -- all entities valid".
- pytest fixture green: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed".
- Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` should only list paths in the allowlist below.
- Sources cited (no invented IDs); flag missing trial Sources in commit body.


## Reference YAML pattern

`git show origin/master:knowledge_base/hosted/content/indications/ind_aml_2l_idh2_enasidenib.yaml`

## Sources to cite

- Study 2102-HEM-101
- TOWER
- INO-VATE ALL
- ATLANTIS
- INVICTUS
- KEYNOTE-054

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/indications/indication_(aml|ball|sclc|gist|melanoma|hnscc)_*.yaml (subset)
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/tier2-ind-aml-bal-misc-2026-05-01-027 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): tier2-ind-aml-bal-misc-2026-05-01-027

<one-line scope description per roadmap section>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/tier2-ind-aml-bal-misc-2026-05-01-027
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
