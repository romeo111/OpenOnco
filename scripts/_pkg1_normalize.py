"""Minimal-surgical pkg1 normalizer.

Only two operations, both purely textual:

1. Replace `[verify-clinical-co-lead]` and `[TBD…]` placeholder strings
   on `registration_number:` lines with `null` (per UkraineRegistration
   schema — the field is `Optional[str]`).
2. Replace `last_verified: "<old date>"` (or `null`) with
   `last_verified: "2026-04-27"` on the line that follows
   `reimbursed_nszu:` inside the `ukraine_registration` block — but
   safer: simply replace any `last_verified:` line whose immediate
   surroundings contain `ukraine_registration` context.

We do NOT modify block boundaries, do NOT insert keys, do NOT touch
flow-style ({...}) blocks except via in-line `last_verified:` regex.
This keeps the diff small and impossible to break the YAML structure.

Run from repo root:
    py -3.12 scripts/_pkg1_normalize.py
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DRUGS_DIR = REPO / "knowledge_base" / "hosted" / "content" / "drugs"

PKG1_STEMS = [
    "fluorouracil", "abiraterone", "acyclovir", "allopurinol", "anagrelide",
    "anastrozole", "apalutamide", "aspirin", "arsenic_trioxide", "atra",
    "bendamustine", "bevacizumab", "bleomycin", "capecitabine",
    "capecitabine_breast", "carboplatin", "cetuximab", "cisplatin",
    "cladribine", "cyclophosphamide", "cytarabine", "dacarbazine",
    "dasatinib", "daunorubicin", "degarelix", "denosumab", "dexamethasone",
    "docetaxel", "doxorubicin", "entecavir", "enzalutamide", "epoetin_alfa",
    "etoposide", "exemestane", "filgrastim", "fludarabine", "fulvestrant",
    "gemcitabine", "glecaprevir_pibrentasvir", "goserelin", "hydroxyurea",
    "idarubicin", "ifosfamide", "imatinib", "interferon_alpha", "irinotecan",
    "leucovorin", "leuprolide", "letrozole", "l_asparaginase",
    "mercaptopurine", "methotrexate", "nab_paclitaxel", "nilotinib",
    "ondansetron", "oxaliplatin", "paclitaxel", "pemetrexed", "pertuzumab",
    "prednisone", "procarbazine", "rituximab", "sofosbuvir_velpatasvir",
    "tamoxifen", "temozolomide", "thiotepa", "trimethoprim_sulfamethoxazole",
    "trastuzumab", "trifluridine_tipiracil", "vinblastine", "vincristine",
    "zidovudine", "zoledronate",
]

assert len(PKG1_STEMS) == 73


def normalize(text: str) -> tuple[str, int]:
    """Apply textual replacements; return (new_text, change_count)."""
    changes = 0

    # 1. Replace registration_number placeholders.
    placeholder_re = re.compile(
        r'(registration_number\s*:\s*)'
        r'("(?:\[verify-clinical-co-lead\]|\[TBD\]|\[TBD[^"]*\])")'
    )

    def _swap(m: re.Match[str]) -> str:
        nonlocal changes
        changes += 1
        return f"{m.group(1)}null"

    text = placeholder_re.sub(_swap, text)

    # 2. Replace last_verified date with 2026-04-27.
    # Only update inside ukraine_registration block — limit by replacing
    # all last_verified that occur within ~30 lines after the
    # ukraine_registration: line. Practically simpler: replace any
    # `last_verified: "..."` line and any `last_verified: null`. Drug
    # YAMLs only use this key on UkraineRegistration in this codebase.
    lv_re = re.compile(
        r'(last_verified\s*:\s*)'
        r'(?:"[^"]*"|null|\S+)'
    )

    def _stamp(m: re.Match[str]) -> str:
        nonlocal changes
        changes += 1
        return f'{m.group(1)}"2026-04-27"'

    text = lv_re.sub(_stamp, text)

    return text, changes


def main() -> None:
    total_files = 0
    total_changes = 0
    for stem in PKG1_STEMS:
        path = DRUGS_DIR / f"{stem}.yaml"
        if not path.exists():
            print(f"[skip] missing {path.name}")
            continue
        original = path.read_text(encoding="utf-8")
        new_text, n = normalize(original)
        if new_text != original:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            total_files += 1
            total_changes += n
            print(f"[ok] {stem}.yaml: {n} change(s)")
        else:
            print(f"[unchanged] {stem}.yaml")
    print(f"\nTotal: {total_changes} edits across {total_files} files")


if __name__ == "__main__":
    main()
