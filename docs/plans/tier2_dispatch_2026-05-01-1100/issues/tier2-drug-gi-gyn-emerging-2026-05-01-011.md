# [Chunk] tier2-drug-gi-gyn-emerging-2026-05-01-011

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Tier-2 drug coverage` from current drug count 220 (13 of 35 Tier-2 drugs already present) toward 220 + 21 = 241 (W8 scope: 21 not-yet-in-KB drugs) for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W8d -- GI + GYN emerging (5 drugs)`.

## Manifest IDs (this chunk's allowlist)

- drug_futibatinib (FGFR2 TKI for cholangio; FOENIX-CCA2, FDA Sep 2022)
- drug_infigratinib (FGFR2 TKI for cholangio; CBGJ398X2204, FDA May 2021 -- verify still marketed)
- drug_magrolimab (CD47 mAb -- AML/MDS dev discontinued 2024; chunk may DROP and document)
- drug_tisotumab_vedotin (TF ADC; innovaTV 204, FDA Sep 2021 cervical)
- drug_olutasidenib (IDH1 R132 inhibitor; Study 2102-HEM-101, FDA Dec 2022 R/R AML)

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly outside the allowlist.
- KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK -- all entities valid".
- pytest fixture green: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed".
- Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` should only list paths in the allowlist below.
- Sources cited (no invented IDs); flag missing trial Sources in commit body.


## Reference YAML pattern

`git show origin/master:knowledge_base/hosted/content/drugs/pemigatinib.yaml`

## Sources to cite

- FDA labels for futibatinib (Lytgobi), tisotumab vedotin (Tivdak), olutasidenib (Rezlidhia)
- FOENIX-CCA2, innovaTV 204, Study 2102-HEM-101
- For magrolimab: Gilead announcement of MDS/AML program halt (Feb 2024) -- if dropped, document in commit body

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/drugs/futibatinib.yaml
knowledge_base/hosted/content/drugs/infigratinib.yaml
knowledge_base/hosted/content/drugs/magrolimab.yaml
knowledge_base/hosted/content/drugs/tisotumab_vedotin.yaml
knowledge_base/hosted/content/drugs/olutasidenib.yaml
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/tier2-drug-gi-gyn-emerging-2026-05-01-011 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): tier2-drug-gi-gyn-emerging-2026-05-01-011

<one-line scope description per roadmap section>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/tier2-drug-gi-gyn-emerging-2026-05-01-011
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
