# Intent: Khách doanh nghiệp muốn tự giữ một bản sao lưu danh sách việc

Author: Minh (nhân viên kinh doanh) · Status: draft · Source: câu hỏi của 2 khách doanh nghiệp trong 2 buổi demo, do Minh kể · Date: 2026-10-19

## Problem
Khách doanh nghiệp sợ mất danh sách việc trong app. Trong buổi demo, họ hỏi app có sao lưu được không và muốn giữ một bản ở chỗ của
họ. Hiện tại app không có cách nào để họ lấy danh sách việc ra và tự giữ.

## Evidence
- Tuần trước (tính từ 19/10/2026), 2 khách doanh nghiệp hỏi app có sao lưu danh sách việc được không, trong 2 buổi demo [originator]
- Hai khách này nói họ sợ mất dữ liệu và muốn giữ một bản ở chỗ của họ [originator]
- App chỉ lưu việc trong `localStorage` của trình duyệt đang dùng: không có server, không có tài khoản, không đồng bộ. Xoá dữ liệu
  trang, đổi trình duyệt hoặc đổi máy là bắt đầu lại với danh sách trống [app/store.js]
- Giao diện chỉ có ô thêm việc, ba bộ lọc (Tất cả / Chưa xong / Đã xong) và danh sách. Không có nút hay chức năng nào để lấy danh
  sách việc ra khỏi app [app/index.html, app/app.js]

## Desired outcome
Khách doanh nghiệp không còn sợ mất danh sách việc, và tự giữ được một bản danh sách việc ở chỗ của họ.

## Success criteria

## Affected users and systems
- Người dùng: khách doanh nghiệp. Đã biết có 2 khách hỏi. Chưa biết họ đã mua hay đang dùng app chưa, và tổng số khách doanh nghiệp.
- Hệ thống: phần lưu dữ liệu của app (`app/store.js`). Mỗi việc gồm id, tiêu đề, trạng thái xong và thời điểm tạo (`app/app.js`).
- Liên quan: `intent/2026-10-19-khach-khong-mat-viec.md` (Lan, draft) cũng nói về khách mất việc vì app chỉ lưu trong trình duyệt.
  Phần khác: intent đó nhắm tới việc app không làm mất việc và đồng bộ giữa hai máy. Intent này nhắm tới việc khách tự giữ một bản ở
  chỗ của họ.

## Constraints
- Hiện tại app không có tài khoản và không có server [app/store.js]
- Originator gợi ý "có cách sao lưu". Đây là gợi ý, chưa phải quyết định [originator]

## Out of scope

## Impact
Chưa đánh giá: Minh không nêu mức. Dữ kiện đang có: 2 khách doanh nghiệp hỏi trong 2 buổi demo, chưa biết có ảnh hưởng tới việc họ
mua hay không. Product owner chọn mức.

## Open questions
- Hai khách này đã mua hay đang dùng app chưa? Họ có ra quyết định mua hoặc tiếp tục dùng tùy vào chuyện sao lưu không? → Minh hỏi lại
  hai khách
- "Giữ một bản ở chỗ của họ" là ở đâu (máy của nhân viên, ổ chung hoặc server công ty, nơi khác)? → hai khách, qua Minh
- Ngoài chuyện sợ mất, họ cần bản sao lưu để làm gì khác không (ví dụ lưu trữ, kiểm tra nội bộ, chuyển sang công cụ khác)? → hai khách,
  qua Minh
- Thế nào là xong và đạt yêu cầu? Mốc thành công kiểm được là gì? → product owner, sau khi Minh hỏi lại hai khách
- Những gì nằm ngoài phạm vi? Ví dụ: đồng bộ giữa hai máy (đã có trong intent của Lan), lấy lại việc đã mất, hạn chót cho việc
  (T-012). → product owner
- Nên giữ intent này riêng hay gộp với `intent/2026-10-19-khach-khong-mat-viec.md`? → product owner (cần báo cho Lan biết)
- Có bao nhiêu khách doanh nghiệp đang dùng app? Repo không có số này. → product owner hoặc nhóm kinh doanh
- Để khách tự giữ bản danh sách việc ở chỗ của họ thì có vấn đề gì về riêng tư hoặc pháp lý không? → product owner
- Hạn chót và ngân sách cho việc này? → product owner
- Mức ảnh hưởng (thấp / vừa / cao)? → product owner
