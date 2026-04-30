# [Chunk] source-recency-refresh-wave2-2026-05-01-022

## Mission

This chunk advances `kb-coverage-matrix.md > Quality gaps > Q2 Source recency wave-2` from 270/271 sources have last_verified field; 219/271 have stale current_as_of (older than 2026-04-01) or are missing the field toward 131 oldest-priority sources refreshed (URL verified, current_as_of bumped, license/terms confirmed) for the manifest IDs below.

Tier-2 roadmap reference: `docs/plans/biomarker_expansion_tier2_roadmap_2026-05-01-1100.md > W12b -- Source recency refresh wave-2`. Pattern mirrors original `source-recency-refresh-*` chunks (issues #92-#121). Recency-stat reconciliation: see roadmap Appendix C.

## Chunk Spec

https://github.com/romeo111/OpenOnco/blob/master/docs/kb-coverage-strategy.md

## Chunk ID

`source-recency-refresh-wave2-2026-05-01-022`

## Branch Naming Convention

`tasktorrent/source-recency-refresh-wave2-2026-05-01-022`

## Sidecar Output Path

```
contributions/source-recency-refresh-wave2-2026-05-01-022/
```

## Claim Method

`formal-issue`

## Drop Estimate

0.5 day

## Task Manifest

```
SRC-FIGHT
SRC-VOYAGER
SRC-RESPONSE-VANNUCCHI-2015
SRC-MONARCH-2-SLEDGE-2017
SRC-IMC-HTLV-2017
```

## Manifest IDs (this chunk's allowlist)

- SRC-FIGHT
- SRC-VOYAGER
- SRC-RESPONSE-VANNUCCHI-2015
- SRC-MONARCH-2-SLEDGE-2017
- SRC-IMC-HTLV-2017

## Task

For each source in the manifest: (1) verify the publisher URL still resolves (or replace with DOI / PubMed canonical URL); (2) confirm clinical content has not been superseded -- if so, add `superseded_by: SRC-XXX`; (3) bump `current_as_of` to the chunk run date IF clinical content is current; (4) confirm license/terms field is populated. Output sidecar audit YAML per source.

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
- Include `source_recency_audit.yaml` with one entry per source: `id`, `url_verified` (yes/no/replaced-with), `content_current` (yes/no/superseded-by), `proposed_current_as_of`, `license_status`, `notes`.

## Quality Gate

- Each manifest ID has a source-backed outcome.
- Each unresolved item has a structured reason.
- No hosted KB file is edited directly.
- `py -3.12 -m scripts.tasktorrent.validate_contributions source-recency-refresh-wave2-2026-05-01-022` passes locally.
- `git diff --name-only origin/master..HEAD` shows no paths outside `contributions/source-recency-refresh-wave2-2026-05-01-022/`.
- No disallowed source IDs (`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`) appear.


## Reference pattern

`git show origin/master:contributions/source-recency-refresh-2026-04-29-001/`

## Branch + commit + push

```
git fetch origin
git checkout -b tasktorrent/source-recency-refresh-wave2-2026-05-01-022 origin/master
# author sidecar files only -- never edit hosted KB
git status --short
git add contributions/source-recency-refresh-wave2-2026-05-01-022/
git commit -m "$(cat <<'EOF'
chore(contributions): source-recency-refresh-wave2-2026-05-01-022

<one-line scope description>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin tasktorrent/source-recency-refresh-wave2-2026-05-01-022
```

Self-push authorized per CLAUDE.md commit `3a60901b`.

## Rejection Criteria

- Hosted KB files are edited directly instead of using sidecars.
- Any manifest ID is silently skipped.
- Clinical claims lack source IDs, PMID/DOI links where available, or an explicit unresolved reason.

## Never

`git add -A`, `--no-verify`, force-push, branch deletion.
