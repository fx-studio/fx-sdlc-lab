'use strict';
// F1 · Sao lưu ra file. AC1, AC2, AC4, AC12.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const backup = require('../app/backup.js');
const { FakeStorage, openApp, makeTodos, backupText, fileOf, asker, bigTodos, nfc } = require('./helpers.js');

test('AC1: backup of 3 todos (1 done) is indented plain text with only the allowed fields, named todo-sao-luu-<YYYY-MM-DD>.json, and reports 3', () => {
  const todos = [
    { id: 'a1', title: 'Đi chợ', done: true, createdAt: 1760000000000 },
    { id: 'a2', title: 'Gọi mẹ', done: false, createdAt: 1760000001000 },
    { id: 'a3', title: 'Trả tiền điện', done: false, createdAt: 1760000002000 },
  ];
  const text = backup.toBackupText(todos);
  assert.equal(typeof text, 'string');

  // Indented plain text: more than one line, and nested lines start with whitespace.
  assert.ok(text.includes('\n'), 'backup text should span several lines');
  assert.ok(/\n[ \t]+\S/.test(text), 'backup text should be indented');

  const data = JSON.parse(text);
  assert.deepEqual(Object.keys(data).sort(), ['todos', 'version']);
  assert.equal(data.version, 1);
  assert.equal(data.todos.length, 3);
  for (const t of data.todos) {
    assert.deepEqual(Object.keys(t).sort(), ['createdAt', 'done', 'id', 'title']);
  }
  assert.deepEqual(data.todos.map((t) => t.title), ['Đi chợ', 'Gọi mẹ', 'Trả tiền điện']);
  assert.deepEqual(data.todos.map((t) => t.done), [true, false, false]);
  assert.deepEqual(data.todos, todos);

  // File name uses the backup date, zero-padded. Noon local time so the calendar day is unambiguous.
  assert.equal(backup.backupFileName(new Date(2026, 9, 19, 12, 0, 0)), 'todo-sao-luu-2026-10-19.json');
  assert.equal(backup.backupFileName(new Date(2026, 0, 5, 12, 0, 0)), 'todo-sao-luu-2026-01-05.json');

  // "Màn hình báo đã sao lưu 3 việc".
  // AMBIGUOUS: api.md says templates use {n} (todos now) and {m} (todos in the file) but not which one
  // `backedUp` uses for the count saved; fill both so either reading shows 3.
  const said = backup.fill(backup.MESSAGES.backedUp, { n: 3, m: 3 });
  assert.equal(typeof said, 'string');
  assert.ok(said.includes('3'), `backup message should say how many were backed up: ${said}`);
  assert.ok(!/\{[nm]\}/.test(said), 'placeholders should be filled');
});

test('AC2: backing up and importing make no network request', async (t) => {
  // Only the Node-checkable part: backup.js must not call any network API. The real "Network panel,
  // network off" check needs a browser (see report).
  const calls = [];
  const saved = {};
  for (const name of ['fetch', 'XMLHttpRequest', 'WebSocket', 'EventSource']) {
    saved[name] = Object.getOwnPropertyDescriptor(globalThis, name);
    Object.defineProperty(globalThis, name, {
      configurable: true, writable: true,
      value: function () { calls.push(name); throw new Error(`network call via ${name}`); },
    });
  }
  t.after(() => {
    for (const [name, d] of Object.entries(saved)) {
      if (d) Object.defineProperty(globalThis, name, d); else delete globalThis[name];
    }
  });

  const todos = makeTodos(3, 'net');
  const text = backup.toBackupText(todos);
  backup.backupFileName(new Date(2026, 9, 19, 12));
  backup.tooBigToImport(text);
  backup.parseBackup(text);

  const { store } = openApp(new FakeStorage());
  await backup.importBackup({ store, current: [], file: fileOf(backupText(todos)), ask: asker(true) });

  assert.deepEqual(calls, []);
});

test('AC4: backing up an empty list tells the customer "Chưa có việc nào để sao lưu"', () => {
  // The "no file is downloaded" half happens in app.js (page script) and needs a browser (see report).
  // AMBIGUOUS: the spec quotes the sentence without a final full stop; accept it with or without one.
  const said = nfc(backup.MESSAGES.nothingToBackUp).trim().replace(/[.!]$/, '');
  assert.equal(said, nfc('Chưa có việc nào để sao lưu'));
});

test('AC12: a backup over 1 MB (5,000 todos x 200-char titles) is still produced, is flagged as too big to import, with the exact sentence', () => {
  const todos = bigTodos(5000);
  const text = backup.toBackupText(todos);
  assert.equal(typeof text, 'string');
  const bytes = Buffer.byteLength(text, 'utf8');
  assert.ok(bytes > 1024 * 1024, `backup should be over 1 MB, was ${bytes} bytes`);
  assert.ok(bytes > backup.MAX_IMPORT_BYTES, 'backup should be over the import limit');
  assert.equal(JSON.parse(text).todos.length, 5000, 'the big backup still holds every todo');

  assert.equal(backup.tooBigToImport(text), true);
  assert.equal(backup.tooBigToImport(backup.toBackupText(makeTodos(3))), false, 'a small backup is importable');

  assert.equal(nfc(backup.MESSAGES.backupTooBig), nfc('File sao lưu đã lưu, nhưng quá lớn nên app không nhập lại được.'));
});
