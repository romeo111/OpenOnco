# Explainer backlog — verified claims awaiting write-up

Fifteen explainer topics were proposed for the news section and fact-checked
against primary literature before any were written. **Not one was publishable
as proposed.** The corrections below are the output of that check; use them
rather than the original phrasing.

Two have been written (marked ✅). The rest are ready to draft — the research
is done, the sources are here.

See `news-editorial-plan.md` for the format rules: `kind: explainer` makes
`sources:` mandatory, and the build fails without it.

## Verdict summary

| # | Topic | Verdict | Status |
|---|---|---|---|
| 1 | Cancer as an atavism — ancient genes switching back on | Contested Hypothesis | unwritten |
| 2 | Genome chaos — cells shattering their own chromosomes under stress | Contested Hypothesis | unwritten |
| 3 | Tumours suppressing their own mismatch repair under drug pressure | Contested Hypothesis | unwritten |
| 4 | Transmissible cancers, and the 11,000-year-old dog lineage | Mostly Right Numbers Off | unwritten |
| 5 | Driver mutations in normal skin | Mostly Right Numbers Off | ✅ `cancer-mutations-in-normal-skin` |
| 6 | What NCCN category 2A actually means | Mostly Right Numbers Off | ✅ `what-nccn-2a-actually-means` |
| 7 | Anyone can submit evidence to NCCN | Mostly Right Numbers Off | unwritten |
| 8 | Guidelines listing regimens before confirmatory randomised data | Mostly Right Numbers Off | unwritten |
| 9 | ESMO grades D and E — 'shown not to work' as a finding | Mostly Right Numbers Off | unwritten |
| 10 | ESMO-MCBS — statistically significant is not the same as worthwhile | Mostly Right Numbers Off | unwritten |
| 11 | Precision oncology checked honestly — SHIVA and NCI-MATCH | Mostly Right Numbers Off | unwritten |
| 12 | DRUP — same evidence level, different results | Wrong | unwritten |
| 13 | The same cell line, diverged across labs | Mostly Right Numbers Off | unwritten |
| 14 | The common-essential filter that hid PRMT5 | Mostly Right Numbers Off | unwritten |
| 15 | TMB ≥10 mut/Mb is assay-specific | Contested Hypothesis | unwritten |

Counts: 10 needed number or attribution fixes, 4 state a contested hypothesis
as settled fact, 1 is wrong. Zero were clean.

---

## 1. Cancer as an atavism — ancient genes switching back on

**Verdict:** Contested Hypothesis — real research, but the framing states a contested idea as settled

### Corrected claim

"Seven tumour types" is correct, but the biology is stated more strongly than the data
support. Defensible version: "A 2017 PNAS study by Trigos and colleagues (Peter
MacCallum Cancer Centre) dated the evolutionary origin of 17,318 human genes by
phylostratigraphy, sorting them into 16 phylostrata, and compared their expression in
3,473 tumour samples against 386 matched normal samples across seven TCGA solid-tumour
cohorts (breast BRCA, colon COAD, liver LIHC, lung adenocarcinoma LUAD, lung squamous
LUSC, prostate PRAD, stomach STAD — seven cohorts drawn from six organs, since LUAD and
LUSC are both lung). Across all seven, genes with orthologues in bacteria, yeast and
protozoa (phylostrata 1–3, 'unicellular' genes) were consistently up-regulated in tumour
tissue, while genes that arose with metazoan multicellularity were predominantly down-
regulated. The inflection point sits at the Opisthokonta phylostratum. The authors also
reported that co-expression between interacting unicellular and multicellular processes
breaks down in tumours, and named 12 highly connected genes (RCC2, TLN1, VASP, ACTG1,
PLEC, CTTN, DSP, ILK, PKN2, CTNNA1, CTNND1, PKP3) as candidate general drivers of that
separation. This pattern is consistent with — and was explicitly framed by the authors
as evidence for — the atavism hypothesis of cancer (a 'reversion' to an ancestral
unicellular program), first formalised by Davies & Lineweaver in 2011 and later extended
by Lineweaver, Bussey, Blackburn & Davies (2021) into a 'serial atavism' model of
stepwise reversions. The atavism/serial-atavism framework remains a contested
hypothesis, not established cancer biology, and no treatment decision currently rests on
it."

### What the original got wrong

WHAT THE CLAIM GETS RIGHT: "Seven tumour types" is exactly correct and verified against
the primary source — Trigos et al., PNAS 2017;114(24):6406-6411 analysed seven TCGA
cohorts (BRCA, COAD, LIHC, LUAD, LUSC, PRAD, STAD), 3,473 tumour and 386 normal samples,
17,318 genes across 16 phylostrata. The directional finding is also correctly stated: UC
genes (phylostrata 1-3) up, metazoan-origin genes down. The authors themselves keyword-
index the paper under "atavism," so attributing an atavism framing to them is fair.

WHERE IT OVERSTATES — four problems a clinician could challenge:

(1) "Oldest genes switch on and evolutionarily YOUNGER ones switch off" is not what the
data show. The relationship is NOT monotonic. Per the paper's own Figure 1 results,
genes with bacterial/yeast/protozoan orthologues are consistently up; genes in metazoan
phylostrata *predating eutherian mammals* are primarily down; but the YOUNGEST genes —
those unique to eutherian (placental) mammals — showed little difference between tumour
and normal. So the correct statement is "genes that arose with metazoan multicellularity
switch off," not "younger genes switch off." The inflection point is specifically at the
Opisthokonta phylostratum. Saying "the younger the gene, the more it is switched off" is
factually wrong at the young end of the scale.

(2) "Seven tumour types" is a real number but a weaker one than it sounds. These are
seven TCGA cohorts from six organs (LUAD and LUSC are both lung). It is bulk RNA-seq of
primary tumour vs adjacent normal — a cross-sectional expression correlation, with no
functional or longitudinal validation, and no demonstration that the ancient program is
causal rather than consequential. Also note the same group's 2024 Genome Biology paper
used 31 tumour types with a different (co-expression) design; if a bigger number is
wanted, it must be attributed to that paper, not this one.

(3) THE MAJOR CONFOUNDER THE CLAIM HIDES. Ancient genes (phylostrata 1-3) are
overwhelmingly the housekeeping/core-machinery genes — ribosome biogenesis, cell cycle,
DNA replication, glycolysis — while metazoan-origin genes encode differentiation,
adhesion and tissue-signalling functions. Any highly proliferative, poorly
differentiated tissue will therefore show "ancient genes up, recent genes down" whether
or not any atavistic program exists. The paper itself reports a negative correlation
between the proliferation marker MKI67 and the transcriptome age index, which is exactly
the pattern proliferation alone would produce. The authors' counter-argument is that the
signature is "distinct from those observed in stem cells" and so goes "beyond
dedifferentiation" — that is an argument, not a settled result, and
dedifferentiation/proliferation remains the leading rival explanation. The paper also
concedes the picture is not a clean dichotomy: multicellular processes such as hormone-
receptor signalling drive several of these tumour types and are up, not down.

(4) ATTRIBUTION ERROR IN THE CLAIM. "Serial atavism" is not Davies & Lineweaver. Davies
& Lineweaver (Phys Biol 2011) proposed the single-reversion "Metazoa 1.0" atavism model.
The serial/stepwise version is Lineweaver, Bussey, Blackburn & Davies (BioEssays
2021;43(7):e2000305) — four authors, a decade later, and explicitly framed by them as
predictions to be tested, not findings ("Advances in phylostratigraphy now enable this
idea to be tested"). Conflating the two misattributes the model.

HOW CONTESTED — this is the core of the verdict:

- The atavism hypothesis is a live minority framework, not consensus. Daignan-Fornier &
Pradeu (BioEssays 2024) devote a full critical review to asking why atavism "has not so
far emerged as a major theory on cancer," faulting it for unclear and non-unified
predictions and for determinism that sits badly with the fact that hallmarks such as
genome instability and the Warburg effect are frequent but not universal.

- A central conceptual objection is convergence vs reversion: the same expression
pattern is equally well explained as convergent evolution toward a proliferative stem-
like attractor state, rather than literal reversal down the phylogenetic ladder. Chen et
al. (Nat Commun 2015) — often cited alongside Trigos as support — themselves describe
the endpoint as resembling embryonic stem cells, which is a dedifferentiation reading as
much as an atavism reading.

- The method itself is disputed. Phylostratigraphy systematically underestimates gene
age for short, fast-evolving proteins and can manufacture spurious non-uniform
distributions across age groups (Moyers & Zhang, MBE 2015). Domazet-Lošo et al. (MBE
2017) rebut this and find the inferences hold. That methodological argument is
unresolved, and it sits directly under the Trigos result.

- Beware citing the PNAS commentary "Ancestral gene regulatory networks drive cancer"
(Bussey, Cisneros, Lineweaver, Davies, PNAS 2017) as independent endorsement — two of
its four authors are the originators of the atavism model.

CLINICAL BOTTOM LINE FOR PUBLICATION: this is an evolutionary-biology hypothesis with
supportive transcriptomic correlations across seven TCGA cohorts. It has produced no
validated biomarker, no approved therapy, and no change to any guideline. The 12 hub
genes are computational candidates, not established drug targets. If this goes on a
decision-support site, it must be labelled explicitly as a research hypothesis with no
current bearing on treatment selection; presenting it as "cancer IS ancient genes
reactivating" would be stating a contested model as settled fact. Per PubMed-sourced
metadata and DOIs cited above.

### Sources

- Trigos AS, Pearson RB, Papenfuss AT, Goode DL. Altered interactions between unicellular and multicellular genes drive hallmarks of transformation in a diverse range of solid tumors. Proc Natl Acad Sci U S A. 2017;114(24):6406-6411. [PRIMARY SOURCE for the '7 tumour types' claim] — `PMID: 28484005; DOI: 10.1073/pnas.1617743114`
- Davies PCW, Lineweaver CH. Cancer tumors as Metazoa 1.0: tapping genes of ancient ancestors. Phys Biol. 2011;8(1):015001. [PRIMARY SOURCE for the atavism hypothesis] — `PMID: 21301065; DOI: 10.1088/1478-3975/8/1/015001`
- Lineweaver CH, Bussey KJ, Blackburn AC, Davies PCW. Cancer progression as a sequence of atavistic reversions. BioEssays. 2021;43(7):e2000305. [PRIMARY SOURCE for 'serial atavism' — note authorship is NOT 'Davies & Lineweaver' alone] — `PMID: 33984158; DOI: 10.1002/bies.202000305`
- Daignan-Fornier B, Pradeu T. Critically assessing atavism, an evolution-centered and deterministic hypothesis on cancer. BioEssays. 2024;46(6):e2300221. [Critical review; explains why atavism 'has not so far emerged as a major theory on cancer'] — `PMID: 38644621; DOI: 10.1002/bies.202300221`
- Bussey KJ, Cisneros LH, Lineweaver CH, Davies PCW. Ancestral gene regulatory networks drive cancer. Proc Natl Acad Sci U S A. 2017;114(24):6160-6162. [Commentary on Trigos et al. — written by the atavism model's own proponents, so not independent corroboration] — `PMID: 28584134; DOI: 10.1073/pnas.1706990114`
- Moyers BA, Zhang J. Phylostratigraphic bias creates spurious patterns of genome evolution. Mol Biol Evol. 2015;32(1):258-267. [Methodological challenge to the gene-dating method Trigos et al. rely on] — `PMID: 25312911; DOI: 10.1093/molbev/msu286`
- Domazet-Lošo T, Carvunis AR, Albà MM, et al. No Evidence for Phylostratigraphic Bias Impacting Inferences on Patterns of Gene Emergence and Evolution. Mol Biol Evol. 2017;34(4):843-856. [Rebuttal defending phylostratigraphy] — `PMID: 28087778; DOI: 10.1093/molbev/msw284`
- Trigos AS, Pearson RB, Papenfuss AT, Goode DL. Somatic mutations in early metazoan genes disrupt regulatory links between unicellular and multicellular genes in cancer. eLife. 2019;8:e40947. — `PMID: 30803482; DOI: 10.7554/eLife.40947`
- Trigos AS, Bongiovanni F, Zhang Y, et al. Disruption of metazoan gene regulatory networks in cancer alters the balance of co-expression between genes of unicellular and multicellular origins. Genome Biol. 2024;25(1):110. [Same group's later work — 31 tumour types, co-expression design] — `PMID: 38685127; DOI: 10.1186/s13059-024-03247-1`
- Chen H, Lin F, Xing K, He X. The reverse evolution from multicellularity to unicellularity during carcinogenesis. Nat Commun. 2015;6:6367. (Corrigendum: Nat Commun. 2015;6:8812, PMID 26511015) [Independent line of supporting evidence, published before Trigos] — `PMID: 25751731; DOI: 10.1038/ncomms7367`
- Trigos AS, Pearson RB, Papenfuss AT, Goode DL. How the evolution of multicellularity set the stage for cancer. Br J Cancer. 2018;118(2):145-152. [Authors' own review, more hedged than the PNAS paper] — `PMID: 29337961; DOI: 10.1038/bjc.2017.398`

---

## 2. Genome chaos — cells shattering their own chromosomes under stress

**Verdict:** Contested Hypothesis — real research, but the framing states a contested idea as settled

### Corrected claim

Cancer cells can undergo catastrophic chromosome shattering and error-prone reassembly.
Two related but distinct concepts must not be conflated:  (1) CHROMOTHRIPSIS is the
established, sequencing-defined phenomenon: tens to hundreds of clustered rearrangements
confined to one or a few chromosomes, acquired in a single cellular catastrophe, with
fragments rejoined in largely random order and orientation and copy number oscillating
between two states (Stephens 2011). Its best-supported mechanism is not direct "stress
shattering" but mis-segregation of a chromosome into a micronucleus, whose envelope
ruptures and exposes the chromatin to fragmentation, followed by reassembly within one
cell division (Zhang 2015). Chromothripsis is detected in roughly 30-50% of cancers,
exceeding 50% in several tumour types (Cortés-Ciriano 2020, PCAWG, 2,658 tumours across
38 cancer types; Simovic-Lorenz & Ernst 2025). The original Stephens 2011 estimate of
"at least 2-3% of all cancers and ~25% of bone cancers" is superseded and should not be
quoted as current.  (2) GENOME CHAOS is Henry Heng's broader, largely cytogenetics-
derived term for rapid genome-wide karyotype reorganisation under crisis; Heng treats
chromothripsis, chromoplexy, chromoanasynthesis and chromoanagenesis as subtypes of it
(Liu et al. 2014). "Genome chaos" is Heng-lab terminology and is not standard usage in
mainstream cancer genomics.  On stressors: in Heng-lab experiments, genome chaos was
induced by CHEMOTHERAPEUTICS acting as collective stressors (doxorubicin, mitomycin-C,
docetaxel, the HSP90 inhibitor 17-DMAG), alongside heat shift and ER stress (Liu 2014;
Stevens 2011). Radiation was NOT tested in that work; chromothripsis-like rearrangements
after ionizing radiation were shown separately, using focused proton microbeam
irradiation of cell lines (Morishita 2016). Hypoxia should be removed from the list:
Stevens 2011 found that acclimating cells to 3.5% O2 REDUCED the chromosome-
fragmentation index to 54.7%, versus "nearly 100%" for the same drug treatment at
atmospheric 20% O2 — low oxygen suppressed fragmentation rather than inducing it.  On
outcome: most cells undergoing chromosome fragmentation die — Heng's own group
classifies it as a distinct form of mitotic cell death (Stevens 2011) — while a minority
of survivors emerge with new, subsequently stabilised karyotypes and increased
transcriptomic and karyotypic heterogeneity (Liu 2014). Heng's group describes this
survivor route to treatment resistance as occurring at "low frequency" (Horne et al.
2026). No published figure quantifies the die/survive ratio, so no percentage should be
attached to "most die, a few survive."  On the "strategy" framing: the attribution to
Heng is accurate and verbatim-supportable — his 2014 paper is titled "Genome chaos:
survival strategy during crisis," and Ye, Liu & Heng (2018) write that "genome chaos, or
karyotype chaos, represents a powerful survival strategy for somatic cells under high
levels of stress/selection." However, this adaptive/purposive reading is a minority
interpretation, not field consensus. The mainstream position treats chromothripsis as a
catastrophic accident whose products are subsequently acted on by Darwinian selection,
conferring selective advantage only after the fact (Simovic-Lorenz & Ernst 2025). The
phenomenon is established; the "strategy, not breakdown" interpretation is contested and
should be presented as Heng's hypothesis, explicitly attributed, not as settled biology.

### What the original got wrong

WHAT THE SNIPPET GETS WRONG OR OVERSIMPLIFIES:

1. HYPOXIA IS FACTUALLY BACKWARDS — the single hardest error. The claim lists hypoxia as
a stressor that makes cells shatter. The Heng lab's own primary stress-survey paper
found the opposite: HCT116 cells acclimated to 3.5% O2 for 5 days and then given
doxorubicin + colcemid showed a chromosome-fragmentation index (CFI) of 54.7%, versus
"nearly 100%" for identical treatment at atmospheric 20% O2. The authors conclude
verbatim that "a normoxic environment suppresses C-Frag as compared with a hyperoxic
environment" (Stevens 2011). Hypoxia must be deleted from the stressor list; a clinician
who checks the source will catch this immediately.

2. RADIATION IS MIS-ATTRIBUTED. Stevens 2011 tested chemotherapeutics, temperature shift
(37<->42C), ER stress (DTT, thapsigargin, tunicamycin), HSP90 inhibition, and
spontaneous genomic instability. It did not test radiation. Liu 2014 induced genome
chaos with chemotherapeutics. Radiation evidence exists but is independent, artificial,
and weaker: Morishita 2016 used a focused proton microbeam (SPICE) on oral SCC cell
lines and obtained "chromothripsis-like" rearrangements in a single derived subline
irradiated with 200 protons. Presenting radiation alongside chemo as equally established
Heng-lab findings overstates the evidence.

3. CONFLATION OF CHROMOTHRIPSIS AND GENOME CHAOS. These are not synonyms and the claim
slides between them. Chromothripsis: strictly defined, confined to one or a few
chromosomes, copy number oscillating between two states, dominant mechanism =
micronucleus envelope rupture (Zhang 2015). Genome chaos: Heng's broader genome-wide
concept, of which he considers chromothripsis a subtype. "Genome chaos" is not standard
mainstream cancer-genomics vocabulary — it is Heng-lab terminology tied to his heterodox
Genome Architecture Theory. Saying tumour cells "shatter and reassemble their
chromosomes" (plural, implying the whole karyotype) describes genome chaos, not
chromothripsis.

4. "STRATEGY, NOT BREAKDOWN" OVERSIMPLIFIES EVEN HENG'S OWN DATA. Stevens 2011
explicitly classifies chromosome fragmentation as a form of MITOTIC CELL DEATH (MCD),
"distinct from apoptosis and mitotic catastrophe," and notes it is more dominant than
apoptosis at lower drug concentrations. So in Heng's own framework it is primarily a
death mechanism that occasionally throws off viable survivors. It is both breakdown and
(rarely) opportunity — the "not a breakdown" phrasing is rhetorically stronger than the
data.

5. "RANDOMLY REASSEMBLE" IS DEFENSIBLE BUT NOT FULLY. Liu 2014 states chaotic genomes
"seem to form by random rejoining of chromosomal fragments, in part through non-
homologous end joining (NHEJ)" — so the wording tracks Heng's own language. However,
Cortés-Ciriano 2020 detected signatures of replication-associated processes and
templated insertions in addition to NHEJ, and Shapiro 2021 argues the restructuring is
"probably less chaotic than its name implies," identifying non-random, cell-type- and
virus-dependent patterns. Note carefully: Shapiro must NOT be cited as support for the
"chaos" framing — he is arguing against it, and he is himself heterodox (natural genetic
engineering).

6. NO NUMBER EXISTS FOR "MOST DIE, A FEW SURVIVE." The direction is supported but
unquantified. Do not attach a percentage. The closest published characterisation from
Heng's group is that the transition to treatment-induced resistance occurs "despite its
low frequency" (Horne 2026). Available CFI numbers describe fragmentation frequency
among mitotic cells, not survival: 36.3% (UCN-01 + doxorubicin) vs 7.2% and 9.4% for
each agent alone; spontaneous CFI 6% falling to 2.9% as MDAH-041 cells stabilised, and
8.8% falling to 0.8% in the MOSEC model; centrosome amplification 21.3% untreated vs
51.7% treated.

7. PREVALENCE NUMBER TO WATCH. If the site elsewhere quotes "2-3% of cancers, 25% of
bone cancers," that is the 2011 Stephens low-resolution estimate and is obsolete.
Current figures: 30-50% of cancers overall, >50% in several types (PCAWG, 2,658 tumours,
38 cancer types).

ESTABLISHED VS CONTESTED — the line a clinician will care about:

ESTABLISHED: chromothripsis is real, common, occurs in a single catastrophic event, is
mechanistically linked to micronuclei and chromosome bridges, and drives oncogene
amplification and tumour-suppressor inactivation. Chemotherapy-induced chromosome
fragmentation in cell lines is a reproducible experimental observation.

CONTESTED: that this constitutes a "strategy" — i.e. an adaptive, quasi-purposive
cellular response rather than a catastrophic accident followed by ordinary selection.
Mainstream reviews frame selective advantage as arising after the event, not as the
event's purpose. Heng's wider Genome Architecture Theory (genome context over gene
content, "fuzzy inheritance," karyotype as the unit of selection) is a minority
position.

ALSO CONTESTED: timing. Chromothripsis is often an early, clonal, pre-treatment event —
in clear cell RCC the 3p loss / 5q gain chromothripsis event can precede the most recent
common ancestor by years to decades. Longitudinal data show it present in primary but
not relapse clones, and vice versa, so the view of it as a single early clonal event
holds only in a subset. This matters because the claim's framing implies therapy is
generally what triggers the shattering; for most detected chromothripsis, it is not.

CLINICAL-COMMUNICATION RISK: the claim as written can be read as "chemotherapy and
radiation cause cancers to become more aggressive," which would be an unsupported and
potentially harmful inference from cell-line data. Any published version must state that
this is in vitro and model-system evidence, that therapy-induced genome chaos is a low-
frequency event, and that it does not argue against giving indicated treatment.
Attribute the strategy framing to Heng by name rather than asserting it.

### Sources

- Liu G, Stevens JB, Horne SD, Abdallah BY, Ye KJ, Bremer SW, Ye CJ, Chen DJ, Heng HH. Genome chaos: survival strategy during crisis. Cell Cycle. 2014;13(4):528-537. — `PMID 24299711 / DOI 10.4161/cc.27378`
- Stevens JB, Abdallah BY, Liu G, Ye CJ, Horne SD, Wang G, Savasan S, Shekhar M, Krawetz SA, Hüttemann M, Tainsky MA, Wu GS, Xie Y, Zhang K, Heng HH. Diverse system stresses: common mechanisms of chromosome fragmentation. Cell Death Dis. 2011;2(6):e178. — `PMID 21716293 / DOI 10.1038/cddis.2011.60`
- Ye CJ, Liu G, Heng HH. Experimental Induction of Genome Chaos. Methods Mol Biol. 2018;1769:337-352. — `PMID 29564834 / DOI 10.1007/978-1-4939-7780-2_21`
- Stephens PJ, Greenman CD, Fu B, Yang F, Bignell GR, et al. Massive genomic rearrangement acquired in a single catastrophic event during cancer development. Cell. 2011;144(1):27-40. — `PMID 21215367 / DOI 10.1016/j.cell.2010.11.055`
- Cortés-Ciriano I, Lee JJ, Xi R, Jain D, Jung YL, Yang L, Gordenin D, Klimczak LJ, Zhang CZ, Pellman DS, Park PJ; PCAWG Consortium. Comprehensive analysis of chromothripsis in 2,658 human cancers using whole-genome sequencing. Nat Genet. 2020;52(3):331-341. — `PMID 32025003 / DOI 10.1038/s41588-019-0576-7`
- Simovic-Lorenz M, Ernst A. Chromothripsis in cancer. Nat Rev Cancer. 2025;25(2):79-92. — `PMID 39548283 / DOI 10.1038/s41568-024-00769-5`
- Zhang CZ, Spektor A, Cornils H, Francis JM, Jackson EK, Liu S, Meyerson M, Pellman D. Chromothripsis from DNA damage in micronuclei. Nature. 2015;522(7555):179-184. — `PMID 26017310 / DOI 10.1038/nature14493`
- Shapiro JA. How Chaotic Is Genome Chaos? Cancers (Basel). 2021;13(6):1358. — `PMID 33802828 / DOI 10.3390/cancers13061358`
- Morishita M, Muramatsu T, Suto Y, Hirai M, Konishi T, Hayashi S, Shigemizu D, Tsunoda T, Moriyama K, Inazawa J. Chromothripsis-like chromosomal rearrangements induced by ionizing radiation using proton microbeam irradiation system. Oncotarget. 2016;7(9):10182-10192. — `PMID 26862731 / DOI 10.18632/oncotarget.7186`
- Horne SD, Ye JC, Liu G, Abdallah BY, Stevens JB, Heng HH. Therapy-induced rapid drug resistance driven by genome chaos and polyploid giant cancer cells. Cancer Lett. 2026;645:218355. — `PMID 41763449 / DOI 10.1016/j.canlet.2026.218355`
- Ye CJ, Sharpe Z, Alemara S, Mackenzie S, Liu G, Abdallah B, Horne S, Regan S, Heng HH. Micronuclei and Genome Chaos: Changing the System Inheritance. Genes (Basel). 2019;10(5):366. — `PMID 31086101 / DOI 10.3390/genes10050366`

---

## 3. Tumours suppressing their own mismatch repair under drug pressure

**Verdict:** Contested Hypothesis — real research, but the framing states a contested idea as settled

### Corrected claim

The study is real and correctly identified: Russo M, Crisafulli G, Sogari A, et al.,
"Adaptive mutability of colorectal cancers in response to targeted therapies," Science
2019;366(6472):1473–1480 (Bardelli lab, Candiolo/Turin). A defensible restatement:  "In
2019, Russo et al. reported that microsatellite-stable (MMR-proficient) colorectal
cancer cell lines exposed to EGFR blockade (cetuximab) or to combined BRAF/EGFR blockade
(dabrafenib + cetuximab) do not simply die or persist passively: the small 'drug-
tolerant persister' population that survives transiently down-regulates mismatch-repair
genes (MLH1, MSH2, MSH6, EXO1) and homologous-recombination genes (BRCA2, RAD51), while
up-regulating low-fidelity, error-prone translesion polymerases (Pol iota, Pol kappa,
REV1, Pol lambda, Pol mu). Functional assays confirmed that MMR capacity fell to levels
comparable with an MMR-deficient control line and that HR capacity fell; reactive oxygen
species and DNA-damage markers (gamma-H2AX, 53BP1) rose. Mutability rose in a
microsatellite frameshift reporter, and microsatellite tracts became unstable in
persister, resistant, and PDX-derived resistant tumours. The state was reversible — DNA-
repair gene expression returned to baseline once the drug was withdrawn, and permanently
resistant derivatives no longer showed the response. MLH1/MSH2 protein down-regulation
was also seen by immunohistochemistry in six cetuximab-treated patient-derived
xenografts and in paired biopsies from two patients responding to FOLFOX plus
panitumumab. The authors framed this explicitly as the mammalian counterpart of
bacterial stress-induced mutagenesis, noting that the induced Y-family polymerases are
orthologues of the bacterial stress-induced polymerases Pol IV and Pol V."  Two
corrections must be attached whenever the claim is used: (1) Magnitude. The 2019 paper
reported no mutation-rate fold change. It explicitly found that exome-wide mutational
burden (mutations/megabase) of persister and resistant populations was "only marginally
affected"; the increased mutability was demonstrated as microsatellite/indel instability
and reporter-frameshift signal, not as a global rise in point mutations. The
quantitative figure comes from a 2022 follow-up by the same group (Russo M, Pompei S,
Sogari A, et al., Nat Genet 2022;54(7):976–984), which used a modified Luria–Delbrück
fluctuation assay to estimate a temporary 7- to 50-fold increase in persister mutation
rate (DiFi + cetuximab; WiDr + dabrafenib/cetuximab) and modelled a corresponding
increase in persister-derived resistant cells. Cite "7- to 50-fold, 2022, cell lines
only" — never a fold change to the 2019 paper. (2) Causality and scope. The 2019 paper
showed increased mutability; it did not show that adaptive mutability generates the
specific resistance drivers seen clinically (KRAS/NRAS, EGFR ectodomain, MAP2K1). Its
own wording is that the polymerase switch is "potentially increasing the occurrence of
mutations conferring drug resistance." Adaptive mutability is offered as an additional
route to resistance alongside — not instead of — outgrowth of pre-existing resistant
subclones, which remains well documented (Misale 2012, Diaz 2012). The authors
themselves note the phenotype is transient, confined to a small subpopulation, and
usually masked by pre-existing clones, which is why elevated mutational burden is not
routinely seen in patient tumours at relapse.  The bacterial analogy is stated correctly
and is the authors' own framing, with one caveat worth keeping: the mutagenesis is
undirected. It raises the genome-wide probability that some cell acquires a resistance
allele; it does not target resistance genes. This is stress-induced mutagenesis in the
Rosenberg/Foster sense, not Cairns-style "directed mutation."

### What the original got wrong

WHAT THE CLAIM GETS RIGHT

- Year, journal, first author, tumour type and mechanism direction are all correct.
Russo et al., Science, published online 7 Nov 2019, print 366(6472):1473-1480.

- MMR down-regulation is real and is the paper's central finding, shown at mRNA (RNA-
seq/qPCR), protein (western/IHC) and functional (FM-HCR G:G mismatch assay) level.
Homologous recombination was down-regulated too — the claim omits this, which matters
because the HR half is the part with an actionable consequence (proposed PARP-inhibitor
synthetic lethality).

- The bacterial analogy is the authors' own, not a journalist's. The abstract opens with
it and the paper states that the induced Y-family polymerases (Pol iota, Pol kappa,
REV1) are "orthologous to the bacterial stress-induced polymerases Pol IV and Pol V." A
clinician cannot fault the analogy as an embellishment.

WHERE THE CLAIM OVERSTATES — fix before publishing

1. "raising mutation rate" implies a measured global rate increase in 2019. It was not
measured in 2019, and the exome data cut against the simple reading: overall mutational
burden in persisters and resistant cells was "only marginally affected." The
demonstrable 2019 signal was microsatellite/indel instability (CA-NanoLuc frameshift
reporter, WES microsatellite tract shifts, high-depth capture panel). The 7- to 50-fold
rate figure is from the 2022 Nature Genetics fluctuation-test paper, in two cell lines,
and is a "phenotypic" mutation rate inferred from late-emerging resistant colonies plus
mathematical modelling — not a directly sequenced per-base rate.

2. "and the chance of a resistance mutation" is an inference, not a 2019 result. No
specific clinical resistance driver (KRAS, NRAS, EGFR ectodomain, MAP2K1) was shown to
arise de novo from adaptive mutability. The paper's own hedge: "potentially increasing
the occurrence of mutations conferring drug resistance."

3. Scope creep. It is not "colorectal cancer cells" generally — it is MSS/MMR-proficient
CRC lines (DiFi, WiDr, NCI-H508, HT29) under cetuximab or dabrafenib+cetuximab, and
specifically the persister subpopulation. Not shown for chemotherapy, VEGF agents, or
MSI-high CRC. Permanently resistant derivatives did NOT show the phenotype.

4. Clinical evidence is thin and should not be implied to be more. Six PDX models by
IHC, and exactly two patients (FOLFOX + panitumumab) with paired biopsies showing
MLH1/MSH2 down-regulation. No patient mutational or outcome data.

5. Reversibility must be stated. This is a transient, drug-dependent transcriptional
state, not acquired MMR deficiency. Cells do not become dMMR/MSI-high tumours. A
clinician could reasonably infer from the snippet that these patients become checkpoint-
inhibitor candidates — that inference is not supported by this paper, and framing that
avoids it is important on a decision-support site.

WHAT IS GENUINELY CONTESTED (why this is CONTESTED_HYPOTHESIS, not SOLID)

- The molecular observation (MMR/HR down, error-prone polymerases up, reversible) is
solid and replicated within the field. The disputed part is its causal weight in
patients. The dominant, well-evidenced model remains outgrowth of pre-existing resistant
subclones (Misale 2012, Diaz 2012, with mathematical modelling placing the mutations
before treatment). Russo et al. position adaptive mutability as an additional route;
they do not overturn the pre-existing-clone model and say so in their opening paragraph.

- The 2022 authors concede the phenotype is "probably restricted in time... confined to
a small subpopulation of cells and masked by the outgrowth of pre-existing resistant
cells," which is their explanation for why elevated mutational burden is not detected in
patient tumours at relapse. That is an unfalsified-but-unconfirmed position: the
clinical contribution is currently unquantified.

- Independent corroboration exists for the general principle in another tumour type via
a different mechanism (Isozaki 2023, therapy-induced APOBEC3A in EGFR-mutant lung cancer
persisters), which strengthens "therapy-induced mutagenesis in persisters" as a class.
It does not independently confirm the MMR-down mechanism in CRC, which so far rests
largely on one group's work.

- Mechanistic gap in the original paper: mTOR down-regulation tracked the DNA-repair
loss, but mTOR silencing did not reproduce it. The authors state mTOR suppression "is
not sufficient to activate this phenotype." The upstream trigger of adaptive mutability
is unresolved. ROS contributes to DNA damage but N-acetylcysteine did not rescue the
DNA-repair gene down-regulation.

- Analogy caveat worth one clause: bacterial stress-induced mutagenesis is undirected.
The mechanism raises the probability that some surviving cell acquires a useful
mutation; it does not mutate resistance genes preferentially. Do not let phrasing drift
toward Cairns-style "directed mutation," a hypothesis the microbiology field rejected.

SUGGESTED ONE-LINE SAFE VERSION FOR A LAY/CLINICIAN-FACING PAGE

"A 2019 Science study (Russo et al.) found that the small population of colorectal
cancer cells surviving EGFR- or BRAF-targeted therapy transiently switches off mismatch-
repair and homologous-recombination genes and switches on error-prone DNA polymerases —
a reversible, bacteria-like stress response that makes those survivors more mutable and,
the authors propose, more likely to throw off a resistance mutation. A 2022 follow-up
from the same group estimated a temporary 7- to 50-fold rise in mutation rate in these
cells. The contribution of this mechanism to resistance in actual patients, relative to
resistant clones that were already present before treatment, is not yet established."

### Sources

- Russo M, Crisafulli G, Sogari A, Reilly NM, Arena S, Lamba S, Bartolini A, Amodio V, Magrì A, Novara L, Sarotto I, Nagel ZD, Piett CG, Amatu A, Sartore-Bianchi A, Siena S, Bertotti A, Trusolino L, Corigliano M, Gherardi M, Cosentino Lagomarsino M, Di Nicolantonio F, Bardelli A. Adaptive mutability of colorectal cancers in response to targeted therapies. Science. 2019;366(6472):1473-1480. — `PMID 31699882; DOI 10.1126/science.aav4474`
- Russo M, Pompei S, Sogari A, Corigliano M, Crisafulli G, Puliafito A, Lamba S, Erriquez J, Bertotti A, Gherardi M, Di Nicolantonio F, Bardelli A, Cosentino Lagomarsino M. A modified fluctuation-test framework characterizes the population dynamics and mutation rate of colorectal cancer persister cells. Nature Genetics. 2022;54(7):976-984. — `PMID 35817983; DOI 10.1038/s41588-022-01105-z; PMC9279152`
- Fahrer J. Switching off DNA repair—how colorectal cancer evades targeted therapies through adaptive mutability. Signal Transduction and Targeted Therapy. 2020;5(1):19. (News & Views summarising the mechanism of Russo 2019) — `PMID 32296051; DOI 10.1038/s41392-020-0120-3; PMC7035417`
- Diaz LA Jr, Williams RT, Wu J, Kinde I, Hecht JR, Berlin J, Allen B, Bozic I, Reiter JG, Nowak MA, Kinzler KW, Oliner KS, Vogelstein B. The molecular evolution of acquired resistance to targeted EGFR blockade in colorectal cancers. Nature. 2012;486(7404):537-540. (Evidence that resistance clones pre-exist therapy) — `PMID 22722843; DOI 10.1038/nature11219`
- Misale S, Yaeger R, Hobor S, et al. Emergence of KRAS mutations and acquired resistance to anti-EGFR therapy in colorectal cancer. Nature. 2012;486(7404):532-536. (Companion evidence for pre-existing resistant subclones) — `PMID 22722830; DOI 10.1038/nature11156`
- Isozaki H, Sakhtemani R, Abbasi A, et al. Therapy-induced APOBEC3A drives evolution of persistent cancer cells. Nature. 2023;620(7973):393-401. (Independent, different-mechanism support for therapy-induced mutagenesis in persisters, in lung cancer) — `PMID 37407818; DOI 10.1038/s41586-023-06303-1`
- Parseghian CM, Sun R, Woods M, et al. Resistance mechanisms to anti-epidermal growth factor receptor therapy in RAS/RAF wild-type colorectal cancer vary by regimen and line of therapy. Journal of Clinical Oncology. 2023;41(3):460-471. (Clinical ctDNA series; found transcriptional rather than mutational acquired resistance predominating with anti-EGFR plus chemotherapy) — `DOI 10.1200/JCO.22.01423`
- Bjedov I, Tenaillon O, Gérard B, Souza V, Denamur E, Radman M, Taddei F, Matic I. Stress-induced mutagenesis in bacteria. Science. 2003;300(5624):1404-1409. (Background for the bacterial side of the analogy) — `DOI 10.1126/science.1082240`
- Gutierrez A, Laureti L, Crussard S, et al. β-Lactam antibiotics promote bacterial mutagenesis via an RpoS-mediated reduction in replication fidelity. Nature Communications. 2013;4:1610. (Cited by Russo et al. as the bacterial antibiotic precedent) — `DOI 10.1038/ncomms2607`

---

## 4. Transmissible cancers, and the 11,000-year-old dog lineage

**Verdict:** Mostly Right Numbers Off — real, but figures or attribution need correcting

### Corrected claim

Transmissible cancers — clonal cancer cell lineages that spread between hosts as an
infectious agent — are known in dogs (canine transmissible venereal tumour, CTVT),
Tasmanian devils (two independent lineages, DFT1 and DFT2), and marine bivalves (bivalve
transmissible neoplasia, BTN). A 2024 review counted 11 lineages (1 canine + 2 devil + 8
BTN across nine bivalve species); the tally has since risen to at least 13, after two
further BTN lineages (CnuBTN1, CnuBTN2) were described in the basket cockle Clinocardium
nuttallii in 2025. The count is a running total that rises with sampling effort, not a
fixed census. CTVT is the oldest known somatic cell lineage: the current best estimate,
from a time-resolved phylogeny of 546 tumour exomes, places its origin at roughly 6,200
years ago (95% HPDI 4,148–8,508 years), with the most recent common ancestor of all
sampled present-day tumours only ~1,900 years ago and global spread beginning with
colonial-era dog movement ~500 years ago. The widely repeated "~11,000 years" figure
comes from an earlier two-genome study and has been superseded.

### What the original got wrong

Sourcing from PubMed and the primary literature. Two distinct problems, one minor and
one substantive.

1. THE CTVT AGE IS THE REAL ERROR — the claim cites a superseded estimate. "~11,000
years" traces to Murchison et al., Science 2014 (PMID 24458646), which sequenced just
TWO CTVT genomes and concluded the founder dog "may have lived about 11,000 years ago."
The same laboratory overturned this in Baez-Ortega et al., Science 2019 (PMID 31371581)
using 546 CTVT exomes and a Bayesian time-resolved phylogeny: origin ~6,220 years ago,
95% HPDI 4,148–8,508 (the abstract summarises this as "transmitted by dogs for 4000 to
8500 years"). 11,000 falls OUTSIDE the 95% credible interval of the current estimate —
it is not a rounding difference, it is roughly a two-fold overstatement. The 2014 figure
remains ubiquitous in press coverage and secondary sources, which is presumably where
the snippet picked it up. If the piece wants a single headline number, use ~6,200 years,
or hedge as "several thousand years." Do NOT write "11,000." Caveat in the other
direction: both figures are molecular-clock estimates resting on assumed somatic
mutation rates in a lineage with no fossil calibration, so present ~6,200 with its
interval rather than as a precise value. A separate figure worth keeping straight: the
most recent common ancestor of all sampled modern tumours is only ~1,938 years old (95%
HPDI 993–3,055) — much younger than the lineage's origin. Conflating "lineage age" with
"MRCA of extant tumours" is a common error.

2. "11 LINEAGES" WAS CORRECT FOR MID-2024 AND IS NOW STALE. The number is verbatim from
Bramwell et al., Evolution 2024 (PMID 38656785): "There are currently 11 different
lineages of transmissible cancers, one in dogs..., two in Tasmanian devils..., and eight
bivalve transmissible neoplasia (BTN) in nine bivalve species." Independently
corroborated by Santamarina et al. 2024 (PMID 39522939): "three independent clonal
lineages in mammals and eight different clonal lineages in bivalves." But Yonemitsu et
al., Mol Ecol 2025 (PMID 39980242) then described two further BTN lineages (CnuBTN1,
CnuBTN2) in a previously unaffected host, the basket cockle Clinocardium nuttallii —
bringing the total to at least 13. Write "at least 13" or "more than a dozen," attribute
the number to a dated source, and state that it is rising.

3. LINEAGES vs HOST SPECIES ARE ROUTINELY CONFLATED and this trips up secondary write-
ups. These are different counts and neither implies the other: one lineage can infect
several species (MtrBTN2 arose in Mytilus trossulus but circulates in M. edulis, M.
chilensis and M. galloprovincialis — a xenograft, not just an allograft), while one
species can host several lineages (C. edule has CedBTN1+CedBTN2; C. nuttallii has
CnuBTN1+CnuBTN2; M. trossulus has MtrBTN1+MtrBTN2). Hart et al. 2025 (PMID 40163526) and
Giersch et al. 2025 (PMID 41021636) both say "ten bivalve species" / "at least 10
bivalve species" — species, not lineages. If the piece says "11 lineages... in dogs,
Tasmanian devils, bivalves" it should not also be read as 11 species.

4. "PASS BETWEEN ANIMALS" OVERSIMPLIFIES THE MECHANISM, and a comparative pathologist
would object. The three systems transmit by genuinely different routes: CTVT by coitus
(direct allograft implantation on genital mucosa); DFT1/DFT2 by biting during
social/mating conflict; BTN by cancer cells shed into seawater and taken up by filter-
feeding — i.e. an environmental, non-contact route, now directly supported by eDNA
detection of cancer cells in tank and field seawater (Giersch et al. 2025, PMID
41021636; Weinandt et al., PNAS 2026, PMID 42335235). "Direct contact" is wrong for
bivalves.

5. NOT CONTESTED, but the sub-claims differ in evidential strength. That these are
clonal transmissible lineages is settled — established by genotype mismatch between
tumour and host and confirmed by whole-genome/exome phylogenies. The AGES are the soft
part: MarBTN is dated ">200 years" (Hart et al. 2023, PMID 37783804), cockle BTN origins
are inferred only qualitatively as "ancient" from satellite DNA (Bruzos et al. 2023,
PMID 37783803). Do not attach confident ages to the bivalve lineages.

6. CLINICAL-RELEVANCE CAVEAT FOR THIS SITE. None of these are human entities and the
piece should not imply otherwise even by juxtaposition. Naturally transmissible clonal
cancer lineages have never been documented in humans. The human cases sometimes cited
alongside this material — donor-derived malignancy after organ transplant, maternal-
fetal transmission, laboratory/surgical inoculation accidents — are isolated one-off
transfer events under immunosuppression or shared tolerance, not self-sustaining
lineages passing through a population. That distinction is the one a clinician is most
likely to challenge if the article blurs it.

7. If the count and age both matter, the safest published anchors are: lineage count →
Bramwell 2024 for "11 as of 2024" plus Yonemitsu 2025 for the update; CTVT age → Baez-
Ortega 2019 only.

### Sources

- Bramwell G, DeGregori J, Thomas F, Ujvari B. Transmissible cancers, the genomes that do not melt down. Evolution. 2024;78(7):1205-1211. — `PMID 38656785 / DOI 10.1093/evolut/qpae063`
- Baez-Ortega A, Gori K, Strakova A, et al. Somatic evolution and global expansion of an ancient transmissible cancer lineage. Science. 2019;365(6452):eaau9923. — `PMID 31371581 / DOI 10.1126/science.aau9923`
- Murchison EP, Wedge DC, Alexandrov LB, et al. Transmissible dog cancer genome reveals the origin and history of an ancient cell lineage. Science. 2014;343(6169):437-440. — `PMID 24458646 / DOI 10.1126/science.1247167`
- Yonemitsu MA, Sevigny JK, Vandepas LE, et al. Multiple lineages of transmissible neoplasia in the basket cockle (C. nuttallii) with repeated horizontal transfer of mitochondrial DNA. Mol Ecol. 2025;34(6):e17682. — `PMID 39980242 / DOI 10.1111/mec.17682`
- Santamarina M, Bruzos AL, Pequeño-Valtierra A, et al. Novel PCR assay for the identification of two transmissible cancers in Cerastoderma edule. J Invertebr Pathol. 2024;207:108232. — `PMID 39522939 / DOI 10.1016/j.jip.2024.108232`
- Bruzos AL, Santamarina M, García-Souto D, et al. Somatic evolution of marine transmissible leukemias in the common cockle, Cerastoderma edule. Nat Cancer. 2023;4(11):1575-1591. — `PMID 37783803 / DOI 10.1038/s43018-023-00641-9`
- Hart SFM, Yonemitsu MA, Giersch RM, et al. Centuries of genome instability and evolution in soft-shell clam, Mya arenaria, bivalve transmissible neoplasia. Nat Cancer. 2023;4(11):1561-1574. — `PMID 37783804 / DOI 10.1038/s43018-023-00643-7`
- Michnowska A, Hart SFM, Smolarz K, Hallmann A, Metzger MJ. Horizontal transmission of disseminated neoplasia in the widespread clam Macoma balthica from the Southern Baltic Sea. Mol Ecol. 2022;31(11):3128-3136. — `PMID 35403750 / DOI 10.1111/mec.16464`
- Hart SFM, Garrett FES, Kerr JS, Metzger MJ. Gene expression in soft-shell clam (Mya arenaria) transmissible cancer reveals survival mechanisms during host infection and seawater transfer. PLoS Genet. 2025;21(3):e1011629. — `PMID 40163526 / DOI 10.1371/journal.pgen.1011629`
- Giersch RM, Sevigny JK, Weinandt SA, et al. Variation in natural infection outcomes and cancer cell release from soft-shell clams (Mya arenaria) with bivalve transmissible neoplasia. PLoS Pathog. 2025;21(9):e1013537. — `PMID 41021636 / DOI 10.1371/journal.ppat.1013537`

---

## 5. Driver mutations in normal skin

**Verdict:** Mostly Right Numbers Off — real, but figures or attribution need correcting
**Written:** `content/news/` → `cancer-mutations-in-normal-skin`

### Corrected claim

Ultradeep sequencing (~500x effective coverage) of 74 cancer genes across 234 biopsies
of 0.79-4.71 mm2 each (~5 cm2 of skin in total) of physiologically and histologically
normal, sun-exposed eyelid epidermis, taken from four adults aged 55-73 undergoing
blepharoplasty, found a somatic mutation burden of 2-6 mutations per megabase per cell
with a characteristic ultraviolet signature. Positively selected driver mutations - in
NOTCH1, NOTCH2, NOTCH3, TP53, FAT1 and RBM10 - were estimated to be present in 18-32% of
cells (the paper's own summary: "over a quarter"), at a density of approximately 140
driver mutations per square centimetre, averaging 0.27 driver point mutations per cell
versus 2.7 per cutaneous squamous cell carcinoma. The epidermis remained physiologically
and histologically normal throughout. Because only 74 genes were sequenced, these are
floor estimates; and because the donors were older adults sampled at a chronically sun-
exposed site, the figures characterise aged photodamaged skin rather than skin in
general - mutant clone density varies substantially by body site (Martincorena et al.,
Science 2015; Fowler et al., Cancer Discovery 2021).

### What the original got wrong

WHAT IS EXACTLY RIGHT: "~140 driver mutations per square centimetre" is verbatim from
the abstract and needs no change. Component estimates in the body: NOTCH1 57.1/cm2 (CI
51-61), NOTCH2 24.6/cm2 (19-28), NOTCH3 1.3/cm2 (0.6-1.6) = 83/cm2 for NOTCH genes
alone, plus FAT1 9.5/cm2 (4.6-11.8), plus TP53/RBM10/FGFR3 to reach ~140. The
attribution (Martincorena et al., Science 2015, eyelid, sun-exposed) is correct. "While
the skin remains functionally normal" is faithful - the paper states the epidermis
"remains physiologically and histologically normal" and the abstract ends "while
maintaining the physiological functions of epidermis."

WHAT IS OFF: (1) "Up to a third of cells" reports only the top of a published range and
rounds 32% up to 33%. The paper's figure is 18-32%, and the authors' own one-line gloss
is "over a quarter of cells." Publish the range, not the maximum. Per-gene cell
fractions: NOTCH1 14-21%, NOTCH2 5-7%, NOTCH3 2-3%, TP53 3-5%, FAT1 3-5%. (2) The claim
reads as a general property of sun-exposed eyelid skin. It is not: n=4 donors, aged
55-73 (3F, 1M), three Western European and one South Asian, all with age-related eyelid
changes warranting surgery. A young person's eyelid would not carry this burden, and the
authors found statistically significant between-individual heterogeneity in the driver
landscape (q=0.0005 for one gene). Publishing without "aged" and "four donors" is the
main defensibility gap. (3) Both figures are model-based estimates, not cell counts:
cell fractions come from variant allele fractions corrected for local copy number, and
driver counts come from a dN/dS excess-of-nonsynonymous-mutations model. They carry
confidence intervals. (4) Both are floors - only 74 genes were sequenced; Fowler 2021
later found 11 genes under positive selection across body sites, including TP63, KMT2D,
ARID2 and AJUBA not counted in the 2015 eyelid total.

WHAT IS CONTESTED (mechanism, not the numbers): Simons (PNAS 2016) argued that the
observed clone-size distributions are largely consistent with neutral drift, creating a
paradox with the dN/dS evidence of strong selection; Martincorena, Jones and Campbell
replied that selection is real but "constrained" - strong only during initial clonal
expansion, after which growth reverts to near-neutral drift. Simons maintained the
evidence for that constrained-selection model is lacking. Crucially, neither side
disputed the 18-32% or ~140/cm2 estimates; the dispute is about what drives clone
growth. The paper's own data show the driver-vs-neutral clone size gap is small (neutral
0.15 mm2; NOTCH1 0.23; TP53 0.33; FGFR3 0.69), which the authors call "unexpectedly
small." So the headline numbers are settled; the evolutionary interpretation is not.

CLINICAL FRAMING CAVEAT: do not let this read as "a third of your skin cells are pre-
cancerous." The authors' own point cuts the other way - FGFR3 hotspot mutations produced
the largest clones yet are associated with seborrheic keratosis, which never becomes
invasive, showing clone size does not track malignant potential. The paper also notes
CDKN2A point mutations were absent from normal skin despite being frequent in cSCC, i.e.
some events remain cancer-specific. Fowler 2021 adds that variation in cancer risk
between body sites substantially exceeds variation in mutant clone density - driver
presence is not a risk readout. This is the key message for a decision-support site:
detecting a canonical cSCC driver in tissue is not by itself evidence of malignancy.

### Sources

- Martincorena I, Roshan A, Gerstung M, Ellis P, Van Loo P, McLaren S, Wedge DC, Fullam A, Alexandrov LB, Tubio JM, Stebbings L, Menzies A, Widaa S, Stratton MR, Jones PH, Campbell PJ. Tumor evolution. High burden and pervasive positive selection of somatic mutations in normal human skin. Science. 2015;348(6237):880-886. — `PMID 25999502; DOI 10.1126/science.aaa6806; PMC4471149`
- Simons BD. Deep sequencing as a probe of normal stem cell fate and preneoplasia in human epidermis. Proc Natl Acad Sci U S A. 2016;113:128-133. — `DOI 10.1073/pnas.1516123113; PMC4711853`
- Martincorena I, Jones PH, Campbell PJ. Constrained positive selection on cancer mutations in normal skin. Proc Natl Acad Sci U S A. 2016;113(9):E1128-E1129. — `PMID 26884187; DOI 10.1073/pnas.1600910113; PMC4780655`
- Simons BD. Reply to Martincorena et al.: Evidence for constrained positive selection of cancer mutations in normal skin is lacking. Proc Natl Acad Sci U S A. 2016;113(9):E1130-E1131. — `PMID 26884186; DOI 10.1073/pnas.1601045113; PMC4780657`
- Fowler JC, King C, Bryant C, Hall MWJ, Sood R, Ong SH, et al., Jones PH. Selection of Oncogenic Mutant Clones in Normal Human Skin Varies with Body Site. Cancer Discov. 2021;11(2):340-361. — `PMID 33087317; DOI 10.1158/2159-8290.CD-20-1092; PMC7116717`

---

## 6. What NCCN category 2A actually means

**Verdict:** Mostly Right Numbers Off — real, but figures or attribution need correcting
**Written:** `content/news/` → `what-nccn-2a-actually-means`

### Corrected claim

NCCN grades every recommendation on a combined evidence-and-consensus scale. Category 1
and Category 2A both require "uniform NCCN consensus," which NCCN defines as at least
85% (≥85%, not >85%) support of the panel; the two categories differ only in the
strength of the underlying evidence — Category 1 rests on high-level evidence (e.g.
randomized phase 3 trials or high-quality meta-analyses), Category 2A on lower-level
evidence. Category 2A is the default: every NCCN guideline carries the standing note
"All recommendations are category 2A unless otherwise indicated." Category 2B is lower-
level evidence with only ≥50% but <85% panel support; Category 3 reflects major panel
disagreement (≥25% of the panel voting to include it).  In an independent academic
analysis — not an NCCN analysis — Desai, Go and Poonacha reviewed the 2019 versions of
the NCCN guidelines for the most common cancers in the United States (the same 10
tumour-type guidelines used in the authors' 2010 study), counting staging, therapy and
surveillance recommendations. Of 1,818 such recommendations, 7% were Category 1, 87%
Category 2A, 6% Category 2B and 0% Category 3. That was essentially unchanged from 1,023
recommendations in 2010 (6% / 83% / 10% / 1%), even though the total number of
recommendations grew 77%.  Two caveats matter for interpretation. First, the 1,818
denominator is not all of NCCN: it covers roughly 10 of NCCN's 80-plus guidelines and
excludes screening, supportive-care and other content. Parallel studies give different
figures — 91% Category 2A among 1,353 recommendations in the 2020 hematologic-malignancy
guidelines, and 80.6% Category 2A among radiation-therapy recommendations. Second,
because 2A is the automatic default for any recommendation that carries no explicit
label, the 87% figure should not be read as "87% of recommendations cleared a recorded
≥85% panel ballot." The ≥85% threshold defines the category; the default designation is
administrative. Category 2A therefore signals "lower-level evidence with no meaningful
expert dissent" — neither a formally tallied supermajority on each item, nor, as it is
often misread, a weak or poorly supported recommendation.

### What the original got wrong

WHAT THE CLAIM GETS RIGHT (verified against primary sources):

- 1,818 total recommendations and 87% Category 2A are EXACT matches to the published
abstract of Desai 2021. Full breakdown 7%/87%/6%/0% for categories 1/2A/2B/3.

- Category 2A does mean uniform consensus on lower-level evidence, and the consensus
threshold genuinely is the same as Category 1. The two categories differ only in
evidence strength. This is the substantively important and correct core of the claim,
and it is the part most often gotten wrong in the wild (2A is routinely misread as "weak
recommendation").

- The default rule is correct and I confirmed it verbatim from an actual NCCN guideline
PDF: "All recommendations are category 2A unless otherwise indicated."

WHAT IS WRONG OR OVERSTATED (each is something a clinician could challenge):

1. MISATTRIBUTION — the question asks "which NCCN analysis and year?" There is no NCCN
analysis. This is an INDEPENDENT academic study by Desai (UConn), Go (Mayo) and Poonacha
(Univ. Minnesota), published in International Journal of Cancer 2021 (online Aug 2020),
analysing the 2019 guideline versions. NCCN did not conduct or publish it. Attributing
it to NCCN is a citation error that a reader could check in thirty seconds. Note the
same group also published a critical 2019-guidelines conflict-of-interest analysis
(Desai et al., Cancer 2020;126:3742-3749, PMID 32497271), so they are external auditors
of NCCN, not NCCN.

2. ">85%" SHOULD BE "≥85%." NCCN's wording is "at least 85% of the panel vote" / "≥85%
support of the Panel." Small, but on a decision-support site a threshold operator stated
backwards is exactly the kind of error that erodes trust.

3. DENOMINATOR SCOPE MATERIALLY OVERSTATED. "Of 1,818 recommendations, 87% are category
2A" reads as though it covers NCCN in general. It does not. The study covered only the
2019 versions of the guidelines for the most common US cancers — the same 10 tumour-type
guidelines as the 2010 predecessor study (breast, lung, prostate, colorectal, melanoma,
bladder, kidney, pancreatic, uterine, non-Hodgkin lymphoma) — and only staging, therapy
and surveillance recommendations. NCCN publishes 80+ guidelines including supportive
care, screening, age-related and detection guidelines, none of which are in this count.
Parallel analyses give materially different percentages: 91% 2A in hematologic
malignancies (n=1,353, 2020 guidelines) and 80.6% 2A for radiation therapy
recommendations. So "87%" is not a universal NCCN constant.

Confidence note: the published abstract itself says only "the common cancers in the
United States." The "10 guidelines" scope is inferred with high confidence from (a) the
direct 2010 comparator, whose abstract states "the 1,023 recommendations found in the 10
guidelines" for "the 10 most common cancers," and (b) the same authors' companion 2020
COI paper, which explicitly used "the latest 2019 versions of the NCCN CPGs for the 10
most common cancers by incidence in the United States." The Wiley full text is paywalled
(HTTP 403), so I could not read the Methods section directly. If the site wants to state
the exact guideline list, it should be verified against the full text first.

4. BIGGEST OVERSIMPLIFICATION — THE DEFAULT RULE AND THE 85% THRESHOLD ARE IN TENSION.
The claim juxtaposes "≥85% panel agreement" with "it is the DEFAULT when no category is
stated" without noticing these pull against each other. Because 2A is applied
automatically to every unlabeled recommendation, a large share of the 87% consists of
items that were never put to a recorded panel ballot at all. The ≥85% figure defines
what the category *means*; the default designation is administrative bookkeeping.
Writing "87% of NCCN recommendations were endorsed by ≥85% of the panel" would be a
genuine factual error. Correct framing: 2A denotes lower-level evidence with no
registered expert dissent.

5. SOURCING SUBTLETY WORTH KNOWING. I verified from NCCN NSCLC v3.2020 that the one-page
"NCCN Categories of Evidence and Consensus" (CAT-1) printed in the guidelines themselves
contains NO percentages — it reads only "uniform NCCN consensus." The ≥85% / ≥50% / ≥25%
thresholds appear only in NCCN's online process documentation and in guideline
Discussion text. If the site cites the guideline front matter for the 85% figure, that
citation will not support it; cite the NCCN process page instead.

Additional trap: the NSCLC v3.2020 Discussion paragraph that supplies the "at least 85%"
quote also contains an NCCN typo — it describes Category 2B as "major NCCN disagreement
(at least 50%...)" and Category 3 as "NCCN consensus (at least 25%...)," which
transposes the two. Do not quote that passage for the 2B or 3 definitions.

IS THE SCIENCE CONTESTED? The underlying factual measurement is not contested — three
independent teams using the same method get concordant results (87%, 91%, 80.6% across
solid tumours, heme, and radiation oncology), and the 2010 vs 2019 stability is robust.
What IS contested is the INTERPRETATION. The Desai/Poonacha framing treats the 2A
predominance as an evidence deficit demanding more trials. NCCN's counter-position (see
JNCCN 2012;10(4):427, "Evidence and Insights in the NCCN Guidelines," responding to the
2011 paper) is that the finding does not indicate panels ignoring high-quality data, but
reflects the state of the oncology evidence base, and that many 2A recommendations cover
clinically uncontroversial matters where randomized trials would be unnecessary or
unethical. If the site editorializes about what the 87% *means* for guideline quality,
that opinion should be flagged as an interpretive position with a named counter-
position, not presented as settled. The bare statistic itself is safe to state, with the
scope qualifier attached.

RECOMMENDATION FOR PUBLICATION: keep the numbers, fix the attribution to
Desai/Go/Poonacha 2021 (not NCCN), change > to ≥, add the "10 common-cancer guidelines,
staging/therapy/surveillance only" qualifier, and do not phrase the 87% as though each
item passed an 85% vote.

### Sources

- Desai AP, Go RS, Poonacha TK. Category of evidence and consensus underlying National Comprehensive Cancer Network guidelines: Is there evidence of progress? International Journal of Cancer. 2021;148(2):429-436. (Published online 14 Aug 2020.) — `PMID: 32674225; DOI: 10.1002/ijc.33215`
- Poonacha TK, Go RS. Level of scientific evidence underlying recommendations arising from the National Comprehensive Cancer Network clinical practice guidelines. Journal of Clinical Oncology. 2011;29(2):186-191. (The 2010 comparator study: 1,023 recommendations across the 10 most common cancers; 6%/83%/10%/1%.) — `PMID: 21149653; DOI: 10.1200/JCO.2010.31.6414`
- National Comprehensive Cancer Network. NCCN Categories of Evidence and Consensus; NCCN Categories of Preference. Page CAT-1 of NCCN Clinical Practice Guidelines in Oncology: Non-Small Cell Lung Cancer, Version 3.2020 (02/11/20). Verbatim: 'Category 2A Based upon lower-level evidence, there is uniform NCCN consensus that the intervention is appropriate.' and 'All recommendations are category 2A unless otherwise indicated.' Note the printed CAT-1 definitions contain no percentage thresholds. — `https://www.nccn.org/guidelines/category_1`
- National Comprehensive Cancer Network. NCCN Clinical Practice Guidelines in Oncology: Non-Small Cell Lung Cancer, Version 3.2020, Discussion section (MS-3). Verbatim: 'Category 1 recommendations indicate uniform NCCN consensus (at least 85% of the panel vote) that the intervention is appropriate based on high-level evidence such as randomized phase 3 trials. Category 2A recommendations indicate uniform NCCN consensus that the intervention is appropriate based on lower level evidence such as phase 2 trials. It is important to note that all recommendations are category 2A in the NCCN Guidelines unless otherwise indicated.' (Caution: the same paragraph's descriptions of Categories 2B and 3 are internally transposed/erroneous in this version — do not cite it for those two definitions.) — `NCCN NSCLC v3.2020, MS-3`
- National Comprehensive Cancer Network. Development and Update of Guidelines (NCCN Guidelines Process). Source for the full vote thresholds: Category 1 and 2A = uniform consensus (≥85% support of the Panel); Category 2B = ≥50% but <85%; Category 3 = ≥25% of the panel voting to include. — `https://www.nccn.org/guidelines/guidelines-process/development-and-update-of-guidelines`
- Chengappa M, Desai A, Go R, Poonacha T. Level of Scientific Evidence Underlying the National Comprehensive Cancer Network Clinical Practice Guidelines for Hematologic Malignancies: Are We Moving Forward? Oncology (Williston Park). 2021;35(7):390-396. (1,353 recommendations in 2020 guidelines: 5%/91%/4%/1%.) — `PMID: 34270186; DOI: 10.46883/ONC.2021.3507.390`
- Noy MA, Rich BJ, Llorente R, Kwon D, Abramowitz M, Mahal B, Mellon EA, Zaorsky NG, Dal Pra A. Levels of Evidence for Radiation Therapy Recommendations in the National Comprehensive Cancer Network (NCCN) Clinical Guidelines. Advances in Radiation Oncology. 2021;7(1):100832. (Radiation therapy recommendations: 9.7% category 1, 80.6% category 2A, 8.4% 2B, 1.3% 3.) — `PMID: 34869943; DOI: 10.1016/j.adro.2021.100832`

---

## 7. Anyone can submit evidence to NCCN

**Verdict:** Mostly Right Numbers Off — real, but figures or attribution need correcting

### Corrected claim

NCCN runs a public submission process for its Clinical Practice Guidelines in Oncology.
Its published policy states: "NCCN accepts external requests (submissions) for Panel
consideration for changes to Guidelines recommendations. Examples of external requests
include submissions from industry, organizations, clinicians/clinical groups, patient
advocates, and/or payers." All submitter types use the same online Submission Request
Form under the same rules — NCCN's policy defines no separate track for pharmaceutical
companies — though an NCCN.org account (free to create) is required to submit.  The
deadline in the claim is exactly right: NCCN states requests "must be submitted at least
4 weeks prior to the scheduled annual Panel meeting to allow the submission materials to
be distributed to the Panel leadership and Panel Members for review in advance of the
Panel meeting"; NCCN's Submission Process FAQ states the same rule as "at least 28 days
in advance of the meeting date." Two qualifications: (a) the deadline is anchored to the
**annual** Panel meeting, whose dates NCCN posts publicly (meetings run April–December,
dates usually posted by mid-January); interim meeting dates are explicitly *not*
published, so submissions cannot be timed to them. (b) A submission arriving <28 days
before the meeting "may not be considered until the following year/annual update" — i.e.
a potential ~12-month delay, not a short one.  On discussion, voting and publication:
NCCN states "All submissions are discussed and voted on by the Panel at the Panel
meeting" and "A Panel vote is taken for all external submission requests… All results of
Panel votes relating to drugs, biologics, and external submissions are included in the
transparency document, which is posted to the NCCN website." Outcomes are recorded as a
decision (e.g. "Change Made," "Change Not Made," "Defer to a future update") with the
Panel vote. Four qualifications the original claim omits: (1) Not literally *every*
submission reaches the Panel — NCCN's own FAQ defines a "Closed" status for a submission
that "does not meet the outlined requirements for consideration," and a resubmission of
an already-decided request without new supporting evidence "NCCN will not consider… and
you will be notified that the status has been changed to 'Closed'." So the guarantee
applies to submissions that pass intake screening. (2) Votes are published in
**aggregate**, not per panelist; each NCCN Member Institution holds one vote (plus one
for the patient advocate), ≥50% Panel attendance is required for a meeting to proceed,
and members with a meaningful conflict of interest are recused from the relevant
discussion and vote. (3) Publication is not immediate: the transparency document appears
when the corresponding Guideline version publishes — NCCN says the annual update is
"usually published within 3 to 6 months of the meeting," and its FAQ says "the average
annual update is published 5-6 months after the annual panel meeting." (4) The
transparency documents are on nccn.org but sit behind a free NCCN.org login, and the
Panel deliberation itself is confidential (NCCN "cannot provide specific information on
the content or status of your submissions" beyond a status label).  All of the above
describes NCCN's *stated* policy as published on nccn.org; it is not an independently
audited finding, and no peer-reviewed study has verified submission-level compliance or
compared outcomes for industry vs. non-industry submitters.

### What the original got wrong

NUMBER CHECK — the claim's only figure is correct. NCCN's process page says "at least 4
weeks prior to the scheduled annual Panel meeting"; its Submission Process FAQ (27 Nov
2024) states the identical rule as "at least 28 days in advance of the meeting date." No
hedge needed on "~4 weeks" — it is 4 weeks / 28 days exactly, and both NCCN documents
agree.

WHAT THE SNIPPET GETS RIGHT: the open-to-all framing, the equal-terms framing, the
deadline, and the discussed-voted-published chain all track NCCN's published policy
almost verbatim. This is genuinely unusual transparency among guideline bodies and the
claim is not hype.

WHAT A CLINICIAN COULD PUSH BACK ON:

1. "Every submission is discussed" is the single overstatement. NCCN's own FAQ defines a
"Closed" status — "Submission does not meet the outlined requirements for consideration"
— and states that a resubmission of a decided request without new evidence "NCCN will
not consider." So there is an intake gate before the Panel. The correct formulation is
"every submission accepted for review." Fix this wording or a clinician will catch it.

2. "Same terms as pharmaceutical companies" is an inference, not an NCCN sentence. NCCN
lists industry, organizations, clinicians/clinical groups, patient advocates and payers
together with no differential rules, which supports the inference about the *formal*
process. It says nothing about equal practical influence. Note the structural asymmetry:
interim Panel meetings are convened largely for new FDA approvals/expanded indications
and their dates are not published, so the off-cycle route is in practice tied to
regulatory events; and Panel seats themselves are filled by NCCN Member Institution
appointees (plus a patient advocate), so submission is the only route for outsiders.

3. "The result published with the vote count" needs two qualifiers: votes are AGGREGATE
(institution-level: one vote per Member Institution plus one for the patient advocate),
never per-named-panelist; and publication is deferred to the corresponding Guideline
version — 3-6 months per the process page, "5-6 months" on average per the FAQ. Also,
the transparency pages returned an NCCN login form to unauthenticated fetches on 20 July
2026, so "published" means "posted behind free registration," not open web.

4. The 4-week clock runs against the ANNUAL meeting only. Missing it can defer
consideration to the next annual update (~1 year). Worth stating because it changes how
a reader would plan a submission.

STATUS OF THE UNDERLYING FACTS: established, not contested — every element is directly
sourced to current NCCN policy documents, so this is not a CONTESTED_HYPOTHESIS case.
The one honest epistemic caveat is that it is self-reported process: I found no peer-
reviewed audit verifying that all accepted submissions are in fact voted on, nor any
published analysis comparing outcomes by submitter type. Peer-reviewed work on NCCN
concerns adjacent questions — panel-author financial conflicts (Mitchell 2016, PMID
27561170; Liu 2018, PMID 30459237, which found 71.9% of systemic-treatment
recommendations rest on low-level evidence) and evidence quality behind off-label
recommendations (Kurzrock 2019, PMID 31373348, co-authored by NCCN staff). If the site
wants to imply the process works as advertised rather than that it is documented as
such, that stronger claim is unverified. Article metadata above retrieved via PubMed;
DOI links: https://doi.org/10.1001/jamaoncol.2016.2710,
https://doi.org/10.1634/theoncologist.2017-0655, https://doi.org/10.1093/annonc/mdz232.

SOURCING NOTE: nccn.org returns HTTP 403 to WebFetch and web.archive.org is unavailable
in this environment; the primary text was retrieved by direct HTTP GET with a browser
user-agent and the FAQ PDF parsed locally. Quotes above are verbatim from those
retrievals (20 July 2026). The 2008 CMS compendium submission is included only as
historical contrast — it describes a weaker, chair-screened agenda process and must not
be quoted as current policy.

### Sources

- National Comprehensive Cancer Network. Development and Update of Guidelines. NCCN Guidelines Process (accessed 20 July 2026). PRIMARY SOURCE — contains the verbatim sentences on who may submit, the 4-week deadline, 'All submissions are discussed and voted on by the Panel at the Panel meeting', 'A Panel vote is taken for all external submission requests', transparency document with aggregate voting results, 50% attendance quorum, one vote per Member Institution, and COI recusal. — `https://www.nccn.org/guidelines/guidelines-process/development-and-update-of-guidelines`
- National Comprehensive Cancer Network. NCCN Guidelines Submission Process FAQs, version dated 27 Nov 2024 (3 pp). PRIMARY SOURCE — '…must be received at least 28 days in advance of the meeting date'; submission status definitions including 'Closed: Submission does not meet the outlined requirements for consideration'; resubmission-without-new-data rule; 'the average annual update is published 5-6 months after the annual panel meeting'; transparency document carries 'the decision indicated (eg, Change Made, Change Not Made, etc.) and the panel vote'; interim meeting dates not publicly posted. — `https://www.nccn.org/docs/default-source/default-document-library/gl-submission-process-faqs_11_27-24.pdf?sfvrsn=88670faf_3`
- National Comprehensive Cancer Network. Submission Request Form / Submission Request Details, NCCN Guidelines — Submissions Request to the Guidelines Panels (accessed 20 July 2026). Confirms a single common form for all submitters, the NCCN account requirement, and 'For submissions already reviewed by a panel, you may only submit a new form if there is new or additional supporting data.' — `https://www.nccn.org/guidelines/submissions-request-to-the-guidelines-panels/submission-request-form`
- National Comprehensive Cancer Network. Transparency Process / Transparency Document pages (accessed 20 July 2026). Where submission outcomes and aggregate Panel votes are posted; both pages return an NCCN login form to unauthenticated requests. — `https://www.nccn.org/guidelines/guidelines-process/transparency-process-and-recommendations`
- National Comprehensive Cancer Network. Guidelines Panels Meeting Schedule (accessed 20 July 2026). Public listing of annual Panel meeting dates against which the 4-week deadline is measured. — `https://www.nccn.org/guidelines/guidelines-process/guidelines-panels-schedule`
- National Comprehensive Cancer Network (McGivney WT). Submission Request: The NCCN Drugs and Biologics Compendium — submitted to CMS under FR Vol. 72 No. 133 (2008). HISTORICAL/SUPERSEDED — describes an earlier screening step: 'These requests are evaluated by staff and then the panel chair. Depending upon the cogency of supporting evidence, the issue/request may be placed on the agenda for consideration by the expert panel.' Cited only to show the current 'all submissions are voted on' language is a later, stronger commitment; do not quote as current policy. — `https://www.cms.gov/Medicare/Coverage/CoverageGenInfo/downloads/covdoc14.pdf`
- Mitchell AP, Basch EM, Dusetzina SB. Financial Relationships With Industry Among National Comprehensive Cancer Network Guideline Authors. JAMA Oncol. 2016;2(12):1628-1631. (via PubMed) — `PMID 27561170 / DOI 10.1001/jamaoncol.2016.2710`
- Liu X, Tang LL, Mao YP, et al. Evidence Underlying Recommendations and Payments from Industry to Authors of the National Comprehensive Cancer Network Guidelines. Oncologist. 2019;24(4):498-504. (via PubMed) — `PMID 30459237 / DOI 10.1634/theoncologist.2017-0655`
- Kurzrock R, Gurski LA, Carlson RW, et al. Level of evidence used in recommendations by the National Comprehensive Cancer Network (NCCN) guidelines beyond Food and Drug Administration approvals. Ann Oncol. 2019;30(10):1647-1652. (via PubMed; note two co-authors are NCCN staff) — `PMID 31373348 / DOI 10.1093/annonc/mdz232`

---

## 8. Guidelines listing regimens before confirmatory randomised data

**Verdict:** Mostly Right Numbers Off — real, but figures or attribution need correcting

### Corrected claim

In a longitudinal analysis of 21 new regimens added to the NCCN guidelines for NEWLY
DIAGNOSED multiple myeloma across 50 guideline iterations between January 2000 and April
2021 (Mohyuddin et al., The Oncologist 2025), the MEDIAN time from the first prospective
clinical data on a regimen — often a single-arm phase 1 or 2 study — to its first
appearance in the NCCN guidelines was 15 months (Q1 9, Q3 37; range 2 months for
melphalan/prednisone/bortezomib to over 10 years for VTD-PACE). Where phase 3 data
followed guideline listing, the median time from listing to phase 3 data being reported
(publication or abstract presentation, whichever came first) was 43 months, i.e. roughly
3.5–3.6 years (Q1 26, Q3 67); the same paper elsewhere reports 45 months for the 12
regimens in which listing preceded phase 3 data. This sequence was not universal: 4 of
21 regimens (19%) still had no phase 3 trial at the October 2023 analysis cutoff, and
for 4 others phase 3 data preceded listing by 3–9 months. IMPORTANT: this study did not
examine FDA approval dates at all, so it cannot be cited for the proposition that
guidelines precede regulators — it shows only that NCCN listing frequently precedes
randomized confirmatory data.

### What the original got wrong

PRIMARY SOURCE CONFIRMED (not a news write-up): Mohyuddin et al., The Oncologist
2025;30(7):oyae332, PMID 39719103. Both headline numbers in the claim exist in this
paper, but four of the claim's descriptors are indefensible as written.

1) MISATTRIBUTED FRAMING (most serious). The framing "Guidelines can precede regulators"
is not supported by this study. The paper contains no analysis of FDA approval dates
whatsoever; the only appearance of "regulatory" is an aside that the ENDURANCE trial
"was not considered to be a regulatory trial." The study compares guideline listing to
CLINICAL TRIAL DATA timing, not to regulatory action. A clinician who checks the source
will immediately see the mismatch. Either drop the headline or source it separately (the
real mechanism — NCCN being a CMS-recognized compendium since 2012 under OBRA 1993,
which lets listing drive reimbursement for off-label use — is mentioned in the paper's
introduction but never quantified against FDA timing).

2) "ON AVERAGE" IS WRONG. Both 15 and 43 are MEDIANS, not means, and the distributions
are highly skewed. 15 months: Q1 9, Q3 37, IQR 28, with a range from 2 months
(melphalan/prednisone/bortezomib) to over 10 years (VTD-PACE). Presenting 15 months as a
typical or average interval hides an order-of-magnitude spread the authors explicitly
flag as unexplained and inconsistent.

3) "FIRST PRESENTATION OF RESULTS" IS AMBIGUOUS AND MISLEADS. The clock starts at the
date any prospective clinical data were first reported — the Methods say explicitly "eg,
a single arm phase 1 or 2 study." It is early-phase-data-to-listing, not pivotal-trial-
results-to-listing. Read the wrong way, the claim implies NCCN listed regimens 15 months
after the definitive trial reported, which inverts the paper's actual point.

4) "FULL PUBLICATION OF THE PIVOTAL TRIAL" IS WRONG ON TWO COUNTS. (a) The 43-month
endpoint is "publication/abstract presentation (whichever came first) of phase 3 data" —
an ASCO/ASH abstract stops the clock, so it is not full publication. (b) "Pivotal"
implies regulatory; the paper measured any phase 3 randomized trial, and explicitly
notes one of them (ENDURANCE) was not a regulatory trial. Correct wording: "phase 3 data
first reported."

5) THE SEQUENCE IS NOT UNIVERSAL. 4 of 21 regimens (19%) had NO phase 3 trial at all as
of the October 2023 cutoff (VCd; VTD-PACE; KCd; Dara-VCd). For 4 more, phase 3 data
actually PRECEDED listing — MPT by 9 months, Dara-VMP by 5, Dara-Rd by 4, Dara-VTd by 3.
So only 12 of 21 regimens (57%) fit the "listed first, phase 3 later" pattern the claim
describes. Stating "with full publication coming ~3.5 years after that" as a general
rule overstates.

6) THE PAPER CONTRADICTS ITSELF — verify which figure you quote. Abstract and one
Results sentence give 43 months (Q1 26, Q3 67) for listing-to-phase-3; a second Results
sentence and the Discussion give 45 months (Q1 25, Q3 68) for the 12 regimens where
listing preceded phase 3. These should be the same set. Similar abstract-vs-body
mismatches: endpoint met in "13 trials (81%)" per abstract vs "15 of these trials...
(88%)" of 17 per Results; OS benefit in "Six regimens (38%)" per abstract vs "7 of these
17 trials (41%)" per Results; removals "Five (23%)" vs "5 regimens (24%)" of 21. If the
site cites any secondary figure, cite the Results-section value and say so.

7) SCOPE LIMITS THE AUTHORS THEMSELVES STATE. Newly diagnosed myeloma only — explicitly
NOT relapsed/refractory, where new drugs are usually studied and approved first, and
where the authors say early listing matters more. US/NCCN only (no ESMO, no EMA).
Guidelines sampled Jan 2000–Apr 2021 with analysis frozen Oct 2023, so nothing after
that. n=21 regimens is small; medians on 12–21 observations are fragile. The authors
also excluded one existing phase 3 trial of cyclophosphamide/bortezomib/dexamethasone on
dosing grounds — a judgment call that changes the 80%-had-phase-3 figure.

8) SPIN RISK. The paper is a critique calling for standardization, not a celebration of
guideline speed. Its counterweight findings: the primary endpoint was a surrogate
(PFS/EFS or response rate) in 16 of 17 phase 3 trials, only ~41% (Results) showed an OS
benefit, and two regimens whose confirmatory trials failed their endpoint (KRd, IRd)
remained listed. Quoting only the two timing numbers as evidence that "guidelines move
fast, which is good" reverses the authors' emphasis. Note also that this is the
Prasad/Haslam group, whose consistent research program critiques surrogate endpoints and
guideline evidence standards — not grounds to discount the data, but the interpretive
frame is a policy argument, not a neutral description.

Underlying science is not contested — this is a descriptive audit with reproducible
dates. What is contested is the normative reading (whether early listing ahead of
randomized data is good or bad), and the site should not present either side of that as
settled.

### Sources

- Mohyuddin GR, Almasri J, Goodman A, Haslam A, Prasad V. The lifecycle and evolution of new regimens on the National Comprehensive Cancer Network Guidelines for newly diagnosed multiple myeloma. The Oncologist. 2025;30(7):oyae332. (Online first 24 Dec 2024.) — `PMID: 39719103; DOI: 10.1093/oncolo/oyae332; PMCID: PMC12311275`
- Full text (open access) of the same primary study, used to verify the Results-section figures, IQRs and internal discrepancies not visible in the abstract. — `https://pmc.ncbi.nlm.nih.gov/articles/PMC12311275/`

---

## 9. ESMO grades D and E — 'shown not to work' as a finding

**Verdict:** Mostly Right Numbers Off — real, but figures or attribution need correcting

### Corrected claim

ESMO Clinical Practice Guidelines grade the strength of each recommendation on a five-
letter scale, A–E, adapted from the Infectious Diseases Society of America–United States
Public Health Service Grading System (Dykewicz, Clin Infect Dis 2001), with ESMO
expanding the underlying evidence levels from three to five (I–V). The published wording
is: A — "Strong evidence for efficacy with a substantial clinical benefit, strongly
recommended"; B — "Strong or moderate evidence for efficacy but with a limited clinical
benefit, generally recommended"; C — "Insufficient evidence for efficacy or benefit does
not outweigh the risk or the disadvantages (adverse events, costs, …), optional"; D —
"Moderate evidence against efficacy or for adverse outcome, generally not recommended";
E — "Strong evidence against efficacy or for adverse outcome, never recommended". Two
clarifications matter clinically: (1) grades D and E can be triggered either by evidence
against efficacy or by evidence of an adverse outcome, so an intervention with
demonstrated harm can be graded E even where some efficacy exists; (2) "moderate" versus
"strong" describes the strength of the evidence against the intervention, not the
probability that the intervention lacks effect. Absence or insufficiency of evidence is
graded C, not D or E. Each letter grade is reported alongside a separate Roman-numeral
level of evidence (I–V) describing study design and risk of bias; the letter alone does
not convey the evidence base. This grading scheme is distinct from the ESMO Magnitude of
Clinical Benefit Scale (ESMO-MCBS), which is a separate benefit-magnitude scale and is
not the same as a grade of recommendation.

### What the original got wrong

The claim gets the structure right (ESMO does use letter grades A-E, and D/E are
negative recommendations) but the paraphrase is loose in three ways a clinician would
object to.\n\n1. It drops the harm arm. Both D and E read '...against efficacy OR for
adverse outcome'. An intervention can be graded E on the basis of demonstrated harm, not
only on demonstrated absence of benefit. 'Shown not to work' misdescribes half the
grade's scope.\n\n2. It relocates the uncertainty. 'Probably not work' (D) vs 'not work'
(E) implies the difference is how likely the intervention is to be inert. The actual D/E
distinction is the strength of the evidence base against it: 'moderate evidence against'
vs 'strong evidence against'. A grade D can sit on a single moderate-quality trial; it
is not a statement that the drug probably does nothing.\n\n3. 'Never use' overstates
'never recommended'. ESMO's scale grades the strength of a recommendation, not
permissibility of use; guidelines are explicitly non-binding on individual clinical
judgement (and ESMO CPGs carry the usual disclaimer to that effect).\n\nAdditional
correction worth making on a decision-support site: 'insufficient evidence' maps to
grade C ('optional'), not to D or E. Conflating 'no evidence' with 'evidence of no
benefit' is the single most common misreading of this scale, and the claim as written
invites it.\n\nAttribution correction: the A-E scheme is not original to ESMO. It is
adapted, by permission of IDSA, from the IDSA-USPHS grading system published by Dykewicz
(Clin Infect Dis 2001;33:139-144), which ESMO cites in the table footnote of every CPG.
ESMO's modification was to subdivide the evidence-quality axis from three levels (I-III)
to five (I-V).\n\nContext: the letter grade is always paired with a Roman-numeral level
of evidence (e.g. 'I, A'), and quoting the letter alone strips the evidence-quality half
of the rating.\n\nStatus: established, not contested. This is a documented editorial
convention reproduced verbatim across ESMO CPGs from at least 2017 through the 2025
express updates; it is not a scientific hypothesis. What is legitimately debated in the
methodology literature is whether this IDSA-derived scheme is adequate compared with
GRADE, and note that ESMO has not migrated its CPGs to GRADE. Frequency caveat: grades D
and E are rarely applied in practice, but I could not verify a per-grade D/E count - the
Skelin 2024 analysis reports only the LOE I (30%) and GOR A (43%) figures in its main
text, with the full A-E breakdown confined to unpublished supplementary table S4. Do not
publish a D/E percentage without that supplement.\n\nAmbiguity flag: 'ESMO grades' could
be read as the ESMO-MCBS (scored 1-5 for non-curative and A-C for curative intent). That
is a different instrument measuring magnitude of benefit, and it has no D or E grade in
the sense the claim describes. The corrected claim disambiguates.

### Sources

- Le Rhun E, Weller M, Brandsma D, et al. EANO-ESMO Clinical Practice Guidelines for diagnosis, treatment and follow-up of patients with leptomeningeal metastasis from solid tumours. Ann Oncol. 2017;28(Suppl 4):iv84-iv99. (Table 8: 'Levels of evidence and grades of recommendation as recommended by ESMO (adapted from the Infectious Diseases Society of America-United States Public Health Service Grading System)') — `10.1093/annonc/mdx221 (PMID 28881917)`
- Dykewicz CA. Summary of the guidelines for preventing opportunistic infections among hematopoietic stem cell transplant recipients. Clin Infect Dis. 2001;33(2):139-144. — the IDSA-USPHS source grading system ESMO adapted, cited by permission of IDSA in the ESMO table footnote — `PMID 11418871; 10.1086/321805`
- Skelin M, Perkov-Stipicin B, Vuskovic S, et al. Levels of evidence and grades of recommendation supporting European Society for Medical Oncology clinical practice guidelines. Oncol Res. 2024;32(5):807-815. — cross-sectional analysis of 1,823 recommendations across 41 current ESMO CPGs; 550 (average 30%) LOE I, 794 (average 43%) GOR A — `PMID 38686053; 10.32604/or.2024.048948`
- ESMO Clinical Practice Guideline Express Update on the management of metastatic pancreatic cancer (2025) — confirms the identical A-E / I-V table is still in force in current ESMO guidelines — `https://pmc.ncbi.nlm.nih.gov/articles/PMC12125698/`

---

## 10. ESMO-MCBS — statistically significant is not the same as worthwhile

**Verdict:** Mostly Right Numbers Off — real, but figures or attribution need correcting

### Corrected claim

ESMO built the Magnitude of Clinical Benefit Scale (ESMO-MCBS) because statistical
significance says nothing about how large a benefit is. The founding paper states that
benefit from anti-cancer therapy "may range from trivial (median progression-free
survival advantage of only a few weeks) to substantial (improved long-term survival)"
(Cherny et al., Ann Oncol 2015). Crucially, the scale is applied only to already-
positive studies — superiority trials that reached statistical significance on the
primary endpoint (or on OS as a secondary endpoint) and non-inferiority trials that
concluded non-inferiority — so by construction every graded trial is formally positive,
and the scale's job is to grade how much that positive result is worth.  For the
survival-endpoint forms (2a, primary endpoint OS; 2b, primary endpoint PFS), grading
uses a dual rule: (1) a relative-benefit rule, in which the LOWER limit of the 95% CI of
the hazard ratio must fall at or below a threshold (for OS: ≤0.65 when the control-arm
median OS is short, ≤0.70 for longer control medians; for PFS: ≤0.65); and (2) an
absolute-benefit rule, in which the observed difference in median outcome must exceed a
minimum. In ESMO-MCBS v1.1 Form 2a (control median OS ≤12 months) the published
thresholds were: grade 4 = HR ≤0.65 AND gain ≥3 months, or an increase in 2-year
survival ≥10%; grade 3 = HR ≤0.65 AND gain ≥2.0–<3 months; grade 2 = HR ≤0.65 AND gain
≥1.5–<2.0 months, or HR >0.65–0.70 AND gain ≥1.5 months; grade 1 = HR >0.70 OR gain <1.5
months. Grade 1 is the lowest grade on the non-curative scale (5–1); C is the lowest on
the curative scale (A–C). So a statistically significant trial delivering a median
survival gain of roughly two weeks falls to grade 1 — the design intent, described by
the MCBS statisticians as increasing "the probability of downgrading a trial with a
statistically significant but clinically insignificant observed benefit" (Dafni et al.,
ESMO Open 2017).  A real example: gemcitabine plus erlotinib in advanced pancreatic
cancer (NCIC CTG PA.3) improved median OS from 5.91 to 6.24 months — about 10 days — HR
0.82 (95% CI 0.69–0.99), p = 0.038, and was approved on that basis (Moore et al., JCO
2007). Empirically, Del Paggio et al. found that only 31% (43/138) of statistically
significant RCTs in breast, NSCLC, colorectal and pancreatic cancer published 2011–2015
met MCBS thresholds for substantial benefit.  Two precision caveats: (a) the relative-
benefit criterion is deliberately permissive — it tests whether the data are
statistically compatible with a large relative benefit (the CI limit), not whether the
observed effect size is itself large; the absolute-gain rule is what does the work of
excluding trivial benefit; (b) the dual rule governs only the OS/PFS comparative forms
(2a/2b). Form 2c (response rate, QoL, non-inferiority) and Form 3 (single-arm studies in
orphan/high-unmet-need settings) use different criteria, and QoL and toxicity can raise
or lower a score. The current version is ESMO-MCBS v2.0 (Ann Oncol 2025), which
restratified Form 2a into four control-median-OS bands (<12, ≥12–<24, ≥24–<36, ≥36
months), revised tail-of-curve and toxicity handling, and changed the score of 13.6% of
previously evaluated studies (10.5% down, 3.1% up) — so exact thresholds should be
quoted with the version they come from.

### What the original got wrong

Article metadata and abstracts in this check were retrieved from PubMed; DOI links are
given in the sources list. Threshold values were confirmed verbatim against ESMO's own
v1.1 Evaluation Form 2A PDF and the official ESMO-MCBS booklet, not from news write-ups.

VERDICT RATIONALE — the claim's direction and logic are correct and well supported; what
needs fixing is precision, not substance. Four issues a clinician could legitimately
object to:

1. "Requires a strong enough effect size." This is the biggest imprecision. The MCBS
relative-benefit rule is applied to the LOWER limit of the 95% CI of the HR, not to the
point estimate. That is deliberately permissive/inclusive: ESMO's stated goal was "not
unfairly penalising experimental treatments from trials designed with adequate power
targeting clinically meaningful relative benefit." A trial with an unimpressive point
estimate can still satisfy the relative-benefit limb if its CI reaches low enough. The
absolute-gain limb is what actually excludes trivial benefit. Saying the scale "requires
a strong enough effect size" implies a point-estimate test and overstates the strictness
of that limb.

2. "The scale requires both." True only of the comparative OS/PFS forms (2a, 2b). Form
2c (response rate, QoL, non-inferiority) and Form 3 (single-arm studies in orphan
diseases / high unmet need) do not use the dual rule. Even within Form 2a there is an
alternative route to grade 4 via tail-of-curve data (v1.1: increase in 2-year survival
≥10%; v2.0 adds a restriction that ≥20% of patients on the experimental arm must have
reached the evaluation timepoint). QoL improvement and toxicity also adjust scores up or
down. So "the scale" should be narrowed to "the OS/PFS forms."

3. "Two weeks of life" is an unsourced illustration, not a published MCBS figure. The
primary source's own wording is "trivial (median progression-free survival advantage of
only a few weeks)". The best documented real anchor is gemcitabine+erlotinib in
pancreatic cancer: 6.24 vs 5.91 months median OS = 0.33 months ≈ 10 days, HR 0.82 (95%
CI 0.69–0.99), p=0.038. (An ESMO guideline text describes this as "a 12-day improvement
in median survival," which is a different rounding of the same trial; use the JCO
medians to be safe.) Under v1.1 Form 2a for control median OS ≤12 months this falls into
grade 1 on both limbs (HR limit 0.99 > 0.70, and gain 0.33 months < 1.5 months). I could
not open an ESMO scorecard to quote an official grade for this specific trial, so state
it as "would score grade 1 under the published thresholds," not as "ESMO scored it 1,"
unless you verify the scorecard.

4. Version currency. Most published MCBS scores in circulation are v1.1 (2017), but v2.0
was published in Ann Oncol 2025 and is the current version. v2.0 restratified Form 2a
into four control-median-OS bands (<12, ≥12–<24, ≥24–<36, ≥36 months or not reached with
≥36 months follow-up), revised tail-of-curve crediting and toxicity handling, added a
single-arm de-escalation form (1b), and changed the score of 13.6% of 353 evaluated
studies. I was NOT able to obtain the exact v2.0 Form 2a grade thresholds (the v2.0
paper is paywalled and ESMO has not exposed the v2.0 form PDFs at guessable URLs), so
any exact numbers you publish should be labelled "v1.1" — those I verified verbatim from
ESMO's own form.

WHAT IS CORRECT AND SHOULD BE KEPT:

- The applicability point is exactly right and is the strongest support for the claim:
MCBS is applied only to trials that are already statistically positive (superiority
trials significant on the primary endpoint, or on OS as secondary, plus non-inferiority
trials concluding non-inferiority). Grading therefore operates entirely downstream of
the p-value.

- "A formally positive trial can score the lowest grade" is correct. Grade 1 is the
floor of the non-curative scale (5–1); grade C is the floor of the curative scale (A–C).
Only A/B (curative) and 4/5 (non-curative) count as substantial benefit; 1 and 2 are
negligible benefit.

- The stated purpose is corroborated in ESMO's own words: the scale is intended to
"reduce hype" and distinguish substantial improvements "from trials demonstrating more
limited and sometimes even marginal benefits," and the MCBS statisticians explicitly
describe the dual rule as increasing the probability of downgrading a statistically
significant but clinically insignificant result.

- Empirical corroboration: only 31% (43/138) of statistically significant RCTs across
four tumour types met MCBS substantial-benefit thresholds (Del Paggio 2017) — i.e. the
scale really does grade most positive trials as non-substantial.

INCOMPLETENESS RATHER THAN ERROR: the claim frames MCBS purely as an effect-size filter.
ESMO's stated rationale is broader — value (benefit balanced against cost), reducing
bias and hype in data interpretation, "accountability for reasonableness,"
HTA/reimbursement prioritisation, and WHO Essential Medicines List screening. MCBS also
explicitly credits living better (QoL, reduced toxicity), not only living longer. Worth
one sentence so the framing is not reductive.

ESTABLISHED VS CONTESTED: the mechanics described above are documented fact, not
contested. What IS contested in the literature is the scale's methodology — notably its
reliance on the proportional-hazards assumption (problematic for immunotherapy trials
with delayed or crossing curves), the absence of restricted mean survival time (RMST)
despite FDA interest, handling of informative censoring and crossover, and poor
concordance with the ASCO Value Framework. These do not undermine the claim but are fair
to flag if the site presents MCBS as an authoritative arbiter. Also note the threshold
values themselves are consensus judgements by the ESMO working group, not empirically
derived from patient preference studies — they are a value framework, not a measurement.

### Sources

- Cherny NI, Sullivan R, Dafni U, Kerst JM, Sobrero A, Zielinski C, de Vries EGE, Piccart MJ. A standardised, generic, validated approach to stratify the magnitude of clinical benefit that can be anticipated from anti-cancer therapies: the European Society for Medical Oncology Magnitude of Clinical Benefit Scale (ESMO-MCBS). Ann Oncol. 2015;26(8):1547-73. — `PMID 26026162 / DOI 10.1093/annonc/mdv249`
- Cherny NI, Dafni U, Bogaerts J, Latino NJ, Pentheroudakis G, Douillard JY, Tabernero J, Zielinski C, Piccart MJ, de Vries EGE. ESMO-Magnitude of Clinical Benefit Scale version 1.1. Ann Oncol. 2017;28(10):2340-2366. — `PMID 28945867 / DOI 10.1093/annonc/mdx310`
- Cherny NI, Oosting SF, Dafni U, Latino NJ, Galotti M, Zygoura P, et al. ESMO-Magnitude of Clinical Benefit Scale version 2.0 (ESMO-MCBS v2.0). Ann Oncol. 2025;36(8):866-908. — `PMID 40409995 / DOI 10.1016/j.annonc.2025.04.006`
- Dafni U, Karlis D, Pedeli X, Bogaerts J, Pentheroudakis G, Tabernero J, Zielinski CC, Piccart MJ, de Vries EGE, Latino NJ, Douillard JY, Cherny NI. Detailed statistical assessment of the characteristics of the ESMO Magnitude of Clinical Benefit Scale (ESMO-MCBS) threshold rules. ESMO Open. 2017;2(4):e000216. — `PMID 29067214 / PMC5640101 / DOI 10.1136/esmoopen-2017-000216`
- ESMO. ESMO-Magnitude of Clinical Benefit Scale v1.1, Evaluation Form 2A (non-curative, primary endpoint OS, median OS with standard treatment ≤12 months) [official scoring form; verbatim grade 4/3/2/1 thresholds]. — `https://dam.esmo.org/image/upload/ESMO-MCBS-version-1.1-Evaluation-Form-2a-OS-12-Months.pdf`
- ESMO. Understanding ESMO-MCBS (official booklet, v2.0 edition) — applicability criteria ('positive' superiority and non-inferiority trials), dual rule definition, form/grade table (1a,1b: A/B/C; 2a: 5-1; 2b, 2c, 3: 4-1), v2.0 four OS strata. — `https://dam.esmo.org/image/upload/esmo-mcbs-booklet.pdf`
- Moore MJ, Goldstein D, Hamm J, et al. Erlotinib plus gemcitabine compared with gemcitabine alone in patients with advanced pancreatic cancer: a phase III trial of the National Cancer Institute of Canada Clinical Trials Group. J Clin Oncol. 2007;25(15):1960-6. — `PMID 17452677 / DOI 10.1200/JCO.2006.07.9525`
- Del Paggio JC, Azariah B, Sullivan R, Hopman WM, James FV, Roshni S, Tannock IF, Booth CM. Do Contemporary Randomized Controlled Trials Meet ESMO Thresholds for Meaningful Clinical Benefit? Ann Oncol. 2017;28(1):157-162. — `PMID 27742650 / DOI 10.1093/annonc/mdw538`
- Mauro E, Serra-Burriel M. ESMO-MCBS v2.0: Advances, challenges, and perspectives in the assessment of clinical benefit in oncology. JHEP Rep. 2025;7(10):101553. (independent commentary on v2.0 limitations: proportional-hazards assumption, absence of RMST, informative censoring, crossover) — `PMID 41132442 / PMC12541619 / DOI 10.1016/j.jhepr.2025.101553`

---

## 11. Precision oncology checked honestly — SHIVA and NCI-MATCH

**Verdict:** Mostly Right Numbers Off — real, but figures or attribution need correcting

### Corrected claim

Precision oncology reality check. In the randomised phase 2 SHIVA trial (Le Tourneau et
al., Lancet Oncol 2015), 741 patients with treatment-refractory metastatic solid tumours
were screened, 293 (40%) had an alteration matching one of 10 available regimens, and
195 (26%) were randomised to a marketed molecularly targeted agent used off-label versus
treatment at physician's choice. There was no difference in the primary endpoint: median
progression-free survival 2.3 months (95% CI 1.7-3.8) versus 2.0 months (1.8-2.1),
hazard ratio 0.88 (95% CI 0.65-1.19), p=0.41. Important qualifier: SHIVA tested one pre-
specified matching algorithm using 11 already-marketed single agents restricted to three
pathways (hormone receptor, PI3K/AKT/mTOR, RAF/MEK), in heavily pretreated patients,
without weighting alterations by evidence tier. Its authors concluded that off-label use
of targeted agents outside their indications should be discouraged outside trials — not
that biomarker-matched treatment fails in general.  In NCI-MATCH (EAY131; Flaherty et
al., J Clin Oncol 2020), tumour specimens were submitted from 5,954 patients; sequencing
succeeded in 5,540 (93.0%); an alteration actionable for a trial subprotocol was present
in 37.6% of successfully sequenced patients; and 17.8% (985/5,540; 95% CI 16.8-18.8)
were assigned to a treatment arm after clinical and molecular exclusions (26.4% could
have been assigned had all subprotocols been open simultaneously). Only about 70% of
assigned patients actually started subprotocol treatment, so roughly 12% of successfully
sequenced patients — approximately 690 of 5,540 — actually received a matched drug.  The
broader inference is contested rather than settled. SAFIR02-BREAST (André et al., Nature
2022) randomised 238 patients with HER2-non-overexpressing metastatic breast cancer and
found that matched targeted therapy improved PFS when the alteration was ESCAT tier I/II
(adjusted HR 0.41, 90% CI 0.27-0.61, p<0.001) but not when alterations were unselected
by evidence tier (adjusted HR 0.77, 95% CI 0.56-1.06, p=0.109). The defensible reading
of SHIVA and NCI-MATCH is that matching on weak-evidence alterations with single
marketed agents in late-line disease does not help, and that the operational funnel from
sequencing to treatment is steep — not that molecular matching is ineffective per se.

### What the original got wrong

SHIVA result: verified against the primary Lancet Oncology publication. "No difference"
is accurate for the primary endpoint (mPFS 2.3 vs 2.0 months, HR 0.88, 95% CI 0.65-1.19,
p=0.41). The claim is defensible as stated but under-specified — it omits that SHIVA
tested off-label use of 11 already-marketed agents as monotherapy across only three
pathways in heavily pretreated patients, with no evidence-tier weighting. A clinician
can and will object to SHIVA being cited as a verdict on precision oncology generally;
the trial's own conclusion is narrower (discourage off-label matched use outside
trials).

NCI-MATCH numbers, all from Flaherty et al. JCO 2020 (the primary molecular-landscape
report, not a news write-up):

- 93%: correct. Exact figure 93.0% (5,540 of 5,954 submitted specimens sequenced
successfully). Note the earlier JNCI design/interim paper reports 87.3% profiling
success at interim and 93.9% assay completion after process changes — cite the 93.0% to
the JCO paper to avoid a mismatch.

- 37%: correct, exact figure 37.6%. Denominator is successfully sequenced patients, not
all screened. Actionability varied widely by histology (>35% urothelial, <6% pancreatic
and small-cell lung), so a single pooled number oversimplifies.

- 18% "actually received a matched drug": this is the error. 17.8% (985/5,540) were
ASSIGNED to a treatment arm; only ~70% of those assigned actually started subprotocol
treatment, giving roughly 12% (~690/5,540) who actually received a matched drug. The
claim conflates assignment with receipt and therefore overstates real-world delivery by
about 50% relative. The paper also reports a counterfactual 26.4% assignment rate had
all subprotocols been open simultaneously — worth noting so the 17.8% is not read as an
intrinsic biological ceiling.

Contested-science caveat: framing SHIVA + NCI-MATCH as a blanket "precision oncology
doesn't deliver" is a contested interpretation, not settled fact. SAFIR02-BREAST (Nature
2022) is randomised evidence that matching does improve PFS when restricted to ESCAT
tier I/II alterations (adj HR 0.41) and does not when alterations are unselected (adj HR
0.77) — i.e. evidence-tier selection, not matching itself, is the discriminator. Also,
the SHIVA cross-over analysis (Ann Oncol 2017) found a PFS-ratio >1.3 in 37% of patients
crossing from physician's choice to matched therapy but in 61% crossing the other way,
which undercuts the PFS-ratio methodology rather than rescuing the matched arm; do not
cite the 37% cross-over figure as evidence of matched-therapy benefit.

Recommended publication guardrail: state the denominators explicitly ("of specimens
sequenced"), say "assigned to a matched arm" versus "actually received a matched drug"
as two separate numbers, and pair the SHIVA result with the ESCAT-tier finding so the
takeaway is "match on strong evidence tiers" rather than "matching does not work."

### Sources

- Le Tourneau C, Delord JP, Gonçalves A, et al. Molecularly targeted therapy based on tumour molecular profiling versus conventional therapy for advanced cancer (SHIVA): a multicentre, open-label, proof-of-concept, randomised, controlled phase 2 trial. Lancet Oncol. 2015;16(13):1324-1334. — `PMID 26342236; DOI 10.1016/S1470-2045(15)00188-6`
- Flaherty KT, Gray RJ, Chen AP, et al. Molecular Landscape and Actionable Alterations in a Genomically Guided Cancer Clinical Trial: National Cancer Institute Molecular Analysis for Therapy Choice (NCI-MATCH). J Clin Oncol. 2020;38(33):3883-3894. — `PMID 33048619; DOI 10.1200/JCO.19.03010`
- Flaherty KT, Gray R, Chen A, et al. The Molecular Analysis for Therapy Choice (NCI-MATCH) Trial: Lessons for Genomic Trial Design. J Natl Cancer Inst. 2020;112(10):1021-1029. — `PMID 31922567; DOI 10.1093/jnci/djz245`
- Belin L, Kamal M, Mauborgne C, et al. Randomized phase II trial comparing molecularly targeted therapy based on tumor molecular profiling versus conventional therapy in patients with refractory cancer: cross-over analysis from the SHIVA trial. Ann Oncol. 2017;28(3):590-596. — `PMID 27993804; DOI 10.1093/annonc/mdw666`
- André F, Filleron T, Kamal M, et al. Genomics to select treatment for patients with metastatic breast cancer. Nature. 2022;610(7931):343-348. — `PMID 36071165; DOI 10.1038/s41586-022-05068-3`

---

## 12. DRUP — same evidence level, different results

**Verdict:** Wrong — do not publish in the proposed form

### Corrected claim

In the Dutch DRUP trial (Drug Rediscovery Protocol), off-label drug–biomarker cohorts
produced widely divergent outcomes. The tumour-agnostic nivolumab cohort in
microsatellite-instable (MSI) tumours reached a CLINICAL BENEFIT RATE of 63% (van der
Velden et al., Nature 2019, https://doi.org/10.1038/s41586-019-1600-x). By contrast,
palbociclib or ribociclib monotherapy in tumours with cyclin D–CDK4/6 pathway
alterations (CDK4, CDK6, CCND1/2/3 amplification, or complete loss of CDKN2A or SMARCA4)
produced a CLINICAL BENEFIT RATE at 16 weeks of only 15% with an objective response rate
of 0% in 112 evaluable patients — and that figure comes from a pooled analysis of DRUP
together with the Australian MoST programme, not DRUP alone (Zeverijn et al., Int J
Cancer 2023, https://doi.org/10.1002/ijc.34649). Both headline numbers are clinical
benefit rates (confirmed objective response OR stable disease ≥16 weeks), not response
rates. The two cohorts were NOT at the same formal evidence level: DRUP's only enrolment
gate is a "potentially actionable" variant matched to a drug approved in another
indication, and where several matches exist the protocol explicitly selects "the agent
with the highest level of evidence." DRUP's own 2026 Nature analysis of 1,610 patients
draws the opposite conclusion to "evidence level ≠ effect size": it reports that "the
highest-performing targets in DRUP shared a common denominator: a strong biological
rationale and prior clinical evidence of activity," notes that MSI-H is now ESCAT Tier
I-C / OncoKB Level 1 tumour-agnostically, states that "several molecular alterations
included in the study are now recognized as weak or non-actionable biomarkers, which
helps explain the modest activity observed in some cohorts," and recommends that future
frameworks "prioritize high-confidence targets" (Verkerk et al., Nature 2026,
https://doi.org/10.1038/s41586-026-10405-x). A defensible use of DRUP is therefore the
reverse of the claim: formal actionability tier DID track outcome, and equal eligibility
for a basket-trial cohort is not equal evidence.

### What the original got wrong

Sourced via PubMed. Four separate defects, any one of which a clinician could challenge.

1. WRONG METRIC. Both 63% and 15% are CLINICAL BENEFIT rates (confirmed CR/PR or stable
disease ≥16 weeks), DRUP's primary endpoint — not response rates. Calling them response
rates inflates them substantially, because CBR is dominated by stable disease.

2. THE 15% FIGURE IS ESPECIALLY WRONG AS STATED. The Zeverijn abstract reads: "In 112
evaluable patients, the objective response rate was 0% and clinical benefit rate at 16
weeks was 15%." The claim's "15% response rate" is off by the entire quantity — the true
response rate was zero. Publishing "15% response rate" for a cohort with no responders
is the kind of error that destroys credibility with an oncologist reading it.

3. NOT PURELY DRUP, AND NOT LIKE-FOR-LIKE. The 15% comes from a pooled DRUP + Australian
MoST analysis of 139 treated / 112 evaluable patients (116 palbociclib, 23 ribociclib),
published four years after and in a different journal from the 63% figure. The 63% is a
single DRUP stage-2 cohort from the 2019 interim report of the first 215 patients. These
are not two cohorts read off one table; presenting them as a head-to-head DRUP
comparison is a framing artefact of the 2024 Acta Oncologica review (a secondary
source), which juxtaposes them in one sentence. For context, DRUP's stage-3 MSI
expansion (130 patients) later reported CBR 62% / ORR 45%, but that is so far only an
ASCO abstract, not peer-reviewed in full.

4. THE FRAMING IS NOT MERELY UNSUPPORTED — IT IS CONTRADICTED. No DRUP publication
assigns these two matches "formally the same evidence level." DRUP has no tier system
for opening cohorts; eligibility is a single binary gate (a potentially actionable
target with an FDA/EMA-approved drug not approved for that tumour type), and the
protocol explicitly picks "the agent with the highest level of evidence" when multiple
matches exist — i.e. a hierarchy was assumed, not equality. More damaging: the
definitive 2026 Nature DRUP paper (1,610 patients) explicitly concludes that formal
actionability DID predict benefit. Its discussion states the best targets shared "a
strong biological rationale and prior clinical evidence of activity," reflected in
ESCAT/OncoKB rankings (BRAF V600E, MSI-H, TMB-H = ESCAT I-C / OncoKB Level 1 tumour-
agnostically), and attributes weak cohorts to alterations "now recognized as weak or
non-actionable biomarkers." Its closing recommendation is that frameworks "prioritize
high-confidence targets." CDK4/6 pathway alterations are exactly the weak-biomarker
category; MSI-H is the top tier. So DRUP is close to the worst possible example for an
"evidence level ≠ effect size" argument.

WHAT IS SALVAGEABLE. The underlying idea has real merit but needs a different vehicle.
ESCAT tiers grade the strength and design of supporting evidence, not the magnitude of
benefit (I-A prospective randomized, I-B prospective single-arm, I-C basket) — so two
alterations can share a tier and differ in effect size. If OpenOnco wants to make that
point, cite ESCAT's own definitions (Mateo 2018) and the DRUP tumour-type finding
instead: DRUP showed tumour type significantly affected CBR in 4 of 17 drug–target
subgroups, e.g. thyroid BRAF V600E CBR 86.7% (n=15) vs 25.0% in other thyroid targets
(n=16, p=0.001), and pembrolizumab in TML-H performing worse in colorectal cancer. The
classic textbook version is BRAF V600E: high response in melanoma, minimal single-agent
activity in colorectal cancer — same variant, same drug class, same nominal
actionability, opposite effect size. That framing is well supported; the 63%-vs-15%
framing is not.

ADDITIONAL CAVEAT FOR PUBLICATION. DRUP figures come from heavily pretreated patients
with no standard options remaining and no control arm; the trial's own authors warn that
"comparison of tumour subgroups should be interpreted cautiously, as differences in CBR
and PFS can reflect intrinsic variations in disease biology rather than differences in
treatment efficacy." Any cross-cohort comparison drawn from DRUP inherits that caveat
and should carry it.

STATUS: this is not contested science. It is a mislabelled statistic plus an inference
the primary source rejects. Recommend the claim not be published in its current form.

### Sources

- van der Velden DL, Hoes LR, van der Wijngaart H, et al. The Drug Rediscovery protocol facilitates the expanded use of existing anticancer drugs. Nature. 2019;574(7776):127-131. — `PMID 31570881 / DOI 10.1038/s41586-019-1600-x`
- Zeverijn LJ, Looze EJ, Thavaneswaran S, et al. Limited clinical activity of palbociclib and ribociclib monotherapy in advanced cancers with cyclin D-CDK4/6 pathway alterations in the Dutch DRUP and Australian MoST trials. Int J Cancer. 2023;153(7):1413-1422. — `PMID 37424386 / DOI 10.1002/ijc.34649`
- Verkerk K, Spiekman AC, Haj Mohammad SF, et al. Prospective evaluation of genomics-guided off-label treatment. Nature. 2026;653(8114):558-566. — `PMID 41986720 / DOI 10.1038/s41586-026-10405-x`
- Haj Mohammad SF, Timmer HJL, Zeverijn LJ, et al. The evolution of precision oncology: The ongoing impact of the Drug Rediscovery Protocol (DRUP). Acta Oncol. 2024;63:368-372. — `PMID 38779868 / DOI 10.2340/1651-226X.2024.34885`
- Hoes LR, van Berge Henegouwen JM, van der Wijngaart H, et al. Patients with Rare Cancers in the Drug Rediscovery Protocol (DRUP) Benefit from Genomics-Guided Treatment. Clin Cancer Res. 2022;28(7):1402-1411. — `PMID 35046062 / DOI 10.1158/1078-0432.CCR-21-3752`
- Geurts B, Zeverijn LJ, Battaglia TW, et al. Efficacy and predictors of response of nivolumab in treatment-refractory MSI solid tumors: results of a tumor-agnostic DRUP cohort. J Clin Oncol. 2023;41(16_suppl):2590. [ASCO conference abstract — not a peer-reviewed full paper] — `DOI 10.1200/JCO.2023.41.16_suppl.2590`
- Mateo J, Chakravarty D, Dienstmann R, et al. A framework to rank genomic alterations as targets for cancer precision medicine: the ESMO Scale for Clinical Actionability of molecular Targets (ESCAT). Ann Oncol. 2018;29(9):1895-1902. — `PMID 30137196 / DOI 10.1093/annonc/mdy263`

---

## 13. The same cell line, diverged across labs

**Verdict:** Mostly Right Numbers Off — real, but figures or attribution need correcting

### Corrected claim

Ben-David et al. (Nature, 2018) performed genomic characterization of 27 different
laboratory versions ("strains") of MCF7, the most widely used breast cancer cell line,
and found extensive genetic divergence between them — only 35% of coding point mutations
and indels were shared by all 27 strains, and ten chromosome arms (25% of the genome)
differed in at least one pairwise comparison. When the 27 strains were screened against
321 anti-cancer compounds at a single 5 uM dose, 55 compounds strongly inhibited growth
(>50%) in at least one strain — and of those 55, 48 (87%) were completely inactive (<20%
growth inhibition) in at least one other strain. Under a stricter two-strain criterion,
33 of 42 compounds (79%) were differentially active. The paper's abstract states this
conservatively as "at least 75% of compounds that strongly inhibited some strains were
completely inactive in others." Note that the denominator is the 55 compounds active
anywhere, not all 321 screened.

### What the original got wrong

STRAIN COUNT IS CORRECT (27), and the cell line is definitively MCF7 — the claim's hedge
"likely MCF7" is unnecessary and should be dropped; the paper names it explicitly and
also reports parallel results for 23 A549 strains, 15 MCF10A strains, and 11 further
cell lines.

FOUR PROBLEMS WITH THE CLAIM AS WRITTEN:

1. WRONG DENOMINATOR (most important). "~75% of compounds killing some samples had no
effect on others" reads as 75% of the 321 compounds screened. It is not. Only 55 of 321
compounds (17%) had strong activity against any strain at all; 48 of those 55 (87%) had
at least one fully resistant strain. Quoting "75%" without naming the 55-compound
denominator invites a clinician to infer ~240 discordant compounds when the true count
is 48. The abstract's "at least 75%" is a deliberately conservative floor — the actual
reported figures are 87% (one-strain threshold) and 79% (two-strain threshold, 33/42).
So "~75%" also understates the paper's own headline numbers while risking overstatement
of scale.

2. "FROM DIFFERENT LABS" IS IMPRECISE. The 27 strains comprise 19 that had never
undergone drug treatment or genetic manipulation, 7 carrying a supposedly neutral
genetic modification (reporter gene, Cas9, or DNA barcode), and 1 (MCF7-M) expanded in
mice after anti-estrogen therapy. Eleven of the 27 came from the Connectivity Map
project at a single institution, sampled over a 10-year period, and strains D and E were
siblings only a few passages apart. So the divergence reflects passage history, time in
culture, and deliberate engineering — not purely independent inter-laboratory sourcing.
Strain M was an acknowledged outlier and was excluded from downstream quantitative
genomic analyses.

3. "KILLING" OVERSTATES THE ASSAY. The readout was CellTiter-Glo viability after 72 h at
a single 5 uM concentration. "Strong activity" = >50% growth inhibition; "entirely
resistant"/"no effect" = <20% growth inhibition. These are defined thresholds, not cell
death and not literally zero effect. Say "strongly inhibited growth in" and "produced
little or no growth inhibition in."

4. ROBUSTNESS CAVEAT THE PAPER ITSELF FLAGS. Extended Data Fig. 10c repeats the compound
classification excluding strains Q and M, which were "generally more drug resistant" —
i.e., part of the discordance is carried by two outlier strains. The claim should not
present 75-87% as a threshold-free constant; it is threshold- and strain-set-dependent
(87% at one-strain / >50% activity; 79% at two-strain; further attenuated at an 80%
activity threshold or with Q and M removed).

WHAT IS SOLID AND NOT CONTESTED: The authors ruled out assay noise convincingly —
replicate concordance median Pearson r = 0.97; compounds sharing a mechanism of action
clustered together (three proteasome inhibitors gave matching patterns, corroborated by
biochemical proteasome activity); all 33 differentially active compounds validated in
8-point dose-response across all 27 strains (median Spearman rho = 0.42 across screens);
and 82% of differentially active compounds showed the expected mechanism-of-action
expression signature in sensitive versus insensitive strains. The finding is well
replicated in spirit: Quevedo et al. 2020 (PMID 32937114) found genetic drift in nearly
all of 1,497 cell lines (median 4.5-6.1% of genome drifted between any two isogenic
lines). No published rebuttal was found.

ONE THING TO STATE MORE CAUTIOUSLY THAN THE CLAIM DOES: the causal chain "genetically
diverged SO MUCH THAT drug response differed." Ben-David et al. establish strong
association plus mechanistic plausibility (genomic, transcriptomic, and morphological
clusterings agree), but Quevedo et al. found the drift-to-pharmacological-response
association, while statistically significant, was weak and drug-specific. Phrase as
"genetic divergence was associated with, and mechanistically linked to, large
differences in drug response" rather than asserting drift as the quantified cause of the
full discordance.

RELEVANCE CAVEAT FOR AN ONCOLOGY DECISION-SUPPORT SITE: this is a preclinical-
reproducibility finding about in vitro models. It does not speak to variability of drug
response in patients, and should not be presented adjacent to clinical recommendations
in a way that implies it does. Its legitimate use is to caution that a preclinical
citation resting on a single cell line is weaker evidence than it appears.

### Sources

- Ben-David U, Siranosian B, Ha G, Tang H, Oren Y, Hinohara K, Strathdee CA, Dempster J, Lyons NJ, Burns R, Nag A, Kugener G, Cimini B, Tsvetkov P, Maruvka YE, O'Rourke R, Garrity A, Tubelli AA, Bandopadhayay P, Tsherniak A, Vazquez F, Wong B, Birger C, Ghandi M, Thorner AR, Bittker JA, Meyerson M, Getz G, Beroukhim R, Golub TR. Genetic and transcriptional evolution alters cancer cell line drug response. Nature. 2018 Aug;560(7718):325-330. [PRIMARY SOURCE] — `PMID: 30089904; DOI: 10.1038/s41586-018-0409-3; PMC6522222`
- Quevedo R, Smirnov P, Tkachuk D, Ho C, El-Hachem N, Safikhani Z, Pugh TJ, Haibe-Kains B. Assessment of Genetic Drift in Large Pharmacogenomic Studies. Cell Systems. 2020 Oct 21;11(4):393-401.e2. [independent confirmation of drift prevalence; qualifies the drift-to-drug-response link as significant but weak] — `PMID: 32937114; DOI: 10.1016/j.cels.2020.08.012`

---

## 14. The common-essential filter that hid PRMT5

**Verdict:** Mostly Right Numbers Off — real, but figures or attribution need correcting

### Corrected claim

Two of the claim's three components check out; the third — the historical narrative —
does not.  (1) PRMT5/MTAP synthetic lethality is established. Three independent 2016
papers found that loss of MTAP (co-deleted with CDKN2A at 9p21) sensitises cells to
PRMT5 loss. Kryukov et al. (Science 2016) used Project Achilles genome-scale shRNA data
— 216 cell lines (50 MTAP-null / 166 MTAP-positive) plus a 275-line validation set (47 /
228), 491 lines total; MTAP-null lines had ~3.3-fold higher median intracellular MTA,
and MTA was a SAM-competitive PRMT5 inhibitor with >100-fold selectivity over the other
30 methyltransferases profiled. Mavrakis et al. (Science 2016) found the same signal in
a 390-cell-line shRNA screen. Marjon et al. (Cell Reports 2016) extended it to the
MAT2A/PRMT5/RIOK1 axis. MTAP deletion occurs in roughly 10–15% of cancers: 9.6% of
51,828 pan-cancer cases in the Japanese C-CAT registry (18.4% pancreatic, 15.6% biliary
tract, 14.3% lung), validated in TCGA (n=9,896) and AACR GENIE (n=178,034).  (2) PRMT5
is genuinely classed "common essential" in DepMap CRISPR data — verified directly in the
release files, not inferred: PRMT5 (Entrez 10419) is listed in
CRISPRInferredCommonEssentials.csv in both DepMap Public 24Q2 (2,023 genes) and 24Q4
(1,523 genes).  (3) The claim that "a sensible filter discarded the finding before
analysis" is not what happened. The discovery was made in RNAi/shRNA screens, where
PRMT5 is a selective — not pan-lethal — dependency, so no common-essential filter would
have removed it. The real, documented methodological hazard is narrower and applies to
CRISPR-knockout data specifically: Krill-Burger et al. (Genome Biology 2023,
DepMap/Broad) show that of 1,867 CRISPR pan-lethal genes, ~30% are also pan-lethal by
RNAi but ~50% are selective under RNAi, and they name PRMT5 explicitly as a CRISPR pan-
dependency whose biomarker (MTAP copy number) is recoverable only from the RNAi data. So
the correct statement is: had this been screened by CRISPR knockout alone with a
standard common-essential filter, the MTAP association would plausibly have been lost —
not that it actually was.  Also correct the framing "PRMT5 is critical for tumours with
a specific deletion": PRMT5 is required by essentially all proliferating cells. MTAP
deletion does not create the dependency; it creates a partially inhibited (hypomorphic)
PRMT5 state that widens the therapeutic index. That window is real but modest with
first-generation inhibitors (Kryukov reported only "modest" and statistically non-
significant mean IC50 differences with EPZ015666 across 11 isogenic pairs) and is large
only with second-generation MTA-cooperative agents (>70-fold in isogenic HCT116 for
MRTX1719/BMS-986504; ~40-fold for AMG 193).  Clinical validation is early and partial,
not settled. In the first-in-human phase I of AMG 193 (80 patients dosed), the objective
response rate among 42 efficacy-evaluable patients at active/tolerable doses was 21.4%
(95% CI 10.3–36.8%). No PRMT5 inhibitor is FDA-approved as of July 2026.

### What the original got wrong

WHAT THE CLAIM GETS RIGHT

- PRMT5/MTAP synthetic lethality is real, replicated by three independent 2016 groups
(Broad/DFCI, Novartis, Agios) with a clean biochemical mechanism, and now supported by
clinical responses. Not contested.

- PRMT5 really is on DepMap's common-essential list. I verified this by downloading
CRISPRInferredCommonEssentials.csv from the DepMap 24Q2 and 24Q4 Public releases rather
than relying on secondary description; PRMT5 (Entrez 10419) is present in both. Krill-
Burger et al. (Genome Biology 2023) independently name PRMT5 as a CRISPR pan-dependency.

- The general methodological point — that filtering out common-essential genes can hide
selective, druggable dependencies — is a documented, published concern from the DepMap
team itself, and PRMT5 is their worked example.

WHERE THE CLAIM IS NOT DEFENSIBLE

1. "So a sensible filter discarded the finding before analysis" is counterfactual
presented as history. The MTAP/PRMT5 dependency was FOUND, in 2016, in RNAi (shRNA)
screens — Project Achilles (Kryukov), a 390-line Novartis shRNA screen (Mavrakis), and
Agios shRNA screening (Marjon). In RNAi data PRMT5 is a selective dependency, so a
common-essential filter would not have removed it. Genome-scale CRISPR-KO screening
across large cell-line panels barely existed at the time. The correct statement is
conditional ("would have been filtered out of a CRISPR-only pipeline"), not historical.

2. "PRMT5 is critical for tumours with a specific deletion" inverts the biology. PRMT5
is required by essentially all proliferating cells — that is why it is common-essential.
MTAP deletion does not create the dependency; MTA accumulation partially inhibits PRMT5,
producing a hypomorphic state, so MTAP-null cells are sensitised to further inhibition.
This distinction is clinically load-bearing: it is why first-generation active-site
PRMT5 inhibitors caused on-target haematological toxicity with little tumour
selectivity, and why the field had to invent MTA-cooperative binders.

3. "One of the most promising targets of recent years" is defensible as commentary but
should not be stated as an efficacy claim. Best published phase I data: AMG 193 ORR
21.4% (95% CI 10.3–36.8%) in 42 evaluable patients. MRTX1719/BMS-986504 phase I NSCLC
data (ORR ~23%, mDOR ~10.5 months) were presented at WCLC 2025 and are conference-only,
not peer-reviewed — do not cite as a published figure. No PRMT5 inhibitor is FDA-
approved.

4. Selectivity within MTAP-null tumours is imperfect and this is stated plainly in the
primary source. Kryukov et al. write that sensitivities of MTAP-null and MTAP-positive
lines overlap, and that MTAP status alone is not sufficient to identify PRMT5-sensitive
lines. Krill-Burger et al. and downstream work note a subset (~15%) of MTAP-null lines
are insensitive to PRMT5 knockdown.

GENUINELY CONTESTED / OPEN

- Whether MTAP-deleted tumours accumulate enough MTA in vivo for MTA-cooperative
inhibitors to retain their window: MTAP-expressing stroma and surrounding normal cells
metabolise MTA, and at least one study shows this materially blunts MRTX1719 activity
against MTAP-null glioma in vivo (PMID 39711357). Treat the size of the in-vivo
therapeutic window as an open question, not settled.

- Acquired resistance mechanisms are only now being characterised (MAPK-program
enrichment / collateral MEK sensitivity, bioRxiv 2026 — preprint, not peer-reviewed; do
not cite as established).

RECOMMENDATION FOR PUBLICATION

Split the claim into (a) a verified factual statement — PRMT5 is DepMap common-essential
AND a validated MTAP-synthetic-lethal target — and (b) a clearly labelled methodological
illustration: "if you screen only by CRISPR knockout and filter out common-essential
genes, you would drop PRMT5 and lose the MTAP biomarker; this is why DepMap retains RNAi
data." Do not assert that the finding was historically discarded. Add the caveat that
MTAP-deletion status alone does not predict response (ORR ~21%), and that no PRMT5
inhibitor is approved.

### Sources

- Kryukov GV, Wilson FH, Ruth JR, et al. MTAP deletion confers enhanced dependency on the PRMT5 arginine methyltransferase in cancer cells. Science. 2016;351(6278):1214-1218. — `PMID 26912360; DOI 10.1126/science.aad5214`
- Mavrakis KJ, McDonald ER 3rd, Schlabach MR, et al. Disordered methionine metabolism in MTAP/CDKN2A-deleted cancers leads to dependence on PRMT5. Science. 2016;351(6278):1208-1213. — `PMID 26912361; DOI 10.1126/science.aad5944`
- Marjon K, Cameron MJ, Quang P, et al. MTAP deletions in cancer create vulnerability to targeting of the MAT2A/PRMT5/RIOK1 axis. Cell Rep. 2016;15(3):574-587. — `PMID 27068473; DOI 10.1016/j.celrep.2016.03.043`
- Krill-Burger JM, Dempster JM, Borah AA, et al. Partial gene suppression improves identification of cancer vulnerabilities when CRISPR-Cas9 knockout is pan-lethal. Genome Biol. 2023;24(1):192. (Names PRMT5 as a CRISPR pan-dependency whose MTAP-copy-number biomarker is recovered only by RNAi; 1,867 CRISPR pan-lethals.) — `PMID 37612728; DOI 10.1186/s13059-023-03020-w`
- DepMap, Broad Institute. DepMap Public 24Q2 and 24Q4, file CRISPRInferredCommonEssentials.csv. PRMT5 (Entrez 10419) is present in both lists (2,023 and 1,523 genes respectively). Verified by direct download. — `https://plus.figshare.com/articles/dataset/DepMap_24Q2_Public/25880521 ; https://plus.figshare.com/articles/dataset/DepMap_24Q4_Public/27993248`
- Engstrom LD, Aranda R, Waters L, et al. MRTX1719 is an MTA-cooperative PRMT5 inhibitor that exhibits synthetic lethality in preclinical models and patients with MTAP-deleted cancer. Cancer Discov. 2023;13(11):2412-2431. — `PMID 37552839; DOI 10.1158/2159-8290.CD-23-0669`
- Rodon J, Prenen H, Sacher A, et al. First-in-human study of AMG 193, an MTA-cooperative PRMT5 inhibitor, in patients with MTAP-deleted solid tumors: results from phase I dose exploration. Ann Oncol. 2024;35(12):1138-1147. — `PMID 39293516; DOI 10.1016/j.annonc.2024.08.2339`
- Pettus LH, Bourbeau M, Tamayo NA, et al. Discovery of AMG 193, an MTA-cooperative PRMT5 inhibitor for the treatment of MTAP-deleted cancers. J Med Chem. 2025;68(7):6932-6954. (~40x selectivity in isogenic HCT116; MTAP deletion in 10-15% of human cancers.) — `PMID 40146197; DOI 10.1021/acs.jmedchem.4c03121`
- Ikushima H, Watanabe K, Shinozaki-Ushiku A, Oda K, Kage H. Pan-cancer clinical and molecular landscape of MTAP deletion in nationwide and international comprehensive genomic data. ESMO Open. 2025;10(4):104535. — `PMID 40138743; DOI 10.1016/j.esmoop.2025.104535`
- Briggs KJ, Cottrell KM, Tonini MR, et al. TNG908 is a brain-penetrant, MTA-cooperative PRMT5 inhibitor developed for the treatment of MTAP-deleted cancers. Transl Oncol. 2025;52:102264. — `PMID 39756156; DOI 10.1016/j.tranon.2024.102264`
- Wang Y, Sun X, Ma R, et al. Inhibitory effect of PRMT5/MTA inhibitor on MTAP-deficient glioma may be influenced by surrounding normal cells. Cancer Med. 2024;13(24):e70526. (MTAP-expressing stroma metabolises MTA, attenuating MTA-cooperative inhibitor activity in vivo.) — `PMID 39711357; DOI 10.1002/cam4.70526`
- Kalev P, Hyer ML, Gross S, et al. MAT2A inhibition blocks the growth of MTAP-deleted cancer cells by reducing PRMT5-dependent mRNA splicing and inducing DNA damage. Cancer Cell. 2021;39(2):209-224.e11. — `PMID 33450196; DOI 10.1016/j.ccell.2020.12.010`

---

## 15. TMB ≥10 mut/Mb is assay-specific

**Verdict:** Contested Hypothesis — real research, but the framing states a contested idea as settled

### Corrected claim

A tissue tumour mutational burden (tTMB) of ≥10 mutations/megabase identifies a subgroup
of previously treated advanced solid tumours enriched for response to pembrolizumab
monotherapy, and on 16 June 2020 the US FDA granted pembrolizumab an accelerated,
tumour-agnostic approval on that basis. The evidence was the prospective biomarker
analysis of the single-arm phase 2 KEYNOTE-158 trial: of 790 evaluable patients across
ten tumour-type cohorts, 102 (13%) were tTMB-high, with an objective response rate of
29% (95% CI 21–39) versus 6% (95% CI 5–8) in the 688 non-tTMB-high patients; 57% of
responses lasted ≥12 months. Because the trial had no randomised comparator, this
demonstrates response enrichment, not a demonstrated survival benefit. Two caveats a
clinician will insist on. First, the "10" is assay-defined, not biology-defined. TMB in
KEYNOTE-158 was measured only with FoundationOne CDx (F1CDx), which the FDA approved the
same day as the companion diagnostic for this indication; per its FDA technical
labelling F1CDx counts both synonymous and non-synonymous substitutions and short indels
at ≥5% allele frequency across roughly 0.8 Mb of coding sequence, after filtering
germline and known driver variants — a counting rule different from the exome convention
(the FDA treated ≥10 mut/Mb by F1CDx as roughly equivalent to ≥175 mutations/exome by
WES). Published harmonisation work confirms the same nominal number is not
interchangeable across panels: the Friends of Cancer Research TMB Harmonization Project
showed in silico that panel–WES variability grows as TMB rises (phase I, Merino 2020)
and that panels below ~667 kb cannot hold adequate agreement at cut-offs used in
practice, requiring assay-specific calibration (phase II, Vega 2021); the German QuIP
study mapped a WES cut-point of 199 missense mutations onto panel cut-points ranging
from 7.8 to 12.6 mut/Mb, with only 74.9% classification agreement; and a head-to-head
study in 96 NSCLC samples found that to reproduce FoundationOne's 10 mut/Mb at >88%
sensitivity, the cut-off had to be lowered to 7.85 mut/Mb (TruSight Oncology 500) and
8.38 mut/Mb (Oncomine TML), with roughly one third of patients misclassified when the
same numeric threshold was applied across assays. Second, the threshold is soft even
within F1CDx and the pan-tumour generalisation is contested: within KEYNOTE-158's TMB-
high group, ORR was 13% (95% CI 4–29) for 10–<13 mut/Mb versus 37% (95% CI 26–50) for
≥13 mut/Mb; McGrail et al. (2021) found that in cancer types where CD8 T-cell
infiltration does not track neoantigen load (e.g. breast, prostate, glioma) TMB-high
tumours had a 15.3% ORR and did no better than TMB-low (OR 0.46, 95% CI 0.24–0.88); and
in NSCLC, CheckMate 227 met its TMB-selected progression-free survival endpoint (HR
0.58) but the subsequent overall-survival analysis showed benefit irrespective of TMB,
after which TMB was dropped as a selection biomarker there. Adoption is therefore not
uniformly "international": FDA approval remains accelerated and conditional on a
confirmatory post-marketing requirement, ESMO's Precision Medicine Working Group
recommends TMB testing only in specific histologies (cervical, well/moderately
differentiated neuroendocrine, salivary, thyroid and vulvar cancers), and the EMA has
never approved a TMB-based indication for pembrolizumab in the EU.

### What the original got wrong

WHAT THE SNIPPET GETS RIGHT: The two load-bearing facts check out exactly. (1) The
threshold is ≥10 mut/Mb and it was operationalised on FoundationOne CDx — Marabelle 2020
states "Tissue TMB (tTMB) was assessed ... using the FoundationOne CDx assay" and "The
prespecified definition of tTMB-high status was at least 10 mutations per megabase." (2)
FDA granted accelerated approval on 16 June 2020 and approved F1CDx as the companion
diagnostic at the 10 mut/Mb cut-point the same day (sPMA P170019/S016). (3) Cross-panel
non-interchangeability is real and quantified in peer-reviewed work — this part of the
claim is if anything understated.

WHERE IT OVERSTATES — four things a clinician would push back on:

1. "Predicts immunotherapy benefit" is too strong for the evidence cited. KEYNOTE-158
was single-arm, non-randomised. It shows response ENRICHMENT (ORR 29% vs 6%), not
benefit versus an alternative. The FDA approval summary itself says the approval rested
on ORR/DoR plus "a scientific understanding of the effects of PD-1 inhibition," and
explicitly notes "the potential exists for future modification or withdrawal of the
indication." The one randomised trial that prospectively selected on ≥10 mut/Mb by F1CDx
(CheckMate 227) met its PFS endpoint (HR 0.58, 97.5% CI 0.41–0.81) but the later OS
analysis showed benefit irrespective of TMB, and TMB was subsequently abandoned as a
selection biomarker in NSCLC. Say "enriches for response" or "identifies a subgroup with
higher response rates," not "predicts benefit."

2. The "10" is soft even on the assay it was defined for. Within KEYNOTE-158's own TMB-
high group, ORR was 13% (95% CI 4–29) at 10–<13 mut/Mb versus 37% (95% CI 26–50) at ≥13
(n=32 and n=70). FDA required a post-marketing study specifically to characterise the
10–13 band. So the cross-assay problem the claim describes sits on top of a threshold
that is already unstable within the reference assay.

3. "Entered international documents" overstates adoption. FDA: yes, but accelerated and
conditional (PMR 3871-1, still listed as ongoing in Merck's Oct-2024 public
postmarketing-requirements disclosure). ESMO PMWG (2020, reaffirmed in scope 2024):
recommends TMB testing only in cervical, well/moderately differentiated neuroendocrine,
salivary, thyroid and vulvar cancers — a histology-restricted recommendation, not a pan-
tumour one. EMA: no TMB-based indication for pembrolizumab exists in the EU product
information. Writing "international documents" without that split will read as sloppy to
a European clinician.

4. "The same 10 can mean different biology" is directionally right but should be given
its actual numbers rather than left as an assertion. Concretely: QuIP mapped a WES cut
of 199 missense mutations to panel cut-points spanning 7.8–12.6 mut/Mb across six panels
(74.9% classification agreement); Ramos-Paradas found the equivalents of FoundationOne's
10 mut/Mb were 7.85 (TSO500) and 8.38 (Oncomine TML), with ~20% of FO-defined TMB-high
NSCLCs reclassified as low by the other panels and "around one third" of patients
misclassified overall when the same numeric threshold was reused; Vega/FoCR phase II
found panels <667 kb cannot maintain adequate agreement and published a calibration
tool. Mechanism, per FoCR/QuIP: panel size, gene content, germline filtering, driver
filtering, VAF cut-off, deamination correction and bioinformatics pipeline all move the
number.

ESTABLISHED VS CONTESTED: That panel-based TMB values are assay-dependent and require
calibration is ESTABLISHED and uncontroversial. That TMB-H ≥10 identifies pembrolizumab
responders in the specific KEYNOTE-158 histologies is ESTABLISHED as an observation.
That ≥10 mut/Mb is a valid tumour-agnostic predictive biomarker is CONTESTED — McGrail
2021 (Ann Oncol) found that in cancer types where CD8 T-cell level does not correlate
with neoantigen load (breast, prostate, glioma), TMB-H tumours achieved only 15.3% ORR
(95% CI 9.2–23.4) and did significantly WORSE than TMB-low (OR 0.46, 95% CI 0.24–0.88,
P=0.02), while in melanoma/lung/bladder TMB-H gave 39.8% ORR (OR 4.1). None of
KEYNOTE-158's ten cohorts were breast, prostate or glioma, so the pan-tumour
extrapolation is inference, not data. Hence the CONTESTED_HYPOTHESIS verdict rather than
SOLID.

ONE NUMBER TO RE-VERIFY BEFORE PUBLICATION: the "~0.8 Mb of coding region" figure for
F1CDx comes from the FoundationOne CDx FDA technical labelling (P170019), which I could
only confirm via search extraction of the label text, not by reading the PDF directly
(the PDF would not render). Note that Chalmers 2017 — the foundational TMB-landscape
paper — describes ~1.1 Mb of coding genome for the earlier research-use FoundationOne
assay, so 1.1 Mb and 0.8 Mb both circulate in the literature for "Foundation Medicine
TMB" and refer to different assay versions. If the site states a specific Mb figure, pin
it to the current F1CDx label version and say which assay it refers to.

OTHER FACTUAL DETAILS WORTH KEEPING STRAIGHT: 1073 enrolled / 1066 treated / 790 in the
efficacy analysis / 102 TMB-H (13%); ten tumour-type cohorts enrolled, responses
observed in 8 tumour types per FDA review (FDA's abstract says the TMB-H subset "spanned
nine different tumour types"); median follow-up 37.1 months; 4 complete responses
(3.9%); excluding the 14 MSI-H patients the TMB-H ORR was 26.1%, so the signal is not
merely MSI-H in disguise; TMB was missing for 260/1050 (25%) of patients, a limitation
FDA flagged.

### Sources

- Marabelle A, Fakih M, Lopez J, et al. Association of tumour mutational burden with outcomes in patients with advanced solid tumours treated with pembrolizumab: prospective biomarker analysis of the multicohort, open-label, phase 2 KEYNOTE-158 study. Lancet Oncol. 2020;21(10):1353-1365. — `PMID 32919526; DOI 10.1016/S1470-2045(20)30445-9`
- Marcus L, Fashoyin-Aje LA, Donoghue M, et al. FDA Approval Summary: Pembrolizumab for the Treatment of Tumor Mutational Burden-High Solid Tumors. Clin Cancer Res. 2021;27(17):4685-4689. — `PMID 34083238; DOI 10.1158/1078-0432.CCR-21-0327`
- Chalmers ZR, Connelly CF, Fabrizio D, et al. Analysis of 100,000 human cancer genomes reveals the landscape of tumor mutational burden. Genome Med. 2017;9(1):34. — `PMID 28420421; DOI 10.1186/s13073-017-0424-2`
- Foundation Medicine, Inc. FoundationOne CDx Technical Information (FDA PMA P170019 labeling) — TMB calculation methodology and TMB-High cut-point. — `https://www.accessdata.fda.gov/cdrh_docs/pdf17/P170019S048D.pdf`
- Merino DM, McShane LM, Fabrizio D, et al. Establishing guidelines to harmonize tumor mutational burden (TMB): in silico assessment of variation in TMB quantification across diagnostic platforms: phase I of the Friends of Cancer Research TMB Harmonization Project. J Immunother Cancer. 2020;8(1):e000147. — `PMID 32217756; DOI 10.1136/jitc-2019-000147`
- Vega DM, Yee LM, McShane LM, et al. Aligning tumor mutational burden (TMB) quantification across diagnostic platforms: phase II of the Friends of Cancer Research TMB Harmonization Project. Ann Oncol. 2021;32(12):1626-1636. (Erratum: Ann Oncol. 2024;35(1):145, PMID 37558578) — `PMID 34606929; DOI 10.1016/j.annonc.2021.09.016`
- Stenzinger A, Endris V, Budczies J, et al. Harmonization and Standardization of Panel-Based Tumor Mutational Burden Measurement: Real-World Results and Recommendations of the Quality in Pathology Study. J Thorac Oncol. 2020;15(7):1177-1189. — `PMID 32119917; DOI 10.1016/j.jtho.2020.01.023`
- Ramos-Paradas J, Hernández-Prieto S, Lora D, et al. Tumor mutational burden assessment in non-small-cell lung cancer samples: results from the TMB2 harmonization project comparing three NGS panels. J Immunother Cancer. 2021;9(5):e001904. — `PMID 33963008; DOI 10.1136/jitc-2020-001904`
- McGrail DJ, Pilié PG, Rashid NU, et al. High tumor mutation burden fails to predict immune checkpoint blockade response across all cancer types. Ann Oncol. 2021;32(5):661-672. — `PMID 33736924; DOI 10.1016/j.annonc.2021.02.006`
- Hellmann MD, Ciuleanu TE, Pluzanski A, et al. Nivolumab plus Ipilimumab in Lung Cancer with a High Tumor Mutational Burden. N Engl J Med. 2018;378(22):2093-2104. — `PMID 29658845; DOI 10.1056/NEJMoa1801946`
- Hellmann MD, Paz-Ares L, Bernabe Caro R, et al. Nivolumab plus Ipilimumab in Advanced Non-Small-Cell Lung Cancer. N Engl J Med. 2019;381(21):2020-2031. — `PMID 31562796; DOI 10.1056/NEJMoa1910231`
- Mosele F, Remon J, Mateo J, et al. Recommendations for the use of next-generation sequencing (NGS) for patients with metastatic cancers: a report from the ESMO Precision Medicine Working Group. Ann Oncol. 2020;31(11):1491-1505. — `PMID 32853681; DOI 10.1016/j.annonc.2020.07.014`
- Mosele MF, Westphalen CB, Stenzinger A, et al. Recommendations for the use of next-generation sequencing (NGS) for patients with advanced cancer in 2024: a report from the ESMO Precision Medicine Working Group. Ann Oncol. 2024;35(7):588-606. — `PMID 38834388; DOI 10.1016/j.annonc.2024.04.005`
- European Medicines Agency. Keytruda (pembrolizumab) EPAR — Product information / authorised therapeutic indications (no TMB-based indication). — `https://www.ema.europa.eu/en/medicines/human/EPAR/keytruda`

---
