// Tests for app/backup.js (plan/2026-10-19-khach-khong-mat-viec.md, commit A). Run: node --test
const test = require('node:test');
const assert = require('node:assert/strict');
const { randomUUID } = require('node:crypto');
const {
  MAX_IMPORT_BYTES, MESSAGES, formatCount, fill, toBackupText, backupFileName, tooBigToImport, parseBackup, confirmText, persist,
  importBackup,
} = require('../app/backup.js');

const todo = (title, extra = {}) => ({ id: randomUUID(), title, done: false, createdAt: Date.now(), ...extra });
const list = (n) => Array.from({ length: n }, (_, i) => todo(`Việc ${i + 1}`));
const fileOf = (todos) => JSON.stringify({ version: 1, todos });

function fakeStore({ readError = false, saveResult = 'saved', replaceResult = 'saved' } = {}) {
  const calls = { save: [], replace: [] };
  return {
    readError,
    calls,
    save(t) { calls.save.push(t); return saveResult; },
    replace(t) { calls.replace.push(t); return replaceResult; },
  };
}

function fakeFile(text, size = Buffer.byteLength(text)) {
  const file = { size, reads: 0, async text() { file.reads++; return text; } };
  return file;
}

function fakeAsk(answer) {
  const ask = async (q) => { ask.questions.push(q); return answer; };
  ask.questions = [];
  return ask;
}

// --- Backup file (AC1, P2, P3) ---

test('toBackupText: indented, version 1, only the four todo fields', () => {
  const todos = [todo('Mua sữa'), todo('Gọi mẹ', { done: true }), todo('Nộp thuế')];
  todos[0].x = 1; // a stray field in memory must not reach the file
  const text = toBackupText(todos);
  assert.match(text, /\n  "version": 1/);
  const data = JSON.parse(text);
  assert.deepEqual(Object.keys(data), ['version', 'todos']);
  assert.deepEqual(data.todos.map((t) => t.title), ['Mua sữa', 'Gọi mẹ', 'Nộp thuế']);
  assert.deepEqual(data.todos.map((t) => t.done), [false, true, false]);
  for (const t of data.todos) assert.deepEqual(Object.keys(t), ['id', 'title', 'done', 'createdAt']);
});

test('backupFileName uses the local date, including just after midnight (A11)', () => {
  assert.equal(backupFileName(new Date(2026, 9, 27, 0, 30)), 'todo-sao-luu-2026-10-27.json');
  assert.equal(backupFileName(new Date(2026, 0, 5, 23, 59)), 'todo-sao-luu-2026-01-05.json');
});

test('tooBigToImport counts bytes, with the boundary at 1,048,576 (Q3)', () => {
  assert.equal(MAX_IMPORT_BYTES, 1048576);
  assert.equal(tooBigToImport('a'.repeat(1048576)), false);
  assert.equal(tooBigToImport('a'.repeat(1048577)), true);
  assert.equal(tooBigToImport('ệ'.repeat(349526)), true); // 349,526 characters but 1,048,578 bytes
});

test('a backup of 5,000 todos with 200-character titles is too big to import (AC12)', () => {
  const todos = Array.from({ length: 5000 }, () => todo('x'.repeat(200)));
  assert.equal(tooBigToImport(toBackupText(todos)), true);
});

// --- Checking an imported file (AC8–AC11, Q4, S1) ---

test('parseBackup accepts a valid file and keeps the todos as they are', () => {
  const todos = [todo('Mua sữa'), todo('Gọi mẹ', { done: true })];
  assert.deepEqual(parseBackup(fileOf(todos)), { ok: true, todos });
});

test('parseBackup rejects files that are not a backup (AC9)', () => {
  const png = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0, 0, 0, 0x0d]).toString('utf8');
  const cases = [png, 'Danh sách đi chợ: rau, thịt', '', 'null', '[]', '42', JSON.stringify([todo('a')]),
    JSON.stringify({ version: 2, todos: [todo('a')] }), JSON.stringify({ version: 1 }),
    JSON.stringify({ version: 1, todos: {} }), JSON.stringify({ version: 1, todos: [todo('a')], x: 1 }),
    '{"version": 1, "todos": [{"id": "a", "title": "b", "done": false, "createdAt": NaN}]}'];
  for (const text of cases) assert.deepEqual(parseBackup(text), { ok: false, message: MESSAGES.notBackup }, text);
});

test('parseBackup rejects a file with no todos (Q4)', () => {
  assert.deepEqual(parseBackup(fileOf([])), { ok: false, message: MESSAGES.emptyFile });
});

test('parseBackup rejects the whole file when one todo is bad (AC8, AC10)', () => {
  const t = todo('Việc tốt');
  const bad = {
    'unknown field': { ...todo('a'), x: 1 },
    'missing field': { id: 'z', title: 'a', done: false },
    'proto key': JSON.parse('{"id": "p", "title": "a", "done": false, "createdAt": 1, "__proto__": {}}'),
    'empty id': todo('a', { id: '' }),
    'id not a string': todo('a', { id: 7 }),
    'empty title': todo(''),
    'blank title': todo('   '),
    'title not a string': todo(5),
    'done not boolean': todo('a', { done: 'true' }),
    'createdAt is a word': todo('a', { createdAt: 'hôm qua' }),
    'createdAt is infinite': null, // written as 1e999 below, which JSON.parse reads as Infinity
    'not an object': 'việc',
  };
  for (const [name, b] of Object.entries(bad)) {
    const text = b === null
      ? `{"version": 1, "todos": [{"id": "i", "title": "a", "done": false, "createdAt": 1e999}]}`
      : fileOf([t, b]);
    assert.deepEqual(parseBackup(text), { ok: false, message: MESSAGES.badTodo }, name);
  }
  assert.deepEqual(parseBackup(fileOf([t, { ...todo('Khác'), id: t.id }])), { ok: false, message: MESSAGES.badTodo });
});

test('parseBackup keeps an HTML-looking title as plain text (AC11)', () => {
  const t = todo('<img src=x onerror=alert(1)>');
  assert.equal(parseBackup(fileOf([t])).todos[0].title, '<img src=x onerror=alert(1)>');
});

test('every list the app can create survives backup then import unchanged', () => {
  const todos = [
    todo('Mua sữa'), todo('Đã xong', { done: true }), todo('Đi chợ 🛒 rồi về 🏠'), todo('Học tiếng Việt: ă â ê ô ơ ư đ'),
    todo('<b>đậm</b> & "ngoặc" \'đơn\''), todo('a'), todo('x'.repeat(500)), todo('tab\tvà\nxuống dòng'),
  ];
  assert.deepEqual(parseBackup(toBackupText(todos)), { ok: true, todos });
  assert.deepEqual(parseBackup(toBackupText(list(2000))).ok, true);
});

// --- Confirmation (AC5, AC6, AC19, AC20, S2) ---

test('confirmText asks before replacing anything, and only then', () => {
  assert.equal(confirmText({ readError: false, current: 12, incoming: 30 }), 'Thay 12 việc hiện có bằng 30 việc trong file?');
  assert.equal(confirmText({ readError: false, current: 1, incoming: 30 }), 'Thay 1 việc hiện có bằng 30 việc trong file?');
  assert.equal(confirmText({ readError: false, current: 0, incoming: 30 }), null);
  assert.equal(confirmText({ readError: true, current: 0, incoming: 30 }),
    'Thay danh sách đã lưu không đọc được bằng 30 việc trong file?');
  assert.equal(confirmText({ readError: true, current: 3, incoming: 30 }),
    'Thay danh sách đã lưu không đọc được và 3 việc bạn vừa thêm (chưa lưu) bằng 30 việc trong file?');
});

// --- Saving after add, toggle, remove (AC13, AC15, F3) ---

test('persist shows the not-saved message only when the write failed', () => {
  assert.deepEqual(persist(fakeStore({ saveResult: 'saved' }), []), { message: null });
  assert.deepEqual(persist(fakeStore({ saveResult: 'failed' }), []), { message: MESSAGES.notSaved });
  assert.deepEqual(persist(fakeStore({ saveResult: 'skipped' }), []), { message: null });
});

// --- Import flow ---

test('importBackup rejects a file over the limit without reading it (AC7, AC22)', async () => {
  const store = fakeStore();
  const current = list(2);
  const big = fakeFile(fileOf(list(1)), 1048577);
  assert.deepEqual(await importBackup({ store, current, file: big, ask: fakeAsk(true) }),
    { todos: current, message: MESSAGES.fileTooBig });
  assert.equal(big.reads, 0);
  assert.equal(store.calls.replace.length, 0);

  const atLimit = fakeFile(fileOf(list(1)), 1048576);
  await importBackup({ store, current: [], file: atLimit, ask: fakeAsk(true) });
  assert.equal(atLimit.reads, 1);
});

test('importBackup keeps the list when the file cannot be read', async () => {
  const store = fakeStore();
  const current = list(2);
  const file = { size: 10, async text() { throw new Error('NotReadableError'); } };
  assert.deepEqual(await importBackup({ store, current, file, ask: fakeAsk(true) }),
    { todos: current, message: MESSAGES.cannotReadFile });
  assert.equal(store.calls.replace.length, 0);
});

test('importBackup rejects a bad file without asking or writing (AC8–AC10, AC22)', async () => {
  for (const readError of [false, true]) {
    const store = fakeStore({ readError });
    const ask = fakeAsk(true);
    const current = list(2);
    const result = await importBackup({ store, current, file: fakeFile(fileOf([{ ...todo('a'), x: 1 }])), ask });
    assert.deepEqual(result, { todos: current, message: MESSAGES.badTodo });
    assert.equal(ask.questions.length, 0);
    assert.equal(store.calls.replace.length, 0);
  }
});

test('importBackup into an empty list does not ask (AC3)', async () => {
  const store = fakeStore();
  const ask = fakeAsk(false);
  const incoming = list(3);
  const result = await importBackup({ store, current: [], file: fakeFile(fileOf(incoming)), ask });
  assert.deepEqual(result, { todos: incoming, message: 'Đã nhập 3 việc.' });
  assert.equal(ask.questions.length, 0);
  assert.deepEqual(store.calls.replace, [incoming]);
});

test('importBackup over 12 todos asks first; cancel writes nothing, agree replaces (AC5, AC6)', async () => {
  const current = list(12);
  const incoming = list(30);

  const store1 = fakeStore();
  const no = fakeAsk(false);
  assert.deepEqual(await importBackup({ store: store1, current, file: fakeFile(fileOf(incoming)), ask: no }),
    { todos: current, message: null });
  assert.deepEqual(no.questions, ['Thay 12 việc hiện có bằng 30 việc trong file?']);
  assert.equal(store1.calls.replace.length, 0);

  const store2 = fakeStore();
  const yes = fakeAsk(true);
  assert.deepEqual(await importBackup({ store: store2, current, file: fakeFile(fileOf(incoming)), ask: yes }),
    { todos: incoming, message: 'Đã nhập 30 việc.' });
  assert.equal(store2.calls.replace.length, 1);
});

test('importBackup keeps the old list when the write fails, with its own message (AC14, AC21, A20, F2 step 8)', async () => {
  for (const readError of [false, true]) {
    const store = fakeStore({ readError, replaceResult: 'failed' });
    const current = list(readError ? 0 : 12);
    const result = await importBackup({ store, current, file: fakeFile(fileOf(list(30))), ask: fakeAsk(true) });
    assert.deepEqual(result, { todos: current, message: MESSAGES.importNotSaved });
  }
});

test('importBackup while the saved list is unreadable writes only through replace, never save (AC19–AC21)', async () => {
  const store = fakeStore({ readError: true });
  const ask = fakeAsk(true);
  const incoming = list(30);
  const result = await importBackup({ store, current: list(3), file: fakeFile(fileOf(incoming)), ask });
  assert.deepEqual(ask.questions,
    ['Thay danh sách đã lưu không đọc được và 3 việc bạn vừa thêm (chưa lưu) bằng 30 việc trong file?']);
  assert.deepEqual(result.todos, incoming);
  assert.equal(store.calls.save.length, 0);
  assert.equal(store.calls.replace.length, 1);
});

// --- Wording (AC4, AC12, AC15, AC24, U4) ---

test('messages quoted in the spec and plan are word for word', () => {
  assert.equal(MESSAGES.nothingToBackUp, 'Chưa có việc nào để sao lưu.');
  assert.equal(MESSAGES.backupTooBig, 'File sao lưu đã lưu, nhưng quá lớn nên app không nhập lại được.');
  assert.match(MESSAGES.notSaved, /Hãy sao lưu ra file, rồi xoá bớt việc đã xong/);
  assert.equal(MESSAGES.emptyFile,
    'File này không có việc nào, nên chưa nhập được. Danh sách của bạn vẫn giữ nguyên. Hãy chọn file sao lưu khác.');
  assert.equal(MESSAGES.notBackup,
    'File này không phải file sao lưu của app, nên chưa nhập được. Danh sách của bạn vẫn giữ nguyên. ' +
    'Hãy chọn file tạo từ nút "Sao lưu ra file".');
  assert.equal(MESSAGES.badTodo,
    'File sao lưu này bị lỗi, nên chưa nhập được việc nào. Danh sách của bạn vẫn giữ nguyên. Hãy chọn file sao lưu khác.');
  assert.equal(MESSAGES.fileTooBig,
    'File này quá lớn, nên chưa nhập được. Danh sách của bạn vẫn giữ nguyên. Hãy chọn file sao lưu của danh sách ngắn hơn.');
  assert.equal(MESSAGES.cannotReadFile,
    'Không đọc được file này. Danh sách của bạn vẫn giữ nguyên. Hãy chọn lại file hoặc chọn file khác.');
  assert.equal(MESSAGES.unreadable,
    'Không đọc được danh sách đã lưu trên trình duyệt này. Việc bạn thêm hoặc sửa lúc này sẽ không được lưu. ' +
    'Nếu có file sao lưu, hãy bấm "Nhập từ file".');
  assert.equal(fill(MESSAGES.backedUp, { n: 3 }), 'Đã sao lưu 3 việc.');
  assert.equal(MESSAGES.importNotSaved,
    'Chưa nhập được file. Danh sách trên màn hình vẫn nguyên nhưng có thể chưa được lưu, nên đừng tải lại trang. ' +
    'Hãy sao lưu ra file, xoá bớt việc đã xong rồi thử lại.');
  assert.notEqual(MESSAGES.importNotSaved, MESSAGES.notSaved);
});

test('counts in sentences: a dot every three digits from 1,000 up, plain below (Linh, R9)', () => {
  const cases = { 0: '0', 1: '1', 12: '12', 999: '999', 1000: '1.000', 2001: '2.001', 12500: '12.500', 1234567: '1.234.567' };
  for (const [n, text] of Object.entries(cases)) assert.equal(formatCount(Number(n)), text, n);
  assert.equal(fill(MESSAGES.confirmReplace, { n: 999, m: 1000 }), 'Thay 999 việc hiện có bằng 1.000 việc trong file?');
  assert.equal(fill(MESSAGES.confirmReplace, { n: 2001, m: 12500 }), 'Thay 2.001 việc hiện có bằng 12.500 việc trong file?');
  assert.equal(confirmText({ readError: true, current: 2001, incoming: 12500 }),
    'Thay danh sách đã lưu không đọc được và 2.001 việc bạn vừa thêm (chưa lưu) bằng 12.500 việc trong file?');
  assert.equal(fill(MESSAGES.backedUp, { n: 2001 }), 'Đã sao lưu 2.001 việc.');
  assert.equal(fill(MESSAGES.imported, { n: 1000 }), 'Đã nhập 1.000 việc.');
});

test('the backup file name keeps the year without a dot', () => {
  assert.equal(backupFileName(new Date(2026, 9, 27)), 'todo-sao-luu-2026-10-27.json');
});

test('no message uses a technical word', () => {
  for (const [key, text] of Object.entries(MESSAGES)) {
    assert.doesNotMatch(text, /localStorage|JSON|console/i, key);
  }
});
