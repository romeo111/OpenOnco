# [Chunk] tier2-rf-breast-nsclc-2026-05-01-029

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Tier-2 RedFlag coverage` from Tier-1 RFs landed; Tier-2 biomarkers require RF gating toward ~25 new RFs gating W10 indications for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W11 -- Breast/NSCLC RFs (~7)`. Each RF uses structured `findings` keys (no free-text condition strings -- drift signal #4 already documented).

## Manifest IDs (this chunk's allowlist)

- RF-BREAST-HER2-ULTRALOW-CANDIDATE (DESTINY-Breast06)
- RF-BREAST-ESR1-Y537S-D538G-CANDIDATE (EMERALD)
- RF-BREAST-AKT1-E17K-CAPIVASERTIB-CANDIDATE (CAPItello-291)
- RF-BREAST-PIK3CA-COALT-INAVOLISIB-CANDIDATE (INAVO120)
- RF-NSCLC-NRG1-FUSION-ZENO-CANDIDATE
- RF-NSCLC-HER3-HIGH-PATRITUMAB-CANDIDATE
- RF-NSCLC-TROP2-DATO-CANDIDATE

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly outside the allowlist.
- KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK -- all entities valid".
- pytest fixture green: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed".
- Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` should only list paths in the allowlist below.
- Sources cited (no invented IDs); flag missing trial Sources in commit body.


## Reference YAML pattern

`git show origin/master:knowledge_base/hosted/content/redflags/rf_breast_pik3ca_alpelisib_candidate.yaml`

## Sources to cite

- DESTINY-Breast06
- EMERALD
- CAPItello-291
- INAVO120
- eNRGy
- HERTHENA-Lung01
- TROPION-Lung01

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/redflags/rf_(breast|nsclc)_*.yaml (subset)
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/tier2-rf-breast-nsclc-2026-05-01-029 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): tier2-rf-breast-nsclc-2026-05-01-029

<one-line scope description per roadmap section>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/tier2-rf-breast-nsclc-2026-05-01-029
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
