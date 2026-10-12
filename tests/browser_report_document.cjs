// A successful iframe load event is not evidence of a readable report.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function fn(page,name){const m=page.match(new RegExp(`^(?:async )?function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,name);return m[0].replace(/\r\n/g,'\n');}
const names=['loadedReportError','waitForFrameLoad','withReportUiLock','updateWorkflowControls','openPlanModal'];
async function check(page){
 const events=new Map(),timers=new Map();let id=0,error,doc;
 const frame={get contentDocument(){if(doc==='blocked')throw Error('VIRTUAL-BLOCKED');return doc;},addEventListener:(t,f)=>events.set(t,f),removeEventListener:t=>events.delete(t)};
 const button=()=>({disabled:false});
 const context=vm.createContext({resultFrame:frame,profileInputCopy:JSON.parse(page.match(/^const profileInputCopy = (.*);$/m)[1]),
  setTimeout:f=>{timers.set(++id,f);return id;},clearTimeout:i=>timers.delete(i),setError:e=>error=e,
  isInteractionLocked:()=>false,validateNumericInputs:()=>true,setLockedTitle(){},refreshModeButtonAvailability(){},highlightLangButtons(){},
  document:{activeElement:null},planModalReturnFocus:null,planModalClose:{focus(){}},planModal:{hidden:true},textarea:{value:'{"patient_id":"VIRTUAL-REPORT-CHECK"}'},activeQuest:null,
  runBtn:button(),viewPlanBtn:button(),pdfBtn:button(),modalPdfBtn:button(),modalHtmlBtn:button(),
  resetBtn:button(),formatBtn:button(),diseaseSelect:button(),exampleSelect:button(),modeFormBtn:button(),modeJsonBtn:button(),personalizeBtn:button(),
  withUiLock:async(a,b,c,action)=>action()});
 vm.runInContext('let reportReady=true,planSource="example",planDirty=false,mode="json";'+names.map(n=>fn(page,n)).join('\n'),context);
 const run=s=>vm.runInContext(s,context);
 for(const bad of [null,'blocked',{querySelector:()=>null},{querySelector:()=>({textContent:'   '})}]){
  doc=bad;const pending=run('waitForFrameLoad()');const rejected=assert.rejects(pending,{message:context.profileInputCopy.reportInvalid});
  events.get('load')();await rejected;
  assert.equal(run('reportReady'),false);assert.equal(context.viewPlanBtn.disabled,true);assert.equal(context.pdfBtn.disabled,true);
  assert.equal(context.modalHtmlBtn.disabled,true);assert.equal(context.modalPdfBtn.disabled,true);assert.equal(context.runBtn.disabled,false);
  run('openPlanModal();openPlanModal({force:true})');assert.equal(context.planModal.hidden,true);
  assert.equal(events.size,0);assert.equal(timers.size,0);assert.equal(error,context.profileInputCopy.reportInvalid);
 }
 for(const text of ['Treatment plan — VIRTUAL','Diagnostic brief — VIRTUAL','Patient report — VIRTUAL']){
  doc={querySelector:selector=>{assert.equal(selector,'.page .doc-header .doc-title, .patient-report h1');return {textContent:text};}};
  const pending=run('waitForFrameLoad()');events.get('load')();await pending;
  assert.equal(run('reportReady'),true);assert.equal(context.viewPlanBtn.disabled,false);assert.equal(context.modalHtmlBtn.disabled,false);
  run('openPlanModal()');assert.equal(context.planModal.hidden,false);context.planModal.hidden=true;
 }
 await run('withReportUiLock("","","",async()=>{throw Error("VIRTUAL-SWITCH-FAILURE")})');
 assert.equal(error,'VIRTUAL-SWITCH-FAILURE','Report switch failures are handled, not unhandled promises');
}
(async()=>{
 const root=fs.readFileSync('docs/try.html','utf8');
 for(const prefix of ['', 'ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
  const page=fs.readFileSync('docs/'+prefix+'try.html','utf8');await check(page);
  for(const name of names)assert.equal(fn(page,name),fn(root,name));
  for(const name of ['switchResultLang','switchResultMode'])assert(fn(page,name).includes('await withReportUiLock('));
 }
 console.log('Loaded error/blank/unreadable documents never enable report viewing/export/print; readable shells and retry recover; eleven clients passed');
})().catch(e=>{console.error(e);process.exitCode=1;});
