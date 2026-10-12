// Draft/example restores must select controls, not identically tagged wrappers.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const page=fs.readFileSync('docs/try.html','utf8');
function fn(text,name){const m=text.match(new RegExp(`^function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,name);return m[0].replace(/\r\n/g,'\n');}
const fields=['demographics.age','findings.active_tb','demographics.ecog','patient_id'];
const controls=new Map(fields.map(field=>[field,{dataset:{type:field==='demographics.ecog'?'enum':field==='findings.active_tb'?'boolean':'text'},value:''}]));
const wrappers=new Map(fields.map(field=>[field,{dataset:{field},value:'WRAPPER-UNCHANGED'}]));
const storage=new Map();
const context=vm.createContext({CSS:{escape:s=>s},STORAGE_KEY:'VIRTUAL-DRAFT-TEST',textarea:{value:''},
 localStorage:{setItem:(k,v)=>storage.set(k,v),getItem:k=>storage.get(k)},
 formPane:{querySelector:selector=>{
  const field=selector.match(/data-field="([^"]+)"/)[1];
  return selector.startsWith('input[')?controls.get(field):wrappers.get(field);
 }},setMode:mode=>vm.runInContext('mode='+JSON.stringify(mode),context)});
const names=['findAnswerControl','applyDraftFields','saveDraft','loadDraft','getByPath','populateFormFromProfile'];
vm.runInContext('let answers={},mode="form";const activeQuest={id:"QUEST-VIRTUAL"};'+names.map(n=>fn(page,n)).join('\n'),context);
const draft={answers:{'demographics.age':'61.5','findings.active_tb':false,'demographics.ecog':0,patient_id:'VIRTUAL-RESTORE-001'},mode:'form',jsonText:'{"unmapped":"VIRTUAL"}'};
context.draft=draft;vm.runInContext('applyDraftFields(draft)',context);
assert.equal(controls.get('demographics.age').value,'61.5');
assert.equal(controls.get('findings.active_tb').value,'false');
assert.equal(controls.get('demographics.ecog').value,'0');
assert.equal(controls.get('patient_id').value,'VIRTUAL-RESTORE-001');
assert([...wrappers.values()].every(w=>w.value==='WRAPPER-UNCHANGED'));
assert.deepEqual(JSON.parse(storage.get('VIRTUAL-DRAFT-TEST')).answers,draft.answers,'Use the actual persistence function, including invalid numeric edits');
const restored=JSON.parse(JSON.stringify(vm.runInContext('loadDraft()',context)));
controls.get('demographics.age').value='60';
context.draft=restored;vm.runInContext('answers={};applyDraftFields(draft)',context);
assert.equal(controls.get('demographics.age').value,'61.5','Reload restores the displayed invalid edit instead of default 60');
context.profile={patient_id:'VIRTUAL-EXAMPLE-001',demographics:{age:62,ecog:0},findings:{active_tb:false}};
context.quest={groups:[{questions:fields.map(field=>({field,type:field==='demographics.ecog'?'enum':field==='findings.active_tb'?'boolean':'text'}))}]};
vm.runInContext('populateFormFromProfile(quest,profile)',context);
assert.equal(controls.get('demographics.age').value,62);
assert.equal(controls.get('patient_id').value,'VIRTUAL-EXAMPLE-001');
assert([...wrappers.values()].every(w=>w.value==='WRAPPER-UNCHANGED'));
for(const prefix of ['', 'ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
 const html=fs.readFileSync('docs/'+prefix+'try.html','utf8');
 for(const name of names)assert.equal(fn(html,name),fn(page,name));
 assert(html.includes('applyDraftFields(draft);'));
}
console.log('Actual draft save/load, controls vs wrappers, invalid edit reload, zero/false enums and example/QR profile population passed for all eleven clients');
