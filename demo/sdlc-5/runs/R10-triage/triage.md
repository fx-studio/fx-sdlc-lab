## Build failed: the backup message wording changed, and two tests still expect the old sentence

- **Failed:** `node --test` (44 of 46 passed). The 2 failures are almost certainly these two tests in `tests/backup.test.js`:
  - `messages quoted in the spec and plan are word for word` (line 233)
  - `counts in sentences: a dot every three digits from 1,000 up, plain below (Linh, R9)` (line 258)

  The lint step (`node --check`) printed no errors.
- **Likely cause:** `app/backup.js:13`. Commit `685a86f` ("R10: đổi câu báo sao lưu") changed the `backedUp` message from `'Đã sao lưu {n} việc.'` to `'Đã sao lưu {n} việc ra file.'`.
- **Evidence:**
  - Log: `ℹ tests 46` / `ℹ pass 44` / `ℹ fail 2`, then `== check: FAILED`.
  - Diff of `685a86f`:
    ```
    -  backedUp: 'Đã sao lưu {n} việc.',
    +  backedUp: 'Đã sao lưu {n} việc ra file.',
    ```
  - `tests/backup.test.js:251` expects `fill(MESSAGES.backedUp, { n: 3 })` to equal `'Đã sao lưu 3 việc.'`.
  - `tests/backup.test.js:265` expects `fill(MESSAGES.backedUp, { n: 2001 })` to equal `'Đã sao lưu 2.001 việc.'`.
  - Neither assertion can pass with the new text. No other test uses `backedUp`. The other user of the message is `app/app.js:97`, which shows it and isn't tested on its wording.
  - The accepted plan, `plan/2026-10-19-khach-khong-mat-viec.md:114`, still lists the message as M4a `Đã sao lưu {n} việc.`. The spec only says the app reports how many todos were backed up (F1 step 3, AC line 198), so either wording meets the spec.
- **Suggested fix:** The tests are correct and the code doesn't match the accepted plan. Revert `app/backup.js:13` to `'Đã sao lưu {n} việc.'`. If a person really wants the new wording, they should update plan M4a and the tests at lines 251 and 265 in the same commit.
- **Confidence:** High on the cause: it's the only change in the commit, and exactly two assertions depend on that string, which matches `fail 2`. Medium on the exact test names, because I couldn't run the tests here (the `node --test` call needed approval that this session couldn't get). Running `node --test tests/backup.test.js` would confirm both names and show the `actual`/`expected` diffs.

I didn't change any files. The commit message itself says this failure was planted on purpose ("gài build fail có chủ ý").
