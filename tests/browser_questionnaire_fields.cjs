const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const zlib = require('node:zlib');
const source = fs.readFileSync('docs/try.html', 'utf8');
const code = source.match(/^function normalizeQuestionnaire\([^\n]*\{[\s\S]*?^\}/m)[0];
const context = vm.createContext({});
vm.runInContext(code, context);
// Exercise the actual older published payload that users may still cache.
const cached = JSON.parse(zlib.gunzipSync(fs.readFileSync('tests/fixtures/legacy-questionnaires-duplicate-screening.json.gz')));
const current = JSON.parse(fs.readFileSync('docs/questionnaires.json', 'utf8'));
assert.equal(cached.length, current.length);
for (const original of cached) {
  const before = JSON.stringify(original);
  context.quest = original;
  const normalized = JSON.parse(JSON.stringify(vm.runInContext('normalizeQuestionnaire(quest)',context)));
  const expected = current.find(questionnaire => questionnaire.id === original.id);
  assert.deepEqual(normalized, expected, original.id);
  assert.equal(JSON.stringify(original), before, 'Cached payload must remain unchanged');
  const fields = normalized.groups.flatMap(group => group.questions.map(question => question.field));
  assert.equal(fields.length, new Set(fields).size, original.id);
}
for (const prefix of ['', 'ukr/', 'es/', 'pt/', 'de/', 'fr/', 'it/', 'da/', 'sv/', 'nb/', 'fi/']) {
  const page = fs.readFileSync('docs/'+prefix+'try.html','utf8');
  assert(page.includes('quest = normalizeQuestionnaire(quest);'));
  assert.equal(page.match(/^function normalizeQuestionnaire\([^\n]*\{[\s\S]*?^\}/m)[0], code);
}
console.log('All 78 legacy cached forms match corrected data; authored values preserved; eleven clients normalize before rendering');
