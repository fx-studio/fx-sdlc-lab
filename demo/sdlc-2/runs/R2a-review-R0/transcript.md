# R2a-review-R0

Chạy 2026-10-20 17:05 ở gốc repo. Nguyên văn, không sửa. Luồng thô: `stream.jsonl`.

## Prompt

Use the spec-reviewer subagent to review demo/sdlc-2/runs/R0-prompt-mau/spec.md . Its intent is intent/2026-10-19-khach-khong-mat-viec.md. Return the subagent's report verbatim, nothing added.

## Tool call (17)

1. Agent · subagent_type=spec-reviewer
2. Read · file_path=<repo>/demo/sdlc-2/runs/R0-prompt-mau/spec.md
3. Read · file_path=<repo>/intent/2026-10-19-khach-khong-mat-viec.md
4. Glob · pattern=.claude/skills/policy-*/**
5. Glob · pattern=app/**
6. Read · file_path=<repo>/.claude/skills/policy-privacy/SKILL.md
7. Read · file_path=<repo>/.claude/skills/policy-security/SKILL.md
8. Read · file_path=<repo>/.claude/skills/policy-ux/SKILL.md
9. Read · file_path=<repo>/app/store.js
10. Read · file_path=<repo>/app/app.js
11. Read · file_path=<repo>/app/index.html
12. Read · file_path=<repo>/app/style.css
13. Glob · pattern=demo/sdlc-2/runs/R0-prompt-mau/**
14. Glob · pattern=.claude/skills/write-spec/**
15. Read · file_path=<repo>/.claude/skills/write-spec/template.md
16. Grep · pattern=brand
17. Grep · pattern=ở chỗ của họ|Status|Author

## Claude · 261 s

The spec does not use the `write-spec` template. The R0 run used a free-form prompt (`demo/sdlc-2/runs/R0-prompt-mau/transcript.md:7`). So there is no `## Assumptions`, no `## Concerns` and no `## Questions carried forward`. §9 "Areas of concern" does the job of Concerns, so I left it out of the audit, except where it states facts. Line 2 of the spec is empty. The version metadata is on line 7.

## 1. Hidden assumptions

**(a) Reasonable inference from a source: 12**
1. L22 `"(storage full, storage blocked, corrupt data)"`. The intent only names `"bộ nhớ đầy"`. The wider list follows from U1 `"Any failed save"`.
2. F1.3 `"Export builds the file from the in-memory list, not from storage"`. Follows from U1.
3. F1.7 `"Blob + URL.createObjectURL + a temporary <a download> ... No library"`. Follows from S4.
4. F2.2 `"file.size > 1 048 576 bytes"`. S1 says `"1 MB"`. Reading that as binary MB (MiB) is a choice the spec does not state.
5. F2.4 `"Any violation rejects the whole file. Nothing is imported partially."` Follows from S1.
6. F3.1 `"{ ok: false, reason: 'quota' | 'unavailable' | 'unknown' }"` and `"legacy codes 22 / 1014"`. Follows from U1, plus platform knowledge.
7. F3.7 `"proved by tests (§10), not measured in production"`. Follows from P1.
8. F4.4 `"On unavailable, show the list normally (empty) and the F3.3 "unavailable" banner right away."` Follows from U1.
9. F6 `"All 23 complaining users had none"`. True because the app has no export today (`app/store.js`).
10. C3 `"Same risk class as S1"`.
11. §6.2 `"Build a fresh object ... so no prototype tricks (__proto__ keys) or extra properties can leak in."` Follows from S1.
12. §6.7 `"system font, #f6f6f4 background, #222 text, light #ddd dividers"`. Matches `app/style.css`.

**(b) Decision or assumption nobody confirmed: 28**
1. F2.5 `"Merge, never overwrite ... keep the local one unchanged"`. §9.2 raises it, but §9.2 also says `"engineering can build F1–F3 ... as specified"`.
2. F2.6 `"New tasks are inserted by createdAt ascending, interleaved ... Ties go to the existing task first."`
3. F6, the whole backup reminder, which the intent never asks for. Includes F6.2 `"the last backup is > 7 days old"`.
4. F8 is labelled `"PO to confirm"`, yet §9.2 says `"engineering can build F1–F3, F5–F8 as specified"` and §11 schedules it for day 7.
5. F1.1 `"sits in a new "Sao lưu" section below the list"`. The same bullet contradicts itself: `"It stays available when the list is empty"` and then `"the button is shown disabled"`.
6. F1.6 `"todo-sao-luu-YYYY-MM-DD.json"`.
7. F1.8 `"record lastBackupAt and lastBackupCount under the local key todo.meta"`.
8. §5 limits: `"0 to 10 000 items"`, `"1–64 chars, ^[A-Za-z0-9-]+$"`, `"1–1 000 characters"`, `"Any control character ... means reject"`, `"Date.now() + 1 day"`.
9. §5 `"also apply in the add form (maxlength="1000")"`. This changes how the existing form behaves (`app/index.html:13` has no limit today).
10. F4.2 `"Loaded data goes through the same task validator as import ... unknown fields and invalid items count as corrupt"`. S1 covers imported files only. Stored lists that are valid today would become "corrupt" after the update: a title over 1 000 chars (no limit today), a pasted tab, or a `createdAt` ahead of a clock that was moved back. One such task blocks the whole list. This clashes with §6.3 `"There is no migration, because the stored shape is unchanged."`
11. F4.3 `"Best-effort copy of the raw string to todo.v1.hong-<epoch ms>"`. The copy is never cleaned up and keeps using quota. The user is told `"Danh sách cũ vẫn được giữ lại"`, but per `"Engineering may add a recovery path later"` there is no way to get it back.
12. F4.3 `"Until the user picks one, adding tasks is disabled."`
13. F3.3/F3.4 banner design and wording. F3.4 always says `"vì bộ nhớ của trình duyệt đã đầy"`, even when the reason is `unavailable` or `unknown`.
14. F2.11 messages, including `"Hãy tải lại trang rồi thử lại"`. This assumes a reload brings in a newer app version.
15. F1.9 `"ví dụ gửi cho chính bạn"`.
16. Wording in F2.8, F7 and F8.1, plus `"Fix the counter: "0 việc chưa xong" is not shown in the Empty state."`
17. §6.1 `"backup.js NEW"`. Line 9 `"Code touched"` does not list it.
18. §6.5 `"Static Vietnamese strings live in one const T = {…} table"`.
19. §6.6 `"pressing Esc does not dismiss it. The 10-second timer pauses while the Undo button has focus or hover"`.
20. §6.7 `"background #fff4e5, left border 4px #b45309"` and `"(contrast ≥ 4.5:1)"`. The contrast figure was not checked.
21. §6.8 `navigator.storage.persist()` and `"Safari can still wipe site data after a long period without use"`. Nothing in the repo backs this.
22. §8.1 `"file lands in Downloads/Files → the user sends it to themselves (email, chat, their own cloud)"`.
23. §8.3 `"F1 already lets a business customer keep a copy "ở chỗ của họ""`. That intent is still a draft and still asks `"là ở đâu (máy của nhân viên, ổ chung hoặc server công ty, nơi khác)?"` (`intent/2026-10-19-khach-doanh-nghiep-sao-luu.md:42`).
24. §8.4 `"bump to version: 2 and add dueAt as an optional field"`.
25. Estimates: F8 `"about 0.5 day of work"`, §9.6 `"about 0.5 day of work"`, §9.4 `"about 6 000 typical tasks"`, and the day split in §11.
26. §10 `"Run in current Chrome, Firefox, Safari (macOS), Safari (iOS) and Chrome (Android)."`
27. F3.6 `beforeunload`. §9.3 raises it.
28. F2.8 `"Undo puts back the exact pre-import list"`. Any task added during the 10 seconds is wiped too. Adding a task is not destructive, so F8.3 does not cancel the Undo.

**(c) Contradicts a source: 5**
1. L10 `"Status | Ready for engineering, except the 3 decisions marked BLOCKING in §9"`.
   - CLAUDE.md says `"Intents and specs start as Status: draft"`, and template line 3 says `"Status: draft"`.
   - Only §9.2 is marked BLOCKING, not 3 decisions.
2. L44 `"Out of scope (from the intent)"` lists `"Any server, cloud storage or analytics"`. The intent's Out of scope (lines 40–43) has three items and this is not one of them. It comes from P1/P5/S4.
3. §6.4 `"The snapshot is a structured copy of todos"` against `"snapshot = todos.slice()"`. `slice()` is a shallow copy, and `app/app.js:14` changes tasks in place (`t.done = !t.done`). A toggle made after an import also changes the snapshot, so Undo would not restore F2.8's `"exact pre-import list"`.
4. F4.3 `"Use Undo-free wording plus an explicit second press"` contradicts U2. Raised as BLOCKING in §9.2.
5. §7 S2 row `"Import is add-only, so no multi-item overwrite or delete happens"`, and §9.2 `"neither rule is triggered"`. But Undo of an import (F2.8) deletes every added task at once (for example 30) with no confirmation, which is exactly what S2 covers.

**Totals:** 45 statements without a real source. (a) 12, (b) 28, (c) 5. `## Assumptions` has **0 lines** because the section does not exist. The template's `Risk:` field is also missing.

## 2. Policy coverage

| Rule | Applies | Result |
|---|---|---|
| P1 | yes | satisfied (F1.2, F3.7, F6.3) |
| P2 | yes | satisfied. The `format`/`version` marker is raised as a concern (§9.5) |
| P3 | yes | satisfied (F1.5). `.json` naming raised in §9.5 |
| P4 | yes | satisfied (F5) |
| P5 | yes (nothing leaves the browser) | satisfied |
| S1 | yes | satisfied. The 1 MB lock-out is raised (§9.4). Missed: applying S1 to stored data (F4.2) goes beyond the rule and is not flagged |
| S2 | yes | raised for the F4.3 fallback (§9.2). **Missed** for import-Undo (c5) and for F4.3 "Bắt đầu danh sách mới" when the copy succeeded (it overwrites `todo.v1` with no confirmation and no Undo) |
| S3 | yes | satisfied (§6.5, F2.10, F8.1) |
| S4 | yes | satisfied |
| U1 | yes | satisfied in intent. Missed: the F4.2 lock-out of currently valid lists, the hard-coded quota wording in F3.4, and the `hong-*` copy the user cannot reach |
| U2 | yes | raised (§9.2, §9.3). The F3.6 `beforeunload` prompt is a confirmation dialog and is raised in §9.3 |
| U3 | yes | satisfied (F7) |
| U4 | yes | satisfied. `.json` raised (§9.5) |
| U5 | yes | satisfied (§6.6) |

**Rule conflicts the spec resolved without saying so:**
- S2 vs U2, import Undo: deleting several items with no confirmation. U2 wins silently.
- S2 vs U2, F4.3 "Bắt đầu danh sách mới" when the raw copy succeeded: neither rule is applied. The spec seems to treat the hidden copy as making the overwrite non-destructive.
- S1 vs U1, F4.2: rejecting unknown fields or bad items now also applies to stored data, so one bad task blocks the whole list. S1 wins silently.
- U2's "10 seconds": §6.6 pauses the timer on focus or hover, so Undo can stay longer. Minor, but not stated.

## 3. Versions

Line 2 of the spec is empty. The versions are on line 7: `policy-privacy@1`, `policy-security@1`, `policy-ux@1`. All three policy files currently have `version: 1`, so they **match**.

## 4. Acceptance criteria that cannot be checked as written

- **Test 1:** `"shows the 3 titles readably"` is subjective.
- **Test 8:** `"Storage nearly full + a valid large import"` gives no sizes, so the outcome is not determined.
- **Test 10:** `"Private window with storage blocked"` names no browser. The stub alternative can be checked.
- **Test 12:** a grep cannot show `"finds no swallowed save errors"`. `"every store.save( call site uses the result"` needs a manual review.
- **Test 13:** names no screen reader and browser pair, and gives no expected announcement text.
- **§10 header:** `"current Chrome, Firefox…"` gives no versions.
- **Untested requirements:** F1.10, F1.9, F2.8 (10-second expiry), F2.9, F3.3 (`"Vẫn chưa lưu được."`), F3.6, the F4.3 fallback, F5, F6, F7 empty and filter states, F8.
- **Intent criteria:** §9.1 says criteria 1–3 are not met by this release. Criterion 4 (email count) cannot be checked by engineering.

## 5. Scope

- **Designed despite being out of scope:** §8.4 designs the v2 format for due dates (`"add dueAt as an optional field. The v2 app must accept v1 files"`). The intent's line 43 puts T-012 out of scope.
- **Not excluded by the intent, but not asked for either** (for the product owner to note): F4 corrupt-data handling, F6 reminder, F8, §6.8 `persist()`, the add-form `maxlength`, the C6/C7 fixes, the §9.6 two-tab fix, and the §8.3 suggestion to close or merge Minh's intent.
- **No server, account or sync is designed.**

Files: `<repo>/demo/sdlc-2/runs/R0-prompt-mau/spec.md`, `<repo>/intent/2026-10-19-khach-khong-mat-viec.md`, `<repo>/.claude/skills/policy-{privacy,security,ux}/SKILL.md`, `<repo>/app/app.js`, `<repo>/app/store.js`

Decision: product owner
