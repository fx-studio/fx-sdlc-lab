# R3f-so-r0-r3

Chạy 2026-10-27 11:23 ở gốc repo, chế độ quyền `plan`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Read-only comparison; do not change any file. Two implementations of spec/2026-10-19-khach-khong-mat-viec.md exist:
- R0: Claude coded straight from the intent, no spec Q&A and no plan. Its whole diff is demo/sdlc-3/runs/R0-lam-luon/diff.patch (against commit fdf3791). It left no tests in the repo.
- R3: Claude coded from the accepted plan. It is commits eae2c2c and 8300aaa (git show them; app/ and tests/).
For each acceptance criterion in the spec (numbered list), give one row: criterion number, R0 meets / does not / cannot tell, R3 meets / does not / cannot tell, and a few words of evidence (file:line). Judge by reading code only; say 'cannot tell' when it needs a browser. Then three lines: how many criteria each meets, the decisions R0 made by itself that the spec later decided differently, and anything R0 did better than R3. Be exact; do not round in R3's favour.

## Tool call (9)

1. Bash · command=cat -n spec/2026-10-19-khach-khong-mat-viec.md
2. Bash · command=wc -l demo/sdlc-3/runs/R0-lam-luon/diff.patch && cat -n demo/sdlc-3/runs/R0-lam-luon/diff.patch
3. Bash · command=awk '/^\+\+\+ /{f=$2; next} /^--- /{next} /^diff /{next} /^index /{next} /^@@/{match($0,/\+[0-9]+/); n=substr($0,RSTART+1,RLENGTH-1); next} /^-/{next} {printf "%s:%d %s\n", f, n, substr($0,1); n++}' demo/sdlc-3/runs/R0-lam-luon/diff.patch | grep -E '^\S+:[0-9]+ \+' | cut -c1-170
4. Bash · command=git show --stat eae2c2c 8300aaa | cat; git diff fdf3791 8300aaa --stat -- app tests | cat
5. Bash · command=for f in app/store.js app/backup.js app/app.js app/index.html app/style.css; do echo "=== $f"; git show 8300aaa:$f | cat -n; done; git diff 8300aaa HEAD --stat -- app tests | cat
6. Bash · command=git diff 8300aaa HEAD --quiet -- app tests && echo SAME_AS_HEAD; sed -n 13p <(awk '/^\+\+\+ b\/app\/index.html/{p=1} p' demo/sdlc-3/runs/R0-lam-luon/diff.patch | grep load-error); git show fdf3791:app/app.js | grep -n textContent; grep -n "throw\|readError\|unreadable\|banner" tests/*.js | head -40
7. Bash · command=grep -o 'hidden>.*</p>' demo/sdlc-3/runs/R0-lam-luon/diff.patch | head -3; sed -n 60,80p tests/store.test.js; grep -n "banner\|unreadable\|empty" tests/app.test.js tests/static.test.js | head
8. Bash · command=ls demo/sdlc-3/runs/R0-lam-luon/; git log --oneline -3 fdf3791 | cat; git show fdf3791:spec/2026-10-19-khach-khong-mat-viec.md 2>/dev/null | head -5; head -60 demo/sdlc-3/runs/R0-lam-luon/transcript.md 2>/dev/null
9. Bash · command=git diff fdf3791 HEAD -- spec/ intent/ | cat; git log --oneline fdf3791..HEAD -- spec intent | cat

## Claude · 143 s

**Before the table, a correction to the premise.** R0 did not work from the intent alone. Its prompt was "Implement spec/2026-10-19-khach-khong-mat-viec.md" (`demo/sdlc-3/runs/R0-lam-luon/transcript.md`). Its base commit `fdf3791` is the commit where the spec was accepted, and `git diff fdf3791 HEAD -- spec/ intent/` is empty. So R0 had the same accepted spec as R3, word for word. What it skipped was the plan.

I read code only and changed no files. R3's `app/` and `tests/` at `8300aaa` are identical to HEAD, so the R3 line numbers below are current. R0 line numbers are positions in the files after its patch is applied.

| # | R0 | R3 | Evidence |
|---|---|---|---|
| 1 | meets | meets | Both: indented JSON, only the four fields, file name `todo-sao-luu-YYYY-MM-DD.json` in local time, "Đã sao lưu N việc." R0 `app.js:91-102`; R3 `backup.js:58-66`, `app.js:84-96` |
| 2 | meets | meets | Neither has fetch or XHR; both use a Blob URL only |
| 3 | meets | meets | No key gives an empty list; empty line hidden only when there are items or a read error; empty list gives no confirm. R0 `store.js:16`, `app.js:75,147`; R3 `store.js:15`, `app.js:55`, `backup.js:96` |
| 4 | meets | meets | R0 `app.js:87-89`, exact text; R3 `backup.js:6`, adds a final "." |
| 5 | meets | meets | R0 `app.js:146,150-158,179-189`; R3 `backup.js:97,119-121`, `app.js:59-67`. Esc and Huỷ both mean cancel |
| 6 | meets | meets | Same code paths as 5: the confirm fires for any list of 1 or more |
| 7 | meets | meets | Size checked before reading. R0 `app.js:161`; R3 `backup.js:109` |
| 8 | meets | meets | Exact-key check. R0 `app.js:125`; R3 `backup.js:50` |
| 9 | meets | meets | A JSON.parse failure is rejected. R0 `app.js:115-117`; R3 `backup.js:75-79` |
| 10 | meets | meets | R0 `app.js:127-128`; R3 `backup.js:51-54,86` |
| 11 | meets | meets | Neither changed the existing `textContent` rendering. R0 `app.js:66`; R3 `app.js:46` |
| 12 | meets | meets | Download first, then the exact sentence. R0 `app.js:99-100` (Blob byte size); R3 `app.js:96`, `backup.js:68-70` (TextEncoder byte count) |
| 13 | meets | meets | Both messages contain the required sentence. R0 `app.js:14,39-40`; R3 `backup.js:8,101-103` |
| 14 | meets | meets | A failed write leaves the list unchanged. R0 `app.js:184-187`; R3 `backup.js:120` |
| 15 | meets | meets | Banner text is exact in both; writes are skipped during a read error. R0 `index.html:13`, `app.js:34,73-75`; R3 `backup.js:22-24`, `store.js:25`, `app.js:53-55` |
| 16 | meets | meets | Non-array counts as a read error. R0 `store.js:23`; R3 `store.js:19` |
| 17 | meets (code) | meets (code) | A throwing read is caught in R0 `store.js:12-14` and R3 `store.js:13-19`. R0 has no test. R3's test covers only `load()` throwing (`tests/store.test.js:67-69`), not the banner and not "no write after add" in the throwing case |
| 18 | meets | meets | Export uses the on-screen `todos`. R0 `app.js:91`; R3 `app.js:86` |
| 19 | meets | meets | Read error is cleared only after a successful write. R0 `app.js:144,184-190`; R3 `backup.js:94`, `store.js:30-33` |
| 20 | meets | meets | R0 `app.js:145`; R3 `backup.js:95` |
| 21 | meets | meets | A failed write keeps the read-error state, and later adds still skip. R0 `app.js:184-187,34`; R3 `store.js:32,25` |
| 22 | meets | meets | Validation runs before the confirm. R0 `app.js:161-177`; R3 `backup.js:109-117` |
| 23 | meets | meets | R0 `index.html:32`; R3 `index.html:32` (says "dữ liệu trang web" instead of "dữ liệu trình duyệt") |
| 24 | meets | meets | No user-visible string contains those words. R0's `accept=".json,…"` is a filter attribute, not app text |
| 25 | cannot tell | cannot tell | Needs a real keyboard and screen-reader run. R0 uses a button that clicks a hidden input (`index.html:30-31`); R3 uses a visually hidden input inside a label (`index.html:30`, `style.css:16-19`). Both have a `<dialog>` with `aria-labelledby` and a `role="status"` area |
| 26 | meets | meets | R0 adds no tags; R3 adds only the local `<script src="backup.js">` (`index.html:42`) |

- **Count:** each meets 25 of 26. Each has one "cannot tell", criterion 25. On criterion 17, R3's code meets it and its tests cover only part of it; R0's code meets it and it has no test.
- **Decisions R0 made that the spec later decided differently:** none. R0 had the final accepted spec, and its code quotes the spec's answers exactly (A16 banner, A19 confirm wording, C2 sentence, A20 failure path). Its own choices fell where the spec is silent: the `accept` filter, the button that triggers a hidden input, revoking the download URL at 0 ms, and adding a likely cause ("có thể vì trình duyệt đã hết chỗ") to the not-saved message.
- **Where R0 did better than R3:**
  - **Rejection messages:** spec F2 step 4 asks each rejection to say why and what to do next. Every R0 rejection message does both (`app.js:136-140`). Three of R3's do not suggest a next step: `fileTooBig`, `notBackup`, `badTodo` (`backup.js:16-18`). Two do not say the list was kept: `emptyFile`, `cannotReadFile`.
  - **Damaged-file reason:** R0 names the cause (duplicate, missing title, wrong date).
  - **Exact wording:** R0 matches the spec's "Chưa có việc nào để sao lưu" exactly.
  - **Size and fit:** R0 used about 290 diff lines in the four files the spec lists. R3 added `backup.js`.
  - In the other direction, R3 handles the iOS Safari download risk that R0's 0 ms revoke leaves open (`app.js:94-95`), and it leaves 38 tests in the repo.
