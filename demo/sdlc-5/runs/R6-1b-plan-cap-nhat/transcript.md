# R6-1b-plan-cap-nhat

Chạy 2026-11-04 10:10 ở gốc repo, chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

The people answered the open questions of plan/2026-10-19-han-chot-cho-viec.md and the tech lead approved it with conditions: see the section 'Vòng hai' of demo/sdlc-5/tra-loi-gia-dinh.md. Update the draft plan with every answer and condition (Q3 change plus its tests, Q5 'Đã hoàn tác.', A16 texts, C4 = (a), Q7 decision). Keep Status: draft: a person accepts it. Do not write code, do not touch other files.

## Tool call (37)

1. Read · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
2. Read · file_path=<repo>/demo/sdlc-5/tra-loi-gia-dinh.md
3. Glob · pattern=demo/sdlc-5/runs/B6p-*/**
4. Read · file_path=<repo>/demo/sdlc-5/runs/B6p-khoa-tech-lead/transcript.md
5. Read · file_path=<repo>/demo/sdlc-5/runs/B6p-linh-ux-owner/transcript.md
6. Grep · pattern=message|notices|aria-live|role=
7. Grep · pattern=Đã hoàn tác
8. Grep · pattern=MESSAGES|notSaved|function (show|commit|persist)
9. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
10. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
11. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
12. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
13. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
14. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
15. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
16. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
17. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
18. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
19. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
20. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
21. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
22. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
23. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
24. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
25. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
26. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
27. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
28. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
29. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
30. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
31. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
32. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
33. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
34. Edit · file_path=<repo>/plan/2026-10-19-han-chot-cho-viec.md
35. Grep · pattern=chưa trả lời|chờ Linh|chờ Khoa|đề xuất của plan|nếu chọn|chưa có quyết định|Status:
36. Bash · command=git status --short
37. Bash · command=bash scripts/check.sh 2>&1 | tail -n 6

## Claude · 194 s

I updated `plan/2026-10-19-han-chot-cho-viec.md` with every answer from "Vòng hai" and with Khoa's three conditions. It is still `Status: draft`, so a person still has to accept it. I edited no other file and wrote no code.

**What changed in the plan**
- **Header:** says Khoa approved with three conditions and that all three are now written into the plan. Size is Large (Khoa, Q1).
- **Q1–Q7:** each one now shows the decision instead of a proposal, with who made it. The spec questions A16–A19 and C4 are in a table of answers.
- **Q3 (fix plus tests):**
  - In the design: a date change on a row is saved only when the new value is a valid date. An empty field does nothing at that moment, so Backspace while typing no longer deletes a saved due date. Removing the date is decided when the field loses focus, by comparing with its value when it gained focus.
  - Tests added: four app tests (Backspace while typing, change-then-clear, set-then-clear in one focus, a broken date left as is) and the matching checks in hand test T4.
- **Q5:** after "Hoàn tác", the message area shows the new line D9 "Đã hoàn tác." when the save works, and the "not saved" line D7 when it fails. Linh had asked whether screen readers announce it: they do, because the message area is a live region (`app/index.html:12`). I added this to the tests, to T3 and to T8.
- **Q7:** PR A goes first and builds one shared Undo, `offerUndo(message, restore)`, plus D9. PR 2 rebases later and reuses them. If PR 2 is merged first anyway, step 1 of PR A stops and reports.
- **A16:** the texts D5 "Đã bỏ hạn chót của việc {tiêu đề}." and D6 "Hoàn tác", and when the button disappears, are now Linh's confirmed answers.
- **C4 = (a):** the backup copies a due date only when it is valid. A broken date is left out of the file without any message. I added this to the design, the risks, a new backup test, the export-then-import test, and T11.
- **A17–A19:** recorded. Production waits for PR B, the backup always writes `version: 2`, and Mai does not need to review the file format again.

**For the reviewer:** I made three small choices the answers didn't cover. They are listed in Risks:
- If a date is set and then cleared while the field still has focus, it is removed with no message and no Undo button.
- "Hoàn tác" brings back the date that was saved when it was removed, not the one from before the field had focus.
- Leaving the field while the date is half-typed counts as removing it, and Undo is offered.

`bash scripts/check.sh` on the current tree (no code changed):
```
ℹ tests 46
ℹ pass 46
ℹ fail 0
== check: OK
```
