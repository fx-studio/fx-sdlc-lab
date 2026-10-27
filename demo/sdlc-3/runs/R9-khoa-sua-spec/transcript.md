# R9-khoa-sua-spec

Chạy 2026-10-27 11:57 ở `persona-empty` (thư mục riêng của lượt này), chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Bạn là Khoa. Spec khach-khong-mat-viec (đã accepted) có hai chỗ được đề xuất sửa sau khi code xong:
(1) F4 bước 1 và tiêu chí 23 viết "xoá dữ liệu trình duyệt". Câu trên app (Linh chốt, Mai xác nhận đạt P4) viết "xoá dữ liệu trang web", vì gần tên mục khách thấy khi xoá trong trình duyệt. Đề xuất: sửa spec theo chữ "dữ liệu trang web" để spec và app khớp nhau.
(2) F2 bước 8: "Nếu lưu sau khi nhập bị lỗi: danh sách cũ được giữ nguyên..., app báo như F3" (dùng chung câu "Thay đổi vừa rồi chưa được lưu. Hãy sao lưu ra file, rồi xoá bớt việc đã xong."). Lúc đó việc khách vừa làm là nhập file nên "thay đổi vừa rồi" hơi mơ hồ. Linh đề xuất câu riêng: "Chưa nhập được file. Danh sách cũ của bạn vẫn nguyên. Hãy xoá bớt việc đã xong rồi thử lại." Đã kiểm bằng test: khi đó danh sách cũ còn nguyên, không mất, không lẫn. Đề xuất: sửa F2 bước 8 thành "app báo câu riêng cho lúc nhập".
Ngoài spec: (3) hộp xác nhận đang viết số "2001", đề xuất viết "2.001" (dấu chấm hàng nghìn).
Về kỹ thuật và bảo mật, (1) (2) (3) có rủi ro gì không? Mỗi cái một dòng. Đổi (2) là hạng gì theo bảng phân hạng (Trivial/Small/Medium/Large)?

## Tool call (1)

1. Bash · command=ls -la && grep -ril "trivial\|policy-security\|khach-khong-mat-viec" . 2>/dev/null | head

## Claude · 26 s

Thư mục làm việc đang trống: mình không có spec, policy-security hay bảng phân hạng để đối chiếu. Phần dưới dựa trên mô tả của bạn. Hạng của (2) là suy luận, chưa đối chiếu bảng.

1. **"Dữ liệu trang web"**: không có rủi ro kỹ thuật hay bảo mật, vì đây chỉ là chữ. Chữ này khớp tên mục trong Chrome ("Cookie và dữ liệu trang web") và Safari ("Dữ liệu trang web"). Cần sửa luôn tiêu chí 23 và mọi test đang so chuỗi.

2. **Câu riêng cho lúc nhập**: hành vi giữ danh sách cũ thì an toàn, nhưng câu mới bỏ lời nhắc sao lưu.
   - Nếu trước đó đã có lần lưu lỗi (F3), danh sách "vẫn nguyên" trên màn hình vẫn chưa nằm trong bộ nhớ trình duyệt. Tải lại trang sẽ mất, mà câu mới không báo.
   - Đề nghị: nếu đang có thay đổi chưa lưu thì dùng câu cũ hoặc thêm "hãy sao lưu ra file". Chỉ dùng câu riêng khi danh sách cũ đã được lưu.
   - Câu hiển thị bằng textContent như các câu lỗi khác, và phải khác câu từ chối file sai định dạng.

3. **"2.001"**: không có rủi ro bảo mật, đây chỉ là định dạng số.
   - Nên dùng `toLocaleString('vi-VN')` thay vì ghép dấu chấm bằng tay.
   - Chỉ dùng để hiển thị, đừng để chỗ nào đọc ngược lại thành số.
   - Test nào đang so chuỗi "2001" phải sửa theo.

**Hạng của (2): Small.** Mình đoán vì không có bảng.
- Không đổi định dạng file, giới hạn S1 hay logic lưu, nên không lên Medium.
- Nhưng đây là thêm một câu mới ở đường lỗi của spec đã accepted, cộng với trường hợp biên ở trên. Vậy nên không phải Trivial.
- Nếu làm theo đề nghị ở dòng 2 thì đổi thêm một nhánh điều kiện, vẫn là Small.
- Nếu bảng ghi Trivial là "chỉ đổi chữ, không đổi hành vi", thì (1) và (3) là Trivial, còn (2) là Small.
- Cần Linh chốt lại câu chữ và Mai xác nhận lại P4 nếu câu thay đổi so với bản đã duyệt.
