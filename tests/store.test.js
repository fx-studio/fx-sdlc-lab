// Tests for app/store.js (plan/2026-10-19-khach-khong-mat-viec.md, commit B). Run: node --test
// Browser storage is replaced by a fake that counts writes and can be told to throw.
const test = require('node:test');
const assert = require('node:assert/strict');
const { randomUUID } = require('node:crypto');
const { store, STORE_KEY } = require('../app/store.js');

function fakeStorage(initial = {}) {
  const data = new Map(Object.entries(initial));
  const s = {
    data,
    sets: 0,
    getThrows: false,
    setThrows: false,
    getItem(k) {
      if (s.getThrows) throw new Error('SecurityError');
      return data.has(k) ? data.get(k) : null;
    },
    setItem(k, v) {
      s.sets++;
      if (s.setThrows) {
        const err = new Error('quota');
        err.name = 'QuotaExceededError';
        throw err;
      }
      data.set(k, String(v));
    },
  };
  globalThis.localStorage = s;
  return s;
}

// What the current version of the app writes: an array of { id, title, done, createdAt }.
const oldVersionList = (n) =>
  Array.from({ length: n }, (_, i) => ({ id: randomUUID(), title: `Việc ${i}`, done: i % 3 === 0, createdAt: Date.now() - i }));

// --- Loading: no false alarm on good data (condition 3) ---

test('no saved key is an ordinary empty list (AC3, A13)', () => {
  fakeStorage();
  assert.deepEqual(store.load(), { todos: [], readError: false });
  assert.equal(store.readError, false);
});

test('a list saved by the current version loads, 3 and 2,000 todos, and saving still writes', () => {
  for (const n of [3, 2000]) {
    const todos = oldVersionList(n);
    const s = fakeStorage({ [STORE_KEY]: JSON.stringify(todos) });
    assert.deepEqual(store.load(), { todos, readError: false }, `${n} todos`);
    assert.equal(store.save(todos), 'saved');
    assert.equal(s.sets, 1);
  }
});

test('a saved empty array is not a read error', () => {
  fakeStorage({ [STORE_KEY]: '[]' });
  assert.deepEqual(store.load(), { todos: [], readError: false });
});

// --- Loading: the three read-error cases (AC15–AC17, Q5) ---

test('unparsable data, data that is not an array, and storage that throws are read errors', () => {
  for (const raw of ['{hỏng', '{"a": 1}', 'null', '"chữ"', '42']) {
    fakeStorage({ [STORE_KEY]: raw });
    assert.deepEqual(store.load(), { todos: [], readError: true }, raw);
  }
  const s = fakeStorage({ [STORE_KEY]: '[]' });
  s.getThrows = true;
  assert.deepEqual(store.load(), { todos: [], readError: true });
});

test('after a read error, saving never writes and the unreadable value stays (AC15–AC17)', () => {
  for (const raw of ['{hỏng', '{"a": 1}']) {
    const s = fakeStorage({ [STORE_KEY]: raw });
    store.load();
    const todos = oldVersionList(2);
    assert.equal(store.save(todos), 'skipped');
    todos[0].done = true;
    assert.equal(store.save(todos), 'skipped');
    assert.equal(store.save(todos.slice(1)), 'skipped');
    assert.equal(s.sets, 0);
    assert.deepEqual([...s.data.keys()], [STORE_KEY]);
    assert.equal(s.data.get(STORE_KEY), raw);
  }
  const s = fakeStorage();
  s.getThrows = true;
  store.load();
  assert.equal(store.save(oldVersionList(1)), 'skipped');
  assert.equal(s.sets, 0);
});

// --- Saving fails (AC13, AC14, AC21) ---

test('a failed write is reported and leaves the old value (AC13)', () => {
  const old = JSON.stringify(oldVersionList(12));
  const s = fakeStorage({ [STORE_KEY]: old });
  store.load();
  s.setThrows = true;
  assert.equal(store.save(oldVersionList(13)), 'failed');
  assert.equal(s.data.get(STORE_KEY), old);
});

test('a failed replace keeps the old list; after a read error it keeps the error too (AC14, AC21)', () => {
  const old = JSON.stringify(oldVersionList(12));
  const s1 = fakeStorage({ [STORE_KEY]: old });
  store.load();
  s1.setThrows = true;
  assert.equal(store.replace(oldVersionList(30)), 'failed');
  assert.equal(s1.data.get(STORE_KEY), old);

  const s2 = fakeStorage({ [STORE_KEY]: '{hỏng' });
  store.load();
  s2.setThrows = true;
  assert.equal(store.replace(oldVersionList(30)), 'failed');
  assert.equal(store.readError, true);
  assert.equal(s2.data.get(STORE_KEY), '{hỏng');
  s2.setThrows = false;
  assert.equal(store.save(oldVersionList(1)), 'skipped');
  assert.equal(s2.data.get(STORE_KEY), '{hỏng');
});

// --- Leaving the read-error state (AC19, AC20, A17) ---

test('a successful replace ends the read error, and later saves are written', () => {
  const s = fakeStorage({ [STORE_KEY]: '{hỏng' });
  store.load();
  const thirty = oldVersionList(30);
  assert.equal(store.replace(thirty), 'saved');
  assert.equal(store.readError, false);
  const thirtyOne = [...thirty, ...oldVersionList(1)];
  assert.equal(store.save(thirtyOne), 'saved');
  assert.deepEqual(store.load(), { todos: thirtyOne, readError: false });
  assert.equal(s.sets, 2);
});

// --- Today's flow ---

test('save then load gives the same list', () => {
  fakeStorage();
  store.load();
  const todos = oldVersionList(5);
  assert.equal(store.save(todos), 'saved');
  assert.deepEqual(store.load().todos, todos);
});
