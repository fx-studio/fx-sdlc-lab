# R2-day032-ci_fail_rate

Chạy 2026-11-10 15:52 bởi scripts/watch.py (không người khởi động phiên), quyền: `Read,Glob,Grep,Skill,Bash(python3 scripts/ci_log.py:*),Bash(git log:*),Bash(git show:*),Bash(git diff:*),mcp__deploy__status`. Nguyên văn, chỉ che đường dẫn máy và email. Luồng thô: `stream.jsonl`.

## Prompt

You were invoked by the watch job (scripts/watch.py), non-interactive. No person started this session and nobody is
watching it. Use the `diagnose` skill.

Metric `ci_fail_rate` reached **level 2** (diagnose, read-only) on simulated day 32 (2026-11-01). The clock of this demo is simulated: a "day"
is one collection run.

Noise model of this metric (ops/bands.yaml): not described

Detection (scripts/detect.py, no model):
```json
{
 "metric": "ci_fail_rate",
 "day": 32,
 "date": "2026-11-01",
 "value": 0.25,
 "level": 2,
 "mode": "fixed",
 "rules": [
  "no baseline (sd is 0): mean of last 3 = 0.2500 vs fixed thresholds"
 ],
 "mean": 0.0,
 "sd": 0.0,
 "baseline_points": 21,
 "release_changes": [
  {
   "day": 31,
   "from": "a5351c7",
   "to": "3afe66d"
  }
 ],
 "action": "diagnose",
 "simulated_clock": true
}
```

Last points of ops/metrics/ci_fail_rate.jsonl (oldest first):
```
{"day": 23, "date": "2026-10-23", "value": 0.0, "runs": 4, "failed": 0, "failing_tests": [], "commit": "a5351c7"}
{"day": 24, "date": "2026-10-24", "value": 0.0, "runs": 4, "failed": 0, "failing_tests": [], "commit": "a5351c7"}
{"day": 25, "date": "2026-10-25", "value": 0.0, "runs": 4, "failed": 0, "failing_tests": [], "commit": "a5351c7"}
{"day": 26, "date": "2026-10-26", "value": 0.0, "runs": 4, "failed": 0, "failing_tests": [], "commit": "a5351c7"}
{"day": 27, "date": "2026-10-27", "value": 0.0, "runs": 4, "failed": 0, "failing_tests": [], "commit": "a5351c7"}
{"day": 28, "date": "2026-10-28", "value": 0.0, "runs": 4, "failed": 0, "failing_tests": [], "commit": "a5351c7"}
{"day": 29, "date": "2026-10-29", "value": 0.0, "runs": 4, "failed": 0, "failing_tests": [], "commit": "a5351c7"}
{"day": 30, "date": "2026-10-30", "value": 0.0, "runs": 4, "failed": 0, "failing_tests": [], "commit": "a5351c7"}
{"day": 31, "date": "2026-10-31", "value": 0.5, "runs": 4, "failed": 2, "failing_tests": ["a list with random titles survives backup and import"], "commit": "3afe66d"}
{"day": 32, "date": "2026-11-01", "value": 0.25, "runs": 4, "failed": 1, "failing_tests": ["a list with random titles survives backup and import"], "commit": "3afe66d"}
```

Level 2 means diagnose only: you have read tools. Do not try to change anything. The intent you return is saved by the watch job.

Agent-written intents still waiting for triage (0 of max 5):
(empty)

If an open intent above is about the same problem, merge into it instead of writing a new one.

Reply in exactly this shape:
- First line: a JSON object, either {"action": "new", "slug": "<short-kebab-name>"} or {"action": "merge", "into": "intent/auto/<file>.md"}.
- Then the intent in Markdown (for "merge": only what is new, it is appended as an update).
- Last line: `ACTIONS TAKEN: <none, or what you did through the level 3 paths>`.


## Tool call (10)

1. Skill · skill=diagnose
2. Bash · command=git log --oneline a5351c7..3afe66d
3. Bash · command=python3 scripts/ci_log.py list
4. Bash · command=git show 9253a71
5. Bash · command=python3 scripts/ci_log.py view ci-day031-run2
6. Grep · pattern=title
7. Bash · command=python3 scripts/ci_log.py view ci-day031-run4
8. Bash · command=python3 scripts/ci_log.py view ci-day032-run2
9. Read · file_path=<repo>/app/backup.js
10. Grep · pattern=trim\(\)

## Claude · 33 s

{"action": "new", "slug": "ci-random-titles-test-empty-title"}

# CI fails about one run in three since the new random-title backup test

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch ci_fail_rate level 2, simulated day 32 · Date: 2026-11-01

## Problem

Since commit 3afe66d went live, developers see CI go red on roughly one run in three, with no change to the code they touched. Each time it is the same test, and a re-run often turns it green. A flaky red CI teaches people to re-run and ignore failures, so real regressions in backup/import could get through. Users of the app are not affected: no app code changed.

## Evidence

- CI fail rate was 0.0 every day from day 23 to day 30 on commit a5351c7, then 0.5 (2/4) on day 31 and 0.25 (1/4) on day 32 on commit 3afe66d [ops/metrics/ci_fail_rate.jsonl days 23–32]
- All 3 failed runs fail only one test, "a list with random titles survives backup and import". The other 46 of 47 pass [ops/ci/ci-day031-run2, ci-day031-run4, ci-day032-run2]
- The only change to tests or app in a5351c7..3afe66d is 9253a71, which adds that test. The other commits touch the demo, ops, the skill and scripts [git log a5351c7..3afe66d]
- The test builds 5 titles with `randomTitle()`, where `n = Math.floor(Math.random() * 12)`, so `n` can be 0 and the title can be `""` [git show 9253a71, tests/backup.test.js]
- Every failing run printed an empty title: `["unbhyr","kvuáqiyqà","","ooãqãâk","rtạ"]`, `["ơê","","dăảđsnrlả","da","inôôcpeđc"]`, `["ă","lvtacdeư","","smãoc","ntư"]` [ops/ci/ci-day031-run2, ci-day031-run4, ci-day032-run2]
- `isValidTodo` rejects a title that is empty after trim (`t.title.trim() !== ''`), so `parseBackup` returns `ok: false` for the whole file [app/backup.js:66]
- The app never creates an empty title: the add form skips a blank input and trims the title [app/app.js:73, app/app.js:9]

## Diagnosis

**Cause:** a wrong test, not wrong code. `tests/backup.test.js` `randomTitle()` (added in 9253a71) can return `""` (`n = 0`, chance 1/12 per title). The app can never make that title, and `parseBackup` correctly rejects it (app/backup.js:66, as specified by "parseBackup rejects the whole file when one todo is bad"). So the test's claim ("whatever a person can type") is false for this input.

**Arithmetic:** P(a run has at least one empty title) = 1 − (11/12)^5 ≈ 0.35. Expected failures over 4 runs ≈ 1.4 per day. Observed 2 and 1, which matches. The jump from 0 to this rate is not noise: it starts exactly with the commit that added the test, and 100 % of the failing runs contain `""`.

**Confidence:** high. To be surer: run the test with `Math.random` seeded so `n = 0`, and check that it fails every time, and that with `n ≥ 1` it passes over many runs.

**Ruled out:** a regression in backup.js (backup.js did not change in the window, and test 18, the fixed round-trip, passes every run). Environment or Node flakiness (the failure is always the same assertion, at tests/backup.test.js:293).

**Fix pointer:** make the generator produce only titles the app can create (length ≥ 1, not whitespace-only), or use a fixed seed. Per CLAUDE.md, a person decides this, since it changes a committed test.

## Desired outcome

CI is green again on every run unless the code is really broken, and the random-title test stays as real coverage of backup round-trips.

## Success criteria

- ci_fail_rate back to 0.0 (under its band) for at least 3 days in a row after the fix
- The random-title test passes over many repeated runs (for example `bash scripts/flaky.sh 10`)

## Open questions

- Tech lead: fix the generator (min length 1), or seed the randomness so that failures can be reproduced?
- Product owner: can an existing todo be edited to an empty title anywhere? (I found only the add path.) If so, the backup reject would be a real user bug, not just a test bug.
- On-call: should the test be quarantined in CLAUDE.md's flaky list until the fix lands?

ACTIONS TAKEN: none
