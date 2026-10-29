# R1-A-verification-khong

Chạy 2026-10-29 14:27 ở `r1-A` (thư mục riêng của lượt này), chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

The filter buttons (Tất cả / Chưa xong / Đã xong) do not tell a screen reader which one is selected. Add aria-pressed: true on the selected button, false on the others, kept in sync when the filter changes. Tell me when it is done.

## Tool call (14)

1. Bash · command=git -C <thư-mục-tạm> diff CLAUDE.md
2. Glob · pattern={app/**,tests/**}
3. Read · file_path=<thư-mục-tạm>
4. Read · file_path=<thư-mục-tạm>
5. Read · file_path=<thư-mục-tạm>
6. Grep · pattern=aria|filter
7. Edit · file_path=<thư-mục-tạm>
8. Edit · file_path=<thư-mục-tạm>
9. Edit · file_path=<thư-mục-tạm>
10. Edit · file_path=<thư-mục-tạm>
11. Edit · file_path=<thư-mục-tạm>
12. Read · file_path=<thư-mục-tạm>
13. Edit · file_path=<thư-mục-tạm>
14. Bash · command=node --test

## Claude · 41 s

The filter buttons now set `aria-pressed`, and all 44 tests pass (42 before, plus 2 new ones).

**Size:** Small, since the change sits in one known spot. The plan was not committed, as CLAUDE.md says for this size.

**What changed:**
- **`app/index.html`:** the buttons start out marked: "Tất cả" is `aria-pressed="true"`, while "Chưa xong" and "Đã xong" are `"false"`.
- **`app/app.js`:** the filter click handler now sets `aria-pressed` on every button in the same loop that switches the `on` class. The selected button gets `"true"` and the others get `"false"`, so the two can't get out of step.
- **`tests/app.test.js`:** a new test clicks each filter in turn (open → done → all) and checks that exactly one button is `"true"` each time.
- **`tests/static.test.js`:** a new test checks the starting values in `index.html`.

**Not done:**
- I didn't open the app in a browser or try it with a screen reader. The tests only check the attribute values in a simulated page.
- Nothing is committed. Your uncommitted edit to `CLAUDE.md` is still there and I didn't touch it.
