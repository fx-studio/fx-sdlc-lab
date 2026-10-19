# Phase 3 · Build: plan trước, code sau

> Thuộc bộ tài liệu đọc *The AI-native SDLC playbook* (Anthropic, 21/8/2026). Xem [tổng quan](00-tong-quan.md).

---

## Tóm gọn

Không dòng code nào được viết khi chưa có plan được duyệt. Tri thức của team chuyển từ đầu người và wiki vào các file mà agent đọc mỗi lần làm việc. Rào chắn chạy bằng code, không dựa vào thói quen. Một engineer có thể điều phối nhiều session song song.

Phase này có nhiều play nhất trong playbook: plan mode, auto mode, `CLAUDE.md`, skill, hook, và chạy song song.

---

## 1. Vấn đề của cách cũ

Engineer đọc thiết kế rồi bắt tay code. Cách thay đổi sẽ được thực hiện, sửa file nào, test gì, nằm trong đầu người viết, hoặc cùng lắm là một comment trong ticket. Không ai khác review được.

Thứ đầu tiên reviewer nhìn thấy là diff đã xong. Lúc đó phát hiện hướng sai thì phải làm lại, và làm lại thì chậm.

Một vấn đề nữa: một engineer làm một việc một lúc, và mất phần lớn thời gian chờ build, chờ test, chờ review. Chuyển sang việc khác trong lúc chờ thì mệt vì đổi ngữ cảnh, nên ít ai làm.

---

## 2. Playbook xử lý thế nào

### 2.1. Plan mode làm điểm bắt đầu mặc định

Engineer mở Claude Code ở plan mode, đưa vào `spec.md` đã duyệt, rồi để Claude hỏi lại. Ở plan mode, Claude đọc được codebase nhưng không sửa được gì cho tới khi engineer chấp nhận plan.

Các bước:

1. Yêu cầu Claude viết plan gồm: file nào thay đổi, thứ tự làm, test nào chứng minh thay đổi đúng.
2. Chất vấn plan: thay đổi này có thể làm hỏng gì, bước nào rủi ro nhất, có phương án nào Claude đã cân nhắc rồi bỏ.
3. Sửa đến khi một engineer chưa đọc cuộc trò chuyện vẫn làm theo được chỉ bằng plan.
4. Commit plan thành `plan.md`. Ở bước review PR sau này, diff sẽ được so với plan.
5. Chấp nhận plan và để Claude làm. Plan tốt thì thường làm một lượt là xong.
6. Khi code đi khác plan, cập nhật `plan.md` trong cùng commit. Có thể dùng hook để ép việc này.

Lợi ích lớn nhất: review thiết kế diễn ra **trước khi có code**, lúc đổi hướng chỉ là sửa một tài liệu.

### 2.2. Auto mode khi rào chắn đã đủ chắc

Ở auto mode, engineer duyệt plan một lần, sau đó Claude tự sửa file mà không hỏi từng lần. Khi các rào chắn đã trưởng thành (`CLAUDE.md` tốt, skill chứa policy, hook chặn hành động nguy hiểm, test chạy được), auto mode trở thành mặc định cho việc thường ngày: spec chặt, phạm vi ảnh hưởng nhỏ, code đã có test bao.

Sự chú ý của con người chuyển từ việc ngồi xem agent sửa từng dòng sang việc **review artifact sau một phiên làm việc dài**. Đây cũng là điều kiện để chạy song song và để khép vòng ở Maintain.

### 2.3. `CLAUDE.md`: thứ một người mới cần biết

`CLAUDE.md` chứa những gì một người mới vào team cần biết: quy ước, lệnh build và test, kiến trúc, và các lỗi team hay gặp. Agent đọc file này đầu mỗi session.

Cách làm:

1. Chạy `/init` trong repo để Claude sinh bản đầu.
2. Cắt bớt, chỉ giữ thứ người mới cần trong ngày đầu: lệnh build, test, lint, quy ước quan trọng, và những chỗ Claude hay làm sai.
3. Commit vào gốc repo để cả team dùng chung một bản, sửa đổi được review như code.
4. Quy tắc làm việc: **Claude sai một lỗi hai lần thì ghi cách sửa vào `CLAUDE.md`.**
5. Giữ dưới một trang. Claude đọc toàn bộ mỗi session, nên thứ đã cũ chỉ chiếm chỗ mà không giúp gì.

### 2.4. Skill: tri thức tổ chức thành thứ dùng được

Skill là cách biến tri thức của tổ chức thành chỉ dẫn rõ ràng, có phiên bản, áp dụng rộng và cập nhật tập trung khi policy đổi.

Quy tắc phân biệt:
- Tri thức **phải được áp dụng nhất quán** ở nhiều nơi → skill.
- Thứ thuộc về `CLAUDE.md` hoặc prompt → không viết thành skill.

Nói cách khác, `CLAUDE.md` giữ ngữ cảnh làm việc của repo, prompt giữ yêu cầu của từng lần, còn skill dành cho tri thức cần áp dụng giống nhau ở nhiều nơi.

Cách làm: chọn một kiến thức hôm nay đang bị áp dụng không đều (chuẩn bảo mật, quy ước API, quy tắc brand), viết thành skill, để trong repo hoặc phân phối toàn tổ chức qua plugin, thử xem skill có được kích hoạt với nhiều cách hỏi khác nhau không. Khi policy đổi, sửa skill và người sở hữu policy duyệt.

Điểm quan trọng nhất: **skill là control mang tính khuyến nghị**. Nó làm agent nhiều khả năng áp đúng policy, nhưng không gì ép một session phải tuân theo. Policy bắt buộc phải có hook đứng sau.

### 2.5. Hook: rào chắn lúc build

Hook là lớp bắt buộc đứng sau skill. Ở bước build, agent chủ yếu sửa file và chạy lệnh, nên đây là nơi hook được kích hoạt nhiều nhất. Hook có thể:

- Chặn sửa đường dẫn được bảo vệ (code sinh tự động, package đã đóng băng).
- Chạy formatter và linter sau mỗi lần sửa file để code không lệch chuẩn dần.
- Giữ credential không lọt vào diff.

Hai lưu ý từ playbook:
- Hook ở bước build phải **nhanh và chỉ kiểm file vừa đổi**. Kiểm tra nặng như chạy cả bộ test để ở commit hoặc PR.
- Hook **hỏi người duyệt không nên đặt ở bước build**. Nó đưa con người quay lại đường găng của mọi session đang chạy song song. Để hook duyệt ở [Deploy](05-deploy.md).

### 2.6. Chạy song song và subagent

Hai khái niệm khác nhau:

| | Session song song | Subagent |
|---|---|---|
| Là gì | Một Claude Code đầy đủ khác, làm việc khác, trong git worktree riêng | Trợ lý có phạm vi hẹp chạy bên trong một session, có context và giới hạn công cụ riêng |
| Biết về nhau | Không. Thứ chung duy nhất là engineer điều phối | Báo kết quả về session chính |
| Dùng cho | Tăng số việc làm cùng lúc | Việc lặp lại: kiểm app có chạy, đơn giản hoá code, khảo sát codebase |

Cách làm:
1. Dùng plan để tách việc thành các phần sửa file khác nhau. Việc đụng chung file thì làm tuần tự trong một session.
2. Mỗi việc song song một worktree riêng.
3. Bắt đầu với 2–3 session. **Giới hạn thực tế là số luồng một người review được tử tế.** Chỉ thêm session khi review vẫn theo kịp.
4. Biến việc lặp lại thành subagent, định nghĩa trong `.claude/agents/`, commit vào git để cả team dùng chung.

Playbook đưa ví dụ một subagent `verifier`: chạy app, thử hành vi vừa đổi và hai luồng lân cận, báo lại những gì không khớp `plan.md`, và chỉ báo cáo chứ không tự sửa.

### 2.7. Sống chung với hệ thống cũ

Phần này nằm trong Build nhưng áp dụng cho mọi artifact. Xem mục "Sống chung với hệ thống cũ" trong [tổng quan](00-tong-quan.md).

### Đo hiệu quả

| Play | Chỉ số dẫn | Chỉ số trễ |
|---|---|---|
| Plan mode | Tỉ lệ thay đổi merge được ngay từ lượt code đầu | Số vòng làm lại mỗi thay đổi, mức khớp giữa diff và `plan.md` |
| `CLAUDE.md` | Số lần Claude lặp lại lỗi lẽ ra file đã chặn | Thời gian tới PR đầu tiên được merge của người mới |
| Skill | Thời gian từ lúc policy đổi tới lúc skill được cập nhật | Số finding trong review liên quan tới policy đó, kỳ vọng giảm về gần 0 |
| Song song | Số session đồng thời mỗi engineer khi chất lượng review vẫn giữ | Số thay đổi merge mỗi tuần, đọc cùng tỉ lệ làm lại |

---

## 3. Chỗ còn hở

Phần này là phân tích, không có trong bài gốc.

### Plan cho mọi việc thành thủ tục

Bắt viết và commit `plan.md` cho việc sửa một dòng là lãng phí. Playbook nói plan mode là mặc định nhưng không nói khi nào được bỏ qua. Không có ranh giới thì team sẽ hoặc làm hình thức, hoặc lặng lẽ bỏ luôn.

### `CLAUDE.md` cũ dần mà không ai để ý

Quy tắc "sai hai lần thì ghi vào" làm file dài ra. Quy tắc "giữ dưới một trang" làm file phải ngắn lại. Không ai được giao việc dọn. Sau vài tháng, file chứa những dòng đúng với code cũ.

### Không biết skill có thật sự được kích hoạt

Playbook khuyên thử bằng nhiều cách hỏi, nhưng thử một lần lúc viết thì chưa đủ. Model mới, skill mới thêm vào có thể làm skill cũ không còn được chọn.

### Song song va vào đặc thù mobile

Với app iOS, file `project.pbxproj` thay đổi gần như mỗi khi thêm file. Hai session song song cùng thêm file sẽ xung đột ở đây dù code không liên quan. Build iOS và Android cũng chậm hơn web nhiều, và simulator ngốn tài nguyên. Ba session song song trên một máy có thể chậm hơn một session.

---

## 4. Giải pháp ban đầu

### 4.1. Phân hạng thay đổi để quyết định mức plan

| Hạng | Ví dụ | Plan |
|---|---|---|
| Rất nhỏ | Sửa chữ, đổi màu, đổi hằng số | Không cần plan mode |
| Nhỏ | Sửa bug khoanh vùng rõ, một file | Plan mode, không cần commit `plan.md` |
| Vừa | Tính năng nhỏ, vài file | Plan mode, commit `plan.md` |
| Lớn | Đụng nhiều module, đổi kiến trúc | `plan.md` + tech lead duyệt trước khi code |

Ghi bảng này vào `CLAUDE.md` để agent tự đề xuất hạng khi bắt đầu.

### 4.2. Năm câu chất vấn plan

Dùng cố định mỗi lần duyệt plan:

1. File nào thay đổi, có file nào bất ngờ không?
2. Thay đổi này có thể làm hỏng luồng nào đang chạy?
3. Bước nào rủi ro nhất, và làm sao biết nó hỏng?
4. Test nào sẽ fail nếu làm sai?
5. Có cách nào đơn giản hơn mà Claude đã bỏ qua?

### 4.3. Chăm `CLAUDE.md` như một file code

- Có một người chịu trách nhiệm, thường là tech lead.
- Mỗi dòng trong mục "những chỗ Claude hay sai" ghi kèm tháng thêm vào.
- Mỗi tháng rà một lần: dòng nào ba tháng không còn tác dụng thì xoá hoặc chuyển thành hook.
- Một quy tắc đã được ghi mà Claude vẫn sai thì không ghi thêm lần nữa. Chuyển thành hook.

### 4.4. Bộ thử kích hoạt skill

Với mỗi skill quan trọng, viết 5 câu yêu cầu với nhiều cách diễn đạt. Lưu thành một file. Chạy lại mỗi khi thêm skill mới hoặc đổi model, xem skill có được nạp không. Bộ này về sau chính là một phần của eval ở [Phase 4](04-test.md).

### 4.5. Bộ hook khởi đầu cho repo mobile

| Hook | Chặn hoặc làm gì |
|---|---|
| Đường dẫn được bảo vệ | Không sửa `Pods/`, code sinh tự động, file khoá phiên bản phụ thuộc |
| Format sau khi sửa | Chạy `swiftformat` hoặc `ktlint` trên file vừa đổi |
| Credential | Chặn diff chứa key, file `.p12`, `google-services.json` có dữ liệu thật |
| Phiên bản phụ thuộc | Chặn tự ý nâng version trong `Package.resolved`, `build.gradle` |

### 4.6. Giảm xung đột khi chạy song song trên iOS

- Cân nhắc sinh file project từ cấu hình (XcodeGen, Tuist) hoặc dùng Swift Package cho module mới. Khi đó `project.pbxproj` không còn là điểm xung đột.
- Chia việc song song theo module, không theo màn hình.
- Bắt đầu với 2 session, đo thời gian build. Nếu máy chậm rõ, giữ ở 2.

---

## 5. Tuần đầu tiên

1. Chạy `/init`, cắt `CLAUDE.md` xuống dưới một trang, thêm bảng phân hạng thay đổi.
2. Thêm hai hook đơn giản nhất: chặn đường dẫn được bảo vệ và chạy formatter.
3. Làm 3 việc hạng vừa bằng plan mode, commit `plan.md`, ghi lại bao nhiêu việc merge được từ lượt code đầu.
4. Ghi mọi lỗi Claude lặp lại. Cuối tuần chuyển thành dòng trong `CLAUDE.md` hoặc hook.
5. Thử 2 session song song trên hai module khác nhau ít nhất một ngày.
