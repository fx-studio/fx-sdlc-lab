# R3b-tech-lead-tra-loi-gia-dinh

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

## Claude · 9 s

- A1. Không phải việc của mình: hỏi product owner.
- A2. Không phải việc của mình: hỏi Mai.
- A3. Không phải việc của mình: hỏi Mai.
- A4. Không biết. Hồ sơ không nói gì về cách xử lý file nhập không hợp lệ. Hồ sơ chỉ nói nhập file là thay toàn bộ danh sách hiện có.
- A5. Không phải việc của mình: hỏi product owner.
- A6. Không phải việc của mình: hỏi product owner.
- A7. Không phải việc của mình: hỏi Linh.
- A8. Không phải việc của mình: hỏi Linh.
- A9. Không phải việc của mình: hỏi Linh.
- A10. Không phải việc của mình: hỏi Linh.
- A11. Không biết. Hồ sơ không nói gì về việc hiển thị khi lưu lỗi.
- A12. Không biết. Hồ sơ không nói gì về risk-list hay về việc dữ liệu lưu trong trình duyệt.
