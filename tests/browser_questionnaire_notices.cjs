// Own display claims must not become clinical guarantees or mutate source data.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const page=fs.readFileSync('docs/try.html','utf8');
function fn(html,name){const m=html.match(new RegExp(`^function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,name);return m[0].replace(/\r\n/g,'\n');}
const copy=JSON.parse(page.match(/^const questionnaireNoticeCopy = (.*);$/m)[1]);
const context=vm.createContext({questionnaireNoticeCopy:copy});
vm.runInContext(fn(page,'questionnaireIntro')+fn(page,'questionnaireDescription'),context);
const qs=JSON.parse(fs.readFileSync('docs/questionnaires.json','utf8'));
let starters=0,defaults=0,unknown=0;
for(const q of qs){
 const before=JSON.stringify(q);context.q=q;
 const intro=vm.runInContext('questionnaireIntro(q)',context);
 if((q.intro||'').startsWith('⚠ STUB questionnaire for ')){assert.equal(intro,copy.starter);starters++;}
 else assert.equal(intro,q.intro||'','Preserve other authored introductions');
 for(const group of q.groups){
  context.group=group;const text=vm.runInContext('questionnaireDescription(group)',context);
  if((group.description||'').includes('safe defaults')){assert.equal(text,copy.defaults);defaults++;}
  if((group.description||'').includes("replaces 'unevaluated RedFlag' warnings")){assert.equal(text,copy.unknown);unknown++;}
 }
 assert.equal(JSON.stringify(q),before,'Every field/default/source/clinical instruction remains unchanged');
}
assert.equal(starters,75);assert.equal(defaults,75);assert.equal(unknown,78);
context.group={description:'Authored clinical instruction: use 100 mg; review source SRC-VIRTUAL.'};
assert.equal(vm.runInContext('questionnaireDescription(group)',context),context.group.description);
for(const prefix of ['', 'ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
 const html=fs.readFileSync('docs/'+prefix+'try.html','utf8');
 for(const name of ['questionnaireIntro','questionnaireDescription'])assert.equal(fn(html,name),fn(page,name));
 const labels=JSON.parse(html.match(/^const questionnaireNoticeCopy = (.*);$/m)[1]);
 if(prefix)assert.notEqual(labels.defaults,copy.defaults);
 assert(html.includes('questIntro.textContent = questionnaireIntro(quest);'));
 assert(html.includes('escHtml(questionnaireDescription(group))'));
}
console.log('75 own safety-default/committee claims replaced for display; 78 missing-data descriptions clarified; source questions/defaults/rules untouched; native copy in all eleven clients');
