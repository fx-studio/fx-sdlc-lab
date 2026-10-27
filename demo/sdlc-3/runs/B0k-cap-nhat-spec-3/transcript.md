# B0k-cap-nhat-spec-3

Chạy 2026-10-27 09:26 ở gốc repo, chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Round three: A17–A19 of spec/2026-10-19-khach-khong-mat-viec.md are answered (third table in demo/sdlc-3/tra-loi-gia-dinh.md). Update the spec with Edit: move each answer into the body as [answer A<n>, <name>], use Khoa's A19 wording verbatim, adjust acceptance criteria. Keep Status: draft. Re-run the write-spec checklist and report remaining open assumptions, if any.

## Tool call (22)

1. Read · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
2. Read · file_path=<repo>/demo/sdlc-3/tra-loi-gia-dinh.md
3. Glob · pattern=.claude/skills/write-spec/**
4. Read · file_path=<repo>/.claude/skills/write-spec/checklist.md
5. Read · file_path=<repo>/.claude/skills/write-spec/SKILL.md
6. Bash · command=ls <repo>/demo/sdlc-3/ <repo>/demo/sdlc-3/runs/ 2>/dev/null; git -C <repo> diff --stat
7. Glob · pattern=demo/sdlc-3/runs/B0j*
8. Glob · pattern=demo/sdlc-3/**/*B0j*
9. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
10. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
11. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
12. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
13. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
14. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
15. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
16. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
17. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
18. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
19. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
20. Grep · pattern=A1[789]|A20|tiêu chí \d+|Status|bấm "Nhập từ file"."; không
21. Read · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
22. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md

## Claude · 98 s

I've updated the spec with A17–A19. `Status: draft` is unchanged, and nothing has been committed.

**What changed in `spec/2026-10-19-khach-khong-mat-viec.md`**
- **A19 (Khoa), F5 step 6:** there are now two confirmation messages. If nothing is on screen, it uses the A15 wording. If there are unsaved items on screen, it uses Khoa's wording verbatim: **"Thay danh sách đã lưu không đọc được và 3 việc bạn vừa thêm (chưa lưu) bằng 30 việc trong file?"** I also updated the S2 line under Policy constraints to match.
- **A17 (Khoa · Linh):**
  - New F5 step 7: if the write succeeds, the app leaves the read-error state, the banner goes away, and edits save normally again.
  - New F5 step 8: if the write fails, the app stays in the read-error state.
  - Data and integrations now says the read-error flag is only cleared after a successful write.
- **A18 (Linh), screen states:** while in the read-error state, only the F5 banner shows, not the empty-list line. I noted this under U3 as well.
- **Acceptance criteria**, now 26 instead of 24:
  - Changed: 15 now also checks that the empty-list line does not show. 19 checks that the banner goes away after import, and that a new item still saves after a reload (31 items).
  - New: 20 checks the A19 message with 3 unsaved items, on both cancel and agree. 21 checks that a failed write keeps the read-error state (storage full while `todo.v1` holds `{hỏng`).
  - The old 20–24 are now 22–26.
- **C3** now says "A13–A19 đã trả lời; còn mở A20."

**write-spec checklist**
- ✅ **Versions:** policy-privacy@1, policy-security@1, policy-ux@2.
- ✅ **Sourced:** every new statement cites `[answer A17/A18/A19, <tên>]`. One sentence is my own inference from A14 + A19: during the read-error state every item on screen is unsaved, so the number in the message is the number of items on screen. Check that sentence when you review.
- ✅ **Assumptions:** the one open item is written as a yes/no question with who answers it.
- ✅ **Policies:** A19 makes the S2 "say what will be lost" message stricter. The U2 gap stays open as before (C4).
- ✅ **Conflicts:** none new.
- ✅ **Scope:** no change.
- ✅ **Acceptance criteria:** all can be checked. Criterion 21 deliberately leaves out what the screen shows, because that depends on A20.
- ✅ **Carried forward:** the 2 questions for Lan are still there.

**Still open: 1 assumption**
- **A20** (Khoa, Linh): in the read-error state, if the import is confirmed but the write fails, the screen keeps the items from before the import and also shows the F3 "couldn't save" message next to the F5 banner, the same as F2 step 8. Is that right? This came up from Khoa's answer to A17, which says what state the app stays in but not what the screen shows.

There are also 4 concerns, all decided, and 2 questions carried forward for Lan.

There is no B0j transcript under `demo/sdlc-3/`, so the sources for A17–A19 are the third table in `tra-loi-gia-dinh.md`. If B0j should exist as a raw run, it still needs to be saved.

The assumption count goes 12 → 4 → 3 → 1 if you want to add that to the closing line of `tra-loi-gia-dinh.md`.
