// Static checks on app/ files (plan/2026-10-19-khach-khong-mat-viec.md, commit B). Run: node --test
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const read = (f) => fs.readFileSync(path.join(__dirname, '..', 'app', f), 'utf8');
const html = read('index.html');

test('scripts load in the order store, backup, app (Q2)', () => {
  const scripts = [...html.matchAll(/<script\b[^>]*\bsrc="([^"]+)"/g)].map((m) => m[1]);
  assert.deepEqual(scripts, ['store.js', 'backup.js', 'app.js']);
});

test('index.html loads nothing from outside (AC26, S4)', () => {
  assert.doesNotMatch(html, /\b(src|href)\s*=\s*["']?\s*(https?:)?\/\//i);
});

test('only store.js touches browser storage', () => {
  for (const f of ['app.js', 'backup.js']) assert.doesNotMatch(read(f), /localStorage/, f);
});

test('the main screen says where the list is kept, and has the new controls (AC23, U5)', () => {
  assert.ok(html.includes(
    'Danh sách chỉ được lưu trên trình duyệt này, nên xoá dữ liệu trang web, đổi trình duyệt hoặc đổi máy là mất, trừ khi bạn đã sao lưu ra file.'));
  assert.ok(html.includes('>Sao lưu ra file</button>'));
  assert.match(html, /<label[^>]*>Nhập từ file<input type="file"/);
  assert.match(html, /role="status"/);
  assert.match(html, /<dialog id="confirm" aria-labelledby="confirm-text">/);
});

test('visible text in index.html has no technical words (AC24, U4)', () => {
  const text = html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<[^>]+>/g, ' ');
  assert.doesNotMatch(text, /localStorage|JSON|console/i);
});
