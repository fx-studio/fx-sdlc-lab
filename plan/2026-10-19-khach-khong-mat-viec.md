# Plan: Sao lưu ra file, nhập lại, và báo khi không lưu được

Status: accepted · From: spec/2026-10-19-khach-khong-mat-viec.md (accepted) · Size: **Large** [Khoa, Q1] · Date: 2026-10-27

Khoa (tech lead) đã duyệt plan này **có điều kiện** [demo/sdlc-3/runs/R2b-tech-lead-doc-plan]. Một người đổi chữ `draft` ở dòng 3 thành
`accepted` khi các điều kiện ở mục "Điều kiện duyệt" đã có trong plan. Chưa viết code trước đó.

**Chú dẫn mã:** `F<n>` = luồng trong mục User flows của spec · `A<n>` = câu trả lời giả định, `C<n>` = concern đã quyết (mục Assumptions,
Concerns của spec) · `AC<n>` = tiêu chí nghiệm thu thứ n của spec · `P<n>`/`S<n>`/`U<n>` = luật trong `policy-privacy@1`,
`policy-security@1`, `policy-ux@2` · `Q<n>` = câu hỏi của plan này (mục Quyết định) · `M<n>` = câu chữ (mục Câu chữ) ·
`T<n>` = bước kiểm tay (mục Proof).

## Context
Khách mất hết việc khi đổi máy hoặc xoá dữ liệu trình duyệt, vì app chỉ giữ việc trong bộ nhớ trình duyệt (`app/store.js`). Spec chốt:
sao lưu ra file (F1), nhập lại thay toàn bộ có xác nhận (F2), báo khi ghi lỗi (F3), dòng chữ nói việc được giữ ở đâu (F4), và khi danh
sách đã lưu không đọc được thì báo và **không ghi đè** (F5). Hôm nay `store.save` nuốt lỗi, `store.load` trả `[]` cho cả "chưa có" lẫn
"hỏng", và lần lưu sau ghi đè dữ liệu hỏng. `tests/` đang trống: plan này dựng bộ test đầu tiên.

## Quyết định
| Q | Câu hỏi | Trả lời | Ai |
|---|---|---|---|
| Q1 | Size | **Large**: đổi hợp đồng tầng lưu, thêm module, chạm cả 5 file `app/`, bộ test đầu tiên, spec `Risk: high` | Khoa [R2b] |
| Q2 | Thêm `app/backup.js` ngoài danh sách file của spec? | **Có.** Script thường, không ES module, không build; thứ tự `store` → `backup` → `app` | Khoa [R2b] |
| Q3 | 1 MB bằng bao nhiêu byte? | **1.048.576 byte** (1 MiB). Một hằng `MAX_IMPORT_BYTES` cho cả `file.size` khi nhập và `TextEncoder` khi sao lưu; test biên 1.048.576 (nhận) và 1.048.577 (từ chối). Chữ hiển thị vẫn ghi "1 MB" | Khoa [R2b] |
| Q4 | File hợp lệ nhưng `todos: []` | **Chặn.** Câu báo nguyên văn M8 | Thảo (product owner) [demo/sdlc-3/runs/R2c-thao-q4], câu chữ Linh (UX owner) [demo/sdlc-3/runs/R2c-linh-q4]; Khoa đồng ý về kỹ thuật [R2b] |
| Q5 | `todo.v1` = `"null"` | **Đọc lỗi**, theo A13. App không bao giờ ghi `"null"`, nên báo nhầm gần như không xảy ra | Khoa [R2b] |
| Q6 | AC chỉ kiểm được trong trình duyệt do người chạy tay? | **Chấp nhận, có điều kiện:** checklist nằm trong plan này, ghi người chạy, ngày, trình duyệt, đạt/không; tối thiểu Safari iOS máy thật, Chrome Android, một trình duyệt desktop; tải file và chọn file chạy cả ba | Khoa [R2b] |
| Q7 | Các câu chữ **mới** (không có nguyên văn trong spec), mục Câu chữ cột "Đề xuất" | **Linh duyệt**: các câu đề xuất đạt, trừ M11 và M12 (Linh thay, ghi ở mục Câu chữ) | Linh [R2e] |
| – | Câu cảnh báo kiểu "file này chứa việc của bạn" | Plan **không** thêm. Nếu cần thì chuyển Mai (privacy) | Khoa [R2b] |

`[R2b]` = `demo/sdlc-3/runs/R2b-tech-lead-doc-plan`. `[R2e]` = `demo/sdlc-3/runs/R2e-linh-q7`.

## Điều kiện duyệt (Khoa)
1. Sửa 7 điểm Khoa nêu: Order of work theo commit A/B (mục Order of work); câu chữ và chú dẫn mã trong plan (mục Câu chữ, Chú dẫn);
   lỗi `file.text()` (Thiết kế, M14); `URL.revokeObjectURL` (Thiết kế); cấm bộ nhớ trình duyệt trong cả `backup.js` (Proof, static);
   grep nơi gọi `store` (Risks); rollback (mục Rollback). Kiểm tay có người/ngày/trình duyệt (Proof, bảng kiểm tay).
2. Q3, Q5 như trên; Q4 đã có Thảo và Linh trả lời.
3. **Thử bằng dữ liệu thật từ bản cũ trước mọi AC khác**, kể cả 2.000 việc (T0).
4. **Diff của commit B được một người khác review** (không phải người viết code).
5. Không nâng giới hạn 1 MB; khách vượt thì câu M2 báo trước (C2).

## Files that change
| File | Commit | Thay đổi |
|---|---|---|
| `app/backup.js` (mới, Q2) | A | Logic không DOM: nội dung file, tên file, kiểm file nhập, lời xác nhận, `MESSAGES`, hai hàm điều phối `persist` / `importBackup`. Không đụng bộ nhớ trình duyệt; nhận `store` làm tham số |
| `tests/backup.test.js` (mới) | A | Test mọi hàm của `backup.js` với `store` giả, `ask` giả, file giả `{ size, text() }` |
| `app/store.js` | B | `load()` phân biệt chưa có / đọc lỗi; `save()` trả kết quả; khoá ghi khi đọc lỗi; `replace()` cho đường nhập file. Thêm `module.exports` có điều kiện |
| `app/app.js` | B | Chỉ còn nối DOM: nút, `<dialog>`, vùng thông báo, dải báo F5, dòng trống; gọi `persist` / `importBackup` và vẽ kết quả |
| `app/index.html` | B | Nút "Sao lưu ra file", `<input type="file">` có nhãn "Nhập từ file", vùng `role="status" aria-live="polite"`, dải báo F5, dòng trống, dòng chữ F4 (M12), `<dialog>`, `<script src="backup.js">` giữa `store.js` và `app.js` |
| `app/style.css` | B | Kiểu cho dải báo, vùng thông báo, dialog, dòng trống |
| `tests/store.test.js` · `tests/static.test.js` (mới) | B | Bộ nhớ trình duyệt giả (`getItem`/`setItem` ghi lại số lần gọi, ném lỗi được khi cần); kiểm tĩnh `index.html`, `app.js`, `backup.js` |
| `plan/2026-10-19-khach-khong-mat-viec.md` | A, B | Người commit ghi mục Tiến độ và bảng kiểm tay (pre-commit đòi `plan/` đi cùng `app/`) |

Không file nào khác gọi `store` hay bộ nhớ trình duyệt: đã grep 2026-10-27, xem Risks.

### Thiết kế
- **`store`** (giữ khoá `todo.v1` và dạng mảng việc; không thêm khoá, không thêm trường, A12):
  - `load()` → `{ todos, readError }`. Không có khoá (`getItem` trả `null`) → `{ todos: [], readError: false }`. Có dữ liệu nhưng
    `JSON.parse` lỗi, parse ra không phải mảng (kể cả `"null"`, Q5), hoặc `getItem` ném lỗi → `{ todos: [], readError: true }`.
    Không kiểm từng việc trong mảng (A13 chỉ có ba trường hợp).
  - `store.readError` là **nguồn duy nhất** của trạng thái đọc lỗi, chỉ trong bộ nhớ trang (A12); `app.js` không giữ bản sao.
  - `save(todos)` → `'saved' | 'failed' | 'skipped'`. Khi `readError`: **không gọi `setItem`**, trả `'skipped'` (F5 bước 5, A14).
    `setItem` ném lỗi → `'failed'` (không `console.error` nữa).
  - `replace(todos)` → `'saved' | 'failed'`: đường duy nhất được ghi khi đọc lỗi (F5 bước 6, A15); chỉ xoá `readError` khi ghi thành
    công (A17).
- **`backup.js`** (không có chữ "localStorage" kể cả trong comment, vì `static.test.js` cấm):
  - `MAX_IMPORT_BYTES = 1048576` (Q3).
  - `toBackupText(todos)` → `JSON.stringify({ version: 1, todos: [{ id, title, done, createdAt }] }, null, 2)`; chỉ chép bốn trường
    (P2, P3).
  - `backupFileName(date)` → `todo-sao-luu-YYYY-MM-DD.json` theo **giờ máy** (A11).
  - `tooBigToImport(text)` → `new TextEncoder().encode(text).length > MAX_IMPORT_BYTES` (F1 bước 5).
  - `parseBackup(text)` → `{ ok: true, todos }` hoặc `{ ok: false, message }`, chỉ dùng `JSON.parse`, không bao giờ eval (S1):
    - không parse được, hoặc gốc không phải object (ảnh, văn bản bất kỳ, `null`, mảng) → M9;
    - khoá gốc khác đúng `version` + `todos`, `version !== 1`, `todos` không phải mảng → M9;
    - `todos` rỗng → M8 (Q4);
    - một việc có khoá khác đúng bốn khoá, `id` không phải chuỗi hoặc rỗng, `title` không phải chuỗi hoặc rỗng sau `trim`, `done`
      không phải boolean, `createdAt` không phải số hữu hạn, hoặc hai việc trùng `id` → M10, từ chối **cả file** (A7).
  - `confirmText({ readError, current, incoming })` → `null` khi không đọc lỗi và `current === 0` (F2 bước 6); ngược lại M5, M6
    hoặc M7.
  - `persist(store, todos)` → `{ message }`: `'saved'` → `null` (xoá thông báo F3 cũ); `'failed'` → M3; `'skipped'` → `null` (dải
    báo F5 đã hiện, không bật gì thêm, A14).
  - `importBackup({ store, current, file, ask })` (async; `file` có `size` và `text()`; `ask(câu)` trả `Promise<boolean>`) →
    `{ todos, message }`. Thứ tự:
    1. `file.size > MAX_IMPORT_BYTES` → M11, **không gọi `file.text()`**;
    2. `await file.text()`; ném lỗi (file không đọc được, bị thu hồi quyền) → M14 (Khoa #3);
    3. `parseBackup` → lỗi thì trả `message` của nó;
    4. `confirmText` khác `null` → `await ask(câu)`; `false` → không có thông báo;
    5. **`store.replace(incoming)`** (không bao giờ `save`) → `'saved'`: trả `incoming` + M4b; `'failed'`: trả `current` + M17
       (F2 bước 8 bản sửa R9, F5 bước 8, A20).

    Mọi nhánh trừ bước 5 `'saved'` trả **`current`**; các nhánh 1–4 không gọi `replace`.
- **`app.js`**:
  - Khởi động: `todos = store.load().todos`; `render()`.
  - `render()`: dải báo F5 (M16) hiện khi `store.readError`; dòng trống (M13) hiện khi `todos.length === 0 && !store.readError`
    (A18). Dựa trên `todos`, **không** dựa trên `visible()`: lọc "Đã xong" khi chưa có việc xong vẫn không hiện gì như hôm nay. Tiêu
    đề vẫn qua `textContent` (S3). Thêm, đánh dấu, xoá giữ nguyên.
  - `commit()`: `message = persist(store, todos).message`, hiện ở vùng thông báo, rồi `render()`.
  - Sao lưu: `todos` rỗng → M1, không tải. Ngược lại `text = toBackupText(todos)`, `Blob` + `URL.createObjectURL` + `<a download>`
    + `click()`, rồi `setTimeout(() => URL.revokeObjectURL(url), 10000)` (Khoa #4; chờ 10 giây vì thu hồi ngay sau `click()` có thể
    làm hỏng tải trên Safari iOS, xem Risks). Báo M4a, hoặc M2 thay cho M4a khi `tooBigToImport(text)`. Không có request mạng (P1).
  - Nhập: hiện M15 (U3), `importBackup({ store, current: todos, file, ask })` với `ask` mở `<dialog>` (`showModal`, Esc = huỷ,
    `aria-labelledby` trỏ vào câu hỏi, nút "Thay" / "Huỷ", U5); gán `todos`, hiện `message`, `render()`; đặt lại `input.value` để chọn
    lại cùng file được.

### Câu chữ
Tất cả nằm trong `MESSAGES` của `backup.js` (trừ nhãn và M12 trong `index.html`, theo bảng Files that change; sửa sau review R3c). Cột "Nguồn": nguyên văn từ đâu; "Đề xuất" = câu mới, chờ
Linh (Q7). Không câu nào chứa "localStorage", "JSON", "console" (U4, AC24).

| M | Câu | Nguồn |
|---|---|---|
| M1 | Chưa có việc nào để sao lưu. | Spec F1 bước 4 [A6, Thảo] |
| M2 | File sao lưu đã lưu, nhưng quá lớn nên app không nhập lại được. | Spec F1 bước 5 [C2, Khoa · Linh · Thảo] |
| M3 | Thay đổi vừa rồi chưa được lưu. Hãy sao lưu ra file, rồi xoá bớt việc đã xong. | Câu sau: spec F3 bước 2 [A8, Linh]; câu trước: **đề xuất** |
| M4a | Đã sao lưu {n} việc. | **Đề xuất** (spec F1 bước 3 chỉ nói "báo đã sao lưu bao nhiêu việc") |
| M4b | Đã nhập {n} việc. | **Đề xuất** (spec F2 bước 6–7) |
| M5 | Thay {n} việc hiện có bằng {m} việc trong file? | Spec F2 bước 7 [A3, Khoa · Linh], S2 |
| M6 | Thay danh sách đã lưu không đọc được bằng {m} việc trong file? | Spec F5 bước 6 [A15, Khoa · Thảo] |
| M7 | Thay danh sách đã lưu không đọc được và {n} việc bạn vừa thêm (chưa lưu) bằng {m} việc trong file? | Spec F5 bước 6 [A19, Khoa] |
| M8 | File này không có việc nào, nên chưa nhập được. Danh sách của bạn vẫn giữ nguyên. Hãy chọn file sao lưu khác. | Q4 [Thảo, Linh]; viết lại theo F2 bước 4 [R7-linh, R7c Thảo đồng ý] |
| M9 | File này không phải file sao lưu của app, nên chưa nhập được. Danh sách của bạn vẫn giữ nguyên. Hãy chọn file tạo từ nút "Sao lưu ra file". | Linh viết lại theo F2 bước 4 [R7-linh] |
| M10 | File sao lưu này bị lỗi, nên chưa nhập được việc nào. Danh sách của bạn vẫn giữ nguyên. Hãy chọn file sao lưu khác. | Linh viết lại theo F2 bước 4 [R7-linh] |
| M11 | File này quá lớn, nên chưa nhập được. Danh sách của bạn vẫn giữ nguyên. Hãy chọn file sao lưu của danh sách ngắn hơn. | Linh viết lại theo F2 bước 4 [R7-linh] |
| M12 | Danh sách chỉ được lưu trên trình duyệt này, nên xoá dữ liệu trang web, đổi trình duyệt hoặc đổi máy là mất, trừ khi bạn đã sao lưu ra file. | Câu R2e của Linh bỏ vế "xoá dữ liệu" nên trượt AC23 (Claude báo ở R3). Mai đề xuất giữ (P4), Linh chốt chữ "dữ liệu trang web", Mai xác nhận đạt [R3c] |
| M13 | Chưa có việc nào. Nếu có file sao lưu, hãy bấm "Nhập từ file". | **Đề xuất** (spec mục Trạng thái màn hình, U3) |
| M14 | Không đọc được file này. Danh sách của bạn vẫn giữ nguyên. Hãy chọn lại file hoặc chọn file khác. | Linh viết lại theo F2 bước 4 [R7-linh] |
| M15 | Đang đọc file… | **Đề xuất** (spec F2 bước 2, U3) |
| M16 | Không đọc được danh sách đã lưu trên trình duyệt này. Việc bạn thêm hoặc sửa lúc này sẽ không được lưu. Nếu có file sao lưu, hãy bấm "Nhập từ file". | Spec F5 bước 4 [A16, Linh] (dải báo) |
| M17 | Chưa nhập được file. Danh sách trên màn hình vẫn nguyên nhưng có thể chưa được lưu, nên đừng tải lại trang. Hãy sao lưu ra file, xoá bớt việc đã xong rồi thử lại. | Spec F2 bước 8 sửa sau accepted; Linh chốt, đúng cả ca đã có phần chưa lưu (Khoa) [R9] |
| – | Nhãn: "Sao lưu ra file", "Nhập từ file" · nút hộp xác nhận: "Thay", "Huỷ" | Nhãn: spec F1, F2; nút hộp: **đề xuất** |

## Order of work
Agent viết code và chạy test; **người** review và commit (agent không commit). Mỗi commit kèm thay đổi trong file plan này (pre-commit).

1. **Commit A: `app/backup.js` + `tests/backup.test.js`.** Chưa file nào nạp `backup.js` (chưa có trong `index.html`), nên app chạy y
   như hôm nay. Xong khi: `node --test` xanh, `node --check app/backup.js`. Người commit ghi Tiến độ A.
2. **Commit B: `app/store.js` + `app/app.js` + `app/index.html` + `app/style.css` + `tests/store.test.js` + `tests/static.test.js`.**
   Đổi kiểu trả về của `load`/`save` và nối app phải đi cùng nhau, nếu tách thì app vỡ ở giữa. Thứ tự trong commit:
   1. grep lại nơi gọi `store` / bộ nhớ trình duyệt (Risks); khác kết quả 2026-10-27 thì dừng và báo;
   2. `store.js` + `store.test.js`;
   3. `index.html` + `style.css` + `static.test.js`;
   4. `app.js`;
   5. `node --test` xanh, `node --check` từng file `.js`; gọi subagent `verifier` với plan này;
   6. **T0 trước** (dữ liệu bản cũ, điều kiện 3), rồi bảng kiểm tay T1–T13 trên ba trình duyệt;
   7. **một người khác** review diff (điều kiện 4); người commit ghi Tiến độ B và bảng kiểm tay vào plan trong cùng commit.

## Risks
- **Bước rủi ro nhất: commit B.** Hai cách hỏng:
  - *Báo nhầm đọc lỗi với dữ liệu tốt*: khách đang dùng bình thường bỗng thấy danh sách trống + dải báo, và từ đó không gì được lưu.
    Luồng hôm nay đang chạy (mở app → thấy việc cũ → thêm, đánh dấu, xoá được lưu) có thể vỡ cho **mọi** khách. Biết bằng:
    `store.test.js` (dữ liệu bản cũ, 3 và 2.000 việc) và T0.
  - *Ghi đè dữ liệu hỏng* (risk-list dòng 1, C3): một đường ghi lách qua `store`, hoặc nhập file gọi `save` thay vì `replace` (khi đọc
    lỗi `save` trả `'skipped'`, app báo "Đã nhập" mà không lưu gì). Biết bằng: `backup.test.js` (`importBackup` không bao giờ gọi
    `save`), `store.test.js` (`setItem` 0 lần khi đọc lỗi), `static.test.js` (`app.js`, `backup.js` không có `localStorage`), T9–T10.
- **Nơi gọi `store`** (Khoa #6): grep `store\.(load|save)|localStorage` ngày 2026-10-27, ngoài `demo/` và `docs/`: code chỉ có
  `app/app.js:2` (`store.load()`), `app/app.js:24` (`store.save(todos)`) và `app/store.js` (nơi duy nhất dùng bộ nhớ trình duyệt). Không
  script, hook hay test nào khác gọi. Chạy lại ở bước B.1.
- **File sao lưu tải về được nhưng không nhập lại được**: `toBackupText` và `parseBackup` lệch nhau. Khách chỉ phát hiện ở máy mới, khi
  không còn bản gốc. Test vòng: mọi danh sách app tạo được (`add` có `trim`, `crypto.randomUUID`, `Date.now()`, `done` cả hai giá trị,
  tiêu đề có emoji, dấu tiếng Việt, HTML) → `parseBackup(toBackupText(x))` ra đúng `x`. Ngoại lệ duy nhất đã biết: file lớn hơn giới
  hạn (C2, M2).
- **Thứ tự `<script>`**: thiếu `backup.js` hoặc đặt sau `app.js` thì `app.js` ném lỗi lúc khởi động, cả app trắng. `static.test.js` kiểm.
- **Nhập thất bại khi bộ nhớ đầy** (AC14, AC21): dựa vào việc `setItem` ném lỗi thì giá trị cũ không đổi. Test bằng bộ nhớ giả ném
  `QuotaExceededError`, kiểm lại tay ở T8, T10.
- **Thu hồi URL tải quá sớm**: Safari iOS có thể tải hỏng nếu thu hồi ngay sau `click()`; plan chờ 10 giây. T1 trên Safari iOS kiểm.
- **Kiểm trên điện thoại cần HTTPS**: `crypto.randomUUID` (đã dùng trong `add` hôm nay) chỉ có ở secure context. Mở
  `http://<IP máy>:8000` từ điện thoại thì nút Thêm hỏng **trước cả thay đổi này**. Người chạy kiểm tay dùng một địa chỉ HTTPS (nơi app
  đang được đăng, hoặc một tunnel HTTPS) và ghi địa chỉ vào bảng kiểm tay.
- **Ngày trong tên file**: theo giờ máy, không UTC (sao lưu lúc 0h–7h ở VN ra sai ngày nếu dùng UTC). Test với giờ 00:30.
- **Spec hạn chót cho việc** (`spec/2026-10-19-han-chot-cho-viec.md`, đang draft) thêm trường `dueDate`. Khi nó được làm, file sao lưu
  bản 1 sẽ bỏ mất trường này và `parseBackup` sẽ từ chối file có trường đó; spec đó phải nâng `version` và sửa `backup.js`. Plan này
  không làm gì thêm; ghi để người làm spec kia biết.
- **Quyết định nhỏ plan tự chọn** (người review xem): tiêu đề chỉ có khoảng trắng bị từ chối như tiêu đề rỗng (khớp `add` đã `trim`);
  `id` rỗng bị từ chối; `version` khác 1 bị từ chối; sao lưu quá giới hạn chỉ hiện M2 (M2 đã nói "đã lưu").

## Rollback
- **Không đổi dữ liệu đã lưu:** khoá `todo.v1` và dạng mảng việc `{ id, title, done, createdAt }` giữ nguyên; bản mới không thêm khoá
  hay trường (A12). Dữ liệu bản mới ghi (kể cả sau khi nhập file) bản cũ đọc được.
- **Revert commit B** (`git revert <B>`, một người chạy) là an toàn cho dữ liệu: app quay lại hành vi cũ, tức dữ liệu hỏng lại bị ghi đè
  không báo ở lần lưu sau, và mất nút sao lưu/nhập. File sao lưu khách đã tải về vẫn nằm trên máy họ.
- **Revert commit A** một mình không ảnh hưởng gì khi B chưa có (chưa ai nạp `backup.js`); revert A mà giữ B thì app vỡ, nên revert theo
  thứ tự B rồi A.

## Proof
Chạy: `node --test` (toàn bộ xanh) · `node --check app/*.js` · subagent `verifier` · bảng kiểm tay dưới đây.

### Test tự động
| Test | Chứng minh | AC / mục |
|---|---|---|
| **`tests/store.test.js`** (commit B) | | |
| Không có khoá `todo.v1` → `readError: false`, `[]` | Chưa có là trống bình thường | AC3, A13 |
| Dữ liệu dạng bản cũ, 3 việc và **2.000 việc** → `readError: false`, đúng `todos`; `save` sau đó gọi `setItem` đúng 1 lần | Không báo nhầm | Điều kiện 3, Risks |
| `[]` đã lưu → `readError: false` | Danh sách rỗng đã lưu không phải lỗi | A13 |
| `{hỏng`, `{"a": 1}`, `"null"`, `getItem` ném lỗi → `readError: true` | Ba trường hợp đọc lỗi | AC15, AC16, AC17, Q5 |
| Đọc lỗi rồi `save` ba lần → `'skipped'`, `setItem` 0 lần, không có khoá mới, giá trị vẫn như cũ | Không ghi đè | AC15–AC17 |
| `setItem` ném `QuotaExceededError` → `save` `'failed'`, giá trị cũ không đổi | Ghi lỗi được báo | AC13 |
| `replace` khi `setItem` ném lỗi → `'failed'`; nếu đang đọc lỗi thì `readError` vẫn `true`, giá trị vẫn `{hỏng`, `save` sau đó `'skipped'` | Nhập thất bại không phá gì | AC14, AC21 |
| Đọc lỗi, `replace` 30 việc → `'saved'`, `readError: false`; `save` 31 việc sau đó ghi được | Thoát trạng thái đọc lỗi | AC19, AC20, A17 |
| `save` rồi `load` → đúng danh sách | Luồng cũ | Không vỡ luồng cũ |
| **`tests/backup.test.js`** (commit A) | | |
| `toBackupText`: thụt lề, đúng tiêu đề và `done`, chỉ các khoá cho phép, kể cả khi việc trong bộ nhớ có thêm trường lạ | Nội dung file | AC1, P2, P3 |
| `backupFileName` cho một ngày cố định và cho 00:30 giờ máy | Tên file | AC1, A11 |
| `tooBigToImport`: 5.000 việc × 200 ký tự → `true`; văn bản đúng 1.048.576 byte → `false`, 1.048.577 → `true` | Biên giới hạn | AC12, Q3 |
| `parseBackup` nhận file hợp lệ; từ chối bytes PNG, văn bản thường, `null`, mảng gốc (M9); khoá lạ ở gốc (M9) và ở một việc `"x": 1` (M10); `version: 2` (M9); trùng `id`, `title: ""`, `title: "  "`, `createdAt: "hôm qua"`, `createdAt` = `1e999` đọc ra Infinity (M10; `NaN` không viết được trong JSON nên rơi vào M9, sửa sau R3b); `todos: []` (M8) | Kiểm file | AC8, AC9, AC10, Q4 |
| Tiêu đề `<img src=x onerror=alert(1)>` qua `parseBackup` giữ nguyên chữ | Không chạy nội dung | AC11, S1 |
| Vòng `parseBackup(toBackupText(x))` = `x` | File tải về nhập lại được | Risks |
| `confirmText`: 12/30 → M5, 1/30 → M5, 0/30 → `null`, đọc lỗi 0/30 → M6, đọc lỗi 3/30 → M7 (so nguyên văn) | Lời xác nhận | AC5, AC6, AC19, AC20 |
| `persist`: `'saved'` → `null`, `'failed'` → M3, `'skipped'` → `null` | Thông báo F3 | AC13, AC15 |
| `importBackup`, `size` 1.048.577 → M11, `text()` không được gọi; `size` 1.048.576 → có đọc | Từ chối trước khi đọc | AC7, AC22, Q3 |
| `importBackup`, `text()` ném lỗi → M14, trả `current`, `replace` không được gọi | Khoa #3 | – |
| `importBackup`, file sai → trả `current`, `ask` và `replace` không được gọi | Từ chối không hỏi, không ghi | AC8–AC10, AC22 |
| `importBackup`, `current` rỗng, không đọc lỗi → không `ask`, `replace` 1 lần, M4b | Nhập vào danh sách trống | AC3 |
| `importBackup`, `current` 12 việc: `ask` nhận đúng M5; `ask` → `false` → `replace` 0 lần; `ask` → `true` → `replace` 1 lần, trả 30 việc | Huỷ / đồng ý | AC5, AC6 |
| `importBackup`, `replace` `'failed'` → trả `current` + M17 (cả khi đọc lỗi); thêm, đánh dấu, xoá vẫn M3 | Nhập thất bại | AC14, AC21, A20 |
| `importBackup` khi `store.readError`: `save` **không bao giờ** được gọi, chỉ `replace` | Không ghi đè | AC19–AC21, Risks |
| `MESSAGES`: M1, M2, M5–M8, M16 đúng nguyên văn nguồn; không giá trị nào chứa "localStorage", "JSON", "console" | Câu chữ | AC4, AC12, AC15, AC24 |
| **`tests/static.test.js`** (commit B) | | |
| `index.html`: `store.js` < `backup.js` < `app.js`; không `src`/`href` bắt đầu bằng `http`, `//` | Thứ tự script, không phụ thuộc ngoài | AC26, S4, Risks |
| `app/app.js` và `app/backup.js` không chứa `localStorage` | Chỉ `store` chạm bộ nhớ trình duyệt | Khoa #5 |
| `index.html` có M12, hai nhãn nút, vùng `role="status"`, `<dialog>`; chữ hiển thị không chứa "localStorage", "JSON", "console" | Dòng chữ F4, U4, U5 | AC23, AC24 |

### Kiểm tay
Chạy trên cây làm việc đã có thay đổi của commit B, **trước** khi commit B. Địa chỉ HTTPS cho điện thoại: xem Risks. Ô ghi `đạt` /
`không` + ghi chú; dòng ★ bắt buộc cả ba trình duyệt, dòng khác bắt buộc desktop, điện thoại nếu kịp.

Người chạy: **chủ kênh** (T12, bằng tay) + **máy** (T0–T11, T13: `demo/sdlc-4/kiem-tay-may.py`, Chromium headless 1228, 82/82 phép kiểm,
`demo/sdlc-4/runs/T-kiem-may/ket-qua.md`) · Ngày: 2026-10-29 (demo SDLC-4) · Desktop: Chromium headless (máy); Firefox trên macOS (người)
· Safari iOS: chưa thử (không có HTTPS) · Chrome Android: chưa thử · Địa chỉ đã mở: http://localhost:8000. Ô "đạt (máy)" là máy chạy, không
phải người nhìn.

| T | Việc làm | AC | Desktop | Safari iOS | Chrome Android |
|---|---|---|---|---|---|
| T0 ★ | **Trước mọi bước khác.** Trên bản hiện tại (chưa có thay đổi của commit B): tạo 3 việc (1 đã xong). Trên một hồ sơ trình duyệt khác, nạp 2.000 việc dạng cũ bằng console: `localStorage.setItem('todo.v1', JSON.stringify(Array.from({length: 2000}, (_, i) => ({id: crypto.randomUUID(), title: 'Việc ' + i, done: i % 3 === 0, createdAt: Date.now() - i}))))`. Mở bản mới ở cùng địa chỉ: đủ việc, đúng trạng thái, không dải báo; thêm, đánh dấu, xoá; tải lại vẫn giữ | Điều kiện 3 | đạt (máy) | chưa thử | chưa thử |
| T1 ★ | Sao lưu 3 việc: file `todo-sao-luu-<hôm nay>.json` tải về, mở thấy thụt lề, đúng nội dung, M4a. Danh sách trống: M1, không tải | AC1, AC4 | đạt (máy) | chưa thử | chưa thử |
| T2 | Tắt mạng: sao lưu và nhập vẫn chạy; tab Network không có request | AC2 | đạt (máy) | chưa thử | chưa thử |
| T3 ★ | Xoá dữ liệu trang: thấy M13, không dải báo; nhập file T1: không hỏi, đủ 3 việc; tải lại vẫn còn | AC3 | đạt (máy) | chưa thử | chưa thử |
| T4 ★ | 12 việc, nhập 30 việc: hộp M5; huỷ → 12 việc, tải lại 12; đồng ý → 30 việc, không Undo, tải lại 30. Lặp với 1 việc | AC5, AC6 | đạt (máy) | chưa thử | chưa thử |
| T5 ★ | Chọn file 1,1 MB, file có `"x": 1`, một ảnh, một file văn bản, ba file ở AC10, file `todos: []`: từng file bị từ chối, đúng câu, danh sách không đổi | AC7–AC10, Q4 | đạt (máy) | chưa thử | chưa thử |
| T6 | Tiêu đề `<img src=x onerror=alert(1)>` nhập vào hiện đúng chữ, không alert | AC11 | đạt (máy) | chưa thử | chưa thử |
| T7 ★ | 5.000 việc × 200 ký tự: sao lưu tải được file > 1 MB, thấy M2 | AC12 | đạt (máy) | chưa thử | chưa thử |
| T8 | Làm đầy bộ nhớ (ghi khoá khác tới khi lỗi), thêm việc: M3, việc còn trên màn hình; tải lại mất việc đó. 12 việc, nhập 30, đồng ý: M3, tải lại 12 việc | AC13, AC14 | đạt (máy) | chưa thử | chưa thử |
| T9 | `todo.v1` = `{hỏng`: dải báo M16, không dòng trống; thêm 2, đánh dấu 1, xoá 1: không hộp thoại, giá trị vẫn `{hỏng`, không khoá mới; tải lại: không còn việc, dải báo vẫn hiện. Lặp với `{"a": 1}` | AC15, AC16 | đạt (máy) | chưa thử | chưa thử |
| T10 ★ | Đọc lỗi: thêm 2, sao lưu: file có đúng 2 việc, `todo.v1` vẫn `{hỏng`. Nhập 30 việc khi chưa thêm: M6, huỷ/đồng ý, dải báo biến mất, thêm 1, tải lại 31. Thêm 3 rồi nhập: M7, huỷ/đồng ý. `{hỏng` + bộ nhớ đầy, nhập và đồng ý: dải báo vẫn hiện, `todo.v1` vẫn `{hỏng`. File 1,1 MB và `"x": 1` khi đọc lỗi: từ chối, không hỏi | AC18–AC22 | đạt (máy) | chưa thử | chưa thử |
| T11 | Màn hình chính có M12 | AC23 | đạt (máy) | chưa thử | chưa thử |
| T12 | Chỉ bàn phím (Tab, Enter/Space, Esc) sao lưu, chọn file, đồng ý và huỷ hộp xác nhận; VoiceOver/TalkBack đọc nhãn hai nút, câu hỏi, thông báo, dải báo | AC25 | bàn phím đạt (người, Firefox): sao lưu, chọn file, Esc huỷ, Tab + Enter thay. Ghi nhận: Huỷ không hiện viền sẵn khi hộp mở. Chrome của người kiểm không mở hộp chọn file kể cả bằng chuột (Firefox, Chromium máy mở được). VoiceOver chưa thử | chưa thử | chưa thử |
| T13 | Lọc "Đã xong" khi chưa có việc xong: không hiện dòng trống, giống hôm nay | Không vỡ luồng cũ | đạt (máy) | chưa thử | chưa thử |

## Tiến độ
Người commit điền (sau khi plan được duyệt, hook không cho agent sửa plan này).

- Commit A: commit có dòng này (2026-10-27, `node --test` trên đúng cây của commit A: 21 pass / 0 fail). `backup.js` chưa được
  `index.html` nạp nên chưa đổi hành vi app. Code do Claude viết ở R3 (`demo/sdlc-3/runs/R3-code-theo-plan/`).
- Commit B: commit có dòng này (2026-10-27, `node --test`: 38 pass / 0 fail). Người review diff: Khoa (giả lập) [R3c], cho commit
  kèm ba điều kiện, đã làm cả ba: (a) test ghim `add()` (trim, bỏ tiêu đề trắng, `id` chuỗi) và vòng sao lưu → nhập của danh sách app
  tự tạo, `tests/app.test.js` [R3d]; (b) tách A rồi B; (c) sửa plan dòng Câu chữ, M12, `createdAt`. Verifier [R3b]: 5 chỗ lệch, xử lý như trên.
  **Bảng kiểm tay: thiếu T0–T13, chưa người nào chạy.** Commit B trước kiểm tay là lệch plan (mục Kiểm tay), người chạy demo quyết
  vì demo không có người cầm ba thiết bị: tính năng **chưa nghiệm thu**. Máy đã chạy một phần T0 và T9 trên Chromium headless, đạt hết
  (`demo/sdlc-3/runs/R3e-t0-chromium/`); không thay ô nào trong bảng.
- Ghi nhận, không chặn: (1) ~~nhập file đang đọc mà khách thêm việc vào danh sách trống thì nhập ghi đè việc mới không hỏi~~: ca này không
  xảy ra (`add()` dùng `push`, cùng mảng); ca thật là hai lần nhập chồng nhau hoặc xoá việc lúc đang đọc file [R7a]. Đã sửa, hạng Small,
  test hai lần nhập fail trước khi sửa [R7b-B]; (2) câu M3 dùng chung khi nhập lỗi lúc lưu, đúng spec F2 bước 8, Linh đề xuất câu riêng
  cho lần sau: "Chưa nhập được file. Danh sách cũ của bạn vẫn nguyên. Hãy xoá bớt việc đã xong rồi thử lại."; (3) tiêu chí 23 của
  spec nên đổi theo chữ "dữ liệu trang web" (Mai), cần Thảo; (4) hộp xác nhận viết số "2001" chứ không "2.001" (máy thấy ở R3e), chờ Linh.
- Sau commit B (2026-10-27): năm câu từ chối M8–M11, M14 chưa đạt spec F2 bước 4 (thiếu "danh sách giữ nguyên" hoặc "làm gì tiếp").
  Lượt đọc lại so với spec [R3f] tìm ra; plan, Linh, verifier, Khoa đều bỏ qua. Linh viết lại, Thảo đồng ý M8. Hạng Trivial.
- R9 (2026-10-27, `node --test`: 42 pass / 0 fail): spec sửa sau accepted (commit `65fae52`, Thảo) nên làm luôn ba mục ghi nhận (2),
  (3), (4) ở trên: M17 cho lúc nhập lỗi khi lưu; số từ 1.000 có dấu chấm (`formatCount`, Linh: mọi câu có số, cả dòng đếm việc chưa
  xong). Hạng Small (Khoa, Claude cùng đề xuất). Code do Claude viết [R9-code-cau-nhap-va-so, R9b-dong-dem].
