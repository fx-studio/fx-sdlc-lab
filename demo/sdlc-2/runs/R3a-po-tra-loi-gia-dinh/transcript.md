# R3a-po-tra-loi-gia-dinh

Chạy 2026-10-20 17:07 ở `persona-empty` (thư mục riêng của lượt này). Nguyên văn, không sửa. Luồng thô: `stream.jsonl`.

## Prompt

## Assumptions
- A1. Khách tự chuyển file sao lưu sang máy mới (qua email, Zalo, ổ đĩa…), app không cần giúp bước này, đúng không? → product owner
- A2. File dạng JSON thụt lề (văn bản thường) là đủ "plain and human-readable" theo P3, đúng không? → Mai (privacy owner)
- A3. File chỉ gồm `{ "version": 1, "todos": [ … ] }`; trường `version` và `id` của việc (app tự sinh) không vi phạm P2, đúng không?
  → Mai (privacy owner)
- A4. Khi nhập, file có hai việc trùng `id`, tiêu đề rỗng, hoặc `createdAt` không phải số thì từ chối cả file (không nhập một phần),
  đúng không? → Khoa (tech lead)
- A5. Tên file là `todo-sao-luu-<YYYY-MM-DD>.json`, đúng không? → product owner
- A6. Khi danh sách trống, nút sao lưu vẫn bấm được và báo "chưa có việc nào để sao lưu" thay vì tạo file rỗng, đúng không?
  → product owner
- A7. Nút sao lưu và nút nhập từ file đặt dưới danh sách, cạnh dòng đếm việc, đúng không? → Linh (UX owner)
- A8. Khi không lưu được, lời gợi ý là "sao lưu ra file rồi xoá bớt việc đã xong", đúng không? → Linh (UX owner)
- A9. Thông báo lỗi và kết quả đặt trong một vùng `role="status"` / `aria-live` để trình đọc màn hình đọc lên, và nút nhập dùng
  `<input type="file">` có nhãn, đúng không? → Linh (UX owner)
- A10. Đuôi `.json` hiện trong tên file do hệ điều hành hiển thị, không tính là chữ trong app theo U4, đúng không? → Linh (UX owner)
- A11. Khi không lưu được, việc vừa thêm/sửa vẫn hiện trên màn hình (chưa lưu) cho tới lần lưu thành công sau, đúng không?
  → Khoa (tech lead)
- A12. File sao lưu không tính là "changes the shape of stored data" (risk-list dòng 2), vì bộ nhớ trình duyệt không đổi, đúng không?
  → Khoa (tech lead)

## Tool call (0)

(không có)

## Claude · 7 s

Mình là Thảo, product owner, không đọc code. Hồ sơ không nói gì về từng dòng này, nên mình chỉ trả lời được những gì hồ sơ có.

- A1. Không biết. Hồ sơ chỉ nói file sao lưu nằm trên máy khách và khách tự giữ. Không có gì về cách chuyển sang máy mới.
- A2. Không phải việc của mình: hỏi Mai (privacy owner). Mình chỉ biết là theo policy riêng tư hiện có thì được.
- A3. Không phải việc của mình: hỏi Mai (privacy owner).
- A4. Không phải việc của mình: hỏi Khoa (tech lead). Đây là chuyện kỹ thuật.
- A5. Không biết. Hồ sơ không có gì về tên file. Định dạng file thì mình chuyển tech lead.
- A6. Không biết. Hồ sơ không nói gì về trường hợp danh sách trống.
- A7. Không phải việc của mình: hỏi Linh (UX owner).
- A8. Không phải việc của mình: hỏi Linh (UX owner).
- A9. Không phải việc của mình: hỏi Linh (UX owner). Phần `aria-live` và `<input type="file">` cũng là chuyện kỹ thuật, nên chuyển tech lead.
- A10. Không phải việc của mình: hỏi Linh (UX owner).
- A11. Không phải việc của mình: hỏi Khoa (tech lead).
- A12. Không phải việc của mình: hỏi Khoa (tech lead).
