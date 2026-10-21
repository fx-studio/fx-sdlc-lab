# Spec: Backup to file, restore from file, and visible save failures

Source intent: `intent/2026-10-19-khach-khong-mat-viec.md` (Lan, accepted, PO answers 2026-10-20)
Date: 2026-10-20 · Status: **ready for engineering, with 3 sign-offs pending** (see §2) · Budget: 1 developer, 2 weeks

Policies applied: `policy-privacy@1`, `policy-security@1`, `policy-ux@1`.
Brand guidelines: **none exist in the repo** (no brand skill or style guide). This spec reuses the existing look in `app/style.css`
and adds no new colours, fonts or icons beyond what §6.6 lists. If a brand guide exists elsewhere, it has not been applied.

---

## 1. Summary

Customers lose their whole todo list when they switch phones or clear browser data, because the list lives only in this browser's
`localStorage` (`app/store.js:1-3`). The product owner scoped this release to:

1. **Back up**: the user saves the whole list to a file on their device.
2. **Restore**: the user picks a backup file and the app adds its items back.
3. **Save failures are visible**: when a save fails (storage full or blocked), the user is told on the same screen and given a way out.

Plus two small items that the policies require and the success criteria depend on:

4. **Tell users where their data lives** (`policy-privacy@1#P4`), with a backup reminder.
5. **Stop the silent wipe on unreadable data**: today a corrupted saved list is replaced by an empty one on the next save (§3, defect D1).

Out of scope (PO): multi-device sync, accounts/login, shared lists, recovering data for the 23 customers who already emailed, due
dates (T-012).

## 2. Decisions needed before or during build

These block nothing on day 1, but each must be answered before the item it names ships.

| # | Question | Owner | Default this spec uses | Blocks |
|---|---|---|---|---|
| D-1 | **Policy conflict.** `policy-security@1#S2` requires a confirmation *before* any overwrite/delete of >1 item. `policy-ux@1#U2` forbids confirmation dialogs and requires Undo instead. A "replace my list with this file" import cannot satisfy both. | Khoa (security) + Linh (UX) | Avoid the conflict: import **only adds** items and never overwrites or deletes existing ones (§6.4). No dialog needed, Undo offered anyway. A "replace" mode is **not** built. | Nothing, if the default is accepted |
| D-2 | Is **Undo of an import** (removes the items just added, can be >1) a "delete of >1 item" under S2? We read it as reversing the user's own action within 10 s, not a new destructive operation. | Khoa | Undo runs at once, no confirmation | FR-4 Undo |
| D-3 | The backup file holds a format marker and export time (`app`, `version`, `exportedAt`) besides the user's items. `policy-privacy@1#P2` allows "only data the user created". We read these as non-identifying file metadata, needed to validate the file (S1). No device ID, browser info or user name is included. | Mai (privacy) | Include the three fields | FR-1 |
| D-4 | Backup reminder (FR-6) is not in the PO's list, but the success criteria cannot be met without it (a user who never backs up still loses everything). Keep it? | Thảo (PO) | Build it; it is ~0.5 day and can be cut | FR-6 |
| D-5 | Success criterion 3 ("add/complete/delete on one device, the other sees it") is sync, which the PO put out of scope. This release **will not meet it**. Please remove or move it to the sync intent so the release is not judged against it. | Thảo (PO) | Treated as not applicable | Release review |

No new external dependency is used, so no `policy-security@1#S4` sign-off is needed. No data is stored outside the browser, so no
`policy-privacy@1#P5` sign-off is needed.

## 3. Current state (facts from the code)

- Storage: one key `todo.v1` holding a JSON array (`app/store.js:3`).
- A todo is `{ id, title, done, createdAt }`: `id` from `crypto.randomUUID()`, `createdAt` from `Date.now()` (`app/app.js:8`).
- Every change calls `commit()` → `store.save()` → `render()` (`app/app.js:23-26`).
- `store.save()` catches all errors and only logs them (`app/store.js:15-19`). The UI carries on as if the save worked. This breaks
  `policy-ux@1#U1` today.
- **Defect D1 (silent wipe):** `store.load()` returns `[]` if the stored value cannot be parsed (`app/store.js:9-11`). The next add
  then saves `[newItem]` over the unreadable data, destroying it with no message. Also, valid JSON that is not an array (e.g. `{}`)
  is returned as is and crashes `visible()`.
- **Defect D2:** if `localStorage` itself is blocked (some privacy modes), `localStorage.getItem` throws inside `load()` and is
  caught, so the app silently works in memory only and loses everything on reload.
- Rendering: titles are already set with `textContent` (`app/app.js:41`), compliant with `policy-security@1#S3`. The `innerHTML` on
  `app/app.js:40` is a static template with no user text; keep it that way.
- Deleting a single item has no Undo (`app/app.js:18-21`), which does not meet `policy-ux@1#U2`. Not in this intent's scope; logged
  as a follow-up (§11).
- No empty state is shown for an empty list (`policy-ux@1#U3`).

## 4. Users and scenarios

| Scenario | Today | After this release |
|---|---|---|
| A. Switching to a new phone | Starts with an empty list | User backs up on the old phone, moves the file (email to self, cloud drive, AirDrop: the user's choice), opens the app on the new phone, taps **Nhập từ file**, sees all items |
| B. Clearing browser data | Empty list | Same as A, from a backup made before clearing |
| C. Storage full or blocked | Changes vanish on reload, no message | A message appears at once; the user can back up to a file so nothing is lost |
| D. Laptop + phone | Two separate lists | Still two lists. User can move items one way by backup + import (import adds, never removes). Real sync is a later intent |

## 5. Requirements

Priorities: **Must** = needed for the PO's scope or a policy. **Should** = cut first if time runs out.

### FR-1 Back up to a file (Must)
- A button **Sao lưu ra file** downloads a file of the whole list (all items, regardless of the current filter).
- File name: `viec-can-lam-YYYY-MM-DD.json` (local date).
- Content: format in §6.3. Plain, indented, UTF-8, human-readable (`policy-privacy@1#P3`). Only the user's items plus the three
  metadata fields (D-3). Nothing else (`policy-privacy@1#P2`).
- Generated in the browser only (`Blob` + `<a download>`). Nothing is sent anywhere (`policy-privacy@1#P1`).
- Works from the in-memory list, so it still works when saving to storage is failing (this is the rescue path for FR-5).
- Works with an empty list (exports `"todos": []`); the status line says the list is empty, the file is still produced.
- After download: status message "Đã sao lưu N việc ra file." and the last-backup date is recorded (FR-6).
- If the file would be over 1 MB (the import cap, `policy-security@1#S1`), still download it, but show: "File sao lưu lớn hơn 1 MB
  nên chưa nhập lại được. Hãy xoá bớt việc đã xong rồi sao lưu lại." (≈8,000 items needed to reach this; see §10 R4.)

**Acceptance:** with 3 items (1 done), the downloaded file opens in a text editor and shows exactly those 3 titles and states; no other
data. Works in latest Chrome, Safari (macOS + iOS), Firefox, Chrome Android.

### FR-2 Restore from a file (Must)
- A button **Nhập từ file** opens the system file picker (hidden `<input type="file" accept=".json,application/json">`, triggered by
  the button).
- The file is validated as in §6.5 **before** anything changes. Any failure → nothing changes, an error message in plain Vietnamese
  (§6.6) says what is wrong and what to do.
- If valid, items are **added** by the merge rules in §6.4. Existing items are never changed or removed.
- Result message (with Undo, FR-4), e.g. "Đã thêm 30 việc từ file. 2 việc đã có sẵn nên giữ nguyên."
- If the merged list cannot be saved (FR-5), the import is rolled back in memory and the save-failure message is shown; the list is
  as it was.
- Picking the same file twice adds nothing the second time ("Không có việc mới. 30 việc trong file đã có sẵn.").

**Acceptance:** export on browser 1 → clear site data on browser 1 → import → list is identical (ids, titles, done, order). Import
the same file again → no duplicates.

### FR-3 Loading state while reading a file (Must, `policy-ux@1#U3`)
- While the file is being read and checked: both backup buttons are disabled and the status line shows "Đang đọc file…". Typical
  files read in well under a second; the state exists for slow phones and the 1 MB worst case.

### FR-4 Undo import for 10 seconds (Must, `policy-ux@1#U2`)
- The import result message has a **Hoàn tác** button for 10 s.
- Undo restores the list exactly as it was before the import and saves it. Message: "Đã hoàn tác. Danh sách trở lại như trước."
- Any other change to the list (add, toggle, delete, another import) within the 10 s ends the Undo offer, so Undo never discards a
  change made after the import.
- If the Undo save fails, FR-5 applies.

### FR-5 Save failures are shown (Must, `policy-ux@1#U1`, PO success criterion "no failed save the user is not told about")
- `store.save()` returns success or failure instead of swallowing the error (§6.2).
- On failure the app shows a persistent alert banner at the top of the list:
  - Storage full: "Không lưu được: bộ nhớ của trình duyệt đã đầy. Việc vừa sửa sẽ mất khi tải lại trang. Hãy **sao lưu ra file**
    ngay, rồi xoá bớt việc đã xong."
  - Storage blocked/other: "Không lưu được trên trình duyệt này. Việc vừa sửa sẽ mất khi tải lại trang. Hãy **sao lưu ra file** ngay."
  - "sao lưu ra file" in the banner is a button that runs FR-1.
- The in-memory list keeps the change (the user still sees it and can export it). The banner stays until a later save succeeds,
  then it is replaced by "Đã lưu lại được." for a few seconds.
- Every later commit retries the save (no extra timer).
- The browser's `beforeunload` prompt is shown while unsaved changes exist, so a reload does not drop them without warning. (This is
  the browser's own leave-page prompt, not an app dialog; see §10 R5 for the U2 reading.)

**Acceptance:** fill storage in devtools (or stub `localStorage.setItem` to throw `QuotaExceededError`), add an item → banner appears
on the same screen within the same interaction, item is visible, **Sao lưu ra file** in the banner downloads a file containing it.

### FR-6 Where your data lives + backup reminder (Must for P4 text; Should for reminder, D-4)
- Below the list, a short "Sao lưu" section with the two buttons and this text (`policy-privacy@1#P4`):
  "Danh sách việc chỉ được lưu trong trình duyệt này, trên máy này. Nếu xoá dữ liệu trình duyệt hoặc đổi máy, danh sách sẽ mất.
  Hãy sao lưu ra file để giữ lại."
- A line "Sao lưu gần nhất: 20/10/2026" or "Chưa sao lưu lần nào". The date is kept in `localStorage` key `todo.lastBackup`
  (a timestamp, on this device only, never exported).
- Reminder (Should): if the list has ≥ 1 item and there has been no backup, or the last backup is > 7 days old **and** the list has
  changed since, the line is shown emphasised: "Đã 9 ngày chưa sao lưu." No popups, no timers.

### FR-7 Empty and error states for the list (Must, `policy-ux@1#U3`)
- **Empty** (no items at all): "Chưa có việc nào." plus "Mới đổi máy? Bấm **Nhập từ file** để lấy lại danh sách đã sao lưu." (button
  runs FR-2). For an empty filter result: "Không có việc nào ở mục này."
- **Loading**: data is read synchronously at start; no loading state for the list itself. File reading: FR-3.
- **Error, saved data unreadable** (fix for D1): see §6.2. Message: "Không đọc được danh sách đã lưu trên máy này. Dữ liệu cũ vẫn
  được giữ nguyên. Bạn có thể nhập lại từ file sao lưu." The app runs with an empty list, and **does not overwrite** the unreadable
  data (it is moved aside, §6.2).
- **Error, storage blocked** (D2): the FR-5 "blocked" banner is shown from page load.

### NFR
- **No new dependencies** (`policy-security@1#S4`): plain JS, browser APIs only (`Blob`, `URL.createObjectURL`, `File.text()`,
  `JSON.parse`). Keep the current no-build, two-script setup.
- **No network calls, no analytics** (`policy-privacy@1#P1`). Success is measured by Lan's email count (§8), not in-app tracking.
- **Untrusted input** (`policy-security@1#S1`): §6.5. Titles from files rendered only via `textContent` (`policy-security@1#S3`).
- **Language**: all UI text Vietnamese, short, no technical words (`policy-ux@1#U4`). The words "JSON", "localStorage", "console",
  "quota", "schema" must not appear on screen. The `.json` file extension is visible only in the system's file name, not in app text.
- **Accessibility** (`policy-ux@1#U5`): §6.7.

## 6. Design

### 6.1 Files touched

| File | Change |
|---|---|
| `app/store.js` | `load()` returns status; `save()` returns result; corrupt-data handling; `lastBackup` get/set |
| `app/backup.js` (new) | `toBackupFile(todos)`, `parseBackupFile(text)` (validation), `mergeTodos(current, incoming)`. Pure functions, no DOM, so they can be unit tested |
| `app/app.js` | `commit()` handles save result; banner, status/Undo, buttons, empty states, `beforeunload` |
| `app/index.html` | Banner region, status region, "Sao lưu" section, hidden file input, `<script src="backup.js">` between `store.js` and `app.js` |
| `app/style.css` | Banner, status line, section, disabled buttons, visually-hidden helper, focus outline |

### 6.2 Storage layer (`app/store.js`)

```js
// load(): { todos, status }  status: 'ok' | 'empty' | 'unreadable' | 'blocked'
// save(todos): { ok: true } | { ok: false, reason: 'full' | 'blocked' }
```

- `load()`:
  - `getItem` throws → `{ todos: [], status: 'blocked' }`.
  - value `null` → `'empty'`.
  - value parses to an array whose items all pass the item rules in §6.5 → `'ok'`.
  - otherwise → `'unreadable'`: copy the raw string to `todo.v1.unreadable` (once; do not overwrite an existing copy), then remove
    `todo.v1`. If the copy fails (storage full), leave `todo.v1` in place and set a flag so `save()` refuses to write until the user
    imports or a later copy succeeds; show the FR-5 "full" banner. Either way the old data is never silently destroyed.
- `save()`: on error, `reason = 'full'` if `err.name === 'QuotaExceededError'` or `'NS_ERROR_DOM_QUOTA_REACHED'` (old Firefox) or
  `err.code === 22 || err.code === 1014`; else `'blocked'`. Keep the `console.error` for developers.
- Key `todo.v1` and its array format are **unchanged**, so existing users' data loads as before. No migration.

### 6.3 Backup file format (version 1)

```json
{
  "app": "todo",
  "version": 1,
  "exportedAt": "2026-10-20T08:15:00.000Z",
  "todos": [
    { "id": "3f1c…", "title": "Mua sữa", "done": false, "createdAt": 1760947200000 }
  ]
}
```

- `JSON.stringify(data, null, 2)`, MIME `application/json;charset=utf-8`.
- Items are written in current list order, with only these four fields (build new objects; do not spread stored objects).
- When due dates (T-012) add a field, bump to `"version": 2`. A v1 app rejects v2 files with the "newer version" message (§6.6).
  T-012's spec must say how v2 imports v1 files.

### 6.4 Import merge rules (`mergeTodos`)

1. Validate the whole file first (§6.5). Any error → stop, nothing changes.
2. For each file item, in file order:
   - `id` not in the current list → append it (copy of the four fields).
   - `id` already in the current list → skip; the current item wins (even if title/done differ). Count it as "đã có sẵn".
3. Existing items keep their order and values. Nothing is removed. So on an empty list (new phone), the result equals the file.
4. Keep a snapshot of the pre-import list for Undo (FR-4).
5. Save. On failure: restore the snapshot in memory, show FR-5 banner, no success message.

Rationale: purely additive import is not an "overwrite or delete" under `policy-security@1#S2`, so no confirmation is needed, and it
satisfies `policy-ux@1#U2` (no dialog, Undo offered). This is the default proposed in D-1.

### 6.5 Validation (`parseBackupFile`, `policy-security@1#S1`)

Checks in this order, stopping at the first failure. Each maps to one message in §6.6.

| # | Rule | Message key |
|---|---|---|
| 1 | `file.size` ≤ 1,048,576 bytes, checked **before** reading | `tooBig` |
| 2 | Reads as text; `JSON.parse` succeeds. Never `eval`, `Function`, or insert as HTML | `notBackup` |
| 3 | Top level is a plain object with exactly the keys `app`, `version`, `exportedAt`, `todos`; no others | `notBackup` |
| 4 | `app === "todo"` | `notBackup` |
| 5 | `version` is a number; `version === 1`. If `> 1` | `newerVersion` (else `notBackup`) |
| 6 | `exportedAt` is a string (not otherwise used) | `notBackup` |
| 7 | `todos` is an array, length ≤ 10,000 | `damaged` |
| 8 | Each item is a plain object with exactly `id`, `title`, `done`, `createdAt`; no others | `damaged` |
| 9 | `id`: string, 1–100 chars | `damaged` |
| 10 | `title`: string, non-empty after trim (no max beyond the file cap; the app has no title limit today, so a max could reject the user's own backup) | `damaged` |
| 11 | `done`: boolean | `damaged` |
| 12 | `createdAt`: finite number ≥ 0 | `damaged` |
| 13 | No duplicate `id` within the file | `damaged` |

- "Exactly these keys" is checked with `Object.keys`, so a `__proto__` or `constructor` key in the file is rejected as unknown.
- Validated items are copied into new objects with only the four fields before use.
- Rules 8–12 are reused by `store.load()` for stored data.

### 6.6 UI text (all Vietnamese, `policy-ux@1#U4`)

| Key | Text |
|---|---|
| section title | Sao lưu |
| btn export | Sao lưu ra file |
| btn import | Nhập từ file |
| where data lives | Danh sách việc chỉ được lưu trong trình duyệt này, trên máy này. Nếu xoá dữ liệu trình duyệt hoặc đổi máy, danh sách sẽ mất. Hãy sao lưu ra file để giữ lại. |
| last backup | Sao lưu gần nhất: {dd/mm/yyyy} · Chưa sao lưu lần nào · Đã {n} ngày chưa sao lưu. |
| export ok | Đã sao lưu {n} việc ra file. |
| export empty | Danh sách đang trống. Đã tạo file sao lưu trống. |
| export too big | File sao lưu lớn hơn 1 MB nên chưa nhập lại được. Hãy xoá bớt việc đã xong rồi sao lưu lại. |
| reading | Đang đọc file… |
| import ok | Đã thêm {n} việc từ file. ({m} việc đã có sẵn nên giữ nguyên.) |
| import nothing new | Không có việc mới. {m} việc trong file đã có sẵn. |
| import empty file | File này không có việc nào. |
| btn undo | Hoàn tác |
| undo ok | Đã hoàn tác. Danh sách trở lại như trước. |
| tooBig | File quá lớn (trên 1 MB). Hãy chọn đúng file sao lưu của app này. |
| notBackup | Đây không phải file sao lưu của app này. Hãy chọn file có tên bắt đầu bằng "viec-can-lam-". |
| newerVersion | File này được tạo từ bản app mới hơn. Hãy tải lại trang để cập nhật app rồi thử lại. |
| damaged | File sao lưu bị hỏng hoặc đã bị sửa, nên chưa nhập. Danh sách của bạn không thay đổi. Hãy thử một file sao lưu khác. |
| read failed | Không mở được file. Hãy thử lại hoặc chọn file khác. |
| save full | Không lưu được: bộ nhớ của trình duyệt đã đầy. Việc vừa sửa sẽ mất khi tải lại trang. Hãy [sao lưu ra file] ngay, rồi xoá bớt việc đã xong. |
| save blocked | Không lưu được trên trình duyệt này. Việc vừa sửa sẽ mất khi tải lại trang. Hãy [sao lưu ra file] ngay. |
| save recovered | Đã lưu lại được. |
| unreadable | Không đọc được danh sách đã lưu trên máy này. Dữ liệu cũ vẫn được giữ nguyên. Bạn có thể nhập lại từ file sao lưu. |
| empty list | Chưa có việc nào. Mới đổi máy? Bấm [Nhập từ file] để lấy lại danh sách đã sao lưu. |
| empty filter | Không có việc nào ở mục này. |

Error messages for import all end by implying "your list did not change" or say it directly; keep that property if copy is edited.

### 6.7 Layout, states and accessibility

```
Todo
[ Việc cần làm…              ] [Thêm]
┌ banner (role="alert") — only when a save failed / data unreadable ┐
[Tất cả] [Chưa xong] [Đã xong]
☐ Mua sữa                                   ×
…  (or empty-state text)
3 việc chưa xong
── Sao lưu ───────────────────────────────
Danh sách việc chỉ được lưu trong trình duyệt này…
Sao lưu gần nhất: 20/10/2026
[Sao lưu ra file] [Nhập từ file]
status line (role="status", aria-live="polite")  Đã thêm 30 việc từ file. [Hoàn tác]
```

- Banner: `role="alert"`, so screen readers announce a failed save at once. Contains a real `<button>` for "sao lưu ra file".
- Status line: `role="status"`, `aria-live="polite"`. Undo is a `<button>` inside it; it stays in the tab order while shown; when it
  expires, focus is not moved (if it had focus, move focus to **Nhập từ file**).
- After import (success or error) focus returns to **Nhập từ file**.
- Hidden file input: visually hidden but not `display:none`, `tabindex="-1"`, `aria-hidden="true"`; the visible **Nhập từ file**
  `<button>` calls `input.click()`. Clear `input.value` after each pick so picking the same file again fires `change`.
- Disabled state during reading: `disabled` attribute on both buttons plus `aria-busy="true"` on the section.
- Visible focus outline on all buttons (add `:focus-visible` style; the current CSS has none).
- Styling: reuse current font, `#f6f6f4` background, `#ddd` borders. Banner uses a light warm background with dark text meeting
  4.5:1 contrast. No icons, no new fonts.
- Existing controls: the delete button already has `aria-label="Xoá"`. The checkbox has no accessible name besides the visible
  title inside its `<label>`, which is fine.

### 6.8 `commit()` flow (`app/app.js`)

```
commit(): result = store.save(todos)
  ok   → if banner was showing: hide it, status "Đã lưu lại được."; unsaved = false
  fail → show banner for result.reason; unsaved = true
  endUndoOffer() unless this commit is the import itself
  render()
beforeunload: if unsaved → event.preventDefault()
```

## 7. Policy compliance

| Rule | How this spec meets it |
|---|---|
| privacy P1 | Export/import only on a user tap; no network code; no analytics (§NFR) |
| privacy P2 | File has only the user's items + 3 metadata fields, pending Mai's OK (D-3) |
| privacy P3 | Indented plain text file (§6.3) |
| privacy P4 | "Where data lives" text (FR-6) |
| privacy P5 | Nothing stored outside the browser; not triggered |
| security S1 | Size cap before reading, strict schema, unknown fields rejected, no eval (§6.5) |
| security S2 | Import is additive only, nothing overwritten or deleted (§6.4); D-1, D-2 for owner confirmation |
| security S3 | Imported titles rendered via existing `textContent` path; new UI text uses `textContent` |
| security S4 | No new dependency |
| UX U1 | FR-5 banner, same screen, plain words, action button |
| UX U2 | No dialogs; import Undo 10 s (FR-4). Existing single delete lacks Undo: follow-up (§11) |
| UX U3 | Empty/loading/error states (FR-3, FR-7) |
| UX U4 | Copy table §6.6 |
| UX U5 | §6.7 |

## 8. Success criteria, mapped

| Criterion (intent) | Met by this release? |
|---|---|
| New phone: user still sees all previous items | **Only if they backed up first.** FR-1/FR-2 make it possible; FR-6 reminder pushes users to do it |
| After clearing browser data: still sees all items | Same condition as above |
| Change on one device shows on the other | **No.** That is sync, out of scope (D-5) |
| Emails about lost items < 5 per 2 weeks, within 6 weeks of release | Measured by Lan counting support emails per 2-week window, starting from release date. Baseline 23 / 2 weeks (1–14 Oct). Risk: users who never back up keep losing data (R1) |
| No failed save the user is not told about | FR-5 + D1/D2 fixes. Verified by tests T5–T8 |

Lan should also record, for each new loss email, whether the customer had a backup. That tells us if the miss is "didn't back up" (fix
with stronger reminder or sync) or a bug.

## 9. Test plan

Unit tests for `app/backup.js` (pure functions; run in a plain HTML test page or Node, no new dependency needed):

- T1 Round trip: `parseBackupFile(toBackupFile(list))` equals `list` (fields and order), including titles with Vietnamese
  diacritics, emoji, `<script>`, quotes, newlines.
- T2 Each row of §6.5 has one failing case that returns the right message key; a valid file passes.
- T3 `__proto__` / `constructor` key at top level and item level → `notBackup` / `damaged`, and `Object.prototype` untouched.
- T4 Merge: empty + file = file; overlap ids keep current values; nothing removed; same file twice adds 0.

Manual / browser tests (Chrome, Safari macOS, Safari iOS, Firefox, Chrome Android):

- T5 Stub `setItem` to throw `QuotaExceededError` → add item → "full" banner, item visible, banner button downloads file with it.
- T6 Stub `setItem` to throw `SecurityError` → "blocked" banner. Stub `getItem` to throw → banner at page load.
- T7 Remove stub → next change → banner gone, "Đã lưu lại được.", reload keeps data.
- T8 Put `{bad` in `todo.v1` → reload → "unreadable" message; `todo.v1.unreadable` holds `{bad`; adding an item does not destroy it.
- T9 Scenario A end to end: export on device 1, send file to device 2 (email/drive), import on device 2 → same list.
- T10 Import then Undo within 10 s → list as before; import, add item, then Undo is gone.
- T11 Import a v2 file, a 2 MB file, a random image, an empty `{}` → right messages, list unchanged.
- T12 Keyboard only: reach and use every new control; screen reader (VoiceOver) announces banner and status messages.
- T13 Item titled `<img src=x onerror=alert(1)>` imported → shown as text, no alert.
- T14 Existing data in `todo.v1` from the current version loads unchanged after deploy.

## 10. Risks

- **R1 Users don't back up.** Backup only helps those who do it before losing data. Mitigations: FR-6 reminder and empty-state hint.
  If emails stay above 5/2 weeks, the answer is the sync intent (needs P5 sign-off and an account/server decision by the PO).
- **R2 Moving the file to a new phone is a hurdle**, especially on iOS (file lands in Files app). Lan's support replies should get a
  short how-to. Possible later improvement: Web Share API (`navigator.share` with a file), a browser API, no dependency; not in v1.
- **R3 iOS Safari / in-app browsers** may handle `<a download>` poorly (e.g. opening the file instead of saving). Test early (day 2);
  fallback is opening the blob in a new tab so the user can save it.
- **R4 1 MB import cap vs large lists.** ~8,000 items reach 1 MB; export warns (FR-1). If real users hit it, ask Khoa to raise the cap.
- **R5 `beforeunload` prompt** is browser UI, not an app confirmation, so we read it as outside U2. If Linh disagrees, drop it; the
  banner alone still meets U1.
- **R6 Two tabs open** overwrite each other's saves (existing behaviour, unchanged). Not in scope; note for the sync intent.

## 11. Follow-ups (not in this release)

- Undo for single-item delete (`policy-ux@1#U2` gap in existing code, `app/app.js:18-21`).
- Multi-device sync / accounts: separate intent; needs PO decision on accounts and Mai's P5 sign-off.
- T-012 due dates: bump backup format to version 2 (§6.3).
- Minh's enterprise backup intent (`intent/2026-10-19-khach-doanh-nghiep-sao-luu.md`) likely shares FR-1. PO to decide whether to merge.

## 12. Plan (1 developer, 10 working days)

| Day | Work |
|---|---|
| 1 | `store.js` result types, D1/D2 fixes, `commit()` handling, banner (FR-5, FR-7 errors) |
| 2 | `backup.js` export + FR-1 UI; iOS/Android download check (R3) |
| 3–4 | `parseBackupFile` validation + unit tests T1–T3 |
| 5 | `mergeTodos`, import flow, loading state, Undo (FR-2/3/4), T4 |
| 6 | "Sao lưu" section, P4 text, last-backup + reminder, empty states (FR-6/7) |
| 7 | Accessibility pass (§6.7), copy check against §6.6 |
| 8–9 | Browser matrix T5–T14, fixes |
| 10 | Buffer; release; Lan starts the 6-week email count |

Cut order if late: FR-6 reminder (keep the P4 text), then `beforeunload`.

## 13. Open questions (carried from the intent)

- Lan: copy the 23 anonymised emails into `tickets/` so reviewers can check the count.
- Lan: split the 23 by cause (new phone vs cleared data). Does not change this design, but helps judge R1 and R2.
- Plus D-1 … D-5 in §2.
