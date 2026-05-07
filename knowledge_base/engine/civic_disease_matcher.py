"""Disease-aware matching helpers for CIViC snapshot evidence.

CIViC evidence carries free-text disease names plus optional DOID. OpenOnco
BMAs carry ``DIS-*`` IDs and local disease YAML. This module supplies a
conservative text matcher so CIViC evidence can be filtered by disease before
being attached to disease-specific BMA cells.
"""

from __future__ import annotations

import re
from typing import Any


_MANUAL_DISEASE_ALIASES: dict[str, tuple[str, ...]] = {
    "DIS-CRC": ("colorectal cancer", "colorectal carcinoma", "colon cancer", "rectal cancer"),
    "DIS-NSCLC": ("non-small cell lung cancer", "lung non-small cell carcinoma", "nsclc"),
    "DIS-SCLC": ("small cell lung cancer", "sclc"),
    "DIS-PDAC": ("pancreatic ductal adenocarcinoma", "pancreatic cancer"),
    "DIS-GBM": ("glioblastoma", "glioblastoma multiforme"),
    "DIS-HCL": ("hairy cell leukemia",),
    "DIS-AML": ("acute myeloid leukemia",),
    "DIS-CML": ("chronic myeloid leukemia",),
    "DIS-B-ALL": ("b-cell acute lymphoblastic leukemia", "b acute lymphoblastic leukemia"),
    "DIS-MELANOMA": ("melanoma",),
    "DIS-GIST": ("gastrointestinal stromal tumor", "gist"),
    "DIS-GASTRIC": ("gastric cancer", "stomach cancer", "gastric adenocarcinoma"),
    "DIS-OVARIAN": ("ovarian cancer", "ovarian carcinoma"),
    "DIS-BREAST": ("breast cancer", "breast carcinoma"),
    "DIS-PROSTATE": ("prostate cancer", "prostate adenocarcinoma"),
    "DIS-MTC": ("medullary thyroid cancer", "medullary thyroid carcinoma"),
    "DIS-THYROID-ANAPLASTIC": ("anaplastic thyroid cancer", "anaplastic thyroid carcinoma"),
    "DIS-THYROID-PAPILLARY": ("papillary thyroid cancer", "papillary thyroid carcinoma"),
    "DIS-CHOLANGIOCARCINOMA": ("cholangiocarcinoma", "bile duct cancer"),
}


def civic_entry_matches_disease(
    entry: dict[str, Any],
    disease_data: dict[str, Any] | None,
) -> bool:
    """Return True when a CIViC evidence item appears disease-compatible.

    If disease metadata is unavailable, return True so callers can preserve
    existing fail-open behavior. When metadata is available and CIViC supplies
    no disease text, return False: a disease-specific BMA should not be
    supported by untyped evidence.
    """

    if not disease_data:
        return True

    civic_disease = _normalize(entry.get("disease"))
    if not civic_disease:
        return False

    aliases = disease_aliases(disease_data)
    if not aliases:
        return True

    return any(_texts_overlap(civic_disease, alias) for alias in aliases)


def disease_aliases(disease_data: dict[str, Any]) -> tuple[str, ...]:
    aliases: list[str] = []

    disease_id = str(disease_data.get("id") or "").strip().upper()
    aliases.extend(_MANUAL_DISEASE_ALIASES.get(disease_id, ()))

    names = disease_data.get("names") or {}
    if isinstance(names, dict):
        for key in ("preferred", "english", "ukrainian"):
            value = names.get(key)
            if value:
                aliases.append(str(value))
        syns = names.get("synonyms") or []
        if isinstance(syns, list):
            aliases.extend(str(s) for s in syns if s)

    oncotree = disease_data.get("oncotree_code")
    if oncotree:
        aliases.append(str(oncotree))

    normalized = []
    seen = set()
    for alias in aliases:
        norm = _normalize(alias)
        if norm and norm not in seen:
            seen.add(norm)
            normalized.append(norm)
    return tuple(normalized)


def _texts_overlap(left: str, right: str) -> bool:
    if not left or not right:
        return False
    if left in right or right in left:
        return True

    left_tokens = _tokens(left)
    right_tokens = _tokens(right)
    if not left_tokens or not right_tokens:
        return False

    overlap = left_tokens & right_tokens
    return len(overlap) >= min(2, len(left_tokens), len(right_tokens))


def _normalize(value: Any) -> str:
    if value is None:
        return ""
    out = str(value).lower()
    out = out.replace("&", " and ")
    out = re.sub(r"[^a-z0-9]+", " ", out)
    return re.sub(r"\s+", " ", out).strip()


def _tokens(value: str) -> set[str]:
    stop = {"and", "of", "the", "nos", "not", "otherwise", "specified"}
    return {token for token in value.split() if len(token) > 2 and token not in stop}


__all__ = ["civic_entry_matches_disease", "disease_aliases"]
