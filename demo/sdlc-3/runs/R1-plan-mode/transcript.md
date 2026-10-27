# R1-plan-mode

Chạy 2026-10-27 09:31 ở gốc repo, chế độ quyền `plan`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Attached: intent/2026-10-19-khach-khong-mat-viec.md and its accepted spec, spec/2026-10-19-khach-khong-mat-viec.md. Write an implementation plan for this change: which files change, the order of work, and which tests prove each step is right. Ask me if anything is unclear.

## Tool call (6)

1. Bash · command=cat intent/2026-10-19-khach-khong-mat-viec.md spec/2026-10-19-khach-khong-mat-viec.md && ls -la app tests plan .claude/hooks scripts && wc -l app/* tests/*
2. Read · file_path=<repo>/spec/2026-10-19-khach-khong-mat-viec.md
3. Bash · command=ls -la app tests plan scripts .claude/hooks .claude/agents; cat app/store.js app/app.js app/index.html; ls app; cat tests/* 2>/dev/null | head -200
4. Bash · command=cat app/style.css .claude/hooks/protect-paths.py .claude/hooks/check-js.py scripts/pre-commit .claude/agents/verifier.md; cat .claude/settings.json 2>/dev/null; ls demo/sdlc-3 | head -30; cat .claude/skills/policy-security/SKILL.md | head -60
5. Write · file_path=<home>/.claude/plans/attached-intent-2026-10-19-khach-khong-m-playful-hoare.md
6. Edit · file_path=<home>/.claude/plans/attached-intent-2026-10-19-khach-khong-m-playful-hoare.md

## Claude · 135 s

I've written a draft plan, in Vietnamese like the spec: `<home>/.claude/plans/attached-intent-2026-10-19-khach-khong-m-playful-hoare.md`. Once you approve it, I'll copy it to `plan/2026-10-19-khach-khong-mat-viec.md` as `Status: draft`. A person still has to accept it before I write any code. I haven't changed anything in the repo.

**Size:** I picked Medium. It touches five app files, adds one new module, and adds the repo's first tests (`tests/` is empty today). Question 1 below asks whether it should be Large instead.

**Files that change:**
- `app/store.js`:
  - `load()` reports whether the saved list could be read (the three failure cases in A13).
  - `save()` returns `saved`, `failed` or `skipped`.
  - While the saved list is unreadable, it never writes to storage. The only way to write is a new `replace()` used by import, and that clears the unreadable state only when the write succeeds.
  - Keeping the "never overwrite unreadable data" rule here means a Node test can check it.
- `app/backup.js` (new): plain logic with no page code, so Node tests can run it. It builds the backup text and file name, checks imported files, builds the three confirmation sentences, and holds all the new wording.
- `app/app.js`: wires in the buttons, the confirmation dialog, the message area, the warning banner for unreadable data, and the empty-list line. `commit()` now acts on what `save` returns.
- `app/index.html` and `app/style.css`: the new page elements and their styles.
- `tests/store.test.js`, `tests/backup.test.js`, `tests/static.test.js`: run with `node --test` against a fake browser storage that can be made to fail on read or write.

**Order of work:** store → backup → HTML/CSS → app.js → test by hand in the browser and run the `verifier` subagent. The store and app.js changes go in one commit, because changing what `load()` returns would break the app in between.

**Proof:** the plan maps each of the 26 acceptance criteria to a test or to a manual browser check. Some can only be checked by hand: downloading, picking a file, the dialog, keyboard use, the screen reader, and the Network tab.

**Questions before you accept it:**
1. **Medium or Large?** The spec says `Risk: high` and the change rewrites the storage code. If it's Large, Khoa approves the plan before any code.
2. **Is adding `app/backup.js` OK?** The spec lists only four files to change. A separate file lets Node tests check the import rules and the wording without a browser.
3. **How many bytes is "1 MB"?** 1,048,576 or 1,000,000. This is Khoa's call as owner of the 1 MB rule (S1).
4. **What about a valid file with an empty list (`todos: []`)?** I suggest rejecting it, because importing it would empty the list. The alternative is to allow it with a confirmation.
5. **What if `todo.v1` holds the text `"null"`?** A13 makes that "can't read the saved list"; today's code treats it as an empty list. I followed A13.
6. **Are manual checks enough for the browser-only criteria** (2, 25, and the download/file-picker/dialog parts)? A person would run them.

A few smaller choices are listed under Risks for the reviewer:
- A title that is only spaces is rejected, the same as an empty title.
- Any `version` other than 1 is rejected.
- When the backup is too big to import again, only the agreed C2 sentence is shown, not a count of tasks saved.
