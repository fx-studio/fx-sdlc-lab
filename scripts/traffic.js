#!/usr/bin/env node
// Simulated users for one environment (SDLC-6, Maintain). The todo app has no server, so there is no 5xx rate to watch.
// The stand-in: simulated users run the app's own logic (store.js + backup.js of the release that is live in <env>) and
// we count the actions that fail from the user's side. This is SIMULATED traffic, not real users.
//
//   node scripts/traffic.js --release <dir> --state <file.json> --seed <n> [--users 40] [--fault 0.01]
//
// One run = one simulated day. Each user keeps their browser storage in <state> between days (so a bad release that
// writes something wrong today breaks tomorrow's session, as it would for a real person).
// A failed action is one of:
//   - not_saved      persist() told the user "not saved" (storage refused the write)
//   - import_failed  the user backed up to a file and imported that same file back, and the app refused it
//   - exception      the app code threw
// Storage refuses a write with probability --fault (the browser quota, a private window...). That is the normal noise.
// Prints one JSON line: { actions, failed, rate, by_kind, users, release }.
'use strict';
const fs = require('node:fs');
const path = require('node:path');

function arg(name, dflt) {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : dflt;
}

// Small deterministic PRNG (mulberry32): the same seed gives the same day.
function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const release = path.resolve(arg('--release'));
const stateFile = arg('--state');
const rand = rng(Number(arg('--seed', '1')));
const USERS = Number(arg('--users', '40'));
const FAULT = Number(arg('--fault', '0.01'));
const TAG = arg('--tag', ''); // id prefix of a check run, so it never repeats the ids of the day's real run

const { store, STORE_KEY } = require(path.join(release, 'store.js'));
const backup = require(path.join(release, 'backup.js'));

const state = stateFile && fs.existsSync(stateFile) ? JSON.parse(fs.readFileSync(stateFile, 'utf8')) : {};
const WORDS = ['Mua sữa', 'Gọi mẹ', 'Nộp báo cáo', 'Đặt vé', 'Trả tiền điện', 'Đọc sách', 'Tập thể dục', 'Sửa xe', 'Họp nhóm'];

function storageFor(user) {
  const data = state[user] || {};
  state[user] = data;
  return {
    getItem: (k) => (Object.prototype.hasOwnProperty.call(data, k) ? data[k] : null),
    setItem: (k, v) => {
      if (rand() < FAULT) {
        const e = new Error('quota');
        e.name = 'QuotaExceededError';
        throw e;
      }
      data[k] = String(v);
    },
  };
}

let actions = 0;
let failed = 0;
const byKind = { not_saved: 0, import_failed: 0, exception: 0 };
const fail = (kind) => {
  failed++;
  byKind[kind]++;
};

async function session(user, day) {
  globalThis.localStorage = storageFor(user);
  let todos = store.load().todos;
  const n = 3 + Math.floor(rand() * 6);
  for (let i = 0; i < n; i++) {
    const r = rand();
    actions++;
    try {
      if (r < 0.45 || todos.length === 0) {
        const t = { id: `${TAG}${user}-${day}-${i}`, title: WORDS[Math.floor(rand() * WORDS.length)], done: false,
          createdAt: Date.UTC(2026, 9, 1) + day * 86400000 + i };
        todos = [...todos, t];
        if (backup.persist(store, todos).message) fail('not_saved');
      } else if (r < 0.72) {
        const k = Math.floor(rand() * todos.length);
        todos = todos.map((t, j) => (j === k ? { ...t, done: !t.done } : t));
        if (backup.persist(store, todos).message) fail('not_saved');
      } else if (r < 0.85) {
        const k = Math.floor(rand() * todos.length);
        todos = todos.filter((_, j) => j !== k);
        if (backup.persist(store, todos).message) fail('not_saved');
      } else {
        // Back up to a file, then import that same file (for example on a new laptop).
        const text = backup.toBackupText(todos);
        const file = { size: Buffer.byteLength(text), text: async () => text };
        const out = await backup.importBackup({ store, current: todos, file, ask: async () => true });
        const ok = out.message && out.message.startsWith('Đã nhập');
        if (ok) todos = out.todos;
        else fail('import_failed');
      }
    } catch {
      fail('exception');
    }
  }
}

(async () => {
  const day = Number(arg('--day', '0'));
  for (let u = 0; u < USERS; u++) await session(`u${String(u).padStart(2, '0')}`, day);
  if (stateFile) fs.writeFileSync(stateFile, JSON.stringify(state));
  let rel = null;
  try {
    rel = JSON.parse(fs.readFileSync(path.join(release, 'RELEASE.json'), 'utf8')).id;
  } catch {}
  console.log(JSON.stringify({ actions, failed, rate: actions ? failed / actions : 0, by_kind: byKind, users: USERS, release: rel,
    key: STORE_KEY }));
})();
