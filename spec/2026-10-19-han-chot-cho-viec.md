# Spec: Hạn chót cho việc

From: intent/2026-10-19-han-chot-cho-viec.md · Skills: policy-privacy@1, policy-security@2, policy-ux@2 · Status: accepted · Risk: high (risk-list dòng 2: "Changes the shape of stored data (a new field, a new key, a migration)"; dòng 1: "personal data leaving the user's device", vì file sao lưu nay chứa hạn chót) · Date: 2026-11-04 (bản đầu 2026-10-20)

## Goal
Hà không quên những việc có deadline, và nhìn danh sách là biết ngay việc nào tới hạn trước [intent]. Lần này người dùng đặt được
**ngày** hạn chót cho một việc, thấy hạn chót trên danh sách, xếp được danh sách theo hạn chót, và việc quá hạn hiện nổi bật [intent].
"Nhắc" chỉ có nghĩa là thấy khi mở app [intent]. Hạn chót được giữ khi sao lưu ra file và nhập lại [answer C2, Thảo · Khoa].

Mốc đo sau khi ra bản mới (không phải tiêu chí nghiệm thu của spec này): trong 4 tuần, ít nhất một nửa người +1 ticket dùng hạn chót,
hỏi lại qua form góp ý [intent]. Khi đọc mốc đo, nhớ trường hợp Hà không mở app hôm đó (C1) [answer C1, Thảo].

## Out of scope
- Thông báo khi không mở app, nhắc trên điện thoại [intent] [answer C1, Thảo]
- Việc lặp lại hằng tuần, chia sẻ hạn chót cho đồng nghiệp [intent]
- Giờ của hạn chót: chỉ có ngày [intent]
- Đồng bộ nhiều máy [intent].
- Sao lưu và nhập lại: intent ghi là thuộc intent `2026-10-19-khach-khong-mat-viec.md` [intent]. Thảo và Khoa đã quyết mở rộng spec
  này sang **cấu trúc file sao lưu** (thêm hạn chót, `version: 2`), không đổi gì khác của sao lưu [answer C2, Thảo · Khoa]. Spec
  không sửa `intent/`; câu chữ trong intent vẫn là bản cũ, sửa intent là việc của người.
- Spec này không đổi nút xoá một việc; nút đó hiện xoá ngay, không có Undo [app/app.js]. Undo cho nút xoá để intent riêng
  [spec/2026-10-19-khach-khong-mat-viec.md C4]. Undo trong spec này chỉ dành cho bỏ hạn chót (F2) [answer A3, Linh].
- Không lưu dữ liệu ở đâu khác ngoài trình duyệt, nên không cần duyệt của privacy owner theo P5 [policy-privacy@1#P5].

## User flows

### F1 · Đặt hạn chót khi thêm việc
1. Form thêm việc có thêm một ô chọn ngày hạn chót, không bắt buộc [intent], đặt cạnh ô tiêu đề, có nhãn "Hạn chót" [answer A1, Linh].
2. Người dùng gõ tiêu đề, chọn ngày hoặc để trống, bấm Thêm [intent] [app/index.html].
3. Việc mới có hạn chót nếu đã chọn ngày, không có nếu để trống [intent]. Chỉ có ngày, không có giờ [intent].
4. Sau khi thêm, ô chọn ngày được xoá trống như ô tiêu đề [answer A1, Linh] [app/app.js].
5. Được chọn ngày đã qua (ví dụ ghi lại một việc đã trễ); việc đó hiện quá hạn ngay (F3) [answer A4, Thảo].
6. Lưu như mọi lần thêm việc [app/app.js]. Nếu lưu lỗi, app hiện thông báo không lưu được đã có trên cùng màn hình: "Thay đổi vừa rồi
   chưa được lưu. Hãy sao lưu ra file, rồi xoá bớt việc đã xong." [app/backup.js] [answer C3, Thảo · Linh] [policy-ux@2#U1].

### F2 · Đặt, đổi, bỏ hạn chót của việc đang có
1. Mỗi dòng việc có ô chọn ngày hạn chót, có nhãn "Hạn chót của việc <tiêu đề>"; người dùng đặt ngày, chọn ngày khác, hoặc xoá
   trống ô [answer A2, Thảo · Linh].
2. Đổi xong là lưu và vẽ lại danh sách ngay, như khi đánh dấu xong hiện nay [app/app.js]. Đặt hoặc đổi sang ngày khác: không có Undo
   [answer A3, Linh].
3. Xoá trống ô là bỏ hạn chót của việc đó. Bỏ hạn chót làm mất ngày đã đặt, nên là thao tác trên một việc có **Undo 10 giây**: thao
   tác chạy ngay, không hỏi xác nhận, rồi app cho hoàn tác trong 10 giây [answer A3, Linh] [policy-ux@2#U2]. Chữ, vị trí của Undo và
   khi nào nó biến mất: xem A16.
4. Bấm Undo trong 10 giây → việc có lại đúng ngày hạn chót cũ, app lưu lại và vẽ lại danh sách [answer A3, Linh] [policy-ux@2#U2].
5. Lưu lỗi (khi đặt, đổi, bỏ hạn chót hay khi Undo): app hiện thông báo không lưu được như F1 bước 6 [app/backup.js] [answer C3,
   Thảo · Linh] [policy-ux@2#U1].

### F3 · Thấy hạn chót trên danh sách
1. Việc có hạn chót hiện ngày hạn chót trên dòng của nó [intent], dạng "Hạn 25/10/2026" (ngày/tháng/năm) [answer A5, Linh].
2. Việc quá hạn là việc **chưa xong** có ngày hạn chót **trước hôm nay**; việc tới hạn đúng hôm nay chưa tính quá hạn và không có đánh
   dấu riêng [answer A6, Thảo]. Việc đã xong không bao giờ hiện quá hạn, dù ngày hạn chót đã qua [answer A7, Thảo].
3. Việc quá hạn hiện nổi bật [intent] bằng chữ "Quá hạn" kèm màu, không chỉ dùng màu, để trình đọc màn hình cũng đọc được
   [answer A8, Linh] [policy-ux@2#U5].
4. "Hôm nay" là ngày trên máy người dùng theo giờ máy, lấy bằng `getFullYear` / `getMonth` / `getDate`, **không** dùng `toISOString()`
   vì đó là ngày UTC, lệch một ngày ở múi giờ +7 [answer A9, Thảo · Khoa]; như cách đặt tên file sao lưu hiện nay [app/backup.js].
5. "Hôm nay" được tính lại mỗi lần danh sách vẽ lại (mở app, thêm, đánh dấu, đổi hạn chót, đổi lọc, đổi cách xếp). Để app mở qua
   nửa đêm thì trạng thái quá hạn chỉ cập nhật ở thao tác kế tiếp; điều này được chấp nhận [answer A9, Thảo · Khoa].

### F4 · Xếp theo hạn chót
1. Cạnh bộ lọc có một ô chọn nhãn "Xếp theo", hai lựa chọn "Thứ tự thêm" và "Hạn chót" [answer A10, Linh] [intent].
2. Mở app mặc định xếp theo thứ tự thêm như hiện nay [app/app.js]; lựa chọn xếp không được nhớ sau khi tải lại trang, nên không thêm
   khoá lưu mới [answer A11, Thảo].
3. Xếp theo hạn chót: ngày sớm hơn ở trên, để biết việc nào tới hạn trước [intent]. Việc không có hạn chót nằm cuối [intent]. Hai việc
   cùng ngày hạn chót giữ thứ tự thêm [answer A12, Thảo].
4. Cách xếp áp dụng chung với bộ lọc Tất cả / Chưa xong / Đã xong đang có [app/index.html] [app/app.js].

### F5 · Sao lưu và nhập lại có hạn chót
Spec sao lưu `2026-10-19-khach-khong-mat-viec.md` (accepted) và code hiện tại dùng file `version: 1`, mỗi việc đúng bốn trường, từ
chối trường lạ [spec/2026-10-19-khach-khong-mat-viec.md] [app/backup.js]. Spec này đổi như sau [answer C2, Thảo · Khoa]:
1. Bấm "Sao lưu ra file": app ghi file `version: 2`; việc có hạn chót có thêm trường `dueDate`, việc không có hạn chót không có
   trường này [answer C2, Thảo · Khoa] [answer A15, Khoa]. Mọi bước khác của sao lưu (tên file, thông báo, giới hạn 1 MB) không đổi
   [spec/2026-10-19-khach-khong-mat-viec.md F1]. Có ghi `version: 2` cả khi không việc nào có hạn chót không: xem A18.
2. Nhập file `version: 2`: kiểm như hiện nay, cộng thêm `dueDate` là trường không bắt buộc của mỗi việc [answer C2, Thảo · Khoa]
   [policy-security@2#S1]. `dueDate` hỏng (không phải chuỗi `YYYY-MM-DD`, hoặc ngày không có thật) → **từ chối cả file**, danh sách
   đang có giữ nguyên, báo như file lỗi hiện nay [answer C2, Thảo · Khoa] [app/backup.js]. Khác với A14 (giữ giá trị hỏng trong bộ
   nhớ), vì file nhập là đầu vào không tin được [answer C2, Khoa].
3. Nhập file `version: 1` (sao lưu từ trước): vẫn nhập được như hiện nay; các việc nhập vào không có hạn chót [answer C2, Thảo · Khoa].
4. File `version: 1` mà có `dueDate` → vẫn bị từ chối như trường lạ [answer C2, Thảo · Khoa] [app/backup.js].
5. Hộp xác nhận, Undo (không có), lưu lỗi sau khi nhập: không đổi so với spec sao lưu [spec/2026-10-19-khach-khong-mat-viec.md F2].
6. Phần này làm thành **PR riêng, sau PR hạn chót** [answer C2, Khoa]. Khoảng giữa hai PR: xem A17.

### Trạng thái màn hình
- Trống: spec này không đổi. Danh sách trống hiện dòng "Chưa có việc nào. Nếu có file sao lưu, hãy bấm "Nhập từ file"." [app/app.js]
  [app/backup.js]. Xếp theo hạn chót khi không việc nào có hạn chót: danh sách hiện như thứ tự thêm, không có dòng báo riêng
  [answer A13, Linh].
- Đang tải: không có. App đọc bộ nhớ trình duyệt một lần, đồng bộ, trước lần vẽ đầu tiên [app/app.js] [app/store.js]. Đọc file nhập
  vẫn hiện "Đang đọc file…" như hiện nay [app/backup.js].
- Lỗi: lưu lỗi, F1 bước 6 và F2 bước 5. Hạn chót hỏng trong bộ nhớ: hiện và xếp như việc không có hạn chót, app không tự xoá giá trị
  đó [answer A14, Khoa]. File nhập có `dueDate` hỏng: F5 bước 2.

## Data and integrations
- Bộ nhớ trình duyệt: giữ khoá `todo.v1`, vẫn là một mảng việc [app/store.js] [answer A15, Khoa].
- Mỗi việc hiện gồm `id`, `title`, `done`, `createdAt` [app/app.js]. Spec thêm trường không bắt buộc `dueDate`, giá trị là chuỗi
  `YYYY-MM-DD` theo lịch, không phải mốc thời gian, để không lệch ngày theo múi giờ; việc không có hạn chót thì **không có** trường
  này [answer A15, Khoa]. Không cần chuyển đổi dữ liệu cũ [answer A15, Khoa].
- Bỏ hạn chót (F2 bước 3) là xoá trường `dueDate` khỏi việc [answer A15, Khoa]. Ngày cũ chỉ giữ trong bộ nhớ của trang trong 10 giây
  Undo, không ghi vào bộ nhớ trình duyệt [answer A3, Linh] (A16).
- Việc đã có từ trước không có trường này, nên được hiện như việc không có hạn chót [app/app.js] [answer A15, Khoa].
- `dueDate` hỏng trong bộ nhớ (không đúng dạng, hoặc ngày không có thật): hiện và xếp như không có hạn chót, giá trị được giữ nguyên
  [answer A14, Khoa].
- `store.save` ghi cả mảng việc bằng `JSON.stringify`, nên trường mới được lưu mà không phải sửa `app/store.js` [app/store.js]. Mọi
  lần lưu đi qua `persist`, đã trả về thông báo khi lưu lỗi [app/backup.js] [app/app.js].
- File sao lưu: `{ "version": 2, "todos": [ … ] }`, mỗi việc gồm `id`, `title`, `done`, `createdAt` và `dueDate` không bắt buộc;
  vẫn nhập được file `version: 1` [answer C2, Thảo · Khoa]. Hiện `pick`, `TODO_KEYS`, `toBackupText` và `parseBackup` chỉ biết
  `version: 1` và bốn trường, nên sao lưu hiện nay bỏ mất mọi trường khác [app/backup.js].
- Ngày hạn chót và mọi chữ đi kèm gắn vào trang bằng `textContent` [policy-security@2#S3], như tiêu đề việc hiện nay [app/app.js].
- Không thêm thư viện, CDN hay dịch vụ ngoài [policy-security@2#S4]: ô chọn ngày dùng `<input type="date">` sẵn của trình duyệt.
- Các file sửa, PR hạn chót: `app/app.js` (trường mới, vẽ dòng việc, xếp, Undo, chú thích dòng 1 đang ghi "No due date"
  [app/app.js]), `app/index.html`, `app/style.css`. `app/store.js` không đổi [app/store.js]. PR sao lưu sau đó: `app/backup.js`
  (chú thích dòng 2 đang ghi `version: 1` [app/backup.js]) [answer C2, Khoa].
- `policy-security` S1 hiện ghi "reject unknown fields" [policy-security@2#S1]. **Khoa (owner) tự sửa S1** để khớp file `version: 2`
  [answer C2, Thảo · Khoa]; spec này không sửa policy. Khi S1 đổi bản, dòng 2 của spec phải ghi bản mới.

## Policy constraints
- policy-privacy@1#P1 → hạn chót chỉ nằm trong bộ nhớ trình duyệt, chỉ rời trình duyệt khi người dùng bấm sao lưu; không có request
  mạng mới (tiêu chí 11).
- policy-privacy@1#P2 → file sao lưu thêm `dueDate`, là ngày người dùng tự đặt; không thêm định danh thiết bị (F5). Xem A19.
- policy-privacy@1#P3 → file vẫn là JSON thụt lề, văn bản thường, `dueDate` là chuỗi ngày đọc được (F5). Xem A19.
- policy-privacy@1#P4 → không áp dụng: nơi giữ dữ liệu không đổi; dòng chữ nói nơi giữ dữ liệu đã có theo spec sao lưu F4.
- policy-privacy@1#P5 → không áp dụng: không lưu ngoài trình duyệt.
- policy-security@2#S1 → F5 bước 2–4: file nhập vẫn được kiểm, giới hạn 1 MB không đổi, `dueDate` hỏng thì từ chối cả file,
  `version: 1` có `dueDate` vẫn bị từ chối. Câu "reject unknown fields" sẽ do Khoa sửa trong S1 [answer C2, Khoa].
- policy-security@2#S2 → không áp dụng cho phần mới: không thao tác mới nào ghi đè hay xoá quá một việc; nhập file giữ hộp xác nhận
  của spec sao lưu (F5 bước 5).
- policy-security@2#S3 → ngày hạn chót, chữ "Quá hạn", chữ Undo gắn bằng `textContent` (tiêu chí 12).
- policy-security@2#S4 → không thêm phụ thuộc ngoài (tiêu chí 11).
- policy-ux@2#U1 → đặt, đổi, bỏ hạn chót và Undo đều là lần lưu; lưu lỗi hiện thông báo đã có (F1 bước 6, F2 bước 5, tiêu chí 13).
  Sao lưu không còn bỏ mất hạn chót (F5, tiêu chí 14); khoảng giữa hai PR: A17; giá trị hỏng trong file sao lưu: C4.
- policy-ux@2#U2 → bỏ hạn chót có Undo 10 giây, không hỏi xác nhận (F2 bước 3–4, tiêu chí 6). Đặt hay đổi ngày không có Undo
  [answer A3, Linh].
- policy-ux@2#U3 → mục Trạng thái màn hình.
- policy-ux@2#U4 → mọi chữ mới bằng tiếng Việt, ngắn, không có từ kỹ thuật (tiêu chí 10): "Hạn chót", "Hạn 25/10/2026", "Quá hạn",
  "Xếp theo", "Thứ tự thêm", chữ Undo (A16).
- policy-ux@2#U5 → ô chọn ngày ở form thêm (nhãn "Hạn chót"), ô chọn ngày trên mỗi dòng (nhãn "Hạn chót của việc <tiêu đề>"), ô
  "Xếp theo" và nút Undo dùng được bằng bàn phím và có nhãn (tiêu chí 9).

## Assumptions
A1–A15 đã được trả lời và nằm trong thân spec với nguồn `[answer A<n>, <tên>]`; C1–C3 cũng vậy với `[answer C<n>, <tên>]`
[demo/sdlc-5/tra-loi-gia-dinh.md]. Những dòng dưới đây mới, sinh ra khi đưa các câu trả lời vào spec:

- A16. Bỏ hạn chót xong, vùng thông báo hiện "Đã bỏ hạn chót của việc <tiêu đề>." kèm nút "Hoàn tác"; nút biến mất sau 10 giây hoặc
  khi người dùng làm thao tác khác (thêm, đánh dấu, xoá, đổi hạn chót, nhập file), đúng không? → Linh (UX owner)
- A17. PR sao lưu `version: 2` ra cùng bản phát hành với PR hạn chót, để không có bản nào mà người dùng đặt được hạn chót nhưng sao lưu
  vẫn là `version: 1` và bỏ mất hạn chót không báo (`pick` hiện chỉ giữ bốn trường [app/backup.js], trái `policy-ux@2#U1`), đúng
  không? → Khoa (tech lead), Thảo (product owner)
- A18. Sau thay đổi, app luôn ghi file `version: 2`, kể cả khi không việc nào có hạn chót, đúng không? → Khoa (tech lead)
- A19. Hạn chót trong file sao lưu là dữ liệu người dùng tạo theo P2, file vẫn đọc được theo P3, nên không cần Mai duyệt lại cấu trúc
  file, đúng không? → Mai (privacy owner)

## Concerns
- **C1 · "Nhắc chỉ khi mở app" có thể không chặn được đúng chuyện Hà đã gặp.** **Đã quyết:** ghi nhận, giữ phạm vi [answer C1, Thảo].
  Mốc đo 4 tuần nhớ trường hợp Hà không mở app; vẫn phải hỏi Hà cái báo cáo đó có trong app không (Questions carried forward)
  [answer C1, Thảo].
- **C2 · File sao lưu không chứa hạn chót.** **Đã quyết:** phương án (b) [answer C2, Thảo · Khoa]; (a) và (c) không còn vì bản sao lưu
  `version: 1` đã ra [demo/sdlc-5/tra-loi-gia-dinh.md]. Spec mở rộng sang cấu trúc file sao lưu (F5): `version: 2` có `dueDate` không
  bắt buộc, `version: 1` vẫn nhập được, `dueDate` hỏng trong file thì từ chối cả file. Khoa tự sửa `policy-security` S1. Làm thành PR
  riêng sau PR hạn chót [answer C2, Khoa]; còn mở A17.
- **C3 · Lưu hạn chót lỗi.** **Đã quyết:** phương án (a) [answer C3, Thảo · Linh]. F3 của spec sao lưu đã ra: mọi lần lưu lỗi hiện
  thông báo trên màn hình [app/backup.js] [app/app.js], nên đặt hay đổi hạn chót lúc lưu lỗi cũng có báo (F1 bước 6, F2 bước 5, tiêu
  chí 13).
- **C4 · Sao lưu một danh sách có `dueDate` hỏng sẽ không nhập lại được.** Mới, sinh ra từ A14 và C2. A14 giữ nguyên giá trị hỏng trong
  bộ nhớ [answer A14, Khoa]; nếu sao lưu chép nguyên giá trị đó ra file `version: 2`, thì khi nhập lại, F5 bước 2 từ chối cả file
  [answer C2, Khoa], tức file sao lưu của chính app không dùng được mà người dùng không biết, trái `policy-ux@2#U1` (owner Linh). Còn
  nếu sao lưu sửa giá trị, thì A14 ("không tự xoá") cần nói rõ có áp dụng cho file không (owner Khoa, `policy-security@2#S1`). Spec
  này không chọn. Các phương án:
  - (a) Sao lưu bỏ `dueDate` hỏng khỏi việc đó trong file (bộ nhớ vẫn giữ). Tốn ít; giá trị hỏng vốn đã hiện như không có hạn chót.
  - (b) Sao lưu chép nguyên, và báo ngay lúc sao lưu rằng file không nhập lại được, như cách F1 bước 5 của spec sao lưu báo file quá
    1 MB. Tốn thêm một câu báo; người dùng vẫn không có bản sao lưu dùng được.
  - (c) Khi nhập, coi `dueDate` hỏng như không có hạn chót thay vì từ chối cả file. Đi ngược câu trả lời C2 của Khoa.
  → Khoa (tech lead, owner S1), Linh (UX owner, U1)

## Acceptance criteria
Các tiêu chí dùng ngày trên máy là 10/11/2026, múi giờ máy UTC+7.

1. Thêm việc "Nộp báo cáo" với hạn chót 12/11/2026 → dòng việc hiện "Hạn 12/11/2026". Tải lại trang → vẫn hiện. Ô chọn ngày ở form
   thêm trống lại sau khi thêm.
2. Thêm việc không chọn ngày → dòng việc không hiện hạn chót. Trong bộ nhớ trình duyệt, việc đó không có trường `dueDate`.
3. Việc chưa xong có hạn 09/11/2026 → hiện nổi bật với chữ "Quá hạn". Việc có hạn 10/11/2026 hoặc 11/11/2026 → không có. Đánh dấu xong
   việc hạn 09/11/2026 → không còn "Quá hạn". Giờ máy 06:00 ngày 10/11/2026 (23:00 ngày 09/11 theo UTC) → việc hạn 10/11/2026 vẫn
   không hiện "Quá hạn", việc hạn 09/11/2026 vẫn hiện. Thêm việc với hạn 01/11/2026 → hiện "Quá hạn" ngay.
4. Thêm lần lượt: A (không hạn chót), B (15/11/2026), C (12/11/2026), D (12/11/2026). Chọn "Xếp theo" → "Hạn chót" → thứ tự C, D, B, A.
   Chọn lại "Thứ tự thêm" → A, B, C, D. Tải lại trang khi đang xếp theo hạn chót → mở ra xếp theo thứ tự thêm.
5. Đang xếp theo hạn chót, bấm lọc "Chưa xong" → chỉ còn việc chưa xong và vẫn xếp theo hạn chót.
6. Đổi hạn chót của B sang 11/11/2026 ngay trên dòng của nó → hiện ngày mới, không có nút Undo; tải lại trang vẫn còn. Xoá trống ô ngày
   của B → B không còn hạn chót ngay, không có hộp xác nhận, có nút Undo. Bấm Undo trong 10 giây → B có lại hạn 11/11/2026; tải lại
   trang vẫn còn. Xoá trống lại, chờ quá 10 giây → nút Undo không còn; tải lại trang B không có hạn chót.
7. Ghi vào `todo.v1` một mảng việc dạng cũ (chỉ `id`, `title`, `done`, `createdAt`), mở app → đủ việc, đúng trạng thái xong, không
   việc nào có hạn chót, không có lỗi trong console.
8. Ghi vào `todo.v1` một việc có `dueDate` là `"abc"` và một việc có `dueDate` là `"2026-02-30"` → app mở bình thường; hai việc đó hiện
   như không có hạn chót và nằm cuối khi xếp theo hạn chót; hai giá trị vẫn còn nguyên trong bộ nhớ.
9. Chỉ dùng bàn phím (Tab, Enter, Space, phím mũi tên): đặt hạn chót khi thêm việc, đổi và bỏ hạn chót việc đang có, bấm Undo, đổi
   cách xếp. Trình đọc màn hình đọc được nhãn "Hạn chót", "Hạn chót của việc <tiêu đề>", "Xếp theo", nút Undo và chữ "Quá hạn".
10. Mọi chữ mới trong app không chứa "localStorage", "JSON", "console", "dueDate".
11. Tắt mạng: tiêu chí 1 tới 6 vẫn đạt; công cụ Network của trình duyệt không ghi request nào khi thêm, đổi hạn chót, Undo hay đổi cách
    xếp. `app/index.html` không có thêm `<script>` hay `<link>` trỏ ra ngoài.
12. Thêm việc có tiêu đề `<img src=x onerror=alert(1)>` và hạn chót 09/11/2026 → tiêu đề hiện đúng nguyên chữ đó, ngày và chữ
    "Quá hạn" hiện bình thường, không có hộp alert. Bỏ hạn chót của việc đó → chữ Undo hiện đúng nguyên tiêu đề, không có hộp alert.
13. Làm cho lưu lỗi (ví dụ `localStorage.setItem` ném lỗi). Thêm việc có hạn chót, rồi đổi hạn chót một việc đang có, rồi bỏ hạn chót →
    mỗi lần, màn hình hiện "Thay đổi vừa rồi chưa được lưu. Hãy sao lưu ra file, rồi xoá bớt việc đã xong."
14. (PR sao lưu) Có 2 việc: X hạn 12/11/2026, Y không hạn chót. Bấm "Sao lưu ra file" → file có `"version": 2`; X có
    `"dueDate": "2026-11-12"`, Y không có trường `dueDate`. Xoá dữ liệu trang, nhập file đó → X hiện "Hạn 12/11/2026", Y không có hạn
    chót; tải lại trang vẫn vậy.
15. (PR sao lưu) Nhập một file `version: 1` tạo trước thay đổi này (bốn trường mỗi việc) → nhập được, đủ việc, không việc nào có hạn chót.
16. (PR sao lưu) Nhập lần lượt, mỗi file chỉ sai một chỗ: (a) file `version: 1` có một việc mang `dueDate` hợp lệ, (b) file `version: 2`
    có một việc `dueDate` là `"abc"`, (c) file `version: 2` có `dueDate` là `"2026-02-30"`, (d) file `version: 2` có `dueDate` là
    `null`, (e) file `version: 2` có một trường lạ `"x": 1` → cả năm bị từ chối, danh sách không đổi, không việc nào được nhập, thấy
    thông báo.

## Questions carried forward from the intent
- Cái báo cáo Hà quên tuần trước có nằm trong app không? → Hà (liên quan C1; Thảo nhắc vẫn phải hỏi [answer C1, Thảo])
- 14 người +1 là ai, có cùng nhu cầu với Hà không? → Thảo (product owner, xem lại form góp ý)
- Tổng số người dùng là bao nhiêu? → Thảo (product owner)
