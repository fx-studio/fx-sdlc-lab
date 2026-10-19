# Intent: Người dùng không quên những việc có hạn chót

Author: Hà (người dùng) · Status: draft · Source: ticket T-012 (`tickets/T-012-due-dates.md`) và trả lời của Hà · Date: 2026-10-19

## Problem
Hà dùng app mỗi ngày trên laptop ở chỗ làm và hay quên những việc có deadline. Hà không đặt được hạn chót cho từng việc, nên nhìn
danh sách thì không biết việc nào tới hạn trước, và cũng không được nhắc khi một việc sắp tới hạn.

## Evidence
- Ticket T-012 gửi qua form góp ý ngày 12/10/2026: "Cho mình đặt hạn chót cho từng việc, và nhắc khi gần tới hạn. Mình hay quên mấy
  việc có deadline." [tickets/T-012-due-dates.md]
- Ticket có 14 lượt +1 [tickets/T-012-due-dates.md]
- Tuần trước (tính từ 19/10/2026), Hà quên nộp một báo cáo vì không nhớ hạn. Hà không nhớ việc đó có nằm trong app không, và hôm đó
  có mở app không [originator]
- Hiện một việc chỉ có id, tiêu đề, trạng thái xong và thời điểm tạo. Không có hạn chót [app/app.js]

## Desired outcome
Hà không quên những việc có deadline. Nhìn danh sách là biết ngay việc nào tới hạn trước.

## Success criteria
- Một việc đã đặt hạn chót thì nhìn danh sách là thấy hạn chót của việc đó.
- Nhìn danh sách là biết việc nào tới hạn trước.
- Mốc đo bằng số (ví dụ số việc bị trễ hạn) chưa được đặt ra, Hà không có con số nào. Xem Open questions.

## Affected users and systems
- Người dùng: Hà, dùng app mỗi ngày trên laptop ở chỗ làm. Có 14 người +1 ticket, chưa biết họ là ai và cần gì. Chưa biết tổng số
  người dùng.
- Hệ thống: dữ liệu của mỗi việc (`app/app.js`) và phần lưu dữ liệu (`app/store.js`).
- Liên quan: hai intent `2026-10-19-khach-khong-mat-viec.md` (Lan) và `2026-10-19-khach-doanh-nghiep-sao-luu.md` (Minh) có hỏi T-012
  nằm trong hay ngoài phạm vi của họ. Hai intent đó nói về chuyện mất danh sách việc, không trùng với intent này.

## Constraints
- App chỉ lưu dữ liệu trong trình duyệt đang dùng, không có server, không có tài khoản [app/store.js]
- Hà gợi ý hiện hạn chót ngay trong danh sách và xếp việc theo hạn chót. Đây là gợi ý, chưa phải quyết định [originator]
- Ticket xin "nhắc khi gần tới hạn". Hà không biết nên nhắc bằng cách nào, chỉ muốn "đừng để quên" [tickets/T-012-due-dates.md, originator]

## Out of scope

## Impact
Chưa đánh giá: Hà không nêu mức. Dữ kiện đang có: 14 lượt +1 cho ticket, một lần Hà quên nộp báo cáo. Product owner chọn mức.

## Open questions
- Những mục sau nằm trong hay ngoài phạm vi? (a) nhắc trên điện thoại; (b) việc lặp lại hằng tuần; (c) chia sẻ hạn chót cho đồng
  nghiệp. Hà không biết. → product owner
- Nhắc theo cách nào: chỉ thấy khi mở app, hay cả khi không mở app? → product owner
- Nhắc trước hạn bao lâu? Hạn chót chỉ cần ngày hay cần cả giờ? Hà chưa nghĩ tới. → product owner (có thể hỏi những người +1 ticket)
- Khi xếp theo hạn chót, việc không có hạn chót nằm ở đâu? → product owner
- Cái báo cáo Hà quên tuần trước có nằm trong app không? Nếu không, hiện hạn chót trong app có giúp được lần đó không? → Hà (xem lại
  danh sách việc trong app trên laptop)
- Quên báo cáo đó gây hậu quả gì? Mỗi tuần Hà có bao nhiêu việc có deadline? → Hà, nếu theo dõi thêm
- 14 người +1 là ai, có cùng nhu cầu với Hà không? → product owner (xem lại form góp ý)
- Mốc thành công bằng số là gì? → product owner
- Tổng số người dùng là bao nhiêu? Repo không có số này. → product owner
- Mức ảnh hưởng, ngân sách và hạn chót cho việc này? → product owner
