# R3-code-theo-plan

Chạy 2026-10-27 09:48 ở gốc repo, chế độ quyền `acceptEdits`, tiếp session trước. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

The plan is accepted: plan/2026-10-19-khach-khong-mat-viec.md (Khoa approved it as Large, with conditions; Linh changed M11 and M12 under Q7). Implement it now, commit A then commit B in that order. You cannot commit: stop after each part is done and its tests pass, then go on; a person commits both parts afterwards. If the code has to depart from the plan, do not edit the plan; tell me where and why. Run node --test before you finish.

## Tool call (43)

1. Bash · command=git log --oneline -3 && git status --short && git diff HEAD~1 --stat 2>/dev/null | tail -3; sed -n 1,5p plan/2026-10-19-khach-khong-mat-viec.md; grep -n "M11\|M12\|Q7" plan/2026-10-19-khach-khong-mat-viec.md
2. Read · file_path=<repo>/plan/2026-10-19-khach-khong-mat-viec.md
3. Bash · command=cat demo/sdlc-3/runs/R2e-linh-q7/transcript.md; grep -n "P4" .claude/skills/policy-privacy/SKILL.md
4. Bash · command=node --version
5. Write · file_path=<repo>/app/backup.js
6. Write · file_path=<repo>/tests/backup.test.js
7. Bash · command=node --check app/backup.js && node --test 2>&1 | tail -25
8. Grep · pattern=store\.(load|save|replace|readError)|localStorage
9. Write · file_path=<repo>/app/store.js
10. Bash · command=sed -i '' 's/return write(todos);/return writeList(todos);/; s/const result = write(todos);/const result = writeList(todos);/; s/^function write(todos) {/function writeList(todos) {/' app/store.js && grep -n "write" app/store.js && node --check app/store.js
11. Edit · file_path=<repo>/app/store.js
12. Edit · file_path=<repo>/app/store.js
13. Edit · file_path=<repo>/app/store.js
14. Write · file_path=<repo>/tests/store.test.js
15. Bash · command=node --test 2>&1 | grep -E "^(✖|ℹ (tests|pass|fail))" ; node --test tests/store.test.js 2>&1 | grep -A15 "✖" | head -40
16. Write · file_path=<repo>/app/index.html
17. Write · file_path=<repo>/app/style.css
18. Write · file_path=<repo>/tests/static.test.js
19. Write · file_path=<repo>/app/app.js
20. Bash · command=for f in app/*.js tests/*.js; do node --check "$f" || echo "FAIL $f"; done; node --test 2>&1 | grep -E "^(✖|ℹ (tests|pass|fail))"
21. Bash · command=node --check app/app.js && node --check app/store.js && node --check app/backup.js && node --check tests/backup.test.js && node --check tests/store.test.js && node --check tests/static.test.js && echo "check ok" && node --test 2>&1 | grep -E "^(✖|ℹ (tests|pass|fail))"
22. Agent · subagent_type=verifier
23. Read · file_path=<repo>/plan/2026-10-19-khach-khong-mat-viec.md
24. Bash · command=git status --short && git diff --stat && ls tests app
25. Bash · command=git diff && cat app/backup.js && cat app/app.js
26. Bash · command=node --test 2>&1 | tail -40; for f in app/*.js; do node --check $f && echo "ok $f"; done
27. Bash · command=node --test 2>&1 | tail -15; node --check app/app.js && node --check app/backup.js && node --check app/store.js && echo check-ok; node --version
28. Bash · command=node --test 2>&1 | grep -E '^[✔✖]'; echo ----; cat tests/store.test.js tests/static.test.js; echo ----; grep -nE "^test\(|^  test\(|test\('" tests/backup.test.js
29. Read · file_path=<repo>/tests/backup.test.js
30. Bash · command=grep -rnE "store\.(load|save|replace)|localStorage" --exclude-dir=demo --exclude-dir=docs --exclude-dir=.git . | grep -v "^./plan/\|^./spec/\|^./intent/\|^./tickets/" 
31. Bash · command=mkdir -p <thư-mục-tạm> && cat > <thư-mục-tạm> <<'EOF'
const vm = require('vm'), fs = require('fs'), crypto = require('crypto');
const APP = '<repo>/app/';
function el(id) {
  const e = { id, hidden: false, textContent: '', value: '', children: [], className: '', dataset: {},
    classList: { toggle() {} }, _inner: '',
    set innerHTML(v) { e._inner = v; if (v === '') e.children = []; else { e.span = el('span'); e.input = el('input'); e.button = el('button'); } },
    get innerHTML() { return e._inner; },
    append(c) { e.children.push(c); }, remove() {},
    querySelector(s) { return s === 'span' ? e.span : s === 'input' ? e.input : e.button; },
    addEventListener() {}, showModal() {}, click() {} };
  return e;
}
function run(raw, { label }) {
  const data = new Map(); if (raw !== undefined) data.set('todo.v1', raw);
  let sets = 0;
  const localStorage = { getItem: (k) => data.has(k) ? data.get(k) : null, setItem: (k, v) => { sets++; data.set(k, String(v)); } };
  const els = {};
  const document = { querySelector: (s) => (els[s] ||= el(s)), querySelectorAll: () => [], createElement: (t) => el(t), body: el('body') };
  const ctx = vm.createContext({ document, localStorage, crypto, TextEncoder, Blob, URL, setTimeout, console });
  // top-level const/let are shared across scripts in one context, like separate <script> tags
  for (const f of ['store.js', 'backup.js', 'app.js']) vm.runInContext(fs.readFileSync(APP + f, 'utf8'), ctx, { filename: f });
  const $ = (s) => els[s];
  const state = () => ({ items: $('#list').children.length, banner: !$('#unreadable').hidden, empty: !$('#empty').hidden,
    msg: $('#message').textContent, sets, size: data.size, stored: (data.get('todo.v1') || '').slice(0, 20),
    storedCount: (() => { try { return JSON.parse(data.get('todo.v1')).length; } catch { return 'n/a'; } })() });
  console.log(`\n== ${label}`); console.log(' open   ', JSON.stringify(state()));
  $('#title').value = 'Việc mới'; $('#add').onsubmit({ preventDefault() {} });
  console.log(' add    ', JSON.stringify(state()));
  $('#list').children[0].input.onchange();
  console.log(' toggle ', JSON.stringify(state()), 'first done =', vm.runInContext('todos[0].done', ctx));
  $('#list').children[0].button.onclick();
  console.log(' remove ', JSON.stringify(state()));
  console.log(' banner text ok:', $('#unreadable').textContent.startsWith('Không đọc được danh sách'), ' empty text ok:', $('#empty').textContent.startsWith('Chưa có việc nào.'));
}
const list = (n) => JSON.stringify(Array.from({ length: n }, (_, i) => ({ id: crypto.randomUUID(), title: 'Việc ' + i, done: i % 3 === 0, createdAt: Date.now() - i })));
run(list(3), { label: 'current format, 3 todos' });
run(list(2000), { label: 'current format, 2000 todos' });
run('{hỏng', { label: '{hỏng' });
run('{"a": 1}', { label: '{"a": 1}' });
run('null', { label: '"null"' });
run(undefined, { label: 'no key' });
run('[]', { label: 'saved []' });
EOF
node <thư-mục-tạm>
32. Bash · command=cat > <thư-mục-tạm> <<'EOF'
const vm = require('vm'), fs = require('fs'), crypto = require('crypto');
const APP = '<repo>/app/';
const LB = String.fromCharCode(123);
function el(id) {
  const e = { id, hidden: false, textContent: '', value: '', children: [], className: '', dataset: {},
    classList: { toggle() {} }, _inner: '',
    set innerHTML(v) { e._inner = v; if (v === '') e.children = []; else { e.span = el('span'); e.input = el('input'); e.button = el('button'); } },
    get innerHTML() { return e._inner; },
    append(c) { e.children.push(c); }, remove() {},
    querySelector(s) { return s === 'span' ? e.span : s === 'input' ? e.input : e.button; },
    addEventListener() {}, showModal() {}, click() {} };
  return e;
}
function run(raw, label) {
  const data = new Map(); if (raw !== undefined) data.set('todo.v1', raw);
  let sets = 0;
  const localStorage = { getItem: (k) => data.has(k) ? data.get(k) : null, setItem: (k, v) => { sets++; data.set(k, String(v)); } };
  const els = {};
  const document = { querySelector: (s) => (els[s] ||= el(s)), querySelectorAll: () => [], createElement: (t) => el(t), body: el('body') };
  const ctx = vm.createContext({ document, localStorage, crypto, TextEncoder, Blob, URL, setTimeout, console });
  for (const f of ['store.js', 'backup.js', 'app.js']) vm.runInContext(fs.readFileSync(APP + f, 'utf8'), ctx, { filename: f });
  const $ = (s) => els[s];
  const state = () => JSON.stringify({ shown: $('#list').children.length, banner: !$('#unreadable').hidden, empty: !$('#empty').hidden,
    msg: $('#message').textContent, setItemCalls: sets, keys: data.size, stored: (data.get('todo.v1') || '').slice(0, 12),
    storedCount: (() => { try { return JSON.parse(data.get('todo.v1')).length; } catch (e) { return 'n/a'; } })() });
  console.log('\n== ' + label); console.log(' open   ', state());
  $('#title').value = 'Việc mới'; $('#add').onsubmit({ preventDefault() {} });
  console.log(' add    ', state());
  $('#list').children[0].input.onchange();
  console.log(' toggle ', state(), 'todos[0].done=' + vm.runInContext('todos[0].done', ctx));
  $('#list').children[0].button.onclick();
  console.log(' remove ', state());
  console.log(' banner text ok:', $('#unreadable').textContent.startsWith('Không đọc được danh sách'), ' empty text ok:', $('#empty').textContent.startsWith('Chưa có việc nào.'));
}
const list = (n) => JSON.stringify(Array.from({ length: n }, (_, i) => ({ id: crypto.randomUUID(), title: 'Việc ' + i, done: i % 3 === 0, createdAt: Date.now() - i })));
run(list(3), 'current format, 3 todos');
run(list(2000), 'current format, 2000 todos');
run(LB + 'hỏng', 'broken: LB+hỏng');
run(LB + '"a": 1}', 'broken: object');
run('null', 'broken: "null"');
run(undefined, 'no key');
run('[]', 'saved []');
EOF
node <thư-mục-tạm>
33. Bash · command=S=<thư-mục-tạm> cat > $S/harness.js <<'EOF'
const vm = require('vm'), fs = require('fs'), crypto = require('crypto');
const APP = '<repo>/app/';
const LB = String.fromCharCode(123), RB = String.fromCharCode(125);
function el(id) {
  const e = { id, hidden: false, textContent: '', value: '', children: [], className: '', dataset: {},
    classList: { toggle() {} }, _inner: '',
    set innerHTML(v) { e._inner = v; if (v === '') e.children = []; else { e.span = el('span'); e.input = el('input'); e.button = el('button'); } },
    get innerHTML() { return e._inner; },
    append(c) { e.children.push(c); }, remove() {},
    querySelector(s) { return s === 'span' ? e.span : s === 'input' ? e.input : e.button; },
    addEventListener() {}, showModal() {}, click() {} };
  return e;
}
function run(raw, label) {
  const data = new Map(); if (raw !== undefined) data.set('todo.v1', raw);
  let sets = 0;
  const localStorage = { getItem: (k) => data.has(k) ? data.get(k) : null, setItem: (k, v) => { sets++; data.set(k, String(v)); } };
  const els = {};
  const document = { querySelector: (s) => (els[s] ||= el(s)), querySelectorAll: () => [], createElement: (t) => el(t), body: el('body') };
  const ctx = vm.createContext({ document, localStorage, crypto, TextEncoder, Blob, URL, setTimeout, console });
  for (const f of ['store.js', 'backup.js', 'app.js']) vm.runInContext(fs.readFileSync(APP + f, 'utf8'), ctx, { filename: f });
  const $ = (s) => els[s];
  const count = () => { try { return JSON.parse(data.get('todo.v1')).length; } catch (e) { return 'n/a'; } };
  const state = () => JSON.stringify({ shown: $('#list').children.length, banner: !$('#unreadable').hidden, empty: !$('#empty').hidden,
    msg: $('#message').textContent, setItemCalls: sets, keys: data.size, stored: (data.get('todo.v1') || '').slice(0, 12), storedCount: count() });
  console.log('\n== ' + label); console.log(' open   ', state());
  $('#title').value = 'Việc mới'; $('#add').onsubmit({ preventDefault() {} });
  console.log(' add    ', state());
  $('#list').children[0].input.onchange();
  console.log(' toggle ', state(), 'todos[0].done=' + vm.runInContext('todos[0].done', ctx));
  $('#list').children[0].button.onclick();
  console.log(' remove ', state());
  console.log(' banner text ok:', $('#unreadable').textContent.startsWith('Không đọc được danh sách'), ' empty text ok:', $('#empty').textContent.startsWith('Chưa có việc nào.'));
}
const list = (n) => JSON.stringify(Array.from({ length: n }, (_, i) => ({ id: crypto.randomUUID(), title: 'Việc ' + i, done: i % 3 === 0, createdAt: Date.now() - i })));
run(list(3), 'current format, 3 todos');
run(list(2000), 'current format, 2000 todos');
run(LB + 'hỏng', 'broken: LB+hỏng');
run(LB + '"a": 1' + RB, 'broken: object a:1');
run('null', 'broken: null');
run(undefined, 'no key');
run('[]', 'saved empty array');
EOF
node $S/harness.js
34. Bash · command=cat > <thư-mục-tạm> <<EOF
const vm = require('vm'), fs = require('fs'), crypto = require('crypto');
const APP = '<repo>/app/';
const LB = String.fromCharCode(123), RB = String.fromCharCode(125);
function el(id) {
  const e = { id, hidden: false, textContent: '', value: '', children: [], className: '', dataset: {},
    classList: { toggle() {} }, _inner: '',
    set innerHTML(v) { e._inner = v; if (v === '') e.children = []; else { e.span = el('span'); e.input = el('input'); e.button = el('button'); } },
    get innerHTML() { return e._inner; },
    append(c) { e.children.push(c); }, remove() {},
    querySelector(s) { return s === 'span' ? e.span : s === 'input' ? e.input : e.button; },
    addEventListener() {}, showModal() {}, click() {} };
  return e;
}
function run(raw, label) {
  const data = new Map(); if (raw !== undefined) data.set('todo.v1', raw);
  let sets = 0;
  const localStorage = { getItem: (k) => data.has(k) ? data.get(k) : null, setItem: (k, v) => { sets++; data.set(k, String(v)); } };
  const els = {};
  const document = { querySelector: (s) => (els[s] ||= el(s)), querySelectorAll: () => [], createElement: (t) => el(t), body: el('body') };
  const ctx = vm.createContext({ document, localStorage, crypto, TextEncoder, Blob, URL, setTimeout, console });
  for (const f of ['store.js', 'backup.js', 'app.js']) vm.runInContext(fs.readFileSync(APP + f, 'utf8'), ctx, { filename: f });
  const q = (s) => els[s];
  const count = () => { try { return JSON.parse(data.get('todo.v1')).length; } catch (e) { return 'n/a'; } };
  const state = () => JSON.stringify({ shown: q('#list').children.length, banner: !q('#unreadable').hidden, empty: !q('#empty').hidden,
    msg: q('#message').textContent, setItemCalls: sets, keys: data.size, stored: (data.get('todo.v1') || '').slice(0, 12), storedCount: count() });
  console.log('\n== ' + label); console.log(' open   ', state());
  q('#title').value = 'Việc mới'; q('#add').onsubmit({ preventDefault() {} });
  console.log(' add    ', state());
  q('#list').children[0].input.onchange();
  console.log(' toggle ', state(), 'todos[0].done=' + vm.runInContext('todos[0].done', ctx));
  q('#list').children[0].button.onclick();
  console.log(' remove ', state());
  console.log(' banner text ok:', q('#unreadable').textContent.startsWith('Không đọc được danh sách'), ' empty text ok:', q('#empty').textContent.startsWith('Chưa có việc nào.'));
}
const list = (n) => JSON.stringify(Array.from({ length: n }, (_, i) => ({ id: crypto.randomUUID(), title: 'Việc ' + i, done: i % 3 === 0, createdAt: Date.now() - i })));
run(list(3), 'current format, 3 todos');
run(list(2000), 'current format, 2000 todos');
run(LB + 'hỏng', 'broken: LB+hỏng');
run(LB + '"a": 1' + RB, 'broken: object a:1');
run('null', 'broken: null');
run(undefined, 'no key');
run('[]', 'saved empty array');
EOF
node <thư-mục-tạm>
35. Bash · command=node -e "const o = { a: 1 }; console.log(o.a)"
36. Bash · command=node -e 'const o = { a: 1 }; console.log(o.a)'
37. Bash · command=node -e "
const vm = require('vm'), fs = require('fs'), crypto = require('crypto');
const APP = '<repo>/app/';
const LB = String.fromCharCode(123), RB = String.fromCharCode(125), DQ = String.fromCharCode(34);
function el(id) {
  const e = { id, hidden: false, textContent: '', value: '', children: [], className: '', dataset: {},
    classList: { toggle() {} }, _inner: '',
    set innerHTML(v) { e._inner = v; if (v === '') e.children = []; else { e.span = el('span'); e.input = el('input'); e.button = el('button'); } },
    get innerHTML() { return e._inner; },
    append(c) { e.children.push(c); }, remove() {},
    querySelector(s) { return s === 'span' ? e.span : s === 'input' ? e.input : e.button; },
    addEventListener() {}, showModal() {}, click() {} };
  return e;
}
function run(raw, label) {
  const data = new Map(); if (raw !== undefined) data.set('todo.v1', raw);
  let sets = 0;
  const localStorage = { getItem: (k) => data.has(k) ? data.get(k) : null, setItem: (k, v) => { sets++; data.set(k, String(v)); } };
  const els = {};
  const document = { querySelector: (s) => (els[s] ||= el(s)), querySelectorAll: () => [], createElement: (t) => el(t), body: el('body') };
  const ctx = vm.createContext({ document, localStorage, crypto, TextEncoder, Blob, URL, setTimeout, console });
  for (const f of ['store.js', 'backup.js', 'app.js']) vm.runInContext(fs.readFileSync(APP + f, 'utf8'), ctx, { filename: f });
  const q = (s) => els[s];
  const count = () => { try { return JSON.parse(data.get('todo.v1')).length; } catch (e) { return 'n/a'; } };
  const state = () => JSON.stringify({ shown: q('#list').children.length, banner: !q('#unreadable').hidden, empty: !q('#empty').hidden,
    msg: q('#message').textContent, setItemCalls: sets, keys: data.size, stored: (data.get('todo.v1') || '').slice(0, 12), storedCount: count() });
  console.log('== ' + label); console.log(' open   ', state());
  q('#title').value = 'Việc mới'; q('#add').onsubmit({ preventDefault() {} });
  console.log(' add    ', state());
  q('#list').children[0].input.onchange();
  console.log(' toggle ', state(), 'todos[0].done=' + vm.runInContext('todos[0].done', ctx));
  q('#list').children[0].button.onclick();
  console.log(' remove ', state());
  console.log(' banner text ok:', q('#unreadable').textContent.startsWith('Không đọc được danh sách'), ' empty text ok:', q('#empty').textContent.startsWith('Chưa có việc nào.'));
}
const list = (n) => JSON.stringify(Array.from({ length: n }, (_, i) => ({ id: crypto.randomUUID(), title: 'Việc ' + i, done: i % 3 === 0, createdAt: Date.now() - i })));
run(list(3), 'current format, 3 todos');
run(list(2000), 'current format, 2000 todos');
run(LB + 'hỏng', 'broken: LB+hỏng');
run(LB + DQ + 'a' + DQ + ': 1' + RB, 'broken: object a:1');
run('null', 'broken: null');
run(undefined, 'no key');
run('[]', 'saved empty array');
"
38. Bash · command=node -e "
const vm = require('vm'), fs = require('fs'), crypto = require('crypto');
const APP = '<repo>/app/';
const LB = String.fromCharCode(123), RB = String.fromCharCode(125), DQ = String.fromCharCode(34);
function el(id) {
  const e = { id, hidden: false, textContent: '', value: '', children: [], className: '', dataset: {},
    classList: { toggle() {} }, _inner: '',
    set innerHTML(v) { e._inner = v; if (v === '') e.children = []; else { e.span = el('span'); e.input = el('input'); e.button = el('button'); } },
    get innerHTML() { return e._inner; },
    append(c) { e.children.push(c); }, remove() {},
    querySelector(s) { return s === 'span' ? e.span : s === 'input' ? e.input : e.button; },
    addEventListener() {}, showModal() {}, click() {} };
  return e;
}
function run(raw, label) {
  const data = new Map(); if (raw !== undefined) data.set('todo.v1', raw);
  let sets = 0;
  const localStorage = { getItem: (k) => data.has(k) ? data.get(k) : null, setItem: (k, v) => { sets++; data.set(k, String(v)); } };
  const els = {};
  const document = { querySelector: (s) => (els[s] ||= el(s)), querySelectorAll: () => [], createElement: (t) => el(t), body: el('body') };
  const ctx = vm.createContext({ document, localStorage, crypto, TextEncoder, Blob, URL, setTimeout, console });
  for (const f of ['store.js', 'backup.js', 'app.js']) vm.runInContext(fs.readFileSync(APP + f, 'utf8'), ctx, { filename: f });
  const q = document.querySelector;
  const count = () => { try { return JSON.parse(data.get('todo.v1')).length; } catch (e) { return 'n/a'; } };
  const state = () => JSON.stringify({ shown: q('#list').children.length, banner: !q('#unreadable').hidden, empty: !q('#empty').hidden,
    msg: q('#message').textContent, setItemCalls: sets, keys: data.size, stored: (data.get('todo.v1') || '').slice(0, 12), storedCount: count() });
  console.log('== ' + label); console.log(' open   ', state());
  q('#title').value = 'Việc mới'; q('#add').onsubmit({ preventDefault() {} });
  console.log(' add    ', state());
  q('#list').children[0].input.onchange();
  console.log(' toggle ', state(), 'todos[0].done=' + vm.runInContext('todos[0].done', ctx));
  q('#list').children[0].button.onclick();
  console.log(' remove ', state());
  console.log(' banner text ok:', q('#unreadable').textContent.startsWith('Không đọc được danh sách'), ' empty text ok:', q('#empty').textContent.startsWith('Chưa có việc nào.'));
}
const list = (n) => JSON.stringify(Array.from({ length: n }, (_, i) => ({ id: crypto.randomUUID(), title: 'Việc ' + i, done: i % 3 === 0, createdAt: Date.now() - i })));
run(list(3), 'current format, 3 todos');
run(list(2000), 'current format, 2000 todos');
run(LB + 'hỏng', 'broken: LB+hỏng');
run(LB + DQ + 'a' + DQ + ': 1' + RB, 'broken: object a:1');
run('null', 'broken: null');
run(undefined, 'no key');
run('[]', 'saved empty array');
"
39. Bash · command=node -e "
const vm = require('vm'), fs = require('fs'), crypto = require('crypto');
const APP = '<repo>/app/';
const LB = String.fromCharCode(123);
let answer = 'yes', asked = [], clicks = 0, revokes = 0;
function el(id) {
  const e = { id, hidden: false, textContent: '', value: '', children: [], className: '', dataset: {}, files: [],
    classList: { toggle() {} }, _inner: '', handlers: [],
    set innerHTML(v) { e._inner = v; if (v === '') e.children = []; else { e.span = el('span'); e.input = el('input'); e.button = el('button'); } },
    get innerHTML() { return e._inner; },
    append(c) { e.children.push(c); }, remove() {},
    querySelector(s) { return s === 'span' ? e.span : s === 'input' ? e.input : e.button; },
    addEventListener(n, h) { e.handlers.push(h); },
    showModal() { setTimeout(() => { e.returnValue = answer; e.handlers.splice(0).forEach((h) => h()); }, 0); },
    click() { clicks++; } };
  return e;
}
function boot(raw) {
  const data = new Map(); if (raw !== undefined) data.set('todo.v1', raw);
  const ls = { full: false, sets: 0, getItem: (k) => data.has(k) ? data.get(k) : null,
    setItem(k, v) { ls.sets++; if (ls.full) throw Object.assign(new Error('q'), { name: 'QuotaExceededError' }); data.set(k, String(v)); } };
  const els = {};
  const document = { querySelector: (s) => (els[s] ||= el(s)), querySelectorAll: () => [], createElement: (t) => el(t), body: el('body') };
  const FakeURL = { createObjectURL: () => 'blob:x', revokeObjectURL: () => { revokes++; } };
  const timers = [];
  const ctx = vm.createContext({ document, localStorage: ls, crypto, TextEncoder, Blob, URL: FakeURL, console,
    setTimeout: (f, ms) => { if (ms === 10000) timers.push(f); else setTimeout(f, ms); } });
  for (const f of ['store.js', 'backup.js', 'app.js']) vm.runInContext(fs.readFileSync(APP + f, 'utf8'), ctx);
  return { q: document.querySelector, data, ls, ctx, timers };
}
const list = (n) => Array.from({ length: n }, (_, i) => ({ id: crypto.randomUUID(), title: 'V ' + i, done: false, createdAt: Date.now() - i }));
const file = (todos) => { const t = JSON.stringify({ version: 1, todos }); return { size: Buffer.byteLength(t), text: async () => t }; };
(async () => {
  // storage full on add
  let a = boot(JSON.stringify(list(3)));
  a.ls.full = true; a.q('#title').value = 'X'; a.q('#add').onsubmit({ preventDefault() {} });
  console.log('full: shown', a.q('#list').children.length, '| msg', a.q('#message').textContent, '| stored count', JSON.parse(a.data.get('todo.v1')).length);
  a.ls.full = false; a.q('#title').value = 'Y'; a.q('#add').onsubmit({ preventDefault() {} });
  console.log('after free: msg cleared =', a.q('#message').textContent === '');
  // export
  a.q('#export').onclick();
  console.log('export: clicks', clicks, '| msg', a.q('#message').textContent, '| revoke pending', a.timers.length, 'revokes', revokes);
  a.timers.forEach((f) => f()); console.log('after 10s: revokes', revokes);
  let e = boot(undefined); e.q('#export').onclick(); console.log('export empty: msg', e.q('#message').textContent, '| clicks still', clicks);
  // import over broken data, 2 added unsaved
  let b = boot(LB + 'hỏng');
  b.q('#title').value = 'A'; b.q('#add').onsubmit({ preventDefault() {} });
  b.q('#title').value = 'B'; b.q('#add').onsubmit({ preventDefault() {} });
  answer = 'no'; b.q('#import').files = [file(list(30))];
  await b.q('#import').onchange({ target: b.q('#import') });
  console.log('broken+cancel: question', b.q('#confirm-text').textContent, '| shown', b.q('#list').children.length, '| stored', b.data.get('todo.v1'), '| banner', !b.q('#unreadable').hidden, '| msg', JSON.stringify(b.q('#message').textContent));
  answer = 'yes'; b.q('#import').files = [file(list(30))];
  await b.q('#import').onchange({ target: b.q('#import') });
  console.log('broken+agree: shown', b.q('#list').children.length, '| stored count', JSON.parse(b.data.get('todo.v1')).length, '| banner', !b.q('#unreadable').hidden, '| msg', b.q('#message').textContent, '| input.value', JSON.stringify(b.q('#import').value));
  b.q('#title').value = 'C'; b.q('#add').onsubmit({ preventDefault() {} });
  console.log('then add: stored count', JSON.parse(b.data.get('todo.v1')).length);
  // broken + storage full + agree
  let c = boot(LB + 'hỏng'); c.ls.full = true; c.q('#import').files = [file(list(30))];
  await c.q('#import').onchange({ target: c.q('#import') });
  console.log('broken+full+agree: shown', c.q('#list').children.length, '| stored', c.data.get('todo.v1'), '| banner', !c.q('#unreadable').hidden, '| msg', c.q('#message').textContent);
})();
"
40. Bash · command=S=<thư-mục-tạm> && rm -rf "$S" && mkdir -p "$S" && git archive HEAD app | tar -x -C "$S" && mkdir -p "$S/tests" && cp app/backup.js "$S/app/" && cp tests/backup.test.js "$S/tests/" && cd "$S" && node --test 2>&1 | grep -E "^(✖|ℹ (tests|pass|fail))" && git -C <repo> diff --quiet HEAD -- app/index.html; echo "index.html differs from HEAD: $?"
41. Bash · command=S=<thư-mục-tạm> R=<repo>; rm -rf "$S"; mkdir -p "$S/tests"; git -C "$R" archive HEAD app | tar -x -C "$S"; cp "$R/app/backup.js" "$S/app/"; cp "$R/tests/backup.test.js" "$S/tests/"; node --test "$S/tests/" 2>&1 | grep -E "^(✖|ℹ (tests|pass|fail))"; grep -c backup.js "$S/app/index.html"
42. Bash · command=node --test tests/backup.test.js 2>&1 | grep -E "^(✖|ℹ (tests|pass|fail))"; git show HEAD:app/index.html | grep -c "backup.js"
43. Bash · command=node --test 2>&1 | tail -8 && git status --short

## Claude · 441 s

Both parts are written and `node --test` passes: 35 out of 35. Nothing is committed and I didn't touch the plan. Before you commit, Khoa or Mai and Linh need to settle M12: as written it doesn't meet the accepted spec.

**Commit A** is `app/backup.js` and `tests/backup.test.js`. Run on their own, those tests pass 21 out of 21. The current `index.html` doesn't load `backup.js`, so the app behaves exactly as before. Add only `tests/backup.test.js` to this commit, not the whole `tests/` folder: `tests/store.test.js` needs commit B's `store.js`, so it would fail in commit A.

**Commit B** is `app/store.js`, `app/app.js`, `app/index.html`, `app/style.css`, `tests/store.test.js` and `tests/static.test.js`. I re-ran the search for code that reads or writes storage (step B.1), and it matches the plan's 2026-10-27 result.

The `verifier` subagent loaded the real `app.js` in Node with a stand-in page and checked the two riskiest flows:
- **List saved by today's version, 3 and 2,000 tasks:** the app opens with every task and no warning banner, and adding, ticking and deleting are saved.
- **Unreadable saved list (`{hỏng`, `{"a": 1}`, `"null"`):** the banner shows and the empty-list line doesn't. Nothing is ever written and the stored value stays unchanged. Importing a file with "Thay" ends the banner, and the next change is saved.

A browser has not run anything yet. That means T0, then T1–T13 on desktop, Safari iOS and Chrome Android, and Khoa's condition 4: a second person reviews the commit B diff.

**Where the plan doesn't match the spec, or the code doesn't match the plan:**
1. **M12 fails the accepted spec.** Linh removed the part about clearing browser data. AC23 and F4 step 1 both require the line to say the list is lost when browser data is cleared, and P4 requires saying "what happens when they clear it". I used Linh's wording as the plan has it. `tests/static.test.js` and T11 check for M12's exact text, so they will pass while AC23 fails. In her answer (R2e), Linh said Khoa or Mai should propose other wording if they want that idea kept. A fix is one line in `app/index.html` plus the matching line in `tests/static.test.js`.
2. **One Proof row is labelled wrong:** "`createdAt: NaN` → M10". `NaN` isn't valid in a backup file, so the whole file fails to read and the message is M9 ("not a backup file"); the test expects that. I covered the "not a finite number" case for M10 with `1e999`, which reads as Infinity.
3. **The warning banner sits inside the `role="status"` area,** next to the message line; the plan lists them as separate parts. This follows the spec ("kể cả dải báo F5, trong vùng role=status"). T12 should check that screen readers read it at the right time.
4. **Two small additions in `app.js`:**
   - The list is replaced only when an import actually succeeds. That way, deleting a task while a file is being read can't bring the deleted task back on screen.
   - The file input has no file-type filter. That keeps AC9 testable by hand (picking an image or text file), and iOS can grey out `.json` files when a filter is set.
5. **Backup file name:** Linh's Q7 answer also suggested `sao-luu-viec-<date>.json`. That differs from the spec's `todo-sao-luu-<YYYY-MM-DD>.json`, which A11 settled with Linh and Thảo, and the plan didn't adopt it. I kept the spec's name.

When you commit, fill in each commit's "Tiến độ" (progress) entry in the plan, and the manual checklist for commit B. The pre-commit hook needs the plan file in both commits, and the hook won't let me edit it now that it's accepted.
