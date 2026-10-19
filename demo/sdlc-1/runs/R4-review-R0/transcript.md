# R4-review-R0

Chạy 2026-10-19 06:38. Nguyên văn, không sửa.

## Yêu cầu

Use the intent-reviewer subagent to review demo/sdlc-1/runs/R0-lan-khong-skill/intent-R0.md. The originator (Lan, customer support) said only this, nothing else: "Dạo này khách cứ email than là mất hết việc trong app, nhất là sau khi đổi điện thoại. Mình muốn làm gì đó để khách không mất việc nữa." The repo (app/) is also a valid source. Return the subagent's report verbatim, in Vietnamese.

## Claude · 101 s

# Báo cáo review: `demo/sdlc-1/runs/R0-lan-khong-skill/intent-R0.md`

Nguồn đối chiếu: câu gốc của Lan ("Dạo này khách cứ email than là mất hết việc trong app, nhất là sau khi đổi điện thoại. Mình muốn làm gì đó để khách không mất việc nữa."), cùng `app/`, `tickets/` và `intent/`. Tôi không sửa file nào.

**Đọc trước:** Bản nháp không có dòng nào ghi nguồn. Nó hiểu sản phẩm là app điện thoại cài từ store. Nhưng repo cho thấy app là trang web tĩnh, dữ liệu nằm trong `localStorage` của trình duyệt (`app/store.js`, dòng 1–2). Đã có sẵn một intent khác của Lan về đúng vấn đề này.

## 1. Câu không có nguồn

**Các câu có nguồn:** tiêu đề; "khách liên tục email phàn nàn là mất hết việc"; "nhiều nhất là sau khi đổi điện thoại"; "Việc khách đã tạo không bị mất"; "đổi sang điện thoại mới"; "Có vẻ dữ liệu chỉ nằm trên máy". Câu cuối được `app/store.js` xác nhận, nhưng bản nháp không trích nguồn và viết như đang đoán ("Có vẻ").

| # | Trích nguyên văn | Loại | Ghi chú |
|---|---|---|---|
| 1 | "khi đổi máy, cài lại app hay xoá dữ liệu app thì việc của khách cũng mất theo" | (b) | "đổi máy" khớp `store.js`. Còn "cài lại app" thì sai: app là HTML/JS tĩnh, không cài được. `store.js` nói "Clearing site data, switching browser or switching device" |
| 2 | "Với một app quản lý việc, mất dữ liệu là lỗi nặng nhất" | (b) | |
| 3 | "khách mất lòng tin, không dám nhập việc quan trọng vào app nữa, rồi bỏ app" | (b) | Lan không nói có khách bỏ app |
| 4 | "(cùng hệ điều hành hoặc khác hệ điều hành)" | (b) | |
| 5 | "gỡ rồi cài lại app" | (b) | Repo cho thấy app không cài được |
| 6 | "mất hoặc hỏng điện thoại" | (a) | Suy ra từ "đổi điện thoại" |
| 7 | "Lấy lại việc phải **dễ**: khách không cần biết kỹ thuật, cũng không cần nhớ đã làm gì trước đó." | (b) | Câu này ngầm loại hướng "xuất/nhập file thủ công" ở câu hỏi mở 3 |
| 8 | "Cộng tác hoặc chia sẻ việc giữa nhiều người." | (b) | Phạm vi do người viết tự chọn, chưa ai duyệt |
| 9 | "Bản web hay bản desktop." | (b) | Mâu thuẫn với repo: app chính là bản web. Loại bản web là loại cả sản phẩm |
| 10 | "Đồng bộ thời gian thực giữa nhiều máy dùng cùng lúc. Có thì tốt, nhưng không bắt buộc." | (b) | |
| 11 | "Khách đổi máy, đăng nhập hoặc khôi phục" | (c) | "đăng nhập" là giải pháp (tài khoản) |
| 12 | "(cả việc đã xong lẫn chưa xong, ghi chú và hạn chót)" | (b) | Mâu thuẫn với `app/app.js` dòng 1: "A todo has: id, title, done, createdAt. No due date". Hạn chót mới là đề xuất ở T-012 |
| 13 | "Số email than mất dữ liệu giảm về gần 0 sau khi ra bản mới." | (b) | Mốc này không ai đặt, không có số hiện tại, không có hạn thời gian. "ra bản mới" mặc định là có phát hành qua store |
| 14 | "Khách đang dùng app **không bị mất dữ liệu trong lúc chuyển** sang cơ chế mới." | (a) | |
| 15 | "việc của khách có thể chứa thông tin cá nhân" | (a) | |
| 16 | "Nếu đưa dữ liệu lên server thì phải nói rõ với khách, và có cách để khách xoá dữ liệu của mình." | (c) | Đã mặc định giải pháp là server |
| 17 | "người không muốn tạo tài khoản vẫn dùng được app như hiện nay" | (c) | Đã mặc định giải pháp là tài khoản. Ý "như hiện nay" (chưa có tài khoản) thì đúng theo `store.js` |
| 18 | "**Vẫn dùng được khi không có mạng.**" | (b) | |

**Tổng: 18 câu không có nguồn. (a) 3, (b) 12, (c) 3.**

Thêm hai điều:
- Câu hỏi mở 1 ("Hiện app lưu dữ liệu ở đâu") đã có câu trả lời trong `app/store.js`.
- Câu hỏi mở 2 ("iOS, Android hay cả hai") đặt sai khung, vì app chạy trên trình duyệt.

## 2. Checklist (`.claude/skills/write-intent/checklist.md`)

- **Problem:** pass. Có nói ai bị ("khách") và khi nào ("sau khi đổi điện thoại"), dù "khách" còn chung chung.
- **Evidence:** fail. Không có mục Evidence. Không có con số, ticket hay email cụ thể nào.
- **Out of scope:** pass về hình thức, vì mục có và không trống. Nhưng cả 3 dòng đều không có nguồn, và "Bản web hay bản desktop" mâu thuẫn với repo.
- **Success criteria:** pass về hình thức, vì tiêu chí 1 quan sát được. Nhưng tiêu chí 1 đòi những trường không tồn tại ("ghi chú và hạn chót"), còn "gần 0" không có số hiện tại và không có hạn thời gian.
- **Open questions:** fail. Không câu nào ghi ai trả lời. Phần thân vẫn còn câu hỏi ẩn ("Có vẻ dữ liệu chỉ nằm trên máy", "Có thì tốt, nhưng không bắt buộc").
- **Sourced:** fail. Không câu nào trong Constraints có nguồn, và không có mục Evidence.

## 3. Trùng lặp

- `intent/2026-10-19-khach-khong-mat-viec.md`: **trùng trực tiếp**. Cùng người kể (Lan), cùng vấn đề, cùng ngày. Bản đó có nguồn cho từng câu, đúng với repo (localStorage, trình duyệt), và tự ghi mục Out of scope còn trống. Lưu ý: các con số trong bản đó ("23 email", "3 khách nói sẽ bỏ app") được gắn [originator]. Câu gốc Lan đưa cho lần review này không có các số đó, nên tôi không kiểm được.
- `intent/2026-10-19-khach-doanh-nghiep-sao-luu.md`: **gần trùng**. Bản này của Minh, cũng về nỗi sợ mất danh sách việc, nhưng nhắm tới việc khách tự giữ bản sao lưu. Hướng "xuất/nhập file" ở câu hỏi mở 3 của R0 chồng lên intent này.
- `intent/2026-10-19-han-chot-cho-viec.md` (T-012): không trùng vấn đề. Nhưng R0 kéo "hạn chót" vào tiêu chí thành công, nên bị chồng phạm vi.

## 4. Câu hỏi cho Lan (người kể)

1. Có bao nhiêu email, trong khoảng thời gian nào? Có thể chép các email (đã bỏ thông tin cá nhân) vào `tickets/` để người duyệt tự kiểm không?
2. Trong email, khách mất việc khi nào: đổi điện thoại, xoá dữ liệu trình duyệt, hay đổi trình duyệt? Mỗi loại bao nhiêu email? Câu trả lời quyết định nên chọn đồng bộ, sao lưu hay cảnh báo.
3. Có khách nào dùng app trên nhiều máy và muốn thấy cùng một danh sách không? Câu này quyết định đồng bộ là bắt buộc hay ngoài phạm vi.
4. Khách cần lấy lại việc đã mất, hay chỉ cần không bị mất từ giờ?
5. Có khách nào nói sẽ bỏ hoặc đã bỏ app vì chuyện này không? Câu này ảnh hưởng mức ưu tiên.

Decision: product owner

---

*Ngoài báo cáo:* Một số connector claude.ai chưa được cấp quyền: Atlassian Rovo, Canva, Figma, Gmail, Google Calendar, Miro, Notion, Postman, Slack, draw.io. Lần review này không cần đến chúng. Khi nào cần, bạn có thể bật chúng trong phần cài đặt connector trên claude.ai.
