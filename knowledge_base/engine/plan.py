"""Top-level plan generation.

    patient profile  →  Disease match  →  applicable Algorithm
                                    →   Algorithm walked with RedFlags
                                    →   (default_indication, alternative_indication)
                                    →   two-plan output

Per CHARTER §2, the output always contains two alternative plans. The
data-model guarantee for this comes from `Algorithm.output_indications`
plus `default_indication` + `alternative_indication` fields.

Patient profile shape (dict; MVP — we will move to FHIR/mCODE later):

    {
        "patient_id": "PZ-001",                      # optional
        "disease": {"icd_o_3_morphology": "9699/3"}, # or {"id": "DIS-HCV-MZL"}
        "line_of_therapy": 1,                        # default 1
        "biomarkers": {"BIO-HCV-RNA": "positive"},
        "demographics": {"age": 58, "ecog": 1, ...},
        "findings": {"dominant_nodal_mass_cm": 4.0, ...},
    }
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from knowledge_base.schemas import ENTITY_BY_DIR
from knowledge_base.validation.loader import load_content
from .algorithm_eval import walk_algorithm


@dataclass
class PlanResult:
    patient_id: Optional[str]
    disease_id: Optional[str]
    algorithm_id: Optional[str]

    # The two plans
    default_indication_id: Optional[str]
    alternative_indication_id: Optional[str]

    # Full Indication records for rendering
    default_indication: Optional[dict]
    alternative_indication: Optional[dict]

    # Structured trace of rule-engine steps — audit / debug
    trace: list[dict] = field(default_factory=list)

    # Warnings accumulated during plan generation (not errors)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "patient_id": self.patient_id,
            "disease_id": self.disease_id,
            "algorithm_id": self.algorithm_id,
            "default_indication_id": self.default_indication_id,
            "alternative_indication_id": self.alternative_indication_id,
            "default_indication": self.default_indication,
            "alternative_indication": self.alternative_indication,
            "trace": self.trace,
            "warnings": self.warnings,
        }


def _find_disease_id(patient: dict, entities_by_id: dict) -> Optional[str]:
    dinfo = patient.get("disease") or {}
    if "id" in dinfo:
        return dinfo["id"]

    # Look up by ICD-O-3 morphology
    icd = dinfo.get("icd_o_3_morphology")
    if icd:
        for eid, info in entities_by_id.items():
            if info["type"] != "diseases":
                continue
            codes = info["data"].get("codes") or {}
            if codes.get("icd_o_3_morphology") == icd:
                return eid
    return None


def _find_algorithm(
    disease_id: str, line: int, entities_by_id: dict
) -> Optional[dict]:
    for eid, info in entities_by_id.items():
        if info["type"] != "algorithms":
            continue
        d = info["data"]
        if d.get("applicable_to_disease") == disease_id and d.get("applicable_to_line_of_therapy") == line:
            return d
    return None


def _collect_redflags(entities_by_id: dict) -> dict[str, dict]:
    return {
        eid: info["data"]
        for eid, info in entities_by_id.items()
        if info["type"] == "redflags"
    }


def generate_plan(
    patient: dict,
    kb_root: Path | str = "knowledge_base/hosted/content",
) -> PlanResult:
    """Load KB + generate two-plan result for a patient."""

    result = PlanResult(
        patient_id=patient.get("patient_id"),
        disease_id=None,
        algorithm_id=None,
        default_indication_id=None,
        alternative_indication_id=None,
        default_indication=None,
        alternative_indication=None,
    )

    load = load_content(Path(kb_root))
    if not load.ok:
        for path, msg in load.schema_errors:
            result.warnings.append(f"schema error in {path.name}: {msg[:120]}")
        for path, msg in load.ref_errors:
            result.warnings.append(f"ref error in {path.name}: {msg}")
        # Continue — partially-loaded KB is still useful for basic flows

    entities = load.entities_by_id
    disease_id = _find_disease_id(patient, entities)
    if disease_id is None:
        result.warnings.append("Could not resolve disease from patient.disease")
        return result
    result.disease_id = disease_id

    line = int(patient.get("line_of_therapy", 1))
    algo = _find_algorithm(disease_id, line, entities)
    if algo is None:
        result.warnings.append(
            f"No Algorithm found for disease={disease_id}, line_of_therapy={line}"
        )
        return result
    result.algorithm_id = algo["id"]

    # Merge findings + biomarkers + demographics into a single flat lookup
    findings = dict(patient.get("findings") or {})
    for k, v in (patient.get("biomarkers") or {}).items():
        findings.setdefault(k, v)
    for k, v in (patient.get("demographics") or {}).items():
        findings.setdefault(k, v)

    redflag_lookup = _collect_redflags(entities)

    selected, trace = walk_algorithm(algo, findings, redflag_lookup)
    result.trace = trace

    # Default = what decision tree selected (or algorithm.default_indication fallback)
    result.default_indication_id = selected or algo.get("default_indication")

    # Alternative = the OTHER one in output_indications, prefer algo.alternative_indication
    alt = algo.get("alternative_indication")
    if alt and alt != result.default_indication_id:
        result.alternative_indication_id = alt
    else:
        # Pick any other candidate from output_indications
        candidates = algo.get("output_indications") or []
        for c in candidates:
            if c != result.default_indication_id:
                result.alternative_indication_id = c
                break

    # Materialize full Indication records for rendering
    if result.default_indication_id and result.default_indication_id in entities:
        result.default_indication = entities[result.default_indication_id]["data"]
    if result.alternative_indication_id and result.alternative_indication_id in entities:
        result.alternative_indication = entities[result.alternative_indication_id]["data"]

    return result


__all__ = ["PlanResult", "generate_plan"]
