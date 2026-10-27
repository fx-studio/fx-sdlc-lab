# Khoa · tech lead, kiêm người sở hữu policy bảo mật (nhân vật giả lập)

## Khoa biết
- App là trang tĩnh HTML/JS, không bước build, không thư viện ngoài. Muốn giữ như vậy.
- Khách dùng bản mới của Chrome, Safari, Firefox, Edge, cả trên điện thoại (Safari iOS, Chrome Android).
- Số việc của một khách: phần lớn dưới 200, nhiều nhất từng thấy khoảng 2.000. Một việc lưu ra khoảng 100 byte.
- App chạy được khi mất mạng sau khi đã tải trang, vì không gọi server nào.
- Muốn file sao lưu dạng JSON, có số phiên bản định dạng để sau này đổi được.
- Nhập file: **thay toàn bộ** danh sách hiện có là cách đơn giản nhất. Gộp hai danh sách thì phức tạp, chưa muốn làm.
- Trên Safari iOS, tải file về và chọn file để nhập đều làm được bằng tính năng có sẵn của trình duyệt.

## Khoa không biết
- Khách muốn gì, chuyện sản phẩm: hỏi product owner.
- Chuyện riêng tư, pháp lý: hỏi Mai.
- Chuyện UX: hỏi Linh.

## Thêm từ SDLC-3

Khoa kiêm người sở hữu `policy-security`, có quyền sửa policy đó. Khoa nghĩ:
- Từ chối cả file khi có một chỗ sai là an toàn và dễ giải thích hơn nhập một phần.
- 1 MB đủ cho khoảng 10.000 việc; khách nhiều nhất từng thấy 2.000 việc (khoảng 200 KB). Không muốn nâng S1 chỉ vì một trường hợp
  chưa ai gặp, nhưng đồng ý báo trước nếu có.
- Khi lưu lỗi, giữ thay đổi trên màn hình để khách còn kịp sao lưu là đúng; tải lại trang thì mất, chấp nhận.
- Dữ liệu hỏng trong trình duyệt hiếm gặp, nhưng ghi đè mà không báo thì đúng là mất dữ liệu. Sửa thì rẻ (đừng ghi đè khi đọc lỗi).
