const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function fn(p,n){const m=p.match(new RegExp(`^function ${n}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,n);return m[0].replace(/\r\n/g,'\n');}
const root=fs.readFileSync('docs/try.html','utf8');
const names=['getByPath','profileInputError','questionnaireValuePresent','displayQuestion','updateImpactPanelLocal','setProgress','setReadinessCritical','updateImpactPanel'];
for(const prefix of ['', 'ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
 const page=fs.readFileSync('docs/'+prefix+'try.html','utf8');
 const c=vm.createContext({nsclcQuestionCopy:JSON.parse(page.match(/^const nsclcQuestionCopy = (.*);$/m)[1]),profileInputCopy:JSON.parse(page.match(/^const profileInputCopy = (.*);$/m)[1]),
  textarea:{value:''},progressText:{},progressPct:{},progressFill:{style:{}},readinessCriticalText:{dataset:{}},numericInputErrors:new Map(),
  QUESTIONNAIRES_MANIFEST:[{id:'QUEST-VIRTUAL'}],findQuestionnaireForProfile:p=>p.disease?.id==='DIS-VIRTUAL'?0:-1,setFiredRedflags(){}});
 vm.runInContext('let mode="json",answers={"demographics.age":61,"demographics.ecog":0,"findings.flag":false,"findings.anc":0};let activeQuest={id:"QUEST-VIRTUAL",groups:[{questions:['+
  '{field:"demographics.age",type:"integer",range_min:18,range_max:110,impact:"critical",label:"Age"},'+
  '{field:"demographics.ecog",type:"enum",options:[{value:0}],impact:"critical",label:"ECOG"},'+
  '{field:"findings.flag",type:"boolean",impact:"critical",label:"Flag"},'+
  '{field:"findings.anc",type:"float",range_min:0,impact:"critical",label:"ANC"}]}]};'+names.map(n=>fn(page,n)).join('\n'),c);
 const run=s=>vm.runInContext(s,c);
 for(const invalid of ['{"disease":{"id":"DIS-VIRTUAL"},"metadata":{"value":9007199254740993}}', '{"disease":{"id":"DIS-VIRTUAL"},"demographics":{"age":17,"age":61,"ecog":0},"findings":{"flag":false,"anc":0}}', '{"patient_id":','[]','{"disease":{"id":"DIS-OTHER"}}','{"disease":{"id":"DIS-VIRTUAL"},"findings":{"anc":1e9999}}']){
  c.textarea.value=invalid;run('updateImpactPanelLocal()');assert.equal(c.progressText.textContent,'0 / 0');assert.equal(c.readinessCriticalText.dataset.kind,'idle');assert.equal(c.readinessCriticalText.textContent,c.profileInputCopy.readinessUnknown);
 }
 c.textarea.value='{"disease":{"id":"DIS-VIRTUAL"}}';run('updateImpactPanelLocal()');assert.equal(c.progressText.textContent,'0 / 4');assert.equal(c.readinessCriticalText.dataset.kind,'warn');
 run('updateImpactPanel({filled_count:4,total_questions:4,missing_critical:[]})');assert.equal(c.progressText.textContent,'0 / 4','Async old counts cannot overwrite current JSON');
 const complete={disease:{id:'DIS-VIRTUAL'},demographics:{age:61,ecog:0},findings:{flag:false,anc:0}};
 c.textarea.value=JSON.stringify(complete);run('updateImpactPanelLocal()');assert.equal(c.progressText.textContent,'4 / 4');assert.equal(c.readinessCriticalText.textContent,c.profileInputCopy.readinessComplete);
 complete.demographics.age=111;c.textarea.value=JSON.stringify(complete);run('updateImpactPanelLocal()');assert.equal(c.progressText.textContent,'3 / 4');assert.equal(c.readinessCriticalText.dataset.kind,'warn');
 run('mode="form";delete answers["demographics.age"];updateImpactPanel({filled_count:4,total_questions:4,missing_critical:[]})');assert.equal(c.progressText.textContent,'3 / 4','Async old counts cannot overwrite current form');
 for(const n of ['questionnaireValuePresent','updateImpactPanelLocal'])assert.equal(fn(page,n),fn(root,n));
 assert(/updateImpactPanelLocal\(\);\s*\/\/ No live preview from JSON/.test(page));
 assert(fn(page,'setMode').includes('updateImpactPanelLocal();'));
}
console.log('Readiness reflects current JSON/form, typed values and authored bounds; incomplete/mismatched JSON is unknown; stale async counts cannot overwrite it; eleven clients passed');
