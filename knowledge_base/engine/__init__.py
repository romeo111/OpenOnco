"""OpenOnco rule engine: patient profile → applicable Indications → two plans.

No clinical reasoning happens in code — the code only **evaluates** rules
authored by clinical reviewers (CHARTER §8.3). Decisions about *which*
regimen to recommend are already encoded in the Indication / Algorithm
entities under `knowledge_base/hosted/content/`.
"""

from .plan import PlanResult, generate_plan

__all__ = ["PlanResult", "generate_plan"]
