# OpenOnco — MCP Registry & Directory Listings

**Asset:** `mcp-registries`
**Purpose:** Get the OpenOnco MCP server listed in the major public Model Context Protocol directories.
**Server path:** `https://github.com/romeo111/OpenOnco/tree/main/mcp_server`
**State:** 2026-06-17 KB figures · v0.1 draft

> **Read before submitting.** OpenOnco is informational clinical decision support for healthcare professionals and tumor boards — **not a medical device, not FDA-cleared/approved, not clinically validated, not for patients, not for emergencies.** No LLM ever picks the regimen or dose. Every listing below already bakes the not-a-medical-device framing into its blurb. Do not edit a blurb in a way that drops the disclaimer, implies validation/approval, or implies an LLM chooses treatment. When a directory has a hard character limit that won't fit the disclaimer, use the short form (below) and make sure the linked README/site carries the full disclaimer — which it does.

---

## Canonical copy blocks (reuse verbatim)

These are pre-cleared against the fact sheet's `approved_claims`, `forbidden_claims`, and `safety_rules`. Pick the one that fits each registry's length limit.

**Name:** `OpenOnco`

**One-line (≈ 100 chars):**
> Rules-first, source-cited oncology CDS for clinicians — drafts two treatment plans; no LLM picks the regimen.

**Short blurb (≈ 250 chars):**
> Free, open-source clinical decision support for oncology tumor boards. A deterministic rule engine over a versioned, fully source-cited knowledge base drafts two alternative treatment plans (standard + aggressive) for the treating oncologist to verify. No LLM picks the regimen or dose. Informational support, not a medical device. Early-stage (v0.1).

**Long blurb (no hard limit):**
> OpenOnco is a free, open-source, informational clinical decision support resource for oncologists, hematologists, and tumor boards. Feed it a structured FHIR/mCODE-shaped patient profile and a deterministic rule engine returns two alternative treatment tracks side by side (a standard track and a more aggressive track), each with regimen, supportive care, contraindications, monitoring, a step-by-step decision trace, and a source citation on every claim. If histology isn't confirmed, it returns a diagnostic workup brief instead of a treatment plan.
>
> The MCP server exposes this engine to any Model Context Protocol client (Claude Desktop, Cursor, etc.) via `engine_info`, `list_diseases`, `generate_treatment_plan`, and `generate_diagnostic_brief`. The LLM relays cited engine output — **it never picks the regimen or dose itself**, so it can't hallucinate a drug or dose. The engine is deterministic (same input + same KB version = same output) and runs offline; patient JSON never leaves the user's machine.
>
> Covers 92 diseases across hematologic and solid-tumor oncology with 444 cited sources (state 2026-06-17). Code is MIT; specs and generated content are CC BY 4.0.
>
> **This is an early-stage v0.1 draft, actively seeking clinician feedback. It is informational support for healthcare professionals — not a medical device, not FDA-cleared/approved, not clinically validated, and not for direct patient use or time-critical decisions. Most clinical content is STUB (only 15 of 806 entities have two-reviewer sign-off). Every output must be verified by a qualified oncologist.**

**Categories / tags (reuse across registries that accept them):**
`healthcare` · `clinical-decision-support` · `oncology` · `medical` · `knowledge-base` · `deterministic` · `rules-engine` · `research`

**Links (use ONLY these five — do not invent URLs):**
- Site: `https://openonco.info`
- Repo: `https://github.com/romeo111/OpenOnco`
- MCP server: `https://github.com/romeo111/OpenOnco/tree/main/mcp_server`
- In-browser demo: `https://openonco.info/try.html`
- `llms.txt`: `https://openonco.info/llms.txt`

**Tools to declare (exact names, verified in `mcp_server/server.py`):**
`engine_info`, `list_diseases`, `generate_treatment_plan`, `generate_diagnostic_brief`

---

## At-a-glance: what each registry needs

| Registry | Mechanism | Outward action required? | Who acts |
|---|---|---|---|
| Official MCP Registry (`registry.modelcontextprotocol.io`) | `server.json` + `mcp-publisher` CLI (GitHub auth) | **Yes — auth-gated publish** | Maintainer |
| `punkpeye/awesome-mcp-servers` | PR to README | **DONE — PR [#8276](https://github.com/punkpeye/awesome-mcp-servers/pull/8276) open** | — |
| PulseMCP | Web form / submit page (auto-enriches from GitHub) | **Yes — web form** | Maintainer |
| Glama | Auto-indexes public GitHub repos; can claim/submit | Mostly automatic; **optional submit/claim** | Maintainer (optional) |
| mcp.so | Web "Submit" form | **Yes — web form** | Maintainer |
| Smithery | Connect GitHub + add `smithery.yaml`; deploys/indexes | **Yes — repo config + connect** | Maintainer |

> **All six require an outward action by the maintainer** (account, PR, or form submission) — Claude cannot submit these. Glama is the only one that may list the repo automatically without any submission, but claiming/curating it is still a maintainer action. Verify each registry's current `CONTRIBUTING`/submission rules at submission time, since formats change.

---

## 1. Official MCP Registry (`registry.modelcontextprotocol.io`)

> **Updated 2026-06-18:** `modelcontextprotocol/servers` is now **reference-servers-only**
> (its README explicitly houses just the steering-group's reference servers).
> **Do NOT open a README PR there for a community server — it will be declined.**
> Community servers now live in the **official MCP Registry**.

- **Registry:** `https://registry.modelcontextprotocol.io`
- **Mechanism:** add a `server.json` manifest to the repo (registry schema; namespace
  like `io.github.romeo111/openonco`) and publish with the GitHub-authenticated
  `mcp-publisher` CLI (or a GitHub Action). **Auth-gated → maintainer action.**
- **Auto-index?** No — requires the maintainer to authenticate and publish.

**Steps (maintainer):**
1. Add a `server.json` to the repo (server root or `mcp_server/`) per the current
   registry schema, declaring the four tools and the start command
   (`python -m mcp_server.server`). Open it as a normal feature-branch PR into
   OpenOnco (never commit to `master`).
2. Install the `mcp-publisher` CLI, authenticate with GitHub (proves ownership of
   the `io.github.romeo111` namespace), and `mcp-publisher publish`.
3. Verify the listing surfaces the disclaimer-bearing description and the canonical
   links; use the **short blurb** for the description.
4. Confirm the schema/CLI names against the current registry docs at submission
   time — the registry is young and its tooling changes.

**Prerequisite:** the registry's `packages` entries point at a real package
registry (PyPI/npm/OCI/…). OpenOnco currently runs from source, so **publish the
`openonco` package to PyPI first** (maintainer's PyPI account) — then the
manifest below validates. Alternatively declare a `remotes` HTTP transport if a
hosted endpoint is stood up.

**Draft `server.json` (validate with `mcp-publisher` before publishing):**
```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
  "name": "io.github.romeo111/openonco",
  "description": "Rules-first, source-cited oncology clinical decision support; deterministic engine drafts two cited treatment plans for a clinician to verify (no LLM picks the regimen). Informational, not a medical device.",
  "version": "0.1.3",
  "packages": [
    {
      "registryType": "pypi",
      "registryBaseUrl": "https://pypi.org",
      "identifier": "openonco",
      "version": "0.1.3",
      "runtimeHint": "uvx",
      "transport": { "type": "stdio" }
    }
  ]
}
```
The package's console entry point must launch `mcp_server.server` (add a
`[project.scripts]` entry, e.g. `openonco-mcp = "mcp_server.server:main"`, before
publishing to PyPI).

---

## 2. `punkpeye/awesome-mcp-servers`

- **Repo:** `https://github.com/punkpeye/awesome-mcp-servers`
- **Mechanism:** Pull request adding a one-line entry under the appropriate category heading.
- **Auto-index?** No. **Outward action: open a PR.**

**Steps (maintainer):**
1. Fork the repo and read `CONTRIBUTING.md` — it specifies the line format (emoji legend for language/scope, alphabetical ordering within category).
2. Choose the closest existing category. Likely **Healthcare** / **Knowledge & Memory** / **Research & Data** — use whatever exists in the current README; do not invent a category.
3. Apply the repo's emoji legend honestly: Python (`🐍`), and the platform/scope markers per their legend. Do **not** add a "cloud service" marker — it runs locally.
4. Open a PR.

**Exact entry line (Markdown — adjust emoji to match the repo's current legend):**
```markdown
- [OpenOnco](https://github.com/romeo111/OpenOnco/tree/main/mcp_server) 🐍 - Free, open-source oncology clinical decision support. A deterministic, fully source-cited rule engine drafts two alternative treatment plans (standard + aggressive) for a clinician to verify — no LLM picks the regimen or dose. Informational support, not a medical device; v0.1, seeking clinician feedback.
```

---

## 3. PulseMCP

- **Site:** `https://www.pulsemcp.com`
- **Mechanism:** Public "Submit" / add-a-server page; PulseMCP then enriches from the GitHub repo.
- **Auto-index?** Partial — submission triggers indexing; it pulls README/metadata from GitHub. **Outward action: submit via the form.**

**Steps (maintainer):**
1. Go to PulseMCP's submit/add-server page.
2. Provide the **MCP server URL:** `https://github.com/romeo111/OpenOnco/tree/main/mcp_server` (and repo root `https://github.com/romeo111/OpenOnco` if asked separately).
3. Name: `OpenOnco`. Use the **short blurb** for the description field.
4. Set category to **Healthcare / Medical** (or nearest available); tags from the canonical list.
5. Confirm the listing renders the disclaimer-bearing description and links to the demo (`https://openonco.info/try.html`) and site.

**Description to paste:** use the **short blurb** above.

---

## 4. Glama

- **Site:** `https://glama.ai/mcp/servers`
- **Mechanism:** Glama crawls public GitHub repos and auto-generates listings; maintainers can **claim** a listing and improve metadata.
- **Auto-index?** **Yes** — may already appear or appear without submission. **Outward action: optional — claim/curate the listing** (recommended).

**Steps (maintainer):**
1. Search Glama for "OpenOnco" to see if it's auto-listed.
2. If present, **claim** the repo (Glama verifies GitHub ownership) and edit the description to the **short blurb** so the disclaimer and "no LLM picks the regimen" line are surfaced — auto-generated text may omit safety framing, which must be corrected.
3. Set category **Healthcare / Medical**; add tags from the canonical list.
4. If not present, use Glama's "add server" path with the MCP server URL.

> **Safety note:** auto-generated registry text can overstate maturity or drop the disclaimer. Where the listing is editable, replace it with the cleared short blurb. Where it isn't, ensure the linked README (which carries the full disclaimer) is the canonical landing point.

---

## 5. mcp.so

- **Site:** `https://mcp.so`
- **Mechanism:** Public "Submit" form.
- **Auto-index?** No. **Outward action: submit via the form.**

**Steps (maintainer):**
1. Open mcp.so's **Submit** page.
2. **Name:** `OpenOnco`. **GitHub/URL:** `https://github.com/romeo111/OpenOnco/tree/main/mcp_server`.
3. **Description:** paste the **short blurb**.
4. **Category:** Healthcare / Medical (or nearest). **Tags:** from canonical list.
5. Submit and verify the rendered card keeps the not-a-medical-device line.

---

## 6. Smithery

- **Site:** `https://smithery.ai`
- **Mechanism:** Connect the GitHub repo to Smithery and add a `smithery.yaml` (deployment/registry config) in the server directory; Smithery then indexes/hosts it.
- **Auto-index?** No — requires connecting the repo and config. **Outward action: connect repo + add config file (a code change to the repo).**

**Steps (maintainer):**
1. Sign in to Smithery with GitHub.
2. Add the OpenOnco repo and point Smithery at the `mcp_server/` directory.
3. Add a `smithery.yaml` per Smithery's current schema declaring the four tools (`engine_info`, `list_diseases`, `generate_treatment_plan`, `generate_diagnostic_brief`) and the start command — open this as a normal feature-branch PR into OpenOnco (per repo branch rules; never commit to `master`).
4. Set the listing description to the **short blurb**; category **Healthcare / Medical**; tags from the canonical list.
5. **Caution:** if Smithery offers hosted/remote execution, confirm it does not run patient data server-side. OpenOnco's privacy-by-design guarantee ("patient data never leaves your machine") only holds for local/in-browser use. If you enable a hosted runtime, the listing must **not** repeat the "data never leaves your machine" claim for that deployment, and the public demo/examples must stay synthetic-only. Prefer listing it as a self-hosted/local server.

---

## Post-submission checklist (every registry)

- [ ] Description carries the **not-a-medical-device** framing and "verified by a qualified oncologist" intent (full or short form).
- [ ] No claim of FDA approval/clearance, CE mark, clinical validation, or production-readiness.
- [ ] No implication that an LLM/AI chooses or recommends the regimen.
- [ ] Maturity is honest: v0.1, seeking clinician feedback; most content STUB.
- [ ] Audience framed as HCP/tumor boards/builders — never patients self-treating.
- [ ] Only the five canonical links used; demo and examples are synthetic-only.
- [ ] Tool names match exactly: `engine_info`, `list_diseases`, `generate_treatment_plan`, `generate_diagnostic_brief`.

---

*OpenOnco is an informational clinical decision support resource for healthcare professionals — not a medical device, not FDA-cleared/approved, and not clinically validated. It is an early-stage v0.1 open-source project actively seeking clinician feedback. No LLM picks the regimen or dose; recommendations are deterministic, rule-based, and source-cited. All recommendations must be verified by a qualified oncologist (CHARTER §11 + §15).*

---

*Submission note (do not publish in listings):* The MCP server source backing every listing above is at `C:\Users\805\cancer-autoresearch\.claude\worktrees\gallant-yonath-456e1c\mcp_server\` (`server.py`, `engine_bridge.py`, `README.md`). The four tool names in the asset were verified against `mcp_server\server.py`. There is no top-level `LICENSE` file in this worktree — confirm MIT/CC BY 4.0 license files are present in the published repo before submitting, since several registries surface a license badge.
