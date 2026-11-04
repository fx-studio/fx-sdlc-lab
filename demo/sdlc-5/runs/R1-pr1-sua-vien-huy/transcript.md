# R1-pr1-sua-vien-huy

Chạy 2026-11-04 09:37 ở `pr-1` (thư mục riêng của lượt này), chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

You are working on local pull request #1 in this worktree (branch pr/1-huy-hien-vien). A person found this during manual keyboard testing (Firefox on macOS, see demo/sdlc-4/README.md, section Kiểm tay): when the import confirmation dialog opens, the 'Huỷ' button has focus (it has autofocus) but shows no focus ring, so a keyboard user cannot see where they are. Fix it, following CLAUDE.md. Commit on this branch. Then fill in the PR description at ../../review/1/PR.md (sections 'What changes' and 'How it was checked'), and stop: a person reviews and merges.

## Tool call (16)

1. Bash · command=ls app tests review/1 ../../review/1 2>&1; cat ../../review/1/PR.md
2. Glob · pattern={app/**,tests/**}
3. Read · file_path=<repo>/review/1/PR.md
4. Grep · pattern=Kiểm tay
5. Read · file_path=<repo>/.worktrees/pr-1/app/style.css
6. Read · file_path=<repo>/.worktrees/pr-1/app/index.html
7. Grep · pattern=focus|dialog|showModal|Huỷ
8. Read · file_path=<repo>/.worktrees/pr-1/tests/static.test.js
9. Grep · pattern=(?i)focus|keyboard|bàn phím
10. Edit · file_path=<repo>/.worktrees/pr-1/tests/static.test.js
11. Bash · command=node --test tests/static.test.js
12. Edit · file_path=<repo>/.worktrees/pr-1/app/style.css
13. Bash · command=bash scripts/check.sh
14. Bash · command=git add app/style.css tests/static.test.js
15. Bash · command=git commit -m "PR 1: nút Huỷ trong hộp xác nhận nhập hiện viền khi có focus

Firefox (macOS) không vẽ viền focus cho nút Huỷ có autofocus khi hộp xác nhận
mở sau hộp chọn file: heuristic :focus-visible không coi đó là focus bàn phím.
Thêm 'dialog button:focus' (cùng viền với #import-label) và một test tĩnh
trong tests/static.test.js (U5).

Co-Authored-By: Claude Opus 5.5 <<email>>"
16. Edit · file_path=<repo>/review/1/PR.md

## Claude · 48 s

The fix is committed on `pr/1-huy-hien-vien` (commit `4ec1f73`), but nobody has tried it in a browser yet. A person still needs to repeat T12 by keyboard in Firefox on macOS and confirm "Huỷ" now shows a ring when the dialog opens.

I sized it as **Small**, so plan mode with no committed plan.

- **Cause (probable, not confirmed in a browser):** browsers only draw their default focus ring when they think focus came from the keyboard. The dialog opens just after the file picker closes, and at that moment Firefox doesn't treat the `autofocus` on "Huỷ" as keyboard focus. So the button has focus but no ring.
- **Fix:** one rule in `app/style.css`: `dialog button:focus { outline: 2px solid #1a5fd0; outline-offset: 2px; }`. It's the same ring the "Nhập từ file" label already uses, and it applies to any focus, so the browser's guess no longer matters. Side effect: clicking a dialog button with the mouse also shows the ring for a moment before the dialog closes.
- **Test first:** I added a test in `tests/static.test.js` and ran it before the fix. It failed because `style.css` had no such rule. The test only checks that the rule exists; it can't reproduce Firefox's focus behaviour.
- **Result:** the test passes after the fix, and the count goes from 44 to 45.

```
ℹ tests 45
ℹ pass 45
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

I filled in "What changes" and "How it was checked" in `review/1/PR.md`, including the output of the test failing before the fix. That file lives in the main checkout and I didn't commit it.

I'm stopping here: reviewing and merging are yours.
