"""Proposed medication input contract; not integrated into clinical screening.

Completeness is caller supplied, not independently verified reconciliation.
Only active concomitant drugs belong here; historical exposure is separate.
"""
from dataclasses import dataclass
from collections.abc import Collection, Mapping


@dataclass(frozen=True)
class MedicationInput:
    status: str
    drug_ids: tuple[str, ...]
    unsupported_paths: tuple[str, ...] = ()

    @property
    def reported_complete(self):
        return self.status == "complete" and not self.unsupported_paths


def parse_medication_input(profile: Mapping, known_drug_ids: Collection[str]) -> MedicationInput:
    """Parse a candidate contract without mutation, aliases or safety clearance.

    Canonical field: concomitant_medications={status, drug_ids}.
    Absent/null stays unknown. Complete empty lists must be explicit.
    Unsupported legacy shapes prevent a reported-complete interpretation.
    """
    if not isinstance(profile, Mapping):
        raise ValueError("Medication profile must be an object.")
    unsupported = [key for key in ("medications", "concomitant_drugs") if key in profile]
    findings = profile.get("findings")
    if isinstance(findings, Mapping):
        unsupported.extend("findings." + key for key in ("concomitant_drugs", "bleomycin_concomitant") if key in findings)
    value = profile.get("concomitant_medications")
    if value is None:
        return MedicationInput("unknown", (), tuple(unsupported))
    if not isinstance(value, dict) or set(value) != {"status", "drug_ids"}:
        raise ValueError("concomitant_medications requires only status and drug_ids.")
    status, drugs = value["status"], value["drug_ids"]
    if type(status) is not str or status not in {"unknown", "partial", "complete"}:
        raise ValueError("Medication status must be unknown, partial or complete.")
    if type(drugs) is not list:
        raise ValueError("Medication drug_ids must be a list.")
    if any(type(drug) is not str or drug not in known_drug_ids for drug in drugs):
        raise ValueError("Medication entries must be exact existing drug IDs.")
    if len(set(drugs)) != len(drugs):
        raise ValueError("Medication drug IDs must be unique.")
    if status == "unknown" and drugs:
        raise ValueError("Known medicines require partial or complete status.")
    return MedicationInput(status, tuple(drugs), tuple(unsupported))
