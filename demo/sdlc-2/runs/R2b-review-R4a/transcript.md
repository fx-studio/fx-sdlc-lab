# R2b-review-R4a

Chạy 2026-10-20 17:04 ở gốc repo. Nguyên văn, không sửa. Luồng thô: `stream.jsonl`.

## Prompt

Use the spec-reviewer subagent to review demo/sdlc-2/runs/R4a-bo-cau-cuoi/spec.md . Its intent is intent/2026-10-19-khach-khong-mat-viec.md. Return the subagent's report verbatim, nothing added.

## Tool call (18)

1. Agent · subagent_type=spec-reviewer
2. Read · file_path=<repo>/demo/sdlc-2/runs/R4a-bo-cau-cuoi/spec.md
3. Read · file_path=<repo>/intent/2026-10-19-khach-khong-mat-viec.md
4. Glob · pattern=.claude/skills/policy-*/SKILL.md
5. Glob · pattern=app/**/*
6. Read · file_path=<repo>/.claude/skills/policy-privacy/SKILL.md
7. Read · file_path=<repo>/.claude/skills/policy-security/SKILL.md
8. Read · file_path=<repo>/.claude/skills/policy-ux/SKILL.md
9. Read · file_path=<repo>/app/store.js
10. Read · file_path=<repo>/app/app.js
11. Read · file_path=<repo>/app/index.html
12. Read · file_path=<repo>/app/style.css
13. Glob · pattern=.claude/skills/write-spec/**/*
14. Glob · pattern=demo/sdlc-2/runs/R4a-bo-cau-cuoi/*
15. Read · file_path=<repo>/.claude/skills/write-spec/template.md
16. Read · file_path=<repo>/.claude/skills/write-spec/SKILL.md
17. Read · file_path=<repo>/.claude/skills/write-spec/risk-list.md
18. Glob · pattern=intent/*.md

## Claude · 211 s

I reviewed the draft at `<repo>/demo/sdlc-2/runs/R4a-bo-cau-cuoi/spec.md` against its intent `<repo>/intent/2026-10-19-khach-khong-mat-viec.md`, the four files in `app/` and the three policy files. No files were edited.

**Structure first.** The spec does not use the `write-spec` template. It has no `## Assumptions`, `## Concerns` or `## Questions carried forward` sections and no `## Acceptance criteria` heading. It has no `Risk:` label and no inline `[source]` tags (both required by `.claude/skills/write-spec/SKILL.md`). Line 2 is blank. So every line of the spec is in scope for part 1. §2 "Decisions needed" and §13 "Open questions (carried from the intent)" do that work instead, and I count them as raised, not hidden.

## 1. Hidden assumptions

**(c) Contradicts a source: 5**
1. Line 4: "Status: **ready for engineering, with 3 sign-offs pending**". CLAUDE.md says "Intents and specs start as `Status: draft`", and write-spec rule 6 says "Write the file with `Status: draft`". The "3" also doesn't match the five items D-1 to D-5 in §2.
2. §6.2: "Key `todo.v1` and its array format are **unchanged** … No migration." The same spec adds the keys `todo.lastBackup` (FR-6) and `todo.v1.unreadable` (§6.2). `risk-list.md` line 2 says "Changes the shape of stored data (a new field, a new key, a migration)", so the spec should be high risk. It has no Risk label at all.
3. NFR: "Keep the current no-build, two-script setup." But §6.1 adds `<script src="backup.js">`. `app/index.html` has two scripts today, so this makes three.
4. FR-1 Acceptance: "shows exactly those 3 titles and states; no other data". The format in §6.3 also writes `id`, `createdAt`, `app`, `version` and `exportedAt`.
5. §3: "is returned as is and crashes `visible()`". In the code, `visible()` returns `todos` unchanged for the 'all' filter. The crash actually happens in the `for…of` in `render()` (`app/app.js:37`) or in `todos.filter` (`app/app.js:46`). This is minor and factual.

**(b) Decision or assumption nobody confirmed (not in §2): 25**
1. "File name: `viec-can-lam-YYYY-MM-DD.json` (local date)."
2. "Works in latest Chrome, Safari (macOS + iOS), Firefox, Chrome Android." Nothing in the repo sets this browser list.
3. "≈8,000 items needed to reach this" (also R4). This estimate has no source.
4. "Typical files read in well under a second".
5. "The browser's `beforeunload` prompt is shown while unsaved changes exist". Linh is only named in R5, not in §2.
6. "Every later commit retries the save (no extra timer)."
7. "then it is replaced by "Đã lưu lại được." for a few seconds."
8. "The date is kept in `localStorage` key `todo.lastBackup`". This is a new stored key.
9. "the last backup is > 7 days old **and** the list has changed since". D-4 asks whether to keep the reminder, not about this threshold. "Changed since" also needs a last-change record, and §6.2 doesn't design one.
10. "copy the raw string to `todo.v1.unreadable` … then remove `todo.v1`" and "set a flag so `save()` refuses to write until the user imports".
11. "`id` already in the current list → skip; the current item wins (even if title/done differ)". The file's version is dropped and the user isn't told that the two versions differed.
12. §6.5 limits: "length ≤ 10,000", "string, 1–100 chars", "finite number ≥ 0".
13. "Rules 8–12 are reused by `store.load()` for stored data." One stored item that fails these rules marks the whole list `'unreadable'`, and the user then sees an empty list.
14. newerVersion message: "Hãy tải lại trang để cập nhật app rồi thử lại." This assumes reloading the page loads a newer app. Nothing in the repo says how the app is deployed or cached.
15. notBackup message: "Hãy chọn file có tên bắt đầu bằng "viec-can-lam-"." This assumes the user never renames the file.
16. "When due dates (T-012) add a field, bump to `"version": 2` … T-012's spec must say how v2 imports v1 files."
17. §6.7: "light warm background with dark text". Also "focus is not moved (if it had focus, move focus to **Nhập từ file**)", which contradicts itself.
18. "Success is measured by Lan's email count (§8)" and "starting from release date". The intent doesn't say who measures or from when.
19. "Lan should also record, for each new loss email, whether the customer had a backup."
20. "Lan's support replies should get a short how-to."
21. "fallback is opening the blob in a new tab". This fallback is not in FR-1.
22. "If real users hit it, ask Khoa to raise the cap."
23. "run in a plain HTML test page or Node".
24. The 10-day plan in §12 and "Cut order if late: FR-6 reminder (keep the P4 text), then `beforeunload`."
25. §7 P2: "File has only the user's items + 3 metadata fields". `id` comes from `crypto.randomUUID()` and `createdAt` from `Date.now()` (`app/app.js:8`). The app generates both, so neither is strictly "data the user created". D-3 doesn't ask about them.

**(a) Reasonable inference from a source: 12**
1. "Brand guidelines: **none exist in the repo**".
2. Widening the PO's "vì bộ nhớ đầy" to "storage full or blocked", based on the success criterion "Không còn lần lưu lỗi nào".
3. The D2 description of `getItem` throwing.
4. Quota detection by `QuotaExceededError` and error codes 22/1014.
5. "The words "JSON", "localStorage", "console", "quota", "schema" must not appear", which extends U4.
6. "data is read synchronously at start".
7. "The checkbox has no accessible name besides the visible title inside its `<label>`, which is fine."
8. "R6 Two tabs open overwrite each other's saves".
9. Rule 10, non-empty title, which matches `app/app.js:8` and `:53`.
10. "Works from the in-memory list, so it still works when saving to storage is failing".
11. "the current CSS has none" (no `:focus-visible` style).
12. "email to self, cloud drive, AirDrop: the user's choice".

**Totals:** 5 (c), 25 (b), 12 (a). `## Assumptions` has **0 lines** because the section is missing. Its nearest substitute, §2, has 5 rows.

## 2. Policy coverage

| Rule | Applies? | Status |
|---|---|---|
| privacy P1 | yes | satisfied (no network calls; export only on a tap) |
| privacy P2 | yes | raised as concern (D-3) for the metadata; **missed** for app-generated `id` and `createdAt` |
| privacy P3 | yes | satisfied (indented plain text, §6.3) |
| privacy P4 | yes | satisfied (FR-6 text) |
| privacy P5 | no | stated as not triggered |
| security S1 | yes | satisfied (§6.5: size checked before reading, unknown keys rejected, no eval) |
| security S2 | yes | raised (D-1, D-2), but the spec picks a default and designs to it. **Missed** for §6.2 "then remove `todo.v1`", which deletes a stored list without the confirmation S2 requires |
| security S3 | yes | satisfied |
| security S4 | yes | satisfied |
| UX U1 | yes | satisfied (FR-5) |
| UX U2 | yes | raised (D-1, D-2). The `beforeunload` prompt is only covered in R5, where the spec decides on its own reading. The existing single-item delete has no Undo, logged as a follow-up (§11) |
| UX U3 | yes | satisfied (FR-3, FR-7) |
| UX U4 | yes | mostly satisfied. Not raised: "MB" appears in on-screen text ("File quá lớn (trên 1 MB)", "lớn hơn 1 MB") and may count as a technical word |
| UX U5 | yes | satisfied (§6.7) |

**Conflicts between rules:**
- **S2 vs U2 for import (D-1).** The spec states the conflict, then resolves it itself: "Avoid the conflict: import **only adds** items … A "replace" mode is **not** built." Write-spec rule 4 says "you do not choose."
- **S2 vs U2 for `beforeunload` (R5).** Resolved without saying so in §2: "we read it as outside U2". It appears only under Risks.
- **S2 vs U1 for unreadable data (§6.2).** Resolved without saying so: the spec copies the data and then removes `todo.v1`, with no S2 confirmation and no U2 Undo, and doesn't discuss either rule.

## 3. Versions

The versions are not on line 2 (it is blank). Line 6 has "`policy-privacy@1`, `policy-security@1`, `policy-ux@1`". All three policy files currently have `version: 1`, so the versions **match**.

## 4. Acceptance criteria that cannot be checked as written

- **FR-1:** "no other data" is false for the file format in §6.3, and "Works in latest …" doesn't say what "works" means.
- **FR-3:** no acceptance criterion. "well under a second" can't be tested.
- **FR-4, FR-6, FR-7:** no acceptance line. FR-4 is partly covered by T10. The FR-6 reminder condition "list has changed since" has no data behind it.
- **FR-5:** "for a few seconds" can't be tested. The `beforeunload` behaviour has no test in §9.
- **§6.2:** the copy-failure path (the flag that makes `save()` refuse to write) has no test.
- **§6.7:** "light warm background" can't be checked. The focus rule on Undo expiry contradicts itself.
- **§8:** criteria 1 and 2 are conditional ("Only if they backed up first"). The email criterion can only be checked 6 weeks after release.

## 5. Scope

- The spec designs nothing for sync, accounts, shared lists or recovering the 23 customers' data.
- **T-012 (out of scope):** §6.3 sets a rule for T-012: "bump to `"version": 2` … T-012's spec must say how v2 imports v1 files."
- **Scenario D** presents backup and import as a way to move items between devices ("User can move items one way by backup + import"). That touches multi-device use, which is out of scope, though nothing new is built for it.
- **Beyond the PO's scope but not marked out of scope:** the FR-6 reminder (raised as D-4), the D1 fix, the `beforeunload` prompt, and a focus outline added to every button, including existing ones.
- **Not covered by the release:** success criterion 3 (sync) is acknowledged as unmet (D-5) and is "Treated as not applicable" by default, before the PO has agreed.

Decision: product owner
