# Plan: Hạn chót cho việc

Status: accepted · From: spec/2026-10-19-han-chot-cho-viec.md (accepted, commit `f0c7589`) · Size: **Large** (Khoa, Q1) ·
Date: 2026-11-04

Khoa (tech lead) duyệt **có điều kiện** (`demo/sdlc-5/tra-loi-gia-dinh.md`, Vòng hai; `demo/sdlc-5/runs/B6p-*`): (1) sửa Q3 và thêm test,
(2) Linh trả lời A16 (và Q3) trước PR A, (3) ghi C4 = (a) trước PR B. Bản này đã ghi cả ba và mọi câu trả lời khác. Chưa viết code trước
khi một người đổi chữ `draft` ở dòng 3 thành `accepted`.

**Chú dẫn mã:** `F<n>` = luồng trong mục User flows của spec · `A<n>` = câu trả lời giả định, `C<n>` = concern (mục Assumptions, Concerns
của spec) · `AC<n>` = tiêu chí nghiệm thu thứ n của spec · `P<n>`/`S<n>`/`U<n>` = luật trong `policy-privacy@1`, `policy-security@2`,
`policy-ux@2` · `Q<n>` = câu hỏi của plan này (mục Quyết định) · `D<n>` = câu chữ (mục Câu chữ) · `T<n>` = bước kiểm tay (mục Proof) ·
**PR A** = PR hạn chót, **PR B** = PR sao lưu `version: 2` (số PR do `scripts/pr.py new` cấp).

## Context
Người dùng đặt được ngày hạn chót cho một việc (khi thêm, và trên từng dòng), thấy "Hạn 25/10/2026" trên dòng, thấy "Quá hạn" với việc
chưa xong đã trễ, xếp danh sách theo hạn chót, bỏ hạn chót có Undo 10 giây; file sao lưu lên `version: 2` có `dueDate` không bắt buộc
(F1–F5). Spec chia làm hai PR: PR A (hạn chót) rồi PR B (sao lưu) [C2, Khoa].

Code hôm nay (đã đọc 2026-11-04, `main` @ `f0c7589`, `bash scripts/check.sh`: 46/46):
- `app/app.js` giữ `todos` trong một biến, mọi thay đổi đi qua `commit()` → `persist(store, todos)` → `render()`. `render()` vẽ lại cả
  `#list` bằng một mẫu `innerHTML` không có chữ người dùng, rồi gắn tiêu đề bằng `textContent`. Không có Undo nào, không có ô nào khác
  ngoài tiêu đề. `show()` ghi `#message` bằng `textContent`.
- `app/store.js` ghi cả mảng bằng `JSON.stringify`, không kiểm từng việc: trường mới được lưu và đọc lại mà không sửa `store.js`.
- `app/backup.js`: `pick` chỉ chép bốn trường, `toBackupText` ghi `version: 1`, `parseBackup` đòi `version === 1` và đúng bốn khoá
  (`hasExactKeys`). `formatCount`/`fill` dành cho số đếm, không dùng cho ngày (chú thích dòng 39).
- `policy-security` đã lên v2 (Khoa): S1 kiểm theo schema của `version` của file. Spec dòng 3 đã ghi `policy-security@2`.
- Thứ tự `<script>` `store.js` → `backup.js` → `app.js` được ghim bởi `tests/static.test.js`.

## Quyết định
Trả lời ở `demo/sdlc-5/tra-loi-gia-dinh.md`, mục "Vòng hai" (lượt `demo/sdlc-5/runs/B6p-*`, 2026-11-04). Không còn câu hỏi mở.

| Q | Câu hỏi | Quyết định | Ai |
|---|---|---|---|
| Q1 | Size | **Large** (như đề xuất): đổi dạng dữ liệu đã lưu, đổi cấu trúc file sao lưu, thêm một file script và đổi thứ tự script đang được ghim, hai PR, spec `Risk: high` | Khoa |
| Q2 | Logic ngày để ở đâu? | **File mới `app/due.js`** (như đề xuất), không DOM, như `backup.js`: kiểm ngày, ngày hôm nay theo giờ máy, quá hạn, định dạng, xếp. Thứ tự script mới `store.js` → `due.js` → `backup.js` → `app.js` (PR B cần `isValidDueDate` trong `backup.js`) | Khoa |
| Q3 | Ô ngày trên dòng việc: lưu lúc nào, vẽ lại lúc nào? | **Lưu ở `change`, vẽ lại ở `blur`, có sửa (điều kiện 1 của Khoa):** `change` **chỉ lưu khi giá trị hợp lệ**; giá trị `''` không làm gì ở `change` mà được xử lý lúc `blur`, so với giá trị lúc ô nhận focus. Lý do: khi gõ bằng bàn phím, Chrome bắn `change` sau mỗi phần ngày, và Backspace một phần làm giá trị thành `''`; đề xuất cũ sẽ xoá hạn chót đã lưu và hiện "Hoàn tác" giữa lúc gõ. Trong lúc ô còn focus, chỉ dòng đó được cập nhật tại chỗ (chữ "Hạn …", "Quá hạn"); danh sách xếp lại khi rời ô. Linh đồng ý về trải nghiệm (lưu ngay, vẽ lại khi rời ô). Chi tiết ở Thiết kế, test ở Proof | Khoa · Linh |
| Q4 | Bỏ hạn chót mà lưu lỗi (`failed`) hoặc đang đọc lỗi (`skipped`): có Undo không, câu nào? | **Có Hoàn tác cả ba trường hợp** (như đề xuất). `failed` → D7 thay cho D5, nút "Hoàn tác" vẫn hiện; `skipped` → D5 như thường, dải báo đọc lỗi đã có. U1 vẫn đạt vì câu lưu lỗi luôn hiện | Linh |
| Q5 | Bấm "Hoàn tác" xong có báo gì không? | **Có: D9 "Đã hoàn tác."** khi lưu được (khác đề xuất cũ "không báo"); lưu lỗi thì D7. Dùng chung với PR 2 (Q7). Linh hỏi trình đọc màn hình có tự đọc `#message` không: có, `#message` nằm trong `#notices` `role="status" aria-live="polite"` (`app/index.html:12`) | Linh |
| Q6 | "Thứ tự thêm" là thứ tự nào? | **Thứ tự trong mảng `todos`** (như đề xuất): `push` khi thêm, nhập file giữ thứ tự trong file; không xếp theo `createdAt`. Xếp theo hạn chót chỉ đổi thứ tự hiện, không đổi mảng đã lưu | Khoa |
| Q7 | PR 2 (`pr/2-doi-ten-viec`, đổi tên việc, có `offerUndo`) chưa merge và cũng sửa `render()` của `app.js` | **Một cơ chế Undo duy nhất. PR A đi trước và tự làm Undo; PR 2 chờ, rebase sau PR A và dùng lại Undo của PR A.** Khoa muốn PR 2 merge trước (nhỏ hơn), nhưng PR 2 còn đang chờ plan (Medium, `review/2/watch.md`), nên người chạy demo để PR 2 chờ. Để PR 2 rebase dễ, Undo của PR A dùng tên và dạng chung `offerUndo(message, restore)`, không gắn với hạn chót (xem Thiết kế) | Khoa · người chạy demo |

**Câu hỏi của spec** (A16–A19, C4), đã có trả lời:

| | Chặn | Trả lời | Ảnh hưởng tới plan |
|---|---|---|---|
| A16 (Linh): câu Undo, khi nào nút biến mất | PR A | D5 "Đã bỏ hạn chót của việc {tiêu đề}." · D6 "Hoàn tác" · nút mất sau 10 giây hoặc khi thêm, đánh dấu, xoá, đổi hạn chót, nhập file. Đổi lọc, đổi cách xếp, rời ô ngày **không** làm mất nút | Như mặc định cũ; D5, D6 hết "chưa trả lời" (điều kiện 2 của Khoa đã đạt) |
| A17 (Thảo, Khoa): hai PR ra cùng bản phát hành | Phát hành PR A | Có: PR A chỉ lên `dev`/`staging`; `production` chờ PR B | Không `prepare_release` cho `production` trước khi PR B merge |
| A18 (Khoa): luôn ghi `version: 2` | PR B | Có, luôn ghi `version: 2` | `toBackupText` không có nhánh theo nội dung |
| A19 (Mai): không cần duyệt lại cấu trúc file | PR B | Không cần duyệt lại | PR B không chờ Mai |
| C4 (Khoa, Linh): sao lưu danh sách có `dueDate` hỏng | PR B | **(a) `pick` chỉ chép `dueDate` hợp lệ** (điều kiện 3 của Khoa) | Việc có `dueDate` hỏng ra file sao lưu **không có khoá `dueDate`**, không báo (Linh: khách không thấy giá trị hỏng trên màn hình nên không mất gì, không cần câu mới). File app tự tạo luôn nhập lại được; AC16 giữ nguyên (file nhập có `dueDate` hỏng vẫn bị từ chối cả file) |

## Files that change
| File | PR | Thay đổi |
|---|---|---|
| `app/due.js` (mới, Q2) | A | Logic ngày, không DOM, không bộ nhớ trình duyệt; `DUE_TEXT` (câu chữ mới); `module.exports` có điều kiện như `backup.js` |
| `tests/due.test.js` (mới) | A | Test mọi hàm của `due.js`, chạy với `process.env.TZ = 'Asia/Ho_Chi_Minh'` |
| `app/app.js` | A | Chú thích dòng 1; `add(title, dueDate)`; `setDue`, `clearDue`; Undo chung `offerUndo` (Q7); ô ngày, chữ "Hạn …", "Quá hạn" trên dòng; ô "Xếp theo"; giữ focus khi vẽ lại |
| `app/index.html` | A | Ô ngày có nhãn "Hạn chót" trong form thêm; ô chọn "Xếp theo" cạnh bộ lọc; nút "Hoàn tác" (ẩn) trong `#notices`; `<script src="due.js">` giữa `store.js` và `backup.js` |
| `app/style.css` | A | Kiểu cho ô ngày, chữ hạn chót, dòng quá hạn (màu, đủ tương phản), nút Hoàn tác, ô Xếp theo |
| `tests/app.test.js` | A | Thêm test luồng (thêm có/không hạn, đổi, bỏ, Undo, xoá một phần ngày lúc gõ (Q3), xếp, lọc + xếp, lưu lỗi); `loadApp` nhận thêm `due.js`, `Date` cố định, `setTimeout` giả. Test cũ giữ nguyên |
| `tests/static.test.js` | A | **Sửa test đang ghim hành vi cũ:** thứ tự script thành `store, due, backup, app`; vòng "chỉ store chạm bộ nhớ" thêm `due.js`; chữ hiển thị cấm thêm `dueDate` (AC10); có nhãn "Hạn chót", "Xếp theo" |
| `app/backup.js` | B | Chú thích dòng 2; `pick` thêm `dueDate` khi hợp lệ (C4 = a); `toBackupText` ghi `version: 2`; `parseBackup` nhận `version` 1 và 2, mỗi bản một schema |
| `tests/backup.test.js` | B | **Sửa hai test đang ghim hành vi cũ** (dòng 37 "version 1, only the four todo fields", dòng 76 trường hợp `version: 2` bị từ chối → đổi thành `version: 3`); thêm test F5. Nạp `due.js` vào `globalThis` trước `backup.js` |
| `plan/2026-10-19-han-chot-cho-viec.md` | A, B | Người commit ghi Tiến độ (pre-commit đòi `plan/` đi cùng `app/`) |

`app/store.js` **không đổi** (spec mục Data). Không file nào khác gọi `store` hay bộ nhớ trình duyệt: grep `store\.(load|save|replace)|localStorage`
ngày 2026-11-04 cho `app/app.js:3` (`load`), `app/backup.js:116` (`save`), `app/backup.js:134` (`replace`), `app/store.js`, cùng các
test. Chạy lại ở bước A.1.

### Thiết kế
- **Dữ liệu** (spec mục Data, A15): mỗi việc có thể có `dueDate`, chuỗi `YYYY-MM-DD`. Không có hạn chót thì **không có khoá** (không
  `null`, không `''`). Khoá `todo.v1` giữ nguyên, không chuyển đổi dữ liệu cũ. Giá trị hỏng trong bộ nhớ được giữ nguyên (A14): không
  hàm nào trong PR A ghi đè `dueDate` trừ khi người dùng đổi ô ngày của chính việc đó.
- **`due.js`** (không chứa chữ "localStorage", kể cả trong chú thích):
  - `isValidDueDate(v)` → `true` khi `v` là chuỗi khớp `/^\d{4}-\d{2}-\d{2}$/` **và** là ngày có thật: dựng bằng `Date.UTC(y, m - 1, d)`
    rồi so lại năm, tháng, ngày bằng `getUTC*` (loại `2026-02-30`, `2026-13-01`; không phụ thuộc múi giờ).
  - `localDateString(date)` → `YYYY-MM-DD` từ `getFullYear` / `getMonth` / `getDate` (A9). Không bao giờ `toISOString()`.
  - `isOverdue(todo, today)` → `!todo.done && isValidDueDate(todo.dueDate) && todo.dueDate < today`. So chuỗi được vì dạng cố định 4-2-2
    (A6: đúng hôm nay không quá hạn; A7: đã xong không bao giờ quá hạn).
  - `formatDueDate(s)` → `Hạn DD/MM/YYYY` (A5), chỉ gọi với giá trị hợp lệ.
  - `sortByDue(todos)` → **mảng mới** (không đổi `todos`): ngày hợp lệ tăng dần, việc không có hoặc có `dueDate` hỏng xuống cuối; cùng
    ngày giữ thứ tự gốc (A12, `Array.prototype.sort` ổn định từ ES2019; không phụ thuộc vào đó: so thêm chỉ số gốc).
  - `DUE_TEXT`: D1–D6, D8, D9.
- **`app.js`**:
  - Biến mới `sort = 'added'` (A11: không lưu; tải lại trang là về `added`) và `undo = null` (`{ restore, timer }`, chỉ trong bộ nhớ
    trang, spec mục Data).
  - `visible()`: lọc như cũ, rồi `sort === 'due' ? sortByDue(…) : …` (F4 bước 4).
  - `add(title, dueDate)`: thêm khoá `dueDate` chỉ khi `isValidDueDate(dueDate)` (ô trống → `''` → không có khoá, AC2). Form: sau khi
    thêm, xoá cả `#title` và `#due` (F1 bước 4). Ngày đã qua được nhận (A4).
  - `setDue(id, value)` (gọi ở `change`, Q3): tìm việc theo `id` (như `toggle`). **Chỉ khi** `isValidDueDate(value)` và khác ngày đang có
    → gán, lưu, cập nhật dòng tại chỗ. `value === ''` (hay bất kỳ giá trị không hợp lệ nào) → **không làm gì**: không lưu, không D5, không
    nút Hoàn tác. Vì thế Backspace giữa lúc gõ không xoá hạn chót đã lưu.
  - Ô ngày nhớ giá trị lúc nhận focus: `focus` → `input.dataset.before = input.value` (`''` nếu việc không có hạn chót hoặc có `dueDate`
    hỏng).
  - `clearDue(id, before)` (gọi ở `blur` khi `input.value === ''`, Q3): tìm việc theo `id`. Việc không có `dueDate` hợp lệ → không làm gì
    (giữ nguyên giá trị hỏng, A14). Có `dueDate` hợp lệ:
    - `before !== ''` (lúc vào ô việc đã có hạn chót) → nhớ ngày đang lưu, `delete t.dueDate`, lưu, `offerUndo(D5 hoặc D7, restore)`
      (A16, Q4). `restore` gán lại **ngày đang lưu lúc bỏ** (nếu đã đổi sang ngày khác trong cùng lần focus rồi mới xoá, Hoàn tác trả về
      ngày mới đó).
    - `before === ''` (ngày được đặt trong chính lần focus này rồi xoá đi) → `delete t.dueDate`, lưu, không D5, không nút: người dùng không
      mất ngày nào đã có trước đó. Lưu lỗi vẫn hiện D7 (U1).
  - Lưu luôn qua `persist(store, todos)` như `commit()` (U1, AC13). Tách `commit()` thành `save()` (lưu + hiện câu) và `render()`, để
    `setDue` lưu ngay mà chưa vẽ lại (Q3).
  - Undo chung (Q7, PR 2 dùng lại khi rebase): `offerUndo(message, restore)` → `show(message)`, hiện `#undo`, hẹn giờ 10 giây gọi
    `clearUndo()`, `undo = { restore, timer }`. `show()` (mọi lần hiện câu mới) gọi `clearUndo()` trước: ẩn nút, `clearTimeout`,
    `undo = null`; `offerUndo` gắn `undo` **sau** `show()`. Vì thêm, đánh dấu, xoá, đổi hạn chót, nhập file đều gọi `show()`, nút tự mất
    đúng như A16; lọc, xếp, rời ô ngày (khi không bỏ hạn) không gọi `show()`. Bấm "Hoàn tác": `undo.restore()` (với hạn chót: tìm việc
    theo `id`, đã bị xoá thì không làm gì; còn thì gán lại ngày), lưu, `render()`, rồi `show(D9)` khi lưu được, `show(D7)` khi lưu lỗi
    (Q5, F2 bước 4). `show()` làm nút mất.
  - Dòng việc: mẫu `innerHTML` tĩnh (không có chữ người dùng) thêm `<input type="date">`, `<span class="due">`, `<span class="overdue-tag">`.
    `input.value = isValidDueDate(t.dueDate) ? t.dueDate : ''`; nhãn bằng `setAttribute('aria-label', 'Hạn chót của việc ' + t.title)`
    (thuộc tính, không phải HTML, S3); chữ hạn và "Quá hạn" bằng `textContent` (S3, AC12). `li` có class `overdue` khi `isOverdue`.
    `li.dataset.id = t.id` để giữ focus.
  - `render()` tính `today = localDateString(new Date())` mỗi lần (F3 bước 5). Trước khi xoá `#list`, nhớ phần tử đang focus trong danh
    sách (`id` của việc + phần nào: ô đánh dấu, ô ngày, nút xoá) và focus lại sau khi vẽ. Cần cho AC9: Tab từ ô ngày sang nút xoá làm ô
    mất focus → vẽ lại (Q3) → không có bước này thì focus rơi về `body`.
  - Ô ngày trên dòng: `focus` → nhớ `before`; `change` → `setDue` (chỉ giá trị hợp lệ; lưu ngay, cập nhật chữ "Hạn …" và class quá hạn
    của **dòng đó** tại chỗ); `blur` → nếu `input.value === ''` thì `clearDue(id, before)`, rồi `render()` nếu đã có thay đổi kể từ lần
    vẽ trước (Q3). `blur` không bỏ hạn thì không gọi `show()`, nên không làm mất nút Hoàn tác.
  - Ô ngày gõ dở (ví dụ còn ngày và tháng, năm trống) có `value === ''`: rời ô lúc đó được coi là bỏ hạn chót, có D5 và Hoàn tác 10 giây.
    Chấp nhận được vì có Undo; T4 kiểm.
  - `#sort` `change` → `sort = value`, `render()`.
- **`index.html`**: trong `#add`, `<label>` "Hạn chót" bọc `<input type="date" id="due">` (A1); `<label>` "Xếp theo" bọc
  `<select id="sort">` với hai `<option>` "Thứ tự thêm" (`added`, mặc định), "Hạn chót" (`due`) cạnh `#filters` (A10); trong `#notices`,
  `<button type="button" id="undo" hidden>Hoàn tác</button>` sau `#message`. Không `<script>`/`<link>` ra ngoài (S4).
- **`backup.js`** (PR B; A18: luôn `version: 2`; C4 = (a)):
  - `BACKUP_VERSION = 2`; schema theo `version` của file (S1 v2): v1 đúng bốn khoá; v2 bốn khoá, có thể thêm `dueDate`, và nếu có thì
    `isValidDueDate` phải đúng (`null`, `"abc"`, `"2026-02-30"` → M10 hiện nay, từ chối cả file, AC16). `version` khác 1 và 2 → M9.
  - `pick(t)`: bốn trường, cộng `dueDate` **chỉ khi `isValidDueDate(t.dueDate)`** (C4 = (a)). `dueDate` hỏng trong bộ nhớ không ra
    file, không báo; bộ nhớ trình duyệt vẫn giữ nguyên giá trị đó (A14). Nhờ vậy file app tạo ra luôn qua được `parseBackup`.
  - `toBackupText`: `{ version: 2, todos }`, thụt lề như cũ (P3, A18).
  - `backup.js` dùng `isValidDueDate` như biến toàn cục (như `app.js` dùng `store`); `due.js` nạp trước nó. Trong test: `Object.assign(globalThis,
    require('../app/due.js'))` trước `require('../app/backup.js')`.

### Câu chữ
Cột "Nguồn": nguyên văn từ đâu. Mọi câu đã có người chọn. Không câu nào chứa "localStorage", "JSON", "console", "dueDate" (U4, AC10).

| D | Câu / nhãn | Nguồn |
|---|---|---|
| D1 | Hạn chót (nhãn ô ngày ở form thêm) | Spec F1 bước 1 [A1, Linh] |
| D2 | Hạn chót của việc {tiêu đề} (nhãn ô ngày trên dòng) | Spec F2 bước 1 [A2, Thảo · Linh] |
| D3 | Hạn {DD/MM/YYYY} | Spec F3 bước 1 [A5, Linh] |
| D4 | Quá hạn | Spec F3 bước 3 [A8, Linh] |
| D5 | Đã bỏ hạn chót của việc {tiêu đề}. | Spec A16 [Linh, Vòng hai] |
| D6 | Hoàn tác (nút) | Spec A16 [Linh, Vòng hai] |
| D7 | Thay đổi vừa rồi chưa được lưu. Hãy sao lưu ra file, rồi xoá bớt việc đã xong. | `MESSAGES.notSaved` hiện có, spec F1 bước 6 [C3] |
| D8 | Xếp theo · Thứ tự thêm · Hạn chót (ô chọn) | Spec F4 bước 1 [A10, Linh] |
| D9 | Đã hoàn tác. (sau khi bấm Hoàn tác và lưu được) | Plan Q5 [Linh, Vòng hai]; câu gốc từ `review/2/watch.md` #6. Dùng chung cho mọi Undo, kể cả PR 2 (Q7) |

D7 dùng lại `MESSAGES.notSaved`, không chép. D5 chứa tiêu đề người dùng: ghép chuỗi rồi gán bằng `textContent` (S3, AC12).

## Order of work
Agent viết code trên nhánh `pr/<n>-<slug>` (`python3 scripts/pr.py new <slug>`) và chạy test; **người** review và commit, ghi Tiến độ
vào plan này trong cùng commit (pre-commit; agent không sửa plan đã duyệt). Merge vào `main` là việc của người.

**PR A: hạn chót** (sau khi plan được duyệt; A16, Q3–Q5 đã có trả lời):
1. Grep lại nơi gọi `store` / bộ nhớ trình duyệt và `render(`; khác kết quả 2026-11-04 thì dừng và báo. PR 2 đã merge vào `main` (trái
   với Q7) cũng dừng và báo: khi đó Undo phải lấy của PR 2, plan cần sửa.
2. Subagent `test-writer` viết test nghiệm thu từ spec, plan này (Q3, Q5) và danh sách tên công khai (`isValidDueDate`, `localDateString`,
   `isOverdue`, `formatDueDate`, `sortByDue`, `DUE_TEXT`, các id `#due`, `#sort`, `#undo`), **trước** khi có code. Chạy, thấy fail vì
   chưa có hàm.
3. `app/due.js` + `tests/due.test.js`. Xong khi: `due.test.js` xanh. Chưa file nào nạp `due.js`, app chạy y như cũ.
4. `app/index.html` + `tests/static.test.js` (thứ tự script mới, nhãn, AC10) + `app/style.css`.
5. `app/app.js` + phần mới của `tests/app.test.js`. Bước 4 và 5 đi cùng một commit: `index.html` có ô mới mà `app.js` chưa nối thì form
   thêm vẫn chạy nhưng ô ngày vô tác dụng.
6. `bash scripts/check.sh` OK; subagent `verifier` với plan này; T0 trước, rồi T1–T10.
7. `python3 scripts/review.py <n>`, sửa các mục Important trên nhánh PR, dừng. Một người khác người viết code review diff.

**PR B: sao lưu `version: 2`** (sau khi PR A merge; A18, A19, C4 đã có trả lời):
1. Sửa hai test cũ trong `tests/backup.test.js` (liệt kê ở Files that change) và thêm test F5, chạy, thấy fail đúng chỗ.
2. `app/backup.js`.
3. `bash scripts/check.sh` OK; `verifier`; T11–T13; review như PR A bước 7.

Phát hành: theo A17, chỉ `prepare_release` cho `production` khi cả hai PR đã merge. `dev`, `staging` deploy được sau từng PR.

PR 2 (đổi tên việc) chờ PR A merge, rồi rebase và dùng `offerUndo` cùng D9 của PR A (Q7). Việc đó thuộc plan của PR 2, không thuộc plan này.

## Risks
- **Bước rủi ro nhất: PR A bước 5 (`app.js`).** Ba cách hỏng:
  - *Mất hạn chót hoặc sửa nhầm việc*: ô ngày gửi `''` khi người dùng đang gõ lại một phần ngày (Q3: `change` bỏ qua `''`, chỉ `blur`
    mới bỏ hạn), hoặc `setDue`/`clearDue` tìm theo vị trí thay vì `id` khi đang lọc/xếp (lỗi PR 2 từng có: `review/2/watch.md` watch-0
    #1). Biết bằng: test "Backspace giữa lúc gõ" ở `app.test.js`; test sửa đúng việc khi đang lọc "Chưa xong" và xếp theo hạn chót; T3,
    T4 (gõ bằng bàn phím).
  - *Mất focus khi dùng bàn phím* (AC9, U5): vẽ lại dựng lại ô đang focus. Biết bằng: test focus trong `app.test.js` (`document.activeElement`
    giả) và T8.
  - *Xếp làm đổi thứ tự đã lưu*: `sortByDue` sắp xếp tại chỗ thì lần lưu sau ghi mảng đã xếp, "Thứ tự thêm" mất vĩnh viễn. Biết bằng: test
    `sortByDue` không đổi mảng vào; test luồng xếp theo hạn → đánh dấu → `saved.at(-1)` giữ thứ tự thêm.
- **Lệch ngày theo múi giờ** (A9): `toISOString()`, `new Date('2026-11-10')` (chuỗi ngày được đọc là UTC) hay `Date.parse` đều có thể lệch
  một ngày ở UTC+7. Plan không dựng `Date` từ `dueDate` ngoài `isValidDueDate` (dùng `Date.UTC` + `getUTC*`); "hôm nay" chỉ từ
  `localDateString`. Biết bằng: `due.test.js` với `TZ=Asia/Ho_Chi_Minh` lúc 06:00 ngày 10/11 (23:00 ngày 09/11 UTC) và lúc 00:30; static
  test cấm `toISOString` trong `due.js`, `app.js`.
- **Thứ tự script**: thiếu `due.js` hoặc đặt sau `app.js`/`backup.js` thì app trắng khi khởi động. `static.test.js` kiểm.
- **Dữ liệu cũ và dữ liệu hỏng** (A14, A15, AC7, AC8): việc không có `dueDate`, hay có `"abc"`, `"2026-02-30"`, `null`, số, phải hiện và
  xếp như không có hạn chót, không ném lỗi, không bị ghi lại thành giá trị khác. Biết bằng: test luồng nạp mảng như vậy, đánh dấu một việc
  khác, kiểm `saved.at(-1)` còn nguyên giá trị hỏng; T0.
- **Khoảng giữa PR A và PR B** (A17): trên `main` sau PR A, sao lưu bỏ mất hạn chót không báo (`pick`). Không phát hành `production` ở giữa.
  Test vòng sao lưu → nhập của PR A chỉ dùng việc không có hạn chót; PR B thêm vòng có hạn chót.
- **File sao lưu của chính app không nhập lại được** (C4, PR B): C4 = (a), `pick` bỏ `dueDate` hỏng nên file luôn hợp lệ. Giá: giá trị
  hỏng mất khỏi file sao lưu mà không báo (Linh, Khoa chấp nhận). Biết bằng: test vòng `parseBackup(toBackupText(x))` cho mọi danh sách app
  tạo được, kể cả việc có `dueDate` hỏng (ra lại không có khoá `dueDate`).
- **Rollback PR B làm file `version: 2` không nhập được** (xem Rollback).
- **Ô `<input type="date">` khác nhau giữa trình duyệt**: Safari iOS mở bánh xe chọn ngày, Chrome/Firefox desktop có ô gõ theo phần, cách
  hiện ngày trong ô theo ngôn ngữ trình duyệt (có thể là `11/12/2026` kiểu Mỹ). Chữ "Hạn DD/MM/YYYY" cạnh ô là cách hiện chuẩn (A5). Kiểm
  tay cả ba trình duyệt như plan sao lưu (Q6 của plan đó); điện thoại cần địa chỉ HTTPS (`crypto.randomUUID`).
- **Xung đột với PR 2** (Q7): cả hai sửa `render()` và vùng thông báo. PR A đi trước với một `offerUndo` chung; PR 2 rebase sau và bỏ
  cơ chế Undo riêng của nó. Nếu PR 2 bị merge trước, PR A bước 1 dừng.
- **Quyết định nhỏ plan tự chọn** (người review xem): đổi ô ngày sang đúng ngày đang có thì không lưu; bỏ hạn chót của việc vốn có `dueDate`
  hỏng (ô hiện trống, `clearDue` không làm gì) là không làm được trên giao diện, giá trị hỏng chỉ mất khi người dùng đặt ngày mới; trong
  cùng một lần focus, đặt ngày cho việc chưa có hạn rồi xoá đi thì bỏ hạn không kèm D5/Hoàn tác (Q3); Hoàn tác trả về ngày đang lưu lúc
  bỏ, không phải ngày lúc vào ô.

## Rollback
- **Không chuyển đổi dữ liệu:** khoá `todo.v1`, mảng việc giữ nguyên; chỉ có thể thêm khoá `dueDate` vào từng việc.
- **Revert PR A** an toàn cho dữ liệu: bản cũ đọc mảng có `dueDate` bình thường (không đọc trường này), và vẫn ghi lại nguyên các đối tượng
  việc nên `dueDate` không mất khi đánh dấu hay xoá việc khác. Người dùng chỉ không thấy hạn chót nữa; bật lại PR A thì thấy lại. Việc
  thêm mới khi đã revert không có hạn chót.
- **Revert PR B** có giá: file `version: 2` người dùng đã tải về sẽ bị bản cũ từ chối (M9) cho tới khi PR B quay lại. Trên môi trường
  hỏng, dùng `python3 scripts/rollback.py <env>` theo CLAUDE.md, rồi sửa tiếp thay vì để lâu ở bản không nhập được `version: 2`.
- Revert theo thứ tự B rồi A. Revert A mà giữ B: sao lưu vẫn chép `dueDate` có sẵn, không vỡ, nhưng thứ tự script trong `index.html` phải
  còn `due.js` (B cần `isValidDueDate`), nên không revert A riêng.

## Proof
Chạy: `bash scripts/check.sh` (kết thúc bằng `ℹ fail 0` và `== check: OK`, dán dòng cuối thật) · subagent `verifier` · bảng kiểm tay.

### Test tự động
| Test | Chứng minh | AC / mục |
|---|---|---|
| **`tests/due.test.js`** (PR A, bước 3; `TZ=Asia/Ho_Chi_Minh`) | | |
| `isValidDueDate`: nhận `2026-11-12`, `2028-02-29`; từ chối `abc`, `2026-02-30`, `2027-02-29`, `2026-13-01`, `2026-1-5`, `''`, `null`, số, `" 2026-11-12"` | Dạng và ngày có thật | AC8, AC16, A14 |
| `localDateString(new Date('2026-11-09T23:00:00Z'))` = `2026-11-10`; `new Date(2026, 10, 10, 0, 30)` → `2026-11-10` | Ngày theo giờ máy, không UTC | AC3, A9 |
| `isOverdue` với today `2026-11-10`: chưa xong 09/11 → `true`; 10/11, 11/11 → `false`; đã xong 09/11 → `false`; không có, `"abc"` → `false`; 01/11 → `true` | Quá hạn | AC3, A4, A6, A7 |
| `formatDueDate('2026-11-12')` = `Hạn 12/11/2026` | Dạng hiện | AC1, A5 |
| `sortByDue` A (không), B 15/11, C 12/11, D 12/11 → C, D, B, A; hai việc hỏng nằm cuối theo thứ tự gốc; mảng vào không đổi | Xếp | AC4, AC8, A12, Q6 |
| `DUE_TEXT` đúng D1–D6, D8, D9 nguyên văn; không giá trị nào chứa "localStorage", "JSON", "console", "dueDate" | Câu chữ | AC10, U4 |
| **`tests/app.test.js`** (PR A, bước 5; `Date` cố định 10/11/2026 06:00 UTC+7, `setTimeout` giả) | | |
| Thêm "Nộp báo cáo" với 12/11/2026 → việc lưu có `dueDate: '2026-11-12'`, dòng có "Hạn 12/11/2026", `#due` trống lại | F1 | AC1 |
| Thêm không chọn ngày → việc lưu không có khoá `dueDate` | Không có hạn chót | AC2 |
| Dòng việc chưa xong hạn 09/11 có "Quá hạn" và class `overdue`; 10/11, 11/11 không; đánh dấu xong → mất "Quá hạn" | F3 | AC3 |
| Thêm A, B, C, D (AC4), chọn "Hạn chót" → C, D, B, A; "Thứ tự thêm" → A, B, C, D; lần lưu sau khi xếp vẫn A, B, C, D | F4, Q6 | AC4 |
| Xếp theo hạn + lọc "Chưa xong" → chỉ việc chưa xong, vẫn xếp theo hạn | F4 bước 4 | AC5 |
| Đổi hạn B sang 11/11 (`change`) → lưu ngay, không có nút Hoàn tác; focus, xoá trống, `blur` → lưu không có `dueDate`, D5, nút hiện; bấm → lưu lại `2026-11-11`, `#message` = D9, nút ẩn; xoá trống lại, chạy hẹn giờ 10 giây → nút ẩn | F2, A16, Q5 | AC6 |
| **Backspace giữa lúc gõ (Q3, điều kiện 1 của Khoa):** việc hạn 12/11; focus ô, `change` với `''` → không lần lưu nào mới, việc vẫn `2026-11-12`, `#message` trống, nút ẩn; `change` với `2026-11-15` → lưu `2026-11-15`; `blur` → không D5, không nút | Xoá một phần ngày không mất hạn đã lưu | AC6, Q3 |
| Việc hạn 12/11; focus, `change` `2026-11-15` (lưu), `change` `''`, `blur` với `''` → lưu không có `dueDate`, D5, nút hiện; bấm → `2026-11-15`, D9 | Bỏ hạn chỉ ở `blur`; Hoàn tác trả ngày đang lưu | Q3, A16 |
| Việc chưa có hạn; focus, `change` `2026-11-13` (lưu), `change` `''`, `blur` với `''` → lưu không có `dueDate`, không D5, không nút | Ngày đặt rồi xoá trong cùng lần focus | Q3 |
| Việc `dueDate: "abc"`; focus, `blur` với `''` → không lần lưu nào, giá trị `"abc"` còn nguyên | Không bỏ giá trị hỏng | A14, Q3 |
| Nút Hoàn tác mất khi thêm, đánh dấu, xoá, đổi hạn khác, nhập file; còn khi đổi lọc, đổi xếp, rời ô ngày (không bỏ hạn) | A16 | AC6 |
| Đang lọc "Chưa xong" và xếp theo hạn, đổi hạn của việc thứ 2 trên màn hình → đúng việc đó đổi | Sửa đúng việc | Risks |
| Nạp mảng dạng cũ (bốn trường) → đủ việc, không có hạn chót, không ném lỗi | Dữ liệu cũ | AC7 |
| Nạp việc `dueDate: "abc"` và `"2026-02-30"` → không có chữ hạn, nằm cuối khi xếp; đánh dấu việc khác → lần lưu còn nguyên hai giá trị | Giữ giá trị hỏng | AC8, A14 |
| Tiêu đề `<img src=x onerror=alert(1)>` hạn 09/11 → tiêu đề, "Quá hạn" qua `textContent`; nhãn ô ngày qua `setAttribute`; D5 khi bỏ hạn đúng nguyên tiêu đề | Không chạy nội dung | AC12, S3 |
| `store.save` trả `'failed'`: thêm có hạn, đổi hạn, bỏ hạn (nút Hoàn tác vẫn hiện), Hoàn tác → mỗi lần `#message` = D7, không bao giờ D9 | Lưu lỗi được báo | AC13, U1, Q4, Q5 |
| Focus ở ô ngày của một việc, `render()` → focus ở ô ngày của đúng việc đó trên danh sách mới | Giữ focus | AC9, Q3 |
| **`tests/static.test.js`** (PR A, bước 4; sửa test thứ tự script) | | |
| `index.html`: `store.js` < `due.js` < `backup.js` < `app.js`; không `src`/`href` ra ngoài | Thứ tự script, S4 | AC11, Q2 |
| `app.js`, `backup.js`, `due.js` không chứa `localStorage`; `app.js`, `due.js` không chứa `toISOString` | Chỉ store chạm bộ nhớ; không UTC | A9 |
| `index.html` có `<label>` "Hạn chót" chứa `type="date"`, `<label>` "Xếp theo" chứa `<select id="sort">` với hai lựa chọn, `#undo` là `<button>`; chữ hiển thị không chứa `dueDate` | Nhãn, U4, U5 | AC9, AC10 |
| **`tests/backup.test.js`** (PR B) | | |
| `toBackupText`: `"version": 2`, việc có hạn có `dueDate`, việc không có thì không có khoá (sửa test dòng 37) | File sao lưu | AC14, A18 |
| `toBackupText` với việc `dueDate` `"abc"`, `"2026-02-30"`, `null` → việc đó ra file **không có khoá `dueDate`**, ba trường còn lại đủ; đối tượng việc trong bộ nhớ không đổi | `pick` chỉ chép ngày hợp lệ | C4 = (a), A14 |
| `parseBackup` nhận file v2 có và không có `dueDate`; nhận file v1 bốn trường, các việc không có hạn | Nhập v2, v1 | AC14, AC15 |
| Từ chối, danh sách giữ nguyên: v1 có `dueDate` hợp lệ; v2 `dueDate` `"abc"`, `"2026-02-30"`, `null`; v2 có `"x": 1` → M10; `version: 3` → M9 (sửa test dòng 76) | Kiểm file theo version | AC16, S1 |
| Vòng `parseBackup(toBackupText(x))`: nhận, bằng `x` với việc có hạn và không hạn; việc có `dueDate` hỏng ra lại không có khoá `dueDate` | File tải về nhập lại được | C4 = (a), Risks |
| `importBackup` file v2 hợp lệ → `replace` một lần với việc giữ `dueDate` | Nhập có hạn chót | AC14 |

### Kiểm tay
Như plan sao lưu: ô ghi `đạt` / `không` + ghi chú, người chạy, ngày, trình duyệt; dòng ★ bắt buộc Safari iOS máy thật, Chrome Android và một
trình duyệt desktop (địa chỉ HTTPS cho điện thoại), dòng khác bắt buộc desktop. Các bước dùng ngày máy 10/11/2026 thì đổi ngày hệ thống,
hoặc tính lại theo ngày chạy thật và ghi vào ghi chú.

| T | Việc làm | AC | Desktop | Safari iOS | Chrome Android |
|---|---|---|---|---|---|
| T0 ★ | **Trước mọi bước khác.** Trên bản hiện tại tạo 3 việc (1 đã xong), và một hồ sơ khác nạp 2.000 việc dạng cũ (lệnh console ở T0 của plan sao lưu). Mở bản mới: đủ việc, đúng trạng thái, không hạn chót, không lỗi console; thêm, đánh dấu, xoá; tải lại vẫn giữ | AC7 | chưa thử | chưa thử | chưa thử |
| T1 ★ | Thêm việc có hạn và không hạn; tải lại; ô ngày ở form trống lại | AC1, AC2 | chưa thử | chưa thử | chưa thử |
| T2 ★ | Quá hạn: hạn hôm qua, hôm nay, ngày mai; đánh dấu xong; thêm việc hạn đã qua | AC3 | chưa thử | chưa thử | chưa thử |
| T3 ★ | Đổi hạn trên dòng bằng bộ chọn ngày của trình duyệt; xoá trống; Hoàn tác trong 10 giây (thấy "Đã hoàn tác."); chờ quá 10 giây; tải lại mỗi bước | AC6, Q5 | chưa thử | chưa thử | chưa thử |
| T4 | **Gõ bằng bàn phím** vào ô ngày trên dòng: sửa riêng phần ngày (ví dụ 12 → 15), xoá một phần rồi gõ lại: ngày cuối đúng, không mất tháng/năm, không xếp lại giữa lúc gõ. **Backspace một phần ngày giữa lúc gõ: không hiện D5, không hiện nút Hoàn tác; mở tab thứ hai (tải lại) thấy hạn đã lưu vẫn còn** (Q3, điều kiện 1 của Khoa). Rời ô khi ngày còn gõ dở: D5 + Hoàn tác, bấm Hoàn tác lấy lại ngày | AC6, Q3, Risks | chưa thử | – | – |
| T5 ★ | Xếp theo hạn (AC4), lọc "Chưa xong"; tải lại về "Thứ tự thêm" | AC4, AC5 | chưa thử | chưa thử | chưa thử |
| T6 | `todo.v1` có `dueDate` `"abc"` và `"2026-02-30"`: app mở, hai việc không hạn, nằm cuối khi xếp; sau vài thao tác, hai giá trị còn nguyên | AC8 | chưa thử | chưa thử | chưa thử |
| T7 | Tắt mạng, lặp T1–T3, T5: tab Network không có request | AC11 | chưa thử | chưa thử | chưa thử |
| T8 | Chỉ bàn phím: đặt hạn khi thêm, đổi và bỏ hạn, Tab sang nút xoá (focus không rơi về đầu trang), bấm Hoàn tác, đổi cách xếp. VoiceOver/TalkBack đọc "Hạn chót", "Hạn chót của việc …", "Xếp theo", "Hoàn tác", "Quá hạn", và tự đọc "Đã hoàn tác." sau khi bấm Hoàn tác (Q5) | AC9 | chưa thử | chưa thử | chưa thử |
| T9 | Tiêu đề `<img src=x onerror=alert(1)>` hạn hôm qua, rồi bỏ hạn: không alert, chữ đúng | AC12 | chưa thử | chưa thử | chưa thử |
| T10 | Làm đầy bộ nhớ (như T8 của plan sao lưu): thêm có hạn, đổi hạn, bỏ hạn → mỗi lần D7 | AC13 | chưa thử | chưa thử | chưa thử |
| T11 ★ | (PR B) Sao lưu X có hạn, Y không; mở file xem `version: 2`, `dueDate`; xoá dữ liệu trang, nhập lại, tải lại. Lặp lại với thêm một việc `dueDate` `"abc"` (như T6): file không có `dueDate` cho việc đó và nhập lại được (C4 = a) | AC14, C4 | chưa thử | chưa thử | chưa thử |
| T12 | (PR B) Nhập một file `version: 1` tạo trước thay đổi (ví dụ file của T1 plan sao lưu) | AC15 | chưa thử | chưa thử | chưa thử |
| T13 | (PR B) Năm file của AC16: từng file bị từ chối, đúng câu, danh sách không đổi | AC16 | chưa thử | chưa thử | chưa thử |

AC10 (không có chữ kỹ thuật) do `due.test.js` và `static.test.js` kiểm, không cần kiểm tay.

## Tiến độ
Người commit điền (sau khi plan được duyệt, hook không cho agent sửa plan này).

- PR A: chưa bắt đầu.
- PR B: chưa bắt đầu.
