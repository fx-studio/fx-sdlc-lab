# Kiểm tay T0–T13: hướng dẫn cho người chạy

Bảng kiểm tay của plan `khach-khong-mat-viec` (mục "Kiểm tay") chưa ai chạy từ SDLC-3. Chủ kênh nhận chạy ở tập SDLC-4 (2026-10-29).
Đây là **lượt nghiệm thu của người thật** duy nhất trong demo: máy không điền thay ô nào.

## Chuẩn bị

1. Lấy bản `main` mới nhất của repo (đã sửa T-013, T-014). Ở gốc repo: `python3 -m http.server -d app 8000`.
2. **Máy tính:** mở http://localhost:8000 bằng Chrome và Safari (localhost được coi là an toàn, nút Thêm chạy).
3. **Điện thoại cần HTTPS.** App dùng `crypto.randomUUID`, chỉ chạy ở HTTPS hoặc localhost. Mở `http://<IP máy>:8000` từ điện thoại
   thì nút Thêm hỏng, và đó **không** phải lỗi của tính năng sao lưu. Cách có HTTPS: bật GitHub Pages cho thư mục `app/` của
   `fx-sdlc-lab` (việc ra ngoài, chủ kênh quyết), hoặc một tunnel HTTPS. Không có thì bỏ cột điện thoại, ghi "không có HTTPS".
4. File để thử nằm sẵn ở `demo/sdlc-4/kiem-tay-files/` (tạo bằng `app/backup.js`, dữ liệu mẫu):

   | File | Dùng ở | Là gì |
   |---|---|---|
   | `T4-30-viec.json` | T4, T10 | file sao lưu hợp lệ, 30 việc |
   | `T5-a-qua-lon.json` | T5, T10 | file sao lưu hợp lệ nhưng 1,7 MB (trên giới hạn 1 MB) |
   | `T5-b-truong-la.json` | T5, T10 | có trường lạ `"x": 1` |
   | `T5-c-van-ban.txt` · `T5-h-anh.png` | T5 | không phải file sao lưu |
   | `T5-d-trung-id.json` · `T5-e-tieu-de-rong.json` · `T5-f-createdAt-chu.json` | T5 | ba file ở AC10 |
   | `T5-g-todos-rong.json` | T5 | `todos: []` |
   | `T6-tieu-de-html.json` | T6 | một việc có tiêu đề `<img src=x onerror=alert(1)>` |

5. Đoạn console hay dùng (DevTools → Console):
   - Nạp N việc: `localStorage.setItem('todo.v1', JSON.stringify(Array.from({length: 12}, (_, i) => ({id: crypto.randomUUID(), title: 'Việc ' + i, done: i % 3 === 0, createdAt: Date.now() - i})))); location.reload()` (đổi 12 thành 2000 cho T0)
   - Làm hỏng danh sách đã lưu (T9, T10): `localStorage.setItem('todo.v1', '{hỏng'); location.reload()`
   - Làm đầy bộ nhớ (T8): `try { for (let i = 0; ; i++) localStorage.setItem('day' + i, 'x'.repeat(500000)) } catch (e) { console.log('đầy') }`, dọn lại: `Object.keys(localStorage).filter(k => k.startsWith('day')).forEach(k => localStorage.removeItem(k))`
   - Xem giá trị đang lưu: `localStorage.getItem('todo.v1')`

Câu M1–M17 mà bảng nhắc tới nằm ở `app/backup.js` (`MESSAGES`) và bảng Câu chữ của plan. T0 bản gốc so "bản cũ" với "bản mới"; ở đây
làm gọn: nạp 2.000 việc dạng cũ bằng console rồi mở app (dạng dữ liệu không đổi qua các bản).

## Ghi kết quả

Điền vào bảng dưới (`đạt` / `không` + một câu ghi chú; ô không thử để trống). Plan đã `accepted` nên agent không sửa được nó: người
chạy demo sẽ chép bảng này vào mục "Kiểm tay" của plan trong một commit dưới tên người kiểm.

Người chạy: ______ · Ngày: ______ · Máy tính: ______ (trình duyệt, bản) · Điện thoại: ______ · Địa chỉ đã mở: ______

| T | Việc làm (rút gọn, bản đủ ở plan) | Chrome máy tính | Safari máy tính | Điện thoại |
|---|---|---|---|---|
| T0 ★ | 2.000 việc dạng cũ: mở app đủ việc, đúng trạng thái, không dải báo; thêm, đánh dấu, xoá; tải lại vẫn giữ | | | |
| T1 ★ | Sao lưu 3 việc: tên `todo-sao-luu-<hôm nay>.json`, thụt lề, đúng nội dung, câu "Đã sao lưu 3 việc". Danh sách trống: câu M1, không tải | | | |
| T2 | Tắt mạng: sao lưu và nhập vẫn chạy; tab Network không có request | | | |
| T3 ★ | Xoá dữ liệu trang: thấy câu danh sách trống, không dải báo; nhập file T1: không hỏi, đủ 3 việc; tải lại vẫn còn | | | |
| T4 ★ | 12 việc, nhập `T4-30-viec.json`: hộp hỏi; Huỷ → 12, tải lại 12; Thay → 30, tải lại 30. Lặp với 1 việc | | | |
| T5 ★ | Từng file T5-a → T5-h bị từ chối, câu nói vì sao + làm gì tiếp, danh sách không đổi | | | |
| T6 | Nhập `T6-tieu-de-html.json`: hiện đúng chữ, không alert | | | |
| T7 ★ | 5.000 việc × 200 ký tự (console, đổi tiêu đề thành `'x'.repeat(200)`): sao lưu tải file > 1 MB, thấy câu M2 | | | |
| T8 | Bộ nhớ đầy, thêm việc: câu M3, việc còn trên màn hình; tải lại mất việc đó. 12 việc, nhập 30, đồng ý: câu M17, tải lại 12 | | | |
| T9 | `{hỏng`: dải báo, không dòng trống; thêm 2, đánh dấu 1, xoá 1: không hộp thoại, giá trị vẫn `{hỏng`; tải lại: dải báo vẫn hiện | | | |
| T10 ★ | Đọc lỗi: thêm 2, sao lưu: file đúng 2 việc, `todo.v1` vẫn `{hỏng`. Nhập 30 khi chưa thêm: hỏi, Thay → dải báo mất. File quá lớn và file trường lạ khi đọc lỗi: từ chối, không hỏi | | | |
| T11 | Màn hình chính có câu "Danh sách chỉ được lưu trên trình duyệt này…" | | | |
| T12 | Chỉ bàn phím (Tab, Enter/Space, Esc) sao lưu, chọn file, Thay/Huỷ; VoiceOver đọc nhãn hai nút, câu hỏi, thông báo | | | |
| T13 | Lọc "Đã xong" khi chưa có việc xong: không hiện câu danh sách trống (đúng chỗ lỗi T-014 vừa sửa) | | | |

★ = bắt buộc. Thời gian ước: máy tính ~40 phút một trình duyệt.
