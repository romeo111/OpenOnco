"""Bulk-generate STUB Questionnaire YAMLs for diseases without one.

Hybrid Variant 3 of the try.html dropdown gap fix:
  - 3 hand-authored questionnaires existed for CLL/HCV-MZL/MM
  - 62 diseases lacked any → dropdown showed only 3
  - This generator creates a baseline STUB for each missing disease
    so users can at least pick the disease in the dropdown and see
    the engine routing/render end-to-end. Clinicians deepen priority
    diseases (BREAST/CRC/NSCLC/DLBCL first) over time.

Each generated YAML carries `_stub_auto_generated: true` flag so:
  - downstream tooling can filter or warn
  - try.html can show "Preliminary auto-generated questionnaire" banner
  - clinical-content reviewers can target-search for review work

The generator pulls:
  - patient_id + demographics (age/sex/ECOG/line) — universal
  - biomarkers from Indication.applicable_to.biomarker_requirements_required
    (so the form asks about exactly the biomarkers the engine routes on)
  - HBV/HCV serology + cytopenias + key findings — universal safety panel

Idempotent: skips files that already exist. Safe to re-run after KB grows.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
QUEST_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "questionnaires"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from knowledge_base.validation.loader import load_content  # noqa: E402


# ── Disease-id → quest-file basename ─────────────────────────────────────


def _filename_for(disease_id: str) -> str:
    """DIS-NSCLC → quest_nsclc_1l.yaml; DIS-MZL-HCV-MZL → quest_hcv_mzl_1l.yaml."""
    base = disease_id
    if base.startswith("DIS-"):
        base = base[4:]
    base = base.lower().replace("-", "_")
    return f"quest_{base}_1l.yaml"


# ── Question generation helpers ──────────────────────────────────────────


_BIOMARKER_HINT_QUESTIONS = {
    # Common patterns: each entry = (label, helper). For boolean biomarkers
    # we render a yes/no question; for known measurement biomarkers we render
    # an enum.
}


def _q_yaml_dict(d: dict) -> str:
    """Hand-render a YAML question as a list-item entry under
    `groups[].questions:`. First key gets `- ` dash prefix; subsequent
    keys are aligned. Indent matches canonical CLL example (6 spaces
    for first key after `- `, total visual indent 8)."""
    keys = list(d.items())
    lines = []
    for idx, (k, v) in enumerate(keys):
        # First key starts with `      - ` (6 spaces + dash + space);
        # subsequent keys with `        ` (8 spaces) so they align under
        # the first key's value column.
        prefix = "      - " if idx == 0 else "        "
        if isinstance(v, bool):
            lines.append(f"{prefix}{k}: {str(v).lower()}")
        elif isinstance(v, (int, float)):
            lines.append(f"{prefix}{k}: {v}")
        elif isinstance(v, list):
            if not v:
                continue
            lines.append(f"{prefix}{k}:")
            for item in v:
                if isinstance(item, dict):
                    parts = []
                    for ik, iv in item.items():
                        if isinstance(iv, str):
                            iv_s = f'"{iv}"'
                        elif isinstance(iv, bool):
                            iv_s = str(iv).lower()
                        else:
                            iv_s = str(iv)
                        parts.append(f"{ik}: {iv_s}")
                    lines.append("          - {" + ", ".join(parts) + "}")
                else:
                    lines.append(f'          - "{item}"')
        elif isinstance(v, str):
            # Quote when contains special chars or starts with reserved chars
            if "\n" in v or v.startswith(("-", "?", "*", "&", "[", "{", "|", ">")):
                lines.append(f"{prefix}{k}: |")
                for line in v.split("\n"):
                    lines.append(f"          {line}")
            else:
                escaped = v.replace('"', '\\"')
                lines.append(f'{prefix}{k}: "{escaped}"')
        else:
            lines.append(f"{prefix}{k}: {v}")
    return "\n".join(lines)


def _baseline_demographics_group(disease_short: str) -> str:
    """Universal demographics + ECOG block. Identical across diseases."""
    return f"""  - title: "Demographics + baseline status"
    description: "Base fields. ECOG 4 → engine routes to palliative track."
    questions:
{_q_yaml_dict({
    'field': 'patient_id',
    'label': 'Patient ID (synthetic)',
    'type': 'text',
    'impact': 'required',
    'default_value': f'VIRTUAL-{disease_short.upper()}-001',
})}

{_q_yaml_dict({
    'field': 'demographics.age',
    'label': 'Age',
    'type': 'integer',
    'impact': 'critical',
    'range_min': 18,
    'range_max': 110,
    'units': 'years',
    'default_value': 60,
})}

{_q_yaml_dict({
    'field': 'demographics.sex',
    'label': 'Sex',
    'type': 'enum',
    'impact': 'optional',
    'options': [{'value': 'male', 'label': 'Male'}, {'value': 'female', 'label': 'Female'}],
})}

{_q_yaml_dict({
    'field': 'demographics.ecog',
    'label': 'ECOG Performance Status',
    'type': 'enum',
    'impact': 'critical',
    'options': [
        {'value': 0, 'label': '0'},
        {'value': 1, 'label': '1'},
        {'value': 2, 'label': '2'},
        {'value': 3, 'label': '3'},
        {'value': 4, 'label': '4'},
    ],
    'helper': 'ECOG 4 → engine will not propose active treatment.',
    'default_value': 1,
})}

{_q_yaml_dict({
    'field': 'line_of_therapy',
    'label': 'Line of therapy',
    'type': 'integer',
    'impact': 'critical',
    'range_min': 1,
    'range_max': 5,
    'default_value': 1,
    'helper': 'This questionnaire targets 1L. For 2L+ use the extended JSON mode.',
})}
"""


def _safety_panel_group() -> str:
    """Universal HBV/HCV/HIV + cytopenia panel — relevant to most cancers
    that may receive immunosuppressive therapy."""
    return f"""  - title: "Baseline safety (virology + blood)"
    description: "Screening before systemic therapy. Engine uses this for RF-HBV-REACTIVATION-RISK etc."
    questions:
{_q_yaml_dict({
    'field': 'findings.hbsag',
    'label': 'HBsAg',
    'type': 'enum',
    'impact': 'critical',
    'options': [{'value': 'negative', 'label': 'Negative'}, {'value': 'positive', 'label': 'Positive'}],
    'helper': 'HBsAg+ → entecavir prophylaxis before anti-CD20/anti-CD38/cytotoxic immunosuppressive.',
    'default_value': 'negative',
})}

{_q_yaml_dict({
    'field': 'findings.anti_hbc_total',
    'label': 'Anti-HBc total',
    'type': 'enum',
    'impact': 'required',
    'options': [{'value': 'negative', 'label': 'Negative'}, {'value': 'positive', 'label': 'Positive (occult)'}],
    'default_value': 'negative',
})}

{_q_yaml_dict({
    'field': 'findings.hcv_status',
    'label': 'HCV status',
    'type': 'enum',
    'impact': 'recommended',
    'options': [
        {'value': 'negative', 'label': 'HCV-Ab negative'},
        {'value': 'cured', 'label': 'Anti-HCV+, RNA undetectable (cured / SVR)'},
        {'value': 'active', 'label': 'Active HCV (RNA+)'},
    ],
    'default_value': 'negative',
})}

{_q_yaml_dict({
    'field': 'findings.hiv_status',
    'label': 'HIV status',
    'type': 'enum',
    'impact': 'recommended',
    'options': [
        {'value': 'negative', 'label': 'Negative'},
        {'value': 'positive_controlled', 'label': 'Positive, on ART, vRNA undetectable'},
        {'value': 'positive_uncontrolled', 'label': 'Positive, uncontrolled'},
    ],
    'default_value': 'negative',
})}
"""


def _biomarker_group_from_disease(
    disease_id: str, biomarker_ids: list[str], entities_by_id: dict
) -> str:
    """Generate a "Biomarkers" group question per relevant biomarker.

    For each biomarker referenced by an indication for this disease,
    add a yes/no field at `biomarkers.<BIO-ID>`. The engine reads
    these directly. We don't try to be clever about value enums —
    real questionnaires need clinician-authored choices."""
    if not biomarker_ids:
        return ""

    questions = []
    for bio_id in sorted(biomarker_ids):
        bio_data = entities_by_id.get(bio_id, {}).get("data") or {}
        names = bio_data.get("names") or {}
        label = (names.get("preferred") or names.get("english") or bio_id)[:120]
        biomarker_type = bio_data.get("biomarker_type") or "unknown"

        # Boolean for gene mutations / fusions; enum (positive/negative) for
        # IHC/expression markers; freeform-disabled (text) for everything else.
        if biomarker_type in {"gene_mutation", "gene_fusion", "copy_number"}:
            q = {
                "field": f"biomarkers.{bio_id}",
                "label": f"{label}",
                "type": "boolean",
                "impact": "recommended",
                "helper": f"Engine routes through this biomarker if positive. Source: KB {bio_id}.",
                "default_value": False,
            }
        else:
            q = {
                "field": f"biomarkers.{bio_id}",
                "label": f"{label}",
                "type": "enum",
                "impact": "recommended",
                "options": [
                    {"value": "positive", "label": "Positive"},
                    {"value": "negative", "label": "Negative"},
                    {"value": "unknown", "label": "Unknown / pending"},
                ],
                "default_value": "unknown",
                "helper": f"Source: KB {bio_id}.",
            }
        questions.append(_q_yaml_dict(q))

    if not questions:
        return ""

    sep = "\n\n"
    return f"""  - title: "Biomarkers (auto-extracted from indications)"
    description: "Fields auto-generated from biomarker_requirements in disease Indications. To be refined by clinician."
    questions:
{sep.join(questions)}
"""


def _findings_pool_group() -> str:
    """A small open-ended findings block — the engine often reads
    extra findings (cytopenia values, organ dysfunction flags). Stub
    just ECOG-adjacent ones."""
    return f"""  - title: "Additional parameters"
    description: "Fill in what is available; the rest — engine will fall back to safe defaults."
    questions:
{_q_yaml_dict({
    'field': 'findings.creatinine_clearance_ml_min',
    'label': 'Creatinine clearance (CrCl, mL/min)',
    'type': 'integer',
    'impact': 'recommended',
    'range_min': 5,
    'range_max': 200,
    'units': 'mL/min',
    'helper': '<30 → renal-impaired regimens; <60 → dose modify many cytotoxics.',
    'default_value': 90,
})}

{_q_yaml_dict({
    'field': 'findings.bilirubin_uln_x',
    'label': 'Bilirubin × ULN',
    'type': 'float',
    'impact': 'recommended',
    'range_min': 0,
    'range_max': 20,
    'units': '× ULN',
    'helper': '>1.5× ULN → hepatic-impairment regimens.',
    'default_value': 1.0,
})}

{_q_yaml_dict({
    'field': 'findings.absolute_neutrophil_count_k_ul',
    'label': 'ANC (K/μL)',
    'type': 'float',
    'impact': 'recommended',
    'range_min': 0,
    'range_max': 50,
    'units': 'K/μL',
    'helper': '<1.0 K/μL — engine will add G-CSF prophylaxis.',
    'default_value': 2.5,
})}

{_q_yaml_dict({
    'field': 'findings.platelets_k_ul',
    'label': 'Platelets (K/μL)',
    'type': 'integer',
    'impact': 'recommended',
    'range_min': 0,
    'range_max': 1000,
    'units': 'K/μL',
    'helper': '<75 — many regimens dose-modify; <50 — hold most cytotoxics.',
    'default_value': 200,
})}
"""


def _build_questionnaire_yaml(
    disease_id: str,
    disease_data: dict,
    biomarker_ids: list[str],
    entities_by_id: dict,
) -> str:
    """Compose full YAML text for one stub questionnaire."""
    short = disease_id.replace("DIS-", "")
    quest_id = f"QUEST-{short}-1L-STUB"
    names = disease_data.get("names") or {}
    name_en = names.get("english") or names.get("preferred") or short
    icd_o3 = (disease_data.get("codes") or {}).get("icd_o_3_morphology") or ""

    title = f"{name_en} — first line (auto-generated STUB)"

    # Header
    out = [
        f"id: {quest_id}",
        f"disease_id: {disease_id}",
        "line_of_therapy: 1",
        f'title: "{title}"',
        "",
        "_stub_auto_generated: true",
        "_stub_reason: |",
        "  Auto-generated by scripts/generate_stub_questionnaires.py to unblock",
        "  /try.html dropdown coverage. PRELIMINARY — NOT clinically signed off.",
        "  Engine routing works end-to-end with these defaults; specific",
        "  thresholds and biomarker enums may need clinician adjustment per CHARTER §6.1.",
        "",
        "intro: >",
        f"  ⚠ STUB questionnaire for {name_en}. Auto-filled from KB",
        "  metadata. Allows running end-to-end engine + render to understand",
        "  the algorithmic pathway, but clinical details are lacking — questions",
        "  are simplified, defaults are conservative. Awaiting clinical co-lead review.",
        "",
        "fixed_fields:",
    ]
    if icd_o3:
        out.append("  disease:")
        out.append(f'    icd_o_3_morphology: "{icd_o3}"')
    else:
        out.append("  disease:")
        out.append(f'    id: "{disease_id}"')
    out.append("  line_of_therapy: 1")
    out.append("")

    out.append("groups:")
    out.append(_baseline_demographics_group(short.lower()))
    bio_group = _biomarker_group_from_disease(disease_id, biomarker_ids, entities_by_id)
    if bio_group:
        out.append(bio_group)
    out.append(_safety_panel_group())
    out.append(_findings_pool_group())

    out.append("sources: []")
    out.append('last_reviewed: "2026-04-27"')
    out.append("reviewer_signoffs: 0")
    out.append("")
    out.append("notes: >")
    out.append("  STUB auto-generated 2026-04-27. Required: clinician review of biomarker")
    out.append("  question wording, defaults, missing disease-specific risk factors.")

    return "\n".join(out) + "\n"


# ── Walker ───────────────────────────────────────────────────────────────


def _collect_disease_biomarkers(entities_by_id: dict) -> dict[str, set[str]]:
    """{disease_id: {biomarker_id, ...}} from indications applicable to it."""
    out: dict[str, set[str]] = defaultdict(set)
    for eid, info in entities_by_id.items():
        if info["type"] != "indications":
            continue
        d = info["data"]
        applicable = d.get("applicable_to") or {}
        if not isinstance(applicable, dict):
            continue
        disease_id = applicable.get("disease_id") or applicable.get("disease")
        if not disease_id:
            continue

        # Walk for biomarker references
        def _walk(node):
            if isinstance(node, dict):
                for k, v in node.items():
                    if k == "biomarker_id" and isinstance(v, str):
                        out[disease_id].add(v)
                    else:
                        _walk(v)
            elif isinstance(node, list):
                for item in node:
                    _walk(item)
            elif isinstance(node, str):
                if node.startswith("BIO-"):
                    out[disease_id].add(node)

        _walk(d)
    return out


def main() -> int:
    QUEST_DIR.mkdir(parents=True, exist_ok=True)

    load = load_content(REPO_ROOT / "knowledge_base" / "hosted" / "content")
    if not load.ok and load.schema_errors:
        print("WARN: KB has schema errors — proceeding anyway", file=sys.stderr)

    existing_quest_diseases: set[str] = set()
    for eid, info in load.entities_by_id.items():
        if info["type"] == "questionnaires":
            d = info["data"].get("disease_id") or info["data"].get("applicable_to", {}).get("disease_id")
            if d:
                existing_quest_diseases.add(d)

    biomarker_index = _collect_disease_biomarkers(load.entities_by_id)

    written: list[str] = []
    skipped_existing = 0
    processed_diseases: set[str] = set()
    for eid, info in sorted(load.entities_by_id.items()):
        if info["type"] != "diseases":
            continue
        processed_diseases.add(eid)
        if eid in existing_quest_diseases:
            skipped_existing += 1
            continue

        path = QUEST_DIR / _filename_for(eid)
        if path.exists():
            skipped_existing += 1
            continue

        bio_ids = sorted(biomarker_index.get(eid, set()))
        text = _build_questionnaire_yaml(eid, info["data"], bio_ids, load.entities_by_id)
        path.write_text(text, encoding="utf-8")
        written.append(eid)
        print(f"  + {path.name:50s} ({len(bio_ids)} biomarkers wired)")

    disease_dir = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "diseases"
    for disease_path in sorted(disease_dir.glob("*.yaml")):
        disease_data = yaml.safe_load(disease_path.read_text(encoding="utf-8")) or {}
        disease_id = disease_data.get("id")
        if not disease_id or disease_id in processed_diseases:
            continue
        path = QUEST_DIR / _filename_for(disease_id)
        if path.exists():
            skipped_existing += 1
            continue
        text = _build_questionnaire_yaml(disease_id, disease_data, [], load.entities_by_id)
        path.write_text(text, encoding="utf-8")
        written.append(disease_id)
        print(f"  + {path.name:50s} (0 biomarkers wired; disease-yaml fallback)")

    print(f"\nWrote {len(written)} stub questionnaires.")
    print(f"Skipped (already had questionnaire): {skipped_existing}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
