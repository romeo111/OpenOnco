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
const currentBurkitt = current.find(questionnaire => questionnaire.id === 'QUEST-BURKITT-1L-STUB');
const recentBurkitt = structuredClone(currentBurkitt);
const scopeFields = ['findings.burkitt_high_risk', 'findings.cns_involvement'];
for (const group of recentBurkitt.groups) {
  for (const question of group.questions) {
    if (scopeFields.includes(question.field)) {
      question.default_value = question.field === 'findings.burkitt_high_risk';
      question.impact = 'recommended';
    }
  }
}
recentBurkitt.groups.find(group => group.title === 'General screening (optional)').questions.push({
  field: 'findings.cns_involvement', type: 'boolean', default_value: false,
});
recentBurkitt.last_reviewed = '2026-04-27';
recentBurkitt.notes = 'Obsolete cached protocol questions';
const recentBurkittBefore = JSON.stringify(recentBurkitt);
context.quest = recentBurkitt;
const upgradedBurkitt = JSON.parse(JSON.stringify(vm.runInContext('normalizeQuestionnaire(quest)', context)));
assert.deepEqual(upgradedBurkitt, currentBurkitt, 'Cached scope defaults and duplicates must not bypass current unanswered questions');
assert.equal(JSON.stringify(recentBurkitt), recentBurkittBefore, 'Cached questionnaire remains unchanged');
context.quest = upgradedBurkitt;
assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext('normalizeQuestionnaire(quest)', context))), currentBurkitt, 'Scope upgrade is idempotent');
for (const field of scopeFields) {
  const matching = upgradedBurkitt.groups.flatMap(group => group.questions).filter(question => question.field === field);
  assert.equal(matching.length, 1);
  assert.equal(matching[0].impact, 'critical');
  assert.equal(Object.hasOwn(matching[0], 'default_value'), false);
}
const currentNsclc = current.find(questionnaire => questionnaire.id === 'QUEST-NSCLC-1L-STUB');
const recentNsclc = structuredClone(currentNsclc);
for (const group of recentNsclc.groups) group.questions = group.questions.filter(question => !['findings.stage','findings.driver_negative','findings.nsclc_taxane_choice'].includes(question.field));
const recentBefore = JSON.stringify(recentNsclc);
context.quest = recentNsclc;
const upgraded = JSON.parse(JSON.stringify(vm.runInContext('normalizeQuestionnaire(quest)', context)));
assert.deepEqual(upgraded, currentNsclc, 'A cached form with histology alone must receive all current applicability questions');
assert.equal(JSON.stringify(recentNsclc), recentBefore);
for (const field of ['findings.histology','findings.stage','findings.driver_negative','findings.nsclc_taxane_choice']) {
  const question = upgraded.groups.flatMap(group => group.questions).find(question => question.field === field);
  assert.equal(question.impact, 'critical');
  assert.equal(Object.hasOwn(question, 'default_value'), false, field);
}
for (const prefix of ['', 'ukr/', 'es/', 'pt/', 'de/', 'fr/', 'it/', 'da/', 'sv/', 'nb/', 'fi/']) {
  const page = fs.readFileSync('docs/'+prefix+'try.html','utf8');
  assert(page.includes('quest = normalizeQuestionnaire(quest);'));
  assert.equal(page.match(/^function normalizeQuestionnaire\([^\n]*\{[\s\S]*?^\}/m)[0].replace(/\r\n/g,'\n'), code.replace(/\r\n/g,'\n'));
}
console.log('All 78 legacy cached forms match corrected data; authored values preserved; eleven clients normalize before rendering');
