import { mkdirSync, writeFileSync } from "node:fs";
import {
  Presentation,
  PresentationFile,
  row,
  column,
  grid,
  layers,
  panel,
  text,
  shape,
  rule,
  fill,
  fixed,
  hug,
  wrap,
  fr,
} from "@oai/artifact-tool";

const OUT_DIR = "C:/Users/805/cancer-autoresearch/out/openonco_competitors_uk";
const PREVIEW_DIR = `${OUT_DIR}/previews`;
const LAYOUT_DIR = `${OUT_DIR}/layouts`;
const PPTX_PATH = `${OUT_DIR}/openonco_competitors_uk.pptx`;

mkdirSync(PREVIEW_DIR, { recursive: true });
mkdirSync(LAYOUT_DIR, { recursive: true });

const W = 1920;
const H = 1080;
const FONT = "Segoe UI";
const SERIF = "Georgia";

const C = {
  ink: "#171717",
  paper: "#F7F4ED",
  paper2: "#EFE8DC",
  muted: "#625C54",
  quiet: "#8A8177",
  line: "#D8CFC2",
  teal: "#0B6B6B",
  teal2: "#D9EFEC",
  coral: "#E24A3B",
  coral2: "#F7D8D1",
  violet: "#5651A7",
  violet2: "#E2E0F5",
  gold: "#B7852D",
  gold2: "#F2E3C4",
  green: "#287A4E",
  green2: "#DCECE2",
  white: "#FFFFFF",
};

const pres = Presentation.create({
  slideSize: { width: W, height: H },
});

function tx(value, {
  name,
  size = 28,
  color = C.ink,
  bold = false,
  typeface = FONT,
  width = fill,
  height = hug,
  align,
  columnSpan,
  rowSpan,
} = {}) {
  return text(value, {
    name,
    width,
    height,
    columnSpan,
    rowSpan,
    style: {
      fontSize: size,
      color,
      bold,
      typeface,
      ...(align ? { alignment: align } : {}),
    },
  });
}

function bg(fillColor = C.paper) {
  return shape({
    name: "slide-bg",
    width: fill,
    height: fill,
    fill: fillColor,
    line: { style: "solid", width: 0, fill: fillColor },
  });
}

function compose(slide, content, fillColor = C.paper) {
  slide.compose(
    layers({ name: "slide-layers", width: fill, height: fill }, [
      bg(fillColor),
      content,
    ]),
    { frame: { left: 0, top: 0, width: W, height: H }, baseUnit: 8 },
  );
}

function titleBlock(kicker, title, subtitle, color = C.ink) {
  return column({ name: "title-block", width: fill, height: hug, gap: 16 }, [
    tx(kicker, {
      name: "kicker",
      size: 18,
      color: color === C.ink ? C.teal : C.teal2,
      bold: true,
      width: wrap(1100),
    }),
    tx(title, {
      name: "slide-title",
      size: 54,
      color,
      bold: true,
      width: wrap(1480),
    }),
    subtitle
      ? tx(subtitle, {
          name: "slide-subtitle",
          size: 26,
          color: color === C.ink ? C.muted : "#E7DED1",
          width: wrap(1320),
        })
      : null,
  ].filter(Boolean));
}

function sourceLine(value, dark = false) {
  return tx(value, {
    name: "source",
    size: 13,
    color: dark ? "#C8C0B4" : C.quiet,
    width: fill,
  });
}

function chip(label, color, fillColor, chipWidth = 150) {
  return panel(
    {
      name: `chip-${label}`,
      width: fixed(chipWidth),
      height: hug,
      padding: { x: 16, y: 8 },
      fill: fillColor,
      line: { style: "solid", width: 1, fill: fillColor },
      borderRadius: "rounded-full",
    },
    tx(label, {
      size: 17,
      color,
      bold: true,
      width: fill,
      align: "center",
    }),
  );
}

function divider(color = C.line) {
  return rule({ name: "divider", width: fill, weight: 2, stroke: color });
}

function openMetric(number, label, accent = C.coral) {
  return column({ name: `metric-${label}`, width: fill, height: hug, gap: 8 }, [
    tx(number, {
      name: `metric-number-${label}`,
      size: 82,
      bold: true,
      color: accent,
      width: fill,
      typeface: SERIF,
    }),
    tx(label, {
      name: `metric-label-${label}`,
      size: 23,
      color: C.muted,
      width: wrap(420),
    }),
  ]);
}

function bar(label, value, color, note) {
  const full = 820;
  const w = Math.round((value / 5) * full);
  return grid(
    {
      name: `bar-row-${label}`,
      width: fill,
      height: fixed(70),
      columns: [fixed(300), fixed(full), fr(1)],
      columnGap: 28,
      alignItems: "center",
    },
    [
      tx(label, { name: `bar-label-${label}`, size: 24, bold: true, width: fill }),
      layers({ name: `bar-track-${label}`, width: fixed(full), height: fixed(22) }, [
        shape({
          name: `bar-bg-${label}`,
          width: fixed(full),
          height: fixed(22),
          fill: C.paper2,
          line: { style: "solid", width: 0, fill: C.paper2 },
          borderRadius: "rounded-full",
        }),
        shape({
          name: `bar-fill-${label}`,
          width: fixed(w),
          height: fixed(22),
          fill: color,
          line: { style: "solid", width: 0, fill: color },
          borderRadius: "rounded-full",
        }),
      ]),
      tx(note, { name: `bar-note-${label}`, size: 20, color: C.muted, width: fill }),
    ],
  );
}

function tableRow(cells, options = {}) {
  const {
    name = "table-row",
    header = false,
    fillColor = "transparent",
    color = C.ink,
    heights = 78,
    columns = [fixed(250), fixed(420), fixed(420), fr(1)],
  } = options;
  return panel(
    {
      name,
      width: fill,
      height: fixed(heights),
      padding: { x: 20, y: 10 },
      fill: fillColor,
      line: { style: "solid", width: 0, fill: fillColor },
      borderRadius: header ? "rounded-lg" : "rounded-sm",
    },
    grid(
      {
        name: `${name}-grid`,
        width: fill,
        height: fill,
        columns,
        columnGap: 26,
        alignItems: "center",
      },
      cells.map((cell, idx) =>
        tx(cell, {
          name: `${name}-cell-${idx}`,
          size: header ? 18 : 19,
          color: header ? C.white : color,
          bold: header || idx === 0,
          width: fill,
        }),
      ),
    ),
  );
}

function slide1() {
  const slide = pres.slides.add();
  compose(
    slide,
    layers({ name: "cover", width: fill, height: fill }, [
      shape({
        name: "cover-left-band",
        width: fixed(300),
        height: fill,
        fill: C.teal,
        line: { style: "solid", width: 0, fill: C.teal },
      }),
      shape({
        name: "cover-coral-slab",
        width: fixed(22),
        height: fill,
        fill: C.coral,
        line: { style: "solid", width: 0, fill: C.coral },
      }),
      column(
        {
          name: "cover-content",
          width: fill,
          height: fill,
          padding: { left: 390, right: 110, top: 110, bottom: 82 },
          gap: 34,
          justify: "center",
        },
        [
          tx("КОНКУРЕНТНИЙ ЛАНДШАФТ", {
            name: "cover-kicker",
            size: 20,
            bold: true,
            color: C.gold2,
            width: fill,
          }),
          tx("OpenOnco", {
            name: "cover-title",
            size: 108,
            color: C.white,
            bold: true,
            typeface: SERIF,
            width: fill,
          }),
          tx("дефенсивна ніша відкритої, перевірної онко-CDS інфраструктури", {
            name: "cover-subtitle",
            size: 36,
            color: "#E9E1D6",
            width: wrap(1080),
          }),
          rule({ name: "cover-rule", width: fixed(420), weight: 5, stroke: C.coral }),
          tx("Українська презентація для стратегії продукту, партнерств і фандрейзингу", {
            name: "cover-context",
            size: 24,
            color: "#BFB7AB",
            width: wrap(1000),
          }),
        ],
      ),
    ]),
    C.ink,
  );
}

function slide2() {
  const slide = pres.slides.add();
  compose(
    slide,
    column(
      {
        name: "s2-root",
        width: fill,
        height: fill,
        padding: { x: 96, y: 72 },
        gap: 56,
      },
      [
        titleBlock(
          "1 / ВИСНОВОК",
          "OpenOnco не має вигравати в усіх «онко-АІ». Йому треба зайняти вузьку довірчу нішу.",
          "Конкуренти сильні в EHR, оплаті, workflow і даних. OpenOnco сильний там, де потрібні прозорі правила, джерела і локальний контекст.",
        ),
        grid(
          {
            name: "s2-metrics",
            width: fill,
            height: hug,
            columns: [fr(1), fr(1), fr(1)],
            columnGap: 56,
          },
          [
            openMetric("відкритість", "код, логіка і контент можна інспектувати", C.teal),
            openMetric("цитати", "кожне твердження прив’язане до джерела", C.coral),
            openMetric("локальність", "браузер-local + контекст доступності препаратів", C.violet),
          ],
        ),
        panel(
          {
            name: "s2-bottom-claim",
            width: fill,
            height: hug,
            padding: { x: 34, y: 28 },
            fill: C.paper2,
            line: { style: "solid", width: 0, fill: C.paper2 },
            borderRadius: "rounded-lg",
          },
          tx("Рекомендована позиція: «аудитований генератор чернетки tumor-board плану», а не «чатбот, що призначає лікування».", {
            name: "s2-bottom-text",
            size: 30,
            bold: true,
            color: C.ink,
            width: fill,
          }),
        ),
        sourceLine("Локальна база: README OpenOnco, CHARTER §15, аналіз конкурентів станом на 2026-04-29."),
      ],
    ),
  );
}

function slide3() {
  const slide = pres.slides.add();
  const layersData = [
    ["AI-копілоти", "Tempus One, OncoIA", C.violet, "натуральна мова + EHR / RAG"],
    ["Workflow tumor board", "OncoLens, NAVIFY", C.teal, "координація MDT, кейси, trial awareness"],
    ["Pathways / CDS", "Flatiron Assist, ClinicalPath, Eviti", C.coral, "вибір режиму, prior auth, аналітика"],
    ["Trial matching", "MatchMiner, Massive Bio, GenomOncology", C.gold, "пацієнт ↔ критерії досліджень"],
    ["Evidence KB", "CIViC, OncoKB, JAX-CKB", C.green, "варіанти, біомаркери, рівні доказів"],
  ];
  compose(
    slide,
    column(
      {
        name: "s3-root",
        width: fill,
        height: fill,
        padding: { x: 90, y: 52 },
        gap: 24,
      },
      [
        titleBlock(
          "2 / КАРТА РИНКУ",
          "Ринок складається з п’яти шарів. OpenOnco перетинає їх, але не замінює кожен.",
          "Найкраща стратегія — не фронтальна атака, а інтеграція з джерелами і чітка власна роль: плановий артефакт для перевірки лікарем.",
        ),
        grid(
          {
            name: "s3-map",
            width: fill,
            height: fixed(545),
            columns: [fixed(520), fr(1)],
            columnGap: 58,
          },
          [
            column(
              { name: "s3-left", width: fill, height: fill, gap: 18 },
              layersData.map(([layer, examples, color, note], idx) =>
                row(
                  {
                    name: `layer-row-${idx}`,
                    width: fill,
                    height: fixed(92),
                    gap: 20,
                    align: "center",
                  },
                  [
                    shape({
                      name: `layer-dot-${idx}`,
                      width: fixed(18),
                      height: fixed(64),
                      fill: color,
                      line: { style: "solid", width: 0, fill: color },
                      borderRadius: "rounded-full",
                    }),
                    column({ name: `layer-copy-${idx}`, width: fill, height: fill, gap: 3, justify: "center" }, [
                      tx(layer, { size: 26, bold: true, color: C.ink, width: fill }),
                      tx(examples, { size: 19, color: C.muted, width: fill }),
                      tx(note, { size: 15, color: C.quiet, width: fill }),
                    ]),
                  ],
                ),
              ),
            ),
            panel(
              {
                name: "s3-openonco-field",
                width: fill,
                height: fill,
                padding: { x: 46, y: 38 },
                fill: C.ink,
                line: { style: "solid", width: 0, fill: C.ink },
                borderRadius: "rounded-lg",
              },
              column({ name: "s3-field-copy", width: fill, height: fill, gap: 22, justify: "center" }, [
                row({ width: fill, height: hug, gap: 14 }, [
                  chip("OpenOnco", C.ink, C.gold2, 142),
                  chip("open-source", C.teal, C.teal2, 164),
                  chip("CDS artifact", C.coral, C.coral2, 174),
                ]),
                tx("Не база варіантів. Не EHR. Не сервіс prior auth. Не autonomous AI.", {
                  size: 32,
                  bold: true,
                  color: C.white,
                  width: wrap(760),
                }),
                tx("Це шар, який збирає докази, правила, red flags і локальні обмеження у чернетку плану для tumor-board перевірки.", {
                  size: 27,
                  color: "#E9E1D6",
                  width: wrap(780),
                }),
              ]),
            ),
          ],
        ),
        sourceLine("Джерела: Flatiron, Elsevier ClinicalPath, OncoLens, NAVIFY, Tempus, GenomOncology, MatchMiner, CIViC, OncoKB."),
      ],
    ),
  );
}

function slide4() {
  const slide = pres.slides.add();
  const rows = [
    ["Flatiron Assist", "EHR-integrated pathways, NCCN, prior auth", "глибина workflow і OncoEMR/Epic", "вразливість: закритість, vendor lock-in"],
    ["ClinicalPath", "pathways + analytics + trials", "15+ років, EHR, payer/ops аналітика", "OpenOnco має вигравати прозорістю"],
    ["Eviti Advisor", "режими, доказ, outcomes, costs, toxicities", "payer-first decision support", "не повторювати payer framing"],
    ["OncoLens", "MDT workflow + AI extraction + trials", "мережа центрів, tumor-board операції", "OpenOnco не logistics, а plan logic"],
    ["Tempus One", "GenAI assistant + EHR + ASCO + trials", "data moat, multimodal, agents", "позиція OpenOnco: white-box rules"],
    ["GenomOncology", "molecular reporting + trial optimization", "biomarker depth, real-time trial alerts", "OpenOnco ширший за molecular-only"],
  ];
  compose(
    slide,
    column(
      {
        name: "s4-root",
        width: fill,
        height: fill,
        padding: { x: 78, y: 60 },
        gap: 24,
      },
      [
        titleBlock(
          "3 / ПРЯМІ КОНКУРЕНТИ",
          "Найближча комерційна загроза — не чатботи, а pathway/CDS + workflow платформи.",
          "Вони вже сидять у клінічному потоці. OpenOnco має компенсувати відсутність EHR-дистрибуції довірою, відкритістю і локальним контекстом.",
        ),
        column({ name: "s4-table", width: fill, height: hug, gap: 7 }, [
          tableRow(["Гравець", "Що продає", "Сила", "Контрпозиція OpenOnco"], {
            name: "s4-header",
            header: true,
            fillColor: C.teal,
            heights: 58,
          }),
          ...rows.map((r, idx) =>
            tableRow(r, {
              name: `s4-row-${idx}`,
              fillColor: idx % 2 === 0 ? C.white : C.paper2,
              heights: 78,
            }),
          ),
        ]),
        sourceLine("Офіційні сторінки продуктів: Flatiron Assist, Elsevier ClinicalPath, Eviti Advisor, OncoLens, Tempus One, GenomOncology."),
      ],
    ),
  );
}

function slide5() {
  const slide = pres.slides.add();
  compose(
    slide,
    column(
      {
        name: "s5-root",
        width: fill,
        height: fill,
        padding: { x: 92, y: 68 },
        gap: 42,
      },
      [
        titleBlock(
          "4 / РАНЖУВАННЯ ЗАГРОЗ",
          "Найвищий ризик там, де конкурент уже вбудований у клінічну дію.",
          "Оцінка якісна: сила дистрибуції, близькість до плану лікування, регуляторна довіра, дані та switching cost.",
        ),
        column({ name: "s5-bars", width: fill, height: hug, gap: 18 }, [
          bar("Flatiron / ClinicalPath", 5, C.coral, "pathway + EHR + prior authorization"),
          bar("OncoLens / NAVIFY", 4, C.teal, "MDT workflow і кейс-менеджмент"),
          bar("Tempus / GenomOncology", 4, C.violet, "молекулярні дані, trial matching, AI assistants"),
          bar("MatchMiner / Massive Bio", 3, C.gold, "trial matching як окрема цінність"),
          bar("CIViC / OncoKB / JAX-CKB", 2, C.green, "радше evidence layer, ніж повний plan engine"),
        ]),
        row({ name: "s5-takeaway", width: fill, height: hug, gap: 22, align: "center" }, [
          shape({
            name: "s5-takeaway-mark",
            width: fixed(12),
            height: fixed(92),
            fill: C.coral,
            line: { style: "solid", width: 0, fill: C.coral },
          }),
          tx("Висновок: OpenOnco має швидко наростити trust proof — coverage, sign-off, validation — бо саме це замінює enterprise-дистрибуцію на ранньому етапі.", {
            name: "s5-takeaway-text",
            size: 29,
            bold: true,
            color: C.ink,
            width: wrap(1480),
          }),
        ]),
        sourceLine("Оцінка автора на основі публічних матеріалів конкурентів і поточного README OpenOnco."),
      ],
    ),
  );
}

function slide6() {
  const slide = pres.slides.add();
  compose(
    slide,
    column(
      {
        name: "s6-root",
        width: fill,
        height: fill,
        padding: { x: 86, y: 66 },
        gap: 34,
      },
      [
        titleBlock(
          "5 / PATHWAY-CDS",
          "Flatiron, ClinicalPath і Eviti продають контроль рішення в точці замовлення.",
          "Це найближча категорія до OpenOnco за клінічною функцією.",
        ),
        grid(
          {
            name: "s6-body",
            width: fill,
            height: fixed(520),
            columns: [fr(1), fr(1)],
            columnGap: 70,
          },
          [
            column({ name: "s6-left", width: fill, height: fill, gap: 24 }, [
              tx("Що в них сильне", { size: 30, bold: true, color: C.coral }),
              tx("• інтеграція в EHR / ordering\n• NCCN / guideline content\n• prior authorization і payer reporting\n• аналітика concordance / variation\n• adoption у великих практиках", {
                size: 28,
                color: C.ink,
                width: wrap(760),
              }),
            ]),
            column({ name: "s6-right", width: fill, height: fill, gap: 24 }, [
              tx("Де OpenOnco може бити", { size: 30, bold: true, color: C.teal }),
              tx("• повна інспекція правил і джерел\n• альтернативні треки поруч, не один answer\n• локальні бейджі доступності / NSZU\n• no-PHI браузерний режим\n• відкритий контриб’юторський контур", {
                size: 28,
                color: C.ink,
                width: wrap(760),
              }),
            ]),
          ],
        ),
        sourceLine("Джерела: Flatiron Assist, Elsevier ClinicalPath, Eviti Advisor.", false),
      ],
    ),
  );
}

function slide7() {
  const slide = pres.slides.add();
  compose(
    slide,
    column(
      {
        name: "s7-root",
        width: fill,
        height: fill,
        padding: { x: 90, y: 52 },
        gap: 28,
      },
      [
        titleBlock(
          "6 / WORKFLOW ТА AI-КОПІЛОТИ",
          "OncoLens, NAVIFY, Tempus і GenomOncology виграють не лише якістю рекомендацій, а місцем у роботі команди.",
          "OpenOnco має не імітувати їхній enterprise стек, а стати легким «reasoning artifact» поруч із ним.",
        ),
        grid(
          {
            name: "s7-grid",
            width: fill,
            height: fixed(500),
            columns: [fr(1), fr(1), fr(1)],
            columnGap: 36,
          },
          [
            panel(
              {
                name: "s7-oncolens",
                width: fill,
                height: fill,
                padding: { x: 30, y: 30 },
                fill: C.teal2,
                line: { style: "solid", width: 0, fill: C.teal2 },
                borderRadius: "rounded-lg",
              },
              column({ width: fill, height: fill, gap: 20 }, [
                tx("OncoLens / NAVIFY", { size: 30, bold: true, color: C.teal }),
                tx("Сила: MDT workflow, кейси, колаборація, trial awareness.", { size: 25, color: C.ink }),
                divider("#B8DCD6"),
                tx("OpenOnco response: експортований plan artifact для обговорення, а не заміна board workflow.", { size: 24, color: C.muted }),
              ]),
            ),
            panel(
              {
                name: "s7-tempus",
                width: fill,
                height: fill,
                padding: { x: 30, y: 30 },
                fill: C.violet2,
                line: { style: "solid", width: 0, fill: C.violet2 },
                borderRadius: "rounded-lg",
              },
              column({ width: fill, height: fill, gap: 20 }, [
                tx("Tempus One", { size: 30, bold: true, color: C.violet }),
                tx("Сила: multimodal data, EHR queries, ASCO guidelines, agents.", { size: 25, color: C.ink }),
                divider("#C6C1EC"),
                tx("OpenOnco response: rules-first, source-first, visible limitations instead of black-box copilot.", { size: 24, color: C.muted }),
              ]),
            ),
            panel(
              {
                name: "s7-go",
                width: fill,
                height: fill,
                padding: { x: 30, y: 30 },
                fill: C.gold2,
                line: { style: "solid", width: 0, fill: C.gold2 },
                borderRadius: "rounded-lg",
              },
              column({ width: fill, height: fill, gap: 20 }, [
                tx("GenomOncology", { size: 30, bold: true, color: C.gold }),
                tx("Сила: biomarker logic, molecular tumor board, trial optimization.", { size: 25, color: C.ink }),
                divider("#E2C987"),
                tx("OpenOnco response: поєднати molecular actionability із повним клінічним планом.", { size: 24, color: C.muted }),
              ]),
            ),
          ],
        ),
        sourceLine("Джерела: OncoLens, NAVIFY Tumor Board, Tempus One, GenomOncology."),
      ],
    ),
  );
}

function slide8() {
  const slide = pres.slides.add();
  compose(
    slide,
    column(
      {
        name: "s8-root",
        width: fill,
        height: fill,
        padding: { x: 88, y: 52 },
        gap: 26,
      },
      [
        titleBlock(
          "7 / OPEN-SOURCE ТА EVIDENCE LAYER",
          "CIViC і MatchMiner — найкращі кандидати на партнерство, не вороги.",
          "OpenOnco має брати структуровані докази й матчинг, а зверху будувати plan reasoning, safety gates і локальний контекст.",
        ),
        grid(
          {
            name: "s8-grid",
            width: fill,
            height: fixed(560),
            columns: [fr(1), fr(1)],
            rows: [fr(1), fr(1)],
            columnGap: 38,
            rowGap: 32,
          },
          [
            panel({ width: fill, height: fill, padding: 30, fill: C.green2, line: { style: "solid", width: 0, fill: C.green2 }, borderRadius: "rounded-lg" },
              column({ width: fill, height: fill, gap: 16 }, [
                tx("CIViC", { size: 32, bold: true, color: C.green }),
                tx("Відкрита база інтерпретації варіантів: публічний контент, provenance, expert moderation.", { size: 25, color: C.ink }),
                tx("Для OpenOnco: primary actionability substrate.", { size: 22, bold: true, color: C.muted }),
              ])),
            panel({ width: fill, height: fill, padding: 30, fill: C.paper2, line: { style: "solid", width: 0, fill: C.paper2 }, borderRadius: "rounded-lg" },
              column({ width: fill, height: fill, gap: 16 }, [
                tx("OncoKB / JAX-CKB", { size: 32, bold: true, color: C.ink }),
                tx("Сильні curated KB для biomarker interpretation; OncoKB має FDA recognition subset.", { size: 25, color: C.ink }),
                tx("Для OpenOnco: порівняння покриття, але ліцензійні межі важливі.", { size: 22, bold: true, color: C.muted }),
              ])),
            panel({ width: fill, height: fill, padding: 30, fill: C.teal2, line: { style: "solid", width: 0, fill: C.teal2 }, borderRadius: "rounded-lg" },
              column({ width: fill, height: fill, gap: 16 }, [
                tx("MatchMiner", { size: 32, bold: true, color: C.teal }),
                tx("Open-source trial matching від DFCI; CTML структурує clinical/genomic eligibility.", { size: 25, color: C.ink }),
                tx("Для OpenOnco: інтегрувати trial layer, не будувати все заново.", { size: 22, bold: true, color: C.muted }),
              ])),
            panel({ width: fill, height: fill, padding: 30, fill: C.coral2, line: { style: "solid", width: 0, fill: C.coral2 }, borderRadius: "rounded-lg" },
              column({ width: fill, height: fill, gap: 16 }, [
                tx("Massive Bio", { size: 32, bold: true, color: C.coral }),
                tx("Пацієнт- і sponsor-facing trial matching з масштабною базою досліджень.", { size: 25, color: C.ink }),
                tx("Для OpenOnco: trial awareness має бути частиною плану, не основним продуктом.", { size: 22, bold: true, color: C.muted }),
              ])),
          ],
        ),
        sourceLine("Джерела: CIViCdb 2022, OncoKB FAQ, JAX-CKB npj Precision Oncology, MatchMiner, Massive Bio."),
      ],
    ),
  );
}

function slide9() {
  const slide = pres.slides.add();
  compose(
    slide,
    grid(
      {
        name: "s9-root",
        width: fill,
        height: fill,
        padding: { x: 92, y: 70 },
        columns: [fr(1)],
        rows: [fixed(314), fr(1), fixed(28)],
        rowGap: 28,
      },
      [
        titleBlock(
          "8 / ДЕФЕНСИВНА НІША",
          "OpenOnco має продавати не «рекомендацію», а перевірний клінічний артефакт.",
          "Це важлива різниця для довіри, регуляторного позиціонування і adoption серед клініцистів.",
        ),
        grid(
          {
            name: "s9-wedge",
            width: fill,
            height: fill,
            columns: [fr(1.1), fr(1)],
            columnGap: 70,
          },
          [
            column({ name: "s9-left", width: fill, height: fill, gap: 24, justify: "center" }, [
              tx("Формула позиціонування", { size: 28, bold: true, color: C.teal }),
              tx("відкриті правила\n+ джерела\n+ safety gates\n+ локальна доступність\n= чернетка плану для MDT", {
                size: 48,
                bold: true,
                color: C.ink,
                typeface: SERIF,
                width: wrap(780),
              }),
            ]),
            column({ name: "s9-right", width: fill, height: fill, gap: 20, justify: "center" }, [
              row({ width: fill, height: hug, gap: 18, align: "center" }, [
                shape({ width: fixed(18), height: fixed(72), fill: C.coral, line: { style: "solid", width: 0, fill: C.coral } }),
                tx("дві альтернативи поруч, щоб зменшити automation bias", { size: 29, color: C.ink, width: fill }),
              ]),
              row({ width: fill, height: hug, gap: 18, align: "center" }, [
                shape({ width: fixed(18), height: fixed(72), fill: C.teal, line: { style: "solid", width: 0, fill: C.teal } }),
                tx("кожен план має rationale, red flags, contraindications і «що не робити»", { size: 29, color: C.ink, width: fill }),
              ]),
              row({ width: fill, height: hug, gap: 18, align: "center" }, [
                shape({ width: fixed(18), height: fixed(72), fill: C.violet, line: { style: "solid", width: 0, fill: C.violet } }),
                tx("STUB / sign-off статус робить незавершеність видимою, а не прихованою", { size: 29, color: C.ink, width: fill }),
              ]),
            ]),
          ],
        ),
        sourceLine("Локальні джерела: README OpenOnco — two-track plan generator, Pyodide browser demo, sign-off infrastructure, CIViC/ESCAT/NSZU badges."),
      ],
    ),
  );
}

function slide10() {
  const slide = pres.slides.add();
  const rows = [
    ["1", "Sign-off coverage", "найбільший trust gap: 15 / 202 одиниць із ≥2 sign-offs", "публічний backlog + клінічні co-leads"],
    ["2", "Validation metrics", "конкуренти продають concordance, adoption, час і denials", "reference cases + concordance audit"],
    ["3", "Interoperability", "без EHR/FHIR імпорт лишається ручним", "FHIR / OMOP / JSON профілі"],
    ["4", "Trials layer", "trial matching окремо вже добре вирішує MatchMiner", "інтеграція CTML / ClinicalTrials.gov"],
    ["5", "Позиціонування", "ризик виглядати як treatment chatbot", "мовити: audited tumor-board draft"],
  ];
  compose(
    slide,
    column(
      {
        name: "s10-root",
        width: fill,
        height: fill,
        padding: { x: 78, y: 60 },
        gap: 24,
      },
      [
        titleBlock(
          "9 / ЩО РОБИТИ ДАЛІ",
          "План на 90 днів: підвищити довіру швидше, ніж конкуренти зможуть копіювати відкритість.",
          "Не треба будувати повний enterprise suite. Фокус: довести, що OpenOnco дає кращий перевірний plan artifact.",
        ),
        column({ name: "s10-table", width: fill, height: hug, gap: 7 }, [
          tableRow(["#", "Напрям", "Чому критично", "Наступна дія"], {
            name: "s10-header",
            header: true,
            fillColor: C.coral,
            heights: 58,
            columns: [fixed(70), fixed(330), fixed(720), fr(1)],
          }),
          ...rows.map((r, idx) =>
            tableRow(r, {
              name: `s10-row-${idx}`,
              fillColor: idx % 2 === 0 ? C.white : C.paper2,
              heights: 82,
              columns: [fixed(70), fixed(330), fixed(720), fr(1)],
            }),
          ),
        ]),
        sourceLine("Локальні джерела: README OpenOnco; конкурентні claims — офіційні сторінки продуктів."),
      ],
    ),
  );
}

function slide11() {
  const slide = pres.slides.add();
  const sources = [
    ["OpenOnco", "README.md, CHARTER.md — локальне позиціонування, sign-off, Pyodide, non-device CDS"],
    ["Flatiron Assist", "flatiron.com/oncology/clinical-decision-support — NCCN, EHR, prior auth, trials"],
    ["ClinicalPath", "elsevier.com/products/clinicalpath — pathways, EHR, analytics, trial prioritization"],
    ["OncoLens", "oncolens.com — MDT platform, AI extraction, research network"],
    ["NAVIFY", "usinfo.roche.com/SimplifyOncology.html — tumor board, trial/guideline apps"],
    ["Tempus One", "investors.tempus.com — EHR integration, ASCO guidelines, agents, trial matching"],
    ["GenomOncology", "genomoncology.com — precision oncology platform, trial optimization"],
    ["CIViC / OncoKB / JAX-CKB", "CIViCdb 2022; OncoKB FAQ; JAX-CKB npj Precision Oncology"],
    ["MatchMiner / Massive Bio / Eviti", "matchminer.org; massivebio.com; connect.eviti.com/evitiAdvisor"],
  ];
  compose(
    slide,
    column(
      {
        name: "s11-root",
        width: fill,
        height: fill,
        padding: { x: 86, y: 52 },
        gap: 20,
      },
      [
        titleBlock(
          "10 / ДЖЕРЕЛА",
          "Джерела використані як доказ конкурентного позиціонування, не як клінічні рекомендації.",
          "Дату перевірки треба оновлювати перед зовнішнім використанням.",
        ),
        column(
          { name: "s11-source-list", width: fill, height: hug, gap: 10 },
          sources.map((s, idx) =>
            grid(
              {
                name: `source-row-${idx}`,
                width: fill,
                height: fixed(56),
                columns: [fixed(320), fr(1)],
                columnGap: 24,
                alignItems: "center",
              },
              [
                tx(s[0], { size: 21, bold: true, color: C.ink, width: fill }),
                tx(s[1], { size: 18, color: C.muted, width: fill }),
              ],
            ),
          ),
        ),
        sourceLine("Підготовлено для OpenOnco конкурентного аналізу українською мовою."),
      ],
    ),
  );
}

[
  slide1,
  slide2,
  slide3,
  slide4,
  slide5,
  slide6,
  slide7,
  slide8,
  slide9,
  slide10,
  slide11,
].forEach((fn) => fn());

const pptx = await PresentationFile.exportPptx(pres);
await pptx.save(PPTX_PATH);

const previewPaths = [];
const layoutPaths = [];
for (let i = 0; i < pres.slides.count; i += 1) {
  const slide = pres.slides.getItem(i);
  const n = String(i + 1).padStart(2, "0");
  const pngPath = `${PREVIEW_DIR}/slide_${n}.png`;
  const layoutPath = `${LAYOUT_DIR}/slide_${n}.layout.json`;
  const png = await slide.export({ format: "png" });
  writeFileSync(pngPath, Buffer.from(await png.arrayBuffer()));
  const layout = await slide.export({ format: "layout" });
  writeFileSync(layoutPath, JSON.stringify(layout, null, 2), "utf8");
  previewPaths.push(pngPath);
  layoutPaths.push(layoutPath);
}

writeFileSync(
  `${OUT_DIR}/manifest.json`,
  JSON.stringify(
    {
      pptx: PPTX_PATH,
      previews: previewPaths,
      layouts: layoutPaths,
      generatedAt: new Date().toISOString(),
    },
    null,
    2,
  ),
  "utf8",
);

console.log(JSON.stringify({ pptx: PPTX_PATH, previews: previewPaths.length, layouts: layoutPaths.length }, null, 2));
