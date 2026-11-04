# PR 2 · /watch-pr report

Branch `pr/2-doi-ten-viec`, head **03ba05d**. Rounds: no review existed, so watch-0 was the first review; then 2 rounds of fixes
(watch-1, watch-2). The loop stopped after watch-2: its only Important finding is a sizing decision for a person (below), and the check is OK.
Every bug fix began with a test that failed for the reason the finding gave. That test and the fix are in one commit.

## Findings

### watch-0 (head 80c5c4a): 5 Important, 2 Nit

| # | Sev | Finding | Outcome |
|---|---|---|---|
| 1 | Important | The wrong todo is renamed when a filter is on | **fixed** 248f4ac: `rename()` takes the id, like `toggle`/`remove` |
| 2 | Important | The new title is written with innerHTML (S3) | **fixed** fce9b44: message goes through `show()` (`textContent`); `<b>` dropped, title in quotes |
| 3 | Important | The rename message hides a failed save (U1) | **fixed** 1b6ae87: `commit()` returns `persist()`'s result; rename speaks only after a real save (not `failed`, not `skipped`) |
| 4 | Important | A confirm dialog on a single-item action (U2) | **fixed** 7ef34f0: no `confirm()`; rename at once + "Hoàn tác" button for 10 s in `#message` (`offerUndo`) |
| 5 | Important | Renaming cannot be started from the keyboard (U5) | **fixed** 5a6d21b: title has `tabIndex 0`; Enter or F2 opens the edit box |
| 6 | Nit | The edit box stays open when focus leaves it | **left**: save-on-blur or cancel-on-blur is a behaviour choice; the reviewer also says "should be decided and written down" |
| 7 | Nit | No test for the new behaviour, and the size label is disputed | Tests: **fixed** (8 tests added across the commits). Size: **Needs a person** (below) |

### watch-1 (head 5a6d21b): 3 Important, 4 Nit

| # | Sev | Finding | Outcome |
|---|---|---|---|
| 1 | Important | Double-clicking a title also ticks or unticks the todo | **fixed** c79b997: the title cancels its own clicks (`preventDefault`), so the wrapping `<label>` never reaches the checkbox. Bug was in the original PR. Side effect: a single click on the title no longer ticks the todo (the checkbox still does) |
| 2 | Important | Sized as Small, but it is a Medium feature with no committed plan | **Needs a person** (below) |
| 3 | Important | CLAUDE.md's healthy check output (tests 44) is out of date, and so is the PR's proof | **fixed** 03ba05d: CLAUDE.md now says 52/52. PR.md's check block replaced with a real run on 03ba05d (`review/` is not tracked, so no commit) |
| 4 | Nit | Text typed in the edit box is thrown away silently on blur | **left**: same as watch-0 #6 |
| 5 | Nit | Enter during Vietnamese input-method composition saves a half-typed name | **fixed** 0f4711c: keys ignored while `e.isComposing` |
| 6 | Nit | Keyboard focus is lost after Enter or Esc in the edit box | **left**: rows carry no id, so restoring focus means changing the row markup; and it is a choice where focus goes (the title or the Undo button) |
| 7 | Nit | Undo holds a reference to the old todo object | **fixed** 8265ec7: Undo finds the todo by id and does nothing if it is gone; the button removes itself on click |

### watch-2 (head 03ba05d): 1 Important, 5 Nit (loop stopped here, nothing fixed after this review)

| # | Sev | Finding | Outcome |
|---|---|---|---|
| 1 | Important | Sized as Small, but the change is Medium and has no committed plan | **Needs a person** (below). The stale size block it mentions is now refreshed by `pr.py` (202 lines in 3 files) |
| 2 | Nit | Keyboard focus is lost after saving or cancelling a rename | **left**: same as watch-1 #6 |
| 3 | Nit | Enter on an empty name does nothing and says nothing | **left**: treat it like Esc, or show a message: a wording/behaviour choice |
| 4 | Nit | An open edit box has no blur handling | **left**: same as watch-0 #6 |
| 5 | Nit | Renaming to the same name reports a change and offers Undo | **left**: trivial (`if (title.trim() === old) return render();`). Found in the last review, after the loop stopped |
| 6 | Nit | Undo gives no feedback | **left**: needs new wording ("Đã hoàn tác."?), which is a person's call |

No finding I disagree with.

## Needs a person

1. **Size: Small or Medium?** (watch-0 #7, watch-1 #2, watch-2 #1). PR.md says Small, so it has no plan. After review the change
   is a small feature: `app.js` +60 lines plus an Undo mechanism that U2 requires. Under the CLAUDE.md table that reads as Medium, which
   needs `plan/<name>.md` accepted *before* code. I did not write a plan after the code, and I did not re-size the PR. A person decides:
   either accept Small, or ask for a draft plan (Files · Order · Risks · Proof) to accept and check this PR against.
2. **Undo design** (watch-0 #4). U2 asks for an Undo, and I added it in `app.js` only: a "Hoàn tác" button after the message, gone after 10 s
   or at the next message. `remove()` (delete) still has no Undo, as on `main`. The wording and where the button sits need a UX check.
3. **A single click on the title no longer ticks the todo** (side effect of c79b997). Confirm this is acceptable.
4. **CLAUDE.md is now in the diff** (03ba05d, 2 lines). That alone raises the risk label from medium to **high**. If you would rather keep
   this PR at medium, drop 03ba05d and update the count on `main` yourself.
5. Nits left for a decision: blur behaviour, focus after Enter/Esc, empty Enter, same-name rename, Undo feedback.

## Last check (head 03ba05d)

```
== test: node --test
ℹ tests 52
ℹ pass 52
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

Waiting for: 2 people, one of them the tech lead (risk **high** in PR.md, raised from medium because the PR touches CLAUDE.md).
