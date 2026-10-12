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

console.log(JSON.stringify({status:'passed',runtime:'0.26.4',networkAttempts,reportCharacters:result.length,profile:'VIRTUAL-OFFLINE-AML-001',histologyStates,bepState,environment:'Node WASM, not browser'}));
