"""Fix duplicated `reimbursement_indications` block left by
_pkg1_indications.py when applied to YAMLs that already had an empty
`reimbursement_indications: []` immediately followed by `last_verified:`.

Pattern in broken files:

    reimbursement_indications:
      - "..."
      - "..."
    last_verified: "2026-04-27"
                                  <-- blank line
      - "..."                     <-- stale duplicate items (no header)
      - "..."
    last_verified: "2026-04-27"   <-- second last_verified

We delete the lines from the blank-line-after-first-`last_verified` UP TO
AND INCLUDING the second `last_verified` line. Net: keep only the first
correct block.

Run: py -3.12 scripts/_pkg1_fix_dup.py
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DRUGS_DIR = REPO / "knowledge_base" / "hosted" / "content" / "drugs"

BROKEN = [
    "acyclovir", "allopurinol", "capecitabine", "cytarabine", "dasatinib",
    "daunorubicin", "dexamethasone", "doxorubicin", "enzalutamide",
    "epoetin_alfa", "filgrastim", "fludarabine", "hydroxyurea", "idarubicin",
    "leucovorin", "mercaptopurine", "nilotinib", "ondansetron", "pemetrexed",
    "prednisone", "tamoxifen", "trimethoprim_sulfamethoxazole",
    "vincristine", "zoledronate",
]


def fix(text: str) -> tuple[str, bool]:
    lines = text.split("\n")
    # find pattern: line ` ... last_verified: "..."` then blank then `   - "..."` (yaml seq item without parent key)
    # Strategy: find every `last_verified:` line; if the next non-blank line
    # is a sequence item ("- ...") that is NOT preceded by a `key:` header,
    # delete from blank line up to AND including the SECOND `last_verified:`.
    out = []
    i = 0
    changed = False
    n = len(lines)
    while i < n:
        line = lines[i]
        out.append(line)
        m = re.match(r"^(\s*)last_verified\s*:", line)
        if m:
            # peek ahead: skip blanks
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1
            if j < n and re.match(r"^\s*-\s+", lines[j]):
                # this is a stale sequence — find the second `last_verified:`
                k = j
                while k < n and not re.match(r"^\s*last_verified\s*:", lines[k]):
                    k += 1
                # k is the second last_verified (or n)
                # delete lines i+1 .. k (inclusive) — but keep blank lines AFTER k
                # i.e., skip from i+1 to k inclusive
                if k < n:
                    i = k + 1
                    changed = True
                    continue
        i += 1
    return "\n".join(out), changed


def main() -> None:
    fixed = 0
    for stem in BROKEN:
        p = DRUGS_DIR / f"{stem}.yaml"
        text = p.read_text(encoding="utf-8")
        new_text, changed = fix(text)
        if changed:
            p.write_text(new_text, encoding="utf-8", newline="\n")
            fixed += 1
            print(f"[fix] {stem}.yaml")
        else:
            print(f"[unchanged] {stem}.yaml")
    print(f"\nFixed: {fixed}")


if __name__ == "__main__":
    main()
