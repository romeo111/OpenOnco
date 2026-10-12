// Resolve questionnaire identity independently of payload order, then change state.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function fn(page,name){const m=page.match(new RegExp(`^(?:async )?function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,name);return m[0].replace(/\r\n/g,'\n');}
const root=fs.readFileSync('docs/try.html','utf8');
const manifest=JSON.parse(root.match(/^const QUESTIONNAIRES_MANIFEST = (.*);$/m)[1]);
const source=JSON.parse(fs.readFileSync('docs/questionnaires.json','utf8'));
async function fixture(page){
 let payload=[...source].reverse(),fail=false,cleared=0,saved=0,error;
 const context=vm.createContext({QUESTIONNAIRES_MANIFEST:manifest,profileInputCopy:JSON.parse(page.match(/^const profileInputCopy = (.*);$/m)[1]),
  ensureQuestionnaires:async()=>{if(fail)throw Error('VIRTUAL-NETWORK-FAILURE');return payload;},
  diseaseSearch:{value:'VIRTUAL-NEW-SEARCH'},renderDiseaseOptions(){},diseaseSelect:{value:'1'},exampleSelect:{value:'VIRTUAL'},UI_LOCK_TEXT:{},
  withUiLock:async(a,b,c,task)=>task(),clearPlanState:()=>cleared++,saveDraft:()=>saved++,
  setError:e=>error=e,updateRunBtnEnabled(){},updateImpactPanelLocal(){},repopulateExamples(){},
  renderForm:q=>{context.next=q;vm.runInContext('activeQuest=next;answers={};formProfileBase=null',context);}});
 vm.runInContext('let activeQuest=null,answers={patient_id:"VIRTUAL-UNCHANGED"},formProfileBase={metadata:{synthetic:true}};'+
  ['normalizeQuestionnaire','loadQuestionnaire','changeDisease'].map(n=>fn(page,n)).join('\n'),context);
 const run=s=>vm.runInContext(s,context);
 for(let i=0;i<manifest.length;i++)assert.equal((await run(`loadQuestionnaire(${i})`)).id,manifest[i].id,'All actual questionnaires resolve by ID in reversed payload');
 context.old=source[0];run('activeQuest=old');const before=run('JSON.stringify({activeQuest,answers,formProfileBase})');
 for(const broken of ['network','missing','duplicate','wrong-disease','bad-shape','invalid-index']){
  fail=broken==='network';payload=structuredClone(source);
  if(broken==='duplicate')payload.push(structuredClone(payload.find(q=>q.id===manifest[1].id)));
  if(broken==='missing')payload=payload.filter(q=>q.id!==manifest[1].id);
  if(broken==='wrong-disease')payload.find(q=>q.id===manifest[1].id).disease_id='DIS-VIRTUAL-WRONG';
  if(broken==='bad-shape')payload.find(q=>q.id===manifest[1].id).groups=[{questions:[{field:'bad',type:'enum',options:null}]}];
  context.diseaseSelect.value=broken==='invalid-index'?'9999':'1';await run('changeDisease()');
  assert.equal(context.diseaseSearch.value,'');assert.equal(context.diseaseSelect.value,'0');assert.equal(cleared,0);assert.equal(saved,0);
  assert.equal(run('JSON.stringify({activeQuest,answers,formProfileBase})'),before,'Failure retains old state');
  assert.equal(error,context.profileInputCopy.switchFailed);
 }
 fail=false;payload=[...source].reverse();context.diseaseSelect.value='1';await run('changeDisease()');
 assert.equal(run('activeQuest.id'),manifest[1].id);assert.equal(cleared,1);assert.equal(saved,1);assert.equal(error,null);
 context.diseaseSelect.value='';await run('changeDisease()');assert.equal(run('activeQuest'),null);assert.equal(saved,2);
}
(async()=>{
 for(const prefix of ['', 'ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
  const page=fs.readFileSync('docs/'+prefix+'try.html','utf8');await fixture(page);
  for(const name of ['loadQuestionnaire','changeDisease'])assert.equal(fn(page,name),fn(root,name));
  assert(page.includes("diseaseSelect.addEventListener('change', changeDisease)"));
  assert(page.includes('const quest = await loadQuestionnaire(idx)'));
  assert(page.includes('const quest = await loadQuestionnaire(qIdx)'));
  assert(page.includes('const quest = qIndex >= 0 ? await loadQuestionnaire(qIndex) : null'));
 }
 console.log('All 78 questionnaire identities survive payload reordering; network/missing/mismatched/malformed selection failures retain previous state; eleven clients passed');
})().catch(e=>{console.error(e);process.exitCode=1;});
