# Spec: Sao lưu ra file, nhập lại, và báo khi không lưu được

From: intent/2026-10-19-khach-khong-mat-viec.md · Skills: policy-privacy@1, policy-security@1, policy-ux@1 · Status: draft · Risk: high (risk-list dòng 1: "personal data leaving the user's device") · Date: 2026-10-20

## Goal
Khách không mất việc nữa [intent]. Lần này khách tự sao lưu danh sách ra một file và nhập lại được, và khách được báo khi việc không
lưu được vì bộ nhớ đầy [intent]. Đồng bộ hai máy để một intent sau [intent].

Mốc đo sau khi ra bản mới (đo bằng email, không phải tiêu chí nghiệm thu của spec này): email than mất việc giảm từ 23 email / 2 tuần
xuống dưới 5 email / 2 tuần, trong 6 tuần sau khi ra bản mới [intent].

## Out of scope
- Lấy lại việc đã mất cho 23 khách đã email: dữ liệu chưa từng rời máy họ [intent]
- Đồng bộ nhiều máy, tài khoản đăng nhập, nhiều người dùng chung danh sách [intent]
- Hạn chót cho việc: intent riêng T-012 [intent]
- Spec này không đổi nút xoá một việc đang có. Nút đó hiện xoá ngay, không có Undo [app/app.js], trong khi policy yêu cầu mọi thao tác
  phá huỷ có Undo 10 giây [policy-ux@1#U2]. Intent không nhắc tới nút này [intent], nên để ngoài phạm vi.
- Không lưu dữ liệu ở đâu khác ngoài trình duyệt của khách, nên không cần duyệt của privacy owner [policy-privacy@1#P5].

## User flows

### F1 · Sao lưu ra file
1. Khách bấm nút sao lưu [intent].
2. App tạo một file chứa toàn bộ danh sách việc hiện có (id, tiêu đề, trạng thái xong, thời điểm tạo) và trình duyệt tải file đó về máy
   [intent] [app/app.js]. File chỉ được tạo khi khách bấm, không gửi đi đâu [policy-privacy@1#P1].
3. App báo trên cùng màn hình là đã sao lưu bao nhiêu việc [policy-ux@1#U1].
4. Nếu danh sách trống: xem Assumptions (A6).
5. Nếu file sao lưu lớn hơn 1 MB: xem Concerns (C3).

### F2 · Nhập lại từ file
1. Khách bấm nút nhập từ file và chọn một file [intent].
2. Trong lúc đọc file, app hiện trạng thái đang đọc [policy-ux@1#U3].
3. App kiểm file trước khi đụng tới danh sách đang có [policy-security@1#S1]:
   - file lớn hơn 1 MB → từ chối [policy-security@1#S1];
   - nội dung không đúng cấu trúc ở mục Data, hoặc có trường lạ → từ chối [policy-security@1#S1];
   - nội dung chỉ được đọc như dữ liệu, không bao giờ chạy [policy-security@1#S1].
4. Khi từ chối: danh sách đang có giữ nguyên, app báo trên cùng màn hình bằng lời thường, kèm việc khách làm tiếp được
   [policy-ux@1#U1] [policy-ux@1#U4].
5. Khi file hợp lệ và danh sách đang trống: app hiện các việc trong file và lưu lại [intent]. Không có việc nào bị thay, nên không cần
   xác nhận hay Undo [policy-security@1#S2] [policy-ux@1#U2].
6. Khi file hợp lệ và danh sách đang có việc: **chưa thiết kế được**, vì hai policy mâu thuẫn. Xem Concerns (C1).
7. Nếu lưu sau khi nhập bị lỗi: danh sách cũ giữ nguyên và app báo như F3 [policy-ux@1#U1].

### F3 · Báo khi không lưu được
1. Khách thêm, đánh dấu xong hoặc xoá một việc [app/app.js].
2. App ghi danh sách vào bộ nhớ trình duyệt [app/store.js].
3. Nếu ghi lỗi (ví dụ bộ nhớ đầy, khoảng 5 MB ở đa số trình duyệt [app/store.js]): thay vì chỉ ghi ra console như hiện nay
   [app/store.js], app hiện thông báo trên cùng màn hình, bằng lời thường, nói việc vừa rồi chưa được lưu và khách làm gì tiếp được
   [intent] [policy-ux@1#U1] [policy-ux@1#U4].
4. Lời gợi ý làm tiếp: xem Assumptions (A8).

### F4 · Cho khách biết việc được giữ ở đâu
1. Trên màn hình chính, app ghi bằng lời thường rằng danh sách chỉ được giữ trên trình duyệt này, và xoá dữ liệu trình duyệt, đổi trình
   duyệt hoặc đổi máy là mất danh sách [policy-privacy@1#P4] [app/store.js].
2. Lời này không dùng từ kỹ thuật [policy-ux@1#U4].

### Trạng thái màn hình
- Trống: khi danh sách không có việc nào, app hiện một dòng nói chưa có việc và chỉ tới nút nhập từ file [policy-ux@1#U3]. Hiện nay
  danh sách trống không hiện gì [app/app.js].
- Đang đọc: F2 bước 2 [policy-ux@1#U3].
- Lỗi: F2 bước 4 và F3 bước 3 [policy-ux@1#U3].

## Data and integrations
- Bộ nhớ trình duyệt: giữ nguyên khoá `todo.v1` và cấu trúc hiện có, một mảng việc [app/store.js]. Spec này không thêm khoá, không thêm
  trường [app/store.js].
- Một việc gồm `id` (chuỗi), `title` (chuỗi), `done` (đúng/sai), `createdAt` (số mili giây) [app/app.js].
- File sao lưu: chỉ chứa dữ liệu khách tạo ra, không có định danh thiết bị hay dấu vết trình duyệt [policy-privacy@1#P2]; là văn bản
  thường, mở ra đọc được [policy-privacy@1#P3]. Cấu trúc cụ thể: xem Assumptions (A2, A3).
- `store.save` phải cho nơi gọi biết ghi thành công hay lỗi; hiện nó nuốt lỗi [app/store.js].
- `store.load` hiện trả về danh sách trống khi dữ liệu hỏng [app/store.js]. Xem Concerns (C4).
- Hiển thị tiêu đề việc (kể cả việc vừa nhập từ file) bằng `textContent` [policy-security@1#S3]; `render` đã làm vậy cho tiêu đề
  [app/app.js].
- Không thêm thư viện, CDN hay dịch vụ ngoài [policy-security@1#S4]. Tải file về và chọn file dùng sẵn tính năng của trình duyệt
  (xem A9).
- Các file sửa: `app/store.js`, `app/app.js`, `app/index.html`, `app/style.css` [app/].

## Policy constraints
- policy-privacy@1#P1 → file chỉ được tạo khi khách bấm sao lưu, không gửi đi đâu (F1).
- policy-privacy@1#P2 → file chỉ chứa bốn trường của việc; xem A3 về trường `id` và trường phiên bản.
- policy-privacy@1#P3 → file là văn bản thường, đọc được; xem A2.
- policy-privacy@1#P4 → dòng chữ ở F4.
- policy-privacy@1#P5 → không áp dụng: không lưu ngoài trình duyệt.
- policy-security@1#S1 → F2 bước 3: giới hạn 1 MB, kiểm cấu trúc, từ chối trường lạ, không chạy nội dung. Xem C3.
- policy-security@1#S2 → áp dụng khi nhập thay danh sách có từ 2 việc trở lên; mâu thuẫn với U2, xem C1.
- policy-security@1#S3 → tiêu đề hiển thị bằng `textContent`.
- policy-security@1#S4 → không thêm phụ thuộc ngoài.
- policy-ux@1#U1 → F2 bước 4 và 7, F3 bước 3.
- policy-ux@1#U2 → áp dụng khi nhập thay danh sách đang có; mâu thuẫn với S2, xem C1.
- policy-ux@1#U3 → mục Trạng thái màn hình.
- policy-ux@1#U4 → mọi lời trong app bằng tiếng Việt, ngắn, không có từ kỹ thuật; xem A10 về đuôi tên file.
- policy-ux@1#U5 → nút sao lưu, nút nhập từ file dùng được bằng bàn phím và có nhãn cho trình đọc màn hình; xem A9.

## Assumptions
- A1. Khách tự chuyển file sao lưu sang máy mới (qua email, Zalo, ổ đĩa…), app không cần giúp bước này, đúng không? → product owner
- A2. File dạng JSON thụt lề (văn bản thường) là đủ "plain and human-readable" theo P3, đúng không? → Mai (privacy owner)
- A3. File chỉ gồm `{ "version": 1, "todos": [ … ] }`; trường `version` và `id` của việc (app tự sinh) không vi phạm P2, đúng không?
  → Mai (privacy owner)
- A4. Khi nhập, file có hai việc trùng `id`, tiêu đề rỗng, hoặc `createdAt` không phải số thì từ chối cả file (không nhập một phần),
  đúng không? → Khoa (tech lead)
- A5. Tên file là `todo-sao-luu-<YYYY-MM-DD>.json`, đúng không? → product owner
- A6. Khi danh sách trống, nút sao lưu vẫn bấm được và báo "chưa có việc nào để sao lưu" thay vì tạo file rỗng, đúng không?
  → product owner
- A7. Nút sao lưu và nút nhập từ file đặt dưới danh sách, cạnh dòng đếm việc, đúng không? → Linh (UX owner)
- A8. Khi không lưu được, lời gợi ý là "sao lưu ra file rồi xoá bớt việc đã xong", đúng không? → Linh (UX owner)
- A9. Thông báo lỗi và kết quả đặt trong một vùng `role="status"` / `aria-live` để trình đọc màn hình đọc lên, và nút nhập dùng
  `<input type="file">` có nhãn, đúng không? → Linh (UX owner)
- A10. Đuôi `.json` hiện trong tên file do hệ điều hành hiển thị, không tính là chữ trong app theo U4, đúng không? → Linh (UX owner)
- A11. Khi không lưu được, việc vừa thêm/sửa vẫn hiện trên màn hình (chưa lưu) cho tới lần lưu thành công sau, đúng không?
  → Khoa (tech lead)
- A12. File sao lưu không tính là "changes the shape of stored data" (risk-list dòng 2), vì bộ nhớ trình duyệt không đổi, đúng không?
  → Khoa (tech lead)

## Concerns
- **C1 · Mâu thuẫn policy khi nhập thay danh sách đang có.** `policy-security@1#S2` (owner Khoa) bắt hỏi xác nhận **trước** khi thay
  hoặc xoá từ 2 việc trở lên, và lời xác nhận nói rõ mất gì. `policy-ux@1#U2` (owner Linh) cấm hộp xác nhận, bắt làm ngay và cho Undo
  10 giây. Nhập file khi danh sách đang có việc là thay nhiều việc một lúc, nên không thể theo cả hai. Spec không chọn. Các phương án:
  - (a) Theo S2, xin ngoại lệ U2: hỏi "Thay 12 việc hiện có bằng 30 việc trong file?". Tốn ít công; Linh phải đồng ý ngoại lệ.
  - (b) Theo U2, xin ngoại lệ S2: thay ngay, Undo 10 giây. Phải giữ danh sách cũ trong 10 giây và lưu lại nếu Undo; nếu khách đóng
    trang trong 10 giây thì mất danh sách cũ. Khoa phải đồng ý ngoại lệ.
  - (c) Không thay mà gộp: chỉ thêm việc có `id` chưa có. Không xoá gì nên cả S2 và U2 không bị kích hoạt. Cách này đổi hành vi
    "nhập lại" mà product owner chốt, và việc đã xoá ở máy cũ có thể quay lại. Cần product owner đồng ý.
  → Khoa (security owner) và Linh (UX owner) cùng quyết; product owner nếu chọn (c).
- **C2 · Tiêu chí thành công của intent không khớp phạm vi.** Intent ghi "máy này thêm/xoá thì máy kia cũng thấy" [intent], nhưng đồng
  bộ nhiều máy nằm ngoài phạm vi [intent]. Hai tiêu chí "đổi điện thoại mới / xoá dữ liệu trình duyệt vẫn thấy đủ việc" [intent] chỉ
  đạt khi khách đã sao lưu trước đó. Spec này không đạt tiêu chí thứ ba, và chỉ đạt hai tiêu chí đầu có điều kiện.
  → product owner (sửa tiêu chí trong intent, hoặc chấp nhận).
- **C3 · Giới hạn 1 MB khi nhập nhỏ hơn bộ nhớ trình duyệt.** `policy-security@1#S1` giới hạn file nhập 1 MB, còn bộ nhớ trình duyệt
  khoảng 5 MB [app/store.js]. Khách có danh sách lớn sẽ sao lưu được nhưng không nhập lại được: bản sao lưu vô dụng, trái
  `policy-ux@1#U1`. Phương án: (a) khi sao lưu mà file > 1 MB thì báo trước ngay lúc sao lưu; (b) Khoa nâng giới hạn S1. → Khoa
  (security owner), Linh (UX owner).
- **C4 · Dữ liệu hỏng bị ghi đè không báo.** `store.load` trả về danh sách trống khi đọc lỗi, lần lưu sau sẽ ghi đè dữ liệu hỏng
  [app/store.js]. Đây là mất dữ liệu không báo theo `policy-ux@1#U1`, nhưng intent chỉ nói tới lỗi khi lưu [intent], nên spec không
  thiết kế phần này. Có đưa vào phạm vi lần này không? → product owner, Khoa (tech lead).

## Acceptance criteria
1. Có 3 việc (1 đã xong). Bấm sao lưu → trình duyệt tải về một file; mở bằng trình soạn văn bản thấy đúng 3 tiêu đề, trạng thái xong
   đúng, và không có trường nào ngoài `version`, `todos`, `id`, `title`, `done`, `createdAt`.
2. Mạng tắt hoàn toàn, bấm sao lưu vẫn ra file; công cụ Network của trình duyệt không ghi request nào khi sao lưu hay nhập.
3. Xoá dữ liệu trang, mở lại app → thấy dòng trạng thái trống chỉ tới nút nhập từ file. Nhập file ở tiêu chí 1 → thấy đủ 3 việc,
   đúng trạng thái; tải lại trang vẫn còn đủ 3 việc.
4. Nhập file lớn hơn 1 MB → bị từ chối, danh sách không đổi, thấy thông báo trên cùng màn hình.
5. Nhập file có thêm một trường lạ ở một việc (ví dụ `"x": 1`) → bị từ chối, danh sách không đổi, thấy thông báo.
6. Nhập file không đúng dạng (ảnh, file văn bản bất kỳ) → bị từ chối, danh sách không đổi, thấy thông báo.
7. Nhập file có tiêu đề `<img src=x onerror=alert(1)>` → tiêu đề hiện đúng nguyên chữ đó, không có hộp alert.
8. Làm đầy bộ nhớ trình duyệt (ví dụ ghi khoá khác tới khi lỗi), rồi thêm một việc → thấy thông báo trên cùng màn hình nói việc chưa
   được lưu và gợi ý làm tiếp; console không còn là nơi duy nhất báo lỗi.
9. Trên màn hình chính có dòng chữ nói danh sách chỉ giữ trên trình duyệt này và mất khi xoá dữ liệu trình duyệt hoặc đổi máy.
10. Mọi chữ mới trong app không chứa "localStorage", "JSON", "console".
11. Chỉ dùng bàn phím (Tab, Enter/Space): sao lưu được và chọn file nhập được; trình đọc màn hình đọc được nhãn hai nút và đọc thông
    báo lỗi.
12. `app/index.html` không có thêm `<script>` hay `<link>` trỏ ra ngoài.
13. Nhập khi danh sách đang có việc: tiêu chí viết sau khi C1 được quyết.

## Questions carried forward from the intent
- Chép 23 email (đã bỏ thông tin cá nhân) vào `tickets/` để người duyệt kiểm được con số không? → Lan
- Trong 23 email, bao nhiêu email là do đổi điện thoại, bao nhiêu là do xoá dữ liệu trình duyệt? → Lan (đếm lại email)
