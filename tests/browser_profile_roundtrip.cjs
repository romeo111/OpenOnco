// Execute the shipped importer, mode switch, assembly and draft persistence.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('docs/try.html','utf8');
function fn(page,name){const m=page.match(new RegExp(`^function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,name);return m[0].replace(/\r\n/g,'\n');}
const names=['parseNumericValue','readValue','onAnswerChange','getByPath','profileInputError','populateFormFromProfile','buildProfile','setMode','saveDraft','applyDraftFields','findAnswerControl'];
const fields=[{field:'patient_id',type:'text'},{field:'demographics.age',type:'integer'},{field:'demographics.ecog',type:'enum',options:[{value:0},{value:1}]},{field:'findings.active_tb',type:'boolean'},{field:'findings.anc',type:'float'}];
const controls=new Map(fields.map(q=>[q.field,{value:'STALE',type:q.type==='float'||q.type==='integer'?'number':'text',dataset:{type:q.type,field:q.field},validity:{badInput:false}}]));
let saved,error;
const context=vm.createContext({textarea:{value:''},profileInputCopy:JSON.parse(html.match(/^const profileInputCopy = (.*);$/m)[1]),
 CSS:{escape:s=>s},STORAGE_KEY:'VIRTUAL-ROUNDTRIP',localStorage:{setItem:(_,v)=>saved=v},
 formPane:{querySelector:s=>controls.get(s.match(/data-field="([^"]+)"/)[1])},jsonPane:{},
 modeFormBtn:{classList:{toggle(){}}},modeJsonBtn:{classList:{toggle(){}}},
 validateNumericInputs:()=>true,updateRunBtnEnabled(){},markPlanDirty(){},updateImpactPanelLocal(){},setError:e=>error=e,
 findQuestionnaireForProfile:p=>p.disease?.id==='DIS-VIRTUAL'?0:-1,
 QUESTIONNAIRES_MANIFEST:[{id:'QUEST-VIRTUAL'}],quest:{id:'QUEST-VIRTUAL',fixed_fields:{demographics:{age:60},line_of_therapy:1},groups:[{questions:fields}]}});
vm.runInContext('let mode="json",answers={},activeQuest=quest,formProfileBase=null,removedProfileFields=new Set();'+names.map(n=>fn(html,n)).join('\n'),context);
const run=s=>vm.runInContext(s,context),plain=v=>JSON.parse(JSON.stringify(v));
const profile={patient_id:'VIRTUAL-ROUNDTRIP-001',disease:{id:'DIS-VIRTUAL',custom:'preserved'},demographics:{age:61,ecog:0,unmapped:0},findings:{active_tb:false,anc:0.836},metadata:{synthetic:true,list:[false,0,null]},line_of_therapy:3,unknown:null,concomitant_medications:{status:'partial',drug_ids:['DRUG-BLEOMYCIN']}};
context.textarea.value=JSON.stringify(profile);
run('setMode("form",{syncFromJson:true})');
assert.equal(run('mode'),'form');assert.deepEqual(plain(run('buildProfile()')),profile);
assert.equal(controls.get('demographics.age').value,61);assert.equal(controls.get('findings.active_tb').value,'false');
controls.get('demographics.age').value='62';context.input=controls.get('demographics.age');run('onAnswerChange({target:input})');
controls.get('findings.anc').value='';context.input=controls.get('findings.anc');run('onAnswerChange({target:input})');
const edited=structuredClone(profile);edited.demographics.age=62;delete edited.findings.anc;
assert.deepEqual(plain(run('buildProfile()')),edited,'Edits and explicit clearing retain unmapped data');
run('saveDraft()');context.draft=JSON.parse(saved);
run('formProfileBase=null;removedProfileFields=new Set();answers={};applyDraftFields(draft)');
assert.deepEqual(plain(run('buildProfile()')),edited,'Full base and explicit deletions survive draft restoration');
run('setMode("json",{syncFromForm:true})');assert.deepEqual(JSON.parse(context.textarea.value),edited);
for(const patch of [{demographics:{age:'61'}},{demographics:{ecog:99}},{findings:{active_tb:'false'}},{disease:{id:'DIS-OTHER'}}]){
 const invalid={...profile,...patch};context.textarea.value=JSON.stringify(invalid);const before=context.textarea.value;
 run('setMode("form",{syncFromJson:true})');assert.equal(run('mode'),'json');assert.equal(context.textarea.value,before);assert(error);
}
const missing={disease:{id:'DIS-VIRTUAL'},patient_id:'VIRTUAL-MISSING',demographics:{age:null}};
context.textarea.value=JSON.stringify(missing);run('setMode("form",{syncFromJson:true})');
assert.equal(controls.get('demographics.age').value,'');assert.equal(controls.get('findings.active_tb').value,'');
assert.deepEqual(plain(run('buildProfile()')),missing,'Missing fields stay missing; null stays null; questionnaire defaults are not injected');
for(const prefix of ['', 'ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
 const page=fs.readFileSync('docs/'+prefix+'try.html','utf8');for(const name of names)assert.equal(fn(page,name),fn(html,name));
 assert(page.includes("setMode('form', { syncFromJson: true })"));
 assert(page.includes('if (populateFormFromProfile(quest, example.json))'));
 assert(page.includes('if (!populateFormFromProfile(quest, patient))'));
}
console.log('Full JSON/form/draft round trips preserve unmapped fields, null/zero/false, missing data and edits; incompatible imports remain JSON; all eleven clients match');

// Medication editing extends this same full-profile preservation contract.
require('./browser_medication_editor.cjs');

require('./browser_form_medication.cjs');
