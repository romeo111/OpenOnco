# Scheduled KB audit — weekly biomarker + integrity check

**Дата:** 2026-04-26.
**Статус:** product + engineering plan, draft.
**Зв'язки:** CHARTER §6.1 (two-reviewer rule for clinical content),
CHARTER §9.3 (no patient data in artifacts), CHARTER §10.2 (immutable
audit), `scripts/audit_biomarkers.py` (existing v1 audit), `docs/
BIOMARKER_CATALOG.md` (output of audit).

---

## 0. Project principle (першочергове)

> Scheduled-агент дивиться на KB регулярно, **не змінює клінічний
> контент автоматично**, і повідомляє людину коли щось ламається або
> деградує. Він — sentinel, не decision-maker.

Three architectural invariants:

1. **No clinical-content auto-edits.** Cron-агент не редагує жодного
   YAML під `knowledge_base/hosted/content/{biomarkers,indications,
   algorithms,redflags,regimens,drugs}/`. Це clinical content; CHARTER
   §6.1 потребує two-reviewer signoff. Будь-яка пропозиція виходить як
   issue або draft PR з `clinical-review-required` label, ніколи не
   auto-merged.
2. **Auditability over speed.** Кожен run пише immutable log entry в
   `docs/audit_log/<YYYY-MM-DD>.md`. Якщо щось пішло не так, можна
   reconstruct що cron-агент бачив і вирішив — рік потому.
3. **Idempotent + bounded.** Same delta detected 4 тижні поспіль не
   породжує 4 дублі issue/PR. Cron має upper-bound на кількість issues
   per run — explosion-protection (e.g., якщо validator зламається і
   видасть 1000 ref errors, агент відкриває **один** мета-issue, не 1000).

---

## 1. Що працює сьогодні (acceptance baseline)

| Component | Стан | Файл |
|---|---|---|
| Біомаркер-audit script (cmdline) | ✅ | `scripts/audit_biomarkers.py` |
| KB validator (entity refs, schemas) | ✅ | `knowledge_base/validation/loader.py` |
| Catalog markdown generation | ✅ | `docs/BIOMARKER_CATALOG.md` |
| Cron infra (CronCreate API) | ✅ available | Claude Code agent feature |
| Manual catalog freshness | ⚠ user-triggered only | — |
| Delta detection (week-to-week) | ❌ | — |
| Issue/PR auto-creation з cron | ❌ | — |
| Audit log archive | ❌ | — |
| Stale-cron health check | ❌ | — |

**Gaps:**

1. **Drift invisibility.** Catalog regenerates тільки коли user запускає
   skript вручну. Між sessions може дрейфнути (parallel agent комітить
   нову Indication що тригерить нову dormant entity).
2. **No integrity-regression alarm.** Якщо validator несподівано виявляє
   broken ref після merge — ніхто не знає до наступної manual session.
3. **No coverage-trend tracking.** "У нас 57 LOINC missing" — ОК, але чи
   стає краще чи гірше з часом? Без log time-series це невидимо.
4. **No regression of `last_reviewed` ages.** Entity з `last_reviewed:
   "2024-12-01"` старіша 12+ міс — нікому не повідомлено.

---

## 2. Архітектура — що saved cron робить

### 2.1. Components

```
┌──────────────────────────────────────────────────┐
│ CronCreate(schedule="0 9 * * MON",               │
│            agent_type="kb-audit-sentinel",       │
│            permissions=AUDIT_PERMS)              │
└──────────────────────────────────────────────────┘
                        │
                        ▼ Mon 09:00
┌──────────────────────────────────────────────────┐
│ scripts/run_scheduled_audit.py                    │
│                                                   │
│  1. pre-flight: clean git, on master, up-to-date  │
│  2. run audit_biomarkers.py → audit.json          │
│  3. run validator → validator.json                │
│  4. run last_reviewed_audit → freshness.json      │
│  5. compute deltas vs last archived audit         │
│  6. classify each delta → action plan             │
│  7. enforce caps + idempotency                    │
│  8. emit audit log entry                          │
│  9. perform actions (commit / issue / PR / nop)   │
│ 10. release lock                                  │
└──────────────────────────────────────────────────┘
```

**Key principle:** the runner script is the brain; the Claude agent
just executes its action plan. The agent is NOT free to make decisions
beyond what `run_scheduled_audit.py` outputs.

### 2.2. New script: `scripts/run_scheduled_audit.py`

Pure Python; all decisions deterministic; no LLM calls. Emits one of:

```jsonc
// action_plan.json
{
  "run_id": "audit-2026-04-26-weekly",
  "started_at": "2026-04-26T09:00:00Z",
  "actions": [
    {
      "type": "commit_catalog_refresh",
      "files": ["docs/BIOMARKER_CATALOG.md", "docs/audit_log/2026-04-26.md"],
      "message": "chore(catalog): weekly KB audit — refs +1, dormant -1"
    },
    {
      "type": "open_issue",
      "title": "[kb-audit] BIO-NEW-MARKER referenced 3× without entity file",
      "labels": ["kb-audit", "clinical-review-required"],
      "body": "...",
      "dedupe_key": "missing-bio-NEW-MARKER"
    }
  ],
  "diagnostics": {
    "deltas_detected": 4,
    "actions_taken": 2,
    "actions_suppressed_by_idempotency": 2,
    "actions_capped": 0
  }
}
```

**The Claude agent's only job is to execute these actions** — write
files, run `git commit` + `git push`, run `gh issue create`. It does
not invent new actions. This is a strong safety property: any policy
change goes through `run_scheduled_audit.py` (a code review), not
through prompt drift.

### 2.3. Existing audit script extensions

`scripts/audit_biomarkers.py` already exists and is reused. Add two
companions:

- **`scripts/audit_validator.py`** (new) — wraps `load_content()` + emits
  `{"schema_errors": N, "ref_errors": [...], "errors_by_file": {...}}`
  as JSON. Today's logic exists in `loader.py` but only for
  imperative use; cron needs structured output.

- **`scripts/audit_freshness.py`** (new) — walks every entity's
  `last_reviewed` field, computes age, surfaces those past 12 months.
  Different SLA per entity type:
  - `Drug` / `Regimen`: 12 months (FDA-label changes, dosing updates)
  - `Indication` / `Algorithm`: 6 months (guideline updates)
  - `Source`: 18 months (publishers update on slower cycles)
  - `Biomarker`: 12 months
  - `RedFlag`: 12 months

### 2.4. Audit log archive

Each run writes `docs/audit_log/<YYYY-MM-DD>.md`:

```markdown
# KB audit — 2026-04-26 (weekly)

**Run id:** audit-2026-04-26-weekly
**Triggered by:** cron `0 9 * * MON`
**Duration:** 12.4s
**Outcome:** 1 commit, 1 issue opened, 0 PRs

## Snapshot
- Defined biomarkers: 62 → 62 (Δ 0)
- Referenced: 62 → 63 (Δ +1)
- Dormant: 0 → 0
- Broken refs: 0 → 1
- Missing LOINC: 57 → 56 (Δ -1, improvement)
- Entities past `last_reviewed` SLA: 14 → 18 (Δ +4)

## Actions
- [issue #42](url) — BIO-FOO-MARKER referenced but no entity file
- [commit a1b2c3d](url) — catalog refresh: 1 new ref, 1 LOINC added

## Suppressed
- 3 stale-freshness reflags (already open as issues #18, #19, #20)
```

These files commit as part of the run — append-only log of agent
decisions across all time.

---

## 3. Output channels — decision tree

What the runner does with each delta:

```
┌──────────────────────────────────────────────────┐
│            DELTA TYPE                             │
└──────────────────────────────────────────────────┘
       │
       ├─ Catalog refresh only (no semantic change)
       │   → COMMIT to master  ("chore(catalog): ...")
       │
       ├─ New entity reference appeared
       │   → COMMIT to master (catalog row + log)
       │
       ├─ New dormant biomarker
       │   → ISSUE only (clinical task)
       │     "label: kb-audit, clinical-review-required"
       │     dedupe by entity id
       │
       ├─ New broken ref (referenced but no entity)
       │   → ISSUE with high priority
       │     "label: kb-audit, blocker"
       │     dedupe by entity id
       │
       ├─ Schema error appeared (regression)
       │   → ISSUE with priority + notify reviewers
       │     "label: kb-audit, regression"
       │     dedupe by file:error-type
       │
       ├─ Coverage degraded (LOINC went DOWN)
       │   → ISSUE
       │     "label: kb-audit, regression"
       │
       ├─ last_reviewed past SLA
       │   → ISSUE per entity-type (one issue
       │     listing all stale entries; refresh
       │     existing issue if open)
       │     "label: kb-audit, freshness"
       │
       ├─ Coverage improved (LOINC went UP)
       │   → COMMIT log entry only (no issue spam)
       │
       └─ Nothing changed
           → NO-OP (but still write audit log entry
             so we know the cron ran)
```

**No auto-PRs that touch clinical content.** The catalog markdown is
the only artifact the cron writes. New biomarker entities, wired
references, schema fixes — все це через manual session з clinical
context.

**Exception (one allowed auto-PR class):** `chore(catalog)` commits
that touch ONLY `docs/BIOMARKER_CATALOG.md` and `docs/audit_log/*.md`.
These are doc-only, derivable from current KB state, low-risk.
CHARTER §6.1 doesn't gate doc-only changes.

---

## 4. Safety + permission model

### 4.1. Tool whitelist for the cron-agent

The agent invoked from `CronCreate` gets ONLY these tools:

```python
AUDIT_PERMS = [
    "Read",                # read KB + scripts
    "Bash(python scripts/run_scheduled_audit.py*)",   # the runner
    "Bash(git status*)",
    "Bash(git diff*)",
    "Bash(git add docs/BIOMARKER_CATALOG.md)",
    "Bash(git add docs/audit_log/*)",
    "Bash(git commit -m chore\\(catalog\\)*)",       # commits scoped
    "Bash(git push origin master)",
    "Bash(gh issue create*)",
    "Bash(gh issue list*)",                           # for dedupe
    "Bash(gh issue comment*)",                        # for refresh
]
```

Notably NOT in the list:

- ❌ `Edit` / `Write` — agent cannot author free-form files; only the
  runner script writes outputs.
- ❌ `git add knowledge_base/*` — agent cannot stage clinical content.
- ❌ `git commit -m feat(*)` / `fix(*)` / `content(*)` — only
  `chore(catalog)` commits allowed.
- ❌ `git push --force` — guard against history rewrite.
- ❌ `Agent` — no recursive sub-agents (prevents permission escalation).
- ❌ `WebFetch` / `WebSearch` — no external network calls outside
  `gh`-CLI to GitHub.

### 4.2. Pre-flight gates

`run_scheduled_audit.py` aborts (no actions taken) if any of:

1. `git status` not clean (uncommitted changes — manual session active).
2. Current branch is not `master`.
3. `git fetch && git status` shows `behind origin/master` (stale clone).
4. Stale cron lock file (`.claude/scheduled_tasks.lock` older than 1
   hour) → log warning, refuse to run.
5. Validator fails to even load (catastrophic — runner cannot run
   audit on broken KB; emit a single `regression` issue and abort).

Each abort path writes an audit log entry explaining why nothing happened.

### 4.3. Worktree isolation

Cron-agent runs in `.claude/worktrees/audit-cron/` (isolated git
worktree). Pros:

- No interference with active dev sessions on `master`.
- If agent crashes mid-run, the dev session in `master` is untouched.
- Lock contention impossible (separate worktree, separate index).

Cons:

- Pushing requires syncing `audit-cron` worktree → fetch +
  fast-forward to remote master → commit → push. Runner handles this
  ordering atomically.

### 4.4. Action caps (explosion protection)

```python
MAX_ISSUES_PER_RUN = 5
MAX_COMMITS_PER_RUN = 1   # only the catalog refresh
MAX_TOTAL_ACTIONS = 6
```

If a run wants to take more actions, it instead opens **one**
`meta-issue`:

```
Title: [kb-audit] Run 2026-04-26 found 47 deltas (capped)
Body: See docs/audit_log/2026-04-26.md for full list. Run was
      capped at MAX_ISSUES_PER_RUN=5 to prevent issue spam.
```

This catches the failure mode where validator suddenly finds 1000
broken refs (e.g., a YAML mass-rename happened mid-week and was
partially merged).

### 4.5. Kill switch

`docs/audit_log/CRON_DISABLED.md` (presence of file) → runner aborts
immediately with a "cron disabled by maintainer" log entry. Manual
override for emergencies.

---

## 5. Idempotency design

The hardest part. Without it, the cron opens N copies of the same
issue every week.

### 5.1. Dedupe keys

Every `open_issue` action carries a `dedupe_key`:

```python
def dedupe_key(action_type: str, payload: dict) -> str:
    if action_type == "missing_ref":
        return f"missing-bio-{payload['biomarker_id']}"
    if action_type == "dormant":
        return f"dormant-bio-{payload['biomarker_id']}"
    if action_type == "schema_error":
        return f"schema-{payload['file']}"
    if action_type == "freshness_breach":
        return f"freshness-{payload['entity_type']}"  # one issue per type, not per entity
    raise ValueError(f"unknown action type {action_type}")
```

`dedupe_key` becomes a stable label on the GitHub issue: `kb-audit-key:<key>`.

### 5.2. Dedupe protocol

Before opening an issue:

1. `gh issue list --label "kb-audit" --state open --json number,labels`
2. If any open issue has label `kb-audit-key:<key>` → suppress new
   creation; instead post a `gh issue comment` saying "still seen this
   week; <link to audit log>".
3. If no match → create issue with the dedupe label.

### 5.3. Auto-close

Once a delta is resolved (e.g., the dormant marker gets wired in a
manual session), next cron run detects "no longer dormant" → posts a
final comment "resolved as of audit run X" and closes the issue.

This requires the runner to track previous open issues and detect
which ones no longer match a current delta. Implementation: keep
a "last seen" timestamp per dedupe_key in `docs/audit_log/.state.json`
(committed; small file, ~100 entries max).

### 5.4. Catalog-refresh commit dedupe

If catalog content is byte-identical to current `docs/BIOMARKER_CATALOG.md`
in master, skip the commit (no empty commits).

---

## 6. Failure modes

### 6.1. Cron fires but `run_scheduled_audit.py` crashes

- Lock acquired; agent crashes; lock not released.
- **Detection:** stale lock check (§4.2 #4). Next cron run sees
  >1h-old lock → emits "stale lock" issue, then takes over.
- **Recovery:** runner clears stale lock as its first action when a
  new run starts.

### 6.2. `git push` fails (parallel commit landed)

- Runner re-fetches, rebases catalog commit on new HEAD, retries push
  up to 3 times.
- After 3 failures, abort run; emit `[kb-audit] push contention` issue.

### 6.3. `gh issue create` rate-limited

- GitHub API limit is 5000 req/hour for authenticated users; cron
  agent operates well below this.
- On rate-limit response, runner waits 60s and retries. Max 3 retries.
- After 3 failures, log to audit-log only (issue creation deferred
  to next run via dedupe_key).

### 6.4. Validator crashes catastrophically

- E.g., Pydantic upgrade incompatibility breaks `load_content()`.
- Runner catches the exception, emits `[kb-audit] validator broken`
  issue with the traceback, aborts cleanly.
- Subsequent runs continue to abort until validator is fixed.

### 6.5. Audit-log file conflicts

- Multiple cron runs in close succession (admin manually triggered).
- Filename collisions: `2026-04-26.md` exists.
- Runner appends a sequence: `2026-04-26.md`, `2026-04-26-2.md`, etc.
- Or: scheduled runs use weekly file `2026-W17.md`; manual runs use
  date+suffix.

### 6.6. KB renamed / restructured

- Someone moves `knowledge_base/hosted/content/biomarkers/` to
  `knowledge_base/content/biomarkers/`.
- Audit script falls back to "0 entities found" → looks like
  catastrophic regression → cap-protected.
- **Compromise:** runner sanity-checks that audit found >50% of
  baseline entity count; if not, abort with "structural change
  detected" issue rather than 50 individual missing-ref issues.

---

## 7. Observability

### 7.1. Audit log

`docs/audit_log/<YYYY-MM-DD>.md` per run (§2.4). Time-series
queryable via grep/git-log.

### 7.2. Trend metrics

Append a single CSV row per run to `docs/audit_log/.metrics.csv`:

```csv
date,run_type,duration_s,defined,referenced,dormant,missing,schema_err,ref_err,loinc_missing,freshness_breaches
2026-04-26,weekly,12.4,62,62,0,0,0,0,57,14
2026-05-03,weekly,11.8,63,63,0,0,0,0,56,15
```

Future: `scripts/audit_trends.py` plots these → catches slow drift
("LOINC was decreasing for 4 weeks straight").

### 7.3. Cron-alive heartbeat

Even no-op runs emit a `<YYYY-MM-DD>.md` log entry. If no log entries
appear for 14+ days → cron is dead; need manual investigation. A
separate **monthly meta-cron** (`0 8 1 * *`) checks the freshness of
the most recent audit log; opens issue if >14 days stale.

### 7.4. Run-attempt notifications

Runner posts a comment on a pinned `kb-audit-status` issue every run
(success or failure). Pinned issue is the at-a-glance "is this thing
working" surface.

---

## 8. Phasing

### Phase A — Manual run pipeline (~3 days)

1. `scripts/audit_validator.py` — JSON output of validator state.
2. `scripts/audit_freshness.py` — JSON output of stale `last_reviewed`.
3. `scripts/run_scheduled_audit.py` — orchestrates all three audits,
   emits action_plan.json, but does NOT execute actions yet.
4. Tests: `tests/test_run_scheduled_audit.py` — fixture KB with known
   deltas, assert action_plan matches expected.
5. CLI: `python scripts/run_scheduled_audit.py --dry-run --json` for
   manual reproducibility.

### Phase B — Audit log + trend metrics (~1 day)

1. Audit log markdown writer (`docs/audit_log/<date>.md`).
2. CSV row append (`.metrics.csv`).
3. State file (`docs/audit_log/.state.json`) for dedupe across runs.
4. Tests: action_plan → log markdown round-trip.

### Phase C — Action executors (~2 days)

1. `commit_catalog_refresh` executor — git ops; respects pre-flight
   gates.
2. `open_issue` / `comment_issue` executors — `gh`-CLI wrappers with
   dedupe.
3. `close_issue` executor (when delta resolved).
4. Action-cap enforcement; meta-issue emission when capped.
5. Tests: mock git + gh; assert action sequence matches plan.

### Phase D — Wire as Claude Code cron (~1 day)

1. `CronCreate` invocation with `0 9 * * MON` schedule.
2. Tool whitelist (`AUDIT_PERMS`) — restricted to action-executor surface.
3. Worktree isolation: cron runs in `.claude/worktrees/audit-cron/`.
4. Kill switch: `docs/audit_log/CRON_DISABLED.md` check.
5. First production run: monitor closely, manually triggered.
6. After 4 weeks of clean runs: declare GA.

### Phase E — Heartbeat + trend dashboard (~2 days, deferrable)

1. Monthly meta-cron checks audit-log freshness.
2. `scripts/audit_trends.py` plots `.metrics.csv` → simple HTML.
3. Pinned `kb-audit-status` issue auto-updated each run.

**Total estimate: ~9 days.** Phase A-D is the must-have (8 days);
Phase E is nice-to-have observability polish.

---

## 9. Acceptance criteria (overall)

Plan complete when:

1. **Dry-run reproducibility** — `python scripts/run_scheduled_audit.py
   --dry-run` on the same git SHA produces byte-identical action_plan.json
   across runs.
2. **Audit log integrity** — every cron-fire creates exactly one
   `docs/audit_log/<date>.md`; file is git-tracked.
3. **No clinical-content writes** — automated check: `git log --author
   "<cron-bot>" -- knowledge_base/hosted/content/` returns zero commits
   touching anything other than `docs/`.
4. **Idempotency** — running 2 cycles back-to-back with no KB changes
   produces no new issues, no duplicate issue comments, only an
   audit-log entry per run.
5. **Cap enforcement** — synthetic test: validator returns 100 fake
   ref errors → exactly one meta-issue created, not 100.
6. **Kill switch works** — touch `docs/audit_log/CRON_DISABLED.md` →
   next cron-fire writes log "disabled" entry, takes no actions.
7. **Stale-lock recovery** — manually corrupt
   `.claude/scheduled_tasks.lock` with a 2h-old timestamp → next
   run-fire opens stale-lock issue, then takes over cleanly.

---

## 10. Risks + chesni compromise-и

### Ризик: cron-агент відкриває занадто багато issues, заспамлює репо

Action caps (§4.4) — hard upper bound 6 actions per run. Meta-issue
collapses overflow.

### Ризик: dedupe key collisions or drift

Якщо `dedupe_key()` функція змінюється — old issues won't match new
keys, дублі. **Compromise:** keys versioned (`kb-audit-key-v1:<key>`);
on key-version bump, runner auto-closes v1 issues with comment "key
schema migrated; new tracking issue: #N".

### Ризик: agent permissions creep

Хтось додає `Edit` до AUDIT_PERMS "just for one fix" → cron починає
писати free-form YAML. **Compromise:** permission whitelist в
`scripts/run_scheduled_audit.py` як constant + unit test that asserts
the actual cron config matches the constant.

### Ризик: silent failure (cron not running)

Cron-fires але run script crashes ще до log write → no log entry → не
видно. **Compromise:** monthly meta-cron heartbeat (Phase E §7.3).
Phase A-D ship without it; meta-cron is independent insurance.

### Ризик: false-positive "dormant" або "missing"

Naming convention drift triggers false alarm. **Compromise:** runner
explicitly checks for the recently-fixed naming-mismatch class first;
if detected, emits ONE issue with all suspected typos, not N issues.

### Ризик: clinical reviewer fatigue

Кожного тижня issue → лікарі ігнорують. **Compromise:** issue body
includes "this issue has been open N weeks" counter; freshness label
escalates `freshness-week-1` → `freshness-week-4` → `freshness-stale`
to make staleness visible.

### Ризик: GitHub API outage during run

`gh issue create` fails. **Compromise:** runner saves the action_plan
to `docs/audit_log/.pending/<run-id>.json`; next run picks up
pending actions before doing fresh ones. Bounded queue (drop oldest
if >10 pending — outage of >10 weeks means bigger problems).

---

## 11. Open questions (для co-leads)

1. **Schedule timing.** Mon 09:00 UTC = 11:00 Kyiv. Reasonable for
   Ukrainian clinical co-leads to see issues at start-of-week. Or
   prefer Friday EOD so they review on Monday morning?
2. **Issue assignee.** Auto-assign to a clinical-review pool? Or
   leave unassigned and triage manually?
3. **Notification channel.** GitHub issues only, or also a webhook
   into clinical-team Slack / Telegram? (Latter requires an external
   integration outside the cron-agent's permission scope.)
4. **Freshness SLA values.** Are 12mo (Drug/Regimen/Biomarker/RF) and
   6mo (Indication/Algorithm) realistic for OpenOnco's update tempo?
5. **Catalog auto-commit hours.** Should `chore(catalog)` commits be
   gated to business-hours-Ukraine to avoid 3am pushes? Or low-traffic
   hours preferred?
6. **Multi-week regression detection.** Should runner detect "metric X
   has been worse for ≥3 consecutive runs" and escalate to a special
   `regression-trend` issue? Or trust eyes on `.metrics.csv`?

---

## 12. Recommended first PR

Phase A (manual pipeline, no cron) — ~3 днів роботи:

1. New `scripts/audit_validator.py` (JSON wrapper around `loader.py`).
2. New `scripts/audit_freshness.py` (last_reviewed SLA check).
3. New `scripts/run_scheduled_audit.py` — orchestrator + action_plan
   emitter, but `--dry-run` only (no actions taken).
4. New `tests/test_run_scheduled_audit.py` — fixture-KB-driven tests
   for delta classification + dedupe-key generation.
5. Update `docs/plans/scheduled_kb_audit_2026-04-26.md` (this file)
   with `[x]` checkboxes as phases complete.

After this lands and tests pass, Phase B (audit log) and C (executors)
parallel-safe; Phase D (cron-wire) blocks on clinical-co-lead signoff
of the SLA values + permission whitelist.

**Critical-path question** to pin down before writing any code:
**confirmation from clinical co-leads** that they'd actually triage
weekly issues from this thing. Without that signoff, the cron's
output goes nowhere — better to skip the build than to ship a noise
generator. Plan §11 question 1-3 captures this gate.

---

## 13. Out of scope (explicitly)

- **Auto-fix of clinical content.** Only docs/.
- **Scheduled ctgov / OncoKB / NCCN polling.** These are upstream
  ingestion; separate cron-design (different SLA, different failure
  modes). This plan covers KB-internal-state only.
- **Cron-driven KB content authoring.** No "auto-author missing
  biomarker entity" — clinical work, manual session.
- **Cross-repo aggregation.** Single-repo audit only.
- **Realtime triggers** (e.g., post-merge audit-on-push). Cron-only;
  if real-time gating is wanted, that's a CI hook, not a cron.
- **PDF / OCR / external NLP.** Audit consumes structured KB only.
