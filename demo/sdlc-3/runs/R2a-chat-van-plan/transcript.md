# R2a-chat-van-plan

Chạy 2026-10-27 09:33 ở gốc repo, chế độ quyền `plan`, tiếp session trước. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Before I accept, five questions about your plan. Answer each briefly, then revise the plan wherever an answer shows a gap:
1. Which files change, and is any of them a surprise?
2. Which flow that works today could this change break?
3. Which step is riskiest, and how would we know it broke?
4. Which test fails if that step is done wrong?
5. Is there a simpler way you considered and dropped?

## Tool call (8)

1. Read · file_path=<home>/.claude/plans/attached-intent-2026-10-19-khach-khong-m-playful-hoare.md
2. Edit · file_path=<home>/.claude/plans/attached-intent-2026-10-19-khach-khong-m-playful-hoare.md
3. Edit · file_path=<home>/.claude/plans/attached-intent-2026-10-19-khach-khong-m-playful-hoare.md
4. Edit · file_path=<home>/.claude/plans/attached-intent-2026-10-19-khach-khong-m-playful-hoare.md
5. Edit · file_path=<home>/.claude/plans/attached-intent-2026-10-19-khach-khong-m-playful-hoare.md
6. Edit · file_path=<home>/.claude/plans/attached-intent-2026-10-19-khach-khong-m-playful-hoare.md
7. Edit · file_path=<home>/.claude/plans/attached-intent-2026-10-19-khach-khong-m-playful-hoare.md
8. Edit · file_path=<home>/.claude/plans/attached-intent-2026-10-19-khach-khong-m-playful-hoare.md

## Claude · 85 s

Answering your questions showed three gaps in the plan, and I've revised it. The biggest: if `app.js` wired up saving wrong, no automated test would have failed. The plan is still in the same file, and the repo hasn't been touched.

**1. Which files change, and is any a surprise?**
The files are `app/store.js`, `app/app.js`, `app/index.html`, `app/style.css`, the new `app/backup.js`, and three new test files. The surprise is `backup.js`, which the spec doesn't list (that's still Q2). One more surprise I hadn't written down: script order. If `backup.js` is missing or loads after `app.js`, the app throws at startup and the whole page is blank.
- **Added:** the plan now says `backup.js` goes between `store.js` and `app.js`, and a test checks the order.

**2. Which flow that works today could break?**
Opening the app and seeing your saved tasks, then adding, ticking and deleting with every change saved. If `load()` wrongly decides valid saved data can't be read, every customer would see an empty list and a warning banner, and nothing would be saved after that. A second, quieter break: a customer downloads a backup that the app's own import then rejects, and only finds out on the new phone.
- **Added:** a round-trip test proving that any list the app can create imports back unchanged.
- **Added:** the empty-list line now depends on the total number of tasks, not on the current filter. Otherwise "Đã xong" with no finished tasks would start showing it, which it doesn't today.

**3. Which step is riskiest, and how would we know it broke?**
Steps 1 and 4: the new storage code and wiring it into the app. Besides the false alarm above, the danger is overwriting unreadable saved data. That happens if a write goes around `store`, or if import calls `save` instead of `replace`. While the saved list is unreadable, `save` does nothing, so the app would say "Đã nhập" and nothing would actually be saved. In the old plan, only the manual browser checks would have caught that.
- **Changed:** the import and save decisions move out of `app.js` into two functions with no page code, `persist` and `importBackup`. `app.js` now only draws the result.
- **Changed:** `store.readError` is the only copy of the "can't read" state, so the banner and the write lock can't get out of step.

**4. Which test fails if that step is done wrong?**
Before the revision, none did. Now:
- `store.test.js` fails if a valid saved list is reported as unreadable.
- `backup.test.js` fails if `importBackup` calls `save`, or calls `replace` after a cancel or a rejected file. It also fails if a failed write doesn't give back the old list plus the "not saved" message.
- `static.test.js` fails if `app.js` mentions `localStorage` at all.

**5. A simpler way considered and dropped?**
Yes, three:
- **Keep everything in `app.js` and check it by hand.** This matches the spec's file list, but Node can't load `app.js`, so the most dangerous logic would have no tests.
- **Keep the "can't read" flag in `app.js` only.** Less change to storage, but one missed check would overwrite the unreadable data.
- **A fake page environment for the tests.** With no packages allowed, it would be bigger than the code it tests.

The plan now has a short section listing these.

The six questions from the first draft are still open: size, adding `backup.js`, how many bytes 1 MB is, files with an empty list, `"null"` in storage, and manual checks for browser-only criteria. Once they're answered and you accept the plan, I'll write it to `plan/2026-10-19-khach-khong-mat-viec.md` as `Status: draft`.
