# Intent: Khách không mất việc khi đổi máy hoặc xoá dữ liệu trình duyệt

Author: Lan (nhân viên chăm sóc khách hàng) · Status: accepted · Source: email của khách, do Lan đọc · Date: 2026-10-19

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

Lần này (product owner chốt): khách tự sao lưu danh sách ra một file và nhập lại được; khách được báo khi việc không lưu được vì bộ nhớ
đầy. Đồng bộ hai máy để một intent sau.

## Success criteria
- Khách đổi sang điện thoại mới vẫn thấy đủ các việc đã có trước đó.
- Khách xoá dữ liệu trình duyệt xong vẫn thấy đủ các việc đã có trước đó.
- Khách thêm, đánh dấu xong hoặc xoá một việc trên máy này thì máy kia cũng thấy đúng như vậy.
- Email than mất việc giảm từ 23 email / 2 tuần xuống dưới 5 email / 2 tuần, trong 6 tuần sau khi ra bản mới [product owner]
- Không còn lần lưu lỗi nào mà khách không được báo [product owner]

## Affected users and systems
- Người dùng: khách mất việc khi đổi điện thoại hoặc xoá dữ liệu trình duyệt, và khách dùng nhiều máy. Chưa biết tổng số người dùng.
- Hệ thống: phần lưu dữ liệu của app (`app/store.js`). Mỗi việc gồm id, tiêu đề, trạng thái xong và thời điểm tạo (`app/app.js`).

## Constraints
- Hiện tại app không có tài khoản và không có server [app/store.js]
- Có giữ việc không cần tài khoản hay không, và khách có chịu đăng nhập không, là chuyện product owner quyết [originator]
- Một bạn dev có gợi ý "chắc phải làm tài khoản đăng nhập". Đây chỉ là gợi ý, chưa phải quyết định [originator]
- Bộ nhớ `localStorage` có giới hạn, khoảng 5 MB ở đa số trình duyệt. Khi ghi lỗi, app chỉ ghi ra console, khách không được báo [app/store.js]

## Out of scope
- Lấy lại việc đã mất cho 23 khách đã email: dữ liệu chưa từng rời máy họ [product owner]
- Đồng bộ nhiều máy, tài khoản đăng nhập, nhiều người dùng chung danh sách [product owner]
- Hạn chót cho việc: intent riêng T-012 [product owner]

## Impact
Cao [product owner]: 23 email trong 14 ngày, 3 khách nói sẽ bỏ app. Khoảng 1.200 người dùng mỗi tuần [product owner].
Nguồn lực: một lập trình viên, hai tuần [product owner].

## Open questions
Product owner đã trả lời 2026-10-20 (phạm vi, tài khoản, riêng tư, mốc thành công, số người dùng, nguồn lực: xem các mục trên).
Còn lại:
- Chép 23 email (đã bỏ thông tin cá nhân) vào `tickets/` để người duyệt kiểm được con số không? → Lan
- Trong 23 email, bao nhiêu email là do đổi điện thoại, bao nhiêu là do xoá dữ liệu trình duyệt? → Lan (đếm lại email)
