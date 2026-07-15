"""Tests for the dependency-free MCP engine bridge (mcp_server/engine_bridge.py).

The bridge is the logic layer behind the OpenOnco MCP server. It must call the
deterministic engine and relay cited output without ever fabricating clinical
content — these tests lock the contract that an LLM client depends on.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mcp_server import engine_bridge as eb

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = REPO_ROOT / "examples"


def _load_example(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def test_list_diseases_returns_catalog():
    out = eb.list_diseases()
    assert out["count"] > 50  # KB covers dozens of diseases
    assert out["diseases"], "expected a non-empty disease catalog"
    sample = out["diseases"][0]
    assert sample["id"].startswith("DIS-")
    assert sample["name"]
    assert out["disclaimer"]


def test_list_diseases_query_filters():
    out = eb.list_diseases("dlbcl")
    ids = {d["id"] for d in out["diseases"]}
    assert "DIS-DLBCL-NOS" in ids
    assert out["count"] == len(out["diseases"])
    # Filtering narrows the result vs. the full catalog.
    assert out["count"] < eb.list_diseases()["count"]


def test_generate_treatment_plan_is_covered_and_cited():
    profile = _load_example("auto_aml.json")
    out = eb.generate_treatment_plan(profile)
    assert out["mode"] == "treatment"
    assert out["covered"] is True
    assert out["disease_id"] == "DIS-AML"
    assert out["tracks"], "expected at least one track"
    assert any(t["is_default"] for t in out["tracks"])
    # Every plan must carry source citations and the safety disclaimer.
    assert out["sources_cited_count"] >= 1
    assert out["disclaimer"]
    assert out["engine_note"]


def test_treatment_entrypoint_routes_diagnostic_when_no_histology():
    profile = {
        "patient_id": "test-suspicion",
        "disease": {
            "suspicion": {
                "lineage_hint": "lymphoid",
                "tissue_locations": ["lymph_node"],
            }
        },
    }
    out = eb.generate_treatment_plan(profile)
    assert out["mode"] == "diagnostic"
    assert out["routed_from"] == "generate_treatment_plan"
    assert out["disclaimer"]


def test_generate_diagnostic_brief_returns_workup():
    profile = {
        "patient_id": "test-suspicion",
        "disease": {
            "suspicion": {
                "lineage_hint": "lymphoid",
                "tissue_locations": ["lymph_node"],
            }
        },
    }
    out = eb.generate_diagnostic_brief(profile)
    assert out["mode"] == "diagnostic"
    assert out["covered"] is True
    assert out["workup_steps"], "expected workup steps for a suspicion profile"
    assert out["disclaimer"]


def test_engine_info_advertises_rules_first_safety_model():
    info = eb.engine_info()
    assert info["diseases_covered"] > 50
    assert "rule" in info["decision_model"].lower()
    # The repository must be discoverable from the engine description.
    assert "github.com" in info["repository"].lower()
    assert info["disclaimer"]
