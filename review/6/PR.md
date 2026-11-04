# PR 6 · Hạn chót · bước 4–5a: cơ chế Hoàn tác dùng chung

Branch: `pr/6-han-chot-undo` · Base: `pr/5-han-chot-co-tran` (f07ff41)

Spec: `spec/2026-10-19-han-chot-cho-viec.md` (accepted) · Plan: `plan/2026-10-19-han-chot-cho-viec.md` (accepted), PR A, bước 4–5a
theo mục Tiến độ (Khoa chọn (b): ba PR dưới trần 400 dòng). Size: **Large** (plan Q1).

## What changes

Commit `2a40506`, 176 dòng đổi so với base `pr/5-han-chot-co-tran` (168 thêm, 8 bớt, 5 file).

- `app/app.js`: một cơ chế Undo dùng chung (Q7), không gắn với hạn chót, để PR 2 dùng lại khi rebase:
  - `let undo = null` (`{ restore, timer }`, chỉ trong bộ nhớ trang), `UNDO_MS = 10000`.
  - `offerUndo(message, restore)`: `show(message)`, hiện `#undo`, hẹn giờ 10 giây gọi `clearUndo()`; gán `undo` **sau** `show()`.
  - `clearUndo()`: `clearTimeout`, `undo = null`, ẩn `#undo`. `show()` gọi nó trước mỗi câu mới, nên thêm, đánh dấu, xoá, nhập file
    làm nút mất (A16); lọc không gọi `show()` nên nút còn.
  - `undoLast()` (nút "Hoàn tác"): `restore()`, lưu qua `persist(store, todos)`, `render()`, rồi D9 "Đã hoàn tác." hoặc D7 khi lưu
    lỗi (Q5, U1).
  - `commit()` tách thành `save()` (lưu + hiện câu) rồi `render()`; `add`/`toggle`/`remove` vẫn gọi `commit()`, hành vi không đổi.
- `app/index.html`: `<button type="button" id="undo" hidden>Hoàn tác</button>` sau `#message` trong `#notices` (`role="status"`);
  `<script src="due.js">` giữa `store.js` và `backup.js` (Q2).
- `app/style.css`: khoảng cách và vòng focus cho `#undo` (vòng trên `:focus`, như nút của hộp xác nhận).
- `tests/static.test.js`: **sửa test đang ghim hành vi cũ** "scripts load in the order store, backup, app" → `store, due, backup, app`
  (plan, Files that change); vòng "chỉ store chạm bộ nhớ" thêm `due.js`; test mới: `#undo` là `<button>` ẩn trong `#notices`, chữ
  bằng `DUE_TEXT.undo` (D6); test mới: `app.js`, `due.js` không gọi `.toISOString(` (A9).
- `tests/app.test.js`: `loadApp` nạp thêm `due.js`, có `setTimeout`/`clearTimeout` giả, `store.save` đổi được kết quả, trả `ctx` để
  gọi `offerUndo`. Test cũ giữ nguyên. Năm test mới: hiện câu + nút, bấm thì khôi phục, lưu, vẽ lại, D9, nút ẩn, bấm lần hai không làm
  gì · hết 10 giây nút mất, câu còn · thêm/đánh dấu/xoá/nhập file làm nút mất, lọc thì không · lời mời mới thay lời mời cũ và dừng hẹn
  giờ cũ · lưu lỗi → D7, không bao giờ D9; `skipped` → D9.

Chưa làm (bước 4–5b, PR sau): ô ngày, "Hạn …", "Quá hạn", "Xếp theo", `setDue`/`clearDue`, giữ focus khi vẽ lại, chú thích dòng 1
của `app.js`, test luồng hạn chót. Chưa chỗ nào trong app gọi `offerUndo`, nên trên màn hình app chạy y như cũ; test gọi `offerUndo`
trực tiếp.

### Cho người review xem

1. **`due.js` được nạp ở PR này**, không đợi 4–5b: `undoLast()` dùng `DUE_TEXT.undone` (D9, plan đặt D9 trong `DUE_TEXT`). Kéo theo
   việc sửa test thứ tự script ở đây. Mục Tiến độ không nói rõ phần `index.html` nào thuộc 5a; nếu muốn D9 nằm ngoài `due.js`
   (Undo là chung, PR 2 cũng dùng), đó là thay đổi plan.
2. **`skipped` (đọc lỗi) sau khi bấm Hoàn tác → D9.** Plan Q5 chỉ nói "lưu được → D9, lưu lỗi → D7"; `persist` không có câu cho
   `skipped` (dải báo đọc lỗi đã có), nên đi theo Q4. Có test pin.
3. **Sao lưu ra file cũng làm nút mất**, vì `#export` gọi `show()`. A16 không nhắc tới sao lưu; plan Thiết kế nói "mọi lần hiện câu mới".
4. **Focus sau khi bấm Hoàn tác:** nút ẩn đi nên focus rơi về `body`. Plan không nói focus đi đâu; T8 (chỉ bàn phím) sẽ thấy. Chưa sửa,
   cần một quyết định (ví dụ focus về dòng việc vừa khôi phục, ở 5b).
5. Test toISOString lúc đầu khớp cả chữ trong chú thích của `due.js` (PR 5) nên fail; đã đổi test thành khớp lời gọi `.toISOString(`,
   không sửa `due.js`.
6. `scripts/pr.py show 6` tính so với `main`, nên số dòng ở mục dưới gồm cả PR 5 (và dòng CLAUDE.md của R6-2B). Riêng PR này: 176 dòng.

Commit đi qua mà pre-commit không chặn; plan không bị sửa (mục Tiến độ của bước 4–5a do người ghi).

## How it was checked

`bash scripts/check.sh` trên `2a40506` (head của nhánh, sau thay đổi cuối):

```
== test: node --test
ℹ tests 63
ℹ pass 63
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

Chưa chạy: subagent `verifier`, `python3 scripts/review.py 6`, kiểm tay T0–T10 (plan bước 6–7; nút chưa có đường gọi trên màn hình
nên kiểm tay có nghĩa từ 4–5b).

<!-- pr.py -->
## Size and risk (computed by scripts/pr.py)

176 lines in 5 files · risk **medium** → 1 code owner, who reads the plan
