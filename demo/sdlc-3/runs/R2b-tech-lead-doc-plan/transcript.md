# R2b-tech-lead-doc-plan

Chạy 2026-10-27 09:34 ở `persona-empty` (thư mục riêng của lượt này), chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Bạn là Khoa, tech lead. Bạn KHÔNG đọc cuộc trò chuyện giữa engineer và Claude, chỉ có bản plan dưới đây. Việc của bạn:
1) Chỉ với bản plan này, một engineer khác trong team có làm theo được không? Nếu không, thiếu chỗ nào (liệt kê).
2) Trả lời các câu hỏi ở mục Questions của plan: câu nào của bạn thì chốt (Có/Không hoặc giá trị cụ thể, một câu lý do); câu nào không phải của bạn thì nói chuyển ai.
3) Thay đổi này hạng Vừa hay Lớn theo bảng phân hạng (Lớn = đụng nhiều module, đổi kiến trúc: tech lead duyệt plan trước khi code). Nếu Lớn, bạn có duyệt plan không, kèm điều kiện gì.

--- PLAN ---
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
| `app/backup.js` (**mới**, xem Q2) | Logic không DOM: tạo nội dung file, tên file, kiểm file nhập, lời xác nhận, mọi câu chữ mới (một object `MESSAGES`), **và hai hàm điều phối `persist` / `importBackup`** để quyết định "ghi gì, báo gì" được test bằng Node |
| `app/app.js` | Chỉ còn nối DOM: nút, `<dialog>`, vùng thông báo, dải báo F5, dòng trống; gọi `persist` / `importBackup` và vẽ kết quả. Không có logic lưu riêng, không chạm `localStorage` |
| `app/index.html` | Nút "Sao lưu ra file", `<input type="file">` có nhãn "Nhập từ file", vùng `role="status" aria-live`, dải báo F5, dòng trống, dòng chữ F4, `<dialog>` xác nhận, `<script src="backup.js">` **giữa** `store.js` và `app.js` |
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
  - `store.readError` là **nguồn duy nhất** của trạng thái đọc lỗi; app.js không giữ bản sao (tránh dải báo đã ẩn mà store vẫn chặn ghi,
    hoặc ngược lại).
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
  - `persist(store, todos)` → `{ message }`: `'failed'` → thông báo F3 (A8); `'skipped'` → không thông báo (A14); `'saved'` → `null`
    (xoá thông báo F3 cũ).
  - `importBackup({ store, current, text, ask })` (async; `ask(câu)` trả `Promise<boolean>`, app.js truyền hàm mở `<dialog>`, test
    truyền hàm giả) → `{ todos, message }`. Thứ tự: kiểm số byte → `parseBackup` → `confirmText` → `ask` nếu cần → **`store.replace`**
    (không bao giờ `save`) → `'saved'`: trả danh sách mới + "Đã nhập N việc."; `'failed'`: trả **`current`** + thông báo F3. Từ chối hoặc
    huỷ: trả `current`, không gọi `replace`.
- **`app.js`**:
  - Khởi động: `todos = store.load().todos`; `store.readError` → hiện dải báo F5, ẩn dòng trống (A18).
  - `commit()`: `persist(store, todos)` rồi `render()`; `render()` hiện dải báo theo `store.readError`.
  - Dòng trống dựa trên `todos.length === 0`, **không** dựa trên `visible()`: bộ lọc "Đã xong" không có việc nào vẫn không hiện gì như
    hôm nay.
  - Sao lưu: rỗng → "Chưa có việc nào để sao lưu", không tải; ngược lại `Blob` + `URL.createObjectURL` + `<a download>` (không request
    mạng), báo "Đã sao lưu N việc."; nếu `tooBigToImport` thì hiện đúng câu C2 thay cho câu đếm.
  - Nhập: kiểm `file.size > MAX_IMPORT_BYTES` **trước khi đọc** (không đọc file lớn) → từ chối; hiện "Đang đọc file…" (U3);
    `await file.text()` → `importBackup({ store, current: todos, text, ask })` → gán `todos`, hiện `message`, `render()`. `ask` mở
    `<dialog>` (`showModal`, Esc = huỷ, `aria-labelledby` trỏ vào câu hỏi). Reset `input.value` để chọn lại cùng file được.
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
- **Bước rủi ro nhất: bước 1 + 4 (store mới và nối vào app).** Hai cách hỏng:
  - *Báo nhầm đọc lỗi với dữ liệu tốt*: khách đang dùng bình thường bỗng thấy danh sách trống + dải báo, và từ đó không gì được lưu.
    Đây là luồng hôm nay đang chạy (mở app → thấy việc cũ → thêm/đánh dấu/xoá được lưu) và có thể vỡ cho **mọi** khách.
  - *Ghi đè dữ liệu hỏng* (risk-list dòng 1 + C3): một đường ghi lách qua store, hoặc nhập file gọi `save` thay vì `replace` (khi đọc
    lỗi thì `save` trả `'skipped'`, app báo "Đã nhập" mà không lưu gì).
  - Cách biết: test trong `store.test.js` và `backup.test.js` (mục Proof, dòng "Bước rủi ro"); `static.test.js` chặn `localStorage`
    trong `app.js`; tay: mở app với dữ liệu thật đang có từ bản cũ trước khi chạy các AC khác.
- **File sao lưu khách tải về nhưng không nhập lại được**: `toBackupText` và `parseBackup` lệch nhau (ví dụ một luật kiểm chặt hơn dữ
  liệu app tự tạo). Khách chỉ phát hiện khi đã sang máy mới, lúc đó không còn bản gốc. Test vòng: mọi danh sách app tạo được
  (`add` có `trim`, `crypto.randomUUID`, `Date.now()`, `done` cả hai giá trị, tiêu đề có ký tự lạ/emoji/HTML) → `parseBackup(toBackupText(x))`
  ra đúng `x`. Ngoại lệ đã biết duy nhất: file lớn hơn giới hạn (C2, đã có câu báo).
- **Thứ tự `<script>`**: thiếu hoặc đặt `backup.js` sau `app.js` thì app.js ném lỗi lúc khởi động, cả app trắng. `static.test.js` kiểm.
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
| **Bước rủi ro: không báo nhầm** | `store.test.js`: mảng hợp lệ (kể cả `[]`, kể cả dữ liệu do bản app hiện tại ghi) → `readError: false`; `save` sau đó gọi `setItem` đúng 1 lần |
| **Bước rủi ro: không ghi đè** | `backup.test.js`: `importBackup` khi `store.readError` gọi `replace`, không gọi `save`; `replace` `'failed'` → trả `current`, có thông báo F3; huỷ/từ chối → `replace` không được gọi. `static.test.js`: `app.js` không chứa `localStorage` |
| Vòng sao lưu → nhập | `backup.test.js`: `parseBackup(toBackupText(x))` ra đúng `x` cho các danh sách ở mục Risks |
| Thứ tự script | `static.test.js`: `store.js` < `backup.js` < `app.js` trong `index.html` |
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
| Không vỡ luồng cũ | `store.test.js`: lưu rồi đọc lại; `backup.test.js`: `persist` `'saved'` → không thông báo. Tay: mở app với dữ liệu đã có từ bản cũ, thêm, đánh dấu xong, xoá, lọc "Đã xong" khi chưa có việc xong (không hiện dòng trống) |

## Cách đơn giản hơn đã cân nhắc và bỏ
- **Không thêm file mới, để hết trong `app.js`, chỉ kiểm tay.** Khớp danh sách file của spec, nhưng `app.js` chạy DOM ngay khi nạp nên
  Node không test được: phần nguy hiểm nhất (khi nào được ghi) chỉ còn kiểm tay. Bỏ.
- **Cờ `readError` chỉ ở `app.js`, store giữ nguyên "ngốc".** Ít thay đổi ở store hơn, nhưng một chỗ gọi `save` quên kiểm cờ là ghi đè
  dữ liệu hỏng. Bỏ; luật nằm ở store.
- **Giả DOM trong test để chạy thẳng `app.js`.** Không có package (S4) thì phải tự viết DOM giả, nhiều hơn cả phần code cần test. Bỏ;
  thay bằng `persist` / `importBackup` không DOM.
- **`window.confirm()` thay `<dialog>`.** Đơn giản nhất, nhưng A10 đã chốt `<dialog>`. Không phải lựa chọn.

Chạy: `node --test` (toàn bộ xanh) · `node --check app/*.js` · verifier subagent · danh sách tay ở trên do một người chạy.

## Questions (cần trả lời trước khi accept)
- Q1. Size Medium (5 file app, 1 module mới) hay Large vì spec ghi `Risk: high` và đổi tầng lưu → Khoa duyệt plan trước khi code?
- Q2. Thêm file mới `app/backup.js` dù spec chỉ liệt kê 4 file sửa? (Để logic kiểm file và câu chữ test được bằng Node không cần DOM.)
- Q3. 1 MB = 1.048.576 byte hay 1.000.000 byte? → Khoa (owner S1)
- Q4. File hợp lệ nhưng `todos: []`: từ chối (đề xuất, vì nhập sẽ xoá hết mà không còn gì thay) hay cho nhập kèm xác nhận?
- Q5. `todo.v1` = `"null"`: đọc lỗi (theo A13) hay danh sách trống (như code hiện tại)?
- Q6. Các AC chỉ kiểm được trong trình duyệt (2, 25, phần tải/chọn file/dialog) do một người chạy tay — chấp nhận?

## Tool call (0)

(không có)

## Claude · 45 s

# Khoa duyệt plan: sao lưu, nhập lại, báo lỗi lưu

## 1) Engineer khác làm theo được không?

**Được, với vài chỗ cần sửa.** Phần hay nhất là luật "không ghi khi đọc lỗi" nằm ở `store`, `importBackup` chỉ gọi `replace`, và test được bằng Node. Chỗ còn thiếu hoặc mơ hồ:

1. **Order of work tự mâu thuẫn.** Bước 1 ghi "chưa đụng app.js", rồi lại bảo gộp vào commit của bước 4. Hãy viết lại thành các commit cụ thể:
   - Commit A: `backup.js` + test. Chưa ai gọi nên an toàn.
   - Commit B: `store.js` + `app.js` + html/css + test. Đổi kiểu trả về của `load` và nối app phải đi cùng nhau.
   - Mỗi commit kèm thay đổi trong `plan/` theo pre-commit.
2. **Câu chữ nằm ngoài plan.** `MESSAGES` (C2, A8, F5 bước 4, F1.5) chỉ trỏ về spec. Chấp nhận được nếu engineer có spec, nhưng plan cần ghi rõ mục nào trong spec. Các mã A/F/C/U/AC cũng nên có một dòng chú dẫn.
3. **Chưa có xử lý khi `file.text()` bị lỗi** (file đọc không được, bị thu hồi quyền). Cần một câu báo và phải trả lại `current`.
4. **Chưa nói về `URL.revokeObjectURL`** sau khi tải. Cần gọi, kẻo rò bộ nhớ.
5. **`static.test.js` chỉ cấm `localStorage` trong `app.js`.** Cấm luôn trong `backup.js`, vì `backup.js` cũng không được tự ghi.
6. **Chưa nói app có `store.load/save` gọi ở chỗ nào khác ngoài `app.js` không.** Cần grep xác nhận trước khi đổi kiểu trả về.
7. **Chưa có rollback.** Nên ghi: khoá `todo.v1` và dạng dữ liệu không đổi, nên revert commit là an toàn.
8. **Kiểm tay không ghi rõ ai chạy, trình duyệt nào, ghi kết quả ở đâu** (xem Q6).

## 2) Trả lời Questions

- **Q1. Large.** Plan đổi hợp đồng của tầng lưu (`load`/`save`/`replace`), thêm module mới, chạm cả 5 file trong `app/` và dựng bộ test đầu tiên. Spec lại ghi `Risk: high`. Tôi duyệt, kèm điều kiện ở mục 3.
- **Q2. Có.** Thêm `app/backup.js` là đúng, vì không DOM thì Node test được. Giữ script thường (không ES module, không build), thứ tự `store` → `backup` → `app` như plan.
- **Q3. 1 MB = 1.048.576 byte** (1 MiB), dùng một hằng `MAX_IMPORT_BYTES` cho cả hai chỗ kiểm (`file.size` và `TextEncoder`). Test biên ở đúng 1.048.576 và 1.048.577. Nếu có câu chữ hiển thị "1 MB" thì để nguyên.
- **Q4. Từ chối `todos: []` thì tôi đồng ý về kỹ thuật**, vì app không tạo ra file rỗng (nó chặn sao lưu khi rỗng). Nhưng đây là hành vi sản phẩm và câu chữ: **chuyển product owner chốt** có chặn hay không, **Linh** chốt câu báo. Câu báo phải nói rõ "file không có việc nào", không phải "file sai".
- **Q5. Đọc lỗi**, theo A13. Ghi đè mà không báo là mất dữ liệu, còn báo nhầm trong trường hợp này gần như không xảy ra, vì app không bao giờ ghi `"null"`.
- **Q6. Chấp nhận kiểm tay, có điều kiện.** Checklist phải nằm trong `plan/`, ghi người chạy, ngày, trình duyệt, đạt hay không. Tối thiểu là **Safari iOS máy thật**, Chrome Android và một trình duyệt desktop. Riêng tải file và chọn file thì chạy cả ba, vì khách dùng điện thoại.
- **Riêng tư và pháp lý: chuyển Mai** nếu cần câu cảnh báo kiểu "file này chứa việc của bạn". Plan hiện không đụng đến.

## 3) Hạng và duyệt

**Hạng Lớn. Tôi duyệt plan với các điều kiện:**

1. Sửa mục 1–7 ở trên trước khi chuyển `Status: accepted`.
2. Q3 chốt như trên. Q4 chờ PO và Linh, mặc định từ chối. Q5 chốt như trên.
3. **Thử bằng dữ liệu thật từ bản cũ trước mọi AC khác.** Mở bản mới với `todo.v1` do bản hiện tại ghi, và thử cả trường hợp 2.000 việc, rồi thêm, đánh dấu, xoá. Đây là bước rủi ro nhất, đúng như plan nêu.
4. Review diff của commit B bởi một người khác, vì đó là chỗ có thể làm hỏng luồng của mọi khách.
5. Không nâng giới hạn 1 MB. Nếu thấy khách vượt, câu C2 báo trước như đã thống nhất.

Chưa có điều kiện nào ngoài danh sách này. Sửa xong thì chuyển `Status: accepted` và bắt đầu code.
