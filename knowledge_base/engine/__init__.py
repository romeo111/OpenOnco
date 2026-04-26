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
from .experimental_options import (
    TrialQuery,
    clear_cache as clear_experimental_cache,
    enumerate_experimental_options,
)
from .lazy_loader import (
    apply_disease_module,
    disease_bundle_basename,
    lazy_load_disease,
    load_bundle_index,
    load_disease_module,
    merge_disease_module,
    url_for_disease,
)
from .mdt_orchestrator import (
    MDTOrchestrationResult,
    MDTRequiredRole,
    OpenQuestion,
    SkillMetadata,
    get_skill,
    orchestrate_mdt,
)
from .persistence import (
    DEFAULT_ROOT as PATIENT_PLANS_ROOT,
    latest_version_path,
    list_versions,
    load_result,
    save_result,
    update_superseded_by_on_disk,
)
from .plan import PlanResult, generate_plan
from .questionnaire_eval import (
    QPreviewResult,
    assemble_profile,
    evaluate_partial,
    list_questions,
)
from .provenance import (
    DecisionProvenanceGraph,
    ProvenanceEvent,
    make_event,
)
from .render import (
    render,
    render_diagnostic_brief_html,
    render_plan_html,
    render_revision_note_html,
)
from .revisions import revise_plan

__all__ = [
    "DecisionProvenanceGraph",
    "DiagnosticPlanResult",
    "MDTOrchestrationResult",
    "MDTRequiredRole",
    "OpenQuestion",
    "PATIENT_PLANS_ROOT",
    "PlanResult",
    "ProvenanceEvent",
    "QPreviewResult",
    "SkillMetadata",
    "TrialQuery",
    "apply_disease_module",
    "assemble_profile",
    "clear_experimental_cache",
    "disease_bundle_basename",
    "enumerate_experimental_options",
    "evaluate_partial",
    "generate_diagnostic_brief",
    "generate_plan",
    "get_skill",
    "is_diagnostic_profile",
    "is_treatment_profile",
    "latest_version_path",
    "lazy_load_disease",
    "list_questions",
    "list_versions",
    "load_bundle_index",
    "load_disease_module",
    "load_result",
    "make_event",
    "merge_disease_module",
    "orchestrate_mdt",
    "render",
    "render_diagnostic_brief_html",
    "render_plan_html",
    "render_revision_note_html",
    "revise_plan",
    "save_result",
    "update_superseded_by_on_disk",
    "url_for_disease",
]
