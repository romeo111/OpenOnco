All facts confirmed: no `FUNDING.yml`, no `funding.json`, no `server.json`; `mcp_server/` present; `promo/` has `mcp-registries.md` and existing distribution material; `docs/llms.txt` and MIT `LICENSE` present. Here is the plan.

---

# OpenOnco — Funding & Distribution Plan

**Last updated:** 2026-06-18 · **Status:** v0.1 early-stage · **Maintainer:** solo + AI-assisted contributors

> **What OpenOnco is, for a funder/program.** Free, open-source clinical decision support for oncology tumor boards. A *deterministic rule engine* runs over a versioned, fully source-cited knowledge base and drafts two treatment-plan options for a clinician to verify. **No LLM picks the regimen or dose** — so it cannot hallucinate a drug or dose. It runs **offline / in-browser**, so it works without reliable connectivity and **patient data never leaves the device**. Most useful where specialist tumor boards are scarce (LMICs, rural care). Ukrainian clinical roots; bilingual UA/EN. Maps to **UN SDG 3 (health)**.
>
> **License:** code MIT, content CC BY 4.0 — non-commercial / public-good. **Links:** https://openonco.info · https://github.com/romeo111/OpenOnco
>
> **Honest maturity:** ~103 diseases, 471 cited sources, but **most content is STUB pending two-reviewer sign-off, with no formal clinical validation yet.** This shapes eligibility throughout (see §4).

---

## 1. Prioritized shortlist

Confidence and effort are carried over from per-target verification. Programs, fees, deadlines and region rules change — **verify each at apply time.**

### A. Apply now — best fit, lowest effort

| # | Target | Fit / confidence | Effort · who acts | Why now | Link |
|---|--------|------------------|-------------------|---------|------|
| 1 | **Official MCP Registry** (Anthropic-backed) | partial / low | low–med · either | Free listing, **no legal entity, no clinical-validity bar** — early-stage/STUB is *not* a blocker. The "app store" where Claude & other clients discover MCP servers. | https://registry.modelcontextprotocol.io/ |
| 2 | **DPG Registry** (Digital Public Goods Alliance) | good / med | low–med · either | Recognition, not cash, but it's **the biggest distribution lever for LMIC government/NGO adoption** and is referenced by downstream health funders (UNICEF, Digital Square, WHO). No legal entity required; MIT + CC BY satisfy the license indicator; SDG 3 + privacy-by-design + "no LLM picks dose" is a strong do-no-harm story. | https://app.digitalpublicgoods.net/signup |
| 3 | **Anthropic AI for Science** | partial / med | med · user (maintainer) | Up to **$20k API credits / 6 mo** (cash-equivalent for the LLM-as-prose tasks the CHARTER allows — KB extraction/translation). Rolling; evaluated 1st Monday each month. Solo maintainer technically eligible. | https://www.anthropic.com/ai-for-science-program-rules |
| 4 | **Claude for Open Source** | med-high | low · user | 6 mo free Claude Max 20x (~$1,200 value) for OSS maintainers; **no nonprofit entity required**. ⚠️ Applications **close 2026-06-30** (~12 days out). Personal-use plan, no API. | https://claude.com/contact-sales/claude-for-oss |
| 5 | **FLOSS/fund** (Zerodha) `funding.json` | partial / low | low · either | Adding the in-repo `funding.json` manifest is harmless and keeps the door open. ⚠️ A near-term **award is unlikely** — FLOSS/fund explicitly excludes "very new / minimal-usage" projects today. | https://floss.fund/ |

> **Note on items 4 & 5:** *list/prepare* now, but set expectations — #4 is a deadline sprint for the maintainer's personal Claude use (not infra); #5 is discoverability plumbing, not income at this stage.

### B. High-effort / high-value (watch + prepare)

| # | Target | Fit / confidence | Effort · who acts | Notes | Link |
|---|--------|------------------|-------------------|-------|------|
| 6 | **NLnet NGI Zero Restack** | good / high — but **NOT YET OPEN** | high · user | Best EU grant fit: **€5k–€50k R&D grants**, funds individuals (no legal entity), FOSS-only (MIT + CC BY qualify). As of 2026-06-18 the fund is "being set up" and NGI open calls are paused — **expected to reopen after summer 2026.** Frame as R&D (CIViC actionability engine, FHIR/mCODE intake, offline rule engine — *not* "fill in stubs"). **Action: WATCH** https://nlnet.nl/restack/ and https://nlnet.nl/funding.html after summer. | https://nlnet.nl/restack/ |

### C. Needs a legal entity / fiscal host first

| # | Target | Status | Notes | Link |
|---|--------|--------|-------|------|
| 7 | **Open Source Collective** (fiscal host) | partial / med · user | **The key enabler — see §2.** US 501(c)(6) umbrella so you receive donations / pay reviewers with no entity of your own. ~10% fee. Frictions: move repo to a GitHub **org**, line up a 2nd admin, use **manual verification** (only ~1 star). | https://opencollective.com/opensource/apply |
| 8 | **Open Collective / Open Source Europe** (alt fiscal host) | good / med · user | EU-based; explicitly accepts "any open-source project, regardless of size or maturity," including individuals. Cleaner for **EU grant payouts (NLnet/NGI)** and has a Ukraine-solidarity track. ~8–10% fee. **Pick ONE fiscal host per funding source** — don't run this *and* OSC for the same money. | https://opensourceeurope.org/ |
| 9 | **GitHub Sponsors** (via fiscal host) | partial / med · user | Always-on donate button. **Ukraine residents can't use direct Stripe payouts** → route through OSC. Requires a GitHub org + an OSC Collective set up *before* signup. ⚠️ Whether the OSC route fully neutralizes UA-residency is **undocumented — confirm with GitHub Support + OSC before relying on it.** | https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/using-a-fiscal-host-to-receive-github-sponsors-payouts |
| 10 | **Polar / thanks.dev** | low value · user | Donation surfaces. Both pay out via **Stripe, which excludes Ukraine residents** — only useful with a foreign entity or fiscal host. thanks.dev pays by dependency-graph usage; OpenOnco is an end-user app, so realistic inflow ≈ $0. **Lowest priority.** | https://polar.sh/ · https://thanks.dev/ |
| 11 | **Claude for Nonprofits** | **BLOCKED** · future · user | Up to 75% off Claude Team/Enterprise — but **requires 501(c)(3) or equivalent charitable status; no path for individuals.** Becomes viable only after incorporation / fiscal sponsorship. (Use **Claude for Open Source #4** instead in the near term.) | https://www.anthropic.com/news/claude-for-nonprofits |

---

## 2. The single most important enabler: a fiscal host

**Recommendation: adopt a fiscal host (Open Source Collective or Open Source Europe) — do *not* register your own nonprofit yet.**

**The problem it solves.** OpenOnco's #1 funding blocker is that it has no legal entity. Many channels (GitHub Sponsors payouts, donations, grant disbursement, Claude for Nonprofits) assume someone with a bank account, tax ID, and the legal standing to issue receipts and pay contributors. A solo maintainer — especially one with Ukraine ties, where Stripe payouts are unsupported — hits a wall.

**What a fiscal host is, plainly.** A fiscal host is an existing nonprofit that "adopts" your project as a line item under its own legal/financial umbrella. It receives money on your behalf, issues invoices and receipts, handles tax compliance, and pays out your reviewers and infra bills — **without you registering anything.** You manage a budget; they are the legal entity. Open Source Collective (US 501(c)(6)) and Open Source Europe (Belgium foundation) both do exactly this, take ~8–10%, and explicitly accept individual maintainers and immature projects.

**Why this beats registering a nonprofit now.** Incorporating a 501(c)(3) (or a Ukrainian/EU charity) means legal fees, a board, bylaws, annual filings, and months of lead time — heavy overhead for a one-maintainer v0.1. A fiscal host gives you ~90% of the benefit (receive funds, pay people, tax-deductible donations, satisfy "who do we pay?" on grant forms) in days, reversibly. **Incorporate later**, once recurring funding or a real team justifies it — and at that point Claude for Nonprofits (#11) also unlocks.

**Decision rule.** Use **one** host per funding source. If your near-term money is **EU grants (NLnet/Restack)** → favor **Open Source Europe** (cleaner EU payouts, Ukraine-solidarity track). If it's **GitHub Sponsors + global donations** → favor **Open Source Collective** (it's the supported GitHub Sponsors fiscal host). Don't double-host the same money.

**Prerequisites to line up before applying to either:**
1. Move the repo from `github.com/romeo111/OpenOnco` (personal) to a **GitHub Organization** (e.g. an `OpenOnco` org) — OSC's criteria require an org repo, and GitHub Sponsors' fiscal-host route does too.
2. Recruit a **2nd administrator** (strengthens the application; preferred, not strictly mandatory).
3. Use the **manual verification** path (OpenOnco has ~1 star, below the automated threshold).
4. For the Ukraine angle, **confirm in writing** with GitHub Support + the host whether routing through the host neutralizes UA-residency payout limits before relying on it.

---

## 3. Autonomous in-repo actions I can do now (checklist)

These need **no external accounts** and make every external submission above one short step for the maintainer. None touch clinical content or patient data.

- [ ] **`/.github/FUNDING.yml`** — sponsor button. Can point to custom URLs (Open Collective / Ko-fi / PayPal) and a `thanks_dev:` / `polar:` key without requiring GitHub Sponsors approval first. (Confirmed absent today.)
- [ ] **`funding.json`** (FLOSS/fund manifest, schema ~v1.1.0) at repo root/website — makes OpenOnco discoverable in the public FLOSS/fund directory. (Confirmed absent today.)
- [ ] **DPG self-assessment doc** (e.g. `docs/dpg-self-assessment.md`) — map OpenOnco to the **9 DPG indicators**: SDG 3 relevance, open license (MIT + CC BY), clear ownership, platform independence, documentation, non-PII data extraction, privacy & applicable law, open standards, do-no-harm (9A/9B/9C). Lead with the medical disclaimer, privacy-by-design ("data never leaves device"), and "no LLM picks regimen/dose." Pre-fills the registry submission form.
- [ ] **In-repo do-no-harm / privacy artifacts** referenced by DPG 9A/7 — a short data-handling/privacy statement, a content/medical-safety policy, and contributor-conduct doc, so DPG indicators point to *concrete* files, not implied ones. (`promo/disclaimer-checklist.md` is good raw material.)
- [ ] **MCP `server.json`** for the Official MCP Registry (current schema ~2025-12-11), namespace `io.github.romeo111/openonco`, plus the **PyPI README ownership marker** `mcp-name: io.github.romeo111/openonco`. (Confirmed absent today; `mcp_server/server.py` + `engine_bridge.py` exist; `promo/mcp-registries.md` already has pre-cleared blurbs.) **Drafting `server.json` is not enough on its own** — see caveat in §4.
- [ ] **JOSS `paper.md` + metadata** — *draft only, marked DO-NOT-SUBMIT.* 250–1000 words (summary + statement of need + comparison + references). State v0.1 / STUB / no formal validation honestly; add a "do not submit until" checklist. (See §4 — hard blockers today.)
- [ ] **Refresh `promo/distribution-plan.md` / `promo/mcp-registries.md`** to cross-reference this funding plan so the two stay consistent.

> I can do all seven drafts autonomously in this repo on a feature branch. They are prep artifacts; the maintainer reviews maturity claims and performs the external account/auth steps.

---

## 4. Honest caveats

- **Early-stage / no clinical validation disqualifies or weakens some targets.**
  - **FLOSS/fund (#5):** explicitly excludes "very new / minimal-usage" projects *today* — list, but don't expect a grant.
  - **Anthropic AI for Science (#3):** solo maintainer is *technically* eligible (no nonprofit required, 18+, Ukraine not excluded), but the program is framed for institution-affiliated researchers and scores on credentials / scientific merit / impact — STUB content + no validation is a real competitive disadvantage, not a hard bar. (The "$50k" figure floating around is **unverified — cite "up to $20k" only.** Credits are API-only.)
  - **JOSS:** has **hard current blockers** — software must be public + actively developed **>6 months**, **feature-complete** ("no half-baked solutions" — STUB content fails this), and show **demonstrated research use** (no formal validation yet). A submission today would likely be desk-rejected; 2026 rules also scrutinize AI-assisted dev. **Draft now, submit later.**

- **The MCP Registry needs a published package, not just `server.json` (#1).** The registry hosts *metadata only* — every entry must point to a published package (PyPI/npm/OCI/etc.) with ownership proof, **or** a reachable remote server URL. OpenOnco installs via `git clone` + `pip install -e` only — **there is no source-only listing path.** Lowest-friction fix: publish the Python stdio server to **PyPI**, add the `mcp-name:` README marker, then publish via the `mcp-publisher` CLI (maintainer GitHub device-auth). Effort is low-to-medium (one package release), not pure-low. Registry is **pre-GA** — "breaking changes or data resets may occur," so a listing could be reset before general availability.

- **Ukraine residency / Stripe is the load-bearing payout question.** Stripe excludes Ukraine-resident accounts, which directly blocks **GitHub Sponsors direct payouts, Polar, and thanks.dev**. The fiscal-host route (§2) is the realistic workaround, **but whether it fully neutralizes the residency restriction is undocumented — confirm in writing before relying on it.** (Ukraine is *not* excluded from Anthropic AI for Science; only Russia + Crimea/Donetsk/Luhansk are.)

- **One fiscal host per money.** Don't route the same funding through both OSC and Open Source Europe.

- **Programs / deadlines / fees change — verify at apply time.** Especially: Claude for OSS deadline (**~2026-06-30**), NLnet Restack first-call open date (**after summer 2026**), exact MCP `server.json` schema + CLI auth (pre-GA), fiscal-host fee %, and DPG indicator details. Don't cite dollar amounts not confirmed on the official rules page.

- **Keep framing consistent everywhere:** "research/support tool, **not a medical device**," human-verified, no LLM in the clinical decision path. This is both accurate and your strongest do-no-harm / safety story for DPG and health funders.

---

### Suggested sequence
1. **This week:** apply to **Claude for Open Source (#4)** before 2026-06-30; I draft all §3 in-repo artifacts.
2. **Next:** submit to the **DPG Registry (#2)** and **MCP Registry (#1, after PyPI release)**; apply to **Anthropic AI for Science (#3)**.
3. **Set up a fiscal host (§2)** — move repo to an org, recruit a 2nd admin — to unlock GitHub Sponsors + donations and to be grant-ready.
4. **Watch NLnet Restack (#6)** and apply in the first post-summer-2026 call, framed as R&D.

---

Repo facts verified for this plan (all absolute paths): no `C:\Users\805\cancer-autoresearch\.claude\worktrees\gallant-yonath-456e1c\.github\FUNDING.yml`, no `funding.json`, no `server.json`; present: `mcp_server\server.py`, `mcp_server\engine_bridge.py`, `promo\mcp-registries.md`, `promo\distribution-plan.md`, `docs\llms.txt`, MIT `LICENSE`.

---

# Reusable grant / program pitch

Both references are real and currently plausible. The pitch is the deliverable, so the body stays close to ~250 words; the program list is supplementary (marked confidence + verify-at-apply-time), per the accuracy rules.

---

# OpenOnco — Grant / Program Pitch (reusable boilerplate)

**One line:** Free, open-source, offline clinical decision support that helps oncology tumor boards draft safer treatment plans — built for the places where specialist expertise is scarcest.

**The problem.** Most of the world lacks reliable access to a multidisciplinary tumor board. In rural and low- and middle-income settings, treatment decisions are often made without specialist review, and a single missed drug interaction, contraindication, or dosing error can be fatal. The expertise exists — it just isn't where many patients are.

**The solution.** OpenOnco takes a patient profile and drafts **two** alternative, fully source-cited treatment-plan options (standard and aggressive) for a clinician to review. A **deterministic rule engine** reads a **versioned, citation-backed knowledge base** — **no language model ever chooses a regimen or dose**, so it cannot hallucinate a drug or dosage. It runs **offline / in-browser**: it works without connectivity, and **patient data never leaves the device**. A bundled MCP server lets any AI assistant query the engine safely.

**Why open-source / public-good.** Code is MIT, content CC BY 4.0; non-commercial by design. The project aligns with **UN SDG 3 (good health and well-being)** and the Digital Public Goods definition. It has Ukrainian clinical roots and a bilingual UA/EN site.

**Honest status.** Early-stage **v0.1**: ~103 diseases and 471 cited sources, most content still in **stub** state pending two-reviewer clinical sign-off. **No formal clinical validation yet.** Built largely by one maintainer with AI-assisted contributors.

**The ask.** Funding, compute credits, or recognition to unlock: **paid clinician-reviewer time** (two-reviewer sign-off on stubbed content), **independent clinical validation**, and **hosting/infrastructure**. In-kind support and DPG/registry recognition also move the needle.

**Not a medical device.** OpenOnco is a research/decision-support tool. Every recommendation must be verified by a qualified oncologist before use.

**Links:** https://openonco.info · https://github.com/romeo111/OpenOnco

---

### Maintainer notes (delete before submitting)

- **Eligibility caveat to disclose up front:** OpenOnco is an individual/small-team project, **not yet a registered nonprofit or legal entity**. Some grants require a fiscal sponsor or registered org — check this first; it is the most common disqualifier. Consider a fiscal sponsor (e.g., a software-freedom or open-source umbrella org) where one is needed.
- **Tailor the "ask"** to each program's allowed use of funds (some fund infra/compute only, not personnel).

### Real, currently-plausible programs to target — *verify all details at apply time; programs, scopes, and deadlines change*

| Program | Why plausible fit | Confidence | URL |
|---|---|---|---|
| **Digital Public Goods Registry (DPG Alliance, UN-endorsed)** | Recognition, not cash — strong fit: open-source + open content, SDG 3, privacy-by-design (offline, no data egress). Rolling nominations. | High (fit) / Medium (acceptance) | https://www.digitalpublicgoods.net/explore — nominate via https://github.com/DPGAlliance/publicgoods-candidates |
| **Patrick J. McGovern Foundation (AI for health / digital health)** | Funds AI-for-public-good incl. health equity in LMICs; rolling intake noted. Likely requires registered org / fiscal sponsor. | Medium | https://www.mcgovern.org/grants/ |
| **GitHub Sponsors / Open-source maintainer funding** | Ongoing maintainer support for a public-good FOSS project; no legal-entity barrier. | High (eligibility) | https://github.com/sponsors |
| **Cloud / AI compute credit programs (e.g., Azure/AWS/Google nonprofit & startup credits, Anthropic)** | Covers hosting + validation compute; some tiers accept individuals/early projects. | Medium | check each provider's nonprofit/startup credit page |

Do not cite dollar amounts or deadlines in an application without re-confirming them on the official page on the day you apply.

---

Sources: [Digital Public Goods Alliance registry](https://www.digitalpublicgoods.net/explore) · [DPG candidates (nomination)](https://github.com/DPGAlliance/publicgoods-candidates) · [Patrick J. McGovern Foundation grants](https://www.mcgovern.org/grants/)

