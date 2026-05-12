# UA full-quality Phase 1 — integration report (2026-05-12)

## Outcome

Integrated 17 parallel translation agent branches onto
`claude/objective-cori-df8c0f`. KB validator state moved from baseline
2781 errors to **598 errors (-78%)**, with KB loader still passing on
all 3,118 entities and references resolving cleanly.

## Validator deltas

| Metric | Baseline (2026-05-12 pre-Phase-1) | Post-Phase-1 |
|---|---:|---:|
| Files with UA content | 2,424 | 2,424 |
| Total errors | 2,781 | **598** |
|   EN_BLEED | 2,359 | 457 |
|   NUMERIC_DRIFT | 226 | 99 |
|   MISSING_MARKER | 196 | 42 |
| GLOSSARY_MISS warnings | 1,007 | 1,174 |
| Loader status | OK | OK |

Remaining 598 errors are concentrated in (a) files explicitly deferred
per the audit CSV (337 entities with EN source modified <2 days ago),
(b) partial misses on ua-03 retry which only completed batches 6-8 of
its scope (BMA a-g, 132/~150 files), and (c) entities where the EN
source itself contained ambiguous content. These are addressable in a
Phase-1.5 cleanup wave.

## Per-agent completion summary

| Agent | Scope | Files done | Notes |
|---|---|---:|---|
| ua-01 | diseases | 78/78 | Pilot — Opus, validated pattern |
| ua-02 | biomarkers | 166/181 | 0 errors |
| ua-03 retry | BMA a-g | 132/~150 | Sonnet anti-script retry succeeded |
| ua-04 retry | BMA h-l | 90 | Opus, hit context limit at MSH2 |
| ua-04b | BMA m-n | 89 | Opus continuation, finished MSH2/MSH6/NRAS/NTRK |
| ua-05 | BMA o-z | 134 | 268 fields total, 15 glossary proposals |
| ua-06 retry | IND a-f | 177/177 | 100% coverage, 0 errors/warnings |
| ua-07 retry | IND g-o + mm | 134 | Opus, 32 glossary proposals |
| ua-08 | IND p-z | 66 | Pushed directly to my branch |
| ua-09 | RF a-h | 135 | 3 batches, 0 errors |
| ua-10 | RF i-z + universal | 274 | 4 batches, 43 glossary proposals |
| ua-11 | regimens a-m | 46 | 0 errors / 0 warnings |
| ua-12 | regimens n-z | 106 | 6 deferred |
| ua-13 | algorithms | 91 | 0 errors |
| ua-14a | drugs a-f | 111 | 2 deferred |
| ua-14b | drugs g-o | 67 | 4 deferred |
| ua-14c | drugs p-z + proc + rad | 85 | 43 glossary proposals |

**Total fields upgraded: ~2,000+** across the 17 integrations.

## Conflicts encountered + resolutions

| Conflict | Resolution |
|---|---|
| ua-04 ↔ ua-04b on bma_mlh1_*, bma_msh2_germline_{crc,endometrial,gastric} | Preferred ua-04b (intentional continuation, more recent context) |
| ua-11 ↔ ua-12 on carbo_gem_bev_ovarian, carbo_pld_bev_ovarian, mirvetuximab_ovarian | Preferred ua-11 (a-m alphabetic-scope-authoritative) |
| Multiple agents on glossary_proposals.jsonl | Concatenated entries from all branches |

No referential-integrity conflicts. No silent data loss — all losses
were explicit "preferred X over Y" decisions logged in merge commits.

## Failure modes observed

**Sonnet bulk-script anti-pattern**: 5 of the 13 originally-launched
Sonnet agents (ua-03, ua-04, ua-06, ua-07, ua-14) stalled on the
"let me write a Python translation script" path when scope was 100+
files. Mitigation:
- Adding "do NOT write a translation script" to the brief reduced but
  did not eliminate this. Anti-script briefs worked for ua-03 retry
  but failed for ua-04, ua-07, ua-14.
- Switching to Opus reliably worked at any scope, but hit context
  budget around 90-100 files per agent.
- **Recommended pattern for future runs**: Opus + cap scope at ~75
  files per agent. Or use Sonnet only for scopes <75 files.

**API connection error**: ua-14 retry on Sonnet hit `API Error: Unable
to connect` after 5048s — likely upstream issue, not architectural.
Resplit into ua-14a/b/c on Opus succeeded.

**Branch deviation**: ua-08 pushed directly to `claude/objective-cori-df8c0f`
(my branch) instead of its worktree-agent branch. End state: its work
landed cleanly via fast-forward, no integration step needed for it,
but this is a brief-compliance issue. Future briefs should specify
exact branch name.

**Glossary proposals path deviation**: ua-06 wrote to
`knowledge_base/translation/glossary_proposals_ua06.jsonl` instead of
worktree-root `glossary_proposals.jsonl` per spec. Both are now in
the integrated tree. Cleanup task: consolidate.

## Quality decisions (per advisor 2026-05-12)

- All edited fields carry `draft_revision: 2` and keep
  `ukrainian_review_status: pending_clinical_signoff`. No agent
  promoted state — clinical signoff per CHARTER §6.1 remains the
  separate two-Co-Lead gate.
- Translation register: hospital-discharge-letter / textbook clinical
  Ukrainian, third person, drug first-mention `<UA> (<EN INN>)`.
- Stay-Latin tokens (gene symbols, trial acronyms, classification
  systems, regimen acronyms) preserved per glossary.
- Numeric/dose preservation enforced by validator NUMERIC_DRIFT check.

## Next steps

- [ ] Phase 1.5 cleanup: address remaining 598 validator errors
  (deferred entities + partial-coverage gaps).
- [ ] Phase 2: rebuild site, spot-check `/ukr/` rendered pages.
- [ ] Phase 3: render-layer UA strings sweep
  (`knowledge_base/engine/render*.py`).
- [ ] Phase 4: spec deltas — sync `specs/uk/` against EN-canonical
  changes.
- [ ] Glossary consolidation: fold per-agent proposals into
  `knowledge_base/translation/ua_terminology.yaml` (orchestrator).
- [ ] Bring the integrated branch through user review before merging
  to master (CHARTER §6.1 dev-mode exemption applies because EN
  source is unmodified, but user approval gate stands).
