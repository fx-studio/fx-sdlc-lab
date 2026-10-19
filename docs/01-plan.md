# Phase 1 · Plan: ý tưởng thành `intent.md`

> Thuộc bộ tài liệu đọc *The AI-native SDLC playbook* (Anthropic, 21/8/2026). Xem [tổng quan](00-tong-quan.md).

---

## Tóm gọn

Ý tưởng không còn phải chờ ai đó rảnh để viết thành tài liệu. Người có ý tưởng tự làm việc với Claude, ghi lại thành một file `intent.md` bằng chính ngôn ngữ của mình, rồi commit vào git. Product owner duyệt file đó, và việc duyệt kích hoạt bước thiết kế.

---

## 1. Vấn đề của cách cũ

Một ý tưởng ở quy trình truyền thống phải đi qua nhiều trạm trước khi có người bắt tay làm: vào backlog, viết thành user story, ước lượng story point, mang ra buổi refinement. Mỗi trạm đổi chủ một lần.

Có hai cái giá phải trả:

- **Chậm.** Từ lúc có ý tưởng tới lúc engineering nhận việc có thể mất vài tuần, chủ yếu là thời gian chờ.
- **Méo.** Qua mỗi lần chuyển tay, ý gốc bị diễn giải lại. Thứ đến tay engineer đã cách người nghĩ ra nó vài bước.

Thêm một rào cản ít được nói: người có ý tưởng thường không phải người viết tài liệu. Một nhân viên vận hành thấy vấn đề phải đi thuyết phục ai đó trong team product viết giúp. Nhiều ý tưởng chết ở bước này.

---

## 2. Playbook xử lý thế nào

### Một file, ba con đường vào

`intent.md` là điểm khởi đầu của cả vòng lặp. Nó có thể đến từ ba nguồn:

- Một người có ý tưởng.
- Một ticket được tạo.
- Một cảnh báo từ production (xem [Maintain](06-maintain.md)).

Dù đến từ đâu, quy tắc chung là product owner đọc và sửa file trước khi nó được commit chính thức.

### Cách làm

1. Người có ý tưởng kể vấn đề với Claude theo cách tự nhiên: hôm nay không làm được gì, ai bị ảnh hưởng, tốt hơn trông thế nào, cái gì nằm ngoài phạm vi. Không cần ngôn ngữ chuyên môn.
2. Claude hỏi lại như một business analyst sẽ hỏi: phạm vi, người dùng, ràng buộc, thế nào là thành công. Hai bên trao đổi cho đến khi ý tưởng đủ cụ thể.
3. Claude viết kết quả theo template của tổ chức. Template này nên được đóng gói thành skill do người kỹ thuật dựng và trưởng nhóm duyệt.
4. Người có ý tưởng sửa những chỗ Claude hiểu sai.
5. Commit file vào nơi chứa intent chung. Git tự ghi tác giả và thời gian.

### File trông thế nào

Ví dụ trong playbook là một yêu cầu tự tra cứu trạng thái hồ sơ bảo hiểm. Cấu trúc gồm: vấn đề, kết quả mong muốn, người dùng và hệ thống bị ảnh hưởng, ràng buộc, câu hỏi còn mở. Ngắn, không quá một trang.

### Hạ tầng cần có

- Người không phải engineer có quyền dùng Claude (claude.ai hoặc Cowork).
- Một template thống nhất cho `intent.md`.
- Một chỗ chứa intent có quản lý phiên bản. Với một sản phẩm, đơn giản nhất là thư mục `intent/` trong repo. Repo riêng cho intent chỉ đáng làm khi intent trải trên nhiều repo.
- Một connector tới GitHub để Claude commit thay cho người không biết git.

Người dựng hạ tầng là team platform hoặc engineering, làm một lần. Họ quyết định ai được ghi vào thư mục intent, vì người đóng góp sẽ đến từ khắp tổ chức.

### Governance

Bằng chứng là chính file đã commit: tác giả, thời gian, lịch sử sửa. Quyết định chấp nhận hay từ chối của product owner được ghi lại dưới dạng merge hoặc đóng review.

### Đo hiệu quả

| Loại | Chỉ số |
|---|---|
| Dẫn | Thời gian từ cuộc trò chuyện đầu tiên tới khi `intent.md` được commit. Kỳ vọng giảm từ vài tuần xuống vài giờ |
| Trễ | Tỉ lệ intent được chấp nhận sang bước Design. Số lần intent bị sửa sau khi `spec.md` đầu tiên đã commit |

---

## 3. Chỗ còn hở

Phần này là phân tích, không có trong bài gốc.

### Product owner thành nút thắt mới

Khi ai cũng tạo được intent trong vài phút, số intent tăng nhanh hơn khả năng đọc của product owner. Hàng đợi chỉ dời từ "chờ người viết" sang "chờ người duyệt". Playbook đo thời gian tạo intent nhưng không đo thời gian intent nằm chờ.

### Chất lượng phụ thuộc người kể

Claude hỏi lại được, nhưng chỉ hỏi được những gì người kể gợi ra. Nếu người kể không biết hệ thống có ràng buộc gì, file vẫn trông đầy đủ mà thiếu thứ quan trọng. Một file viết trôi chảy dễ khiến người duyệt tin rằng nó đã được nghĩ kỹ.

### Trùng lặp

Ba người thấy cùng một vấn đề sẽ tạo ba intent. Không có bước nào trong playbook kiểm tra trùng.

### Yêu cầu đến từ khách hàng bên ngoài

Playbook giả định người có ý tưởng ở trong tổ chức. Với dự án outsource, yêu cầu đến từ khách hàng, thường qua một người trung gian như BrSE, và đôi khi bằng ngôn ngữ khác. Khách không vào repo của mình để viết intent.

---

## 4. Giải pháp ban đầu

Các đề xuất dưới đây chưa được kiểm chứng ở quy mô lớn. Mục đích là có điểm khởi đầu để thử và điều chỉnh.

### 4.1. Đặt "điều kiện sẵn sàng" cho intent

Trước khi commit, cho Claude tự kiểm file theo một danh sách ngắn. Thiếu mục nào thì hỏi lại người kể chứ không tự điền.

```markdown
## Kiểm trước khi commit intent.md
- [ ] Vấn đề nói được ai đang gặp, gặp lúc nào
- [ ] Có ít nhất một bằng chứng (số liệu, ticket, lời phàn nàn, ảnh chụp)
- [ ] Có mục "Không làm" ghi rõ ngoài phạm vi
- [ ] Tiêu chí thành công đo được, không phải "tốt hơn", "nhanh hơn"
- [ ] Câu hỏi mở được liệt kê, không bị giấu trong văn bản
```

Đóng gói danh sách này vào cùng skill template. Như vậy mọi intent đi qua cùng một cửa lọc.

### 4.2. Template mở rộng

So với ví dụ trong playbook, thêm ba mục giúp product owner duyệt nhanh hơn:

```markdown
# Intent: <tên ngắn>
Tác giả: <tên> (<team>) · Trạng thái: draft · Nguồn: <người / ticket / cảnh báo>

## Vấn đề
## Bằng chứng            ← thêm: vì sao biết đây là vấn đề thật
## Kết quả mong muốn
## Tiêu chí thành công   ← thêm: con số hoặc hành vi kiểm được
## Người và hệ thống bị ảnh hưởng
## Ràng buộc
## Không làm
## Mức ảnh hưởng         ← thêm: thấp / vừa / cao, để product owner xếp thứ tự
## Câu hỏi mở
```

### 4.3. Giới hạn hàng đợi duyệt

- Đặt trần số intent đang chờ duyệt, ví dụ 10. Vượt trần thì intent mới vẫn được tạo nhưng nằm ở trạng thái "chờ xếp hàng".
- Intent chờ quá 14 ngày tự động được đánh dấu để product owner quyết: nhận, gộp hay đóng.
- Thêm một chỉ số dẫn mà playbook chưa có: **thời gian từ lúc commit tới lúc được duyệt**.

### 4.4. Kiểm trùng trước khi tạo

Thêm một bước vào skill: trước khi viết file mới, Claude tìm trong thư mục `intent/` các file có vấn đề tương tự. Có thì đề xuất bổ sung vào file cũ thay vì tạo file mới.

### 4.5. Intent hai lớp cho yêu cầu từ khách hàng

Với dự án làm cho khách nước ngoài:

- **Lớp nguyên văn.** Giữ lời khách viết bằng ngôn ngữ gốc (email, tin nhắn, biên bản họp).
- **Lớp diễn giải.** Phần intent chuẩn do team viết cùng Claude, bằng ngôn ngữ làm việc của team.
- **Câu hỏi mở thành danh sách gửi khách.** Mục này tách ra để BrSE gửi một lần, thay vì hỏi rải rác.

Hai lớp giúp đối chiếu khi có tranh cãi về phạm vi sau này: khách nói gì, team hiểu thế nào.

---

## 5. Tuần đầu tiên

1. Tạo thư mục `intent/` trong một repo đang hoạt động.
2. Viết template và danh sách kiểm, đóng gói thành một skill.
3. Chọn 3 yêu cầu đang nằm trong backlog, viết lại thành `intent.md` cùng Claude.
4. Product owner duyệt cả ba và ghi lại mất bao lâu.
5. Cuối tuần, so với thời gian một yêu cầu tương tự đi qua quy trình cũ.

Nếu product owner thấy đọc ba file này nhanh hơn đọc ba ticket cũ, đó là tín hiệu đúng hướng.
