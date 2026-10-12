const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function fn(p,n){const m=p.match(new RegExp(`^function ${n}\\([^\\n]*\\{[\\s\\S]*?^\\}`,'m'));assert(m,n);return m[0].replace(/\r\n/g,'\n');}
const root=fs.readFileSync('docs/try.html','utf8');
const names=['openPlanModal','closePlanModal','planModalFocusableElements','containPlanModalFocus','handlePlanModalKeys'];
for(const prefix of ['', 'ukr/','es/','pt/','de/','fr/','it/','da/','sv/','nb/','fi/']){
 const page=fs.readFileSync('docs/'+prefix+'try.html','utf8'),doc={activeElement:null};let locked=false;
 const control=()=>({ownerDocument:doc,isConnected:true,disabled:false,tabIndex:0,getClientRects:()=>[{}],closest:()=>null,focus(){doc.activeElement=this;}});
 const opener=control(),first=control(),close=control(),frame=control(),outside=control(),disabled=control(),hidden=control();
 disabled.disabled=true;hidden.getClientRects=()=>[];
 const controls=[first,disabled,hidden,close,frame],modal={hidden:true,querySelectorAll:()=>controls,contains:e=>controls.includes(e)};
 const c=vm.createContext({document:doc,resultFrame:frame,planModal:modal,planModalClose:close,viewPlanBtn:opener,runBtn:control(),highlightLangButtons(){},isInteractionLocked:()=>locked});
 vm.runInContext('let reportReady=true,planSource="example",planModalReturnFocus=null;'+names.map(n=>fn(page,n)).join('\n'),c);
 const run=s=>vm.runInContext(s,c),key=(name,shift=false,owner=doc)=>{c.event={key:name,shiftKey:shift,defaultPrevented:false,target:{ownerDocument:owner},preventDefault(){this.defaultPrevented=true;}};run('handlePlanModalKeys(event)');return c.event;};
 outside.focus();c.invoker=opener;run('openPlanModal({currentTarget:invoker})');assert.equal(doc.activeElement,close);
 first.focus();assert(key('Tab',true).defaultPrevented);assert.equal(doc.activeElement,frame);
 assert(key('Tab').defaultPrevented);assert.equal(doc.activeElement,first);
 outside.focus();run('containPlanModalFocus()');assert.equal(doc.activeElement,close);
 const childFirst=control(),childLast=control(),childMiddle=control();const childDoc={activeElement:childMiddle,querySelectorAll:()=>[childFirst,childMiddle,childLast]};assert(key('Escape',false,childDoc).defaultPrevented);assert.equal(modal.hidden,true);assert.equal(doc.activeElement,opener,'Iframe Escape returns to the invoker');
 opener.focus();run('openPlanModal()');locked=true;key('Escape');assert.equal(modal.hidden,false,'Generation lock cannot be bypassed by Escape');locked=false;
 assert.equal(key('Tab',false,childDoc).defaultPrevented,false,'Native iframe tab order stays intact');
 childDoc.activeElement=childLast;assert(key('Tab',false,childDoc).defaultPrevented);assert.equal(doc.activeElement,first,'The last report link wraps to the first dialog control');
 childDoc.activeElement=childFirst;assert(key('Tab',true,childDoc).defaultPrevented);assert.equal(doc.activeElement,close,'Reverse tabbing from the first report control returns before the iframe');
 run('closePlanModal()');assert.equal(doc.activeElement,opener);
 opener.focus();run('openPlanModal()');opener.isConnected=false;opener.disabled=true;run('closePlanModal()');assert.equal(doc.activeElement,c.runBtn,'Use an available workflow control when the invoker is gone');
 for(const n of names)assert.equal(fn(page,n),fn(root,n));
 assert(page.includes("document.addEventListener('focusin', containPlanModalFocus)"));
 assert(page.includes("doc.addEventListener('keydown', handlePlanModalKeys)"));
}
console.log('Dialog opening/return focus, Tab/Shift+Tab boundaries, iframe Escape, background focus containment and loading locks passed in all eleven clients');
