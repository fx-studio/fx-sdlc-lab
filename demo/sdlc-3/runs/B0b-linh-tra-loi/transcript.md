# B0b-linh-tra-loi

Chạy 2026-10-27 09:14 ở `persona-empty` (thư mục riêng của lượt này), chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Bạn là Linh. Đây là mục Giả định và mục Chỗ đáng lo của bản spec 'Sao lưu ra file, nhập lại, và báo khi không lưu được' (bản nháp). Trả lời TỪNG dòng có tên bạn (hoặc vai của bạn): bắt đầu bằng mã dòng, rồi 'Có', 'Không' hoặc 'Không biết', kèm một câu lý do. Nếu không phải việc của bạn thì nói chuyển cho ai. Với Chỗ đáng lo có tên bạn, nói bạn chọn phương án nào và vì sao, hoặc nói rõ bạn cần ai khác quyết. Chỉ dựa vào những gì bạn biết trong hồ sơ, không bịa.

## Assumptions
- A1. Khách tự chuyển file sao lưu sang máy mới (qua email, Zalo, ổ đĩa…), app không cần giúp bước này, đúng không? → product owner
- A2. "Nhập lại" là thay toàn bộ danh sách hiện có bằng danh sách trong file, không gộp hai danh sách, đúng không? → product owner
- A3. Khi danh sách đang có đúng 1 việc, nhập file được tính là thao tác trên một việc theo U2: thay ngay, không hỏi, cho Undo 10 giây,
  đúng không? (Nếu không, app hỏi xác nhận như F2 bước 6.) → Linh (UX owner), Khoa (security owner)
- A4. File dạng JSON thụt lề (văn bản thường) là đủ "plain and human-readable" theo P3, đúng không? → Mai (privacy owner)
- A5. File chỉ gồm `{ "version": 1, "todos": [ … ] }`; trường `version` và `id` của việc (app tự sinh) không vi phạm P2, đúng không?
  → Mai (privacy owner)
- A6. Khi danh sách trống, nút sao lưu vẫn bấm được và báo "Chưa có việc nào để sao lưu" thay vì tạo file rỗng, đúng không?
  → product owner
- A7. Khi nhập, file có hai việc trùng `id`, tiêu đề rỗng, hoặc `createdAt` không phải số thì từ chối cả file (không nhập một phần),
  đúng không? → Khoa (tech lead)
- A8. Khi không lưu được, lời gợi ý là "Hãy sao lưu ra file, rồi xoá bớt việc đã xong", đúng không? → Linh (UX owner)
- A9. Khi không lưu được, thay đổi vừa làm vẫn hiện trên màn hình (chưa lưu) cho tới lần lưu thành công sau, đúng không?
  → Khoa (tech lead)
- A10. Thông báo đặt trong một vùng `role="status"` / `aria-live` để trình đọc màn hình đọc lên; nút nhập dùng `<input type="file">`
  có nhãn; hộp xác nhận dùng `<dialog>` có sẵn của trình duyệt, đúng không? → Linh (UX owner)
- A11. Đuôi `.json` trong tên file do hệ điều hành hiển thị, không tính là chữ trong app theo U4; tên file là
  `todo-sao-luu-<YYYY-MM-DD>.json`, đúng không? → Linh (UX owner), product owner
- A12. File sao lưu không tính là "changes the shape of stored data" (risk-list dòng 2), vì bộ nhớ trình duyệt không đổi, đúng không?
  → Khoa (tech lead)

## Concerns
- **C1 · Tiêu chí thành công của intent không khớp phạm vi.** Intent ghi "máy này thêm, đánh dấu xong hoặc xoá thì máy kia cũng thấy"
  [intent], nhưng đồng bộ nhiều máy nằm ngoài phạm vi [intent]. Hai tiêu chí "đổi điện thoại mới / xoá dữ liệu trình duyệt vẫn thấy đủ
  việc" [intent] chỉ đạt khi khách đã sao lưu trước đó. Spec này không đạt tiêu chí thứ ba, và chỉ đạt hai tiêu chí đầu có điều kiện.
  → product owner (sửa tiêu chí trong intent, hoặc chấp nhận).
- **C2 · Giới hạn 1 MB khi nhập nhỏ hơn bộ nhớ trình duyệt.** `policy-security@1#S1` (owner Khoa) giới hạn file nhập 1 MB, còn bộ nhớ
  trình duyệt khoảng 5 MB [app/store.js]. Khách có danh sách lớn sẽ sao lưu được nhưng không nhập lại được, tức là mất việc mà không
  được báo lúc sao lưu, trái `policy-ux@2#U1` (owner Linh). Spec không chọn. Phương án:
  - (a) Khi sao lưu mà file > 1 MB thì vẫn tạo file nhưng báo ngay rằng file này sẽ không nhập lại được. Tốn ít công; khách vẫn không
    có bản sao lưu dùng được.
  - (b) Khoa nâng giới hạn của S1 lên ít nhất bằng bộ nhớ trình duyệt. Cần sửa policy-security.
  → Khoa (security owner), Linh (UX owner).
- **C3 · Dữ liệu hỏng bị ghi đè không báo.** `store.load` trả về danh sách trống khi đọc lỗi; lần lưu sau sẽ ghi đè dữ liệu hỏng
  [app/store.js]. Đây là mất dữ liệu không báo theo `policy-ux@2#U1`, nhưng intent chỉ nói tới lỗi khi lưu [intent], nên spec không
  thiết kế phần này. Có đưa vào phạm vi lần này không? → product owner, Khoa (tech lead).
- **C4 · Thao tác trên một việc chưa có Undo 10 giây.** `policy-ux@2#U2` yêu cầu thao tác trên một việc làm ngay và cho Undo 10 giây.
  Nút xoá một việc hiện xoá ngay, không có Undo [app/app.js]. Intent không yêu cầu đổi nút này [intent], nên spec để ngoài phạm vi.
  Có đưa vào lần này, hay để một intent riêng? → product owner, Linh (UX owner).

## Tool call (0)

(không có)

## Claude · 124 s

**A3.** Có, về phía UX. Theo U2, nhập khi đang có đúng 1 việc là thao tác trên một việc, nên thay ngay và cho Undo 10 giây. Chỉ "từ hai việc trở lên" mới phải hỏi. Phần bảo mật (S2) là của Khoa. Khoa cần xác nhận S2 chấp nhận cách tính này, và Undo có khôi phục được danh sách cũ không.

**A8.** Có. Câu ngắn, tiếng Việt, nói rõ việc cần làm và đúng thứ tự (sao lưu trước, xoá sau). Nếu nút trên app đã dùng chữ "file" thì giữ nguyên, để cả app dùng một cách gọi.

**A10.** Có. Tôi muốn dùng thành phần có sẵn của trình duyệt vì chúng dùng được bằng bàn phím và trình đọc màn hình. Vùng `role="status"`, `<input type="file">` có nhãn và `<dialog>` đều hợp ý đó.

**A11.** Có. Đuôi `.json` do hệ điều hành hiển thị nên không tính là chữ trong app. Tôi muốn tên file có ngày để khách biết bản nào mới, và `todo-sao-luu-<YYYY-MM-DD>.json` đáp ứng điều đó. Product owner xác nhận phần còn lại, gồm cả chữ "todo" trong tên file có hợp với tên app không.

**C2.** Tôi thiên về (b), vì khách cần một bản sao lưu dùng được. (a) chỉ báo cho khách biết file không nhập lại được, nên U1 được giữ nhưng khách vẫn không có bản sao lưu. Tuy vậy S1 là policy bảo mật của Khoa. Tôi không biết vì sao giới hạn là 1 MB, nên Khoa phải quyết có nâng được không. Nếu Khoa không nâng thì lấy (a) làm mức tối thiểu. Câu báo phải ngắn, không từ kỹ thuật, ví dụ: "File này lớn quá nên sau này không nhập lại được." Câu này đặt ngay lúc sao lưu, không đợi tới lúc nhập.

**C4.** Nút xoá một việc không có Undo là đang lệch U2 của tôi. Tôi chọn để một intent riêng, vì intent này nói về sao lưu và nhập lại, trộn thêm sẽ khó kiểm. Điều kiện là spec ghi rõ chỗ lệch U2 này còn mở và có người nhận việc. Product owner quyết lịch.

**Các dòng còn lại không có tên tôi:**
- A1, A2, A6 và C1 chuyển product owner.
- A4 và A5 chuyển Mai.
- A7, A9, A12 chuyển Khoa.
- C3 chuyển product owner và Khoa.
