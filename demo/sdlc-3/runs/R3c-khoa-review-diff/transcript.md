# R3c-khoa-review-diff

Chạy 2026-10-27 11:09 ở `persona-empty` (thư mục riêng của lượt này), chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Bạn là Khoa, tech lead. Lúc duyệt plan bạn đặt điều kiện 4: "người khác review diff commit B trước khi commit". Đây là lượt review đó.
Bạn có: (a) diff chưa commit của thay đổi sao lưu / nhập lại (code do Claude viết theo plan đã accepted), (b) báo cáo của subagent verifier (chỉ chạy test và đọc, không sửa).
Việc của bạn:
1) Review diff: lỗi thật (file, dòng, vì sao), chỗ đáng sửa nhưng không chặn, và chỗ ổn. Không khen chung chung.
2) Quyết từng mục "Does not match plan.md" của verifier: chấp nhận lệch (ghi vào Tiến độ của plan) hay bắt sửa code.
3) Kết luận: cho commit (A rồi B) / cho commit kèm điều kiện / chưa cho. Nhắc rằng T0 và bảng kiểm tay vẫn do người làm trên trình duyệt thật.
Trả lời ngắn, có đánh số.

--- BÁO CÁO VERIFIER ---
I found no code defects and all 35 tests pass. The change departs from plan.md in three places, and I could not run the page wiring in `app/app.js` at all, so adding, toggling and deleting a todo through the page are unchecked.

**Ran:**
- `node --test`: 35 tests, 35 pass, 0 fail, 0 skipped. The tests are in `tests/backup.test.js`, `tests/store.test.js` and `tests/static.test.js`.
- `node --check` on all three `app/*.js` files and all three test files: all clean.
- The plan's step B.1 search for code that reads or writes the saved list (`store\.(load|save|replace)|localStorage`, leaving out `demo/`, `docs/`, `tests/` and the plan, spec and intent folders): only `app/store.js` touches browser storage. `app/app.js:3` calls `store.load()` and `app/backup.js` calls `store.save` (line 102) and `store.replace` (line 120). Nothing else calls `store`, which matches the plan's grep from 2026-10-27.
- `git status`, `git diff` and `git log` on `app/`, `tests/` and `plan/`.
- I wrote a small fake-page script (scratchpad, not the repo) to load `store.js`, `backup.js` and `app.js` together in Node. The command was blocked four times ("brace with quote character"), so it never ran. I did not try to get around the block.

**Saw:**
- **Loading the saved list:** a list saved by today's version (3 and 2,000 todos) loads with no error and the next save writes once. No saved key is a normal empty list, and so is a saved `[]`. `{hỏng`, `{"a": 1}`, `"null"`, `"chữ"`, `42`, and storage that throws on read all count as "cannot read".
- **Not overwriting an unreadable list:** saving after a read error is skipped and nothing is written. The broken value stays and no new key appears.
- **Save fails (storage full):** reported as `failed` and the old value is unchanged. The not-saved message appears only on `failed`.
- **Import:**
  - Files over 1,048,576 bytes are refused before being read; a file of exactly that size is read.
  - A bad file is refused without asking or writing, even in the "cannot read" state.
  - Importing into an empty list does not ask.
  - With 12 todos, the question matches the spec word for word. Cancel writes nothing; agree replaces once.
  - A failed write keeps the old list and shows the not-saved message.
  - In the "cannot read" state, import writes only through `replace`, never `save`.
  - A successful `replace` ends the "cannot read" state.
- **Backup file:** it is indented and holds only the four todo fields, even when a todo in memory has an extra field. The file name uses local time (00:30 is checked). Backing up and importing again gives back the same list, including emoji, Vietnamese accents and HTML in titles.
- **Adding, toggling and deleting a todo through the page:** not exercised, because my script was blocked. From reading the code: each action still goes through `commit()` → `persist(store, todos)` → `show` → `render`, titles still use `textContent`, and the empty-list line is driven by the whole list rather than the active filter, as the plan says.

**Does not match plan.md:**
1. **Order of work (plan lines 133–143):** Commit A (`app/backup.js` and `tests/backup.test.js`) was meant to be committed before any Commit B work. Neither is committed: A and B sit together in the working tree, and the Commit A progress line (plan line 247) is blank. Whoever commits has to split them into the two planned commits, or the plan has to be updated.
2. **Proof row for `parseBackup` (plan line 202):** the plan says `createdAt: NaN` is refused with the bad-todo message (M10). `tests/backup.test.js:78` expects the not-a-backup message (M9) instead, because `NaN` is not valid in a JSON file and the file fails to parse first. A value that is not a finite number is still refused with M10 via `1e999`, which reads as Infinity (lines 99 and 104). The behaviour is reasonable, but the plan row cannot happen as written.
3. **Where the "where your list is kept" sentence (M12) lives:** the plan's wording section (line 106) says every sentence is in `MESSAGES` in `backup.js` except labels in `index.html`. M12 is a full sentence, but it is written straight into `app/index.html:32`. The plan's file table (line 49) does put it in `index.html`, so the plan contradicts itself; the code follows the file table.
4. **No test for the warning banner on the page (spec criteria 15–17):** the store tests check the "cannot read" flag. No test checks that `render()` in `app/app.js:53-55` shows the banner and hides the empty-list line. The plan sends this to manual checks T9 and T10, so it is a gap in automated proof, not a broken promise.
5. **Plan file not touched:** `plan/2026-10-19-khach-khong-mat-viec.md` has no changes yet. The git pre-commit hook will refuse an `app/` commit without it, so the committer must fill in the progress section and the manual-check table.

Everything else matches the plan. That covers the file list (with `backup.js` approved under Q2), the store design, the import order of steps, the backup steps (no download when empty, release the download link after 10 seconds, too-big message instead of the count), the script order, and the dialog wiring. Every other proof row has a matching test.

**Not checked (needs a browser or a person):**
- The page wiring in `app/app.js`: add, toggle, delete, filters, the warning banner and the empty-list line, and the "reading file" message (M15). My Node script was blocked, so none of this ran.
- **T0 (plan's condition 3) has not been run:** opening real data from today's version, including 2,000 todos, in a real browser.
- The real download and file name, and Safari iOS with the 10-second delay.
- The file picker, picking the same file twice, and the `<dialog>` (Esc, focus, "Thay" and "Huỷ").
- How the banner, message area and hidden file input look.
- Screen reader announcements and keyboard-only use (T12).
- Network silence (T2), real storage-full behaviour (T8, T10), and HTTPS on phones.
- The whole manual table T0–T13 on the three browsers.
- **Plan condition 4 is still open:** someone other than the author must review the Commit B diff before it is committed.

Files involved: `<repo>/plan/2026-10-19-khach-khong-mat-viec.md`, `<repo>/spec/2026-10-19-khach-khong-mat-viec.md`, `<repo>/app/app.js`, `<repo>/app/backup.js`, `<repo>/app/store.js`, `<repo>/app/index.html`, `<repo>/app/style.css`, `<repo>/tests/backup.test.js`, `<repo>/tests/store.test.js`, `<repo>/tests/static.test.js`.

--- DIFF (git diff + file mới) ---
diff --git a/app/app.js b/app/app.js
index 5068eab..e10d836 100644
--- a/app/app.js
+++ b/app/app.js
@@ -1,5 +1,6 @@
 // A todo has: id, title, done, createdAt. No due date, no tags, no owner.
-let todos = store.load();
+// Saving and importing decisions live in backup.js (persist, importBackup); this file only wires them to the page.
+let todos = store.load().todos;
 let filter = 'all';
 
 const $ = (sel) => document.querySelector(sel);
@@ -21,10 +22,14 @@ function remove(id) {
 }
 
 function commit() {
-  store.save(todos);
+  show(persist(store, todos).message);
   render();
 }
 
+function show(message) {
+  $('#message').textContent = message || '';
+}
+
 function visible() {
   if (filter === 'open') return todos.filter((t) => !t.done);
   if (filter === 'done') return todos.filter((t) => t.done);
@@ -45,6 +50,20 @@ function render() {
   }
   const open = todos.filter((t) => !t.done).length;
   $('#count').textContent = `${open} việc chưa xong`;
+  $('#unreadable').hidden = !store.readError;
+  // Based on the whole list, not the filter; and not shown on a read error, where the list only looks empty.
+  $('#empty').hidden = todos.length > 0 || store.readError;
+}
+
+// Resolves true only when the customer picks "Thay"; Esc and "Huỷ" resolve false.
+function ask(question) {
+  const dialog = $('#confirm');
+  $('#confirm-text').textContent = question;
+  dialog.returnValue = '';
+  dialog.showModal();
+  return new Promise((resolve) => {
+    dialog.addEventListener('close', () => resolve(dialog.returnValue === 'yes'), { once: true });
+  });
 }
 
 $('#add').onsubmit = (e) => {
@@ -62,4 +81,34 @@ $('#filters').onclick = (e) => {
   render();
 };
 
+$('#export').onclick = () => {
+  if (todos.length === 0) return show(MESSAGES.nothingToBackUp);
+  const text = toBackupText(todos);
+  const url = URL.createObjectURL(new Blob([text], { type: 'application/json' }));
+  const a = document.createElement('a');
+  a.href = url;
+  a.download = backupFileName(new Date());
+  document.body.append(a);
+  a.click();
+  a.remove();
+  // Revoking right after click() can break the download on Safari iOS, so wait.
+  setTimeout(() => URL.revokeObjectURL(url), 10000);
+  show(tooBigToImport(text) ? MESSAGES.backupTooBig : fill(MESSAGES.backedUp, { n: todos.length }));
+};
+
+$('#import').onchange = async (e) => {
+  const input = e.target;
+  const file = input.files[0];
+  input.value = ''; // so the same file can be picked again
+  if (!file) return;
+  show(MESSAGES.reading);
+  const current = todos;
+  const result = await importBackup({ store, current, file, ask });
+  if (result.todos !== current) todos = result.todos;
+  show(result.message);
+  render();
+};
+
+$('#unreadable').textContent = MESSAGES.unreadable;
+$('#empty').textContent = MESSAGES.emptyList;
 render();
diff --git a/app/index.html b/app/index.html
index 1e06321..4789169 100644
--- a/app/index.html
+++ b/app/index.html
@@ -9,6 +9,10 @@
 <body>
   <main>
     <h1>Todo</h1>
+    <div id="notices" role="status" aria-live="polite">
+      <p id="unreadable" class="banner" hidden></p>
+      <p id="message"></p>
+    </div>
     <form id="add">
       <input id="title" placeholder="Việc cần làm…" autocomplete="off" required>
       <button>Thêm</button>
@@ -19,9 +23,23 @@
       <button data-filter="done">Đã xong</button>
     </nav>
     <ul id="list"></ul>
+    <p id="empty" hidden></p>
     <p id="count"></p>
+    <div id="backup">
+      <button type="button" id="export">Sao lưu ra file</button>
+      <label id="import-label">Nhập từ file<input type="file" id="import"></label>
+    </div>
+    <p id="where-kept" class="note">Danh sách chỉ được lưu trên trình duyệt này. Đổi trình duyệt hoặc đổi máy là mất danh sách, trừ khi bạn đã sao lưu ra file.</p>
   </main>
+  <dialog id="confirm" aria-labelledby="confirm-text">
+    <form method="dialog">
+      <p id="confirm-text"></p>
+      <button value="yes">Thay</button>
+      <button value="no" autofocus>Huỷ</button>
+    </form>
+  </dialog>
   <script src="store.js"></script>
+  <script src="backup.js"></script>
   <script src="app.js"></script>
 </body>
 </html>
diff --git a/app/store.js b/app/store.js
index 7ce1963..dc71455 100644
--- a/app/store.js
+++ b/app/store.js
@@ -3,19 +3,44 @@
 const STORE_KEY = 'todo.v1';
 
 const store = {
+  // True when todo.v1 holds something that cannot be read as a list. Kept in page memory only. While it is true, save()
+  // never writes, so the unreadable data is not overwritten; only replace() (import, after the customer agreed) may.
+  readError: false,
+
+  // No key yet is an ordinary empty list. Unparsable data, data that is not an array, or storage that throws is a read error.
   load() {
+    let todos = null;
     try {
-      return JSON.parse(localStorage.getItem(STORE_KEY)) || [];
+      const raw = localStorage.getItem(STORE_KEY);
+      todos = raw === null ? [] : JSON.parse(raw);
     } catch {
-      return [];
+      todos = null;
     }
+    store.readError = !Array.isArray(todos);
+    return { todos: store.readError ? [] : todos, readError: store.readError };
   },
+
+  // 'saved' | 'failed' (for example storage full, about 5 MB in most browsers) | 'skipped' (read error, nothing written).
   save(todos) {
-    // localStorage is capped per origin (about 5 MB in most browsers). A failed write is only logged.
-    try {
-      localStorage.setItem(STORE_KEY, JSON.stringify(todos));
-    } catch (err) {
-      console.error('save failed', err);
-    }
+    if (store.readError) return 'skipped';
+    return writeList(todos);
+  },
+
+  // The import path: writes even after a read error, and clears it only when the write succeeds.
+  replace(todos) {
+    const result = writeList(todos);
+    if (result === 'saved') store.readError = false;
+    return result;
   },
 };
+
+function writeList(todos) {
+  try {
+    localStorage.setItem(STORE_KEY, JSON.stringify(todos));
+    return 'saved';
+  } catch {
+    return 'failed';
+  }
+}
+
+if (typeof module !== 'undefined') module.exports = { store, STORE_KEY };
diff --git a/app/style.css b/app/style.css
index 01530bd..3cd635a 100644
--- a/app/style.css
+++ b/app/style.css
@@ -7,3 +7,16 @@ nav button.on { font-weight: 700; }
 ul { list-style: none; padding: 0; }
 li { display: flex; justify-content: space-between; padding: .4rem 0; border-bottom: 1px solid #ddd; }
 li.done span { text-decoration: line-through; color: #888; }
+.banner { background: #fff4e5; border: 1px solid #d08a2a; border-radius: 4px; padding: .6rem .8rem; }
+#message { background: #eaf1fb; border-radius: 4px; padding: .5rem .8rem; }
+#message:empty { display: none; }
+#empty, .note { color: #555; }
+.note { font-size: .875rem; }
+#backup { display: flex; gap: .5rem; align-items: center; margin: 1rem 0 .25rem; }
+#import-label { position: relative; border: 1px solid #767676; border-radius: 3px; background: #efefef; padding: 1px 6px; cursor: pointer; }
+#import-label:focus-within { outline: 2px solid #1a5fd0; outline-offset: 2px; }
+/* The file input stays focusable and clickable through its label; only its own button is hidden. */
+#import { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer; }
+dialog { border: 1px solid #bbb; border-radius: 6px; max-width: 24rem; }
+dialog form { flex-wrap: wrap; justify-content: flex-end; }
+dialog p { flex-basis: 100%; margin-top: 0; }
=== new file: app/backup.js
     1	// Backup to a file and import it back. No DOM and no browser storage here: storage goes through the `store` passed in,
     2	// so this file can be tested in Node. A backup file is { version: 1, todos: [{ id, title, done, createdAt }] }.
     3	const MAX_IMPORT_BYTES = 1048576; // 1 MiB, policy-security#S1. Also the size above which a backup cannot be imported back.
     4	
     5	const MESSAGES = {
     6	  nothingToBackUp: 'Chưa có việc nào để sao lưu.',
     7	  backupTooBig: 'File sao lưu đã lưu, nhưng quá lớn nên app không nhập lại được.',
     8	  notSaved: 'Thay đổi vừa rồi chưa được lưu. Hãy sao lưu ra file, rồi xoá bớt việc đã xong.',
     9	  backedUp: 'Đã sao lưu {n} việc.',
    10	  imported: 'Đã nhập {n} việc.',
    11	  confirmReplace: 'Thay {n} việc hiện có bằng {m} việc trong file?',
    12	  confirmReplaceUnreadable: 'Thay danh sách đã lưu không đọc được bằng {m} việc trong file?',
    13	  confirmReplaceUnreadableAndUnsaved:
    14	    'Thay danh sách đã lưu không đọc được và {n} việc bạn vừa thêm (chưa lưu) bằng {m} việc trong file?',
    15	  emptyFile: 'File này không có việc nào, nên chưa nhập được.',
    16	  notBackup: 'File này không phải file sao lưu của app, nên chưa nhập được. Danh sách của bạn vẫn giữ nguyên.',
    17	  badTodo: 'File sao lưu có việc bị lỗi, nên chưa nhập được việc nào. Danh sách của bạn vẫn giữ nguyên.',
    18	  fileTooBig: 'File này quá lớn, nên chưa nhập được. Danh sách của bạn vẫn giữ nguyên.',
    19	  emptyList: 'Chưa có việc nào. Nếu có file sao lưu, hãy bấm "Nhập từ file".',
    20	  cannotReadFile: 'Không đọc được file này. Hãy chọn lại file.',
    21	  reading: 'Đang đọc file…',
    22	  unreadable:
    23	    'Không đọc được danh sách đã lưu trên trình duyệt này. Việc bạn thêm hoặc sửa lúc này sẽ không được lưu. ' +
    24	    'Nếu có file sao lưu, hãy bấm "Nhập từ file".',
    25	};
    26	
    27	const TODO_KEYS = ['id', 'title', 'done', 'createdAt'];
    28	const FILE_KEYS = ['version', 'todos'];
    29	
    30	function fill(template, values) {
    31	  return template.replace(/\{(\w+)\}/g, (_, k) => String(values[k]));
    32	}
    33	
    34	function pick(t) {
    35	  return { id: t.id, title: t.title, done: t.done, createdAt: t.createdAt };
    36	}
    37	
    38	function isObject(v) {
    39	  return v !== null && typeof v === 'object' && !Array.isArray(v);
    40	}
    41	
    42	function hasExactKeys(o, keys) {
    43	  const own = Object.keys(o);
    44	  return own.length === keys.length && keys.every((k) => Object.prototype.hasOwnProperty.call(o, k));
    45	}
    46	
    47	function isValidTodo(t) {
    48	  return (
    49	    isObject(t) &&
    50	    hasExactKeys(t, TODO_KEYS) &&
    51	    typeof t.id === 'string' && t.id !== '' &&
    52	    typeof t.title === 'string' && t.title.trim() !== '' &&
    53	    typeof t.done === 'boolean' &&
    54	    typeof t.createdAt === 'number' && Number.isFinite(t.createdAt)
    55	  );
    56	}
    57	
    58	function toBackupText(todos) {
    59	  return JSON.stringify({ version: 1, todos: todos.map(pick) }, null, 2);
    60	}
    61	
    62	// The customer's own day (local time), not UTC.
    63	function backupFileName(date) {
    64	  const pad = (n) => String(n).padStart(2, '0');
    65	  return `todo-sao-luu-${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}.json`;
    66	}
    67	
    68	function tooBigToImport(text) {
    69	  return new TextEncoder().encode(text).length > MAX_IMPORT_BYTES;
    70	}
    71	
    72	// Untrusted input: only JSON.parse, never evaluated. Rejects the whole file on any bad todo (no partial import).
    73	function parseBackup(text) {
    74	  let data;
    75	  try {
    76	    data = JSON.parse(text);
    77	  } catch {
    78	    return { ok: false, message: MESSAGES.notBackup };
    79	  }
    80	  if (!isObject(data) || !hasExactKeys(data, FILE_KEYS) || data.version !== 1 || !Array.isArray(data.todos)) {
    81	    return { ok: false, message: MESSAGES.notBackup };
    82	  }
    83	  if (data.todos.length === 0) return { ok: false, message: MESSAGES.emptyFile };
    84	  const ids = new Set();
    85	  for (const t of data.todos) {
    86	    if (!isValidTodo(t) || ids.has(t.id)) return { ok: false, message: MESSAGES.badTodo };
    87	    ids.add(t.id);
    88	  }
    89	  return { ok: true, todos: data.todos.map(pick) };
    90	}
    91	
    92	// null when nothing would be lost (empty list, saved list readable), so no confirmation is needed.
    93	function confirmText({ readError, current, incoming }) {
    94	  if (readError && current === 0) return fill(MESSAGES.confirmReplaceUnreadable, { m: incoming });
    95	  if (readError) return fill(MESSAGES.confirmReplaceUnreadableAndUnsaved, { n: current, m: incoming });
    96	  if (current === 0) return null;
    97	  return fill(MESSAGES.confirmReplace, { n: current, m: incoming });
    98	}
    99	
   100	// After add, toggle or remove. 'skipped' (saved list unreadable) shows nothing extra: the banner already says so.
   101	function persist(store, todos) {
   102	  return { message: store.save(todos) === 'failed' ? MESSAGES.notSaved : null };
   103	}
   104	
   105	// Returns the list to show and the message. Every path except a successful replace returns `current` unchanged.
   106	// Writes only through store.replace, never store.save, so an unreadable saved list is replaced only here.
   107	async function importBackup({ store, current, file, ask }) {
   108	  const keep = (message) => ({ todos: current, message });
   109	  if (file.size > MAX_IMPORT_BYTES) return keep(MESSAGES.fileTooBig);
   110	  let text;
   111	  try {
   112	    text = await file.text();
   113	  } catch {
   114	    return keep(MESSAGES.cannotReadFile);
   115	  }
   116	  const parsed = parseBackup(text);
   117	  if (!parsed.ok) return keep(parsed.message);
   118	  const question = confirmText({ readError: store.readError, current: current.length, incoming: parsed.todos.length });
   119	  if (question !== null && !(await ask(question))) return keep(null);
   120	  if (store.replace(parsed.todos) !== 'saved') return keep(MESSAGES.notSaved);
   121	  return { todos: parsed.todos, message: fill(MESSAGES.imported, { n: parsed.todos.length }) };
   122	}
   123	
   124	if (typeof module !== 'undefined') {
   125	  module.exports = {
   126	    MAX_IMPORT_BYTES, MESSAGES, fill, toBackupText, backupFileName, tooBigToImport, parseBackup, confirmText, persist,
   127	    importBackup,
   128	  };
   129	}
=== new file: tests/backup.test.js
     1	// Tests for app/backup.js (plan/2026-10-19-khach-khong-mat-viec.md, commit A). Run: node --test
     2	const test = require('node:test');
     3	const assert = require('node:assert/strict');
     4	const { randomUUID } = require('node:crypto');
     5	const {
     6	  MAX_IMPORT_BYTES, MESSAGES, fill, toBackupText, backupFileName, tooBigToImport, parseBackup, confirmText, persist,
     7	  importBackup,
     8	} = require('../app/backup.js');
     9	
    10	const todo = (title, extra = {}) => ({ id: randomUUID(), title, done: false, createdAt: Date.now(), ...extra });
    11	const list = (n) => Array.from({ length: n }, (_, i) => todo(`Việc ${i + 1}`));
    12	const fileOf = (todos) => JSON.stringify({ version: 1, todos });
    13	
    14	function fakeStore({ readError = false, saveResult = 'saved', replaceResult = 'saved' } = {}) {
    15	  const calls = { save: [], replace: [] };
    16	  return {
    17	    readError,
    18	    calls,
    19	    save(t) { calls.save.push(t); return saveResult; },
    20	    replace(t) { calls.replace.push(t); return replaceResult; },
    21	  };
    22	}
    23	
    24	function fakeFile(text, size = Buffer.byteLength(text)) {
    25	  const file = { size, reads: 0, async text() { file.reads++; return text; } };
    26	  return file;
    27	}
    28	
    29	function fakeAsk(answer) {
    30	  const ask = async (q) => { ask.questions.push(q); return answer; };
    31	  ask.questions = [];
    32	  return ask;
    33	}
    34	
    35	// --- Backup file (AC1, P2, P3) ---
    36	
    37	test('toBackupText: indented, version 1, only the four todo fields', () => {
    38	  const todos = [todo('Mua sữa'), todo('Gọi mẹ', { done: true }), todo('Nộp thuế')];
    39	  todos[0].x = 1; // a stray field in memory must not reach the file
    40	  const text = toBackupText(todos);
    41	  assert.match(text, /\n  "version": 1/);
    42	  const data = JSON.parse(text);
    43	  assert.deepEqual(Object.keys(data), ['version', 'todos']);
    44	  assert.deepEqual(data.todos.map((t) => t.title), ['Mua sữa', 'Gọi mẹ', 'Nộp thuế']);
    45	  assert.deepEqual(data.todos.map((t) => t.done), [false, true, false]);
    46	  for (const t of data.todos) assert.deepEqual(Object.keys(t), ['id', 'title', 'done', 'createdAt']);
    47	});
    48	
    49	test('backupFileName uses the local date, including just after midnight (A11)', () => {
    50	  assert.equal(backupFileName(new Date(2026, 9, 27, 0, 30)), 'todo-sao-luu-2026-10-27.json');
    51	  assert.equal(backupFileName(new Date(2026, 0, 5, 23, 59)), 'todo-sao-luu-2026-01-05.json');
    52	});
    53	
    54	test('tooBigToImport counts bytes, with the boundary at 1,048,576 (Q3)', () => {
    55	  assert.equal(MAX_IMPORT_BYTES, 1048576);
    56	  assert.equal(tooBigToImport('a'.repeat(1048576)), false);
    57	  assert.equal(tooBigToImport('a'.repeat(1048577)), true);
    58	  assert.equal(tooBigToImport('ệ'.repeat(349526)), true); // 349,526 characters but 1,048,578 bytes
    59	});
    60	
    61	test('a backup of 5,000 todos with 200-character titles is too big to import (AC12)', () => {
    62	  const todos = Array.from({ length: 5000 }, () => todo('x'.repeat(200)));
    63	  assert.equal(tooBigToImport(toBackupText(todos)), true);
    64	});
    65	
    66	// --- Checking an imported file (AC8–AC11, Q4, S1) ---
    67	
    68	test('parseBackup accepts a valid file and keeps the todos as they are', () => {
    69	  const todos = [todo('Mua sữa'), todo('Gọi mẹ', { done: true })];
    70	  assert.deepEqual(parseBackup(fileOf(todos)), { ok: true, todos });
    71	});
    72	
    73	test('parseBackup rejects files that are not a backup (AC9)', () => {
    74	  const png = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0, 0, 0, 0x0d]).toString('utf8');
    75	  const cases = [png, 'Danh sách đi chợ: rau, thịt', '', 'null', '[]', '42', JSON.stringify([todo('a')]),
    76	    JSON.stringify({ version: 2, todos: [todo('a')] }), JSON.stringify({ version: 1 }),
    77	    JSON.stringify({ version: 1, todos: {} }), JSON.stringify({ version: 1, todos: [todo('a')], x: 1 }),
    78	    '{"version": 1, "todos": [{"id": "a", "title": "b", "done": false, "createdAt": NaN}]}'];
    79	  for (const text of cases) assert.deepEqual(parseBackup(text), { ok: false, message: MESSAGES.notBackup }, text);
    80	});
    81	
    82	test('parseBackup rejects a file with no todos (Q4)', () => {
    83	  assert.deepEqual(parseBackup(fileOf([])), { ok: false, message: MESSAGES.emptyFile });
    84	});
    85	
    86	test('parseBackup rejects the whole file when one todo is bad (AC8, AC10)', () => {
    87	  const t = todo('Việc tốt');
    88	  const bad = {
    89	    'unknown field': { ...todo('a'), x: 1 },
    90	    'missing field': { id: 'z', title: 'a', done: false },
    91	    'proto key': JSON.parse('{"id": "p", "title": "a", "done": false, "createdAt": 1, "__proto__": {}}'),
    92	    'empty id': todo('a', { id: '' }),
    93	    'id not a string': todo('a', { id: 7 }),
    94	    'empty title': todo(''),
    95	    'blank title': todo('   '),
    96	    'title not a string': todo(5),
    97	    'done not boolean': todo('a', { done: 'true' }),
    98	    'createdAt is a word': todo('a', { createdAt: 'hôm qua' }),
    99	    'createdAt is infinite': null, // written as 1e999 below, which JSON.parse reads as Infinity
   100	    'not an object': 'việc',
   101	  };
   102	  for (const [name, b] of Object.entries(bad)) {
   103	    const text = b === null
   104	      ? `{"version": 1, "todos": [{"id": "i", "title": "a", "done": false, "createdAt": 1e999}]}`
   105	      : fileOf([t, b]);
   106	    assert.deepEqual(parseBackup(text), { ok: false, message: MESSAGES.badTodo }, name);
   107	  }
   108	  assert.deepEqual(parseBackup(fileOf([t, { ...todo('Khác'), id: t.id }])), { ok: false, message: MESSAGES.badTodo });
   109	});
   110	
   111	test('parseBackup keeps an HTML-looking title as plain text (AC11)', () => {
   112	  const t = todo('<img src=x onerror=alert(1)>');
   113	  assert.equal(parseBackup(fileOf([t])).todos[0].title, '<img src=x onerror=alert(1)>');
   114	});
   115	
   116	test('every list the app can create survives backup then import unchanged', () => {
   117	  const todos = [
   118	    todo('Mua sữa'), todo('Đã xong', { done: true }), todo('Đi chợ 🛒 rồi về 🏠'), todo('Học tiếng Việt: ă â ê ô ơ ư đ'),
   119	    todo('<b>đậm</b> & "ngoặc" \'đơn\''), todo('a'), todo('x'.repeat(500)), todo('tab\tvà\nxuống dòng'),
   120	  ];
   121	  assert.deepEqual(parseBackup(toBackupText(todos)), { ok: true, todos });
   122	  assert.deepEqual(parseBackup(toBackupText(list(2000))).ok, true);
   123	});
   124	
   125	// --- Confirmation (AC5, AC6, AC19, AC20, S2) ---
   126	
   127	test('confirmText asks before replacing anything, and only then', () => {
   128	  assert.equal(confirmText({ readError: false, current: 12, incoming: 30 }), 'Thay 12 việc hiện có bằng 30 việc trong file?');
   129	  assert.equal(confirmText({ readError: false, current: 1, incoming: 30 }), 'Thay 1 việc hiện có bằng 30 việc trong file?');
   130	  assert.equal(confirmText({ readError: false, current: 0, incoming: 30 }), null);
   131	  assert.equal(confirmText({ readError: true, current: 0, incoming: 30 }),
   132	    'Thay danh sách đã lưu không đọc được bằng 30 việc trong file?');
   133	  assert.equal(confirmText({ readError: true, current: 3, incoming: 30 }),
   134	    'Thay danh sách đã lưu không đọc được và 3 việc bạn vừa thêm (chưa lưu) bằng 30 việc trong file?');
   135	});
   136	
   137	// --- Saving after add, toggle, remove (AC13, AC15, F3) ---
   138	
   139	test('persist shows the not-saved message only when the write failed', () => {
   140	  assert.deepEqual(persist(fakeStore({ saveResult: 'saved' }), []), { message: null });
   141	  assert.deepEqual(persist(fakeStore({ saveResult: 'failed' }), []), { message: MESSAGES.notSaved });
   142	  assert.deepEqual(persist(fakeStore({ saveResult: 'skipped' }), []), { message: null });
   143	});
   144	
   145	// --- Import flow ---
   146	
   147	test('importBackup rejects a file over the limit without reading it (AC7, AC22)', async () => {
   148	  const store = fakeStore();
   149	  const current = list(2);
   150	  const big = fakeFile(fileOf(list(1)), 1048577);
   151	  assert.deepEqual(await importBackup({ store, current, file: big, ask: fakeAsk(true) }),
   152	    { todos: current, message: MESSAGES.fileTooBig });
   153	  assert.equal(big.reads, 0);
   154	  assert.equal(store.calls.replace.length, 0);
   155	
   156	  const atLimit = fakeFile(fileOf(list(1)), 1048576);
   157	  await importBackup({ store, current: [], file: atLimit, ask: fakeAsk(true) });
   158	  assert.equal(atLimit.reads, 1);
   159	});
   160	
   161	test('importBackup keeps the list when the file cannot be read', async () => {
   162	  const store = fakeStore();
   163	  const current = list(2);
   164	  const file = { size: 10, async text() { throw new Error('NotReadableError'); } };
   165	  assert.deepEqual(await importBackup({ store, current, file, ask: fakeAsk(true) }),
   166	    { todos: current, message: MESSAGES.cannotReadFile });
   167	  assert.equal(store.calls.replace.length, 0);
   168	});
   169	
   170	test('importBackup rejects a bad file without asking or writing (AC8–AC10, AC22)', async () => {
   171	  for (const readError of [false, true]) {
   172	    const store = fakeStore({ readError });
   173	    const ask = fakeAsk(true);
   174	    const current = list(2);
   175	    const result = await importBackup({ store, current, file: fakeFile(fileOf([{ ...todo('a'), x: 1 }])), ask });
   176	    assert.deepEqual(result, { todos: current, message: MESSAGES.badTodo });
   177	    assert.equal(ask.questions.length, 0);
   178	    assert.equal(store.calls.replace.length, 0);
   179	  }
   180	});
   181	
   182	test('importBackup into an empty list does not ask (AC3)', async () => {
   183	  const store = fakeStore();
   184	  const ask = fakeAsk(false);
   185	  const incoming = list(3);
   186	  const result = await importBackup({ store, current: [], file: fakeFile(fileOf(incoming)), ask });
   187	  assert.deepEqual(result, { todos: incoming, message: 'Đã nhập 3 việc.' });
   188	  assert.equal(ask.questions.length, 0);
   189	  assert.deepEqual(store.calls.replace, [incoming]);
   190	});
   191	
   192	test('importBackup over 12 todos asks first; cancel writes nothing, agree replaces (AC5, AC6)', async () => {
   193	  const current = list(12);
   194	  const incoming = list(30);
   195	
   196	  const store1 = fakeStore();
   197	  const no = fakeAsk(false);
   198	  assert.deepEqual(await importBackup({ store: store1, current, file: fakeFile(fileOf(incoming)), ask: no }),
   199	    { todos: current, message: null });
   200	  assert.deepEqual(no.questions, ['Thay 12 việc hiện có bằng 30 việc trong file?']);
   201	  assert.equal(store1.calls.replace.length, 0);
   202	
   203	  const store2 = fakeStore();
   204	  const yes = fakeAsk(true);
   205	  assert.deepEqual(await importBackup({ store: store2, current, file: fakeFile(fileOf(incoming)), ask: yes }),
   206	    { todos: incoming, message: 'Đã nhập 30 việc.' });
   207	  assert.equal(store2.calls.replace.length, 1);
   208	});
   209	
   210	test('importBackup keeps the old list when the write fails (AC14, AC21, A20)', async () => {
   211	  for (const readError of [false, true]) {
   212	    const store = fakeStore({ readError, replaceResult: 'failed' });
   213	    const current = list(readError ? 0 : 12);
   214	    const result = await importBackup({ store, current, file: fakeFile(fileOf(list(30))), ask: fakeAsk(true) });
   215	    assert.deepEqual(result, { todos: current, message: MESSAGES.notSaved });
   216	  }
   217	});
   218	
   219	test('importBackup while the saved list is unreadable writes only through replace, never save (AC19–AC21)', async () => {
   220	  const store = fakeStore({ readError: true });
   221	  const ask = fakeAsk(true);
   222	  const incoming = list(30);
   223	  const result = await importBackup({ store, current: list(3), file: fakeFile(fileOf(incoming)), ask });
   224	  assert.deepEqual(ask.questions,
   225	    ['Thay danh sách đã lưu không đọc được và 3 việc bạn vừa thêm (chưa lưu) bằng 30 việc trong file?']);
   226	  assert.deepEqual(result.todos, incoming);
   227	  assert.equal(store.calls.save.length, 0);
   228	  assert.equal(store.calls.replace.length, 1);
   229	});
   230	
   231	// --- Wording (AC4, AC12, AC15, AC24, U4) ---
   232	
   233	test('messages quoted in the spec and plan are word for word', () => {
   234	  assert.equal(MESSAGES.nothingToBackUp, 'Chưa có việc nào để sao lưu.');
   235	  assert.equal(MESSAGES.backupTooBig, 'File sao lưu đã lưu, nhưng quá lớn nên app không nhập lại được.');
   236	  assert.match(MESSAGES.notSaved, /Hãy sao lưu ra file, rồi xoá bớt việc đã xong/);
   237	  assert.equal(MESSAGES.emptyFile, 'File này không có việc nào, nên chưa nhập được.');
   238	  assert.equal(MESSAGES.fileTooBig, 'File này quá lớn, nên chưa nhập được. Danh sách của bạn vẫn giữ nguyên.');
   239	  assert.equal(MESSAGES.unreadable,
   240	    'Không đọc được danh sách đã lưu trên trình duyệt này. Việc bạn thêm hoặc sửa lúc này sẽ không được lưu. ' +
   241	    'Nếu có file sao lưu, hãy bấm "Nhập từ file".');
   242	  assert.equal(fill(MESSAGES.backedUp, { n: 3 }), 'Đã sao lưu 3 việc.');
   243	});
   244	
   245	test('no message uses a technical word', () => {
   246	  for (const [key, text] of Object.entries(MESSAGES)) {
   247	    assert.doesNotMatch(text, /localStorage|JSON|console/i, key);
   248	  }
   249	});
=== new file: tests/static.test.js
     1	// Static checks on app/ files (plan/2026-10-19-khach-khong-mat-viec.md, commit B). Run: node --test
     2	const test = require('node:test');
     3	const assert = require('node:assert/strict');
     4	const fs = require('node:fs');
     5	const path = require('node:path');
     6	
     7	const read = (f) => fs.readFileSync(path.join(__dirname, '..', 'app', f), 'utf8');
     8	const html = read('index.html');
     9	
    10	test('scripts load in the order store, backup, app (Q2)', () => {
    11	  const scripts = [...html.matchAll(/<script\b[^>]*\bsrc="([^"]+)"/g)].map((m) => m[1]);
    12	  assert.deepEqual(scripts, ['store.js', 'backup.js', 'app.js']);
    13	});
    14	
    15	test('index.html loads nothing from outside (AC26, S4)', () => {
    16	  assert.doesNotMatch(html, /\b(src|href)\s*=\s*["']?\s*(https?:)?\/\//i);
    17	});
    18	
    19	test('only store.js touches browser storage', () => {
    20	  for (const f of ['app.js', 'backup.js']) assert.doesNotMatch(read(f), /localStorage/, f);
    21	});
    22	
    23	test('the main screen says where the list is kept, and has the new controls (AC23, U5)', () => {
    24	  assert.ok(html.includes(
    25	    'Danh sách chỉ được lưu trên trình duyệt này. Đổi trình duyệt hoặc đổi máy là mất danh sách, trừ khi bạn đã sao lưu ra file.'));
    26	  assert.ok(html.includes('>Sao lưu ra file</button>'));
    27	  assert.match(html, /<label[^>]*>Nhập từ file<input type="file"/);
    28	  assert.match(html, /role="status"/);
    29	  assert.match(html, /<dialog id="confirm" aria-labelledby="confirm-text">/);
    30	});
    31	
    32	test('visible text in index.html has no technical words (AC24, U4)', () => {
    33	  const text = html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<[^>]+>/g, ' ');
    34	  assert.doesNotMatch(text, /localStorage|JSON|console/i);
    35	});
=== new file: tests/store.test.js
     1	// Tests for app/store.js (plan/2026-10-19-khach-khong-mat-viec.md, commit B). Run: node --test
     2	// Browser storage is replaced by a fake that counts writes and can be told to throw.
     3	const test = require('node:test');
     4	const assert = require('node:assert/strict');
     5	const { randomUUID } = require('node:crypto');
     6	const { store, STORE_KEY } = require('../app/store.js');
     7	
     8	function fakeStorage(initial = {}) {
     9	  const data = new Map(Object.entries(initial));
    10	  const s = {
    11	    data,
    12	    sets: 0,
    13	    getThrows: false,
    14	    setThrows: false,
    15	    getItem(k) {
    16	      if (s.getThrows) throw new Error('SecurityError');
    17	      return data.has(k) ? data.get(k) : null;
    18	    },
    19	    setItem(k, v) {
    20	      s.sets++;
    21	      if (s.setThrows) {
    22	        const err = new Error('quota');
    23	        err.name = 'QuotaExceededError';
    24	        throw err;
    25	      }
    26	      data.set(k, String(v));
    27	    },
    28	  };
    29	  globalThis.localStorage = s;
    30	  return s;
    31	}
    32	
    33	// What the current version of the app writes: an array of { id, title, done, createdAt }.
    34	const oldVersionList = (n) =>
    35	  Array.from({ length: n }, (_, i) => ({ id: randomUUID(), title: `Việc ${i}`, done: i % 3 === 0, createdAt: Date.now() - i }));
    36	
    37	// --- Loading: no false alarm on good data (condition 3) ---
    38	
    39	test('no saved key is an ordinary empty list (AC3, A13)', () => {
    40	  fakeStorage();
    41	  assert.deepEqual(store.load(), { todos: [], readError: false });
    42	  assert.equal(store.readError, false);
    43	});
    44	
    45	test('a list saved by the current version loads, 3 and 2,000 todos, and saving still writes', () => {
    46	  for (const n of [3, 2000]) {
    47	    const todos = oldVersionList(n);
    48	    const s = fakeStorage({ [STORE_KEY]: JSON.stringify(todos) });
    49	    assert.deepEqual(store.load(), { todos, readError: false }, `${n} todos`);
    50	    assert.equal(store.save(todos), 'saved');
    51	    assert.equal(s.sets, 1);
    52	  }
    53	});
    54	
    55	test('a saved empty array is not a read error', () => {
    56	  fakeStorage({ [STORE_KEY]: '[]' });
    57	  assert.deepEqual(store.load(), { todos: [], readError: false });
    58	});
    59	
    60	// --- Loading: the three read-error cases (AC15–AC17, Q5) ---
    61	
    62	test('unparsable data, data that is not an array, and storage that throws are read errors', () => {
    63	  for (const raw of ['{hỏng', '{"a": 1}', 'null', '"chữ"', '42']) {
    64	    fakeStorage({ [STORE_KEY]: raw });
    65	    assert.deepEqual(store.load(), { todos: [], readError: true }, raw);
    66	  }
    67	  const s = fakeStorage({ [STORE_KEY]: '[]' });
    68	  s.getThrows = true;
    69	  assert.deepEqual(store.load(), { todos: [], readError: true });
    70	});
    71	
    72	test('after a read error, saving never writes and the unreadable value stays (AC15–AC17)', () => {
    73	  for (const raw of ['{hỏng', '{"a": 1}']) {
    74	    const s = fakeStorage({ [STORE_KEY]: raw });
    75	    store.load();
    76	    const todos = oldVersionList(2);
    77	    assert.equal(store.save(todos), 'skipped');
    78	    todos[0].done = true;
    79	    assert.equal(store.save(todos), 'skipped');
    80	    assert.equal(store.save(todos.slice(1)), 'skipped');
    81	    assert.equal(s.sets, 0);
    82	    assert.deepEqual([...s.data.keys()], [STORE_KEY]);
    83	    assert.equal(s.data.get(STORE_KEY), raw);
    84	  }
    85	  const s = fakeStorage();
    86	  s.getThrows = true;
    87	  store.load();
    88	  assert.equal(store.save(oldVersionList(1)), 'skipped');
    89	  assert.equal(s.sets, 0);
    90	});
    91	
    92	// --- Saving fails (AC13, AC14, AC21) ---
    93	
    94	test('a failed write is reported and leaves the old value (AC13)', () => {
    95	  const old = JSON.stringify(oldVersionList(12));
    96	  const s = fakeStorage({ [STORE_KEY]: old });
    97	  store.load();
    98	  s.setThrows = true;
    99	  assert.equal(store.save(oldVersionList(13)), 'failed');
   100	  assert.equal(s.data.get(STORE_KEY), old);
   101	});
   102	
   103	test('a failed replace keeps the old list; after a read error it keeps the error too (AC14, AC21)', () => {
   104	  const old = JSON.stringify(oldVersionList(12));
   105	  const s1 = fakeStorage({ [STORE_KEY]: old });
   106	  store.load();
   107	  s1.setThrows = true;
   108	  assert.equal(store.replace(oldVersionList(30)), 'failed');
   109	  assert.equal(s1.data.get(STORE_KEY), old);
   110	
   111	  const s2 = fakeStorage({ [STORE_KEY]: '{hỏng' });
   112	  store.load();
   113	  s2.setThrows = true;
   114	  assert.equal(store.replace(oldVersionList(30)), 'failed');
   115	  assert.equal(store.readError, true);
   116	  assert.equal(s2.data.get(STORE_KEY), '{hỏng');
   117	  s2.setThrows = false;
   118	  assert.equal(store.save(oldVersionList(1)), 'skipped');
   119	  assert.equal(s2.data.get(STORE_KEY), '{hỏng');
   120	});
   121	
   122	// --- Leaving the read-error state (AC19, AC20, A17) ---
   123	
   124	test('a successful replace ends the read error, and later saves are written', () => {
   125	  const s = fakeStorage({ [STORE_KEY]: '{hỏng' });
   126	  store.load();
   127	  const thirty = oldVersionList(30);
   128	  assert.equal(store.replace(thirty), 'saved');
   129	  assert.equal(store.readError, false);
   130	  const thirtyOne = [...thirty, ...oldVersionList(1)];
   131	  assert.equal(store.save(thirtyOne), 'saved');
   132	  assert.deepEqual(store.load(), { todos: thirtyOne, readError: false });
   133	  assert.equal(s.sets, 2);
   134	});
   135	
   136	// --- Today's flow ---
   137	
   138	test('save then load gives the same list', () => {
   139	  fakeStorage();
   140	  store.load();
   141	  const todos = oldVersionList(5);
   142	  assert.equal(store.save(todos), 'saved');
   143	  assert.deepEqual(store.load().todos, todos);
   144	});

## Tool call (0)

(không có)

## Claude · 65 s

**Review commit B (sao lưu / nhập lại)**

**1. Review diff**

*Lỗi thật hoặc nghi lỗi thật, cần xử lý trước khi commit B*
- `app/backup.js:47-56` (`isValidTodo`) có thể chặt hơn đoạn code tạo việc.
  - Nó từ chối `title` chỉ có dấu cách và `id` không phải chuỗi.
  - `<input required>` vẫn nhận "   ".
  - Nếu `add` trong `app/app.js` (ngoài diff) không trim và không từ chối tiêu đề trắng, hoặc `id` không phải chuỗi, thì khách tự sao lưu rồi không nhập lại được. Dữ liệu cũ từ bản trước cũng có thể dính.
  - Test "mọi danh sách app tạo ra đều quay lại nguyên vẹn" (`tests/backup.test.js:116`) chỉ dùng `randomUUID` và tiêu đề tử tế, nên chưa chứng minh được điều này.
  - Cách xử lý: đọc handler `add`. Nếu nó đã trim, từ chối tiêu đề trắng và sinh `id` chuỗi, thì thêm một test ghim điều đó. Nếu chưa, nới validator hoặc sửa `add`. Làm bước này trước.

*Đáng sửa, không chặn*
- `app/app.js:101-108` (`$('#import').onchange`) có một cửa sổ race nhỏ. Danh sách `current` được chụp trước `await`. Nếu khách thêm việc trong lúc đang đọc file và danh sách lúc chọn file đang trống, nhập thành công sẽ ghi đè việc mới mà không hỏi. Cửa sổ chỉ vài mili giây. Có thể sửa bằng cách chặn nhập khi `todos !== current` ở cuối, hoặc cứ ghi nhận.
- `app/style.css`: `dialog form { flex-wrap; justify-content }` chỉ có tác dụng nếu `form` đang là flex ở phần CSS không nằm trong diff. Nếu không, hai nút trong hộp thoại sẽ xếp trái. Đây là việc của Linh, kiểm lúc chạy tay.
- `MESSAGES.notSaved` ("Thay đổi vừa rồi chưa được lưu… xoá bớt việc đã xong") cũng hiện khi nhập hỏng. Lúc đó "thay đổi vừa rồi" hơi mơ hồ. Báo Linh, không sửa ở đây.

*Chỗ ổn, tôi có đối chiếu*
- `store.js`: "không có key" tách khỏi "đọc lỗi". `save` bỏ qua khi đọc lỗi. `replace` chỉ tắt `readError` khi ghi thành công. Cả lúc chạm `localStorage` cũng nằm trong `try`.
- `parseBackup`: `Object.keys` cộng khóa chính xác chặn được `__proto__`. Chỉ dùng `JSON.parse`. Từ chối cả file nếu một việc sai, trùng `id` cũng bị từ chối. `pick()` được áp dụng cả lúc ghi file lẫn lúc nhập.
- Giới hạn kích thước: kiểm `file.size` trước khi đọc. Dùng `TextEncoder` để đếm byte, nên mốc 1.048.576 khớp ở cả hai chiều.
- Các điểm phụ: tên file theo giờ địa phương, hoãn `revokeObjectURL` 10 giây cho Safari iOS, tiêu đề dùng `textContent`, `input.value = ''` để chọn lại cùng file, input file không có `accept`.

**2. Các mục "Does not match plan.md"**

1. **Thứ tự commit A rồi B:** bắt sửa quy trình, không phải code. Phải tách thành hai commit.
   - Commit A gồm `app/backup.js` và `tests/backup.test.js`. Chạy `node --test` riêng. File này chưa được `index.html` nạp nên không đổi hành vi.
   - Hook yêu cầu sửa plan cho mọi commit đụng `app/`, nên A cũng cần một dòng Tiến độ.
2. **`createdAt: NaN` bị từ chối bằng M9, không phải M10:** chấp nhận lệch. `NaN` không hợp lệ trong JSON nên file hỏng ngay ở bước parse. `1e999` vẫn chứng minh M10 (dòng 99 và 104). Ghi vào Tiến độ và sửa dòng 202 của plan.
3. **M12 nằm trong `index.html`:** chấp nhận lệch. Bảng file của plan đã nói vậy, câu ở dòng 106 mới sai. Có `static.test.js` ghim đúng từng chữ. Sửa dòng 106 của plan.
4. **Không có test tự động cho banner:** chấp nhận, vì plan đã giao cho T9 và T10. Ghi rõ đây là khoảng trống bằng chứng tự động.
5. **Plan chưa đụng:** đây là việc phải làm chứ không phải lệch.
   - Điền Tiến độ và ghi các lệch 2–4.
   - Để trống các ô T0–T13 cho tới khi có người chạy thật. Không tick giùm.

**3. Kết luận: cho commit kèm điều kiện**

Điều kiện:
- (a) Xử lý mục validator ở phần 1 trước khi commit B.
- (b) Tách A rồi B, mỗi commit đều xanh và đều có dòng plan.
- (c) Cập nhật plan theo mục 2.

Verifier không chạy được `app/app.js`, vì lệnh bị chặn bốn lần. Thêm, bật tắt và xoá việc trên trang chưa có bằng chứng nào ngoài việc đọc code. Việc này, T0 (dữ liệu thật từ bản hiện tại, kể cả 2.000 việc) và cả bảng T0–T13 vẫn phải do người làm trên trình duyệt thật, gồm Safari iOS và Chrome Android. Khi chạy T0, nên thêm một vòng sao lưu rồi nhập lại chính dữ liệu thật đó. Review của tôi không thay được các bước này.
