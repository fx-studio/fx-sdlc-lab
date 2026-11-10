// E10 · incident of SDLC-6 R4 (planted for the demo, reached staging and production on simulated day 38): release 2e2ce98 refused
// every backup that holds two todos with the same title ("Mua sữa" twice), so people could not import the file the app wrote itself.
// Caught by the watch job (staging_error_rate level 3, rollback by runbook). Base 2e2ce98.
// Checks only the requirement, not a design: a backup the app wrote can be imported back, also with repeated titles; a file that
// repeats an id is still refused (the accepted rule, spec khach-khong-mat-viec A7). Any dedupe that keeps both holds passes.
const test = require('node:test');
const assert = require('node:assert/strict');
const backup = require('../app/backup.js');

const t = (id, title, done = false) => ({ id, title, done, createdAt: 1760000000000 + id.length });

test('E10: two todos with the same title survive a round trip through a backup file', async () => {
  const list = [t('a1', 'Mua sữa'), t('b2', 'Gọi mẹ'), t('c3', 'Mua sữa', true), t('d4', 'mua sữa ')];
  const parsed = backup.parseBackup(backup.toBackupText(list));
  assert.equal(parsed.ok, true, 'a backup with repeated titles parses');
  assert.deepEqual(parsed.todos, list);
  const text = backup.toBackupText(list);
  const store = { readError: false, replace: () => 'saved' };
  const out = await backup.importBackup({ store, current: [], file: { size: text.length, text: async () => text }, ask: async () => true });
  assert.deepEqual(out.todos, list, 'importBackup keeps every todo');
});

test('E10: a file that repeats an id is still refused', () => {
  const parsed = backup.parseBackup(JSON.stringify({ version: 1, todos: [t('a1', 'Mua sữa'), t('a1', 'Gọi mẹ')] }));
  assert.equal(parsed.ok, false);
});
