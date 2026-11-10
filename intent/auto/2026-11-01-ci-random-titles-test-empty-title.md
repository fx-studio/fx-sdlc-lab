# CI fails about one run in three since the new random-title backup test

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch ci_fail_rate level 2, simulated day 32 · Date: 2026-11-01
Triage: fix-now (Huy, ngày 37; cách ly PR 9 do agent mở ngày 36, sửa bộ sinh PR 10, xem ops/triage.md)

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

## Update · simulated day 33 · level 2 (watch job)

## Update: simulated day 33 (2026-11-02), watch ci_fail_rate level 2

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch ci_fail_rate level 2, simulated day 33 · Date: 2026-11-02

### New evidence

- Day 33: 1 of 4 runs failed (0.25), still on commit 3afe66d. No new commit has gone live since day 31 [ops/metrics/ci_fail_rate.jsonl day 33]
- The one failed run fails only test 32, "a list with random titles survives backup and import", at the same assertion (tests/backup.test.js:293). The other 46 of 47 tests pass, including test 18, the fixed round-trip [ops/ci/ci-day033-run3]
- That run's titles include **two** empty titles: `["yrôn","yà","","","cạ"]` [ops/ci/ci-day033-run3]
- So far all 4 failed runs (days 31–33) include at least one `""` title. Runs with no empty title have not failed [ops/ci/ci-day031-run2, ci-day031-run4, ci-day032-run2, ci-day033-run3]

### Diagnosis (unchanged, confidence still high)

The cause is the same as in the intent above: `randomTitle()` in `tests/backup.test.js` can return `""`, and `parseBackup` is right to reject it (app/backup.js:66). The test is wrong, not the app.

**Arithmetic over the whole window:** P(at least one empty title in a run) = 1 − (11/12)^5 ≈ 0.35. Over the 12 runs on days 31–33, that predicts about 4.2 failures, and we saw 4 (2 + 1 + 1). This is the rate the test bug predicts. It is not random noise, and nothing new has broken. Day 33 does not show a new problem. The test is still in the code, so it will keep failing about one run in three until someone fixes it.

**What would prove me wrong:** a failed run whose logged titles contain no `""` (or no whitespace-only title), or a failure in any test other than test 32.

### Open questions (new)

- On-call: this intent is still waiting for triage while CI stays red about one run in three. Should someone quarantine the test (add it to CLAUDE.md's flaky list) until the generator is fixed, so the alert does not fire again every day?

ACTIONS TAKEN: none

## Update · simulated day 34 · level 2 (watch job)

## Update: simulated day 34 (2026-11-03), watch ci_fail_rate level 2

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch ci_fail_rate level 2, simulated day 34 · Date: 2026-11-03

### New evidence

- Day 34: 1 of 4 runs failed (0.25), on the new commit ba139d3 [ops/metrics/ci_fail_rate.jsonl day 34]
- ba139d3 changes no file under `app/` or `tests/`. It only adds demo transcripts, CI logs, metric points, `ops/watch.jsonl` and this intent. So the new commit cannot have caused this failure or fixed the test [git show --stat ba139d3]
- The failed run fails only test 32, "a list with random titles survives backup and import", at the same assertion (tests/backup.test.js:293). The other 46 of 47 tests pass [ops/ci/ci-day034-run3.log]
- That run's titles include an empty title: `["rơháơêbásà","cđmáv","tãơdaqoxe","ôe",""]` [ops/ci/ci-day034-run3.log:199]
- All 5 failed runs from day 31 to day 34 include at least one `""` title [ops/ci/ci-day031-run2, ci-day031-run4, ci-day032-run2, ci-day033-run3, ci-day034-run3]

### Diagnosis (unchanged, confidence high)

The cause is the same as above. `randomTitle()` in `tests/backup.test.js` can return `""`, and `parseBackup` is right to reject that title (app/backup.js:66). The test is wrong, not the app.

**Arithmetic over days 31–34:** P(a run fails) = 1 − (11/12)^5 ≈ 0.35. Over 16 runs that predicts about 5.6 failures, and we saw 5 (2 + 1 + 1 + 1). That fits the test bug. Nothing new has broken.

**Why the alert keeps firing:** the metric has no baseline (sd 0, so it uses fixed thresholds), and the test bug has not been fixed. Until it is, this alert will fire about once a day and get merged into this intent each time.

**What would prove me wrong:** a failed run whose titles contain no `""` or whitespace-only title, or a failure in any test other than test 32.

### Open questions (new)

- On-call: this intent is still waiting for triage four days after the first failure. Can it be triaged now? Or should the test be quarantined in CLAUDE.md's flaky list so the watch job stops reopening this diagnosis every day?
- Tech lead: the next CI run still uses the test as it is. Should the fix (generate titles of length ≥ 1, not blank) go through a pull request now, ahead of triage?

ACTIONS TAKEN: none

## Update · simulated day 35 · level 2 (watch job)

## Update: simulated day 35 (2026-11-04), watch ci_fail_rate level 2

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch ci_fail_rate level 2, simulated day 35 · Date: 2026-11-04

### New evidence

- Day 35: 2 of 4 runs failed (0.5), still on commit ba139d3. No commit has gone live since day 34 [ops/metrics/ci_fail_rate.jsonl day 35]
- Both failed runs fail only test 32, "a list with random titles survives backup and import". The other 46 of 47 tests pass in each run [ops/ci/ci-day035-run2.log:192,308-311; ops/ci/ci-day035-run3.log:192,308-311]
- Both runs logged an empty title: `["ocsh","ăsoưnhađải","eđookvpeb","xưdhtà",""]` and `["ăd","đq","","e","bạiưby"]` [ops/ci/ci-day035-run2.log:199; ops/ci/ci-day035-run3.log:199]
- All 7 failed runs from day 31 to day 35 include at least one `""` title [ops/ci/ci-day031-run2 … ci-day035-run3, `python3 scripts/ci_log.py list`]
- The generator is still unfixed: `randomTitle()` still uses `n = Math.floor(Math.random() * 12)`, so `n` can still be 0 [tests/backup.test.js:280-283]

### Diagnosis (unchanged, confidence high)

The cause is the same as above. `randomTitle()` in `tests/backup.test.js:283` can return `""`, and `parseBackup` is right to reject that title (app/backup.js:66). The test is wrong, not the app. The jump to 0.5 does not point to a new problem.

**Arithmetic:** a run fails with p = 1 − (11/12)^5 ≈ 0.35. Over the 20 runs on days 31–35 that predicts about 7.0 failures, and we saw 7 (2+1+1+1+2). For a single day, P(≥ 2 of 4 runs fail) = 1 − 0.65⁴ − 4·0.35·0.65³ ≈ 0.44. So a day at 0.5 is expected about 4 days in 10. Within the known test bug, today's 0.5 is ordinary. Compared with the pre-day-31 baseline (0 out of many runs), it is not noise.

**What would prove me wrong:** a failed run whose titles contain no `""` or whitespace-only title, or a failure in any test other than test 32.

### Open questions (new)

- On-call: this intent has now been waiting for triage for 5 simulated days, and the alert has fired at level 2 every day. Can it be triaged? If the fix will not land soon, should test 32 go on CLAUDE.md's flaky list for now? It would come off once the generator only makes titles of length ≥ 1 that are not blank.
- Tech lead: the metric has no noise model in `ops/bands.yaml` ("not described") and uses fixed thresholds because sd is 0. Should a known, triaged cause like this one suppress repeat level-2 alerts for the same failing test? If so, a person would make that change to the bands or the watch job.

ACTIONS TAKEN: none

## Update · simulated day 36 · level 3 (watch job)

## Update: simulated day 36 (2026-11-05), watch ci_fail_rate level 3

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch ci_fail_rate level 3, simulated day 36 · Date: 2026-11-05

### New evidence

- Day 36: 2 of 4 runs failed (0.5), still on commit ba139d3. No commit has gone live since day 34 [ops/metrics/ci_fail_rate.jsonl day 36]
- Both failed runs fail only test 32, "a list with random titles survives backup and import". Each run has `fail 1` [ops/ci/ci-day036-run3.log:192,311; ops/ci/ci-day036-run4.log:192,311]
- Both runs logged an empty title: `["hvu","","ddyô","ktldndđâăạv","xôôyxyơêc"]` and `["xr","thêt","dãmhtáăm","",""]` [ops/ci/ci-day036-run3.log:199; ops/ci/ci-day036-run4.log:199]
- All 9 failed runs from day 31 to day 36 logged at least one `""` title [`python3 scripts/ci_log.py list`, ops/ci/ci-day031-run2 … ci-day036-run4]
- The generator has not been fixed: `n = Math.floor(Math.random() * 12)` can still be 0 [tests/backup.test.js:283]

### Diagnosis (unchanged, confidence high)

The cause is still `randomTitle()` at `tests/backup.test.js:283`, which can return `""`. `parseBackup` is right to reject that title (app/backup.js:66), so the test is wrong, not the app.

**Arithmetic:** a run fails with p = 1 − (11/12)^5 ≈ 0.35. Over the 24 runs on days 31–36 that predicts about 8.4 failures, and we saw 9. On a given day, P(≥ 2 of 4 runs fail) ≈ 0.44. Level 3 fired because two days in a row hit 0.5 against a baseline that was almost all zeros. It was not set off by a new fault.

**What would prove me wrong:** a failed run with no `""` or blank title, or a failure in any other test.

### Action through the level 3 gate

I opened local pull request **9** (`pr/9-quarantine-random-titles-test`, commit 8e43edf). I chose to quarantine the test rather than revert 9253a71, because the test is worth keeping once its generator is fixed:
- `tests/backup.test.js`: the test gets `{ skip: 'quarantined: …' }` plus a comment. The test body and the generator are not changed.
- `CLAUDE.md`: the test is added to the "Flaky tests (quarantined)" line.
- `review/9/PR.md`: the reason, the risk (low, no `app/` change) and the check output.

`bash scripts/check.sh` on the PR worktree: `ℹ tests 47 · ℹ pass 46 · ℹ fail 0 · == check: OK`. `tests` and `pass` differ by 1 on purpose: that is the skipped test. The PR is not merged. A person reviews it.

### Desired outcome / success criteria (added)

- Once PR 9 is merged, ci_fail_rate is 0.0 for 3 days in a row.
- The skip and the CLAUDE.md line are removed when the generator only makes titles of length ≥ 1 that are not blank. After that, `bash scripts/flaky.sh 10` passes.

### Open questions (new)

- Tech lead: merge PR 9 as it is, or fix the generator in the same PR instead and drop the skip?
- On-call: this intent has waited 6 simulated days without triage. Please triage it in `ops/triage.md` with PR 9 as the proposed fix.

ACTIONS TAKEN: opened local pull request 9 (`pr/9-quarantine-random-titles-test`, worktree `.worktrees/pr-9`). It skips the random-title backup test with a stated reason and lists it as quarantined in CLAUDE.md. I committed on the PR branch only (8e43edf), ran `bash scripts/check.sh` there (`tests 47, pass 46, fail 0, check: OK`), and stopped. Nothing was merged, nothing was deployed, and nothing on `main` was changed.

## Update · simulated day 37 · level 2 (watch job)

## Update: simulated day 37 (2026-11-06), watch ci_fail_rate level 2

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch ci_fail_rate level 2, simulated day 37 · Date: 2026-11-06

### New evidence

- Day 37: 1 of 4 runs failed (0.25). The commit is still ba139d3, and nothing new has gone live since day 34 [ops/metrics/ci_fail_rate.jsonl day 37]
- The failed run fails only test 32, "a list with random titles survives backup and import", at the same assertion. The run reports `tests 47, pass 46, fail 1, skipped 0` [ops/ci/ci-day037-run3.log:192,209,308-313]
- Its titles include an empty one: `["syvãnbpahà","iđ","","ănqmơcneo","àáaánâ"]` [ops/ci/ci-day037-run3.log:199]
- All 10 failed runs from day 31 to day 37 logged at least one `""` title [`python3 scripts/ci_log.py list`, ops/ci/ci-day031-run2 … ci-day037-run3]
- `main` still has the faulty generator, `n = Math.floor(Math.random() * 12)`, and the test has no skip [tests/backup.test.js:283]
- PR 9 (`pr/9-quarantine-random-titles-test`) is still an open local branch and has not been merged into `main`. That explains why the day-37 run has `skipped 0` [git branch --list "pr/*"]

### Diagnosis (unchanged, confidence high)

The cause is still the test, not the app. `randomTitle()` at `tests/backup.test.js:283` can return `""`. `parseBackup` is right to reject an empty title (app/backup.js:66).

**Arithmetic:** each run fails with p = 1 − (11/12)^5 ≈ 0.35. Over the 28 runs on days 31–37 that predicts about 9.8 failures, and we saw 10. For one day, P(exactly 1 of 4 runs fails) = 4·0.35·0.65³ ≈ 0.38, so day 37 is ordinary for the known bug. WE2/WE3 fire only because the baseline is almost all zeros (mean 0.036). Nothing new has broken.

**What would prove me wrong:** a failed run with no `""` or blank title, a failure in any other test, or a failure after PR 9 has been merged.

### Open questions (new)

- Tech lead / repo owner: PR 9 has waited one simulated day. Merging it, or fixing the generator so every title is at least 1 character and not blank, is the only thing that will stop this alert from firing daily.
- On-call: this intent has now waited 7 simulated days without a decision in `ops/triage.md`. Please triage it.

ACTIONS TAKEN: none
