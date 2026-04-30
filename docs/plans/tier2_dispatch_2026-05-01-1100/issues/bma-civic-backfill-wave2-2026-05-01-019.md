# [Chunk] bma-civic-backfill-wave2-2026-05-01-019

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Q1 BMA-CIViC backfill wave-2` from 295/399 BMAs (74%) toward 399/399 (100%) for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W12a -- BMA-CIViC backfill wave-2`. Pattern mirrors closed `bma-civic-backfill-2026-04-29-007` (issue #43).

## Chunk Spec

https://github.com/romeo111/OpenOnco/blob/master/docs/kb-coverage-strategy.md

## Chunk ID

`bma-civic-backfill-wave2-2026-05-01-019`

## Branch Naming Convention

`tasktorrent/bma-civic-backfill-wave2-2026-05-01-019`

## Sidecar Output Path

```
contributions/bma-civic-backfill-wave2-2026-05-01-019/
```

## Claim Method

`formal-issue`

## Drop Estimate

0.5 day

## Task Manifest

```
BMA-CHEK2-GERMLINE-BREAST
BMA-MET-AMP-RCC-PAPILLARY
BMA-MSH2-SOMATIC-CRC
BMA-NTRK-FUSION-GIST
BMA-RAD51C-SOMATIC-BREAST
```

## Manifest IDs (this chunk's allowlist)

- BMA-CHEK2-GERMLINE-BREAST
- BMA-MET-AMP-RCC-PAPILLARY
- BMA-MSH2-SOMATIC-CRC
- BMA-NTRK-FUSION-GIST
- BMA-RAD51C-SOMATIC-BREAST

## Task

Review each hosted BMA in the manifest for possible CIViC evidence linkage. Add sidecar updates that propose either an `evidence_sources[SRC-CIVIC]` entry (with CIViC evidence ID + PMID) or an explicit `no_civic_match_reason`. Do not invent treatment claims when CIViC has no suitable evidence item.

## Allowed Sources

- Hosted OpenOnco YAML files already present in this repository.
- Source records already present in `knowledge_base/hosted/content/sources/`.
- Public CC0/open-access metadata and publisher landing pages for IDs in the manifest.
- CIViC evidence pages and linked PubMed records where relevant.

## Disallowed Sources

- `SRC-ONCOKB`
- `SRC-SNOMED`
- `SRC-MEDDRA`
- Private, paywalled, or copied guideline text.

## Output Requirements

- All edits must be sidecar files under `contributions/<chunk-id>/` only.
- Include `_contribution_meta.yaml` with `chunk_id: <chunk-id>` and `claim_method: formal-issue`.
- Include `task_manifest.txt` containing exactly the manifest IDs above.
- Include a YAML report that records one outcome per manifest ID and cites all evidence used.
- Each proposed CIViC link is checked against disease context, biomarker alteration, therapy, and evidence direction.

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly.
- `py -3.12 -m scripts.tasktorrent.validate_contributions bma-civic-backfill-wave2-2026-05-01-019` passes locally.
- `git diff --name-only origin/master..HEAD` shows no paths outside `contributions/bma-civic-backfill-wave2-2026-05-01-019/`.
- No disallowed source IDs (`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`) appear.


## Reference pattern

`git show origin/master:contributions/bma-civic-backfill-2026-04-29-001/`

## Branch + commit + push

```
git fetch origin
git checkout -b tasktorrent/bma-civic-backfill-wave2-2026-05-01-019 origin/master
# author sidecar files only -- never edit hosted KB
git status --short
git add contributions/bma-civic-backfill-wave2-2026-05-01-019/
git commit -m "$(cat <<'EOF'
chore(contributions): bma-civic-backfill-wave2-2026-05-01-019

<one-line scope description>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin tasktorrent/bma-civic-backfill-wave2-2026-05-01-019
```

Self-push authorized per CLAUDE.md commit `3a60901b`.

## Rejection Criteria

- Hosted KB files are edited directly instead of using sidecars.
- Any manifest ID is silently skipped.
- Clinical claims lack source IDs, PMID/DOI links where available, or an explicit unresolved reason.

## Never

`git add -A`, `--no-verify`, force-push, branch deletion.
