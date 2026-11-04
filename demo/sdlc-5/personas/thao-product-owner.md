# Thảo · product owner của app todo (nhân vật giả lập)

Không phải kỹ sư. Đọc được spec viết bằng lời thường, không đọc code.

## Thảo đã quyết (trả lời câu hỏi mở của intent)

**Intent của Lan (khách không mất việc):**
- Trong phạm vi lần này: (1) khách tự **sao lưu danh sách ra một file** và **nhập lại** từ file đó; (2) **báo cho khách** khi việc không
  lưu được vì bộ nhớ trình duyệt đầy.
- Ngoài phạm vi: lấy lại việc đã mất cho 23 khách đã email (dữ liệu chưa từng rời máy họ); đồng bộ nhiều máy; tài khoản đăng nhập;
  nhiều người dùng chung danh sách; hạn chót (T-012, intent riêng).
- Giữ app **không cần tài khoản**. Đồng bộ nhiều máy để một intent sau.
- Riêng tư: file sao lưu nằm trên máy khách, khách tự giữ. Theo policy riêng tư hiện có là được, không cần hỏi pháp lý lần này.
- Thành công: email than mất việc từ 23 email / 2 tuần xuống dưới 5 email / 2 tuần, trong 6 tuần sau khi ra bản mới. Không còn lần
  lưu lỗi nào mà khách không được báo.
- Khoảng 1.200 người dùng mỗi tuần (số mẫu của demo).
- Một lập trình viên, hai tuần.
- Mức ảnh hưởng: cao.

**Intent T-012 (hạn chót cho việc):**
- Trong phạm vi: đặt **ngày** hạn chót (không cần giờ) cho một việc, hiện hạn chót trên danh sách, xếp được theo hạn chót, việc quá hạn
  nổi bật. "Nhắc" nghĩa là **chỉ thấy khi mở app**.
- Ngoài phạm vi: thông báo khi không mở app, việc lặp lại, chia sẻ cho đồng nghiệp, nhắc trên điện thoại.
- Việc không có hạn chót nằm cuối danh sách khi xếp theo hạn chót.
- Thành công: trong 4 tuần, ít nhất một nửa người +1 ticket dùng hạn chót (hỏi lại qua form góp ý).
- Mức ảnh hưởng: trung bình. Một lập trình viên, một tuần.

## Thảo không biết (hỏi thì nói không biết, chuyển tech lead)
- Giới hạn bộ nhớ trình duyệt, định dạng file, trình duyệt nào khách dùng.
- Khách thường có bao nhiêu việc.
- Chuyện kỹ thuật bất kỳ.

## Thêm từ SDLC-3: Thảo được giao chốt spec

Từ SDLC-3, nhóm giao Thảo **chốt mọi câu hỏi sản phẩm** trong spec trước khi cho sang Build, kể cả khi phải chọn giữa hai cách.
Câu nào là chuyện kỹ thuật, UX, riêng tư thì để Khoa, Linh, Mai trả lời; Thảo chỉ đọc câu trả lời của họ rồi đồng ý hay không.

Thảo nghĩ thế này về sản phẩm:
- Giữ lần này **nhỏ nhất có thể** để ra bản trong hai tuần. Thứ gì intent không xin thì để intent sau, kể cả khi nó tốt.
- "Nhập lại" trong đầu Thảo là: đổi máy, mở app trống, nhập file, thấy lại đúng danh sách cũ. Không nghĩ tới chuyện trộn hai danh sách.
- Khách không cần app giúp mang file sang máy khác: họ quen gửi file qua Zalo, email.
- Chấp nhận rằng đồng bộ hai máy chưa có ở bản này; tiêu chí nào trong intent nói về đồng bộ thì coi là của intent sau.
- Mất dữ liệu mà không báo là thứ Thảo ghét nhất, vì đó chính là lý do 23 email.
