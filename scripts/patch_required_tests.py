#!/usr/bin/env python3
"""Patch required_tests: [] in indication YAML files."""
import os, re

base = 'C:/Users/805/cancer-autoresearch/knowledge_base/hosted/content/indications'

TESTS = {
  'ind_cervical_locally_advanced_crt.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-HBV-SEROLOGY','TEST-HCV-ANTIBODY','TEST-HIV-SEROLOGY','TEST-PREGNANCY','TEST-PDL1-IHC','TEST-PELVIC-MRI','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-ECHO'],
  'ind_cervical_metastatic_1l_pembro_chemo_bev.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-HBV-SEROLOGY','TEST-HCV-ANTIBODY','TEST-HIV-SEROLOGY','TEST-PREGNANCY','TEST-PDL1-IHC','TEST-PELVIC-MRI','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-ECHO'],
  'ind_cholangio_advanced_gem_cis.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-CEA','TEST-AFP','TEST-HBV-SEROLOGY','TEST-HCV-ANTIBODY','TEST-HIV-SEROLOGY','TEST-COAG-PANEL','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-NGS-COMPREHENSIVE'],
  'ind_cholangio_2l_fgfr2_fusion_futibatinib.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-CEA','TEST-HBV-SEROLOGY','TEST-HCV-ANTIBODY','TEST-HIV-SEROLOGY','TEST-COAG-PANEL','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-NGS-COMPREHENSIVE'],
  'ind_cholangio_2l_fgfr2_fusion_infigratinib.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-CEA','TEST-HBV-SEROLOGY','TEST-HCV-ANTIBODY','TEST-HIV-SEROLOGY','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-NGS-COMPREHENSIVE'],
  'ind_cholangio_2l_fgfr2_fusion_pemigatinib.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-CEA','TEST-HBV-SEROLOGY','TEST-HCV-ANTIBODY','TEST-HIV-SEROLOGY','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-NGS-COMPREHENSIVE'],
  'ind_chondrosarcoma_advanced_doxorubicin.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-COAG-PANEL','TEST-ECHO','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-WHOLE-BODY-MRI','TEST-NGS-COMPREHENSIVE'],
  'ind_gist_1l_avapritinib_pdgfra_d842v.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-PET-CT','TEST-ECHO','TEST-NGS-COMPREHENSIVE','TEST-PREGNANCY'],
  'ind_gist_1l_imatinib.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-PET-CT','TEST-ECHO','TEST-NGS-COMPREHENSIVE','TEST-PREGNANCY'],
  'ind_gist_2l_sunitinib.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-ECHO','TEST-NGS-COMPREHENSIVE'],
  'ind_gist_4l_ripretinib.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-ECHO','TEST-NGS-COMPREHENSIVE'],
  'ind_glioma_low_grade_1l_rt_pcv.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-BRAIN-MRI-CONTRAST','TEST-IDH-MUTATION','TEST-MGMT-METHYLATION','TEST-FISH-PANEL','TEST-NGS-COMPREHENSIVE','TEST-PREGNANCY'],
  'ind_hnscc_rm_1l_pembro_chemo.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-HBV-SEROLOGY','TEST-HCV-ANTIBODY','TEST-HIV-SEROLOGY','TEST-PREGNANCY','TEST-PDL1-IHC','TEST-ECHO','TEST-PET-CT','TEST-CT-CHEST-ABDOMEN-PELVIS'],
  'ind_hnscc_rm_1l_pembro_mono_cps_high.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-HBV-SEROLOGY','TEST-HCV-ANTIBODY','TEST-HIV-SEROLOGY','TEST-PREGNANCY','TEST-PDL1-IHC','TEST-ECHO','TEST-PET-CT','TEST-CT-CHEST-ABDOMEN-PELVIS'],
  'ind_ifs_ntrk_larotrectinib.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-FISH-PANEL','TEST-NGS-COMPREHENSIVE','TEST-PREGNANCY'],
  'ind_imt_alk_crizotinib.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-ECHO','TEST-FISH-PANEL','TEST-NGS-COMPREHENSIVE','TEST-PREGNANCY'],
  'ind_advsm_1l_avapritinib.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-COAG-PANEL','TEST-BM-ASPIRATE','TEST-BM-TREPHINE','TEST-FLOW-CYTOMETRY','TEST-NGS-MYELOID-PANEL','TEST-ECHO','TEST-CT-CHEST-ABDOMEN-PELVIS'],
  'ind_advsm_1l_midostaurin.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-COAG-PANEL','TEST-BM-ASPIRATE','TEST-BM-TREPHINE','TEST-FLOW-CYTOMETRY','TEST-NGS-MYELOID-PANEL','TEST-ECHO','TEST-CT-CHEST-ABDOMEN-PELVIS'],
  'ind_mpnst_doxorubicin_ifosfamide.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-COAG-PANEL','TEST-ECHO','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-WHOLE-BODY-MRI','TEST-NGS-COMPREHENSIVE','TEST-PREGNANCY'],
  'ind_mtc_advanced_1l_cabozantinib_ret_wt.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-CEA','TEST-HBV-SEROLOGY','TEST-HCV-ANTIBODY','TEST-HIV-SEROLOGY','TEST-ECHO','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-NGS-COMPREHENSIVE','TEST-PREGNANCY'],
  'ind_mtc_advanced_1l_selpercatinib.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-CEA','TEST-HBV-SEROLOGY','TEST-HCV-ANTIBODY','TEST-HIV-SEROLOGY','TEST-ECHO','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-NGS-COMPREHENSIVE','TEST-PREGNANCY'],
  'ind_salivary_palliative_paclitaxel_carbo.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-HER2-IHC-FISH','TEST-PDL1-IHC','TEST-ECHO','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-NGS-COMPREHENSIVE','TEST-PREGNANCY'],
  'ind_atc_paclitaxel_carboplatin.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-ECHO','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-PET-CT','TEST-BRAF-V600E','TEST-NGS-COMPREHENSIVE','TEST-PREGNANCY'],
  'ind_thyroid_papillary_rai_refractory_lenvatinib.yaml': ['TEST-CBC','TEST-CMP','TEST-LFT','TEST-RENAL-FUNCTION-EGFR','TEST-ECHO','TEST-CT-CHEST-ABDOMEN-PELVIS','TEST-BONE-SCAN','TEST-BRAF-V600E','TEST-NGS-COMPREHENSIVE','TEST-PREGNANCY'],
}

def make_block(tests):
    lines = ['required_tests:']
    for t in tests:
        lines.append(f'  - {t}')
    return '\n'.join(lines)

edited, skipped = [], []

for fname, tests in TESTS.items():
    fp = os.path.join(base, fname)
    if not os.path.exists(fp):
        skipped.append(f'{fname} (not found)')
        continue
    with open(fp, encoding='utf-8') as f:
        content = f.read()
    new_block = make_block(tests)
    # Try: required_tests: []
    new_content = re.sub(r'required_tests:\s*\[\]', new_block, content)
    # Try: required_tests: followed by newline + desired_tests (empty block)
    if new_content == content:
        new_content = re.sub(r'(required_tests:)\s*\n(\s*desired_tests:)',
                             new_block + r'\n\2', content)
    if new_content != content:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        edited.append(fname)
    else:
        skipped.append(f'{fname} (pattern not matched)')

print(f'Edited: {len(edited)} files')
for f in edited: print(f'  OK  {f}')
print(f'Skipped: {len(skipped)}')
for f in skipped: print(f'  --  {f}')
