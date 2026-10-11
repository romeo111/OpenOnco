const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync('docs/try.html', 'utf8');
const names = ['waitForFrameLoad', 'downloadHtml', 'downloadPdf', 'updateWorkflowControls', 'switchResultLang'];
const code = names.map(name => {
  const match = html.match(new RegExp(`^(?:async )?function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`, 'm'));
  assert(match, name); return match[0];
}).join('\n');
const events = new Map(), timers = new Map(), errors = [];
let nextTimer = 0, blob, filename, prints = 0;
const button = () => ({ disabled: false });
const frame = {
  srcdoc: '<html>Previous report</html>',
  contentDocument: { documentElement: { dataset: { translationLocale: 'fr' }, outerHTML: '<html lang="fr"><a href="https://example.org/source">Source</a><p>DIS-AML 100 mg</p></html>' } },
  contentWindow: { focus() {}, print() { prints++; } },
  addEventListener: (type, fn) => events.set(type, fn),
  removeEventListener: type => events.delete(type),
};
const context = vm.createContext({
  resultFrame: frame, Blob, Date,
  setTimeout: fn => { const id = ++nextTimer; timers.set(id, fn); return id; },
  clearTimeout: id => timers.delete(id), setError: error => errors.push(error),
  URL: { createObjectURL: value => { blob = value; return 'blob:test'; }, revokeObjectURL() {} },
  document: { body: { appendChild() {}, removeChild() {} }, createElement: () => ({ click() { filename = this.download; } }) },
  isInteractionLocked: () => false, setLockedTitle() {}, refreshModeButtonAvailability() {}, openPlanModal() {},
  runBtn: button(), viewPlanBtn: button(), pdfBtn: button(), modalPdfBtn: button(), modalHtmlBtn: button(),
  resetBtn: button(), formatBtn: button(), diseaseSelect: button(), exampleSelect: button(), modeFormBtn: button(), modeJsonBtn: button(), personalizeBtn: button(),
  textarea: { value: '{}' }, activeQuest: {}, planModal: { hidden: false },
  UI_LOCK_TEXT: {}, withUiLock: async (_title, _lead, _hint, action) => action(),
});
vm.runInContext(`let reportReady=false,planSource='generated',planDirty=false,uiBusy=false,generating=false;
  let mode='json',currentResultMode='clinician',currentResultLang='en';` + code, context);
const run = value => vm.runInContext(value, context);
(async () => {
  run('downloadHtml(); downloadPdf(); updateWorkflowControls();');
  assert.equal(blob, undefined); assert.equal(prints, 0);
  assert.equal(context.runBtn.disabled, false, 'A failed report must allow generation again');
  let pending = run('waitForFrameLoad()');
  events.get('load')(); await pending;
  assert.equal(run('reportReady'), true); assert.equal(events.size, 0); assert.equal(timers.size, 0);
  run('downloadHtml(); downloadPdf();');
  assert.equal(await blob.text(), '<!DOCTYPE html>\n' + frame.contentDocument.documentElement.outerHTML);
  assert.match(filename, /^openonco-plan\.clinician\.fr\./); assert.equal(prints, 1);
  pending = run('waitForFrameLoad()');
  const failure = assert.rejects(pending, /failed to load/);
  events.get('error')(); await failure;
  assert.equal(run('reportReady'), false); assert.equal(context.modalHtmlBtn.disabled, true);
  assert.equal(context.runBtn.disabled, false);
  pending = run('waitForFrameLoad()');
  const timeout = assert.rejects(pending, /timed out/);
  timers.get(nextTimer)(); await timeout;
  assert.equal(run('reportReady'), false); assert.equal(events.size, 0);
  pending = run('waitForFrameLoad()'); events.get('load')(); await pending;
  assert.equal(run('reportReady'), true); assert.equal(errors.length, 2);
  pending = run("switchResultLang('en')");
  assert.equal(run('reportReady'), false, 'Same-source language reload must block export');
  run('downloadPdf()'); assert.equal(prints, 1);
  events.get('load')(); await pending;
  assert.equal(run('reportReady'), true);
  frame.contentDocument.documentElement.dataset = {};
  frame.contentDocument.documentElement.lang = 'uk';
  frame.contentDocument.documentElement.outerHTML = '<html lang="uk"><p>Український звіт</p></html>';
  run("currentResultMode='patient'; downloadHtml();");
  assert.match(filename, /^openonco-plan\.patient\.uk\./, 'Filename must reflect actual report language');
  assert.equal(await blob.text(), '<!DOCTYPE html>\n' + frame.contentDocument.documentElement.outerHTML);
  const overlay = fs.readFileSync('scripts/clinical-localization.js', 'utf8');
  assert(!overlay.includes('reloadReport'), 'Overlay must delegate all reloads to the guarded builder');
  assert(overlay.includes("await switchResultLang('en')"));
  const worker = fs.readFileSync('docs/sw.js', 'utf8');
  const swr = worker.match(/^function staleWhileRevalidate\([^\n]*\{[\s\S]*?^\}/m)[0];
  const cacheOptions = [];
  const sw = vm.createContext({ URL, CACHE_NAME: 'test', fetch: async () => ({ ok: true, clone() { return this; } }),
    caches: { open: async () => ({ match: async (_request, options) => { cacheOptions.push(options.ignoreSearch); }, put() {} }) },
  });
  vm.runInContext(swr, sw);
  for (const path of ['/clinical-localization.js?v=new', '/style.css?v=new']) {
    let response;
    sw.event = { request: { url: 'https://openonco.info' + path }, respondWith: value => { response = value; } };
    vm.runInContext('staleWhileRevalidate(event)', sw); await response;
  }
  assert.deepEqual(cacheOptions, [false, true], 'Translation script versions must remain distinct in cache');
  for (const locale of ['', 'ukr/', 'es/', 'pt/', 'de/', 'fr/']) {
    const page = fs.readFileSync(`docs/${locale}try.html`, 'utf8');
    assert(page.includes('const planFresh = reportReady && planSource !== null && !planDirty;'));
    assert(page.includes('if (planSource == null || !reportReady) return;'));
    assert(page.includes('if (!planSource || !reportReady || isInteractionLocked()) return;'));
  }
  console.log('Report export readiness, failure recovery, displayed language and six clients passed');
})().catch(error => { console.error(error); process.exitCode = 1; });
