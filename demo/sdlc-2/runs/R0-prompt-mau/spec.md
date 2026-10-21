# Spec: Sao lưu và nhập lại danh sách việc, báo khi không lưu được

| | |
|---|---|
| Intent | `intent/2026-10-19-khach-khong-mat-viec.md` (Lan, status: accepted) |
| Spec date | 2026-10-20 |
| Policies applied | `policy-privacy@1`, `policy-security@1`, `policy-ux@1` |
| Budget | 1 developer, 2 weeks (from intent, product owner) |
| Code touched | `app/store.js`, `app/app.js`, `app/index.html`, `app/style.css` |
| Status | Ready for engineering, **except the 3 decisions marked BLOCKING in §9** |

---

## 1. Summary

The app keeps every task only in this browser's `localStorage`. When users clear browser data or move to a new phone, the list is gone. When storage is full, the write fails and only goes to the console.

The product owner set the scope for this release. It ships three things:

1. **Export.** The user downloads a backup file of their list.
2. **Import.** The user loads a backup file back into the app, on the same device or on a new one.
3. **Save-failure feedback.** When a save fails (storage full, storage blocked, corrupt data), the user sees it on the same screen, in plain words, and is told what to do next.

It also adds a short in-app notice about where the data is kept, which `policy-privacy@1#P4` requires, and a backup reminder so users actually have a file when they need one.

Sync between devices, accounts and servers are **out of scope** (product owner). See §9.1 for what that means for the intent's success criteria.

---

## 2. Scope

### In scope
| ID | Item |
|---|---|
| F1 | Export the full list to a backup file on an explicit user action |
| F2 | Import a backup file. Validated, merged without overwriting or deleting, with Undo |
| F3 | Detect every failed save and show it on screen with next steps |
| F4 | Detect unreadable stored data at startup without overwriting it silently |
| F5 | In-app notice about where data lives and what clearing it does |
| F6 | Backup reminder, computed on the device only |
| F7 | Empty / loading / error states for the list |
| F8 | *(Recommended, PO to confirm)* Undo for deleting a single task. Today it is deleted at once with no Undo, which breaks `policy-ux@1#U2` |

### Out of scope (from the intent)
- Recovering tasks for the 23 customers who already lost them. That data never left their devices.
- Multi-device sync, login accounts, shared lists.
- Due dates (T-012). §8.4 covers how the file format should leave room for them.
- Any server, cloud storage or analytics. Adding one would need privacy-owner sign-off (`P5`) and security-owner sign-off (`S4`).

---

## 3. Current state (findings from the code)

| # | Finding | Location | Policy impact |
|---|---|---|---|
| C1 | `store.save` catches every error and only calls `console.error`. The caller cannot tell that the save failed | `app/store.js:13-19` | Violates `U1` |
| C2 | `store.load` returns `[]` when parsing fails. The next `commit()` then **overwrites the unreadable data with the new list**, so the old list is destroyed silently | `app/store.js:6-11`, `app/app.js:23-26` | Violates `U1`. Silent data loss |
| C3 | Loaded data is never checked against the schema | `app/store.js:8` | Same risk class as `S1` |
| C4 | Deleting a task happens at once, with no Undo | `app/app.js:18-21,43` | Violates `U2` |
| C5 | No empty state. An empty list renders a blank `<ul>` and "0 việc chưa xong" | `app/app.js:34-48` | Violates `U3` |
| C6 | The row template uses `innerHTML`, but the title goes in through `textContent` | `app/app.js:40-41` | Meets `S3`. The template should still move to `createElement` so later edits cannot put user text in it by accident |
| C7 | The filter buttons have no `aria-pressed`. The delete button is labelled "Xoá" without saying which task | `app/index.html:16-20`, `app/app.js:40` | Weak on `U5` |
| C8 | Two open tabs overwrite each other's saves (last write wins) | `app/store.js` | Silent loss. Out of scope, noted in §9.6 |

---

## 4. Functional requirements

### F1 Export (Tải bản sao lưu)

- **F1.1** A button labelled **"Tải bản sao lưu"** sits in a new "Sao lưu" section below the list. It stays available when the list is empty, but the file is then empty, so the button is shown disabled with the hint "Chưa có việc nào để sao lưu".
- **F1.2** Export runs **only** when the user presses the button. No automatic or background export, and no upload anywhere (`P1`).
- **F1.3** Export builds the file from the **in-memory list**, not from storage. Export therefore still works when storage is full or broken, and in those cases it is the user's way out (see F3).
- **F1.4** File content follows §5. It holds only the four task fields the user's actions created, plus a format marker. No device ID, user agent, timestamp of export, locale or any other environment data (`P2`).
- **F1.5** The file is pretty-printed (2-space indent, one field per line, UTF-8, no BOM), so a user who opens it in a text editor can read every task (`P3`).
- **F1.6** File name: `todo-sao-luu-YYYY-MM-DD.json`, using the local date.
- **F1.7** Mechanism: `Blob` + `URL.createObjectURL` + a temporary `<a download>`, with the object URL revoked afterwards. No library (`S4`).
- **F1.8** After export, record `lastBackupAt` and `lastBackupCount` under the local key `todo.meta` (used by F6). This value stays on the device and is never exported.
- **F1.9** On success, show the status line "Đã tải bản sao lưu (12 việc). Hãy cất file này ở nơi an toàn, ví dụ gửi cho chính bạn." in an `aria-live="polite"` region.
- **F1.10** If the serialized file is larger than **1 MB**, the app could not import it back (S1 cap). Export still runs, so the user is never left without a copy, and the screen shows the warning in §9.4. *(Pending decision §9.4.)*

### F2 Import (Nhập bản sao lưu)

- **F2.1** A button labelled **"Nhập bản sao lưu"** in the "Sao lưu" section opens the system file picker through a hidden `<input type="file" accept=".json,application/json">`. The visible control is a real `<button>`. The input is not focusable on its own.
- **F2.2** **Size check first.** If `file.size > 1 048 576` bytes, reject the file **before reading it** (`S1`).
- **F2.3** Read with `file.text()`, parse with `JSON.parse` only. Never `eval`, `Function`, dynamic `import`, or inserting the content into the DOM as HTML (`S1`, `S3`).
- **F2.4** Validate against §5 with a strict validator (§6.2). **Any** violation rejects the **whole file**. Nothing is imported partially.
- **F2.5** **Merge, never overwrite.** For each task in the file:
  - if no task with that `id` exists locally, add it;
  - if a task with that `id` already exists locally, **keep the local one unchanged** and skip the file's copy.
  Import therefore never overwrites or deletes an existing task. §9.2 explains why this was chosen.
- **F2.6** Order after merge: existing tasks keep their order. New tasks are inserted by `createdAt` ascending, interleaved with the existing ones by `createdAt`. Ties go to the existing task first.
- **F2.7** Saving is atomic. The merged list is saved in one `store.save`. If that save fails, the in-memory list goes back to its state before the import, and the error from F3.4 is shown. A failed import never looks like it worked.
- **F2.8** On success, show a status line with **Undo** for 10 seconds (`U2`):
  - "Đã thêm 30 việc từ file. 4 việc đã có sẵn nên giữ nguyên." **[Hoàn tác]**
  - Undo puts back the exact pre-import list and saves it. If that save fails, F3 applies.
  - If the file adds 0 tasks: "File không có việc nào mới. Danh sách giữ nguyên." (no Undo).
- **F2.9** While the file is read and checked, show the loading state "Đang đọc file…" (F7). Disable both backup buttons, and set `aria-busy="true"` on the section.
- **F2.10** The file name is user-controlled text. Wherever it is shown, it goes in through `textContent` (`S3`).
- **F2.11** Rejection messages. Plain Vietnamese, with no technical words (`U4`), shown in the "Sao lưu" section with `role="alert"`:

| Case | Message |
|---|---|
| > 1 MB | "File quá lớn (hơn 1 MB). Hãy chọn đúng file sao lưu của app này." |
| Not parseable / not our format / wrong marker | "File này không phải bản sao lưu của app. Hãy chọn file có tên dạng todo-sao-luu-…" |
| Newer `version` than the app knows | "File này được tạo từ phiên bản app mới hơn. Hãy tải lại trang rồi thử lại." |
| Valid format but a task is broken (bad field, unknown field, duplicate id…) | "File sao lưu bị hỏng hoặc đã bị sửa, nên chưa nhập gì cả. Hãy dùng một bản sao lưu khác." |
| File read error | "Không đọc được file. Hãy thử lại hoặc chọn file khác." |

  Internal detail (which rule failed, at which index) may go to `console.debug`, for developers only. The user must never need it.

### F3 Save-failure feedback

- **F3.1** `store.save` returns a result instead of swallowing errors: `{ ok: true }` or `{ ok: false, reason: 'quota' | 'unavailable' | 'unknown' }`. `QuotaExceededError` (and its legacy codes 22 / 1014) maps to `quota`. `SecurityError` or `localStorage` being absent maps to `unavailable`.
- **F3.2** `commit()` checks the result on **every** save: add, toggle, delete, import, undo.
- **F3.3** On failure, the in-memory list **keeps** the user's change, so the user still sees what they typed. The app enters an **unsaved** state:
  - A persistent banner appears at the top of `<main>`, under the `<h1>`, with `role="alert"`. It stays until a save succeeds. It is not a toast, and it has no auto-dismiss.
  - Banner text (quota): "**Chưa lưu được thay đổi vừa rồi** vì bộ nhớ của trình duyệt đã đầy. Nếu đóng trang bây giờ, thay đổi này sẽ mất. Hãy tải bản sao lưu, rồi xoá bớt việc đã xong."
  - Banner text (unavailable): "**Trình duyệt đang chặn việc lưu**, nên danh sách sẽ mất khi đóng trang. Hãy tải bản sao lưu. Nếu đang mở ở chế độ ẩn danh, hãy mở app ở cửa sổ thường."
  - Banner text (unknown): "**Chưa lưu được thay đổi vừa rồi.** Hãy tải bản sao lưu để giữ danh sách, rồi thử lưu lại."
  - Banner actions: **[Tải bản sao lưu]** (F1, from memory) and **[Thử lưu lại]** (retries `store.save`).
  - When the user picks [Thử lưu lại] and the retry still fails, the banner stays and adds "Vẫn chưa lưu được." Pressing the button must always produce visible feedback.
- **F3.4** For an import that fails to save, see F2.7. The import message is "Chưa nhập được vì bộ nhớ của trình duyệt đã đầy. Danh sách giữ nguyên." and the banner from F3.3 is **not** shown, because nothing is left unsaved.
- **F3.5** Every later `commit()` tries the save again. The first success clears the banner and announces "Đã lưu lại được." (polite live region).
- **F3.6** While in the unsaved state, register a `beforeunload` handler, so the browser shows its own "leave page?" prompt. Remove it once saved. *(Interpretation of U2, see §9.3. UX owner to confirm.)*
- **F3.7** No telemetry of failures (`P1`). Compliance with the success criterion "no unreported save failure" is proved by tests (§10), not measured in production.

### F4 Unreadable stored data at startup

- **F4.1** `store.load` returns `{ ok: true, todos }`, `{ ok: true, todos: [], empty: true }` when the key is absent, or `{ ok: false, reason: 'corrupt' | 'unavailable', raw? }`.
- **F4.2** Loaded data goes through the **same task validator** as import (§6.2), because stored data could have been changed by an extension, the developer tools or an older bug. In stored data, unknown fields and invalid items count as `corrupt`.
- **F4.3** On `corrupt`, the app must **not** overwrite `todo.v1` silently:
  1. Best-effort copy of the raw string to `todo.v1.hong-<epoch ms>`. Failure here is tolerated.
  2. Show the list **error state** (F7): "Không đọc được danh sách đã lưu trên trình duyệt này. Danh sách cũ vẫn được giữ lại, chưa bị xoá. Bạn có thể nhập một bản sao lưu, hoặc bắt đầu danh sách mới." with actions **[Nhập bản sao lưu]** and **[Bắt đầu danh sách mới]**.
  3. Until the user picks one, adding tasks is disabled. Choosing "Bắt đầu danh sách mới" enables normal use. The raw copy stays where it is. Engineering may add a recovery path later.
  - If the raw copy in step 1 failed, step 2 says "Danh sách cũ sẽ bị thay nếu bắt đầu danh sách mới." In that case "Bắt đầu danh sách mới" overwrites one or more unreadable items, so §9.2 applies. Use Undo-free wording plus an explicit second press. **(BLOCKING policy conflict, see §9.2.)**
- **F4.4** On `unavailable`, show the list normally (empty) and the F3.3 "unavailable" banner right away.

### F5 Where your data lives (`P4`)

- **F5.1** The "Sao lưu" section always shows this text (not hidden behind a link):
  > "Danh sách việc chỉ được lưu trong trình duyệt này, trên máy này. Nếu xoá dữ liệu trình duyệt, dùng trình duyệt khác hoặc đổi máy, danh sách sẽ không còn. Hãy tải bản sao lưu thường xuyên và cất file ở nơi an toàn. App không gửi danh sách của bạn đi đâu cả."
- **F5.2** No technical words (`U4`): no "localStorage", "JSON", "file .json", "console", "cache".

### F6 Backup reminder

Export only helps users who already have a file when they lose their data. All 23 complaining users had none, and without reminders this feature would barely move the success metric (§9.1).

- **F6.1** Show the reminder line "Bạn chưa sao lưu lần nào." (or "Lần sao lưu gần nhất: 3 tuần trước.") in the "Sao lưu" section, next to the export button, with the export button styled as the primary action.
- **F6.2** Condition: the list has ≥ 1 task **and** either there has been no backup, or the last backup is > 7 days old and the task count or content changed since then. Use a cheap hash, or a count plus the newest `createdAt`.
- **F6.3** Computed entirely on the device from `todo.meta`. Nothing is sent anywhere (`P1`).
- **F6.4** Non-blocking: no modal, no auto-download, and it doesn't come back as a pop-up.

### F7 Screen states (`U3`)

| State | List area | "Sao lưu" section |
|---|---|---|
| **Loading** (startup) | Load is synchronous and normally invisible. The `<ul>` is rendered with `aria-busy="true"` until the first render | Hidden until first render |
| **Empty** (no tasks, storage OK) | "Chưa có việc nào. Thêm việc ở ô phía trên." + "Đổi máy mới hoặc vừa xoá dữ liệu trình duyệt? **[Nhập bản sao lưu]** để lấy lại danh sách." | Export disabled with hint (F1.1). Import enabled |
| **Empty under a filter** | "Không có việc chưa xong." / "Chưa có việc nào đã xong." | normal |
| **Populated** | as today | normal + F6 reminder |
| **Importing** | unchanged | "Đang đọc file…", buttons disabled (F2.9) |
| **Unsaved** | list shows in-memory state | F3.3 banner at top of page |
| **Error (corrupt)** | F4.3 message + actions. Add form disabled | Import enabled, export disabled (nothing valid to export) |

Fix the counter: "0 việc chưa xong" is not shown in the Empty state.

### F8 Undo for single delete *(recommended. PO to confirm whether it is in this release)*

- **F8.1** Deleting a task removes it at once and shows "Đã xoá "<title>". **[Hoàn tác]**" for 10 seconds (`U2`). The title goes in through `textContent` (`S3`).
- **F8.2** Undo puts the task back at its original index and saves.
- **F8.3** Only one pending Undo at a time. A new destructive action replaces the earlier Undo line. The earlier action stays done.
- Reason: about 0.5 day of work, closes an existing `U2` violation, and the Undo component is built for F2.8 anyway.

---

## 5. Backup file format, version 1

```json
{
  "format": "todo-sao-luu",
  "version": 1,
  "todos": [
    {
      "id": "3f2b8c1e-6a4d-4c3e-9b1a-2f7d5e8c9a10",
      "title": "Mua sữa",
      "done": false,
      "createdAt": 1760860800000
    }
  ]
}
```

| Field | Type | Rule |
|---|---|---|
| `format` | string | Exactly `"todo-sao-luu"` |
| `version` | integer | `1`. Greater than the app's known max means the "newer version" rejection. Less than 1 or not an integer means broken |
| `todos` | array | 0 to 10 000 items |
| `todos[].id` | string | 1–64 chars, `^[A-Za-z0-9-]+$`, unique within the file |
| `todos[].title` | string | After `trim()`: 1–1 000 characters. Any control character (U+0000–U+001F, U+007F, including tab and newline) means reject |
| `todos[].done` | boolean | `true` or `false` only |
| `todos[].createdAt` | number | Integer, `0 ≤ x ≤ Date.now() + 1 day` (tolerates clock skew between devices) |

- **No other keys** at the top level or inside a task. An unknown key means reject (`S1`).
- `format` and `version` are not user-created data. They contain no identifier and are needed to validate the file (`S1`). The privacy owner should confirm this reading of `P2` (§9.5).
- `id` is a random UUID per task (`crypto.randomUUID()`). It identifies the task, not the device or person.
- The 1 000-char title limit and the control-character rule also apply in the add form (`maxlength="1000"`), so every task the app creates can be exported and imported again.

---

## 6. Technical design

### 6.1 Module layout (no build step, no new dependency, `S4`)

```
app/
  index.html   + banner region, "Sao lưu" section, live regions, hidden file input
  store.js     load()/save() return results; meta load/save; corrupt-copy
  backup.js    NEW: serialize(todos) -> string; validate(text) -> {ok, todos} | {ok:false, code}; merge(local, incoming)
  app.js       state machine (ok | unsaved | corrupt), commit() result handling, undo, UI wiring
  style.css    banner, status line, disabled state, focus styles
```

`backup.js` holds only pure functions. It never touches the DOM or storage, so it can be unit tested without a browser.

### 6.2 Validator (shared by import and load)

```js
// backup.js
const TASK_KEYS = ['id', 'title', 'done', 'createdAt'];

function validTask(t, now) {
  if (!t || typeof t !== 'object' || Array.isArray(t)) return false;
  const keys = Object.keys(t);
  if (keys.length !== TASK_KEYS.length || !TASK_KEYS.every((k) => keys.includes(k))) return false;
  if (typeof t.id !== 'string' || !/^[A-Za-z0-9-]{1,64}$/.test(t.id)) return false;
  if (typeof t.title !== 'string') return false;
  const title = t.title.trim();
  if (title.length < 1 || title.length > 1000 || /[\u0000-\u001F\u007F]/.test(title)) return false;
  if (typeof t.done !== 'boolean') return false;
  if (!Number.isInteger(t.createdAt) || t.createdAt < 0 || t.createdAt > now + 86_400_000) return false;
  return true;
}
```

- Use `Object.keys` plus an exact key list. Do **not** use `for…in`, and do not copy the parsed object straight into state. Build a fresh object `{ id, title: title.trim(), done, createdAt }` so no prototype tricks (`__proto__` keys) or extra properties can leak in.
- Check for duplicate ids with a `Set`.
- Check the size before reading (F2.2), and check `text.length` again after reading as a second guard.

### 6.3 Store API

```js
store.load()        // -> {ok:true, todos, empty?} | {ok:false, reason:'corrupt'|'unavailable', raw?}
store.save(todos)   // -> {ok:true} | {ok:false, reason:'quota'|'unavailable'|'unknown'}
store.loadMeta()    // -> {lastBackupAt?, lastBackupCount?, lastBackupSig?}   (never throws)
store.saveMeta(m)   // best effort; failure ignored (reminder is not user data)
store.keepCorrupt(raw) // -> boolean
```

The storage key stays `todo.v1`. There is no migration, because the stored shape is unchanged.

### 6.4 App state

```
            save ok                       save fails
  ┌────── ok ◄──────────── unsaved ◄──────────────── ok
  │                                                    
  └─ load corrupt ──► corrupt ──(import ok | start new)──► ok
```

- `commit()` = `const r = store.save(todos); setSaveState(r); render();`
- `pendingUndo = { label, snapshot, timer }`. The snapshot is a structured copy of `todos` taken before the action.
- Import: `snapshot = todos.slice()` → `merged = merge(todos, incoming)` → `r = store.save(merged)` → if ok, `todos = merged` and offer Undo; if not, keep `todos` as it was and show the F3.4 message.

### 6.5 Rendering rules

- All user text (task titles, file names, titles inside Undo messages) goes in through `textContent` (`S3`).
- Replace the `li.innerHTML` template (`app/app.js:40`) with `createElement`. No `innerHTML` in new code, except `''` for clearing.
- Static Vietnamese strings live in one `const T = {…}` table in `app.js`, so they are easy to review against `U4`.

### 6.6 Accessibility (`U5`)

- Every new control is a native `<button>` with visible text. Icon-only buttons get `aria-label`. The delete button becomes `aria-label="Xoá việc: <title>"`.
- The hidden file input is triggered by the button. After the picker closes, focus goes back to the "Nhập bản sao lưu" button.
- The banner uses `role="alert"`. Status and Undo lines go in one `aria-live="polite"` region. The Undo button is reachable by Tab while it is visible, and **pressing Esc does not dismiss it**. The 10-second timer pauses while the Undo button has focus or hover, so keyboard and screen-reader users have time to reach it.
- Filter buttons get `aria-pressed`.
- Visible focus outline on every control (`:focus-visible`).
- Disabled buttons use the `disabled` attribute and carry the reason as text next to them, not only in color.

### 6.7 Visual style

There is **no brand guideline in the repo or the loaded skills** (§9.7). New UI follows the existing `style.css`: system font, `#f6f6f4` background, `#222` text, light `#ddd` dividers. Suggested additions:
- Banner: background `#fff4e5`, left border 4px `#b45309`, text `#222` (contrast ≥ 4.5:1).
- Status line: `#222` on page background. Undo as a text button with underline.
- "Sao lưu" section: separated from the list by a `#ddd` top border and 2rem of space.

### 6.8 Optional hardening (low effort, needs verification)

- Call `navigator.storage?.persist?.()` once, after the user adds the first task. This asks the browser not to evict the site's storage under pressure. It sends nothing off the device and is a browser API, not a dependency. How much it protects `localStorage` differs by browser. Safari can still wipe site data after a long period without use, so check the behavior in Safari and on iOS before relying on it. It is **not** a replacement for backups.

---

## 7. Policy compliance matrix

| Rule | How this spec complies | Status |
|---|---|---|
| P1 nothing leaves the device without the user's action | Export only on click. No upload, analytics or reminder pings. Meta stays local | ✅ |
| P2 export contains only user data | Four task fields + `format`/`version` marker. No device or browser data, no export timestamp | ⚠️ marker interpretation, §9.5 |
| P3 export is plain, human-readable | Pretty-printed UTF-8 text, opens in any text editor | ✅ (see §9.5 for the `.json` file name) |
| P4 tell user where data lives | F5 text always visible | ✅ |
| P5 off-browser storage needs privacy sign-off | Nothing stored off-browser | ✅ |
| S1 untrusted import | Size cap before read, `JSON.parse` only, strict schema, unknown fields rejected, whole-file reject | ✅ (cap side-effect §9.4) |
| S2 confirm before overwriting/deleting > 1 item | Import is add-only, so no multi-item overwrite or delete happens. **Conflicts with U2 for any future multi-item destructive action, and for F4.3** | ❌ **conflict, §9.2** |
| S3 `textContent` for user text | §6.5 | ✅ |
| S4 no new dependency | Browser APIs only | ✅ |
| U1 no silent loss | F3, F4, F2.7 | ✅ |
| U2 no confirmations, Undo for 10s | F2.8, F8. `beforeunload` interpretation §9.3 | ⚠️ §9.2, §9.3 |
| U3 empty/loading/error states | F7 | ✅ |
| U4 Vietnamese, no technical words | All strings in §4. File extension `.json` shows up in the download bar, §9.5 | ⚠️ minor |
| U5 keyboard + labels | §6.6 | ✅ |

---

## 8. Integration notes

### 8.1 Moving from the old phone to a new one (user journey)
Old phone: Tải bản sao lưu → file lands in Downloads/Files → the user sends it to themselves (email, chat, their own cloud). That is the user's own explicit action, so `P1` is respected. New phone: open the app → empty state → Nhập bản sao lưu → pick the file → "Đã thêm N việc từ file."

### 8.2 After clearing browser data
The user opens the app, sees the empty state with the import hint, and picks the file from the device.

### 8.3 Relation to other intents
- `intent/2026-10-19-khach-doanh-nghiep-sao-luu.md` (Minh): F1 already lets a business customer keep a copy "ở chỗ của họ". The PO should decide whether to close or merge that intent once this ships.
- T-012 due dates: see §8.4.

### 8.4 Format versioning
When due dates arrive, bump to `version: 2` and add `dueAt` as an optional field. The v2 app must accept v1 files. A v1 app rejects v2 files with the "newer version" message (F2.11) and never drops the new field silently.

---

## 9. Areas of concern

### 9.1 This release does not meet three of the intent's five success criteria (scope, not a defect)
| Success criterion (intent) | Met by this release? |
|---|---|
| New phone still shows all earlier tasks | **Only if the user exported first and moves the file over.** Not automatic |
| After clearing browser data, all earlier tasks are still there | **Only if a backup file exists**, and the user must import it |
| Add / mark done / delete on one device shows up on the other | **No.** Sync is explicitly out of scope (PO). Manual export/import between devices is possible but slow, and import is add-only (F2.5), so deletes and done-toggles don't carry over |
| Complaint emails fall from 23 to < 5 per 2 weeks | **At risk.** It depends on users backing up before they lose data. F6 reminders are the only lever. No telemetry is allowed (`P1`), so the only measure is Lan's email count |
| No save failure goes unreported | **Yes**, proved by tests (§10) |

**Ask to the PO:** confirm in the intent that criteria 1–3 are deferred to the sync intent, or accept that this release meets them only partly. Without that, the release will be judged against criteria it was never scoped to meet.

### 9.2 BLOCKING: `policy-security@1#S2` and `policy-ux@1#U2` contradict each other
- **S2:** an operation that overwrites or deletes more than one item must ask for explicit confirmation **before** it runs.
- **U2:** no confirmation dialogs. Every destructive action runs at once and offers Undo for 10 seconds.

No design can satisfy both for a multi-item overwrite or delete. Where this spec meets it:

1. **Import with replace.** This is the obvious design ("replace my list with the file"), and it is exactly the example in S2. **Workaround in this spec:** import is add-only (F2.5), so it never overwrites or deletes and neither rule is triggered. Cost: a backup cannot carry deletes or done-toggles across devices, and tasks the user deleted on this device come back if they import an older file. Undo covers that.
2. **F4.3 "Bắt đầu danh sách mới"** when the corrupt data could not be copied aside: this overwrites every unreadable item. The spec currently asks for an explicit second press. That counts as a confirmation and **breaks U2**. Undo is not possible here, because the data can't be read back.
3. **Future features** such as "Xoá các việc đã xong", "Xoá tất cả" and sync conflict resolution will all hit the same contradiction.

**What we need:** the security owner and UX owner agree a precedence rule, for example "for operations whose effect Undo can fully reverse, U2 applies; for operations Undo cannot reverse, S2 applies", and publish it as v2 of either policy. Until then:
- engineering can build F1–F3, F5–F8 as specified;
- F4.3's fallback branch needs a decision before it is merged;
- the PO must approve the add-only import trade-off.

### 9.3 `beforeunload` while unsaved (F3.6) is an interpretation of U2
It is a browser-native "leave page?" prompt, not an app confirmation for a destructive action. Leaving with unsaved changes **is** silent loss under U1, so the spec favors U1. **UX owner to confirm.** If rejected, drop F3.6. The persistent banner from F3.3 still satisfies U1.

### 9.4 The 1 MB import cap (S1) can lock users out of their own backup
`localStorage` holds about 5 MB, so a list can grow to more than the 1 MB a backup may be. Rough guide: about 6 000 typical tasks, or fewer with long titles. Such a user can export but **can never import**, which would be silent loss at the worst moment. Real exposure is probably tiny for a todo app, but nobody has measured it.
- Spec behavior (F1.10): export anyway and warn: "Danh sách quá lớn để nhập lại từ một file. Hãy xoá bớt việc đã xong rồi tải lại bản sao lưu."
- **Decision needed (security owner):** keep 1 MB and accept this, or allow a higher cap for files that pass the strict schema. The size cap would still be checked before reading.

### 9.5 Small policy readings that need an owner's nod
- **P2:** the `format` and `version` keys are not user-created data, but S1 needs them to validate the file. They carry no identifier. *(Privacy owner.)*
- **U4 vs P3:** the file is named `….json`, so "json" shows in the browser's download bar and file picker. The app's own text never says it. A `.txt` name would read as plainer, but the file picker filter and the meaning of the file would suffer. *(UX owner.)*

### 9.6 Known silent-loss paths that remain
- **Two tabs open (C8):** the last save wins and overwrites the other tab's changes, with no notice. Fix it with a `storage` event listener that reloads or merges. It is not in the intent, about 0.5 day of work, and the PO may want it given U1.
- **The browser evicts storage without warning** (for example Safari's limit on site data for sites not used in a while). The app cannot detect this before it happens. Backups (F6) and `persist()` (§6.8) only reduce the risk.

### 9.7 No brand guideline was available
The request asked for brand compliance, but there is no brand skill or brand document in the repo. Only the privacy, security and UX policies exist. The visual design follows `app/style.css` (§6.7). **Design/brand owner:** please share the guideline, or confirm the existing style is the brand.

### 9.8 Evidence gaps in the intent (from its Open questions, still open)
- Nobody has split the 23 emails between "new phone" and "cleared browser data". This matters for whether F6 reminders or the import UX on mobile deserve more effort. → Lan
- The emails have not been copied into `tickets/`, so reviewers cannot check the baseline. → Lan

---

## 10. Acceptance tests

Run in current Chrome, Firefox, Safari (macOS), Safari (iOS) and Chrome (Android).

**Export**
1. A list with 3 tasks → Tải bản sao lưu → the file opens in a text editor and shows the 3 titles readably. It has exactly the keys in §5, and no other keys anywhere.
2. Empty list → export button disabled, with the hint.
3. Storage full (fill `localStorage` first) → add a task → the banner appears → [Tải bản sao lưu] in the banner downloads a file that **contains the unsaved task**.

**Import**
4. New browser profile → import the file from test 1 → the 3 tasks appear in `createdAt` order. Reload → still there.
5. Import the same file again → "File không có việc nào mới." and the list is unchanged.
6. Device has tasks A, B. The file has B (edited title) and C → result is A, B (local title kept), C. The message says 1 added, 1 already there. Undo → back to A, B exactly.
7. Rejected files, each leaving the list unchanged and showing the right F2.11 message: 1.1 MB file; `.png` renamed `.json`; valid JSON with `format` wrong; `version: 2`; a task with an extra key `"x":1`; a task with `"__proto__"` key; duplicate ids; `done: "true"`; `createdAt` as a string; empty title; 1 001-char title; a title containing `<img src=x onerror=alert(1)>` **is accepted and shown as literal text** (S3).
8. Storage nearly full + a valid large import → "Chưa nhập được…" and the list is unchanged after reload.

**Save failures**
9. For each of add, toggle, delete, import-undo with storage full → the banner appears every time and the change stays visible. Free space → [Thử lưu lại] → the banner clears and "Đã lưu lại được." is announced.
10. Private window with storage blocked (or `localStorage` stubbed to throw `SecurityError`) → the "unavailable" banner shows at startup.
11. Put the corrupt string `{bad` in `todo.v1` → the error state shows. `todo.v1.hong-*` holds `{bad`. `todo.v1` is **not** overwritten until the user picks an action.
12. Static check: `grep console.error app/store.js` finds no swallowed save errors, and every `store.save(` call site uses the result.

**Accessibility and wording**
13. The whole flow (add, delete, Undo, export, import, banner retry) can be done with the keyboard alone. The screen reader announces the banner, the status lines and the Undo button.
14. A grep of all UI strings finds none of: localStorage, JSON, console, cache, storage, file .json.

---

## 11. Plan (1 developer, 10 working days)

| Day | Work |
|---|---|
| 1 | `store.js` result API (F3.1, F4.1). `backup.js` serialize, validate, merge, with unit tests (§10 test 7 as unit tests) |
| 2–3 | F3 banner + unsaved state + retry. F4 corrupt handling (except the §9.2 fallback branch) |
| 4–5 | F1 export, F2 import + merge + Undo component |
| 6 | F5 notice, F6 reminder, F7 states, wording table |
| 7 | F8 single-delete Undo (if PO confirms). `createElement` row (C6). `aria-pressed` (C7) |
| 8 | Accessibility pass (§6.6), styling (§6.7) |
| 9 | Cross-browser and mobile run of §10, especially iOS file pick and download |
| 10 | Buffer, fixes, and the §9.2 fallback once decided |

**Decisions needed before day 2:** §9.2 (security + UX owners, PO approval of add-only import), §9.1 (PO).
**Decisions needed before day 9:** §9.3, §9.4, §9.5, §9.7.
