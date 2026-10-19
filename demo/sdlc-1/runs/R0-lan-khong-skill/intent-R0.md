# Intent: Khách không bị mất việc trong app

## Vấn đề

Dạo gần đây khách liên tục email phàn nàn là **mất hết việc (task) trong app**, nhiều nhất là **sau khi đổi điện thoại**. Có vẻ dữ liệu chỉ nằm trên máy, nên khi đổi máy, cài lại app hay xoá dữ liệu app thì việc của khách cũng mất theo.

Với một app quản lý việc, mất dữ liệu là lỗi nặng nhất: khách mất lòng tin, không dám nhập việc quan trọng vào app nữa, rồi bỏ app.

## Mục tiêu

Việc khách đã tạo **không bị mất**, kể cả khi:

- đổi sang điện thoại mới (cùng hệ điều hành hoặc khác hệ điều hành),
- gỡ rồi cài lại app,
- mất hoặc hỏng điện thoại.

Lấy lại việc phải **dễ**: khách không cần biết kỹ thuật, cũng không cần nhớ đã làm gì trước đó.

## Không nằm trong phạm vi (lần này)

- Cộng tác hoặc chia sẻ việc giữa nhiều người.
- Bản web hay bản desktop.
- Đồng bộ thời gian thực giữa nhiều máy dùng cùng lúc. Có thì tốt, nhưng không bắt buộc.

## Tiêu chí thành công

- Khách đổi máy, đăng nhập hoặc khôi phục, rồi thấy lại **đủ** việc cũ (cả việc đã xong lẫn chưa xong, ghi chú và hạn chót).
- Số email than mất dữ liệu giảm về gần 0 sau khi ra bản mới.
- Khách đang dùng app **không bị mất dữ liệu trong lúc chuyển** sang cơ chế mới.

## Ràng buộc và lưu ý

- **Quyền riêng tư:** việc của khách có thể chứa thông tin cá nhân. Nếu đưa dữ liệu lên server thì phải nói rõ với khách, và có cách để khách xoá dữ liệu của mình.
- **Không ép khách:** người không muốn tạo tài khoản vẫn dùng được app như hiện nay.
- **Vẫn dùng được khi không có mạng.**

## Câu hỏi còn mở

1. Hiện app lưu dữ liệu ở đâu và bằng cách nào (chỉ trên máy? có backup của hệ điều hành không)?
2. Khách chủ yếu dùng iOS, Android hay cả hai? Có nhiều người đổi máy sang hệ điều hành khác không?
3. Chọn hướng nào: tài khoản kèm đồng bộ lên cloud, dựa vào backup của iCloud/Google, hay cho xuất/nhập file thủ công? Mỗi hướng tốn công và chi phí vận hành khác nhau.
4. Những khách **đã** mất việc rồi thì có cứu được không, hay chỉ có thể ngăn chuyện này xảy ra từ giờ?
5. Có cần đo trước xem bao nhiêu khách bị ảnh hưởng (số email, đánh giá trên store) để quyết định mức ưu tiên không?
