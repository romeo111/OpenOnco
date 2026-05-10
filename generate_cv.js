const {
  Document, Packer, Paragraph, TextRun, AlignmentType,
  HeadingLevel, LevelFormat, BorderStyle, ExternalHyperlink
} = require('docx');
const fs = require('fs');

const greenAccent = "1A5C38";
const darkText = "222222";
const mutedText = "555555";

function sectionHeader(text) {
  return new Paragraph({
    spacing: { before: 320, after: 80 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: greenAccent, space: 4 } },
    children: [new TextRun({
      text: text.toUpperCase(),
      bold: true, size: 24, color: greenAccent, font: "Arial",
    })]
  });
}

function jobTitle(title, org, dates) {
  return [
    new Paragraph({
      spacing: { before: 200, after: 40 },
      children: [new TextRun({ text: title, bold: true, size: 22, color: darkText, font: "Arial" })]
    }),
    new Paragraph({
      spacing: { before: 0, after: 80 },
      children: [
        new TextRun({ text: org, italics: true, size: 20, color: mutedText, font: "Arial" }),
        new TextRun({ text: "  |  " + dates, size: 20, color: mutedText, font: "Arial" }),
      ]
    }),
  ];
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text, size: 20, color: darkText, font: "Arial" })]
  });
}

function numbered(text) {
  return new Paragraph({
    numbering: { reference: "numbered", level: 0 },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text, size: 20, color: darkText, font: "Arial" })]
  });
}

function body(text) {
  return new Paragraph({
    spacing: { before: 40, after: 60 },
    children: [new TextRun({ text, size: 20, color: darkText, font: "Arial" })]
  });
}

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 560, hanging: 280 } } }
        }]
      },
      {
        reference: "numbered",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 560, hanging: 280 } } }
        }]
      },
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 20, color: darkText } } },
    characterStyles: [{
      id: "Hyperlink",
      name: "Hyperlink",
      run: { color: "1A5C38", underline: { type: "single" } }
    }]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1200, right: 1200, bottom: 1200, left: 1200 }
      }
    },
    children: [
      // Name
      new Paragraph({
        spacing: { before: 0, after: 60 },
        children: [new TextRun({ text: "Roman Slyvotskyi", bold: true, size: 52, color: greenAccent, font: "Arial" })]
      }),
      // Org
      new Paragraph({
        spacing: { before: 0, after: 40 },
        children: [new TextRun({ text: "Open Onco Info — Ukraine", size: 22, color: mutedText, font: "Arial" })]
      }),
      // Email + site
      new Paragraph({
        spacing: { before: 0, after: 200 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: greenAccent, space: 6 } },
        children: [
          new TextRun({ text: "8054345@gmail.com", size: 20, color: mutedText, font: "Arial" }),
          new TextRun({ text: "     |     ", size: 20, color: mutedText, font: "Arial" }),
          new ExternalHyperlink({
            link: "https://openonco.info",
            children: [new TextRun({ text: "openonco.info", style: "Hyperlink", size: 20, font: "Arial" })]
          }),
        ]
      }),

      // EDUCATION
      sectionHeader("Education"),

      new Paragraph({
        spacing: { before: 160, after: 40 },
        children: [new TextRun({ text: "Master of Law (LL.M.) — Corporate Law & Advocacy", bold: true, size: 21, color: darkText, font: "Arial" })]
      }),
      new Paragraph({
        spacing: { before: 0, after: 40 },
        children: [new TextRun({ text: "National Technical University of Ukraine “Kyiv Polytechnic Institute” (NTUU KPI), 2007", size: 20, color: mutedText, font: "Arial", italics: true })]
      }),
      body("Specialisation: corporate law, contract regulation, intellectual property"),

      new Paragraph({
        spacing: { before: 160, after: 40 },
        children: [new TextRun({ text: "Bachelor — Human Research & Law", bold: true, size: 21, color: darkText, font: "Arial" })]
      }),
      new Paragraph({
        spacing: { before: 0, after: 40 },
        children: [new TextRun({ text: "National Technical University of Ukraine “Kyiv Polytechnic Institute” (NTUU KPI), 2005", size: 20, color: mutedText, font: "Arial", italics: true })]
      }),
      body("Interdisciplinary programme bridging technical sciences and legal frameworks for human-subjects research — directly relevant to clinical trial regulation and research ethics"),

      // PROFESSIONAL EXPERIENCE
      sectionHeader("Professional Experience"),

      ...jobTitle("Founder & Lead Architect — OpenOnco", "Open Onco Info — Ukraine", "2024 – present"),
      body("Free public oncology clinical decision-support platform serving Ukrainian patients and clinicians."),
      body("Key problems resolved:"),
      bullet("Designed a structured, versioned knowledge base: 78 disease entities, 360 regimens, 438 biomarker-actionability records, 251 drugs, 474 clinical red flags, 140 decision algorithms — all source-cited to ESMO, NCCN, PubMed, ClinicalTrials.gov, CIViC."),
      bullet("Built a declarative rule engine (not generative AI) that produces two treatment plans (standard + aggressive) with full citations. LLMs are excluded from clinical decisions by architectural design — a deliberate legal and safety choice."),
      bullet("Implemented a virtual tumour board layer: structured MDT input (oncology, radiology, pathology, surgery) feeding a bilingual (Ukrainian/English) plan-assembly engine."),
      bullet("Selected CIViC (CC0) as the actionability data backbone over OncoKB — a licence-compatibility decision driven by non-commercial public-resource mandate."),
      bullet("Authored the project CHARTER: contributor governance, two-reviewer merge policy for clinical content, CoI declarations, patient data de-identification protocol (consent + ethics approval required before any patient artifact enters public repository)."),
      bullet("Validated plans on a real patient case with clinical review from practising oncologists — received positive evaluation."),
      bullet("Integrated Ukrainian Ministry of Health (MoZ) clinical instructions and standard-of-care protocols as a parallel evidence layer alongside ESMO/NCCN guidelines — enabling the platform to reflect both international best-evidence and locally approved care pathways."),
      bullet("Implemented automated drug availability checking against the Ukrainian State Register of Medicines (NSZU/DLZ), flagging regimen components by local registration status, reimbursement eligibility, and procurement accessibility — ensuring plans are actionable within the Ukrainian healthcare system, not just evidence-correct."),

      ...jobTitle("Advocate & Legal Counsel — Corporate Law", "Private practice, Ukraine", "2007 – 2017 (10 years)"),
      bullet("Contract drafting and dispute resolution in corporate, construction, and technology sectors."),
      bullet("Regulatory compliance and IP protection for technology companies."),
      bullet("Legal structuring of construction and real estate development projects."),

      ...jobTitle("IT Project Manager", "Various organisations", "2015 – present (parallel track)"),
      bullet("Managed software development lifecycles, vendor contracts, and technical teams."),
      bullet("Specialised in defence-technology software products: requirements engineering, procurement compliance, dual-use technology regulation."),

      ...jobTitle("Energy-Efficient Building Expertise", "Independent practice", "2010 – present"),
      bullet("Applied building physics and passive house standards to residential and commercial projects."),
      bullet("Expertise in thermal envelope design, energy audit methodology, and materials specification — background that informs systems-thinking approach applied to clinical protocol design."),

      // SELF-DIRECTED SCIENTIFIC LEARNING
      sectionHeader("Self-Directed Scientific Learning"),

      ...jobTitle("Genomic Data Interpretation — Personal Research", "23andMe platform analysis", "~2014–2015 (10+ years ago)"),
      bullet("Early adopter of direct-to-consumer whole-genome genotyping; independently analysed raw variant data against published GWAS studies, pharmacogenomics literature, and cancer-risk loci."),
      bullet("This experience motivated a decade of self-study in molecular oncology, biomarker science, and precision medicine — forming the scientific foundation for the OpenOnco knowledge base design."),

      // LANGUAGES
      sectionHeader("Languages"),
      new Paragraph({
        spacing: { before: 120, after: 40 },
        children: [
          new TextRun({ text: "Ukrainian", bold: true, size: 20, font: "Arial", color: darkText }),
          new TextRun({ text: " — native     ", size: 20, font: "Arial", color: mutedText }),
          new TextRun({ text: "Russian", bold: true, size: 20, font: "Arial", color: darkText }),
          new TextRun({ text: " — native     ", size: 20, font: "Arial", color: mutedText }),
          new TextRun({ text: "English", bold: true, size: 20, font: "Arial", color: darkText }),
          new TextRun({ text: " — professional working proficiency (technical and legal)", size: 20, font: "Arial", color: mutedText }),
        ]
      }),

      // RELEVANCE TO ESMO MEMBERSHIP
      sectionHeader("Relevance to ESMO Membership"),
      body("My background uniquely combines:"),
      numbered("Legal expertise to navigate source licensing, research ethics, and clinical tool liability frameworks"),
      numbered("Technical depth to architect compliant, rule-based (non-hallucinating) clinical decision support"),
      numbered("Direct patient impact — validated output reviewed positively by practising oncologists in Ukraine"),
      new Paragraph({
        spacing: { before: 120, after: 40 },
        children: [new TextRun({
          text: "ESMO guidelines are the primary evidence backbone for OpenOnco. Membership would enable proper licence-tier citation of ESMO Clinical Practice Guidelines and open pathways for clinical validation partnerships within the European oncology network.",
          size: 20, color: darkText, font: "Arial"
        })]
      }),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("Roman_Slyvotskyi_CV_ESMO.docx", buffer);
  console.log("Done: Roman_Slyvotskyi_CV_ESMO.docx");
});
