# R1-B-verification-co

Chạy 2026-10-29 14:27 ở `r1-B` (thư mục riêng của lượt này), chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

The filter buttons (Tất cả / Chưa xong / Đã xong) do not tell a screen reader which one is selected. Add aria-pressed: true on the selected button, false on the others, kept in sync when the filter changes. Tell me when it is done.

## Tool call (11)

1. Grep · pattern=filter|Tất cả|aria
2. Read · file_path=<thư-mục-tạm>
3. Grep · pattern=filter|aria-pressed|classList
4. Read · file_path=<thư-mục-tạm>
5. Edit · file_path=<thư-mục-tạm>
6. Edit · file_path=<thư-mục-tạm>
7. Edit · file_path=<thư-mục-tạm>
8. Bash · command=node --test tests/app.test.js
9. Edit · file_path=<thư-mục-tạm>
10. Edit · file_path=<thư-mục-tạm>
11. Bash · command=bash scripts/check.sh

## Claude · 41 s

The filter buttons now have `aria-pressed`, and the check passes. I picked size **Small**: one behaviour, two app files and a test. There's no committed plan, and I haven't committed anything. The changes are waiting for you to review.

**What changed**
- `app/index.html`: the page loads with "Tất cả" set to `aria-pressed="true"` and "Chưa xong" / "Đã xong" set to `"false"`.
- `app/app.js`: the filter click handler sets `aria-pressed` on all three buttons each time, right next to the existing `on` class, so the two always match.
- `tests/app.test.js`: I added three fake filter buttons to `loadApp` and a new test. It checks the starting state, then picks "Chưa xong", "Đã xong" and "Tất cả" in turn, and each time only the selected button should be `true`.

I ran the new test before changing the app and it failed for the expected reason: after clicking "Chưa xong", the attributes still read `all=true open=false`. With the change in place, `bash scripts/check.sh` ends with:

```
ℹ tests 43
ℹ pass 43
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

That's 43 tests rather than the 42 in CLAUDE.md, because of the new one. I only tested with the fake DOM. I didn't open the app in a browser or try it with a real screen reader.
