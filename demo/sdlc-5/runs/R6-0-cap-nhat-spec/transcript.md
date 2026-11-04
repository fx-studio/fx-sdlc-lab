# R6-0-cap-nhat-spec

Chạy 2026-11-04 10:00 ở gốc repo, chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

The people answered every assumption and concern of the draft spec spec/2026-10-19-han-chot-cho-viec.md: see demo/sdlc-5/tra-loi-gia-dinh.md. Update the draft spec with those answers, the way /write-spec would: turn each answered assumption into a settled statement with its source, rewrite C2/C3 as decisions, update the flows, data section and acceptance criteria (Undo when clearing a due date; backup file version 2 with an optional dueDate, version 1 files still importable; a due date set while saving fails is reported). Note in the spec that Khoa will change policy-security S1 himself. Keep Status: draft and keep it in Vietnamese like the rest of the file. Do not touch any other file.

## Tool call (17)

1. Read · file_path=<repo>/spec/2026-10-19-han-chot-cho-viec.md
2. Read · file_path=<repo>/demo/sdlc-5/tra-loi-gia-dinh.md
3. Skill · skill=write-spec
4. Read · file_path=<repo>/.claude/skills/write-spec/checklist.md
5. Read · file_path=<repo>/.claude/skills/write-spec/template.md
6. Read · file_path=<repo>/.claude/skills/policy-security/SKILL.md
7. Read · file_path=<repo>/.claude/skills/policy-ux/SKILL.md
8. Read · file_path=<repo>/app/backup.js
9. Read · file_path=<repo>/app/store.js
10. Grep · pattern=^version|^owner
11. Read · file_path=<repo>/app/app.js
12. Grep · pattern=Status:|^### F3|Undo
13. Read · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
14. Read · file_path=<repo>/.claude/skills/write-spec/risk-list.md
15. Read · file_path=<repo>/.claude/skills/policy-privacy/SKILL.md
16. Write · file_path=<repo>/spec/2026-10-19-han-chot-cho-viec.md
17. Bash · command=bash scripts/check.sh 2>&1 | tail -6

## Claude · 154 s

I updated `spec/2026-10-19-han-chot-cho-viec.md` with every answer from `demo/sdlc-5/tra-loi-gia-dinh.md`. It's still `Status: draft`, still in Vietnamese, and I didn't change any other file.

**What changed**
- **A1–A15 are now settled statements in the body**, each with its source, for example `[answer A3, Linh]`, in the same style as the backup spec. The Assumptions section says where the answers come from.
- **C1, C2 and C3 are now marked "Đã quyết" (decided).** C2 went with option (b): the spec now covers the backup file format, and the backup work ships as a separate PR after the due-date PR. C3 went with option (a): the existing "not saved" message now covers due-date saves.
- **F2 (setting, changing, clearing a due date):** clearing a due date now has a 10-second Undo. Changing it to another date has no Undo.
- **F3 (showing due dates):** "today" comes from the device's local date (`getFullYear`/`getMonth`/`getDate`), not `toISOString()`, which gives the UTC date and is a day off at UTC+7.
- **New flow F5 for backup:**
  - Backup files are now `version: 2`, with an optional `dueDate` on each todo.
  - Old `version: 1` files can still be imported.
  - A `version: 1` file that contains `dueDate` is still rejected.
  - A broken `dueDate` in an imported file rejects the whole file.
- **Data section:** adds `app/backup.js` to the files that change (in the backup PR) and states that Khoa will change policy-security S1 himself. The spec itself doesn't touch the policy.
- **Acceptance criteria:**
  - Criterion 6 now includes the Undo steps.
  - Criterion 3 adds the UTC+7 case.
  - New criterion 13: setting a due date while saving fails shows the "not saved" message.
  - New criteria 14–16 cover backup round-trip, importing old `version: 1` files, and the rejection cases.
- **Header:** I changed it to `policy-ux@2`, because the file now says version 2 and U2 changed in that version. Risk now also lists line 1 of the risk list ("personal data leaving the user's device"), because backup files now carry due dates.

**New open items (4 assumptions, 1 concern)**
- **A16:** the Undo wording ("Đã bỏ hạn chót của việc …" with a "Hoàn tác" button) and when the button disappears. → Linh
- **A17:** the two PRs ship in the same release. Otherwise, in between, backups silently drop due dates, because `pick` in `app/backup.js` keeps only four fields. → Khoa, Thảo
- **A18:** the app always writes `version: 2`, even when no todo has a due date. → Khoa
- **A19:** due dates in the backup file are still fine under P2 and P3, so the privacy owner doesn't need to review the format again. → Mai
- **C4:** A14 keeps a broken `dueDate` in storage, and C2 rejects a whole imported file with a broken `dueDate`. Together, a backup of such a list can't be imported back, and the user isn't told. That conflicts with U1. The spec lists three options and doesn't choose. → Khoa, Linh

`bash scripts/check.sh` passes; only the spec changed:
```
ℹ tests 46
ℹ pass 46
ℹ fail 0
== check: OK
```
