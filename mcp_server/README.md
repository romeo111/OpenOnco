# OpenOnco MCP server

**Let any LLM call OpenOnco's deterministic oncology engine instead of guessing.**

When you ask a general-purpose assistant (Claude, ChatGPT, a Cursor agent…) an
oncology treatment question, it answers from training memory — and can
hallucinate a drug, a dose, or a contraindication. This [Model Context
Protocol](https://modelcontextprotocol.io) server puts the **OpenOnco rule
engine** in front of the model: the assistant calls an auditable, source-cited
engine over a versioned knowledge base, then relays its output with citations
and a disclaimer.

No LLM picks the regimen. The recommendation comes from a declarative rule
engine over human-reviewed, source-cited clinical content (most entities are
still STUB — not yet dual-reviewer signed off); the clinical decision stays with
the engine and the treating oncologist ([CHARTER §8.3](../specs/CHARTER.md)).
That is the whole point — **safer results, by construction.**

> Informational decision support, **not** a medical device. Every output must be
> verified by a qualified oncologist. See [CHARTER §11 + §15](../specs/CHARTER.md).

---

## Tools exposed

| Tool | What it does |
|------|--------------|
| `engine_info` | Scope, safety model, license, and how an assistant should use the engine. Call this first if unsure. |
| `list_diseases` | List the oncology diseases the engine covers; optional substring/ICD filter to resolve free text (e.g. `"DLBCL"`, `"C92.0"`) to a covered entity. |
| `generate_treatment_plan` | Two alternative treatment tracks (standard + aggressive) for a structured patient profile, each with regimen, supportive care, contraindications, selection reason, and cited sources. Auto-routes to a diagnostic brief if histology is missing. |
| `generate_diagnostic_brief` | Workup steps, timeline, and mandatory questions for a not-yet-confirmed case (`disease.suspicion` only). |

Every clinical response carries the engine's source citations and a mandatory
disclaimer.

---

## Install

```bash
git clone https://github.com/romeo111/OpenOnco.git
cd OpenOnco
pip install -e ".[mcp]"     # installs the engine + the MCP SDK
```

Python 3.11+ required (3.12 recommended).

### Claude Desktop

Add to `claude_desktop_config.json`
(`%APPDATA%\Claude\` on Windows, `~/Library/Application Support/Claude/` on macOS):

```json
{
  "mcpServers": {
    "openonco": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/absolute/path/to/OpenOnco"
    }
  }
}
```

Restart Claude Desktop; the OpenOnco tools appear in the tools menu.

### Cursor / VS Code / other MCP clients

Point the client at the same stdio command — `python -m mcp_server.server`
with `cwd` set to the repo root. The server speaks MCP over stdio (the default
for desktop clients).

### Quick check (no client needed)

```bash
python -m mcp_server.server      # starts the stdio server; Ctrl-C to stop
```

The underlying logic lives in `engine_bridge.py`, which has **no MCP
dependency**, so you can also call it directly or from a notebook:

```python
from mcp_server import engine_bridge as eb
eb.list_diseases("dlbcl")
eb.generate_treatment_plan({"disease": {"id": "DIS-DLBCL-NOS"}, "biomarkers": {}})
```

---

## Patient profile shape

A minimal treatment profile needs a covered disease and any relevant biomarkers
/ findings / demographics:

```json
{
  "patient_id": "anon-001",
  "disease": { "id": "DIS-DLBCL-NOS" },
  "biomarkers": { "cell_of_origin": "GCB" },
  "demographics": { "age": 62 },
  "findings": {}
}
```

A diagnostic (suspicion-only) profile omits a confirmed disease:

```json
{
  "disease": {
    "suspicion": {
      "lineage_hint": "lymphoid",
      "tissue_locations": ["lymph_node"]
    }
  }
}
```

Use `list_diseases` to resolve a name or ICD code to a `DIS-*` id. The full
schema is documented in
[`specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md`](../specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md)
and the in-browser builder at [openonco.info/try.html](https://openonco.info/try.html).

**Do not send identifiable patient data** to a hosted LLM. Run the engine
locally (this server) or de-identify first.

---

## Architecture (for people building something similar)

This server is intentionally tiny so it's easy to copy:

- `engine_bridge.py` — dependency-free functions that call the engine
  (`generate_plan`, `generate_diagnostic_brief`) and return JSON-friendly dicts
  with citations + disclaimer. Fully unit-tested without the MCP SDK.
- `server.py` — a thin [FastMCP](https://modelcontextprotocol.io) shell that
  maps each bridge function onto an MCP tool.

The pattern generalizes to **any** rules-first decision-support project: keep
the decision logic deterministic and the LLM as a relay/interface, then expose
it over MCP. See the repository root [`README.md`](../README.md) and
[`specs/`](../specs/) for the full OpenOnco design.

OpenOnco is fully open source (code MIT, content CC BY 4.0). Fork it, lift this
server, or build your own engine behind the same interface.
