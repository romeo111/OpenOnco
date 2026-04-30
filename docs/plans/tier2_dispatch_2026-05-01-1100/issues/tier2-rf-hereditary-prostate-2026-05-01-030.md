# [Chunk] tier2-rf-hereditary-prostate-2026-05-01-030

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Tier-2 RedFlag coverage` from Tier-1 RFs landed; Tier-2 biomarkers require RF gating toward ~25 new RFs gating W10 indications for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W11 -- Hereditary + prostate RFs (~6)`. Each RF uses structured `findings` keys (no free-text condition strings -- drift signal #4 already documented).

## Manifest IDs (this chunk's allowlist)

- RF-PAN-BRCA-SOMATIC-PARPI-CANDIDATE
- RF-PAN-PALB2-PARPI-CANDIDATE
- RF-PAN-ATM-CHEK2-CDK12-PARPI-CANDIDATE (composite)
- RF-BREAST-CDH1-LOBULAR-CANDIDATE (informational; lobular subtype)
- RF-PROSTATE-AR-AMP-ARSI-RESISTANCE
- RF-PROSTATE-TMPRSS2-ERG-PROGNOSTIC

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly outside the allowlist.
- KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK -- all entities valid".
- pytest fixture green: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed".
- Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` should only list paths in the allowlist below.
- Sources cited (no invented IDs); flag missing trial Sources in commit body.


## Reference YAML pattern

`git show origin/master:knowledge_base/hosted/content/redflags/rf_prostate_ar_v7_arsi_resistance.yaml`

## Sources to cite

- PROfound
- EMBRACA
- OlympiAD
- NCCN hereditary cancer panel

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/redflags/rf_(pan|breast|prostate)_*.yaml (subset)
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/tier2-rf-hereditary-prostate-2026-05-01-030 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): tier2-rf-hereditary-prostate-2026-05-01-030

<one-line scope description per roadmap section>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/tier2-rf-hereditary-prostate-2026-05-01-030
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
