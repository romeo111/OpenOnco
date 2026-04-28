# Cross-Repo task_torrent Sync Plan — координація змін з OpenOnco workstreams

**Дата:** 2026-04-28
**Статус:** план узгоджено, до coding не приступали
**Тригер:** "треба буде оновити спільні файли із task_torrent" — користувач підтвердив, що OpenOnco workstreams (`feat/regimen-phases-refactor`, `feat/citation-verifier`, `feat/one-prompt-onboarding`) потребують узгоджених змін у `romeo111/task_torrent` repo.

## 1. Прийняті рішення (з попередньої розмови)

| # | Питання | Відповідь |
|---|---|---|
| 1 | Доступ до task_torrent | **1b — Claude продукує patches/diffs; user застосовує PR-ами** (немає write-access) |
| 2 | Прочитати їх improvement plan? | ✅ Зроблено — див. §3 |
| 3 | Versioning handshake | **"Always latest, fail loud"** — без semver-pinning, без `tasktorrent_version` поля, без `.tasktorrent.yaml`. Validators читають raw `main`; mismatch → loud error, не silent accept. (Trade-off: multi-consumer-future простіший за #21, але solo-maintainer у v0.1 не платить ціну ceremonии.) |
| 4 | Single source of truth контракту | **Sync-rule:** у обох репо з automated drift-detection |

## 2. Recon — що в task_torrent (фактично прочитано)

### 2.1. Структура repo

```
romeo111/task_torrent/
├── chunks/openonco/         12 chunk specs + README.md (shelf index)
├── docs/                     11 docs, ключові:
│   ├── chunk-system.md       Schema definition
│   ├── safety-rules.md       Безпекові правила
│   ├── openonco-pilot-workflow.md
│   ├── protocol-v0.4-design.md (17KB) — protocol design
│   └── tasktorrent-improvement-plan.md (26KB) — LIVING DOC
├── skills/                   3 skill specs (biomarker-extraction, citation-verification, drug-evidence-mapping)
└── tasktorrent/
    ├── lint_chunk_spec.py    13.7 KB — primary contract enforcement
    └── config.py
```

### 2.2. `lint_chunk_spec.py` v0.4 — обов'язкові секції chunk-spec

```python
REQUIRED_SECTIONS = (
    "Status", "Topic Labels", "Mission", "Economic Profile",
    "Drop Estimate", "Required Skill", "Allowed Sources",
    "Manifest", "Output Format", "Acceptance Criteria",
    "Rejection Criteria", "Claim Method",
)
# Conditional:
#   MARGINAL chunks → expected_violations field
#   Volume-mutating chunks → volume_impact declaration
```

Ці 12 sections — **canonical contract**, не issue-body parsing. Наш `next_chunk.py` має парсити CHUNK SPEC, не issue body. Issue body — лише UI-summary з посиланням на spec.

### 2.3. Existing `tasktorrent-improvement-plan.md` — 21 numbered Proposals

Living document із 12 lessons (L-1..L-21) + 21 numbered Proposals по 3 Tiers. **Більшість того, що я б пропонував, уже там.** Особливо критично:

- **L-21 / Proposal #21**: cross-repo version pinning — точно те, що я мав запропонувати у Q3
- **L-19 / Proposal #19**: claim coordination hardening — уже implemented (recent OpenOnco PRs #25)
- **L-13 / Proposal #13**: citation-verify validator gate — overlaps з нашим citation-verifier
- **L-2/L-12 / Proposal #2/#12**: permissive validator — частково implemented (PRs #16-#20)
- **L-18 / Proposal #18**: volume-impact declaration — в чергі

## 3. Map: наші workstreams ↔ їхні existing Proposals

Жоден з наших OpenOnco workstreams не вимагає **нових** TaskTorrent proposals. Ми extend-имо існуючі або implement-имо запропоноване.

| OpenOnco workstream | Existing TaskTorrent Proposal(s) | Що ми додаємо понад |
|---|---|---|
| `feat/regimen-phases-refactor` | #18 (volume_impact) — relevant if rebuilds all regimens | Reference до `Regimen.phases` shape у chunk-spec template для майбутніх regimen-creating chunks |
| `feat/citation-verifier` | #13 (citation-verify validator gate) — partial overlap | New optional chunk-spec field: `Verifier Threshold` (e.g., "≥85% claims pass Anthropic Citations API"). Skill `citation-verification.md` update з Citations API + CoVe |
| `feat/one-prompt-onboarding` | #19 (claim coordination — implemented), #7 (branch-name CI gate). **NOT adopting #21** (per Q3 = always-latest-fail-loud) | New required fields: `Severity` (low/medium/high stakes) + `Min Contributor Tier` (rejected/new/established/trusted). Static `index.json` for `next_chunk.py`. Public landing tied to verifier-in-CI gate |

### 3.1. Що з нашого додаємо як NEW Proposals для their living doc

Три речі, які НЕ входять у поточні 21 Proposal — варто запропонувати maintainer-у task_torrent для додавання:

| Proposal-кандидат | Зміст | Ціна |
|---|---|---|
| **#22 Severity + Min-Tier фіолд** | `Severity: low\|medium\|high` + `Min Contributor Tier: new\|established\|trusted` у chunk-spec. Linter validates. Дозволяє tier-based gating (див. `one-prompt-onboarding-plan-2026-04-28` §8.1) | ~½ день |
| **#23 Verifier Threshold field** | Опціональний `Verifier Threshold` у chunk-spec для chunks, що включають citation-verification. Linter перевіряє наявність для chunks із `topic_label: citation-verify`. Default = 85% if not specified | ~¼ день |
| **#24 Cross-repo contract sync** | Published canonical contract doc, sync mechanism: (a) у task_torrent — `docs/cross-repo-contract.md` (canonical); (b) у OpenOnco — `docs/contributing/cross-repo-contract.md` із frontmatter `synced_from: task_torrent@main#docs/cross-repo-contract.md` (per Q3 = always-latest, no tag); (c) CI на обох репо — daily job hash-compare (LF-normalized); mismatch → issue в обох | ~1 день |

**Ці 3 я подам як patch до їхнього `tasktorrent-improvement-plan.md` як L-22/L-23/L-24 + Proposal #22/#23/#24.**

## 4. File-by-file changes у task_torrent

### 4.1. From `feat/regimen-phases-refactor` (мінімальний)

| Файл у task_torrent | Зміна | Effort |
|---|---|---|
| `chunks/openonco/_template.md` (якщо існує — інакше не торкаємось) | Reference до `Regimen.phases` shape | ¼ год |
| `skills/drug-evidence-mapping.md` | Додати приклад phases-aware drafting | ½ год |
| _НЕ_ змінюємо `lint_chunk_spec.py` | Phases — це OpenOnco-side schema, не task_torrent-level | — |

**Загалом: <1 година.** Phases-refactor — внутрішня OpenOnco справа.

### 4.2. From `feat/citation-verifier`

| Файл у task_torrent | Зміна | Effort |
|---|---|---|
| `tasktorrent/lint_chunk_spec.py` | Add conditional check: chunks з `Topic Labels: citation-verify` мусять мати `Verifier Threshold` секцію | 2-3 год |
| `skills/citation-verification.md` | Update: Anthropic Citations API as canonical verifier, CoVe як fallback, two-agent disagreement-as-flag pattern | 1-2 год |
| `docs/safety-rules.md` | Add §"Citation grounding verification" — verifier як obligatory pre-merge gate | 1 год |
| `chunks/openonco/citation-*.md` (3 файли: `citation-semantic-verify-v2`, `citation-verify-914-audit`, possibly future) | Add `## Verifier Threshold` section | 2 год |
| `docs/tasktorrent-improvement-plan.md` | Add L-22 + Proposal #22 (Verifier Threshold field) | ½ год |

**Загалом: ~1 день.**

### 4.3. From `feat/one-prompt-onboarding` ⚠️ найбільший impact

| Файл у task_torrent | Зміна | Effort |
|---|---|---|
| `tasktorrent/lint_chunk_spec.py` | Add `Severity` + `Min Contributor Tier` to REQUIRED_SECTIONS. Validation: Severity ∈ {low, medium, high}; Min Tier ∈ {new, established, trusted} | ½ день |
| `chunks/openonco/*.md` (всі 12) | Audit на consistency. Add `Severity` + `Min Tier` per chunk. Best guess defaults: source-stub/UA-translation = low/new; BMA/indication = medium/established; regimen/charter = high/trusted | 1 день |
| `chunks/openonco/README.md` | Add `Severity` + `Min Tier` columns у shelf-index table | ½ год |
| `docs/openonco-pilot-workflow.md` | Update workflow: tier-system + onboarding-via-bootstrap-script reference | 1 год |
| `docs/chunk-system.md` | Update Schema with `Severity` + `Min Tier` fields | 1 год |
| **NEW**: `docs/cross-repo-contract.md` | Single source of truth — schema+versioning+sync rules. Reference у обох репо | 2-3 год |
| Optional: `chunks/openonco/index.json` (auto-generated) | Static published JSON for fast `next_chunk.py` parse without GitHub API rate-limits. CI rebuilds on chunk-spec change | 2-3 год |
| `docs/tasktorrent-improvement-plan.md` | Add L-22/L-23/L-24 + Proposal #22/#23/#24 | 1 год |

**Загалом: ~2.5-3 дні.**

### 4.4. Від нас — sync-rule mechanism (Q4 рішення)

| Файл | Repo | Що |
|---|---|---|
| `docs/cross-repo-contract.md` | task_torrent | **Canonical**. Schema, versioning, sync rules. Frozen per release tag |
| `docs/contributing/cross-repo-contract.md` | OpenOnco | **Mirror**. Frontmatter: `synced_from: task_torrent@main#docs/cross-repo-contract.md` (per Q3 — always main, no tag). Identical content otherwise |
| `.github/workflows/cross-repo-sync-check.yml` | Both repos | Daily CI: `gh api raw` обидва файли, hash-compare (LF-normalized). Mismatch → auto-create issue в обох репо із diff |
| _**НЕ створюємо** `.tasktorrent.yaml`_ | — | Per Q3 = always-latest. Без version pin |

**Загалом: ~1 день для sync mechanism.** Implements Q4 рішення.

## 5. Schema versioning approach: "Always latest, fail loud" (per Q3)

**Не adopt-имо Proposal #21.** Користувач обрав простіший підхід для solo-maintainer / one-consumer scenario.

### 5.1. Як це працює

```
- task_torrent НЕ тегує semver releases
- task_torrent НЕ публікує `_contribution_meta.yaml.tasktorrent_version` поле
- OpenOnco НЕ створює `.tasktorrent.yaml`
- Усі URL у issue-templates referen `main` HEAD, не release tag
- Validators читають raw raw.githubusercontent.com/.../main/... як завжди

КОЛИ schemas drift (наприклад, task_torrent додає required field):
  - lint_chunk_spec.py @ task_torrent main fails closed on existing chunk specs
  - OR OpenOnco validator fails clean із чітким error:
    "chunk-spec at task_torrent/main has section X that this validator
     doesn't understand. Please update OpenOnco validator: see commit Y in task_torrent."
  - Mismatch видно одразу при першому запуску, не silent
```

### 5.2. Все одно бамп — у CHANGELOG, не у version tag

Breaking changes (наші 3 нові required sections — Severity, Min Tier, Verifier Threshold) landing у task_torrent `main` як звичайні merge commits + entry у `docs/CHANGELOG.md`:

```
## 2026-04-30 — Cross-repo sync v1
+ Severity required section у chunk-spec (per OpenOnco onboarding plan §8.1)
+ Min Contributor Tier required section (per OpenOnco onboarding plan §8.1)
+ Verifier Threshold conditional for citation-* chunks
- Existing 12 OpenOnco chunks backfilled with defaults

Breaking: lint_chunk_spec.py rejects pre-this-commit chunk specs.
```

### 5.3. Trade-off, який ми приймаємо

| Що отримуємо | Що ризикуємо |
|---|---|
| Швидка ітерація, нульовий ceremony cost | Multi-consumer adoption у майбутньому потребує retroactive versioning |
| Один файл `CHANGELOG.md` замість release-tags + migration tables | Time-travel debugging тільки через git log, не через checkout v0.X |
| Менше boilerplate в OpenOnco валідаторі | Якщо хтось fork-не TaskTorrent для іншого проєкту — їм доведеться додавати pinning самим |

**Цей trade-off виправданий поки:** TaskTorrent — solo-maintainer проєкт із одним consumer (OpenOnco). Якщо приходить N=2-й consumer — переоцінюємо.

## 6. Coordination protocol (per Q1 = patches-not-direct-write)

Я не маю write-access у task_torrent. Worflow:

```
1. У OpenOnco repo, я створюю:
   contributions/task_torrent_patches/
   ├── README.md                          # Index + apply order
   ├── 0001-add-severity-fields.patch    # git format-patch style
   ├── 0002-add-verifier-threshold.patch
   ├── 0003-cross-repo-contract.patch
   └── ...

2. Кожен patch — git format-patch стиль:
   - From: Claude (via maintainer)
   - Subject: line
   - Diff
   - Self-contained (one logical change)

3. Maintainer (ти):
   - cd ~/task_torrent
   - git checkout -b feat/cross-repo-sync (без version у назві — per Q3)
   - git am ~/cancer-autoresearch/contributions/task_torrent_patches/*.patch
   - git push, open PR у task_torrent

4. Після merge у task_torrent:
   - Add CHANGELOG.md entry (breaking changes описано)
   - НЕ робимо: semver tag, .tasktorrent.yaml у OpenOnco — per Q3
   - Run sync-check CI (для cross-repo-contract.md hash-compare)
```

Альтернатива (Q1=1a в майбутньому): дати мені contributor-permission — спрощує flow, але user не вибрав це.

## 7. Sequencing — узгоджено з OpenOnco refactor train

```
ФАЗА 0: Pre-conditions
└─ OpenOnco PR #3, #5, #29 закриті (поточний стан, ще open)

ФАЗА 1: Schema-side у OpenOnco (PR1)
└─ feat/regimen-phases-refactor: schema + loader auto-wrap
   → task_torrent untouched (per §4.1)

ФАЗА 2: Render + manual migration у OpenOnco (PR2)
└─ feat/regimen-phases-refactor: render + 18 YAML
   → task_torrent untouched

ФАЗА 3: TaskTorrent schema sync — НОВИЙ ETAP
├─ Patches у contributions/task_torrent_patches/ готові
├─ Maintainer apply через git am, push to main
├─ CHANGELOG.md entry для breaking changes
└─ Sync-check CI active у обох (для cross-repo-contract.md)
   (НЕ робимо: semver tag, .tasktorrent.yaml, version field — per Q3)

ФАЗА 4: feat/citation-verifier (паралельно з ФАЗА 5)
├─ OpenOnco-side: Citations API verifier script + CI
└─ task_torrent-side: per §4.2 (skill update + safety-rules)

ФАЗА 5: feat/one-prompt-onboarding scripts (паралельно з ФАЗА 4)
├─ OpenOnco-side: next_chunk.py + bootstrap + tier system
└─ task_torrent-side: per §4.3 (Severity + Min Tier audit)

ФАЗА 6: GA gate (per onboarding plan §6)
└─ Public landing flip коли verifier у CI + ≥3 active chunks
```

ФАЗА 3 — **новий блокер** перед ФАЗА 4-5. Без нових fields у task_torrent main (Severity, Min Tier, Verifier Threshold) наші scripts (next_chunk.py, citation-verifier extensions) будуть посилатись на ще-не-існуючі поля. Це і є "fail loud" поведінка з Q3 — validators крикнуть, не silent-accept.

## 8. Effort consolidated

| Workstream | OpenOnco-side | task_torrent-side (patches) | Maintainer apply | Разом |
|---|---|---|---|---|
| regimen-phases-refactor | 5.5 днів (schema+render+18 YAML) | <1 година | <½ год | ≈5.5 днів |
| citation-verifier | 2-3 дні | 1 день | ½-1 день | ≈4-5 днів |
| one-prompt-onboarding | 5.75 днів (з tier system) | 2.5-3 дні | 1-2 дні | ≈9-11 днів |
| Sync-rule mechanism | ½ день | ½ день | ½ день | ≈1.5 дні |
| **Загалом** | **~14-15 днів** | **~5-6 днів** | **~2-3 дні** | **~21-24 днів elapsed** |

Раніше попередня оцінка для one-prompt onboarding plan була "13-15 днів elapsed for GA". Тепер з task_torrent integration — **21-24 дні**. Maintainer-apply час (2-3 дні) — це **bottleneck**, не coding.

## 9. Open questions (нові, що з'явились після recon)

1. **Чи оновлюємо `protocol-v0.4-design.md` (17KB)?** — Цей файл я не читав детально. Якщо там вже описаний trust model + schema-evolution, наш sync-rule може overlap. Треба прочитати перед написанням patches.
2. **Hash-compare у sync-check CI — чи приймається noise від line-ending differences (CRLF vs LF)?** Windows-collaborators (як user) можуть випадково пушити CRLF. Сanonicalize обидва — read-and-normalize before hash.
3. **Який тип patches генерую — `git format-patch` (за commit) чи `git diff > patches/X.patch` (cumulative)?** Перший зручніше для review, другий для bulk-apply. Я б голосував за format-patch.
4. **Чи запускаємо ФАЗА 3 (task_torrent schema sync) ДО `feat/citation-verifier` та `feat/one-prompt-onboarding`, чи паралельно?** Я виклав sequentially у §7. Альтернатива — паралельно з coding на OpenOnco-side. Ризик паралельного: OpenOnco scripts можуть посилатись на нові поля, що ще не landed → "fail loud" спрацює, але прибуде шум у CI під час coding-вікна. Sequentially чистіше.

## 10. Cross-references

- **Цей repo:**
  - `docs/reviews/regimen-phases-refactor-plan-2026-04-28.md`
  - `docs/reviews/one-prompt-onboarding-plan-2026-04-28.md` (особливо §8.1 для tier system)
- **task_torrent repo:**
  - `docs/tasktorrent-improvement-plan.md` (живий документ, 21 Proposals)
  - `docs/protocol-v0.4-design.md` (17KB — потрібно read для §9 question 1)
  - `tasktorrent/lint_chunk_spec.py` (canonical contract enforcement, v0.4)
  - `chunks/openonco/*.md` (12 specs, потребуть Severity+Min-Tier backfill)
- **CHARTER:**
  - §6.1 — two-reviewer governance
  - §8.3 — LLMs not clinical decision-makers (architectural foundation)
  - §2 — non-commercial / banned commercial sources

---

## Decision log

| # | Питання | Відповідь | Reasoning |
|---|---|---|---|
| 1 | Окремий plan-doc чи інтегрувати? | Окремий | Cross-repo coordination — окремий concern, не subсекція жодного з 3 OpenOnco workstreams |
| 2 | Дублюємо чи extend-имо їх improvement plan? | Extend (3 NEW Proposals: #22/#23/#24) | Уникаємо drift; living doc — їхній механізм |
| 3 | Versioning approach | "Always latest, fail loud" — НЕ adopt-имо Proposal #21 | Per Q3 user choice. Solo-maintainer / one-consumer не платить ціну ceremony. Trade-off задокументовано у §5.3 |
| 4 | Sync mechanism для contract doc | Both repos + automated drift-detection (CI hash-compare) | Per user Q4 = "sync" |
| 5 | Coordination без write access | git format-patch у contributions/task_torrent_patches/ | Per user Q1 = "1b" (patches not direct PRs) |
| 6 | Sequencing | task_torrent schema sync ДО citation-verifier + onboarding scripts | Без нових fields у task_torrent main scripts ламатимуться (fail loud per Q3) |
| 7 | Чи зачіпає phases-refactor task_torrent суттєво? | Ні (<1 год) | Phases — internal OpenOnco schema, не task_torrent-level concern |
