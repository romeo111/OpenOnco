# One-Prompt Contributor Onboarding — план (cross-repo)

**Дата:** 2026-04-28
**Статус:** план узгоджено, до коду не приступали
**Тригер:** запит користувача — "чи можна зробити короткий і безпечний промпт типу 'я хочу допомагати лікувати рак, знайди TaskTorrent і приймайся за роботу', щоб агент сам узяв чанк, виконав, відкрив PR?"

## 1. Vision

Цільовий UX для волонтера-контриб'ютора зі своїм AI-tool (Claude Code / Codex / Cursor / ChatGPT):

```
[8-line paste-and-go prompt + URL]
```

→ агент сам: знаходить наступний доступний чанк, claim, виконує, валідує, відкриває PR.

## 2. Кросс-репо scope (≈80/20)

Робота joint, але вага нерівна:

| Репо | Внесок | Що змінюється |
|---|---|---|
| **OpenOnco** (`romeo111/OpenOnco`) | ≈80% | `next_chunk.py` CLI, `bootstrap_contributor.sh`, `auto_claim.sh`, `auto_pr.sh`, `PROMPT_PASTE_AND_GO.md`, validator hardening |
| **task_torrent** (`romeo111/task_torrent`) | ≈20% | Стандартизація chunk-spec metadata, optional static index JSON, README про cross-repo контракт |
| **openonco.info** (public landing) | ≈3 години | `/contribute` сторінка з copy-paste промптом + SHA-256 |

Переважна частина value лежить в OpenOnco-side скриптах. "Joint" не означає "паритетний effort".

## 3. Що вже побудовано (виявлено в коді)

| Компонент | Шлях | Статус |
|---|---|---|
| Contributor docs | `docs/contributing/CONTRIBUTOR_QUICKSTART.md` (184 рядки, 10 кроків) | ✅ |
| Per-chunk agent prompts | `docs/contributing/AGENT_PROMPT_<chunk-id>.md` | ✅ |
| Issue template | `.github/ISSUE_TEMPLATE/tasktorrent-chunk-task.md` | ✅ |
| Local validator | `scripts/tasktorrent/validate_contributions.py` | ✅ |
| Stale-claim auto-release | `scripts/tasktorrent/auto_release_stale_claims.py` (14d) | ✅ |
| 24h SLA enforcement | `scripts/tasktorrent/check_claim_sla.py` | ✅ |
| Maintainer-side merge | `scripts/tasktorrent/upsert_contributions.py` | ✅ |
| Manifest overlap detection | `scripts/tasktorrent/check_manifest_overlap.py` | ✅ |
| Two claim methods | `formal-issue` + `trusted-agent-wip-branch-first` (L-19) | ✅ |
| Banned-source list | SRC-ONCOKB, SRC-SNOMED, SRC-MEDDRA (CHARTER §2) | ✅ |
| Reference PoC sidecar | `contributions/civic-bma-reconstruct-all/bma_egfr_t790m_nsclc.yaml` | ✅ |

## 4. Cross-repo контракт (pinned)

Перевірено на реальному issue #26 (`trial-source-ingest-pubmed`).

### 4.1. Discovery query (GitHub API)

```
GET /repos/romeo111/OpenOnco/issues
  ?labels=chunk-task,status-active
  &assignee=none
  &state=open
```

### 4.2. Issue body — обов'язкові секції

Всі чанки використовують структуровану markdown із передбачуваними заголовками:

```
## Chunk Spec       → перша посилання на task_torrent/chunks/openonco/<id>.md
## Chunk ID          → перший inline-codeblock = chunk-id
## Drop Estimate     → "~N Drops (~Mk tokens)" — token budget
## Branch Naming     → codeblock з повним branch name
## Sidecar Output Path → codeblock зі шляхом
## Claim Method      → "formal-issue" | "trusted-agent-wip-branch-first"
## Task Manifest     → manifest items
## Acceptance Criteria (machine-checkable) → автоматичний gate
## Acceptance Criteria (semantic, maintainer-checked) → людський gate
```

Парсер `next_chunk.py` витягує chunk-id, branch-name, spec-URL, claim-method, token-budget регекспами на ці заголовки. Відмова парсера = чанк marked maintainer-review.

### 4.3. URL patterns

- Chunk spec (canonical): `https://github.com/romeo111/task_torrent/blob/main/chunks/openonco/<chunk-id>.md`
- Agent prompt (paste-and-go): `https://github.com/romeo111/OpenOnco/blob/master/docs/contributing/AGENT_PROMPT_<chunk-id>.md`
- Reference sidecar: `https://github.com/romeo111/OpenOnco/blob/master/contributions/<chunk-id>/<reference>.yaml`

### 4.4. Поточний стан черги

⚠️ **Усі `chunk-task` issues станом на 2026-04-28 закриті.** Public-facing landing запускати **не раніше**, ніж буде ≥3 `status-active` чанків (інакше перший контрибутор бачить "no chunks available").

## 5. Gap analysis — що бракує

### 5.1. OpenOnco-side (≈3.5 дні)

| Компонент | LOC | Effort |
|---|---|---|
| `scripts/tasktorrent/next_chunk.py` — CLI парсер issue body, повертає JSON next-chunk | ~80 | 1 день |
| `scripts/tasktorrent/bootstrap_contributor.sh` — fork+clone+env+next_chunk пайплайн | ~50 | ½ день |
| `scripts/tasktorrent/auto_claim.sh <chunk-id>` — branch+WIP-commit+push | ~10 | ¼ день |
| `scripts/tasktorrent/auto_pr.sh <chunk-id>` — `gh pr create` з шаблоном | ~15 | ¼ день |
| `docs/contributing/PROMPT_PASTE_AND_GO.md` — canonical 8-line промпт | — | ½ день |
| End-to-end test із одним волонтером | — | 1 день |

### 5.2. task_torrent-side (≈1.25 дні)

| Компонент | Effort |
|---|---|
| Стандартизація chunk-spec front-matter (yaml header або фіксовані ## заголовки) | ½ день |
| Optional: static `index.json` опубліковано через GitHub Pages (next_chunk.py може тягти швидше за GitHub API) | ½ день |
| README з описом cross-repo контракту | ¼ день |

### 5.3. Public landing (≈1.5 дні)

| Компонент | Effort |
|---|---|
| `openonco.info/contribute` — статична сторінка з paste-and-go промптом | ½ день |
| SHA-256 для `bootstrap_contributor.sh` (medical-credibility hygiene; `curl | bash` як MVP, `pip install openonco-contribute` як v0.2 path — одна лінія в доку, не цілий розділ) | ¼ день |
| End-to-end perspective stranger (UX walkthrough) | ½ день |

**Загалом ≈6 днів для production-ready one-prompt onboarding.**

## 6. Sequencing decision — verifier як GATE для public landing

⚠️ **Це найважливіший пункт усього плану.** Радикальне уточнення проти попередньої розмови.

### Чому verifier має йти перед публічним onboarding

Поточний validator ловить: schema errors, banned sources, missing fields, unknown SRC-IDs. Не ловить: семантичну коректність цитат, evidence direction, "fake-but-plausible" зміст. **Це саме те, що додає `feat/citation-verifier`.**

Onboarding scales contributor inflow. Reviewer time per chunk залишається ~constant без semantic auto-checks. Якщо запустити onboarding-first:
- Contributor velocity 5×
- Reviewer capacity unchanged
- **Bottleneck переїжджає з contributor до reviewer**, не зникає
- Черга PR росте unbounded

Verifier-first означає: кожен PR прибуває з grounding pre-checked → reviewer time per chunk падає → **тоді** scaling contributors compounds. Інакше — це pump-and-suffer.

### Послідовність

```
ФАЗА 0 — pre-conditions
└─ Завершити поточні відкриті PR (#3, #5, #29)

ФАЗА 1 — паралельний розвиток (technically independent)
├─ feat/regimen-phases-refactor   ← внутрішня schema work
├─ feat/citation-verifier          ← MUST land in CI before §3
└─ feat/one-prompt-onboarding      ← можна розробляти, але НЕ відкривати landing

ФАЗА 2 — onboarding GA gate
└─ ❗ Не флипати public-facing landing на openonco.info/contribute, поки:
   ├─ citation-verifier у CI на every PR
   ├─ ≥3 свіжих status-active chunk-task issues у черзі
   ├─ Reviewer bandwidth перевірено (див. §7)
   └─ Threat model defenses активні (див. §8)

ФАЗА 3 — soft launch
├─ Запросити 3-5 trusted volunteers через приватні канали
├─ Метрики: time-to-first-PR, validator-pass-rate, reviewer-touch-time
└─ Ітерувати

ФАЗА 4 — public launch
└─ openonco.info/contribute відкрито
```

Гілки **технічно незалежні** — можна розробляти `feat/one-prompt-onboarding` паралельно з `feat/citation-verifier`. Залежність — на момент **публічного запуску**, не на момент написання коду.

## 7. Reviewer bottleneck (named, not solved)

**Поточна капасіть:**
- 3 reviewers (Co-Leads) per CHARTER §6.1
- Dev-mode exemption: 1-of-3 sufficient у v0.1
- Full §6.1: 2-of-3 sufficient post-pilot

**Якщо contributor velocity ×5:**
- 3 reviewers × N chunks/week → ~3N (dev-mode) або ~1.5N (full)
- Чергa росте якщо contributor inflow > reviewer throughput
- Onboarding scales одну сторону рівняння

**Опції (план не вирішує, але називає):**
1. **Більше reviewers** — але recruitment of clinical co-leads — повільний (місяці)
2. **Async-batched review** — reviewer бере 5 PR одночасно, амортизує context-switch
3. **Tiered review** — низько-stakes чанки (UA translations, source stubs) — single-sample 1-of-3; high-stakes (BMA, regimen, indication) — обов'язково 2-of-3
4. **Auto-promotion bands** — якщо validator + verifier passes + sidecar matches reference shape >95% → auto-merge до `contributions/`, signoff потрібен лише для апсерту в `hosted/`

Ризик не названий → onboarding запускається → черга росте → ентропія. Має бути в плані як explicit known-limit.

## 8. Threat model — повна таблиця

Інтегровано advisor feedback. Три попередньо-непомічені вектори (T7-T9).

| # | Загроза | Поточний захист | Що додати |
|---|---|---|---|
| T1 | Adversarial PR (фейкові цитати, отруєння KB) | Banned sources, validator catches schema, two-reviewer signoff | CI: SRC-id resolves до реального PMID/DOI |
| T2 | Token-cost / abuse claims | 14-day auto-release, 24h SLA | Rate-limit per GitHub-user (≤2 active claims); tier-based eligibility — див. §8.1 |
| T3 | Agent виконує malicious код з brief | Brief — markdown, worktree isolation | Sandbox container для validator |
| T4 | Contributor пише в `hosted/content/` | CONTRIBUTOR_QUICKSTART забороняє | Pre-commit: блок stage у hosted/ якщо не maintainer |
| T5 | Auto-merge bypass review | Manual merge by maintainer | Branch protection rules на master |
| T6 | Agent пише medical advice phrasing | Documented в QUICKSTART | Lint: regex для banned phrases ("best treatment", "patients should") |
| **T7** | **Prompt injection в chunk briefs** | Briefs maintainer-authored (наразі OK) | **Майбутнє: contributor-suggested briefs / external URL fetches → потребує sanitization layer** |
| **T8** | **Sock-puppet identity** (нові GitHub usernames для evade rate-limits) | — | **Tiered contributor system + identity attestation — повний дизайн у §8.1. Не запобігає, але raises cost** |
| **T9** | **Off-topic poisoning** (sidecar passes schema але цитата не підтримує claim) | — | **Rows T9 + verifier = 1:1 mapping. Це ЯДРО `feat/citation-verifier`** |
| T10 | CHARTER §8.3 violation (LLM як decision-maker) | Architectural: contributions у sandbox dir, NEVER engine | Жодного авто-апдейту KB, all через 2-reviewer signoff |

**Зв'язок T9 ↔ verifier явно у плані:** саме off-topic poisoning є load-bearing reason для verifier-first sequencing у §6.

## 8.1. Author identity attestation + contributor tier system (T2 + T8 expansion)

Дві комплементарні механіки. Identity attestation відповідає на питання "хто ти" (cryptographic). Tier system відповідає "що тобі дозволено" (privileges, given that we know who).

### 8.1.1. Identity attestation levels

| Рівень | Що | Effort | Що ловить | Що НЕ ловить |
|---|---|---|---|---|
| **L0** Signed commits | Branch protection requires GPG/SSH-signed commits, GitHub "Verified" badge | ½ день | Stolen-account attacks, anonymous force-pushes | Sock-puppet (один атакер = N keys) |
| **L1** `_contribution.github_identity` | Bootstrap-script через `gh auth status` записує в кожен sidecar: `{github_login, account_id, account_age_days, public_repos, attestation_ts}`. Validator перевіряє консистентність | ~1 день | Audit trail "хто і коли", per-user rate-limiting (T2), reputation tracking | Sock-puppet (новий username за 30с) |
| **L2** Sigstore keyless | Контриб'ютор підписує sidecar через `cosign sign-blob`, OIDC прокидає GitHub identity в публічний transparency log (Rekor) | ~2 дні | Tamper-evident sidecars, формальне non-repudiation | Sock-puppet, але створює permanent audit chain |
| **L3** GitHub App + reputation | Власний OpenOnco-Contribute GitHub App; short-lived installation tokens; track per-username metrics | ~5 днів | Sock-puppet **частково**, abuse-claims (T2), tiered-review eligibility | State-actor adversary |

**Прийнятий план:** L0 immediately (free), L1 до public GA (1 день), L3 post-launch коли reputation data накопичиться. L2 — only if formal non-repudiation потрібно (low priority).

### 8.1.2. Contributor tier system

Не binary "accept/reject", а tiered — щоб не відбити legit-новачків (онкологи / резиденти типово мають "нулячі" GitHub-акаунти).

| Тір | Сигнали | Що дозволено | Review-bar |
|---|---|---|---|
| **rejected** | `age=0d AND repos=0 AND profile_empty AND email_unverified` (мінімальний поріг — справді disposable acc) | Нічого. Bootstrap відмовляє з повідомленням "fill profile + verify email + try again in 7 days" | — |
| **new** | `age < 90d` OR `repos < 3` OR `≤1 prior accepted PR у цьому проекті` | Тільки **low-stakes chunks**: UA translations, source stubs (referenced, not hosted), citation audits | 2-of-3 reviewers **обов'язково** (override dev-mode exemption) |
| **established** | (`age ≥ 90d` AND `repos ≥ 3`) OR `≥3 accepted PRs у цьому проекті` | Усі чанки крім high-stakes (regimen-creation, charter-impacting) | Standard (1-of-3 dev-mode або 2-of-3 full §6.1) |
| **trusted** | `≥10 accepted PRs з validator-pass-first-try ≥90%` AND maintainer endorsement | Усі чанки, включно high-stakes | Standard, eligible для tiered single-sample review |

### 8.1.2.1. Queue × Severity × Tier matrix (per `kb-coverage-strategy.md`)

Cross-доку integration 2026-04-29: `kb-coverage-strategy.md` запровадила Queue A/B/C класифікацію (purpose), що ортогональна до Severity (stakes). Tier-eligibility = function of (queue, severity), не лише severity.

| Queue | Типова severity | Min tier | Приклади |
|---|---|---|---|
| **A — Coverage-fill** (entity count↑) | low або medium | `new` для low (UA-translation, source stubs); `established` для medium (BMA drafting) | `bma-drafting-gap-diseases`, `redflag-indication-coverage-fill` |
| **B — Audit-only** (read-only sidecars) | low | `new` (ризик низький — тільки findings, не fixes) | `citation-verify-914-audit`, `escat-tier-audit`, `rec-wording-audit` |
| **B — Remediation** (acts on triage queue) | medium або high | `established` для medium, `trusted` для high (clinical content edit) | `citation-verify-v2 remediation` (793-row queue), `rec-wording remediation` (229 critical) |
| **C — Schema-evolution** (cross-cutting field add) | high | `trusted` (charter-impacting) | `civic-bma-reconstruct-all`, `regimen-phases-refactor` |

`Queue` поле у chunk-spec (Proposal #26 у cross-repo plan §3.1) дає linter і `next_chunk.py` enough context для визначення min-tier. Без queue-tag system покладається тільки на severity, що недо-disambiguates.

### 8.1.3. Composite credibility signals (для tier elevation)

Кожен сигнал — +1 score; тhresholds для tier-промоції — конфігуровні:

- 2FA enabled
- Email verified (institutional > free email = +2 vs +1)
- Profile filled (bio, location, photo) — кожне поле +1
- Linked ORCID / LinkedIn у bio
- Prior PR/issue activity у будь-якому іншому public repo
- GitHub account age (continuous, не binary): +1 / 30 days
- Existing OpenOnco contributions: +3 per accepted PR

Score < 3 → forced to `rejected` regardless of age.
Score 3-5 → `new`.
Score 6-9 → `established`.
Score ≥10 + maintainer endorsement → `trusted`.

### 8.1.4. Anti-abuse hook (auto-suspend)

Якщо `new`-tier акаунт submits PR що fails validator з "exotic" failure pattern → auto-suspend на 30 днів. Exotic = одночасно ≥2 з:
- banned-source citations (`SRC-ONCOKB`/`SRC-SNOMED`/`SRC-MEDDRA`)
- writes to `knowledge_base/hosted/` поза whitelist
- medical-advice phrasing (regex: "best treatment", "patients should", "recommended")
- citation IDs не resolve до real PMID/DOI
- chunk-id у sidecar не відповідає branch name

Single-failure суб'єкт не triggers — це signature spammer, not novice mistake. 30-day suspension скидається після manual maintainer review.

### 8.1.5. Tier promotion path (трасть-bootstrap)

Будь-який реальний новачок-онколог із `age=0` починає у `rejected` і просувається ось так:

```
1. Fill GitHub profile (name, bio, photo, location)
   → score 3-5 → промоція до `new`
2. Take 1-3 low-stakes chunks (UA translation, source stubs)
   → 2-of-3 review кожен, але кожен accepted PR = +3 score
3. Після 3 accepted PRs → тоtal score ≥10
   → промоція до `established`
4. Після 10 accepted PRs з ≥90% validator-pass → 
   → eligible до `trusted` із maintainer endorsement
```

Realistic timeline: реальний волонтер може стати `established` за 1-2 тижні work, `trusted` — 1-2 місяці consistent contribution.

### 8.1.6. Effort breakdown

| Компонент | Effort |
|---|---|
| `scripts/tasktorrent/check_contributor_eligibility.py` (composite score + tier) | ½ день |
| GitHub Action на PR open (auto-comment з tier + review-requirement) | ¼ день |
| Auto-suspend bot (30-day) | ¼ день |
| Reputation tracker (per-user PR history JSON) | ½ день |
| Tier promotion bot (auto-promote when score crossed) | ¼ день |
| Tuning + testing thresholds (½ день треба для tuning через short pilot) | ½ день |

**Загалом ≈2.25 дні.** Один з найкращих ROI/day items у плані — захищає T2 + T8 + частина T3 одним механізмом.

### 8.1.7. Що НЕ намагаємось вирішити

- **State-actor adversary** з aged GitHub accounts ($10-50 на чорному ринку) — pas defense
- **Insider threat** (existing trusted contributor turns hostile) — peer review + git history
- **Coordinated bot-net через legitimate-looking accounts** — потребує behavioral analysis, поза scope
- **GitHub account compromise** — L0 signed commits частково; повністю — поза нашим control

Чесний flow: tier-system raises cost для drive-by spam і opportunistic adversaries. Determined attacker з ресурсами $1000+ — не блокується ніяк, але такого немає на медичних non-commercial KB-проектах.

## 9. The paste-and-go prompt — MVP

```
Ти — контриб'ютор OpenOnco (https://github.com/romeo111/OpenOnco) — безкоштовного
публічного інструменту допомоги в плануванні лікування раку.

Виконай:
  bash <(curl -sL https://openonco.info/contribute.sh)
  # SHA-256: <hash> (звірити перед запуском)

Скрипт зробить fork+clone, set up env, claim наступний доступний чанк, створить
worktree, видасть тобі canonical chunk-prompt у контекст. Дотримуйся:
- Output ТІЛЬКИ в contributions/<chunk-id>/, ніколи в knowledge_base/hosted/
- НЕ вигадуй SRC-* IDs (filе source_stub якщо потрібно)
- НЕ пиши medical advice, лише evidence drafting
- Запусти validator перед PR
- Один чанк = один PR
- Жодного git add -A, жодного --no-verify
```

8 рядків + URL. SHA-256 mention як одна лінія, не розділ.

V0.2 path (mention only): `pip install openonco-contribute` коли pypi-package буде.

## 10. Effort breakdown

| Workstream | Гілка | Effort | Залежить від |
|---|---|---|---|
| OpenOnco-side скрипти | `feat/one-prompt-onboarding` | 3.5 дні | — (technical independence) |
| task_torrent-side standardization | у repo `task_torrent` | 1.25 дні | — |
| **Identity attestation L0+L1 + tier system** (§8.1) | `feat/one-prompt-onboarding` | 2.25 дні | — (technical independence) |
| Public landing | (build_site або static deploy) | 1.5 дні | OpenOnco-side готово |
| Soft launch + iteration | — | 3-5 днів elapsed | Усе вище |
| Hardening (T7-T9 defenses) | — | 2 дні | citation-verifier у CI |

**Загалом 13-15 днів elapsed для production-ready GA**, з яких ~8.25 днів фокусованого coding (рахуючи tier system).

## 11. Що мені треба перед стартом

1. **Підтвердити: verifier-перед-public-landing GATE прийнятний.** Це впливає на маркетингову швидкість — onboarding "готовий" може стояти 1-2 тижні очікуючи verifier.
2. **Розпочати `feat/citation-verifier` пріоритетніше за `feat/one-prompt-onboarding`?** Або паралельно — обидва незалежні технічно.
3. **Поповнити чергу chunk-task issues** до запуску onboarding (зараз 0 active). Це окремий "chunk-design" workstream — не бачив поточних запланованих чанків. Список 5-10 наступних чанків треба сформувати.
4. **Reviewer bandwidth (§7) — потрібна окрема розмова** з Clinical Co-Leads перед launch: чи приймається tiered-review, чи готові до 5× inflow.
5. **task_torrent repo доступ** — у мене read-only наразі (через GitHub API). Для PR у task_torrent потрібен write/contributor-permission.

## 12. Cross-references

- `docs/reviews/regimen-phases-refactor-plan-2026-04-28.md` — паралельний рефактор schema (technical independence)
- `feat/citation-verifier` (TBD branch) — verifier algorithms (gating dependency, §6)
- CHARTER §6.1 — two-reviewer governance
- CHARTER §8.3 — LLMs not clinical decision-makers (architectural foundation)
- CHARTER §2 — non-commercial / banned commercial sources

---

## Decision log

| # | Питання | Відповідь | Reasoning |
|---|---|---|---|
| 1 | Окремий plan-doc файл? | Так | Cross-repo workstream — не subсекція phases-refactor |
| 2 | Cross-repo task confirmed? | Так | task_torrent host chunk specs; OpenOnco host validators + contributions; ~80/20 split |
| 3 | Verifier vs onboarding sequence | Verifier-first як GATE для public launch | Per advisor: інакше bottleneck переїжджає на reviewer |
| 4 | Reviewer bottleneck — solve чи name? | Name only у v1 | Solving потребує clinical co-lead recruitment (months), не блокує план |
| 5 | curl\|bash format | One-line MVP, pip path як v0.2 | Medical credibility — antipattern dramatize не потрібен |
| 6 | "Не приймати від нулячих акаунтів"? | Так, але tiered, не binary | Binary reject відсіює legit-новачків (онкологи з age=0). Tier system у §8.1 |
| 7 | "Rejected" tier поріг | Мінімальний: `age=0 AND repos=0 AND profile_empty AND email_unverified` | Точково throwaway accounts; реальні новачки можуть пройти за 5 хвилин (заповнити profile + verify email) |
| 8 | Identity attestation level | L0 immediately, L1 до public GA (1 день), L3 post-launch | L1 = найкращий ROI/day; L2 sigstore — only if formal non-repudiation потрібно |
| 9 | Queue × Severity × Tier matrix (added 2026-04-29) | Adopt orthogonal axes per `kb-coverage-strategy.md` integration | Severity сама по собі не disambiguates: low-stakes audit ≠ low-stakes coverage-fill. Queue tag (Proposal #26 у cross-repo plan) додає purpose dimension |
