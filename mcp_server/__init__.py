"""OpenOnco MCP server package.

Exposes the deterministic OpenOnco rule engine to LLM clients over the Model
Context Protocol so assistants call an auditable, source-cited engine instead
of guessing oncology regimens. See ``mcp_server/README.md``.
"""

from . import engine_bridge

__all__ = ["engine_bridge"]
