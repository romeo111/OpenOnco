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
for lang in ['en','uk']:
    tcell_html=render_plan_html(tcell_result,target_lang=lang)
    assert 'MON-R-CHOP-REGIMEN' not in tcell_html
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
console.log(JSON.stringify({status:'passed',runtime:'0.26.4',networkAttempts,reportCharacters:result.length,profile:'VIRTUAL-OFFLINE-AML-001',histologyStates,bepState,chlState,advancedChlState,tcellState,mclState,epochState,environment:'Node WASM, not browser'}));
