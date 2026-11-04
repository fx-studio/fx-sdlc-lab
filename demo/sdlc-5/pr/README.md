# Pull request cục bộ của demo SDLC-5

Repo này không có remote: mỗi pull request là một nhánh `pr/<n>-<slug>` ở git cục bộ. Nhánh không theo zip/PR lên GitHub, nên diff của từng
nhánh được chép ra đây (so với base của chính nó, `review/<n>/base`). Mô tả, review, duyệt của từng PR ở `review/<n>/`.

| PR | Trạng thái |
|---|---|
| 1 · nút Huỷ hiện viền | **đã merge** (Khoa duyệt, giả lập); thử lại T12 trên Firefox đạt |
| 2 · đổi tên việc (ba lỗi gài + `/watch-pr` sửa) | chưa merge: chờ plan (Medium) + tech lead |
| 3 · "Đã xong hết" | **đã merge** |
| 4 · hạn chót, bản A (không dòng trần), 950 dòng | đóng, không merge: giữ để so |
| 5 → 6 → 7 · hạn chót, bản B (có dòng trần), xếp chồng | chưa merge: chờ review của người, kiểm tay, rồi PR B (sao lưu `version: 2`) |
