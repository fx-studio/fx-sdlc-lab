# PR 7 · Hạn chót · bước 4–5b: ô ngày, Xếp theo, Quá hạn

Branch: `pr/7-han-chot-giao-dien` · Base: `pr/6-han-chot-undo` (2a40506)

Spec: `spec/2026-10-19-han-chot-cho-viec.md` (accepted) · Plan: `plan/2026-10-19-han-chot-cho-viec.md` (accepted), PR A, bước 4–5b
theo mục Tiến độ (Khoa chọn (b): ba PR dưới trần 400 dòng). Size: **Large** (plan Q1).

## What changes

Commit `efb7a18`, **397 dòng** đổi so với base `pr/6-han-chot-undo` (372 thêm, 25 bớt, 5 file): `app/app.js` 90 · `app/index.html` 14 ·
`app/style.css` 15 · `tests/app.test.js` 262 · `tests/static.test.js` 16.

- `app/app.js` (plan Thiết kế, `app.js`):
  - Chú thích dòng 1: việc có thể có `dueDate`.
  - `let sort = 'added'` (không lưu, A11) · `let dirty` (đã lưu hạn chót từ lần `render()` trước, Q3).
  - `add(title, dueDate)`: thêm khoá `dueDate` chỉ khi `isValidDueDate` (AC2, A4). Form xoá cả `#title` và `#due` sau khi thêm.
  - `setDue(id, value)` ở `change`: chỉ ngày hợp lệ và khác ngày đang có → gán, `save()`, vẽ lại **dòng đó** tại chỗ (`drawDue`).
    `''` không làm gì (Backspace giữa lúc gõ, Q3).
  - `clearDue(id, before)` ở `blur` khi ô trống: `dueDate` hỏng → không làm gì (A14); `before === ''` → bỏ hạn, `save()`, không D5,
    không nút; còn lại → bỏ hạn, `persist`, `offerUndo(D7 hoặc D5, restore)` (Q4), `restore` trả lại ngày đang lưu lúc bỏ, việc đã bị
    xoá thì không làm gì.
  - `visible()`: lọc rồi `sortByDue` khi `sort === 'due'` (F4 bước 4, mảng `todos` không đổi, Q6).
  - `drawDue(li, t)`: "Hạn …", "Quá hạn", class `done`/`overdue`; "hôm nay" = `localDateString(new Date())` mỗi lần gọi (F3).
  - `render(focusTo = document.activeElement)`: dòng có `<span class="due">`, `<span class="overdue-tag">`, `<input type="date">`
    trong `<span class="when">`; mẫu `innerHTML` không có chữ người dùng; nhãn D2 bằng `setAttribute`, chữ bằng `textContent` (S3).
    Mỗi ô của dòng có `dataset.id`/`dataset.part` (`toggle`/`due`/`remove`); vẽ xong thì focus lại đúng ô của đúng việc (AC9).
    Ô ngày: `focus` nhớ `before`, `change` → `setDue`, `blur` → `clearDue` nếu trống, rồi `render(e.relatedTarget)` nếu `dirty`.
  - `#sort` `change` → `sort`, `render()`.
- `app/index.html`: `<label id="due-label">Hạn chót <input type="date" id="due"></label>` trong `#add` (D1); `#filters` và
  `<label id="sort-label">Xếp theo <select id="sort">` (Thứ tự thêm `added`, mặc định · Hạn chót `due`, D8) cùng nằm trong `<div id="view">`.
- `app/style.css`: form thêm và dòng việc xuống hàng được (màn hình hẹp); `#view`; chữ hạn nhỏ, xám; dòng quá hạn: chữ hạn `#a3261b`, nhãn
  "Quá hạn" chữ trắng trên `#a3261b` (tính tay: ~6,8:1 trên nền trang, 7,3:1 chữ trắng; AA là 4,5:1). `span:empty` ẩn.
- `tests/static.test.js`: **sửa test đang ghim hành vi cũ** "visible text in index.html has no technical words": thêm `dueDate` vào chữ
  cấm (AC10, như plan). Test mới: `<label>` "Hạn chót" chứa `type="date" id="due"`; `<label>` "Xếp theo" chứa `<select id="sort">` đúng hai
  lựa chọn, đúng chữ `DUE_TEXT`, `added` mặc định.
- `tests/app.test.js`: trang giả thêm `setAttribute`, `focus()`/`document.activeElement`, `#list` nhớ các dòng của lần vẽ cuối, `#undo`
  bắt đầu `hidden` như `index.html`, `Date` cố định 10/11/2026 06:00 `Asia/Ho_Chi_Minh` (09/11 theo UTC), `submit(title, date)`. Test cũ giữ
  nguyên. 16 test mới, theo từng dòng `tests/app.test.js` ở mục Proof của plan: thêm có/không hạn (AC1, AC2) · Quá hạn (AC3) · xếp và lần lưu
  giữ thứ tự thêm (AC4, Q6) · xếp + lọc (AC5) · đổi, bỏ, Hoàn tác, hết 10 giây (AC6, Q5) · Backspace giữa lúc gõ (Q3, điều kiện 1 của Khoa) ·
  đổi rồi bỏ trong cùng lần focus · đặt rồi xoá trên việc chưa có hạn · `"abc"` giữ nguyên · nút mất khi đổi hạn, còn khi xếp/rời ô · sửa
  đúng việc khi lọc + xếp · dữ liệu cũ và hỏng (AC7, AC8) · tiêu đề có HTML và `$&` (AC12) · lưu lỗi → D7 (AC13) · giữ focus khi vẽ lại và
  khi Tab rời ô ngày đã đổi (AC9).

Plan không bị sửa; commit đi qua mà pre-commit không chặn (như PR 6: hook có vẻ chưa cài trong worktree này). Mục Tiến độ cho bước 4–5b
do người ghi.

### Cho người review xem

1. **`render(focusTo)` nhận tham số**, khác plan một chút: plan nói "nhớ phần tử đang focus". Trong `blur`, `document.activeElement` vẫn
   là ô đang rời hoặc `body`, chưa phải ô sắp nhận focus, nên `blur` truyền `e.relatedTarget`. Mọi chỗ gọi khác dùng mặc định
   `document.activeElement`. Kéo theo: đánh dấu xong bằng ô đánh dấu nay giữ focus trên ô đó sau khi vẽ lại (trước đây rơi về `body`).
2. **Gọi `.focus()` trong lúc `blur`** rồi trình duyệt chuyển focus tới phần tử đã bị gỡ khỏi trang: test giả không chứng minh được
   trình duyệt thật làm gì. Cần T8 (chỉ bàn phím) trên cả ba trình duyệt.
3. **Rời cửa sổ / đổi tab khi ô ngày đã đổi** bắn `blur` với `relatedTarget = null` → vẽ lại, focus không được giữ khi quay lại.
   Ô đang gõ dở (`value === ''`) lúc đó cũng bị coi là bỏ hạn, có D5 + Hoàn tác (plan đã chấp nhận ở Thiết kế).
4. **Dòng đã xong vẫn hiện "Hạn …" gạch ngang** (`li.done span` có sẵn áp cho mọi `span` trong dòng). Plan/spec không nói; Linh xem.
5. **D2, D5 ghép bằng `replace('{title}', () => t.title)`** (hàm, không phải chuỗi), để tiêu đề có `$&` không bị đổi. Có test.
6. Focus sau khi bấm Hoàn tác vẫn rơi về `body` (PR 6, mục 4): plan chưa quyết, PR này không đổi.
7. `scripts/pr.py show 7` và `scripts/review.py 7` tính so với `main` (merge-base), nên gồm cả PR 5 và PR 6. Riêng PR này: 397 dòng.

## How it was checked

`bash scripts/check.sh` trên `efb7a18` (head của nhánh, sau thay đổi cuối):

```
== test: node --test
ℹ tests 80
ℹ pass 80
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

- Subagent `verifier` với plan này trên `efb7a18`: chạy `bash scripts/check.sh` (80/80, OK) và `git diff 2a40506 efb7a18`; khớp Thiết kế
  `app.js`/`index.html`, D1–D9 và mọi dòng Proof của `app.test.js`/`static.test.js`. Script tự viết để thử luồng lân cận bị từ chối,
  nên phần đó chỉ đọc code. Lệch plan (không chặn, **chưa sửa**, người review quyết):
  1. `data-id` gắn trên từng ô của dòng (ô đánh dấu, ô ngày, nút xoá) chứ không trên `li` (plan dòng 114). Giữ focus vẫn chạy như plan muốn.
  2. "Hôm nay" được tính trong `drawDue`, tức mỗi dòng và mỗi lần cập nhật tại chỗ, không phải một lần cho cả `render()` (plan dòng 115).
     Chỉ khác khi một lần vẽ vắt qua nửa đêm.
  3. Proof dòng 247: thêm/đánh dấu/xoá/nhập file làm nút mất mới được test với `offerUndo` gọi thẳng (PR 6), chưa thử với Hoàn tác thật
     của việc bỏ hạn chót. Đổi hạn, xếp, rời ô đã thử với Hoàn tác thật.
  4. Proof dòng 249 (dữ liệu cũ bốn trường): chỉ có một việc bốn trường trong test dữ liệu hỏng, cộng các test đếm cũ.
  5. Ngoài plan: dòng đã xong gạch ngang cả "Hạn …" (mục 4 ở trên); `blur` không có `focus` trước đó (`dataset.before` chưa có) thì
     được coi là việc đã có hạn, nên hiện D5 + Hoàn tác (`app/app.js:42`, trình duyệt thường bắn `focus` trước).
  6. Plan chưa ghi Tiến độ cho bước 4–5b (người ghi). Verifier không thử được: đánh dấu xong khi đang lọc "Chưa xong" (dòng mất, focus
     về `body`), xoá (focus về `body`), nhập file khi đang xếp theo hạn. Các luồng này nên có trong lần kiểm tay.
- Chưa chạy: `python3 scripts/review.py 7` (plan bước 7; nó so với `main`, sẽ review cả PR 5–6), kiểm tay T0–T10 (cần người và máy thật).

<!-- pr.py -->
## Size and risk (computed by scripts/pr.py)

397 lines in 5 files · risk **medium** → 1 code owner, who reads the plan
