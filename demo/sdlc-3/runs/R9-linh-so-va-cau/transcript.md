# R9-linh-so-va-cau

Chạy 2026-10-27 11:56 ở `persona-empty` (thư mục riêng của lượt này), chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Bạn là Linh. Spec khach-khong-mat-viec (đã accepted) có hai chỗ được đề xuất sửa sau khi code xong:
(1) F4 bước 1 và tiêu chí 23 viết "xoá dữ liệu trình duyệt". Câu trên app (Linh chốt, Mai xác nhận đạt P4) viết "xoá dữ liệu trang web", vì gần tên mục khách thấy khi xoá trong trình duyệt. Đề xuất: sửa spec theo chữ "dữ liệu trang web" để spec và app khớp nhau.
(2) F2 bước 8: "Nếu lưu sau khi nhập bị lỗi: danh sách cũ được giữ nguyên..., app báo như F3" (dùng chung câu "Thay đổi vừa rồi chưa được lưu. Hãy sao lưu ra file, rồi xoá bớt việc đã xong."). Lúc đó việc khách vừa làm là nhập file nên "thay đổi vừa rồi" hơi mơ hồ. Linh đề xuất câu riêng: "Chưa nhập được file. Danh sách cũ của bạn vẫn nguyên. Hãy xoá bớt việc đã xong rồi thử lại." Đã kiểm bằng test: khi đó danh sách cũ còn nguyên, không mất, không lẫn. Đề xuất: sửa F2 bước 8 thành "app báo câu riêng cho lúc nhập".
Ngoài spec: (3) hộp xác nhận đang viết số "2001", đề xuất viết "2.001" (dấu chấm hàng nghìn).
Chốt chữ: (2) câu cuối cho lúc nhập lỗi khi lưu, giữ câu bạn đề xuất hay sửa; (3) số có nhiều chữ số trong mọi câu của app viết thế nào (ví dụ 2001, 12, 1000). Trả lời ngắn.

## Tool call (0)

(không có)

## Claude · 12 s

Chốt như sau:

**(1) Đồng ý.** Sửa F4 bước 1 và tiêu chí 23 thành "xoá dữ liệu trang web", để spec khớp với app.

**(2) Giữ nguyên câu tôi đề xuất:** "Chưa nhập được file. Danh sách cũ của bạn vẫn nguyên. Hãy xoá bớt việc đã xong rồi thử lại." F2 bước 8 sửa thành "app báo câu riêng cho lúc nhập". Câu này đúng với việc khách vừa làm, và test đã xác nhận danh sách cũ còn nguyên nên nói "vẫn nguyên" là thật.

**(3) Đồng ý viết "2.001".** Quy tắc cho mọi câu của app:
- Số từ 1.000 trở lên có dấu chấm hàng nghìn: 1.000, 2.001, 12.500.
- Số dưới 1.000 viết trơn: 12, 999.
- Năm và ngày không dùng dấu chấm: "2026" vẫn viết là 2026.

Mọi câu có số phải theo cùng một cách, không để chỗ có dấu, chỗ không. Nhờ Khoa kiểm cách áp dụng cho đủ các câu.
