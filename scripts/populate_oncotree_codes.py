"""One-shot script to populate Disease.oncotree_code on existing KB.

Phase 2 PR-B of OncoKB safe-rollout v3 §5. Adds an explicit OncoTree
code (MSK taxonomy) to each Disease YAML so OncoKB lookups can resolve
tumorType. Conservative mappings — when uncertain, use the parent-level
code (e.g. NSCLC instead of LUAD/LUSC); biomarker-driven subtyping
happens via Disease.molecular_subtypes downstream.

Mapping rationale stored alongside each entry. If a disease has no
clean OncoTree mapping, leave it absent (engine will fall back to
pan-tumor mode and render adds a warning badge).
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml


# Canonical mapping. Keys = file basename (without .yaml). Values = OncoTree code.
# Source: http://oncotree.mskcc.org/api/tumorTypes (verified terminology, 2024 release).
ONCOTREE_MAPPING: dict[str, str] = {
    # ── Lymphoid hematologic ──
    "multiple_myeloma": "MM",
    "dlbcl_nos": "DLBCLNOS",
    "follicular_lymphoma": "FL",
    "cll_sll": "CLLSLL",
    "mantle_cell_lymphoma": "MCL",
    "splenic_mzl": "SMZL",
    "nodal_mzl": "NMZL",
    "burkitt": "BL",
    "hairy_cell_leukemia": "HCL",
    "waldenstrom": "WM",
    "hgbl_double_hit": "HGBCL",
    "ptcl_nos": "PTCL",
    "alcl": "ALCL",
    "aitl": "AITL",
    "mycosis_fungoides_sezary": "MYCF",
    "hodgkin_classical": "CHL",
    "nlpbl": "NLPHL",
    "hcv_mzl": "MZL",
    "pmbcl": "PMBL",
    "pcnsl": "PCNSL",
    "b_all": "BLL",
    "t_all": "TLL",
    "ptld": "PTLD",
    "eatl": "EATL",
    "hstcl": "HSTCL",
    "nk_t_nasal": "NKCL",
    "atll": "ATLL",
    "t_pll": "TPLL",
    # ── Myeloid hematologic ──
    "aml": "AML",
    "apl": "APLPMLRARA",
    "cml": "CML",
    "mds_lr": "MDS",
    "mds_hr": "MDS",
    "pv": "PV",
    "et": "ET",
    "pmf": "PMF",
    "mastocytosis": "MASTSC",
    # ── Solid tumors ──
    "prostate_cancer": "PRAD",
    "breast_cancer": "BREAST",
    "nsclc": "NSCLC",
    "sclc": "SCLC",
    "crc": "COADREAD",
    "gastric": "STAD",
    "hcc": "HCC",
    "pdac": "PAAD",
    "esophageal": "ESCA",
    "ovarian": "OV",
    "melanoma": "MEL",
    "rcc": "RCC",
    "endometrial": "UCEC",
    "urothelial": "BLCA",
    "cervical": "CESC",
    "gbm": "GBM",
    "cholangiocarcinoma": "CHOL",
    "chondrosarcoma": "CHS",
    "gist": "GIST",
    "glioma_low_grade": "DIFG",
    "hnscc": "HNSC",
    "ifs": "IFS",
    "imt": "IMT",
    "mpnst": "MPNST",
    "mtc": "MTC",
    "salivary": "SACA",
    "thyroid_anaplastic": "ATC",
    "thyroid_papillary": "PTC",
}


def _ordered_insert_oncotree(text: str, code: str) -> str:
    """Insert `oncotree_code: <code>` after the `lineage:` line if present,
    else after `archetype:` line, else after `codes:` block (which we detect
    by the next line not being indented). Preserves YAML formatting so the
    diff is one line per file.

    Idempotent: if `oncotree_code:` already present anywhere, no-op.
    """
    if "oncotree_code:" in text:
        return text

    lines = text.splitlines(keepends=True)
    out: list[str] = []
    inserted = False

    # Strategy: insert right after the first occurrence of `lineage:` or
    # `archetype:` at indent level 0 (no leading whitespace).
    target_keys = ("lineage:", "archetype:")
    for i, line in enumerate(lines):
        out.append(line)
        if inserted:
            continue
        stripped = line.lstrip()
        # Only act on top-level keys (no indent)
        if line == stripped and any(stripped.startswith(k) for k in target_keys):
            out.append(f"oncotree_code: {code}\n")
            inserted = True

    if not inserted:
        # Fallback: append before the first blank line, or at end-of-file
        text_with_newline = text.rstrip() + f"\noncotree_code: {code}\n"
        return text_with_newline

    return "".join(out)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    diseases_dir = repo_root / "knowledge_base" / "hosted" / "content" / "diseases"

    if not diseases_dir.exists():
        print(f"ERROR: {diseases_dir} not found", file=sys.stderr)
        return 1

    updated = 0
    skipped_already = 0
    skipped_unmapped: list[str] = []

    for yaml_path in sorted(diseases_dir.glob("*.yaml")):
        stem = yaml_path.stem
        code = ONCOTREE_MAPPING.get(stem)
        if code is None:
            skipped_unmapped.append(stem)
            continue

        text = yaml_path.read_text(encoding="utf-8")
        if "oncotree_code:" in text:
            skipped_already += 1
            continue

        # Sanity-check the YAML loads + has Disease shape
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as e:
            print(f"  SKIP {stem}: YAML parse error — {e}", file=sys.stderr)
            continue
        if not isinstance(data, dict) or "id" not in data:
            print(f"  SKIP {stem}: not a Disease entity", file=sys.stderr)
            continue

        new_text = _ordered_insert_oncotree(text, code)
        if new_text == text:
            print(f"  SKIP {stem}: insertion no-op", file=sys.stderr)
            continue

        yaml_path.write_text(new_text, encoding="utf-8")
        updated += 1
        print(f"  + {stem:30s} -> oncotree_code: {code}")

    print(f"\nUpdated {updated} Disease YAMLs.")
    print(f"Skipped (already had oncotree_code): {skipped_already}")
    if skipped_unmapped:
        print(f"\nUnmapped (no entry in ONCOTREE_MAPPING): {len(skipped_unmapped)}")
        for s in skipped_unmapped:
            print(f"  - {s}")
        print(
            "\nIf any of these need OncoKB lookups, add to ONCOTREE_MAPPING "
            "(see http://oncotree.mskcc.org)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
