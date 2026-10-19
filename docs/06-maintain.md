# Phase 6 · Maintain: khép vòng lặp

> Thuộc bộ tài liệu đọc *The AI-native SDLC playbook* (Anthropic, 21/8/2026). Xem [tổng quan](00-tong-quan.md).

---

## Tóm gọn

Đây là phase biến đường thẳng thành vòng lặp. Một điểm kích hoạt gọi Claude mà không cần người khởi động. Claude chẩn đoán, chỉ hành động qua các đường đã có cổng, và ghi những gì tìm thấy thành `intent.md` mới. File đó quay lại [Phase 1](01-plan.md) như mọi ý tưởng khác.

Phase này có ba play: **khép vòng bằng ngưỡng giám sát**, **scan codebase định kỳ**, và **Claude trực sự cố qua Claude Tag**.

---

## 1. Vấn đề của cách cũ

Vận hành là giai đoạn bị động. Mọi ticket và sự cố đều chờ một người nhận rồi mới bắt đầu lại quy trình:

- Cảnh báo lúc 3 giờ sáng có thể bị bỏ lỡ.
- Ticket nằm trong backlog tới khi có người để ý.
- Việc cần làm sau post-mortem có khi không bao giờ đến được codebase, vì đã có sự cố mới.

Scan bảo mật cũng bị động theo kiểu khác: nó là một sự kiện. Chạy trước release hoặc trước audit, báo cáo đưa vào tracker, rồi xử lý dần tới lần scan sau. Code viết ra ở giữa hai lần scan chỉ được bảo vệ bởi những gì review PR bắt được.

---

## 2. Playbook xử lý thế nào

### 2.1. Khép vòng bằng ngưỡng giám sát

Ở các phase trước, mỗi stage đều cần người khởi động. Phase này chuyển sang chạy tự động.

Ý tưởng: một agent giám sát liên tục, khi có bug được báo, tự tạo `intent.md` rồi đi tiếp qua requirements, plan, build, test, review. Giữa các stage có **một cổng tin cậy độc lập**, có thể là một phép kiểm cố định hoặc một agent review đối kháng, quyết định cho đi tiếp hay chuyển lên người.

#### Cơ chế phát hiện

Điểm cần lưu ý trong thiết kế này: **khâu phát hiện hoàn toàn không dùng model.**

1. Chọn một chỉ số có baseline ổn định, ví dụ tỉ lệ test fail trong CI, tỉ lệ lỗi 5xx sau deploy, thời gian vòng đời PR.
2. Viết script phát hiện: trung bình và độ lệch chuẩn trên một cửa sổ trượt, kèm các luật như Western Electric để bắt cả trôi chậm lẫn đột biến. Script có quản lý phiên bản và có unit test.
3. Định nghĩa các mức phản ứng trong file cấu hình, ví dụ `bands.yaml`:

| Mức lệch | Phản ứng |
|---|---|
| 1σ | Chỉ ghi log |
| 2σ | Gọi Claude ở chế độ chỉ đọc để chẩn đoán |
| 3σ | Claude được hành động, nhưng chỉ qua hai đường: mở PR vào cổng review, hoặc chạy runbook đã duyệt trước (như rollback) |

4. Điểm kích hoạt có thể là workflow chạy theo lịch, webhook từ hệ thống giám sát, hoặc cron trong mạng nội bộ. Claude chạy không trạng thái, không tương tác, trên CI runner hoặc qua Agent SDK trong container có sandbox. Vòng lặp vì vậy bắt đầu và kết thúc mà không ai phải khởi động.
5. Agent ghi chẩn đoán thành `intent.md` theo đúng format Phase 1: bất thường và bằng chứng, kết quả đề xuất, hệ thống bị ảnh hưởng, câu hỏi mở.
6. Người trực hoặc service owner phân loại hàng đợi: sửa ngay, xếp lịch, hay bỏ qua. **Việc bỏ qua được dùng để chỉnh lại ngưỡng**, giảm nhiễu.
7. Khi bản sửa đã lên, thêm một eval cho sự cố đó (xem [Phase 4](04-test.md)).

Ba ví dụ trong playbook:
- Tỉ lệ test fail trong CI vượt 3σ → agent cách ly test chập chờn hoặc mở PR revert, cổng review quyết định.
- Tỉ lệ 5xx sau deploy vượt 3σ, có deploy trong khung thời gian đó → agent kích hoạt pipeline rollback có sẵn.
- Thời gian vòng đời PR trôi dần → agent viết báo cáo cho lãnh đạo engineering. Ví dụ này cho thấy cơ chế dùng được cho cả chỉ số quy trình, không chỉ chỉ số production.

### 2.2. Scan codebase định kỳ

Một lần scan bảo mật là một nhận định tại một thời điểm, với một model cụ thể. Cả hai yếu tố đều cũ đi: code thay đổi mỗi tuần, và mỗi thế hệ model tìm ra lỗ hổng mà thế hệ trước bỏ sót.

Cách xử lý của playbook: **scan theo lịch, không cần người khởi động**, và đưa phát hiện qua cùng các cổng như mọi thay đổi khác.

Công cụ được giới thiệu là Claude Security: kết nối repo GitHub, scan chạy trên Claude Mythos 5 trong hạ tầng của Anthropic, mỗi phát hiện được xác thực trước khi báo và có mức độ tin cậy kèm theo. Bản vá đề xuất được review và áp trong Claude Code on the web. Hiện chỉ có cho gói Enterprise, ở dạng public beta, tính phí theo mức dùng.

Cách làm:
1. Kết nối repo, nhóm theo dự án, dịch vụ hoặc team để rõ ai chịu trách nhiệm phát hiện nào.
2. Chạy một lần scan đầy đủ trên các repo quan trọng nhất, kể cả repo đã từng được tool khác scan. Coi đây là baseline. Lần đầu thường tìm ra vấn đề ở chỗ tưởng là sạch.
3. Đặt lịch cho từng dự án. Hằng tuần là mặc định hợp lý cho dịch vụ đang phát triển.
4. Phân loại phát hiện kèm mức tin cậy. Bỏ qua phải ghi lý do, để lần sau phát hiện đó không quay lại như mới.
5. Phát hiện gói gọn trong một bản vá → review và đưa qua cổng PR. Agent đề xuất bản vá không có đường tự duyệt.
6. Phát hiện rộng hơn một bản vá (điểm yếu kiến trúc, lỗi lặp lại ở nhiều dịch vụ) → viết thành `intent.md`, bắt đầu từ Plan.
7. Khi bản sửa lên production, thêm eval cho loại lỗ hổng đó.
8. Xuất phát hiện ra CSV, Markdown hoặc webhook để hệ thống tracker và audit hiện có vẫn là nơi lưu chính.

Playbook nói rõ: scan bằng model **bổ sung** cho static analysis và scan phụ thuộc, không thay thế. Kiểm tra cố định vẫn ở trong CI. Scan bằng model nhắm vào lỗ hổng phụ thuộc ngữ cảnh mà các công cụ kia không được thiết kế để tìm.

### 2.3. Claude trực sự cố qua Claude Tag

Sự cố còn đến qua kênh chat: một tin nhắn lúc 10 giờ tối trong kênh sự cố trên Slack. Claude Tag (public beta, hiện có trên Slack) đưa Claude vào kênh với danh tính riêng, nên mỗi sự cố có một người phản hồi đầu tiên ngay lập tức.

Điểm đáng chú ý:
- Cuộc trao đổi và tri thức nằm lại trong kênh. Ai trong kênh cũng dẫn dắt được, thử giả thuyết, điều tra cùng lúc.
- Qua MCP, Claude xác nhận chỉ số đã về baseline và báo trong thread.
- Post-mortem được ghi vào một file bài học có quản lý phiên bản, để những lần điều tra sau đọc được.
- **Kênh chính là audit trail**: yêu cầu, chẩn đoán, sự cho phép của người, bản sửa đều nằm ở nơi xử lý sự cố.

Không chỉ sự cố: được tag vào ticket hoặc được hỏi trong kênh, Claude phân loại việc theo cùng cách. Sửa nhỏ, khoanh vùng rõ thì thành PR qua cổng review. Việc lớn hơn thì viết thành `intent.md`, và vòng lặp tự nuôi chính nó.

### Governance

- Ranh giới các mức được thực thi từ cấu hình có phiên bản. Quyền và managed settings chặn truy cập production.
- Mọi lần gọi, phát hiện, quyết định phân loại đều có timestamp.
- Service owner phân loại và duyệt. Thay đổi phát sinh đi qua cổng review PR bình thường. Runbook agent được phép chạy đã được duyệt từ trước.
- Với scan: repo nào được kết nối, ai có quyền scan, giới hạn chi tiêu đều do admin đặt tập trung. Lịch sử scan là bản ghi audit về thứ đã được tìm thấy, đã sửa, và đã chấp nhận có chủ đích.

### Đo hiệu quả

| Play | Chỉ số dẫn | Chỉ số trễ |
|---|---|---|
| Khép vòng | Thời gian từ lúc vượt ngưỡng tới khi có `intent.md` trong hàng đợi, so với thời gian từ sự cố tới việc cần làm sau post-mortem trước đây | Tỉ lệ phát hiện thành bản sửa được merge, số sự cố lặp lại cùng loại |
| Scan định kỳ | Tỉ lệ repo đã có lịch scan, thời gian từ phát hiện tới khi bản vá vào cổng PR | Lỗ hổng do scan tìm ra so với lỗ hổng lộ ra ở production hoặc do bên ngoài báo, xu hướng số phát hiện mỗi lần scan |

---

## 3. Chỗ còn hở

Phần này là phân tích, không có trong bài gốc.

### Hàng đợi phân loại thành backlog mới

Vòng lặp tự sinh `intent.md`, nhưng vẫn cần người phân loại. Nếu ngưỡng chưa được chỉnh tốt, hàng đợi đầy những phát hiện nửa đúng. Người trực bắt đầu bỏ qua cả loạt, và vòng lặp lại quay về đúng tình trạng bị động ban đầu, chỉ là với nhiều file hơn.

### Ai sở hữu hàng đợi

Playbook nói service owner hoặc người trực phân loại. Với team nhỏ không có lịch trực chính thức, hàng đợi rất dễ không có chủ.

### Dịch vụ mới chưa có baseline

Ngưỡng 1σ, 2σ, 3σ cần một baseline ổn định. Dịch vụ mới ra, hoặc chỉ số có tính mùa vụ mạnh, sẽ báo động nhầm liên tục.

### Mobile có nhịp khác

Chỉ số sức khoẻ của app di động không thay đổi theo từng phút như 5xx trên server. Chúng thay đổi theo **từng bản phát hành**, và phải chờ đủ người dùng cập nhật mới có số đáng tin. Rollback cũng không có như server (xem [Phase 5](05-deploy.md)).

### Chi phí và quyền truy cập

Scan bằng Mythos 5 tính phí theo mức dùng và chỉ có ở gói Enterprise. Team không có gói này cần cách khác cho phần scan định kỳ.

---

## 4. Giải pháp ban đầu

### 4.1. Bắt đầu bằng chỉ số nội bộ, không phải production

Chỉ số đầu tiên nên là **tỉ lệ test fail trong CI**:
- Hậu quả của báo nhầm thấp, không ảnh hưởng người dùng.
- Dữ liệu có sẵn trong CI.
- Hành động ở mức 3σ (cách ly test, mở PR) đều đi qua cổng review.

Chỉ chuyển sang chỉ số production khi đã chỉnh ngưỡng xong cho chỉ số này.

### 4.2. Giữ hàng đợi khỏi phình to

- Đặt trần số `intent.md` do agent sinh đang chờ phân loại, ví dụ 5. Vượt trần thì agent gộp phát hiện mới vào file cũ cùng loại thay vì tạo file mới.
- Hẹn thời gian phân loại, ví dụ 2 ngày làm việc.
- Phân công người sở hữu hàng đợi theo tuần, kể cả khi team không có lịch trực.

### 4.3. Phân loại lý do bỏ qua

Mỗi lần bỏ qua, chọn một lý do từ danh sách cố định:

| Lý do | Hành động tiếp theo |
|---|---|
| Báo nhầm, chỉ số dao động bình thường | Nới ngưỡng |
| Đúng nhưng đã biết, đang xử lý | Gộp vào intent có sẵn |
| Đúng nhưng chấp nhận được | Ghi lý do chấp nhận, tắt cảnh báo loại này trong thời hạn nhất định |
| Chẩn đoán sai nguyên nhân | Cải thiện prompt chẩn đoán, thêm eval |

Đếm theo lý do mỗi tháng. Tỉ lệ "báo nhầm" cao nghĩa là ngưỡng chưa đúng. Tỉ lệ "chẩn đoán sai" cao nghĩa là agent thiếu ngữ cảnh.

### 4.4. Ngưỡng cho app mobile

Theo dõi theo **từng phiên bản phát hành**, không theo thời gian thực:

| Chỉ số | Nguồn thường dùng |
|---|---|
| Tỉ lệ người dùng không gặp crash | Crashlytics, Xcode Organizer, Play Console |
| Tỉ lệ ANR (Android) | Play Console |
| Thời gian khởi động lạnh | Công cụ đo hiệu năng của từng nền tảng |
| Đánh giá trên store sau phát hành | App Store Connect, Play Console |

Gắn ngưỡng 3σ với hành động: **dừng phát hành dần** và **đề xuất tắt feature flag** của tính năng mới nhất. Cả hai cần người xác nhận theo bảng ở Phase 5.

Với dịch vụ chưa có baseline, dùng ngưỡng cố định do team đặt trong vài tuần đầu, rồi mới chuyển sang ngưỡng thống kê.

### 4.5. File bài học sau sự cố

Playbook nhắc tới file bài học nhưng không đưa format. Một format gọn:

```markdown
## 2026-10-02 · Crash khi token hết hạn giữa lúc tải hồ sơ
Dấu hiệu: crash-free users bản 3.4.1 giảm 1.2% so với bản trước
Nguyên nhân: completion handler gọi sau khi màn hình đã bị huỷ
Sửa: PR #482
Eval: inc-2026-031-null-session
Bài học: mọi request gắn với vòng đời màn hình phải huỷ được
```

Dòng cuối là thứ có thể chuyển lên `CLAUDE.md` hoặc thành skill nếu lặp lại.

### 4.6. Scan định kỳ khi chưa có Claude Security

Có thể dựng phiên bản đơn giản bằng công cụ sẵn có:

- Workflow chạy hằng tuần, gọi `claude -p` với một skill review bảo mật, chỉ đọc, trên các thư mục thay đổi trong tuần.
- Kết quả ghi thành một issue tổng hợp, không tự sửa.
- Giữ nguyên các scan cố định đã có (static analysis, scan phụ thuộc) trong CI.

Phiên bản này không có bước xác thực phát hiện như Claude Security, nên tỉ lệ báo nhầm sẽ cao hơn. Áp dụng bảng phân loại lý do ở 4.3 ngay từ đầu.

---

## 5. Tuần đầu tiên

1. Lấy dữ liệu tỉ lệ test fail của CI trong 30 ngày qua.
2. Viết script tính trung bình và độ lệch chuẩn, có unit test.
3. Viết `bands.yaml` chỉ với mức 1σ ghi log và 2σ chẩn đoán chỉ đọc. Chưa bật mức 3σ.
4. Chạy một tuần, đọc mọi chẩn đoán agent viết ra, phân loại theo bảng lý do.
5. Chỉ bật mức 3σ khi tỉ lệ báo nhầm đủ thấp để team tin vào nó.

Vòng lặp khép được khi team tin vào cảnh báo. Niềm tin đó cần vài tuần dữ liệu thật, không bật một lần là có.
