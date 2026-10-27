# B0g-khoa-gia-dinh-moi

Chạy 2026-10-27 09:20 ở `persona-empty` (thư mục riêng của lượt này), chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Bạn là Khoa. Spec sao lưu đã cập nhật theo câu trả lời của mọi người. Khi thiết kế phần C3 (dữ liệu trong trình duyệt đọc lỗi), spec mọc thêm bốn giả định mới. Đây là đoạn thiết kế và bốn dòng đó:

### F5 · Danh sách đã lưu không đọc được
1. Khi mở app, nếu đọc danh sách trong bộ nhớ trình duyệt bị lỗi, app **không ghi đè** dữ liệu đó và báo cho khách trên cùng màn hình
   [answer C3, Thảo · Khoa] [policy-ux@2#U1]. Hiện nay `store.load` trả về danh sách trống và lần lưu sau ghi đè dữ liệu hỏng mà không
   báo [app/store.js].
2. App không sửa, không khôi phục, không chép dữ liệu hỏng sang chỗ khác [answer C3, Thảo · Khoa].
3. Thế nào là "đọc lỗi": xem Assumptions (A13). Thêm, đánh dấu xong, xoá trong lúc đó: xem A14. Nhập từ file trong lúc đó: xem A15.
   Lời báo: xem A16.

- A13. "Đọc lỗi" là: khoá `todo.v1` có dữ liệu nhưng không đọc được, hoặc đọc được mà không phải một mảng; còn chưa có khoá `todo.v1`
  là danh sách trống bình thường, không báo lỗi, đúng không? → Khoa (tech lead)
- A14. Khi đọc lỗi, app không ghi gì vào `todo.v1` cho tới khi trang được mở lại: việc khách thêm, đánh dấu xong hay xoá vẫn hiện trên
  màn hình nhưng không được lưu (như A9), và app nhắc lại lời báo ở F5, đúng không? → Khoa (tech lead), Linh (UX owner)
- A15. Khi đọc lỗi, khách vẫn nhập được từ file, và đó là cách duy nhất thay dữ liệu hỏng; vì không đếm được số việc sẽ mất, lời xác
  nhận theo S2 là "Thay danh sách đã lưu không đọc được bằng 30 việc trong file?", đúng không? → Khoa (security owner), Thảo (product
  owner)
- A16. Lời báo ở F5 là "Không đọc được danh sách đã lưu trên trình duyệt này. App sẽ không ghi đè lên nó. Nếu có file sao lưu, hãy bấm
  "Nhập từ file".", đúng không? → Linh (UX owner)

Trả lời TỪNG dòng có tên bạn: mã dòng, 'Có'/'Không'/'Không biết', một câu lý do (nếu 'Không' thì nói cách bạn muốn). Dòng không có tên bạn thì bỏ qua.

## Tool call (0)

(không có)

## Claude · 11 s

**A13.** Có. Chưa có khoá `todo.v1` là danh sách trống bình thường. Nếu bản thân việc truy cập bộ nhớ trình duyệt bị lỗi (ném ngoại lệ) thì cũng tính là "đọc lỗi", để app không ghi đè.

**A14.** Có. Giữ thay đổi trên màn hình để khách kịp sao lưu, tải lại trang thì mất, và tôi chấp nhận điều đó. Việc không ghi đè khi đọc lỗi cũng rẻ để làm.

**A15.** Có. Nhập từ file thay toàn bộ là cách đơn giản nhất, và khách đã xác nhận rõ ràng trước khi dữ liệu hỏng bị thay. Việc kiểm tra file (cỡ file, từ chối cả file khi một chỗ sai) vẫn áp dụng như bình thường.
