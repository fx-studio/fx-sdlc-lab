# R8a-intent-reviewer

Chạy 2026-11-10 16:19 ở gốc repo, chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Use the intent-reviewer subagent on intent/auto/2026-11-07-import-refuses-duplicate-titles.md (written by the watch job, not by a person; the originator is the metric, its evidence lives in ops/metrics/, deploy/*/history.jsonl and git). Return its report as it is.

## Tool call (29)

1. Agent · subagent_type=intent-reviewer
2. Read · file_path=<repo>/intent/auto/2026-11-07-import-refuses-duplicate-titles.md
3. Read · file_path=<repo>/.claude/skills/write-intent/checklist.md
4. Glob · pattern={intent,spec,ops,deploy}/**/*
5. Glob · pattern={intent/auto/*,ops/*,ops/metrics/*,ops/state/*,release/**/*,deploy/*/history.jsonl,deploy/*/releases/2e2ce98*/backup.js,deploy/*/releases/b51a55e*/backup.js}
6. Read · file_path=<repo>/deploy/staging/releases/2e2ce98-20261110-160042-934299/backup.js
7. Read · file_path=<repo>/deploy/staging/history.jsonl
8. Read · file_path=<repo>/deploy/production/history.jsonl
9. Read · file_path=<repo>/ops/triage.md
10. Read · file_path=<repo>/release/approvals/2e2ce98.md
11. Grep · pattern="day": (29|3[0-9]|4[0-9])\b
12. Read · file_path=<repo>/ops/watch.jsonl
13. Read · file_path=<repo>/scripts/traffic.js
14. Read · file_path=<repo>/scripts/collect.py
15. Read · file_path=<repo>/ops/bands.yaml
16. Grep · pattern=ids|titles|Set\(
17. Grep · pattern=ids|titles|same todo|twice
18. Grep · pattern=twice|same title|repeat|duplicate|trùng
19. Read · file_path=<repo>/scripts/deploy.py
20. Grep · pattern=duplicate|trùng|same title|repeated|2e2ce98|import
21. Glob · pattern=.git/refs/heads/**/*
22. Grep · pattern=^# |Status|Triage|repeated|trùng|duplicate
23. Grep · pattern=4b3f1b5|2e2ce98|import-guard
24. Read · file_path=<repo>/release/gate-log.jsonl
25. Grep · pattern=u0[0-4]-3[89]-\d+
26. Grep · pattern=(?i)title|tên việc|trùng|id
27. Read · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
28. Read · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
29. Read · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md

## Claude · 160 s

Here is the intent-reviewer's report, unchanged. I haven't checked its claims myself.

---

I reviewed `<repo>/intent/auto/2026-11-07-import-refuses-duplicate-titles.md`. It is out of date: most of it describes a situation that no longer exists in the repo.

- **Production is already rolled back.** `deploy/production/history.jsonl` line 4 shows `"b51a55e-20261110-154535-364521", "actor": "person:huy-on-call (giả lập)"` at 16:05:03. The second page was written at 16:03:19 (`ops/watch.jsonl` line 117). Production days 40–42 had 0 import_failed. The production success criterion is met.
- **The test harness is already fixed.** `scripts/collect.py:68-75` now runs `--confirm` on a temp copy with an id prefix `c-`. Staging day 39 was measured again (`"value": 0.01942 ... "import_failed": 0, "value_before_fix": 0.07292`). The first confirm row now says `"không dùng số này"` ("do not use this number"). The day-39 staging "Desired outcome" and both success criteria are already met.
- **The title rule is not on `main`.** `app/backup.js:98-101` checks repeated ids only. No `feat/import-guard` branch exists. Both environments run b51a55e.

What is left is a product question, not an incident: should 2e2ce98's rule (refuse repeated titles) ever ship?

## 1. Unsourced claims

I left out the Open questions sections. I couldn't run `git show`, so I checked commit claims against the deployed copies in `deploy/*/releases/`.

**(a) Reasonable inference (7)**
1. "so most lists hold a repeated title"
2. "this is an artifact of the replay harness, not of b51a55e". The draft labels this a hypothesis, and day 39 confirmed it.
3. "those users' imports will keep failing on any release"
4. "Restoring a backup is the only way to move or recover a list". It fits the localStorage-only app.
5. "a refused import writes nothing (the whole file is refused), so rolling back should not leave bad data in production". `importBackup` returns `keep()` before `replace`, but the draft doesn't cite that.
6. "Most simulated users now have a stored list where the same todo **id** appears twice". It is drawn from 5 sampled users out of 40.
7. "Every day on 2e2ce98 costs about 28 failed restores"

**(b) Assumption no one confirmed (4)**
1. "Two todos with the same title are valid data in this app; only a repeated **id** means a bad file." This is the central claim. It has a source the draft doesn't cite: the accepted spec, `spec/2026-10-19-khach-khong-mat-viec.md:45` and `:131`, lists the refusal rules as "trùng `id`, tiêu đề rỗng, `createdAt` không phải số" (repeated id, empty title, `createdAt` not a number) [answer A7, Khoa]. Repeated titles are not on that list. But Khoa also approved 2e2ce98, so whether the rule is right is still a product call.
2. "The new test in `tests/backup.test.js` pins this wrong rule." It has no source, and the test is not on `main`.
3. "on 2e2ce98 it breaks for most real lists". This comes from simulated users who pick from 9 fixed words. Real users do not.
4. "This is the second page, because the day-38 page was not acted on." On the simulated clock the two pages were 79 real seconds apart (16:02:00 and 16:03:19).

**(c) Solution placed where a problem should be (1)**
1. Success criterion: "or writes ids that cannot collide with the main run". It prescribes a mechanism. (The "Page: on-call / roll back to" block is required by `ops/bands.yaml`, `production_error_rate.level3`, so I did not count it.)

**Totals: 12 unsourced (a 7, b 4, c 1).**

## 2. Checklist

- **Problem: pass.** It says who ("people who save their list to a file and import that same file back") and when (on 2e2ce98, when two titles repeat).
- **Evidence: pass.** Concrete numbers. Staging day 38 (44/215, 36 import_failed) and production days 38–39 (25/211, 28/221) match `ops/metrics`.
- **Out of scope: pass.** The section is present, but it only covers the title rule. Nothing scopes the harness section added on day 39.
- **Success criteria: pass.** They are checkable, and all are already met.
- **Open questions: fail.** They are split over 5 sections. One question sits in the body: Diagnosis, "The 11 import failures after rollback: unexplained..." / "I could not check `ops/state/staging.json`". Also, production Evidence answers an earlier open question in place. There are empty headings at lines 52, 90 and 127.
- **Sourced: fail.**
  - "13 % of actions" cites `scripts/traffic.js:94-101`, but the code imports on `r >= 0.85`, which is at most 15 %. The draft also uses "about 32 imports" out of 215 (15 %) on staging and 13 % on production.
  - "[approval] was committed while this intent was still waiting for triage [git show 4b3f1b5]" conflicts with the timestamps. Production went live at 16:00:43 and this intent was first created by the run logged at 16:00:44 (`ops/watch.jsonl` line 113), so the approval came first. The open question "Why was 2e2ce98 approved ... while this intent ... was open?" rests on this. What actually happened is in `release/approvals/2e2ce98.md`: "Lên staging và production cùng đầu ngày, không chờ staging chạy một ngày" (staging and production went up at the start of the same day, without waiting for a day on staging).
  - Several citations are now off by one line after the harness fix (`traffic.js:82` is now `:83`, `:47` is now `:48`, `:112` is now `:113`).
  - The day-39 staging breakdown "import_failed 11, not_saved 3" is no longer in the metrics file.
  - "No rollback or new release has happened since day 38" is now false.

## 3. Duplicates

No true duplicate. Related intents:
- `<repo>/intent/auto/2026-10-19-production-import-failed-spike-day19.md`: same symptom. Its "Giả thuyết 2" (hypothesis 2) is the same repeated-id replay mechanism. Triage was dismiss, `wrong-diagnosis` (Huy, ngày 22): noise at that time. This draft's day-39 section confirms that mechanism for the `--confirm` replay.
- `<repo>/intent/auto/2026-11-01-ci-random-titles-test-empty-title.md`: same module (backup with titles), different problem. Triage was fix-now, closed by PR 9/10.
- `<repo>/spec/2026-10-19-khach-khong-mat-viec.md`: the accepted spec that 2e2ce98 departed from without a spec change.
- `ops/triage.md` has no row for this intent.

## 4. Questions for the originator

The originator here is the metric. These questions go to the people involved.

1. **Long-dev and Khoa:** what complaint or case led to 2e2ce98 ("two backups pasted together")? Should duplicate titles be refused, which would mean changing spec answer A7, or is A7 still right?
2. **Khoa:** 2e2ce98 changes a rule the accepted spec fixes, and it went to staging and production at the same time. Should a release that departs from an accepted spec need a spec update first, and should production wait one day on staging?
3. **Product owner:** with both environments on b51a55e, the harness fixed and the title rule off `main`, is anything left to do besides "do not promote 2e2ce98"? Or should this intent be closed as already handled, keeping the lesson?
4. **On-call (Huy):** was `ops/state/staging.json` repaired or rebuilt after the fix? I see no repeated `u0[0-4]-3[89]` ids now. Is the day-38 confirm row kept only as a record?
5. **Tech lead:** an agent wrote "the second page, because the day-38 page was not acted on" 79 seconds after the first page. Should pages on the simulated clock carry real elapsed time so on-call is not told they missed a page?

Decision: product owner
