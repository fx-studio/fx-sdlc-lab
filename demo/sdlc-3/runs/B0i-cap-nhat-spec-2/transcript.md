# B0i-cap-nhat-spec-2

Chạy 2026-10-27 09:23 ở gốc repo, chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Round two: A13–A16 of spec/2026-10-19-khach-khong-mat-viec.md are now answered (see the second table in demo/sdlc-3/tra-loi-gia-dinh.md, Vietnamese). Update the spec draft with Edit: move each answer into the body sourced as [answer A<n>, <name>], use Linh's A16 wording verbatim, add or adjust acceptance criteria. Keep Status: draft. Re-run the write-spec checklist and report remaining open assumptions.

## Tool call (17)

1. Read · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
2. Read · file_path=<repo>/demo/sdlc-3/tra-loi-gia-dinh.md
3. Glob · pattern=.claude/skills/write-spec/**
4. Read · file_path=<repo>/.claude/skills/write-spec/checklist.md
5. Read · file_path=<repo>/.claude/skills/write-spec/SKILL.md
6. Read · file_path=<repo>/app/store.js
7. Read · file_path=<repo>/.claude/skills/policy-security/SKILL.md
8. Read · file_path=<repo>/.claude/skills/policy-ux/SKILL.md
9. Bash · command=git diff --stat && ls demo/sdlc-3 demo/sdlc-3/runs 2>/dev/null | head -50
10. Bash · command=cd <repo>/demo/sdlc-3/runs && ls B0g-* B0h-* B0i-* && wc -c B0g-*/* B0h-*/*
11. Read · file_path=<repo>/demo/sdlc-3/runs/B0g-khoa-gia-dinh-moi/transcript.md
12. Read · file_path=<repo>/demo/sdlc-3/runs/B0g-linh-gia-dinh-moi/transcript.md
13. Read · file_path=<repo>/demo/sdlc-3/runs/B0h-thao-a15/transcript.md
14. Edit · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
15. Bash · command=cp <repo>/spec/2026-10-19-khach-khong-mat-viec.md <thư-mục-tạm>
16. Write · file_path=<thư-mục-tạm>
17. Bash · command=cd <thư-mục-tạm> && git diff --no-index --stat <repo>/spec/2026-10-19-khach-khong-mat-viec.md 2026-10-19-khach-khong-mat-viec.md; grep -c "Status: draft" 2026-10-19-khach-khong-mat-viec.md

## Claude · 181 s

**The spec in the repo is unchanged.** My Edit on `spec/2026-10-19-khach-khong-mat-viec.md` was stopped by a permission prompt, and so was a `cp` from that file. So I wrote the full updated draft here instead:

`<thư-mục-tạm>`

Allow the edit and I'll apply it to the repo file, or copy the file over yourself. It is still `Status: draft`. I also didn't write anything to `demo/sdlc-3/runs/B0i-cap-nhat-spec-2/`.

**What changed**
- **F5** now holds the answers, each with its source:
  - **A13 (Khoa):** "can't read" covers three cases: data that won't parse, data that isn't a list, and the browser storage throwing an error. Khoa added the third case. No `todo.v1` key means a normal empty list.
  - **A14 (Khoa · Linh):** nothing is written while the list can't be read. Changes stay on screen but aren't saved. Per Linh, the warning is a fixed banner at the top, with no dialog on each action. Khoa's reason also covers "backing up still works, using what's on screen".
  - **A15 (Khoa · Thảo):** importing a file is the only way to replace the damaged data. The file gets the same checks as F2 step 3. The confirmation reads "Thay danh sách đã lưu không đọc được bằng 30 việc trong file?" (replace the saved list that can't be read with 30 items from the file?).
  - **A16 (Linh):** her wording is used verbatim: "Không đọc được danh sách đã lưu trên trình duyệt này. Việc bạn thêm hoặc sửa lúc này sẽ không được lưu. Nếu có file sao lưu, hãy bấm "Nhập từ file"." (the saved list can't be read; anything added or changed now won't be saved; if there's a backup file, press "Nhập từ file").
- **F2 step 9, screen states, Data and integrations, Policy constraints (S1, S2, U1–U5) and C3** are updated to match.
- **Acceptance criteria:** 15 is rewritten to check the exact message and that the stored value stays `{hỏng`. Criteria 16–20 are new: data that isn't a list, storage throwing an error, backup during the error, import with confirm/cancel, and a rejected import during the error. The old 17–20 are now 21–24.

**Checklist:** all 8 boxes pass.
- **Versions:** all three policies are listed (privacy@1, security@1, ux@2).
- **Sourced:** every new statement in the body has a source.
- **Assumptions:** the open ones are yes/no questions with who answers.
- **Policies:** every rule is covered, including S2 for the "can't read" case.
- **Conflicts:** none resolved silently. Khoa decided the S2 wording in A15, and one remaining edge is A19.
- **Scope:** no recovery or sync was designed.
- **Acceptance criteria:** all are checkable. 17 needs a test.
- **Carried forward:** both questions from the intent are still listed.

**Open assumptions (3 new, found while putting A13–A16 into the body):**
- **A17:** After a successful import during the error, does the banner go away and normal saving resume? → Khoa, Linh. Criterion 19 depends on this.
- **A18:** When the list can't be read and nothing is on screen, should the app hide the "no items yet" line so it doesn't look like a real empty list? → Linh
- **A19:** The import confirmation doesn't mention items added on screen that were never saved. Does that still meet S2's "say what will be lost"? → Khoa

The two questions from the intent for Lan (copying the 23 emails into `tickets/`, and splitting them by cause) are also still open.

**Two things for whoever reviews it:**
- **Linh's A14 answer** says "Undo 10 giây vẫn chạy như bình thường" (the 10-second Undo still works as usual). The app has no Undo; that gap is C4, left for a separate intent. Her "Có" (yes) doesn't depend on it, so I kept A14 and noted this under C4.
- **Thảo** said "cho spec sang Build" (send the spec to Build) in B0h, before A17–A19 existed. I didn't touch the Status line: per the repo rules, a person sets `Status: accepted` and commits.
