'use strict';
// Shared fakes for the acceptance tests of spec/2026-10-19-khach-khong-mat-viec.md.
// Written from the spec and api.md only; nothing under app/ was read.

const fs = require('node:fs');
const path = require('node:path');

// Spec, Data and integrations: the storage key stays `todo.v1`, value is an array of todos.
const KEY = 'todo.v1';
// Spec F3 step 2 / AC13: the hint the customer sees when a change could not be saved.
const NOT_SAVED_HINT = 'Hãy sao lưu ra file, rồi xoá bớt việc đã xong';
// Spec F5 step 4 / AC15: the exact unreadable banner.
const UNREADABLE_TEXT =
  'Không đọc được danh sách đã lưu trên trình duyệt này. Việc bạn thêm hoặc sửa lúc này sẽ không được lưu. ' +
  'Nếu có file sao lưu, hãy bấm "Nhập từ file".';

// Fake browser storage. Records every write attempt, can be "full" (setItem throws QuotaExceededError)
// or "unreadable" (getItem throws).
class FakeStorage {
  constructor(entries = {}) {
    this.map = new Map(Object.entries(entries));
    this.full = false;
    this.readThrows = false;
    this.writes = [];
  }
  get length() { return this.map.size; }
  key(i) { const keys = [...this.map.keys()]; return i < keys.length ? keys[i] : null; }
  getItem(k) {
    if (this.readThrows) throw new DOMException('Access denied', 'SecurityError');
    k = String(k);
    return this.map.has(k) ? this.map.get(k) : null;
  }
  setItem(k, v) {
    this.writes.push({ op: 'set', key: String(k), value: String(v) });
    if (this.full) throw new DOMException('The quota has been exceeded.', 'QuotaExceededError');
    this.map.set(String(k), String(v));
  }
  removeItem(k) { this.writes.push({ op: 'remove', key: String(k) }); this.map.delete(String(k)); }
  clear() { this.writes.push({ op: 'clear' }); this.map.clear(); }
  raw(k = KEY) { return this.map.has(k) ? this.map.get(k) : null; }
  writesTo(k = KEY) { return this.writes.filter((w) => w.op === 'clear' || w.key === k); }
}

function seeded(todos) {
  return new FakeStorage({ [KEY]: JSON.stringify(todos) });
}

function installStorage(storage) {
  Object.defineProperty(globalThis, 'localStorage', { value: storage, configurable: true, writable: true });
}

// "Open the app" (or reload the page): install the storage, load a fresh store.js, call store.load().
function openApp(storage) {
  installStorage(storage);
  const file = require.resolve('../app/store.js');
  delete require.cache[file];
  const mod = require('../app/store.js');
  // AMBIGUOUS: api.md names `store` and says `STORE_KEY` is exported, but not the export shape;
  // accept either `module.exports = { store, STORE_KEY }` or `module.exports = store` (with STORE_KEY on it).
  const store = mod.store || mod;
  const STORE_KEY = mod.STORE_KEY !== undefined ? mod.STORE_KEY : store.STORE_KEY;
  const loaded = store.load();
  return { store, STORE_KEY, loaded };
}

function makeTodos(n, tag = 't') {
  return Array.from({ length: n }, (_, i) => ({
    id: `${tag}-${i + 1}`,
    title: `${tag} việc số ${i + 1}`,
    done: i % 3 === 0,
    createdAt: 1760000000000 + i * 1000,
  }));
}

// Backup file text built straight from the spec's structure, independent of the code under test.
function backupText(todos, extraTop = {}) {
  return JSON.stringify({ version: 1, todos, ...extraTop }, null, 2);
}

function fileOf(text) {
  return { size: Buffer.byteLength(text, 'utf8'), text: async () => text };
}

// ask(question) spy. `onAsk` lets a test look at the world at the moment the question is asked.
function asker(answer, onAsk) {
  const fn = async (question) => {
    fn.questions.push(question);
    if (onAsk) onAsk(question);
    return answer;
  };
  fn.questions = [];
  return fn;
}

// AC12: 5,000 todos with 200-character titles.
function bigTodos(count = 5000) {
  return Array.from({ length: count }, (_, i) => ({
    id: `big-${i + 1}`,
    title: (`việc ${i + 1} `).padEnd(200, 'a'),
    done: i % 2 === 0,
    createdAt: 1760000000000 + i,
  }));
}

const nfc = (s) => String(s).normalize('NFC');
// Treat typographic quotes as the straight quotes used in the spec.
const plainQuotes = (s) => nfc(s).replace(/[“”]/g, '"');

function readIndexHtml() {
  return fs.readFileSync(path.join(__dirname, '..', 'app', 'index.html'), 'utf8');
}

module.exports = {
  KEY, NOT_SAVED_HINT, UNREADABLE_TEXT,
  FakeStorage, seeded, installStorage, openApp,
  makeTodos, backupText, fileOf, asker, bigTodos,
  nfc, plainQuotes, readIndexHtml,
};
