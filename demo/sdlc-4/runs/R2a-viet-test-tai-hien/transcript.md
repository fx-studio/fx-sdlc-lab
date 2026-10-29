# R2a-viet-test-tai-hien

Chạy 2026-10-29 14:28 ở gốc repo, chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Tickets T-013 and T-014 (tickets/) report two bugs. Follow 'Fixing a bug' in CLAUDE.md: first write tests that reproduce both bugs, run them, and show that each fails for the right reason. Do not fix the code yet; a person will commit the tests first.

## Tool call (10)

1. Bash · command=ls tickets tests app
2. Read · file_path=<repo>/tickets/T-013-dem-sai-khi-loc.md
3. Read · file_path=<repo>/tickets/T-014-loc-hien-danh-sach-trong.md
4. Read · file_path=<repo>/app/app.js
5. Read · file_path=<repo>/tests/app.test.js
6. Bash · command=git show 16d2846 --stat -p -- app
7. Edit · file_path=<repo>/tests/app.test.js
8. Edit · file_path=<repo>/tests/app.test.js
9. Bash · command=node --test tests/app.test.js
10. Bash · command=bash scripts/check.sh 2>&1 | tail -n 12

## Claude · 41 s

I've written two tests in `tests/app.test.js` that reproduce T-013 and T-014. Both fail on the current code, each for the reason its ticket describes. The code is not fixed yet.

**What I added**
- **Two helpers in `loadApp`:** `filterBy(f)` clicks a filter tab through the real `#filters` handler, and `emptyShown()` reads whether `#empty` is visible. No existing test changed.
- **T-013 test** (`tests/app.test.js:101`): loads 5 todos, 2 of them done, the same case as the ticket. The count line must read "3 việc chưa xong" on every tab: Tất cả, Đã xong, Chưa xong, then back to Tất cả.
- **T-014 test** (`tests/app.test.js:113`): loads 4 todos with none done. The empty-list message must stay hidden on the "Đã xong" tab, and also on the "Chưa xong" tab when every todo is done. It must still show when the list really is empty.

I took the expected behaviour from commit 16d2846, which planted both bugs. Before it, the count and the empty-list message both used the whole list, and the old comment said so: "Based on the whole list, not the filter".

**Why each fails for the right reason**
```
✖ open-todo count line counts the whole list, whatever the filter (T-013)
  AssertionError: tab "Đã xong"
  + '0 việc chưa xong'
  - '3 việc chưa xong'

✖ empty-list message only when the whole list is empty, not when a filter hides everything (T-014)
  AssertionError: tab "Đã xong" with no done todos
  true !== false
```
- **Not a broken fake page:** in both tests the first assertion, on the "Tất cả" tab, passed. Each test only fails after the switch to "Đã xong".
- **T-013:** the line reads "0 việc chưa xong", exactly what the ticket reports. This is because `app/app.js:51` counts `visible()` instead of `todos`.
- **T-014:** the "Chưa có việc nào" message is shown, as the ticket reports. This is because `app/app.js:55` checks `visible().length` instead of `todos.length`.

**Full check, as expected before the fix**
```
ℹ tests 44
ℹ pass 42
ℹ fail 2
== check: FAILED
```
The other 42 tests still pass.

**Next step:** after you review and commit `tests/app.test.js`, the fix is two lines in `app/app.js` (lines 51 and 55), sized Small. I haven't committed anything or touched `app/`.
