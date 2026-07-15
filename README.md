# OpenOnco

[![Code license: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Latest release](https://img.shields.io/github/v/release/romeo111/OpenOnco)](https://github.com/romeo111/OpenOnco/releases)
[![Website](https://img.shields.io/badge/site-openonco.info-14532d.svg)](https://openonco.info)
[![MCP server](https://img.shields.io/badge/MCP-server-7c3aed.svg)](mcp_server/README.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/romeo111/OpenOnco/compare)
[![Stars](https://img.shields.io/github/stars/romeo111/OpenOnco?style=social)](https://github.com/romeo111/OpenOnco/stargazers)

> **Open-source clinical decision support for oncology tumor boards.**
> Upload a patient profile → get two alternative treatment plans
> (standard + aggressive), side by side, with every recommendation cited.
> Plans refresh as new data arrives. All clinical logic lives in a
> declarative rule engine over a curated knowledge base — **no LLM
> picks regimens** ([CHARTER §8.3](specs/CHARTER.md)).

**Live demo:** **[openonco.info](https://openonco.info)** — try it in the browser, no install needed.
**Knowledge base:** 92 diseases · 664 indications · 444 cited sources across hematologic + solid-tumor oncology (growing). Most content is draft/STUB pending two-reviewer clinical sign-off.
**FDA non-device CDS positioning** per [CHARTER §15](specs/CHARTER.md) — informational support tool, not a medical device.
**License:** Code MIT · Content / specs CC BY 4.0.

---

## Why this exists

Picking a regimen for a real patient is **2–4 hours of manual desk work**: open NCCN PDF, cross-check ESMO, re-read the local МОЗ protocol, verify formulary reimbursement, look up renal/hepatic dose adjustments, layer supportive care, remember vaccinations and OI prophylaxis. Every patient. One missed contraindication can be fatal.

OpenOnco automates the chore work. The clinician gets a **drafted plan with every citation already attached** and only verifies / tailors it. The logic mirrors a **classical multidisciplinary tumor board (MDT)** — each "virtual specialist" is a versioned rule module with its own sources and `last_reviewed` stamp.

→ Live KB metrics, per-disease coverage, sign-off ratio: **[openonco.info/capabilities](https://openonco.info/capabilities.html)**

---

## What it does

- **Two-track plan generator.** Always ≥2 alternative tracks side by side — never a single "system-prescribes-X" output. Each track ships rationale, red-flag triggers, hard contraindications, supportive care, monitoring schedule, sourced outcome numbers, and a "what NOT to do" list.
- **Versioned MDT skill registry.** Hematology, hematopathology, ID/hepatology, radiology, molecular genetics, clinical pharmacy, radiation oncology, surgical oncology, transplant, CAR-T, and more — each a versioned rule bundle with `last_reviewed`, `clinical_lead`, and reviewer sign-offs.
- **Diagnostic-phase MDT.** No histology → Workup Brief, never a treatment Plan.
- **Plan revisions / supersedes loop.** Immutable audit chain; refuses illegal downgrades.
- **ESCAT + CIViC actionability.** Biomarker × disease × drug evidence tiers surfaced as render badges. CIViC (CC0) is the primary actionability source.
- **HTML render layer.** Single-file A4-printable HTML per Plan / Diagnostic Brief / Revision Note. Patient-mode and HCP-mode. UA / EN.
- **In-browser Pyodide demo.** The actual Python engine runs in the browser — no backend, no patient data leaves the device.

---

## Try it

**Clinicians:** **[openonco.info/try.html](https://openonco.info/try.html)** — paste a patient JSON profile and the Pyodide-loaded engine generates a treatment plan. No installation required, no PHI server-side.

**Tumor-board questions:** **[openonco.info/ask.html](https://openonco.info/ask.html)** — optional server-backed prototype for free-text oncology vignettes. ChatGPT structures the case, OpenOnco runs the deterministic rule engine, then the response is framed as an answer, alternatives, or clarifying questions. Do not paste identifiable real-patient data.

**Sample patients:** **[openonco.info/gallery.html](https://openonco.info/gallery.html)** — pre-rendered cases across DLBCL, FL, CLL/SLL, MCL, MZL, MM (hematologic) and gastric, esophageal, PDAC, cholangiocarcinoma, CRC, NSCLC, SCLC, mesothelioma (solid tumors).

**Contributors:** start with [`specs/`](specs/) and [`CLAUDE.md`](CLAUDE.md) — these define scope, schemas, and authoring conventions before any KB or code change.

**AI-assisted contributions:** OpenOnco accepts distributed contributor work through the [TaskTorrent chunk-shelf](https://github.com/romeo111/task_torrent/tree/main/chunks/openonco). Read [`docs/contributing/HELP_WANTED.md`](docs/contributing/HELP_WANTED.md) — pick an active `[Chunk]` issue, run with your AI tool, submit a sidecar PR. Safety boundaries: no medical advice, no treatment recommendations, no patient-specific outputs; everything reviewed before merge.

**Developers:**

```bash
git clone https://github.com/romeo111/OpenOnco.git
cd OpenOnco
pip install -e .
python scripts/audit_validator.py --human
pytest tests/
```

Python 3.11+ required.

---

## Use it from your LLM (MCP)

Doing oncology research inside ChatGPT, Claude, or a Cursor agent? Don't let the
model answer treatment questions from memory — point it at OpenOnco's
deterministic engine instead. The **[MCP server](mcp_server/README.md)** exposes
the engine as tools any [Model Context Protocol](https://modelcontextprotocol.io)
client can call:

```bash
pip install -e ".[mcp]"
python -m mcp_server.server          # stdio server for Claude Desktop, Cursor, …
```

Tools: `engine_info`, `list_diseases`, `generate_treatment_plan`,
`generate_diagnostic_brief`. The model calls the rule engine, then relays its
**cited** tracks and the disclaimer — it never picks the regimen itself
([CHARTER §8.3](specs/CHARTER.md)). That is what makes routing an oncology
question through OpenOnco safer than asking a general-purpose model directly: the
engine cannot hallucinate a drug or a dose. Setup for Claude Desktop / Cursor is
in **[`mcp_server/README.md`](mcp_server/README.md)**.

---

## Build your own

OpenOnco is fully open source — code MIT, content/specs CC BY 4.0 — precisely so
others can reuse or fork it. The replicable pattern, for any safety-critical
decision-support domain: keep clinical decisions in a **declarative rule engine
over a versioned, human-reviewed knowledge base**, cite every claim, and use the
LLM only as a relay/interface behind an explicit "no decisions" invariant. Start
from [`specs/CHARTER.md`](specs/CHARTER.md) and the architecture in
[`specs/`](specs/), and copy [`mcp_server/`](mcp_server/) as a working interface
layer. Questions or a similar project in flight? [Open an
issue](https://github.com/romeo111/OpenOnco/issues) — we'd rather coordinate
than have the work duplicated.

---

## How to contribute

**Try it and tell us what's wrong.** A clinician's eye on a rendered Plan is the most valuable contribution right now. Try the [demo](https://openonco.info/try.html) on a case you know, then **[open a clinical-feedback issue](https://github.com/romeo111/OpenOnco/issues/new?labels=clinical-feedback)** — even one line ("this regimen is missing the CrCl <30 dose adjustment") helps.

**Add a disease or fix a regimen.** KB is YAML under `knowledge_base/hosted/content/`. Read [`specs/CLINICAL_CONTENT_STANDARDS.md`](specs/CLINICAL_CONTENT_STANDARDS.md) for citation format and [`specs/REDFLAG_AUTHORING_GUIDE.md`](specs/REDFLAG_AUTHORING_GUIDE.md) for RedFlags (≥2 Source citations required). New clinical content stays `draft` / `proposed` / `partial` / `stub_full_chain` until two of three Clinical Co-Leads sign off ([CHARTER §6.1](specs/CHARTER.md)) — **never set `reviewed: true` yourself.**

**Engine / render / infrastructure.** Standard PR — `pytest` must pass, new code needs tests. Schema and spec changes go through CHARTER §6 review.

**Become a Clinical Co-Lead.** Hematology / oncology / clinical pharmacology sub-specialty depth needed to dual-sign content out of STUB. **[Open a PR](https://github.com/romeo111/OpenOnco/compare)** that adds your name + area + CV / public profile link to [`specs/CLINICAL_LEADS.md`](specs/CLINICAL_LEADS.md), or **[open an issue](https://github.com/romeo111/OpenOnco/issues/new?labels=co-lead-application&title=Co-Lead+application:+%5Byour+area%5D)** with the same — public audit trail by design.

---

## Specifications

All specifications live in [`specs/`](specs/) (Ukrainian, English technical terms inline). **Read [`CHARTER.md`](specs/CHARTER.md) first** — it governs scope, FDA positioning, dual-review process, and what the project explicitly does **not** do.

Key specs: [`CLINICAL_CONTENT_STANDARDS`](specs/CLINICAL_CONTENT_STANDARDS.md) · [`KNOWLEDGE_SCHEMA_SPECIFICATION`](specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md) · [`SOURCE_INGESTION_SPEC`](specs/SOURCE_INGESTION_SPEC.md) · [`REDFLAG_AUTHORING_GUIDE`](specs/REDFLAG_AUTHORING_GUIDE.md).

---

## Medical disclaimer

OpenOnco is an **informational resource** to support tumor-board discussion. It is **not** a system that makes clinical decisions, **not** a medical device, and **not** for use without a qualified oncologist. Every recommendation must be verified by the treating physician with access to the full clinical picture and discussed by a multidisciplinary team. See [`specs/CHARTER.md`](specs/CHARTER.md) §11 + §15 for the full positioning statement.

---

## License

- **Code:** MIT.
- **Specifications & generated content:** CC BY 4.0.
- **Source citations** retain their original licenses — NCCN, ESMO, EHA, BSH, EASL, МОЗ України НСЗУ, etc. are **referenced, not redistributed** ([CHARTER §2](specs/CHARTER.md) non-commercial scope; many source licenses depend on this).

---

**Oncologist or clinical pharmacologist?** [Try the demo](https://openonco.info/try.html) on a case you know, then [open an issue](https://github.com/romeo111/OpenOnco/issues/new?labels=clinical-feedback) with what you'd change. That's the loop we're optimizing for.
