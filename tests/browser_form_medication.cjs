// Form medicines use the same full-profile base as import, assembly and drafts.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const editor=fs.readFileSync('scripts/medication_editor.js','utf8').replace(/\r\n/g,'\n');
function fn(html,name){const m=html.match(new RegExp(`^function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,name);return m[0];}
class Element {
 constructor(tag){this.tag=tag;this.children=[];this.events={};this.style={};this.classList={toggle(){}};this.disabled=false;this.value='';}
 appendChild(child){this.children.push(child);return child;}
 addEventListener(name,fn){this.events[name]=fn;}
 setAttribute(name,value){this[name]=value;}
 get options(){return this.children;}
 get selectedOptions(){return this.children.filter(option=>option.selected);}
}
const plain=value=>JSON.parse(JSON.stringify(value));
for(const prefix of ['','ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
 const html=fs.readFileSync('docs/'+prefix+'try.html','utf8');
 const config=JSON.parse(html.match(/^const medicationEditorConfig = (.*);$/m)[1]);
 const fields=[{field:'patient_id',type:'text'},{field:'demographics.age',type:'integer'},{field:'findings.flag',type:'boolean'}];
 const controls=new Map(fields.map(q=>[q.field,{value:'',type:q.type==='integer'?'number':'text',dataset:{type:q.type,field:q.field},validity:{badInput:false}}]));
 const form=new Element('section'),json=new Element('section'),banner={hidden:true};
 form.querySelector=s=>controls.get(s.match(/data-field="([^"]+)"/)[1]);
 let saved,dirty=0,error;
 const c=vm.createContext({document:{createElement:tag=>new Element(tag),getElementById:()=>banner,querySelectorAll:()=>[...form.children,...json.children]},
  formPane:form,jsonPane:json,modeFormBtn:new Element('button'),modeJsonBtn:new Element('button'),personalizeBtn:new Element('button'),
  textarea:{value:'UNCHANGED JSON TEXT'},medicationEditorConfig:config,profileInputCopy:JSON.parse(html.match(/^const profileInputCopy = (.*);$/m)[1]),
  CSS:{escape:s=>s},STORAGE_KEY:'VIRTUAL-FORM-MEDICINES',localStorage:{setItem:(_,v)=>saved=v},
  locked:false,numericValid:true,isInteractionLocked:()=>c.locked,validateNumericInputs:()=>c.numericValid,
  setError:e=>error=e,markPlanDirty:()=>dirty++,updateRunBtnEnabled(){},updateImpactPanelLocal(){},
  quest:{id:'QUEST-VIRTUAL',fixed_fields:{disease:{id:'DIS-VIRTUAL'},line_of_therapy:1},groups:[{questions:fields}]},
  findQuestionnaireForProfile:p=>p.disease?.id==='DIS-VIRTUAL'?0:-1,QUESTIONNAIRES_MANIFEST:[{id:'QUEST-VIRTUAL'}]});
 const names=['parseNumericValue','readValue','onAnswerChange','getByPath','profileInputError','populateFormFromProfile','buildProfile','setMode','saveDraft','applyDraftFields','findAnswerControl'];
 vm.runInContext('let mode="form",answers={"demographics.age":61},activeQuest=quest,formProfileBase=null,removedProfileFields=new Set();'+names.map(n=>fn(html,n)).join('\n')+'\n'+editor,c);
 const run=code=>vm.runInContext(code,c),panel=form.children[0];
 const status=panel.children.find(x=>x.tag==='label').children[0],drugs=panel.children.filter(x=>x.tag==='label')[1].children[0],apply=panel.children.find(x=>x.tag==='button'),message=panel.children.at(-1);
 const open=()=>{panel.open=true;panel.events.toggle();},choose=id=>{for(const option of drugs.options)option.selected=option.value===id;};
 assert.equal(panel.id,'formMedicationEditor');assert.equal(panel.children[0].textContent,config.copy.formTitle);assert.equal(apply.textContent,config.copy.formApply);
 const untouched=plain(run('buildProfile()'));open();assert.equal(status.value,'unknown');assert(!apply.disabled);assert.deepEqual(plain(run('buildProfile()')),untouched);assert.equal(saved,undefined);
 choose('DRUG-BLEOMYCIN');apply.events.click();assert.equal(message.textContent,config.copy.formInvalid);assert.deepEqual(plain(run('buildProfile()')),untouched);
 status.value='partial';apply.events.click();assert.equal(message.textContent,config.copy.formSaved);assert.equal(error,'');assert.equal(dirty,1);assert.equal(c.textarea.value,'UNCHANGED JSON TEXT');
 assert.deepEqual(plain(run('buildProfile().concomitant_medications')),{status:'partial',drug_ids:['DRUG-BLEOMYCIN']});
 // A later change to another field cannot be rolled back by a stale editor.
 open();controls.get('demographics.age').value='62';c.input=controls.get('demographics.age');run('onAnswerChange({target:input})');
 status.value='complete';apply.events.click();assert.equal(message.textContent,config.copy.formChanged);assert.equal(run('buildProfile().demographics.age'),62);assert.equal(run('buildProfile().concomitant_medications.status'),'partial');
 open();choose('');status.value='complete';assert.equal(run('buildProfile().concomitant_medications.status'),'partial');apply.events.click();assert.deepEqual(plain(run('buildProfile().concomitant_medications')),{status:'complete',drug_ids:[]});
 // Imports, unmapped fields and normal field edits survive medicines and drafts.
 const imported={patient_id:'VIRTUAL-FORM-MED-001',disease:{id:'DIS-VIRTUAL'},demographics:{age:61,unmapped:0},findings:{flag:false},metadata:{list:[false,0,null]},prior_therapies:['REG-VIRTUAL'],concomitant_medications:{status:'partial',drug_ids:['DRUG-BLEOMYCIN']}};
 c.profile=imported;assert(run('populateFormFromProfile(quest,profile)'));open();assert.equal(status.value,'partial');assert.equal(drugs.selectedOptions[0].value,'DRUG-BLEOMYCIN');
 status.value='complete';apply.events.click();const expected={...imported,concomitant_medications:{status:'complete',drug_ids:['DRUG-BLEOMYCIN']}};
 assert.deepEqual(plain(run('buildProfile()')),expected);c.draft=JSON.parse(saved);
 run('formProfileBase=null;answers={};removedProfileFields=new Set();applyDraftFields(draft)');assert.deepEqual(plain(run('buildProfile()')),expected,'Actual draft restoration retains the complete medication object and other fields');
 run('setMode("json",{syncFromForm:true})');assert.deepEqual(JSON.parse(c.textarea.value),expected);run('setMode("form",{syncFromJson:true})');assert.deepEqual(plain(run('buildProfile()')),expected);
 // Exact user clearing and normal edits still override the preserved base.
 controls.get('demographics.age').value='';c.input=controls.get('demographics.age');run('onAnswerChange({target:input})');const cleared=plain(run('buildProfile()'));assert(!Object.hasOwn(cleared.demographics,'age'));open();status.value='partial';apply.events.click();assert(!Object.hasOwn(plain(run('buildProfile()')).demographics,'age'));
 open();const before=plain(run('buildProfile()'));c.locked=true;status.value='complete';apply.events.click();assert.deepEqual(plain(run('buildProfile()')),before);c.locked=false;
 banner.hidden=false;open();assert(apply.disabled);assert.equal(message.textContent,config.copy.formLocked);apply.events.click();assert.deepEqual(plain(run('buildProfile()')),before);banner.hidden=true;c.personalizeBtn.events.click();assert(!panel.open);open();assert(!apply.disabled);
 // A different questionnaire object invalidates even an otherwise equal profile.
 open();run('activeQuest={...quest}');apply.events.click();assert.equal(message.textContent,config.copy.formChanged);run('activeQuest=quest');
 for(const patch of [{medications:[]},{findings:{concomitant_drugs:[]}},{concomitant_medications:{status:'partial',drug_ids:['DRUG-MISSING']}}]){
  c.profile={...imported,...patch};assert(run('populateFormFromProfile(quest,profile)'));const invalid=plain(run('buildProfile()'));open();assert(apply.disabled);apply.events.click();assert.deepEqual(plain(run('buildProfile()')),invalid);
 }
 c.numericValid=false;open();assert(apply.disabled);assert.equal(message.textContent,config.copy.formInvalid);c.numericValid=true;
 c.modeJsonBtn.events.click();assert(!panel.open);assert(fn(html,'renderForm').includes('closeMedicationEditors();'),'Questionnaire/example/reset rendering closes stale medicine controls');
 assert.equal(dirty>0,true);
}
console.log('Form medicines: eleven languages, normal assembly, preserved fields, actual draft/JSON round trips, clearing, explicit statuses, stale edits, questionnaire/example locks passed');
