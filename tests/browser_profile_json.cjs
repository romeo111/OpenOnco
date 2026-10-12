const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const page=fs.readFileSync('docs/try.html','utf8');
function fn(html,name){const m=html.match(new RegExp(`^function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,name);return m[0].replace(/\r\n/g,'\n');}
const copy=JSON.parse(page.match(/^const profileInputCopy = (.*);$/m)[1]);
const textarea={value:''},errors=[];
const context=vm.createContext({textarea,profileInputCopy:copy,setError:e=>errors.push(e)});
vm.runInContext('let mode="json";'+fn(page,'profileInputError')+fn(page,'buildProfile'),context);
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
for(const prefix of ['', 'ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
 const html=fs.readFileSync('docs/'+prefix+'try.html','utf8');
 assert.equal(fn(html,'profileInputError'),fn(page,'profileInputError'));
 const labels=JSON.parse(html.match(/^const profileInputCopy = (.*);$/m)[1]);
 if(prefix)assert.notEqual(labels.object,copy.object);
 assert(html.includes("if (mode !== 'json') setError("),'Keep the specific JSON error instead of replacing it with a generic assembly failure');
}
console.log('Direct JSON: object/section/finite boundaries, localized errors and unchanged zero/false/null/decimal data passed in all eleven clients');
