// Shipped mode switching must preserve actual answers and caller-supplied drafts.
const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict');
const html = fs.readFileSync('docs/try.html', 'utf8');
function fn(page, name) {
  const match = page.match(new RegExp(`^function ${name}\\([^\\n]*\\{[\\s\\S]*?^\\}`, 'm'));
  assert(match, name); return match[0].replace(/\r\n/g, '\n');
}
const code = fn(html, 'setMode') + '\n' + fn(html, 'buildProfile');
function fixture() {
  const fixed = { disease: { id: 'DIS-VIRTUAL' }, metadata: { synthetic: true } };
  const answers = { patient_id: 'VIRTUAL-MODE-001', 'demographics.ecog': 0,
    'findings.virtual_boolean': false, 'findings.virtual_measurement': 12.34 };
  const textarea = { value: '{"patient_id":"VIRTUAL-OLD","demographics":{"ecog":3}}' };
  const calls = { saves: [], updates: 0 };
  const context = vm.createContext({
    validateNumericInputs: () => true, fixed, answers, textarea,
    modeFormBtn: { classList: { toggle() {} } }, modeJsonBtn: { classList: { toggle() {} } },
    formPane: {}, jsonPane: {},
    saveDraft: () => calls.saves.push(textarea.value), updateRunBtnEnabled: () => calls.updates++,
  });
  vm.runInContext('let mode="form",activeQuest={fixed_fields:fixed};' + code, context);
  return { context, textarea, fixed, calls, run: s => vm.runInContext(s, context) };
}
let f = fixture();
const before = JSON.stringify(f.fixed);
const expected = JSON.parse(JSON.stringify(f.run('buildProfile()')));
f.run('setMode("json", {syncFromForm:true})');
assert.deepEqual(JSON.parse(f.textarea.value), expected, 'Mode changes must transfer current answers, not stale JSON');
assert.equal(JSON.stringify(f.fixed), before, 'Questionnaire fixed fields remain unchanged');
assert.equal(JSON.parse(f.textarea.value).demographics.ecog, 0);
assert.equal(JSON.parse(f.textarea.value).findings.virtual_boolean, false);
assert.equal(JSON.parse(f.textarea.value).findings.virtual_measurement, 12.34);
assert.equal(f.calls.saves.at(-1), f.textarea.value, 'Save only after copying current values');
assert.equal(f.context.formPane.hidden, true); assert.equal(f.context.jsonPane.hidden, false);
// Restoring caller-supplied JSON must preserve extra fields, formatting and even
// an unfinished draft rather than silently replacing it with the form snapshot.
for (const supplied of [' {"patient_id":"VIRTUAL-DRAFT","unmapped":{"value":0}}\n', '{"patient_id":']) {
  f = fixture(); f.textarea.value = supplied;
  f.run('setMode("json")');
  assert.equal(f.textarea.value, supplied);
  f.run('setMode("json", {syncFromForm:true})');
  assert.equal(f.textarea.value, supplied, 'Repeated JSON clicks must not rewrite raw input');
}
f = fixture(); f.textarea.value = '';
f.run('setMode("json", {syncFromForm:true})');
assert.equal(JSON.parse(f.textarea.value).patient_id, 'VIRTUAL-MODE-001', 'An empty old JSON pane cannot erase the form');
f = fixture(); f.run('activeQuest=null');
const original = f.textarea.value;
f.run('setMode("json", {syncFromForm:true})');
assert.equal(f.textarea.value, original, 'Without a questionnaire, preserve existing raw input');
for (const prefix of ['', 'ukr/', 'es/', 'pt/', 'de/', 'fr/', 'it/', 'da/', 'sv/', 'nb/', 'fi/']) {
  const page = fs.readFileSync('docs/' + prefix + 'try.html', 'utf8');
  assert.equal(fn(page, 'setMode'), fn(html, 'setMode'));
  assert.equal(fn(page, 'buildProfile'), fn(html, 'buildProfile'));
  assert(page.includes("modeJsonBtn.addEventListener('click', () => { if (!isInteractionLocked()) setMode('json', { syncFromForm: true }); }"));
}
console.log('Current form profile transfers to JSON; zero/false/decimals preserved; draft/example/QR raw data and incomplete edits retained; all eleven clients match');
