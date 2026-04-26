"""Read-only citation verification sweep across BMA / Indication / Regimen YAMLs.

Output: docs/reviews/citation-verification-2026-04-27.md

Checks per entity:
1. primary_sources / sources entries reference Source yaml IDs that EXIST.
2. Every claim in evidence_summary / notes that names a trial (LIBRETTO-001,
   ARROW, PETHEMA, FLAURA, ALEX, BEACON, ALINA, CROWN, etc.) has a corresponding
   SRC-TRIAL-* citation (or trial-named SRC-*) in the entity's source list.
3. Claims naming an FDA / EMA approval have a regulatory SRC-FDA-* / SRC-EMA-*
   citation (loose: any source whose ID contains FDA or EMA, or whose
   source_type is 'regulatory' / 'label').
4. Drug names in recommended_combinations are consistent with the
   regulatory_approval block (every drug listed in the combinations should
   appear somewhere in regulatory_approval text, OR be flagged as off-label
   in the combination text itself).
5. oncokb_level vs escat_tier loose mapping:
     IA -> 1
     IB -> 1 or 2
     II / IIA / IIB -> 3A or 3B
     III / IIIA -> 4
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
import yaml

REPO = Path(__file__).resolve().parents[1]
KB = REPO / "knowledge_base" / "hosted" / "content"
SOURCES_DIR = KB / "sources"
BMA_DIR = KB / "biomarker_actionability"
IND_DIR = KB / "indications"
REG_DIR = KB / "regimens"

OUT = REPO / "docs" / "reviews" / "citation-verification-2026-04-27.md"


def load_source_ids() -> set[str]:
    ids = set()
    for f in SOURCES_DIR.glob("*.yaml"):
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"WARN: failed to parse {f}: {e}", file=sys.stderr)
            continue
        if isinstance(data, dict) and "id" in data:
            ids.add(str(data["id"]).strip())
    return ids


# Trial-name patterns we look for in evidence_summary / notes / outcomes.
# Each entry is (display_name, regex). Regex must use word boundaries.
TRIAL_PATTERNS: list[tuple[str, re.Pattern]] = [
    (name, re.compile(rf"\b{re.escape(name)}\b", re.IGNORECASE))
    for name in [
        # NSCLC TKIs
        "FLAURA", "ALEX", "ALINA", "CROWN", "ADAURA", "MARIPOSA", "PAPILLON",
        "ASCEND-4", "ALTA-1L", "PROFILE-1014", "AURA3", "LIBRETTO-001",
        "LIBRETTO-431", "ARROW", "TRIDENT-1", "ENTRECTINIB-1", "STARTRK",
        "CodeBreaK", "KRYSTAL-1",
        # CRC / GI
        "BEACON", "BEACON-CRC", "KEYNOTE-177", "KEYNOTE-590",
        "CheckMate-577", "CheckMate-649", "CROSS", "FLOT4", "PRODIGE",
        "PRIME", "FIRE-3", "CRYSTAL", "PARADIGM",
        # Heme
        "PETHEMA", "APL0406", "AIDA", "ELIANA", "MURANO", "CLL14",
        "ECHELON-1", "ECHELON-2", "BRIGHT", "STIL", "SHINE", "TRIANGLE",
        "GALLIUM", "RELEVANCE", "MAGNOLIA", "BCWM",
        # Breast
        "MONALEESA-2", "MONALEESA-7", "MONARCH-3", "PALOMA-2",
        "MONARCHE", "OLYMPIA", "OLYMPIAD", "EMBRACA", "DESTINY-Breast03",
        "DESTINY-Breast04", "KEYNOTE-522", "CLEOPATRA", "APHINITY",
        "KATHERINE", "ASCENT", "TROPiCS-02",
        # Prostate / GU
        "LATITUDE", "STAMPEDE", "ENZAMET", "TITAN", "ARASENS",
        "PROpel", "MAGNITUDE", "TALAPRO-2", "VISION", "KEYNOTE-426",
        "CheckMate-214", "CheckMate-9ER", "JAVELIN-Bladder-100",
        "EV-302", "PADCEV", "DANUBE",
        # Ovarian / GYN
        "SOLO1", "SOLO-1", "PAOLA-1", "PRIMA", "ATHENA", "ARIEL3",
        "GOG-218", "ICON7", "RUBY", "NRG-GY018",
        # Lung other
        "PACIFIC", "KEYNOTE-024", "KEYNOTE-189", "KEYNOTE-407",
        "KEYNOTE-407", "CASPIAN", "IMpower133", "IMpower150",
        "ADRIATIC",
        # Heme other / MM
        "MAIA", "ALCYONE", "POLLUX", "CASTOR", "GRIFFIN", "CEPHEUS",
        "CARTITUDE-1", "KarMMa", "MajesTEC-1", "MonumenTAL-1",
        # Melanoma
        "COMBI-d", "COMBI-v", "COMBI-AD", "CheckMate-067", "CheckMate-238",
        "KEYNOTE-006", "RELATIVITY-047",
        # GBM / brain
        "Stupp", "EORTC-22981", "EORTC-26981",
        # Pediatric / rare
        "AALL0232", "CALGB-10403",
        # APL
        "APML4", "APL15", "APL17",
        # MDS / AML
        "VIALE-A", "VIALE-C", "QUAZAR", "ASTRAL-1", "COMMANDS",
        "AGILE", "ADMIRAL", "ASTRAL",
        # Lymphoma CAR-T
        "ZUMA-1", "ZUMA-7", "ZUMA-12", "TRANSCEND", "TRANSFORM",
        "BELINDA", "JULIET",
        # T-cell
        "ECHELON-2", "ROMICE", "Lumiere",
        # CML
        "ENESTnd", "DASISION", "BFORE", "ASCEMBL",
        # FGFR / urothelial / cholangio
        "BLC2001", "THOR", "FIGHT-202",
        # KRAS
        "CodeBreaK-200", "KRYSTAL-12",
    ]
]


# Trial mention -> expected source-id substrings. Loose match: if entity has any
# source whose ID contains any of these substrings, the citation passes.
TRIAL_TO_SOURCE_HINTS: dict[str, list[str]] = {
    "LIBRETTO-001": ["LIBRETTO", "SELPERCATINIB"],
    "LIBRETTO-431": ["LIBRETTO", "SELPERCATINIB"],
    "ARROW": ["ARROW", "PRALSETINIB"],
    "FLAURA": ["FLAURA", "OSIMERTINIB", "AURA"],
    "ALEX": ["ALEX", "ALECTINIB"],
    "ALINA": ["ALINA", "ALECTINIB"],
    "CROWN": ["CROWN", "LORLATINIB"],
    "ADAURA": ["ADAURA", "OSIMERTINIB"],
    "PAPILLON": ["PAPILLON", "AMIVANTAMAB"],
    "MARIPOSA": ["MARIPOSA"],
    "PETHEMA": ["PETHEMA", "APL0406", "LOCOCO"],
    "APL0406": ["APL0406", "PETHEMA", "LOCOCO"],
    "BEACON": ["BEACON", "ENCORAFENIB", "KOPETZ"],
    "BEACON-CRC": ["BEACON", "ENCORAFENIB", "KOPETZ"],
    "KEYNOTE-177": ["KEYNOTE-177", "KEYNOTE177"],
    "KEYNOTE-590": ["KEYNOTE-590", "KEYNOTE590"],
    "KEYNOTE-189": ["KEYNOTE-189", "KEYNOTE189"],
    "KEYNOTE-024": ["KEYNOTE-024", "KEYNOTE024"],
    "KEYNOTE-426": ["KEYNOTE-426", "KEYNOTE426"],
    "KEYNOTE-522": ["KEYNOTE-522", "KEYNOTE522"],
    "KEYNOTE-006": ["KEYNOTE-006", "KEYNOTE006"],
    "KEYNOTE-407": ["KEYNOTE-407", "KEYNOTE407"],
    "MURANO": ["MURANO", "VENETOCLAX"],
    "CLL14": ["CLL14", "VENETOCLAX"],
    "ELIANA": ["ELIANA", "TISAGEN", "MAUDE"],
    "MAIA": ["MAIA", "DARATUMUMAB"],
    "ALCYONE": ["ALCYONE"],
    "PACIFIC": ["PACIFIC", "DURVALUMAB"],
    "STAMPEDE": ["STAMPEDE"],
    "LATITUDE": ["LATITUDE", "ABIRATERONE"],
    "ARASENS": ["ARASENS", "DAROLUTAMIDE"],
    "TITAN": ["TITAN", "APALUTAMIDE"],
    "ENZAMET": ["ENZAMET", "ENZALUTAMIDE"],
    "VISION": ["VISION", "LUTETIUM", "PSMA"],
    "PROpel": ["PROPEL", "OLAPARIB-PROST"],
    "TALAPRO-2": ["TALAPRO", "TALAZOPARIB"],
    "MAGNITUDE": ["MAGNITUDE", "NIRAPARIB"],
    "OLYMPIA": ["OLYMPIA", "OLAPARIB"],
    "OLYMPIAD": ["OLYMPIAD", "OLAPARIB"],
    "EMBRACA": ["EMBRACA", "TALAZOPARIB"],
    "SOLO1": ["SOLO", "OLAPARIB"],
    "SOLO-1": ["SOLO", "OLAPARIB"],
    "PAOLA-1": ["PAOLA", "OLAPARIB"],
    "PRIMA": ["PRIMA", "NIRAPARIB"],
    "ATHENA": ["ATHENA", "RUCAPARIB"],
    "RUBY": ["RUBY", "DOSTARLIMAB"],
    "NRG-GY018": ["GY018", "PEMBRO-ENDOM"],
    "EV-302": ["EV-302", "EV302", "ENFORTUMAB", "PADCEV"],
    "PADCEV": ["PADCEV", "ENFORTUMAB", "EV-302"],
    "JAVELIN-Bladder-100": ["JAVELIN", "AVELUMAB"],
    "CheckMate-067": ["CHECKMATE-067", "CHECKMATE067"],
    "CheckMate-214": ["CHECKMATE-214", "CHECKMATE214"],
    "CheckMate-9ER": ["CHECKMATE-9ER", "CABOZ"],
    "CheckMate-577": ["CHECKMATE-577", "CHECKMATE577"],
    "CheckMate-649": ["CHECKMATE-649", "CHECKMATE649"],
    "RELATIVITY-047": ["RELATIVITY", "RELATLIMAB"],
    "ECHELON-1": ["ECHELON-1", "ECHELON1", "BRENTUXIMAB"],
    "ECHELON-2": ["ECHELON-2", "ECHELON2", "BRENTUXIMAB"],
    "ZUMA-1": ["ZUMA-1", "ZUMA1", "AXICEL"],
    "ZUMA-7": ["ZUMA-7", "ZUMA7", "AXICEL"],
    "ZUMA-12": ["ZUMA-12", "ZUMA12"],
    "TRANSCEND": ["TRANSCEND", "LISOCABTAGENE"],
    "TRANSFORM": ["TRANSFORM"],
    "JULIET": ["JULIET", "TISAGEN"],
    "POLLUX": ["POLLUX", "DARATUMUMAB"],
    "CASTOR": ["CASTOR", "DARATUMUMAB"],
    "GRIFFIN": ["GRIFFIN"],
    "CARTITUDE-1": ["CARTITUDE", "CILTACABTAGENE"],
    "KarMMa": ["KARMMA", "IDECABTAGENE"],
    "MajesTEC-1": ["MAJESTEC", "TECLISTAMAB"],
    "MonumenTAL-1": ["MONUMENTAL", "TALQUETAMAB"],
    "VIALE-A": ["VIALE-A", "VIALEA", "VEN-AZA"],
    "VIALE-C": ["VIALE-C"],
    "QUAZAR": ["QUAZAR", "ORAL-AZA", "CC-486"],
    "ADMIRAL": ["ADMIRAL", "GILTERITINIB", "PERL"],
    "AGILE": ["AGILE", "IVOSIDENIB"],
    "MONALEESA-2": ["MONALEESA", "RIBOCICLIB"],
    "MONALEESA-7": ["MONALEESA", "RIBOCICLIB"],
    "MONARCH-3": ["MONARCH", "ABEMACICLIB"],
    "PALOMA-2": ["PALOMA", "PALBOCICLIB"],
    "MONARCHE": ["MONARCHE", "ABEMACICLIB"],
    "DESTINY-Breast03": ["DESTINY-BREAST03", "TDXD", "TRASTUZUMAB-DERUXTECAN"],
    "DESTINY-Breast04": ["DESTINY-BREAST04", "TDXD", "TRASTUZUMAB-DERUXTECAN"],
    "KATHERINE": ["KATHERINE", "TDM1"],
    "CLEOPATRA": ["CLEOPATRA", "PERTUZUMAB"],
    "APHINITY": ["APHINITY"],
    "ASCENT": ["ASCENT", "SACITUZUMAB"],
    "TROPiCS-02": ["TROPICS", "SACITUZUMAB"],
    "COMBI-d": ["COMBI", "DABRAFENIB-TRAMETINIB"],
    "COMBI-v": ["COMBI", "DABRAFENIB-TRAMETINIB"],
    "COMBI-AD": ["COMBI-AD"],
    "CodeBreaK": ["CODEBREAK", "SOTORASIB"],
    "CodeBreaK-200": ["CODEBREAK", "SOTORASIB"],
    "KRYSTAL-1": ["KRYSTAL", "ADAGRASIB"],
    "ENESTnd": ["ENESTND", "NILOTINIB"],
    "DASISION": ["DASISION", "DASATINIB"],
    "BFORE": ["BFORE", "BOSUTINIB"],
    "ASCEMBL": ["ASCEMBL", "ASCIMINIB", "REA"],
    "Stupp": ["STUPP", "TEMOZOLOMIDE"],
    "CROSS": ["CROSS"],
    "PRODIGE": ["PRODIGE"],
    "FLOT4": ["FLOT4", "FLOT"],
    "AALL0232": ["AALL0232"],
    "CALGB-10403": ["CALGB-10403", "CALGB10403", "STOCK"],
    "BLC2001": ["BLC2001", "ERDAFITINIB"],
    "THOR": ["THOR", "ERDAFITINIB"],
    "FIGHT-202": ["FIGHT-202", "PEMIGATINIB"],
    "GALLIUM": ["GALLIUM", "OBINUTUZUMAB"],
    "RELEVANCE": ["RELEVANCE"],
    "SHINE": ["SHINE", "IBRUTINIB-MCL"],
    "TRIANGLE": ["TRIANGLE"],
    "ADRIATIC": ["ADRIATIC", "DURVALUMAB-SCLC"],
    "IMpower133": ["IMPOWER133", "ATEZOLIZUMAB-SCLC"],
    "CASPIAN": ["CASPIAN", "DURVALUMAB-SCLC"],
}


def collect_text_fields(entity: dict) -> str:
    """Concatenate the free-text fields where claims live."""
    parts = []
    for k in ("evidence_summary", "notes", "rationale", "name"):
        v = entity.get(k)
        if isinstance(v, str):
            parts.append(v)
    # expected_outcomes and similar nested dicts may contain trial mentions
    eo = entity.get("expected_outcomes")
    if isinstance(eo, dict):
        for v in eo.values():
            if isinstance(v, str):
                parts.append(v)
    # regulatory_approval block (BMA): drug-by-drug FDA / EMA strings
    ra = entity.get("regulatory_approval")
    if isinstance(ra, dict):
        for v in ra.values():
            if isinstance(v, list):
                parts.extend(str(x) for x in v)
    return " \n ".join(parts)


def collect_source_ids_from_entity(entity: dict) -> list[str]:
    """Return the list of SRC-* IDs cited by this entity."""
    out: list[str] = []
    # BMA / Regimen style
    ps = entity.get("primary_sources")
    if isinstance(ps, list):
        out.extend(str(x).strip() for x in ps if x)
    # Regimen 'sources' as flat list
    s = entity.get("sources")
    if isinstance(s, list):
        for item in s:
            if isinstance(item, str):
                out.append(item.strip())
            elif isinstance(item, dict) and "source_id" in item:
                out.append(str(item["source_id"]).strip())
    return out


# ESCAT -> OncoKB allowed mapping
ESCAT_TO_ONCOKB: dict[str, set[str]] = {
    "IA": {"1"},
    "IB": {"1", "2"},
    "IC": {"1", "2", "2A"},
    "II": {"3A", "3B", "3"},
    "IIA": {"3A", "3B", "3"},
    "IIB": {"3A", "3B", "3"},
    "III": {"4"},
    "IIIA": {"4"},
    "IV": {"4", "R1", "R2"},
    "V": {"R1", "R2"},
    "X": set(),  # not actionable
}


def normalize_level(s: str) -> str:
    return str(s).strip().upper()


def check_escat_oncokb(entity: dict) -> str | None:
    escat = entity.get("escat_tier")
    onco = entity.get("oncokb_level")
    if escat is None or onco is None:
        return None
    e = normalize_level(escat)
    o = normalize_level(onco)
    allowed = ESCAT_TO_ONCOKB.get(e)
    if allowed is None:
        return f"unknown ESCAT tier '{escat}' (cannot validate against OncoKB level '{onco}')"
    if o not in {x.upper() for x in allowed}:
        return f"ESCAT {escat} typically maps to OncoKB {{{','.join(sorted(allowed))}}} but entity declares OncoKB level '{onco}'"
    return None


def fda_ema_check(entity: dict, source_ids: list[str], all_source_ids: set[str], source_meta: dict[str, dict]) -> list[str]:
    """If regulatory_approval lists FDA / EMA approvals, flag if no regulatory
    source is among the citations. We accept any source whose ID contains
    'FDA' or 'EMA', or whose source_type is 'regulatory_label' / 'regulatory'
    / 'label' / 'drug_label'.
    """
    findings: list[str] = []
    ra = entity.get("regulatory_approval")
    if not isinstance(ra, dict):
        return findings
    has_fda = bool(ra.get("fda"))
    has_ema = bool(ra.get("ema"))
    if not (has_fda or has_ema):
        return findings
    has_regulatory_src = False
    for sid in source_ids:
        if "FDA" in sid.upper() or "EMA" in sid.upper() or "DAILYMED" in sid.upper() or "OPENFDA" in sid.upper():
            has_regulatory_src = True
            break
        meta = source_meta.get(sid)
        if meta:
            stype = str(meta.get("source_type", "")).lower()
            if stype in {"regulatory_label", "regulatory", "label", "drug_label", "fda_label", "ema_label"}:
                has_regulatory_src = True
                break
    if not has_regulatory_src:
        bits = []
        if has_fda:
            bits.append(f"FDA approvals listed ({len(ra.get('fda', []))})")
        if has_ema:
            bits.append(f"EMA approvals listed ({len(ra.get('ema', []))})")
        findings.append(
            "regulatory_approval cites " + " + ".join(bits)
            + " but no FDA/EMA-tagged Source entity is among primary_sources"
        )
    return findings


def trial_mention_check(entity: dict, text: str, source_ids: list[str]) -> list[str]:
    """Find trial-name mentions in evidence_summary/notes that lack a corresponding source."""
    findings: list[str] = []
    cited_upper = [s.upper() for s in source_ids]
    seen_trials: set[str] = set()
    for trial_name, pat in TRIAL_PATTERNS:
        if pat.search(text) and trial_name not in seen_trials:
            seen_trials.add(trial_name)
            hints = TRIAL_TO_SOURCE_HINTS.get(trial_name, [trial_name.upper()])
            # remove all-non-alphanum from hints for loose match
            hint_upper = [h.upper() for h in hints]
            ok = False
            for sid in cited_upper:
                for h in hint_upper:
                    if h in sid:
                        ok = True
                        break
                if ok:
                    break
            if not ok:
                findings.append(f"trial '{trial_name}' mentioned but no matching source citation (looked for substrings: {hints})")
    return findings


def drug_consistency_check(entity: dict) -> list[str]:
    """For a BMA: every drug listed in recommended_combinations should appear
    in the regulatory_approval text, OR the combination string must mark itself
    off-label / experimental.
    """
    findings: list[str] = []
    rc = entity.get("recommended_combinations")
    ra = entity.get("regulatory_approval")
    if not isinstance(rc, list) or not isinstance(ra, dict):
        return findings
    reg_text = ""
    for v in ra.values():
        if isinstance(v, list):
            reg_text += " " + " ".join(str(x) for x in v)
    reg_text_low = reg_text.lower()
    for combo in rc:
        if not isinstance(combo, str):
            continue
        # Skip if explicitly flagged off-label / investigational / clinical-trial
        low = combo.lower()
        if any(tag in low for tag in ["off-label", "off label", "investigational", "clinical trial", "compassionate", "experimental"]):
            continue
        # Tokenize on '+' / ' or ' and pick simple drug names
        # Strip parenthetical comments
        core = re.sub(r"\(.*?\)", "", combo)
        # Split by '+' and ' or '
        parts = re.split(r"\+|\bor\b|/", core)
        missing: list[str] = []
        for p in parts:
            tok = p.strip().lower()
            if not tok:
                continue
            # drop non-drug fillers
            tok = re.sub(r"\b(monotherapy|maintenance|mono|continuous|with|food|dose|bid|qd|po|iv|sc)\b", "", tok).strip()
            if not tok or len(tok) < 4:
                continue
            # take first word as best-effort drug name
            head = tok.split()[0]
            if head in {"the", "any", "and"}:
                continue
            if head in _GENERIC_COMBO_TOKENS:
                continue
            if head not in reg_text_low:
                missing.append(head)
        if missing:
            findings.append(
                f"recommended_combination '{combo}' contains drug name(s) {missing} not appearing in regulatory_approval text "
                "(may be legitimate combination-component naming OR off-label not flagged)"
            )
    return findings


def src_existence_check(source_ids: list[str], all_ids: set[str]) -> list[str]:
    findings: list[str] = []
    for sid in source_ids:
        if sid not in all_ids:
            findings.append(f"primary_sources entry '{sid}' does not match any Source yaml id")
    return findings


SEVERITY_ORDER = {"yaml-parse-error": 0, "broken-citation": 1, "missing-trial-source": 2, "missing-regulatory-source": 2, "level-mismatch": 3, "drug-inconsistency": 4, "suggestion": 5}


# Noise-suppression: if recommended_combination collapses to one of these
# generic words after stripping fillers, skip the drug-inconsistency check.
_GENERIC_COMBO_TOKENS = {
    "standard", "platinum", "chemotherapy", "chemo", "best", "supportive",
    "observation", "clinical", "trial", "treatment", "therapy", "regimen",
    "watch", "wait", "hospice", "palliative", "no", "none",
}


def main() -> int:
    if not SOURCES_DIR.exists():
        print(f"sources dir not found: {SOURCES_DIR}", file=sys.stderr)
        return 2
    all_ids = load_source_ids()
    # Also build metadata for source_type lookup
    source_meta: dict[str, dict] = {}
    for f in SOURCES_DIR.glob("*.yaml"):
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict) and "id" in data:
            source_meta[str(data["id"]).strip()] = data

    print(f"loaded {len(all_ids)} source IDs")

    findings: list[dict] = []  # {entity_id, kind, type (file kind), severity, message}

    def add(entity_id: str, kind: str, etype: str, severity: str, message: str):
        findings.append({"entity_id": entity_id, "kind": kind, "type": etype, "severity": severity, "message": message})

    # BMA
    bma_files = sorted(BMA_DIR.glob("*.yaml"))
    ind_files = sorted(IND_DIR.glob("*.yaml"))
    reg_files = sorted(REG_DIR.glob("*.yaml"))

    for f in bma_files:
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception as e:
            add(f.name, "BMA", "parse-error", "yaml-parse-error", f"YAML parse error: {e}")
            continue
        if not isinstance(data, dict):
            continue
        eid = str(data.get("id", f.stem))
        sids = collect_source_ids_from_entity(data)
        for msg in src_existence_check(sids, all_ids):
            add(eid, "BMA", f.name, "broken-citation", msg)
        text = collect_text_fields(data)
        for msg in trial_mention_check(data, text, sids):
            add(eid, "BMA", f.name, "missing-trial-source", msg)
        for msg in fda_ema_check(data, sids, all_ids, source_meta):
            add(eid, "BMA", f.name, "missing-regulatory-source", msg)
        mm = check_escat_oncokb(data)
        if mm:
            add(eid, "BMA", f.name, "level-mismatch", mm)
        for msg in drug_consistency_check(data):
            add(eid, "BMA", f.name, "drug-inconsistency", msg)

    for f in ind_files:
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception as e:
            add(f.name, "Indication", "parse-error", "yaml-parse-error", f"YAML parse error: {e}")
            continue
        if not isinstance(data, dict):
            continue
        eid = str(data.get("id", f.stem))
        sids = collect_source_ids_from_entity(data)
        for msg in src_existence_check(sids, all_ids):
            add(eid, "Indication", f.name, "broken-citation", msg)
        text = collect_text_fields(data)
        for msg in trial_mention_check(data, text, sids):
            add(eid, "Indication", f.name, "missing-trial-source", msg)

    for f in reg_files:
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception as e:
            add(f.name, "Regimen", "parse-error", "yaml-parse-error", f"YAML parse error: {e}")
            continue
        if not isinstance(data, dict):
            continue
        eid = str(data.get("id", f.stem))
        sids = collect_source_ids_from_entity(data)
        for msg in src_existence_check(sids, all_ids):
            add(eid, "Regimen", f.name, "broken-citation", msg)
        text = collect_text_fields(data)
        for msg in trial_mention_check(data, text, sids):
            add(eid, "Regimen", f.name, "missing-trial-source", msg)

    # Summary counters
    n_total = len(bma_files) + len(ind_files) + len(reg_files)
    n_bma = len(bma_files)
    n_ind = len(ind_files)
    n_reg = len(reg_files)
    by_sev: dict[str, int] = {}
    by_kind: dict[str, int] = {}
    for fnd in findings:
        by_sev[fnd["severity"]] = by_sev.get(fnd["severity"], 0) + 1
        by_kind[fnd["kind"]] = by_kind.get(fnd["kind"], 0) + 1

    # Per-entity grouping
    per_entity: dict[str, list[dict]] = {}
    for fnd in findings:
        per_entity.setdefault(fnd["entity_id"], []).append(fnd)

    # Sort entities by max severity (lowest order = most severe), then by count
    def entity_key(eid: str):
        items = per_entity[eid]
        return (min(SEVERITY_ORDER.get(i["severity"], 9) for i in items), -len(items), eid)

    sorted_entities = sorted(per_entity.keys(), key=entity_key)

    # Build report
    md: list[str] = []
    md.append("# Citation verification sweep — 2026-04-27\n")
    md.append("Read-only audit (no YAMLs modified). Triage input for clinical co-leads.\n")
    md.append("")
    md.append("## Summary\n")
    md.append(f"- Source yamls indexed: **{len(all_ids)}**")
    md.append(f"- Total entities checked: **{n_total}**")
    md.append(f"  - BiomarkerActionability (BMA): {n_bma}")
    md.append(f"  - Indications: {n_ind}")
    md.append(f"  - Regimens: {n_reg}")
    md.append("")
    md.append("### Counters by severity\n")
    md.append(f"- YAML parse errors (entity could not be evaluated): **{by_sev.get('yaml-parse-error', 0)}**")
    md.append(f"- Broken citations (primary_sources entry not found in `sources/`): **{by_sev.get('broken-citation', 0)}**")
    md.append(f"- Missing trial sources (trial named in evidence_summary/notes but no matching SRC-*): **{by_sev.get('missing-trial-source', 0)}**")
    md.append(f"- Missing regulatory sources (FDA/EMA approval cited without an FDA/EMA Source entity): **{by_sev.get('missing-regulatory-source', 0)}**")
    md.append(f"- ESCAT vs OncoKB level mismatches: **{by_sev.get('level-mismatch', 0)}**")
    md.append(f"- recommended_combinations vs regulatory_approval drug inconsistencies: **{by_sev.get('drug-inconsistency', 0)}**")
    md.append("")
    md.append("### Counters by entity kind\n")
    md.append(f"- Findings on BMA: {by_kind.get('BMA', 0)}")
    md.append(f"- Findings on Indication: {by_kind.get('Indication', 0)}")
    md.append(f"- Findings on Regimen: {by_kind.get('Regimen', 0)}")
    md.append(f"- Total findings: **{len(findings)}**")
    md.append(f"- Entities with at least one finding: **{len(per_entity)}**")
    md.append("")

    # Top 20 most-impactful gaps
    md.append("## Top 20 most-impactful gaps\n")
    md.append("Ordered by (worst severity first, then highest finding count). Use this list for Source-stub triage.\n")
    top = sorted_entities[:20]
    if not top:
        md.append("_No findings._\n")
    else:
        md.append("| # | Entity | Kind | Worst severity | Findings | First-line note |")
        md.append("|---|--------|------|----------------|----------|-----------------|")
        for i, eid in enumerate(top, 1):
            items = per_entity[eid]
            worst = min(items, key=lambda x: SEVERITY_ORDER.get(x["severity"], 9))
            md.append(
                f"| {i} | `{eid}` | {worst['kind']} | {worst['severity']} | {len(items)} | {worst['message'][:120].replace('|', '/')} |"
            )
        md.append("")

    md.append("## Per-entity findings\n")
    md.append("Severity precedence: yaml-parse-error > broken-citation > missing-trial-source / missing-regulatory-source > level-mismatch > drug-inconsistency > suggestion.\n")
    if not sorted_entities:
        md.append("_No findings — all entities pass the configured checks._\n")
    else:
        for eid in sorted_entities:
            items = per_entity[eid]
            kind = items[0]["kind"]
            file_hint = items[0]["type"]
            md.append(f"### `{eid}` ({kind} — `{file_hint}`)")
            # sort items by severity
            items_sorted = sorted(items, key=lambda x: SEVERITY_ORDER.get(x["severity"], 9))
            for it in items_sorted:
                md.append(f"- **[{it['severity']}]** {it['message']}")
            md.append("")

    md.append("## Methodology notes\n")
    md.append("- Trial-name pattern list is a curated set of well-known oncology trials; entities citing trials outside that list are not flagged. Treat findings as a triage seed, not an exhaustive audit.")
    md.append("- Trial-to-source matching is loose: an entity passes if ANY of its cited source IDs contains one of the substring hints registered for that trial. False negatives are possible when source IDs are named idiosyncratically.")
    md.append("- ESCAT->OncoKB mapping uses the loose ranges in the brief (IA->1, IB->1/2, II->3A/3B, III->4). Real-world borderline cases (e.g. IB->3A for combo-only approvals) are flagged for human review, not auto-corrected.")
    md.append("- FDA/EMA regulatory check passes if any cited source's ID contains `FDA`, `EMA`, `DAILYMED`, or `OPENFDA`, OR if its `source_type` is regulatory/label.")
    md.append("- Drug-consistency check is best-effort token matching against the `regulatory_approval` block; combinations explicitly tagged 'off-label' / 'investigational' are skipped.")
    md.append("- This script is `scripts/verify_citations_2026_04_27.py`.")
    md.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(md), encoding="utf-8")
    print(f"report written: {OUT}")
    print(f"findings: {len(findings)} across {len(per_entity)} entities")
    print(f"by severity: {json.dumps(by_sev, sort_keys=True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
