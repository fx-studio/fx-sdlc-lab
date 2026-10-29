// E9 · incident T-014 (reached customers): with todos in the list, a filter tab that shows none of them said "Chưa có việc nào…
// hãy bấm Nhập từ file", and a customer nearly imported an old backup over her list. Accepted fix: 2aa698d (base 16d2846).
// Checks only the requirement, not that fix's design: when the list has todos, #empty is either hidden or says something other
// than the empty-list sentence this same build shows for a truly empty list, and never points to importing a backup. A
// filter-specific sentence ("Chưa có việc nào đã xong") passes as well as hiding #empty does. A truly empty list must still show it.
const test = require('node:test');
const assert = require('node:assert/strict');
const { loadApp, todos } = require('./_harness.js');

const IMPORT_HINT = /nhập từ file|sao lưu|backup/i;

function emptyListText() {
  const { $ } = loadApp([]);
  assert.equal($('#empty').hidden, false, 'a truly empty list still shows the empty-list sentence');
  const text = $('#empty').textContent;
  assert.ok(text.trim().length > 0, 'the empty-list sentence is not blank');
  return text;
}

function assertNotSaidEmpty(app, emptyText, where) {
  const el = app.$('#empty');
  if (el.hidden) return;
  assert.notEqual(el.textContent, emptyText, `${where}: does not show the empty-list sentence`);
  assert.doesNotMatch(el.textContent, IMPORT_HINT, `${where}: does not suggest importing a backup`);
}

test('E9: a truly empty list still shows the empty-list sentence, in every tab', () => {
  emptyListText();
  for (const f of ['open', 'done', 'all']) {
    const app = loadApp([]);
    app.filter(f);
    assert.equal(app.$('#empty').hidden, false, `empty list, tab ${f}: sentence shown`);
  }
});

const CASES = [
  { name: '4 open todos, tab "Đã xong" (the T-014 report)', list: todos(4, false), tab: 'done' },
  { name: '3 done todos, tab "Chưa xong"', list: todos(3, true), tab: 'open' },
];

for (const c of CASES) {
  test(`E9: ${c.name}: not told the list is empty`, () => {
    const emptyText = emptyListText();
    const app = loadApp(c.list);
    assertNotSaidEmpty(app, emptyText, 'tab Tất cả on load');
    app.filter(c.tab);
    assertNotSaidEmpty(app, emptyText, `tab ${c.tab}`);
    app.filter('all');
    assertNotSaidEmpty(app, emptyText, 'back to tab Tất cả');
  });
}
