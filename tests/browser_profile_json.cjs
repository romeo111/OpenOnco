const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const page=fs.readFileSync('docs/try.html','utf8');
function fn(html,name){const m=html.match(new RegExp(`^function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,name);return m[0].replace(/\r\n/g,'\n');}
const copy=JSON.parse(page.match(/^const profileInputCopy = (.*);$/m)[1]);
const textarea={value:''},errors=[];
const context=vm.createContext({textarea,profileInputCopy:copy,setError:e=>errors.push(e),isInteractionLocked:()=>false});
vm.runInContext('let mode="json";'+fn(page,'profileInputError')+fn(page,'buildProfile')+fn(page,'formatProfileJson'),context);
for(const [text,error] of [['[]',copy.object],['null',copy.object],['42',copy.object],['"VIRTUAL"',copy.object],
 ['{"findings":[]}',copy.section+' findings'],['{"demographics":false}',copy.section+' demographics'],
 ['{"findings":{"nested":[{"value":1e9999}]}}',copy.finite],['{"findings":{"value":-1e9999}}',copy.finite],
 ['{"findings":{"value":NaN}}',copy.json],['{"patient_id":',copy.json]]){
 textarea.value=text;assert.equal(vm.runInContext('buildProfile()',context),null);assert.equal(errors.at(-1),error);
}
textarea.value='{"patient_id":"VIRTUAL-JSON-001","findings":{"value":0.836,"negative":false,"zero":0,"unknown":null},"demographics":null}';
const profile=vm.runInContext('buildProfile()',context);
assert.deepEqual(JSON.parse(JSON.stringify(profile)),JSON.parse(textarea.value));
// Wide valid JSON must not hit JavaScript's function-argument limit, and the
// numeric guard must still examine the final value rather than truncate work.
const wideCount=180000;
const wide={patient_id:'VIRTUAL-WIDE-JSON',metadata:{samples:Array(wideCount).fill(0)}};
textarea.value=JSON.stringify(wide);
assert(vm.runInContext('buildProfile()',context),'A valid wide array remains valid JSON');
assert.equal(vm.runInContext('buildProfile().metadata.samples.length',context),wideCount);
textarea.value='{"patient_id":"VIRTUAL-WIDE-INVALID","metadata":{"samples":['+'0,'.repeat(wideCount-1)+'1e9999]}}';
assert.equal(vm.runInContext('buildProfile()',context),null);assert.equal(errors.at(-1),copy.finite,'Inspect the final value in a wide array');
textarea.value='{"patient_id":"VIRTUAL-WIDE-INVALID","metadata":{"samples":[1e9999,'+'0,'.repeat(wideCount-2)+'0]}}';
assert.equal(vm.runInContext('buildProfile()',context),null);assert.equal(errors.at(-1),copy.finite,'Inspect early values after traversing the entire wide collection');
const wideObject={patient_id:'VIRTUAL-WIDE-OBJECT',metadata:Object.fromEntries(Array.from({length:wideCount},(_,i)=>['virtual_'+i,0]))};
textarea.value=JSON.stringify(wideObject);
assert(vm.runInContext('buildProfile()',context),'A valid wide object remains valid JSON');
const ambiguous = [
 '{"demographics":{"age":17,"age":61}}',
 '{"concomitant_medications":{"status":"partial","status":"complete","drug_ids":[]}}',
 '{"concomitant_medications":{"status":"complete","drug_ids":["DRUG-BLEOMYCIN"],"drug_ids":[]}}',
 '{"biomarkers":{"BIO-CD30-IHC":"negative","BIO-CD30-IHC":"positive"}}',
 '{"metadata":[{"value":0,"value":0}]}',
 String.raw`{"metadata":{"status":0,"\u0073tatus":1}}`,
 String.raw`{"metadata":{"a\"b":0,"a\u0022b":1}}`,
 '{"metadata":{"__proto__":0,"__proto__":1}}',
];
for (const text of ambiguous) {
 textarea.value=text;
 assert.equal(vm.runInContext('buildProfile()',context),null,'Ambiguous JSON cannot generate a profile');
 assert.equal(errors.at(-1),copy.duplicate);
 vm.runInContext('formatProfileJson()',context);
 assert.equal(textarea.value,text,'Formatting must preserve conflicting original text for correction');
 assert.equal(errors.at(-1),copy.duplicate);
}
// JSON.parse rounds unsafe integers before the engine can inspect them.
for (const numeric of ['9007199254740992','9007199254740993','-9007199254740993','1e20']) {
 const original='{"metadata":{"nested":[{"value":'+numeric+'}]}}';
 textarea.value=original;
 assert.equal(vm.runInContext('buildProfile()',context),null);
 assert.equal(errors.at(-1),copy.integerRange);
 vm.runInContext('formatProfileJson()',context);
 assert.equal(textarea.value,original,'Unsafe integers must not be rewritten after rounding');
 assert.equal(errors.at(-1),copy.integerRange);
}
for (const numeric of ['9007199254740991','-9007199254740991','42','0','-0','0.836','1.25e-3']) {
 textarea.value='{"metadata":{"value":'+numeric+'}}';
 assert(vm.runInContext('buildProfile()',context),'Safe integers and ordinary decimals remain accepted');
}
textarea.value='{"patient_id":"9007199254740993","metadata":{"value":"1e20"}}';
assert(vm.runInContext('buildProfile()',context),'Text identifiers are not coerced into numbers');
const safe={patient_id:'VIRTUAL-KEY-CONTROL',metadata:[{status:0},{status:false}],text:'{"status":0,"status":1}',nested:{brackets:'[{},] and escaped " quotes',value:null}};
textarea.value=JSON.stringify(safe);
assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext('buildProfile()',context))),safe);
vm.runInContext('formatProfileJson()',context);
assert.deepEqual(JSON.parse(textarea.value),safe,'Valid formatting preserves values');
assert.equal(errors.at(-1),'');
for(const prefix of ['', 'ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
 const html=fs.readFileSync('docs/'+prefix+'try.html','utf8');
 for (const name of ['profileInputError','buildProfile','formatProfileJson']) assert.equal(fn(html,name),fn(page,name));
 const labels=JSON.parse(html.match(/^const profileInputCopy = (.*);$/m)[1]);
 assert(labels.duplicate);
 assert(labels.integerRange);
 if(prefix){assert.notEqual(labels.integerRange,copy.integerRange);assert.notEqual(labels.object,copy.object);assert.notEqual(labels.duplicate,copy.duplicate);}
 assert(html.includes("if (mode !== 'json') setError("),'Keep the specific JSON error instead of replacing it with a generic assembly failure');
}
console.log('Direct JSON: object/section/finite boundaries, localized errors and unchanged zero/false/null/decimal data passed in all eleven clients');
