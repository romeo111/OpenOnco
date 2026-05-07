"""OpenOnco Pydantic schemas for the knowledge base.

Every entity under `hosted/content/<type>/` validates against one of
these models on load. See `validation/loader.py`.
"""

from .access_pathway import AccessPathway, CostOrientation
from .algorithm import Algorithm
from .biomarker import Biomarker
from .biomarker_actionability import BiomarkerActionability, RegulatoryApproval
from .contraindication import Contraindication
from .diagnostic import (
    BiopsyApproach,
    DiagnosticPlan,
    DiagnosticWorkup,
    IHCPanel,
    SuspicionSnapshot,
    WorkupStep,
)
from .disease import Disease
from .drug import Drug
from .drug_indication import (
    DrugIndication,
    RegulatoryLabelRecord,
    ReimbursementRecord,
)
from .experimental_option import ExperimentalOption, ExperimentalTrial
from .indication import Indication
from .mdt_skill import MdtSkill
from .monitoring import MonitoringSchedule
from .modality import (
    ModalityTiming,
    RadiationDose,
    RadiationModality,
    SurgeryModality,
)
from .plan import (
    AccessMatrix,
    AccessMatrixRow,
    FDAComplianceMetadata,
    Plan,
    PlanAnnotation,
    PlanTrack,
    VariantActionabilityHit,
)
from .questionnaire import (
    QGroup,
    Question,
    QuestionOption,
    Questionnaire,
)
from ._reviewer_signoff import ReviewerSignoff
from .red_flag import RedFlag
from .regimen import Regimen, RegimenComponent, RegimenPhase
from .reviewer_profile import ReviewerProfile, SignOffScope
from .source import Source
from .supportive_care import SupportiveCare
from .test import Test

# Map content directory name → entity class.
# Used by the loader to pick the right schema for each YAML file.
# Plan / DiagnosticPlan are NOT included — instances live outside the
# public KB (in patient_plans/<patient_id>/v<N>.yaml, gitignored per
# CHARTER §9.3). Only DiagnosticWorkup (curated content) belongs here.
ENTITY_BY_DIR: dict[str, type] = {
    "diseases": Disease,
    "drugs": Drug,
    "drug_indications": DrugIndication,
    "regimens": Regimen,
    "indications": Indication,
    "biomarkers": Biomarker,
    "biomarker_actionability": BiomarkerActionability,
    "contraindications": Contraindication,
    "redflags": RedFlag,
    "algorithms": Algorithm,
    "tests": Test,
    "supportive_care": SupportiveCare,
    "monitoring": MonitoringSchedule,
    "sources": Source,
    "workups": DiagnosticWorkup,
    "questionnaires": Questionnaire,
    "access_pathways": AccessPathway,
    "surgery": SurgeryModality,
    "radiation": RadiationModality,
    "mdt_skills": MdtSkill,
    "reviewers": ReviewerProfile,
}

__all__ = [
    "AccessMatrix",
    "AccessMatrixRow",
    "AccessPathway",
    "Algorithm",
    "Biomarker",
    "BiomarkerActionability",
    "CostOrientation",
    "BiopsyApproach",
    "Contraindication",
    "DiagnosticPlan",
    "DiagnosticWorkup",
    "Disease",
    "Drug",
    "DrugIndication",
    "ENTITY_BY_DIR",
    "ExperimentalOption",
    "ExperimentalTrial",
    "FDAComplianceMetadata",
    "IHCPanel",
    "Indication",
    "MdtSkill",
    "ModalityTiming",
    "MonitoringSchedule",
    "Plan",
    "PlanAnnotation",
    "PlanTrack",
    "QGroup",
    "Question",
    "QuestionOption",
    "Questionnaire",
    "RadiationDose",
    "RadiationModality",
    "RedFlag",
    "Regimen",
    "RegimenComponent",
    "RegimenPhase",
    "RegulatoryApproval",
    "RegulatoryLabelRecord",
    "ReimbursementRecord",
    "ReviewerProfile",
    "ReviewerSignoff",
    "SignOffScope",
    "Source",
    "SurgeryModality",
    "SupportiveCare",
    "SuspicionSnapshot",
    "Test",
    "VariantActionabilityHit",
    "WorkupStep",
]
