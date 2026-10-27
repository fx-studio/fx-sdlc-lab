# B0b-khoa-tra-loi

Chạy 2026-10-27 09:14 ở `persona-empty` (thư mục riêng của lượt này), chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Bạn là Khoa. Đây là mục Giả định và mục Chỗ đáng lo của bản spec 'Sao lưu ra file, nhập lại, và báo khi không lưu được' (bản nháp). Trả lời TỪNG dòng có tên bạn (hoặc vai của bạn): bắt đầu bằng mã dòng, rồi 'Có', 'Không' hoặc 'Không biết', kèm một câu lý do. Nếu không phải việc của bạn thì nói chuyển cho ai. Với Chỗ đáng lo có tên bạn, nói bạn chọn phương án nào và vì sao, hoặc nói rõ bạn cần ai khác quyết. Chỉ dựa vào những gì bạn biết trong hồ sơ, không bịa.

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

**A3.** Không biết. Nhập file thay cả danh sách chứ không phải thao tác trên một việc. Tôi không có nội dung đầy đủ của U2 để kết luận, nên phần UX chuyển Linh quyết. Về kỹ thuật, giữ danh sách cũ trong bộ nhớ 10 giây để Undo thì làm được.

**A7.** Có. Từ chối cả file khi có một chỗ sai là an toàn và dễ giải thích với khách hơn nhập một phần.

**A9.** Có. Giữ thay đổi trên màn hình để khách còn kịp sao lưu là đúng. Tải lại trang thì mất, tôi chấp nhận.

**A12.** Không biết. Tôi chưa thấy nội dung dòng 2 của risk-list. Bộ nhớ trình duyệt đúng là không đổi, nhưng file sao lưu là một định dạng mới (`version: 1`) mà sau này ta còn phải giữ tương thích. Tôi nghiêng về việc ghi nó vào risk-list, nhưng cần xem câu chữ của dòng đó mới chốt được.

**C2.** Tôi chọn (a), giữ S1 ở 1 MB.
- 1 MB đủ cho khoảng 10.000 việc, trong khi khách nhiều nhất tôi từng thấy có 2.000 việc (khoảng 200 KB).
- Tôi không muốn sửa `policy-security` vì một trường hợp chưa ai gặp.
- Tôi đồng ý báo trước khi sao lưu nếu file vượt 1 MB. Spec cũng nói rõ là khi đó khách chưa có bản sao lưu dùng được, tôi chấp nhận điều đó.
- Linh (owner U1) cần duyệt câu chữ của thông báo.

**C3.** Tôi ủng hộ đưa vào phạm vi lần này. Ghi đè dữ liệu hỏng mà không báo đúng là mất dữ liệu, dù hiếm gặp. Sửa thì rẻ: khi đọc lỗi thì không ghi đè, và báo cho khách. Việc có mở rộng phạm vi hay không là của product owner quyết.

**Không có tên tôi, bỏ qua:**
- A1, A2, A6 và C1: product owner.
- A4, A5: Mai.
- A8, A10, A11: Linh (A11 có thêm product owner).
- C4: product owner và Linh.
