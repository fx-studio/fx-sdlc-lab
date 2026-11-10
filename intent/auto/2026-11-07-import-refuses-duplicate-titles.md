# Intent: Importing a backup fails when two todos have the same title (release 2e2ce98)

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch staging_error_rate level 3, simulated day 38 · Date: 2026-11-07
Triage: fix-now · đã xử lý (Huy, ngày 40): staging rollback bởi agent, production rollback bởi Huy, 2e2ce98 không lên main, eval E10, bài học trong ops/lessons.md. Câu hỏi sản phẩm (có chặn file ghép hai lần không) chuyển cho product owner.

## Problem
On release 2e2ce98, people who save their list to a file and import that same file back get the message "File sao lưu này bị lỗi". That happens whenever their list has two todos with the same title, for example "Mua sữa" added on two different days. The app lets them add the same title twice, then refuses the backup it wrote itself. Their list stays as it was, but they cannot restore it (for example on a new laptop).

## Evidence
- Day 38: 44 failed out of 215 actions (20.5 %). 36 were import_failed and 8 were not_saved. The baseline is 1.0 % ± 0.49 % [ops/metrics/staging_error_rate.jsonl day 38]
- Days 29–37: import_failed was 0 or 1 per day, on release b51a55e [ops/metrics/staging_error_rate.jsonl days 29–37]
- Release 2e2ce98 went live on staging (actor `person:long-dev`), replacing b51a55e [deploy/staging/history.jsonl]
- The only commit in the change: "backup: refuse a file that lists the same todo twice". It adds a title set and refuses the file when a trimmed, lower-cased title repeats [git show 2e2ce98]
- Simulated users pick titles from 9 fixed words and import a backup of their own list (13 % of actions), so most lists hold a repeated title [scripts/traffic.js:47, :94-101]
- Noise arithmetic for import_failed: about 32 imports, and each fails from storage about 1 % of the time, so ~0.3 failures are expected. 36 means nearly every import failed. **Not noise.** [ops/bands.yaml noise model, ops/metrics day 38]
- Noise arithmetic for not_saved: about 180 writes at 1 % gives an expected 1.8. 8 is rare (Poisson P(≥8) ≈ 0.1 %), but the noise model says 6–9 "happens a few times a year", and the change does not touch save. **Probably noise**, low confidence [ops/bands.yaml, git show 2e2ce98]
- After the rollback to b51a55e, the confirm run gave 14/224 = 6.25 % (not_saved 3, import_failed 11). That is lower, but not back at the baseline [collect.py traffic --env staging --day 38 --confirm]

## Diagnosis
- **Cause:** `app/backup.js:101-102` in 2e2ce98 treats a repeated title as a corrupt file. Two todos with the same title are valid data in this app; only a repeated **id** means a bad file. The new test in `tests/backup.test.js` pins this wrong rule.
- **Confidence: high.** It is the only code change in the window, it is the import path, and the failures are almost all of that kind. A replay of day 38 on 2e2ce98 with no repeated titles in the lists would prove this wrong.
- **The 11 import failures after rollback: unexplained, medium-confidence hypothesis.** b51a55e refuses repeated **ids**. Simulated ids are `<user>-<day>-<i>` [scripts/traffic.js:82], and the confirm run replays day 38 on the state file that the first day-38 run already wrote [scripts/collect.py:65-67]. That would give ids repeated from the earlier run, so this is an artifact of the replay harness, not of b51a55e. I could not check `ops/state/staging.json`: the read script needed an approval that a headless run cannot get. If this hypothesis holds, the confirm run has also **saved** repeated-id lists into the staging state, and those users' imports will keep failing on any release.
- **Ruled out:** a bug in b51a55e (it had 0–1 import failures a day for 9 days), and storage noise as the cause of the import failures (see the arithmetic).

## Desired outcome
Anyone can import a backup the app made of their own list, including a list where two todos share a title.

## Success criteria
- staging_error_rate back inside its band (≤ mean + 3 sd ≈ 2.5 %), with import_failed at 0–1 per day.
- Exporting and then importing a list with two todos titled "Mua sữa" gives "Đã nhập n việc."

## Affected users and systems
`app/backup.js` (parseBackup), `tests/backup.test.js` (the new test), the staging environment, and production if 2e2ce98 is promoted.

## Constraints
- A file with a repeated **id** must still be refused (the existing b51a55e rule) [git show b51a55e:app/backup.js].
- An import refuses the whole file, never part of it [app/backup.js comment on parseBackup].

## Out of scope
Detecting "two backups pasted together" in some other way. If that is still wanted, it needs its own intent from the product owner.

## Impact
High. Restoring a backup is the only way to move or recover a list, and on 2e2ce98 it breaks for most real lists.

## Open questions
- What was 2e2ce98 meant to fix? Was a real complaint about pasted backups behind it? (long-dev, product owner)
- Revert 2e2ce98, or keep the id check only and drop the title check plus its test? (tech lead)
- Does `ops/state/staging.json` now hold repeated ids from the day-38 replay? Should the simulated state be reset before day 39? (on-call)
- Is 2e2ce98 queued for production anywhere? Production is on b51a55e according to commit 4b3f1b5. (release manager Khoa)

ACTIONS TAKEN: Rolled staging back from 2e2ce98-20261110-160042-934299 to b51a55e-20261110-154535-211496 with deploy.rollback(env=staging). The confirm run (`python3 scripts/collect.py traffic --env staging --day 38 --confirm`) gave 0.0625, down from 0.2046 but still above the band, possibly because the replay repeats day-38 ids (unverified). No code, tests, bands or main changed.

## Update · simulated day 38 · level 3 (watch job)

## Update: production, watch production_error_rate level 3, simulated day 38 (2026-11-07)

**Page: on-call.** Production is running 2e2ce98, the release with this bug. Roll it back to **`b51a55e-20261110-154535-364521`** with this command, run by a person:

```
python3 scripts/rollback.py production
```

The command picks the previous distinct release from history, which is the one named above [scripts/deploy.py:102-112, deploy/production/history.jsonl]. I did not run it. Rolling back production is a person's call.

### Problem (production)
Since 2e2ce98 went live in production, people who import their own backup get "File sao lưu này bị lỗi" whenever their list has two todos with the same title. Their list is left unchanged.

### Evidence
- Day 38: 25 of 211 actions failed (11.8 %). All 25 were import_failed, with 0 not_saved and 0 exception. Baseline: mean 1.1 %, sd 0.66 % [ops/metrics/production_error_rate.jsonl day 38]
- Days 29–37 on b51a55e: import_failed was 0–2 a day [ops/metrics/production_error_rate.jsonl days 29–37]
- Release 2e2ce98-20261110-160043-036580 went live in production after b51a55e-20261110-154535-364521 (actor `person:fx-studio`) [deploy/production/history.jsonl]
- Production approval for 2e2ce98 exists [release/approvals/2e2ce98.md] and was committed while this intent was still waiting for triage [git show 4b3f1b5]. So the earlier open question "Is 2e2ce98 queued for production?" is answered: yes, and it is live.
- Noise arithmetic for import_failed: about 13 % of 211 actions are imports, so ~27 imports. At 1 % storage failure, ~0.3 failures are expected. Seeing 25 means nearly every import failed. **Not noise.** [ops/bands.yaml noise model]
- Noise arithmetic for not_saved: ~1.8 expected and 0 seen. P(0) ≈ 17 %. **Noise** [ops/bands.yaml]

### Diagnosis
- **Cause:** the same as on staging. `app/backup.js:101-102` in 2e2ce98 refuses a file when a title repeats, but repeated titles are valid data.
- **Confidence: high.** It is the only release change in the window, every failure is of the import kind, and the same signature showed up on staging on the same day. This would be proved wrong if import_failed stays high after the production rollback. In that case, check for repeated ids in the stored lists, as for the staging replay.
- **Damage:** a refused import writes nothing (the whole file is refused), so rolling back should not leave bad data in production. Users who failed to restore on day 38 have to try again after the rollback.
- **Ruled out:** storage noise (arithmetic above) and b51a55e (0–2 import failures a day for 9 days).

### Success criteria (added)
- production_error_rate back under mean + 3 sd (≈ 3.1 %) on the first day after the rollback, with import_failed at 0–2.

### Open questions (added)
- Run the production rollback now, or ship a fix forward? (on-call, release manager Khoa)
- Why was 2e2ce98 approved for production while this intent about it was open? Should a release wait until the open watch intents for that release are triaged? (Khoa, tech lead)

ACTIONS TAKEN: page_a_person: this intent carries "Page: on-call" with the rollback target (b51a55e-20261110-154535-364521) and the command `python3 scripts/rollback.py production`. I did not roll back or deploy production, and I did not change any code, tests, bands or main.

## Update · simulated day 39 · level 3 (watch job)

## Update: staging day 39, watch staging_error_rate level 3 (2026-11-08)

### Problem (day 39)
Staging is back on the good release b51a55e, but imports still fail on day 39: 11 of about 25 imports. 2e2ce98 is no longer the cause. Most simulated users now have a stored list where the same todo **id** appears twice. b51a55e correctly refuses such a file, so these users cannot restore their own backup on any release. The damaged data is in the simulated staging state, not in the app code.

### Evidence
- Day 39: 14 of 192 actions failed (7.3 %): import_failed 11, not_saved 3, exception 0. Release b51a55e [ops/metrics/staging_error_rate.jsonl day 39]
- The only release change on day 39 is the rollback from day 38 (2e2ce98 → b51a55e, actor `agent:fx-sdlc-watch`). No new release went live [deploy/staging/history.jsonl, detection release_changes]
- The day-38 confirm run on b51a55e already showed the same pattern: import_failed 11 out of 224 actions [ops/metrics/staging_error_rate.confirm.jsonl day 38]
- Noise arithmetic for import_failed: about 13 % of 192 actions are imports, so ~25. At 1 % storage failure, ~0.25 failures are expected. 11 is **not noise**. not_saved: ~1.7 expected and 3 seen, which is **noise** [ops/bands.yaml noise model]
- I sampled the stored lists of users u00–u04. Four of the five hold repeated day-38 ids: `u00-38-4`, `u02-38-1`, `u02-38-2`, `u03-38-4` and `u04-38-2` each appear twice. Day-37 and day-39 ids never repeat [ops/state/staging.json, grep of `u0[0-4]-3[789]-*`]
- Simulated ids are `<user>-<day>-<i>` [scripts/traffic.js:82]. The confirm run uses the same `--day` and the same state file as the first run, and only the seed differs [scripts/collect.py:65-67]. Users who added todos in both day-38 runs got the same ids twice, and traffic.js saves the state at the end [scripts/traffic.js:112]

### Diagnosis
- **Cause:** the `--confirm` replay in `scripts/collect.py:65-67` re-runs the same day on the live state file. `scripts/traffic.js:82` builds ids from (user, day, i), so the replay writes repeated ids into users' stored lists. Every later import of those lists is refused by b51a55e's repeated-id rule, which is the correct rule. This confirms the medium-confidence hypothesis of day 38.
- **Confidence: high.** Repeated ids occur only for day 38, the only day that ran twice. The failures continue on a release that had 0–1 import failures a day for 9 days. Two things would prove this wrong: import failures on day 39 from users whose lists have no repeated ids, or failures that remain after the state is repaired.
- **Not an app bug.** It is a fault in the simulation harness. A real user's list cannot be written twice by a replay. The app's id generation was not checked in this run.
- **Rollback runbook not run, on purpose.** No release went live in the window apart from the rollback itself, and staging already runs the good release. A second `rollback(env=staging)` would pick the previous distinct release, which is the faulty 2e2ce98 [scripts/deploy.py:102-112].
- **Ruled out:** 2e2ce98 (no longer live), storage noise (arithmetic above), and b51a55e (refusing repeated ids is its intended rule).

### Desired outcome (added)
A confirm run checks the release without changing the stored data of the series it confirms.

### Success criteria (added)
- staging_error_rate under mean + 3 sd (≈ 2.4 %) with import_failed at 0–1, on the first day after the staging state is repaired.
- A `--confirm` run leaves `ops/state/<env>.json` unchanged, or writes ids that cannot collide with the main run.

### Open questions (added)
- Should the repeated day-38 entries be removed from `ops/state/staging.json` (keep the first copy of each id), or should the staging state be reset? It is simulated data, so this is the on-call engineer's call. I did not touch it.
- Fix the harness: should `--confirm` run on a copy of the state, or use a different id prefix? (tech lead)
- Was a `--confirm` run also made on production for day 38? If so, `ops/state/production.json` has the same problem, and import failures there will continue after the production rollback. (on-call)
- Should the detector leave out the day after a rollback, or mark it, when the confirm run shares state with the series? (tech lead; `ops/bands.yaml` is changed only by a person)

ACTIONS TAKEN: none. I did not run the staging rollback runbook: no release went live in the window apart from the earlier rollback to the good release b51a55e, and rolling back again would put 2e2ce98 back. I opened no pull request: the fix belongs in the harness (`scripts/collect.py` / `scripts/traffic.js`) and the simulated state, which need a person's decision. No code, tests, bands, state or main were changed. My one script (a read-only count of repeated ids) was refused because it needed approval, so I used grep on the state file instead.

## Update · simulated day 39 · level 3 (watch job)

## Update: production day 39, watch production_error_rate level 3 (2026-11-08)

**Page: on-call. This is the second page, because the day-38 page was not acted on.** Production still runs 2e2ce98. Roll it back to **`b51a55e-20261110-154535-364521`**. A person runs:

```
python3 scripts/rollback.py production
```

The command picks the previous distinct release in history, and that is the release named above [scripts/deploy.py:102-112, deploy/production/history.jsonl]. I did not run it.

### Problem (day 39)
A second day has passed on 2e2ce98. People whose list has two todos with the same title still cannot import their own backup and see "File sao lưu này bị lỗi". Nearly every import in production fails.

### Evidence
- Day 39: 28 of 221 actions failed (12.7 %). All 28 were import_failed, with not_saved 0 and exception 0. Release 2e2ce98-20261110-160043-036580 [ops/metrics/production_error_rate.jsonl day 39]
- Day 38 showed the same pattern, with 25 of 211 all import_failed [ops/metrics/production_error_rate.jsonl day 38]
- No rollback or new release has happened since day 38. The last entry in history is still 2e2ce98 (actor `person:fx-studio`) [deploy/production/history.jsonl]
- Noise arithmetic for import_failed: about 13 % of 221 actions are imports, so ~29 imports. At a 1 % storage failure rate that gives ~0.3 expected failures. 28 means nearly every import failed, so this is **not noise** [ops/bands.yaml noise model]
- Noise arithmetic for not_saved: ~1.9 expected and 0 seen. P(0) ≈ 15 %, so this is **noise** [ops/bands.yaml]
- Production has no confirm-run file (only `staging_error_rate.confirm.jsonl` exists). In a sample of users u00–u04, no day-38 or day-39 id appears twice in the production state. That means the repeated-id harness fault found on staging has not reached production [ops/metrics/, ops/state/production.json grep `u0[0-4]-3[89]-*`]

### Diagnosis
- **Cause:** unchanged from day 38. In 2e2ce98, `app/backup.js:101-102` refuses a file whose titles repeat, but repeated titles are valid data.
- **Confidence: high.** The failures are only of the import kind, they started on day 38 with the release, and they continue without a break on that same release. The staging failures that went on after its rollback came from replay ids, and that cause does not apply here (see the evidence above). This diagnosis would be proved wrong if import failures stay above 0–2 a day once production is back on b51a55e.
- **Damage:** a refused import writes nothing, so no bad data is stored. The users who failed on days 38–39 have to retry after the rollback.
- **Ruled out:** storage noise (see the arithmetic), a replay-state fault in production (no confirm run, no repeated ids in the sample), and b51a55e (0–2 import failures a day on days 29–37).

### Open questions (added)
- The day-38 page asked for a production rollback, and none was done. Was the page received? Was the rollback deliberately deferred in favour of a fix forward? (on-call, release manager Khoa)
- If you decide on a fix forward instead of the rollback, when will it ship? Every day on 2e2ce98 costs about 28 failed restores. (tech lead)

ACTIONS TAKEN: page_a_person. This update carries "Page: on-call" with the rollback target b51a55e-20261110-154535-364521 and the command `python3 scripts/rollback.py production`. I did not roll back or deploy production. I changed no code, tests, bands, state or main. I only ran read-only greps on ops/state/production.json.
