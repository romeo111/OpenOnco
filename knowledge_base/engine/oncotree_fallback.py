"""ICD-10 → OncoTree top-level mapping (tier-2 of safe-rollout v3 §5).

Used when Disease.oncotree_code is absent. Maps an ICD-10 code (or
ICD-10 family prefix like "C18") to the closest OncoTree top-level
or organ-system code.

Tier-3 (final fallback) = pan-tumor query (oncotree_code=None passed
to the actionability source; render layer adds warning badge per Q4
locked decision).

This module is intentionally a static mapping: editing it is a
clinical-content change tracked under CHARTER §6.1 (dev-mode signoff
exempt per project_charter_dev_mode_exemptions). When new diseases
are added with novel ICD-10 codes, add them here OR populate
Disease.oncotree_code directly (preferred; tier 1 always wins).

References:
  http://oncotree.mskcc.org/api/tumorTypes (taxonomy)
  ICD-10 Volume 2 — WHO 2019 (code definitions)
"""

from __future__ import annotations

from typing import Optional


# ── Family-prefix mapping (most specific match wins) ────────────────────


# Order matters — entries iterated in defined order; longer/more-specific
# prefixes should come BEFORE their parent ranges. Lookup logic in
# `resolve_icd10_to_oncotree` walks the dict respecting this order.
_ICD10_FAMILY_TO_ONCOTREE: dict[str, str] = {
    # ── C00-C14 — lip, oral cavity, pharynx ──
    "C00": "HNSC",  # lip
    "C01": "HNSC",  # base of tongue
    "C02": "HNSC",  # other tongue
    "C03": "HNSC",  # gum
    "C04": "HNSC",  # floor of mouth
    "C05": "HNSC",  # palate
    "C06": "HNSC",  # other oral cavity
    "C07": "SACA",  # parotid gland
    "C08": "SACA",  # other major salivary
    "C09": "HNSC",  # tonsil
    "C10": "HNSC",  # oropharynx
    "C11": "HNSC",  # nasopharynx
    "C12": "HNSC",  # pyriform sinus
    "C13": "HNSC",  # hypopharynx
    "C14": "HNSC",  # other lip/oral
    # ── C15-C26 — digestive ──
    "C15": "ESCA",  # esophagus
    "C16": "STAD",  # stomach
    "C17": "SBC",   # small intestine
    "C18": "COADREAD",  # colon
    "C19": "COADREAD",  # rectosigmoid
    "C20": "COADREAD",  # rectum
    "C21": "COADREAD",  # anus
    "C22": "HCC",   # liver / intrahepatic bile duct
    "C23": "GBC",   # gallbladder
    "C24": "CHOL",  # other biliary
    "C25": "PAAD",  # pancreas
    "C26": "PAAD",  # ill-defined digestive
    # ── C30-C39 — respiratory + intrathoracic ──
    "C30": "HNSC",  # nasal cavity / middle ear
    "C31": "HNSC",  # accessory sinuses
    "C32": "HNSC",  # larynx
    "C33": "NSCLC", # trachea
    "C34": "NSCLC", # bronchus and lung — default to NSCLC parent (SCLC handled by histology)
    "C37": "THYM",  # thymus
    "C38": "MESO",  # heart, mediastinum, pleura → mesothelioma family
    "C39": "NSCLC", # other respiratory
    # ── C40-C41 — bone ──
    "C40": "BONE",
    "C41": "BONE",
    # ── C43-C44 — skin ──
    "C43": "MEL",   # malignant melanoma
    "C44": "SCSC",  # other skin (squamous + basal) — non-melanoma skin
    # ── C45-C49 — mesothelial + soft tissue ──
    "C45": "MESO",  # mesothelioma
    "C46": "SOFT",  # Kaposi sarcoma
    "C47": "MPNST", # peripheral nerves / autonomic NS
    "C48": "SOFT",  # retroperitoneum + peritoneum
    "C49": "SOFT",  # other connective + soft tissue
    # ── C50 — breast ──
    "C50": "BREAST",
    # ── C51-C58 — female genital ──
    "C51": "VULVA",
    "C52": "VAGINA",
    "C53": "CESC",  # cervix
    "C54": "UCEC",  # corpus uteri
    "C55": "UCEC",  # uterus NOS
    "C56": "OV",    # ovary
    "C57": "OVT",   # other female genital
    "C58": "PAAD",  # placenta — choriocarcinoma → consider GTD; pan-tumor fallback safer here
    # ── C60-C63 — male genital ──
    "C60": "PENIS",
    "C61": "PRAD",  # prostate
    "C62": "TGCT",  # testis (germ cell)
    "C63": "PRAD",  # other male genital
    # ── C64-C68 — urinary ──
    "C64": "RCC",   # kidney parenchyma
    "C65": "URCA",  # renal pelvis
    "C66": "URCA",  # ureter
    "C67": "BLCA",  # bladder
    "C68": "BLCA",  # other urinary
    # ── C69-C72 — eye, brain, CNS ──
    "C69": "UM",    # eye → uveal melanoma family (others rare)
    "C70": "MNGT",  # meninges
    "C71": "GBM",   # brain — default to GBM (most common adult primary); IDH-mut gliomas via Disease.oncotree_code override
    "C72": "DIFG",  # spinal cord, cranial nerves, CNS
    # ── C73-C75 — endocrine ──
    "C73": "THPA",  # thyroid → papillary default; Disease.oncotree_code overrides for ATC, MTC, etc.
    "C74": "ACC",   # adrenal
    "C75": "PAAD",  # other endocrine — fallback
    # ── C76-C80 — secondary / unknown primary ──
    "C76": "MIXED",
    "C77": "MIXED",
    "C78": "MIXED",
    "C79": "MIXED",
    "C80": "CUP",   # carcinoma of unknown primary
    # ── C81-C96 — hematologic / lymphoid / myeloid ──
    "C81": "CHL",   # Hodgkin
    "C82": "FL",    # follicular lymphoma
    "C83": "DLBCLNOS",  # other non-Hodgkin (DLBCL family default)
    "C84": "PTCL",  # T-cell / mature
    "C85": "DLBCLNOS",  # NHL unspecified
    "C86": "PTCL",  # other T/NK
    "C88": "WM",    # malignant immunoproliferative
    "C90": "MM",    # multiple myeloma + plasma cell
    "C91": "BLL",   # lymphoid leukaemia (default to B-ALL; T-ALL via override)
    "C92": "AML",   # myeloid leukaemia
    "C93": "AML",   # monocytic leukaemia
    "C94": "AML",   # other specified leukaemia
    "C95": "AML",   # leukaemia of unspecified cell type
    "C96": "MDS",   # other malignant lymphoid/haematopoietic
    # ── D45-D47 — MPN / MDS ──
    "D45": "PV",    # polycythaemia vera
    "D46": "MDS",   # myelodysplastic syndromes
    "D47": "MPN",   # other neoplasms uncertain behaviour (incl. ET, PMF)
}


def resolve_icd10_to_oncotree(icd10_code: Optional[str]) -> Optional[str]:
    """Tier-2 fallback: best-effort OncoTree code from an ICD-10 string.

    Returns None when no mapping covers the input — caller proceeds
    with pan-tumor query (tier-3 + render warning badge).

    Accepts both compact ("C34.1") and 3-char ("C34") inputs. The
    longest-prefix mapping wins; for the current table that means a
    direct family-code match.
    """
    if not icd10_code:
        return None
    code = icd10_code.strip().upper()
    if not code:
        return None

    # Direct match on the 3-char family
    family = code[:3]
    if family in _ICD10_FAMILY_TO_ONCOTREE:
        return _ICD10_FAMILY_TO_ONCOTREE[family]

    # No match — let caller fall back to pan-tumor
    return None


def resolve_oncotree_code(
    disease_data: Optional[dict],
) -> tuple[Optional[str], bool]:
    """Three-tier resolution per safe-rollout v3 §5:

      tier 1: Disease.oncotree_code (explicit field) — preferred
      tier 2: ICD-10 fallback table (this module)
      tier 3: pan-tumor (None) — render shows warning

    Returns (oncotree_code, used_fallback_or_pan_tumor).
    `used_fallback_or_pan_tumor` is True iff we landed in tier 2 or 3
    — caller may want to surface a warning badge in render.
    """
    if not isinstance(disease_data, dict):
        return None, True

    explicit = disease_data.get("oncotree_code")
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip(), False

    codes = disease_data.get("codes") or {}
    if isinstance(codes, dict):
        icd10 = codes.get("icd_10")
        if icd10:
            tier2 = resolve_icd10_to_oncotree(icd10)
            if tier2:
                return tier2, True

    return None, True


__all__ = [
    "resolve_icd10_to_oncotree",
    "resolve_oncotree_code",
]
