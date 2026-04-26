"""Clinical sign-off CLI for Clinical Co-Leads (CHARTER §6.1).

Workflow:
  1. Reviewer (Clinical Co-Lead) decides which entities they want to sign off on.
  2. They run `python scripts/clinical_signoff.py approve --reviewer REV-... --pattern ...`.
  3. Each matching entity gets a `ReviewerSignoff` appended to its
     `reviewer_signoffs_v2` list, plus a row appended to the audit log
     `knowledge_base/hosted/audit/signoffs.jsonl`.
  4. Two distinct reviewers (different REV-* IDs) covering the same
     entity satisfy CHARTER §6.1.

Sub-commands:
  approve    Add a sign-off to one or many entities.
  withdraw   Remove a sign-off (and append a withdraw row to the audit log).
  list       Show sign-offs for an entity OR by reviewer.

Usage examples:
    # Approve all DLBCL indications by hematology lead
    py scripts/clinical_signoff.py approve \\
        --reviewer REV-HEME-LEAD-PLACEHOLDER \\
        --pattern "indications/ind_dlbcl_*.yaml" \\
        --rationale "NCCN-aligned, evidence reviewed"

    # Approve a specific entity by ID
    py scripts/clinical_signoff.py approve \\
        --reviewer REV-SOLID-LEAD-PLACEHOLDER \\
        --entity-id IND-CRC-METASTATIC-2L-BRAF-BEACON \\
        --rationale "BEACON-CRC validated; UA NSZU coverage flagged"

    # Dry-run (show what would be approved without writing)
    py scripts/clinical_signoff.py approve \\
        --reviewer REV-HEME-LEAD-PLACEHOLDER \\
        --pattern "indications/ind_aml_*.yaml" \\
        --rationale "ELN-2022 aligned" \\
        --dry-run

    # Withdraw a sign-off (revoke approval)
    py scripts/clinical_signoff.py withdraw \\
        --reviewer REV-HEME-LEAD-PLACEHOLDER \\
        --entity-id IND-AML-1L-7-3 \\
        --rationale "Reconsider after IDH1+ subgroup data"

    # List sign-offs for an entity or reviewer
    py scripts/clinical_signoff.py list --entity-id IND-DLBCL-1L-RCHOP
    py scripts/clinical_signoff.py list --reviewer REV-HEME-LEAD-PLACEHOLDER

Exit codes:
  0  success
  2  argparse / arg error
  3  unknown reviewer
  4  no entities matched
  5  scope mismatch under --strict
  6  duplicate sign-off (without --force)
  7  entity has no reviewer_signoffs_v2 capability
  8  unknown entity (for withdraw / list)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from knowledge_base.schemas.reviewer_profile import ReviewerProfile  # noqa: E402

KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
REVIEWERS_DIR = KB_ROOT / "reviewers"
AUDIT_LOG = REPO_ROOT / "knowledge_base" / "hosted" / "audit" / "signoffs.jsonl"

# Entity types that are "clinical content" per CHARTER §6.1 — sign-off applies.
SIGNOFF_ELIGIBLE_DIRS = {
    "indications",
    "algorithms",
    "regimens",
    "redflags",
    "biomarker_actionability",
}

# Map dir name → entity-type label used in audit rows / dashboards.
ENTITY_TYPE_LABEL = {
    "indications": "Indication",
    "algorithms": "Algorithm",
    "regimens": "Regimen",
    "redflags": "RedFlag",
    "biomarker_actionability": "BiomarkerActionability",
}


# ── Disease-category inference ────────────────────────────────────────────
#
# Disease YAMLs don't carry a `category` field today, so the CLI infers it
# from the disease lineage / ID. This is a best-effort scope check; if the
# inference is wrong, the operator can pass `--no-strict` (default) to
# proceed with a warning.

HEME_LINEAGE_PREFIXES = (
    "b_cell", "t_cell", "myeloid", "plasma_cell", "lymphoid", "nk_cell",
    "histiocytic",
)
HEME_DISEASE_TOKENS = (
    "DLBCL", "FL", "CLL", "AML", "APL", "MM", "MCL", "CHL", "NLPBL",
    "ALCL", "AITL", "PTCL", "ATLL", "B-ALL", "T-ALL", "PMBCL", "PCNSL",
    "BURKITT", "HCL", "MZL", "SMZL", "NMZL", "WM", "MF", "SEZARY",
    "ET", "MDS", "CML", "MPN", "ADVSM", "HGBL", "TFL", "PTLD",
    "RICHTER", "PV", "PMF",
)
SOLID_DISEASE_TOKENS = (
    "BRCA", "CRC", "NSCLC", "SCLC", "LUNG", "PROSTATE", "BLADDER",
    "OVARIAN", "ENDOMETRIAL", "CERVICAL", "GASTRIC", "ESOPH", "PANC",
    "HCC", "CHOLANGIO", "MELANOMA", "HNSCC", "MTC", "GIST", "SARCOMA",
    "RENAL", "GLIOMA", "MENINGIOMA", "TESTICULAR", "BREAST",
    "CHONDROSARCOMA", "OSTEOSARCOMA",
)


def _infer_disease_category(disease_id: Optional[str], disease_lineage: Optional[str]) -> set[str]:
    """Return tags like {'hematologic', 'lymphoid'} or {'solid', 'breast'}.

    Prefers `lineage` field when present (Disease.lineage); falls back to
    token match on the DIS-* ID. Empty set when unknown."""
    tags: set[str] = set()
    lin = (disease_lineage or "").lower()
    did = (disease_id or "").upper().replace("DIS-", "")

    if any(lin.startswith(p) for p in HEME_LINEAGE_PREFIXES):
        tags.add("hematologic")
        if "lymph" in lin or "b_cell" in lin or "t_cell" in lin:
            tags.add("lymphoid")
        if "myeloid" in lin:
            tags.add("myeloid")
        if "plasma" in lin:
            tags.add("plasma-cell")

    for tok in HEME_DISEASE_TOKENS:
        if tok in did.split("-"):
            tags.add("hematologic")
            if tok in ("AML", "APL", "MDS", "CML", "MPN", "PV", "PMF", "ET"):
                tags.add("myeloid")
            elif tok in ("MM", "WM"):
                tags.add("plasma-cell")
            else:
                tags.add("lymphoid")
            break

    for tok in SOLID_DISEASE_TOKENS:
        if tok in did:
            tags.add("solid")
            if tok in ("CRC", "GASTRIC", "ESOPH", "PANC", "HCC", "CHOLANGIO", "GIST"):
                tags.add("gastrointestinal")
            elif tok in ("BREAST", "BRCA"):
                tags.add("breast")
            elif tok in ("PROSTATE", "BLADDER", "TESTICULAR", "RENAL"):
                tags.add("gu")
            elif tok in ("OVARIAN", "ENDOMETRIAL", "CERVICAL"):
                tags.add("gyn")
            elif tok in ("NSCLC", "SCLC", "LUNG"):
                tags.add("thoracic")
            elif tok in ("GLIOMA", "MENINGIOMA"):
                tags.add("cns")
            elif tok in ("HNSCC", "MTC"):
                tags.add("hnscc")
            elif "SARCOMA" in tok:
                tags.add("sarcoma")
            elif tok == "MELANOMA":
                tags.add("melanoma")
            break
    return tags


# ── Reviewer + entity loaders ─────────────────────────────────────────────


def _load_reviewer(reviewer_id: str) -> Optional[ReviewerProfile]:
    """Resolve REV-* by scanning the reviewers/ directory."""
    if not REVIEWERS_DIR.is_dir():
        return None
    for p in sorted(REVIEWERS_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and data.get("id") == reviewer_id:
            try:
                return ReviewerProfile.model_validate(data)
            except Exception:
                return None
    return None


def _entity_dir_for_id(entity_id: str) -> Optional[str]:
    """Heuristic: map ID prefix → entity dir name."""
    eid = entity_id.upper()
    if eid.startswith("IND-"):
        return "indications"
    if eid.startswith("ALGO-"):
        return "algorithms"
    if eid.startswith("REG-"):
        return "regimens"
    if eid.startswith("RF-"):
        return "redflags"
    if eid.startswith("BMA-"):
        return "biomarker_actionability"
    return None


def _find_entity_path(entity_id: str) -> Optional[tuple[Path, str]]:
    """Walk SIGNOFF_ELIGIBLE_DIRS, return (path, dir_name) or None."""
    expected_dir = _entity_dir_for_id(entity_id)
    dirs_to_search = [expected_dir] if expected_dir else list(SIGNOFF_ELIGIBLE_DIRS)
    for d in dirs_to_search:
        if d is None:
            continue
        root = KB_ROOT / d
        if not root.is_dir():
            continue
        for p in sorted(root.rglob("*.yaml")):
            try:
                raw = yaml.safe_load(p.read_text(encoding="utf-8"))
            except yaml.YAMLError:
                continue
            if isinstance(raw, dict) and raw.get("id") == entity_id:
                return p, d
    return None


def _resolve_pattern(pattern: str) -> list[tuple[Path, str]]:
    """Pattern is glob relative to KB_ROOT, e.g. 'indications/ind_dlbcl_*.yaml'."""
    out: list[tuple[Path, str]] = []
    parts = pattern.replace("\\", "/").split("/", 1)
    if len(parts) != 2:
        return out
    dir_name, glob = parts
    if dir_name not in SIGNOFF_ELIGIBLE_DIRS:
        return out
    root = KB_ROOT / dir_name
    if not root.is_dir():
        return out
    for p in sorted(root.rglob(glob)):
        if p.is_file() and p.suffix == ".yaml":
            out.append((p, dir_name))
    return out


def _load_disease(disease_id: Optional[str]) -> Optional[dict]:
    if not disease_id:
        return None
    diseases_dir = KB_ROOT / "diseases"
    if not diseases_dir.is_dir():
        return None
    for p in sorted(diseases_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and data.get("id") == disease_id:
            return data
    return None


def _entity_disease_id(data: dict, dir_name: str) -> Optional[str]:
    """Best-effort extract of the disease ID an entity targets."""
    if dir_name == "indications":
        a = data.get("applicable_to") or {}
        return a.get("disease_id") if isinstance(a, dict) else None
    if dir_name == "algorithms":
        return data.get("applicable_to_disease")
    if dir_name == "regimens":
        # Regimens are disease-agnostic in schema; defer to N/A.
        return None
    if dir_name == "redflags":
        rd = data.get("relevant_diseases") or []
        if isinstance(rd, list) and rd and isinstance(rd[0], str) and rd[0] != "*":
            return rd[0]
        return None
    if dir_name == "biomarker_actionability":
        return data.get("disease_id")
    return None


# ── Scope check ───────────────────────────────────────────────────────────


def _scope_match(reviewer: ReviewerProfile, entity_data: dict, dir_name: str) -> tuple[bool, str]:
    """Return (in_scope, reason). Reason explains the verdict."""
    scope = reviewer.sign_off_scope

    # Entity-type gate
    if scope.entity_types and dir_name not in scope.entity_types:
        return False, f"reviewer scope excludes entity_type '{dir_name}'"

    # Disease ID exact-match shortcut
    disease_id = _entity_disease_id(entity_data, dir_name)
    if scope.disease_ids:
        if disease_id and disease_id in scope.disease_ids:
            return True, f"disease_id '{disease_id}' on explicit allow-list"
        return False, f"disease_id '{disease_id}' not on reviewer's explicit allow-list"

    # Disease-category check
    if scope.disease_categories:
        disease_data = _load_disease(disease_id) or {}
        lineage = disease_data.get("lineage") if isinstance(disease_data, dict) else None
        inferred = _infer_disease_category(disease_id, lineage)
        if not inferred:
            return False, f"could not infer disease category for '{disease_id}'"
        overlap = inferred & set(scope.disease_categories)
        if overlap:
            return True, f"category match: {sorted(overlap)}"
        return False, (
            f"reviewer covers {sorted(scope.disease_categories)} "
            f"but entity disease '{disease_id}' is {sorted(inferred)}"
        )

    # No restriction → in-scope
    return True, "reviewer has no disease-category restriction"


# ── YAML round-trip preserving comments where possible ────────────────────


def _read_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _write_yaml(path: Path, data: dict) -> None:
    """Write YAML with stable key order, no flow style."""
    text = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=120,
    )
    path.write_text(text, encoding="utf-8")


# ── Audit log ─────────────────────────────────────────────────────────────


def _now_iso_z() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _today_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _append_audit(row: dict) -> None:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(row, ensure_ascii=False, sort_keys=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


# ── Approve ───────────────────────────────────────────────────────────────


def cmd_approve(args: argparse.Namespace) -> int:
    reviewer = _load_reviewer(args.reviewer)
    if reviewer is None:
        print(f"ERR: reviewer '{args.reviewer}' not found in {REVIEWERS_DIR}", file=sys.stderr)
        return 3

    targets: list[tuple[Path, str]] = []
    if args.entity_id:
        hit = _find_entity_path(args.entity_id)
        if not hit:
            print(f"ERR: entity '{args.entity_id}' not found", file=sys.stderr)
            return 4
        targets.append(hit)
    if args.pattern:
        targets.extend(_resolve_pattern(args.pattern))

    if not targets:
        print("ERR: no entities matched. Pass --entity-id and/or --pattern.", file=sys.stderr)
        return 4

    approved = 0
    skipped_dup = 0
    skipped_scope = 0
    skipped_ineligible = 0
    today = _today_iso()
    ts = _now_iso_z()

    for path, dir_name in targets:
        if dir_name not in SIGNOFF_ELIGIBLE_DIRS:
            print(f"  SKIP (not signoff-eligible): {path.relative_to(REPO_ROOT)}")
            skipped_ineligible += 1
            continue

        data = _read_yaml(path)
        eid = data.get("id") or "?"

        # Scope check
        in_scope, reason = _scope_match(reviewer, data, dir_name)
        if not in_scope:
            if args.strict:
                print(f"  REFUSE (scope, --strict): {eid} — {reason}", file=sys.stderr)
                skipped_scope += 1
                continue
            else:
                print(f"  WARN (scope mismatch, proceeding): {eid} — {reason}")

        # Duplicate check
        existing = data.get("reviewer_signoffs_v2") or []
        if not isinstance(existing, list):
            existing = []
        if any(isinstance(s, dict) and s.get("reviewer_id") == args.reviewer for s in existing):
            if not args.force:
                print(f"  SKIP (duplicate sign-off, use --force to override): {eid}")
                skipped_dup += 1
                continue

        signoff_entry = {
            "reviewer_id": args.reviewer,
            "signoff_date": today,
            "rationale": args.rationale,
            "entity_version_at_signoff": data.get("last_reviewed") or today,
            "scope_match": in_scope,
        }
        existing.append(signoff_entry)
        data["reviewer_signoffs_v2"] = existing
        # Also bump the legacy counter so existing render / coverage tooling
        # that reads `reviewer_signoffs: int` stays in sync.
        if dir_name == "indications":
            data["reviewer_signoffs"] = len([
                s for s in existing if isinstance(s, dict)
            ])
            data["last_reviewed"] = today

        if args.dry_run:
            print(f"  DRY-RUN approve: {eid} ({path.relative_to(REPO_ROOT)})")
        else:
            _write_yaml(path, data)
            _append_audit({
                "timestamp": ts,
                "action": "approve",
                "reviewer_id": args.reviewer,
                "entity_id": eid,
                "entity_type": ENTITY_TYPE_LABEL.get(dir_name, dir_name),
                "rationale": args.rationale,
                "entity_version_at_signoff": signoff_entry["entity_version_at_signoff"],
                "scope_match": in_scope,
            })
            print(f"  APPROVE: {eid}")
        approved += 1

    print(
        f"\nDone: {approved} approved, "
        f"{skipped_dup} skipped (duplicate), "
        f"{skipped_scope} refused (scope+strict), "
        f"{skipped_ineligible} skipped (ineligible type)."
    )
    if args.dry_run:
        print("(dry-run — nothing written)")
    return 0


# ── Withdraw ──────────────────────────────────────────────────────────────


def cmd_withdraw(args: argparse.Namespace) -> int:
    reviewer = _load_reviewer(args.reviewer)
    if reviewer is None:
        print(f"ERR: reviewer '{args.reviewer}' not found", file=sys.stderr)
        return 3

    hit = _find_entity_path(args.entity_id)
    if not hit:
        print(f"ERR: entity '{args.entity_id}' not found", file=sys.stderr)
        return 8
    path, dir_name = hit

    data = _read_yaml(path)
    eid = data.get("id") or "?"
    existing = data.get("reviewer_signoffs_v2") or []
    if not isinstance(existing, list):
        existing = []

    new_list = [
        s for s in existing
        if not (isinstance(s, dict) and s.get("reviewer_id") == args.reviewer)
    ]
    if len(new_list) == len(existing):
        print(f"ERR: no sign-off by {args.reviewer} on {eid} to withdraw", file=sys.stderr)
        return 6

    data["reviewer_signoffs_v2"] = new_list
    if dir_name == "indications":
        data["reviewer_signoffs"] = len([s for s in new_list if isinstance(s, dict)])

    if args.dry_run:
        print(f"DRY-RUN withdraw: {eid} (would remove {args.reviewer} sign-off)")
        return 0

    _write_yaml(path, data)
    _append_audit({
        "timestamp": _now_iso_z(),
        "action": "withdraw",
        "reviewer_id": args.reviewer,
        "entity_id": eid,
        "entity_type": ENTITY_TYPE_LABEL.get(dir_name, dir_name),
        "rationale": args.rationale or "",
        "entity_version_at_signoff": data.get("last_reviewed") or _today_iso(),
        "scope_match": True,  # withdraw never blocked by scope
    })
    print(f"WITHDRAW: {eid} — {args.reviewer}")
    return 0


# ── List ──────────────────────────────────────────────────────────────────


def cmd_list(args: argparse.Namespace) -> int:
    if args.entity_id:
        hit = _find_entity_path(args.entity_id)
        if not hit:
            print(f"ERR: entity '{args.entity_id}' not found", file=sys.stderr)
            return 8
        path, dir_name = hit
        data = _read_yaml(path)
        signoffs = data.get("reviewer_signoffs_v2") or []
        print(f"{data.get('id')} ({ENTITY_TYPE_LABEL.get(dir_name, dir_name)}) — "
              f"{len(signoffs)} sign-off(s)")
        for s in signoffs:
            if not isinstance(s, dict):
                continue
            print(f"  - {s.get('reviewer_id')} on {s.get('signoff_date')} "
                  f"(scope_match={s.get('scope_match')}): {s.get('rationale', '')[:80]}")
        return 0

    if args.reviewer:
        rows = []
        for d in SIGNOFF_ELIGIBLE_DIRS:
            root = KB_ROOT / d
            if not root.is_dir():
                continue
            for p in sorted(root.rglob("*.yaml")):
                try:
                    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
                except yaml.YAMLError:
                    continue
                for s in data.get("reviewer_signoffs_v2") or []:
                    if isinstance(s, dict) and s.get("reviewer_id") == args.reviewer:
                        rows.append((data.get("id"), d, s.get("signoff_date")))
        print(f"{args.reviewer} — {len(rows)} sign-off(s)")
        for eid, d, date in sorted(rows, key=lambda r: (r[2] or "", r[0] or "")):
            print(f"  - [{date}] {eid} ({ENTITY_TYPE_LABEL.get(d, d)})")
        return 0

    print("ERR: list requires --entity-id or --reviewer", file=sys.stderr)
    return 2


# ── Argparse wiring ───────────────────────────────────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="clinical_signoff",
        description="Clinical sign-off CLI (CHARTER §6.1).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    # approve
    a = sub.add_parser("approve", help="Add sign-off to one or many entities.")
    a.add_argument("--reviewer", required=True, help="REV-* reviewer profile ID")
    a.add_argument("--entity-id", help="Single entity by ID (IND-*, ALGO-*, REG-*, RF-*, BMA-*)")
    a.add_argument("--pattern", help="Glob relative to KB content root, e.g. 'indications/ind_dlbcl_*.yaml'")
    a.add_argument("--rationale", required=True, help="Clinical rationale (free text, mandatory)")
    a.add_argument("--dry-run", action="store_true", help="Print what would change without writing")
    a.add_argument("--strict", action="store_true", help="Refuse to proceed on scope mismatch (default: warn)")
    a.add_argument("--force", action="store_true", help="Allow duplicate sign-off (re-affirm)")
    a.set_defaults(func=cmd_approve)

    # withdraw
    w = sub.add_parser("withdraw", help="Remove a sign-off (audit row preserved).")
    w.add_argument("--reviewer", required=True)
    w.add_argument("--entity-id", required=True)
    w.add_argument("--rationale", default="", help="Why withdrawing (recommended)")
    w.add_argument("--dry-run", action="store_true")
    w.set_defaults(func=cmd_withdraw)

    # list
    L = sub.add_parser("list", help="Show sign-offs for an entity OR by reviewer.")
    L.add_argument("--entity-id")
    L.add_argument("--reviewer")
    L.set_defaults(func=cmd_list)

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
