# Phase 5 · Deploy: review hai chiều, cổng do hook giữ

> Thuộc bộ tài liệu đọc *The AI-native SDLC playbook* (Anthropic, 21/8/2026). Xem [tổng quan](00-tong-quan.md).

---

## Tóm gọn

Review chạy theo hai chiều: Claude review PR của người khác và tự xử lý comment trên PR của mình. Governance được thực thi ngay khi agent hành động, không chờ chu kỳ họp. Agent làm mọi thứ đến trước cổng production, và không được vượt qua.

Phase này có ba play: **AI trong vòng review PR**, **hook làm cổng duyệt**, và **tích hợp vào CI/CD**.

---

## 1. Vấn đề của cách cũ

Năng lực review được lên kế hoạch theo lượng code con người viết ra. Một PR phải chờ có người đọc hết. Chất lượng review dao động theo độ bận của người review. Tác giả phải đi nhắc, còn hàng đợi thì dài dần.

Governance diễn ra theo chu kỳ review, thường không nhất quán. Pipeline chạy các script cố định, việc gì cần phán đoán thì chờ người: phân loại test chập chờn, viết changelog, tìm lý do build hỏng. Deploy và rollback là những runbook người phải làm theo khi đang chịu áp lực.

---

## 2. Playbook xử lý thế nào

### 2.1. AI trong vòng review PR

Mọi PR đều đi qua cùng một bộ lượt review, finding được xếp theo mức nghiêm trọng. Sự chú ý của người review dịch lên một tầng: **thay đổi có làm đúng ý plan không, và rủi ro có chấp nhận được không**.

Hai cách triển khai:
- Dịch vụ **Code Review** được quản lý (research preview): admin bật lên, chọn repo. Nhanh nhất.
- **claude-code-action** chạy trong CI của mình: khi cần kiểm soát pipeline, hoặc cần gọi model qua Bedrock, Vertex hay Foundry theo hợp đồng cloud của tổ chức.

Cách làm:

1. Tech lead viết chính sách review thành **`REVIEW.md`** ở gốc repo, chia thành các lượt: bug và lỗi logic; bảo mật; tuân thủ `spec.md`, `plan.md` và nguyên tắc thiết kế. File cũng định nghĩa thế nào là "Important", thế nào là "Nit", và thứ gì bỏ qua.
2. **Finding không tự duyệt hay chặn PR.** Branch protection vẫn bắt buộc có code owner duyệt. Nếu muốn chặn merge theo finding, đọc bảng đếm theo mức nghiêm trọng mà check run xuất ra.
3. **Vòng sửa:** người review hoặc tác giả tag `@claude` vào comment, Claude sửa và đẩy commit. Vòng này chạy qua claude-code-action; ở dịch vụ Code Review được quản lý, comment `@claude review` sẽ yêu cầu một lượt review mới thay vì sửa. Với PR do Claude mở, có thể để Claude "trông" PR tới khi merge: một slash command quét các comment chưa giải quyết và check đang fail, sửa, đẩy lên, cho tới khi PR chỉ còn chờ code owner duyệt.
4. **Finding quay về `CLAUDE.md`.** Một lỗi bị review bắt lần thứ hai thì ghi cách sửa vào `CLAUDE.md`. Vì review đọc `CLAUDE.md`, lỗi đó bị chặn từ PR sau. Review cũng báo khi một thay đổi làm `CLAUDE.md` lỗi thời.
5. **Tinh chỉnh hằng tháng:** chấm điểm finding để review tốt lên, giới hạn số nit, loại trừ code sinh tự động và những gì CI đã kiểm.

`REVIEW.md` mẫu trong playbook có ba lượt (bug, bảo mật, tuân thủ), định nghĩa Important là thứ làm hỏng hành vi, lộ dữ liệu hoặc vi phạm policy, giới hạn tối đa 5 nit mỗi review, và liệt kê những gì không cần báo.

Nguyên tắc governance: **agent viết code không có cách nào duyệt code đó.** Tách bạch nhiệm vụ được giữ nguyên.

### 2.2. Hook làm cổng duyệt

Ở Build, hook cho qua hoặc chặn mà không cần người. Hook còn có lựa chọn thứ ba: **hỏi**, tạm dừng hành động cho tới khi một người cụ thể đồng ý. Đây đúng là thứ cổng release cần.

Cách làm:

1. Lãnh đạo engineering cùng change management và compliance liệt kê những cổng duyệt phải giữ: ký duyệt thay đổi, cho phép release, sửa đường dẫn được bảo vệ.
2. Platform engineer viết mỗi cổng thành một hook có thể cho qua, hỏi, hoặc chặn.
3. Hook của team để trong `.claude/settings.json` trong git. **Hook không được thương lượng để trong managed settings** do platform hoặc IT quản lý, engineer không tắt được.
4. Hook chặn phải tự giải thích: lý do và cách xin duyệt hiện ra trong output của Claude.

Ví dụ trong playbook: một hook kiểm mọi lệnh Bash, nếu lệnh chứa "deploy" và "production" mà không có biến môi trường xác nhận release thì chặn, trả thông báo cho Claude.

#### Managed settings cho doanh nghiệp bị quản lý chặt

Playbook đưa một cấu hình mẫu đầy đủ, giải thích từng dòng mua được gì:

| Nhóm cấu hình | Tác dụng |
|---|---|
| Danh sách deny / allow | Giữ secret ngoài context, chặn truy cập mạng qua công cụ. Cho phép sẵn các lệnh an toàn để không phải bấm duyệt liên tục |
| Tắt chế độ bỏ qua quyền, chỉ dùng rule được quản lý | Không engineer, file project hay cờ dòng lệnh nào nới được rule |
| Sandbox ở mức hệ điều hành | Chặn mạng thật sự, vì deny một công cụ không ngăn được lệnh shell gọi ra ngoài |
| Bắt buộc sandbox | Claude Code không khởi động nếu sandbox lỗi, lệnh fail trong sandbox không được chạy lại bên ngoài |
| Chặn đọc credential | Lệnh shell không đọc được `~/.ssh`, `~/.aws/credentials`, biến môi trường chứa token |
| Chỉ hook được quản lý | Cổng duyệt của tổ chức là hook duy nhất được chạy |
| Chỉ marketplace được duyệt | Mọi skill, agent, hook, MCP server đến từ kho plugin của tổ chức |
| Phiên bản tối thiểu | Không chạy trên bản Claude Code cũ hơn bản đã được đánh giá |

Playbook nhấn mạnh đây là **điểm khởi đầu để chỉnh, không phải để chép**. Mỗi dòng deny đổi lấy một phần năng lực, và mức cân bằng phụ thuộc mức độ nhạy cảm của dữ liệu trong repo.

### 2.3. Claude trong CI/CD

Cách làm theo thứ tự tăng dần rủi ro:

1. **Bước chỉ đọc trước.** Dùng `claude -p` trong pipeline để phân loại build fail, tóm tắt test chập chờn, soạn changelog.
2. **Bước ghi đi qua cổng có sẵn.** Sửa lint, cập nhật tài liệu sinh tự động, xử lý comment review. Mọi thứ agent viết đều thành PR qua branch protection. Agent không có đường đẩy thẳng lên main.
3. **Sandbox khi chạy.** Job của agent chạy trong container với network policy, token ngắn hạn có phạm vi hẹp, mặc định không có credential production.
4. **Deploy qua MCP.** Deploy, kiểm trạng thái, rollback trở thành công cụ có phạm vi theo từng môi trường. Quyền deploy của agent là một danh sách cho phép, không phải script cầm credential.
5. **Mức tự chủ theo môi trường.** Dev: agent deploy tự do. Production: agent chuẩn bị release, release manager cho phép, hook giữ cổng. Staging ở giữa.
6. **Rollback là đường được tập nhiều nhất.** Một lệnh duy nhất agent chạy được, được tập thường xuyên ở staging. Phase Maintain sẽ gọi lệnh này khi chỉ số vượt ngưỡng, nên nó phải được chứng minh từ trước.

Mỗi lần chạy không tương tác dùng **danh tính riêng của agent**, nên log phân biệt được việc agent làm với việc của engineer đã kích hoạt.

### Đo hiệu quả

| Play | Chỉ số dẫn | Chỉ số trễ |
|---|---|---|
| AI review | Thời gian tới review đầu tiên (kỳ vọng vài phút), tỉ lệ comment được xử lý mà người không phải sửa branch | Lỗi và lỗ hổng bắt được trước merge so với lọt ra production |
| Hook cổng duyệt | Thời gian chờ ở mỗi cổng (mọi quyết định hook đều có timestamp trong OpenTelemetry) | Vi phạm cổng lọt ra production trước và sau khi có hook |
| CI/CD | Tỉ lệ pipeline fail được phân loại mà không phải gọi người | Các chỉ số DORA |

---

## 3. Chỗ còn hở

Phần này là phân tích, không có trong bài gốc.

### Người review vẫn là trần

AI review làm mỗi lần duyệt nhẹ hơn, nhưng mỗi PR vẫn cần một code owner duyệt. Nếu agent tạo gấp năm lần số PR, hàng đợi duyệt vẫn dài ra. Playbook không đưa cơ chế điều tiết số PR.

### Duyệt cho có

Khi PR đã có AI review, test pass, finding đã được sửa, người duyệt dễ bấm approve mà không thật sự đọc. Đây là thiên kiến tin vào máy (automation bias). Tách bạch nhiệm vụ vẫn đúng trên giấy nhưng rỗng trong thực tế.

### PR lớn làm review vô nghĩa

Agent viết nhanh nên dễ sinh PR vài nghìn dòng. Không ai review tử tế được cỡ đó, dù có AI hỗ trợ.

### Mobile có cổng nằm ngoài tầm tay

Với app di động:
- **App Store và Google Play review là một cổng bên ngoài.** Không hook nào thay được, và có thể mất từ vài giờ tới vài ngày.
- **Rollback không phải một lệnh.** Bản đã cài trên máy người dùng không gỡ về được. Chỉ có thể dừng phát hành dần, phát hành bản sửa, hoặc tắt tính năng từ xa.
- **Chứng chỉ ký app** là loại credential nhạy cảm nhất, không được lọt vào môi trường của agent.

---

## 4. Giải pháp ban đầu

### 4.1. Số người duyệt theo mức rủi ro

Gắn nhãn rủi ro tự động dựa trên đường dẫn PR đụng tới:

| Mức | Điều kiện | Duyệt |
|---|---|---|
| Thấp | Chỉ UI text, test, tài liệu | 1 code owner |
| Vừa | Logic nghiệp vụ, API client | 1 code owner + đọc `plan.md` |
| Cao | Xác thực, thanh toán, lưu trữ dữ liệu, cấu hình build và ký | 2 người, trong đó 1 tech lead |

Nhãn do một script gắn, không do agent tự chọn.

### 4.2. Chống duyệt cho có

- Khi approve, người duyệt ghi một dòng: đã kiểm điều gì. Ví dụ: "đã chạy thử luồng hết hạn phiên trên simulator".
- Mỗi tháng chọn ngẫu nhiên vài PR đã merge, một người khác review lại. Đếm số vấn đề lẽ ra phải bị bắt.

### 4.3. Giới hạn kích thước PR

- Đặt trần, ví dụ 400 dòng thay đổi không tính file sinh tự động.
- Ghi vào `CLAUDE.md`: thay đổi lớn hơn thì tách thành nhiều PR theo thứ tự trong `plan.md`.
- Thêm một check trong CI cảnh báo PR vượt trần.

### 4.4. `REVIEW.md` khởi đầu cho repo mobile

```markdown
# Review instructions

## Passes
- Bugs: lỗi logic, trường hợp biên, rò rỉ bộ nhớ, retain cycle
- Security: lưu token sai chỗ (UserDefaults, SharedPreferences), log dữ liệu cá nhân, deep link không kiểm
- Compliance: khớp spec.md và plan.md, có xử lý trạng thái tải / rỗng / lỗi / mất mạng

## Important nghĩa là
Crash, mất dữ liệu người dùng, lộ dữ liệu, vi phạm quy định store.
Đặt tên, định dạng là nit.

## Tối đa 5 nit mỗi review

## Không báo
Code sinh tự động, file project của Xcode, những gì lint đã kiểm.
```

### 4.5. Release mobile theo tinh thần "đến trước cổng"

| Agent được làm | Cần người |
|---|---|
| Tăng số build, soạn release note | Gửi bản lên store review |
| Upload bản thử nội bộ (TestFlight nội bộ, internal track) | Mở phát hành cho người dùng thật |
| Tạo cấu hình phát hành dần | Tăng tỉ lệ phát hành dần |
| Đề xuất tắt feature flag khi có sự cố | Bật lại tính năng cho mọi người |

"Rollback" của mobile thực chất là ba thứ cần chuẩn bị trước: **feature flag** cho mọi tính năng mới, **phát hành dần** để dừng được khi thấy vấn đề, và **cấu hình từ xa** để đổi hành vi không cần bản mới. Đây là thứ cần tập dượt, tương đương lệnh rollback trong playbook.

Chứng chỉ ký app chỉ nằm trong môi trường CI riêng, không bao giờ nằm trong sandbox của agent.

---

## 5. Tuần đầu tiên

1. Viết `REVIEW.md` cho một repo, bật AI review trên repo đó.
2. Bật branch protection bắt buộc code owner duyệt, nếu chưa có.
3. Viết một hook duy nhất: chặn lệnh deploy hoặc release lên production khi không có xác nhận.
4. Thêm một bước chỉ đọc vào CI: khi build fail, Claude tóm tắt nguyên nhân vào PR.
5. Sau một tuần, đọc lại toàn bộ finding, đánh dấu cái nào hữu ích, cái nào nhiễu. Chỉnh `REVIEW.md` theo kết quả.
