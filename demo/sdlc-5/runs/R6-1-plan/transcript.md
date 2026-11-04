# R6-1-plan

Chạy 2026-11-04 10:06 ở gốc repo, chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Plan the implementation of the accepted spec spec/2026-10-19-han-chot-cho-viec.md, following the Build section of CLAUDE.md (size the change; a plan has four sections: Files that change, Order of work, Risks, Proof). Read the code first. Write the plan to plan/2026-10-19-han-chot-cho-viec.md with Status: draft, in Vietnamese like plan/2026-10-19-khach-khong-mat-viec.md. Do not write any code: the tech lead approves the plan first.

## Tool call (26)

1. Read · file_path=<repo>/spec/2026-10-19-han-chot-cho-viec.md
2. Read · file_path=<repo>/plan/2026-10-19-khach-khong-mat-viec.md
3. Glob · pattern={app/**,tests/**,scripts/check.sh}
4. Read · file_path=<repo>/app/app.js
5. Read · file_path=<repo>/app/index.html
6. Read · file_path=<repo>/app/backup.js
7. Read · file_path=<repo>/app/store.js
8. Read · file_path=<repo>/app/style.css
9. Read · file_path=<repo>/tests/app.test.js
10. Read · file_path=<repo>/tests/static.test.js
11. Read · file_path=<repo>/scripts/check.sh
12. Grep · pattern=A16|A17|A18|A19|C4
13. Grep · pattern=S1|version
14. Grep · pattern=version: 1|version !== 1|TODO_KEYS|"x": 1|x: 1
15. Read · file_path=<repo>/tests/backup.test.js
16. Read · file_path=<repo>/demo/sdlc-5/runs/R6-0-cap-nhat-spec/transcript.md
17. Grep · pattern=A1[6-9]|C4|Hoàn tác
18. Bash · command=ls <repo>/plan <repo>/.git/hooks <repo>/scripts
19. Bash · command=git -C <repo> branch -a
20. Read · file_path=<repo>/scripts/pre-commit
21. Read · file_path=<repo>/review/2/watch.md
22. Grep · pattern=plan|accepted|Status
23. Bash · command=python3 <repo>/scripts/pr.py list
24. Bash · command=bash scripts/check.sh
25. Write · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
26. Bash · command=bash scripts/check.sh

## Claude · 302 s

I wrote the plan to `plan/2026-10-19-han-chot-cho-viec.md`. It is `Status: draft`, in Vietnamese, and uses the same layout as the backup plan. I didn't change any code and didn't commit anything.

**Size: Large** (my proposal; Khoa decides, Q1). The change alters the shape of stored data and the backup file format, adds a new script file in an order a test pins, and ships as two PRs on a high-risk spec.

**Main design choices Khoa or Linh need to check:**
- **Q2: date logic goes in a new `app/due.js`.** It has no DOM code, like `backup.js`, and holds the date check, "today" from the device clock, overdue, the "Hạn DD/MM/YYYY" format and sorting. Script order becomes `store` → `due` → `backup` → `app`, so `tests/static.test.js` changes. The other option is to keep the logic in `app.js` and test it through `vm`.
- **Q3: the date box on each row saves on `change` but redraws the list only on blur.** When typing with the keyboard, Chrome fires `change` after each part of the date. A full redraw at that point would rebuild the box mid-typing: typing "15" ends up as day 01, and editing the day can lose the month and year. This needs Linh's agreement.
- **Q6: sorting by due date never reorders the saved array.** If it did, "Thứ tự thêm" (the order todos were added) would be lost for good.
- **Q7: PR 2 (renaming a todo) isn't merged yet.** It also changes `render()` and has its own Undo. Whichever PR merges first, the other should reuse its Undo rather than add a second one.

**Two PRs:**
- **PR A (due dates):** `due.js`, `app.js`, `index.html`, `style.css`, plus tests. It starts with the `test-writer` subagent writing acceptance tests from the spec before any code exists.
- **PR B (backup `version: 2`):** `backup.js`. Two existing tests in `tests/backup.test.js` pin the old behaviour, and the plan lists them for update: the "version 1, four fields" test at line 37, and the case at line 76 that rejects `version: 2`.

**Open questions:** the spec is accepted, but A16–A19 and C4 have no answers yet. The plan has a table showing which PR each one blocks:
- **A16** blocks PR A.
- **A18, A19 and C4** block PR B. C4 has no default, because the spec doesn't choose an option.
- **A17** blocks production. Until PR B ships, a backup silently drops due dates, so PR A shouldn't go out alone.

**Rollback risk:** reverting PR A is safe for data. Reverting PR B means the backup files users already downloaded (`version: 2`) can't be imported until PR B comes back.

`bash scripts/check.sh` on the current tree:
```
ℹ tests 46
ℹ pass 46
ℹ fail 0
== check: OK
```
