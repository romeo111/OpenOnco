from knowledge_base.validation.loader import load_content
from knowledge_base.engine.redflag_eval import evaluate_redflag_trigger


KB_ROOT = "knowledge_base/hosted/content"
ASSESSMENT_ONLY_IDS = {
    "RF-UNIVERSAL-OLDER-ADULT-VULNERABILITY",
    "RF-UNIVERSAL-PEDIATRIC-SPECIALIST-REVIEW",
}


def _red_flag_references(node):
    if isinstance(node, dict):
        value = node.get("red_flag")
        if isinstance(value, str):
            yield value
        for item in node.values():
            yield from _red_flag_references(item)
    elif isinstance(node, list):
        for item in node:
            yield from _red_flag_references(item)


def test_universal_assessment_flags_are_investigate_only_and_not_routing_inputs():
    result = load_content(KB_ROOT)
    flags = {
        info["data"]["id"]: info["data"]
        for info in result.entities_by_id.values()
        if info["type"] == "redflags"
        and info["data"].get("id") in ASSESSMENT_ONLY_IDS
    }

    assert set(flags) == ASSESSMENT_ONLY_IDS
    assert flags["RF-UNIVERSAL-OLDER-ADULT-VULNERABILITY"]["clinical_direction"] == "investigate"
    assert flags["RF-UNIVERSAL-PEDIATRIC-SPECIALIST-REVIEW"]["clinical_direction"] == "investigate"
    assert flags["RF-UNIVERSAL-OLDER-ADULT-VULNERABILITY"].get("shifts_algorithm") == []
    assert flags["RF-UNIVERSAL-PEDIATRIC-SPECIALIST-REVIEW"].get("shifts_algorithm") == []

    assert evaluate_redflag_trigger(
        flags["RF-UNIVERSAL-OLDER-ADULT-VULNERABILITY"]["trigger"],
        {"age_years": 72, "ecog_status": 2},
    )
    assert evaluate_redflag_trigger(
        flags["RF-UNIVERSAL-PEDIATRIC-SPECIALIST-REVIEW"]["trigger"],
        {"age_years": 9},
    )

    algorithm_refs = set()
    for info in result.entities_by_id.values():
        if info["type"] == "algorithms":
            algorithm_refs.update(_red_flag_references(info["data"].get("decision_tree") or []))
    assert not (ASSESSMENT_ONLY_IDS & algorithm_refs)
