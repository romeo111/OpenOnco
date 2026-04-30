# [Chunk] tier2-bio-emerging-targeted-2026-05-01-004

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Tier-2 biomarker coverage` from current biomarker count 125 toward full second-wave coverage (28 new biomarkers across W7a-W7f) for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W7d -- Emerging targeted (6 bio)`.

## Manifest IDs (this chunk's allowlist)

- bio_nrg1_fusion (zenocutuzumab pan-tumor, FDA Dec 2024)
- bio_braf_class_ii_iii (non-V600; distinct drug strategy)
- bio_her2_ultralow (DESTINY-Breast06; distinct from bio_her2_low)
- bio_esr1_y537s_d538g (extension to bio_esr1; elacestrant hot-spots)
- bio_akt1_e17k (extension to bio_akt1; capivasertib hot-spot)
- bio_cdkn2a_loss (extension to bio_cdkn2a; co-deletion vs LOH)

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly outside the allowlist.
- KB validator clean: `python -m knowledge_base.validation.loader knowledge_base/hosted/content` returns "OK -- all entities valid".
- pytest fixture green: `pytest tests/test_curated_chunk_e2e.py -q` returns "62 passed".
- Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` should only list paths in the allowlist below.
- Sources cited (no invented IDs); flag missing trial Sources in commit body.


## Reference YAML pattern

`git show origin/master:knowledge_base/hosted/content/biomarkers/bio_braf_v600e.yaml`

## Sources to cite

- eNRGy (zenocutuzumab NRG1)
- DESTINY-Breast06 (HER2-ultralow)
- EMERALD (elacestrant ESR1)
- CAPItello-291 (capivasertib AKT1/PIK3CA/PTEN)
- INAVO120 (inavolisib PIK3CA)

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/biomarkers/bio_nrg1_fusion.yaml
knowledge_base/hosted/content/biomarkers/bio_braf_class_ii_iii.yaml
knowledge_base/hosted/content/biomarkers/bio_her2_ultralow.yaml
knowledge_base/hosted/content/biomarkers/bio_esr1_y537s_d538g.yaml
knowledge_base/hosted/content/biomarkers/bio_akt1_e17k.yaml
knowledge_base/hosted/content/biomarkers/bio_cdkn2a_loss.yaml
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/tier2-bio-emerging-targeted-2026-05-01-004 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): tier2-bio-emerging-targeted-2026-05-01-004

<one-line scope description per roadmap section>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/tier2-bio-emerging-targeted-2026-05-01-004
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
