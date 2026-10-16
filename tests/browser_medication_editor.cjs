// Execute the actual served editor, including its DOM event handlers.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const prefixes=['','ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/'];
const editor=fs.readFileSync('scripts/medication_editor.js','utf8').replace(/\r\n/g,'\n');
function fn(html,name){const m=html.match(new RegExp(`^function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,name);return m[0];}
class Element {
 constructor(tag){this.tag=tag;this.children=[];this.events={};this.style={};this.value='';this.textContent='';this.disabled=false;}
 appendChild(child){this.children.push(child);return child;}
 addEventListener(name,callback){this.events[name]=callback;}
 setAttribute(name,value){this[name]=value;}
 get options(){return this.children;}
 get selectedOptions(){return this.children.filter(option=>option.selected);}
}
const plain=value=>JSON.parse(JSON.stringify(value));
for(const prefix of prefixes){
 const html=fs.readFileSync('docs/'+prefix+'try.html','utf8').replace(/\r\n/g,'\n');
 assert(html.includes(editor),'Served source equals repository editor');
 const config=JSON.parse(html.match(/^const medicationEditorConfig = (.*);$/m)[1]);
 assert(config.copy.notice && config.copy.complete && config.copy.unsupported);
 if(prefix) assert.notEqual(config.copy.title,JSON.parse(fs.readFileSync('docs/try.html','utf8').match(/^const medicationEditorConfig = (.*);$/m)[1]).copy.title);
 const catalog=config.drugs;assert(catalog.length>100);assert.equal(new Set(catalog.map(drug=>drug.id)).size,catalog.length);
 assert(catalog.some(drug=>drug.id==='DRUG-BLEOMYCIN'));
 const pane=new Element('section'),form=new Element('section'),banner={hidden:true};let saved=0,dirty=0,error='';
 const c=vm.createContext({document:{createElement:tag=>new Element(tag),getElementById:()=>banner,querySelectorAll:()=>[...pane.children,...form.children]},jsonPane:pane,formPane:form,medicationEditorConfig:config,
  modeFormBtn:new Element('button'),modeJsonBtn:new Element('button'),personalizeBtn:new Element('button'),activeQuest:{id:'QUEST-VIRTUAL'},
  textarea:{value:''},mode:'json',locked:false,isInteractionLocked:()=>c.locked,
  setError:value=>error=value,saveDraft:()=>saved++,markPlanDirty:()=>dirty++,updateRunBtnEnabled(){},updateImpactPanelLocal(){},
  profileInputCopy:JSON.parse(html.match(/^const profileInputCopy = (.*);$/m)[1])});
 vm.runInContext(fn(html,'profileInputError')+fn(html,'buildProfile')+'\n'+editor,c);
 const panel=pane.children[0],status=panel.children.find(x=>x.tag==='label').children[0];
 const drugs=panel.children.filter(x=>x.tag==='label')[1].children[0],apply=panel.children.find(x=>x.tag==='button'),message=panel.children.at(-1);
 const original={patient_id:'VIRTUAL-MEDICATION-EDITOR',metadata:{unknown:null,zero:0,flag:false},prior_therapies:['REG-VIRTUAL']};
 function open(profile){c.textarea.value=typeof profile==='string'?profile:JSON.stringify(profile);panel.open=true;panel.events.toggle();}
 function choose(id){for(const option of drugs.options)option.selected=option.value===id;}
 open(original);assert.equal(status.value,'unknown');assert(!apply.disabled);assert.equal(saved,0);assert.deepEqual(JSON.parse(c.textarea.value),original);
 choose('DRUG-BLEOMYCIN');const raw=c.textarea.value;apply.events.click();assert.equal(c.textarea.value,raw,'Unknown cannot include known drugs');assert.equal(message.textContent,config.copy.invalid);
 status.value='partial';apply.events.click();assert.equal(saved,1);assert.equal(dirty,1);assert.equal(error,'');
 const expected={...original,concomitant_medications:{status:'partial',drug_ids:['DRUG-BLEOMYCIN']}};
 assert.deepEqual(JSON.parse(c.textarea.value),expected,'Preserve unrelated fields and historical exposure');
 panel.events.toggle();assert.equal(status.value,'partial');assert.equal(drugs.selectedOptions[0].value,'DRUG-BLEOMYCIN');
 c.locked=true;const lockedText=c.textarea.value;status.value='complete';apply.events.click();assert.equal(c.textarea.value,lockedText);c.locked=false;
 c.textarea.value='{"patient_id":"VIRTUAL-CHANGED"}';apply.events.click();assert.equal(c.textarea.value,'{"patient_id":"VIRTUAL-CHANGED"}');assert.equal(message.textContent,config.copy.changed);
 open(original);status.value='complete';choose('');apply.events.click();assert.deepEqual(JSON.parse(c.textarea.value).concomitant_medications,{status:'complete',drug_ids:[]},'Complete empty requires explicit selection and apply');
 for(const key of ['medications','concomitant_drugs']){const bad={...original,[key]:[]};open(bad);assert(apply.disabled);assert.equal(message.textContent,config.copy.unsupported);const before=c.textarea.value;apply.events.click();assert.equal(c.textarea.value,before);}
 for(const key of ['concomitant_drugs','bleomycin_concomitant']){open({...original,findings:{[key]:false}});assert(apply.disabled);assert.equal(message.textContent,config.copy.unsupported);}
 for(const value of [{status:'complete',drug_ids:['DRUG-NOT-IN-CATALOG']},{status:'unknown',drug_ids:['DRUG-BLEOMYCIN']},{status:'partial',drug_ids:['DRUG-BLEOMYCIN','DRUG-BLEOMYCIN']},{status:'complete',drug_ids:[],extra:true}]){open({...original,concomitant_medications:value});assert(apply.disabled);assert.equal(message.textContent,config.copy.invalid);}
 for(const raw of ['{"demographics":{"age":17,"age":61}}','{"metadata":{"x":9007199254740993}}','{"patient_id":']){open(raw);assert(apply.disabled);const before=c.textarea.value;apply.events.click();assert.equal(c.textarea.value,before);}
 c.mode='form';open(original);assert(apply.disabled);apply.events.click();assert.deepEqual(JSON.parse(c.textarea.value),original);c.mode='json';
 const before=JSON.stringify(expected);c.profile=expected;c.ids=['DRUG-BLEOMYCIN'];
 const next=vm.runInContext('medicationEditorUpdate(profile,"partial",ids,medicationEditorConfig.drugs)',c);
 assert.equal(JSON.stringify(expected),before);assert.deepEqual(plain(next),expected);
}
console.log('Medication editor: eleven localized clients, explicit completeness, exact IDs, draft/report hooks, locks, stale JSON and invalid/legacy preservation passed');
