# PR 4 · Hạn chót cho việc (PR A của plan) · bản A, không có dòng trần

Branch: `pr/4-han-chot-khong-tran` · Base: `main` (20b4e8f) · Head: `1af70df` (code `5ccd951`, then tests only)

Spec: `spec/2026-10-19-han-chot-cho-viec.md` (accepted) · Plan: `plan/2026-10-19-han-chot-cho-viec.md` (accepted), **PR A only**.
PR B (sao lưu `version: 2`, `app/backup.js`) is not in this PR. Size: Large (plan Q1). Risk: high (spec).

## What changes

Người dùng đặt được hạn chót khi thêm việc và trên từng dòng, thấy "Hạn DD/MM/YYYY" và "Quá hạn", xếp theo hạn chót, bỏ hạn chót có
"Hoàn tác" 10 giây. Code follows the plan's "Thiết kế"; no departure from the plan.

| File | Change |
|---|---|
| `app/due.js` (new, Q2) | `isValidDueDate` (`Date.UTC` + `getUTC*`), `localDateString` (local day), `isOverdue`, `formatDueDate`, `sortByDue` (new array, original index as tie-break), `DUE_TEXT` (D1–D6, D8, D9). No DOM, no storage |
| `app/app.js` | Comment line 1. `add(title, dueDate)` adds the key only for a valid date. `setDue` on `change`: saves only a valid, different date, updates that row in place (Q3). `clearDue` on `blur` when the field is empty: D5 + Undo if the todo had a date when the field got focus, silent if it was set during this focus, nothing if the stored value is broken (A14). One Undo for the app: `offerUndo(message, restore)` / `clearUndo()`; `show()` always clears Undo (A16, Q7). Undo click → restore, save, render, D9 or D7 (Q4, Q5). `#sort` (not remembered, A11). `render(focusTarget)` keeps focus on the same control of the same todo (AC9), using `relatedTarget` when called from `blur` |
| `app/index.html` | `<label>Hạn chót <input type="date" id="due">` in the add form; `<label>Xếp theo <select id="sort">` next to the filters (wrapped in `#view`); `<button id="undo" hidden>Hoàn tác</button>` in `#notices`; `<script src="due.js">` between `store.js` and `backup.js` |
| `app/style.css` | Wrapping form/rows for narrow screens, date and overdue styles (`#a4161a`, about 7:1 on the page background, plus the word "Quá hạn"), Undo button |
| `tests/due.test.js` (new) | 33 tests, written by the `test-writer` subagent from spec + plan + public names **before** `due.js` existed; ran red on `Cannot find module '../app/due.js'` |
| `tests/app.test.js` | Harness extended (fake rows, focus, `setAttribute`, fixed `Date` at 06:00 10/11/2026 UTC+7, fake timers, `saveResult`). Old test cases unchanged. 18 new flow tests: every PR A row of the plan's Proof table, plus re-sort-on-leave and `$&` in a title |
| `tests/static.test.js` | **Changed a test that pinned old behaviour (planned):** script order is now `store, due, backup, app`. Added: `due.js` in the "only store touches storage" loop, no `toISOString` in `app.js`/`due.js`, labels "Hạn chót"/"Xếp theo" with the two options and the `#undo` button, `dueDate` in the banned visible words |

Small choices the plan did not spell out (reviewer, please look):
- `autocomplete="off"` on `#sort` and `#due`, and `app.js` sets `#sort` to `added` at start: Firefox restores form values on reload, which would show "Hạn chót" while the list is in added order (A11).
- `withTitle()` fills `{title}` with a function replacer so `$&`, `$1` in a title stay as typed (D2, D5); `fill()` is not used for titles because it formats numbers.
- A `rendering` guard: `blur` does nothing while `render()` is removing rows (some browsers blur a removed field).
- "Sao lưu ra file" also hides the Undo button, because it calls `show()` (plan: "`show()` (mọi lần hiện câu mới) gọi `clearUndo()`"). A16 does not mention export either way.

Things a person should check (not fixed here, outside the plan or need a browser):
- **Focus after "Hoàn tác":** the button hides itself after the click, so keyboard focus falls to the page. T8.
- **Mouse click right after editing a date:** blur redraws the list (Q3) on `mousedown` of the next click; if that click is on another row's checkbox or "×", the browser may drop the click because its target was replaced. Keyboard Tab is handled (AC9 test). T3/T8 on desktop.
- **Plan "Tiến độ" not updated in this commit.** The plan is accepted, so I cannot edit it (hook `protect-paths`), and the plan says the person who commits fills it in. The plan-sync pre-commit hook (`.git/hooks/pre-commit`) did not fire on `5ccd951` although the commit changes `app/` without `plan/`. Please check why it did not run (executable bit / `core.hooksPath`), and add the Tiến độ line for PR A.
- Manual steps T0–T10 of the plan are all "chưa thử": T0 first. Release: `dev`/`staging` only; no `production` until PR B is merged (A17).

## Review and verifier (advisory)

`python3 scripts/review.py 4 --label review-a1` on `5ccd951` → `review/4/review-a1/`: **2 Important · 3 Nit**.

| # | Finding | What I did |
|---|---|---|
| 1 Important | Redrawing on `blur` (plan Q3) replaces every row between `mousedown` and `click`, so a click on another row's checkbox or "×" right after picking a date with the mouse is dropped (and rows may move under the pointer when sorted by due date) | **Not fixed: it needs a plan change.** "Vẽ lại ở blur" is Q3 (Khoa · Linh). Proposal for the plan: on leaving a date field, redraw only if the visible order can change (`sort === 'due'`); otherwise the row is already updated in place (also after `clearDue`). When sorted, redraw after the pending click has finished, not on `blur`. Add an app test mousedown→blur→click. Owner: Khoa (plan), Linh (UX) |
| 2 Important | Commit `5ccd951` changes `app/` without the plan's Tiến độ line; the plan-sync pre-commit did not run | **For a person:** add the PR A Tiến độ line on this branch; find out why `.git/hooks/pre-commit` did not run for this worktree. I make no more `app/` commits on this PR |
| 3 Nit | CLAUDE.md "App architecture" still says `store.js` → `backup.js` → `app.js` | Proposed line for a person: "loaded `store.js` → `due.js` → `backup.js` → `app.js` … `due.js` is DOM-free, storage-free date logic (tested in Node)" |
| 4 Nit | Focus falls to the page after pressing "Hoàn tác" (button hides itself) | Not fixed (outside the plan). Suggestion: focus the restored todo's date field if visible. T8 |
| 5 Nit | `Date.UTC` reads years 0–99 as 19xx, so a two-digit year typed as `0026-…` is rejected; an invalid date in `#due` at submit is dropped without a message | Not fixed: the plan specifies this validation; rejecting year 0026 is the intended result. The silent drop in the add form is a wording question for Linh |

Verifier subagent: its Bash calls were denied, so it only read the code (no run). It found no departure from the plan and two
test gaps, both closed in `1af70df` (tests only): the broken `"abc"` value is still there on the next save; set-then-clear in one
focus with a failing save shows D7 and no Undo.

## How it was checked

`bash scripts/check.sh` on head `1af70df`:

```
== test: node --test
ℹ tests 102
ℹ pass 102
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

Before code: `node --test tests/due.test.js tests/app.test.js` failed on `Error: Cannot find module '../app/due.js'` (both files);
`tests/static.test.js` failed on the script order and on the missing "Hạn chót" label before `index.html` changed.

<!-- pr.py -->
## Size and risk (computed by scripts/pr.py)

950 lines in 7 files · ⚠ over 400 lines: split it in the order of the plan · risk **medium** → 1 code owner, who reads the plan
