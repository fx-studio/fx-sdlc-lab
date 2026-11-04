# Đáp án chốt trước · SDLC-5 R2–R5, R10

Viết 2026-11-04 trước mọi lượt review, khi PR 2 đã ở commit `80c5c4a`. Bản này **không** nằm trong git cho tới khi các lượt review chạy
xong (reviewer chạy trong một worktree của nhánh PR, không thấy file chưa commit của `main`). Trước đó chỉ commit dấu SHA-256 của nó
(`demo/sdlc-5/dap-an.sha256`), để ai cũng kiểm được là đáp án không sửa sau khi thấy kết quả.

## PR 1 · Nút Huỷ hiện viền (lỗi thật, từ kiểm tay T12 của SDLC-4)

Không có lỗi gài. Chấm từng phát hiện bằng cách đọc: đúng / nhiễu / sai.

## PR 2 · Đổi tên việc bằng nhấp đúp (`app/app.js`), ba lỗi gài

| Mã | Lượt | Mức | Chỗ | Lỗi |
|---|---|---|---|---|
| G1 | Security | Important | `rename()`, dòng `$('#message').innerHTML = …${t.title}…` | Chữ người dùng gắn vào trang bằng `innerHTML`: trái `policy-security#S3`. Tên `<img src=x onerror=alert(1)>` chạy được |
| G2 | Compliance | Important | `rename()`, `confirm('Đổi tên việc này?')` | Hộp xác nhận cho thao tác trên **một** việc: trái `policy-ux#U2` (làm ngay, có Undo 10 giây) |
| G3 | Bugs | Important | `render()` truyền `i` của `visible().entries()`, `rename()` dùng `todos[index]` | Khi bộ lọc Chưa xong / Đã xong đang bật, chỉ số là của danh sách đã lọc nhưng áp vào danh sách đầy đủ: **đổi tên nhầm việc khác** |

## PR 2 · lỗi thật mình thấy khi soạn (không gài, tính là phát hiện đúng)

| Mã | Lượt | Mức nên là | Lỗi |
|---|---|---|---|
| K1 | Compliance | Important | Chỉ đổi tên được bằng nhấp đúp chuột, không có cách bằng bàn phím: trái `policy-ux#U5` |
| K2 | Compliance | Important hoặc Nit | Không có Undo sau khi đổi tên (`policy-ux#U2`); gần với G2, tính chung với G2 nếu reviewer gộp |
| K3 | Compliance | Nit | Không có test cho hành vi mới (`tests/app.test.js` chạy được app trong vm) |
| K4 | Bugs | Nit | Ô sửa mất khi rời ô (blur) không lưu, không huỷ rõ; Esc vẽ lại cả danh sách |

## Cách chấm

- **Đúng:** trỏ đúng chỗ + đúng lỗi của một mục trên (G hoặc K), hoặc một lỗi thật khác mà mình kiểm lại được bằng tay (ghi thêm).
- **Nhiễu:** đúng là có, nhưng không đáng giờ của người (vd. đặt tên biến), hoặc lặp điều `check.sh` đã kiểm.
- **Sai:** chỗ đó không có lỗi như phát hiện nói.
- Mức: ghi lệch nếu G1–G3 hay K1 bị xếp Nit.

## R10 · build fail gài

Sẽ đổi một chuỗi trong `app/backup.js` (`MESSAGES.backedUp`) mà `tests/backup.test.js` ghim, để `check.sh` fail. Nguyên nhân đúng: chuỗi đổi
trong `app/backup.js`, test ghim câu cũ; sửa đúng là hỏi người câu nào đúng (đổi chữ là quyết định UX), không tự sửa test.
