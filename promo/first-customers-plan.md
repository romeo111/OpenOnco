# OpenOnco — first customers plan

A concrete, implementable plan to get the **first real clinician users**. OpenOnco
is free, so "customer" = a clinician who **runs a real (de-identified) case and
gives feedback**, then comes back. That activation — not signups or stars — is
the goal.

> Honest framing throughout: OpenOnco is early-stage v0.1, most content STUB, not
> a medical device, not validated. The plan is built around that reality, not
> against it.

---

## 1. What counts as a "first customer" (activation)

**North-star activation event:** a clinician runs ≥1 case in the engine **and**
leaves one piece of feedback (an issue, a reply, a DM). A clinician who does that
twice is a retained user. Everything below optimizes for that, not vanity reach.

## 2. Who the realistic first users are (ICP for v0.1)

Be honest about trust: a v0.1, mostly-STUB tool will **not** win busy senior
oncologists at top academic centers yet. Go where curiosity is high and stakes
are low first, then climb the trust ladder:

1. **The maintainer's warm network** — hem/onc colleagues, ex-classmates, the
   Ukrainian oncology community. Highest trust, fastest yes. *Start here.*
2. **Trainees** — oncology/hematology residents & fellows. Curious, online,
   lower stakes, generous with feedback.
3. **Clinical-informatics / AI-in-medicine people** — they try tools and give
   sharp technical feedback; many are also clinicians.
4. **LMIC / rural oncologists** — where free + offline + cited is most valuable;
   reachable via Project ECHO-style networks, HIFA, regional societies.
5. **Open-source / dev-clinician hybrids** — via the OSS + MCP angle.

## 3. The funnel (and where each step is strengthened)

`Reach (warm, disclosed) → Try (a case they know) → Feedback (low friction) → Close the loop (respond/fix/credit) → Retain + refer`

- **Reach:** warm intros first; then disclosed posts in *receptive* communities
  (see `clinician-community-outreach-playbook.md`). Never spam.
- **Try:** the in-browser demo (`try.html`) — no install, no PHI. Hand them a
  *specific* case to run (one they'll recognize), not "go try it."
- **Feedback:** a one-click GitHub issue template (added in this PR) — and for
  clinicians without GitHub, accept a reply by email/DM and file it yourself.
- **Close the loop:** respond within 48h, fix what's real, **credit them by
  name** (with permission), and tell them it's fixed. This is what turns a
  one-time trier into an advocate.
- **Retain + refer:** convert the sharpest critics into **Clinical Co-Leads**
  (template added) — that simultaneously fixes the trust/maturity bottleneck.

## 4. Four-week implementable sequence

### Week 0 — funnel prep  ✅ implemented in this PR
- [x] **Clinician-feedback issue template** — `.github/ISSUE_TEMPLATE/clinician_feedback.md`
- [x] **Clinical Co-Lead application template** — `.github/ISSUE_TEMPLATE/co_lead_application.md`
- [x] **Issue triage config** routing people to the demo first — `.github/ISSUE_TEMPLATE/config.yml`
- [x] Warm-network message + pilot offer (§5–§6 below)
- [x] "Hand them a case" list (§7)

### Week 1 — warm network  ▶ you
Message 10–20 hem/onc contacts directly (DM/email/Signal) with §5. Ask for one
concrete thing: *run this one case, tell me where it's wrong.*
**Target:** 5 run a case, 3 leave feedback. Reply to every one within 48h.

### Week 2 — receptive communities  ▶ you (disclosed, manual)
One post each, spaced out, in the venues marked receptive in the outreach
playbook: clinical-informatics / AI-in-medicine, MedTwitter (#hemonc), the
Ukrainian clinician community, r/healthIT or r/clinicalresearch. Lead with "I
built this and want clinicians to tear the logic apart."

### Week 3 — one pilot  ▶ you
Offer **one** department / tumor board / training program a structured 2-week
look (§6). A single engaged pilot beats broad reach: it produces deep feedback,
a testimonial, and possibly a Co-Lead.

### Ongoing — the loop
Close every feedback item fast, credit contributors, and recruit Co-Leads. Track
the metrics in §8 weekly.

## 5. Warm-network message (paste & personalize)

> Hi [name] — I built a free, open-source tool that drafts oncology treatment
> options with a citation on every line. It's deliberately *not* an LLM guessing
> — a deterministic rule engine over guideline sources drafts two plans for you
> to verify. It's early and I need clinicians to poke holes.
>
> Could you spend 5 minutes on one case you know cold? Open
> https://openonco.info/try.html (runs in your browser, nothing leaves your
> device — use a de-identified case), pick e.g. [a disease you treat], and tell
> me the first thing that's wrong or missing? That single reply is hugely useful.
>
> It's informational support, not a medical device — everything still needs an
> oncologist to verify. Thank you 🙏

## 6. Pilot offer one-pager (for a department / tumor board)

- **What:** a 2-week, no-cost look at OpenOnco on your own de-identified cases.
- **You get:** drafted, fully-cited two-option plans to react to; a direct line
  to fix anything wrong; optional co-authorship/credit and a Co-Lead seat.
- **We get:** honest clinical feedback to harden the engine.
- **Boundaries:** informational support only, not a medical device; no real PHI
  in the public tool; every output verified by your team. Runs offline/in-browser.
- **Ask:** 2–3 clinicians, ~1 hour/week, for two weeks.

## 7. Hand them a case (lower "try" friction)

Don't say "go try it." Send a clinician a case they'll recognize and the demo
link. Good starters (all synthetic): DLBCL first-line, follicular lymphoma, CLL,
multiple myeloma, gastric, NSCLC, CRC — load these from the example picker on
[try.html](https://openonco.info/try.html). "Run the DLBCL 1L case and check the
track split + citations" converts far better than a generic invite.

Note the two surfaces differ: `/gallery.html` is a small curated set built around
the CIViC/ESCAT actionability layer (NSCLC, CRC, breast, ovarian, prostate,
melanoma, gastric/GEJ, cholangiocarcinoma, endometrial, cervical, thyroid, GIST,
AML, BCC, infantile fibrosarcoma) and does **not** include the hematology
starters above. Link the picker when you name a heme case, or the clinician will
land on a gallery that doesn't have it.

## 8. Metrics (activation-first, honest)

| Metric | What it tells you | Target (first month) |
|---|---|---|
| Clinician-feedback issues | real clinical scrutiny — the #1 signal | 5+ |
| Clinicians who ran ≥1 case | top-of-activation | 15+ |
| Repeat clinician users | retention | 3+ |
| Co-Lead applications | trust + the maturity unlock | 1–2 |
| Demo visits to try.html | reach → try conversion | track trend |
| GitHub stars/forks | passive interest (secondary) | — |

**Anti-metric:** vanity reach with no clinical engagement. One sharp "your logic
here is wrong because…" from a real oncologist beats 100 stars.

## 9. What I implement vs. what needs you

| Action | Who |
|---|---|
| Feedback + Co-Lead issue templates, triage config | **done (this PR)** |
| Warm-network message, pilot one-pager, case list | **done (this PR)** |
| Community/registry/funding assets (other promo/ files) | done earlier |
| DM/email the warm network; post in communities; run the pilot | you |
| Respond to feedback, credit contributors, recruit Co-Leads | you |
| A non-GitHub feedback form (e.g. Tally/Google Form) | you create it; I'll wire the link into the site + config |

If you set up a simple feedback form and a sponsor/fiscal-host handle, tell me
and I'll wire both into the repo/site.
