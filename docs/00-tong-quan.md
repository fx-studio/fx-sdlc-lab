# AI-native SDLC: đọc playbook của Anthropic

> Nguồn: *The AI-native SDLC playbook*, Louis Claxton (Applied AI, Anthropic), đăng ngày 21/8/2026.
> https://claude.com/resources/articles/the-ai-native-sdlc-playbook
>
> Bộ tài liệu này viết lại bằng lời của người đọc, không phải bản dịch. Phần nào là ý của playbook, phần nào là phân tích và đề xuất thêm đều được ghi rõ.

---

## Một câu để nhớ

Viết code giờ đã nhanh. Thứ còn chậm là mọi việc xung quanh code. Muốn hưởng trọn tốc độ của agent thì phải làm lại cả quy trình, không chỉ bước viết code.

---

## 1. Vấn đề gốc: code nhanh, quy trình đứng yên

Quy trình phát triển phần mềm (SDLC) quen thuộc có sáu bước: lên kế hoạch, thiết kế, xây dựng, kiểm thử, triển khai, vận hành. Mỗi bước có một vai phụ trách riêng. PM viết yêu cầu, architect chuyển thành thiết kế, engineer code, QA kiểm (ở các doanh nghiệp bị quản lý chặt), team release đưa lên, team vận hành theo dõi. Công việc chuyền tay nhau qua tài liệu, ticket và chữ ký duyệt.

Cách làm này được thiết kế cho thời mà **viết code là khâu tốn kém nhất**. PRD, buổi ước lượng, review bảo mật đều tồn tại để mọi người thống nhất trước khi bỏ ra vài tuần hay vài tháng để code. Mọi control cũng ngầm giả định rằng **con người làm từng bước**.

Khi agent như Claude Code viết code trong vài giờ thay vì vài tuần, giả định đó gãy. Playbook chỉ ra ba hệ quả:

1. **Nút thắt dời chỗ.** Build nhanh lên, nhưng plan, review/test và deploy vẫn chạy ở tốc độ con người. Đường găng giờ nằm ở hai bên bước build.
2. **Control không còn khớp thực tế.** Đọc từng dòng code là hợp lý khi một người viết ra nó. Khi agent viết phần lớn diff, người review không đọc kịp.
3. **Governance đắt dần.** Mỗi ngoại lệ vẫn phải chờ hội đồng họp theo tuần hoặc theo tháng.

Ví dụ playbook dùng là đội bảo mật. Đội này được định biên theo năng lực viết code của con người. Khi agent nhân lượng code lên nhiều lần, chỉ còn hai kết cục: hàng đợi review phình ra, hoặc code lên production mà chưa được soát kỹ. Doanh nghiệp bị quản lý chặt không chấp nhận được kết cục nào.

---

## 2. Ý tưởng chính

### Giữ mục tiêu kiểm soát, đổi cách thực thi

Playbook không bỏ control. Trách nhiệm, tách bạch nhiệm vụ, khả năng audit vẫn giữ nguyên. Thứ thay đổi là **ai và cái gì thực thi** chúng: máy làm phần cơ học ngay lúc agent hành động, người giữ phần cần phán đoán.

### Từ đường thẳng sang vòng lặp

SDLC cũ chạy một chiều, xong bước này mới tới bước kia, và vận hành là điểm cuối. Ở phiên bản AI-native, vận hành nối ngược về lên kế hoạch. Sự cố trên production được chẩn đoán rồi trở thành yêu cầu mới, đi lại từ đầu vòng.

### Sợi chỉ xuyên suốt: artifact được commit

Đây là ý xuyên suốt cả playbook. Mỗi stage kết thúc bằng việc **ghi một file vào git**, và stage sau bắt đầu bằng việc **đọc file đó**.

```
intent.md → spec.md → plan.md → diff + test → PR + review findings → incident record → intent.md mới
```

File `.md` chiếm ưu thế ở các stage đầu vì cả người lẫn agent đọc và sửa được cùng một file. Từ Build trở đi, artifact là code và các bản ghi đi kèm.

Chuỗi commit này có hai tác dụng cùng lúc:
- **Bàn giao không cần họp.** Bước sau đọc file là biết phải làm gì, không phải ngồi giải thích lại.
- **Audit trail sẵn có.** Ai yêu cầu gì, agent làm ra gì, ai duyệt, git đều ghi lại.

Khi một artifact được chấp nhận, nó kích hoạt bước tiếp theo:

| Artifact được chấp nhận | Kích hoạt |
|---|---|
| `intent.md` | Bước viết requirements và design |
| `spec.md` | Plan mode trong Claude Code |
| PR được merge | Pipeline CI/CD |
| Một chỉ số production vượt ngưỡng | `intent.md` mới, vòng lặp tiếp tục |

Lúc đầu mỗi bước vẫn do người kích tay. Đích đến là một vòng lặp tự chạy, con người chỉ đứng ở các cổng để duyệt những gì agent đã đánh dấu.

---

## 3. Sáu stage, nhìn nhanh

| Stage | Cách cũ | Cách AI-native | Artifact |
|---|---|---|---|
| **Plan** | Yêu cầu qua hội đồng, workshop, chữ ký, viết tay | Người có ý tưởng làm việc với Claude, ghi thành proto-spec | `intent.md` |
| **Design** | Analyst viết spec, designer đọc lại rồi thiết kế | Gộp requirements và design vào một session, policy áp qua skill | `spec.md` |
| **Build** | Code và test viết tay, tài liệu viết sau | Plan mode trước, agent viết code và test, tri thức nằm trong `CLAUDE.md` và skill | `plan.md`, diff |
| **Test** | QA gate ở ranh giới giữa các stage | Agent tự kiểm liên tục, eval chạy trong CI | test, eval |
| **Deploy** | Người đọc từng dòng, governance theo chu kỳ họp | Nhiều lượt AI review, người chỉ soát code quan trọng, hook làm cổng duyệt | PR, findings |
| **Maintain** | Người canh production | Agent theo dõi, vượt ngưỡng thì chẩn đoán và viết `intent.md` mới | incident, intent |

Mỗi stage được chia thành các "play". Play nào cũng có cùng khung: thay đổi gì, cần gì trước, các bước làm, governance, và cách đo hiệu quả.

---

## 4. Ba lớp kiểm soát

Playbook phân biệt rõ skill (control mang tính khuyến nghị) và hook (control bắt buộc). Lớp thứ ba, managed settings, xuất hiện trong ví dụ cấu hình cho doanh nghiệp bị quản lý chặt. Gom lại thành ba lớp là cách trình bày của bộ tài liệu này:

| Lớp | Bản chất | Tác dụng |
|---|---|---|
| **Skill** | Hướng dẫn agent đọc khi làm việc | Làm vi phạm *hiếm đi*, nhưng không gì ép session phải tuân theo |
| **Hook** | Script chạy trước hoặc sau hành động của agent | Làm vi phạm *gần như không thể*: chặn, cho qua, hoặc hỏi người |
| **Managed settings** | Cấu hình do platform/IT quản lý | Engineer không tự tắt hay nới được |

Nguyên tắc rút ra: policy nào bắt buộc phải đúng mọi lúc thì phải có hook đứng sau skill. Skill để agent làm đúng ngay từ đầu, hook để chắc chắn không lọt.

Ngoài ra, playbook nhắc nhiều lần một nguyên tắc ở khâu triển khai: **agent được làm mọi thứ đến trước cổng production, và không được vượt qua.** Agent viết code cũng không thể tự duyệt code đó.

---

## 5. Con người đứng ở đâu

Con người không biến mất. Vị trí của họ thay đổi: từ người làm từng bước sang người đứng ở các cổng.

| Cổng | Người duyệt |
|---|---|
| `intent.md` | Product owner |
| `spec.md` | Product owner, tham khảo tech lead nếu rủi ro cao |
| `plan.md` | Engineer, tech lead hoặc architect nếu rủi ro cao |
| PR | Code owner, qua branch protection |
| Release production | Release manager có tên cụ thể |
| Phân loại phát hiện từ production | Service owner hoặc người trực |

Sự chú ý của con người dịch theo artifact cần duyệt. Thay vì đọc từng dòng code, người duyệt hỏi: thay đổi này có đúng ý của plan không, rủi ro có chấp nhận được không.

---

## 6. Áp dụng theo thứ tự nào

Playbook có một đồ thị phụ thuộc giữa các play. Không cần làm đủ sáu stage cùng lúc. Một số play không cần gì trước nên có thể bắt đầu ngay:

- Viết `intent.md` (Plan)
- `CLAUDE.md` cho repo (Build)
- Skill cho một policy (Build)
- Cho agent một vòng tự kiểm (Test)
- Hook làm cổng duyệt (Deploy)

Các play phức tạp hơn, như đưa Claude vào CI/CD hay khép vòng ở Maintain, đòi hỏi các play nền phải chạy trước. Ví dụ: phải có cổng duyệt trước rồi mới tự động hoá thứ đi qua cổng.

### Sống chung với hệ thống cũ

Phần lớn tổ chức đã có Jira, công cụ quản lý yêu cầu, Figma, change board. Những hệ thống này khó thay vì auditor và các team khác đã quen. Playbook đề xuất chọn **một nguồn sự thật cho mỗi loại artifact**, theo một trong ba cấu hình:

1. **Repo là nguồn sự thật.** File markdown là bản chính, hệ thống cũ chỉ trỏ tới commit.
2. **Hệ thống cũ là nguồn sự thật.** Claude đọc ticket đầu session và ghi kết quả về qua MCP.
3. **Tối thiểu là liên kết hai chiều.** File markdown ghi ID của ticket, ticket ghi commit SHA của file.

### Đo bằng dữ liệu có sẵn

Mỗi play có chỉ số dẫn (leading) và chỉ số trễ (lagging), lấy từ những nguồn đội engineering thường đã có: timestamp trong git, metadata của PR, hệ thống CI, hệ thống quản lý sự cố. Riêng phần dữ liệu session của agent cần bật export OpenTelemetry.

---

## 7. Những gì playbook chưa trả lời

Đây là phần nhận xét, không có trong bài gốc.

**Nút thắt bị dời và nén, không biến mất.** Phần soạn thảo, chờ lịch, kiểm tra cơ học được tự động hoá. Phần phán đoán vẫn cần người, và giờ dồn về ít cổng hơn. Chính playbook cũng thừa nhận giới hạn của việc chạy song song là số luồng một người review được tử tế. Nếu điểm nghẽn thật của team là thiếu người có quyền duyệt, playbook chỉ giúp được một phần.

**Chưa có số liệu kết quả.** Bài đưa ra chỉ số để tự đo, không công bố số trước và sau của khách hàng nào. Những kỳ vọng như "từ vài tuần xuống vài giờ" vẫn là kỳ vọng.

**Mobile gần như vắng mặt.** Vòng tự kiểm cho UI dựa vào trình duyệt và screenshot. Rollback dựa vào pipeline. Với app iOS và Android, build chậm hơn, simulator khó chạy song song, và cổng App Store hay Google Play nằm ngoài tầm kiểm soát. Team mobile phải tự lấp khoảng trống này.

**Chi phí ít được bàn.** Eval chạy định kỳ, nhiều session song song, scan bảo mật theo lịch đều tốn token. Bài chỉ nhắc ngắn: cần ngân sách API cho eval, và đặt giới hạn chi tiêu khi dùng Claude Security.

**Phần tổ chức không được bàn.** Đổi quy trình đòi hỏi compliance, change board và khách hàng chấp nhận audit trail trong git thay cho chữ ký cũ. Bài chỉ đưa phương án kỹ thuật cho việc này.

**Nhiều công cụ còn ở giai đoạn thử.** Claude Design, Code Review, Claude Tag đang ở beta hoặc research preview. Claude Security chỉ có cho gói Enterprise. Khung tư duy dùng chung được, còn công cụ cụ thể thì nên kiểm tra trước khi cam kết.

---

## Đọc tiếp

Sáu file tiếp theo đi vào từng phase. Mỗi file có bốn phần: playbook nói gì, vấn đề cũ được xử lý ra sao, chỗ còn hở, và giải pháp ban đầu có thể thử.

1. [Plan: ý tưởng thành `intent.md`](01-plan.md)
2. [Design: spec trong một session](02-design.md)
3. [Build: plan trước, code sau](03-build.md)
4. [Test: agent tự kiểm, cấu hình cũng phải test](04-test.md)
5. [Deploy: review hai chiều, cổng do hook giữ](05-deploy.md)
6. [Maintain: khép vòng lặp](06-maintain.md)
