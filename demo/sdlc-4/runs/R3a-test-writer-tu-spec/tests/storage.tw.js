'use strict';
// F3 · Báo khi không lưu được, F5 · Danh sách đã lưu không đọc được. AC13, AC15–AC22.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const backup = require('../app/backup.js');
const {
  KEY, NOT_SAVED_HINT, UNREADABLE_TEXT, FakeStorage, seeded, openApp, makeTodos, backupText, fileOf, asker, bigTodos,
  nfc, plainQuotes,
} = require('./helpers.js');

const BROKEN = '{hỏng';
const newTodo = (id, title = `việc ${id}`) => ({ id, title, done: false, createdAt: 1770000000000 });

function openUnreadable(raw = BROKEN) {
  const storage = new FakeStorage({ [KEY]: raw });
  const app = openApp(storage);
  return { storage, ...app };
}

function assertReadErrorState({ loaded, store }, label) {
  assert.equal(loaded.readError, true, `${label}: load() reports a read error`);
  assert.deepEqual(loaded.todos, [], `${label}: nothing readable to show`);
  assert.equal(store.readError, true, `${label}: store.readError is set`);
}

test('AC13: storage full, add a todo → customer told the change was not saved, with "Hãy sao lưu ra file, rồi xoá bớt việc đã xong"; after reload the todo is gone', () => {
  const saved = makeTodos(2, 'cu');
  const storage = seeded(saved);
  const { store, loaded } = openApp(storage);
  storage.full = true;

  const screen = [...loaded.todos, newTodo('moi-1')];
  const res = backup.persist(store, screen);
  assert.equal(typeof res.message, 'string', 'customer is told');
  // Only the hint sentence is fixed by the spec; "chưa được lưu" wording is not, so it is not asserted.
  assert.ok(nfc(res.message).includes(nfc(NOT_SAVED_HINT)), `notice should carry the hint: ${res.message}`);

  // Data and integrations: store.save tells the caller the write failed.
  assert.equal(store.save(screen), 'failed');

  storage.full = false;
  assert.deepEqual(openApp(storage).loaded.todos, saved, 'unsaved todo is gone after reload');
});

test('AC15: "{hỏng" in todo.v1 → exact unreadable banner, no empty line; add/toggle/remove are never written, no new keys; still unreadable after reload', () => {
  const app = openUnreadable();
  const { storage, store, STORE_KEY } = app;
  assert.equal(STORE_KEY, KEY);
  assertReadErrorState(app, 'open');
  assert.equal(storage.raw(), BROKEN, 'opening does not overwrite');

  // AMBIGUOUS: the spec quotes the banner with straight inner quotes around "Nhập từ file";
  // typographic quotes are treated as the same sentence.
  assert.equal(plainQuotes(backup.MESSAGES.unreadable), plainQuotes(UNREADABLE_TEXT));
  // "không thấy dòng trạng thái trống" and "không có hộp thoại" are page checks (see report).

  const a = newTodo('m1', 'Mua sữa');
  const b = newTodo('m2', 'Đón con');
  let screen = [a];
  backup.persist(store, screen);
  screen = [a, b];
  backup.persist(store, screen);
  screen = [{ ...a, done: true }, b];
  backup.persist(store, screen);
  screen = [{ ...a, done: true }];
  backup.persist(store, screen);

  assert.notEqual(store.save(screen), 'saved', 'save is not done while unreadable');
  assert.equal(storage.raw(), BROKEN, 'todo.v1 untouched');
  assert.deepEqual(storage.writesTo(KEY), [], 'nothing written to todo.v1');
  assert.deepEqual([...storage.map.keys()], [KEY], 'no new key of the app');
  assert.equal(store.readError, true, 'still unreadable');

  const reloaded = openApp(storage);
  assertReadErrorState(reloaded, 'reload');
  assert.equal(storage.raw(), BROKEN);
});

test('AC16: todo.v1 = {"a": 1} (readable, not an array) → read error; adding a todo leaves the value as is', () => {
  const raw = '{"a": 1}';
  const app = openUnreadable(raw);
  assertReadErrorState(app, 'open');
  backup.persist(app.store, [newTodo('m1')]);
  assert.equal(app.storage.raw(), raw);
  assert.deepEqual(app.storage.writesTo(KEY), []);
});

test('AC17: reading browser storage throws on open → read error; adding a todo writes nothing to browser storage', () => {
  const storage = seeded(makeTodos(2, 'cu'));
  const rawBefore = storage.raw();
  storage.readThrows = true;
  const app = openApp(storage);
  assertReadErrorState(app, 'open');
  // AMBIGUOUS: AC17 says reading throws "khi app mở"; storage is made readable again afterwards so the
  // test checks that the page-level read-error state, not a still-failing read, is what stops writes.
  storage.readThrows = false;
  storage.writes = [];

  backup.persist(app.store, [newTodo('m1')]);
  assert.deepEqual(storage.writes, [], 'nothing written to browser storage');
  assert.equal(storage.raw(), rawBefore);
  assert.equal(app.store.readError, true);
});

test('AC18: unreadable, add two todos, back up → the file holds exactly those two; todo.v1 still "{hỏng"', () => {
  const { storage, store } = openUnreadable();
  const a = newTodo('m1', 'Mua sữa');
  const b = newTodo('m2', 'Đón con');
  backup.persist(store, [a]);
  backup.persist(store, [a, b]);

  const data = JSON.parse(backup.toBackupText([a, b]));
  assert.deepEqual(data.todos, [a, b]);
  assert.equal(storage.raw(), BROKEN);
});

test('AC19: unreadable, nothing added, import 30 → asks "Thay danh sách đã lưu không đọc được bằng 30 việc trong file?"; cancel keeps "{hỏng"; agree replaces it, clears the read error, and later adds are saved', async () => {
  const expected = 'Thay danh sách đã lưu không đọc được bằng 30 việc trong file?';
  const q = backup.confirmText({ readError: true, current: 0, incoming: 30 });
  assert.equal(typeof q, 'string', 'always asks while unreadable, even with nothing on screen');
  assert.ok(nfc(q).includes(nfc(expected)), `confirm text: ${q}`);

  const incoming = makeTodos(30, 'moi');
  const file = fileOf(backupText(incoming));
  const { storage, store, loaded } = openUnreadable();

  const no = asker(false);
  let res = await backup.importBackup({ store, current: loaded.todos, file, ask: no });
  assert.equal(no.questions.length, 1);
  assert.ok(nfc(no.questions[0]).includes(nfc(expected)), `question asked: ${no.questions[0]}`);
  assert.deepEqual(res.todos, []);
  assert.equal(storage.raw(), BROKEN, 'cancel writes nothing');
  assert.equal(store.readError, true, 'banner stays');

  let rawAtAsk;
  const yes = asker(true, () => { rawAtAsk = storage.raw(); });
  res = await backup.importBackup({ store, current: loaded.todos, file, ask: yes });
  assert.equal(rawAtAsk, BROKEN, 'nothing written before the customer answers');
  assert.deepEqual(res.todos, incoming);
  assert.equal(store.readError, false, 'banner goes away');
  assert.deepEqual(JSON.parse(storage.raw()), incoming, 'todo.v1 now holds the file list, as an array');

  const extra = newTodo('m31', 'Việc thứ 31');
  const after = backup.persist(store, [...res.todos, extra]);
  assert.equal(after.message, null, 'a normal save says nothing');

  const reloaded = openApp(storage);
  assert.equal(reloaded.loaded.readError, false, 'no banner after reload');
  assert.deepEqual(reloaded.loaded.todos, [...incoming, extra]);
});

test('AC20: unreadable, 3 todos added, import 30 → asks exactly "Thay danh sách đã lưu không đọc được và 3 việc bạn vừa thêm (chưa lưu) bằng 30 việc trong file?"; cancel keeps the 3; agree gives exactly the 30', async () => {
  const expected = 'Thay danh sách đã lưu không đọc được và 3 việc bạn vừa thêm (chưa lưu) bằng 30 việc trong file?';
  const q = backup.confirmText({ readError: true, current: 3, incoming: 30 });
  assert.equal(typeof q, 'string');
  assert.ok(nfc(q).includes(nfc(expected)), `confirm text: ${q}`);

  const { storage, store } = openUnreadable();
  const added = [newTodo('m1'), newTodo('m2'), newTodo('m3')];
  backup.persist(store, added.slice(0, 1));
  backup.persist(store, added.slice(0, 2));
  backup.persist(store, added);
  assert.equal(storage.raw(), BROKEN);

  const incoming = makeTodos(30, 'moi');
  const file = fileOf(backupText(incoming));

  const no = asker(false);
  let res = await backup.importBackup({ store, current: added, file, ask: no });
  assert.equal(no.questions.length, 1);
  assert.ok(nfc(no.questions[0]).includes(nfc(expected)), `question asked: ${no.questions[0]}`);
  assert.deepEqual(res.todos, added, 'the three stay on screen');
  assert.equal(store.readError, true, 'banner stays');
  assert.equal(storage.raw(), BROKEN);

  const yes = asker(true);
  res = await backup.importBackup({ store, current: added, file, ask: yes });
  assert.deepEqual(res.todos, incoming);
  const addedIds = new Set(added.map((t) => t.id));
  assert.ok(res.todos.every((t) => !addedIds.has(t.id)), 'none of the three left');
  assert.equal(store.readError, false, 'banner goes away');

  const reloaded = openApp(storage);
  assert.equal(reloaded.loaded.readError, false);
  assert.deepEqual(reloaded.loaded.todos, incoming);
});

test('AC21: "{hỏng" and storage full; import 30 and agree → still unreadable, todo.v1 still "{hỏng"; adding a todo leaves it as is', async () => {
  const storage = new FakeStorage({ [KEY]: BROKEN });
  storage.full = true;
  const app = openApp(storage);
  assertReadErrorState(app, 'open');
  const { store, loaded } = app;

  const res = await backup.importBackup({
    store, current: loaded.todos, file: fileOf(backupText(makeTodos(30, 'moi'))), ask: asker(true),
  });
  assert.equal(store.readError, true, 'banner still shown');
  assert.equal(storage.raw(), BROKEN);
  // A20 (answered "Có"): like F2 step 8 the screen keeps what it had before the import, and the F3
  // not-saved notice is shown alongside the banner.
  assert.deepEqual(res.todos, loaded.todos, 'screen keeps the list from before the import');
  assert.equal(typeof res.message, 'string');
  assert.ok(nfc(res.message).includes(nfc(NOT_SAVED_HINT)), `F3 notice expected: ${res.message}`);

  storage.writes = [];
  backup.persist(store, [newTodo('m1')]);
  assert.equal(storage.raw(), BROKEN);
  assert.deepEqual(storage.writesTo(KEY), [], 'no write attempted to todo.v1 while unreadable');
});

test('AC22: unreadable, import the AC7 (over 1 MB) and AC8 (unknown field) files → both refused without a confirm question; "{hỏng" kept, banner stays', async () => {
  const { storage, store, loaded } = openUnreadable();

  const tooBig = backupText(bigTodos(5000));
  assert.ok(Buffer.byteLength(tooBig) > backup.MAX_IMPORT_BYTES);
  const withExtra = makeTodos(30, 'moi');
  withExtra[5] = { ...withExtra[5], x: 1 };

  for (const [label, text] of [['AC7 file', tooBig], ['AC8 file', backupText(withExtra)]]) {
    const ask = asker(true);
    const res = await backup.importBackup({ store, current: loaded.todos, file: fileOf(text), ask });
    assert.deepEqual(ask.questions, [], `${label}: no confirm question`);
    assert.deepEqual(res.todos, loaded.todos, `${label}: screen unchanged`);
    assert.equal(typeof res.message, 'string', `${label}: customer told`);
    assert.ok(res.message.trim().length > 0);
    assert.equal(storage.raw(), BROKEN, `${label}: todo.v1 kept`);
    assert.equal(store.readError, true, `${label}: banner stays`);
  }
  assert.deepEqual(storage.writesTo(KEY), []);
});
