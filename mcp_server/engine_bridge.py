"""Dependency-free bridge between the OpenOnco rule engine and the MCP server.

This module deliberately does **not** import the `mcp` SDK. It exposes plain
functions that take JSON-serializable inputs and return JSON-serializable
dicts, so it can be unit-tested with a stock Python interpreter and reused by
any transport (MCP, a thin HTTP shim, a CLI, a notebook).

Design invariant (CHARTER §8.3): **no LLM decides anything here.** Every
function below calls the deterministic rule engine over the versioned,
source-cited knowledge base and relays its output verbatim. The point of the
MCP server is precisely to move an LLM from *guessing* a regimen to *calling*
an auditable engine — so the LLM's job shrinks to relaying cited engine output
plus the disclaimer, never selecting a treatment.
"""

from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

# ── Repo / KB resolution ──────────────────────────────────────────────────────
# engine_bridge.py lives at <repo>/mcp_server/engine_bridge.py.
_REPO_ROOT = Path(__file__).resolve().parent.parent


def _kb_root() -> Path:
    """Resolve the knowledge-base content root.

    Honors ``OPENONCO_KB_ROOT`` so the server can run against an alternate
    snapshot; otherwise defaults to the in-repo hosted content.
    """
    override = os.environ.get("OPENONCO_KB_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    return _REPO_ROOT / "knowledge_base" / "hosted" / "content"


def _ensure_engine_importable() -> None:
    """Make ``knowledge_base.engine`` importable for source checkouts.

    When OpenOnco is ``pip install``-ed the package is already on the path and
    this is a no-op; for a plain ``git clone`` we add the repo root.
    """
    if str(_REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(_REPO_ROOT))


# ── Shared safety framing ─────────────────────────────────────────────────────

DISCLAIMER = (
    "OpenOnco is an informational clinical-decision-support resource, NOT a "
    "medical device and NOT a substitute for a qualified oncologist. This output "
    "is a draft for a multidisciplinary tumor board to verify and tailor against "
    "the full clinical picture. No LLM selected this regimen: it was produced by "
    "a deterministic rule engine over a versioned, source-cited knowledge base "
    "(CHARTER §8.3, §11, §15). Always verify every recommendation, dose, and "
    "contraindication independently."
)

ENGINE_NOTE = (
    "Deterministic rule-engine output over the OpenOnco knowledge base — not "
    "LLM-generated. Relay it with citations and the disclaimer; do not add, "
    "substitute, or re-rank regimens or doses."
)

# What an assistant should tell the user when a question is out of scope.
OUT_OF_SCOPE_NOTE = (
    "This disease/scenario is not yet covered by the OpenOnco knowledge base. "
    "Do not fabricate a plan; say it is out of scope and recommend the treating "
    "oncologist consult primary guidelines (NCCN/ESMO/etc.) directly."
)


# ── Disease catalog (dep-free YAML read) ──────────────────────────────────────


@lru_cache(maxsize=1)
def _disease_catalog() -> list[dict[str, Any]]:
    """Return a lightweight catalog of covered diseases read from KB YAML.

    Uses pyyaml (already a hard dependency of OpenOnco). Only minimal,
    non-clinical metadata is surfaced (id, names, codes) so this stays cheap
    and safe to expose broadly.
    """
    import yaml  # pyyaml is a core OpenOnco dependency

    diseases_dir = _kb_root() / "diseases"
    catalog: list[dict[str, Any]] = []
    if not diseases_dir.is_dir():
        return catalog
    for path in sorted(diseases_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception:  # pragma: no cover - skip unreadable/partial files
            continue
        names = data.get("names") or {}
        codes = data.get("codes") or {}
        catalog.append(
            {
                "id": data.get("id") or path.stem.upper(),
                "name": names.get("preferred")
                or names.get("english")
                or path.stem,
                "synonyms": [s for s in (names.get("synonyms") or []) if s],
                "icd_10": codes.get("icd_10"),
                "icd_o_3_morphology": codes.get("icd_o_3_morphology"),
                "oncotree_code": data.get("oncotree_code"),
                "lineage": data.get("lineage"),
            }
        )
    return catalog


def list_diseases(query: str | None = None) -> dict[str, Any]:
    """List oncology diseases covered by the OpenOnco engine.

    Optional ``query`` filters by case-insensitive substring over disease id,
    preferred name, synonyms, ICD-10, and ICD-O-3 morphology — useful for an
    assistant resolving free text ("DLBCL", "C92.0") to a covered entity.
    """
    catalog = _disease_catalog()
    if query:
        q = query.strip().lower()
        filtered = []
        for d in catalog:
            haystack = " ".join(
                str(v)
                for v in (
                    d["id"],
                    d["name"],
                    *(d["synonyms"]),
                    d.get("icd_10") or "",
                    d.get("icd_o_3_morphology") or "",
                )
            ).lower()
            if q in haystack:
                filtered.append(d)
        catalog = filtered
    return {
        "count": len(catalog),
        "diseases": catalog,
        "note": (
            "Covered diseases only. Pass a disease `id` (e.g. DIS-DLBCL-NOS) or an "
            "ICD-O-3 morphology code in a patient profile to generate a plan."
        ),
        "disclaimer": DISCLAIMER,
    }


# ── Plan / diagnostic generation ──────────────────────────────────────────────


def _resolve_disease_name(disease_id: str | None) -> str | None:
    if not disease_id:
        return None
    for d in _disease_catalog():
        if d["id"] == disease_id:
            return d["name"]
    return None


def _track_to_dict(track: Any) -> dict[str, Any]:
    """Mirror cli._print_track field access into a JSON-friendly dict."""
    reg = getattr(track, "regimen_data", None) or {}
    supportive = getattr(track, "supportive_care_data", None) or []
    contras = getattr(track, "contraindications_data", None) or []
    return {
        "track_id": getattr(track, "track_id", None),
        "label_en": getattr(track, "label_en", None) or getattr(track, "label", None),
        "is_default": bool(getattr(track, "is_default", False)),
        "indication_id": getattr(track, "indication_id", None),
        "regimen": {"id": reg.get("id"), "name": reg.get("name")} if reg else None,
        "supportive_care": [s.get("id") for s in supportive if isinstance(s, dict)],
        "contraindications": [c.get("id") for c in contras if isinstance(c, dict)],
        "selection_reason": getattr(track, "selection_reason", None),
    }


def generate_treatment_plan(patient_profile: dict[str, Any]) -> dict[str, Any]:
    """Generate the two-track treatment plan for a patient profile.

    ``patient_profile`` is a JSON object following the OpenOnco / mCODE-style
    schema; at minimum ``disease.id`` or ``disease.icd_o_3_morphology`` must be
    present. If the profile only carries a suspicion (no confirmed histology),
    this routes to a diagnostic workup brief instead, never a treatment plan
    (CHARTER §15.2).
    """
    _ensure_engine_importable()
    from knowledge_base.engine.diagnostic import (
        is_diagnostic_profile,
        is_treatment_profile,
    )

    if is_diagnostic_profile(patient_profile) and not is_treatment_profile(
        patient_profile
    ):
        brief = generate_diagnostic_brief(patient_profile)
        brief["routed_from"] = "generate_treatment_plan"
        brief["routing_reason"] = (
            "No confirmed histology in the profile — returned a diagnostic "
            "workup brief instead of a treatment plan (CHARTER §15.2)."
        )
        return brief

    from knowledge_base.engine.plan import generate_plan

    result = generate_plan(patient_profile, kb_root=_kb_root())

    if result.plan is None or not result.default_indication_id:
        return {
            "mode": "treatment",
            "covered": False,
            "disease_id": result.disease_id,
            "disease_name": _resolve_disease_name(result.disease_id),
            "warnings": list(result.warnings or []),
            "note": OUT_OF_SCOPE_NOTE,
            "disclaimer": DISCLAIMER,
        }

    fda = getattr(result.plan, "fda_compliance", None)
    sources = list(getattr(fda, "data_sources_summary", []) or []) if fda else []
    tracks = [_track_to_dict(t) for t in result.plan.tracks]

    return {
        "mode": "treatment",
        "covered": True,
        "patient_id": result.patient_id,
        "disease_id": result.disease_id,
        "disease_name": _resolve_disease_name(result.disease_id),
        "algorithm_id": result.algorithm_id,
        "plan_id": getattr(result.plan, "id", None),
        "plan_version": getattr(result.plan, "version", None),
        "tracks": tracks,
        "intended_use": getattr(fda, "intended_use", None) if fda else None,
        "sources_cited": sources,
        "sources_cited_count": len(sources),
        "warnings": list(result.warnings or []),
        "engine_note": ENGINE_NOTE,
        "disclaimer": DISCLAIMER,
    }


def generate_diagnostic_brief(patient_profile: dict[str, Any]) -> dict[str, Any]:
    """Generate a diagnostic workup brief for a not-yet-confirmed case.

    Use when histology is not established: the engine returns the workup steps,
    biopsy approach, IHC panel, and mandatory questions needed before any
    treatment plan can exist.
    """
    _ensure_engine_importable()
    from knowledge_base.engine.diagnostic import generate_diagnostic_brief as _gdb

    try:
        result = _gdb(patient_profile, kb_root=_kb_root())
    except ValueError as exc:
        return {
            "mode": "diagnostic",
            "covered": False,
            "error": str(exc),
            "note": OUT_OF_SCOPE_NOTE,
            "disclaimer": DISCLAIMER,
        }

    dp = result.diagnostic_plan
    if dp is None:
        return {
            "mode": "diagnostic",
            "covered": False,
            "matched_workup_id": result.matched_workup_id,
            "warnings": list(result.warnings or []),
            "note": OUT_OF_SCOPE_NOTE,
            "disclaimer": DISCLAIMER,
        }

    steps = []
    for s in dp.workup_steps:
        steps.append(
            {
                "step": getattr(s, "step", None),
                "category": getattr(s, "category", None),
                "description": getattr(s, "description", None)
                or getattr(s, "test_id", None),
                "rationale": getattr(s, "rationale", None),
            }
        )

    return {
        "mode": "diagnostic",
        "covered": True,
        "patient_id": result.patient_id,
        "matched_workup_id": result.matched_workup_id,
        "diagnostic_plan_id": getattr(dp, "id", None),
        "expected_timeline_days": getattr(dp, "expected_timeline_days", None),
        "workup_steps": steps,
        "mandatory_questions": list(getattr(dp, "mandatory_questions", []) or []),
        "warnings": list(result.warnings or []),
        "engine_note": ENGINE_NOTE,
        "disclaimer": DISCLAIMER,
    }


def engine_info() -> dict[str, Any]:
    """Static description of the engine's scope, safety model, and provenance."""
    return {
        "name": "OpenOnco",
        "summary": (
            "Open-source oncology clinical-decision-support engine. Takes a "
            "structured patient profile and returns two alternative treatment "
            "tracks (standard + aggressive) with a source citation under every "
            "recommendation."
        ),
        "decision_model": (
            "Rules-first. Clinical recommendations come from a declarative rule "
            "engine over a versioned, peer-reviewed knowledge base. No LLM picks "
            "regimens, generates doses, or interprets biomarkers for therapy "
            "selection (CHARTER §8.3)."
        ),
        "diseases_covered": len(_disease_catalog()),
        "actionability_source": "CIViC (CC0)",
        "homepage": "https://openonco.info",
        "repository": "https://github.com/romeo111/OpenOnco",
        "license": "Code MIT; content & specifications CC BY 4.0",
        "how_an_assistant_should_use_it": (
            "When a user asks an oncology treatment question, call "
            "generate_treatment_plan with a structured profile instead of "
            "answering from memory. Relay the engine's tracks and citations, "
            "always append the disclaimer, and never substitute your own regimen."
        ),
        "disclaimer": DISCLAIMER,
    }
