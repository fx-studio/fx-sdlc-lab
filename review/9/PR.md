# PR 9 · Quarantine the flaky random-title backup test

Author: fx-sdlc-agent (watch job, ci_fail_rate level 3, simulated day 36 · 2026-11-05) · Status: waiting for a person's review

## Why

CI has failed 1–2 of 4 runs every day since day 31 (0.5 on days 35 and 36), always on the same test, "a list with random titles
survives backup and import". `randomTitle()` in `tests/backup.test.js` can return `""` (`n = Math.floor(Math.random() * 12)`
can be 0). The app never creates an empty title, and `parseBackup` is right to reject one (app/backup.js:66). So the test is wrong,
not the app. All 9 failed runs (days 31–36) logged a `""` title. Full diagnosis:
`intent/auto/2026-11-01-ci-random-titles-test-empty-title.md`.

## What changes

- `tests/backup.test.js`: the test gets `{ skip: 'quarantined: …' }` plus a comment. The test body and generator are **not** changed.
- `CLAUDE.md`: the test is added to the "Flaky tests (quarantined)" line.

I picked quarantine, not a revert of 9253a71. A revert would delete the test, and the test is good coverage once its generator is
fixed. Fixing the generator (titles of length ≥ 1, not blank) changes a committed test. That is a person's decision (tech lead),
so this PR does not do it.

## Risk

Low. No file under `app/` changes. Cost: backup round-trips with random titles are not covered until the skip is removed. The
fixed round-trip test still runs.

## Check (run on this branch, after the last change)

```
== test: node --test
ℹ tests 47
ℹ pass 46
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

`tests` (47) ≠ `pass` (46) because one test is skipped on purpose. That is the quarantine.

## For the reviewer

- Tech lead: merge the quarantine as it is, or fix the generator in this PR instead (then drop the skip and the CLAUDE.md line)?
- Follow-up: remove the skip and the CLAUDE.md line once the generator is fixed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
