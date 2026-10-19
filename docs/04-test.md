# Phase 4 · Test: agent tự kiểm, cấu hình cũng phải test

> Thuộc bộ tài liệu đọc *The AI-native SDLC playbook* (Anthropic, 21/8/2026). Xem [tổng quan](00-tong-quan.md).

---

## Tóm gọn

Mỗi session tự kiểm tra công việc của mình trước khi người nhìn thấy. Thêm vào đó, cấu hình điều khiển agent (`CLAUDE.md`, skill, hook) cũng được kiểm hồi quy giống như code mà agent viết.

Phase này có hai play: **vòng tự kiểm** và **eval liên tục trong CI**.

---

## 1. Vấn đề của cách cũ

Tín hiệu "code này chạy đúng" đến muộn: CI báo sau vài phút, tester báo sau vài ngày, production báo sau vài tuần.

Khi người viết code, độ trễ này chấp nhận được. Khi agent viết code nhanh gấp nhiều lần, tín hiệu đến muộn nghĩa là **một người phải kiểm toàn bộ output của agent**, và người đó trở thành nút thắt.

Ở cách cũ, QA là cổng chặn giữa các stage. Cổng này được định biên theo tốc độ code của con người.

---

## 2. Playbook xử lý thế nào

### 2.1. Cho agent một vòng tự kiểm

Nguyên tắc: **luôn cho Claude cách tự kiểm tra công việc của nó**, dù là chạy test, chạy build hay so screenshot. Session tự kiểm, tự sửa trước khi engineer nhìn thấy.

Vòng tự kiểm khác với subagent `verifier` ở Phase 3:
- Vòng tự kiểm chạy **suốt quá trình làm**, lặp bao nhiêu lần cũng được.
- `verifier` là bước kiểm cuối, chạy trong một context mới khi session nghĩ mình đã xong. Context mới giúp kết luận không bị ảnh hưởng bởi những giả định đã sinh ra code.

Cách làm:

1. **Gói việc kiểm vào một lệnh.** Nếu hôm nay kiểm tra cần chuỗi lệnh và hiểu biết về môi trường, gói thành một target như `make test`, trả mã khác 0 khi fail.
2. **Ghi lệnh vào `CLAUDE.md`**, kèm ví dụ output khi mọi thứ ổn.
3. **Đặt mục tiêu đo được** để Claude tự biết khi nào xong mà không cần hỏi. Ví dụ: "mọi test trong file X pass", "screenshot khớp mock đính kèm", "endpoint trả 200 với trường mới".
4. **Sửa bug thì viết test fail trước.** Yêu cầu Claude tái hiện bug bằng một test, chạy, xác nhận nó fail đúng lý do. Commit test đó. Sau đó mới yêu cầu sửa code cho test pass, và không được sửa test. Một test có trước bản sửa mà agent không đụng được là bằng chứng bug đã hết.
5. **Với giao diện, khép vòng bằng hình ảnh.** Cho Claude công cụ chụp màn hình và bản mock. Làm, chụp, so, chỉnh. Hai ba vòng là bình thường.
6. **Kiểm tra là một phần của "xong".** Ghi vào `CLAUDE.md`: chạy test trước khi báo hoàn thành, và dán output.
7. **Bảo vệ chính vòng kiểm.** Agent đang sửa code không được làm yếu đi phép kiểm tra code đó. Dùng hook chặn sửa file test trong lúc sửa bug, hoặc từ chối ở review mọi diff đụng tới test.

Ví dụ khối kiểm trong `CLAUDE.md` gồm ba lệnh build, test, lint, mỗi lệnh kèm điều kiện thành công, và hai câu quy tắc: chạy cả ba trước khi báo xong và dán output; test fail thì sửa code, không sửa test.

### 2.2. Eval liên tục trong CI

Eval là phiên bản AI-native của QA gate. Đó là một bộ bài kiểm tra chạy mỗi khi cấu hình agent thay đổi. Khi đổi model hay viết lại prompt, eval cho biết agent còn làm việc đạt chuẩn cũ không.

Cách làm:

1. Platform engineer gom **20–50 task thật** từ công việc gần đây, kèm kết quả đã được chấp nhận.
2. Viết mỗi task thành một eval: prompt cộng các phép kiểm định nghĩa thế nào là đạt (test pass, lint sạch, hành vi không đổi, policy được tuân thủ).
3. Bộ eval chạy không tương tác trong CI, theo lịch và **mỗi khi `CLAUDE.md`, skill hoặc hook thay đổi**. Cấu hình này điều khiển agent, nên xứng đáng được test hồi quy như code.
4. Đặt cổng: thay đổi skill làm giảm tỉ lệ đạt thì phải được review trước khi merge.
5. **Mỗi sự cố production thành một eval**, do team phụ trách sự cố viết, giữ vĩnh viễn trong bộ.

Playbook có ví dụ workflow GitHub Actions: chạy khi PR đụng tới `CLAUDE.md` hoặc `.claude/`, và chạy hằng đêm. Mỗi eval gọi `claude -p` với danh sách công cụ được giới hạn, rồi một script chấm kết quả.

Lưu ý quan trọng: **bộ eval phải sống**. Khi model mạnh lên, những bài từng phân biệt được tốt xấu sẽ không còn phân biệt nữa. Phải liên tục thêm bài mới từ quá trình theo dõi.

### Governance

| | Vòng tự kiểm | Eval |
|---|---|---|
| Bắt buộc | Kiểm trước khi báo xong, chặn sửa test khi sửa bug (qua hook nếu cần chắc chắn) | Ngưỡng tỉ lệ đạt là điều kiện merge |
| Bằng chứng | Output thật của lệnh test, log build, kết quả so screenshot | Kết quả mỗi lần chạy, so được theo thời gian |
| Nơi lưu | Transcript session (qua OpenTelemetry), check run của PR | Log CI |
| Người duyệt | Code owner, tập trung vào ý đồ và rủi ro vì bằng chứng cơ học đã có sẵn | Team sở hữu thay đổi cấu hình |

### Đo hiệu quả

| Play | Chỉ số dẫn | Chỉ số trễ |
|---|---|---|
| Vòng tự kiểm | Tỉ lệ CI pass ngay lần đầu với thay đổi do agent viết | Thời gian review mỗi PR, tỉ lệ thay đổi gây lỗi |
| Eval | Tỉ lệ đạt theo thời gian, thời gian từ sự cố tới khi có eval | Số lỗi hồi quy bắt được ở CI so với số lỗi lọt ra production |

---

## 3. Chỗ còn hở

Phần này là phân tích, không có trong bài gốc.

### Cùng một tác giả viết code và test

Khi agent viết cả code lẫn test, test thường kiểm đúng những gì agent đã hiểu. Nếu agent hiểu sai yêu cầu, cả code và test sai theo cùng một hướng, và test vẫn pass. Kỹ thuật "test fail trước" của playbook chỉ áp cho sửa bug, chưa áp cho tính năng mới.

### Test chập chờn đầu độc vòng tự kiểm

Một test lúc pass lúc fail làm agent mất thời gian sửa thứ không hỏng, hoặc tệ hơn là học cách bỏ qua test fail. Playbook không nói phải xử lý test chập chờn trước khi bật vòng tự kiểm.

### Vòng hình ảnh trên mobile khó hơn web

Playbook nói về trình duyệt và screenshot. Với app di động, chụp màn hình cần simulator hoặc emulator đang chạy, đưa app tới đúng màn hình cần kiểm, và xử lý khác biệt kích thước màn hình. Không có công cụ nào cắm vào là chạy như trình duyệt.

### Chấm eval là phần khó nhất

Ví dụ trong playbook dùng một script `check.sh` để chấm, nhưng không nói chấm thế nào. Với task "sửa bug", chấm bằng test là được. Với task "viết spec" hay "review PR", chấm khó hơn nhiều.

### Chi phí

50 eval, mỗi eval một session Claude Code đầy đủ, chạy mỗi đêm và mỗi PR đụng cấu hình. Con số cộng dồn nhanh.

---

## 4. Giải pháp ban đầu

### 4.1. Tách người viết test khỏi người viết code

Với tính năng mới, áp cùng tinh thần "test trước" của playbook:

1. Lấy **tiêu chí nghiệm thu** trong `spec.md` (xem [Phase 2](02-design.md)).
2. Một session riêng viết test từ tiêu chí đó, chưa nhìn thấy code. Commit test.
3. Session khác viết code cho test pass, có hook chặn sửa file test.

Test bây giờ phản ánh spec, không phải cách hiểu của người viết code.

### 4.2. Dọn test chập chờn trước khi bật vòng

- Chạy cả bộ test 10 lần liên tiếp, ghi lại test nào có kết quả không ổn định.
- Đưa các test đó vào danh sách cách ly, ghi vào `CLAUDE.md` để agent không cố sửa.
- Sửa dần danh sách cách ly như một việc riêng.

### 4.3. Vòng tự kiểm cho app mobile

| Nhu cầu | iOS | Android |
|---|---|---|
| Một lệnh test | `xcodebuild test` gói trong `make test` | `./gradlew test` gói trong `make test` |
| Chụp màn hình | `xcrun simctl io booted screenshot` | `adb exec-out screencap -p` |
| So giao diện tự động | Snapshot test (ví dụ swift-snapshot-testing) | Snapshot test chạy trên JVM (ví dụ Paparazzi, Roborazzi) |

Snapshot test có lợi hơn chụp màn hình tay vì chạy không cần simulator mở sẵn, nhanh hơn, và kết quả so sánh rõ ràng. Agent nhận được ảnh khác biệt để tự chỉnh.

### 4.4. Bắt đầu eval nhỏ và dễ chấm

- Bắt đầu với **10 task**, không phải 50.
- Chọn task chấm được bằng máy: sửa bug có test, thêm endpoint có test, refactor không đổi hành vi.
- Mỗi task chấm bằng ba phép kiểm: test pass, lint sạch, diff không đụng file ngoài phạm vi.
- Chỉ thêm task chấm bằng đánh giá chủ quan khi bộ đầu đã chạy ổn.

### 4.5. Kiểm soát chi phí eval

- Chạy toàn bộ eval khi PR đụng cấu hình agent.
- Chạy định kỳ mỗi tuần thay vì mỗi đêm, trừ khi team thay đổi cấu hình thường xuyên.
- Ghi lại chi phí mỗi lần chạy cạnh tỉ lệ đạt. Nếu chi phí tăng mà tỉ lệ đạt không đổi, bộ eval có bài thừa.

### 4.6. Cách viết một eval từ sự cố

Khi một sự cố được sửa xong:

```json
{
  "id": "inc-2026-031-null-session",
  "source": "Sự cố 031, crash khi phiên đăng nhập hết hạn giữa chừng",
  "prompt": "Màn hình hồ sơ crash khi token hết hạn lúc đang tải. Sửa lỗi.",
  "checks": [
    "make test pass",
    "test_profile_expired_session tồn tại và pass",
    "diff không sửa file trong tests/ ngoài file test mới"
  ]
}
```

Giữ format đơn giản để team nào cũng viết được.

---

## 5. Tuần đầu tiên

1. Gói build, test, lint thành ba lệnh, ghi vào `CLAUDE.md` kèm output mẫu.
2. Chạy bộ test 10 lần, lập danh sách test chập chờn.
3. Thêm hook chặn sửa file test khi làm việc sửa bug.
4. Sửa 2 bug bằng quy trình "test fail trước".
5. Viết 3 eval đầu tiên từ 3 bug vừa sửa gần đây.

Sau một tuần, so tỉ lệ CI pass lần đầu của thay đổi do agent viết với tuần trước.
