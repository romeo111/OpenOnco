"""MDT Orchestrator — turns a PlanResult into a structured tumor-board brief.

See specs/MDT_ORCHESTRATOR_SPEC.md for full design. Core invariants:

- Does NOT change clinical recommendations. The PlanResult passed in is
  read-only here; default_indication_id and all track data are untouched.
- Does NOT use LLM for clinical reasoning (CHARTER §8.3). All rules
  are deterministic and listed in the spec §3-§4.
- Adds three things: required/recommended/optional roles for the MDT,
  open questions where data is missing or ambiguous, and an initial
  set of provenance events so the formation of the plan is auditable
  from the very first moment.

MVP scope: rules tuned for the HCV-MZL reference case. Other diseases
fall through to the generic lymphoma / generic-cancer rules; expand
as new diseases land in the KB.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Literal, Optional

from knowledge_base.validation.loader import load_content

from .plan import PlanResult
from .provenance import (
    DecisionProvenanceGraph,
    ProvenanceEvent,
    make_event,
    now_iso,
)


TriggerType = Literal[
    "missing_data",
    "diagnosis_complexity",
    "treatment_domain",
    "safety_risk",
    "molecular_data",
    "local_availability",
    "palliative_need",
]

Priority = Literal["required", "recommended", "optional"]
_PRIORITY_RANK = {"required": 3, "recommended": 2, "optional": 1}


@dataclass
class MDTRequiredRole:
    role_id: str
    role_name: str
    reason: str
    trigger_type: TriggerType
    priority: Priority
    linked_findings: list[str] = field(default_factory=list)
    linked_questions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class OpenQuestion:
    id: str
    question: str
    owner_role: str
    blocking: bool
    rationale: str
    linked_findings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MDTOrchestrationResult:
    patient_id: Optional[str]
    plan_id: Optional[str]
    disease_id: Optional[str]
    required_roles: list[MDTRequiredRole] = field(default_factory=list)
    recommended_roles: list[MDTRequiredRole] = field(default_factory=list)
    optional_roles: list[MDTRequiredRole] = field(default_factory=list)
    open_questions: list[OpenQuestion] = field(default_factory=list)
    data_quality_summary: dict = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    provenance: Optional[DecisionProvenanceGraph] = None

    def to_dict(self) -> dict:
        return {
            "patient_id": self.patient_id,
            "plan_id": self.plan_id,
            "disease_id": self.disease_id,
            "required_roles": [r.to_dict() for r in self.required_roles],
            "recommended_roles": [r.to_dict() for r in self.recommended_roles],
            "optional_roles": [r.to_dict() for r in self.optional_roles],
            "open_questions": [q.to_dict() for q in self.open_questions],
            "data_quality_summary": dict(self.data_quality_summary),
            "warnings": list(self.warnings),
            "provenance": self.provenance.to_dict() if self.provenance else None,
        }


# ── Patient profile flattening (mirrors plan.generate_plan) ───────────────


def _flatten_findings(patient: dict) -> dict[str, Any]:
    out: dict[str, Any] = {}
    out.update(patient.get("findings") or {})
    for k, v in (patient.get("biomarkers") or {}).items():
        out.setdefault(k, v)
    for k, v in (patient.get("demographics") or {}).items():
        out.setdefault(k, v)
    return out


def _has(findings: dict[str, Any], *keys: str) -> bool:
    """True if ANY of the given keys is present and not None/empty-string."""
    for k in keys:
        v = findings.get(k)
        if v not in (None, ""):
            return True
    return False


def _truthy(findings: dict[str, Any], key: str) -> bool:
    """True if key present and value is truthy / 'positive' / 'yes' / 'true'."""
    v = findings.get(key)
    if v in (None, "", False, 0):
        return False
    if isinstance(v, str):
        return v.strip().lower() in {"positive", "yes", "true", "+"}
    return bool(v)


def _is_lymphoma(disease: Optional[dict]) -> bool:
    if not disease:
        return False
    lineage = (disease.get("lineage") or "").lower()
    if "lymphoma" in lineage:
        return True
    morph = (disease.get("codes") or {}).get("icd_o_3_morphology") or ""
    # ICD-O-3 morphology 9590-9729 / 9760-9769 = mature B/T-cell lymphomas
    if morph and len(morph) >= 4 and morph[:4].isdigit():
        n = int(morph[:4])
        if 9590 <= n <= 9729 or 9760 <= n <= 9769:
            return True
    return False


def _is_extranodal_malt(disease: Optional[dict]) -> bool:
    if not disease:
        return False
    morph = (disease.get("codes") or {}).get("icd_o_3_morphology") or ""
    return morph.startswith("9699")  # extranodal MZL of MALT type


# ── Role catalog (UA labels, no clinical content) ─────────────────────────


_ROLE_CATALOG: dict[str, str] = {
    "hematologist": "Гематолог / онкогематолог",
    "infectious_disease_hepatology": "Інфекціоніст / гепатолог",
    "radiologist": "Лікар-радіолог",
    "pathologist": "Патолог / гематопатолог",
    "clinical_pharmacist": "Клінічний фармацевт",
    "radiation_oncologist": "Радіотерапевт (променева терапія)",
    "surgical_oncologist": "Хірург-онколог",
    "palliative_care": "Паліативна допомога",
    "social_worker_case_manager": "Соціальний працівник / кейс-менеджер",
    "primary_care": "Сімейний лікар / терапевт",
}


def _role_name(role_id: str) -> str:
    return _ROLE_CATALOG.get(role_id, role_id)


# Maps a fired RedFlag id (or substring) → the role whose priority should
# escalate when that RedFlag fires with clinical_direction in {intensify, hold}.
# MVP scope; extend as KB grows.
_REDFLAG_DOMAIN_ROLE: dict[str, str] = {
    "RF-BULKY-DISEASE": "radiologist",
    "RF-AGGRESSIVE-HISTOLOGY-TRANSFORMATION": "pathologist",
    "RF-HBV-COINFECTION": "infectious_disease_hepatology",
    "RF-DECOMP-CIRRHOSIS": "infectious_disease_hepatology",
}

_ESCALATING_DIRECTIONS = {"intensify", "hold"}


def _collect_fired_red_flags(plan_result: PlanResult) -> list[str]:
    """Pull deduplicated fired-RedFlag IDs from the plan's algorithm trace
    (populated by algorithm_eval.walk_algorithm)."""
    if not plan_result.plan or not plan_result.plan.trace:
        return []
    out: list[str] = []
    seen: set[str] = set()
    for entry in plan_result.plan.trace:
        for rf in entry.get("fired_red_flags") or []:
            if rf not in seen:
                out.append(rf)
                seen.add(rf)
    return out


# ── Rule application ──────────────────────────────────────────────────────


def _apply_role_rules(
    patient: dict,
    plan_result: PlanResult,
    findings: dict[str, Any],
    disease_data: Optional[dict],
    entities: dict,
) -> list[MDTRequiredRole]:
    roles: dict[str, MDTRequiredRole] = {}

    def add(role_id: str, reason: str, trigger_type: TriggerType,
            priority: Priority, linked_findings: Optional[list[str]] = None) -> None:
        existing = roles.get(role_id)
        if existing is None:
            roles[role_id] = MDTRequiredRole(
                role_id=role_id,
                role_name=_role_name(role_id),
                reason=reason,
                trigger_type=trigger_type,
                priority=priority,
                linked_findings=list(linked_findings or []),
            )
            return
        # Dedupe — keep highest-priority + accumulate linked findings + extend reason if new
        if _PRIORITY_RANK[priority] > _PRIORITY_RANK[existing.priority]:
            existing.priority = priority
        for lf in linked_findings or []:
            if lf not in existing.linked_findings:
                existing.linked_findings.append(lf)

    plan = plan_result.plan
    tracks = plan.tracks if plan else []

    # R1 — lymphoma diagnosis → hematologist required
    if _is_lymphoma(disease_data):
        add(
            "hematologist",
            "Лімфомний діагноз — провідна спеціальність для терапевтичного ведення.",
            "diagnosis_complexity",
            "required",
            linked_findings=[plan_result.disease_id] if plan_result.disease_id else [],
        )

    # R2 — HCV/HBV positive → infectious disease / hepatology
    hcv_pos = (
        _truthy(findings, "BIO-HCV-RNA")
        or _truthy(findings, "hcv_rna_positive")
        or _truthy(findings, "hcv_rna_status")
    )
    hbv_pos = _truthy(findings, "hbsag") or _truthy(findings, "anti_hbc_total")
    if hcv_pos or hbv_pos:
        linked: list[str] = []
        if hcv_pos:
            linked.append("BIO-HCV-RNA")
        if hbv_pos:
            linked.append("HBV-serology")
        add(
            "infectious_disease_hepatology",
            "Активна вірусна етіологія (HCV/HBV) потребує паралельного ведення антивірусної терапії та оцінки реактивації.",
            "molecular_data",
            "recommended",
            linked_findings=linked,
        )

    # R3 — imaging fields present → radiologist (priority may escalate via RedFlag below)
    has_imaging = _has(
        findings,
        "dominant_nodal_mass_cm",
        "mediastinal_ratio",
        "pet_ct_date",
        "ct_findings",
        "lugano_stage",
    )
    if has_imaging:
        add(
            "radiologist",
            "Наявні візуалізаційні знахідки — потрібен радіолог для staging/restaging.",
            "diagnosis_complexity",
            "recommended",
            linked_findings=["imaging"],
        )

    # R4 — lymphoma OR pathology fields → pathologist
    pathology_fields_present = _has(
        findings,
        "biopsy_shows_dlbcl",
        "cd20_ihc_status",
        "ki67_percent",
        "biopsy_site",
    )
    if _is_lymphoma(disease_data) or pathology_fields_present:
        add(
            "pathologist",
            "Підтвердження гістології лімфоми + оцінка ризику трансформації (DLBCL/Richter).",
            "diagnosis_complexity",
            "recommended",
            linked_findings=["histology"],
        )

    # R5 — aggressive plan_track present → clinical pharmacist
    has_aggressive = any(
        (t.indication_data or {}).get("plan_track") == "aggressive" for t in tracks
    )
    if has_aggressive:
        add(
            "clinical_pharmacist",
            "Хіміоімунотерапевтичний регімен — drug-drug interactions, dose adjustments, premedication.",
            "treatment_domain",
            "recommended",
            linked_findings=["aggressive-track"],
        )

    # R6 — extranodal MALT → radiation oncologist optional
    if _is_extranodal_malt(disease_data):
        add(
            "radiation_oncologist",
            "Екстранодальна MALT-лімфома — у частини локалізацій локальна променева терапія є опцією.",
            "treatment_domain",
            "optional",
            linked_findings=[plan_result.disease_id] if plan_result.disease_id else [],
        )

    # R7 — any regimen with non-reimbursed drug → social worker / case manager
    non_reimbursed_drugs: list[str] = []
    for t in tracks:
        regimen = t.regimen_data or {}
        per_component = (regimen.get("ukraine_availability") or {}).get("per_component") or {}
        for drug_id, info in per_component.items():
            if isinstance(info, dict) and info.get("reimbursed_nszu") is False:
                non_reimbursed_drugs.append(drug_id)
        # Also check Drug entity directly via component refs
        for comp in regimen.get("components") or []:
            drug_id = comp.get("drug_id")
            if not drug_id:
                continue
            drug = entities.get(drug_id, {}).get("data") if isinstance(entities, dict) else None
            ua = ((drug or {}).get("regulatory_status") or {}).get("ukraine_registration") or {}
            if ua.get("registered") and ua.get("reimbursed_nszu") is False:
                non_reimbursed_drugs.append(drug_id)
    if non_reimbursed_drugs:
        add(
            "social_worker_case_manager",
            "У плані використовуються препарати без реімбурсації НСЗУ — потрібна оцінка доступу для пацієнта.",
            "local_availability",
            "recommended",
            linked_findings=sorted(set(non_reimbursed_drugs)),
        )

    # R8 — palliative care for poor performance status / decompensation
    try:
        ecog = int(findings.get("ecog") or 0)
    except (TypeError, ValueError):
        ecog = 0
    if ecog >= 3 or _truthy(findings, "decompensated_cirrhosis"):
        add(
            "palliative_care",
            "Знижений performance status / декомпенсована коморбідність — потрібна оцінка цілей лікування.",
            "palliative_need",
            "recommended",
            linked_findings=["ecog/decomp"],
        )

    # Priority escalation per spec §3: fired RedFlag with clinical_direction
    # in {intensify, hold} → role mapped via _REDFLAG_DOMAIN_ROLE escalates
    # to `required`.
    fired = _collect_fired_red_flags(plan_result)
    for rf_id in fired:
        rf_data = entities.get(rf_id, {}).get("data") if isinstance(entities, dict) else None
        if not rf_data:
            continue
        direction = (rf_data.get("clinical_direction") or "").strip().lower()
        if direction not in _ESCALATING_DIRECTIONS:
            continue
        escalated_role = _REDFLAG_DOMAIN_ROLE.get(rf_id)
        if not escalated_role or escalated_role not in roles:
            continue
        existing = roles[escalated_role]
        if _PRIORITY_RANK["required"] > _PRIORITY_RANK[existing.priority]:
            existing.priority = "required"
            existing.reason = (
                f"{existing.reason} Ескальовано через RedFlag {rf_id} "
                f"(clinical_direction={direction})."
            )
            if rf_id not in existing.linked_findings:
                existing.linked_findings.append(rf_id)

    return list(roles.values())


def _apply_open_question_rules(
    patient: dict,
    plan_result: PlanResult,
    findings: dict[str, Any],
    disease_data: Optional[dict],
) -> list[OpenQuestion]:
    questions: list[OpenQuestion] = []

    is_lymphoma = _is_lymphoma(disease_data)
    hcv_pos = (
        _truthy(findings, "BIO-HCV-RNA")
        or _truthy(findings, "hcv_rna_positive")
        or _truthy(findings, "hcv_rna_status")
    )
    aggressive_in_plan = any(
        (t.indication_data or {}).get("plan_track") == "aggressive"
        for t in (plan_result.plan.tracks if plan_result.plan else [])
    )
    has_anti_cd20_candidate = aggressive_in_plan or is_lymphoma

    # Q1 — HBV serology missing in any HCV/lymphoma patient considering anti-CD20
    if has_anti_cd20_candidate and not _has(findings, "hbsag", "anti_hbc_total"):
        questions.append(OpenQuestion(
            id="OQ-HBV-SEROLOGY",
            question=(
                "Чи проведена серологія HBV (HBsAg, anti-HBc total)? "
                "До початку anti-CD20 терапії статус має бути відомий."
            ),
            owner_role="infectious_disease_hepatology",
            blocking=True,
            rationale=(
                "Anti-CD20 без HBV профілактики при HBsAg+/anti-HBc+ "
                "несе значний ризик реактивації (CI-HBV-NO-PROPHYLAXIS)."
            ),
            linked_findings=["hbsag", "anti_hbc_total"],
        ))

    # Q2 — Hepatic fibrosis / Child-Pugh / FIB-4 missing for HCV+
    if hcv_pos and not _has(findings, "child_pugh_class", "decompensated_cirrhosis", "fib4_index"):
        questions.append(OpenQuestion(
            id="OQ-FIBROSIS-STAGE",
            question=(
                "Який стадій фіброзу/цирозу печінки (Child-Pugh, FIB-4)? "
                "Це впливає на вибір DAA та dosing бендамустину."
            ),
            owner_role="infectious_disease_hepatology",
            blocking=True,
            rationale=(
                "Декомпенсований цироз — RF-DECOMP-CIRRHOSIS, "
                "вимагає змін у регімені."
            ),
            linked_findings=["child_pugh_class", "fib4_index"],
        ))

    # Q3 — CD20 status missing for lymphoma diagnosis
    if is_lymphoma and not _has(findings, "cd20_ihc_status", "biopsy_confirmed"):
        questions.append(OpenQuestion(
            id="OQ-CD20-CONFIRMATION",
            question=(
                "Чи підтверджено CD20+ статус гістологією (IHC)? "
                "Без CD20+ rituximab/obinutuzumab не показані."
            ),
            owner_role="pathologist",
            blocking=True,
            rationale=(
                "Anti-CD20 терапія — основа для більшості ліній; "
                "відсутність експресії CD20 повністю змінює regimen."
            ),
            linked_findings=["cd20_ihc_status"],
        ))

    # Q4 — staging fields missing
    if is_lymphoma and not _has(findings, "lugano_stage", "pet_ct_date", "ct_findings"):
        questions.append(OpenQuestion(
            id="OQ-STAGING-COMPLETE",
            question=(
                "Чи виконано повне стадіювання (Lugano + PET/CT або CT)?"
            ),
            owner_role="radiologist",
            blocking=False,
            rationale="Прогноз і вибір треку залежать від stage та tumor burden.",
            linked_findings=["lugano_stage", "pet_ct_date"],
        ))

    # Q5 — aggressive track + missing LDH
    if aggressive_in_plan and not _has(findings, "ldh_ratio_to_uln", "ldh"):
        questions.append(OpenQuestion(
            id="OQ-LDH-CURRENT",
            question="Який актуальний LDH? Маркер пухлинного навантаження і трансформації.",
            owner_role="hematologist",
            blocking=False,
            rationale="LDH входить у прогностичні індекси індолентних лімфом.",
            linked_findings=["ldh_ratio_to_uln"],
        ))

    # Q6 — any track has a regimen that includes a non-reimbursed drug
    non_reimbursed: list[str] = []
    for t in (plan_result.plan.tracks if plan_result.plan else []):
        regimen = t.regimen_data or {}
        per_component = (regimen.get("ukraine_availability") or {}).get("per_component") or {}
        for drug_id, info in per_component.items():
            if isinstance(info, dict) and info.get("reimbursed_nszu") is False:
                non_reimbursed.append(drug_id)
    if non_reimbursed:
        questions.append(OpenQuestion(
            id="OQ-DRUG-AVAILABILITY",
            question=(
                "Чи доступні препарати без реімбурсації НСЗУ для пацієнта "
                f"({', '.join(sorted(set(non_reimbursed)))})? "
                "Чи потрібна social work consult / альтернативний регімен?"
            ),
            owner_role="social_worker_case_manager",
            blocking=False,
            rationale=(
                "Препарати з reimbursed_nszu=false означають out-of-pocket "
                "вартість для пацієнта; це впливає на adherence та реалістичність плану."
            ),
            linked_findings=sorted(set(non_reimbursed)),
        ))

    return questions


# ── Data quality summary ──────────────────────────────────────────────────


_CRITICAL_FIELDS_LYMPHOMA = (
    "cd20_ihc_status",
    "hbsag",
    "anti_hbc_total",
    "lugano_stage",
)
_RECOMMENDED_FIELDS_LYMPHOMA = (
    "ldh_ratio_to_uln",
    "fib4_index",
    "ecog",
    "pet_ct_date",
)


def _trigger_referenced_fields(trigger: Any) -> list[str]:
    """Walk a RedFlag.trigger dict (any/all/none_of-style) and collect every
    `finding` / `condition` / `lab` / `symptom` key referenced. Used to
    detect RedFlags whose required inputs are absent from patient findings."""
    if not isinstance(trigger, dict):
        return []
    out: list[str] = []
    for key in ("finding", "condition", "lab", "symptom"):
        v = trigger.get(key)
        if isinstance(v, str) and v:
            out.append(v)
    for nested_key in ("all_of", "any_of", "none_of"):
        for sub in trigger.get(nested_key) or []:
            out.extend(_trigger_referenced_fields(sub))
    return out


def _unevaluated_red_flags(
    findings: dict[str, Any],
    disease_data: Optional[dict],
    entities: dict,
) -> list[str]:
    """RedFlag IDs whose trigger references at least one finding key absent
    from the patient profile, AND whose `relevant_diseases` list either
    includes the patient's disease_id or is unspecified (global RedFlag).

    Empty list when no RedFlags can be evaluated incompletely."""
    out: list[str] = []
    disease_id = (disease_data or {}).get("id")
    for eid, info in (entities or {}).items():
        if info.get("type") != "redflags":
            continue
        rf = info.get("data") or {}
        relevant = rf.get("relevant_diseases") or []
        if relevant and disease_id and disease_id not in relevant:
            continue
        refs = _trigger_referenced_fields(rf.get("trigger") or {})
        if not refs:
            continue
        # If ANY referenced field is absent, RedFlag couldn't be fully evaluated
        if any(not _has(findings, f) for f in refs):
            out.append(eid)
    return sorted(out)


def _data_quality(
    findings: dict[str, Any],
    disease_data: Optional[dict],
    entities: dict,
) -> dict:
    is_lymphoma = _is_lymphoma(disease_data)
    critical = list(_CRITICAL_FIELDS_LYMPHOMA) if is_lymphoma else []
    recommended = list(_RECOMMENDED_FIELDS_LYMPHOMA) if is_lymphoma else []

    missing_critical = [f for f in critical if not _has(findings, f)]
    missing_recommended = [f for f in recommended if not _has(findings, f)]
    unevaluated = _unevaluated_red_flags(findings, disease_data, entities)

    return {
        "missing_critical_fields": missing_critical,
        "missing_recommended_fields": missing_recommended,
        "ambiguous_findings": [],
        "unevaluated_red_flags": unevaluated,
        "fields_present_count": sum(1 for v in findings.values() if v not in (None, "")),
        "fields_expected_count": len(critical) + len(recommended),
    }


# ── Provenance bootstrap ──────────────────────────────────────────────────


def _bootstrap_provenance(
    plan_result: PlanResult,
    required_roles: list[MDTRequiredRole],
    recommended_roles: list[MDTRequiredRole],
    optional_roles: list[MDTRequiredRole],
    open_questions: list[OpenQuestion],
) -> DecisionProvenanceGraph:
    plan = plan_result.plan
    plan_id = (plan.id if plan else "PLAN-UNKNOWN")
    plan_version = (plan.version if plan else 1)

    graph = DecisionProvenanceGraph(plan_version=plan_version)

    if plan_result.disease_id:
        graph.add_node(plan_result.disease_id, "diagnosis", plan_result.disease_id)
    for t in (plan.tracks if plan else []):
        if t.indication_id:
            graph.add_node(t.indication_id, "plan_section", t.label or t.indication_id)
            if plan_result.disease_id:
                graph.add_edge(plan_result.disease_id, t.indication_id, "candidate")

    counter = 0

    def next_id() -> str:
        nonlocal counter
        counter += 1
        return f"EV-{plan_id}-{counter:03d}"

    # Engine plan-generation event
    graph.add_event(make_event(
        event_id=next_id(),
        actor_role="engine",
        event_type="confirmed",
        target_type="plan_section",
        target_id=plan_id,
        summary=f"Engine згенерував план {plan_id} (версія {plan_version}).",
    ))

    # Per-role role-request events
    for role in (*required_roles, *recommended_roles, *optional_roles):
        graph.add_event(make_event(
            event_id=next_id(),
            actor_role="engine",
            event_type="requested_data",
            target_type="plan_section",
            target_id=role.role_id,
            summary=f"Запрошено роль '{role.role_name}' (priority={role.priority}): {role.reason}",
        ))

    # Per-question events
    for q in open_questions:
        graph.add_event(make_event(
            event_id=next_id(),
            actor_role="engine",
            event_type="added_question",
            target_type="plan_section",
            target_id=q.id,
            summary=f"Підняте питання для {q.owner_role} (blocking={q.blocking}): {q.question}",
        ))

    # Per-fired-RedFlag events (one event per RedFlag, deduplicated across steps)
    if plan and plan.trace:
        seen_rfs: set[str] = set()
        for entry in plan.trace:
            for rf_id in entry.get("fired_red_flags") or []:
                if rf_id in seen_rfs:
                    continue
                seen_rfs.add(rf_id)
                graph.add_event(make_event(
                    event_id=next_id(),
                    actor_role="engine",
                    event_type="flagged_risk",
                    target_type="red_flag",
                    target_id=rf_id,
                    summary=(
                        f"RedFlag {rf_id} спрацював на step {entry.get('step')} "
                        f"алгоритму {plan.algorithm_id}."
                    ),
                ))

    return graph


# ── Public entry point ────────────────────────────────────────────────────


def orchestrate_mdt(
    patient: dict,
    plan_result: PlanResult,
    kb_root: Path | str = "knowledge_base/hosted/content",
) -> MDTOrchestrationResult:
    """Build an MDT brief for `plan_result`.

    Important: this function does NOT modify `plan_result` — it only reads.
    Callers can rely on `plan_result.default_indication_id` being unchanged
    after this call (asserted in tests).
    """

    findings = _flatten_findings(patient)

    load = load_content(Path(kb_root))
    entities = load.entities_by_id
    warnings: list[str] = []
    for path, msg in load.schema_errors:
        warnings.append(f"schema error in {path.name}: {msg[:120]}")
    for path, msg in load.ref_errors:
        warnings.append(f"ref error in {path.name}: {msg}")

    disease_data = (
        entities.get(plan_result.disease_id, {}).get("data")
        if plan_result.disease_id
        else None
    )

    roles = _apply_role_rules(patient, plan_result, findings, disease_data, entities)
    questions = _apply_open_question_rules(patient, plan_result, findings, disease_data)
    quality = _data_quality(findings, disease_data, entities)

    # Cross-link: roles that own questions get question IDs in linked_questions
    roles_by_id = {r.role_id: r for r in roles}
    for q in questions:
        owner = roles_by_id.get(q.owner_role)
        if owner is not None and q.id not in owner.linked_questions:
            owner.linked_questions.append(q.id)

    required = sorted(
        [r for r in roles if r.priority == "required"], key=lambda r: r.role_id
    )
    recommended = sorted(
        [r for r in roles if r.priority == "recommended"], key=lambda r: r.role_id
    )
    optional = sorted(
        [r for r in roles if r.priority == "optional"], key=lambda r: r.role_id
    )

    provenance = _bootstrap_provenance(plan_result, required, recommended, optional, questions)

    return MDTOrchestrationResult(
        patient_id=plan_result.patient_id,
        plan_id=(plan_result.plan.id if plan_result.plan else None),
        disease_id=plan_result.disease_id,
        required_roles=required,
        recommended_roles=recommended,
        optional_roles=optional,
        open_questions=questions,
        data_quality_summary=quality,
        warnings=warnings,
        provenance=provenance,
    )


__all__ = [
    "MDTOrchestrationResult",
    "MDTRequiredRole",
    "OpenQuestion",
    "orchestrate_mdt",
]
