'use strict';
// F2 · Nhập lại từ file. AC3, AC5–AC11, AC14.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const backup = require('../app/backup.js');
const {
  KEY, NOT_SAVED_HINT, FakeStorage, seeded, openApp, makeTodos, backupText, fileOf, asker, bigTodos, nfc,
} = require('./helpers.js');

// A rejected import: list on screen and in storage unchanged, no question asked, a message shown.
async function assertRejected(storage, store, current, text, label) {
  const before = storage.raw();
  const ask = asker(true);
  const res = await backup.importBackup({ store, current, file: fileOf(text), ask });
  assert.deepEqual(ask.questions, [], `${label}: no confirm question for a rejected file`);
  assert.deepEqual(res.todos, current, `${label}: list on screen unchanged`);
  assert.equal(storage.raw(), before, `${label}: stored list unchanged`);
  // The spec fixes no wording for the rejection, only that the customer is told (why + what next).
  assert.equal(typeof res.message, 'string', `${label}: customer is told`);
  assert.ok(res.message.trim().length > 0, `${label}: message is not empty`);
  return res;
}

test('AC3: after clearing site data the list is empty (no read error, empty line points to "Nhập từ file"); importing the AC1 file asks nothing, shows 3 todos, and they survive a reload', async () => {
  const storage = new FakeStorage();
  const { store, STORE_KEY, loaded } = openApp(storage);
  assert.equal(STORE_KEY, KEY);
  assert.deepEqual(loaded.todos, []);
  assert.equal(loaded.readError, false, 'no key yet is a normal empty list, not a read error');
  assert.equal(store.readError, false);

  // AMBIGUOUS: the spec says the empty line "chỉ tới nút 'Nhập từ file'"; read as naming the button.
  assert.ok(nfc(backup.MESSAGES.emptyList).includes(nfc('Nhập từ file')), 'empty line points to "Nhập từ file"');

  const todos = [
    { id: 'a1', title: 'Đi chợ', done: true, createdAt: 1760000000000 },
    { id: 'a2', title: 'Gọi mẹ', done: false, createdAt: 1760000001000 },
    { id: 'a3', title: 'Trả tiền điện', done: false, createdAt: 1760000002000 },
  ];
  const text = backup.toBackupText(todos); // the file from AC1
  assert.equal(backup.confirmText({ readError: false, current: 0, incoming: 3 }), null);

  const ask = asker(true);
  const res = await backup.importBackup({ store, current: loaded.todos, file: fileOf(text), ask });
  assert.deepEqual(ask.questions, [], 'no confirm dialog when the list is empty');
  assert.deepEqual(res.todos, todos);
  assert.equal(typeof res.message, 'string');
  assert.ok(res.message.includes('3'), `import message should say how many were imported: ${res.message}`);

  const reloaded = openApp(storage).loaded;
  assert.equal(reloaded.readError, false);
  assert.deepEqual(reloaded.todos, todos);
});

async function replaceFlow(nCurrent) {
  const current = makeTodos(nCurrent, 'cu');
  const incoming = makeTodos(30, 'moi');
  const text = backupText(incoming);
  const expected = `Thay ${nCurrent} việc hiện có bằng 30 việc trong file?`;

  const q = backup.confirmText({ readError: false, current: nCurrent, incoming: 30 });
  assert.equal(typeof q, 'string');
  assert.ok(nfc(q).includes(nfc(expected)), `confirm text should contain "${expected}", got "${q}"`);

  // Cancel: asked before anything changed; nothing written; same list after reload.
  const storage = seeded(current);
  let app = openApp(storage);
  assert.deepEqual(app.loaded.todos, current);
  const rawBefore = storage.raw();
  let rawAtAsk;
  const no = asker(false, () => { rawAtAsk = storage.raw(); });
  let res = await backup.importBackup({ store: app.store, current: app.loaded.todos, file: fileOf(text), ask: no });
  assert.equal(no.questions.length, 1, 'confirm question asked once');
  assert.ok(nfc(no.questions[0]).includes(nfc(expected)), `question asked: ${no.questions[0]}`);
  assert.equal(rawAtAsk, rawBefore, 'nothing written before the customer answers');
  assert.deepEqual(res.todos, current);
  assert.equal(storage.raw(), rawBefore, 'cancel writes nothing');
  assert.deepEqual(openApp(storage).loaded.todos, current);

  // Again, agree: exactly the 30 from the file, none of the old ones; survives reload.
  app = openApp(storage);
  const yes = asker(true, () => { rawAtAsk = storage.raw(); });
  res = await backup.importBackup({ store: app.store, current: app.loaded.todos, file: fileOf(text), ask: yes });
  assert.equal(yes.questions.length, 1);
  assert.equal(rawAtAsk, rawBefore, 'nothing written before the customer answers');
  assert.deepEqual(res.todos, incoming);
  const oldIds = new Set(current.map((t) => t.id));
  assert.ok(res.todos.every((t) => !oldIds.has(t.id)), 'no old todo left (replace, not merge)');
  assert.equal(typeof res.message, 'string');
  assert.ok(res.message.includes('30'), `import message should say how many were imported: ${res.message}`);
  assert.deepEqual(openApp(storage).loaded.todos, incoming);
}

test('AC5: 12 todos, import 30 → asks "Thay 12 việc hiện có bằng 30 việc trong file?" first; cancel keeps 12, agree gives exactly the 30 and survives reload', async () => {
  // "không có nút Undo" is a UI check (see report).
  await replaceFlow(12);
});

test('AC6: exactly 1 todo, import 30 → asks "Thay 1 việc hiện có bằng 30 việc trong file?"; cancel keeps 1, agree gives 30 and survives reload', async () => {
  await replaceFlow(1);
});

test('AC7: a file over 1 MB is refused, list unchanged, customer told', async () => {
  // AMBIGUOUS: "1 MB" is not fixed as 1,000,000 or 1,048,576 bytes; accept either.
  assert.ok([1000000, 1048576].includes(backup.MAX_IMPORT_BYTES), `MAX_IMPORT_BYTES = ${backup.MAX_IMPORT_BYTES}`);

  // A file that is otherwise a valid backup, so only the size can be the reason.
  const text = backupText(bigTodos(5000));
  assert.ok(Buffer.byteLength(text) > backup.MAX_IMPORT_BYTES, 'test file must be over the limit');

  const current = makeTodos(12, 'cu');
  const storage = seeded(current);
  const { store, loaded } = openApp(storage);
  await assertRejected(storage, store, loaded.todos, text, 'over 1 MB');
});

test('AC8: a file with an unknown field is refused, list unchanged, customer told', async () => {
  const current = makeTodos(3, 'cu');
  const storage = seeded(current);
  const { store, loaded } = openApp(storage);

  const withExtraInTodo = makeTodos(30, 'moi');
  withExtraInTodo[5] = { ...withExtraInTodo[5], x: 1 };
  const t1 = backupText(withExtraInTodo);
  const p1 = backup.parseBackup(t1);
  assert.equal(p1.ok, false, 'unknown field in a todo is refused');
  assert.equal(typeof p1.message, 'string');
  await assertRejected(storage, store, loaded.todos, t1, 'unknown field in a todo');

  // Spec F2 step 3 / Data: "không có trường lạ" applies to the file structure too.
  const t2 = backupText(makeTodos(30, 'moi'), { x: 1 });
  assert.equal(backup.parseBackup(t2).ok, false, 'unknown top-level field is refused');
  await assertRejected(storage, store, loaded.todos, t2, 'unknown top-level field');
});

test('AC9: a file that is not a backup (image, any text file, wrong structure) is refused, list unchanged, customer told', async () => {
  const current = makeTodos(3, 'cu');
  const storage = seeded(current);
  const { store, loaded } = openApp(storage);

  const good = makeTodos(2, 'moi');
  const bad = {
    'image (PNG bytes)': Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0, 0, 0, 0x0d, 0x49, 0x48, 0x44, 0x52]).toString('latin1'),
    'plain text file': 'Đi chợ\nMua rau\nGọi mẹ\n',
    'empty file': '',
    'JSON null': 'null',
    'bare array of todos': JSON.stringify(good, null, 2),
    'missing todos': JSON.stringify({ version: 1 }, null, 2),
    'missing version': JSON.stringify({ todos: good }, null, 2),
    'todos not an array': JSON.stringify({ version: 1, todos: {} }, null, 2),
    'todo missing a field': JSON.stringify({ version: 1, todos: [{ id: 'm1', title: 'x', done: false }] }, null, 2),
    'done not true/false': JSON.stringify({ version: 1, todos: [{ id: 'm1', title: 'x', done: 'yes', createdAt: 1 }] }, null, 2),
    'id not a string': JSON.stringify({ version: 1, todos: [{ id: 7, title: 'x', done: false, createdAt: 1 }] }, null, 2),
    'title not a string': JSON.stringify({ version: 1, todos: [{ id: 'm1', title: 42, done: false, createdAt: 1 }] }, null, 2),
  };
  for (const [label, text] of Object.entries(bad)) {
    const p = backup.parseBackup(text);
    assert.equal(p.ok, false, `${label}: parseBackup refuses`);
    assert.equal(typeof p.message, 'string', `${label}: parseBackup gives a message`);
    assert.ok(p.message.trim().length > 0, `${label}: message not empty`);
    await assertRejected(storage, store, loaded.todos, text, label);
  }
});

test('AC10: duplicate id, empty title, or non-number createdAt → whole file refused, nothing imported, customer told', async () => {
  const current = makeTodos(3, 'cu');
  const storage = seeded(current);
  const { store, loaded } = openApp(storage);

  const dupId = makeTodos(30, 'moi');
  dupId[7] = { ...dupId[7], id: dupId[2].id };
  const emptyTitle = makeTodos(30, 'moi');
  emptyTitle[4] = { ...emptyTitle[4], title: '' };
  const textDate = makeTodos(30, 'moi');
  textDate[9] = { ...textDate[9], createdAt: 'hôm qua' };

  for (const [label, todos] of [['(a) duplicate id', dupId], ['(b) empty title', emptyTitle], ['(c) createdAt "hôm qua"', textDate]]) {
    const text = backupText(todos);
    const p = backup.parseBackup(text);
    assert.equal(p.ok, false, `${label}: parseBackup refuses the whole file`);
    assert.equal(p.todos, undefined, `${label}: no partial list returned`);
    const res = await assertRejected(storage, store, loaded.todos, text, label);
    const fileIds = new Set(todos.map((t) => t.id));
    assert.ok(res.todos.every((t) => !fileIds.has(t.id)), `${label}: no todo from the file imported`);
  }
});

test('AC11: a title "<img src=x onerror=alert(1)>" is imported as that exact text and nothing runs', async (t) => {
  const evil = '<img src=x onerror=alert(1)>';
  const alerts = [];
  const savedAlert = Object.getOwnPropertyDescriptor(globalThis, 'alert');
  globalThis.alert = (m) => alerts.push(m);
  t.after(() => { if (savedAlert) Object.defineProperty(globalThis, 'alert', savedAlert); else delete globalThis.alert; });

  const todos = [{ id: 'x1', title: evil, done: false, createdAt: 1760000000000 }];
  const text = backupText(todos);
  const p = backup.parseBackup(text);
  assert.equal(p.ok, true);
  assert.equal(p.todos[0].title, evil);

  const storage = new FakeStorage();
  const { store, loaded } = openApp(storage);
  const res = await backup.importBackup({ store, current: loaded.todos, file: fileOf(text), ask: asker(true) });
  assert.equal(res.todos[0].title, evil);
  assert.equal(openApp(storage).loaded.todos[0].title, evil);
  assert.deepEqual(alerts, [], 'file content is never run');
  // Rendering with textContent (no alert box in the page) needs a browser (see report).
});

test('AC14: storage full, 12 todos, import 30 and agree → customer told it was not saved; the old 12 stay on screen and after reload', async () => {
  const current = makeTodos(12, 'cu');
  const storage = seeded(current);
  const { store, loaded } = openApp(storage);
  storage.full = true;

  const ask = asker(true);
  const res = await backup.importBackup({ store, current: loaded.todos, file: fileOf(backupText(makeTodos(30, 'moi'))), ask });
  assert.equal(ask.questions.length, 1);
  // Spec F2 step 8: old list kept on screen and in memory.
  assert.deepEqual(res.todos, current);
  assert.equal(typeof res.message, 'string');
  // AMBIGUOUS: AC14 only says "thấy thông báo lỗi"; F2 step 8 says "app báo như F3", read as the same
  // not-saved notice including the F3 hint sentence.
  assert.ok(nfc(res.message).includes(nfc(NOT_SAVED_HINT)), `error notice should be the F3 one: ${res.message}`);

  storage.full = false;
  assert.deepEqual(openApp(storage).loaded.todos, current);
});
