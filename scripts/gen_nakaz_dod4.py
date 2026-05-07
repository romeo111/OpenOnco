#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate draft МОЗ Ukraine order — Додаток 4 to наказ 473/2026
Output: docs/moz/draft_nakaz_moz_dod4_2026-06-01.md

Design decisions (resolving spec ambiguities):
- Table has 4 columns: Загальноклінічні | ІГХ та морфологія | Молекулярна генетика | Ключові молекулярні маркери
- Серологія tests folded into Загальноклінічні (semantic fit)
- Візуалізація and Інше tests omitted from table columns (not in table spec)
- Biomarker value_constraint truncated to 60 chars
- Sources: consolidated section below table (no 8th column)
- ICD-10 sort: parse first token, sort C-series before D-series, secondary key = disease id
- TEST-LDH deduplicated in category prefix list
- TEST-* not found in YAML: remove TEST- prefix, replace - with space, title-case
- All 65 disease files are real diseases; no meta-entity skipping needed
"""

import yaml
import os
import re
import sys

KB_BASE = "C:/Users/805/cancer-autoresearch/knowledge_base/hosted/content"
OUT_FILE = "C:/Users/805/cancer-autoresearch/docs/moz/draft_nakaz_moz_dod4_2026-06-01.md"

# ── Category membership sets (prefix-based, exact IDs take priority) ──────────
CLINICAL_TEST_IDS = {
    "TEST-CBC", "TEST-CMP", "TEST-LFT", "TEST-LDH", "TEST-URIC-ACID",
    "TEST-COAG-PANEL", "TEST-RENAL-FUNCTION-EGFR", "TEST-B2-MICROGLOBULIN",
    "TEST-PSA", "TEST-D-DIMER", "TEST-PERIPHERAL-SMEAR", "TEST-PREGNANCY",
    "TEST-CHILD-PUGH", "TEST-MELD", "TEST-FERRITIN", "TEST-B12-FOLATE",
    "TEST-AFP-SERUM", "TEST-CEA", "TEST-CA125", "TEST-BCR-ABL-JAK2",
}
SEROLOGY_TEST_PREFIXES = (
    "TEST-HBV", "TEST-HCV", "TEST-HIV", "TEST-CMV", "TEST-HTLV",
    "TEST-EBV", "TEST-H-PYLORI",
)
IHC_TEST_PREFIXES = (
    "TEST-IHC-", "TEST-FLOW-CYTOMETRY", "TEST-BM-ASPIRATE", "TEST-BM-TREPHINE",
    "TEST-BIOPSY-", "TEST-CYTOLOGY-",
)
IHC_TEST_IDS = {
    "TEST-FLOW-CYTOMETRY", "TEST-BM-ASPIRATE", "TEST-BM-TREPHINE",
    "TEST-CD20-IHC", "TEST-BRONCHOSCOPY-WITH-EBUS",
}
MOLECULAR_TEST_PREFIXES = (
    "TEST-NGS-", "TEST-FISH-", "TEST-PCR-", "TEST-KARYOTYPE",
    "TEST-MSI-", "TEST-TMB", "TEST-BRAF-V600E",
)
MOLECULAR_TEST_IDS = {
    "TEST-KARYOTYPE", "TEST-TMB", "TEST-BRAF-V600E", "TEST-BCR-ABL-JAK2",
    "TEST-FISH-PANEL",
}
IMAGING_TEST_PREFIXES = (
    "TEST-CT-", "TEST-PET-CT", "TEST-MRI-", "TEST-CECT-",
    "TEST-BRAIN-MRI-", "TEST-BREAST-MRI", "TEST-BREAST-US",
)
IMAGING_TEST_IDS = {
    "TEST-PET-CT", "TEST-BONE-SCAN", "TEST-ECHO", "TEST-ECG",
    "TEST-BREAST-MRI", "TEST-BREAST-US", "TEST-CECT-CAP",
}


def classify_test(test_id: str) -> str:
    """Return one of: clinical, serology, ihc, molecular, imaging, other."""
    tid = test_id.upper()
    if tid in CLINICAL_TEST_IDS:
        return "clinical"
    if any(tid.startswith(p.upper()) for p in SEROLOGY_TEST_PREFIXES):
        return "serology"  # folded into clinical in table
    if tid in IHC_TEST_IDS or any(tid.startswith(p.upper()) for p in IHC_TEST_PREFIXES):
        return "ihc"
    if tid in MOLECULAR_TEST_IDS or any(tid.startswith(p.upper()) for p in MOLECULAR_TEST_PREFIXES):
        return "molecular"
    if tid in IMAGING_TEST_IDS or any(tid.startswith(p.upper()) for p in IMAGING_TEST_PREFIXES):
        return "imaging"
    return "other"


def load_yaml_safe(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"  [WARN] could not load {path}: {e}", file=sys.stderr)
        return {}


def nice_test_name(test_id: str, test_map: dict) -> str:
    """Return Ukrainian/preferred name, or formatted ID if unknown."""
    if test_id in test_map:
        t = test_map[test_id]
        names = t.get("names", {})
        return names.get("ukrainian") or names.get("preferred") or test_id
    # Format ID nicely: TEST-FOO-BAR → Foo Bar
    label = test_id
    if label.upper().startswith("TEST-"):
        label = label[5:]
    label = label.replace("-", " ").title()
    return label


def parse_icd10_sort_key(icd10_raw) -> tuple:
    """Return (letter_group, numeric_part, original) for sorting.
    C before D, then by numeric value. Multi-code: take first.
    """
    if not icd10_raw:
        return ("Z", 9999, "")
    raw = str(icd10_raw)
    # Take first code token
    first = re.split(r"[,\s]+", raw.strip())[0]
    m = re.match(r"([A-Z])(\d+(?:\.\d+)?)", first)
    if not m:
        return ("Z", 9999, raw)
    letter = m.group(1)
    try:
        num = float(m.group(2))
    except ValueError:
        num = 9999.0
    # C before D before others
    order = {"C": 0, "D": 1}.get(letter, 2)
    return (order, num, raw)


def truncate(s: str, max_len: int = 60) -> str:
    if not s:
        return ""
    s = str(s)
    if len(s) <= max_len:
        return s
    return s[:max_len - 3].rstrip() + "..."


# ── Load all tests ─────────────────────────────────────────────────────────────
def load_tests(tests_dir: str) -> dict:
    tests = {}
    for fname in os.listdir(tests_dir):
        if not fname.endswith(".yaml"):
            continue
        d = load_yaml_safe(os.path.join(tests_dir, fname))
        tid = d.get("id")
        if tid:
            tests[tid] = d
    return tests


# ── Load all biomarkers ────────────────────────────────────────────────────────
def load_biomarkers(bm_dir: str) -> dict:
    biomarkers = {}
    for fname in os.listdir(bm_dir):
        if not fname.endswith(".yaml"):
            continue
        d = load_yaml_safe(os.path.join(bm_dir, fname))
        bid = d.get("id")
        if bid:
            biomarkers[bid] = d
    return biomarkers


# ── Load all diseases ──────────────────────────────────────────────────────────
def load_diseases(dis_dir: str) -> list:
    diseases = []
    for fname in os.listdir(dis_dir):
        if not fname.endswith(".yaml"):
            continue
        d = load_yaml_safe(os.path.join(dis_dir, fname))
        did = d.get("id")
        if not did:
            continue
        diseases.append(d)
    return diseases


# ── Load all indications, indexed by disease_id ───────────────────────────────
def load_indications_by_disease(ind_dir: str) -> dict:
    by_disease = {}
    for fname in os.listdir(ind_dir):
        if not fname.endswith(".yaml"):
            continue
        d = load_yaml_safe(os.path.join(ind_dir, fname))
        applicable = d.get("applicable_to", {})
        disease_id = applicable.get("disease_id")
        if not disease_id:
            continue
        if disease_id not in by_disease:
            by_disease[disease_id] = []
        by_disease[disease_id].append(d)
    return by_disease


def is_nccn_or_esmo(source_id: str) -> bool:
    sid = source_id.upper()
    return "NCCN" in sid or "ESMO" in sid or "CAP" in sid


def main():
    print("Loading KB data...", file=sys.stderr)
    tests_dir = os.path.join(KB_BASE, "tests")
    bm_dir = os.path.join(KB_BASE, "biomarkers")
    dis_dir = os.path.join(KB_BASE, "diseases")
    ind_dir = os.path.join(KB_BASE, "indications")

    test_map = load_tests(tests_dir)
    bm_map = load_biomarkers(bm_dir)
    diseases = load_diseases(dis_dir)
    ind_by_dis = load_indications_by_disease(ind_dir)

    print(f"  Loaded: {len(diseases)} diseases, {len(test_map)} tests, "
          f"{len(bm_map)} biomarkers, "
          f"{sum(len(v) for v in ind_by_dis.values())} indications",
          file=sys.stderr)

    # Sort diseases by ICD-10
    diseases.sort(key=lambda d: (
        parse_icd10_sort_key(d.get("codes", {}).get("icd_10")),
        d.get("id", "")
    ))

    # Stats trackers
    all_tests_referenced = set()
    all_biomarkers_referenced = set()
    all_sources_referenced = set()

    # Build table rows
    rows = []
    for idx, dis in enumerate(diseases, start=1):
        did = dis.get("id", "")
        codes = dis.get("codes", {})
        icd10 = codes.get("icd_10", "")
        icd_o3 = codes.get("icd_o_3_morphology", "")
        names = dis.get("names", {})
        name_ua = names.get("ukrainian") or names.get("preferred") or did

        # Gather indications
        indications = ind_by_dis.get(did, [])

        # Aggregate required_tests (union, dedup)
        req_tests_all = set()
        bm_req_all = {}  # biomarker_id -> value_constraint (last wins)
        sources_all = set()

        for ind in indications:
            for t in (ind.get("required_tests") or []):
                req_tests_all.add(t)
            bmr_list = ind.get("applicable_to", {}).get("biomarker_requirements_required") or []
            for bmr in bmr_list:
                bid = bmr.get("biomarker_id")
                if bid:
                    bm_req_all[bid] = bmr.get("value_constraint", "")
            for src in (ind.get("sources") or []):
                sid = src.get("source_id") if isinstance(src, dict) else str(src)
                if sid and is_nccn_or_esmo(sid):
                    sources_all.add(sid)

        all_tests_referenced.update(req_tests_all)
        all_biomarkers_referenced.update(bm_req_all.keys())
        all_sources_referenced.update(sources_all)

        # Classify tests
        clinical_tests = []  # includes serology
        ihc_tests = []
        molecular_tests = []
        # imaging + other: not shown in table

        for t in sorted(req_tests_all):
            cat = classify_test(t)
            name = nice_test_name(t, test_map)
            if cat in ("clinical", "serology"):
                clinical_tests.append(name)
            elif cat == "ihc":
                ihc_tests.append(name)
            elif cat == "molecular":
                molecular_tests.append(name)
            # imaging / other silently excluded from table columns

        # Format biomarkers column
        bm_parts = []
        for bid in sorted(bm_req_all.keys()):
            bm = bm_map.get(bid, {})
            bm_names = bm.get("names", {})
            bm_ua = bm_names.get("ukrainian") or bm_names.get("preferred") or bid
            vc = bm_req_all[bid]
            if vc:
                bm_parts.append(f"{bm_ua} ({truncate(vc, 60)})")
            else:
                bm_parts.append(bm_ua)

        placeholder = "— (підлягає визначенню)"

        def col(lst):
            if not lst:
                return ""
            return "; ".join(lst)

        def col_or_placeholder(lst, has_indications):
            if not has_indications:
                return placeholder
            if not lst:
                return ""
            return "; ".join(lst)

        has_ind = len(indications) > 0

        rows.append({
            "num": idx,
            "icd_o3": icd_o3 or "—",
            "icd10": str(icd10) if icd10 else "—",
            "name": name_ua,
            "clinical": col_or_placeholder(clinical_tests, has_ind) if not has_ind else col(clinical_tests),
            "ihc": col_or_placeholder(ihc_tests, has_ind) if not has_ind else col(ihc_tests),
            "molecular": col_or_placeholder(molecular_tests, has_ind) if not has_ind else col(molecular_tests),
            "biomarkers": col(bm_parts),
            "has_ind": has_ind,
        })

    # For diseases with no indications, override all test columns
    for row in rows:
        if not row["has_ind"]:
            row["clinical"] = "— (підлягає визначенню)"
            row["ihc"] = "— (підлягає визначенню)"
            row["molecular"] = "— (підлягає визначенню)"

    # ── Build document ─────────────────────────────────────────────────────────
    lines = []

    lines.append("# ПРОЄКТ\n")
    lines.append("## МІНІСТЕРСТВО ОХОРОНИ ЗДОРОВ'Я УКРАЇНИ\n")
    lines.append("## НАКАЗ")
    lines.append("**від 01 червня 2026 року № ___**\n")
    lines.append("### Про доповнення наказу Міністерства охорони здоров'я України від 07 квітня 2026 року № 473\n")
    lines.append(
        "Відповідно до статей 14, 34 Закону України «Про основи законодавства України про охорону здоров'я», "
        "підпункту 3 пункту 4 Положення про Міністерство охорони здоров'я України, затвердженого постановою "
        "Кабінету Міністрів України від 25 березня 2015 року № 267, з метою забезпечення стандартизованого "
        "підходу до молекулярно-генетичної та імуногістохімічної діагностики злоякісних новоутворень "
        "відповідно до сучасних міжнародних стандартів (NCCN, ESMO, CAP)\n"
    )
    lines.append("**НАКАЗУЮ:**\n")
    lines.append(
        "1. Доповнити наказ Міністерства охорони здоров'я України від 07 квітня 2026 року № 473 "
        "«Про затвердження довідників для кодування та формування онкологічного діагнозу» додатком 4 "
        "«Перелік рекомендованих молекулярно-генетичних та імуногістохімічних досліджень при встановленні "
        "онкологічного діагнозу», що додається.\n"
    )
    lines.append(
        "2. Керівникам закладів охорони здоров'я, що надають спеціалізовану онкологічну допомогу, "
        "забезпечити виконання вимог додатку 4 при формуванні онкологічного діагнозу.\n"
    )
    lines.append(
        "3. Контроль за виконанням цього наказу покласти на заступника Міністра охорони здоров'я України "
        "відповідно до розподілу обов'язків.\n"
    )
    lines.append(
        "Міністр охорони здоров'я України "
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [підпис]\n"
    )
    lines.append("---\n")
    lines.append("## ЗАТВЕРДЖЕНО")
    lines.append("Наказ Міністерства охорони здоров'я України")
    lines.append("від 01 червня 2026 року № ___\n")
    lines.append("## Додаток 4 до наказу МОЗ від 07.04.2026 № 473\n")
    lines.append("# ПЕРЕЛІК")
    lines.append("## рекомендованих молекулярно-генетичних та імуногістохімічних досліджень при встановленні онкологічного діагнозу\n")

    # Table header
    lines.append(
        "| № | ICD-O-3 | ICD-10 | Нозологія | "
        "Загальноклінічні та серологічні | "
        "ІГХ та морфологія | "
        "Молекулярна генетика | "
        "Ключові молекулярні маркери |"
    )
    lines.append(
        "|---|---------|--------|-----------|"
        "--------------------------------|"
        "-------------------|"
        "---------------------|"
        "---------------------------|"
    )

    for row in rows:
        num = row["num"]
        icd_o3 = row["icd_o3"].replace("|", "&#124;")
        icd10 = row["icd10"].replace("|", "&#124;")
        name = row["name"].replace("|", "&#124;")
        clinical = row["clinical"].replace("|", "&#124;")
        ihc = row["ihc"].replace("|", "&#124;")
        molecular = row["molecular"].replace("|", "&#124;")
        biomarkers = row["biomarkers"].replace("|", "&#124;")
        lines.append(
            f"| {num} | {icd_o3} | {icd10} | {name} | "
            f"{clinical} | {ihc} | {molecular} | {biomarkers} |"
        )

    lines.append("")
    lines.append("---\n")

    # Sources section
    if all_sources_referenced:
        lines.append("## Джерела")
        lines.append("")
        lines.append(
            "Перелік сформовано на підставі наступних міжнародних клінічних настанов, "
            "на які посилаються індикації бази знань OpenOnco:\n"
        )
        for src in sorted(all_sources_referenced):
            lines.append(f"- {src}")
        lines.append("")

    lines.append(
        "*Підготовлено: OpenOnco (openonco.info). Джерела: NCCN Clinical Practice Guidelines in Oncology, "
        "ESMO Clinical Practice Guidelines, CAP Cancer Protocols. Версія 1.0, травень 2026.*"
    )

    content = "\n".join(lines)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    # Stats
    file_size = os.path.getsize(OUT_FILE)
    print(f"\n=== Statistics ===", file=sys.stderr)
    print(f"Total diseases in table: {len(rows)}", file=sys.stderr)
    print(f"Total unique tests referenced: {len(all_tests_referenced)}", file=sys.stderr)
    print(f"Total unique biomarkers referenced: {len(all_biomarkers_referenced)}", file=sys.stderr)
    print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)", file=sys.stderr)

    # Print to stdout as well for capture
    print(f"\n=== Statistics ===")
    print(f"Total diseases in table: {len(rows)}")
    print(f"Total unique tests referenced: {len(all_tests_referenced)}")
    print(f"Total unique biomarkers referenced: {len(all_biomarkers_referenced)}")
    print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"Output: {OUT_FILE}")

    # Show which diseases had no indications
    no_ind = [r for r in rows if not r["has_ind"]]
    if no_ind:
        print(f"\nDiseases with NO indications ({len(no_ind)}):")
        for r in no_ind:
            print(f"  - {r['name']} ({r['icd10']})")
    else:
        print("\nAll diseases have at least one indication.")


if __name__ == "__main__":
    main()
