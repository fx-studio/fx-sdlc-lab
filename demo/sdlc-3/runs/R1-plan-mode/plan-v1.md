# Plan: Sao lưu ra file, nhập lại, và báo khi không lưu được

From: spec/2026-10-19-khach-khong-mat-viec.md (accepted) · Size: **Medium** (xem câu hỏi Q1) · Status: draft · Date: 2026-10-27

Sau khi được duyệt, nội dung này được ghi vào `plan/2026-10-19-khach-khong-mat-viec.md` với `Status: draft`; một người đổi sang
`accepted` và commit. Chưa viết code trước khi plan được accept.

## Context
Khách mất hết việc khi đổi máy hoặc xoá dữ liệu trình duyệt, vì app chỉ giữ việc trong `localStorage` (`app/store.js`). Spec đã chốt:
sao lưu ra file JSON, nhập lại (thay toàn bộ, có xác nhận), báo khi ghi lỗi (F3), và khi dữ liệu đã lưu không đọc được thì báo và
**không ghi đè** (F5). Hiện `store.save` nuốt lỗi, `store.load` trả `[]` cho cả "chưa có" lẫn "hỏng" và lần lưu sau ghi đè dữ liệu hỏng.
`tests/` đang trống: plan này tạo bộ test đầu tiên.

## Files that change
| File | Thay đổi |
|---|---|
| `app/store.js` | `load()` phân biệt chưa có / đọc lỗi (3 trường hợp F5 bước 3); `save()` trả kết quả thay vì nuốt lỗi; khoá ghi khi đọc lỗi; `replace()` cho đường nhập file. Thêm `module.exports` có điều kiện để Node test được |
| `app/backup.js` (**mới**, xem Q2) | Logic thuần, không DOM: tạo nội dung file, tên file, kiểm file nhập, lời xác nhận, mọi câu chữ mới (một object `MESSAGES`) |
| `app/app.js` | Nối UI: nút sao lưu, nhập từ file, hộp xác nhận, vùng thông báo, dải báo F5, dòng trạng thái trống; `commit()` dùng kết quả của `store.save` |
| `app/index.html` | Nút "Sao lưu ra file", `<input type="file">` có nhãn "Nhập từ file", vùng `role="status" aria-live`, dải báo F5, dòng trống, dòng chữ F4, `<dialog>` xác nhận, `<script src="backup.js">` |
| `app/style.css` | Kiểu cho dải báo, vùng thông báo, dialog, dòng trống |
| `tests/store.test.js` · `tests/backup.test.js` · `tests/static.test.js` (mới) | `node --test`, không package; `localStorage` giả bằng một object có `getItem/setItem` (ném lỗi được khi cần) |

### Thiết kế chính
- **`store`** (giữ khoá `todo.v1`, không thêm khoá/trường):
  - `load()` → `{ todos, readError }`. Không có khoá → `{ todos: [], readError: false }`. Không parse được / parse ra không phải mảng /
    `getItem` ném lỗi → `{ todos: [], readError: true }` và ghi nhớ `store.readError = true` (chỉ trong bộ nhớ trang, A12).
  - `save(todos)` → `'saved' | 'failed' | 'skipped'`. Khi `readError` thì **không gọi `setItem`**, trả `'skipped'` (F5 bước 5, A14).
  - `replace(todos)` → `'saved' | 'failed'`: đường duy nhất được ghi khi đọc lỗi (F5 bước 6, A15); chỉ xoá `readError` khi ghi thành
    công (A17).
  - Đặt luật "không ghi khi đọc lỗi" ở tầng store để test được bằng Node và không phụ thuộc app.js nhớ kiểm.
- **`backup.js`**:
  - `toBackupText(todos)` → `JSON.stringify({ version: 1, todos: [{id,title,done,createdAt}] }, null, 2)` (chỉ chép 4 trường, P2/P3).
  - `backupFileName(date)` → `todo-sao-luu-YYYY-MM-DD.json` theo **giờ máy** (ngày hôm đó của khách).
  - `MAX_IMPORT_BYTES` (Q3); `tooBigToImport(text)` đo bằng `TextEncoder` (F1 bước 5).
  - `parseBackup(text)` → `{ ok: true, todos }` hoặc `{ ok: false, message }`. Từ chối: không parse được (ảnh, văn bản bất kỳ), không
    phải object, khoá gốc khác đúng `version`+`todos`, `version !== 1`, `todos` không phải mảng, việc có khoá khác đúng 4 khoá, `id`
    không phải chuỗi hoặc rỗng, `title` không phải chuỗi hoặc rỗng sau `trim`, `done` không phải boolean,
    `createdAt` không phải số hữu hạn, trùng `id`, `todos` rỗng (Q4). Chỉ `JSON.parse`, không bao giờ eval (S1).
  - `confirmText({ readError, current, incoming })` → `null` khi không cần hỏi (không đọc lỗi và `current === 0`), ngược lại đúng một
    trong ba mẫu: "Thay {n} việc hiện có bằng {m} việc trong file?", "Thay danh sách đã lưu không đọc được bằng {m} việc trong file?",
    "Thay danh sách đã lưu không đọc được và {n} việc bạn vừa thêm (chưa lưu) bằng {m} việc trong file?".
  - `MESSAGES`: mọi câu mới, nguyên văn từ spec ở chỗ spec có nguyên văn (F1.5, F3 gợi ý A8, F5 bước 4).
- **`app.js`**:
  - Khởi động: `const { todos, readError } = store.load()`; `readError` → hiện dải báo F5, ẩn dòng trống (A18).
  - `commit()`: `store.save` → `'failed'` thì hiện thông báo F3 (việc vẫn trên màn hình, A9); `'skipped'` thì không thêm gì (dải báo
    đã hiện, không bật hộp thoại, A14); `'saved'` thì xoá thông báo lỗi F3 cũ nếu có.
  - Sao lưu: rỗng → "Chưa có việc nào để sao lưu", không tải; ngược lại `Blob` + `URL.createObjectURL` + `<a download>` (không request
    mạng), báo "Đã sao lưu N việc."; nếu `tooBigToImport` thì hiện đúng câu C2 thay cho câu đếm.
  - Nhập: kiểm `file.size > MAX_IMPORT_BYTES` **trước khi đọc** → từ chối; hiện "Đang đọc file…" (U3); `await file.text()` →
    `parseBackup` → lỗi thì báo, không đụng danh sách; `confirmText` → nếu khác `null` mở `<dialog>` (`showModal`, Esc = huỷ,
    `aria-labelledby` trỏ vào câu hỏi); huỷ → không gì thay đổi; đồng ý / không cần hỏi → `store.replace(incoming)`: `'saved'` → thay
    `todos`, ẩn dải báo F5, báo "Đã nhập N việc."; `'failed'` → giữ danh sách cũ trên màn hình, giữ dải báo nếu đang đọc lỗi, hiện
    thêm thông báo F3 (F2 bước 8, A20). Reset `input.value` để chọn lại cùng file được.
  - Tiêu đề vẫn qua `textContent` như `render` hiện có (S3); không đổi thêm/đánh dấu/xoá.

## Order of work
1. **store.js** + `tests/store.test.js`. Chưa đụng app.js; app vẫn chạy vì gọi cũ `store.load()` được sửa ngay ở bước 4 — để app
   không vỡ giữa chừng, bước 1 và bước 4 vào cùng một commit (xem Risks).
2. **backup.js** + `tests/backup.test.js`.
3. **index.html + style.css** + `tests/static.test.js`.
4. **app.js** nối mọi thứ; chạy `node --test`, `node --check` từng file.
5. **Chạy tay trong trình duyệt** (`python3 -m http.server -d app 8000`) theo danh sách ở Proof; gọi subagent `verifier` với plan này.
   Agent dừng ở đây; người review diff và commit.

## Risks
- **Dữ liệu hỏng bị ghi đè** (rủi ro chính, risk-list dòng 1 + C3): mọi đường ghi đi qua `store.save`/`store.replace`; test chứng minh
  `setItem` không bao giờ được gọi khi `readError` trừ `replace`. Không còn chỗ nào trong app.js gọi `localStorage` trực tiếp.
- **Đổi giá trị trả về của `store.load`** làm vỡ app.js nếu commit lệch nhau → bước 1 và 4 commit cùng nhau.
- **`todo.v1` = `"null"`**: code hiện tại coi là danh sách trống (`|| []`); theo chữ của A13 ("đọc được nhưng không phải mảng") thì là
  đọc lỗi. Plan theo A13 (Q5).
- **Nhập thất bại khi bộ nhớ đầy** (AC14, AC21): `setItem` ném lỗi thì giá trị cũ không đổi; plan dựa vào điều này, test bằng
  `localStorage` giả ném `QuotaExceededError`, và kiểm lại tay ở trình duyệt.
- **Tên file theo ngày**: dùng giờ máy, không UTC (khách ở VN sao lưu lúc 0h–7h sẽ ra sai ngày nếu dùng UTC).
- **Không có tự động hoá trình duyệt**: tải file, chọn file, `<dialog>`, bàn phím, trình đọc màn hình, Network chỉ kiểm tay (Q6).
- **pre-commit**: commit sửa `app/` phải kèm thay đổi trong `plan/`; người commit ghi tiến độ vào plan trong cùng commit.
- **Quyết định nhỏ plan tự chọn** (người duyệt xem): tiêu đề chỉ có khoảng trắng bị từ chối như tiêu đề rỗng (khớp cách `add` đã
  `trim`); `id` rỗng bị từ chối; `version` khác 1 bị từ chối; sao lưu lớn hơn giới hạn chỉ hiện câu C2 (câu đó đã nói "đã lưu").

## Proof
| AC | Bằng gì |
|---|---|
| 1 (nội dung file) | `backup.test.js`: `toBackupText` thụt lề, đúng 3 tiêu đề/`done`, chỉ các khoá cho phép, kể cả khi việc trong bộ nhớ có thêm trường lạ; `backupFileName` cho một ngày cố định |
| 1 (tải về, câu báo), 2, 3 | Tay, trình duyệt (Network tab, xoá dữ liệu trang) |
| 3 (load khi chưa có khoá) | `store.test.js`: không có khoá → `readError: false`, `[]` |
| 4 | `backup.test.js`: `MESSAGES` có câu nguyên văn; tay: không có file tải về |
| 5, 6 | `backup.test.js`: `confirmText` với 12/30 và 1/30 ra đúng chữ; `current: 0` → `null`. Tay: huỷ/đồng ý, tải lại |
| 7 | `backup.test.js`: `MAX_IMPORT_BYTES`; tay: file 1,1 MB bị từ chối trước khi đọc |
| 8, 9, 10a–c | `backup.test.js`: `parseBackup` từ chối trường lạ, bytes PNG, văn bản thường, trùng `id`, `title: ""`, `createdAt: "hôm qua"`; nhận file hợp lệ |
| 11 | `backup.test.js`: tiêu đề `<img …>` qua `parseBackup` nguyên chữ; tay: không có alert |
| 12 | `backup.test.js`: 5.000 việc × 200 ký tự → `tooBigToImport` đúng; câu C2 nguyên văn. Tay: file > 1 MB tải về |
| 13 | `store.test.js`: `setItem` ném lỗi → `save` trả `'failed'`. Tay: thông báo + câu A8, việc còn trên màn hình, mất khi tải lại |
| 14 | `store.test.js`: `replace` khi `setItem` ném lỗi → `'failed'`, giá trị cũ còn nguyên. Tay |
| 15, 16, 17 | `store.test.js`: `{hỏng`, `{"a": 1}`, `getItem` ném lỗi → `readError: true`; sau đó `save` ×3 → `'skipped'`, `setItem` không được gọi, không khoá mới. Tay: dải báo, không hộp thoại, không dòng trống |
| 18 | Tay (tải file); logic là `toBackupText` trên `todos` đang hiện |
| 19, 20 | `backup.test.js`: hai mẫu câu đọc lỗi; `store.test.js`: `replace` thành công → `readError: false`, `save` sau đó ghi được (31 việc). Tay: huỷ/đồng ý, dải báo biến mất |
| 21 | `store.test.js`: đọc lỗi + `setItem` ném lỗi → `replace` `'failed'`, `readError` vẫn `true`, giá trị vẫn `{hỏng`; `save` tiếp theo `'skipped'` |
| 22 | `backup.test.js` (từ chối, như 7/8); tay: không có hộp xác nhận, `todo.v1` vẫn `{hỏng` |
| 23 | `static.test.js`: `index.html` có dòng chữ F4 |
| 24 | `static.test.js`: mọi giá trị trong `MESSAGES` và chữ hiển thị trong `index.html` không chứa "localStorage", "JSON", "console" |
| 25 | Tay: chỉ bàn phím + VoiceOver |
| 26 | `static.test.js`: không có `src`/`href` bắt đầu bằng `http`, `//` trong `index.html` |
| Không vỡ luồng cũ | `store.test.js`: lưu rồi đọc lại; tay: thêm, đánh dấu xong, xoá, lọc |

Chạy: `node --test` (toàn bộ xanh) · `node --check app/*.js` · verifier subagent · danh sách tay ở trên do một người chạy.

## Questions (cần trả lời trước khi accept)
- Q1. Size Medium (5 file app, 1 module mới) hay Large vì spec ghi `Risk: high` và đổi tầng lưu → Khoa duyệt plan trước khi code?
- Q2. Thêm file mới `app/backup.js` dù spec chỉ liệt kê 4 file sửa? (Để logic kiểm file và câu chữ test được bằng Node không cần DOM.)
- Q3. 1 MB = 1.048.576 byte hay 1.000.000 byte? → Khoa (owner S1)
- Q4. File hợp lệ nhưng `todos: []`: từ chối (đề xuất, vì nhập sẽ xoá hết mà không còn gì thay) hay cho nhập kèm xác nhận?
- Q5. `todo.v1` = `"null"`: đọc lỗi (theo A13) hay danh sách trống (như code hiện tại)?
- Q6. Các AC chỉ kiểm được trong trình duyệt (2, 25, phần tải/chọn file/dialog) do một người chạy tay — chấp nhận?
