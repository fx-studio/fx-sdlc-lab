# R3a-test-writer-tu-spec

Chạy 2026-10-29 14:49 ở `r3-tw` (thư mục riêng của lượt này), chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Write the acceptance tests for spec/2026-10-19-khach-khong-mat-viec.md into tests/, from the spec and api.md only.

## Tool call (10)

1. Bash · command=ls -la && ls spec tests 2>/dev/null; cat spec/2026-10-19-khach-khong-mat-viec.md; echo ----; cat api.md
2. Read · file_path=<home>/.claude/projects/-private-tmp-<thư-mục-tạm>
3. Read · file_path=<thư-mục-tạm>
4. Write · file_path=<thư-mục-tạm>
5. Write · file_path=<thư-mục-tạm>
6. Write · file_path=<thư-mục-tạm>
7. Write · file_path=<thư-mục-tạm>
8. Write · file_path=<thư-mục-tạm>
9. Bash · command=cd <thư-mục-tạm> && for f in *.js; do node --check "$f" && echo "ok $f"; done; grep -c "AMBIGUOUS" *.js
10. Bash · command=node --check <thư-mục-tạm> && node --check <thư-mục-tạm> && node --check <thư-mục-tạm> && node --check <thư-mục-tạm> && node --check <thư-mục-tạm> && echo all-ok

## Claude · 339 s

I wrote 23 acceptance tests for this spec in `tests/`, one `test()` per criterion, built from the spec and `api.md` only. Nothing has been run: I didn't run the tests against code, as instructed, and my `node --check` syntax check was blocked by a permission prompt, so the syntax hasn't been checked either. I didn't open anything under `app/`.

The tests are in four files, plus `helpers.js`, which holds the fake `localStorage`, a reopen-the-page helper and backup-file builders:
- `backup.test.js`: AC1, AC2, AC4, AC12
- `import.test.js`: AC3, AC5–AC11, AC14
- `storage.test.js`: AC13, AC15–AC22
- `static.test.js`: AC24, AC26

Run them with `node --test tests/`.

## Criteria tested here
- **AC1** – The backup text is indented, has only `version`/`todos` + `id`/`title`/`done`/`createdAt`, keeps the 3 titles and done states, and is named `todo-sao-luu-YYYY-MM-DD.json` (zero-padded). The "backed up" message contains 3. Calls `toBackupText`, `backupFileName`, `fill`, `MESSAGES.backedUp`.
- **AC2** (partial) – Backup and import make no `fetch`/`XMLHttpRequest`/`WebSocket`/`EventSource` calls. Calls `toBackupText`, `parseBackup`, `tooBigToImport`, `importBackup`.
- **AC3** – With no `todo.v1` key, the list loads empty with no read error, and the empty-list message names "Nhập từ file". Importing the AC1 file asks nothing, gives 3 todos, says 3, and survives a reload. Calls `store.load`, `MESSAGES.emptyList`, `confirmText` (expects `null`), `importBackup`.
- **AC4** – `MESSAGES.nothingToBackUp` is "Chưa có việc nào để sao lưu".
- **AC5 / AC6** – The question contains "Thay 12 (or 1) việc hiện có bằng 30 việc trong file?" and is asked before anything is written. Cancel keeps the old list in memory and after reload. Agree gives exactly the 30, none of the old ones, and survives reload. Calls `confirmText`, `importBackup`, `store.load`.
- **AC7** – A valid backup over 1 MB is refused: no question, list and storage unchanged, a message shown. Calls `MAX_IMPORT_BYTES`, `importBackup`.
- **AC8** – An unknown field in a todo, or at the top level, is refused. Calls `parseBackup`, `importBackup`.
- **AC9** – PNG bytes, plain text, an empty file, `null`, a bare array, missing or wrong-typed fields: each is refused with a message. Calls `parseBackup`, `importBackup`.
- **AC10** – A duplicate id, empty title, or `createdAt: "hôm qua"` refuses the whole file, with no partial list. Calls `parseBackup`, `importBackup`.
- **AC11** – The title `<img src=x onerror=alert(1)>` comes through exactly, survives reload, and a spied `alert` is never called. Calls `parseBackup`, `importBackup`.
- **AC12** – A backup of 5,000 todos with 200-character titles is over 1 MB and over `MAX_IMPORT_BYTES`, still holds every todo, and `tooBigToImport` returns true (false for a small one). `MESSAGES.backupTooBig` is the exact sentence.
- **AC13** – With storage full, the `persist` message contains "Hãy sao lưu ra file, rồi xoá bớt việc đã xong", `store.save` returns `'failed'`, and the new todo is gone after reload. Calls `persist`, `store.save`.
- **AC14** – Storage full, 12 todos, import 30 and agree: the 12 are returned, the message is the not-saved notice, and the 12 are there after reload. Calls `importBackup`.
- **AC15** – With `{hỏng` stored: `load`/`store.readError` report the read error, `STORE_KEY` is `todo.v1`, and `MESSAGES.unreadable` is the exact banner. Add, toggle and remove never write to `todo.v1`, and no new keys appear. It is still unreadable after reload. Calls `persist`, `store.save` (expects not `'saved'`).
- **AC16** – `{"a": 1}` is a read error, and adding a todo leaves the value as is.
- **AC17** – If `getItem` throws on open, it's a read error, and adding a todo makes no write at all.
- **AC18** – While unreadable, the backup holds exactly the two todos added, and `{hỏng` stays.
- **AC19** – Calls `confirmText` and `importBackup`. The read-error question is asked even with nothing on screen. Cancel keeps `{hỏng` and `readError`. Agree writes the 30 as an array and clears `readError`. A later `persist` returns a `null` message, and after reload there are 31 todos with no read error.
- **AC20** – The question contains the exact "…và 3 việc bạn vừa thêm (chưa lưu)…" wording. Cancel keeps the 3. Agree gives exactly the 30, clears `readError`, and survives reload.
- **AC21** – `{hỏng` with storage full, import and agree: still a read error, `{hỏng` kept, the screen keeps its old list, and the not-saved notice is shown (per the A20 answer). A later `persist` attempts no write.
- **AC22** – While unreadable, the AC7 and AC8 files are refused with no question, `{hỏng` is kept, and the read error stays.
- **AC24** – No `MESSAGES` value (raw or filled), no `confirmText` output, and no visible text or `aria-label`/`title`/`placeholder`/`alt` in `index.html` contains localStorage, JSON or console (`.json` is excluded per A11).
- **AC26** – `app/index.html` has no `<script src>` or `<link href>` pointing to another site (`data:` is allowed).

## Not testable here (need a browser or a person)
- **AC2** (the rest): turning the network off and watching the browser's Network panel.
- **AC4** (the rest): checking that no file download starts. That happens in `app.js`, which has no exports.
- **AC5**: that no Undo button appears.
- **AC11**: that the page shows the title via `textContent` and no alert box appears.
- **AC15**: that no dialog pops up and no empty-list line is shown.
- **AC19 / AC20**: that the banner visibly disappears. I check `store.readError` instead.
- **AC23**: that the "kept only in this browser" line means what the spec says. That needs a person to judge, and the spec fixes no wording.
- **AC25**: keyboard-only use and the screen reader.

## AMBIGUOUS marks
1. `helpers.js` `openApp`: `api.md` doesn't say how `store.js` exports things. The tests accept either `{ store, STORE_KEY }` or the store object itself with `STORE_KEY` on it.
2. AC1: it's unclear whether `MESSAGES.backedUp` uses `{n}` or `{m}` for the count, so the test fills both.
3. AC3: I read "chỉ tới nút 'Nhập từ file'" as the empty-list message naming that button.
4. AC4: the spec quotes the sentence without a full stop, so one at the end is allowed.
5. AC7: "1 MB" could be 1,000,000 or 1,048,576 bytes, so either is accepted.
6. AC14: AC14 only says an error is shown. I read F2 step 8 ("báo như F3") as requiring the F3 notice with its hint sentence.
7. AC15: curly quotes around "Nhập từ file" in the banner are treated as the same as the straight quotes in the spec.
8. AC17: reading throws only when the app opens. The fake storage is readable afterwards, so the test checks that the page's read-error state is what stops writes.
9. AC24: the three words are matched in any letter case.
10. AC26: "không có **thêm**" can't be compared to the old `index.html`, so the test requires no external script or link at all, which `policy-security@1#S4` also implies.
