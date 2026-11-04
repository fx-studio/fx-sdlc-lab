# PR 5 · Hạn chót cho việc (PR A của plan) · bản B, có dòng trần 400

Branch: `pr/5-han-chot-co-tran` · Base: `main` (20b4e8f) · Head: `6db27f1` (**nothing committed yet**, see "Blocked")

Spec: `spec/2026-10-19-han-chot-cho-viec.md` (accepted) · Plan: `plan/2026-10-19-han-chot-cho-viec.md` (accepted), **PR A, steps 1–3
only**. PR B (sao lưu `version: 2`) is not started. Size: Large (plan Q1).

## Why only steps 1–3

The 400-line ceiling in CLAUDE.md applies, and PR A as a whole will go well over it. CLAUDE.md says to split it into PRs in plan order,
each one green on its own. Step 3 (`due.js` and its tests) is the only part that can stand alone: no page loads `due.js` yet, so the
app behaves exactly as on `main`. The plan says steps 4 and 5 (`index.html`, `static.test.js`, `style.css`, `app.js`, the new flow
tests in `app.test.js`) **go in one commit**. That would be the next PR (`python3 scripts/pr.py new <slug> --base pr/5-han-chot-co-tran`).

**Decision needed (Khoa, plan owner):** steps 4–5 together will very likely be more than 400 lines on their own. The `app.js` changes
plus about 20 flow tests from the Proof table are the bulk. I did not start that PR, because one commit over 400 lines conflicts with the
ceiling, and splitting it departs from plan step 5. Possible splits, for a person to choose and write into the plan:
(a) accept one PR over 400 lines for steps 4–5; (b) step 4–5a: Undo machinery `offerUndo`/`clearUndo` + `save()`/`render()` split +
`#undo` button, with its tests (no date UI), then step 4–5b: date field, sort, overdue; (c) put the flow tests in a separate PR
right after the code (weaker: that code PR would ship without its proof).

## What changes (staged, not committed)

| File | Change |
|---|---|
| `app/due.js` (new, Q2) | `DUE_TEXT` (D1–D6, D8, D9; `{title}` / `{date}` placeholders), `isValidDueDate` (regex + `Date.UTC`/`getUTC*`), `localDateString` (local day, no `toISOString`), `isOverdue`, `formatDueDate` ("Hạn DD/MM/YYYY"), `sortByDue` (new array, valid dates ascending, missing or broken dates last, ties by original index). No DOM, no storage, no "localStorage" anywhere in the file. Conditional `module.exports` like `backup.js` |
| `tests/due.test.js` (new) | 10 tests, written by the `test-writer` subagent from the spec, the plan and the public names **before** `due.js` existed. Covers every `due.test.js` row in the plan's Proof table, with `TZ=Asia/Ho_Chi_Minh` |

Step 1 of the plan (re-grep): `store.(load|save|replace)|localStorage` in `app/` gives `app/app.js:3`, `app/backup.js:116`,
`app/backup.js:134`, `app/store.js`, the same as on 2026-11-04. PR 2 is not merged into `main`. No stop condition was hit.

test-writer flagged three ambiguities; the code follows these readings, so please confirm them:
1. Broken `dueDate` values sort together with "no due date", in original order (one group at the end), per A14/AC8.
2. D8 is three separate keys (`sortLabel`, `sortAdded`, `sortDue`); the test flattens values, so key names are not pinned.
3. D3 is stored as `'Hạn {date}'`; the exact output is pinned by the `formatDueDate` test.

## Blocked: the commit

`git commit` on this branch was refused by the plan-sync pre-commit hook:

```
pre-commit: this commit changes app/ (1 file) but no plan/ file.
  Update the plan in the same commit, or for a tiny change: PLAN_SKIP="<why>" git commit ...
```

I can't edit the plan: it is accepted, and hook `protect-paths` blocks writes to it. The plan also says the person who commits fills in
"Tiến độ". `PLAN_SKIP` is meant for trivial changes, and this is a Large one, so I didn't use it. **For a person:** in this worktree, add
the PR A Tiến độ line to the plan (for example "PR A: bước 1–3 ở PR 5 (`due.js` + test); bước 4–5 chờ quyết định tách PR"), then
commit it together with the two staged files.

## Not done here

`python3 scripts/review.py 5` and the `verifier` subagent were not run: there is no commit for them to review yet. Run them after the
commit. Manual checks T0–T10 belong to the PR that wires `due.js` into the page. Release: none.

## How it was checked

`bash scripts/check.sh` on the working tree (head `6db27f1` + the two staged files):

```
== test: node --test
ℹ tests 56
ℹ pass 56
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

Before `app/due.js` existed: `node --test tests/due.test.js` failed with `Error: Cannot find module '../app/due.js'`.

<!-- pr.py -->
## Size and risk (computed by scripts/pr.py)

184 lines in 4 files · risk **high** → 2 people, one of them the tech lead
