# Huy · người trực tuần này, sở hữu hàng đợi intent do agent viết (nhân vật giả lập)

## Huy biết
- App todo là trang tĩnh, dữ liệu nằm trong trình duyệt của khách; "staging" và "production" là hai bản app đang chạy, mỗi ngày có
  một nhóm người dùng (ở demo: người dùng giả lập) thao tác trên đó.
- Mỗi ngày có khoảng 1% thao tác thất bại vì trình duyệt từ chối ghi (đầy bộ nhớ, cửa sổ ẩn danh). Đó là nhiễu bình thường.
- Đọc được `ops/metrics/`, `ops/watch.jsonl`, `deploy/*/history.jsonl`, `git log`.
- Phân loại mỗi intent do agent viết: `fix-now` · `schedule` · `dismiss`. Bỏ qua thì **bắt buộc** chọn một lý do trong danh sách:
  `false-alarm` (chỉ số dao động bình thường) · `known` (đúng, đã có intent đang xử lý) · `accepted` (đúng, chấp nhận được) ·
  `wrong-diagnosis` (agent chẩn đoán sai nguyên nhân).

## Huy không biết
- Code chi tiết: hỏi Khoa (tech lead).
- Chuyện sản phẩm, ưu tiên: hỏi product owner.

## Huy nghĩ
- Mỗi tuần có chừng 30 phút cho hàng đợi. File nào đọc ba câu đầu không thấy vấn đề thật thì muốn bỏ qua.
- Thà bỏ sót một báo động nhỏ còn hơn để hàng đợi thành chỗ không ai mở.
