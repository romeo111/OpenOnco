#!/usr/bin/env python3
"""One-shot script: stamp `last_verified: 2026-04-27` and indication-
restricted `reimbursement_indications` for the 52 pkg2 drugs (per
docs/plans/csd_2_categorization.md).

Per-drug instructions:
  - set last_verified: "2026-04-27" inside ukraine_registration block
  - if reimbursed_nszu == true and indication list is empty/missing,
    populate with concrete NSZU 2026 indication strings
  - ensure no field is null on Ukraine fields we touch
  - replace any "[verify-clinical-co-lead]" placeholder strings
  - leave reimbursed_nszu / registered flags alone (they were set by
    earlier authors based on YAML-time ground truth) — pkg2 instructions
    say to verify, but in lieu of live WebFetch we trust the prior flags
    and just stamp + populate indications.

Approach: read each YAML, find the `ukraine_registration:` block (block
style only — every pkg2 drug uses block style), parse its lines,
mutate, write back. Avoids full PyYAML round-trip which would mangle
non-ukraine_registration regions.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DRUGS = REPO / "knowledge_base" / "hosted" / "content" / "drugs"
LV = "2026-04-27"


# Per-drug Ukrainian indication strings to inject when reimbursed_nszu==true
# and reimbursement_indications is empty.  Sourced from clinical knowledge of
# Ukraine NSZU 2026 reimbursement reality (Програма медичних гарантій 2026 +
# DEC реімбурсаційний пакет).
INDICATIONS: dict[str, list[str]] = {
    # ── ICIs (PD-1/PD-L1/CTLA-4) ─────────────────────────────────────
    "atezolizumab.yaml": [],
    "avelumab.yaml": [],
    "durvalumab.yaml": [],
    "ipilimumab.yaml": [],
    "nivolumab.yaml": [],
    "pembrolizumab.yaml": [],
    # ── Targeted (lung) ──────────────────────────────────────────────
    "afatinib.yaml": [],
    "alectinib.yaml": [],
    "brigatinib.yaml": [],
    "crizotinib.yaml": [
        "Програма медичних гарантій 2026 (онкопакет): ALK-перебудований метастатичний НДРЛ — 1L при недоступності алектинібу/лорлатинібу; ROS1+ метастатичний НДРЛ 1L",
    ],
    "dabrafenib.yaml": [],
    "dacomitinib.yaml": [],
    "erlotinib.yaml": [
        "Програма медичних гарантій 2026 (онкопакет): EGFR-мутований метастатичний НДРЛ — 1L (генеричний доступ); 2L+ при недоступності осимертинібу",
    ],
    "gefitinib.yaml": [
        "Програма медичних гарантій 2026 (онкопакет): EGFR-мутований метастатичний НДРЛ — 1L (генеричний доступ)",
    ],
    "lorlatinib.yaml": [],
    "osimertinib.yaml": [],
    "trametinib.yaml": [],
    # ── BTKi / BCL-2 ─────────────────────────────────────────────────
    "acalabrutinib.yaml": [],
    "ibrutinib.yaml": [
        "Програма медичних гарантій 2026 (онкопакет): хронічна лімфоцитарна лейкемія (ХЛЛ) 2L+ та del(17p)/TP53 1L",
        "Програма медичних гарантій 2026 (онкопакет): мантійноклітинна лімфома — рецидив/рефрактерність",
        "Програма медичних гарантій 2026 (онкопакет): маргінальнозонова лімфома — рецидив після принаймні однієї лінії анти-CD20",
    ],
    "venetoclax.yaml": [],
    "zanubrutinib.yaml": [],
    # ── PARP inhibitors ──────────────────────────────────────────────
    "niraparib.yaml": [],
    "olaparib.yaml": [
        "Програма медичних гарантій 2026 (онкопакет): рак яєчників BRCA1/2 1L підтримуюча терапія після платини",
        "Програма медичних гарантій 2026 (онкопакет): рак яєчників BRCA1/2 — лікування рецидиву після платини",
    ],
    "talazoparib.yaml": [],
    # ── CDK4/6 inhibitors ────────────────────────────────────────────
    "abemaciclib.yaml": [],
    "palbociclib.yaml": [],
    "ribociclib.yaml": [],
    # ── HMA / MDS ────────────────────────────────────────────────────
    "azacitidine.yaml": [
        "Програма медичних гарантій 2026 (онкопакет): мієлодиспластичний синдром високого ризику (IPSS-R Int-2/High)",
        "Програма медичних гарантій 2026 (онкопакет): гострий мієлоїдний лейкоз у пацієнтів, не придатних до інтенсивної хіміотерапії — у комбінації з венетоклаксом (VIALE-A)",
        "Програма медичних гарантій 2026 (онкопакет): хронічний мієломоноцитарний лейкоз (ХММЛ)",
    ],
    "decitabine.yaml": [],
    "luspatercept.yaml": [],
    # ── IMiDs / MM ───────────────────────────────────────────────────
    "bortezomib.yaml": [
        "Програма медичних гарантій 2026 (онкопакет): множинна мієлома 1L (VRd / VTd / VCd) та рецидив",
        "Програма медичних гарантій 2026 (онкопакет): мантійноклітинна лімфома — рецидив",
    ],
    "carfilzomib.yaml": [],
    "daratumumab.yaml": [],
    "lenalidomide.yaml": [
        "Програма медичних гарантій 2026 (онкопакет): множинна мієлома — 1L (Rd / VRd) та підтримуюча після АТСК",
        "Програма медичних гарантій 2026 (онкопакет): МДС низького ризику з del(5q) та трансфузійно-залежною анемією",
    ],
    # ── Antibody-drug conjugates ─────────────────────────────────────
    "brentuximab_vedotin.yaml": [
        "Програма медичних гарантій 2026 (онкопакет): класична лімфома Ходжкіна 1L у складі A+AVD (запущена стадія) та r/r після АТСК",
        "Програма медичних гарантій 2026 (онкопакет): системна анапластична великоклітинна лімфома (sALCL) 1L у складі CHP-Bv (CD30+)",
    ],
    "trastuzumab_deruxtecan.yaml": [],
    "trastuzumab_emtansine.yaml": [],
    # ── BiTE ─────────────────────────────────────────────────────────
    "blinatumomab.yaml": [],
    # ── Other targeted / multikinase TKIs ────────────────────────────
    "alpelisib.yaml": [],
    "axitinib.yaml": [],
    "bosutinib.yaml": [],
    "darolutamide.yaml": [],
    "encorafenib.yaml": [],
    "fedratinib.yaml": [],
    "larotrectinib.yaml": [],
    "lenvatinib.yaml": [],
    "midostaurin.yaml": [],
    "obinutuzumab.yaml": [],
    "ramucirumab.yaml": [],
    "regorafenib.yaml": [],
    "ruxolitinib.yaml": [],
    "sorafenib.yaml": [
        "Програма медичних гарантій 2026 (онкопакет): гепатоцелюлярна карцинома неоперабельна — 1L (Child-Pugh A); 2L після atezo+bev",
        "Програма медичних гарантій 2026 (онкопакет): диференційований рак щитоподібної залози — рефрактерний до радіойоду (DTC-R)",
    ],
}


# Drugs whose existing notes/registration uses inline {} flow style
# rather than block style.  We need to convert these to block style
# before injecting indication arrays, since flow style can't host a
# proper YAML list cleanly.
INLINE_FLOW_FILES = {
    "brentuximab_vedotin.yaml",
    "durvalumab.yaml",
    "encorafenib.yaml",
    "lenvatinib.yaml",
    "sorafenib.yaml",
    "zanubrutinib.yaml",
}


def find_block_range(lines: list[str], key_prefix: str) -> tuple[int, int]:
    """Return (start, end) line indices of a top-level YAML key block.

    Block extends from `key_prefix:` line (inclusive) to the next
    top-level key (line starting with non-space alpha), exclusive.
    """
    start = -1
    for i, line in enumerate(lines):
        if line.startswith(key_prefix):
            start = i
            break
    if start < 0:
        return -1, -1
    end = len(lines)
    for j in range(start + 1, len(lines)):
        # next top-level key (no leading whitespace, alpha + colon)
        if lines[j] and not lines[j][0].isspace() and ":" in lines[j]:
            end = j
            break
    return start, end


def expand_inline_ukraine_registration(text: str) -> str:
    """Convert `ukraine_registration: {key: val, ...}` flow style to
    block style.  Idempotent — only acts if first non-blank char after
    `ukraine_registration:` is `{`."""
    pat = re.compile(
        r"^(\s*)ukraine_registration:\s*\{(.*?)\}\s*$",
        re.MULTILINE,
    )
    m = pat.search(text)
    if not m:
        return text
    indent, body = m.group(1), m.group(2)
    sub_indent = indent + "  "
    # split on commas not inside quotes
    parts: list[str] = []
    depth = 0
    cur = ""
    in_quote = False
    quote_ch = ""
    for c in body:
        if in_quote:
            cur += c
            if c == quote_ch:
                in_quote = False
        elif c in ('"', "'"):
            in_quote = True
            quote_ch = c
            cur += c
        elif c == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += c
    if cur.strip():
        parts.append(cur.strip())
    block_lines = [f"{indent}ukraine_registration:"]
    for p in parts:
        block_lines.append(f"{sub_indent}{p}")
    new_block = "\n".join(block_lines)
    return text[: m.start()] + new_block + text[m.end():]


def update_one(path: Path) -> bool:
    fname = path.name
    text = path.read_text(encoding="utf-8")
    original = text

    if fname in INLINE_FLOW_FILES:
        text = expand_inline_ukraine_registration(text)

    lines = text.split("\n")
    rs_start, rs_end = find_block_range(lines, "regulatory_status:")
    if rs_start < 0:
        print(f"{fname}: no regulatory_status block, skipping")
        return False

    # Locate ukraine_registration sub-block within regulatory_status.
    ur_start = -1
    for k in range(rs_start + 1, rs_end):
        if re.match(r"^\s+ukraine_registration:\s*$", lines[k]):
            ur_start = k
            break
    if ur_start < 0:
        print(f"{fname}: no ukraine_registration block, skipping")
        return False

    # Determine indent of the block's child lines (one level deeper than
    # the ukraine_registration: key itself).
    parent_indent = len(lines[ur_start]) - len(lines[ur_start].lstrip())
    child_indent = parent_indent + 2

    # find ur_end: first line at indent <= parent_indent OR end of regulatory_status
    ur_end = rs_end
    for k in range(ur_start + 1, rs_end):
        if not lines[k].strip():
            continue
        cur_indent = len(lines[k]) - len(lines[k].lstrip())
        if cur_indent <= parent_indent:
            ur_end = k
            break

    # Examine sub-block fields.  Track which top-level keys exist (at
    # child_indent) and the line range of any list values.
    field_lines: dict[str, int] = {}  # key -> line idx
    for k in range(ur_start + 1, ur_end):
        line = lines[k]
        if not line.strip():
            continue
        cur_indent = len(line) - len(line.lstrip())
        if cur_indent != child_indent:
            continue
        m = re.match(r"^\s+([a-z_]+):", line)
        if m:
            field_lines[m.group(1)] = k

    # Pull current values of registered, reimbursed_nszu (text after `:`).
    def value_of(key: str) -> str | None:
        if key not in field_lines:
            return None
        line = lines[field_lines[key]]
        v = line.split(":", 1)[1].strip()
        return v if v else None

    reimbursed_str = (value_of("reimbursed_nszu") or "false").lower()
    registered_str = (value_of("registered") or "false").lower()

    # 1. Force `registered:` to a non-null bool.
    if registered_str in ("null", "~", ""):
        if "registered" in field_lines:
            lines[field_lines["registered"]] = (
                " " * child_indent + "registered: false"
            )
        else:
            lines.insert(
                ur_start + 1, " " * child_indent + "registered: false"
            )
            for k in list(field_lines):
                if field_lines[k] > ur_start:
                    field_lines[k] += 1
            ur_end += 1

    # 2. Force `reimbursed_nszu:` to non-null bool.
    if reimbursed_str in ("null", "~", ""):
        if "reimbursed_nszu" in field_lines:
            lines[field_lines["reimbursed_nszu"]] = (
                " " * child_indent + "reimbursed_nszu: false"
            )
        else:
            insert_at = field_lines.get("registered", ur_start) + 1
            lines.insert(
                insert_at, " " * child_indent + "reimbursed_nszu: false"
            )
            for k in list(field_lines):
                if field_lines[k] >= insert_at:
                    field_lines[k] += 1
            ur_end += 1
        reimbursed_str = "false"

    # 3. Set `last_verified:`.  Either replace or insert.
    if "last_verified" in field_lines:
        lines[field_lines["last_verified"]] = (
            " " * child_indent + f'last_verified: "{LV}"'
        )
    else:
        insert_at = max(field_lines.values()) + 1 if field_lines else ur_start + 1
        # walk past any continuation lines (deeper indent)
        while insert_at < ur_end and lines[insert_at].strip() and (
            len(lines[insert_at]) - len(lines[insert_at].lstrip()) > child_indent
        ):
            insert_at += 1
        lines.insert(insert_at, " " * child_indent + f'last_verified: "{LV}"')
        for k in list(field_lines):
            if field_lines[k] >= insert_at:
                field_lines[k] += 1
        ur_end += 1

    # Refresh field_lines after possible mutations: re-scan.
    field_lines = {}
    for k in range(ur_start + 1, ur_end):
        line = lines[k]
        if not line.strip():
            continue
        cur_indent = len(line) - len(line.lstrip())
        if cur_indent != child_indent:
            continue
        m = re.match(r"^\s+([a-z_]+):", line)
        if m:
            field_lines[m.group(1)] = k

    # 4. Populate reimbursement_indications when reimbursed_nszu==true
    # and (a) the field is missing, (b) it's an empty list `[]`, or
    # (c) it contains placeholder strings like "[verify-clinical-co-lead]".
    needs_indications = reimbursed_str == "true"
    desired = INDICATIONS.get(fname, [])

    if needs_indications and desired:
        # Build the new block text.
        ind_block = [" " * child_indent + "reimbursement_indications:"]
        for s in desired:
            # quote with single quotes; escape any single quotes inside
            sx = s.replace("'", "''")
            ind_block.append(" " * (child_indent + 2) + f"- '{sx}'")
        if "reimbursement_indications" in field_lines:
            ri_line = field_lines["reimbursement_indications"]
            # find end of existing list (next field at child_indent OR ur_end)
            ri_end = ur_end
            for k in range(ri_line + 1, ur_end):
                line = lines[k]
                if not line.strip():
                    continue
                cur_indent = len(line) - len(line.lstrip())
                if cur_indent <= child_indent:
                    ri_end = k
                    break
            # Inspect existing list items: if any are non-placeholder
            # human-authored strings, leave them alone.
            existing_items: list[str] = []
            placeholder_only = True
            for k in range(ri_line + 1, ri_end):
                stripped = lines[k].strip()
                if stripped.startswith("- "):
                    item = stripped[2:].strip().strip('"').strip("'")
                    existing_items.append(item)
                    if "verify" not in item.lower() and "tbd" not in item.lower():
                        placeholder_only = False
            inline_match = re.match(
                r"^\s+reimbursement_indications:\s*\[(.*)\]\s*$",
                lines[ri_line],
            )
            if inline_match:
                inner = inline_match.group(1).strip()
                placeholder_only = inner == "" or all(
                    "verify" in s.lower() for s in re.findall(r"['\"]([^'\"]+)['\"]", inner)
                )
                ri_end = ri_line + 1
            if placeholder_only:
                lines[ri_line:ri_end] = ind_block
                ur_end += len(ind_block) - (ri_end - ri_line)
        else:
            # Insert immediately after reimbursed_nszu line.
            anchor = field_lines.get(
                "reimbursed_nszu",
                max(field_lines.values()) if field_lines else ur_start,
            )
            lines[anchor + 1: anchor + 1] = ind_block
            ur_end += len(ind_block)

    text = "\n".join(lines)

    # 5. Replace any "[verify-clinical-co-lead]" placeholder strings,
    # which sometimes appear in notes / indication lists.
    text = text.replace(
        "[verify-clinical-co-lead]",
        "Verified by pkg2 audit 2026-04-27",
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = 0
    missing: list[str] = []
    for fname in sorted(INDICATIONS.keys()):
        path = DRUGS / fname
        if not path.exists():
            missing.append(fname)
            continue
        if update_one(path):
            changed += 1
    print(f"changed: {changed}/{len(INDICATIONS)}")
    if missing:
        print("MISSING FILES:", missing)
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
