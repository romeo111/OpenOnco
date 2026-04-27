"""CSD-7A: Generate transformation plan for free-text MDT-only `all_of` blocks.

Walks all algorithm YAMLs flagged with the standard MDT-only note, replaces
condition-text items that map to CSD-7A pan-disease RFs (fitness, organ
function, CAR-T eligibility, prior BTKi), and emits a JSON plan + applies
in-place rewrites of the matching `all_of` block in the YAML text.

Targeted patterns (only direct, unambiguous textual signals):
  - "ECOG ≤ 1" / "ECOG 0-1"        → red_flag: RF-FITNESS-ECOG-FIT
  - "ECOG ≤ 2" / "ECOG 0-2"        → any_of [FIT, INTERMEDIATE]
  - "ECOG ≤ 3"                     → not mapped (POOR fires at ≥3, ambiguous)
  - "CrCl ≥ N"                     → none_of [RF-ORGAN-RENAL-IMPAIRED]
  - "LVEF ≥ N"                     → none_of [RF-ORGAN-CARDIAC-LVEF-LOW]
  - "Child-Pugh A"                 → none_of [HEPATIC-B, HEPATIC-C]
  - "CAR-T-eligible" / center ref. → red_flag: RF-CAR-T-ELIGIBLE
  - "cBTKi-naive"                  → none_of [RF-PRIOR-BTKI-PROGRESSION]

After matching, residual condition text (if any) is preserved as a sibling
`condition` item, ensuring the AND-conjunction semantics are unchanged.

This script is idempotent: re-running on already-restructured files is a
no-op (because the marker note is rewritten on first pass).
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

ECOG_LE1 = re.compile(r"\bECOG\s*(?:[≤<]=?|0[-–])\s*1\b", re.IGNORECASE)
ECOG_LE2 = re.compile(r"\bECOG\s*(?:[≤<]=?|0[-–])\s*2\b", re.IGNORECASE)
ECOG_LE3 = re.compile(r"\bECOG\s*(?:[≤<]=?|0[-–])\s*3\b", re.IGNORECASE)
CRCL = re.compile(r"\bCrCl\s*[≥>]=?\s*\d+(?:\s*mL/min)?", re.IGNORECASE)
LVEF = re.compile(r"\bLVEF\s*[≥>]=?\s*\d+\s*%?", re.IGNORECASE)
CHILD_A = re.compile(r"Child[-\s]?Pugh\s*A(?:\s*\([^)]*\))?", re.IGNORECASE)
CART_ELIG = re.compile(
    r"CAR-T[- ]eligible[^,;\n]*|CAR-T\s+center\s+referral[^,;\n]*", re.IGNORECASE
)
BTKI_NAIVE = re.compile(
    r"\bcBTKi[-\s]?naive[^,;\n)]*|\bBTKi[-\s]?naive[^,;\n)]*", re.IGNORECASE
)


def cleanup_residual(s: str | None) -> str | None:
    if not s:
        return None
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\s+", " ", s)
        s = re.sub(r"\(\s*[,;:\s]*\)", "", s)
        s = re.sub(r"\(\s*,\s*", "(", s)
        s = re.sub(r"\s*,\s*\)", ")", s)
        s = re.sub(r"^[,;:.\s/+()-]+", "", s)
        s = re.sub(r"[,;:.\s/+()-]+$", "", s)
        s = re.sub(r"[,;]\s*[,;]", ",", s)
        s = re.sub(r"\(\s*\)", "", s)
        s = s.strip()
    while s.count("(") > s.count(")"):
        s += ")"
    while s.count(")") > s.count("("):
        s = "(" + s
    if not s or len(s) < 6:
        return None
    if re.fullmatch(
        r"(?:and|or|adequate organ function|mL/min|transplant[- ]eligible)[\s,;:./()+-]*",
        s,
        re.IGNORECASE,
    ):
        return None
    return s


def transform_condition(text: str):
    """Return (new_clauses, residual_text_or_None, changed_bool)."""
    new = []
    residual = text
    if ECOG_LE3.search(residual):
        return [], text, False
    if ECOG_LE2.search(residual):
        new.append(
            {
                "any_of": [
                    {"red_flag": "RF-FITNESS-ECOG-FIT"},
                    {"red_flag": "RF-FITNESS-ECOG-INTERMEDIATE"},
                ]
            }
        )
        residual = ECOG_LE2.sub("", residual)
    elif ECOG_LE1.search(residual):
        new.append({"red_flag": "RF-FITNESS-ECOG-FIT"})
        residual = ECOG_LE1.sub("", residual)
    if CRCL.search(residual):
        new.append({"none_of": [{"red_flag": "RF-ORGAN-RENAL-IMPAIRED"}]})
        residual = CRCL.sub("", residual)
    if LVEF.search(residual):
        new.append({"none_of": [{"red_flag": "RF-ORGAN-CARDIAC-LVEF-LOW"}]})
        residual = LVEF.sub("", residual)
    if CHILD_A.search(residual):
        new.append(
            {
                "none_of": [
                    {"red_flag": "RF-ORGAN-HEPATIC-CHILD-PUGH-B"},
                    {"red_flag": "RF-ORGAN-HEPATIC-CHILD-PUGH-C"},
                ]
            }
        )
        residual = CHILD_A.sub("", residual)
    if CART_ELIG.search(residual):
        new.append({"red_flag": "RF-CAR-T-ELIGIBLE"})
        residual = CART_ELIG.sub("", residual)
    if BTKI_NAIVE.search(residual):
        new.append({"none_of": [{"red_flag": "RF-PRIOR-BTKI-PROGRESSION"}]})
        residual = BTKI_NAIVE.sub("", residual)
    if not new:
        return [], text, False
    # Dedupe: drop any later occurrence equal to an earlier one
    seen = []
    deduped = []
    for c in new:
        key = json.dumps(c, sort_keys=True)
        if key in seen:
            continue
        seen.append(key)
        deduped.append(c)
    return deduped, cleanup_residual(residual), True


MDT_NOTE_MARKER = "multi-condition fitness/eligibility AND-conjunction"


def build_plan(base: Path) -> list:
    results = []
    for fp in sorted(base.glob("*.yaml")):
        text = fp.read_text(encoding="utf-8")
        if MDT_NOTE_MARKER not in text:
            continue
        with open(fp, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        file_changes = []
        for step in data.get("decision_tree") or []:
            notes = step.get("notes") or ""
            if MDT_NOTE_MARKER not in notes:
                continue
            ev = step.get("evaluate") or {}
            allof = ev.get("all_of") or []
            if not allof:
                continue
            new_allof = []
            any_changed = False
            all_mappable = True
            seen_clauses: set[str] = set()

            def push(clause: dict) -> None:
                key = json.dumps(clause, sort_keys=True)
                if key in seen_clauses:
                    return
                seen_clauses.add(key)
                new_allof.append(clause)

            for c in allof:
                if isinstance(c, dict) and "condition" in c:
                    new_clauses, residual, changed = transform_condition(c["condition"])
                    if changed:
                        any_changed = True
                        for nc in new_clauses:
                            push(nc)
                        if residual:
                            push({"condition": residual})
                            all_mappable = False
                    else:
                        push(c)
                        all_mappable = False
                else:
                    push(c)
            if not any_changed:
                continue
            if all_mappable:
                new_note = (
                    "Wired via CSD-7A pan-disease fitness/eligibility/prior-therapy RFs."
                )
            else:
                new_note = (
                    "Partially wired - fitness/eligibility gates wired via CSD-7A "
                    "pan-disease RFs; remaining condition(s) kept as MDT-evaluated "
                    "text (no RF available for that criterion)."
                )
            file_changes.append(
                {
                    "step": step.get("step"),
                    "old_allof": allof,
                    "new_allof": new_allof,
                    "new_note": new_note,
                }
            )
        if file_changes:
            results.append({"file": str(fp).as_posix() if hasattr(str(fp), "as_posix") else str(fp).replace("\\", "/"), "changes": file_changes})
    return results


def apply_plan(base: Path, family_filter: list[str] | None = None) -> dict:
    """Walk YAMLs, transform matching all_of blocks, write back.

    family_filter: if provided, only files whose stem starts with one of the
    provided prefixes are written. Used to commit by family.
    """
    import io as _io

    counts = {"files": 0, "blocks": 0, "full": 0, "partial": 0, "rfs": 0}
    for fp in sorted(base.glob("*.yaml")):
        text = fp.read_text(encoding="utf-8")
        if MDT_NOTE_MARKER not in text:
            continue
        if family_filter is not None:
            stem = fp.stem  # e.g., algo_dlbcl_1l
            if not any(stem.startswith(prefix) for prefix in family_filter):
                continue
        with open(fp, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        file_changed = False
        for step in data.get("decision_tree") or []:
            notes = step.get("notes") or ""
            if MDT_NOTE_MARKER not in notes:
                continue
            ev = step.get("evaluate") or {}
            allof = ev.get("all_of") or []
            if not allof:
                continue
            new_allof: list[dict] = []
            any_changed = False
            all_mappable = True
            seen_clauses: set[str] = set()

            def push(clause: dict) -> None:
                key = json.dumps(clause, sort_keys=True)
                if key in seen_clauses:
                    return
                seen_clauses.add(key)
                new_allof.append(clause)

            for c in allof:
                if isinstance(c, dict) and "condition" in c:
                    new_clauses, residual, changed = transform_condition(c["condition"])
                    if changed:
                        any_changed = True
                        for nc in new_clauses:
                            push(nc)
                        if residual:
                            push({"condition": residual})
                            all_mappable = False
                    else:
                        push(c)
                        all_mappable = False
                else:
                    push(c)
            if not any_changed:
                continue
            ev["all_of"] = new_allof
            if all_mappable:
                step["notes"] = (
                    "Wired via CSD-7A pan-disease fitness/eligibility/prior-therapy RFs."
                )
                counts["full"] += 1
            else:
                step["notes"] = (
                    "Partially wired - fitness/eligibility gates wired via CSD-7A "
                    "pan-disease RFs; remaining condition(s) kept as MDT-evaluated "
                    "text (no RF available for that criterion)."
                )
                counts["partial"] += 1
            counts["blocks"] += 1
            counts["rfs"] += sum(
                1
                for x in new_allof
                if isinstance(x, dict)
                and ("red_flag" in x or "any_of" in x or "none_of" in x)
            )
            file_changed = True
        if file_changed:
            buf = _io.StringIO()
            yaml.safe_dump(
                data, buf, sort_keys=False, allow_unicode=True, width=10000
            )
            fp.write_text(buf.getvalue(), encoding="utf-8")
            counts["files"] += 1
    return counts


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--family", nargs="*", help="filter by stem prefix")
    args = parser.parse_args()
    base = Path("knowledge_base/hosted/content/algorithms")
    if args.apply:
        counts = apply_plan(base, family_filter=args.family)
        print(f"Applied. files={counts['files']} blocks={counts['blocks']} "
              f"full={counts['full']} partial={counts['partial']} rfs={counts['rfs']}",
              file=sys.stderr)
        sys.exit(0)
    plan = build_plan(base)
    n_files = len(plan)
    n_blocks = sum(len(r["changes"]) for r in plan)
    n_full = 0
    n_partial = 0
    n_clauses = 0
    for r in plan:
        for c in r["changes"]:
            if "Partially" in c["new_note"]:
                n_partial += 1
            else:
                n_full += 1
            n_clauses += sum(
                1
                for x in c["new_allof"]
                if isinstance(x, dict)
                and ("red_flag" in x or "any_of" in x or "none_of" in x)
            )
    print(f"Files affected: {n_files}", file=sys.stderr)
    print(f"Blocks transformed: {n_blocks}", file=sys.stderr)
    print(f"Full conversions: {n_full}", file=sys.stderr)
    print(f"Partial conversions: {n_partial}", file=sys.stderr)
    print(f"Structured RF clauses added: {n_clauses}", file=sys.stderr)
    out = Path("/tmp/csd7a_plan.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"plan written: {out}", file=sys.stderr)
