# R2c-review-R1

Chạy 2026-10-20 17:06 ở gốc repo. Nguyên văn, không sửa. Luồng thô: `stream.jsonl`.

## Prompt

Use the spec-reviewer subagent to review spec/2026-10-19-khach-khong-mat-viec.md . Its intent is intent/2026-10-19-khach-khong-mat-viec.md. Return the subagent's report verbatim, nothing added.

## Tool call (14)

1. Agent · subagent_type=spec-reviewer
2. Read · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
3. Read · file_path=<repo>/intent/2026-10-19-khach-khong-mat-viec.md
4. Glob · pattern=.claude/skills/policy-*/SKILL.md
5. Glob · pattern=app/**/*
6. Read · file_path=<repo>/.claude/skills/policy-privacy/SKILL.md
7. Read · file_path=<repo>/.claude/skills/policy-security/SKILL.md
8. Read · file_path=<repo>/.claude/skills/policy-ux/SKILL.md
9. Read · file_path=<repo>/app/store.js
10. Read · file_path=<repo>/app/app.js
11. Read · file_path=<repo>/app/index.html
12. Glob · pattern=.claude/skills/write-spec/**
13. Read · file_path=<repo>/.claude/skills/write-spec/risk-list.md
14. Read · file_path=<repo>/app/style.css

## Claude · 354 s

# Spec review: spec/2026-10-19-khach-khong-mat-viec.md

Sources read: the spec, the intent `<repo>/intent/2026-10-19-khach-khong-mat-viec.md` (Status: accepted), `app/store.js`, `app/app.js`, `app/index.html`, `app/style.css`, the three `policy-*/SKILL.md` files, and `.claude/skills/write-spec/risk-list.md`.

The spec's header (the "From:" line with intent, skills, status and risk) is on **line 3**, not line 2. Line 2 is blank. I used line 3.

---

## 1. Hidden assumptions

I checked every statement outside `## Assumptions`, `## Concerns` and `## Questions carried forward`. Statements with a correct source are not listed. Statements below have no real source, or cite a source that doesn't say what they claim.

### (a) Reasonable inference from a source: 9

1. Line 3: `Risk: high (risk-list dòng 1: "personal data leaving the user's device")`. The risk-list line actually reads "Touches payment, authentication, or personal data leaving the user's device". Treating a user-triggered download to the user's own disk as "leaving the device" is an interpretation. It is reasonable, but see (c)1: the spec contradicts it elsewhere.
2. Line 23: "Khách bấm nút sao lưu [intent]". The intent says "khách tự sao lưu" but never mentions a button.
3. Lines 24-25: "trình duyệt tải file đó về máy". The download mechanism is not in the intent.
4. Line 31: "chọn một file [intent]". Same kind of inference.
5. Line 37: "danh sách đang có giữ nguyên". This cites U1/U4, but U1 covers failed saves, not rejected imports. It does follow from S1 ("untrusted").
6. Lines 39-40: "Không có việc nào bị thay, nên không cần xác nhận hay Undo". This is fine in general, but it has an unflagged interaction with C4: `store.load` returns `[]` when `todo.v1` is corrupt (`app/store.js` lines 9-10). In that case the list looks empty, and an import overwrites the corrupt but still present data with no confirmation and no Undo.
7. Lines 64-65: "Spec này không thêm khoá, không thêm trường [app/store.js]". This is a design choice, cited to the current code.
8. Lines 73-74: "Tải file về và chọn file dùng sẵn tính năng của trình duyệt".
9. Line 75: "`app/style.css`" listed as a modified file "[app/]". No flow says what styling changes.

### (b) Decision or assumption nobody confirmed: 5

1. Line 9: "(đo bằng email, không phải tiêu chí nghiệm thu của spec này)". The intent lists this as a success criterion. Moving it out of acceptance is the spec author's decision.
2. Lines 16-17: "Intent không nhắc tới nút này [intent], nên để ngoài phạm vi." The spec knowingly leaves a current violation of `policy-ux@1#U2` in place. It puts this under Out of scope, not Concerns, so nobody is asked to accept it. (The facts are correct: `remove()` in `app/app.js` lines 18-21 deletes at once with no Undo.)
3. Line 26: "App báo trên cùng màn hình là đã sao lưu bao nhiêu việc [policy-ux@1#U1]". Wrong citation: U1 is "Any failed save is shown…". The success message is a design decision without a source.
4. Line 42: "Nếu lưu sau khi nhập bị lỗi: danh sách cũ giữ nguyên". This is a rollback decision. It is also the opposite of what A11 proposes for F3: there, unsaved items stay on screen. Nobody confirmed either behaviour, and the spec doesn't point out that they differ.
5. Line 58: "chỉ tới nút nhập từ file [policy-ux@1#U3]". U3 only requires that an empty state exists. What it says is a decision.

### (c) Contradicts a source: 1

1. Line 18: "Không lưu dữ liệu ở đâu khác ngoài trình duyệt của khách, nên không cần duyệt của privacy owner [policy-privacy@1#P5]." Line 82 repeats it: "P5 → không áp dụng: không lưu ngoài trình duyệt."
   - P5 reads: "Storing user data anywhere outside the user's browser (server, cloud, account) needs sign-off from the privacy owner first."
   - F1 creates a file outside the browser by design.
   - A1 expects users to move that file "qua email, Zalo, ổ đĩa", which are cloud services.
   - The spec's own Risk line says data is "leaving the user's device".
   - Whether P5 covers this depends on how to read "anywhere" next to the "(server, cloud, account)" examples. That is a call for Mai, not something the spec can settle by itself.

**Counts:** (a) 9, (b) 5, (c) 1. Total 15.

**`## Assumptions`:** 18 lines (lines 94-111), holding 12 assumptions (A1-A12).

Internal inconsistency, not counted above: line 79 says "file chỉ chứa bốn trường của việc", but A3 and AC1 also allow `version` and `todos`.

---

## 2. Policy coverage

| Rule | Applies? | Status |
|---|---|---|
| P1 (no data leaves without user action) | Yes | Satisfied (F1 step 2, AC2) |
| P2 (export only user-created data) | Yes | Raised (A3: `id`, `version`) |
| P3 (plain, human-readable export) | Yes | Satisfied, with interpretation raised (A2) |
| P4 (tell user where data is kept) | Yes | Satisfied (F4, AC9) |
| P5 (storage outside browser needs privacy owner sign-off) | Arguably yes | **Missed**: declared "không áp dụng" with no question to Mai (see (c)1) |
| S1 (untrusted import, schema, unknown fields, 1 MB, no eval) | Yes | Satisfied (F2 step 3, AC4-7); details raised (A4); size clash raised (C3) |
| S2 (confirm before overwriting more than one item) | Yes | Raised (C1). Corrupt-data-then-import case missed (see (a)6) |
| S3 (`textContent`) | Yes | Satisfied (line 71, AC7) |
| S4 (no external dependency) | Yes | Satisfied (line 73, AC12) |
| U1 (no silent data loss; failed save shown) | Yes | Satisfied for saves (F3, AC8). Load path raised (C4), 1 MB backup raised (C3) |
| U2 (no confirmations; Undo 10 s) | Yes | Raised for import (C1). **Missed** for the existing delete button: moved to Out of scope instead of Concerns |
| U3 (empty, loading, error states) | Yes | Partly satisfied. Backup (F1) has no error state, e.g. download blocked. Empty state for filtered views ("Chưa xong" or "Đã xong" with no matches) is not defined. No AC for the loading state |
| U4 (Vietnamese, short, no technical words) | Yes | Satisfied; `.json` suffix raised (A10) |
| U5 (keyboard, accessible labels) | Yes | Satisfied via A9 (unconfirmed), AC11 |

**Conflicts between two rules resolved without saying so:** none found.
- S2 vs U2 is raised openly (C1).
- S1 vs U1 is raised openly (C3).
- Closest case: F2 step 5 combined with C4. When stored data is corrupt, the "empty list" path skips both S2 and U2. The spec doesn't note this.

---

## 3. Versions

Line 3 says: `policy-privacy@1, policy-security@1, policy-ux@1`.

Current files:
- `policy-privacy/SKILL.md`: `version: 1`
- `policy-security/SKILL.md`: `version: 1`
- `policy-ux/SKILL.md`: `version: 1`

**All three match.**

---

## 4. Acceptance criteria that can't be checked as written

- **AC13**: "tiêu chí viết sau khi C1 được quyết". This is a placeholder and can't be checked.
- **AC4, AC5, AC6**: only "thấy thông báo". They don't check that the message is plain Vietnamese or says what to do next (U1, U4). AC4 also doesn't say whether the over-1 MB test file is otherwise valid.
- **AC8**: "gợi ý làm tiếp" depends on A8, which is unconfirmed, so there is no wording to check against. The method "ghi khoá khác tới khi lỗi" is loose. It covers only adding a task. The intent's criterion "Không còn lần lưu lỗi nào mà khách không được báo" also needs toggling, deleting and importing.
- **AC9**: no fixed wording, so pass or fail is a judgment call.
- **AC10**: checks only three words. U4 also requires "short" and "free of technical words" in general.
- **AC11**: no screen reader or browser named. "đọc thông báo lỗi" depends on A9, which is unconfirmed.
- **AC2**: "không ghi request nào" is ambiguous. A `blob:`/`data:` download may show up in the Network panel.
- **Spec behaviour with no AC**: success count (F1 step 3), empty backup (A6), backup over 1 MB (C3), loading state (F2 step 2), save failure after import (F2 step 7), duplicate `id` or empty title (A4).

---

## 5. Scope

Nothing the intent excludes is designed. The spec doesn't design account login, multi-user lists, recovering the 23 users' data, or deadlines (T-012).

Two things to watch:
- **C1 option (c)** ("chỉ thêm việc có `id` chưa có") merges lists from two devices. That moves toward "Đồng bộ nhiều máy", which the intent puts out of scope. The spec notes that it changes behaviour, but not that it overlaps with the sync exclusion.
- **C4** would widen scope (fixing the load path). It is correctly raised as a question rather than designed.

---

Decision: product owner
