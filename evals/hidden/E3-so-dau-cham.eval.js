// E3 · spec revision R9 (SDLC-3, commit 65fae52 → code 028b8c0): counts from 1,000 up get a dot every three digits, everywhere.
const test = require('node:test');
const assert = require('node:assert/strict');
const { backup, loadApp, todos } = require('./_harness.js');

test('E3: counts in sentences use 1.000 / 2.001 / 12.500, plain below 1,000', () => {
  assert.equal(backup.fill(backup.MESSAGES.imported, { n: 2001 }), 'Đã nhập 2.001 việc.');
  assert.equal(backup.fill(backup.MESSAGES.imported, { n: 999 }), 'Đã nhập 999 việc.');
  assert.equal(backup.fill(backup.MESSAGES.confirmReplace, { n: 12500, m: 1000 }), 'Thay 12.500 việc hiện có bằng 1.000 việc trong file?');
});

test('E3: the open-todo count line too', () => {
  assert.equal(loadApp(todos(2001)).count(), '2.001 việc chưa xong');
  assert.equal(loadApp(todos(12)).count(), '12 việc chưa xong');
});

test('E3: the backup file name keeps the year without a dot', () => {
  assert.equal(backup.backupFileName(new Date(2026, 9, 27)), 'todo-sao-luu-2026-10-27.json');
});
