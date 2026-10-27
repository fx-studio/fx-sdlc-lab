// Pins what add() in app/app.js makes, so a backup the app itself made always imports again (Khoa's review of commit B:
// isValidTodo rejects whitespace-only titles and non-string ids). app.js is a plain page script with no exports, so it
// runs unchanged in a vm context with a minimal fake page. Run: node --test
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const backup = require('../app/backup.js');

const appJs = fs.readFileSync(path.join(__dirname, '..', 'app', 'app.js'), 'utf8');

function fakeElement() {
  const el = {
    textContent: '', innerHTML: '', hidden: false, value: '', className: '', dataset: {},
    append() {},
    querySelector(sel) { return (el.children[sel] ||= fakeElement()); },
    children: {},
  };
  return el;
}

// Loads app.js on a readable list (empty unless given) and returns the add form plus every list the app tried to save.
function loadApp(initial = []) {
  const elements = {};
  const saved = [];
  const replaced = [];
  const store = {
    readError: false,
    load() { return { todos: initial, readError: false }; },
    save(todos) { saved.push(todos.map((t) => ({ ...t }))); return 'saved'; },
    replace(todos) { replaced.push(todos); return 'saved'; },
  };
  const document = {
    querySelector(sel) { return (elements[sel] ||= fakeElement()); },
    querySelectorAll() { return []; },
    createElement() { return fakeElement(); },
  };
  vm.runInNewContext(appJs, { ...backup, store, document, crypto });
  const submit = (value) => {
    document.querySelector('#title').value = value;
    document.querySelector('#add').onsubmit({ preventDefault() {} });
  };
  // The confirm dialog records each question and answers "Huỷ".
  const asked = [];
  Object.assign(document.querySelector('#confirm'), {
    showModal() { asked.push(document.querySelector('#confirm-text').textContent); },
    addEventListener(type, fn) { queueMicrotask(fn); },
  });
  const pick = (file) => document.querySelector('#import').onchange({ target: { files: [file], value: '' } });
  const count = () => document.querySelector('#count').textContent;
  return { submit, saved, replaced, asked, pick, count };
}

// A file whose text() resolves only when the test says so.
function slowFile(text) {
  let finish;
  const done = new Promise((resolve) => { finish = resolve; });
  return { file: { size: text.length, text: () => done.then(() => text) }, finish };
}

function backupOf(...titles) {
  return backup.toBackupText(titles.map((title, i) => ({ id: `id-${title}-${i}`, title, done: false, createdAt: 1 })));
}

test('add form: trims the title and makes a string id', () => {
  const { submit, saved } = loadApp();
  submit('  Mua sữa  ');
  assert.equal(saved.length, 1);
  const [t] = saved[0];
  assert.equal(t.title, 'Mua sữa');
  assert.equal(typeof t.id, 'string');
  assert.notEqual(t.id, '');
  assert.equal(t.done, false);
  assert.equal(typeof t.createdAt, 'number');
});

test('add form: skips a whitespace-only title', () => {
  const { submit, saved } = loadApp();
  submit('   ');
  submit('\t\n');
  assert.equal(saved.length, 0);
});

test('open-todo count line: a dot every three digits from 1,000 up, like every other sentence (Linh, R9)', () => {
  const todos = (n, done = false) =>
    Array.from({ length: n }, (_, i) => ({ id: `id-${done}-${i}`, title: `Việc ${i}`, done, createdAt: 1 }));
  const { submit, count } = loadApp([...todos(999), ...todos(5, true)]);
  assert.equal(count(), '999 việc chưa xong');
  submit('Việc thứ 1000');
  assert.equal(count(), '1.000 việc chưa xong');
  assert.equal(loadApp(todos(12)).count(), '12 việc chưa xong');
  assert.equal(loadApp(todos(2001)).count(), '2.001 việc chưa xong');
  assert.equal(loadApp(todos(12500)).count(), '12.500 việc chưa xong');
});

test('a backup of todos the app made imports again', () => {
  const { submit, saved } = loadApp();
  for (const v of ['Mua sữa', '  Gọi mẹ ', '   ', 'Nộp thuế']) submit(v);
  const todos = saved.at(-1);
  assert.equal(todos.length, 3);
  const parsed = backup.parseBackup(backup.toBackupText(todos));
  assert.equal(parsed.ok, true, parsed.message);
  assert.deepEqual(parsed.todos, todos);
});

test('two overlapping imports: the later-finishing one asks before replacing the list the first one filled', async () => {
  const { replaced, asked, pick } = loadApp();
  const large = slowFile(backupOf('Lớn 1', 'Lớn 2', 'Lớn 3'));
  const small = slowFile(backupOf('Nhỏ'));
  const first = pick(large.file);
  const second = pick(small.file);
  small.finish();
  await second;
  assert.equal(replaced.length, 1, 'the small file fills the empty list without asking');
  assert.deepEqual(asked, []);
  large.finish();
  await first;
  assert.deepEqual(asked, [backup.fill(backup.MESSAGES.confirmReplace, { n: 1, m: 3 })]);
  assert.equal(replaced.length, 1, 'cancelled, so the list from the small file stays');
});
