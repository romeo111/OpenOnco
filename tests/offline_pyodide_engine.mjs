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
        assert outcome.plan.knowledge_base_state['histology_selection_withheld']
    states.append({'histology':histology,'default':outcome.default_indication_id})
json.dumps(states)
`));
assert.equal(networkAttempts,0);

console.log(JSON.stringify({status:'passed',runtime:'0.26.4',networkAttempts,reportCharacters:result.length,profile:'VIRTUAL-OFFLINE-AML-001',histologyStates,environment:'Node WASM, not browser'}));
