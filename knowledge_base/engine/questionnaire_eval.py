"""Live questionnaire evaluator — partial-profile preview.

Powers the live "this field affects the plan" preview pane on /try.
Given a questionnaire spec and a partially-filled patient profile,
returns:

  - filled_count / total_questions / completion_pct
  - missing_critical: list of unfilled critical-impact questions
  - fired_redflags: list of RedFlag IDs whose triggers evaluate True
    on the partial profile (uses the same redflag_eval as engine)
  - would_select_indication: best guess at which Indication the
    Algorithm would pick given current findings; None if not enough
    data to traverse decision_tree
  - ready_to_generate: bool — true when no critical questions missing

Designed for Pyodide: pure Python, no external IO, sync function. The
form calls this on every change (debounced ~300ms in JS).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

from knowledge_base.validation.loader import load_content
from .algorithm_eval import walk_algorithm
from .redflag_eval import evaluate_redflag_trigger


# ── Profile flattening (mirrors engine/plan.py) ──────────────────────────


def _flatten_findings(profile: dict) -> dict[str, Any]:
    flat: dict[str, Any] = {}
    for k, v in (profile.get("findings") or {}).items():
        flat[k] = v
    for k, v in (profile.get("biomarkers") or {}).items():
        flat.setdefault(k, v)
    for k, v in (profile.get("demographics") or {}).items():
        flat.setdefault(k, v)
    return flat


def _get_path(profile: dict, dotted: str) -> Any:
    """Walk dotted path through profile dict. Returns sentinel-None
    if any segment missing or not a dict."""
    cur: Any = profile
    for seg in dotted.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(seg)
    return cur


def _is_filled(value: Any) -> bool:
    """A field counts as 'filled' when it's not None and not an empty
    string. Booleans (incl. False) count as filled, zero counts as filled."""
    if value is None:
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    return True


# ── Result dataclass ──────────────────────────────────────────────────────


@dataclass
class QPreviewResult:
    filled_count: int
    total_questions: int
    completion_pct: int
    missing_critical: list[dict]  # [{field, label, group}]
    missing_required: list[dict]
    fired_redflags: list[str]
    would_select_indication: Optional[str]
    decision_trace: list[dict]
    ready_to_generate: bool
    warnings: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


# ── Public entry points ───────────────────────────────────────────────────


def list_questions(questionnaire: dict) -> list[dict]:
    """Flatten all groups → list of question dicts with group title attached."""
    out: list[dict] = []
    for grp in questionnaire.get("groups") or []:
        gtitle = grp.get("title") or ""
        for q in grp.get("questions") or []:
            qq = dict(q)
            qq["_group"] = gtitle
            out.append(qq)
    return out


def evaluate_partial(
    profile: dict,
    questionnaire: dict,
    kb_root: Path | str = "knowledge_base/hosted/content",
    loaded_kb=None,
) -> QPreviewResult:
    """Evaluate a partial profile against a questionnaire spec.

    Returns a QPreviewResult ready for JSON serialization to the browser.
    Engine-state queries (which RedFlag fires, which Indication algorithm
    would pick) reuse production engine modules so preview matches the
    real plan once generated.

    `loaded_kb`: optional pre-built `LoadResult` from `load_content()`. When
    provided, skips the YAML re-walk — used by the what-if loop on /try
    which evaluates 15+ alt-value specs against the same KB snapshot.
    """
    questions = list_questions(questionnaire)
    total = len(questions)

    missing_critical: list[dict] = []
    missing_required: list[dict] = []
    filled_count = 0

    for q in questions:
        path = q.get("field") or ""
        value = _get_path(profile, path)
        impact = q.get("impact", "optional")
        if _is_filled(value):
            filled_count += 1
        else:
            entry = {
                "field": path,
                "label": q.get("label", path),
                "group": q.get("_group", ""),
                "triggers": q.get("triggers") or [],
            }
            if impact == "critical":
                missing_critical.append(entry)
            elif impact == "required":
                missing_required.append(entry)

    completion_pct = int(round(filled_count * 100 / max(1, total)))

    # Engine-side checks: load KB so we can fire RedFlags + walk Algorithm
    load = loaded_kb if loaded_kb is not None else load_content(Path(kb_root))
    entities = load.entities_by_id

    findings = _flatten_findings(profile)
    redflag_lookup = {
        eid: info["data"]
        for eid, info in entities.items()
        if info["type"] == "redflags"
    }
    fired: list[str] = []
    for rf_id, rf in redflag_lookup.items():
        try:
            if evaluate_redflag_trigger(rf.get("trigger") or {}, findings):
                fired.append(rf_id)
        except Exception:
            continue

    # Algorithm preview: only attempt if disease is resolvable
    would_select: Optional[str] = None
    decision_trace: list[dict] = []
    disease_id = questionnaire.get("disease_id")
    line = int(
        (profile.get("line_of_therapy")
         or questionnaire.get("line_of_therapy")
         or 1)
    )
    algo = None
    for eid, info in entities.items():
        if info["type"] != "algorithms":
            continue
        d = info["data"]
        if (d.get("applicable_to_disease") == disease_id
                and d.get("applicable_to_line_of_therapy") == line):
            algo = d
            break
    if algo is not None:
        try:
            selected, trace = walk_algorithm(algo, findings, redflag_lookup)
            would_select = selected
            decision_trace = trace
        except Exception as exc:
            decision_trace = [{"error": str(exc)}]

    warnings: list[str] = []
    if not algo:
        warnings.append(
            f"No Algorithm для {disease_id} 1L — engine fall back на default."
        )

    ready = len(missing_critical) == 0 and would_select is not None

    return QPreviewResult(
        filled_count=filled_count,
        total_questions=total,
        completion_pct=completion_pct,
        missing_critical=missing_critical,
        missing_required=missing_required,
        fired_redflags=sorted(set(fired)),
        would_select_indication=would_select,
        decision_trace=decision_trace,
        ready_to_generate=ready,
        warnings=warnings,
    )


def assemble_profile(questionnaire: dict, answers: dict) -> dict:
    """Merge questionnaire.fixed_fields + user answers into a full
    patient profile dict ready for generate_plan().

    answers is a flat dict {dotted_path: value}; this function expands
    dotted paths back into nested structure (demographics.ecog → nested).
    """
    profile: dict[str, Any] = {}

    # Apply fixed_fields first (deep merge)
    def deep_merge(target: dict, src: dict) -> None:
        for k, v in src.items():
            if isinstance(v, dict) and isinstance(target.get(k), dict):
                deep_merge(target[k], v)
            else:
                target[k] = v
    deep_merge(profile, questionnaire.get("fixed_fields") or {})

    # Then apply user answers
    for dotted, value in answers.items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            continue
        parts = dotted.split(".")
        cur: dict = profile
        for seg in parts[:-1]:
            if seg not in cur or not isinstance(cur.get(seg), dict):
                cur[seg] = {}
            cur = cur[seg]
        cur[parts[-1]] = value
    return profile


__all__ = [
    "QPreviewResult",
    "assemble_profile",
    "evaluate_partial",
    "list_questions",
]
