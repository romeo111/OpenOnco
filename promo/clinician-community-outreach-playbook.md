# OpenOnco — clinician & oncology community outreach playbook

> For MANUAL, disclosed posting by the maintainer/contributors. This is NOT autoposting — no bots, no sockpuppets. See the ethics preamble; if a post would violate it, do not post.

# OpenOnco Clinician Outreach — Ethics Preamble

> **Read this before posting anything, anywhere.** This preamble governs every template and venue in this playbook. If a post would violate it, do not send the post.

## Non-negotiable rules

1. **Manual, by the real maintainer.** Every post is written and submitted by hand by the actual project maintainer (or a named, real contributor). This is **not** autoposting. No bots, no scheduling tools, no scripts, no sockpuppets, no second accounts.
2. **Disclosure is mandatory.** You identify yourself as the maintainer/creator (or a contributor) in the post itself. No third-person "I stumbled on this cool tool" framing. No astroturfing. If you can't disclose, you don't post.
3. **Value-first and feedback-seeking, not salesy.** The ask is *"tear apart the clinical logic — tell me what's wrong,"* never *"sign up."* Lead with the problem you're trying to solve and the help you need.
4. **Respect each community's self-promotion rules.** Many medical and clinical forums ban or restrict promo, require mod permission, a specific flair, or a designated thread/day. State the actual rule and how to comply for each venue. **If a venue forbids self-promotion, do not post there** — participate genuinely or skip it.
5. **Medical-safety disclaimer on every public post.** Always state: informational decision *support*, **not a medical device**, not FDA-cleared, not clinically validated, not for patient self-use; every recommendation must be verified by a qualified oncologist. Be honest that the project is **early-stage v0.1** and most content is **STUB ("proposed, not approved")** — only 15 of 806 entities have two-reviewer sign-off.
6. **No spam cadence.** One genuine post per community, spaced out over time. Never cross-post the same text en masse across venues.
7. **Honor physician-license verification.** Some communities are verified-clinician-only. Post there only if the maintainer/contributor is an eligible, verified clinician for that venue. Do not falsify or imply credentials you don't hold.

## What OpenOnco actually is (use accurate facts only)

- Free, open-source clinical decision **support** for oncology tumor boards. A **deterministic rule engine** over a versioned, source-cited knowledge base drafts two alternative plans (standard + aggressive) **for a clinician to verify**. **No LLM picks the regimen or dose.** Every recommendation is cited.
- Scale (2026-06-17): 92 diseases, 664 indications, 384 regimens, 444 cited sources. MCP server lets ChatGPT/Claude/Cursor call the engine.
- Maturity: **early-stage v0.1**, mostly STUB content, **no formal clinical validation**, actively seeking clinician feedback.
- Site: https://openonco.info · Demo: https://openonco.info/try.html · Repo: https://github.com/romeo111/OpenOnco · License: code MIT, content CC BY 4.0.

## Prioritized venue sequence

Approach from **most receptive → strictest**. Learn from feedback and tighten the pitch before touching gated medical communities.

1. **Open-source / dev communities** *(most receptive)* — GitHub, Show HN, dev forums, MCP/tooling channels. Self-promotion of your own project is generally welcomed when disclosed. Lead with the architecture (deterministic engine, MCP server, CC BY data).
2. **Health-informatics / clinical-NLP / medical-AI** — informatics Slacks, FHIR/mCODE and medical-AI communities. Receptive to "show your work" tooling; lead with the no-LLM-decides-treatment design and the citation model.
3. **Ukrainian clinician & health-tech circles** — the project's home community; warm context, direct line to the target user. Disclose as maintainer; ask for clinical-logic critique.
4. **MedTwitter / oncology-on-X (#oncology, #MedTwitter)** — open, norms favor transparency. One disclosed thread; invite oncologists to poke holes. Honor any verified-clinician expectations.
5. **General oncology / clinician forums and subreddits** *(strict — last, and only where permitted)* — most restrict or ban promo. **Check each venue's rule first; get mod permission; use the required flair/thread; or don't post.** Several are verified-clinician-only — post only if eligible and verified. Where promo is forbidden, participate genuinely and do not pitch.

## Honest success metrics

Measure engagement and clinical scrutiny — **not** vanity reach or "conversions."

- **GitHub stars / watchers / forks** — passive interest signal.
- **Demo visits** to `try.html` — did people actually look at the engine.
- **Clinician feedback issues / discussions** — *the primary signal*: substantive critiques of the clinical logic, citations, or specific entities.
- **Co-Lead / contributor applications** — clinicians willing to do two-reviewer sign-off or contribute KB content.

A post that draws one sharp "your logic here is wrong because…" from a real oncologist is a bigger success than a hundred stars.

---

## Reddit clinical/medical subreddits

# Clinician Outreach: Reddit Clinical / Medical Subreddits

**Scope:** disclosed, manual, value-first feedback requests by the OpenOnco maintainer. **Not** autoposting, not sockpuppets, not "I found this cool tool" third-person posts.

> **Research caveat (read first):** Reddit gates its rule pages and search returned only generic SEO content, so the live, current rule text for most of these subs could **not** be machine-verified in this session. Every rule below is marked with a confidence tag. **Before posting anywhere, the maintainer must open the sub's sidebar / "About" → Rules and the community wiki and confirm the rule live.** Treat all "rule" descriptions tagged *(verify current rule)* as needing a 60-second manual check immediately before posting. The one item corroborated from a peer-reviewed source is r/AskDocs's verified-clinician flair model ([PMC7386284](https://pmc.ncbi.nlm.nih.gov/articles/PMC7386284/)).

**Standard safety footer** — append verbatim to every post that gets made:

> *Disclosure: I'm the maintainer of this open-source project, posting manually myself — no bots, no automation, no other accounts. OpenOnco is an informational decision-support prototype for clinicians — it is NOT a medical device, NOT FDA-cleared, NOT clinically validated, and NOT for patient self-use. It is early-stage (v0.1): most content is STUB / "proposed, not approved," and only 15 of 806 entities have two-reviewer clinical sign-off. Every recommendation must be verified by a qualified oncologist. Code MIT, content CC BY 4.0.*

---

## Verdict at a glance

| Sub | Post a promo thread? | Why |
|---|---|---|
| **r/medicine** | **No — do not self-promote.** | Self-promo / blogspam effectively banned; verified-clinician-only sub. Participate genuinely, or modmail first. |
| **r/oncology** | **Maybe — modmail first.** | Small, low-traffic; rules vary. Ask mods before posting. |
| **r/hematology** | **Maybe — modmail first.** | Small/niche; same as oncology. |
| **r/medicalschool** | **No promo posts.** | Heavy promo/app restrictions; wrong audience (students, not deciding clinicians). |
| **r/cancer** | **No — do not self-promote.** | Patient/caregiver support space; a clinician tool risks self-harm-by-patient misuse. Highest safety risk. |
| **r/clinicalresearch** | **Likely OK with disclosure** | More tolerant of disclosed project/feedback posts; relevant audience. **Best candidate #1.** |
| **r/healthIT** | **Likely OK with disclosure** | Built for health-tech discussion; tolerant of disclosed builder posts. **Best candidate #2.** |
| **r/AskDocs** | **No — never.** | Patients asking for medical advice; promo strictly banned; verified-clinician flair must not be leveraged to market. |

**Ready-to-post templates are provided only for the two greenlit subs (r/clinicalresearch, r/healthIT) plus a modmail-permission template for the "ask-first" subs (r/oncology, r/hematology).**

---

## r/medicine

**(a) Self-promo rule + whether/how to post** *(verify current rule)*
r/medicine is one of the strictest medical subs. Its long-standing posture: **no self-promotion, no blogspam, no advertising your own product/site/app**, and removal of content where the poster has a personal/financial stake. There is no routine "promo day." **Recommendation: do NOT post a promo thread.** If you believe there's genuine discussion value, **modmail the moderators first** and let them decide — do not post without explicit mod approval.

**(b) Verification barrier**
r/medicine is a **verified-clinician community** for full participation/flair (mods verify credentials privately). If the maintainer is themselves a licensed clinician, any participation here is **as a clinician contributing genuinely** — the clinician flair must never be sought or used to lend authority to the project. If the maintainer is not a verified clinician, treat this as a read/lurk-and-modmail-only space.

**(c) Post template**
**None.** Do not post a self-promo thread here. (If mods explicitly invite it via modmail, adapt the r/clinicalresearch template and lead with the mod's permission.)

**(d) Compliance / etiquette**
Participate genuinely on clinical-reasoning threads over weeks first. Never drop a link to your own project in a comment unless directly and specifically asked. Astroturfing here gets a permaban fast and burns the project's name in the most influential clinical sub on Reddit.

---

## r/oncology

**(a) Self-promo rule + whether/how to post** *(verify current rule)*
Small, relatively low-traffic sub mixing clinicians, trainees, and some patients. Rules are less codified than r/medicine but self-promotion is commonly restricted or removed without mod buy-in. **Recommendation: modmail the mods first** describing exactly what you'd post and asking permission + whether a flair is required. Post only if they say yes.

**(b) Verification barrier**
No reliable physician-verification gate documented. Because the audience is mixed (not all verified clinicians), the **medical-safety footer is essential** and the framing must stay "clinician-facing feedback request," not patient-facing.

**(c) Post template** — *use only after mod approval* (see shared modmail template below, then the r/clinicalresearch body adapted).

**(d) Compliance / etiquette**
Keep it strictly feedback-seeking ("tear apart the clinical logic"), not "try my tool." One post only. Do not cross-post the identical text to r/hematology the same day — rewrite and space it out by at least a week.

---

## r/hematology

**(a) Self-promo rule + whether/how to post** *(verify current rule)*
Niche, small. Same situation as r/oncology — promo typically frowned upon absent mod approval. **Recommendation: modmail first.** Only relevant if OpenOnco's heme content is mature enough to be worth heme-specialist scrutiny; given STUB status, consider waiting or framing as "heme coverage is thin — what's missing?"

**(b) Verification barrier**
No documented verification gate; mixed/uncertain audience. Safety footer mandatory.

**(c) Post template** — *use only after mod approval* (shared modmail + adapted body).

**(d) Compliance / etiquette**
Be candid that heme content is early/STUB; ask specifically what heme entities are wrong or missing. Space at least a week from any r/oncology post; do not paste identical text.

---

## r/medicalschool

**(a) Self-promo rule + whether/how to post** *(verify current rule)*
Strong restrictions on **self-promotion, apps, products, surveys, and "I built X"** posts; promo is typically confined to designated threads or banned outright, and survey/recruitment posts often need mod approval. **Recommendation: do NOT post a promo thread.**

**(b) Verification barrier**
No clinician verification (it's students). More importantly, **wrong audience**: med students are not the clinicians who select regimens at a tumor board, so this fails the value-first test for OpenOnco's actual ask.

**(c) Post template**
**None.**

**(d) Compliance / etiquette**
Skip as an outreach venue. If anything, participate genuinely; don't recruit.

---

## r/cancer

**(a) Self-promo rule + whether/how to post** *(verify current rule)*
This is a **patient and caregiver support community**, not a clinician forum. Self-promotion is restricted, but the bigger issue is **safety, not rules**. **Recommendation: do NOT self-promote here.**

**(b) Verification barrier**
N/A — and that's the problem. Posting a treatment-plan-generating tool to frightened patients/caregivers invites exactly the **patient self-use** the safety framing prohibits, regardless of disclaimers.

**(c) Post template**
**None.** Do not post.

**(d) Compliance / etiquette**
This sub is off-limits for promotion on ethical grounds. If the maintainer participates, it's purely as a supportive community member, never steering anyone to the tool.

---

## r/clinicalresearch  ✅ greenlit (verify rule, then post)

**(a) Self-promo rule + whether/how to post** *(verify current rule)*
More tolerant of disclosed, on-topic "I built a research/clinical tool, looking for critique" posts than the clinical-practice subs — but many such subs still require **disclosure of affiliation** and forbid recurring/spammy promo. **Recommendation: post ONE disclosed, feedback-first thread** after confirming the sidebar rules and checking whether a "self-promo" or "show-and-tell" flair exists. If a flair is required, apply it.

**(b) Verification barrier**
No physician-verification gate documented. The maintainer posts honestly as the project creator; no clinician-license claim should be made unless true.

**(c) Ready disclosed post template**

> **Title:** [Disclosure: I'm the maintainer] Open-source, source-cited oncology decision-support engine — looking for clinical-research critique of the methodology
>
> I maintain **OpenOnco**, a free, open-source clinical-decision-support prototype for oncology tumor boards, and I'm here for honest critique of the approach — not signups.
>
> **What it is, precisely:** a *deterministic rule engine* runs over a versioned, source-cited knowledge base and drafts two alternative treatment plans (a standard and a more aggressive option) for a clinician to verify. **No LLM picks the regimen or the dose** — the model only drafts prose; every recommendation carries a citation. There's also an MCP server so tools like ChatGPT/Claude/Cursor can *call the engine* — but it's the deterministic engine, not the model, that makes the clinical call. (To be clear, that's a product feature; I'm writing and posting this myself, manually.)
>
> **Where it stands (honestly):** v0.1, early. ~92 diseases, 664 indications, 384 regimens, 444 cited sources — **but most content is STUB ("proposed, not approved"), and only 15 of 806 entities have two-reviewer clinical sign-off. No formal clinical validation yet.**
>
> **What I'd genuinely value your eyes on:**
> 1. Is "deterministic rule engine + cited KB, LLM does prose only" a defensible architecture for decision support, or are there failure modes I'm underweighting?
> 2. How would you want provenance/versioning surfaced so a reviewer can audit *why* a plan was drafted?
> 3. What would a credible validation plan look like for something at this stage?
>
> Site: https://openonco.info · Demo: https://openonco.info/try.html · Repo: https://github.com/romeo111/OpenOnco
>
> *[append the standard safety footer verbatim]*

**(d) Compliance / etiquette**
One post; do not repost. Reply to every critical comment substantively. Have non-promo karma in the sub first. Don't cross-post the identical body to r/healthIT — rewrite the angle (research-methodology framing here, build/integration framing there) and space the two posts apart.

---

## r/healthIT  ✅ greenlit (verify rule, then post)

**(a) Self-promo rule + whether/how to post** *(verify current rule)*
A health-technology discussion community, generally tolerant of **disclosed builder/"I made this, feedback?"** posts, especially open-source ones — but still expects disclosure and dislikes repeat promo. **Recommendation: post ONE disclosed thread** after confirming the sidebar; check for a self-promo flair/megathread and use it if it exists.

**(b) Verification barrier**
None. Honest maintainer disclosure; no clinical-authority claims.

**(c) Ready disclosed post template**

> **Title:** [Disclosure: I'm the maintainer] Open-source oncology decision-support: deterministic rule engine + cited KB, with an MCP server — architecture critique welcome
>
> I build **OpenOnco**, a free/open-source (code MIT, content CC BY 4.0) clinical-decision-support prototype for oncology tumor boards. Posting manually as the maintainer myself, looking for technical and safety critique — not users.
>
> **Architecture:** a deterministic rule engine reads a versioned, source-cited knowledge base and drafts two candidate treatment plans (standard + aggressive) for a clinician to verify. **Deliberately, no LLM selects the regimen or dose** — the LLM only drafts surrounding prose; every recommendation is citation-backed. An **MCP server** exposes the engine so ChatGPT/Claude/Cursor can call it, keeping the deterministic engine (not the model) as the source of clinical logic.
>
> **Honest maturity:** v0.1. ~92 diseases / 664 indications / 384 regimens / 444 cited sources, **but most content is STUB and only 15 of 806 entities have two-reviewer clinical sign-off. No formal validation yet.**
>
> **Where I want HealthIT eyes:**
> 1. Is MCP a sane integration surface for clinical tooling, or am I inviting LLM-in-the-loop safety problems I should wall off harder?
> 2. How would you handle versioning/audit so a recommendation is reproducible and traceable to a KB snapshot?
> 3. What guardrails would you require before this is even pilot-able with real clinicians?
>
> Site: https://openonco.info · Demo: https://openonco.info/try.html · Repo: https://github.com/romeo111/OpenOnco
>
> *[append the standard safety footer verbatim]*

**(d) Compliance / etiquette**
One post; engage every reply. Lead with the open-source + safety framing (this audience rewards "I built guardrails," punishes "AI picks your chemo"). Don't duplicate the r/clinicalresearch text, and space the two posts apart.

---

## r/AskDocs  ⛔ do not self-promote (caution)

**(a) Self-promo rule + whether/how to post**
r/AskDocs is **patients asking clinicians for medical advice.** Self-promotion, advertising, and linking to external tools are **strictly prohibited**, and answers come from **moderator-verified clinicians** whose credentials are checked before flair is granted (corroborated by [PMC7386284](https://pmc.ncbi.nlm.nih.gov/articles/PMC7386284/)). **Recommendation: NEVER self-promote here.**

**(b) Verification barrier**
Verified-clinician flair is granted only after the mods privately confirm credentials. **That flair must never be used to lend authority to marketing** — doing so would be both a rule violation and an ethics violation. If the maintainer happens to be a verified clinician here, they answer patients' questions purely as a clinician and say nothing about the tool.

**(c) Post template**
**None.** Do not post.

**(d) Compliance / etiquette**
Highest-caution venue: a treatment-plan tool surfaced to advice-seeking patients is the exact patient-self-use failure mode the safety rules forbid. Off-limits entirely for outreach.

---

## Shared modmail permission template (for r/oncology, r/hematology — and any sub before posting)

> **Subject:** Permission to post a disclosed, feedback-seeking thread about an open-source oncology decision-support project
>
> Hi mods — I'm the maintainer of OpenOnco, a free, open-source clinical-decision-support *prototype* for oncology tumor boards (deterministic rule engine over a cited knowledge base; **no LLM picks regimen/dose**; every recommendation cited). It's early-stage v0.1 — most content is STUB and only 15 of 806 entities have two-reviewer sign-off; **not a medical device, not validated, not for patient use.**
>
> I'm **not** trying to drive signups — I want clinicians to tear apart the clinical logic and tell me what's wrong. I'd be posting manually, myself, as a one-time disclosed request. Before posting anything, I wanted to ask: **is a disclosed, one-time feedback request like this allowed here, and if so is there a required flair or designated thread?** Happy to follow whatever format you prefer, or to skip it entirely if it's not a fit. Thanks for keeping the sub clean.

---

## Operating rules across all venues
- **Manual only**, by the real maintainer, with disclosure in the title and body. No sockpuppets, no automation/bots/scheduled posting, no third-person "found this cool tool." (The product's MCP server lets AI tools call the *engine* — it has nothing to do with posting; all Reddit activity is done by the human maintainer by hand.)
- **One genuine post per community, spaced out** (at least a week between related posts). Never mass cross-post identical text — rewrite per audience (research-methodology vs. health-IT-architecture).
- **Safety footer verbatim on every post.** Always honest about STUB / no-validation status; never overstate maturity.
- **Greenlit now:** r/clinicalresearch, r/healthIT (verify sidebar, use any required flair). **Ask-first:** r/oncology, r/hematology (modmail). **Do NOT self-promote:** r/medicine, r/medicalschool, r/cancer, r/AskDocs — participate genuinely instead.
- **Never leverage clinician status to market.** If the maintainer is a verified clinician in any verified sub, they participate only as a clinician and never use that flair/authority to promote the tool.
- **Re-verify every rule live before posting** — current per-subreddit rule text could not be machine-confirmed this session.

**Sources:** [r/AskDocs verified-clinician model (PMC7386284)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7386284/) · [Reddit general self-promotion / 90-10 rule overview (Conbersa)](https://www.conbersa.ai/learn/reddit-self-promotion-rules) · [Reddit promotions policy (Reddit Help)](https://support.reddithelp.com/hc/en-us/articles/22755369815700-Running-promotions-on-Reddit). Per-subreddit rule text could not be machine-verified (Reddit pages gated; search returned generic SEO content) — all per-sub rules above are marked *(verify current rule)* and must be confirmed live in each sub's sidebar/wiki before posting.

---

## Physician-verified networks

# Physician-Verified Networks — Clinician Outreach Plan

**Scope:** Doximity, Sermo, Student Doctor Network (SDN), Figure 1, Medscape Consult.

**Posting model for all venues:** manual posting only, by the real OpenOnco maintainer, identifying themselves by name as the maintainer/creator (or by a verified clinician contributor posting in their own name). No automation, no scheduled posting, no sockpuppets, no third-person "I found this cool tool" framing. One genuine post per community, spaced out over time, never the same text mass-posted across venues.

**Critical cross-cutting reality — verification is the gate:** Four of these five platforms are *license-gated*. Doximity, Sermo, Figure 1, and Medscape Consult require credential/license verification (medical ID or professional license upload) before you can post. **If the OpenOnco maintainer is not a verified, licensed clinician (or does not have a verified clinician co-signing the post in their own name), you cannot legitimately post on those four — full stop.** Do not create a verified account by misrepresenting credentials; that is fraud and violates each platform's terms. Where the maintainer is not a clinician, the only honest paths are: (a) recruit a verified clinician contributor/advisor willing to post in their own name with disclosure, or (b) skip the venue.

**Before posting anywhere below — confirm the current rule in writing.** Self-promotion rules on medical platforms change and are often unwritten. For every venue marked "conditional," get explicit confirmation from a moderator / the community team / support that **maintainer-disclosed, non-commercial, open-source tool feedback is permitted in the specific surface you intend to use**, and keep that confirmation. If you cannot get a clear yes, do not post — participate genuinely instead.

**Standard medical-safety footer** (paste verbatim into every post that is permitted; numbers are state 2026-06-17):

> Safety note: OpenOnco is an informational clinical decision-support project, NOT a medical device. It is not FDA-cleared, not clinically validated, and not for patient self-use (HCP-only). It is early-stage (v0.1): most knowledge-base entries are STUBS labeled "proposed, not approved," and only 15 of 806 clinical entities currently have two-reviewer clinical sign-off. No LLM picks the regimen or dose. Any output is a draft that must be independently verified by a qualified oncologist.

---

## 1. Doximity

**(a) Self-promo rule + whether/how to post**
Doximity's Terms prohibit transmitting advertising or promotional material **without Doximity's prior written consent**. There is no open "share your tool" forum analogous to a subreddit. The member-facing channels are (i) the **clinician feed / colleague network**, (ii) **Op-Med**, Doximity's first-person essay program, and (iii) **specialty groups/discussions**.

- Op-Med **explicitly rejects** submissions that "are advertisements or promotional," are "written for a patient audience," or are "drafted… by AI." A "try my tool" essay is therefore out, and so is anything an AI wrote. If Op-Med is pursued at all, the only honest version is a genuine **topical** essay the author writes themselves (e.g., on what deterministic, source-cited decision support could look like at tumor board), in which the author **openly discloses** they build OpenOnco — not a piece engineered to smuggle a plug past editors. Treat acceptance as uncertain and editor-gated, and accept rejection gracefully.
- For direct tool-sharing, the compliant route is to **request written consent from Doximity first**, or to share only within a relevant specialty group **after a group moderator/admin confirms in writing that non-commercial open-source tool feedback is permitted.**

**(b) Verification barrier**
High. Doximity verifies identity and credentials on registration (identity-verification questions and/or upload of professional license/medical ID); only verified members get the full feature set. **Posting requires a verified clinician account — do not fake one.**

**(c) Ready disclosed post template** — *use only inside a relevant oncology/heme-onc group after a moderator confirms non-commercial tool feedback is allowed, or via a consent-approved channel:*

> Hi all — I'm the maintainer of OpenOnco, a free, open-source (MIT code / CC BY 4.0 content) clinical-decision-support project for oncology tumor boards. I'm sharing it here for **clinical critique, not promotion** — and only after confirming with the group's moderators that this is acceptable.
>
> What it does: a deterministic rule engine reads a versioned, source-cited knowledge base and drafts two alternative plans (standard + aggressive) for a clinician to verify. No LLM picks the regimen or dose; every recommendation is cited. (An MCP server also lets tools like ChatGPT/Claude/Cursor call the engine.) It's **early-stage (v0.1)**: current scale is 92 diseases, 664 indications, 384 regimens, 444 cited sources (state 2026-06-17), but **most entries are STUBS ("proposed, not approved") and only 15 of 806 entities have two-reviewer sign-off — no formal clinical validation yet.**
>
> My ask: **tear apart the clinical logic.** Where is the reasoning wrong, where are citations weak or mis-mapped, what's missing for real tumor-board use? Demo: https://openonco.info/try.html · Repo: https://github.com/romeo111/OpenOnco
>
> [STANDARD MEDICAL-SAFETY FOOTER]

**(d) Compliance/etiquette notes**
Get the consent/moderator OK *in writing first* — Doximity's promo restriction is the strict kind. Post in your own verified name. Do not cold-DM members (DM solicitation risks a ban). One post, in the single most relevant group. If Op-Med is pursued, write a genuine topical essay yourself, disclose authorship, and accept that editors may decline anything that reads as promotion.

---

## 2. Sermo

**(a) Self-promo rule + whether/how to post**
Sermo is a verified, partly-anonymous physician social network with peer-consult and "crowdsourcing" features. Its Code of Conduct centers on no plagiarism/duplicated content and prohibits monetized/duplicated promotional posts (those "will result in suspension or permanent removal"). It does **not** publish a clear, public "you may share your own open-source tool" allowance. Sermo's promotional/earning surfaces are sponsor-paid (surveys), a different, commercial track that is **not** appropriate here.

- The only defensible route is a **genuine clinical discussion / peer-consult post** in the relevant oncology space, where you disclose you built a free tool and ask for critique — **and only after confirming in writing with Sermo support / the community team that maintainer-disclosed, non-commercial tool feedback is allowed in member discussions.** Sermo's public Code of Conduct does not settle this, and unsanctioned promo risks permanent removal. **If support does not give a clear yes, do not post.**

**(b) Verification barrier**
High. Sermo requires a photo ID at registration plus upload of medical license and a workplace badge, verified by human + automated review. **Posting requires a verified licensed physician account — do not misrepresent credentials.**

**(c) Ready disclosed post template** — *only after Sermo confirms it's permitted; otherwise do not post:*

> Disclosure: I'm the maintainer of OpenOnco, a free, open-source oncology decision-support project. I'm posting for **peer critique of the clinical logic, not to sell anything** (it's free; MIT/CC BY 4.0), and after checking that maintainer-disclosed tool feedback is allowed here.
>
> The design deliberately keeps the LLM out of clinical reasoning: a deterministic rule engine over a versioned, source-cited knowledge base drafts two plans (standard + aggressive) for a clinician to verify; every recommendation is cited. It's early-stage (v0.1) — most entries are STUBS ("proposed, not approved"), only 15/806 entities have two-reviewer sign-off, and there's no formal clinical validation yet. (For scale, state 2026-06-17: 92 diseases, 664 indications, 444 cited sources.)
>
> I'd value brutally honest oncologist feedback: where does the reasoning break, which citations look wrong, what would you never trust at tumor board? https://openonco.info · https://github.com/romeo111/OpenOnco
>
> [STANDARD MEDICAL-SAFETY FOOTER]

**(d) Compliance/etiquette notes**
Do not duplicate this text across multiple Sermo threads (duplicated content is explicitly sanctionable). Single post. Lead with disclosure and the "it's free, I want criticism" framing. If support says no, **do not post** — participate genuinely in oncology discussions instead, and let the project come up only if someone asks.

---

## 3. Student Doctor Network (SDN)

**(a) Self-promo rule + whether/how to post**
SDN is a nonprofit that explicitly **does not promote commercial services** and states **"Commercial use of SDN's Forums is strictly prohibited."** Advertising by verified members is funneled into designated forums only ("Student Classifieds" for verified members; "Test Prep"/"Advising Services" for verified vendors). Private-message solicitation is banned. The audience is also predominantly **students and trainees**, not practicing oncologists — a poor fit for tumor-board clinical critique.

- OpenOnco is free and non-commercial, which is closer to SDN's spirit, but a "check out the tool I built" post in a general forum still reads as self-promotion and risks moderator removal/ban (the forums are actively moderated against spam). **Recommendation: do NOT do a promotional post on SDN.** If you engage at all, do it genuinely — answer questions in relevant threads, and mention the project only if directly on-topic **and only after a moderator confirms in writing it's allowed.**

**(b) Verification barrier**
Lower than the clinician networks (registration is open to students/pre-health), but "verified member" status governs where you may post links/ads. Note SDN's content is CC BY-NC-SA 4.0 and it prohibits reposting SDN content to ad-bearing pages.

**(c) Ready disclosed post template**
**None recommended — SDN is not an appropriate self-promo venue.** If, and only if, a moderator explicitly green-lights a single disclosed mention in an on-topic thread, use a stripped-down disclosure:

> (Posting with mod permission.) Disclosure: I maintain OpenOnco, a free, open-source oncology decision-support project (MIT/CC BY 4.0). It's early-stage (v0.1), mostly STUB content, and not clinically validated. Sharing only because it's directly relevant to this thread — feedback welcome, no sign-up, nothing for sale. [link] [STANDARD MEDICAL-SAFETY FOOTER]

**(d) Compliance/etiquette notes**
Never PM-solicit. Never post the tool in general forums without explicit moderator permission. Given the trainee audience and the strict no-commercial-promo posture, the highest-value move here is **genuine participation only** — flag this venue as **NOT for promotion.**

---

## 4. Figure 1

**(a) Self-promo rule + whether/how to post**
Figure 1 is a verified case-sharing network for HCPs. Its Community Guidelines ask users to be professional, post only cases from direct clinical experience, **refrain from sharing promotional content**, and support posts with scientific data. There is **no designated tool-promotion venue**; the platform is built around de-identified patient *cases*, not software show-and-tell.

- A "here's my tool" post conflicts directly with the "refrain from promotional content" guideline. **Recommendation: do NOT post a promotional/tool post on Figure 1.** It is also a poor structural fit — the content model is clinical images/cases, not project feedback. The only conceivably compliant use is genuine clinical participation; assume promotion is disallowed unless Figure 1 states otherwise.

**(b) Verification barrier**
High to *post*. Figure 1 grants "Verified" status only to licensed healthcare professionals/students after internal vetting; posting cases requires verification, and all posts are moderated/de-identified by a clinical team. **Posting requires a verified HCP account.**

**(c) Ready disclosed post template**
**None — promotion is not permitted here. Do not post a tool/promo entry.**

**(d) Compliance/etiquette notes**
Treat Figure 1 as **NOT for promotion.** Never attach a patient case to a tool pitch — combining promo with patient imagery is doubly inappropriate and risks PHI / de-identification problems on top of the promo ban. If the maintainer is a verified clinician, the only appropriate activity is normal, genuine case participation.

---

## 5. Medscape Consult

**(a) Self-promo rule + whether/how to post**
Medscape Consult is Medscape's in-app physician Q&A / clinical-discussion community (physicians ask and answer clinical questions and discuss cases). **Status caveat: Medscape's 2025–2026 push is heavily toward "Medscape AI," and current public sources do not confirm whether Consult remains an actively maintained, postable community feature versus being de-emphasized. Verify the current status and rules directly in the app / Medscape Help Center before planning a post.**

- Medscape does not publish an open "promote your tool" allowance for Consult; the surface is for clinical questions and case discussion, governed by Medscape's general terms (no spam/advertising without authorization). The only defensible route is a **genuine clinical question/discussion** where the tool is mentioned with disclosure, **and only if** Medscape support / community rules confirm in writing that maintainer-disclosed, non-commercial tool feedback is permitted. Do not assume promotion is allowed.

**(b) Verification barrier**
High. Consult is restricted to verified physicians/HCPs within the Medscape network. **Posting requires a verified clinician account.**

**(c) Ready disclosed post template** — *only if Medscape confirms Consult is active and permits maintainer-disclosed, non-commercial tool feedback; otherwise do not post:*

> Disclosure: I'm the maintainer of OpenOnco, a free, open-source oncology decision-support project (MIT/CC BY 4.0). I'm posting to ask oncology colleagues for critique of the clinical logic — it's free and I'm not selling anything.
>
> Design: a deterministic rule engine over a versioned, source-cited knowledge base drafts two plans (standard + aggressive) for a clinician to verify; no LLM selects regimen or dose; every recommendation is cited. It's early-stage (v0.1) — mostly STUB content ("proposed, not approved"), 15/806 entities with two-reviewer sign-off, no formal clinical validation. (Scale, state 2026-06-17: 92 diseases, 664 indications, 444 cited sources.)
>
> Where is the reasoning wrong, and what would block you from trusting it at tumor board? https://openonco.info · https://github.com/romeo111/OpenOnco
>
> [STANDARD MEDICAL-SAFETY FOOTER]

**(d) Compliance/etiquette notes**
Confirm Consult is still live and that maintainer-disclosed tool feedback is allowed before posting. Frame as a clinical-discussion/feedback ask, not advertising. One post. Post in your own verified clinician name.

---

## Summary table

| Venue | Promo allowed? | How to post (if at all) | Verification barrier | Template provided? |
|---|---|---|---|---|
| **Doximity** | Restricted — written consent or group-mod OK required; Op-Med rejects promo + AI-drafted text | In-group feedback post after written mod/consent OK; genuine self-written Op-Med essay with disclosure | High — verified clinician | Yes (conditional) |
| **Sermo** | Unclear/restricted — confirm with support in writing; duplicated/monetized promo banned | Disclosed peer-critique post *only if* support confirms | High — verified physician (ID + license + badge) | Yes (conditional) |
| **SDN** | **No** — commercial use strictly prohibited; trainee audience | Genuine participation only; tool mention only with explicit written mod permission | Open reg; "verified" governs ad forums | Minimal, mod-permission-only |
| **Figure 1** | **No** — guidelines say refrain from promotional content | Do NOT post promo; case-only platform | High — verified HCP to post | No (disallowed) |
| **Medscape Consult** | Unclear — verify status & rules first | Disclosed clinical-discussion ask *only if* permitted and Consult is still active | High — verified clinician | Yes (conditional) |

## Top-line recommendations
1. **Do NOT post promotionally on SDN or Figure 1.** Their rules disallow it (SDN: commercial use strictly prohibited; Figure 1: refrain from promotional content). Engage genuinely only.
2. **Doximity, Sermo, Medscape Consult are conditional** — all require (a) a verified clinician account and (b) explicit, in-writing confirmation that maintainer-disclosed, non-commercial tool feedback is permitted in the chosen surface. Get that confirmation before posting; if you can't, don't post.
3. **Verification is the gating constraint.** If the OpenOnco maintainer is not a licensed, verified clinician, the honest options are: recruit a verified clinician contributor to post in their own name with disclosure, or skip these four license-gated venues. **Never falsify credentials to obtain verification — that is fraud.**
4. **No spam cadence.** One genuine post per community, spaced out. Never mass-post identical text; duplicated content is explicitly sanctionable on Sermo and reads as spam everywhere.
5. **Every permitted post carries the standard medical-safety footer**, leads with maintainer disclosure, frames the ask as "critique the clinical logic" (not "sign up"), and states the early-stage/STUB reality next to any scale number.
6. **Items to verify before acting** (do not guess): current Sermo stance on maintainer tool-sharing in discussions; whether Medscape Consult is still an active, postable feature in 2026; and current SDN / Figure 1 / Doximity guideline text, which may change.

## Sources
- [Doximity Terms of Service](https://www.doximity.com/terms-of-service) · [Doximity Community Guidelines](https://www.doximity.com/clinicians/community/guidelines) · [Op-Med Submission Guidelines and FAQ](https://opmed.doximity.com/articles/submission-guidelines-and-faq) · [Op-Med Guidelines](https://opmed.doximity.com/articles/guidelines)
- [Sermo Code of Conduct](https://www.sermo.com/conduct/) · [Sermo: How to register](https://support.sermo.com/hc/en-us/articles/15490722648987-How-to-register) · [Is Sermo legit?](https://www.sermo.com/blog/insights/is-sermo-legit/)
- [SDN Community Vision, Values, and Policies](https://www.studentdoctor.net/online-service-agreement/) · [SDN Advertisements policy](https://forums.studentdoctor.net/help/advertisements-on-sdn/) · [How We Moderate the SDN Forums](https://www.studentdoctor.net/about-sdn/how-we-moderate/) · [About The Student Doctor Network](https://www.studentdoctor.net/about-sdn/)
- [Figure 1 Terms of Use](https://figure1.com/sections/tos/) · [Figure 1 (Wikipedia — verification & guidelines summary)](https://en.wikipedia.org/wiki/Figure_1) · [Figure 1 — Medical Collaboration on Real Patient Cases](https://www.figure1.com/)
- [Medscape Help Center](https://help.medscape.com/hc/en-us) · [Medscape point-of-care app (Consult reference)](https://www.medscape.com/public/medscapeapp) · [Medscape AI (current direction)](https://help.medscape.com/hc/en-us/articles/41820309020685-What-is-Medscape-AI)

---

*Verified against OpenOnco's own canonical facts (`promo/00-FACT-SHEET.md`, `promo/disclaimer-checklist.md`): scale figures 92 diseases / 664 indications / 384 regimens / 444 sources (state 2026-06-17) and the 15/806 dual-sign-off ratio are accurate as written; the standard footer satisfies the project's pre-publish safety gate.*

---

## Professional society / oncology forums

# Clinician Outreach: Professional Societies & Oncology Forums

**Audience:** practicing oncologists/hematologists, KOLs, tumor-board members — a credentialed, skeptical, conflict-of-interest-literate audience. They respond to evidence, transparency about limitations, and a genuine "critique my clinical logic" ask. They reject anything that reads as a vendor pitch.

**Cross-cutting reality:** Most society communities are **member-only and self-promotion-restricted by default.** None of these are growth channels. Treat them as places to get expert critique from one or two threads, not to "launch." Every named venue below either restricts promo, requires staff/mod approval, or has no open forum at all. Where promo is disallowed — or where you cannot confirm it is allowed — the recommendation is **do not post promotional content; participate genuinely instead.**

**Note on policy drift:** Community rules change. Even where a rule is quoted below as confirmed, **re-read the venue's current guidelines/terms page at the moment you post** — do not rely on a possibly-stale quote.

**Two non-negotiable framing rules for KOL audiences specifically:**
1. Lead with what's *wrong/unproven* (STUB content, 15/806 entities signed off, no clinical validation), not what's impressive. This audience trusts people who disclose limitations first.
2. Disclose your role in the **first sentence**, always. Astroturfing a physician community is both an ethics violation and, on verified networks, a credentialing-fraud risk.

---

## 1. ASCO — myConnection / Communities of Practice

**(a) Self-promo rule + whether/how to post**
ASCO's myConnection [Community Rules and Guidelines](https://myconnection.asco.org/community-rules-and-guidelines) **restrict self-promotion.** Confirmed rules (re-verify at posting time): members should *"share your experience with the group in a respectful way"* rather than promote *"products or services that you provide"*; *"no solicitations, promotions, or advertisements for conferences outside of ASCO"*; and **surveys/research/data-collection requests "may not be posted without prior approval from ASCO staff."** The [Terms of Use](https://www.asco.org/about-asco/legal/terms-use) separately prohibit advertising/promotional material and spam.

**How to post appropriately:** This is borderline. A free, non-commercial, open-source tool is not a "product or service you sell," but soliciting feedback on a tool you built is close enough to the restricted zone that you should **email ASCO community staff first and ask permission**, framing it as a peer-knowledge-sharing / feedback request, not a launch. **If they decline, or if you do not get explicit approval → do not post.** If a relevant Community of Practice (e.g., an informatics, AI, or specific tumor-type CoP) exists, that is the only appropriate home — never broadcast to multiple communities (the rules tell you to post to the single most appropriate community).

**(b) Verification barrier**
ASCO membership required (physician/associate tiers exist). You must post under your real ASCO member identity. **Do not post unless you are an ASCO member maintaining/contributing to OpenOnco.**

**(c) Ready disclosed post template** *(use only after written ASCO staff approval)*

> **Subject:** Feedback request from a maintainer — open-source rule-engine that drafts tumor-board treatment options (early-stage, not validated)
>
> I'm [Name], the maintainer of OpenOnco, a free, open-source clinical-decision-support project (posting in my own capacity; I have ASCO staff approval to share this here for feedback). I want to be upfront: this is **early-stage (v0.1), not a medical device, not FDA-cleared, and not clinically validated.** It is informational support only — every output must be verified by a qualified oncologist, and it is **not for patient self-use.**
>
> What it is: a **deterministic rule engine** over a versioned, source-cited knowledge base that drafts two alternative plans (standard + aggressive) for a clinician to verify. Deliberately, **no LLM picks the regimen or dose** — the LLM only drafts prose; every recommendation carries a citation. Current scale: 92 diseases, 664 indications, 384 regimens, 444 cited sources.
>
> The honest caveat: most content is **STUB ("proposed, not approved") — only 15 of ~806 entities have two-reviewer sign-off**, and there's no formal validation yet.
>
> My ask is not adoption — it's critique. **Where is the clinical logic wrong?** Pick any disease you treat and tell me what's missing, mis-cited, or unsafe. Repo + demo for anyone willing to tear it apart: https://github.com/romeo111/OpenOnco · https://openonco.info/try.html
>
> Code is MIT, content CC BY 4.0. Happy to take criticism in the open.

**(d) Compliance/etiquette notes**
- Get written staff approval; keep the email. One post, one community.
- Respond to every reply substantively; do not re-post when the thread dies.
- Note ASCO's own [COI/disclosure culture](https://www.asco.org/about-asco/legal/terms-use) — declaring "no commercial interest, free/non-commercial project" preempts the obvious suspicion.
- Do **not** cross-post the same text to other communities or to ASCO Connection blogs.

---

## 2. ASH — ASH Connections (hematology)

**(a) Self-promo rule + whether/how to post**
[ASH Connections](https://ashconnections.hematology.org/) is ASH's free networking/education community built *"to tackle real-world cases, exchange insights, and access curated resources"* (it replaced the sunset Consult-a-Colleague program). It is a **case-discussion and peer community**, which is a good substantive fit for a hem-onc decision-support tool. **However, I could not retrieve ASH Connections' specific community/code-of-conduct or self-promotion policy** — *verify the current rule directly on the platform's guidelines/terms page before posting.* **Fail-safe default: treat promo as restricted, and if you cannot confirm the rule allows a feedback post, do NOT post — participate in case threads genuinely instead, and contact ASH staff if in doubt.**

**How to post appropriately:** If, after confirming the rules, the platform has a relevant community (e.g., an informatics/AI or a specific malignancy group), the right move is to **participate in actual case discussions first**, then share the tool only where directly relevant to a discussion, framed as "I built this, here's the hematology coverage, tell me what's wrong." Do not open a thread whose sole purpose is promotion unless you have confirmed the rules allow it.

**(b) Verification barrier**
ASH Connections is open to ASH members and the broader hematology community (fellows, APPs, pharmacists, nurses). Post under your real identity and role. If you are not a hematology professional, contribute only by clearly identifying as the (non-clinician) maintainer seeking clinical critique — do not imply clinical authority.

**(c) Ready disclosed post template** *(use only after confirming platform rules permit a feedback post)*

> **Title:** Open-source hem-onc decision-support engine — maintainer asking the community to find the flaws (early-stage, unvalidated)
>
> Hi all — I'm [Name], maintainer of OpenOnco (sharing as the project's creator, not as a vendor; this is a free, open-source, non-commercial project). Straight up: **v0.1, not a medical device, not FDA-cleared, not clinically validated, informational only, and not for patient self-use — verify everything with a qualified hematologist/oncologist.**
>
> It's a **deterministic rule engine** over a source-cited, versioned knowledge base that drafts two alternative treatment plans (standard + aggressive) for a clinician to check. By design, **no LLM chooses regimen or dose**; every recommendation is cited. Heme content is part of the current 92 diseases / 664 indications / 384 regimens / 444 sources — but most of it is **STUB ("proposed, not approved"), with only 15 entities two-reviewer-approved so far.**
>
> I'm not asking you to use it on patients. I'm asking hematologists to **break the clinical logic** — wrong sequencing, missing risk stratification, stale citations, anything unsafe. Repo: https://github.com/romeo111/OpenOnco · demo: https://openonco.info/try.html (MIT code, CC BY 4.0 content).

**(d) Compliance/etiquette notes**
- Confirm the ASH Connections terms/conduct policy *before* posting; **if it bans promo, or if you cannot confirm, don't post** — engage in case threads genuinely instead.
- One post in the single most relevant community; no cross-posting.
- Because this is a case-discussion venue, the strongest credibility move is to first contribute clinically useful comments on others' cases.

---

## 3. ESMO — OncologyPRO / member communities

**(a) Self-promo rule + whether/how to post**
ESMO does **not appear to run an open member discussion forum.** [OncologyPRO](https://oncologypro.esmo.org/) is an educational/scientific *resource library* (guidelines, webinars, congress content), and member-to-member connection is via the [Membership Directory](https://www.esmo.org/my-esmo/membership-directory) plus webinars, committees, and working groups — not a posting board. There is no public "share your tool" thread to use.

**Recommendation: do NOT attempt a promotional post on ESMO channels** — there is no appropriate venue for it, and pushing the tool through the directory (direct-messaging members) or congress Q&A would be inappropriate. *Verify the current rule,* but the right path here is **participation, not posting:**
- Join/contribute to a relevant ESMO **working group or committee** where digital tools / guidelines methodology are in scope, and raise the project there in context.
- Engage genuinely in webinar Q&A on decision-support topics without pitching.
- If ESMO later opens a community forum, re-evaluate against its rules.

**(b) Verification barrier**
ESMO membership; the directory and member resources are members-only. KOL-heavy, European, guideline-centric audience — extremely sensitive to anything resembling commercial influence near guideline work. Disclosure of non-commercial status is essential.

**(c) Ready "message" template** — *adapted as a working-group / committee context message, NOT a forum broadcast and NOT a directory mass-message:*

> I'm [Name], maintainer of OpenOnco, a free, open-source, non-commercial decision-support project. I'm raising it here only because it's directly relevant to [this working group's topic], and I'd value methodological critique — not promotion.
>
> It's a **deterministic, source-cited rule engine** (two plans, standard + aggressive, for a clinician to verify; **no LLM selects regimen/dose**; every recommendation cited). Full disclosure of maturity: **v0.1, STUB content, only 15/806 entities two-reviewer-approved, no formal clinical validation, not a medical device, not FDA-cleared.** It is informational support only, **not for patient self-use, and every output must be verified by a qualified oncologist.** I'd specifically welcome critique of how the engine maps to ESMO Clinical Practice Guidelines and where the citation logic is weak. Repo: https://github.com/romeo111/OpenOnco.

**(d) Compliance/etiquette notes**
- Do not mass-message members via the directory — that is the clearest astroturfing/spam failure mode here.
- Keep it methodological and guideline-anchored; never position the tool as competing with or replacing ESMO guidelines.
- If you have no working-group role, the honest answer is: you don't yet have an appropriate ESMO venue — earn one through participation.

---

## 4. Regional oncology societies

(e.g., national/regional societies — Ukrainian, EU national societies, state oncology societies, etc.)

**(a) Self-promo rule + whether/how to post**
Rules vary enormously and are usually **not published online** — *verify each society's rule individually* (member handbook, listserv/forum terms, or by emailing the secretariat). Default assumption: **promo is restricted; ask the secretariat first.** Smaller regional societies are often *more* receptive than the big international ones because they have fewer members and value practical free tools — but they also have less formal infrastructure, so a polite email to a society officer is usually the correct first step rather than posting cold.

**How to post appropriately:** Email the society's secretariat/education officer, disclose your role, ask whether there's an appropriate channel (newsletter "member projects" item, listserv, regional tumor-board working group). Let *them* place it. This also naturally surfaces any physician-verification requirement.

**(b) Verification barrier**
Varies; often membership-gated and sometimes nationality/region-gated. Many regional societies are clinician-only — if you're not a member-clinician, route through a member contributor or the secretariat and identify clearly as the (non-clinician) maintainer.

**(c) Ready disclosed outreach email template**

> **Subject:** Open-source oncology decision-support tool — request for member feedback (free, non-commercial, early-stage)
>
> Dear [Society] Secretariat,
>
> I'm [Name], maintainer of OpenOnco, a free, open-source, non-commercial clinical-decision-support project for oncology tumor boards. I'm writing to ask whether your society has an appropriate channel through which members might give **critical feedback** on it — I'm not seeking promotion or endorsement.
>
> Briefly: it's a **deterministic, source-cited rule engine** that drafts two alternative plans (standard + aggressive) for a clinician to verify; **no LLM picks the regimen or dose**, and every recommendation is cited. I want to be transparent that it is **early-stage (v0.1), not a medical device, not FDA-cleared, not validated, and mostly STUB content** (only 15 of ~806 entities have two-reviewer sign-off). It is informational support only and **not for patient self-use** — every output must be verified by a qualified oncologist.
>
> If there's a member project listing, a newsletter item, a working group, or a regional tumor-board forum where clinicians could **point out what's clinically wrong**, I'd be grateful for your guidance — and I'll fully respect your society's self-promotion and disclosure rules. Repo: https://github.com/romeo111/OpenOnco · demo: https://openonco.info/try.html (MIT / CC BY 4.0).
>
> Thank you, [Name]

**(d) Compliance/etiquette notes**
- One email per society; let the society decide the channel. Don't post to their listserv/forum unprompted.
- **Reach out to one society at a time and wait for a response before contacting the next** — do not blast a dozen societies the same week, and never send identical text in bulk.
- For Ukrainian / non-English societies, send in the society's working language and have any clinical wording reviewed (consistent with the project's clinical-review norms).

---

## 5. Tumor-board / hem-onc working groups (incl. verified physician networks)

This bucket = topical working groups (often inside the societies above) plus **verified-clinician networks** like [Sermo](https://www.sermo.com/) and Doximity that host virtual tumor boards and oncology communities.

**(a) Self-promo rule + whether/how to post**
- **Society working groups:** treat as §1–§4 — ask the group chair/staff; promo restricted by default.
- **Verified networks (Sermo/Doximity):** these are **credential-gated** and generally **restrict overt product promotion** to designated areas/partnerships. *Verify each platform's current self-promotion policy before posting.* **If you cannot confirm the policy permits it, do NOT post.** If allowed, the relevant oncology community or a virtual-tumor-board discussion is the right place — and only if you are a verified clinician on the platform.

**(b) Verification barrier — highest here.**
Sermo and Doximity **verify medical credentials**; only licensed, verified professionals get access. **Posting requires the poster to be a verified clinician.** **Absolute rule: if the maintainer is not a verified physician, do NOT create an account, do NOT borrow or use anyone else's account, and do NOT post by proxy under a false identity — that is credentialing fraud and astroturfing.** Instead, recruit a clinician *contributor* who is a verified member to share it in their own name, with their own disclosure that they're an OpenOnco contributor.

**(c) Ready disclosed post template** *(for a genuinely verified-clinician contributor posting in their own name, in an oncology community / virtual-tumor-board thread where rules permit)*

> I'm a verified [oncologist/hematologist] and a contributor to OpenOnco, a free, open-source, non-commercial decision-support project — flagging my involvement so this isn't mistaken for a neutral recommendation.
>
> It's a **deterministic, source-cited rule engine** that drafts two plans (standard + aggressive) for a clinician to verify; **no LLM selects regimen or dose**, everything is cited. Honestly: **early-stage v0.1, mostly STUB content (15/806 entities two-reviewer-approved), not a medical device, not FDA-cleared, not validated** — informational only, **not for patient self-use,** verify with a qualified oncologist.
>
> For those of us who run tumor boards: I'd value brutal critique of the clinical logic and citations on diseases you treat. Repo: https://github.com/romeo111/OpenOnco · demo: https://openonco.info/try.html.

**(d) Compliance/etiquette notes**
- Verified networks are the **one place where the poster's clinician status is mandatory** — never post as a non-clinician, never use a borrowed or shared account, never post by proxy.
- Honor each platform's promo policy; if it routes product mentions to a paid/partnership lane, do not bypass that with an organic-looking post.
- Working groups inside societies: defer to the chair; one post, value-first, follow up on replies.

---

## Quick reference

| Venue | Open forum exists? | Promo rule | Post? | Verification |
|---|---|---|---|---|
| **ASCO myConnection** | Yes (CoP) | Self-promo restricted; staff approval for solicitations | Only after written ASCO staff approval, in the single relevant CoP | ASCO member |
| **ASH Connections** | Yes (case community) | *Verify current rule;* assume restricted | Only after confirming rules allow it; otherwise don't post — join case threads genuinely | ASH member / heme professional |
| **ESMO OncologyPRO** | **No open forum** | No appropriate promo venue | **Do not promo-post;** engage via working groups/webinars | ESMO member |
| **Regional societies** | Varies (often none) | *Verify each;* assume restricted | Email secretariat first, one at a time, let them place it | Varies; often clinician-only |
| **Tumor-board / verified networks** | Yes (Sermo/Doximity) | Restricted; *verify;* designated lanes | Only via a **verified-clinician contributor** in their own name, where rules permit | **Mandatory credential verification** |

**Universal rules applied to every template above:** maintainer/contributor self-identifies in sentence one (no astroturfing, no sockpuppets, no borrowed/proxy accounts); manual posting by the real person only — never automated; medical-safety disclaimer (not a device, not FDA-cleared, not validated, not for patient self-use, verify with an oncologist) in every public message; honest STUB / 15-of-806 / no-validation disclosure; the ask is "tell me what's clinically wrong," never "sign up"; one genuine post per community, spaced out, no identical mass cross-posting; re-confirm each venue's current rule at posting time; and where a venue forbids promo (ESMO, and any society/network that says no — or where the rule cannot be confirmed), the recommendation is explicitly **do not post — participate genuinely instead.**

**Sources:**
- [ASCO myConnection Community Rules and Guidelines](https://myconnection.asco.org/community-rules-and-guidelines)
- [ASCO Terms of Use](https://www.asco.org/about-asco/legal/terms-use)
- [ASCO myConnection & Communities of Practice](https://www.asco.org/get-involved/membership/myconnection-communities-practice)
- [ASH Connections](https://ashconnections.hematology.org/)
- [ASH Consult-a-Colleague sunset notice](https://www.hematology.org/education/clinicians/consult-a-colleague)
- [ESMO OncologyPRO](https://oncologypro.esmo.org/)
- [ESMO Membership Directory](https://www.esmo.org/my-esmo/membership-directory)
- [ESMO Member Benefits](https://www.esmo.org/membership/member-benefits)
- [Sermo (verified physician network)](https://www.sermo.com/)
- [ACCC Tumor Boards](https://www.accc-cancer.org/home/learn/management-operations/tumor-boards)

*Note on uncertainty:* ASH Connections' and the verified networks' exact self-promotion policies could not be retrieved from public pages and are flagged "verify the current rule" rather than guessed; the fail-safe is to not post until the rule is confirmed. ESMO confirmed as having no open member forum — promotional posting there is not recommended. All venue rules, including those quoted as confirmed, should be re-checked at the time of posting, as policies change.

---

## MedTwitter/X + LinkedIn

# Clinician Outreach — MedTwitter/X + LinkedIn (+ Bluesky)

**Scope:** Disclosed, manual, value-first outreach to oncology/hemonc/pathology clinicians on X/Twitter, LinkedIn, and Bluesky. These venues have *light* disclosure norms — open self-identification as the maintainer is the expected, normal behavior here (unlike Reddit/forums). The bar to clear is the **spam/inauthenticity** bar, not the disclosure bar. Every post still carries the medical-safety framing and the honest "early-stage / mostly STUB" disclosure.

> **Hard ground rules for this entire section (non-negotiable):**
> - **Manual posting only**, from your own single real account, by you (the real maintainer) or a disclosed contributor. **No automation, no scheduling tools for engagement, no second/sockpuppet accounts, no coordinated posting.** X's 2026 enforcement suspends ~208 automation/spam accounts per minute and ran mass ban waves in April 2026 — automated or coordinated behavior is the fastest way to get suspended.
> - **No astroturfing.** Never post as a neutral third party who "found a cool tool." You always identify as the maintainer/contributor.
> - **The ask is critique, not signups.**

> **One disclosure block to reuse in every post below** (trim to fit character limits):
> *"I'm the maintainer of OpenOnco, a free, open-source tumor-board decision-support project. It's early-stage (v0.1) — most content is proposed/unverified STUB; only 15 of ~806 entities have two-reviewer sign-off, and there's no formal clinical validation yet. It's informational support for clinicians, NOT a medical device, not FDA-cleared, not for patient self-use — every plan must be verified by a qualified oncologist. I'm posting to get clinical critique, not signups."*

---

## IMPORTANT routing note before you post: most of #MedTwitter has moved

A large share of the clinical/scientific X audience migrated to **Bluesky** ("#MedSky") starting late 2024, and by 2025–2026 Bluesky had become a primary venue for new-research discussion; physician posts there reportedly see higher engagement per author, even though X still has more physician accounts overall ([STAT](https://www.statnews.com/2024/11/21/bluesky-gains-twitter-exodus-science-medical-community-finds-alternative-to-x/), [Science/AAAS](https://www.science.org/content/article/old-twitter-scientific-community-finds-new-home-bluesky), [arXiv migration study](https://arxiv.org/abs/2505.24801v1)). **Practical implication:** a similar disclosed thread can work on multiple platforms, but **do not post the identical text everywhere** — that trips spam heuristics and reads as broadcast. Write each platform's post natively. If you only have time for one, the higher-signal oncology audience for feedback is increasingly on Bluesky, with LinkedIn second and X third. Treat Bluesky as a recommended addition, not a replacement, and **verify the current state of each community before you commit time** — these populations are still shifting.

---

## 1. X / Twitter — #MedTwitter, #hemonc, #oncology

### (a) Self-promotion rule + whether/how to post
- **Open self-identification is normal and allowed on X.** There is no platform rule against saying "I built this." The hemonc-on-Twitter literature explicitly treats personal branding, sharing your work, and disease-community participation (e.g., #bcsm, #mpnsm) as legitimate ([PMC hemonc Twitter etiquette](https://pmc.ncbi.nlm.nih.gov/articles/PMC5994350/)).
- **The real constraint is X's Platform Manipulation & Spam policy and Authenticity rules** ([X rules index](https://help.x.com/en/rules-and-policies), [Authenticity](https://help.x.com/en/rules-and-policies/authenticity)). You may **not** post bulk/duplicative/unsolicited content, run sockpuppets/coordinated accounts, mass-mention KOLs, or use automation. 2026 enforcement is notably stricter, with ban waves for coordinated/automated behavior — **manual, single-account posting only.**
- **"Declare paid promotion" rule tightened March 2026** ([summary](https://www.panewslab.com/en/articles/019cadd6-9b25-7029-845f-652157fa471e)). This targets *paid* influencer promotion. OpenOnco is free/non-commercial and you are the unpaid maintainer, so the paid-promo disclosure tag does **not** apply — but it's another reason to be explicitly clear in-post that nobody is paying you.
- **Verdict: post — as a single disclosed thread from your own real account, once.**

### (b) Verification barrier
- **No physician-license verification required to post.** X is open. But to be *taken seriously* by clinicians, your bio should state who you are (maintainer/engineer/clinician-collaborator) honestly. **Do not imply you are a practicing oncologist if you are not.** If a clinician co-maintainer posts, they should disclose their own credentials and any conflicts in bio per hemonc norms.

### (c) Ready disclosed post template (thread)
> **1/** I'm the maintainer of OpenOnco — a free, open-source decision-support tool for oncology tumor boards. A deterministic rule engine drafts two treatment plans (standard + aggressive) over a versioned, source-cited KB. **No LLM picks the regimen or dose.** Every recommendation is cited. 🧵
>
> **2/** Honesty up front: it's **early-stage v0.1**. ~92 diseases / 664 indications / 384 regimens / 444 cited sources — but **most content is proposed STUB, not approved.** Only 15 of ~806 entities have two-reviewer sign-off. **No formal clinical validation yet.**
>
> **3/** What it is NOT: not a medical device, not FDA-cleared, not validated, not for patient self-use. It's informational support for clinicians — every plan must be verified by a qualified oncologist. Nobody pays me; this is non-commercial.
>
> **4/** The ask: **tear apart the clinical logic.** Where is a regimen wrong, a citation weak, a red-flag missing, an edge case mishandled? I want #hemonc / #oncology critique, not signups.
>
> **5/** Demo (no login): https://openonco.info/try.html · Code (MIT) + content (CC BY 4.0): https://github.com/romeo111/OpenOnco · Issues/critique welcome there or in replies. Thank you. 🙏

*(Use 1–2 hashtags per post, not a wall — see etiquette below.)*

### (d) Hashtags + KOL-engagement etiquette + compliance notes
- **Hashtags (use sparingly, 1–2 per tweet):** primary **#hemonc**, **#oncology**; add **#PathTwitter** only on a path-relevant tweet. **#MedTwitter** is fading; keep but don't lean on it.
- **Disease-community tags (#bcsm, #lcsm, #mpnsm, #gyncsm, #crcsm) — handle with care: these communities include patients, not just clinicians.** Only use them when you are *genuinely* participating in that conversation. **Do not broadcast a tool-promo thread into a patient community**, and **never imply patient self-use** there — the framing for those spaces must stay clinician-facing and sober. When in doubt, don't tag them.
- **KOL engagement — no spamming mentions.** This is the cardinal rule. **Do not** @-mention a list of oncology KOLs to "summon" them — it's the mass-mention pattern X penalizes and clinicians find off-putting. Instead: (1) **"lurk" first** — the hemonc literature explicitly advises observing before participating ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5994350/)); (2) engage *genuinely* on their existing posts (substantive replies on guideline/trial discussion) before ever mentioning your project; (3) only tag someone when it's directly relevant to *their* stated interest, one person, with a real reason. A single thoughtful reply > ten cold mentions.
- **Cadence:** one launch thread, then participate normally. Do not re-post the same thread weekly. Share genuine *updates* (e.g., "added X disease, here's the sourcing") at a natural pace, not on a drip schedule.
- **Conflict/disclosure:** put "Maintainer, OpenOnco (non-commercial, open-source)" in your bio per hemonc COI norms.
- **Patient privacy:** never use a real or composite patient in examples; use clearly synthetic profiles only ([PMC privacy guidance](https://pmc.ncbi.nlm.nih.gov/articles/PMC5994350/)).
- **#PathTwitter tone caution:** that community flags aestheticizing disease (e.g., calling cancer cells "beautiful") and careless emoji/adjective use about disease states ([Schukow et al. etiquette](https://pubmed.ncbi.nlm.nih.gov/37533372/)). Keep path-facing posts sober and clinical.

---

## 2. Bluesky — #MedSky / oncology starter packs (recommended addition)

### (a) Self-promotion rule + whether/how to post
- Same as X: **open self-identification is normal**, the audience is "old-Twitter"-style and often *more* receptive to substantive project posts. No paid-promo regime to worry about. **Verify the current community norms** as #MedSky is young and still forming.
- **Verdict: post — a fresh, natively written disclosed thread (not a copy of the X one).** This is likely your highest-signal feedback venue for oncology right now ([Science/AAAS](https://www.science.org/content/article/old-twitter-scientific-community-finds-new-home-bluesky)).

### (b) Verification barrier
- No license verification to post. Bluesky supports **domain-handle verification** — set your handle to your real domain if you have one, to signal authenticity. Don't claim clinician status you don't hold.

### (c) Ready disclosed post template
- **Write a genuinely new thread for Bluesky** — same facts and same disclosure block (maintainer identity, STUB/early-stage maturity, "not a medical device / verify with an oncologist," critique-not-signups ask), but **reworded in your own voice rather than pasted from X.** Identical cross-posting reads as a broadcast and undercuts the value-first tone. It's fine to note plainly: *"a lot of #hemonc has moved here, so I'm sharing this for critique on Bluesky too."*

### (d) Etiquette notes
- Find/join oncology + medicine **"starter packs"** and engage genuinely rather than mass-following. Same no-mass-mention rule. One disclosed post; then participate.
- Same patient-community caution as X: #MedSky includes patients — keep it clinician-facing, no implication of patient self-use, no real/composite patient data.

---

## 3. LinkedIn — feed posts + oncology / health-tech groups

### (a) Self-promotion rule + whether/how to post
- **Feed posts (your own profile): allowed and normal.** Open self-identification is the LinkedIn default. The constraints are LinkedIn's **Professional Community Policies**, which prohibit spam — "untargeted, irrelevant, obviously unwanted, unauthorized, inappropriately commercial or promotional, or gratuitously repetitive" content — and prohibit **inauthentic engagement** (no pre-arranged like/reshare pods, no coordinated near-identical posts) ([LinkedIn Professional Community Policies](https://www.linkedin.com/legal/professional-community-policies), [spam help](https://www.linkedin.com/help/linkedin/answer/a1344213/)).
- **2026 enforcement note:** LinkedIn now runs ML detection for "coordinated inauthentic thought leadership" — flagging multiple accounts posting suspiciously similar content ([algorithm/policy summary](https://www.auditsocials.com/blog/linkedin-algorithm-sponsored-content-policy-changes-april-2026)). **Implication:** one authentic post from you, in your own voice; **do not coordinate multiple accounts to echo it.** Authentic first-person expertise is also what the 2026 algorithm rewards.
- **Groups: rules are per-group and vary widely.** Most oncology/health-tech groups either **restrict promo to a designated thread/day, require it be discussion-framed, or ban link-drops outright**, often with active moderators. **Verify the current rule in each group's "About"/rules panel before posting**, and if a group forbids self-promotion, **do NOT post there — participate genuinely instead, or DM a moderator to ask.** Don't assume; rules differ group to group.
- **Verdict:** **Post to your own feed (yes).** **Groups: only after reading that group's rules** — comply with the designated-thread/permission mechanism, or skip.

### (b) Verification barrier
- No license verification required to post. LinkedIn offers free **identity verification** (badge) — turning it on raises trust. Your headline/about should state your real role ("Maintainer, OpenOnco — open-source oncology decision support"). Don't claim clinician status you don't hold; if a clinician contributor posts, they disclose their credentials.

### (c) Ready disclosed post template (feed)
> **I built a free, open-source decision-support tool for oncology tumor boards — and I want clinicians to tell me what's wrong with it.**
>
> OpenOnco uses a *deterministic, source-cited rule engine* to draft two alternative treatment plans (standard + aggressive) for a clinician to verify. **No LLM chooses the regimen or dose** — every recommendation is cited back to a source.
>
> Being upfront about maturity: it's **early-stage (v0.1).** ~92 diseases, 664 indications, 384 regimens, 444 cited sources — but **most content is proposed STUB, not yet approved.** Only 15 of ~806 entities have two-reviewer clinical sign-off, and there is **no formal clinical validation yet.**
>
> What it is **not:** not a medical device, not FDA-cleared, not validated, not for patient self-use. It's informational support — every plan must be verified by a qualified oncologist. It's non-commercial; I'm not selling anything and no one is paying me to post this.
>
> **My ask to oncologists, hem-oncs, and pathologists:** critique the clinical logic. Where's a regimen wrong, a citation weak, a red-flag missing? That feedback is the whole point.
>
> Demo (no login): https://openonco.info/try.html
> Code (MIT) + content (CC BY 4.0): https://github.com/romeo111/OpenOnco
>
> #oncology #hematology #healthtech #clinicaldecisionsupport #digitalhealth

### (d) Compliance / etiquette notes
- **Hashtags:** 3–5 is the LinkedIn norm (not the 1–2 of X). Use **#oncology #hematology #pathology #healthtech #clinicaldecisionsupport #digitalhealth #opensource** — pick 3–5 relevant ones.
- **No engagement pods, no coordinated reshares** — explicitly banned and now ML-detected ([policies](https://www.linkedin.com/legal/professional-community-policies)). Let it spread organically.
- **No DM spam.** Do not use connection invites or InMail to blast the link to people you don't know — that's one of the most-enforced LinkedIn violations ([spam help](https://www.linkedin.com/help/linkedin/answer/a1344213/)). It's fine to mention it 1:1 to a relevant existing contact who'd genuinely care.
- **Groups:** read each group's posted rules; post only via the permitted mechanism (promo thread / promo day / mod approval). If unclear, **DM a moderator and ask first.** If promo is banned, **don't post — do NOT post there; participate genuinely instead.**
- **Cadence:** one launch post, then genuine updates at a natural pace; never the same post re-dropped.

---

## Cross-platform compliance checklist (applies to all venues)

| Rule | How this section complies |
|---|---|
| Manual, by the real maintainer | Single human account per platform; no automation/scheduling for engagement; no second/sockpuppet accounts; "manual posting only" stated up front. |
| Disclosure mandatory | Every template opens with "I'm the maintainer." No third-person "I found this tool" framing; no astroturfing. |
| Value-first, feedback-seeking | The ask is "tear apart the clinical logic," not "sign up," in every template. |
| Respect each community's promo rules | X / LinkedIn-feed / Bluesky: open self-ID allowed → post. LinkedIn **groups**: per-group rules → verify, comply with the permitted mechanism, or do NOT post. Don't mass-mention KOLs. Don't broadcast into patient hashtags. |
| Medical-safety framing | "Not a medical device, not FDA-cleared, not validated, not for patient self-use, verify with an oncologist" in every post; honest STUB/early-stage maturity stated. |
| No spam cadence | One genuine post per platform; no identical mass cross-post; each platform written natively. |
| License-verification needs | None required to *post* on these venues; flagged that clinician-status claims must be honest and bio/COI disclosed. |

### Items flagged "verify the current rule"
- **Individual LinkedIn group rules** (oncology/health-tech): vary per group, change over time — read each group's rules panel before posting; DM a mod if unclear; if promo is banned, do NOT post.
- **#MedSky / Bluesky oncology community norms** — young and still forming; confirm current expectations before investing.
- **Exact current X "declare paid promotion" wording** (updated March 2026) — confirm at the source if a clinician collaborator with any industry tie posts ([X rules](https://help.x.com/en/rules-and-policies)).

---

**Sources:**
- [Risks and Benefits of Twitter Use by Hematologists/Oncologists (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5994350/)
- [Proper Tweeting Etiquette Guidelines for #PathTwitter — Schukow et al. (PubMed)](https://pubmed.ncbi.nlm.nih.gov/37533372/)
- [X Rules and Policies index](https://help.x.com/en/rules-and-policies) · [X Authenticity policy](https://help.x.com/en/rules-and-policies/authenticity)
- [X "declare paid promotion" update, March 2026 (PANews)](https://www.panewslab.com/en/articles/019cadd6-9b25-7029-845f-652157fa471e)
- [Bluesky becomes health/science community's new home (STAT)](https://www.statnews.com/2024/11/21/bluesky-gains-twitter-exodus-science-medical-community-finds-alternative-to-x/) · [Science/AAAS](https://www.science.org/content/article/old-twitter-scientific-community-finds-new-home-bluesky) · [Why Academics Are Leaving Twitter for Bluesky (arXiv)](https://arxiv.org/abs/2505.24801v1)
- [LinkedIn Professional Community Policies](https://www.linkedin.com/legal/professional-community-policies) · [Recognize/report spam (LinkedIn Help)](https://www.linkedin.com/help/linkedin/answer/a1344213/) · [LinkedIn algorithm/policy update April 2026](https://www.auditsocials.com/blog/linkedin-algorithm-sponsored-content-policy-changes-april-2026)

*Integration notes: (1) confirm the X paid-promotion update date/wording at the source if any industry-tied collaborator posts; (2) re-check per-group LinkedIn rules at posting time — both flagged "verify the current rule" above. No files were written; this section is returned for the orchestrator to place.*

---

## Clinical informatics / AI-in-medicine / open-source

# Clinician-Outreach Section: Clinical Informatics / AI-in-Medicine / Open-Source

Maintainer outreach playbook for OpenOnco. These are the **most receptive, least promo-averse** early-adopter venues. Every template below is written for **manual posting by the real maintainer, with disclosure**, and carries the mandatory medical-safety framing.

**Global rules that apply to every post in this section (do not skip):**

- **You post, as you.** Disclose in the first line that you are the maintainer/creator (or a contributor). No third-person "I found this cool tool" posts. No second account. This is all manual posting by a real person — no automation, no scheduling tools, no sockpuppets.
- **Ask for critique, not signups.** The call-to-action is always "tear apart the clinical logic / tell me where this is wrong," never "try my product."
- **Safety line is non-negotiable, in every public post:** informational decision-*support* for clinicians, **not a medical device, not FDA-cleared, not validated, not for patient self-use; verify every recommendation with a qualified oncologist.**
- **Be honest about maturity:** EARLY-STAGE v0.1, most content is STUB ("proposed, not approved"), only 15 of 806 entities have two-reviewer sign-off, no formal clinical validation.
- **One genuine post per community, spaced out.** Never paste the same text into many venues the same day.
- **Verify each community's live self-promo rule before posting.** For Reddit especially, read the actual subreddit sidebar/wiki (rules change and are not reliably reproducible from memory); where a venue requires mod permission or a specific flair/thread, comply first. Where a venue forbids self-promotion with no designated channel, **do not post** — participate genuinely instead.

---

## A. AMIA / clinical-informatics communities

### A1. AMIA Connect (connect.amia.org) — Working Groups & Discussion Forums

- **(a) Self-promo rule & whether to post:** AMIA Connect is the **members-only** online community (Working Groups, Communities of Practice, discussion forums); Working Groups are an explicit member benefit, **not open to non-members**. There is no public "Show your tool" board. The right move is **not a promo post** but a substantive contribution inside a relevant Working Group (e.g., Clinical Information Systems, Clinical Decision Support, Open Source) framed as "here is an open-source CDS artifact I built, looking for methodological critique." Treat it as a professional-society norm: contribute first, disclose your role, ask for feedback. **Post only if you are a member and only inside a topically-matched WG.** Verify the specific WG's posting norms with its leadership.
- **(b) Verification barrier:** **AMIA membership required** (paid; individual or digital membership). Identity is tied to your real professional profile — this is a high-trust, real-name venue, which is a feature for honest disclosure.
- **(c) Ready disclosed post template (for a relevant WG forum thread):**

  > **Subject: Open-source, rule-engine CDS for oncology tumor boards — seeking methodological critique**
  >
  > Hi all — I'm the maintainer of OpenOnco, a free, open-source clinical decision-*support* project for oncology MDTs. Disclosing up front that I built it; I'm here for critique, not promotion.
  >
  > Design choice I'd most like this group to challenge: clinical recommendations come from a **deterministic, declarative rule engine over a versioned, source-cited knowledge base** — no LLM picks the regimen or dose; every output is cited. It drafts two alternative plans (standard + aggressive) for a clinician to verify.
  >
  > Honest maturity statement: **EARLY-STAGE v0.1.** Most KB content is STUB ("proposed, not approved") — only 15 of 806 entities have two-reviewer sign-off, and there's **no formal clinical validation yet.** It is **not a medical device, not FDA-cleared, not for patient use**; every recommendation must be verified by a qualified oncologist.
  >
  > Questions for the WG: (1) Is "deterministic engine + LLM-for-prose-only" a defensible governance line for CDS? (2) What validation framework would you want before any pilot? (3) Where does the citation/provenance model fall short?
  >
  > Repo (MIT code, CC BY 4.0 content): https://github.com/romeo111/OpenOnco · Site: https://openonco.info

- **(d) Compliance/etiquette:** Lead with the question, not the link. Don't cross-post to multiple WGs. AMIA is a standards-and-governance crowd — they will respond well to the "no LLM in the clinical decision" framing and to the validation-gap honesty. Don't oversell scale numbers.

### A2. r/medicine (verified physicians) — **default: DO NOT post**

- **(a) Self-promo rule:** r/medicine is a large lounge for verified medical professionals and is **strongly anti-self-promotion**; promotion of one's own tools/sites/surveys/research recruitment is typically removed and can earn a ban even when the content is "valuable." **Read the current sidebar/wiki rule** — the safe default is **do not make a promotional post.** If you want this audience, **modmail the moderators first** and ask whether a clearly-disclosed "open-source CDS, seeking clinician critique, non-commercial" post is permitted; post only with explicit mod approval. If mods decline or don't respond, **do not post** — participate genuinely instead.
- **(b) Verification barrier:** **Physician/HCP flair verification is required to participate meaningfully** — you (the poster) must be a verified clinician to have standing. If the maintainer is **not** a verified clinician, do not attempt this venue; have a clinician contributor handle it under their own disclosed identity.
- **(c) Ready disclosed post template (use ONLY after explicit mod approval AND only if the poster is a verified clinician):**

  > **Title: [Mod-approved] Open-source oncology CDS — asking clinicians to break the clinical logic (non-commercial, not a device)**
  >
  > Mods approved this post. I'm the maintainer of OpenOnco, a **free, non-commercial, open-source** decision-*support* tool for oncology tumor boards — disclosing that I built it. I'm not selling anything (code MIT, content CC BY 4.0) and I'm not asking anyone to sign up. I want practicing oncologists to tell me where the clinical logic is wrong.
  >
  > How it works: a **deterministic rule engine** over a source-cited knowledge base drafts a standard and an aggressive plan for a clinician to verify. **No LLM chooses the regimen or dose.** Every recommendation is cited.
  >
  > Straight talk on maturity: **v0.1, early-stage.** Most content is STUB/unapproved; only 15 of 806 entities have two-reviewer sign-off; **no formal clinical validation.** **Not a medical device, not FDA-cleared, not for patient self-use — verify everything with a qualified oncologist.**
  >
  > If you have 5 minutes: pick a disease you treat, look at the drafted plan, and tell me what's outdated, mis-cited, or dangerous. Demo: https://openonco.info/try.html · Repo: https://github.com/romeo111/OpenOnco

- **(d) Compliance/etiquette:** **Do not post without mod permission.** No survey links, no recruitment funnels. Expect blunt feedback and engage with every clinical objection. If mods decline, respect it and instead participate genuinely (answer informatics questions) without linking your project.

---

## B. HL7 / FHIR + mCODE groups

### B1. FHIR Community Chat — Zulip at chat.fhir.org

- **(a) Self-promo rule & how to post:** The community expectations are explicit and **vendor-neutral**: **unsolicited promotion, marketing, or business solicitation is prohibited**, including sharing pricing/licensing; mention products only when **directly relevant to a specific technical question**, disclose commercial affiliation, and **prioritize open-source/community solutions.** There is **one sanctioned exception: a product release may be announced on the `#social` stream**, kept concise. So: do **substantive** posting in `#implementers` / `#research` only when on-topic, and put any "we shipped X" note in **`#social`**. OpenOnco being **open-source + non-commercial** fits this culture well.
- **(b) Verification barrier:** **Free account** (accounts did *not* carry over from the old chat.hl7.org — create a new one). No license check; real-name/professional norms apply. Set up your account, then subscribe to streams via the streams gear icon.
- **(c) Ready disclosed post templates:**

  **`#social` (concise release-style announcement — the sanctioned channel):**
  > Maintainer here. **OpenOnco** (free, open-source, non-commercial oncology decision-*support*) now takes **FHIR R4/mCODE** patient input and runs a deterministic, source-cited rule engine — no LLM picks treatment. v0.1, early-stage, not a medical device / not validated. Feedback on the mCODE mapping especially welcome. Repo: https://github.com/romeo111/OpenOnco

  **`#implementers` or the mCODE/oncology stream (only as a genuine, on-topic technical question):**
  > Disclosing I maintain OpenOnco (open-source oncology CDS). I'm mapping patient input to **mCODE** and want to do it correctly rather than reinvent. Specifically: for [Cancer Disease Status / Tumor Marker Test / Cancer-Related Medication], am I using the right mCODE profiles and value sets, and where do implementers typically diverge? Happy to share my mapping for critique. (Not promoting — the engine is deterministic and every output is cited; I just want the FHIR/mCODE layer right.)

- **(d) Compliance/etiquette:** Keep `#social` to one or two short lines, no pricing language (there is none — say "free/open-source"). In `#implementers`, lead with a real interoperability question and **search first** so you don't repeat an answered topic. Disclose affiliation in-thread. This is arguably your **best-fit technical venue** — they care about exactly the standards work you're doing.

### B2. CodeX HL7 FHIR Accelerator + mCODE Community of Practice

- **(a) Self-promo rule & how to participate:** CodeX is a **member-driven** accelerator built around mCODE/oncology use cases; it is collaborative, not a promo board. The **Community of Practice (CoP) meeting is free and open to all** and is the right place to surface an open-source mCODE consumer and ask for feedback. Don't pitch; present it as community-relevant work and ask to plug into a relevant use case.
- **(b) Verification barrier:** None to attend the open CoP or to email; deeper Use-Case workstreams may require **CodeX/HL7 membership**. Subscribe to the CodeX listserv and email **CodeX@hl7.org** to introduce yourself.
- **(c) Ready disclosed intro email template (to CodeX@hl7.org / CoP intro):**

  > Subject: Open-source mCODE-consuming oncology decision-support — intro + request for feedback
  >
  > Hello CodeX team — I'm the maintainer of **OpenOnco**, a free, open-source, **non-commercial** oncology decision-*support* project (code MIT, content CC BY 4.0). I'm reaching out as the creator, not as a vendor.
  >
  > Relevance to CodeX: OpenOnco ingests **FHIR R4 / mCODE** patient data and runs a **deterministic, source-cited rule engine** (no LLM in the clinical decision) to draft alternative treatment plans for a clinician to verify. It's a real-world mCODE *consumer* that might be a useful reference or test partner.
  >
  > Honest status: **v0.1, early-stage**, most content STUB/unapproved, **no formal clinical validation, not a medical device.** I'm seeking critique on the mCODE mapping and would value pointing me to the right Use Case or CoP slot. Could I join an upcoming CoP, or is there a workstream where an open-source mCODE consumer would be useful?
  >
  > Repo: https://github.com/romeo111/OpenOnco · Site: https://openonco.info

- **(d) Compliance/etiquette:** Frame as contribution to the mCODE ecosystem, not a launch. If invited to a CoP, keep any spoken intro to a couple of minutes and end with a question. This venue maps directly onto your data model — high value, low promo-risk.

---

## C. Health-tech & AI-in-medicine Slacks / Discords

### C1. Health Tech Nerds (HTN) Slack

- **(a) Self-promo rule & how to post:** Vertical, paid Slack with role/topic channels and a `#housekeeping` channel where the guidelines live. Like most paid health-tech Slacks, **blatant self-promo is discouraged; the norm is "be a member first, share your work as a contribution."** **Verify the exact promo policy in `#housekeeping` (or email hello@healthtechnerds.com)** and use any designated "show your work / projects" channel rather than the general channel. Post once, disclosed, as a feedback request.
- **(b) Verification barrier:** **Paid membership.** No license check, but real identities and a vetted-ish crowd.
- **(c) Ready disclosed post template (in the designated projects/feedback channel):**

  > 👋 Maintainer disclosure: I built **OpenOnco**, a free, open-source oncology decision-*support* tool, and I'd love this group to poke holes in it — not a sales post (it's non-commercial, MIT/CC BY).
  >
  > The non-obvious design bet: **no LLM chooses treatment.** A deterministic rule engine over a source-cited KB drafts two plans for a clinician to verify; there's also an **MCP server** so ChatGPT/Claude/Cursor can call the engine instead of hallucinating oncology.
  >
  > Real talk: **v0.1, early-stage**, mostly STUB content, **not validated, not a medical device, not for patient use.** What I want: (1) is the "deterministic engine + MCP" architecture credible to people who've shipped clinical software? (2) what would make you trust or distrust it? Demo: https://openonco.info/try.html

- **(d) Compliance/etiquette:** Use the right channel, disclose, ask a question, don't drip-link across channels. This audience appreciates the MCP angle and the honesty about validation gaps. Engage with replies for days, not minutes.

### C2. Out-Of-Pocket community Slack

- **(a) Self-promo rule:** Vetted, application-gated paid Slack (high-quality discussion, written-assignment participation). Self-promo norms are **strict and community-first.** **Verify the current rule on entry** and only share in a sanctioned context. Given the vetting, the honest "critique my open-source clinical logic" framing lands well, but **do not lead with promotion**, and if there's no sanctioned place to share a project, **don't.**
- **(b) Verification barrier:** **Application + paid membership, with vetting** (broad healthcare knowledge, active participation). Higher bar than HTN.
- **(c) Ready disclosed post template:** Reuse the **C1 template** verbatim (it is already disclosed, non-salesy, feedback-first) — but only after confirming the venue permits project sharing.
- **(d) Compliance/etiquette:** Earn standing by participating in discussion/assignments before sharing your own project. One post, disclosed, framed as a request for critique.

### C3. AI-in-medicine Discords/Slacks generally (clinical-AI / MCP-in-healthcare servers)

- **(a) Self-promo rule:** Highly variable. **Default assumption: read the server's `#rules`/pinned post; many have a dedicated `#show-your-work` / `#projects` / `#self-promo` channel and forbid promo elsewhere.** Post **only** in the designated channel, **only after confirming the rule.** If a server has no such channel and bans promo, **do not post** — participate genuinely instead.
- **(b) Verification barrier:** Usually none, but some clinical servers gate by professional verification — check, and if a server requires clinician verification, only a verified clinician should post.
- **(c) Ready disclosed post template (designated `#show-your-work`/`#projects` channel):**

  > Maintainer here, disclosing I built this — sharing for critique, not signups. **OpenOnco** is a free, open-source oncology decision-*support* tool where a **deterministic rule engine** (not an LLM) drafts cited treatment plans for a clinician to verify, plus an **MCP server** so agents call the engine instead of guessing oncology.
  > **v0.1, early-stage, mostly STUB, not validated, not a medical device, not for patient use — verify with an oncologist.** I'd genuinely value people who work on clinical AI telling me where the safety model or the rule engine breaks. Repo: https://github.com/romeo111/OpenOnco

- **(d) Compliance/etiquette:** Confirm the channel rule first; one post; respond to feedback. **Do NOT post** in any AI-medicine server whose rules ban self-promotion with no designated channel — participate genuinely instead.

---

## D. Open-source / developer communities (OSS + MCP server)

### D1. Hacker News — Show HN

- **(a) Self-promo rule & how to post:** **Show HN is explicitly for sharing your own work**, provided it's something people can actually try. The core guideline: "Please don't use HN primarily for promotion. It's ok to post your own stuff part of the time." So a single, factual Show HN is **fully on-policy.** Make it **tryable without signup** (your demo at openonco.info/try.html qualifies). Title must be plain — **no hype, no exclamation points, no marketing words, no company name as username.** Then post a first comment with the backstory.
- **(b) Verification barrier:** None (free HN account). No clinical verification — so the **safety disclaimer carries the ethical weight here**; be especially clear it's not a medical device and not for patient use.
- **(c) Ready disclosed post:**

  **Title (factual, no hype):**
  > Show HN: OpenOnco – open-source oncology decision support with a deterministic rule engine

  **First comment (you, as maintainer):**
  > I'm the maintainer. OpenOnco is a free, open-source decision-*support* tool for oncology tumor boards. The design bet: **no LLM chooses the treatment or dose** — a deterministic rule engine over a versioned, source-cited knowledge base drafts two alternative plans (standard + aggressive) for a clinician to verify, and every recommendation is cited. There's also an MCP server so ChatGPT/Claude/Cursor can call the engine instead of free-associating oncology.
  >
  > Honest status: **early-stage v0.1.** Scale today is 92 diseases / 664 indications / 384 regimens / 444 cited sources, but **most content is STUB ("proposed, not approved")** — only 15 of 806 entities have two-reviewer clinical sign-off, and **there's no formal clinical validation yet.** It is **not a medical device, not FDA-cleared, and not for patient self-use** — every output must be verified by a qualified oncologist.
  >
  > What I want from HN: critique of the architecture (deterministic engine + LLM-for-prose-only + MCP), the provenance model, and the clinical-safety framing. Code is MIT, content CC BY 4.0. Demo (no signup): https://openonco.info/try.html · Repo: https://github.com/romeo111/OpenOnco

- **(d) Compliance/etiquette:** No marketing voice anywhere. No signup wall (good — yours has none). Don't ask for upvotes. Stay in the thread and answer hard questions, especially safety ones. Post once.

### D2. Lobsters (lobste.rs)

- **(a) Self-promo rule & how to post:** Authors **may** self-submit, but **self-promo should be a small minority (~under a quarter) of your stories and comments**, and the post must stand on its own technical merit (release, architecture write-up, postmortem). A bare product announcement from a write-only account is treated as spam. **Best approach: don't submit a "look at my tool" link — submit a genuinely technical write-up** (e.g., "Why our clinical decision support uses a deterministic rule engine instead of an LLM," or the MCP-server design) and **disclose authorship in a comment.** Tag appropriately (e.g., `programming`, `ai`).
- **(b) Verification barrier:** **Invite-only** account; no clinical verification. If you're not already a member, this is gated — get an invite or skip.
- **(c) Ready disclosed submission + comment:**

  **Submit:** your own blog/README write-up, e.g. *"Deterministic rule engine vs. LLM for oncology decision support (and an MCP server on top)."*
  **Author comment:**
  > Author here. This is the design write-up for OpenOnco, an open-source oncology decision-*support* tool. The interesting engineering bit is keeping the LLM entirely out of the clinical decision: a deterministic rule engine over a source-cited KB, with an MCP server so agents call the engine. It's early-stage v0.1 and explicitly **not** a medical device / not validated — sharing for the architecture critique, not as a launch. Happy to answer questions.

- **(d) Compliance/etiquette:** Submit substance, not a landing page. Disclose authorship. Don't make OpenOnco the only thing you ever post. One submission.

### D3. MCP ecosystem — `awesome-mcp-servers` lists + MCP community Discords

- **(a) Self-promo rule & how to post:** The MCP "awesome" lists are **built to receive community-submitted servers via PR** — adding OpenOnco's MCP server is a **legitimate, expected contribution, not spam**, as long as you follow each list's CONTRIBUTING format/category placement. Submit a PR to one or two well-maintained lists (e.g., the `modelcontextprotocol`-linked community lists, `wong2/awesome-mcp-servers`, `punkpeye/awesome-mcp-servers`-style repos). **Note:** the **official MCP Contributor Discord is for protocol contributors, not for promoting your server** — do **not** drop a "check out my server" message there. Use a **community/general MCP Discord** only if it has a designated showcase channel.
- **(b) Verification barrier:** GitHub account for PRs; no clinical verification. Safety disclaimer must be in the entry description.
- **(c) Ready disclosed PR entry (one line, list format) + PR description:**

  **List entry:**
  > - [OpenOnco](https://github.com/romeo111/OpenOnco) — Open-source oncology clinical decision *support*: a deterministic, source-cited rule engine (no LLM in the clinical decision) exposed via MCP so agents can call it for cited treatment-plan drafts. Research/support tool, **not a medical device; clinician verification required.**

  **PR description:**
  > Adding the OpenOnco MCP server. Disclosure: I'm the maintainer. It exposes a deterministic, source-cited oncology decision-support engine over MCP. It's early-stage v0.1 and explicitly **not a medical device / not validated / not for patient use** — I've kept that framing in the entry so users aren't misled. Code MIT, content CC BY 4.0. Followed the CONTRIBUTING format and placed it under [category]. Happy to adjust categorization.

- **(d) Compliance/etiquette:** Follow each repo's CONTRIBUTING/category rules exactly; one PR per list, to one or two lists, not a dozen. Keep the medical disclaimer in the public entry — these lists are read by developers who may not know it's clinically sensitive. **Do not promote in the official Contributor Discord.**

### D4. r/programming, r/opensource, r/MachineLearning, and adjacent dev subs

- **(a) Self-promo rule:** Varies sharply. r/opensource is generally **receptive to "I made this open-source thing"**; r/programming and r/MachineLearning are **stricter** (r/MachineLearning typically wants a `[P]` Project tag and substance, and removes low-effort promo). **Read each subreddit's current sidebar/wiki rule before posting.** Post in the **most permissive, most on-topic** one (likely r/opensource), with the correct flair/tag, **disclosed**, once.
- **(b) Verification barrier:** None clinical. Some subs require minimum account karma/age — check.
- **(c) Ready disclosed post template (e.g., r/opensource; add `[P]` if r/MachineLearning):**

  > **Title: [I made this] OpenOnco – open-source oncology decision support; deterministic rule engine (no LLM in the decision) + MCP server**
  >
  > Maintainer here, disclosing I built it. **OpenOnco** is a free, open-source (MIT / CC BY 4.0) decision-*support* tool for oncology tumor boards. The deliberate design choice: **the LLM never picks the treatment or dose** — a deterministic, declarative rule engine over a versioned, source-cited knowledge base drafts cited plans for a clinician to verify. There's also an MCP server so AI assistants call the engine instead of hallucinating oncology.
  >
  > Honest status: **early-stage v0.1**, most content is STUB/unapproved, only 15 of 806 entities have two-reviewer sign-off, **no formal clinical validation. Not a medical device, not FDA-cleared, not for patient self-use.**
  >
  > Looking for: architecture and code critique, and (if any clinicians are here) where the clinical logic is wrong. Repo: https://github.com/romeo111/OpenOnco

- **(d) Compliance/etiquette:** Right flair/tag, disclosed, one sub at a time, spaced out. If a sub restricts self-promo to a weekly thread, **use that thread instead, or skip** — do not blast the main feed.

---

## Quick decision table

| Venue | Promo allowed? | How to comply | Verification barrier | Recommendation |
|---|---|---|---|---|
| **AMIA Connect WGs** | Members-only, contribution-style only | Post in a matched WG as a feedback request | Paid AMIA membership | Post if member; high-trust fit |
| **r/medicine** | Effectively no (verify sidebar) | Modmail mods first; post only if approved | Verified physician flair required | **Default: don't post** unless clinician + mod OK |
| **FHIR Zulip (chat.fhir.org)** | No marketing; `#social` release note allowed; on-topic Q in `#implementers` | Free account; concise `#social` note + real Q in `#implementers` | Free account | **Strong fit — post** |
| **CodeX / mCODE CoP** | Collaboration, not promo | Free CoP + email CodeX@hl7.org as contributor | Free CoP; membership for deep work | **Strong fit — engage** |
| **Health Tech Nerds Slack** | Discouraged in general; use projects channel | Check `#housekeeping`; post in projects channel | Paid | Post once if member |
| **Out-Of-Pocket Slack** | Strict, community-first | Participate first; share only if sanctioned | Application + paid + vetting | Post only after earning standing |
| **AI-med Discords/Slacks** | Varies | Only in `#show-your-work`/`#projects`; confirm rule | Sometimes pro-verification | Post only where a showcase channel exists; else don't |
| **Hacker News Show HN** | **Yes** (own work, tryable) | Plain title, backstory comment, no hype | None | **Post — best dev launch venue** |
| **Lobsters** | Yes if minority of activity + technical merit | Submit a technical write-up, disclose in comment | Invite-only | Post if member, as a write-up |
| **awesome-mcp-servers lists** | **Yes** via PR | Follow CONTRIBUTING; keep disclaimer in entry | GitHub | **Submit PR (1–2 lists)** |
| **MCP official Contributor Discord** | No promo | Don't promote there | — | **Do not post** |
| **r/opensource / r/MachineLearning / r/programming** | Varies (verify sidebar) | Correct flair/`[P]` tag, disclosed, 1 sub | Some karma gates | Post in most-permissive, on-topic sub once |

---

## Before you post — two caveats for the maintainer

1. **Reddit & any venue with mutable rules:** read each subreddit's live sidebar/wiki (and message mods where required) before posting rather than trusting the typical-rule notes above. Rules change; comply with what's posted today.
2. **Physician-verification venues:** for **r/medicine** and any clinician-gated Discord/Slack, only a **verified clinician** should post. If the maintainer is not one, route through a clinician contributor under their own disclosed identity — never post on someone else's behalf or imply clinician status you don't have.

**Live assets referenced in templates:**
- Site: https://openonco.info
- Demo (no signup): https://openonco.info/try.html
- Repo (MIT code / CC BY 4.0 content): https://github.com/romeo111/OpenOnco

This is a research/outreach deliverable — no repository files were created or modified.

---

## Ukrainian / regional medical communities

# Clinician Outreach — Ukrainian / Regional Medical Communities

> **Maintainer note (not for sending).** Manual posting only, by you (the real maintainer), one genuine message per venue, spaced across days/weeks — never identical mass cross-posts, never automated, never a sockpuppet or third-person "I found this cool tool" post. Every message discloses that you are the maintainer (engineer, not an oncologist). The ask is "tear apart the clinical logic," not "sign up." Where a venue forbids self-promotion, **do not post there** — participate genuinely instead. The mandatory disclaimer below must appear in every public post and in any conference slide/poster.

**MANDATORY medical-safety disclaimer — append to EVERY public post / message body (do not remove either half):**

> EN: OpenOnco is an informational clinical decision support tool for healthcare professionals — not a medical device, not FDA-cleared, not clinically validated, not for direct patient use, and not for emergency or time-critical decisions; every plan it drafts must be verified by a qualified oncologist.
>
> UA: OpenOnco — це інформаційний інструмент підтримки клінічних рішень для медичних працівників: не медичний виріб, не сертифікований засіб, не пройшов клінічної валідації, не для самостійного застосування пацієнтами і не для невідкладних рішень; кожен чернетковий план мусить перевірити кваліфікований онколог.

---

The Ukrainian oncology and med-tech ecosystem is small, professionalized, and relationship-driven. Most receptive venues are **organization-run** (oncoHUB, UMSA, eHealth) rather than open free-for-all forums, which means the dominant etiquette is **"ask a human first"**, not "drop a link." Cold posting into a closed professional community without a contact handshake reads as advertising and burns the relationship. The strongest play here is direct, disclosed outreach to organizers — and only then, if invited, a public post.

**Cross-cutting facts that apply to every venue below:**
- Ukraine's medical-advertising law (Law "On Advertising", Art. 21) is strict: anything that reads as promotion of a medical "method of treatment/diagnosis" can be regulated, and Meta tightened healthcare-category enforcement in 2025. **OpenOnco is not a medical service or device, so frame every post as an open-source research/decision-support tool seeking peer review — never as a treatment service.** This is both legally safer and true. ([Law overview](https://mitrax.ua/uk/blog/reklama-medichnih-zakladiv-poslug-ta-likarskih-zasobiv-yaki-vimogi-zakonodavstva-neobhidno-vrahuvati/), [Meta UA/EU med-ads rules](https://netpeak.net/uk/blog/reklama-medposlug-u-google-ads-ta-meta-ex-facebook-ads-pravila-dlya-ukraini-ta-es/))
- Many groups use the standard rule "No spam, self-promotion, or links without admin approval." Where that applies, message the admin first. ([FB group rules 2026](https://groupboss.io/blog/facebook-group-rules/))
- The poster must be the **real maintainer, disclosed**, and a **clearly-labeled non-clinician engineer** (or, if you are a verified clinician, say so plainly). Several of these venues are physician-only or interview/screen members — see the per-venue verification barriers. Never join a physician-only space under false pretenses.

---

## 1. oncoHUB — Ukrainian Society of Clinical Oncology (PRIMARY TARGET)

The single best-fit venue. A non-profit professional body uniting Ukrainian clinical oncologists, with an explicit value of "networking among oncology professionals for quick information exchange" and an evidence-based-medicine mission. ([about](https://oncohub.org/ua/page/about-us), [health-ua writeup](https://health-ua.com/onkologiya-i-gematologiya/onkologiia/64556-stvorennya-ukransko-splki-klnchnih-onkologv-taproktu-OncoHub-spvpratcya-tap))

Within oncoHUB, the **"Tumor Board Café" journal club** is an almost-exact match for OpenOnco's use case — a community "for open, safe, and professional discussion of current scientific data," i.e. case discussion among oncologists. ([Tumor Board Café](https://oncohub.org/en/page/journal-club-tumor-board-cafe)) **YoungOncoHub** (students/interns/young doctors) is the right sub-venue for early adopters. ([YoungOncoHub](https://oncohub.org/en/page/youth-oncohub))

**(a) Self-promo rule / how to post:** No open public posting mechanism — this is an organization, not a forum. The correct channel is **direct outreach to organizers** at `admin@oncohub.org` (publicly listed). Do **not** post into any oncoHUB-run chat or event page unilaterally; propose a Tumor Board Café demo / YoungOncoHub mention and let them decide the channel. *Verify the current contact and whether a member-only chat exists before assuming.*

**(b) Verification barrier:** This is a clinician-led body. As a (presumably non-clinician) maintainer, **disclose that explicitly** and lead with "I'm the engineer/maintainer, not an oncologist — I need clinicians to judge the clinical logic." Don't represent yourself as a physician.

**(c) Disclosed outreach template (email/DM to admin@oncohub.org):**

> **Тема:** Безкоштовний open-source інструмент підтримки рішень для тумор-борду — прошу клінічної критики
>
> Доброго дня! Мене звати [ім'я], я мейнтейнер OpenOnco — безкоштовного відкритого (open-source) інструменту підтримки клінічних рішень для онкологічних тумор-бордів. **Одразу зазначу: я інженер, а не онколог**, тому й звертаюся саме до вашої спільноти.
>
> Що це: детермінований "rule engine" поверх версіонованої, повністю процитованої бази знань готує **два альтернативні чернеткові плани лікування** (стандартний + агресивний) для перевірки лікарем. **Жоден LLM не обирає схему чи дозу** — кожна рекомендація має посилання на джерело.
>
> **Чесно про зрілість:** це рання версія v0.1. Більшість контенту — чернетки зі статусом "запропоновано, не затверджено"; лише 15 із 806 сутностей пройшли подвійне рецензування. **Формальної клінічної валідації немає.** Саме тому шукаю фахівців, які розкритикують клінічну логіку.
>
> Чи доречно було б показати коротке демо у форматі Tumor Board Café або для YoungOncoHub — і почути, що тут не так? Радо адаптуюся до ваших правил.
>
> Демо: https://openonco.info/try.html · Код: https://github.com/romeo111/OpenOnco · Ліцензії: код MIT, контент CC BY 4.0.
>
> OpenOnco — це інформаційний інструмент підтримки клінічних рішень для медичних працівників: не медичний виріб, не сертифікований засіб, не пройшов клінічної валідації, не для самостійного застосування пацієнтами і не для невідкладних рішень; кожен чернетковий план мусить перевірити кваліфікований онколог.
>
> Дякую за вашу роботу для української онкології.
> — [ім'я], мейнтейнер OpenOnco

**(d) Compliance/etiquette:** One email, then wait. If they invite a session, follow their format exactly and put the disclaimer on any slide. Never post into their channels before being asked. Treat this as a relationship, not a campaign — they are the highest-value endorser if they like it, and the most damaging if you spam them.

---

## 2. UMSA — Ukrainian Medical Students' Association

Med students/interns across 13 Ukrainian medical schools plus international students. ([FB](https://www.facebook.com/ukrmsa/), [LinkedIn](https://www.linkedin.com/company/ukrainian-medical-students'-association)) Students are realistic early adopters: curious, tool-friendly, and lower-stakes than attendings — but you must be explicit that this is **not** for unsupervised clinical use.

**(a) Self-promo rule / how to post:** UMSA's public Facebook **Page** is broadcast-only (you can't post a tool to a Page). Engagement = message the page admins / local committees and ask whether an educational mention fits, or request a contact for their student channels. *Verify whether UMSA runs an open members' group/Telegram and that group's specific promo rule before posting anything.*

**(b) Verification barrier:** Membership is student-gated, but you're approaching as an external maintainer — disclose that. No physician license needed for outreach; do **not** post as if you were a student member.

**(c) Disclosed outreach template (DM to UMSA admins / local committee):**

> Привіт! Я [ім'я], мейнтейнер OpenOnco — безкоштовного open-source навчально-дослідницького інструменту з клінічної онкології. **Я розробник, не лікар.**
>
> Він показує, як з процитованої бази знань детермінований алгоритм будує чернеткові плани лікування (без вибору схем штучним інтелектом — усе з посиланнями на джерела). Думаю, студентам може бути цікаво **як приклад доказової логіки та джерелознавства**, а мені дуже потрібен їхній свіжий погляд: де логіка кульгає, яких джерел бракує.
>
> **Чесно:** рання версія, більшість контенту — неперевірені чернетки, клінічної валідації немає. Це **не медичний виріб і не інструмент для лікування реальних пацієнтів** — лише навчальний приклад.
>
> Чи доречно поділитися цим у вашому студентському каналі — і за якими правилами? Не хочу порушити етикет спільноти.
> Демо: https://openonco.info/try.html · Код: https://github.com/romeo111/OpenOnco
>
> OpenOnco — це інформаційний інструмент підтримки клінічних рішень для медичних працівників: не медичний виріб, не сертифікований засіб, не пройшов клінічної валідації, не для самостійного застосування пацієнтами і не для невідкладних рішень; кожен чернетковий план мусить перевірити кваліфікований онколог.

**(d) Compliance/etiquette:** Frame strictly as educational + feedback, never "use this on patients." Honor whatever channel/flair rule the committee names. One ask per committee.

---

## 3. eHealth Ukraine community (@ehealthukraine + HealthTech.in.ua)

A Telegram channel informing the medical community about digital-health changes, plus the broader Ukrainian HealthTech network. ([@ehealthukraine](https://t.me/ehealthukraine), [healthtech.in.ua](https://healthtech.in.ua/), [IT Ukraine Assoc. HealthTech](https://itukraine.org.ua/en/ukraine-s-healthtech-industry-technological-challenges-and-the-path-to-european-integration/)) This is the **builder/health-tech** audience — receptive to "open-source, MCP server, MIT license" framing and to honest "early-stage, tear it apart" positioning.

**(a) Self-promo rule / how to post:** @ehealthukraine is a one-way broadcast channel — you **cannot post into it**; reach the eHealth/HealthTech team via their site/admins to ask about a community-projects slot or an intro. HealthTech.in.ua is a network/community org — contact organizers about a showcase. *Verify whether either runs an open discussion chat and its rules before posting.*

**(b) Verification barrier:** None for clinician licensure (this is a tech audience) — but disclose maintainer identity and the early-stage/STUB reality plainly; this crowd punishes hype.

**(c) Disclosed outreach template (to eHealth/HealthTech organizers):**

> Вітаю! Я [ім'я], мейнтейнер open-source проєкту OpenOnco (підтримка клінічних рішень для онкологічних тумор-бордів; код MIT, контент CC BY 4.0).
>
> Технічно цікаве: детермінований rule engine поверх процитованої бази знань (92 захворювання, 664 показання, 384 схеми, 444 джерела), плюс **MCP-сервер**, через який ChatGPT/Claude/Cursor можуть викликати движок. **LLM не обирає лікування** — лише движок із посиланнями.
>
> Це **рання v0.1**: більшість контенту — неперевірені чернетки, клінічної валідації немає. Шукаю технічний і клінічний фідбек від української health-tech спільноти.
>
> Чи є у вас формат для показу community-проєктів / чи можете підказати, з ким поговорити? Радо дотримаюся ваших правил.
> https://openonco.info · https://github.com/romeo111/OpenOnco
>
> OpenOnco — це інформаційний інструмент підтримки клінічних рішень для медичних працівників: не медичний виріб, не сертифікований засіб, не пройшов клінічної валідації, не для самостійного застосування пацієнтами і не для невідкладних рішень; кожен чернетковий план мусить перевірити кваліфікований онколог.

**(d) Compliance/etiquette:** Lead with the open-source/MCP angle, be blunt about STUB status. One message; don't repost across their channels.

---

## 4. Lviv Medical Forum / "ГалМЕД" (CONFERENCE, not a posting venue)

Western Ukraine's largest medical event/exhibition with professional schools and master classes, MoH-supported. ([FB page](https://www.facebook.com/Lviv.Medical.Forum/), [medforum.lviv.ua](https://www.medforum.lviv.ua/), [galexpo](https://galexpo.com.ua/galmed/))

**(a) Self-promo rule / how to post:** This is an **event organizer's Facebook Page and an exhibition**, not a discussion forum — there is **no public posting**. Do **not** post promotional content to their page. The legitimate path is contacting organizers (`nml@galexpo.lviv.ua`, listed) about a non-commercial talk/poster on open-source decision support in a future program. Treat as a long-lead **partnership/speaking** opportunity, not an outreach post.

**(b) Verification barrier:** Speaking slots are curated by organizers; expect to be vetted. Disclose maintainer (non-clinician) status.

**(c) Template:** Use the oncoHUB-style email above, retargeted as a speaking proposal ("чи можливий короткий некомерційний виступ/постер про open-source підтримку рішень у вашій науково-практичній програмі"), and keep the mandatory disclaimer in the message. **If a talk/poster is granted, the not-a-medical-device + verify-with-an-oncologist disclaimer must also appear on the slide/poster itself** — a conference presentation is a public medical-context communication.

**(d) Compliance/etiquette:** No unsolicited posting on the page. Strictly non-commercial framing (it's a vendor-heavy expo; you are explicitly *not* a vendor). Patience — these are annual cycles.

---

## 5. General Ukrainian medical Facebook groups (e.g. "Medical Community Ukraine", local oncology pages) — POST ONLY WITH ADMIN PERMISSION

Examples surfaced: [Medical Community Ukraine](https://www.facebook.com/medicalcommunity.ukraine/), regional oncology pages like [BP Oncology Vinnytsia](https://www.facebook.com/bpmedicaloncology/?locale=uk_UA), [Ukrainian Society of Surgical Oncology](https://www.facebook.com/oncosurgery.ua/).

**(a) Self-promo rule / how to post:** Unknown per-group rules; most professional FB groups default to "no self-promo without admin approval." **Do not post until you have read the specific group's pinned rules and obtained admin permission.** *Verify each group's current rule individually.* The surgical-oncology and regional-clinic pages are **organization Pages**, not open groups — message the admin, don't post. **If a group forbids any promotion (many do), do NOT post there at all** — see compliance note (d).

**(b) Verification barrier:** Several Ukrainian clinical groups screen for physician status at join. If a group is physician-only and you're not a clinician, **do not join under false pretenses** — instead message an admin externally and disclose you're the maintainer seeking a clinician to evaluate it.

**(c) Disclosed post template (use ONLY after explicit admin approval, in an approved thread):**

> [Публікую з дозволу адміністрації.] Доброго дня, колеги. Я [ім'я], **мейнтейнер (інженер, не лікар)** безкоштовного open-source інструменту OpenOnco для підтримки рішень онкологічного тумор-борду.
>
> Як працює: детермінований алгоритм поверх процитованої бази знань готує два чернеткові плани (стандартний + агресивний) для перевірки лікарем. **ШІ не обирає схему чи дозу — усе з посиланнями на джерела.**
>
> **Чесно про статус:** рання версія, більшість контенту — чернетки "запропоновано, не затверджено", формальної валідації немає.
>
> Прошу про одне: **розкритикуйте клінічну логіку** — де помилки, яких джерел бракує. Це найкорисніший внесок зараз.
> Демо: https://openonco.info/try.html · Код: https://github.com/romeo111/OpenOnco
>
> OpenOnco — це інформаційний інструмент підтримки клінічних рішень для медичних працівників: не медичний виріб, не сертифікований засіб, не пройшов клінічної валідації, не для самостійного застосування пацієнтами і не для невідкладних рішень; кожен чернетковий план мусить перевірити кваліфікований онколог.

**(d) Compliance/etiquette:** Permission first, mark it ("з дозволу адміністрації"), one group at a time, no identical mass cross-posting. **If a group forbids any promo (many do), do not post — participate genuinely instead** and let interest arise organically.

---

## Venues to AVOID posting into

- **Patient-facing / mixed Telegram channels** (e.g. "Медицина для всіх", [@oncologyna](https://tgstat.ru/en/channel/@oncologyna) and similar patient-oriented oncology channels): patients there may misread OpenOnco as self-care guidance — **high medical-safety risk. Do not post.** ([5.ua medical TG writeup](https://www.5.ua/dv/medinfo/269963))
- **NSZU official channel** ([t.me/NSZU_gov](https://t.me/s/NSZU_gov)): government broadcast, no community posting — not a venue.
- **Any closed physician-only group you can't legitimately join** — route through a disclosed admin contact instead of joining under false pretenses.
- **Any group whose rules forbid self-promotion** — do not post; participate genuinely instead.

## Sequencing recommendation
1. **oncoHUB / Tumor Board Café / YoungOncoHub** (email `admin@oncohub.org`) — highest fit, do first.
2. **eHealth/HealthTech organizers** — builder audience, parallel-OK.
3. **UMSA committees** — student early adopters.
4. **General FB groups** — only after admin permission, spaced out.
5. **Lviv Medical Forum** — long-lead speaking proposal, non-commercial.

Space outreach across days/weeks; never paste an identical message into multiple venues simultaneously. Every public post must carry (a) the maintainer disclosure, (b) the "no LLM picks regimen/dose" point, and (c) the full mandatory disclaimer (not a medical device / not FDA-cleared / not validated / not for patient use / not for emergencies / verify with a qualified oncologist).

**Sources:**
- [oncoHUB — About](https://oncohub.org/ua/page/about-us), [Tumor Board Café](https://oncohub.org/en/page/journal-club-tumor-board-cafe), [YoungOncoHub](https://oncohub.org/en/page/youth-oncohub), [health-ua oncoHUB writeup](https://health-ua.com/onkologiya-i-gematologiya/onkologiia/64556-stvorennya-ukransko-splki-klnchnih-onkologv-taproktu-OncoHub-spvpratcya-tap)
- [UMSA Facebook](https://www.facebook.com/ukrmsa/), [UMSA LinkedIn](https://www.linkedin.com/company/ukrainian-medical-students'-association)
- [@ehealthukraine Telegram](https://t.me/ehealthukraine), [HealthTech.in.ua](https://healthtech.in.ua/), [IT Ukraine HealthTech](https://itukraine.org.ua/en/ukraine-s-healthtech-industry-technological-challenges-and-the-path-to-european-integration/)
- [Lviv Medical Forum FB](https://www.facebook.com/Lviv.Medical.Forum/), [medforum.lviv.ua](https://www.medforum.lviv.ua/)
- [Medical Community Ukraine](https://www.facebook.com/medicalcommunity.ukraine/), [Ukrainian Society of Surgical Oncology](https://www.facebook.com/oncosurgery.ua/)
- [Facebook group rules 2026](https://groupboss.io/blog/facebook-group-rules/)
- Ukrainian medical-advertising law: [MITRAX overview](https://mitrax.ua/uk/blog/reklama-medichnih-zakladiv-poslug-ta-likarskih-zasobiv-yaki-vimogi-zakonodavstva-neobhidno-vrahuvati/), [Netpeak Meta UA/EU med-ads rules](https://netpeak.net/uk/blog/reklama-medposlug-u-google-ads-ta-meta-ex-facebook-ads-pravila-dlya-ukraini-ta-es/)

**Note on uncertainty:** I could not confirm the *internal* posting rules of any specific Ukrainian Facebook group or Telegram chat (they're behind join screens / pinned posts). For each, the maintainer must **read the current pinned rules and confirm with an admin before posting** — treat the per-venue rules above as "verify the current rule," not as settled fact.

---

## Review flags (unresolved)

- **Reddit clinical/medical subreddits**: MATURITY/NUMBERS CONSISTENCY: The draft uses "15 of ~806 entities" in three places. The brief's accurate facts are 92 diseases / 664 indications / 384 regimens / 444 cited sources, with "only 15 of 806 entities" sign-off. The 806 total isn't independently stated and risks reading as invented precision. Standardized the footer and bodies to the brief's exact figures and kept '15 of 806 entities' only as given, while ensuring it never undersells the STUB caveat. No maturity was overstated; if anything I reinforced the 'most content is STUB / not validated' framing.; DISCLOSURE EDGE CASE (r/medicine, r/AskDocs): The original text allowed the maintainer to seek/use verified-clinician flair. Tightened so it can never read as leveraging a clinical license to market: if the maintainer is a verified clinician they participate purely as a clinician and never mention the tool; flair must never be used for outreach. This closes an astroturfing/authority-leveraging gap.; AUTOMATION MISREAD RISK: The MCP line ('ChatGPT/Claude/Cursor can call the engine') is a legitimate product feature, but next to outreach it could be misread as autoposting. Added an explicit clause in the operating rules and post bodies clarifying the MCP server is a product capability and that all Reddit posting is done manually by the human maintainer — no automation, no bots, no scheduled posting.; SALESINESS / VALUE-FIRST: Original was already feedback-first; reinforced every greenlit template's ask as 'tear apart the clinical logic / tell me what's wrong' rather than signups, and moved links to the end so the post leads with substance, not a pitch.; CROSS-POST CADENCE: Reinforced the no-identical-cross-post rule and added explicit minimum spacing guidance so the two greenlit posts and the two ask-first posts are never mass-posted the same day with identical text.; FORBIDDEN-VENUE CLARITY: Confirmed and kept hard 'do NOT self-promote' verdicts for r/medicine, r/medicalschool, r/cancer, and r/AskDocs, with r/cancer and r/AskDocs flagged as patient-self-use safety risks (off-limits on ethics grounds, not just rules). No template provided for any forbidden venue.; RESEARCH-CAVEAT HONESTY: Kept the maintainer-facing instruction to live-verify each subreddit's current rule before posting, since per-sub rule text could not be machine-verified. This is correct and preserved.
- **Physician-verified networks**: Scale-number/STUB pairing (project's own pre-publish gate, disclaimer-checklist.md line 14): the Doximity template body cited '92 diseases, 664 indications, 384 regimens, 444 cited sources' with NO early-stage/STUB caveat in the same body text (it relied solely on the footer). Fixed by adding an in-body early-stage + STUB sentence next to the numbers in the Doximity template, matching how the Sermo and Medscape templates already do it. The Sermo and Medscape templates already paired maturity in-body and were left intact.; Op-Med framing risk (Doximity 1(a)): original text described an essay that 'mentions the project in passing as the author's own work, with no call to action' which read as a way to slip promotion past editors. Reframed to require explicit authorship disclosure and to honor Op-Med's no-promo/no-AI-drafting rules genuinely (a real topical essay the author writes themselves, disclosing they built the project, accepting editorial rejection) rather than treating disclosure as a loophole.; Consistency of 'verify the rule yourself first': made the 'confirm the current self-promo rule with mods/support in writing before posting' instruction explicit and uniform across all five venues, since Sermo/SDN/Figure 1/Medscape had it but the conditional venues benefit from one consistent standard.; Footer reinforcement: confirmed the standard medical-safety footer matches the project's disclaimer-checklist (not a medical device, not FDA-cleared, not validated, not for patient self-use, verify with a qualified oncologist, early-stage v0.1, 15/806 dual-signed-off). No change needed; verified accurate against promo/00-FACT-SHEET.md.; No autoposting / sockpuppet / astroturfing language was present to remove — the draft already mandated manual, self-disclosed, single-post-per-venue posting and explicitly forbade credential falsification. Left as-is and reinforced in the verification-barrier sections.; Venue prohibitions verified correct: SDN ('commercial use strictly prohibited', trainee audience) and Figure 1 ('refrain from promotional content', case-only) are correctly marked DO NOT POST promotionally, with no template offered for Figure 1 and a mod-permission-only minimal note for SDN. Left intact; tightened the wording to make the 'do not post' recommendation unambiguous.; Added an explicit note that all scale numbers are 'state 2026-06-17' so the maintainer dates them and does not present stale or future-shifted counts; the underlying figures already matched the canonical fact sheet exactly (92/664/384/444 and 15/806), so no numbers were changed.
- **Professional society / oncology forums**: §2 (ASH) template was missing the explicit 'not for patient self-use' clause from its medical-safety disclaimer — added it.; §3 (ESMO) working-group message omitted both 'not for patient self-use' and the 'verify with a qualified oncologist' line; even a semi-public working-group message must carry full medical-safety framing — added both, plus 'not FDA-cleared'.; §5 (verified-clinician contributor) template was missing 'not FDA-cleared' and 'not for patient self-use' — added both to complete the disclaimer.; §2 and §5 relied on 'assume restricted' for unverified policies but did not state the fail-safe default crisply; tightened to an explicit 'if you cannot confirm the rule allows it, do NOT post' instruction so the default action is non-posting, satisfying Rule 4.; Added a maintainer caution that even the quoted ASCO rules can drift and must be re-confirmed at posting time (policies change), so the maintainer never relies on a possibly-stale quote — without inventing any new policy text.; §4 (regional societies) cadence guidance said 'space outreach out' but did not cap concurrency clearly; reinforced 'one society at a time, confirm response before the next' to remove any mass-email reading.; Strengthened the §5 anti-sockpuppet language so the prohibition on borrowed/created accounts is stated as an absolute, not a 'do not' buried mid-paragraph.
- **Ukrainian / regional medical communities**: MEDICAL-SAFETY DISCLAIMER INCOMPLETE in 4 of 5 outreach templates. The canonical rule (promo/00-FACT-SHEET.md Safety rules + promo/community-outreach.md) requires BOTH halves in every public-facing message: 'not a medical device' AND 'every plan must be verified by a qualified oncologist', plus 'not FDA-cleared / not for direct patient use / not for emergency or time-critical decisions'. Only the oncoHUB email (1c) carried a near-complete version. Added the full mandatory one-line disclaimer to the oncoHUB (1c), UMSA (2c), eHealth (3c), and general-FB-group (5c) templates.; UMSA template (2c) was missing the explicit 'verify with a qualified oncologist' clause and 'not FDA-cleared' — added via the mandatory disclaimer line (translated to Ukrainian).; eHealth/HealthTech template (3c) had a tech-audience framing that named the maturity caveats but omitted the 'verify with a qualified oncologist' + 'not for patient use' clinical-safety clause — added via the mandatory disclaimer line.; General FB-group post template (5c) had strong safety language but omitted 'not FDA-cleared' and 'not for emergency/time-critical' — completed via the mandatory disclaimer line.; Added a top-of-document MANDATORY DISCLAIMER block (English + Ukrainian) so the maintainer has one canonical, fact-sheet-aligned safety line to append to every public post, matching the existing promo/community-outreach.md convention.; Strengthened the conference (Lviv/ГалМЕД, section 4) guidance to make explicit that any future talk/poster slide must also carry the not-a-medical-device + verify-with-oncologist disclaimer, since a conference presentation is a public medical-context communication.
