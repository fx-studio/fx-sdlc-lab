# B0b-mai-tra-loi

Chạy 2026-10-27 09:12 ở `persona-empty` (thư mục riêng của lượt này), chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Bạn là Mai. Đây là mục Giả định và mục Chỗ đáng lo của bản spec 'Sao lưu ra file, nhập lại, và báo khi không lưu được' (bản nháp). Trả lời TỪNG dòng có tên bạn (hoặc vai của bạn): bắt đầu bằng mã dòng, rồi 'Có', 'Không' hoặc 'Không biết', kèm một câu lý do. Nếu không phải việc của bạn thì nói chuyển cho ai. Với Chỗ đáng lo có tên bạn, nói bạn chọn phương án nào và vì sao, hoặc nói rõ bạn cần ai khác quyết. Chỉ dựa vào những gì bạn biết trong hồ sơ, không bịa.

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

## Claude · 43 s

**A4. Có.** File JSON thụt lề là văn bản thường, mở bằng Notepad đọc được bằng mắt, nên đạt P3.

**A5. Có.** `version` và `id` do app tự sinh, không chứa tên, email hay vị trí. Việc của khách vốn chỉ có tiêu đề, trạng thái xong, thời điểm tạo và mã ngẫu nhiên, nên không thêm dữ liệu không cần và không vi phạm P2.

**A1, A2, A6:** Không phải việc của tôi, chuyển cho product owner (Thảo).

**A3, A8, A10, A11:** Không phải việc của tôi, chuyển cho Linh (UX owner). A3 cần thêm Khoa (security owner), và A11 cần thêm product owner.

**A7, A9, A12:** Không phải việc của tôi, chuyển cho Khoa (tech lead).

**C1, C3, C4:** Không có tên tôi, chuyển cho product owner. C3 cần thêm Khoa (tech lead) và C4 cần thêm Linh (UX owner).

**C2:** Tôi không có tên trong dòng này. Nhưng nếu Khoa chọn (b) và nâng giới hạn của S1, thì đó là thay đổi trên policy-security, không phải policy-privacy của tôi. Chuyện chọn (a) hay (b) cần Khoa và Linh quyết.

Về phía riêng tư, cả hai phương án đều không đụng P1 đến P5, vì file vẫn do khách tự tay tạo và tự mang đi. Nếu app có thêm chỗ lưu nào ngoài trình duyệt để làm việc này thì phải hỏi tôi theo P5.
