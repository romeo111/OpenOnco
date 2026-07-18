# OpenOnco — Cold Outreach Drafts

> **Maintainer note (not for sending):** Every message below frames OpenOnco honestly as an early-stage v0.1 open-source draft, addresses healthcare professionals / builders (never patients), and leads with the rules-first/no-LLM-decides differentiator. **The one-line disclaimer below is appended to every message and is mandatory — do not remove it.** Most clinical content is STUB (only 15 of 1061 entities have two-reviewer sign-off) — that caveat is built into each ask. Use only the five canonical links. Personalize the bracketed `[…]` fields before sending.

**Canonical links to use:**
- Site: https://openonco.info
- Repo: https://github.com/romeo111/OpenOnco
- In-browser demo: https://openonco.info/try.html
- MCP server: https://github.com/romeo111/OpenOnco/tree/main/mcp_server
- llms.txt: https://openonco.info/llms.txt

**Mandatory one-line disclaimer (already appended to every message below — keep it):**
> OpenOnco is an informational clinical decision support tool for healthcare professionals — not a medical device, not FDA-cleared, not for direct patient use, not for emergency or time-critical decisions, and every plan it drafts must be verified by a qualified oncologist.

---

## 1. CIViC / clinical-genomics community (WashU, CIViC curators, ClinGen-adjacent)

**Why relevant:** OpenOnco reads actionability evidence directly from CIViC (CC0) as its primary variant-interpretation source, via a local nightly snapshot, and surfaces ESCAT tiers as a badge. This community is both the upstream data source and the most credible reviewer of how that data is being consumed downstream.

**The ask:** A sanity-check on how we consume and attribute CIViC, plus any pointers on edge cases (fusion matching, evidence-level mapping). Optionally, a mention to curators who care about real-world reuse.

**Message:**

> Subject: OpenOnco — an open CDS engine built on CIViC, would value a sanity-check
>
> Hi [name],
> I maintain OpenOnco (https://openonco.info), a free, open-source clinical decision support tool for oncologists and tumor boards. It uses a deterministic rule engine over a versioned, source-cited knowledge base to draft two alternative treatment tracks for a clinician to verify — no LLM ever picks a regimen or dose. Actionability evidence comes from CIViC (CC0) as our primary source, read from a local nightly snapshot, with ESCAT surfaced as a badge. We attribute on every claim and don't redistribute upstream guidelines. It's an early-stage v0.1 draft — most clinical entities are still STUB and there's been no formal validation — so I'd genuinely value a quick check that we're consuming and crediting CIViC the right way (especially fusion-aware matching and evidence-level mapping). Code is here if useful: https://github.com/romeo111/OpenOnco.
>
> OpenOnco is an informational clinical decision support tool for healthcare professionals — not a medical device, not FDA-cleared, not for direct patient use, not for emergency or time-critical decisions, and every plan it drafts must be verified by a qualified oncologist.

---

## 2. OHDSI community (OMOP / observational health data science)

**Why relevant:** OHDSI cares about standardized vocabularies (we code drugs with ATC/RxNorm), transparent and reproducible analytics, and open methods. OpenOnco's deterministic, reproducible engine (same input + same KB version = same output) and standards-based input (FHIR/mCODE) speak that language.

**The ask:** Feedback in the relevant forum/working group on the vocabulary mapping and on whether the deterministic-engine pattern is interesting to the community; not asking for endorsement.

**Message:**

> Subject: Reproducible, rules-first oncology CDS over a cited KB — feedback welcome
>
> Hi OHDSI community,
> I wanted to share OpenOnco (https://openonco.info), an open-source oncology clinical decision support project that may resonate with this group's values. A clinician feeds it a FHIR/mCODE-shaped patient profile and a deterministic rule engine returns two alternative treatment tracks side by side, each with a step-by-step decision trace and a source citation on every claim — clinical logic lives in declarative rules over a versioned, human-reviewed knowledge base, not in an LLM. Output is reproducible (same input + same KB version = same plan), drugs are coded with ATC/RxNorm, and it runs locally so patient JSON never leaves the machine. It's explicitly early-stage (v0.1, most content still STUB, no formal validation yet), so I'm sharing it for critique rather than adoption — I'd especially welcome feedback on the vocabulary mapping and the reproducibility model. Code (MIT) and content (CC BY 4.0): https://github.com/romeo111/OpenOnco.
>
> OpenOnco is an informational clinical decision support tool for healthcare professionals — not a medical device, not FDA-cleared, not for direct patient use, not for emergency or time-critical decisions, and every plan it drafts must be verified by a qualified oncologist.

---

## 3. Open-source-in-medicine groups (e.g. Open Source in Healthcare / medicine mailing lists, relevant subreddits, "awesome-*" maintainers)

**Why relevant:** Fully open (code MIT, content CC BY 4.0), privacy-by-design, forkable as a general pattern for safety-critical rules-first decision support. This is exactly the kind of project these communities catalog and discuss.

**The ask:** A look / possible inclusion in a list or discussion thread, and design feedback on the rules-first + citation-guard pattern.

**Message:**

> Subject: OpenOnco — open-source, rules-first oncology decision support (MIT / CC BY)
>
> Hi [name / group],
> Sharing a project that fits this community: OpenOnco (https://openonco.info), a free and fully open-source clinical decision support tool for oncologists and tumor boards. The design choice I'd most like feedback on: all clinical logic is a deterministic rule engine over a versioned, human-reviewed knowledge base — no LLM picks the regimen or dose, so it can't hallucinate a drug — and every recommendation carries a source citation enforced by a 3-layer citation guard. It always shows two alternative tracks side by side (never one binding directive) to counter automation bias, runs locally/in-browser so patient data never leaves the device, and is built to be forked for any safety-critical decision-support domain. Honest status: it's an early-stage v0.1 draft, most entities are STUB pending two-reviewer clinical sign-off, and there's no formal validation study yet. Repo: https://github.com/romeo111/OpenOnco — happy to be cataloged or torn apart in a thread.
>
> OpenOnco is an informational clinical decision support tool for healthcare professionals — not a medical device, not FDA-cleared, not for direct patient use, not for emergency or time-critical decisions, and every plan it drafts must be verified by a qualified oncologist.

---

## 4. AI-in-oncology newsletters / writers

**Why relevant:** OpenOnco is a counter-example to "let the LLM recommend treatment": it deliberately keeps the LLM out of the clinical decision and routes questions through a deterministic engine — a concrete, opinionated take on safe AI in oncology that's newsletter-worthy.

**The ask:** Consideration for a mention/write-up, with full honesty about maturity; offer to answer questions or give a walkthrough.

**Message:**

> Subject: A deliberately "AI-doesn't-decide" oncology CDS tool — possible story
>
> Hi [name],
> Given your coverage of AI in oncology, OpenOnco (https://openonco.info) might interest you precisely because of what it refuses to do. It's a free, open-source clinical decision support tool for oncologists and tumor boards where no LLM ever picks the regimen or dose — clinical logic is a deterministic rule engine over a versioned, source-cited knowledge base, and it always drafts two alternative tracks side by side for a clinician to verify, never a single directive. There's an MCP server so an LLM (Claude, Cursor, etc.) can route an oncology question through the engine and relay cited output instead of answering from memory. I want to be upfront: it's an early-stage v0.1 project with a 103-disease cited KB but only 15 of 1061 entities dual-reviewer signed off and no formal clinical validation — so the honest framing is "a safety-first design pattern actively seeking clinician feedback," not a finished product. Happy to give you a walkthrough or answer anything: try it at https://openonco.info/try.html (synthetic cases only).
>
> OpenOnco is an informational clinical decision support tool for healthcare professionals — not a medical device, not FDA-cleared, not for direct patient use, not for emergency or time-critical decisions, and every plan it drafts must be verified by a qualified oncologist.

---

## 5. MCP / Claude developer communities (MCP servers directory, Claude/Cursor dev forums, Discord)

**Why relevant:** OpenOnco ships an MCP server exposing `engine_info`, `list_diseases`, `generate_treatment_plan`, `generate_diagnostic_brief` — a clean real-world example of MCP used to make an LLM *safer by construction* (the model relays deterministic, cited engine output instead of guessing).

**The ask:** Try the MCP server, feedback on the tool design, optional listing in MCP directories.

**Message:**

> Subject: MCP server that makes an LLM route oncology questions through a deterministic engine
>
> Hi [name / community],
> Sharing an MCP server you might find interesting as a pattern: OpenOnco (https://github.com/romeo111/OpenOnco/tree/main/mcp_server) exposes a deterministic oncology decision-support engine to any MCP client (Claude Desktop, Cursor, etc.) via four tools — engine_info, list_diseases, generate_treatment_plan, generate_diagnostic_brief. The point is safety-by-construction: the LLM never picks a regimen or dose itself; it relays cited output from a deterministic rule engine over a versioned, human-reviewed knowledge base, so it can't hallucinate a drug. The engine runs locally/offline (~50-200 ms per profile) and is reproducible. Fair warning — it's an early-stage v0.1 project (informational CDS for clinicians, not a medical device, not for patient use) with most clinical content still pending review, so treat it as a reference implementation rather than something production-ready. Would love feedback on the tool surface and whether it's worth listing in MCP directories.
>
> OpenOnco is an informational clinical decision support tool for healthcare professionals — not a medical device, not FDA-cleared, not for direct patient use, not for emergency or time-critical decisions, and every plan it drafts must be verified by a qualified oncologist.

---

## 6. Ukrainian medical / health-tech community (UA med-tech groups, UA oncology/hematology societies, UA open-source/dev meetups)

**Why relevant:** The project has Ukrainian roots, references Ukraine MoH/NSZU guidelines among its sources, and keeps Ukrainian-language originals in the repo. This community can give clinically grounded feedback and reflects the project's origin.

**The ask:** Clinician feedback (try a known case in the demo), and contributors for drafting/verification via the chunk workflow.

**Message (English — translate to Ukrainian before sending; translate the disclaimer too):**

> Subject: OpenOnco — open-source oncology decision support with Ukrainian roots, seeking clinician feedback
>
> Hello [name / group],
> I'm reaching out because OpenOnco (https://openonco.info) has Ukrainian roots and I'd value this community's eyes on it. It's a free, open-source clinical decision support tool for oncologists and tumor boards: a clinician enters a structured patient profile and a deterministic rule engine drafts two alternative treatment tracks side by side, each with a source citation on every claim — no LLM ever picks the regimen or dose. It references guideline sources including Ukraine MoH/NSZU alongside NCCN, ESMO, EHA and others, runs locally so patient data never leaves the machine, and is honest about being early-stage (v0.1, most content still STUB pending two-reviewer sign-off, no formal validation yet). The single most useful thing right now: try the in-browser demo on a case you know well and tell me what's wrong — https://openonco.info/try.html (synthetic cases only). If you'd like to help draft or verify clinical content, there's an AI-assisted "chunk" contribution workflow in the repo, and all clinical content is reviewed by clinical leads before merge: https://github.com/romeo111/OpenOnco.
>
> OpenOnco is an informational clinical decision support tool for healthcare professionals — not a medical device, not FDA-cleared, not for direct patient use, not for emergency or time-critical decisions, and every plan it drafts must be verified by a qualified oncologist.

---

## 7. Researchers / clinicians wanting a transparent, auditable oncology logic reference (academic CDS / clinical informatics lists)

**Why relevant:** OpenOnco offers a fully transparent, source-grounded, auditable oncology logic layer: step-by-step decision trace, FDA Criterion-4 metadata block, reproducible output, citation on every claim — useful as a reference even before it's a validated product.

**The ask:** Use it as a transparent reference / teaching artifact, and critique the auditability model (decision trace, citation guard, two-track design).

**Message:**

> Subject: A transparent, fully-cited oncology decision-logic reference (open source)
>
> Hi [name],
> If you work on clinical decision support or clinical informatics, OpenOnco (https://openonco.info) may be a useful reference even in its current early form. It's an open-source oncology CDS engine where every recommendation is traceable: a step-by-step decision trace accompanies each plan, every claim carries a source citation (enforced by a 3-layer citation guard), output is reproducible, and the clinical logic is declarative rules over a versioned, human-reviewed knowledge base rather than an LLM — by design it presents two alternative tracks side by side to counter automation bias, and it returns a diagnostic workup brief instead of a treatment plan when histology isn't confirmed. I want to be transparent about maturity: it's a v0.1 draft, only 15 of 1061 clinical entities have two-reviewer sign-off, and there's been no formal clinical validation study — so I'm sharing it as an auditable design reference and would welcome critique of the trace/citation/two-track model. Code and specs (MIT / CC BY 4.0): https://github.com/romeo111/OpenOnco.
>
> OpenOnco is an informational clinical decision support tool for healthcare professionals — not a medical device, not FDA-cleared, not for direct patient use, not for emergency or time-critical decisions, and every plan it drafts must be verified by a qualified oncologist.

---

### Sending checklist (maintainer reference, do not send)
- [ ] Personalized the `[name / group]` fields and picked the right channel per target.
- [ ] Confirmed only the five canonical links appear; no invented URLs.
- [ ] **Full disclaimer present in the message body** (both halves: not-a-medical-device AND verify-with-a-qualified-oncologist); audience framed as HCP/builders, never patients.
- [ ] Maturity stated (v0.1, STUB majority, no formal validation) in every message.
- [ ] No forbidden claims (no "validated," "FDA-cleared," "diagnoses," "prescribes," "AI picks treatment," OncoKB/SNOMED/MedDRA as sources).
- [ ] Ukrainian message AND its disclaimer translated before sending.
