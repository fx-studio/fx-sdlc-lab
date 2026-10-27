# R8 · đáp án người chạy demo chốt TRƯỚC khi chạy (2026-10-27)

Theo bảng Size trong `CLAUDE.md`:

1. Đổi màu nền nút "Thêm" sang xanh lá → **Trivial** (một hằng màu)
2. Dòng đếm ghi "1 việc chưa xong" cả khi có 2 việc → **Small** (một lỗi khoanh được trong một file). Lỗi giả định, app không có lỗi này.
3. Thêm nút "Xoá các việc đã xong" → **Medium** (tính năng nhỏ, vài file: app.js, index.html, test; xoá hàng loạt chạm policy-security)
4. Gắn nhãn (tag) cho từng việc, lọc theo nhãn → **Large** (đổi dạng dữ liệu đã lưu: store, backup.js kiểm khoá chính xác, test)
