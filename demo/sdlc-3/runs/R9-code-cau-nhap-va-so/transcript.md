# R9-code-cau-nhap-va-so

Chạy 2026-10-27 11:58 ở gốc repo, chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

The accepted spec spec/2026-10-19-khach-khong-mat-viec.md was revised (see its 'Revisions after acceptance' section, commit 65fae52). Make these two changes in the code for plan/2026-10-19-khach-khong-mat-viec.md, nothing else:
1. F2 step 8: when saving after an import fails, show this new sentence (Linh's exact wording) instead of the shared not-saved message; the add/toggle/delete path keeps the old one:
   Chưa nhập được file. Danh sách trên màn hình vẫn nguyên nhưng có thể chưa được lưu, nên đừng tải lại trang. Hãy sao lưu ra file, xoá bớt việc đã xong rồi thử lại.
2. Numbers in app sentences (Linh's rule): 1,000 and above get a dot as thousands separator (1.000, 2.001, 12.500); below 1,000 plain (12, 999). This applies to the counts filled into messages ({n}, {m}); years and dates are not affected. Tests must cover 999, 1000, 2001 and 12500.
Say which size this is. Do not edit the plan or the spec. Run node --test and report the counts.

## Tool call (18)

1. Bash · command=git show 65fae52 --stat
2. Glob · pattern={app,tests}/**
3. Bash · command=git show 65fae52 -- spec/2026-10-19-khach-khong-mat-viec.md
4. Read · file_path=<repo>/app/app.js
5. Read · file_path=<repo>/plan/2026-10-19-khach-khong-mat-viec.md
6. Read · file_path=<repo>/app/backup.js
7. Read · file_path=<repo>/tests/backup.test.js
8. Read · file_path=<repo>/demo/sdlc-3/runs/R9-linh-so-va-cau/transcript.md
9. Grep · pattern=fill\(|notSaved|việc chưa xong
10. Read · file_path=<repo>/demo/sdlc-3/runs/R9-linh-chot-lai/transcript.md
11. Edit · file_path=<repo>/app/backup.js
12. Edit · file_path=<repo>/app/backup.js
13. Edit · file_path=<repo>/app/backup.js
14. Edit · file_path=<repo>/app/backup.js
15. Edit · file_path=<repo>/tests/backup.test.js
16. Edit · file_path=<repo>/tests/backup.test.js
17. Edit · file_path=<repo>/tests/backup.test.js
18. Bash · command=node --test

## Claude · 60 s

Both changes are in, and `node --test` passes: **41 tests, 0 failures, 0 skipped** (up from 39 because of the two new tests).

**Size: Small.** All the code is in one file, `app/backup.js`, plus its tests in `tests/backup.test.js`. No other file changed. I didn't edit the plan or the spec, and I didn't commit anything.

**1. Failed import save (F2 step 8)**
- There's a new message, `MESSAGES.importNotSaved`, with Linh's exact sentence. It matches her final wording in `demo/sdlc-3/runs/R9-linh-chot-lai/`.
- When saving after an import fails, `importBackup` now shows this new sentence.
- Add, toggle and delete still show the old `MESSAGES.notSaved` sentence, and its existing test still checks that.
- New tests check the exact wording, check that it differs from the old sentence, and check both import failure cases (saved list readable, and saved list unreadable).

**2. Thousands separator**
- A new function `formatCount` adds a dot every three digits from 1,000 up. `fill()` now uses it for every `{n}` and `{m}`, so all the count messages follow the rule: backed up, imported, and the three confirmation questions.
- Years and dates never go through `fill()`, so they don't change. A test checks that the backup file name still reads `todo-sao-luu-2026-10-27.json`.
- Tests cover 0, 1, 12, 999, 1000, 2001, 12500 and 1234567, both on their own and inside real message sentences.

**For whoever commits this:**
- **The code no longer matches the accepted plan.** Three places in the plan need a person to update them in the same commit (the pre-commit hook requires it):
  - the Thiết kế section, `importBackup` step 5 (lines 88–89), still says `'failed'` returns M3;
  - the Proof row at line 212 still expects M3;
  - the Câu chữ table has no row yet for the new sentence or for the number rule.
- **One count is still written without dots.** The line under the list (`app/app.js:52`, `${open} việc chưa xong`) shows a number but isn't one of the `{n}`/`{m}` messages, so I left it as you asked. Linh said every sentence with a number should follow the same rule, so at 1,000 or more open todos it will show "1000". Linh or Khoa should decide whether it's in scope.
