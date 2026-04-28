# Trials Needing Source Ingest

Extracted from 324 source_stub_needed rows in citation-report-v2.yaml. 47 unique trials identified, sorted by usage count (most-cited first → highest priority).

Each trial below needs a `SRC-<TRIAL>-<AUTHOR>-<YEAR>` entity in `knowledge_base/hosted/content/sources/`. Use PubMed/CIViC/etc. to find the pivotal publication; create the Source stub via `source_stub.yaml` template; ingest per `specs/SOURCE_INGESTION_SPEC.md`.

> **⚠️ False-positive warning:** trial names below are extracted from Codex's `verified_rationale` field. In rows where the v1 audit did not identify a specific trial, Codex sometimes labels generic words (e.g. 'CROSS', 'PARADIGM') as trial names — these may NOT correspond to actual RCTs. Quick sanity-check: if a trial spans many unrelated disease domains (e.g. FLT3 AML + esophageal + melanoma), it's likely a false positive. Verify each trial-name vs the cited entity's domain before ingesting.

---

## CROSS

**Cited by:** 16 finding(s)
**Distinct entities:** 16

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0232` → `BMA-FLT3-F691L-AML` (bma_flt3_f691l_aml.yaml)
- `CV914-0297` → `IND-MTC-ADVANCED-1L-SELPERCATINIB` (ind_mtc_advanced_1l_selpercatinib.yaml)
- `CV914-0445` → `IND-ESOPH-ADJUVANT-NIVOLUMAB-POST-CROSS` (ind_esoph_adjuvant_nivolumab_post_cross.yaml)
- `CV914-0450` → `IND-MELANOMA-BRAF-METASTATIC-1L-DABRA-TRAME` (ind_melanoma_braf_metastatic_1l_dabra_trame.yaml)
- `CV914-0474` → `REG-ADT-ABIRATERONE` (reg_adt_abiraterone.yaml)
- `CV914-0491` → `REG-NIVO-ADJUVANT-ESOPH` (nivolumab_adjuvant_esophageal.yaml)
- `CV914-0498` → `REG-PEMBRO-CHEMO-NSCLC-NONSQ` (reg_pembro_chemo_nsclc_nonsq.yaml)
- `CV914-0502` → `REG-RICE-BURKITT` (reg_rice_burkitt.yaml)
- `CV914-0561` → `IND-BURKITT-2L-RDHAP-ASCT` (ind_burkitt_2l_rdhap_asct.yaml)
- `CV914-0568` → `IND-CML-3L-ASCIMINIB` (ind_cml_3l_asciminib.yaml)
- ... +6 more

---

## PARADIGM

**Cited by:** 16 finding(s)
**Distinct entities:** 16

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0007` → `BMA-BCR-ABL1-P210-BALL` (bma_bcr_abl1_p210_ball.yaml)
- `CV914-0107` → `IND-OVARIAN-MAINT-BEV` (ind_ovarian_maint_bev.yaml)
- `CV914-0292` → `IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO` (ind_endometrial_advanced_1l_pembro_chemo.yaml)
- `CV914-0300` → `IND-NSCLC-ALK-MAINT-ALECTINIB` (ind_nsclc_alk_maint_alectinib.yaml)
- `CV914-0318` → `BMA-BCR-ABL1-P210-CML` (bma_bcr_abl1_p210_cml.yaml)
- `CV914-0424` → `IND-ALCL-MAINTENANCE-BV-POST-ASCT` (ind_alcl_maintenance_bv_post_asct.yaml)
- `CV914-0472` → `IND-UROTHELIAL-METASTATIC-1L-EV-PEMBRO` (ind_urothelial_metastatic_1l_ev_pembro.yaml)
- `CV914-0486` → `REG-EV-PEMBRO-UROTHELIAL` (reg_ev_pembro_urothelial.yaml)
- `CV914-0537` → `BMA-NTRK-FUSION-IFS` (bma_ntrk_fusion_ifs.yaml)
- `CV914-0562` → `IND-BURKITT-2L-RICE-ASCT` (ind_burkitt_2l_rice_asct.yaml)
- ... +6 more

---

## RUBY

**Cited by:** 16 finding(s)
**Distinct entities:** 16

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0047` → `BMA-MLH1-GERMLINE-ENDOMETRIAL` (bma_mlh1_germline_endometrial.yaml)
- `CV914-0052` → `BMA-MLH1-SOMATIC-ENDOMETRIAL` (bma_mlh1_somatic_endometrial.yaml)
- `CV914-0057` → `BMA-MSH2-GERMLINE-ENDOMETRIAL` (bma_msh2_germline_endometrial.yaml)
- `CV914-0062` → `BMA-MSH2-SOMATIC-ENDOMETRIAL` (bma_msh2_somatic_endometrial.yaml)
- `CV914-0067` → `BMA-MSH6-GERMLINE-ENDOMETRIAL` (bma_msh6_germline_endometrial.yaml)
- `CV914-0072` → `BMA-MSH6-SOMATIC-ENDOMETRIAL` (bma_msh6_somatic_endometrial.yaml)
- `CV914-0082` → `BMA-PMS2-GERMLINE-ENDOMETRIAL` (bma_pms2_germline_endometrial.yaml)
- `CV914-0087` → `BMA-PMS2-SOMATIC-ENDOMETRIAL` (bma_pms2_somatic_endometrial.yaml)
- `CV914-0136` → `BMA-FGFR2-MUTATION-ENDOMETRIAL` (bma_fgfr2_mutation_endometrial.yaml)
- `CV914-0220` → `BMA-EPCAM-GERMLINE-ENDOMETRIAL` (bma_epcam_germline_endometrial.yaml)
- ... +6 more

---

## NRG-GY018

**Cited by:** 14 finding(s)
**Distinct entities:** 14

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0048` → `BMA-MLH1-GERMLINE-ENDOMETRIAL` (bma_mlh1_germline_endometrial.yaml)
- `CV914-0053` → `BMA-MLH1-SOMATIC-ENDOMETRIAL` (bma_mlh1_somatic_endometrial.yaml)
- `CV914-0058` → `BMA-MSH2-GERMLINE-ENDOMETRIAL` (bma_msh2_germline_endometrial.yaml)
- `CV914-0063` → `BMA-MSH2-SOMATIC-ENDOMETRIAL` (bma_msh2_somatic_endometrial.yaml)
- `CV914-0068` → `BMA-MSH6-GERMLINE-ENDOMETRIAL` (bma_msh6_germline_endometrial.yaml)
- `CV914-0073` → `BMA-MSH6-SOMATIC-ENDOMETRIAL` (bma_msh6_somatic_endometrial.yaml)
- `CV914-0083` → `BMA-PMS2-GERMLINE-ENDOMETRIAL` (bma_pms2_germline_endometrial.yaml)
- `CV914-0088` → `BMA-PMS2-SOMATIC-ENDOMETRIAL` (bma_pms2_somatic_endometrial.yaml)
- `CV914-0137` → `BMA-FGFR2-MUTATION-ENDOMETRIAL` (bma_fgfr2_mutation_endometrial.yaml)
- `CV914-0294` → `IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO` (ind_endometrial_advanced_1l_pembro_chemo.yaml)
- ... +4 more

---

## PAOLA-1

**Cited by:** 10 finding(s)
**Distinct entities:** 10

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0013` → `BMA-BRCA1-GERMLINE-OVARIAN` (bma_brca1_germline_ovarian.yaml)
- `CV914-0092` → `BMA-RAD51B-GERMLINE-OVARIAN` (bma_rad51b_germline_ovarian.yaml)
- `CV914-0097` → `BMA-RAD51C-GERMLINE-OVARIAN` (bma_rad51c_germline_ovarian.yaml)
- `CV914-0102` → `BMA-RAD51D-GERMLINE-OVARIAN` (bma_rad51d_germline_ovarian.yaml)
- `CV914-0109` → `IND-OVARIAN-MAINT-BEV` (ind_ovarian_maint_bev.yaml)
- `CV914-0148` → `BMA-PALB2-GERMLINE-OVARIAN` (bma_palb2_germline_ovarian.yaml)
- `CV914-0172` → `BMA-BARD1-GERMLINE-OVARIAN` (bma_bard1_germline_ovarian.yaml)
- `CV914-0465` → `IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-OLAP` (ind_ovarian_advanced_1l_carbo_pacli_hrd_olap.yaml)
- `CV914-0467` → `IND-OVARIAN-MAINTENANCE-OLAPARIB` (ind_ovarian_maintenance_olaparib.yaml)
- `CV914-0495` → `REG-OLAPARIB-MAINT-OVARIAN` (olaparib_maintenance_ovarian.yaml)

---

## AIDA

**Cited by:** 6 finding(s)
**Distinct entities:** 6

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0427` → `IND-APL-1L-ATRA-ATO-IDA` (ind_apl_1l_atra_ato_ida.yaml)
- `CV914-0554` → `IND-APL-1L-ATRA-ATO` (ind_apl_1l_atra_ato.yaml)
- `CV914-0555` → `IND-APL-SALVAGE-ATRA-ATO` (ind_apl_salvage_atra_ato.yaml)
- `CV914-0616` → `REG-ATRA-ATO-APL` (atra_ato_apl.yaml)
- `CV914-0617` → `REG-ATRA-ATO-APL-SALVAGE` (reg_atra_ato_apl_salvage.yaml)
- `CV914-0618` → `REG-ATRA-ATO-IDA-APL` (atra_ato_ida_apl.yaml)

---

## CODEBREAK

**Cited by:** 6 finding(s)
**Distinct entities:** 6

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0144` → `BMA-KRAS-G12C-PDAC` (bma_kras_g12c_pdac.yaml)
- `CV914-0238` → `BMA-KRAS-G12C-CRC` (bma_kras_g12c_crc.yaml)
- `CV914-0241` → `BMA-KRAS-G12C-NSCLC` (bma_kras_g12c_nsclc.yaml)
- `CV914-0362` → `BMA-KRAS-G12C-OVARIAN` (bma_kras_g12c_ovarian.yaml)
- `CV914-0595` → `IND-NSCLC-KRAS-G12C-MET-2L` (ind_nsclc_kras_g12c_met_2l.yaml)
- `CV914-0646` → `REG-SOTORASIB-KRAS` (reg_sotorasib_kras.yaml)

---

## MAGNITUDE

**Cited by:** 4 finding(s)
**Distinct entities:** 4

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0018` → `BMA-BRCA1-GERMLINE-PROSTATE` (bma_brca1_germline_prostate.yaml)
- `CV914-0028` → `BMA-BRCA2-GERMLINE-PROSTATE` (bma_brca2_germline_prostate.yaml)
- `CV914-0229` → `BMA-FLT3-D835-AML` (bma_flt3_d835_aml.yaml)
- `CV914-0468` → `IND-PROSTATE-MCRPC-1L-PARPI` (ind_prostate_mcrpc_1l_parpi.yaml)

---

## MARIPOSA

**Cited by:** 4 finding(s)
**Distinct entities:** 4

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0032` → `BMA-EGFR-C797S-NSCLC` (bma_egfr_c797s_nsclc.yaml)
- `CV914-0044` → `BMA-EGFR-L858R-NSCLC` (bma_egfr_l858r_nsclc.yaml)
- `CV914-0364` → `BMA-MET-AMP-NSCLC` (bma_met_amp_nsclc.yaml)
- `CV914-0457` → `IND-NSCLC-EGFR-MAINT-OSIMERTINIB` (ind_nsclc_egfr_maint_osimertinib.yaml)

---

## OLYMPIA

**Cited by:** 4 finding(s)
**Distinct entities:** 4

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0022` → `BMA-BRCA2-GERMLINE-BREAST` (bma_brca2_germline_breast.yaml)
- `CV914-0124` → `BMA-BRCA1-GERMLINE-BREAST` (bma_brca1_germline_breast.yaml)
- `CV914-0434` → `IND-BREAST-TNBC-EARLY-NEOADJUVANT` (ind_breast_tnbc_early_neoadjuvant.yaml)
- `CV914-0492` → `REG-OLAPARIB-BREAST` (reg_olaparib_breast.yaml)

---

## PROPEL

**Cited by:** 4 finding(s)
**Distinct entities:** 4

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0017` → `BMA-BRCA1-GERMLINE-PROSTATE` (bma_brca1_germline_prostate.yaml)
- `CV914-0027` → `BMA-BRCA2-GERMLINE-PROSTATE` (bma_brca2_germline_prostate.yaml)
- `CV914-0602` → `IND-PTCL-2L-PRALATREXATE` (ind_ptcl_2l_pralatrexate.yaml)
- `CV914-0643` → `REG-PRALATREXATE-PTCL` (reg_pralatrexate_ptcl.yaml)

---

## THOR

**Cited by:** 4 finding(s)
**Distinct entities:** 4

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0224` → `BMA-FGFR2-MUTATION-UROTHELIAL` (bma_fgfr2_mutation_urothelial.yaml)
- `CV914-0227` → `BMA-FGFR3-TACC3-UROTHELIAL` (bma_fgfr3_tacc3_urothelial.yaml)
- `CV914-0336` → `BMA-FGFR3-R248C-UROTHELIAL` (bma_fgfr3_r248c_urothelial.yaml)
- `CV914-0338` → `BMA-FGFR3-S249C-UROTHELIAL` (bma_fgfr3_s249c_urothelial.yaml)

---

## ARASENS

**Cited by:** 3 finding(s)
**Distinct entities:** 3

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0171` → `IND-PROSTATE-MHSPC-1L-ARPI-DOUBLET` (ind_prostate_mhspc_1l_arpi_doublet.yaml)
- `CV914-0600` → `IND-PROSTATE-MHSPC-1L-TRIPLET` (ind_prostate_mhspc_1l_triplet.yaml)
- `CV914-0611` → `REG-ADT-DAROLUTAMIDE-DOCETAXEL` (reg_adt_darolutamide_docetaxel.yaml)

---

## GOG-218

**Cited by:** 3 finding(s)
**Distinct entities:** 3

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0110` → `IND-OVARIAN-MAINT-BEV` (ind_ovarian_maint_bev.yaml)
- `CV914-0463` → `IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-NEG` (ind_ovarian_advanced_1l_carbo_pacli_hrd_neg.yaml)
- `CV914-0621` → `REG-CARBO-PACLI-OVARIAN` (carboplatin_paclitaxel_ovarian.yaml)

---

## KEYNOTE-522

**Cited by:** 3 finding(s)
**Distinct entities:** 3

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0286` → `BMA-TP53-MUT-BREAST` (bma_tp53_mut_breast.yaml)
- `CV914-0435` → `IND-BREAST-TNBC-EARLY-NEOADJUVANT` (ind_breast_tnbc_early_neoadjuvant.yaml)
- `CV914-0639` → `REG-PEMBRO-CHEMO-TNBC-NEOADJUVANT` (reg_pembro_chemo_tnbc_neoadjuvant.yaml)

---

## MAGNOLIA

**Cited by:** 3 finding(s)
**Distinct entities:** 3

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0262` → `BMA-MYD88-L265P-HCV-MZL` (bma_myd88_l265p_hcv_mzl.yaml)
- `CV914-0265` → `BMA-MYD88-L265P-NODAL-MZL` (bma_myd88_l265p_nodal_mzl.yaml)
- `CV914-0268` → `BMA-MYD88-L265P-SPLENIC-MZL` (bma_myd88_l265p_splenic_mzl.yaml)

---

## PRODIGE

**Cited by:** 3 finding(s)
**Distinct entities:** 3

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0574` → `IND-CRC-METASTATIC-MAINT-FOLFIRI-BEV` (ind_crc_metastatic_maint_folfiri_bev.yaml)
- `CV914-0598` → `IND-PDAC-METASTATIC-1L-FOLFIRINOX` (ind_pdac_metastatic_1l_folfirinox.yaml)
- `CV914-0631` → `REG-FOLFIRINOX` (folfirinox.yaml)

---

## STARTRK

**Cited by:** 3 finding(s)
**Distinct entities:** 3

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0535` → `BMA-NTRK-ETV6-SALIVARY` (bma_ntrk_etv6_salivary.yaml)
- `CV914-0539` → `BMA-NTRK-FUSION-SALIVARY` (bma_ntrk_fusion_salivary.yaml)
- `CV914-0540` → `BMA-NTRK-FUSION-THYROID-PAPILLARY` (bma_ntrk_fusion_thyroid_papillary.yaml)

---

## ALINA

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0117` → `BMA-ALK-FUSION-NSCLC` (bma_alk_fusion_nsclc.yaml)
- `CV914-0477` → `REG-ALECTINIB-NSCLC` (reg_alectinib_nsclc.yaml)

---

## BFORE

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0291` → `IND-CML-1L-2GEN-TKI` (ind_cml_1l_2gen_tki.yaml)
- `CV914-0303` → `REG-2GEN-TKI-CML` (dasatinib_or_nilotinib_cml.yaml)

---

## BLC2001

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0223` → `BMA-FGFR2-MUTATION-UROTHELIAL` (bma_fgfr2_mutation_urothelial.yaml)
- `CV914-0226` → `BMA-FGFR3-TACC3-UROTHELIAL` (bma_fgfr3_tacc3_urothelial.yaml)

---

## CHECKMATE-214

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0603` → `IND-RCC-METASTATIC-1L-NIVO-IPI` (ind_rcc_metastatic_1l_nivo_ipi.yaml)
- `CV914-0636` → `REG-NIVO-IPI-RCC` (reg_nivo_ipi_rcc.yaml)

---

## CHECKMATE-577

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0444` → `IND-ESOPH-ADJUVANT-NIVOLUMAB-POST-CROSS` (ind_esoph_adjuvant_nivolumab_post_cross.yaml)
- `CV914-0490` → `REG-NIVO-ADJUVANT-ESOPH` (nivolumab_adjuvant_esophageal.yaml)

---

## DASISION

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0290` → `IND-CML-1L-2GEN-TKI` (ind_cml_1l_2gen_tki.yaml)
- `CV914-0302` → `REG-2GEN-TKI-CML` (dasatinib_or_nilotinib_cml.yaml)

---

## ENESTND

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0289` → `IND-CML-1L-2GEN-TKI` (ind_cml_1l_2gen_tki.yaml)
- `CV914-0301` → `REG-2GEN-TKI-CML` (dasatinib_or_nilotinib_cml.yaml)

---

## ENZAMET

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0169` → `IND-PROSTATE-MHSPC-1L-ARPI-DOUBLET` (ind_prostate_mhspc_1l_arpi_doublet.yaml)
- `CV914-0612` → `REG-ADT-ENZALUTAMIDE` (reg_adt_enzalutamide.yaml)

---

## EV-302

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0473` → `IND-UROTHELIAL-METASTATIC-1L-EV-PEMBRO` (ind_urothelial_metastatic_1l_ev_pembro.yaml)
- `CV914-0487` → `REG-EV-PEMBRO-UROTHELIAL` (reg_ev_pembro_urothelial.yaml)

---

## FIRE-3

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0488` → `REG-FOLFOX-CETUX` (folfox_cetuximab.yaml)
- `CV914-0570` → `IND-CRC-METASTATIC-1L-RAS-WT-LEFT` (ind_crc_metastatic_1l_ras_wt_left.yaml)

---

## IMPOWER133

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0471` → `IND-SCLC-EXTENSIVE-1L` (ind_sclc_extensive_1l.yaml)
- `CV914-0628` → `REG-EP-ATEZO-SCLC` (reg_ep_atezo_sclc.yaml)

---

## KEYNOTE-426

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0604` → `IND-RCC-METASTATIC-1L-PEMBRO-AXI` (ind_rcc_metastatic_1l_pembro_axi.yaml)
- `CV914-0637` → `REG-PEMBRO-AXI-RCC` (reg_pembro_axi_rcc.yaml)

---

## KEYNOTE-590

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0577` → `IND-ESOPH-METASTATIC-2L-NIVO-SQUAMOUS` (ind_esoph_metastatic_2l_nivo_squamous.yaml)
- `CV914-0640` → `REG-PEMBRO-MONO-ESOPH-2L` (reg_pembro_mono_esoph_2l.yaml)

---

## LATITUDE

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0168` → `IND-PROSTATE-MHSPC-1L-ARPI-DOUBLET` (ind_prostate_mhspc_1l_arpi_doublet.yaml)
- `CV914-0475` → `REG-ADT-ABIRATERONE` (reg_adt_abiraterone.yaml)

---

## PACIFIC

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0597` → `IND-NSCLC-STAGE-III-PACIFIC` (ind_nsclc_stage_iii_pacific.yaml)
- `CV914-0626` → `REG-DURVA-CONSOLIDATION-PACIFIC` (reg_durva_consolidation_pacific.yaml)

---

## STUPP

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0583` → `IND-GBM-NEWLY-DIAGNOSED-STUPP` (ind_gbm_newly_diagnosed_stupp.yaml)
- `CV914-0647` → `REG-STUPP-TMZ` (stupp_temozolomide.yaml)

---

## TALAPRO-2

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0029` → `BMA-BRCA2-GERMLINE-PROSTATE` (bma_brca2_germline_prostate.yaml)
- `CV914-0469` → `IND-PROSTATE-MCRPC-1L-PARPI` (ind_prostate_mcrpc_1l_parpi.yaml)

---

## TITAN

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0170` → `IND-PROSTATE-MHSPC-1L-ARPI-DOUBLET` (ind_prostate_mhspc_1l_arpi_doublet.yaml)
- `CV914-0610` → `REG-ADT-APALUTAMIDE` (reg_adt_apalutamide.yaml)

---

## TRIANGLE

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0132` → `BMA-CCND1-T1114-MCL` (bma_ccnd1_t1114_mcl.yaml)
- `CV914-0160` → `BMA-TP53-MUT-MCL` (bma_tp53_mut_mcl.yaml)

---

## TROPICS-02

**Cited by:** 2 finding(s)
**Distinct entities:** 2

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0167` → `IND-BREAST-HR-POS-MAINT-CDK46I` (ind_breast_hr_pos_maint_cdk46i.yaml)
- `CV914-0505` → `REG-SACITUZUMAB` (reg_sacituzumab.yaml)

---

## AGILE

**Cited by:** 1 finding(s)
**Distinct entities:** 1

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0344` → `BMA-IDH1-R132H-AML` (bma_idh1_r132h_aml.yaml)

---

## BRIGHT

**Cited by:** 1 finding(s)
**Distinct entities:** 1

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0556` → `IND-ATLL-2L-MOGAMULIZUMAB` (ind_atll_2l_mogamulizumab.yaml)

---

## CRYSTAL

**Cited by:** 1 finding(s)
**Distinct entities:** 1

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0489` → `REG-FOLFOX-CETUX` (folfox_cetuximab.yaml)

---

## ICON7

**Cited by:** 1 finding(s)
**Distinct entities:** 1

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0111` → `IND-OVARIAN-MAINT-BEV` (ind_ovarian_maint_bev.yaml)

---

## IMPOWER150

**Cited by:** 1 finding(s)
**Distinct entities:** 1

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0593` → `IND-NSCLC-2L-DOCETAXEL-RAMUCIRUMAB` (ind_nsclc_2l_docetaxel_ramucirumab.yaml)

---

## MONUMENTAL-1

**Cited by:** 1 finding(s)
**Distinct entities:** 1

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0511` → `REG-TECLISTAMAB` (reg_teclistamab.yaml)

---

## PAPILLON

**Cited by:** 1 finding(s)
**Distinct entities:** 1

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0214` → `BMA-EGFR-EX20INS-NSCLC` (bma_egfr_ex20ins_nsclc.yaml)

---

## SHINE

**Cited by:** 1 finding(s)
**Distinct entities:** 1

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0609` → `REG-ACALABRUTINIB-RITUXIMAB` (acalabrutinib_rituximab.yaml)

---

## STIL

**Cited by:** 1 finding(s)
**Distinct entities:** 1

**Maintainer todo:**
- [ ] PubMed lookup → identify pivotal publication (lead author, year, journal, DOI, PMID)
- [ ] Decide stable ID: `SRC-<TRIAL>-<AUTHOR>-<YEAR>`
- [ ] Write `knowledge_base/hosted/content/sources/src_<trial>_<author>_<year>.yaml`
- [ ] Update referencing entities: replace placeholder citation with new SRC-* ID

**Referenced findings (first 10):**
- `CV914-0446` → `IND-FL-1L-BR` (ind_fl_1l_br.yaml)

---

## Rows where trial name could not be extracted

153 `source_stub_needed` rows had rationale text that didn't match known trial-name regex patterns. These need manual look-up.

- `CV914-0008`
- `CV914-0015`
- `CV914-0019`
- `CV914-0025`
- `CV914-0030`
- `CV914-0033`
- `CV914-0039`
- `CV914-0045`
- `CV914-0049`
- `CV914-0054`
- `CV914-0059`
- `CV914-0064`
- `CV914-0069`
- `CV914-0074`
- `CV914-0084`
- `CV914-0089`
- `CV914-0099`
- `CV914-0104`
- `CV914-0113`
- `CV914-0119`
- `CV914-0122`
- `CV914-0127`
- `CV914-0130`
- `CV914-0133`
- `CV914-0140`
- `CV914-0146`
- `CV914-0150`
- `CV914-0155`
- `CV914-0159`
- `CV914-0173`
- ... +123 more
