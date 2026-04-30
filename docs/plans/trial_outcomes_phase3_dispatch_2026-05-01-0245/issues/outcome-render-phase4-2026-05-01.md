# [Chunk] outcome-render-phase4-2026-05-01

## Mission

Phase 4 of the [trial-outcomes ingestion plan](../../pivotal_trial_outcomes_ingestion_plan_2026-04-30.md). Update the render layer to surface `OutcomeValue.source` as a citation reference next to each shown outcome value, and add a "Trial-readout traceability" badge to indication cards when ≥80% of populated outcomes are cited.

Independent of Phase 3 progress — works correctly for both `SRC-LEGACY-UNCITED` (renders muted "(citation pending)") and real `SRC-*` (renders linked citation).

## Scope

1. **Citation reference next to outcome value.** In whatever indication-card render module currently emits `expected_outcomes` (likely `knowledge_base/engine/render.py` or a sibling), look up `OutcomeValue.source` for each populated field and:
   - If `source == "SRC-LEGACY-UNCITED"`: render a muted `(citation pending)` badge next to the value.
   - Otherwise: render `[<source-id>]` as a clickable anchor that links to the source's render section (or the source's external URL if surfaced inline).
   - When `confidence_interval` is set, append it after the value in parens: `5.5 mo (95% CI 4.7–6.5)`.
   - When `median_followup_months` is set, suffix `· median f/u <X> mo`.

2. **Per-card traceability badge.** Compute per-indication `cited% = (# fields with source != SRC-LEGACY-UNCITED) / (# populated fields)`. Render a "Trial-readout traceability ≥80%" badge on the indication card when ≥80%. (Use the same rule as the audit's `cited` definition; ignore `probably-cited` fuzzy heuristic — render layer should be deterministic, audit-only is heuristic.)

3. **HCP-mode only.** Patient-mode rendering MUST NOT surface citation IDs or the badge — it stays clean per CHARTER §15.1 ("verify before use" surface). Verify with the existing patient-mode regex grep test pattern.

4. **Tests:**
   - Add `tests/test_outcome_citation_render.py` (or extend `tests/test_actionability_render.py` if appropriate).
   - Cover: cited value renders link, legacy renders pending tag, CI appears, badge appears at ≥80%, badge absent at <80%, patient-mode renders no citation IDs.

## Quality gates

1. KB validator clean.
2. `py -3.12 -m pytest tests/test_*render*.py -q` → all pass (no regressions in actionability render either).
3. `py -3.12 -m pytest tests/test_outcome_citation_render.py -q` → new tests pass.
4. Patient-mode regex grep: render an HCP+patient pair, grep patient-mode output for `SRC-` → 0 hits.
5. Self-push authorized per CLAUDE.md `3a60901b`.

## Allowlist (file pathspecs this chunk may touch)

```
knowledge_base/engine/render.py
knowledge_base/engine/render_styles.py
knowledge_base/engine/_render_*.py        ← if there's a sibling render module for outcomes
tests/test_outcome_citation_render.py     ← new test module
tests/test_actionability_render.py        ← only if extending; otherwise prefer new module
docs/plans/pivotal_trial_outcomes_ingestion_plan_2026-04-30.md  ← optional: tick Phase 4 done
```

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/outcome-render-phase4-2026-05-01-<HHMM> origin/master
# implement render + tests
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(render): surface OutcomeValue.source citation refs + traceability badge (Phase 4)

Renders citation IDs next to each outcome value (HCP-mode only); adds a
"Trial-readout traceability" badge when ≥80% of populated outcomes carry
non-legacy SRC-* IDs. Patient mode unchanged.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/outcome-render-phase4-2026-05-01-<HHMM>
```

## Stop conditions

- KB validator regresses.
- Existing actionability render tests regress.
- Patient-mode grep finds `SRC-` after change — STOP, fix, do not commit.
- Render touches engine routing logic (must be render-only per CHARTER §8.3).

## Never

`git add -A`, `--no-verify`, force-push, branch deletion, edits to engine/routing logic, edits to indication YAMLs.

## Sequencing note

Phase 4 can ship independently of Phase 3 — it gracefully renders both legacy and cited states. Suggested timing: dispatch in parallel with Phase-3 Wave A so the render is in place by the time real citations start landing.
