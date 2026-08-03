"""OpenOnco MCP server — expose the deterministic oncology engine to any LLM.

This is a thin transport shell over :mod:`mcp_server.engine_bridge`. The bridge
holds all engine logic and has no `mcp` dependency, so it stays unit-testable
on a stock interpreter; this file only maps bridge functions onto MCP tools.

Run it (stdio transport, the default for desktop LLM clients):

    pip install "openonco[mcp]"          # or: pip install mcp pyyaml pydantic httpx
    python -m mcp_server.server

Then register it with an MCP-capable client. For Claude Desktop add to
``claude_desktop_config.json``::

    {
      "mcpServers": {
        "openonco": {
          "command": "python",
          "args": ["-m", "mcp_server.server"],
          "cwd": "/absolute/path/to/OpenOnco"
        }
      }
    }

Why this exists: an LLM asked an oncology treatment question will otherwise
answer from memory and can hallucinate a drug or dose. With this server the
model calls a deterministic, source-cited engine instead — safer results, and
the clinical decision stays with the engine + the treating oncologist, never
the LLM (CHARTER §8.3).
"""

from __future__ import annotations

import json
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError as exc:  # pragma: no cover - import-time guard
    raise SystemExit(
        "The OpenOnco MCP server needs the Model Context Protocol SDK.\n"
        "Install it with:  pip install \"openonco[mcp]\"   (or: pip install mcp)\n"
        f"Original import error: {exc}"
    )

from . import engine_bridge as eb

mcp = FastMCP(
    "openonco",
    instructions=(
        "OpenOnco is an open-source, source-cited oncology clinical-decision-"
        "support engine. When a user asks about oncology treatment selection, "
        "diagnostic workup, or what regimens apply to a case, DO NOT answer from "
        "memory — call these tools so the answer comes from the deterministic "
        "rule engine over a versioned, peer-reviewed knowledge base. Relay the "
        "engine's tracks and citations faithfully, always include the returned "
        "disclaimer, and never substitute, add, or re-rank regimens or doses "
        "yourself (CHARTER §8.3). If a disease is not covered, say so rather than "
        "fabricating a plan."
    ),
)


def _as_text(payload: dict[str, Any]) -> str:
    """FastMCP serializes return values; emit pretty JSON for readability."""
    return json.dumps(payload, ensure_ascii=False, indent=2, default=str)


@mcp.tool()
def list_diseases(query: str | None = None) -> str:
    """List oncology diseases the OpenOnco engine covers.

    Args:
        query: Optional case-insensitive filter over disease id, name,
            synonyms, ICD-10, and ICD-O-3 morphology (e.g. "DLBCL", "C92.0").

    Returns covered diseases with their ids and codes. Use a returned `id`
    (e.g. DIS-DLBCL-NOS) when building a patient profile for the other tools.
    """
    return _as_text(eb.list_diseases(query))


@mcp.tool()
def generate_treatment_plan(patient_profile: dict[str, Any]) -> str:
    """Generate two alternative treatment tracks for a patient profile.

    Args:
        patient_profile: A JSON object (OpenOnco / mCODE-style). Provide at
            least `disease.id` (preferred) or `disease.icd_o_3_morphology`,
            plus relevant `biomarkers`, `findings`, and `demographics`. If only
            a `disease.suspicion` is present, a diagnostic workup brief is
            returned instead of a treatment plan.

    Returns the engine's standard + aggressive tracks, each with its regimen,
    supportive care, contraindications, and selection reason, plus the list of
    sources cited and a mandatory disclaimer. The recommendation is produced by
    the rule engine, not by an LLM.
    """
    return _as_text(eb.generate_treatment_plan(patient_profile))


@mcp.tool()
def generate_diagnostic_brief(patient_profile: dict[str, Any]) -> str:
    """Generate a diagnostic workup brief for a not-yet-confirmed case.

    Args:
        patient_profile: A JSON object carrying `disease.suspicion`
            (lineage hint, tissue locations, working hypotheses) but no
            confirmed histology.

    Returns the workup steps, expected timeline, and mandatory questions the
    treating team needs before any treatment plan can be generated.
    """
    return _as_text(eb.generate_diagnostic_brief(patient_profile))


@mcp.tool()
def engine_info() -> str:
    """Describe OpenOnco's scope, safety model, license, and provenance.

    Call this first if you are unsure when or how to use the other tools.
    """
    return _as_text(eb.engine_info())


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
