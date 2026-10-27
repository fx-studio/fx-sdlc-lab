# R3d-sua-truoc-commit-b

Chạy 2026-10-27 11:12 ở gốc repo, chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

The backup/import change for plan/2026-10-19-khach-khong-mat-viec.md is written but not committed. Review settled two things before commit B; make exactly these changes and nothing else:
1. M12 wording (Linh decided, Mai confirmed it meets P4 and acceptance criterion 23). Replace the M12 sentence in app/index.html and in tests/static.test.js with exactly: "Danh sách chỉ được lưu trên trình duyệt này, nên xoá dữ liệu trang web, đổi trình duyệt hoặc đổi máy là mất, trừ khi bạn đã sao lưu ra file."
2. Khoa's review: isValidTodo in app/backup.js rejects whitespace-only titles and non-string ids. Add a test that pins what add() in app/app.js does today (trims the title, skips a whitespace-only title, makes a string id), so a backup the app itself made always imports again. Do not change app.js behaviour and do not loosen the validator. If a test cannot reach add() without changing app.js, say so and pick the smallest option; tell me what you picked.
Do not edit the plan (a person records these in its progress section). Run node --test before you finish and report the counts.

## Tool call (12)

1. Bash · command=ls tests && grep -n "M12\|trình duyệt" app/index.html tests/*.js | head -30 && cat app/app.js | head -120 && grep -n "isValidTodo" -A20 app/backup.js | head -40
2. Bash · command=head -5 app/app.js; grep -n "script" app/index.html; sed -n 1,40p tests/static.test.js; sed -n 1,40p tests/backup.test.js; grep -n "module.exports\|globalThis\|^function\|^const" app/backup.js app/store.js | head -40
3. Bash · command=sed -n 120,135p app/backup.js && sed -n 1,46p app/store.js | head -20 && node --version
4. Bash · command=python3 - <<'EOF'
old_html = 'Danh sách chỉ được lưu trên trình duyệt này. Đổi trình duyệt hoặc đổi máy là mất danh sách, trừ khi bạn đã sao lưu ra file.'
new = 'Danh sách chỉ được lưu trên trình duyệt này, nên xoá dữ liệu trang web, đổi trình duyệt hoặc đổi máy là mất, trừ khi bạn đã sao lưu ra file.'
for f in ['app/index.html', 'tests/static.test.js']:
    s = open(f, encoding='utf-8').read()
    assert s.count(old_html) == 1, f
    open(f, 'w', encoding='utf-8').write(s.replace(old_html, new))
EOF
git diff --stat -- app/index.html tests/static.test.js; grep -n "nên xoá" app/index.html tests/static.test.js
5. Read · file_path=<repo>/app/index.html
6. Read · file_path=<repo>/tests/static.test.js
7. Edit · file_path=<repo>/app/index.html
8. Edit · file_path=<repo>/tests/static.test.js
9. Write · file_path=<repo>/tests/app.test.js
10. Bash · command=node --test 2>&1 | tail -15
11. Edit · file_path=<repo>/tests/app.test.js
12. Bash · command=node --test 2>&1 | tail -10; git status --short

## Claude · 57 s

I made both changes, and `node --test` passes: **38 tests, 38 pass, 0 fail, 0 skipped.** Nothing is committed, and I didn't touch the plan.

**1. M12 wording.** The old sentence is replaced with Linh's exact text in `app/index.html:32` and in the AC23 test in `tests/static.test.js:25`.

**2. Test for add().** A test can't reach `add()` without changing `app.js`. It's a plain browser script with no exports, and it needs `document`, `store` and the functions from `backup.js` as globals.

- **What I picked:** a new file, `tests/app.test.js`, that runs the real, unchanged `app/app.js` in a `node:vm` sandbox. The sandbox has a minimal fake page, a fake store that records every list the app saves, the `backup.js` exports, and Node's `crypto`. This was the smallest option. The alternative was adding exports to `app.js`, which would change it.
- **The test submits the add form as a person would.** I did this because `add()` doesn't skip whitespace-only titles itself: the form's submit handler does (`if (input.value.trim()) add(input.value)`). Calling `add()` directly would have pinned the wrong thing.
- **Three new tests:**
  - The title is trimmed, and the id is a non-empty string.
  - Whitespace-only input (`'   '`, `'\t\n'`) saves nothing.
  - A list the app built goes through `toBackupText` then `parseBackup` and comes back `ok`, unchanged. This one ties directly to Khoa's point.
- **One limitation:** these tests depend on how `app.js` looks up page elements (`#add`, `#title`) and on its script-level globals. If those names change, the tests will break even if the behaviour hasn't.

`isValidTodo` and `app.js` are unchanged.
