const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const form = JSON.parse(fs.readFileSync('docs/questionnaires.json','utf8')).find(q => q.id === 'QUEST-NSCLC-1L-STUB');
const questions = form.groups.flatMap(group => group.questions).filter(q => ['findings.histology','findings.stage','findings.driver_negative','findings.nsclc_taxane_choice'].includes(q.field));
assert.equal(questions.length,4);
for (const prefix of ['', 'ukr/', 'es/', 'pt/', 'de/', 'fr/', 'it/', 'da/', 'sv/', 'nb/', 'fi/']) {
  const source = fs.readFileSync('docs/'+prefix+'try.html','utf8');
  const copy = JSON.parse(source.match(/^const nsclcQuestionCopy = (.*);$/m)[1]);
  const fn = source.match(/^function displayQuestion\([^\n]*\{[\s\S]*?^\}/m)[0];
  const context = vm.createContext({ nsclcQuestionCopy: copy });
  vm.runInContext(fn,context);
  for (const question of questions) {
    const before = JSON.stringify(question);
    context.question = question;
    const shown = JSON.parse(JSON.stringify(vm.runInContext('displayQuestion(question)',context)));
    assert.equal(JSON.stringify(question),before,'Source questionnaire must stay canonical');
    assert.equal(shown.field,question.field);
    assert.equal(shown.type,question.type);
    assert.equal(shown.impact,question.impact);
    assert.deepEqual(shown.options.map(o=>o.value),question.options.map(o=>o.value));
    assert.equal(Object.hasOwn(shown,'default_value'),false);
    if (prefix) assert.notEqual(shown.label,question.label,prefix+question.field);
    if (prefix) assert.notEqual(shown.helper,question.helper,prefix+question.field);
    assert.equal(shown.label,copy[question.label] || question.label);
  }
  context.question = {field:'unrelated',label:'Confirmed NSCLC stage',options:[{value:false,label:'Not selected'}]};
  assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext('displayQuestion(question)',context))),context.question);
}
console.log('All eleven NSCLC displays preserve source fields, booleans, enum values and empty defaults');
