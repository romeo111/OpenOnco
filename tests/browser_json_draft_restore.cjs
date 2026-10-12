// Run the shipped boot path with unavailable/retired/no questionnaire.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function fn(page,name){const m=page.match(new RegExp(`^(?:async )?function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,name);return m[0];}
async function check(page,draft,kind){
 let stored=JSON.stringify(draft),writes=0,status,error,fetches=0;
 const context=vm.createContext({textarea:{value:''},STORAGE_KEY:'VIRTUAL-JSON-DRAFT',
  localStorage:{getItem:()=>stored,setItem:(_,v)=>{writes++;stored=v;}},
  profileInputCopy:JSON.parse(page.match(/^const profileInputCopy = (.*);$/m)[1]),
  modeFormBtn:{classList:{toggle(){}}},modeJsonBtn:{classList:{toggle(){}}},formPane:{},jsonPane:{},
  updateRunBtnEnabled(){},updateImpactPanelLocal(){},renderDiseaseOptions(){},saveManifestsToCache(){},
  setLoadingProgress(){},repopulateExamples(){},setStatus:s=>status=s,setError:e=>error=e,
  withUiLock:async(a,b,c,callback)=>callback(),UI_LOCK_TEXT:{},diseaseSelect:{value:''},
  QUESTIONNAIRES_MANIFEST:kind==='retired'?[]:[{id:'QUEST-VIRTUAL'}],console:{warn(){}},
  ensureQuestionnaires:async()=>{fetches++;throw Error('VIRTUAL-NETWORK-UNAVAILABLE');},
  renderForm:q=>vm.runInContext('activeQuest='+JSON.stringify(q),context)});
 vm.runInContext('let mode="form",activeQuest=null,answers={},formProfileBase=null,removedProfileFields=new Set();'+
  ['loadDraft','restoreJsonDraft','setMode','saveDraft','loadQuestionnaire','loadAssets'].map(n=>fn(page,n)).join('\n'),context);
 await vm.runInContext('loadAssets()',context);
 if(draft.mode==='json'){
  assert.equal(context.textarea.value,draft.jsonText,'Restore exact bytes, including unfinished JSON');
  assert.equal(vm.runInContext('mode',context),'json');assert.equal(context.jsonPane.hidden,false);
  assert.equal(status,draft.questId?context.profileInputCopy.restoreLimited:context.profileInputCopy.restored);
  assert.equal(error,undefined,'An unavailable questionnaire does not make raw restoration fail');
 }else {assert.equal(context.textarea.value,'');assert.equal(vm.runInContext('mode',context),'form');}
 assert.equal(writes,0,'Boot must not overwrite the saved questionnaire reference or answers');
 assert.equal(stored,JSON.stringify(draft));
 assert.equal(fetches,kind==='missing'?1:0);
}
(async()=>{
 for(const prefix of ['', 'ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
  const page=fs.readFileSync('docs/'+prefix+'try.html','utf8');
  for(const text of [' {"patient_id":"VIRTUAL-RAW","extra":{"value":0,"flag":false}}\n','{"patient_id":','']){
   for(const kind of ['none','retired','missing']) await check(page,{mode:'json',questId:kind==='none'?null:'QUEST-VIRTUAL',answers:{'demographics.age':61},jsonText:text},kind);
  }
  await check(page,{mode:'form',questId:null,jsonText:'stale mirror'},'none');
 }
 console.log('Actual boot restores JSON-only, retired-questionnaire and fetch-failed drafts, including unfinished/empty text, without overwriting storage; all eleven clients passed');
})().catch(e=>{console.error(e);process.exitCode=1;});
