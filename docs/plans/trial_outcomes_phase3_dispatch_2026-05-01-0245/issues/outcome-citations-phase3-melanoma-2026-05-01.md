# [Chunk] outcome-citations-phase3-melanoma-2026-05-01

## Mission

Replace `SRC-LEGACY-UNCITED` placeholders in `expected_outcomes` for **Cutaneous melanoma** (DIS-MELANOMA) indications with real pivotal-trial citations. This is one of the Phase-3 chunks of the [trial-outcomes ingestion plan](../../pivotal_trial_outcomes_ingestion_plan_2026-04-30.md). Phase 2 schema (`OutcomeValue`) is already merged via [PR #177](https://github.com/romeo111/OpenOnco/pull/177).

This chunk owns **10** indications (chunk 1 of 1 for this disease).

## Per-item workflow (per the plan §"Per-item workflow")

For each indication in the manifest below, for each `uncited` outcome field:

1. Identify the pivotal trial referenced by the indication's `notes` / `algorithm` step / `applicable_to` block. If unclear, escalate via `actionability_review_required: true` in the YAML and skip — do NOT guess.
2. Fetch the trial's pivotal publication via PubMed (use `mcp__plugin_bio-research_pubmed__lookup_article_by_citation` or `mcp__plugin_bio-research_pubmed__search_articles`, or fall back to `knowledge_base/clients/pubmed_client.py`).
3. Read the abstract + Results section. If the abstract is sparse, also fetch the NCT primary-results posting.
4. **Transcribe** (don't synthesize) ORR / CR / mPFS / mOS / OS-5y / DFS-HR exactly as the publication states them, with units. If a value is reported with median follow-up X mo, capture both via `OutcomeValue.median_followup_months`. Capture the 95% CI in `OutcomeValue.confidence_interval` when stated.
5. Create or reuse a `SRC-*` entity for the publication at `knowledge_base/hosted/content/sources/src_<trial>_<firstauthor>_<year>.yaml`. Citation must include PMID, DOI, journal, year, first-author surname. Follow existing `src_*.yaml` conventions.
6. Set each remediated `OutcomeValue.source` to the new `SRC-*` ID (drop the `SRC-LEGACY-UNCITED` placeholder).
7. Add a 1-line `notes` on the OutcomeValue if the value differs from frequently-quoted numbers.

## Forbidden (per the plan)

- Synthesizing or interpolating values not stated in the primary source.
- Picking which arm's outcomes apply when the indication's `applicable_to` block doesn't unambiguously map to a single trial arm — flag instead.
- Filling missing CIs from "typical" ranges.
- Translating outcome strings — keep them in the trial's English. UA goes elsewhere.
- Editing any KB file outside the allowlist.

## Manifest IDs (this chunk's allowlist)

- IND-MELANOMA-2L-KIT-IMATINIB (uncited: complete_response, overall_response_rate, overall_survival_5y, progression_free_survival) — `knowledge_base/hosted/content/indications/ind_melanoma_2l_kit_imatinib.yaml`
- IND-MELANOMA-2L-POST-BRAFI-IPI-NIVO (uncited: complete_response, overall_response_rate, overall_survival_5y, progression_free_survival) — `knowledge_base/hosted/content/indications/ind_melanoma_2l_post_brafi_ipi_nivo.yaml`
- IND-MELANOMA-2L-POST-IO-BRAFI-MEKI (uncited: complete_response, overall_response_rate, overall_survival_5y, progression_free_survival) — `knowledge_base/hosted/content/indications/ind_melanoma_2l_post_io_brafi_meki.yaml`
- IND-MELANOMA-2L-RELATLIMAB-NIVOLUMAB (uncited: complete_response, overall_response_rate, overall_survival_5y, progression_free_survival) — `knowledge_base/hosted/content/indications/ind_melanoma_2l_relatlimab_nivolumab.yaml`
- IND-MELANOMA-3L-LIFILEUCEL (uncited: complete_response, overall_response_rate, overall_survival_5y, progression_free_survival) — `knowledge_base/hosted/content/indications/ind_melanoma_3l_lifileucel.yaml`
- IND-MELANOMA-3L-POST-LIFILEUCEL (uncited: complete_response, overall_response_rate, overall_survival_5y, progression_free_survival) — `knowledge_base/hosted/content/indications/ind_melanoma_3l_post_lifileucel.yaml`
- IND-MELANOMA-ADJUVANT-PEMBRO-STAGE-III (uncited: overall_response_rate, overall_survival_5y, progression_free_survival) — `knowledge_base/hosted/content/indications/ind_melanoma_adjuvant_pembro_stage_iii.yaml`
- IND-MELANOMA-METASTATIC-1L-NIVO-IPI (uncited: five_year_overall_survival) — `knowledge_base/hosted/content/indications/ind_melanoma_metastatic_1l_nivo_ipi.yaml`
- IND-MELANOMA-METASTATIC-1L-PEMBRO-MONO (uncited: complete_response, overall_response_rate, overall_survival_5y, progression_free_survival) — `knowledge_base/hosted/content/indications/ind_melanoma_metastatic_1l_pembro_mono.yaml`
- IND-MELANOMA-NIVO-MAINT (uncited: complete_response, overall_response_rate, overall_survival_5y, progression_free_survival) — `knowledge_base/hosted/content/indications/ind_melanoma_nivo_maint.yaml`

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/hosted/content/indications/ind_melanoma_2l_kit_imatinib.yaml
knowledge_base/hosted/content/indications/ind_melanoma_2l_post_brafi_ipi_nivo.yaml
knowledge_base/hosted/content/indications/ind_melanoma_2l_post_io_brafi_meki.yaml
knowledge_base/hosted/content/indications/ind_melanoma_2l_relatlimab_nivolumab.yaml
knowledge_base/hosted/content/indications/ind_melanoma_3l_lifileucel.yaml
knowledge_base/hosted/content/indications/ind_melanoma_3l_post_lifileucel.yaml
knowledge_base/hosted/content/indications/ind_melanoma_adjuvant_pembro_stage_iii.yaml
knowledge_base/hosted/content/indications/ind_melanoma_metastatic_1l_nivo_ipi.yaml
knowledge_base/hosted/content/indications/ind_melanoma_metastatic_1l_pembro_mono.yaml
knowledge_base/hosted/content/indications/ind_melanoma_nivo_maint.yaml
knowledge_base/hosted/content/sources/src_<trial>_<firstauthor>_<year>.yaml   ← new sources you author for this chunk
```

## Quality gates

1. KB validator clean: `PYTHONIOENCODING=utf-8 C:/Python312/python.exe -m knowledge_base.validation.loader knowledge_base/hosted/content` → `OK — all entities valid`.
2. Audit re-run: `py -3.12 scripts/audit_expected_outcomes.py` → confirm this chunk's indications moved out of the `uncited` bucket and into `cited`.
3. Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` may only list paths in the allowlist + new `src_*.yaml` files.
4. Sources cited (no invented IDs / fabricated PMIDs).
5. Self-push authorized per CLAUDE.md `3a60901b` when all gates pass.

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/outcome-citations-phase3-melanoma-2026-05-01 origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): outcome-citations-phase3-melanoma-2026-05-01

Replace SRC-LEGACY-UNCITED in expected_outcomes for 10 Cutaneous melanoma indications; add N new SRC-* trial citations.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/outcome-citations-phase3-melanoma-2026-05-01
```

## Stop conditions

- KB validator regresses.
- Edits land outside the allowlist.
- Indication's pivotal trial is not identifiable from the YAML — flag with `actionability_review_required: true` + 1-line note, do NOT guess.
- Trial publication paywalled and not on PubMed — Tier-2 fallback per plan: cite NCT primary-results posting + FDA label.
- PMID mismatch from typo in audit/source — cross-check first PubMed hit; if unsure, escalate.
- Two chunks editing the same `src_*.yaml` — coordination bug, escalate to orchestrator.

## Never

`git add -A`, `--no-verify`, force-push, branch deletion, edits to existing YAML beyond the allowlist, fabricating outcome values not stated in primary source.
