"""Disease-appropriate demographics for generated example profiles.

The example generators used to hardcode a constant `sex` with no disease
awareness — three defaulted to "male" and one to "female". That produced
24 anatomically incoherent synthetic profiles (male cervical/ovarian/
endometrial cancer, female prostate cancer), 22 of them published.

`sex` is inert in the engine (nothing under knowledge_base/engine/ reads
it), so this was never a clinical misroute — but a male cervical-cancer
patient in a public example destroys credibility with exactly the
clinicians the project is asking to review it.

Only anatomically sex-specific diseases are constrained here. Everything
else keeps the caller's default: sex is a property of the patient, not of
the tumor, and over-constraining it would make real patients
unrepresentable.
"""

from __future__ import annotations

# Diseases defined by anatomy that only one sex has. Breast is deliberately
# absent: male breast cancer is real, and the KB models it explicitly
# (diseases/breast_cancer.yaml — "Male breast cancer follows the same
# algorithm with gender-specific notes"). Generators default breast to
# female for epidemiological plausibility, but male breast profiles are
# valid and must not be rewritten.
_SEX_SPECIFIC: dict[str, str] = {
    "DIS-CERVICAL": "female",
    "DIS-ENDOMETRIAL": "female",
    "DIS-OVARIAN": "female",
    "DIS-SERTOLI-LEYDIG-OVARIAN": "female",
    "DIS-VULVAR-VAGINAL-SCC": "female",
    "DIS-PROSTATE": "male",
    "DIS-TESTICULAR-GCT": "male",
    "DIS-PENILE-SCC": "male",
}

# Diseases that occur in both sexes but whose synthetic default should be
# the epidemiologically dominant one rather than a constant.
_PREFERRED_DEFAULT: dict[str, str] = {
    "DIS-BREAST": "female",
}


def sex_for_disease(disease_id: str | None, default: str = "male") -> str:
    """Return a plausible `demographics.sex` for a synthetic profile.

    Anatomically sex-specific diseases are pinned; a disease that occurs in
    both sexes falls back to its preferred default, then to the caller's.
    """
    if not disease_id:
        return default
    did = str(disease_id).upper()
    if did in _SEX_SPECIFIC:
        return _SEX_SPECIFIC[did]
    return _PREFERRED_DEFAULT.get(did, default)


def is_sex_incoherent(disease_id: str | None, sex: str | None) -> bool:
    """True if `sex` is impossible for `disease_id`.

    Only flags the anatomically impossible; a male breast-cancer profile is
    not incoherent and must not be reported as one.
    """
    if not disease_id or not sex:
        return False
    required = _SEX_SPECIFIC.get(str(disease_id).upper())
    return bool(required and str(sex).lower() != required)
