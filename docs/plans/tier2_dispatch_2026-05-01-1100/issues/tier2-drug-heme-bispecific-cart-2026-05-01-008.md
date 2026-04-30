# [Chunk] tier2-drug-heme-bispecific-cart-2026-05-01-008

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Tier-2 drug coverage` from current drug count 220 (13 of 35 Tier-2 drugs already present) toward 220 + 21 = 241 (W8 scope: 21 not-yet-in-KB drugs) for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W8a -- Heme bispecifics + CAR-T (6 drugs)`.

## Manifest IDs (this chunk's allowlist)

- drug_elranatamab (BCMA bispecific; MagnetisMM-3, FDA Aug 2023)
- drug_talquetamab (GPRC5D bispecific; MonumenTAL-1, FDA Aug 2023)
- drug_idecabtagene_vicleucel (ide-cel BCMA CAR-T; KarMMa, FDA Mar 2021)
- drug_ciltacabtagene_autoleucel (cilta-cel BCMA CAR-T; CARTITUDE-1, FDA Feb 2022)
- drug_epcoritamab (CD3xCD20 bispecific; EPCORE NHL-1, FDA May 2023)
- drug_glofitamab (CD3xCD20 bispecific; NP30179, FDA Jun 2023)

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly outside the allowlist.
- KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK -- all entities valid".
- pytest fixture green: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed".
- Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` should only list paths in the allowlist below.
- Sources cited (no invented IDs); flag missing trial Sources in commit body.


## Reference YAML pattern

`git show origin/master:knowledge_base/hosted/content/drugs/teclistamab.yaml`

## Sources to cite

- FDA labels for each drug
- Pivotal trial sources (MagnetisMM-3, MonumenTAL-1, KarMMa, CARTITUDE-1, EPCORE NHL-1, NP30179)
- EMA SmPCs where applicable

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/drugs/elranatamab.yaml
knowledge_base/hosted/content/drugs/talquetamab.yaml
knowledge_base/hosted/content/drugs/idecabtagene_vicleucel.yaml
knowledge_base/hosted/content/drugs/ciltacabtagene_autoleucel.yaml
knowledge_base/hosted/content/drugs/epcoritamab.yaml
knowledge_base/hosted/content/drugs/glofitamab.yaml
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/tier2-drug-heme-bispecific-cart-2026-05-01-008 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): tier2-drug-heme-bispecific-cart-2026-05-01-008

<one-line scope description per roadmap section>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/tier2-drug-heme-bispecific-cart-2026-05-01-008
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
