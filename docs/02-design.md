# Phase 2 · Design: spec trong một session

> Thuộc bộ tài liệu đọc *The AI-native SDLC playbook* (Anthropic, 21/8/2026). Xem [tổng quan](00-tong-quan.md).

---

## Tóm gọn

Requirements và design không còn là hai giai đoạn của hai team. Claude nhận `intent.md` đã được duyệt, viết ra một bản spec gộp cả hai, tuân theo các policy của tổ chức đã đóng gói thành skill. Product owner duyệt spec chứ không viết spec. Policy được áp ngay lúc viết, không phải chờ đến lúc review mới phát hiện vi phạm.

---

## 1. Vấn đề của cách cũ

Ở quy trình truyền thống, analyst viết requirements, rồi designer đọc lại để làm thiết kế. Hai bước, hai team.

Việc tách đôi có lý do: mỗi bước có người chịu trách nhiệm rõ ràng. Nhưng giá phải trả là:

- **Chậm.** Mỗi lần chuyển tay là một lần chờ.
- **Thất thoát.** Designer phải hiểu lại thứ analyst đã hiểu. Mỗi lần diễn giải lại là một lần lệch.
- **Policy phát hiện muộn.** Vi phạm về bảo mật, compliance hay chuẩn UX thường chỉ lộ ra khi review, có khi vài tuần sau. Lúc đó sửa đã tốn kém.

---

## 2. Playbook xử lý thế nào

### Một session thay cho hai giai đoạn

Khi `intent.md` được duyệt, Claude dùng nó để viết spec. Session được nạp sẵn các skill của tổ chức: brand, bảo mật, compliance, UX. Đầu ra là một spec mà team engineering lập kế hoạch được, kèm danh sách **các chỗ đáng lo** mà Claude tự đánh dấu.

Với giao diện, product owner có thể dựng mock trực tiếp từ `intent.md` bằng Claude Design (đang beta), chỉnh qua lại, rồi chuyển sang Claude Code để build.

### Cách làm

1. Product owner mở session có sẵn các skill của tổ chức và đính kèm `intent.md`.
2. Prompt chỉ rõ file intent, nêu các ràng buộc, và yêu cầu Claude đánh dấu những chỗ đáng lo. Playbook gợi ý tiến hoá theo ba bước:
   - Ban đầu chạy tay.
   - Sau đó đóng gói thành slash command cấp tổ chức.
   - Cuối cùng biến việc merge `intent.md` thành điểm kích hoạt: một job không tương tác tự chạy, sinh `spec.md` dưới dạng pull request. Lúc đó, lần đầu tiên product owner chạm vào là lúc review.
3. Product owner so spec với ý tưởng: spec có giải quyết đúng vấn đề không, các câu hỏi mở trong intent đã được trả lời hay được chuyển tiếp?
4. Xử lý các chỗ đáng lo trước tiên. Đây là những điểm một analyst giỏi sẽ báo lên. Product owner giải quyết từng điểm với người sở hữu policy tương ứng, trước khi engineering nhìn thấy spec.
5. Commit `spec.md` cạnh `intent.md`. Cặp file này ghi lại cái được yêu cầu và cái được quyết định.
6. Product owner quyết định có cho sang Build hay không. Với việc rủi ro cao, hỏi thêm tech lead. Quyết định này luôn do người đưa ra, và việc chấp nhận spec kích hoạt plan mode ở bước Build.

### Prompt mẫu trong playbook

Ý chính của prompt: đọc intent, viết spec tích hợp vào codebase hiện tại, áp các skill để tuân theo brand, bảo mật và UX, ghi đầy đủ vào `spec.md`, và **nói rõ chỗ nào đáng lo, đặc biệt khi các policy mâu thuẫn nhau**.

Câu cuối là phần quan trọng. Nó buộc agent nói ra xung đột thay vì tự chọn một bên.

### Governance

Policy đang có hiệu lực được đọc và áp ngay lúc viết spec. Git lưu spec, prompt đã sinh ra nó, và **phiên bản của các skill tại thời điểm đó**. Product owner ký duyệt spec và chuyển các chỗ đáng lo tới người sở hữu policy.

### Đo hiệu quả

| Loại | Chỉ số |
|---|---|
| Dẫn | Khoảng thời gian giữa commit `intent.md` và commit `spec.md` của cùng một thay đổi |
| Trễ | Số lần `spec.md` bị sửa sau khi `plan.md` đầu tiên đã commit, tức là phải làm lại requirements khi đã bắt đầu build |

---

## 3. Chỗ còn hở

Phần này là phân tích, không có trong bài gốc.

### Product owner duyệt thứ vượt chuyên môn của mình

Spec bây giờ chứa cả phần kỹ thuật: dữ liệu, tích hợp, ràng buộc bảo mật. Product owner được giao việc duyệt nhưng không phải lúc nào cũng đủ nền để thấy chỗ sai. Playbook gợi ý hỏi tech lead với những việc mà tổ chức xếp vào loại rủi ro cao, nhưng để tổ chức tự định nghĩa, không đưa tiêu chí cụ thể.

### Spec trông đầy đủ chưa chắc đã đúng

Agent viết spec rất trôi chảy. Một bản spec mạch lạc, đủ đề mục dễ khiến người duyệt tin rằng mọi thứ đã được tính. Thứ nguy hiểm nhất không phải là chỗ agent đánh dấu đáng lo, mà là **giả định agent tự đặt ra rồi không nói**.

### Người sở hữu policy thành nút thắt

Mỗi chỗ đáng lo phải được giải quyết với người sở hữu policy. Nếu một người phụ trách bảo mật nhận câu hỏi từ hai mươi spec mỗi tuần, ta lại có một hàng đợi mới, chỉ là ở chỗ khác.

### Chất lượng skill quyết định chất lượng spec

Cơ chế "áp policy ngay lúc viết" chỉ tốt bằng skill. Skill viết mơ hồ hoặc đã cũ thì spec tuân theo một policy sai, mà nhìn vẫn có vẻ đúng quy trình.

---

## 4. Giải pháp ban đầu

### 4.1. Bắt agent liệt kê giả định

Thêm vào prompt và template một mục bắt buộc: **những gì agent đã tự giả định vì intent không nói**. Người duyệt đọc mục này đầu tiên.

```markdown
## Giả định (agent tự đặt, cần xác nhận)
- Người dùng đã đăng nhập khi vào màn hình này
- Dữ liệu trạng thái lấy từ API hiện có, không cần endpoint mới
- Không cần hỗ trợ ngoại tuyến
```

Mỗi dòng là một câu hỏi có/không. Product owner xác nhận nhanh hơn đọc lại cả spec.

### 4.2. Template spec gợi ý

```markdown
# Spec: <tên>
Từ: intent/<file>.md · Skill áp dụng: security@v3, ux@v5, brand@v2

## Mục tiêu (một đoạn)
## Không làm
## Luồng người dùng
## Dữ liệu và tích hợp
## Ràng buộc từ policy (ghi rõ skill nào, điều nào)
## Giả định
## Chỗ đáng lo (mỗi chỗ: mô tả, policy liên quan, người cần hỏi)
## Tiêu chí nghiệm thu (viết dạng kiểm được)
## Câu hỏi chuyển tiếp từ intent
```

Hai điểm mấu chốt:
- **Ghi phiên bản skill ngay đầu file.** Khi policy đổi, biết ngay spec nào cần xem lại.
- **Tiêu chí nghiệm thu viết dạng kiểm được.** Đây sẽ là đầu vào cho test ở [Phase 4](04-test.md), nên viết sao cho chuyển thành test được.

### 4.3. Định nghĩa "rủi ro cao" từ trước

Đừng để mỗi product owner tự cảm nhận. Viết sẵn danh sách, ví dụ:

- Đụng tới thanh toán, xác thực, dữ liệu cá nhân
- Thay đổi schema dữ liệu
- Thêm phụ thuộc bên ngoài mới
- Ảnh hưởng tới hơn một team

Spec thuộc danh sách này bắt buộc có tech lead duyệt. Có thể để Claude tự gắn nhãn rủi ro dựa trên danh sách khi viết spec.

### 4.4. Hẹn thời gian phản hồi cho người sở hữu policy

- Lập bảng: mỗi skill policy có một người sở hữu và một người thay thế.
- Đặt thời gian phản hồi, ví dụ 2 ngày làm việc. Quá hạn thì chuyển lên trưởng nhóm.
- Đếm số câu hỏi mỗi người sở hữu nhận mỗi tuần. Con số tăng đều là tín hiệu skill chưa đủ rõ, cần viết lại để agent tự xử lý được nhiều hơn.

### 4.5. Bắt đầu skill từ chỗ đau nhất

Đừng cố viết skill cho mọi policy. Xem lại review gần đây, tìm policy nào bị nhắc đến nhiều nhất, viết skill cho policy đó trước. Một skill tốt cho một policy hay vi phạm có giá trị hơn mười skill chung chung.

### 4.6. Lưu ý cho dự án mobile

Spec cho app di động nên có thêm các mục mà agent hay bỏ sót:

- Trạng thái màn hình: đang tải, rỗng, lỗi, mất mạng
- Quyền hệ điều hành cần xin (camera, vị trí, thông báo) và luồng khi người dùng từ chối
- Hành vi khi app vào nền rồi quay lại
- Khác biệt iOS và Android nếu có
- Những điểm có thể vướng quy định review của App Store hoặc Google Play

Quy định của store là ứng viên tốt để đóng gói thành skill: thay đổi ít, vi phạm thì tốn cả tuần chờ review lại.

---

## 5. Tuần đầu tiên

1. Lấy một `intent.md` đã duyệt từ Phase 1.
2. Chạy prompt sinh spec có kèm mục giả định và chỗ đáng lo.
3. Product owner và tech lead cùng đọc, ghi lại: bao nhiêu giả định sai, bao nhiêu chỗ đáng lo là thật.
4. Viết một skill cho policy gây nhiều vấn đề nhất trong lần đọc đó.
5. Chạy lại lần hai, so sánh số giả định sai.

Nếu lần hai ít giả định sai hơn, skill đang làm đúng việc của nó.
