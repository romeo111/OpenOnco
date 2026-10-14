"""Source-specific BV/bleomycin reference evaluator, not a planning gate.

This candidate is deliberately outside the live engine until interfaces and
report notices are integrated. It neither selects nor substitutes treatment.
"""
from dataclasses import dataclass
from collections.abc import Collection, Mapping

from scripts.medication_input_contract import parse_medication_input

PAIR = frozenset({"DRUG-BRENTUXIMAB-VEDOTIN", "DRUG-BLEOMYCIN"})
SOURCE = "SRC-ADCETRIS-US-LABEL"
CONTRAINDICATION = "CI-BRENTUXIMAB-BLEOMYCIN"
REGIMEN = "REG-CHP-BV"


@dataclass(frozen=True)
class ReferenceInteraction:
    status: str
    contraindication_ids: tuple[str, ...] = ()
    source_ids: tuple[str, ...] = ()
    unsupported_paths: tuple[str, ...] = ()


def evaluate_bv_bleomycin_reference(profile: Mapping, regimen: Mapping,
                                    contraindication: Mapping,
                                    known_drug_ids: Collection[str]) -> ReferenceInteraction:
    """Evaluate only the encoded pair and REG-CHP-BV scope.

    Drug identifiers must be exact catalog IDs. Historical exposure and aliases
    are not interpreted. A partial list can prove presence, never absence.
    Invalid source/input raises: callers must not convert this to clearance.
    No other contraindication grammar, interaction or regimen is evaluated.
    """
    if not isinstance(regimen, Mapping):
        raise ValueError("Regimen reference must be an object.")
    if regimen.get("id") != REGIMEN:
        return ReferenceInteraction("out_of_scope")
    if not isinstance(contraindication, Mapping):
        raise ValueError("Contraindication reference must be an object.")
    trigger = contraindication.get("trigger")
    if not isinstance(trigger, dict) or set(trigger) != {"type", "conditions", "logic"}:
        raise ValueError("Unsupported contraindication trigger.")
    conditions = trigger.get("conditions")
    expected = [{"concomitant_drugs": sorted(PAIR)}]
    valid_conditions = (isinstance(conditions, list) and len(conditions) == 1
                        and isinstance(conditions[0], dict)
                        and set(conditions[0]) == {"concomitant_drugs"}
                        and type(conditions[0]["concomitant_drugs"]) is list
                        and all(type(x) is str for x in conditions[0]["concomitant_drugs"])
                        and [{"concomitant_drugs": sorted(conditions[0]["concomitant_drugs"])}] == expected)
    if (contraindication.get("id") != CONTRAINDICATION
            or contraindication.get("severity") != "absolute"
            or contraindication.get("sources") != [SOURCE]
            or contraindication.get("affects_regimens") != [REGIMEN]
            or trigger.get("type") != "drug_drug_interaction"
            or trigger.get("logic") != "AND" or not valid_conditions):
        raise ValueError("Unsupported source-specific contraindication reference.")
    if not PAIR.issubset(known_drug_ids):
        raise ValueError("Source pair requires existing drug IDs.")
    components = regimen.get("components")
    if (type(components) is not list or not components
            or any(not isinstance(c, dict) or type(c.get("drug_id")) is not str
                   or c["drug_id"] not in known_drug_ids for c in components)):
        raise ValueError("Regimen components require existing drug IDs.")
    planned = {component["drug_id"] for component in components}
    if "DRUG-BRENTUXIMAB-VEDOTIN" not in planned:
        raise ValueError("BV reference is missing its defining component.")
    medicines = parse_medication_input(profile, known_drug_ids)
    if PAIR <= planned | set(medicines.drug_ids):
        return ReferenceInteraction("blocked", (CONTRAINDICATION,), (SOURCE,), medicines.unsupported_paths)
    if medicines.unsupported_paths:
        status = "unsupported_input"
    elif medicines.reported_complete:
        status = "not_detected_in_reported_list"
    elif medicines.status == "partial":
        status = "incomplete"
    else:
        status = "unknown"
    return ReferenceInteraction(status, source_ids=(SOURCE,), unsupported_paths=medicines.unsupported_paths)
