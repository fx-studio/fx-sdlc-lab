// E1 · requirement from R7a/R7b-B (SDLC-3): importing never replaces a non-empty list without asking, even when two imports overlap.
// v2 (2026-10-29, R6a): v1 replayed the accepted fix's design (the second-picked file must finish first) and hung on a correct fix
// that runs imports one at a time. v2 checks only the requirement: the dialog answers "Huỷ", so exactly one replace may happen
// (the first one, into the empty list) and the other import must have asked.
const test = require('node:test');
const assert = require('node:assert/strict');
const { backup, loadApp } = require('./_harness.js');

function slowFile(text) {
  let finish;
  const done = new Promise((resolve) => { finish = resolve; });
  return { file: { size: text.length, text: () => done.then(() => text) }, finish };
}
const backupOf = (...titles) =>
  backup.toBackupText(titles.map((title, i) => ({ id: `id-${title}-${i}`, title, done: false, createdAt: 1 })));
const tick = () => new Promise((r) => setTimeout(r, 0));

for (const order of ['small first', 'large first']) {
  test(`E1: two overlapping imports (${order} to finish): no silent replace of a non-empty list`, async () => {
    const { replaced, asked, pick } = loadApp();
    const large = slowFile(backupOf('Lớn 1', 'Lớn 2', 'Lớn 3'));
    const small = slowFile(backupOf('Nhỏ'));
    const first = pick(large.file);
    const second = pick(small.file);
    const [a, b] = order === 'small first' ? [small, large] : [large, small];
    a.finish();
    for (let i = 0; i < 5; i++) await tick();
    b.finish();
    await Promise.all([first, second]);
    for (let i = 0; i < 5; i++) await tick();
    assert.equal(replaced.length, 1, 'only the import into the empty list may replace without a "Thay" answer');
    assert.equal(asked.length, 1, 'the other import asked first');
  });
}
