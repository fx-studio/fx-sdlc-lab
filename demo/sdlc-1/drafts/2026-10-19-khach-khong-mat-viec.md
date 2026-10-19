# Intent: Khách không mất việc khi đổi máy hoặc xoá dữ liệu trình duyệt

Author: Lan (nhân viên chăm sóc khách hàng) · Status: draft · Source: email của khách, do Lan đọc · Date: 2026-10-19

## Problem
Khách mất hết danh sách việc trong app. Phần lớn bị mất sau khi đổi sang điện thoại mới hoặc sau khi xoá dữ liệu trình duyệt.
Khách dùng cả laptop lẫn điện thoại thì thêm việc ở máy này nhưng máy kia không thấy.

## Evidence
- Từ 1/10 đến 14/10 có 23 email than mất hết danh sách việc. Lan đã đọc hết [originator]
- 3 khách nói sẽ bỏ app nếu còn mất việc [originator]
- Phần lớn email kể là mất sau khi đổi điện thoại mới hoặc sau khi xoá dữ liệu trình duyệt. Chưa đếm riêng từng loại [originator]
- 5 email nói dùng cả laptop lẫn điện thoại, thêm việc ở máy này thì máy kia không thấy [originator]
- App chỉ lưu việc trong `localStorage` của trình duyệt đang dùng: không có server, không có tài khoản, không đồng bộ. Xoá dữ liệu
  trang, đổi trình duyệt hoặc đổi máy là bắt đầu lại với danh sách trống [app/store.js]

## Desired outcome
Khách không mất việc nữa. Ai dùng hai máy thì thấy cùng một danh sách trên cả hai máy.

## Success criteria
- Khách đổi sang điện thoại mới vẫn thấy đủ các việc đã có trước đó.
- Khách xoá dữ liệu trình duyệt xong vẫn thấy đủ các việc đã có trước đó.
- Khách thêm, đánh dấu xong hoặc xoá một việc trên máy này thì máy kia cũng thấy đúng như vậy.
- Mốc đo bằng số (ví dụ số email than mất việc mỗi tuần) chưa được đặt ra. Xem Open questions.

## Affected users and systems
- Người dùng: khách mất việc khi đổi điện thoại hoặc xoá dữ liệu trình duyệt, và khách dùng nhiều máy. Chưa biết tổng số người dùng.
- Hệ thống: phần lưu dữ liệu của app (`app/store.js`). Mỗi việc gồm id, tiêu đề, trạng thái xong và thời điểm tạo (`app/app.js`).

## Constraints
- Hiện tại app không có tài khoản và không có server [app/store.js]
- Có giữ việc không cần tài khoản hay không, và khách có chịu đăng nhập không, là chuyện product owner quyết [originator]
- Một bạn dev có gợi ý "chắc phải làm tài khoản đăng nhập". Đây chỉ là gợi ý, chưa phải quyết định [originator]
- Bộ nhớ `localStorage` có giới hạn, khoảng 5 MB ở đa số trình duyệt. Khi ghi lỗi, app chỉ ghi ra console, khách không được báo [app/store.js]

## Out of scope

## Impact
Chưa đánh giá: Lan không nêu mức. Dữ kiện đang có: 23 email trong 14 ngày, có 3 khách nói sẽ bỏ app. Product owner chọn mức.

## Open questions
- Những mục sau nằm trong hay ngoài phạm vi intent này? (a) lấy lại việc đã mất cho 23 khách đã email; (b) lỗi khi bộ nhớ trình duyệt đầy:
  việc không được lưu mà khách không biết; (c) nhiều người dùng chung một danh sách; (d) hạn chót cho việc (T-012). → product owner
- Có giữ app không cần tài khoản không? Khách có chịu đăng nhập không? → product owner
- Lưu dữ liệu của khách ra ngoài máy của họ thì có vấn đề gì về riêng tư hoặc pháp lý không? → product owner (có thể cần hỏi bên pháp lý)
- Mốc thành công bằng số là gì (ví dụ số email than mất việc giảm về bao nhiêu, trong bao nhiêu tuần)? → product owner
- Tổng số người dùng là bao nhiêu? Repo không có số này. → product owner
- Ngân sách và hạn chót cho việc này? → product owner
- Chép 23 email (đã bỏ thông tin cá nhân) vào `tickets/` để người duyệt kiểm được con số không? → Lan
- Trong 23 email, bao nhiêu email là do đổi điện thoại, bao nhiêu là do xoá dữ liệu trình duyệt? → Lan (đếm lại email)
