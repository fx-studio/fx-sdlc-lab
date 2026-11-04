# Trả lời giả định và chỗ đáng lo của spec hạn chót (bước 0 của R6, SDLC-5)

Người chạy demo gom từ ba lượt `runs/B6-*` (nhân vật giả lập, sonnet, chỉ biết hồ sơ ở `personas/`). Spec được hỏi:
`spec/2026-10-19-han-chot-cho-viec.md` bản draft 2026-10-20, kèm bối cảnh mới: bản sao lưu `version: 1` đã ra (từ chối trường lạ), lưu lỗi
đã báo trên màn hình.

| Dòng | Trả lời | Ai |
|---|---|---|
| A1 | Có | Linh |
| A2 | Có (cho đặt/đổi/bỏ trên dòng: Thảo; nhãn "Hạn chót của việc <tiêu đề>": Linh) | Thảo · Linh |
| A3 | **Không.** Bỏ hạn chót làm mất ngày đã đặt → Undo 10 giây theo U2. Đổi sang ngày khác thì không cần Undo. Tiêu chí 6 thêm bước Undo | Linh |
| A4 | Có | Thảo |
| A5 | Có ("Hạn 25/10/2026") | Linh |
| A6 | Có | Thảo |
| A7 | Có | Thảo |
| A8 | Có | Linh |
| A9 | Có. Ngày theo giờ máy bằng `getFullYear/getMonth/getDate`, **không** `toISOString()` (UTC lệch ngày ở +7) | Thảo · Khoa |
| A10 | Có | Linh |
| A11 | Có | Thảo |
| A12 | Có | Thảo |
| A13 | Có | Linh |
| A14 | Có | Khoa |
| A15 | Có | Khoa |
| C1 | Ghi nhận, giữ phạm vi; mốc đo 4 tuần nhớ trường hợp Hà không mở app; vẫn phải hỏi Hà | Thảo |
| C2 | **(b)**, vì (a) (c) không còn: spec này mở rộng sang sao lưu. File `version: 2` có `dueDate` không bắt buộc; file `version: 1` vẫn nhập được, `version: 1` có `dueDate` vẫn bị từ chối; `dueDate` hỏng trong file nhập thì **từ chối cả file** (khác A14: file nhập là đầu vào không tin được). Khoa sửa `policy-security` S1 (owner). Thêm tiêu chí: sao lưu rồi nhập lại còn hạn chót; file `version: 1` cũ vẫn nhập được. Khoa: **làm thành PR riêng sau PR hạn chót** | Thảo · Khoa |
| C3 | **(a)**: F3 của spec sao lưu đã ra bản; sửa chữ trong spec (bỏ "lưu lỗi vẫn im lặng"), thêm một tiêu chí: đặt hạn chót lúc lưu lỗi thì có báo | Thảo · Linh |

## Vòng hai: câu hỏi của plan (`runs/B6p-*`)

| Dòng | Trả lời | Ai |
|---|---|---|
| Q1 | Large | Khoa |
| Q2 | File mới `app/due.js` | Khoa |
| Q3 | Lưu ở `change`, vẽ lại ở `blur`; **sửa:** `change` chỉ lưu khi giá trị hợp lệ, `''` xử lý lúc `blur` (so với giá trị trước khi focus), để Backspace giữa lúc gõ không xoá hạn chót đã lưu. Thêm test | Khoa · Linh |
| Q4 | Có Hoàn tác cả ba trường hợp | Linh |
| Q5 | **Có câu "Đã hoàn tác."** khi lưu được (khác đề xuất của plan); dùng chung với PR 2 | Linh |
| Q6 | Thứ tự trong mảng `todos`; xếp chỉ đổi thứ tự hiện | Khoa |
| Q7 | Một cơ chế Undo; Khoa muốn PR 2 merge trước. **PR 2 đang chờ plan (Medium, `review/2/watch.md`), nên người chạy demo để PR 2 chờ: PR A đi trước, tự làm Undo, PR 2 rebase sau** | Khoa · người chạy demo |
| A16 | D5 "Đã bỏ hạn chót của việc {tiêu đề}." · D6 "Hoàn tác" · nút mất sau 10 giây hoặc khi thêm, đánh dấu, xoá, đổi hạn chót, nhập file | Linh |
| A17 | Có: PR A chỉ lên `dev`/`staging`; `production` chờ PR B | Thảo · Khoa |
| A18 | Có, luôn ghi `version: 2` | Khoa |
| A19 | Không cần duyệt lại | Mai |
| C4 | (a) `pick` chỉ chép `dueDate` hợp lệ | Khoa · Linh |
| Duyệt plan | **Có với điều kiện** (Q3 sửa + test; A16 trước PR A; ghi C4 = (a)) | Khoa |
