# R7a-hoi-truoc-song-song

Chạy 2026-10-27 11:39 ở gốc repo, chế độ quyền `plan`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Three pieces of work are waiting. Two engineers want to run them at the same time, each with its own Claude session in its own git worktree. Do not plan the work itself; answer only about running them in parallel.
A. Rejection wording: replace the five import rejection messages (M8, M9, M10, M11, M14 of plan/2026-10-19-khach-khong-mat-viec.md) with the UX owner's new wording, so each says why, that the list is kept, and what to do next (spec F2 step 4).
B. Import race: in app/app.js the import handler captures the current list before awaiting the file read; if the person adds a todo to an empty list while the file is being read, the import replaces it without asking. Fix it.
C. Due dates: spec/2026-10-19-han-chot-cho-viec.md (Status: draft).
For each pair (A+B, A+C, B+C): which files both would touch, whether they can run in parallel, and why. Then say which of A, B, C can start now at all. Read the code and the plan/spec files to answer; be specific (file and function).

## Tool call (16)

1. Bash · command=ls app tests spec plan intent
2. Read · file_path=<repo>/app/app.js
3. Read · file_path=<repo>/spec/2026-10-19-han-chot-cho-viec.md
4. Read · file_path=<repo>/app/backup.js
5. Grep · pattern=M8|M9|M10|M11|M14|^Status|Status:
6. Bash · command=ls -R demo/sdlc-3/runs/R7-linh-cau-tu-choi demo/sdlc-3/runs/R8-phan-hang demo/sdlc-3/runs/R3f-so-r0-r3
7. Grep · pattern=MESSAGES\.|nên chưa nhập|Không đọc được file|importBackup|current
8. Read · file_path=<repo>/demo/sdlc-3/runs/R7-linh-cau-tu-choi/transcript.md
9. Grep · pattern=import|test\(
10. Bash · command=ls scripts .claude/hooks
11. Read · file_path=<repo>/plan/2026-10-19-khach-khong-mat-viec.md
12. Read · file_path=<repo>/scripts/pre-commit
13. Read · file_path=<repo>/plan/2026-10-19-khach-khong-mat-viec.md
14. Read · file_path=<repo>/.claude/hooks/protect-paths.py
15. Read · file_path=<repo>/tests/app.test.js
16. Write · file_path=<home>/.claude/plans/three-pieces-of-work-unified-tulip.md

## Claude · 126 s

A and B can run in parallel now. C can't start. One finding on B first: the bug as described doesn't seem to happen. The real version of it is a different case.

## What each piece would touch

**A · Rejection wording**
- **`app/backup.js`:** the `MESSAGES` constants only (`emptyFile`, `notBackup`, `badTodo`, `fileTooBig`, `cannotReadFile`, lines 15–20). No logic changes.
- **`tests/backup.test.js`:** the two checks that compare the exact text, lines 237–238 (`emptyFile` = M8, `fileTooBig` = M11). The other tests refer to `MESSAGES.x` by name, so they keep passing.
- **The plan file:** rows M8–M11 and M14 of the wording table, lines 119–125. The plan is `Status: accepted`, so `protect-paths.py` blocks the agent and a person has to make this edit. `scripts/pre-commit` also requires a `plan/` change in the same commit.
- **Where the new wording comes from:** `demo/sdlc-3/runs/R7-linh-cau-tu-choi/transcript.md`. It isn't committed yet.

**B · Import race**
- **`app/app.js`:** the `$('#import').onchange` handler, lines 99–110.
- **Maybe `app/backup.js`:** `importBackup` (107–122), if the fix goes there.
- **Tests:** either `tests/app.test.js`, whose `loadApp` setup would need a fake `#import` input and a fake `ask`, or `tests/backup.test.js`.
- **The plan file:** the progress section's note (1) at line 255, edited by a person. Or the commit uses `PLAN_SKIP`.

**About the bug itself:**
- **The described case should already ask.** `const current = todos` keeps a reference to the same array, not a copy. `add()` does `todos.push(...)`, which grows that same array. The size check `confirmText(... current.length ...)` runs after `await file.text()` (`backup.js:118`). So adding a todo to an empty list during the read gives a length of 1, and the person is asked "Thay 1 việc…".
- **The snapshot only goes stale when `todos` is replaced by a new array during the read.** Two things do that: `remove()` (it uses `filter`) and another import finishing first (`app.js:107`).
- **The real failure is two imports at once.** Start with an empty list and pick a large file. Then pick a small file, which finishes first and fills the list. When the large file finishes, `current` is still the old empty array, so it replaces the list without asking.

The first step for engineer B should be a failing test. If the add case passes, the ticket and Khoa's note (1) describe the wrong case.

**C · Due dates**
- **`app/app.js`:**
  - `add()`, to set the new field;
  - `visible()`, to sort;
  - `render()`, for the date, the "Quá hạn" mark and the date box on each row;
  - the line-1 comment;
  - new handlers.
- **`app/index.html` and `app/style.css`.**
- **`app/backup.js`, which the spec doesn't list:** `TODO_KEYS`, `pick`, `isValidTodo`, `toBackupText`, and `parseBackup`'s `version !== 1` check. This follows from spec C2 and the plan's Risks (line 168).
- **Tests:** `tests/backup.test.js` and `tests/app.test.js`. The round-trip test and the `add()` check depend on the todo's shape.
- **A new plan:** `plan/2026-10-19-han-chot-cho-viec.md`.

## Pairs

| Pair | Files both touch | Parallel? | Why |
|---|---|---|---|
| **A+B** | The plan file, in different sections. Also `backup.js` and `backup.test.js`, but only if B fixes it inside `importBackup`. | **Yes** | The edits are in separate places: A changes constants, B changes the import function. B's tests use `MESSAGES` by name, so A's new text doesn't break them. B can avoid `backup.js` entirely by fixing only the handler in `app.js`. |
| **A+C** | `app/backup.js` (the messages and the file check) and `tests/backup.test.js` | Could be, but C isn't ready | C rewrites the file check and will likely add a rejection message (for example, a file from a newer version). That message has to follow A's pattern: why, the list is kept, what to do next. Land A first. |
| **B+C** | `app/app.js` (separate handlers, but the same file) and `tests/app.test.js` | Not a good idea, and C isn't ready | Both would extend the same test setup (`loadApp` and `fakeElement`): B needs a fake file input and `ask`, C needs a fake date box. That will conflict. If B fixes inside `importBackup`, it also collides with C's changes to the import code. |

## Which can start now

- **A: yes.** It's a wording change. A person commits the R7 transcript and edits rows M8–M11 and M14 of the plan in the same commit as the code.
- **B: yes.** It's a Small fix: plan mode, no plan file committed. It starts with the test that reproduces the bug, and the result may change what gets fixed.
- **C: no.**
  - The spec is still `Status: draft`, and questions A1–A15 and concerns C1–C3 are unanswered. C2 decides the backup file format.
  - The spec is also out of date. It calls the backup spec a draft and doesn't list `backup.js`.
  - After the spec is accepted it needs its own plan. The spec is marked high risk because it changes the stored data, so that plan is likely sized Large and needs the tech lead's approval before any code.

In each worktree the agent writes code and stops. A person commits and brings the changes into `main`, as CLAUDE.md requires.
