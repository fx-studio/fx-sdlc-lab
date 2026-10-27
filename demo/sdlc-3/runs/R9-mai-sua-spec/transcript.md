# R9-mai-sua-spec

Chạy 2026-10-27 11:56 ở `persona-empty` (thư mục riêng của lượt này), chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Bạn là Mai. Spec khach-khong-mat-viec (đã accepted) có hai chỗ được đề xuất sửa sau khi code xong:
(1) F4 bước 1 và tiêu chí 23 viết "xoá dữ liệu trình duyệt". Câu trên app (Linh chốt, Mai xác nhận đạt P4) viết "xoá dữ liệu trang web", vì gần tên mục khách thấy khi xoá trong trình duyệt. Đề xuất: sửa spec theo chữ "dữ liệu trang web" để spec và app khớp nhau.
(2) F2 bước 8: "Nếu lưu sau khi nhập bị lỗi: danh sách cũ được giữ nguyên..., app báo như F3" (dùng chung câu "Thay đổi vừa rồi chưa được lưu. Hãy sao lưu ra file, rồi xoá bớt việc đã xong."). Lúc đó việc khách vừa làm là nhập file nên "thay đổi vừa rồi" hơi mơ hồ. Linh đề xuất câu riêng: "Chưa nhập được file. Danh sách cũ của bạn vẫn nguyên. Hãy xoá bớt việc đã xong rồi thử lại." Đã kiểm bằng test: khi đó danh sách cũ còn nguyên, không mất, không lẫn. Đề xuất: sửa F2 bước 8 thành "app báo câu riêng cho lúc nhập".
Ngoài spec: (3) hộp xác nhận đang viết số "2001", đề xuất viết "2.001" (dấu chấm hàng nghìn).
(1) và (2) có đụng gì tới policy riêng tư không? Một dòng mỗi cái.

## Tool call (0)

(không có)

## Claude · 9 s

1. **Không đụng policy.** Chỉ đổi chữ trong spec cho khớp câu trên app, nói vẫn là xoá dữ liệu nằm trong trình duyệt, nên P4 vẫn đạt và tôi đồng ý sửa.
2. **Không đụng policy.** Câu riêng chỉ báo lỗi và dặn khách xoá bớt việc đã xong rồi thử lại. Không có dữ liệu nào rời trình duyệt, không thêm dữ liệu, không lưu chỗ nào mới, nên P1 đến P5 đều không liên quan. Danh sách cũ còn nguyên là chuyện test của Khoa, tôi tin kết quả đó.

Mục (3) là chuyện chữ trên app, tôi không có ý kiến. Linh quyết.
