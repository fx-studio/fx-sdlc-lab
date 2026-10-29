// E2 · spec F2 step 4: when a file is rejected, say (in plain words) why, that the list is unchanged, and what to do next.
// Found by R3f (SDLC-3): all five rejection sentences missed "what next". Accepted outcome: commit 8acafc1.
const test = require('node:test');
const assert = require('node:assert/strict');
const { backup } = require('./_harness.js');

const REJECT = ['emptyFile', 'notBackup', 'badTodo', 'fileTooBig', 'cannotReadFile'];

test('E2: every rejection sentence says the list is unchanged and what to do next', () => {
  for (const k of REJECT) {
    const m = backup.MESSAGES[k];
    assert.ok(typeof m === 'string' && m.length > 0, `${k} exists`);
    assert.match(m, /giữ nguyên/, `${k}: says the list is unchanged`);
    assert.match(m, /Hãy /, `${k}: says what to do next`);
  }
});
