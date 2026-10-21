# Spec: Hạn chót cho việc

From: intent/2026-10-19-han-chot-cho-viec.md · Skills: policy-privacy@1, policy-security@1, policy-ux@1 · Status: draft · Risk: high (risk-list dòng 2: "Changes the shape of stored data (a new field, a new key, a migration)") · Date: 2026-10-20

## Goal
Hà không quên những việc có deadline, và nhìn danh sách là biết ngay việc nào tới hạn trước [intent]. Lần này người dùng đặt được
**ngày** hạn chót cho một việc, thấy hạn chót trên danh sách, xếp được danh sách theo hạn chót, và việc quá hạn hiện nổi bật [intent].
"Nhắc" chỉ có nghĩa là thấy khi mở app [intent].

Mốc đo sau khi ra bản mới (không phải tiêu chí nghiệm thu của spec này): trong 4 tuần, ít nhất một nửa người +1 ticket dùng hạn chót,
hỏi lại qua form góp ý [intent].

## Out of scope
- Thông báo khi không mở app, nhắc trên điện thoại [intent]
- Việc lặp lại hằng tuần, chia sẻ hạn chót cho đồng nghiệp [intent]
- Giờ của hạn chót: chỉ có ngày [intent]
- Sao lưu, nhập lại, đồng bộ: thuộc intent `2026-10-19-khach-khong-mat-viec.md` [intent]. Ảnh hưởng qua lại với spec của intent đó:
  xem C2.
- Spec này không đổi nút xoá một việc; nút đó hiện xoá ngay, không có Undo [app/app.js].
- Không lưu dữ liệu ở đâu khác ngoài trình duyệt, nên không cần duyệt của privacy owner [policy-privacy@1#P5].

## User flows

### F1 · Đặt hạn chót khi thêm việc
1. Form thêm việc có thêm một ô chọn ngày hạn chót, không bắt buộc [intent]. Vị trí và cách xoá trống sau khi thêm: xem A1.
2. Người dùng gõ tiêu đề, chọn ngày hoặc để trống, bấm Thêm [intent] [app/index.html].
3. Việc mới có hạn chót nếu đã chọn ngày, không có nếu để trống [intent]. Chỉ có ngày, không có giờ [intent].
4. Chọn một ngày đã qua: xem A4.
5. Lưu như mọi lần thêm việc [app/app.js]. Nếu lưu lỗi: xem C3.

### F2 · Đặt, đổi, bỏ hạn chót của việc đang có
Luồng này chỉ có nếu A2 được trả lời "đúng".
1. Mỗi dòng việc có ô chọn ngày hạn chót; người dùng chọn ngày khác hoặc xoá trống ô (A2).
2. Đổi xong là lưu và vẽ lại danh sách ngay, như khi đánh dấu xong hiện nay [app/app.js].
3. Xoá trống ô là bỏ hạn chót của việc đó. Có cần Undo không: xem A3.

### F3 · Thấy hạn chót trên danh sách
1. Việc có hạn chót hiện ngày hạn chót trên dòng của nó [intent]. Dạng hiện ngày: xem A5.
2. Việc quá hạn hiện nổi bật [intent]. Cách tính quá hạn: xem A6, A7. Cách làm nổi bật: xem A8.
3. Cách tính "hôm nay" và khi nào tính lại: xem A9.

### F4 · Xếp theo hạn chót
1. Danh sách có một điều khiển chọn cách xếp: theo thứ tự thêm như hiện nay [app/app.js], hoặc theo hạn chót [intent]. Dạng điều
   khiển: xem A10. Mặc định và có nhớ lựa chọn không: xem A11.
2. Xếp theo hạn chót: ngày sớm hơn ở trên, để biết việc nào tới hạn trước [intent]. Việc không có hạn chót nằm cuối [intent]. Cùng
   ngày: xem A12.
3. Cách xếp áp dụng chung với bộ lọc Tất cả / Chưa xong / Đã xong đang có [app/index.html] [app/app.js].

### Trạng thái màn hình
- Trống: spec này không đổi. Hiện nay danh sách trống không hiện gì [app/app.js]; spec `2026-10-19-khach-khong-mat-viec.md` (draft)
  thêm dòng báo trống [spec/2026-10-19-khach-khong-mat-viec.md]. Xếp theo hạn chót khi không việc nào có hạn chót: xem A13.
- Đang tải: không có. App đọc bộ nhớ trình duyệt một lần, đồng bộ, trước lần vẽ đầu tiên [app/app.js] [app/store.js].
- Lỗi: lưu lỗi, xem C3. Hạn chót hỏng trong bộ nhớ, xem A14.

## Data and integrations
- Bộ nhớ trình duyệt: giữ khoá `todo.v1`, vẫn là một mảng việc [app/store.js].
- Mỗi việc hiện gồm `id`, `title`, `done`, `createdAt` [app/app.js]. Spec thêm một trường không bắt buộc cho ngày hạn chót, chỉ có
  ngày [intent]. Tên trường, dạng giá trị và việc không cần chuyển đổi dữ liệu cũ: xem A15.
- Việc đã có từ trước không có trường này, nên được hiện như việc không có hạn chót [app/app.js] (A15).
- `store.save` ghi cả mảng việc bằng `JSON.stringify`, nên trường mới được lưu mà không phải sửa `app/store.js` [app/store.js].
- Ngày hạn chót và mọi chữ đi kèm gắn vào trang bằng `textContent` [policy-security@1#S3], như tiêu đề việc hiện nay [app/app.js].
- Không thêm thư viện, CDN hay dịch vụ ngoài [policy-security@1#S4]: ô chọn ngày dùng `<input type="date">` sẵn của trình duyệt.
- Các file sửa: `app/app.js` (trường mới, vẽ dòng việc, xếp, chú thích dòng 1 đang ghi "No due date" [app/app.js]),
  `app/index.html`, `app/style.css`. `app/store.js` không đổi [app/store.js].
- File sao lưu của spec `2026-10-19-khach-khong-mat-viec.md`: xem C2.

## Policy constraints
- policy-privacy@1#P1 → hạn chót chỉ nằm trong bộ nhớ trình duyệt, không gửi đi đâu, không có request mạng mới (tiêu chí 11).
- policy-privacy@1#P2 → không áp dụng: spec này không xuất dữ liệu. Liên quan file sao lưu: C2.
- policy-privacy@1#P3 → không áp dụng: như P2.
- policy-privacy@1#P4 → không áp dụng: nơi giữ dữ liệu không đổi. Dòng chữ nói nơi giữ dữ liệu thuộc spec
  `2026-10-19-khach-khong-mat-viec.md` F4.
- policy-privacy@1#P5 → không áp dụng: không lưu ngoài trình duyệt.
- policy-security@1#S1 → không áp dụng: không nhập file. Giá trị hạn chót hỏng trong bộ nhớ: A14.
- policy-security@1#S2 → không áp dụng: không thao tác nào ghi đè hay xoá quá một việc.
- policy-security@1#S3 → ngày hạn chót, chữ quá hạn gắn bằng `textContent` (tiêu chí 12).
- policy-security@1#S4 → không thêm phụ thuộc ngoài (tiêu chí 11).
- policy-ux@1#U1 → áp dụng, vì đặt hay đổi hạn chót là một lần lưu. Spec này không tự đáp ứng; xem C3.
- policy-ux@1#U2 → áp dụng nếu bỏ hạn chót tính là thao tác phá huỷ; xem A3.
- policy-ux@1#U3 → mục Trạng thái màn hình.
- policy-ux@1#U4 → mọi chữ mới bằng tiếng Việt, ngắn, không có từ kỹ thuật (tiêu chí 10). Chữ đề xuất ở A5, A8, A10.
- policy-ux@1#U5 → ô chọn ngày ở form thêm, ô chọn ngày trên mỗi dòng và điều khiển xếp dùng được bằng bàn phím và có nhãn
  (tiêu chí 9); nhãn ô trên dòng: A2.

## Assumptions
- A1. Ô chọn ngày đặt trong form thêm việc, cạnh ô tiêu đề, có nhãn "Hạn chót", và được xoá trống sau khi thêm như ô tiêu đề, đúng
  không? → Linh (UX owner)
- A2. Người dùng đặt, đổi và bỏ được hạn chót của việc đã có (không chỉ lúc thêm), bằng một ô chọn ngày trên mỗi dòng có nhãn
  "Hạn chót của việc <tiêu đề>", đúng không? → Thảo (product owner), Linh (UX owner)
- A3. Bỏ hạn chót của một việc không tính là thao tác phá huỷ theo U2, nên không cần Undo 10 giây, đúng không? → Linh (UX owner)
- A4. Được chọn ngày đã qua (ví dụ ghi lại một việc đã trễ), và việc đó hiện quá hạn ngay, đúng không? → Thảo (product owner)
- A5. Ngày hiện dạng "Hạn 25/10/2026" (ngày/tháng/năm), đúng không? → Linh (UX owner)
- A6. Quá hạn nghĩa là ngày hạn chót trước hôm nay; việc tới hạn đúng hôm nay chưa tính quá hạn và không có đánh dấu riêng, đúng không?
  → Thảo (product owner)
- A7. Việc đã xong không bao giờ hiện quá hạn, dù ngày hạn chót đã qua, đúng không? → Thảo (product owner)
- A8. Việc quá hạn hiện chữ "Quá hạn" kèm màu, không chỉ dùng màu, để trình đọc màn hình cũng đọc được, đúng không? → Linh (UX owner)
- A9. "Hôm nay" theo ngày trên máy người dùng, tính lại mỗi lần danh sách vẽ lại (mở app, thêm, đánh dấu, đổi lọc, đổi cách xếp);
  để app mở qua nửa đêm thì trạng thái quá hạn chỉ cập nhật ở thao tác kế tiếp, chấp nhận được, đúng không? → Thảo (product owner),
  Khoa (tech lead)
- A10. Điều khiển xếp là một ô chọn có nhãn "Xếp theo", hai lựa chọn "Thứ tự thêm" và "Hạn chót", đặt cạnh bộ lọc, đúng không?
  → Linh (UX owner)
- A11. Mở app mặc định xếp theo thứ tự thêm như hiện nay, và lựa chọn xếp không được nhớ sau khi tải lại trang (nên không thêm khoá lưu
  mới), đúng không? → Thảo (product owner)
- A12. Hai việc cùng ngày hạn chót thì giữ thứ tự thêm, đúng không? → Thảo (product owner)
- A13. Xếp theo hạn chót khi không việc nào có hạn chót thì danh sách hiện như thứ tự thêm, không có dòng báo riêng, đúng không?
  → Linh (UX owner)
- A14. Hạn chót hỏng trong bộ nhớ (không đúng dạng, hoặc ngày không có thật) thì hiện và xếp như việc không có hạn chót, nhưng app
  không tự xoá giá trị đó, đúng không? → Khoa (tech lead)
- A15. Trường mới tên `dueDate`, giá trị là chuỗi `YYYY-MM-DD` theo lịch (không phải mốc thời gian, để không lệch ngày theo múi giờ),
  không có trường này khi không có hạn chót; giữ khoá `todo.v1` và không cần chuyển đổi dữ liệu cũ, đúng không? → Khoa (tech lead)

## Concerns
- **C1 · "Nhắc chỉ khi mở app" có thể không chặn được đúng chuyện Hà đã gặp.** Bằng chứng duy nhất về việc quên là báo cáo tuần trước,
  và Hà không nhớ việc đó có trong app không, hôm đó có mở app không [intent]. Product owner đã chốt "nhắc" là thấy khi mở app, thông báo
  khi không mở app nằm ngoài phạm vi [intent]. Spec theo đúng phạm vi đó và không mở rộng. Nếu Hà không mở app hôm đó, spec này không
  giúp được. Ghi để product owner biết khi đọc mốc đo 4 tuần. → Thảo (product owner), Hà
- **C2 · File sao lưu của spec kia không chứa hạn chót.** Spec `2026-10-19-khach-khong-mat-viec.md` (draft) cho file sao lưu chỉ gồm
  `version`, `todos`, `id`, `title`, `done`, `createdAt`, và khi nhập thì từ chối trường lạ [spec/2026-10-19-khach-khong-mat-viec.md]
  theo `policy-security@1#S1` (owner Khoa). Nếu cả hai spec cùng ra như đang viết, thì hoặc sao lưu bỏ mất hạn chót, là mất dữ liệu
  không báo theo `policy-ux@1#U1` (owner Linh), hoặc file sao lưu có hạn chót bị chính app từ chối khi nhập lại. Spec này không chọn.
  Các phương án:
  - (a) Sửa spec sao lưu: thêm trường hạn chót không bắt buộc vào cấu trúc file và vào phần kiểm khi nhập. Tốn ít; phải sửa trước khi
    spec sao lưu được chấp nhận.
  - (b) Ra spec sao lưu trước như đang viết, rồi spec này sửa luôn cấu trúc file sao lưu (thêm `version: 2`, nhập được cả file
    `version: 1`). Tốn thêm phần đọc hai phiên bản file; spec này phải mở rộng phạm vi sang sao lưu.
  - (c) Ra spec này trước, spec sao lưu viết lại theo dữ liệu mới. Spec sao lưu chậm lại.
  → Thảo (product owner, thứ tự ra), Khoa (tech lead, cấu trúc file và S1)
- **C3 · Lưu hạn chót lỗi vẫn im lặng.** Đặt hay đổi hạn chót là một lần lưu; `store.save` hiện chỉ ghi lỗi ra console [app/store.js],
  trái `policy-ux@1#U1`. Spec `2026-10-19-khach-khong-mat-viec.md` (draft) F3 sửa đúng chỗ này cho mọi lần lưu
  [spec/2026-10-19-khach-khong-mat-viec.md], còn intent này không nhắc tới lỗi khi lưu [intent]. Các phương án:
  - (a) Dựa vào F3 của spec sao lưu; spec này ra sau spec đó. Không tốn thêm; phụ thuộc thứ tự ra.
  - (b) Đưa phần báo lưu lỗi vào spec này. Tốn thêm công và làm trùng với spec kia; mở rộng phạm vi, cần product owner đồng ý.
  → Thảo (product owner), Linh (UX owner)

## Acceptance criteria
Các tiêu chí dùng ngày trên máy là 10/11/2026. Tiêu chí 3, 4, 6 kiểm theo câu trả lời "đúng" của các giả định ghi kèm; nếu câu trả lời
khác thì viết lại tiêu chí đó.

1. Thêm việc "Nộp báo cáo" với hạn chót 12/11/2026 → dòng việc hiện ngày 12/11/2026. Tải lại trang → vẫn hiện.
2. Thêm việc không chọn ngày → dòng việc không hiện hạn chót. Trong bộ nhớ trình duyệt, việc đó không có trường hạn chót (A15).
3. Việc chưa xong có hạn 09/11/2026 → hiện nổi bật với chữ "Quá hạn". Việc có hạn 10/11/2026 hoặc 11/11/2026 → không có. Đánh dấu xong
   việc hạn 09/11/2026 → không còn "Quá hạn" (A6, A7, A8).
4. Thêm lần lượt: A (không hạn chót), B (15/11/2026), C (12/11/2026), D (12/11/2026). Chọn xếp theo hạn chót → thứ tự C, D, B, A.
   Chọn lại thứ tự thêm → A, B, C, D (A12).
5. Đang xếp theo hạn chót, bấm lọc "Chưa xong" → chỉ còn việc chưa xong và vẫn xếp theo hạn chót.
6. Đổi hạn chót của B sang 11/11/2026 ngay trên dòng của nó → hiện ngày mới; tải lại trang vẫn còn. Xoá trống ô ngày của B → B không
   còn hạn chót; tải lại trang vẫn không có (A2).
7. Ghi vào `todo.v1` một mảng việc dạng cũ (chỉ `id`, `title`, `done`, `createdAt`), mở app → đủ việc, đúng trạng thái xong, không
   việc nào có hạn chót, không có lỗi trong console.
8. Ghi vào `todo.v1` một việc có hạn chót là `"abc"` → app mở bình thường; việc đó hiện như không có hạn chót và nằm cuối khi xếp
   theo hạn chót; giá trị `"abc"` vẫn còn trong bộ nhớ (A14).
9. Chỉ dùng bàn phím (Tab, Enter, Space, phím mũi tên): đặt hạn chót khi thêm việc, đổi hạn chót việc đang có, đổi cách xếp. Trình
   đọc màn hình đọc được nhãn các ô chọn ngày, nhãn ô xếp, và chữ "Quá hạn".
10. Mọi chữ mới trong app không chứa "localStorage", "JSON", "console", "dueDate".
11. Tắt mạng: tiêu chí 1 tới 6 vẫn đạt; công cụ Network của trình duyệt không ghi request nào khi thêm, đổi hạn chót hay đổi cách xếp.
    `app/index.html` không có thêm `<script>` hay `<link>` trỏ ra ngoài.
12. Thêm việc có tiêu đề `<img src=x onerror=alert(1)>` và hạn chót 09/11/2026 → tiêu đề hiện đúng nguyên chữ đó, ngày và chữ
    "Quá hạn" hiện bình thường, không có hộp alert.

## Questions carried forward from the intent
- Cái báo cáo Hà quên tuần trước có nằm trong app không? → Hà (liên quan C1)
- 14 người +1 là ai, có cùng nhu cầu với Hà không? → Thảo (product owner, xem lại form góp ý)
- Tổng số người dùng là bao nhiêu? → Thảo (product owner)
