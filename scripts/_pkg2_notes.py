#!/usr/bin/env python3
"""Add NSZU verification citation to ukraine_registration.notes for pkg2 drugs.

Idempotent — only acts if "Verified 2026-04-27" not already in notes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DRUGS = REPO / "knowledge_base" / "hosted" / "content" / "drugs"

PKG2 = [
    "abemaciclib", "acalabrutinib", "afatinib", "alectinib", "alpelisib",
    "atezolizumab", "avelumab", "axitinib", "azacitidine", "blinatumomab",
    "bortezomib", "bosutinib", "brentuximab_vedotin", "brigatinib",
    "carfilzomib", "crizotinib", "dabrafenib", "dacomitinib", "daratumumab",
    "darolutamide", "decitabine", "durvalumab", "encorafenib", "erlotinib",
    "fedratinib", "gefitinib", "ibrutinib", "ipilimumab", "larotrectinib",
    "lenalidomide", "lenvatinib", "lorlatinib", "luspatercept", "midostaurin",
    "niraparib", "nivolumab", "obinutuzumab", "olaparib", "osimertinib",
    "palbociclib", "pembrolizumab", "ramucirumab", "regorafenib", "ribociclib",
    "ruxolitinib", "sorafenib", "talazoparib", "trametinib",
    "trastuzumab_deruxtecan", "trastuzumab_emtansine", "venetoclax",
    "zanubrutinib",
]

CITATION = (
    "NSZU verification 2026-04-27: drlz.com.ua (Держреєстр ЛЗ) + "
    "nszu.gov.ua/likuvannya-zlovkisnykh-novoutvoren (Програма медичних "
    "гарантій 2026, онкопакет) + dec.gov.ua/cmt (DEC реімбурсаційний пакет). "
    "Indication-restricted reimbursement; specific lines/біомаркери listed "
    "in reimbursement_indications."
)


def already_cited(text: str) -> bool:
    return "NSZU verification 2026-04-27" in text or "Verified 2026-04-27" in text


def update_notes(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if already_cited(text):
        return False

    lines = text.split("\n")
    # find ukraine_registration block
    ur_idx = -1
    for i, line in enumerate(lines):
        if re.match(r"^\s+ukraine_registration:\s*$", line):
            ur_idx = i
            break
    if ur_idx < 0:
        return False
    parent_indent = len(lines[ur_idx]) - len(lines[ur_idx].lstrip())
    child_indent = parent_indent + 2

    # find ur_end
    ur_end = len(lines)
    for k in range(ur_idx + 1, len(lines)):
        if not lines[k].strip():
            continue
        ci = len(lines[k]) - len(lines[k].lstrip())
        if ci <= parent_indent:
            ur_end = k
            break

    # Find existing notes line within block.
    notes_idx = -1
    for k in range(ur_idx + 1, ur_end):
        if re.match(rf"^ {{{child_indent}}}notes:", lines[k]):
            notes_idx = k
            break

    if notes_idx >= 0:
        # Append citation to existing notes string. Handle three flavors:
        #   notes: "single line"
        #   notes: >  (block scalar)
        #   notes: |  (block scalar)
        line = lines[notes_idx]
        if re.match(rf'^ {{{child_indent}}}notes:\s*"[^"]*"\s*$', line):
            new = line.rstrip().rstrip('"') + " " + CITATION + '"'
            lines[notes_idx] = new
        elif re.match(rf"^ {{{child_indent}}}notes:\s*'[^']*'\s*$", line):
            new = line.rstrip().rstrip("'") + " " + CITATION + "'"
            lines[notes_idx] = new
        elif re.match(rf"^ {{{child_indent}}}notes:\s*[>|][+-]?\s*$", line):
            # find end of block scalar (next line at <= child_indent or end)
            end = ur_end
            for k in range(notes_idx + 1, ur_end):
                if not lines[k].strip():
                    continue
                ci = len(lines[k]) - len(lines[k].lstrip())
                if ci <= child_indent:
                    end = k
                    break
            # Insert citation as last block-scalar content line.
            content_indent = child_indent + 2
            lines.insert(end, " " * content_indent + CITATION)
        else:
            # plain unquoted scalar
            lines[notes_idx] = (
                line.rstrip()
                + " "
                + CITATION
            )
    else:
        # Insert a new notes line at end of ur block.
        notes_line = " " * child_indent + f'notes: "{CITATION}"'
        # find last non-blank within block
        last = ur_idx
        for k in range(ur_idx + 1, ur_end):
            if lines[k].strip():
                last = k
        lines.insert(last + 1, notes_line)

    new_text = "\n".join(lines)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = 0
    for n in PKG2:
        p = DRUGS / f"{n}.yaml"
        if not p.exists():
            print(f"missing: {n}")
            continue
        if update_notes(p):
            changed += 1
    print(f"notes-citation appended: {changed}/{len(PKG2)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
