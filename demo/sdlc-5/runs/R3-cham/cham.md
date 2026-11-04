# R2–R3 · chấm từng phát hiện

Chấm 2026-11-04 theo đáp án niêm phong (`demo/sdlc-5/dap-an.sha256`, commit `2fd2a93`, trước mọi lượt review). Người chấm: người chạy
demo, đọc từng phát hiện trong `review/<n>/<lượt>/comment.md`. Không đếm tổng thay cho đọc.

## R2 · PR 1 (lỗi thật: nút Huỷ, 9 dòng)

| Lượt | Cách | Phát hiện | Đáng kể |
|---|---|---|---|
| R2-review | có `REVIEW.md` | 1 Important · 2 Nit | Important: `CLAUDE.md` lỗi thời ("tests 44", giờ 45), đúng "Review also flags when a change has made CLAUDE.md outdated". Hai nit: test và sửa chung một commit; test chỉ kiểm chữ CSS |
| R2-generic | "review this PR", repo **có** `REVIEW.md` | 4 | **Không phải đối chứng**: reviewer đọc `REVIEW.md` vì `CLAUDE.md` trỏ tới, tự gắn nhãn `[Compliance · Important]` trong chữ |
| R2-generic-khong-file | như trên, xoá `REVIEW.md` khỏi bản checkout | 2 | **Vẫn không phải đối chứng**: reviewer chạy `git show HEAD:REVIEW.md`, file còn trong lịch sử git |
| R2-generic-repo-khong-file | repo tạm không lịch sử, không `REVIEW.md`, bỏ dòng trỏ trong `CLAUDE.md` | 5, không mức | **Nghi chính chẩn đoán**: theo ghi chép T12 (Tab + Enter chọn "Thay"), Huỷ có thể chưa từng có focus, khi đó luật CSS không sửa gì; đề xuất phép thử Enter ngay khi hộp mở. Cũng bắt `CLAUDE.md` lỗi thời. Lượt có `REVIEW.md` không nêu nghi vấn này |

Chẩn đoán của PR 1 **chưa ai kiểm trên trình duyệt** lúc review (Claude nói rõ trong R1). **Kiểm sau đó (2026-11-04, chủ kênh, Firefox, bàn phím):
Huỷ hiện viền khi hộp mở, nên chẩn đoán đúng và nghi vấn của lượt đối chứng sai.** Phát hiện của reviewer nghe hợp lý vẫn có thể sai.

## R3 · PR 2 (đổi tên việc, ba lỗi gài + lỗi thật khi soạn)

Mã theo đáp án: G1 innerHTML (S3) · G2 confirm cho một việc (U2) · G3 chỉ số của danh sách đã lọc · K1 không dùng được bằng bàn phím (U5) ·
K2 không Undo (U2) · K3 không test · K4 blur/Enter rỗng. **Ngoài đáp án, mình kiểm lại:** X1 câu "Đã đổi tên" đè câu báo lưu lỗi
(`commit()` đã `show(persist(...).message)`), trái U1: **lỗi thật, mình bỏ sót khi soạn đáp án** · X2 chữ nằm trong `<label>` của ô đánh
dấu nên mỗi cú nhấp của nhấp đúp bấm ô đánh dấu: hợp lý theo HTML, chưa thử trên trình duyệt.

| Lượt | G1 | G2 | G3 | K1 | K2 | K3 | K4 | X1 | X2 | Nhiễu / sai | Mức của G1–G3, K1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R3-review-a (có file) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 1 nit nhỏ (chuỗi nên vào `MESSAGES`): đúng, Nit hợp lý | Important cả bốn |
| R3-review-b (có file) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | 0 | Important cả bốn |
| R3-khong-file-a | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | 1: "Base 04ee584 không khớp b6712a1", **do cách mình dựng repo đối chứng** | không có mức |
| R3-khong-file-b | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | 1: như trên | không có mức |

**Kết luận một lượt, ví dụ thật, không phải thống kê:**

- Giả thuyết "không có `REVIEW.md` thì bỏ lỗi lệch policy" **ra ngược**: cả bốn lượt bắt đủ G1–G3. Policy nằm sẵn trong skill của repo
  (SDLC-2), reviewer tự đọc.
- Thứ `REVIEW.md` thêm vào là **mức nghiêm trọng và bảng đếm máy đọc được** (`tally.json`): "5–6 Important" là thứ một cổng merge đọc
  được; tám dòng không mức thì không.
- Trên PR nhỏ (PR 1), lượt có file **hẹp hơn**: đi đúng ba lượt, không đặt câu hỏi ngoài khung; lượt không file nghi cả chẩn đoán.
- Mọi lượt đều bắt lỗi thật mình bỏ sót (X1): đáp án của người cũng thiếu.

Chi phí: R2 bốn lượt 0,94 USD · R3 bốn lượt 0,85 USD.
