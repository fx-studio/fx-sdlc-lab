# R8-su-co-thanh-eval

Chạy 2026-10-29 14:57 ở gốc repo, chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Incident T-014 (tickets/T-014-loc-hien-danh-sach-trong.md) reached customers and was fixed in commit 2aa698d. Turn it into a permanent eval, in the same format as evals/tasks/*.json and evals/hidden/*.eval.js (read evals/check.py for the check types). The task starts from the code as it was before the fix and before its reproducing test (base 16d2846), and the prompt reads like the customer's report. The hidden test must check the requirement, not one particular fix. Prove it: it must fail on 16d2846 and pass on 2aa698d. You may use a temporary git worktree for that; remove it afterwards. Do not run the eval suite itself.

## Tool call (27)

1. Bash · command=ls evals evals/tasks evals/hidden
2. Read · file_path=<repo>/tickets/T-014-loc-hien-danh-sach-trong.md
3. Read · file_path=<repo>/evals/check.py
4. Read · file_path=<repo>/evals/tasks/E2-cau-tu-choi.json
5. Read · file_path=<repo>/evals/hidden/E2-cau-tu-choi.eval.js
6. Read · file_path=<repo>/evals/hidden/_harness.js
7. Read · file_path=<repo>/evals/tasks/E1-nhap-chong.json
8. Bash · command=git show 2aa698d
9. Bash · command=git show 3170517 --stat
10. Bash · command=git show 16d2846:app/app.js
11. Bash · command=git show 16d2846:app/index.html
12. Read · file_path=<repo>/evals/hidden/E1-nhap-chong.eval.js
13. Bash · command=grep -rn "no_test_edits" evals/results --include=*.json* -h | head -5; git show 16d2846:app/backup.js | grep -n "emptyList"
14. Grep · pattern=no_test_edits
15. Grep · pattern="note"
16. Write · file_path=<repo>/evals/tasks/E9-loc-danh-sach-trong.json
17. Write · file_path=<repo>/evals/hidden/E9-loc-danh-sach-trong.eval.js
18. Bash · command=git worktree add --detach <thư-mục-tạm> 16d2846
19. Bash · command=git worktree add --detach <thư-mục-tạm> 2aa698d
20. Write · file_path=<thư-mục-tạm>
21. Bash · command=node <thư-mục-tạm>
22. Edit · file_path=<thư-mục-tạm>
23. Bash · command=node <thư-mục-tạm>
24. Bash · command=git worktree remove --force <thư-mục-tạm>
25. Bash · command=git worktree remove --force <thư-mục-tạm>
26. Bash · command=git worktree list
27. Bash · command=bash scripts/check.sh

## Claude · 137 s

I've added T-014 as eval **E9-loc-danh-sach-trong**. Its hidden test fails on 16d2846 and passes on 2aa698d. Nothing is committed.

**Files**
- `evals/tasks/E9-loc-danh-sach-trong.json`: starts from `base: 16d2846`, which is before the fix and before its reproducing test (3170517). The prompt is Vy's report word for word from the ticket, introduced as "Customer report from the feedback form (Vy):" and ending "Fix it.", the same ending E1 uses. It doesn't hint at where the bug is or how to fix it. The checks match E1's: `tests_pass`, `hidden_test`, `no_test_edits`, and `only_paths app/ tests/ plan/`.
- `evals/hidden/E9-loc-danh-sach-trong.eval.js`: uses the existing `_harness.js` and doesn't change it.

**What the hidden test checks**
- When the list has todos, `#empty` must be either hidden, or showing a sentence that is different from the empty-list sentence this same build shows for a truly empty list. Either way it must not mention importing a backup. Comparing against the build's own empty-list sentence means rewording `MESSAGES.emptyList` doesn't break the test.
- It covers Vy's case (4 open todos, tab "Đã xong"), the mirror case (all todos done, tab "Chưa xong"), and the move back to "Tất cả".
- A truly empty list must still show the sentence in every tab, so "always hide `#empty`" doesn't pass.
- It doesn't look at the count line. 2aa698d also fixed T-013, and this eval is only about T-014.

**Proof** (temporary worktrees, test copied into `evaltmp/` the way `check.py` does it):
```
16d2846 (exit 1)  ℹ tests 3  ℹ pass 1  ℹ fail 2
  AssertionError: tab done: does not show the empty-list sentence
  AssertionError: tab open: does not show the empty-list sentence
2aa698d (exit 0)  ℹ tests 3  ℹ pass 3  ℹ fail 0
```
On the base, the test fails for the reason in the ticket. I also tried a different fix in the base worktree: keep `#empty` visible but show a sentence that depends on the filter ("Chưa có việc nào đã xong."). It passes 3/3, so the test doesn't require 2aa698d's particular design.

Both temporary worktrees are removed. `git worktree list` still shows eight older `eval-E*` worktrees in `$TMPDIR` from earlier eval runs. I didn't create them, so I left them alone.

**Not done:** `bash scripts/check.sh` was refused for lack of approval, so I can't paste its output. The two new files are outside `tests/` and `node --test` doesn't pick up `*.eval.js`, so the 44 tests shouldn't change. Please run the check before you commit. I didn't run the eval suite, as you asked.
