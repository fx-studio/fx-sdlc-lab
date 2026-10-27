# B0a-write-spec-ux2

Chạy 2026-10-27 09:11 ở gốc repo, chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

/write-spec intent/2026-10-19-khach-khong-mat-viec.md — the existing spec/2026-10-19-khach-khong-mat-viec.md was written against policy-ux@1; policy-ux is now version 2. Write the spec again from scratch against the current policy versions and overwrite that file.

## Tool call (14)

1. Bash · command=cat intent/2026-10-19-khach-khong-mat-viec.md && echo ===== && ls .claude/skills/ app/ spec/ && for f in .claude/skills/policy-*/SKILL.md .claude/skills/write-spec/template.md .claude/skills/write-spec/risk-list.md .claude/skills/write-spec/checklist.md; do echo "===== $f"; cat "$f"; done
2. Read · file_path=<repo>/intent/2026-10-19-khach-khong-mat-viec.md
3. Glob · pattern={.claude/skills/policy-*/**,.claude/skills/write-spec/**,app/**,spec/**}
4. Read · file_path=<repo>/.claude/skills/policy-privacy/SKILL.md
5. Read · file_path=<repo>/.claude/skills/policy-security/SKILL.md
6. Read · file_path=<repo>/.claude/skills/policy-ux/SKILL.md
7. Read · file_path=<repo>/.claude/skills/write-spec/template.md
8. Read · file_path=<repo>/.claude/skills/write-spec/risk-list.md
9. Read · file_path=<repo>/.claude/skills/write-spec/checklist.md
10. Read · file_path=<repo>/app/store.js
11. Read · file_path=<repo>/app/app.js
12. Read · file_path=<repo>/app/index.html
13. Read · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
14. Write · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md

## Claude · 100 s

I've rewritten the spec against the current policy versions. It's saved as a draft and nothing was committed.

**Self-check**

- [x] **Versions:** line 2 says `policy-privacy@1, policy-security@1, policy-ux@2`, the versions I read.
- [x] **Sourced:** every statement in the body has a source in brackets. Anything I couldn't source is under Assumptions or Concerns.
- [x] **Assumptions:** all 12 are yes/no questions with the person who answers.
- [x] **Policies:** all 14 rules are covered. P5 doesn't apply; the other 13 are listed under Policy constraints, and those only partly met point to Concerns or Assumptions.
- [x] **Conflicts:** nothing was resolved silently. The old C1 conflict (S2 against U2) is gone because U2 v2 itself says imports that replace more than one item must ask for confirmation first, as S2 requires. The spec follows that wording and does not choose between them. The 1 MB limit against the "never lose data silently" rule (C2) is still open, with options and no choice made.
- [x] **Scope:** no sync, accounts, due dates or recovery for the 23 customers. The existing single-item actions are left unchanged.
- [x] **Acceptance criteria:** all 15 can be checked by a test or by following steps. Criterion 15 will be written once A3 is answered.
- [x] **Carried forward:** both of the intent's open questions for Lan are listed.

**File:** `spec/2026-10-19-khach-khong-mat-viec.md`. Status is `draft`. Risk is `high` because it matches line 1 of the risk list: "personal data leaving the user's device".

**12 assumptions, 4 concerns.**

What changed from the policy-ux@1 version:
- **Importing over an existing list:** this is now designed. If the list has 2 or more items, the app asks for confirmation first (F2 step 6, criteria 4 and 10).
- **New A3:** if the list has exactly 1 item, does that count as a single-item action, so it runs at once with 10 seconds of Undo? Linh and Khoa answer.
- **New A2:** does "import again" mean replacing the whole list rather than merging? The product owner answers.
- **New C4:** U2 v2 says single-item actions get 10 seconds of Undo. The app's delete button doesn't have that today, and the intent doesn't ask to change it. The product owner and Linh decide whether to include it now.

Before the product owner and tech lead look at it, you could run the `spec-reviewer` agent on it.
