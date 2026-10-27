# Trả lời giả định và chỗ đáng lo của spec sao lưu (bước 0 của SDLC-3)

Người chạy demo gom từ các lượt `runs/B0b-*` → `B0e-*` (nhân vật giả lập, sonnet, chỉ biết hồ sơ ở `personas/`). Spec được hỏi: bản
`/write-spec` chạy lại với `policy-ux@2` (`runs/B0a-write-spec-ux2`).

| Dòng | Trả lời | Ai | Run |
|---|---|---|---|
| A1 | Có. Khách tự gửi file qua Zalo, email | Thảo | B0d |
| A2 | Có. Nhập lại = thay toàn bộ, không gộp | Thảo | B0d |
| A3 | **Không.** Nhập file thay danh sách **luôn hỏi trước** theo S2, kể cả khi đang có đúng 1 việc. Linh trả lời "Có" ở B0b, rút lại ở B0e sau khi đọc lời Khoa | Khoa · Linh | B0c · B0e |
| A4 | Có | Mai | B0b |
| A5 | Có | Mai | B0b |
| A6 | Có | Thảo | B0d |
| A7 | Có. Từ chối cả file | Khoa | B0b |
| A8 | Có | Linh | B0b |
| A9 | Có. Tải lại trang thì mất thay đổi chưa lưu, chấp nhận | Khoa | B0b |
| A10 | Có | Linh | B0b |
| A11 | Có | Linh · Thảo | B0b · B0d |
| A12 | Có, với điều kiện spec không thêm khoá hay trường nào vào bộ nhớ trình duyệt; nếu thêm (ví dụ giữ danh sách cũ để Undo) thì khớp dòng 2 | Khoa | B0c |
| C1 | Chấp nhận. Tiêu chí "máy này thêm thì máy kia thấy" chuyển sang intent đồng bộ sau; hai tiêu chí đổi máy / xoá dữ liệu ghi rõ "khi đã sao lưu trước" | Thảo | B0d |
| C2 | Phương án **(a)**: giữ S1 ở 1 MB; sao lưu vẫn tạo file và báo ngay. Câu báo (Linh duyệt): **"File sao lưu đã lưu, nhưng quá lớn nên app không nhập lại được."** Linh thiên về (b) nhưng để Khoa quyết | Khoa · Linh · Thảo | B0b · B0d · B0e |
| C3 | **Đưa vào lần này**, phạm vi hẹp: đọc dữ liệu trong trình duyệt bị lỗi thì không ghi đè, và báo cho khách; không làm khôi phục. Khoa xác nhận vẫn vừa hai tuần | Thảo · Khoa | B0d · B0e |
| C4 | Để **intent riêng** (Undo cho nút xoá một việc); spec ghi rõ chỗ lệch U2 còn mở, Thảo nhận việc mở intent đó | Linh · Thảo | B0b · B0d |

## Vòng hai: bốn giả định mọc thêm khi thiết kế C3

Lượt `B0f` cập nhật spec theo bảng trên; thiết kế phần dữ liệu hỏng (F5) làm mọc thêm A13–A16.

| Dòng | Trả lời | Ai | Run |
|---|---|---|---|
| A13 | Có. Thêm: truy cập bộ nhớ trình duyệt ném lỗi cũng tính là "đọc lỗi" | Khoa | B0g |
| A14 | Có. Lời nhắc là một dải báo cố định trên cùng, không bật hộp thoại mỗi lần thao tác | Khoa · Linh | B0g |
| A15 | Có | Khoa · Thảo | B0g · B0h |
| A16 | **Không**, đổi lời báo thành: "Không đọc được danh sách đã lưu trên trình duyệt này. Việc bạn thêm hoặc sửa lúc này sẽ không được lưu. Nếu có file sao lưu, hãy bấm "Nhập từ file"." | Linh | B0g |

Thảo (B0h): **cho spec sang Build.**

## Vòng ba: ba giả định mọc thêm khi đưa vòng hai vào spec

Lượt `B0i` đưa A13–A16 vào thân spec, mọc thêm A17–A19.

| Dòng | Trả lời | Ai | Run |
|---|---|---|---|
| A17 | Có. Ghi thất bại thì vẫn ở trạng thái đọc lỗi | Khoa · Linh | B0j |
| A18 | Có | Linh | B0j |
| A19 | **Không.** Khi trên màn hình có việc chưa lưu, lời xác nhận nêu số lượng: "Thay danh sách đã lưu không đọc được và 3 việc bạn vừa thêm (chưa lưu) bằng 30 việc trong file?". Không có thì dùng mẫu A15 | Khoa | B0j |

Số giả định qua ba vòng: **12 → 4 → 3**. Mỗi vòng trả lời làm lộ ra chi tiết thiết kế mới.

## Vòng bốn và chốt

`B0k` đưa A17–A19 vào thân spec, mọc thêm **A20** (ghi thất bại khi nhập trong lúc đọc lỗi thì màn hình hiện gì). Khoa, Linh: **Có**
(`B0l`). Để dừng vòng lặp, người chạy demo ghi thẳng câu trả lời A20 dưới dòng giả định, không cho Claude viết lại thân spec lần nữa.

Số giả định mở qua bốn vòng: **12 → 4 → 3 → 1 → 0**. Cùng lúc người chạy demo sửa mục Success criteria của intent theo C1 (Thảo chốt),
rồi đổi spec sang `Status: accepted`, commit dưới tên "Thảo (product owner, giả lập)".
