"""OpenOnco rule engine: patient profile → applicable Indications → two plans.

No clinical reasoning happens in code — the code only **evaluates** rules
authored by clinical reviewers (CHARTER §8.3). Decisions about *which*
regimen to recommend are already encoded in the Indication / Algorithm
entities under `knowledge_base/hosted/content/`.

The MDT Orchestrator (mdt_orchestrator.py) is a separate read-only
layer: it reads a PlanResult and produces a tumor-board brief
(required roles, open questions, provenance events). It does NOT
modify the PlanResult or change clinical recommendations
(specs/MDT_ORCHESTRATOR_SPEC.md §1.2).
"""

from .diagnostic import (
    DiagnosticPlanResult,
    generate_diagnostic_brief,
    is_diagnostic_profile,
    is_treatment_profile,
)
from .mdt_orchestrator import (
    MDTOrchestrationResult,
    MDTRequiredRole,
    OpenQuestion,
    orchestrate_mdt,
)
from .plan import PlanResult, generate_plan
from .provenance import (
    DecisionProvenanceGraph,
    ProvenanceEvent,
    make_event,
)
from .revisions import revise_plan

__all__ = [
    "DecisionProvenanceGraph",
    "DiagnosticPlanResult",
    "MDTOrchestrationResult",
    "MDTRequiredRole",
    "OpenQuestion",
    "PlanResult",
    "ProvenanceEvent",
    "generate_diagnostic_brief",
    "generate_plan",
    "is_diagnostic_profile",
    "is_treatment_profile",
    "make_event",
    "orchestrate_mdt",
    "revise_plan",
]
