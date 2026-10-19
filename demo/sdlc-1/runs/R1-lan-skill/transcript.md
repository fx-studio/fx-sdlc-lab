# R1-lan-skill

Chạy 2026-10-19 06:31. Nguyên văn, không sửa.

## Người kể (lời mở)

/write-intent Dạo này khách cứ email than là mất hết việc trong app, nhất là sau khi đổi điện thoại. Mình muốn làm gì đó để khách không mất việc nữa.

## Claude (lượt 1) · 23 s

**Kiểm tra trùng:** thư mục `intent/` đang trống, chưa có intent nào nói về chuyện này. Mình làm intent mới.

**Những gì repo đã cho biết** (bạn không cần trả lời lại các điểm này):
- Toàn bộ việc chỉ lưu trong `localStorage` của trình duyệt đang dùng. App không có server, không có tài khoản, không đồng bộ. Code ghi rõ: *"Clearing site data, switching browser or switching device means starting from an empty list."* [`app/store.js:1-2`]. Vậy khách đổi điện thoại thì danh sách mới chắc chắn trống, đúng như thiết kế hiện tại.
- Bộ nhớ này có giới hạn khoảng 5 MB. Nếu ghi bị lỗi, app chỉ ghi vào console, khách không hề biết [`app/store.js:14-18`]. Đây là một kiểu mất việc khác, nhưng chưa rõ có ai gặp chưa.
- Mỗi việc chỉ có: tiêu đề, trạng thái xong/chưa, thời điểm tạo [`app/app.js:1`].
- Trong `tickets/` chỉ có T-012 (xin thêm hạn chót), không có ticket nào về mất dữ liệu. Các email than phiền chưa được lưu trong repo.

**Mình cần bạn trả lời 4 câu (câu quan trọng nhất ở trên):**

1. **Bằng chứng:** Bạn nhận khoảng bao nhiêu email như vậy, trong bao lâu? Bạn chép được 1–2 email vào `tickets/` không, hoặc trích nguyên văn vài câu khách viết?
2. **Phạm vi:** Khách mất việc trong những tình huống nào? Chỉ khi đổi điện thoại, hay cả khi đổi trình duyệt, xoá dữ liệu duyệt web, dùng song song máy tính và điện thoại? Bạn muốn intent này lo tất cả các tình huống đó, hay chỉ tình huống đổi điện thoại?
3. **Ràng buộc:** App hiện không có tài khoản và không có server. Đó có phải điều bạn muốn giữ nguyên (ví dụ để khách không phải đăng ký, hay vì chuyện riêng tư) không, hay có thể thay đổi?
4. **Thành công:** Làm sao bạn biết là đã ổn? Ví dụ: "khách đổi điện thoại vẫn còn đủ việc cũ", hay "số email than mất việc giảm về 0 trong X tuần", hay một tiêu chí khác?

Bạn trả lời được câu nào thì trả lời câu đó. Câu nào chưa biết thì cứ nói chưa biết, mình sẽ ghi vào mục câu hỏi mở và ghi rõ ai trả lời được. Nếu muốn mình viết bản nháp luôn với những gì đang có, bạn chỉ cần nói "viết đi".

## Người kể (lượt 1) · 11 s

1. Từ 1/10 tới 14/10 mình nhận 23 email than mất hết danh sách việc, mình đọc hết rồi. Chép email hay trích nguyên văn thì mình không biết, chưa làm. Có 3 khách nói sẽ bỏ app nếu còn mất việc.

2. Phần lớn mất sau khi đổi điện thoại mới, hoặc sau khi xoá dữ liệu trình duyệt. 5 email nói họ dùng cả laptop lẫn điện thoại, thêm việc ở máy này thì máy kia không thấy. Mình muốn lo cả hai: khách không mất việc, và ai dùng hai máy thì thấy cùng một danh sách.

3. Có giữ không có tài khoản hay không thì mình không biết. Khách có chịu đăng nhập không là chuyện product owner quyết. Mình có nghe một bạn dev nói "chắc phải làm tài khoản đăng nhập", nhưng mình không biết có nên không. Chuyện riêng tư hay pháp lý khi lưu dữ liệu của khách mình cũng không biết.

4. Với mình là ổn khi khách không mất việc nữa, và ai dùng hai máy thì thấy cùng một danh sách. Còn mốc cụ thể như giảm về 0 email trong bao nhiêu tuần thì mình không biết, chưa ai đặt ra.

Mấy chuyện như app lưu dữ liệu thế nào, tổng số người dùng, ngân sách, hạn chót thì mình cũng không biết.

## Claude (lượt 2) · 28 s

Cảm ơn bạn, vậy là đã đủ để viết bản nháp. Những gì bạn chưa biết (có làm tài khoản không, chuyện riêng tư/pháp lý, mốc số liệu, tổng số người dùng, ngân sách, hạn chót) mình sẽ đưa vào **Câu hỏi mở**, mỗi câu ghi rõ ai trả lời được. Mình sẽ không tự điền.

Mình đã ráp bản nháp và chạy checklist trước khi lưu:

| Ô | Kết quả | Ghi chú |
|---|---|---|
| Problem | ✅ | Khách mất việc sau khi đổi điện thoại hoặc xoá dữ liệu trình duyệt. Người dùng hai máy thấy hai danh sách khác nhau. |
| Evidence | ✅ | 23 email từ 1/10 đến 14/10, có 3 khách dọa bỏ app, 5 khách dùng hai máy [originator]. Code chỉ lưu trên một trình duyệt [`app/store.js`]. |
| Out of scope | ❌ | Bạn chưa nói gì nằm ngoài phạm vi, và mình không được tự đoán. |
| Success criteria | ✅ | Kiểm được bằng hành vi: đổi máy vẫn còn việc, xoá dữ liệu trình duyệt vẫn còn việc, hai máy thấy cùng một danh sách. Mốc số liệu ghi vào câu hỏi mở. |
| Open questions | ✅ | |
| Sourced | ⚠️ | Mọi dòng đều ghi nguồn. Nhưng 23 email chưa nằm trong repo, nên người duyệt sẽ không tự kiểm được con số này. Mình sẽ ghi một câu hỏi mở để chép email vào `tickets/`. |

**Còn 3 câu nữa là mình lưu file:**

1. **Ngoài phạm vi:** intent này *không* lo những gì? Mấy thứ dưới đây mình thấy có liên quan, nhưng bạn chưa nói chúng thuộc hay không thuộc intent này. Bạn chọn giúp, hoặc nói "chưa biết":
   - a. Lấy lại việc **đã mất** cho 23 khách đã email
   - b. Lỗi khi bộ nhớ trình duyệt đầy: việc không được lưu mà khách không hay biết [`app/store.js:14-18`]
   - c. Cho **nhiều người** dùng chung một danh sách (khác với một người dùng nhiều máy)
   - d. Hạn chót cho việc (ticket T-012)
2. **Tỷ lệ:** trong 23 email, bạn có đếm được bao nhiêu email là do đổi điện thoại, bao nhiêu là do xoá dữ liệu trình duyệt không? Nếu không đếm được, mình sẽ giữ nguyên chữ "phần lớn" như bạn nói.
3. **Dòng tác giả:** mình ghi tên và vai trò của bạn thế nào? Ví dụ "Lan (hỗ trợ khách hàng)".

Nếu bạn muốn lưu luôn, cứ nói "viết đi". Khi đó mục *Ngoài phạm vi* sẽ để trống, kèm một câu hỏi mở gửi product owner.

## Người kể (lượt 2) · 8 s

Mình trả lời 3 câu:

1. **Ngoài phạm vi:** mình chưa biết. Mình chỉ biết mình muốn khách không mất việc nữa, và ai dùng hai máy thì thấy cùng một danh sách. Về từng mục:
   - a. Lấy lại việc đã mất cho 23 khách: mình không biết, mình chưa nghĩ tới.
   - b. Lỗi khi bộ nhớ đầy: mình không biết. Mình không biết app lưu dữ liệu thế nào, và chưa thấy khách nào nói chuyện này.
   - c. Nhiều người dùng chung một danh sách: mình không biết. Trong email chỉ có chuyện một người dùng nhiều máy.
   - d. Hạn chót cho việc (T-012): mình không biết, mình chưa nói tới chuyện này.

   Bạn cứ để trống mục này và ghi câu hỏi mở gửi product owner.

2. **Tỷ lệ:** mình chưa đếm riêng từng loại. Mình chỉ biết phần lớn là sau khi đổi điện thoại mới hoặc sau khi xoá dữ liệu trình duyệt, và có 5 email nói dùng cả laptop lẫn điện thoại. Bạn cứ giữ chữ "phần lớn".

3. **Dòng tác giả:** "Lan (nhân viên chăm sóc khách hàng)".

Viết đi.

## Claude (lượt 3) · 36 s

Lan ơi, mình đã lưu bản nháp ở **`intent/2026-10-19-khach-khong-mat-viec.md`** (`Status: draft`). Mình chưa commit, và mục *Ngoài phạm vi* để trống như bạn dặn.

**Kết quả checklist cuối:**

| Ô | Kết quả | Ghi chú |
|---|---|---|
| Problem | ✅ | |
| Evidence | ✅ | |
| Out of scope | ❌ | Để trống theo ý bạn. Bốn mục a–d đã chuyển thành câu hỏi gửi product owner. |
| Success criteria | ✅ | Ba tiêu chí kiểm được bằng cách thao tác trên app. Mốc bằng số chưa có, đã ghi vào câu hỏi mở. |
| Open questions | ✅ | 8 câu, câu nào cũng ghi ai trả lời. |
| Sourced | ⚠️ | Dòng nào cũng có nguồn. Nhưng 23 email chưa nằm trong repo, nên người duyệt chưa tự kiểm được con số này. Đã có câu hỏi mở gửi bạn. |

**Mấy chỗ mình xử lý, bạn xem lại giúp:**
- **Mức ảnh hưởng (Impact):** mình không tự chọn thấp, vừa hay cao. Mình chỉ ghi các dữ kiện (23 email trong 14 ngày, 3 khách dọa bỏ app) để product owner chọn.
- **Gợi ý làm tài khoản đăng nhập** của bạn dev được ghi ở mục *Ràng buộc*, nói rõ là gợi ý, chưa phải quyết định.
- **Lỗi khi bộ nhớ đầy** là thông tin mình đọc được trong code, không có khách nào nhắc tới. Mình ghi nó ở *Ràng buộc*, còn chuyện có đưa vào phạm vi hay không thì nằm trong câu hỏi gửi product owner.
- **Hai việc bạn có thể làm** để bản này chắc hơn trước khi duyệt: chép vài email (đã bỏ tên và địa chỉ) vào `tickets/`, và đếm xem bao nhiêu email là do đổi máy, bao nhiêu là do xoá dữ liệu trình duyệt.

Chỗ nào mình hiểu sai thì bạn cứ sửa trực tiếp trong file hoặc nói mình sửa. Việc commit, review và merge vào `main` là của người.

---

File mới: 2026-10-19-khach-khong-mat-viec.md
