// Shared by the hidden eval tests: runs app/app.js unchanged in a vm with a minimal fake page (same idea as tests/app.test.js).
// Hidden tests (*.eval.js, a name `node --test` does not pick up on its own) are copied next to this file into <worktree>/evaltmp/ after the agent has finished, so the agent never sees them.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const backup = require('../app/backup.js');

const appJs = fs.readFileSync(path.join(__dirname, '..', 'app', 'app.js'), 'utf8');

function fakeElement() {
  const el = {
    textContent: '', innerHTML: '', hidden: false, value: '', className: '', dataset: {},
    append() {},
    querySelector(sel) { return (el.children[sel] ||= fakeElement()); },
    children: {},
    classList: { toggle() {} },
  };
  return el;
}

function loadApp(initial = []) {
  const elements = {};
  const replaced = [];
  const store = {
    readError: false,
    load() { return { todos: initial, readError: false }; },
    save() { return 'saved'; },
    replace(todos) { replaced.push(todos); return 'saved'; },
  };
  const document = {
    querySelector(sel) { return (elements[sel] ||= fakeElement()); },
    querySelectorAll() { return []; },
    createElement() { return fakeElement(); },
  };
  vm.runInNewContext(appJs, { ...backup, store, document, crypto });
  const asked = [];
  Object.assign(document.querySelector('#confirm'), {
    showModal() { asked.push(document.querySelector('#confirm-text').textContent); },
    addEventListener(type, fn) { queueMicrotask(fn); },
  });
  const $ = (sel) => document.querySelector(sel);
  return {
    $, replaced, asked,
    pick: (file) => $('#import').onchange({ target: { files: [file], value: '' } }),
    count: () => $('#count').textContent,
    filter: (f) => $('#filters').onclick({ target: { dataset: { filter: f } } }),
  };
}

function todos(n, done = false) {
  return Array.from({ length: n }, (_, i) => ({ id: `id-${done}-${i}`, title: `Việc ${i}`, done, createdAt: 1 }));
}

module.exports = { backup, loadApp, todos };
