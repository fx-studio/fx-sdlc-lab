# B0f-cap-nhat-spec

Chạy 2026-10-27 09:19 ở gốc repo, chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

The product owner and the policy owners answered every assumption and concern of spec/2026-10-19-khach-khong-mat-viec.md. Their answers are in demo/sdlc-3/tra-loi-gia-dinh.md (Vietnamese). Update the spec draft to reflect them: turn each answered assumption into body text sourced as [answer A<n>, <name>], design the in-scope part of C3, write the C2 message verbatim, note C1 and C4 as decided. Keep the template, keep Status: draft, re-check the risk label against A12, and re-run the write-spec checklist. Do not touch intent/.

## Tool call (13)

1. Skill · skill=write-spec
2. Read · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
3. Read · file_path=<repo>/demo/sdlc-3/tra-loi-gia-dinh.md
4. Bash · command=git diff spec/ && ls -la demo/sdlc-3/ .claude/skills/write-spec/
5. Bash · command=cat .claude/skills/write-spec/template.md .claude/skills/write-spec/checklist.md .claude/skills/write-spec/risk-list.md && echo ---- && cat app/store.js app/app.js && echo ---- && head -20 intent/2026-10-19-khach-khong-mat-viec.md && ls demo/sdlc-3/runs demo/sdlc-3/personas && cat .claude/skills/policy-*/SKILL.md
6. Bash · command=cd <repo>/demo/sdlc-3/runs && ls -la * && wc -c */* 
7. Bash · command=cat B0e-khoa-c3/transcript.md B0c-khoa-hoi-lai/transcript.md B0e-linh-hoi-lai/transcript.md
8. Bash · command=sed -n '/## Claude/,$p' B0d-thao-chot/transcript.md; sed -n '/## Claude/,$p' B0b-khoa-tra-loi/transcript.md | head -80
9. Read · file_path=<repo>/demo/sdlc-3/runs/B0d-thao-chot/transcript.md
10. Read · file_path=<repo>/demo/sdlc-3/runs/B0b-khoa-tra-loi/transcript.md
11. Write · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
12. Bash · command=echo ok
13. Write · file_path=<thư-mục-tạm>

## Claude · 233 s

The spec isn't updated yet: writing to `spec/2026-10-19-khach-khong-mat-viec.md` was denied. I saved the full updated draft here instead:

`<thư-mục-tạm>`

If you allow the write, I'll put it in place. Or you can copy it over yourself. I didn't touch anything in `intent/`, and nothing is committed.

**What changed**
- **A1–A12:** each answer is now in the body, cited as `[answer A<n>, <name>]`. A3 was answered "Không", so importing over a list with 1 or more tasks always asks first. That includes a list of exactly 1 task ("Thay 1 việc hiện có bằng 30 việc trong file?"), and there is no Undo after an import.
- **C2:** F1 step 5 has the message word for word: **"File sao lưu đã lưu, nhưng quá lớn nên app không nhập lại được."** It also records that Linh leaned towards (b) but left the call to Khoa.
- **C3:** a new flow F5. When the saved list can't be read, the app doesn't overwrite it, tells the user, and doesn't try to recover it. `store.load` must tell "no data yet" apart from "data that can't be read".
- **C1 and C4:** both marked "Đã quyết".
  - C1: the Goal now says the two criteria are met only "khi đã sao lưu trước", and syncing between devices moves to a later intent. The intent itself still has the old wording, and changing it is a person's job.
  - C4: the gap with `policy-ux@2#U2` stays open, and Thảo will open the separate intent.
- **Acceptance criteria:** went from 15 to 20. New ones cover A6, A7, A9, A11, C2, C3 and the 1-task import.

**Risk label against A12:** stays `high`, on risk-list line 1 only. Khoa's condition holds: the spec adds no key or field to browser storage. There's no Undo after import, so the old list isn't stored, and F5's "can't read" state lives only in page memory. Data and integrations now notes that line 2 would match if a later version adds something like that.

**Write-spec checklist: all pass**
- [x] Versions: privacy@1, security@1, ux@2.
- [x] Sourced: everything in the body has a source. One citation points to a transcript rather than the answers file: Khoa accepting under C2 that a file over 1 MB can't be imported, which comes from `runs/B0b-khoa-tra-loi`.
- [x] Assumptions: each is a yes/no question with who answers.
- [x] Policies: each rule is either satisfied or raised.
- [x] Conflicts: the two that came up (A3, C2) were decided by the rule owners, not by me.
- [x] Scope: recovering corrupted data stays out.
- [x] Acceptance criteria: all checkable. Number 16 waits on A15.
- [x] Carried forward: the two questions for Lan are still listed.

**Counts:** 4 open assumptions and 0 open concerns (C1–C4 are all decided). The 4 new assumptions came out of designing C3 and need answers before Build:
- **A13** (Khoa): what counts as "can't read".
- **A14** (Khoa, Linh): whether changes are saved while the stored list can't be read.
- **A15** (Khoa, Thảo): importing in that state, and the confirmation wording, since the number of tasks that would be lost can't be counted.
- **A16** (Linh): the wording of the F5 message.
