const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function fn(page,name){const m=page.match(new RegExp(`^(?:async )?function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,name);return m[0].replace(/\r\n/g,'\n');}
const root=fs.readFileSync('docs/try.html','utf8');
const manifest=JSON.parse(root.match(/^const EXAMPLES_MANIFEST = (.*);$/m)[1]);
const source=JSON.parse(fs.readFileSync('docs/examples.json','utf8'));
async function check(page){
 const copy=JSON.parse(page.match(/^const profileInputCopy = (.*);$/m)[1]);
 const identity=vm.createContext({EXAMPLES_MANIFEST:manifest,profileInputCopy:copy,ensureExamples:async()=>[...source].reverse()});
 vm.runInContext(fn(page,'profileInputError')+fn(page,'loadExample'),identity);
 for(let i=0;i<manifest.length;i++)assert.equal((await vm.runInContext(`loadExample(${i})`,identity)).case_id,manifest[i].case_id);
 const examples=[0,1].map(i=>({case_id:'virtual-example-'+i,disease_id:'DIS-VIRTUAL-'+i,json:{patient_id:'VIRTUAL-EXAMPLE-'+i,disease:{id:'DIS-VIRTUAL-'+i},metadata:{synthetic:true},findings:{unknown:null,flag:false}},has_case_page:false}));
 let payload=examples,network=false,questionnaireFail=false,reportFail=false,compatible=true,qIndex=-1,clears=0,writes=0,error,report='VIRTUAL-OLD-REPORT',status;
 const context=vm.createContext({EXAMPLES_MANIFEST:examples.map(({case_id,disease_id})=>({case_id,disease_id})),profileInputCopy:copy,
  textarea:{value:'VIRTUAL-OLD-JSON'},activeExampleSelection:'0',exampleSelect:{value:'1'},diseaseSelect:{value:'0'},mode:'form',form:{id:'QUEST-OLD'},input:{patient_id:'VIRTUAL-OLD'},
  UI_LOCK_TEXT:{},withUiLock:async(a,b,c,task)=>task(),ensureExamples:async()=>{if(network)throw Error('VIRTUAL-NETWORK');return payload;},
  findQuestionnaireForProfile:()=>qIndex,loadQuestionnaire:async()=>{if(questionnaireFail)throw Error('VIRTUAL-MISSING-QUESTIONNAIRE');return {id:'QUEST-VIRTUAL'};},
  clearPlanState:()=>{clears++;report=null;},setError:e=>error=e,setStatus:s=>status=s,
  renderForm:q=>{context.form=q;context.activeExampleSelection='';},repopulateExamples(){},
  populateFormFromProfile:(q,p)=>{if(compatible)context.input=structuredClone(p);return compatible;},buildProfile:()=>context.input,
  setMode:m=>context.mode=m,lockFilledFields(){},showExampleLockBanner(){},saveDraft:()=>writes++,
  loadExamplePlan:async id=>{if(reportFail)throw Error('VIRTUAL-REPORT');report=id;},updateRunBtnEnabled(){},updateImpactPanelLocal(){}});
 vm.runInContext(['profileInputError','loadExample','changeExample'].map(n=>fn(page,n)).join('\n'),context);
 const run=()=>vm.runInContext('changeExample()',context);
 const snapshot=()=>JSON.stringify({text:context.textarea.value,input:context.input,form:context.form,mode:context.mode,disease:context.diseaseSelect.value,report});
 const before=snapshot();
 for(const kind of ['network','missing','duplicate','metadata-disease','profile-disease','scenario','malformed','questionnaire']){
  payload=structuredClone(examples);network=kind==='network';qIndex=kind==='questionnaire'?0:-1;questionnaireFail=kind==='questionnaire';
  if(kind==='missing')payload.pop();if(kind==='duplicate')payload.push(structuredClone(payload[1]));
  if(kind==='metadata-disease')payload[1].disease_id='DIS-WRONG';
  if(kind==='profile-disease')payload[1].json.disease.id='DIS-WRONG';
  if(kind==='scenario')payload[1].scenario_type='diagnostic';
  if(kind==='malformed')payload[1].json=[];
  context.exampleSelect.value='1';await run();
  assert.equal(snapshot(),before);assert.equal(clears,0);assert.equal(writes,0);assert.equal(context.exampleSelect.value,'0');assert.equal(error,copy.exampleFailed);
 }
 network=false;questionnaireFail=false;qIndex=-1;payload=[...examples].reverse();context.exampleSelect.value='1';await run();
 assert.equal(context.mode,'json');assert.deepEqual(JSON.parse(context.textarea.value),examples[1].json);assert.equal(context.form,null);
 assert.equal(context.exampleSelect.value,'1');assert.equal(writes,1);assert.equal(report,null);assert.equal(status,copy.exampleLoaded);
 qIndex=0;context.exampleSelect.value='0';payload=structuredClone(examples);payload[0].has_case_page=true;reportFail=true;await run();
 assert.equal(context.mode,'form');assert.deepEqual(context.input,examples[0].json);assert.equal(writes,2);assert.equal(report,null);assert.equal(error,copy.exampleReportFailed);
 assert.equal(context.activeExampleSelection,'0');
 compatible=false;reportFail=false;context.exampleSelect.value='1';await run();
 assert.equal(context.mode,'json');assert.deepEqual(JSON.parse(context.textarea.value),examples[1].json);assert.equal(error,copy.transfer);
}
(async()=>{
 for(const prefix of ['', 'ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
  const page=fs.readFileSync('docs/'+prefix+'try.html','utf8');await check(page);
  for(const name of ['loadExample','changeExample'])assert.equal(fn(page,name),fn(root,name));
  assert(page.includes("exampleSelect.addEventListener('change', changeExample)"));
 }
 console.log('All 446 examples resolve by identity under payload reordering; rejected imports preserve input/report; report failures keep loaded profiles; eleven clients passed');
})().catch(e=>{console.error(e);process.exitCode=1;});
