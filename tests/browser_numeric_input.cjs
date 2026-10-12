// Execute shipped parsing, field feedback, profile assembly and action gating.
const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict');
const html = fs.readFileSync('docs/try.html', 'utf8');
function fn(page, name) {
  const m = page.match(new RegExp(`^function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`, 'm'));
  assert(m, name); return m[0].replace(/\r\n/g, '\n');
}
const names = ['parseNumericValue','numericValueError','numericInputError','validateNumericInputs','readValue',
  'onAnswerChange','profileInputError','buildProfile','setMode','updateWorkflowControls','updateImpactPanelLocal'];
const code = names.map(n=>fn(html,n)).join('\n');
function input(field, type, value, min, max) {
  const error = { style: {}, hidden: true };
  return { type: 'number', dataset: { field, type }, value, min, max, step: type === 'float' ? 'any' : '1',
    validity: { badInput: false }, style: {}, attrs: {}, error,
    setCustomValidity(message) { this.validationMessage = message; },
    setAttribute(k,v) { this.attrs[k]=v; }, closest() { return { querySelector:()=>error }; } };
}
const a = input('findings.virtual_integer','integer','61','0','120');
const b = input('findings.virtual_float','float','0.836','0','10');
const summary = {}, textarea = { value: '{"patient_id":"VIRTUAL-OLD"}' }, calls = { drafts: [], missing: [] };
const button = () => ({ disabled:false, classList:{ toggle(){} } });
const copy = JSON.parse(html.match(/^const numericInputCopy = (.*);$/m)[1]);
const context = vm.createContext({ console, profileInputCopy:JSON.parse(html.match(/^const profileInputCopy = (.*);$/m)[1]), numericInputCopy:copy, numericInputSummary:summary, numericInputErrors:new Map(),
  formPane:{ querySelectorAll:()=>[a,b] }, jsonPane:{}, textarea,
  isInteractionLocked:()=>false, setLockedTitle(){}, refreshModeButtonAvailability(){},
  markPlanDirty:()=>vm.runInContext('planDirty=true', context),
  saveDraft:()=>calls.drafts.push(JSON.parse(vm.runInContext('JSON.stringify(answers)',context))),
  updateRunBtnEnabled:()=>vm.runInContext('updateWorkflowControls()',context),
  setProgress:(filled,total)=>{calls.progress=[filled,total];}, setReadinessCritical:missing=>{calls.missing=missing;}, setFiredRedflags(){},
  setError:error=>{calls.error=error;},
  runBtn:button(), viewPlanBtn:button(), pdfBtn:button(), modalPdfBtn:button(), modalHtmlBtn:button(),
  resetBtn:button(), formatBtn:button(), diseaseSelect:button(), exampleSelect:button(), modeFormBtn:button(), modeJsonBtn:button(), personalizeBtn:button(),
});
vm.runInContext(`let mode='form',planSource='generated',reportReady=true,planDirty=true;
let formProfileBase=null,removedProfileFields=new Set();
let answers={'findings.virtual_integer':61,'findings.virtual_float':0.836,'findings.virtual_boolean':false};
const activeQuest={fixed_fields:{patient_id:'VIRTUAL-NUMERIC-001'},groups:[{questions:[
{field:'findings.virtual_integer',label:'Integer',impact:'critical'},
{field:'findings.virtual_float',label:'Float',impact:'optional'},
{field:'findings.virtual_boolean',label:'Boolean',impact:'optional'}]}]};`+code,context);
const run=s=>vm.runInContext(s,context);
for (const [value,type,expected] of [['0','integer',0],['-2','integer',-2],['1.0','integer',1],['2.5e1','integer',25],
  ['0.836','float',0.836],['1e-20','float',1e-20],['61.5','integer',undefined],['1.00000000000000001','integer',undefined],
  ['1e-9999','integer',undefined],['1e-9999','float',undefined],['1e9999','float',undefined],['NaN','float',undefined],
  ['12mg','float',undefined],['0x10','integer',undefined],['1,2','float',undefined],[' ','integer',undefined],
  ['9007199254740993','integer',undefined]]) {
  context.v=value;context.t=type;
  assert.equal(run('parseNumericValue(v,t)'),expected,`${type}: ${value}`);
}
context.a=a;context.b=b;
run('answers[a.dataset.field]=61.5');
assert.equal(run('numericInputError(a)'), 'sync', 'Reject hidden model values that differ from the displayed control');
run('answers[a.dataset.field]=61');
a.value='61.5'; run('onAnswerChange({target:a})');
assert.equal(run('answers[a.dataset.field]'),'61.5','Keep the invalid edit in the draft, not a truncated integer');
assert.equal(calls.drafts.at(-1)[a.dataset.field],'61.5');
assert.equal(a.validationMessage,copy.integer); assert.equal(a.attrs['aria-invalid'],'true');
assert.equal(context.runBtn.disabled,true); assert.equal(context.viewPlanBtn.disabled,false,'Existing reports remain accessible');
assert.equal(summary.hidden,false); assert.equal(calls.progress[0],2,'Invalid numbers do not count as filled');
assert.equal(calls.missing[0].label,'Integer'); assert.equal(run('buildProfile()'),null);
const old=textarea.value; run('setMode("json",{syncFromForm:true})');
assert.equal(run('mode'),'form'); assert.equal(textarea.value,old,'Do not silently omit an invalid value when copying JSON');
a.value='61';run('onAnswerChange({target:a})');
assert.equal(context.runBtn.disabled,false); assert.equal(a.validationMessage,''); assert.equal(summary.hidden,true);
assert.equal(run('buildProfile().findings.virtual_float'),0.836);
assert.equal(run('buildProfile().findings.virtual_boolean'),false);
for (const value of ['0','120']) { a.value=value;run('onAnswerChange({target:a})');assert.equal(context.runBtn.disabled,false); }
a.value='121';run('onAnswerChange({target:a})');
assert(a.validationMessage.includes('0–120')); assert.equal(context.runBtn.disabled,true);
assert.equal(run('answers[a.dataset.field]'),121,'No clamping to the boundary');
a.value='61';run('onAnswerChange({target:a})');
b.value='100.25';run('onAnswerChange({target:b})');
assert.equal(context.runBtn.disabled,true,'Optional invalid input also blocks generation');
assert(b.validationMessage.includes('0–10')); assert.equal(run('buildProfile()'),null);
b.value='';run('onAnswerChange({target:b})');
assert.equal(context.runBtn.disabled,false,'Cleared optional input remains unknown');
assert.equal(run('buildProfile().findings.virtual_float'),undefined);
b.validity.badInput=true;run('onAnswerChange({target:b})');assert.equal(context.runBtn.disabled,true);
b.validity.badInput=false;b.value='0.836';run('onAnswerChange({target:b})');
run('setMode("json",{syncFromForm:true})');
assert.equal(JSON.parse(textarea.value).findings.virtual_float,0.836);
run('mode="form"; answers[a.dataset.field]="unrepresentable"');a.value='';
assert.equal(run('validateNumericInputs()'),false,'An imported value hidden by native number sanitization must not pass');
for (const prefix of ['', 'ukr/', 'es/', 'pt/', 'de/', 'fr/', 'it/', 'da/', 'sv/', 'nb/', 'fi/']) {
  const page=fs.readFileSync('docs/'+prefix+'try.html','utf8');
  for (const name of names) {
    const normalized = text => text.replace(/setFiredRedflags\(\[\], 'uk'\)/g, "setFiredRedflags([], 'en')");
    assert.equal(normalized(fn(page,name)),normalized(fn(html,name)),prefix+name);
  }
  const labels=JSON.parse(page.match(/^const numericInputCopy = (.*);$/m)[1]);
  if(prefix) assert.notEqual(labels.integer,copy.integer,'Native numeric feedback in every language');
  assert(page.includes('step="any"')); assert(page.includes('aria-describedby'));
}
console.log('Strict numeric parsing, precision, authored bounds, unknown optional values, accessible errors, draft retention, generation/JSON blocking and correction recovery passed in all eleven clients');
