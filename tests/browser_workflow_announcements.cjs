const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function fn(p,n){const m=p.match(new RegExp(`^function ${n}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,n);return m[0].replace(/\r\n/g,'\n');}
const root=fs.readFileSync('docs/try.html','utf8');
const names=['flushWorkflowAnnouncements','setStatus','setError','setGeneratingUI'];
for(const prefix of ['', 'ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
 const page=fs.readFileSync('docs/'+prefix+'try.html','utf8');
 const classes={remove(){},toggle(){}};
 const c=vm.createContext({mainTryEl:{inert:false},workflowStatusAnnouncement:{textContent:''},workflowErrorAnnouncement:{textContent:''},
  status:{textContent:'',dataset:{},classList:classes},statusTop:{classList:classes,dataset:{}},statusTopText:{},errorBox:{hidden:true},
  generatingOverlay:{hidden:true},generatingTitle:{},generatingLead:{},UI_LOCK_TEXT:{generateTitle:'VIRTUAL-TITLE',generateLead:'VIRTUAL-LEAD'},
  clearLoadingProgress(){},setGeneratingHint(){}});
 vm.runInContext('let pendingWorkflowStatus="",pendingWorkflowError="";'+names.map(n=>fn(page,n)).join('\n'),c);
 const run=s=>vm.runInContext(s,c);
 run('setError("VIRTUAL-INVALID-JSON")');assert.equal(c.workflowErrorAnnouncement.textContent,'VIRTUAL-INVALID-JSON');assert.equal(c.errorBox.hidden,false);
 run('setError(null)');assert.equal(c.workflowErrorAnnouncement.textContent,'');assert.equal(c.errorBox.hidden,true);
 run('setGeneratingUI(true);setStatus("VIRTUAL-PENDING","info");setError("VIRTUAL-LOADING-FAILED");setStatus("VIRTUAL-FINAL","ok")');
 assert.equal(c.mainTryEl.inert,true);assert.equal(c.workflowStatusAnnouncement.textContent,'');assert.equal(c.workflowErrorAnnouncement.textContent,'');
 assert.equal(c.statusTop.hidden,true,'Success may hide the visual top banner without losing its announcement');
 run('setGeneratingUI(false)');assert.equal(c.mainTryEl.inert,false);assert.equal(c.generatingOverlay.hidden,true);
 assert.equal(c.workflowStatusAnnouncement.textContent,'VIRTUAL-FINAL');assert.equal(c.workflowErrorAnnouncement.textContent,'VIRTUAL-LOADING-FAILED');
 for(const [id,role] of [['workflowStatusAnnouncement','status'],['workflowErrorAnnouncement','alert']]){
  const start=page.indexOf('id="'+id+'"');assert(start>page.indexOf('</main>'),'Live regions remain outside inert main');
  const tag=page.slice(start,page.indexOf('>',start));assert(tag.includes('role="'+role+'"'));assert(tag.includes('aria-atomic="true"'));assert(!/\shidden(?:\s|=|$)/.test(tag));
 }
 assert(/id="generatingOverlay"[^>]*aria-labelledby="generatingTitle"[^>]*aria-describedby="generatingLead generatingHint"/.test(page));
 for(const n of names)assert.equal(fn(page,n),fn(root,n));
}
console.log('Persistent status/alert regions, deferred messages after unlock, cleared errors and named loading dialog passed in all eleven clients; actual screen-reader speech remains unverified');
