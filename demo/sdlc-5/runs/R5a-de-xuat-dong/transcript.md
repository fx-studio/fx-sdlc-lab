# R5a-de-xuat-dong

Chạy 2026-11-04 09:55 ở gốc repo, chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Review has now flagged the same mistake twice: review/1/R2-review/findings.json (PR 1) and review/2/R4-review-0/findings.json (PR 2) both report that the change added tests but left CLAUDE.md's healthy check output (the test count) out of date. Following the Deploy section of CLAUDE.md, propose the fix for 'Things Claude gets wrong'. Write your proposal to review/r5-de-xuat.md (the exact text you would add or change in CLAUDE.md, and why). Do not edit CLAUDE.md: a person decides.

## Tool call (12)

1. Bash · command=ls -R review/
2. Read · file_path=<repo>/review/1/R2-review/findings.json
3. Read · file_path=<repo>/review/2/R4-review-0/findings.json
4. Grep · pattern=claude_md_outdated|tests 4[0-9]|test count
5. Grep · pattern=CLAUDE.md|out of date|outdated
6. Read · file_path=<repo>/review/2/watch.md
7. Read · file_path=<repo>/review/2/watch-1/findings.json
8. Read · file_path=<repo>/review/1/approval.md
9. Grep · pattern=CLAUDE
10. Grep · pattern=tests 4|pass 4|== check
11. Bash · command=bash scripts/check.sh
12. Write · file_path=<repo>/review/r5-de-xuat.md

## Claude · 68 s

I wrote the proposal to `review/r5-de-xuat.md`. I did not edit `CLAUDE.md`.

**One of your two sources is wrong.** `review/2/R4-review-0/findings.json` doesn't report this mistake. That review ran on PR 2's first version (head 80c5c4a), which added no tests, so `claude_md_outdated` is `false`. Its finding is a Nit about the missing tests, which is a different mistake. The real second occurrence is in `review/2/watch-1/findings.json` (head 5a6d21b). By then the PR had grown from 44 to 49 tests and CLAUDE.md still said 44. That review also flagged that PR.md's check block said 44, so it wasn't pasted from a real run. The "same mistake twice" condition still holds; only the evidence file changes.

**Proposed line** for "Things Claude gets wrong":

```markdown
- 2026-11: Adding or removing tests without updating the healthy output under Verification (`ℹ tests N` / `ℹ pass N`), and
  writing a PR's check block from memory instead of pasting it (PR 1, PR 2). After the last test change, run
  `bash scripts/check.sh`, paste its real last lines into PR.md, and if the count changed, set the same N in CLAUDE.md in that PR.
```

**Decisions for you** (all in the file):
- **Cost of the line:** `scripts/pr.py` rates any PR that touches `CLAUDE.md` as high risk. In PR 2, changing just these two number lines raised the PR from medium to high. With this line, every PR that adds tests would become high risk. There are two ways out:
  - Let `pr.py` ignore a diff that only changes the count lines.
  - Drop the exact number from Verification, so this mistake can't happen and the line isn't needed. The cost is that a silently lost test would no longer show up.
- **If it happens a third time:** the line becomes a hook. `scripts/check.sh` could compare the real test count with the one in CLAUDE.md and fail when they differ. I haven't written that.
- **`main` is out of date right now:** `bash scripts/check.sh` on `main` ends with:
  ```
  ℹ tests 45
  ℹ pass 45
  ℹ fail 0
  == lint: node --check app/*.js tests/*.js
  == check: OK
  ```
  `CLAUDE.md:69-70` still says 44. That needs a person to fix, ideally in the same commit as the new line.
