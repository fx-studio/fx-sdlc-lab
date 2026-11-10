# R6c-pr-sua-phat-hien-1

Chạy 2026-11-10 16:08 ở gốc repo, chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Finding #1 of the weekly security scan (ops/scan/baseline.json, high/high, CWE-22, scripts/watch.py:141) was confirmed by a person and triaged fix-now by the security owner (Khoa): 'Watch job can append model output to any repo file via .. in the merge target'. Open one pull request with python3 scripts/pr.py that fixes only this: resolve the merge target and accept it only if it is a file directly inside intent/auto/. Add a unit test in ops/tests/ that shows intent/auto/../../CLAUDE.md is refused (run it failing first, then fixed). Run python3 -m unittest discover -s ops/tests and bash scripts/check.sh in the PR worktree, fill review/<n>/PR.md, commit on the PR branch, and stop. Do not merge.

## Tool call (23)

1. Read · file_path=<repo>/scripts/watch.py
2. Read · file_path=<repo>/scripts/pr.py
3. Glob · pattern=ops/tests/*
4. Read · file_path=<repo>/ops/tests/test_detect.py
5. Bash · command=python3 -c "import json;d=json.load(open('ops/scan/baseline.json'));f=d['findings'][0] if isinstance(d,dict) and 'findings' in d else d[0];print(json.dumps(f,indent=1,ensure_ascii=False))"
6. Grep · pattern=watch.py
7. Bash · command=python3 scripts/pr.py new watch-merge-target --title "Watch job: accept a merge target only directly inside intent/auto/ (scan #1, CWE-22)"
8. Write · file_path=<repo>/.worktrees/pr-11/ops/tests/test_watch_merge_target.py
9. Bash · command=python3 -m unittest discover -s <repo>/.worktrees/pr-11/ops/tests
10. Edit · file_path=<repo>/.worktrees/pr-11/scripts/watch.py
11. Bash · command=python3 -m unittest discover -s <repo>/.worktrees/pr-11/ops/tests
12. Bash · command=cd <repo>/.worktrees/pr-11 && bash scripts/check.sh 2>&1 | tail -n 8
13. Read · file_path=<repo>/review/11/PR.md
14. Bash · command=git log --oneline -3 --stat pr/10-flaky-generator -- review/
15. Bash · command=git log --oneline -6 --name-only --all -- review/10 review/9
16. Write · file_path=<repo>/review/11/PR.md
17. Bash · command=git add scripts/watch.py ops/tests/test_watch_merge_target.py
18. Bash · command=git commit -m "PR 11: watch job accepts a merge target only directly inside intent/auto/ (scan #1, CWE-22)

save_intent resolved nothing: intent/auto/../../CLAUDE.md passed the
startswith check and model text was appended to CLAUDE.md. Resolve the
target and require its parent to be intent/auto/. Unit test in
ops/tests/test_watch_merge_target.py (failed before, passes after).

Co-Authored-By: Claude Opus 5.5 <<email>>"
19. Bash · command=python3 scripts/pr.py show 11
20. Bash · command=mkdir -p review/11
21. Bash · command=cp <repo>/review/11/PR.md <repo>/review/11/base review/11/
22. Bash · command=git add review/11/PR.md review/11/base
23. Bash · command=git commit -m "PR 11: review/11/PR.md

Co-Authored-By: Claude Opus 5.5 <<email>>"

## Claude · 76 s

I opened PR 11 (`pr/11-watch-merge-target`, worktree `.worktrees/pr-11`) and committed on that branch. It is not merged.

**The fix** (`scripts/watch.py`, `save_intent`): the watch job now resolves the merge target the model gives it, including `..`, symlinks and absolute paths. It appends only if the result is an existing file directly inside `intent/auto/`. Any other target is not merged: the text is saved as a new intent in `intent/auto/` instead.

**The test** (`ops/tests/test_watch_merge_target.py`): it uses a temporary copy of the folder layout, so even the failing run before the fix could not write to the real `CLAUDE.md`. It has three cases:
- `intent/auto/../../CLAUDE.md` is refused.
- `intent/auto/sub/x.md` is refused, because it isn't directly inside `intent/auto/`.
- An open intent in `intent/auto/` is still merged as before.

**Results:**
- **Before the fix:** 2 of 10 tests failed for the right reason. The model's text was appended to `CLAUDE.md` (`'# rules\n\n## Update · simulated day 40 …' != '# rules\n'`) and to the subfolder file.
- **After the fix:** `python3 -m unittest discover -s ops/tests` gave `Ran 10 tests … OK`.
- **`bash scripts/check.sh` in the worktree:**
  ```
  ℹ tests 47
  ℹ pass 47
  ℹ fail 0
  == check: OK
  ```
  Two `.git/hooks/pre-push: Not a directory` lines print before it. They come from the shell start-up, because `.git` is a file in a worktree, not from the check.

**Commits:** `4896841` has the fix and the test. `db8d903` adds `review/11/PR.md` and `review/11/base`, with the same files left untracked in the main checkout. `scripts/pr.py` sized the PR at 63 lines in 2 files, risk **medium**, so it needs one code owner to review.

I touched nothing else, including scan findings #2–#4. Merging is up to a person.
