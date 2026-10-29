# Kiểm tay T0–T13, phần máy chạy (Chromium headless)

Chạy 2026-10-29 15:25 bằng `demo/sdlc-4/kiem-tay-may.py` trên `app/` của cây làm việc. Không thay người kiểm: chỉ Chromium, không Safari, không điện thoại, không bàn phím thật, không trình đọc màn hình (T12 để người), không ai nhìn giao diện.


## T0 · đạt · 2.000 việc dạng cũ mở bằng bản mới; thêm, đánh dấu, xoá; tải lại vẫn giữ

- ✅ đủ 2.000 việc
- ✅ không dải báo
- ✅ tải lại: 2.000 việc (thêm 1, xoá 1)
- ✅ việc mới còn sau tải lại
- ✅ dòng đếm đúng số việc chưa xong

## T1 · đạt · Sao lưu 3 việc; danh sách trống thì không tải file

- ✅ có file tải về
- ✅ tên todo-sao-luu-<hôm nay>.json
- ✅ thụt lề
- ✅ đúng 3 việc, đúng nội dung
- ✅ câu Đã sao lưu 3 việc
- ✅ danh sách trống: không tải
- ✅ danh sách trống: câu M1

## T2 · đạt · Mất mạng: sao lưu và nhập vẫn chạy, không có request nào

- ✅ sao lưu khi mất mạng
- ✅ nhập khi mất mạng
- ✅ không request nào trong lúc sao lưu và nhập

## T3 · đạt · Xoá dữ liệu trang: câu danh sách trống; nhập file T1 không hỏi, đủ 3 việc, tải lại còn

- ✅ câu danh sách trống
- ✅ không dải báo
- ✅ không hỏi
- ✅ đủ 3 việc
- ✅ tải lại còn 3

## T4 · đạt · 12 việc, nhập 30: hỏi; huỷ giữ 12; đồng ý thành 30; lặp với 1 việc

- ✅ 12 việc: hộp hỏi đúng câu
- ✅ 12 việc: huỷ giữ 12
- ✅ 12 việc: huỷ, tải lại 12
- ✅ 12 việc: đồng ý thành 30
- ✅ 12 việc: tải lại 30
- ✅ 12 việc: không có Undo
- ✅ 1 việc: hộp hỏi đúng câu
- ✅ 1 việc: huỷ giữ 1
- ✅ 1 việc: huỷ, tải lại 1
- ✅ 1 việc: đồng ý thành 30
- ✅ 1 việc: tải lại 30
- ✅ 1 việc: không có Undo

## T5 · đạt · Tám file sai: từng file bị từ chối, nói vì sao và làm gì tiếp, danh sách không đổi

- ✅ T5-a-qua-lon.json: từ chối, không hỏi, không đổi
- ✅ T5-a-qua-lon.json: câu có 'giữ nguyên' và 'Hãy'
- ✅ T5-b-truong-la.json: từ chối, không hỏi, không đổi
- ✅ T5-b-truong-la.json: câu có 'giữ nguyên' và 'Hãy'
- ✅ T5-c-van-ban.txt: từ chối, không hỏi, không đổi
- ✅ T5-c-van-ban.txt: câu có 'giữ nguyên' và 'Hãy'
- ✅ T5-d-trung-id.json: từ chối, không hỏi, không đổi
- ✅ T5-d-trung-id.json: câu có 'giữ nguyên' và 'Hãy'
- ✅ T5-e-tieu-de-rong.json: từ chối, không hỏi, không đổi
- ✅ T5-e-tieu-de-rong.json: câu có 'giữ nguyên' và 'Hãy'
- ✅ T5-f-createdAt-chu.json: từ chối, không hỏi, không đổi
- ✅ T5-f-createdAt-chu.json: câu có 'giữ nguyên' và 'Hãy'
- ✅ T5-g-todos-rong.json: từ chối, không hỏi, không đổi
- ✅ T5-g-todos-rong.json: câu có 'giữ nguyên' và 'Hãy'
- ✅ T5-h-anh.png: từ chối, không hỏi, không đổi
- ✅ T5-h-anh.png: câu có 'giữ nguyên' và 'Hãy'

## T6 · đạt · Tiêu đề <img src=x onerror=alert(1)> hiện đúng chữ, không alert

- ✅ hiện đúng chữ
- ✅ không alert, không thẻ img

## T7 · đạt · 5.000 việc × 200 ký tự: file > 1 MB tải được, thấy câu M2

- ✅ tải được file > 1 MB
- ✅ câu M2

## T8 · đạt · Bộ nhớ đầy: thêm việc báo M3, tải lại mất; nhập 30 đồng ý báo M17, tải lại còn 12

- ✅ câu M3
- ✅ việc còn trên màn hình
- ✅ tải lại mất việc đó
- ✅ nhập lỗi khi lưu: câu M17
- ✅ tải lại còn 12

## T9 · đạt · Danh sách đã lưu hỏng: dải báo; thêm, đánh dấu, xoá không ghi đè; tải lại dải báo vẫn hiện

- ✅ {hỏng: dải báo
- ✅ {hỏng: không câu danh sách trống
- ✅ {hỏng: không hộp thoại
- ✅ {hỏng: giá trị giữ nguyên, không khoá mới
- ✅ {hỏng: tải lại không còn việc, dải báo vẫn hiện
- ✅ {"a": 1}: dải báo
- ✅ {"a": 1}: không câu danh sách trống
- ✅ {"a": 1}: không hộp thoại
- ✅ {"a": 1}: giá trị giữ nguyên, không khoá mới
- ✅ {"a": 1}: tải lại không còn việc, dải báo vẫn hiện

## T10 · đạt · Đọc lỗi rồi sao lưu, nhập (M6, M7), bộ nhớ đầy, file sai

- ✅ sao lưu khi đọc lỗi: file đúng 2 việc
- ✅ todo.v1 vẫn {hỏng
- ✅ chưa thêm: câu M6
- ✅ huỷ: dải báo vẫn hiện, vẫn {hỏng
- ✅ đồng ý: dải báo biến mất
- ✅ thêm 1, tải lại 31
- ✅ đã thêm 3: câu M7
- ✅ huỷ: còn 3 việc, vẫn {hỏng
- ✅ đồng ý: 30 việc, hết dải báo
- ✅ {hỏng + bộ nhớ đầy, đồng ý: dải báo vẫn hiện, vẫn {hỏng
- ✅ đọc lỗi + T5-a-qua-lon.json: từ chối, không hỏi
- ✅ đọc lỗi + T5-b-truong-la.json: từ chối, không hỏi

## T11 · đạt · Màn hình chính có câu nơi lưu danh sách

- ✅ có câu 'chỉ được lưu trên trình duyệt này'

## T13 · đạt · Lọc 'Đã xong' khi chưa có việc xong: không hiện câu danh sách trống (chỗ lỗi T-014)

- ✅ không hiện câu danh sách trống
- ✅ dòng đếm vẫn 4 (chỗ lỗi T-013)

**82/82 phép kiểm đạt, 13/13 dòng đạt.**

