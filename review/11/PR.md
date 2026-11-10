# PR 11 · Watch job: accept a merge target only directly inside intent/auto/ (scan #1, CWE-22)

Branch: `pr/11-watch-merge-target` · Base: `main` (2c487db)

Spec: (none) · Plan: (none) · Size: **small** (one well-located bug, one file + its test)

Source: weekly security scan, finding #1 (`ops/scan/baseline.json`, high/high, CWE-22, `scripts/watch.py:141`), confirmed by a
person, triaged **fix-now** by the security owner (Khoa).

## What changes

- `scripts/watch.py` `save_intent`: the merge target `into` comes from model output. Before, it was accepted when the string
  started with `intent/auto/` and the path was a file, so `intent/auto/../../CLAUDE.md` passed and the watch job appended model
  text to `CLAUDE.md` (or any repo file). Now the target is resolved (`..`, symlinks, absolute paths) and accepted only if it is
  an existing file **directly inside** `intent/auto/` (`resolved.parent == AUTO.resolve()`). Anything else is not merged: the
  text is saved as a new intent in `intent/auto/`, as with any other unusable control line.
- `ops/tests/test_watch_merge_target.py` (new): runs `save_intent` against a temporary ROOT/AUTO, so the test never writes to the
  real repo.
  - `intent/auto/../../CLAUDE.md` is refused: CLAUDE.md unchanged, a new intent is written in `intent/auto/`.
  - `intent/auto/sub/x.md` is refused (not directly inside).
  - `intent/auto/<open intent>.md` is still merged (normal path unchanged).

Not changed: anything else in `watch.py`, the other scan findings (#2–#4).

## How it was checked

Test first, before the fix (fails for the right reason: the model text is appended to CLAUDE.md):

```
FAIL: test_dotdot_out_of_intent_auto_is_refused (test_watch_merge_target.MergeTarget.test_dotdot_out_of_intent_auto_is_refused)
AssertionError: '# rules\n\n## Update · simulated day 40 · level 2 [26 chars]NE\n' != '# rules\n'
FAIL: test_subfolder_of_intent_auto_is_refused (test_watch_merge_target.MergeTarget.test_subfolder_of_intent_auto_is_refused)
AssertionError: 'x\n\n## Update · simulated day 40 · level 2 (watch job)\n\nINJECTED LINE\n' != 'x\n'
Ran 10 tests in 0.046s
FAILED (failures=2)
```

After the fix, `python3 -m unittest discover -s ops/tests` in `.worktrees/pr-11`:

```
..........
----------------------------------------------------------------------
Ran 10 tests in 0.048s

OK
```

`bash scripts/check.sh` in `.worktrees/pr-11` (last lines):

```
== test: node --test
ℹ tests 47
ℹ pass 47
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

(Two `.git/hooks/pre-push: Not a directory` lines printed before it come from the shell start-up in a worktree, where `.git`
is a file; they are not part of the check.)

<!-- pr.py -->
## Size and risk (computed by scripts/pr.py)

63 lines in 2 files · risk **medium** → 1 code owner, who reads the plan
