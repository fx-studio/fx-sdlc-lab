# Spec: Sao lưu ra file, nhập lại, và báo khi không lưu được

From: intent/2026-10-19-khach-khong-mat-viec.md · Skills: policy-privacy@1, policy-security@1, policy-ux@2 · Status: accepted · Risk: high (risk-list dòng 1: "personal data leaving the user's device") · Date: 2026-10-27

## Goal
Khách không mất việc nữa [intent]. Lần này khách tự sao lưu danh sách ra một file và nhập lại được, và khách được báo khi việc không
lưu được vì bộ nhớ đầy [intent]. Khách cũng được báo khi danh sách đã lưu trong trình duyệt không đọc được, và app không ghi đè lên
nó [answer C3, Thảo · Khoa]. Đổi điện thoại mới hoặc xoá dữ liệu trình duyệt vẫn thấy đủ việc **khi đã sao lưu trước** [answer C1,
Thảo]. Đồng bộ hai máy ("máy này thêm thì máy kia thấy") để intent đồng bộ sau [intent] [answer C1, Thảo].

Mốc đo sau khi ra bản mới (đo bằng email, không phải tiêu chí nghiệm thu của spec này): email than mất việc giảm từ 23 email / 2 tuần
xuống dưới 5 email / 2 tuần, trong 6 tuần sau khi ra bản mới [intent]. Không còn lần lưu lỗi nào mà khách không được báo [intent].

## Out of scope
- Lấy lại việc đã mất cho 23 khách đã email: dữ liệu chưa từng rời máy họ [intent]
- Đồng bộ nhiều máy, tài khoản đăng nhập, nhiều người dùng chung danh sách [intent]
- Hạn chót cho việc: intent riêng T-012 [intent]
- Chuyển file sao lưu sang máy mới: khách tự gửi qua Zalo, email; app không làm bước này [answer A1, Thảo].
- Gộp danh sách trong file với danh sách đang có: nhập là thay toàn bộ [answer A2, Thảo].
- Khôi phục dữ liệu hỏng trong trình duyệt: spec chỉ không ghi đè và báo cho khách (F5) [answer C3, Thảo · Khoa].
- Spec này không đổi các thao tác trên một việc đang có (thêm, đánh dấu xong, xoá) [app/app.js]. Nút xoá một việc chưa có Undo 10
  giây như `policy-ux@2#U2` yêu cầu; chỗ lệch U2 này **còn mở** và để một intent riêng, Thảo nhận việc mở intent đó [answer C4,
  Linh · Thảo].
- Không lưu dữ liệu ở đâu khác ngoài trình duyệt của khách [intent], nên `policy-privacy@1#P5` không áp dụng.

## User flows

### F1 · Sao lưu ra file
1. Khách bấm nút "Sao lưu ra file" [intent].
2. App tạo một file chứa toàn bộ danh sách việc hiện có, mỗi việc gồm id, tiêu đề, trạng thái xong, thời điểm tạo [intent] [app/app.js],
   và trình duyệt tải file về máy với tên `todo-sao-luu-<YYYY-MM-DD>.json` [intent] [answer A11, Linh · Thảo]. File chỉ được tạo khi
   khách bấm và không gửi đi đâu [policy-privacy@1#P1].
3. App báo trên cùng màn hình đã sao lưu bao nhiêu việc [policy-ux@2#U1] [policy-ux@2#U4].
4. Danh sách trống: nút vẫn bấm được, app **không** tạo file và báo "Chưa có việc nào để sao lưu" [answer A6, Thảo].
5. File sao lưu lớn hơn 1 MB (giới hạn nhập của `policy-security@1#S1`): app vẫn tạo và tải file về như bước 2, và báo ngay trên cùng
   màn hình, nguyên văn [answer C2, Khoa · Linh · Thảo]:
   **"File sao lưu đã lưu, nhưng quá lớn nên app không nhập lại được."**

### F2 · Nhập lại từ file
1. Khách bấm nút "Nhập từ file" và chọn một file [intent].
2. Trong lúc đọc file, app hiện trạng thái đang đọc [policy-ux@2#U3].
3. App kiểm file trước khi đụng tới danh sách đang có [policy-security@1#S1]:
   - file lớn hơn 1 MB → từ chối [policy-security@1#S1];
   - nội dung không đúng cấu trúc ở mục Data and integrations, hoặc có trường lạ → từ chối [policy-security@1#S1];
   - có hai việc trùng `id`, một việc có tiêu đề rỗng, hoặc `createdAt` không phải số → từ chối **cả file**, không nhập một phần
     [answer A7, Khoa];
   - nội dung chỉ được đọc như dữ liệu, không bao giờ được chạy [policy-security@1#S1].
4. Khi từ chối: danh sách đang có giữ nguyên, app báo trên cùng màn hình bằng lời thường vì sao không nhập được và khách làm gì tiếp
   [policy-ux@2#U1] [policy-ux@2#U4].
5. Nhập là thay toàn bộ danh sách hiện có bằng danh sách trong file, không gộp [answer A2, Thảo].
6. File hợp lệ, danh sách đang trống: app thay ngay bằng các việc trong file và lưu lại, không hỏi xác nhận, vì không việc nào bị thay
   hay xoá [policy-security@1#S2]. App báo đã nhập bao nhiêu việc [policy-ux@2#U1].
7. File hợp lệ, danh sách đang có **từ 1 việc trở lên**: **trước khi** thay, app luôn hỏi xác nhận và nói rõ mất gì, theo mẫu
   "Thay 12 việc hiện có bằng 30 việc trong file?" [policy-security@1#S2]. Nhập file thay cả danh sách nên là thao tác trên danh sách,
   không phải thao tác trên một việc theo U2; vì vậy đúng 1 việc cũng hỏi ("Thay 1 việc hiện có bằng 30 việc trong file?") và không
   có Undo sau khi nhập [answer A3, Khoa · Linh] [policy-ux@2#U2].
   - Khách đồng ý → app thay danh sách và lưu lại, rồi báo đã nhập bao nhiêu việc [policy-security@1#S2] [policy-ux@2#U1].
   - Khách huỷ → danh sách giữ nguyên, không có gì được ghi [policy-security@1#S2].
   - Hộp xác nhận là `<dialog>` có sẵn của trình duyệt, dùng được bằng bàn phím, có nhãn cho trình đọc màn hình [policy-ux@2#U5]
     [answer A10, Linh].
8. Nếu lưu sau khi nhập bị lỗi: danh sách cũ được giữ nguyên trên màn hình và trong bộ nhớ, app báo bằng câu riêng cho lúc nhập, đúng
   cả khi danh sách trên màn hình còn phần chưa lưu [policy-ux@2#U1] [sửa R9: Linh, Thảo, Khoa, Mai].
9. Nhập khi danh sách đã lưu không đọc được: xem F5 bước 6 [answer A15, Khoa · Thảo].

### F3 · Báo khi không lưu được
1. Khách thêm, đánh dấu xong hoặc xoá một việc [app/app.js]; mỗi thao tác đều ghi lại cả danh sách [app/app.js] [app/store.js].
2. Nếu ghi lỗi (ví dụ bộ nhớ đầy, khoảng 5 MB ở đa số trình duyệt [app/store.js]): thay vì chỉ ghi ra console như hiện nay
   [app/store.js], app hiện thông báo trên cùng màn hình, bằng lời thường, nói thay đổi vừa rồi chưa được lưu và khách làm gì tiếp được
   [intent] [policy-ux@2#U1] [policy-ux@2#U4]. Lời gợi ý là "Hãy sao lưu ra file, rồi xoá bớt việc đã xong" [answer A8, Linh].
3. Thay đổi vừa làm vẫn hiện trên màn hình (chưa lưu) cho tới lần lưu thành công sau; tải lại trang thì mất thay đổi chưa lưu, điều
   này được chấp nhận [answer A9, Khoa].

### F4 · Cho khách biết việc được giữ ở đâu
1. Trên màn hình chính, app ghi bằng lời thường rằng danh sách chỉ được giữ trên trình duyệt này; xoá dữ liệu trang web, đổi trình
   duyệt hoặc đổi máy là mất danh sách, trừ khi đã sao lưu ra file [policy-privacy@1#P4] [app/store.js].
2. Lời này không dùng từ kỹ thuật [policy-ux@2#U4].

### F5 · Danh sách đã lưu không đọc được
1. Khi mở app, nếu đọc danh sách trong bộ nhớ trình duyệt bị lỗi, app **không ghi đè** dữ liệu đó và báo cho khách trên cùng màn hình
   [answer C3, Thảo · Khoa] [policy-ux@2#U1]. Hiện nay `store.load` trả về danh sách trống và lần lưu sau ghi đè dữ liệu hỏng mà không
   báo [app/store.js].
2. App không sửa, không khôi phục, không chép dữ liệu hỏng sang chỗ khác [answer C3, Thảo · Khoa].
3. "Đọc lỗi" là một trong ba trường hợp [answer A13, Khoa]:
   - khoá `todo.v1` có dữ liệu nhưng không đọc được;
   - khoá `todo.v1` đọc được nhưng không phải một mảng;
   - truy cập bộ nhớ trình duyệt ném lỗi.

   Chưa có khoá `todo.v1` là danh sách trống bình thường, không báo lỗi [answer A13, Khoa].
4. Lời báo là một dải báo cố định trên cùng màn hình, không bật hộp thoại mỗi lần khách thêm, đánh dấu xong hay xoá [answer A14, Linh].
   Nguyên văn [answer A16, Linh]:
   **"Không đọc được danh sách đã lưu trên trình duyệt này. Việc bạn thêm hoặc sửa lúc này sẽ không được lưu. Nếu có file sao lưu, hãy bấm "Nhập từ file"."**
5. Trong lúc đọc lỗi, app không ghi gì vào `todo.v1`: việc khách thêm, đánh dấu xong hay xoá vẫn hiện trên màn hình nhưng không được
   lưu, tải lại trang thì mất, điều này được chấp nhận [answer A14, Khoa · Linh] [answer A9, Khoa]. Sao lưu ra file (F1) vẫn dùng được
   và lấy các việc đang hiện trên màn hình, để khách kịp sao lưu [answer A14, Khoa].
6. Nhập từ file là cách duy nhất thay dữ liệu hỏng [answer A15, Khoa · Thảo]. File vẫn được kiểm như F2 bước 3 [answer A15, Khoa].
   **Trước khi** thay, app luôn hỏi xác nhận bằng hộp xác nhận của F2 bước 7 [answer A15, Khoa · Thảo] [policy-security@1#S2]:
   - Trên màn hình chưa có việc nào: theo mẫu "Thay danh sách đã lưu không đọc được bằng 30 việc trong file?" [answer A15, Khoa ·
     Thảo] [answer A19, Khoa].
   - Trên màn hình có việc chưa lưu (khách thêm trong lúc đọc lỗi, F5 bước 5): lời xác nhận nêu số lượng, nguyên văn mẫu của Khoa
     [answer A19, Khoa]:
     **"Thay danh sách đã lưu không đọc được và 3 việc bạn vừa thêm (chưa lưu) bằng 30 việc trong file?"**
     Trong lúc đọc lỗi mọi việc trên màn hình đều chưa lưu (F5 bước 5), nên con số là số việc đang hiện trên màn hình [answer A14,
     Khoa · Linh] [answer A19, Khoa].
   - Khách huỷ → không có gì được ghi, dữ liệu hỏng giữ nguyên [policy-security@1#S2] [answer C3, Thảo · Khoa].
   - Khách đồng ý → app ghi danh sách trong file vào `todo.v1`, thay dữ liệu hỏng [answer A15, Khoa · Thảo].
7. Ghi ở bước 6 thành công: app thoát trạng thái đọc lỗi, dải báo F5 biến mất, và từ đó thêm, đánh dấu xong, xoá được lưu bình thường
   như F3 [answer A17, Khoa · Linh].
8. Ghi ở bước 6 thất bại: app vẫn ở trạng thái đọc lỗi, dải báo F5 vẫn hiện, các bước 4–6 vẫn áp dụng [answer A17, Khoa · Linh].
   Màn hình hiện gì và có thêm thông báo F3 không: xem Assumptions (A20).

### Trạng thái màn hình
- Trống: khi danh sách không có việc nào, app hiện một dòng nói chưa có việc và chỉ tới nút "Nhập từ file" [policy-ux@2#U3]. Hiện nay
  danh sách trống không hiện gì [app/app.js]. Đọc lỗi mà chưa có việc nào trên màn hình: app chỉ hiện dải báo F5, **không** hiện dòng
  trạng thái trống, vì dòng đó nói như thể danh sách trống thật [answer A18, Linh].
- Đang đọc: F2 bước 2 [policy-ux@2#U3].
- Lỗi: F2 bước 4, F2 bước 8, F3 bước 2 và dải báo F5 bước 4 [policy-ux@2#U3].
- Mọi thông báo (kết quả và lỗi) đặt trong một vùng `role="status"` / `aria-live` để trình đọc màn hình đọc lên [policy-ux@2#U5]
  [answer A10, Linh].

## Data and integrations
- Bộ nhớ trình duyệt: giữ nguyên khoá `todo.v1` và cấu trúc hiện có, một mảng việc [app/store.js]. Spec này không thêm khoá, không thêm
  trường vào bộ nhớ trình duyệt [app/store.js]. Nhập file không có Undo, nên không cần giữ danh sách cũ trong bộ nhớ trình duyệt
  [answer A3, Khoa · Linh]. Trạng thái "đọc lỗi" ở F5 chỉ giữ trong bộ nhớ của trang, không ghi vào bộ nhớ trình duyệt [answer A12,
  Khoa].
- Một việc gồm `id` (chuỗi), `title` (chuỗi), `done` (đúng/sai), `createdAt` (số mili giây) [app/app.js].
- File sao lưu: JSON thụt lề, là văn bản thường, mở ra đọc được [policy-privacy@1#P3] [answer A4, Mai]. Cấu trúc chỉ gồm
  `{ "version": 1, "todos": [ … ] }`, mỗi việc đúng bốn trường trên; `version` và `id` do app tự sinh, không vi phạm
  `policy-privacy@1#P2` [answer A5, Mai]. Không có định danh thiết bị hay dấu vết trình duyệt [policy-privacy@1#P2].
- Tên file: `todo-sao-luu-<YYYY-MM-DD>.json`, ngày là ngày sao lưu; đuôi `.json` do hệ điều hành hiển thị, không tính là chữ trong app
  theo U4 [answer A11, Linh · Thảo].
- Kiểm file khi nhập: đúng cấu trúc trên, không có trường lạ, tối đa 1 MB, không chạy nội dung [policy-security@1#S1]; trùng `id`,
  tiêu đề rỗng, `createdAt` không phải số → từ chối cả file [answer A7, Khoa]. Kiểm như vậy cả khi đang đọc lỗi [answer A15, Khoa].
- `store.save` phải cho nơi gọi biết ghi thành công hay lỗi; hiện nó nuốt lỗi và chỉ ghi ra console [app/store.js].
- `store.load` phải cho nơi gọi phân biệt "chưa có dữ liệu" với "đọc lỗi" theo ba trường hợp ở F5 bước 3; hiện cả hai đều trả về danh
  sách trống [app/store.js] [answer C3, Thảo · Khoa] [answer A13, Khoa].
- Trong lúc đọc lỗi, chỉ đường nhập file đã được khách đồng ý (F5 bước 6) được ghi vào `todo.v1` [answer A14, Khoa · Linh]
  [answer A15, Khoa · Thảo]. Trạng thái "đọc lỗi" trong bộ nhớ của trang chỉ được xoá khi lần ghi đó thành công; ghi thất bại thì giữ
  nguyên [answer A17, Khoa · Linh].
- Tiêu đề việc, kể cả việc vừa nhập từ file, hiển thị bằng `textContent` [policy-security@1#S3]; `render` đã làm vậy cho tiêu đề
  [app/app.js].
- Không thêm thư viện, CDN hay dịch vụ ngoài [policy-security@1#S4]. Nút nhập dùng `<input type="file">` có nhãn, hộp xác nhận dùng
  `<dialog>`, thông báo dùng vùng `role="status"` / `aria-live`, đều có sẵn trong trình duyệt [answer A10, Linh].
- Risk-list dòng 2 ("changes the shape of stored data") **không khớp**: file sao lưu nằm ngoài trình duyệt và spec không thêm khoá hay
  trường nào vào bộ nhớ trình duyệt [answer A12, Khoa]. Nếu bản sau thêm (ví dụ giữ danh sách cũ để Undo), dòng 2 khớp và `Risk` phải
  ghi thêm dòng 2 [answer A12, Khoa]. Dòng 1 vẫn khớp vì dữ liệu của khách rời trình duyệt ra file [intent].
- Các file sửa: `app/store.js`, `app/app.js`, `app/index.html`, `app/style.css` [app/].

## Policy constraints
- policy-privacy@1#P1 → file chỉ được tạo khi khách bấm sao lưu, không gửi đi đâu; nhập chỉ đọc file khách tự chọn (F1, F2).
- policy-privacy@1#P2 → file chỉ chứa `version` và bốn trường của việc; Mai xác nhận ở A5.
- policy-privacy@1#P3 → file JSON thụt lề, văn bản thường; Mai xác nhận ở A4.
- policy-privacy@1#P4 → dòng chữ ở F4.
- policy-privacy@1#P5 → không áp dụng: không lưu ngoài trình duyệt; F5 không chép dữ liệu hỏng đi đâu.
- policy-security@1#S1 → F2 bước 3: giới hạn 1 MB, kiểm cấu trúc, từ chối trường lạ, không chạy nội dung. Giữ 1 MB theo C2 (a). Áp
  dụng cả khi đọc lỗi (F5 bước 6, A15).
- policy-security@1#S2 → F2 bước 7: hỏi xác nhận trước khi thay danh sách đang có từ 1 việc trở lên (chặt hơn mức "more than one item"
  của S2, Khoa chốt ở A3), lời xác nhận nói số việc bị thay. Khi đọc lỗi (F5 bước 6): luôn hỏi, lời xác nhận nói thứ bị thay là "danh
  sách đã lưu không đọc được" vì không đếm được số việc; Khoa và Thảo chốt ở A15. Nếu trên màn hình có việc chưa lưu, lời xác nhận
  nêu thêm số việc đó; Khoa (owner S2) chốt ở A19.
- policy-security@1#S3 → tiêu đề hiển thị bằng `textContent`.
- policy-security@1#S4 → không thêm phụ thuộc ngoài.
- policy-ux@2#U1 → F1 bước 3–5, F2 bước 4, 6, 7 và 8, F3 bước 2, F5 bước 4 (dải báo nói rõ việc làm lúc này không được lưu và chỉ tới
  "Nhập từ file"). Danh sách lớn hơn 1 MB được báo ngay lúc sao lưu (F1 bước 5).
- policy-ux@2#U2 → nhập file là thao tác trên danh sách, theo S2 như U2 bản 2 quy định, không có Undo (F2 bước 7, F5 bước 6, A3);
  spec không thêm thao tác nào trên một việc. Nút xoá một việc chưa có Undo: lệch U2 còn mở, để intent riêng (C4).
- policy-ux@2#U3 → mục Trạng thái màn hình; trạng thái lỗi gồm dải báo F5; đọc lỗi thì không hiện trạng thái trống (A18).
- policy-ux@2#U4 → mọi lời mới trong app bằng tiếng Việt, ngắn, không có từ kỹ thuật; đuôi `.json` không tính (A11). Lời báo F5 bỏ chữ
  "ghi đè" vì nghe kỹ thuật [answer A16, Linh].
- policy-ux@2#U5 → nút sao lưu, nút nhập từ file và hộp xác nhận dùng được bằng bàn phím và có nhãn; thông báo, kể cả dải báo F5,
  trong vùng `role="status"` (A10).

## Assumptions
A1–A19 đã được trả lời và nằm trong thân spec với nguồn `[answer A<n>, <tên>]` [demo/sdlc-3/tra-loi-gia-dinh.md]. Dòng dưới đây
mới, sinh ra khi đưa câu trả lời A17 vào F5 (nhánh ghi thất bại):

- A20. Đọc lỗi, khách đồng ý nhập file nhưng ghi thất bại (F5 bước 8): giống F2 bước 8, màn hình vẫn hiện các việc đang có trước khi
  nhập (không hiện 30 việc trong file), và app hiện thêm thông báo không lưu được của F3 bên cạnh dải báo F5, đúng không? → Khoa
  (tech lead), Linh (UX owner)
  **Trả lời (người chạy demo ghi, 2026-10-27): Có** [answer A20, Khoa · Linh] (`demo/sdlc-3/runs/B0l-*`)

## Concerns
- **C1 · Tiêu chí thành công của intent không khớp phạm vi.** **Đã quyết:** chấp nhận [answer C1, Thảo]. Tiêu chí "máy này thêm thì
  máy kia thấy" chuyển sang intent đồng bộ sau; hai tiêu chí đổi máy / xoá dữ liệu ghi rõ "khi đã sao lưu trước" (mục Goal). Spec này
  không sửa `intent/`; câu chữ trong intent vẫn là bản cũ, sửa intent là việc của người.
- **C2 · Giới hạn 1 MB khi nhập nhỏ hơn bộ nhớ trình duyệt.** **Đã quyết:** phương án (a), giữ S1 ở 1 MB, sao lưu vẫn tạo file và báo
  ngay bằng câu Linh duyệt (F1 bước 5) [answer C2, Khoa · Linh · Thảo]. Linh thiên về (b) nhưng để Khoa (owner S1) quyết [answer C2,
  Linh]. Khách có file lớn hơn 1 MB vẫn chưa có bản sao lưu nhập lại được; Khoa chấp nhận điều này [demo/sdlc-3/runs/B0b-khoa-tra-loi].
- **C3 · Dữ liệu hỏng bị ghi đè không báo.** **Đã quyết:** đưa vào lần này, phạm vi hẹp: không ghi đè, báo cho khách, không khôi phục
  (F5) [answer C3, Thảo · Khoa]. Khoa xác nhận vẫn vừa hai tuần [answer C3, Khoa]. A13–A19 đã trả lời và nằm trong F5; còn mở A20.
- **C4 · Thao tác trên một việc chưa có Undo 10 giây.** **Đã quyết:** để intent riêng (Undo cho nút xoá một việc); chỗ lệch
  `policy-ux@2#U2` còn mở; Thảo nhận việc mở intent đó [answer C4, Linh · Thảo]. Lưu ý cho người duyệt: khi trả lời A14, Linh viết
  "Undo 10 giây vẫn chạy như bình thường" [demo/sdlc-3/runs/B0g-linh-gia-dinh-moi], nhưng app hiện chưa có Undo [app/app.js]; spec
  này không thêm Undo. Câu "Có" của Linh ở A14 không phụ thuộc vào Undo, nên spec giữ nguyên A14.

## Acceptance criteria
1. Có 3 việc (1 đã xong). Bấm "Sao lưu ra file" → trình duyệt tải về một file tên `todo-sao-luu-<ngày hôm đó, YYYY-MM-DD>.json`; mở
   bằng trình soạn văn bản thấy văn bản thụt lề, đúng 3 tiêu đề, trạng thái xong đúng, và không có trường nào ngoài `version`, `todos`,
   `id`, `title`, `done`, `createdAt`. Màn hình báo đã sao lưu 3 việc.
2. Tắt mạng hoàn toàn, bấm sao lưu vẫn ra file; công cụ Network của trình duyệt không ghi request nào khi sao lưu hay nhập.
3. Xoá dữ liệu trang, mở lại app → thấy dòng trạng thái trống chỉ tới nút "Nhập từ file", không có dải báo đọc lỗi. Nhập file ở tiêu
   chí 1 → không có hộp xác nhận, thấy đủ 3 việc, đúng trạng thái; tải lại trang vẫn còn đủ 3 việc.
4. Danh sách trống, bấm "Sao lưu ra file" → không có file nào được tải về; màn hình báo "Chưa có việc nào để sao lưu".
5. Có 12 việc, nhập một file hợp lệ có 30 việc → trước khi danh sách đổi, hiện hộp xác nhận có chữ "Thay 12 việc hiện có bằng 30 việc
   trong file?". Bấm huỷ → vẫn đúng 12 việc cũ, tải lại trang vẫn 12 việc cũ. Làm lại, bấm đồng ý → thấy đúng 30 việc trong file, không
   còn việc nào trong 12 việc cũ, không có nút Undo; tải lại trang vẫn 30 việc đó.
6. Có đúng 1 việc, nhập một file hợp lệ có 30 việc → trước khi danh sách đổi, hiện hộp xác nhận có chữ "Thay 1 việc hiện có bằng 30
   việc trong file?". Bấm huỷ → vẫn đúng 1 việc cũ. Làm lại, bấm đồng ý → thấy 30 việc; tải lại trang vẫn 30 việc đó.
7. Nhập file lớn hơn 1 MB → bị từ chối, danh sách không đổi, thấy thông báo trên cùng màn hình.
8. Nhập file có thêm một trường lạ ở một việc (ví dụ `"x": 1`) → bị từ chối, danh sách không đổi, thấy thông báo.
9. Nhập file không đúng dạng (ảnh, file văn bản bất kỳ) → bị từ chối, danh sách không đổi, thấy thông báo.
10. Nhập lần lượt ba file hợp lệ trừ một chỗ: (a) hai việc trùng `id`, (b) một việc có `title` là `""`, (c) một việc có `createdAt` là
    `"hôm qua"` → cả ba bị từ chối, danh sách không đổi, không việc nào trong file được nhập, thấy thông báo.
11. Nhập file có tiêu đề `<img src=x onerror=alert(1)>` → tiêu đề hiện đúng nguyên chữ đó, không có hộp alert.
12. Có đủ việc để file sao lưu lớn hơn 1 MB (ví dụ 5.000 việc, mỗi tiêu đề 200 ký tự), bấm "Sao lưu ra file" → file vẫn được tải về và
    lớn hơn 1 MB; màn hình hiện đúng câu "File sao lưu đã lưu, nhưng quá lớn nên app không nhập lại được."
13. Làm đầy bộ nhớ trình duyệt (ví dụ ghi khoá khác tới khi lỗi), rồi thêm một việc → thấy thông báo trên cùng màn hình nói thay đổi chưa
    được lưu, kèm câu "Hãy sao lưu ra file, rồi xoá bớt việc đã xong"; việc vừa thêm vẫn hiện trên màn hình. Tải lại trang → việc đó
    không còn.
14. Làm đầy bộ nhớ như tiêu chí 13, có 12 việc, nhập file 30 việc và đồng ý → thấy thông báo lỗi; tải lại trang vẫn đúng 12 việc cũ.
15. Ghi tay giá trị `{hỏng` vào khoá `todo.v1` (công cụ của trình duyệt), mở lại app → thấy dải báo trên cùng màn hình với đúng câu
    "Không đọc được danh sách đã lưu trên trình duyệt này. Việc bạn thêm hoặc sửa lúc này sẽ không được lưu. Nếu có file sao lưu, hãy
    bấm "Nhập từ file"."; không thấy dòng trạng thái trống; giá trị của `todo.v1` vẫn là `{hỏng`. Thêm hai việc, đánh dấu xong một
    việc, xoá một việc → không có hộp thoại nào bật lên, dải báo vẫn hiện, việc còn lại hiện đúng trạng thái trên màn hình; giá trị của
    `todo.v1` vẫn là `{hỏng`; công cụ của trình duyệt không thấy khoá mới nào của app. Tải lại trang → không thấy việc nào vừa thêm,
    dải báo vẫn hiện.
16. Ghi tay giá trị `{"a": 1}` (đọc được nhưng không phải mảng) vào khoá `todo.v1`, mở lại app → thấy dải báo như tiêu chí 15; thêm một
    việc → giá trị của `todo.v1` vẫn là `{"a": 1}`.
17. Trong một bài test, cho việc đọc bộ nhớ trình duyệt ném lỗi khi app mở → thấy dải báo như tiêu chí 15, và app không ghi gì vào bộ
    nhớ trình duyệt khi thêm một việc.
18. Đọc lỗi như tiêu chí 15, thêm hai việc, bấm "Sao lưu ra file" → file được tải về, có đúng hai việc đó; giá trị của `todo.v1` vẫn là
    `{hỏng`.
19. Đọc lỗi như tiêu chí 15 (chưa thêm việc nào), nhập một file hợp lệ có 30 việc → trước khi danh sách đổi, hiện hộp xác nhận có chữ
    "Thay danh sách đã lưu không đọc được bằng 30 việc trong file?". Bấm huỷ → giá trị của `todo.v1` vẫn là `{hỏng`, dải báo vẫn hiện.
    Làm lại, bấm đồng ý → thấy đúng 30 việc trong file, dải báo đọc lỗi biến mất. Thêm một việc, tải lại trang → thấy 31 việc (30 việc
    trong file và việc vừa thêm), không có dải báo.
20. Đọc lỗi như tiêu chí 15, thêm ba việc, nhập một file hợp lệ có 30 việc → trước khi danh sách đổi, hiện hộp xác nhận có đúng chữ
    "Thay danh sách đã lưu không đọc được và 3 việc bạn vừa thêm (chưa lưu) bằng 30 việc trong file?". Bấm huỷ → vẫn thấy ba việc
    đó, dải báo vẫn hiện, giá trị của `todo.v1` vẫn là `{hỏng`. Làm lại, bấm đồng ý → thấy đúng 30 việc trong file, không còn việc nào
    trong ba việc vừa thêm, dải báo biến mất; tải lại trang vẫn 30 việc đó.
21. Ghi tay `{hỏng` vào `todo.v1`, rồi làm đầy bộ nhớ trình duyệt như tiêu chí 13; mở lại app, nhập một file hợp lệ có 30 việc và đồng ý
    → dải báo đọc lỗi vẫn hiện, giá trị của `todo.v1` vẫn là `{hỏng`. Thêm một việc → giá trị của `todo.v1` vẫn là `{hỏng`.
22. Đọc lỗi như tiêu chí 15, nhập lần lượt file ở tiêu chí 7 và tiêu chí 8 → cả hai bị từ chối, không có hộp xác nhận, giá trị của
    `todo.v1` vẫn là `{hỏng`, dải báo vẫn hiện.
23. Trên màn hình chính có dòng chữ nói danh sách chỉ giữ trên trình duyệt này và mất khi xoá dữ liệu trang web hoặc đổi máy, trừ khi
    đã sao lưu ra file.
24. Mọi chữ mới trong app không chứa "localStorage", "JSON", "console".
25. Chỉ dùng bàn phím (Tab, Enter/Space, Esc): sao lưu được, chọn file nhập được, đồng ý và huỷ được hộp xác nhận; trình đọc màn hình
    đọc được nhãn hai nút, nội dung hộp xác nhận, các thông báo và dải báo đọc lỗi.
26. `app/index.html` không có thêm `<script>` hay `<link>` trỏ ra ngoài.

## Questions carried forward from the intent
- Chép 23 email (đã bỏ thông tin cá nhân) vào `tickets/` để người duyệt kiểm được con số không? → Lan
- Trong 23 email, bao nhiêu email là do đổi điện thoại, bao nhiêu là do xoá dữ liệu trình duyệt? → Lan (đếm lại email)

## Revisions after acceptance
- 2026-10-27 · F4 bước 1, tiêu chí 23: "dữ liệu trình duyệt" → "dữ liệu trang web", theo câu trên app (Linh chốt, Mai xác nhận đạt P4)
  [demo/sdlc-3/runs/R3c-*, R9-*]. F2 bước 8: câu riêng cho lúc nhập lỗi khi lưu, thay "báo như F3" (Linh đề xuất, Thảo đồng ý; Khoa nêu
  ca đã có phần chưa lưu, Linh chọn một câu đúng cho cả hai ca; Mai: không đụng policy riêng tư) [R9-*]. Người sửa và commit: Thảo.
