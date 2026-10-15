// Reproducible offline WASM proof using a public synthetic example, not a clinical validation.
import fs from 'node:fs';
import path from 'node:path';
import net from 'node:net';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
let networkAttempts=0;
net.Socket.prototype.connect=function () { networkAttempts++; throw Error('TCP disabled for offline proof'); };
globalThis.fetch=async () => { networkAttempts++; throw Error('Network disabled for offline proof'); };
const root=path.resolve(process.argv[2] || '.tmp/pyodide-runtime-0.26.4');
const { loadPyodide }=await import(pathToFileURL(path.join(root,'pyodide.mjs')));
const py=await loadPyodide({indexURL:root+'/',packageCacheDir:root});
await py.loadPackage(['pydantic','pyyaml']);
const index=JSON.parse(fs.readFileSync('docs/openonco-engine-index.json'));
py.unpackArchive(Uint8Array.from(fs.readFileSync('docs/'+index.core_compressed)).buffer,'gztar');
py.unpackArchive(Uint8Array.from(fs.readFileSync('docs/'+index.diseases['DIS-AML'])).buffer,'zip');
const example=JSON.parse(fs.readFileSync('docs/examples.json')).find(x=>x.case_id==='aml-fit-1l-7-3');
const profile=structuredClone(example.json);profile.patient_id='VIRTUAL-OFFLINE-AML-001';profile.comment='Synthetic offline engine verification only';
py.globals.set('_patient_json',JSON.stringify(profile));
const result=await py.runPythonAsync(`
import json
from pathlib import Path
from knowledge_base.engine import generate_plan, orchestrate_mdt, render_plan_html
KB=Path('knowledge_base/hosted/content')
patient=json.loads(_patient_json)
result=generate_plan(patient,kb_root=KB,experimental_cache_root=KB/'cache'/'ctgov')
assert result.plan.algorithm_id and result.plan.tracks, 'No executable plan generated'
mdt=orchestrate_mdt(patient,result,kb_root=KB)
html=render_plan_html(result,mdt=mdt,target_lang='en')
html
`);
assert(result.includes('VIRTUAL-OFFLINE-AML-001'));
assert(result.includes('CHARTER'));
assert(result.length>10000);
py.unpackArchive(Uint8Array.from(fs.readFileSync('docs/'+index.diseases['DIS-NSCLC'])).buffer,'zip');
const nsclcExample=JSON.parse(fs.readFileSync('docs/examples.json')).find(x=>x.case_id==='nsclc-pdl1-low-chemo-io');
assert(nsclcExample, 'Synthetic NSCLC fixture missing');
py.globals.set('_nsclc_json',JSON.stringify(nsclcExample.json));
const histologyStates=JSON.parse(await py.runPythonAsync(`
import copy
from knowledge_base.engine import apply_disease_module
assert apply_disease_module(KB, disease_id='DIS-NSCLC')['ok']
base=json.loads(_nsclc_json)
states=[]
for histology in ['adenocarcinoma','squamous',None]:
    profile=copy.deepcopy(base)
    profile['patient_id']='VIRTUAL-OFFLINE-HISTOLOGY'
    profile['findings']['histology']=histology
    outcome=generate_plan(profile,kb_root=KB)
    if histology == 'adenocarcinoma':
        assert outcome.default_indication_id == 'IND-NSCLC-PDL1-LOW-NONSQ-MET-1L'
    else:
        assert outcome.default_indication_id is None
        assert not outcome.plan.tracks and not outcome.plan.sequencing_tracks
        reason='profile_selection_withheld' if histology == 'squamous' else 'histology_selection_withheld'
        assert outcome.plan.knowledge_base_state[reason]
    states.append({'histology':histology,'default':outcome.default_indication_id})
for taxane, drug in [('paclitaxel','DRUG-PACLITAXEL'),('nab-paclitaxel','DRUG-NAB-PACLITAXEL')]:
    profile=copy.deepcopy(base)
    profile['patient_id']='VIRTUAL-OFFLINE-SQUAMOUS'
    profile['findings']['histology']='squamous'
    profile['findings']['nsclc_taxane_choice']=taxane
    outcome=generate_plan(profile,kb_root=KB)
    assert outcome.default_indication_id == 'IND-NSCLC-SQ-PEMBRO-CARBO-'+taxane.upper()+'-1L'
    selected=next(track for track in outcome.plan.tracks if track.is_default)
    assert [comp['drug_id'] for comp in selected.regimen_data['components']] == ['DRUG-PEMBROLIZUMAB','DRUG-CARBOPLATIN',drug]
    states.append({'histology':'squamous','taxane':taxane,'default':outcome.default_indication_id})
json.dumps(states)
`));
py.unpackArchive(Uint8Array.from(fs.readFileSync('docs/'+index.diseases['DIS-TESTICULAR-GCT'])).buffer,'zip');
const bepExample=JSON.parse(fs.readFileSync('docs/examples.json')).find(x=>x.case_id==='coverage-testicular-gct-bep-1l');
assert(bepExample, 'Synthetic BEP fixture missing');
py.globals.set('_bep_json',JSON.stringify(bepExample.json));
const bepState=JSON.parse(await py.runPythonAsync(`
import yaml
assert apply_disease_module(KB, disease_id='DIS-TESTICULAR-GCT')['ok']
bep_profile=json.loads(_bep_json)
bep_profile['patient_id']='VIRTUAL-OFFLINE-BEP-001'
bep_result=generate_plan(bep_profile,kb_root=KB)
assert bep_result.default_indication_id == 'IND-GCT-METASTATIC-1L-BEP'
reg=yaml.safe_load((KB/'regimens/reg_bep_gct.yaml').read_text())
assert 'not universally required' in reg['premedication'][2]
assert reg['components'][0]['dose'].startswith('30 USP units')
assert '400 USP units' in reg['components'][0]['cumulative_dose_limit']
abvd=yaml.safe_load((KB/'regimens/abvd.yaml').read_text())
assert abvd['components'][1]['dose']=='10 USP units/m²'
bleomycin=yaml.safe_load((KB/'drugs/bleomycin.yaml').read_text())
assert 'USP' in bleomycin['typical_dosing']
assert 'adequate oxygenation' in bleomycin['notes']
assert 'Avoid high-flow O2' not in bleomycin['notes']
assert 'not demonstrated increased pulmonary complications' in bleomycin['major_interactions'][1]
assert 'Г-КСФ протипоказаний' not in abvd['notes_ua']
assert all('DLCO' not in item for item in bleomycin['absolute_contraindications'])
assert 'withhold bleomycin' in abvd['dose_adjustments'][0]['modification']
assert '400 USP units (400000 International Units)' in abvd['dose_adjustments'][1]['modification']
assert 'not an automatic universal stopping dose' in abvd['dose_adjustments'][1]['modification']
assert 'no routine repeated PFTs' in abvd['notes']
assert (KB/'sources/src_bsh_chl_bleomycin_2025.yaml').is_file()
fever=next(w for w in abvd['between_visit_watchpoints'] if w['trigger_ua']=='Лихоманка вище 38°C')
assert fever['urgency']=='call_clinic_same_day'
assert 'не призначається' not in fever['action_ua']
assert (KB/'sources/src_eviq_abvd_56.yaml').is_file()
assert 'HRCT' in reg['monitoring'][0]
assert 'EP still contains cisplatin' in reg['components'][0]['dose_modifications'][2]['action']
assert 'universal 15 mg/m²/day rule' in reg['components'][2]['dose_modifications'][0]['action']
assert 'Do not automatically substitute' in reg['components'][2]['dose_modifications'][1]['action']
assert (KB/'sources/src_horwich_bep_ceb_1997.yaml').is_file()
assert 'not an automatic permanent-discontinuation' in reg['components'][0]['dose_modifications'][0]['action']
assert reg['review_status'] == 'pending_clinical_signoff'
assert reg['last_reviewed'] is None
assert (KB/'sources/src_eviq_testicular_bep_320.yaml').is_file()
assert (KB/'sources/src_bleomycin_uk_best_practice_2018.yaml').is_file()
json.dumps({'default':bep_result.default_indication_id,'clinicalApproval':False})
`));
assert.equal(networkAttempts,0);
py.unpackArchive(Uint8Array.from(fs.readFileSync('docs/'+index.diseases['DIS-CHL'])).buffer,'zip');
const chlExample=JSON.parse(fs.readFileSync('docs/examples.json')).find(x=>x.case_id==='chl-early');
assert(chlExample, 'Synthetic early Hodgkin fixture missing');
py.globals.set('_chl_json',JSON.stringify(chlExample.json));
const chlState=JSON.parse(await py.runPythonAsync(`
assert apply_disease_module(KB, disease_id='DIS-CHL')['ok']
chl_profile=json.loads(_chl_json)
chl_profile['patient_id']='VIRTUAL-OFFLINE-CHL-001'
chl_result=generate_plan(chl_profile,kb_root=KB)
expected_mon={'REG-ABVD':'MON-ABVD-REGIMEN','REG-A-AVD':'MON-A-AVD-REGIMEN','REG-NIVO-AVD':'MON-NIVO-AVD-REGIMEN'}
for track in chl_result.plan.tracks:
    regimen=(track.regimen_data or {}).get('id')
    if regimen in expected_mon:
        assert track.monitoring_data['id']==expected_mon[regimen]
abvd_tracks=[t for t in chl_result.plan.tracks if (t.regimen_data or {}).get('id')=='REG-ABVD']
assert abvd_tracks
for track in abvd_tracks:
    assert track.monitoring_data['id']=='MON-ABVD-REGIMEN'
    assert track.monitoring_data['linked_to_regimen']==track.regimen_data['id']
    during=next(p for p in track.monitoring_data['phases'] if p['name']=='on_treatment')
    assert 'days 1 and 15' in during['window'] and '28-day' in during['window']
for lang,needle in [('en','Before each administration on days 1 and 15'),('uk','Перед кожним введенням у дні 1 і 15')]:
    chl_html=render_plan_html(chl_result,target_lang=lang)
    assert needle in chl_html
    assert 'MON-R-CHOP-REGIMEN' not in chl_html
    assert 'Confirm CD20+ DLBCL histology' not in chl_html
json.dumps({'monitoring':'MON-ABVD-REGIMEN','abvdTracks':len(abvd_tracks),'clinicalApproval':False})
`));
const advancedChl=JSON.parse(fs.readFileSync('docs/examples.json')).find(x=>x.case_id==='chl-advanced');
py.globals.set('_advanced_chl_json',JSON.stringify(advancedChl.json));
const advancedChlState=JSON.parse(await py.runPythonAsync(`
advanced_result=generate_plan(json.loads(_advanced_chl_json),kb_root=KB)
seen=[]
for track in advanced_result.plan.tracks:
    regimen=(track.regimen_data or {}).get('id')
    if regimen in expected_mon:
        assert track.monitoring_data['id']==expected_mon[regimen]
        seen.append(regimen)
assert {'REG-ABVD','REG-A-AVD'} <= set(seen)
from knowledge_base.engine.plan import _materialize_track
from knowledge_base.validation.loader import load_content
nivo_track=_materialize_track('aggressive','IND-CHL-1L-N-AVD',False,'Synthetic materialization check',load_content(KB).entities_by_id)
assert nivo_track.monitoring_data['id']=='MON-NIVO-AVD-REGIMEN'
assert nivo_track.monitoring_data['linked_to_regimen']==nivo_track.regimen_data['id']
assert 'MON-R-CHOP-REGIMEN' not in render_plan_html(advanced_result,target_lang='en')
json.dumps({'regimens':seen,'explicitNivoTrackMonitoring':nivo_track.monitoring_data['id'],'clinicalApproval':False})
`));
assert.equal(networkAttempts,0);

py.unpackArchive(Uint8Array.from(fs.readFileSync('docs/'+index.diseases['DIS-AITL'])).buffer,'zip');
const tcellExample=JSON.parse(fs.readFileSync('docs/examples.json')).find(x=>x.case_id==='aitl-cd30-positive');
assert(tcellExample, 'Synthetic AITL fixture missing');
py.globals.set('_tcell_json',JSON.stringify(tcellExample.json));
const tcellState=JSON.parse(await py.runPythonAsync(`
assert apply_disease_module(KB,disease_id='DIS-AITL')['ok']
tcell_result=generate_plan(json.loads(_tcell_json),kb_root=KB)
expected_tcell={'REG-CHP-BV':'MON-CHP-BV-REGIMEN','REG-CHOEP':'MON-CHOEP-REGIMEN'}
seen_tcell=[]
for track in tcell_result.plan.tracks:
    regimen=(track.regimen_data or {}).get('id')
    if regimen in expected_tcell:
        assert track.monitoring_data['id']==expected_tcell[regimen]
        assert track.monitoring_data['linked_to_regimen']==regimen
        seen_tcell.append(regimen)
        if regimen=='REG-CHP-BV':
            assert 'SUP-GCSF-NEUTROPENIA' in track.regimen_data['mandatory_supportive_care']
            during=track.monitoring_data['phases'][1]
            assert 'Cycle 1' in during['checkpoints'][2]
            assert 'US label' in during['checkpoints'][2]
assert set(seen_tcell)==set(expected_tcell)
aitl_outcomes=tcell_result.plan.tracks[0].indication_data['expected_outcomes']
assert 'AITL subgroup' in aitl_outcomes['progression_free_survival']['value']
assert aitl_outcomes['progression_free_survival']['source']=='SRC-ECHELON-2-FIVE-YEAR-2022'
assert '95% CI' in aitl_outcomes['progression_free_survival']['confidence_interval']
assert tcell_result.plan.tracks[0].indication_data['nccn_category'] is None
assert 'CI-BRENTUXIMAB-BLEOMYCIN' in {ci['id'] for ci in tcell_result.plan.tracks[0].contraindications_data}
assert 'CI-BORTEZOMIB-SEVERE-NEUROPATHY' not in {ci['id'] for ci in tcell_result.plan.tracks[0].contraindications_data}
bv_reg=tcell_result.plan.tracks[0].regimen_data
assert bv_reg['total_cycles'] is None
assert next(c for c in bv_reg['components'] if c['drug_id']=='DRUG-BRENTUXIMAB-VEDOTIN')['dose']=='1.8 mg/kg (maximum 180 mg)'
assert '6–8' in bv_reg['course_context_note'] and '3–4' in bv_reg['course_context_note']
adult_unconfirmed=json.loads(_tcell_json)
adult_unconfirmed['demographics']['age']=None
adult_withheld=generate_plan(adult_unconfirmed,kb_root=KB)
assert not adult_withheld.plan.tracks and not adult_withheld.plan.sequencing_tracks
assert 'demographics.age' in adult_withheld.plan.knowledge_base_state['unconfirmed_profile_fields']
assert 'adult age' in render_plan_html(adult_withheld,target_lang='en',mode='patient')
bv_points=bv_reg['between_visit_watchpoints']
assert len(bv_points)==12 and not any(w.get('cycle_day_window') for w in bv_points)
assert sum(w['urgency']=='contact_clinic_now' for w in bv_points)==7
assert any('38°C' in w['trigger_ua'] and w['urgency']=='contact_clinic_now' for w in bv_points)
assert all(w['sources']==['SRC-EVIQ-BV-CHP-PATIENT-4038'] for w in bv_points)
assert any(r['condition'].startswith('US') and 'grade 2 sensory' in r['condition'] and 'Same-dose' in r['modification'] for r in bv_reg['dose_adjustments'])
assert any(r['condition'].startswith('eviQ') and 'grade 2 motor' in r['condition'] and 'Delay until grade 1 or baseline' in r['modification'] for r in bv_reg['dose_adjustments'])
bv_patient=render_plan_html(tcell_result,target_lang='en',mode='patient')
assert 'do not change the dose yourself' in bv_patient
assert 'Temperature 38°C or higher' in bv_patient
assert 'No course is selected by this shared reference' in bv_patient
for lang in ['en','uk']:
    tcell_html=render_plan_html(tcell_result,target_lang=lang)
    assert 'MON-R-CHOP-REGIMEN' not in tcell_html
    assert 'showed superior outcomes vs standard CHOP' not in tcell_html
    assert 'Confirm CD20+ DLBCL histology' not in tcell_html
    assert 'Підтвердити CD20+ DLBCL гістологію' not in tcell_html
assert (KB/'sources/src_eviq_bv_chp_4038.yaml').is_file()
assert (KB/'sources/src_eviq_choep21_630.yaml').is_file()
assert (KB/'sources/src_adcetris_us_label.yaml').is_file()
json.dumps({'regimens':seen_tcell,'clinicalApproval':False})
`));
assert.equal(networkAttempts,0);
py.unpackArchive(Uint8Array.from(fs.readFileSync('docs/'+index.diseases['DIS-MCL'])).buffer,'zip');
const mclExample=JSON.parse(fs.readFileSync('docs/examples.json')).find(x=>x.case_id==='mcl-fit-younger');
assert(mclExample, 'Synthetic MCL fixture missing');
py.globals.set('_mcl_json',JSON.stringify(mclExample.json));
const mclState=JSON.parse(await py.runPythonAsync(`
assert apply_disease_module(KB,disease_id='DIS-MCL')['ok']
mcl_result=generate_plan(json.loads(_mcl_json),kb_root=KB)
mcl_track=next(t for t in mcl_result.plan.tracks if (t.regimen_data or {}).get('id')=='REG-MCL-INTENSIVE-RDHAP-AUTOSCT')
mcl_reg=mcl_track.regimen_data
assert mcl_reg['components']==mcl_reg['phases'][0]['components']
cis=[c for c in mcl_reg['phases'][0]['components'] if c['drug_id']=='DRUG-CISPLATIN']
assert len(cis)==1 and cis[0]['dose']=='100 mg/m²'
assert '24 hours' in cis[0]['schedule'] and 'cycles 2, 4, 6' in cis[0]['schedule']
cyta=next(c for c in mcl_reg['phases'][0]['components'] if c['drug_id']=='DRUG-CYTARABINE')
assert cyta['dose']=='2 g/m² per dose' and 'two doses 12 hours apart' in cyta['schedule']
assert mcl_track.monitoring_data['id']=='MON-MCL-RCHOP-RDHAP-INDUCTION'
for lang,needle in [('en','Assess cerebellar function before every'),('uk','Оцініть функцію мозочка перед кожною')]:
    mcl_html=render_plan_html(mcl_result,target_lang=lang)
    assert needle in mcl_html and 'DRUG-CISPLATIN' in mcl_html
    assert 'MON-R-CHOP-REGIMEN' not in mcl_html
assert 'time to treatment failure' in mcl_track.indication_data['expected_outcomes']['progression_free_survival']
json.dumps({'regimen':mcl_reg['id'],'cisplatin':cis[0],'monitoring':mcl_track.monitoring_data['id'],'clinicalApproval':False})
`));
assert.equal(networkAttempts,0);
py.unpackArchive(Uint8Array.from(fs.readFileSync('docs/'+index.diseases['DIS-PMBCL'])).buffer,'zip');
const epochExample=JSON.parse(fs.readFileSync('docs/examples.json')).find(x=>x.case_id==='pmbcl-typical');
assert(epochExample, 'Synthetic PMBCL fixture missing');
py.globals.set('_epoch_json',JSON.stringify(epochExample.json));
const epochState=JSON.parse(await py.runPythonAsync(`
assert apply_disease_module(KB,disease_id='DIS-PMBCL')['ok']
epoch_result=generate_plan(json.loads(_epoch_json),kb_root=KB)
epoch_track=next(t for t in epoch_result.plan.tracks if (t.regimen_data or {}).get('id')=='REG-DA-EPOCH-R')
assert epoch_track.monitoring_data['id']=='MON-DA-EPOCH-R-REGIMEN'
assert any('twice weekly, three days apart' in p['window'] for p in epoch_track.monitoring_data['phases'])
epoch=epoch_track.regimen_data
assert 'SUP-GCSF-NEUTROPENIA' in epoch['mandatory_supportive_care']
assert 'retain the previous dose level' in epoch['dose_adjustments'][1]['modification']
assert 'below starting level 1, only cyclophosphamide' in epoch['dose_adjustments'][2]['modification']
assert 'not restricted to HIV-positive' in epoch['dose_adjustments'][4]['modification']
for lang,needle in [('en','During every cycle: CBC twice weekly'),('uk','Під час кожного циклу: загальний аналіз крові двічі на тиждень')]:
    epoch_html=render_plan_html(epoch_result,target_lang=lang)
    assert needle in epoch_html and 'MON-DA-EPOCH-R-REGIMEN' in epoch_html
assert (KB/'sources/src_eviq_da_r_epoch_783.yaml').is_file()
assert 'not a verified PFS' in epoch_track.indication_data['expected_outcomes']['progression_free_survival']
assert (KB/'sources/src_dunleavy_pmbcl_daepoch_2013.yaml').is_file()
json.dumps({'monitoring':epoch_track.monitoring_data['id'],'clinicalApproval':False})
`));
assert.equal(networkAttempts,0);
py.unpackArchive(Uint8Array.from(fs.readFileSync('docs/'+index.diseases['DIS-BURKITT'])).buffer,'zip');
const codoxExample=JSON.parse(fs.readFileSync('docs/examples.json')).find(x=>x.case_id==='burkitt-high-risk');
assert(codoxExample, 'Synthetic Burkitt fixture missing');
py.globals.set('_codox_original_json',JSON.stringify(codoxExample.json));
const codoxConfirmedProfile=structuredClone(codoxExample.json);
codoxConfirmedProfile.findings.cns_involvement=false;
py.globals.set('_codox_json',JSON.stringify(codoxConfirmedProfile));
const codoxState=JSON.parse(await py.runPythonAsync(`
epoch_patient_points=epoch_track.regimen_data['between_visit_watchpoints']
assert any('Температура 38°C або вище' in w['trigger_ua'] and w['urgency']=='contact_clinic_now' and not w.get('cycle_day_window') for w in epoch_patient_points)
assert any('Нова задишка' in w['trigger_ua'] and w['urgency']=='contact_clinic_now' for w in epoch_patient_points)
epoch_patient_html=render_plan_html(epoch_result,target_lang='en',mode='patient')
assert 'Contact your doctor or nurse immediately' in epoch_patient_html
assert 'Uncontrolled vomiting' in epoch_patient_html
assert apply_disease_module(KB,disease_id='DIS-BURKITT')['ok']
original_codox=generate_plan(json.loads(_codox_original_json),kb_root=KB)
assert original_codox.default_indication_id is None and not original_codox.plan.tracks
codox_result=generate_plan(json.loads(_codox_json),kb_root=KB)
codox_track=next(t for t in codox_result.plan.tracks if (t.regimen_data or {}).get('id')=='REG-CODOX-M-IVAC')
a,b=[p['components'] for p in codox_track.regimen_data['phases']]
assert codox_track.regimen_data['components']==a+b
assert any(c['drug_id']=='DRUG-IFOSFAMIDE' and 'IVAC blocks only' in c['schedule'] for c in b)
assert len([c for c in b if c['drug_id']=='DRUG-MESNA'])==2
assert {c['route'] for c in a if c['drug_id']=='DRUG-METHOTREXATE'}=={'IV','IT'}
assert any('36 hours after IV methotrexate START' in c['schedule'] for c in a if c['drug_id']=='DRUG-LEUCOVORIN')
assert codox_track.monitoring_data['id']=='MON-CODOX-IVAC-REGIMEN'
codox_points=codox_track.regimen_data['between_visit_watchpoints']
assert any(w['trigger_ua']=='Температура 38°C або вище' and w['urgency']=='er_now' for w in codox_points)
assert len([w for w in codox_points if w['urgency']=='contact_clinic_now'])==5
tls_point=next(w for w in codox_points if 'м’язові спазми' in w['trigger_ua'])
assert not tls_point.get('cycle_day_window') and 'і до лікування' in tls_point['action_ua']
for lang,heading in [('en','Contact your doctor or nurse immediately'),('uk','Негайно зв’яжіться з лікарем або медсестрою')]:
    patient_codox=render_plan_html(codox_result,target_lang=lang,mode='patient')
    assert heading in patient_codox and ('Unable to eat or drink' if lang=='en' else 'Не можете їсти чи пити') in patient_codox
    assert ('Very severe headache' if lang=='en' else 'Дуже сильний головний біль') in patient_codox
    assert ('before treatment' if lang=='en' else 'і до лікування') in patient_codox
for lang,needle in [('en','Assess neurological function before each ifosfamide dose'),('uk','Оцініть неврологічний стан перед кожною дозою іфосфаміду')]:
    codox_html=render_plan_html(codox_result,target_lang=lang)
    assert needle in codox_html and 'DRUG-MESNA' in codox_html
assert (KB/'sources/src_eviq_burkitt_ivac_4490.yaml').is_file()
json.dumps({'monitoring':codox_track.monitoring_data['id'],'clinicalApproval':False,'protocolScopeGuard':True,'broaderEligibilityAuditPending':True})
`));
assert.equal(networkAttempts,0);
const cnsState=JSON.parse(await py.runPythonAsync(`
cns_profile=json.loads(_codox_original_json)
cns_profile['findings']['burkitt_protocol_variant']='eviq_proven_cns'
cns_result=generate_plan(cns_profile,kb_root=KB)
assert cns_result.default_indication_id=='IND-BURKITT-1L-CODOX-IVAC-PROVEN-CNS'
assert len(cns_result.plan.tracks)==1
cns_track=cns_result.plan.tracks[0]
assert cns_track.monitoring_data['id']=='MON-CODOX-IVAC-PROVEN-CNS'
cns_points=cns_track.regimen_data['between_visit_watchpoints']
assert len(cns_points)==12
assert all(set(w['sources']) <= {'SRC-EVIQ-CNS-CODOX-PATIENT-4492','SRC-EVIQ-CNS-IVAC-PATIENT-4493','SRC-EVIQ-MOUTH-PATIENT-3099'} for w in cns_points)
for lang,heading in [('en','Contact your doctor or nurse immediately'),('uk','Негайно зв’яжіться з лікарем або медсестрою')]:
    cns_patient=render_plan_html(cns_result,target_lang=lang,mode='patient')
    assert heading in cns_patient and ('New confusion' if lang=='en' else 'Нова сплутаність') in cns_patient
    assert ('Unable to eat or drink' if lang=='en' else 'Не можете їсти чи пити') in cns_patient
ca,cb=[p['components'] for p in cns_track.regimen_data['phases']]
assert any(c['drug_id']=='DRUG-CYTARABINE' and c['route']=='IT' and 'days 7 and 9' in c['schedule'] for c in cb)
assert any(c['drug_id']=='DRUG-RITUXIMAB' and 'days 1 and 11' in c['schedule'] for c in ca)
assert 'committee adaptation' in cns_track.regimen_data['notes']
assert (KB/'sources/src_eviq_burkitt_cns_ivac_4493.yaml').is_file()
cns_profile['findings']['cns_involvement']=False
conflicting_cns=generate_plan(cns_profile,kb_root=KB)
assert not conflicting_cns.plan.tracks and conflicting_cns.default_indication_id is None
json.dumps({'variant':'eviq_proven_cns','scopeConflictWithheld':True,'clinicalApproval':False})
`));
assert.equal(networkAttempts,0);
py.unpackArchive(Uint8Array.from(fs.readFileSync('docs/'+index.diseases['DIS-PTCL-NOS'])).buffer,'zip');
py.globals.set('_ptcl_json',fs.readFileSync('examples/patient_ptcl_cd30_negative.json','utf8'));
const withdrawalState=JSON.parse(await py.runPythonAsync(`
import copy
import importlib
assert apply_disease_module(KB,disease_id='DIS-PTCL-NOS')['ok']
ordinary_ptcl=generate_plan(json.loads(_ptcl_json),kb_root=KB)
assert ordinary_ptcl.plan.tracks
assert all(t.indication_id!='IND-PTCL-1L-CHOEP-ALLOSCT' for t in ordinary_ptcl.plan.tracks)
assert all((t.regimen_data or {}).get('id')!='REG-CHP-BV' for t in ordinary_ptcl.plan.tracks)
for cd30_profile in [json.loads(_ptcl_json), json.loads(_tcell_json)]:
    cd30_profile['biomarkers']['BIO-CD30-IHC']='negative'
    cd30_profile['findings']['cd30_positive']=False
    negative_cd30=generate_plan(cd30_profile,kb_root=KB)
    assert negative_cd30.plan.tracks
    assert all((t.regimen_data or {}).get('id')!='REG-CHP-BV' for t in negative_cd30.plan.tracks)
    cd30_profile['findings']['cd30_positive']=True
    unconfirmed_cd30=generate_plan(cd30_profile,kb_root=KB)
    assert not unconfirmed_cd30.plan.tracks and not unconfirmed_cd30.plan.sequencing_tracks
    assert unconfirmed_cd30.plan.knowledge_base_state['profile_selection_withheld']
    assert 'Confirm the documented CD30 result' in render_plan_html(unconfirmed_cd30,target_lang='en',mode='patient')
bundle_module=importlib.import_module('knowledge_base.validation.bundle')
original_loader=bundle_module.load_packaged_content
def forced_loader(*args,**kwargs):
    loaded=copy.deepcopy(original_loader(*args,**kwargs))
    alg=loaded.entities_by_id['ALGO-PTCL-1L']['data']
    alg['output_indications']=['IND-PTCL-1L-CHOEP-ALLOSCT','IND-TCELL-1L-CHOEP']
    alg['default_indication']='IND-PTCL-1L-CHOEP-ALLOSCT'
    alg['decision_tree']=[{'step':1,'evaluate':{'any_of':[]},'if_true':{'result':'IND-PTCL-1L-CHOEP-ALLOSCT'},'if_false':{'result':'IND-PTCL-1L-CHOEP-ALLOSCT'}}]
    return loaded
try:
    bundle_module.load_packaged_content=forced_loader
    withdrawn=generate_plan(json.loads(_ptcl_json),kb_root=KB)
    assert not withdrawn.plan.tracks and not withdrawn.plan.sequencing_tracks
    assert withdrawn.default_indication_id is None
    assert withdrawn.plan.knowledge_base_state['planning_selection_withheld']
    assert 'Clinical reference withheld from planning' in render_plan_html(withdrawn,target_lang='en',mode='patient')
finally:
    bundle_module.load_packaged_content=original_loader
json.dumps({'forcedHistoricalSelectionWithheld':True,'ordinaryRoutesPreserved':True,'clinicalApproval':False})
`));
const medicationState=JSON.parse(await py.runPythonAsync(`
med_profile=json.loads(_ptcl_json)
med_profile.setdefault('demographics',{})['age']=60
med_profile.setdefault('biomarkers',{})['BIO-CD30-IHC']='positive'
med_profile.setdefault('findings',{})['cd30_positive']=True
med_before=copy.deepcopy(med_profile)
med_unknown=generate_plan(med_profile,kb_root=KB)
assert med_unknown.plan.tracks[0].regimen_data['id']=='REG-CHP-BV'
assert med_unknown.plan.knowledge_base_state['medication_screens'][0]['status']=='unknown'
assert 'data-medication-screen="unknown"' in render_plan_html(med_unknown,target_lang='en',mode='patient')
assert med_profile==med_before
for medication_status in ['partial','complete']:
    med_profile['concomitant_medications']={'status':medication_status,'drug_ids':['DRUG-BLEOMYCIN']}
    med_blocked=generate_plan(med_profile,kb_root=KB)
    assert med_blocked.plan.knowledge_base_state['medication_selection_withheld']
    assert not med_blocked.plan.tracks and not med_blocked.plan.sequencing_tracks
    assert med_blocked.default_indication_id is None
    for render_mode in ['patient','clinician']:
        for render_lang in ['en','uk']:
            assert 'data-medication-screen="blocked"' in render_plan_html(med_blocked,target_lang=render_lang,mode=render_mode)
med_profile['concomitant_medications']={'status':'complete','drug_ids':[]}
med_not_detected=generate_plan(med_profile,kb_root=KB)
assert med_not_detected.plan.tracks[0].regimen_data['id']=='REG-CHP-BV'
assert med_not_detected.plan.knowledge_base_state['medication_screens'][0]['status']=='not_detected_in_reported_list'
med_profile['medications']=['bleomycin']
med_unsupported=generate_plan(med_profile,kb_root=KB)
assert med_unsupported.plan.knowledge_base_state['medication_selection_withheld']
assert not med_unsupported.plan.tracks
json.dumps({'knownPairWithheld':True,'noAutomaticSubstitute':True,'unknownExplicit':True,'competingInputWithheld':True,'clinicalApproval':False})
`));
const trialProvenanceState=JSON.parse(await py.runPythonAsync(`
from knowledge_base.engine.experimental_options import enumerate_experimental_options
from knowledge_base.engine.render import _render_experimental_options
from knowledge_base.schemas.experimental_option import ExperimentalOption
no_search=enumerate_experimental_options(disease_id='DIS-AUDIT',disease_term='Synthetic condition',cache=False)
assert no_search.search_status=='not_run' and no_search.last_synced is None
for report_lang in ['en','uk']:
    no_search_html=_render_experimental_options(no_search,target_lang=report_lang)
    assert 'Last synced:' not in no_search_html and 'Останнє оновлення:' not in no_search_html
assert 'Matching trial availability is unknown' in _render_experimental_options(no_search,target_lang='en')
def registry_error(**kwargs):
    raise RuntimeError('synthetic offline failure')
failed_search=enumerate_experimental_options(disease_id='DIS-AUDIT',disease_term='Synthetic condition',cache=False,search_fn=registry_error)
assert failed_search.search_status=='failed' and failed_search.last_synced is None
empty_search=enumerate_experimental_options(disease_id='DIS-AUDIT',disease_term='Synthetic condition',cache=False,search_fn=lambda **kwargs: [])
assert empty_search.search_status=='completed' and empty_search.last_synced
assert 'This does not establish that no other trials exist' in _render_experimental_options(empty_search,target_lang='en')
legacy_search=ExperimentalOption(id='EXPER-LEGACY',disease_id='DIS-AUDIT',trials=[],last_synced='2000-01-01')
assert legacy_search.search_status=='unknown'
assert 'Search execution is unconfirmed' in _render_experimental_options(legacy_search,target_lang='en')
json.dumps({'notRunExplicit':True,'failedNotFresh':True,'emptyQueryScoped':True,'legacyUnknown':True})
`));
const accessProvenanceState=JSON.parse(await py.runPythonAsync(`
from knowledge_base.engine.render import _render_access_matrix
from knowledge_base.schemas.plan import AccessMatrix, AccessMatrixRow
access_fixture=AccessMatrix(generated_at='2001-02-03T04:05:06Z',rows=[AccessMatrixRow(track_id='standard',track_label='Synthetic reference',registered_in_ua=None,reimbursed_nszu=None,cost_last_updated='1999-01-01',cost_is_stale=True)])
access_before=access_fixture.model_dump()
access_en=_render_access_matrix(access_fixture,target_lang='en')
access_uk=_render_access_matrix(access_fixture,target_lang='uk')
assert 'Table assembled: 2001-02-03' in access_en
assert 'Status updated:' not in access_en and 'does not verify registration' in access_en
assert 'Таблицю сформовано: 2001-02-03' in access_uk
assert 'Статус оновлено:' not in access_uk and 'не підтверджує перевірку реєстрації' in access_uk
assert access_fixture.model_dump()==access_before
json.dumps({'assemblyNotVerification':True,'storedMetadataUnchanged':True})
`));
assert.equal(networkAttempts,0);
console.log(JSON.stringify({status:'passed',runtime:'0.26.4',networkAttempts,reportCharacters:result.length,profile:'VIRTUAL-OFFLINE-AML-001',histologyStates,bepState,chlState,advancedChlState,tcellState,mclState,epochState,codoxState,cnsState,withdrawalState,medicationState,trialProvenanceState,accessProvenanceState,environment:'Node WASM, not browser'}));
