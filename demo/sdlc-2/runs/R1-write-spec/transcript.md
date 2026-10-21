# R1-write-spec

Chạy 2026-10-20 16:55 ở gốc repo. Nguyên văn, không sửa. Luồng thô: `stream.jsonl`.

## Prompt

/write-spec intent/2026-10-19-khach-khong-mat-viec.md

## Tool call (11)

1. Read · file_path=<repo>/intent/2026-10-19-khach-khong-mat-viec.md
2. Bash · command=ls .claude/skills/write-spec .claude/skills/ app spec 2>&1; cat .claude/skills/write-spec/template.md .claude/skills/write-spec/risk-list.md .claude/skills/write-spec/checklist.md
3. Bash · command=for f in .claude/skills/policy-*/SKILL.md; do echo "=== $f"; cat "$f"; done; for f in app/*; do echo "=== $f"; cat -n "$f"; done
4. Read · file_path=<repo>/.claude/skills/policy-privacy/SKILL.md
5. Read · file_path=<repo>/.claude/skills/policy-security/SKILL.md
6. Read · file_path=<repo>/.claude/skills/policy-ux/SKILL.md
7. Read · file_path=<repo>/app/store.js
8. Read · file_path=<repo>/app/app.js
9. Read · file_path=<repo>/app/index.html
10. Bash · command=ls spec demo/sdlc-2 && cat app/style.css | head -50
11. Write · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md

## Claude · 141 s

I wrote the spec as a draft. It hasn't been committed or reviewed yet.

**File:** `spec/2026-10-19-khach-khong-mat-viec.md`
**Counts:** 12 assumptions, 4 concerns. **Risk: high**, because it matches line 1 of the risk list ("personal data leaving the user's device"): the backup file exists to carry the todo list off this browser and onto another device. So the tech lead (Khoa) needs to review it too, not just the product owner.

**Self-check against `checklist.md`:**
- [x] **Versions:** line 2 lists policy-privacy@1, policy-security@1 and policy-ux@1.
- [x] **Sourced:** every statement in the body cites `[intent]`, `[app/...]` or `[policy-...#..]`. Details I chose without a source (file name, file structure, button placement, suggested wording) are in Assumptions.
- [x] **Assumptions:** each one is a yes/no question with the person who answers it.
- [x] **Policies:** all 14 rules were checked. P5 doesn't apply; the other 13 are listed under Policy constraints, and the ones that can't be fully met are raised under Concerns.
- [x] **Conflicts:** S2 and U2 conflict, and I didn't pick a side (C1).
- [x] **Scope:** there is no device sync, no accounts and no recovery for the 23 customers. The missing Undo on the existing delete button is noted as out of scope.
- [x] **Acceptance criteria:** there are 13. Criteria 1–12 can each be checked by following steps; criterion 13 can't be written until C1 is decided.
- [x] **Carried forward:** both of Lan's open questions are listed.

**What needs a decision:**
- **C1:** When a customer imports a file while their list already has todos, two rules can't both be followed. Security rule S2 requires asking for confirmation before replacing more than one item. UX rule U2 forbids confirmation dialogs and requires 10 seconds of Undo instead. I listed three options (follow S2, follow U2, or merge instead of replace) for Khoa and Linh to decide. This part of the import flow isn't designed until they do.
- **C2:** The intent's success criteria don't match its scope. The "both devices show the same list" criterion is out of scope. The "new phone" and "cleared browser data" criteria are only met if the customer made a backup beforehand.
- **C3:** S1 caps imported files at 1 MB, but browser storage holds about 5 MB. A customer with a large list could make a backup and then be unable to import it.
- **C4:** When saved data is corrupted, `store.load` returns an empty list, and the next save writes over the old data without telling the customer. The intent only covers failed saves, so I didn't design a fix; the product owner and Khoa need to decide whether it's in scope.

I've stopped here. Committing and changing the status to accepted are for the reviewers to do.
