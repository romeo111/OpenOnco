"""Second-pass: fill `reimbursement_indications` for pkg1 drugs that are
already flagged `reimbursed_nszu: true` but have an empty indication list.

Indications drafted from clinical knowledge of the NSZU онкопакет 2025/2026
formulary and the «Доступні ліки» reimbursement program. These are
**rendering metadata only** — the engine never reads them as a selection
signal (specs/ua_ingestion plan §0 invariant).

Source coverage notes are appended in the per-drug `notes:` field at the
ukraine_registration level (or kept short — the generic citation already
covers source URLs).

Run: py -3.12 scripts/_pkg1_indications.py
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DRUGS_DIR = REPO / "knowledge_base" / "hosted" / "content" / "drugs"

# stem -> list of UA indication strings.
# Phrasing follows the existing convention seen in fluorouracil.yaml,
# cisplatin.yaml etc. — concise UA disease names referencing the NSZU
# package.
INDICATIONS: dict[str, list[str]] = {
    # Hormonals — breast / prostate
    "abiraterone": [
        "Метастатичний кастраційно-резистентний рак передміхурової залози (mCRPC)",
        "Метастатичний гормон-чутливий рак передміхурової залози високого ризику (mHSPC, LATITUDE/STAMPEDE)",
    ],
    "anastrozole": [
        "Гормон-чутливий рак молочної залози (ад'ювантна терапія, постменопауза)",
        "Метастатичний гормон-чутливий рак молочної залози",
    ],
    "enzalutamide": [
        "Метастатичний кастраційно-резистентний рак передміхурової залози (mCRPC)",
        "Метастатичний гормон-чутливий рак передміхурової залози (mHSPC)",
        "Неметастатичний кастраційно-резистентний рак передміхурової залози (nmCRPC)",
    ],
    "exemestane": [
        "Гормон-чутливий рак молочної залози (ад'ювантна, постменопауза)",
        "Метастатичний гормон-чутливий рак молочної залози (після нестероїдного АІ)",
    ],
    "fulvestrant": [
        "Метастатичний HR+/HER2- рак молочної залози (моно- або у комбінації з CDK4/6i / alpelisib)",
    ],
    "letrozole": [
        "Гормон-чутливий рак молочної залози (ад'ювантна, постменопауза)",
        "Метастатичний гормон-чутливий рак молочної залози",
    ],
    "tamoxifen": [
        "Гормон-чутливий рак молочної залози (ад'ювантна, пременопауза/постменопауза)",
        "Метастатичний гормон-чутливий рак молочної залози",
        "Профілактика рецидиву DCIS",
    ],
    "leuprolide": [
        "Рак передміхурової залози (АДТ)",
        "Гормон-чутливий рак молочної залози (пременопауза, у комбінації з АІ)",
    ],
    "goserelin": [
        "Рак передміхурової залози (АДТ, моно- або у комбінації)",
        "Гормон-чутливий рак молочної залози (пременопауза, овариальна супресія)",
    ],

    # Cytotoxics — broad NSZU coverage
    "bleomycin": [
        "Лімфома Ходжкіна (ABVD)",
        "Гермінативно-клітинні пухлини (BEP)",
    ],
    "capecitabine": [
        "Колоректальний рак (ад'ювантна, метастатична)",
        "Рак шлунка / стравохідно-шлункового з'єднання",
        "Рак молочної залози (метастатична, у комбінації)",
    ],
    "capecitabine_breast": [
        "Метастатичний рак молочної залози (моно- або у комбінації, у т.ч. HER2CLIMB / трастузумаб)",
        "Залишкова інвазія TNBC після неоад'ювантної терапії (CREATE-X)",
    ],
    "cladribine": [
        "Волосистоклітинний лейкоз (1L)",
        "Лангергансово-клітинний гістіоцитоз",
    ],
    "cytarabine": [
        "Гострий мієлоїдний лейкоз (індукція 7+3, консолідація HiDAC)",
        "Гострий лімфобластний лейкоз (інтратекальна профілактика ЦНС)",
        "Лімфоми (R-DHAP, R-ESHAP — рятівні схеми)",
    ],
    "dacarbazine": [
        "Лімфома Ходжкіна (ABVD)",
        "Метастатична меланома (моно- або у комбінації)",
        "Саркоми м'яких тканин",
    ],
    "daunorubicin": [
        "Гострий мієлоїдний лейкоз (7+3 індукція)",
        "Гострий промієлоцитарний лейкоз (AIDA, з ATRA/ATO)",
        "Гострий лімфобластний лейкоз (індукція)",
    ],
    "doxorubicin": [
        "Лімфома Ходжкіна (ABVD)",
        "Дифузна великоклітинна B-клітинна лімфома (R-CHOP)",
        "Рак молочної залози (AC/EC ад'ювантна)",
        "Саркоми м'яких тканин",
    ],
    "fludarabine": [
        "Хронічний лімфоцитарний лейкоз (FCR — у відібраних випадках без TP53/del17p)",
        "Кондиціонування перед CAR-T / ало-ТКМ (флударабін + циклофосфамід / мелфалан)",
        "Низькоступеневі лімфоми (рятівні схеми)",
    ],
    "hydroxyurea": [
        "Хронічна мієлоїдна лейкемія (циторедукція до старту ТКІ)",
        "Справжня поліцитемія / есенціальна тромбоцитемія високого ризику",
        "Гострі лейкози (циторедукція при гіперлейкоцитозі)",
    ],
    "idarubicin": [
        "Гострий мієлоїдний лейкоз (7+3 індукція)",
        "Гострий промієлоцитарний лейкоз (AIDA)",
    ],
    "leucovorin": [
        "Колоректальний рак (FOLFOX, FOLFIRI — модулятор 5-ФУ)",
        "Рятувальна терапія після високих доз метотрексату",
    ],
    "mercaptopurine": [
        "Гострий лімфобластний лейкоз (підтримка)",
    ],
    "pemetrexed": [
        "Неплоскоклітинний недрібноклітинний рак легень (1L + підтримка)",
        "Злоякісна плевральна мезотеліома",
    ],
    "pertuzumab": [
        "HER2+ рак молочної залози (неоад'ювантна, ад'ювантна, метастатична — у комбінації з трастузумабом)",
    ],
    "prednisone": [
        "Лімфоми (R-CHOP, BEACOPP, CVP)",
        "Гострі лейкози (індукція ALL)",
        "Множинна мієлома (VMP, VRd, Rd — у комбінації)",
    ],
    "temozolomide": [
        "Гліобластома (Stupp — конкомітантно з променевою терапією та ад'ювантно)",
        "Анапластична астроцитома / олігодендрогліома",
    ],
    "vinblastine": [
        "Лімфома Ходжкіна (ABVD)",
        "Гермінативно-клітинні пухлини",
    ],
    "vincristine": [
        "Лімфоми (R-CHOP, BEACOPP, EPOCH)",
        "Гострий лімфобластний лейкоз (індукція + підтримка)",
        "Множинна мієлома (VAD — історично)",
    ],

    # CML / TKI
    "dasatinib": [
        "Хронічна мієлоїдна лейкемія (1L хронічна фаза, прискорена/бластна фаза)",
        "Ph+ гострий лімфобластний лейкоз (у комбінації з хіміотерапією)",
    ],
    "nilotinib": [
        "Хронічна мієлоїдна лейкемія (1L хронічна фаза, 2L після іматинібу)",
    ],

    # Bone-targeted
    "denosumab": [
        "Профілактика скелетних подій при метастазах у кістки (Xgeva)",
        "Гігантоклітинна пухлина кістки (нерезектабельна / рецидивна)",
    ],
    "zoledronate": [
        "Профілактика скелетних подій при метастазах у кістки (солідні пухлини)",
        "Множинна мієлома (профілактика остеолітичних подій)",
        "Гіперкальциємія злоякісного ґенезу",
    ],

    # Supportive — «Доступні ліки» / онкопакет
    "acyclovir": [
        "Профілактика реактивації HSV/VZV при імуносупресивній терапії (інгібітори протеасоми, флударабін, ало-ТКМ)",
        "Лікування активних HSV/VZV інфекцій",
    ],
    "allopurinol": [
        "Профілактика синдрому лізису пухлини",
        "Гіперурикемія",
    ],
    "dexamethasone": [
        "Антиеметична профілактика при високоемоегенній хіміотерапії",
        "Множинна мієлома (VRd, VCD, Rd, KRd — компонент)",
        "Лімфоми (R-CHOP, BEACOPP, R-DHAP)",
        "Симптоматичне лікування пухлинного набряку (ЦНС, спинальної компресії)",
    ],
    "epoetin_alfa": [
        "Анемія у пацієнтів з хіміотерапіями (у відповідних показаннях)",
        "Анемія при мієлодиспластичних синдромах низького ризику",
    ],
    "filgrastim": [
        "Профілактика та лікування фебрильної нейтропенії (Г-КСФ підтримка)",
        "Мобілізація гемопоетичних стовбурових клітин для авто-/ало-ТКМ",
    ],
    "ondansetron": [
        "Антиеметична профілактика при хіміотерапії (5-HT3 антагоніст)",
    ],
    "trimethoprim_sulfamethoxazole": [
        "Профілактика Pneumocystis jirovecii (PJP) у пацієнтів з імуносупресією (флударабін, ритуксимаб, тривала кортикостероїдна терапія)",
    ],
}


# Per-drug refined notes (only when current notes is missing or generic).
NOTES_OVERRIDE: dict[str, str] = {
    "abiraterone": (
        "Доступний як генерик; покривається НСЗУ для mCRPC та "
        "mHSPC високого ризику. Перевірено 2026-04-27 (drlz.com.ua, "
        "nszu.gov.ua/likuvannya-zlovkisnykh-novoutvoren)."
    ),
    "rituximab": (
        "Біосиміляри (Truxima, Ruxience, Riabni) широко доступні в "
        "Україні — взаємозамінні з MabThera за керівництвом НСЗУ. "
        "Перевірено 2026-04-27."
    ),
    "filgrastim": (
        "Біосиміляри філграстиму (Tevagrastim, Zarzio, Nivestim тощо) "
        "включені в онкопакет НСЗУ як підтримуюча терапія. "
        "Перевірено 2026-04-27."
    ),
    "trastuzumab": (
        "Біосиміляри (Herzuma, Ontruzant, Kanjinti) широко доступні; "
        "взаємозамінні. Покриття НСЗУ для HER2+ РМЗ та HER2+ раку "
        "шлунка. Перевірено 2026-04-27."
    ),
    "procarbazine": (
        "Не зареєстрований в Україні (Держреєстр ЛЗ — не знайдено "
        "станом на 2026-04-27). Доступ через named-patient import "
        "для PCNSL (R-MPV) та escalated BEACOPP. Перевірено 2026-04-27."
    ),
    "trifluridine_tipiracil": (
        "Зареєстрований в Україні; НЕ покривається НСЗУ. Out-of-pocket "
        "або через благодійні програми / клінічні дослідження. "
        "Перевірено 2026-04-27."
    ),
    "anagrelide": (
        "Зареєстрований; НЕ в основному переліку НСЗУ — "
        "хідроксисечовина залишається 1L cytoredutive option для PV/ET. "
        "Перевірено 2026-04-27."
    ),
    "apalutamide": (
        "Зареєстрований; станом на 2026-04 не покривається НСЗУ. "
        "Out-of-pocket або через благодійні програми. Перевірено 2026-04-27."
    ),
    "aspirin": (
        "OTC — не входить у реімбурсаційну програму, але загальнодоступний. "
        "Перевірено 2026-04-27."
    ),
    "bevacizumab": (
        "Оригінальний біологічний препарат у значній мірі OOP; "
        "біосиміляри (Mvasi, Zirabev) дедалі доступніші; покриття НСЗУ "
        "для відібраних показань. Перевірено 2026-04-27."
    ),
    "cetuximab": (
        "Out-of-pocket; селективне покриття НСЗУ для RAS-WT лівобічного "
        "mCRC. Перевірено 2026-04-27."
    ),
    "degarelix": (
        "Зареєстрований; НЕ покривається НСЗУ — лейпролід / госерелін "
        "є стандартом онкопакету для АДТ. Перевірено 2026-04-27."
    ),
    "nab_paclitaxel": (
        "Селективне покриття НСЗУ; для більшості показань — "
        "out-of-pocket. Звичайний паклітаксел є NSZU-default. "
        "Перевірено 2026-04-27."
    ),
}


def find_block_range(lines: list[str], header: str, base_indent: int = 2):
    pat = re.compile(r"^(\s{" + str(base_indent) + r"})" + re.escape(header) + r"\s*:\s*$")
    pat_flow = re.compile(r"^(\s{" + str(base_indent) + r"})" + re.escape(header) + r"\s*:\s*\{")
    start = None
    indent = None
    for i, line in enumerate(lines):
        m = pat.match(line)
        if m:
            start = i
            indent = len(m.group(1))
            break
        m = pat_flow.match(line)
        if m:
            return (i, i + 1, len(m.group(1)), True)
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        line = lines[j]
        if not line.strip():
            continue
        line_indent = len(line) - len(line.lstrip(" "))
        if line_indent <= indent:
            end = j
            break
    return (start, end, indent, False)


def add_indications_block(text: str, indications: list[str]) -> str:
    """Insert reimbursement_indications inside ukraine_registration block.

    Always inserts directly after the `reimbursed_nszu:` line. If a
    `reimbursement_indications: []` already exists empty, replace it.
    """
    lines = text.split("\n")
    # find ukraine_registration block (indent 2)
    rng = find_block_range(lines, "ukraine_registration", base_indent=2)
    if rng is None:
        # try indent 4
        rng = find_block_range(lines, "ukraine_registration", base_indent=4)
    if rng is None:
        return text  # silently skip
    bs, be, indent, is_flow = rng
    if is_flow:
        # Convert flow-style block to block-style first.
        flow_line = lines[bs]
        prefix = " " * indent + "ukraine_registration:"
        # Parse flow content between { and }
        m = re.match(r"^\s*ukraine_registration\s*:\s*\{(.*)\}\s*$", flow_line)
        assert m, flow_line
        inner = m.group(1)
        # Split top-level commas (no nested braces in our data)
        items = [s.strip() for s in inner.split(",") if s.strip()]
        new_block = [prefix]
        inner_indent = " " * (indent + 2)
        for it in items:
            new_block.append(f"{inner_indent}{it}")
        # add reimbursement_indications
        ind_lines = [f"{inner_indent}reimbursement_indications:"]
        for ind in indications:
            ind_lines.append(f'{inner_indent}  - "{ind}"')
        new_block.extend(ind_lines)
        lines[bs:be] = new_block
        return "\n".join(lines)
    # block style
    block = lines[bs:be]
    inner_indent = indent + 2
    inner_pad = " " * inner_indent
    # detect existing empty `reimbursement_indications: []`
    empty_pat = re.compile(r"^\s*reimbursement_indications\s*:\s*\[\s*\]\s*$")
    insert_at = None
    for k, bl in enumerate(block):
        if empty_pat.match(bl):
            insert_at = k
            break
    if insert_at is not None:
        # replace the empty list with block-style list
        new_lines = [f"{inner_pad}reimbursement_indications:"]
        for ind in indications:
            new_lines.append(f'{inner_pad}  - "{ind}"')
        block[insert_at : insert_at + 1] = new_lines
    else:
        # find reimbursed_nszu: line
        rnszu_pat = re.compile(r"^(\s*)reimbursed_nszu\s*:")
        target = None
        for k, bl in enumerate(block):
            if rnszu_pat.match(bl):
                target = k
                break
        if target is None:
            return text
        new_lines = [f"{inner_pad}reimbursement_indications:"]
        for ind in indications:
            new_lines.append(f'{inner_pad}  - "{ind}"')
        block[target + 1 : target + 1] = new_lines
    lines[bs:be + len(block) - (be - bs)] = block  # not needed; replace exactly
    # simpler: just substitute
    new_lines_full = lines[:bs] + block + lines[be:]
    return "\n".join(new_lines_full)


def replace_notes(text: str, new_note: str) -> str:
    """Replace or insert `notes:` line inside ukraine_registration block."""
    lines = text.split("\n")
    rng = find_block_range(lines, "ukraine_registration", base_indent=2)
    if rng is None:
        rng = find_block_range(lines, "ukraine_registration", base_indent=4)
    if rng is None:
        return text
    bs, be, indent, is_flow = rng
    if is_flow:
        return text  # leave flow blocks alone for notes
    block = lines[bs:be]
    inner_pad = " " * (indent + 2)
    notes_pat = re.compile(r"^(\s*)notes\s*:\s*")
    for k, bl in enumerate(block):
        if notes_pat.match(bl):
            # replace single-line notes; if multi-line `>` block, leave alone
            if bl.rstrip().endswith(">"):
                return text  # multi-line — don't touch
            block[k] = f'{inner_pad}notes: "{new_note}"'
            lines[bs:be] = block
            return "\n".join(lines)
    # not found — append
    block.append(f'{inner_pad}notes: "{new_note}"')
    lines[bs:be] = block
    return "\n".join(lines)


def main() -> None:
    updated = 0
    for stem, indications in INDICATIONS.items():
        path = DRUGS_DIR / f"{stem}.yaml"
        if not path.exists():
            print(f"[skip] missing {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        # only if no reimbursement_indications already present (or empty)
        # quick check via regex on the file
        ri_pat = re.compile(r"^\s*reimbursement_indications\s*:\s*$", re.MULTILINE)
        ri_empty_pat = re.compile(r"^\s*reimbursement_indications\s*:\s*\[\s*\]\s*$", re.MULTILINE)
        # Detect a populated indication list (next line is `- ...`)
        already_populated = False
        for m in ri_pat.finditer(text):
            after = text[m.end():m.end() + 200]
            if re.match(r"\s*\n\s*-", after):
                already_populated = True
                break
        if already_populated:
            print(f"[skip-populated] {stem}")
            continue
        new_text = add_indications_block(text, indications)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            updated += 1
            print(f"[ind] {stem} +{len(indications)} indications")
        else:
            print(f"[no-change] {stem}")

    # apply notes overrides
    notes_updated = 0
    for stem, note in NOTES_OVERRIDE.items():
        path = DRUGS_DIR / f"{stem}.yaml"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new_text = replace_notes(text, note)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            notes_updated += 1
            print(f"[notes] {stem}")

    print(f"\nIndications added: {updated}, notes updated: {notes_updated}")


if __name__ == "__main__":
    main()
