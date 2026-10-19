# Demo SDLC-1 · Plan: ý tưởng thành `intent.md`

Demo cho tập **SDLC-1** của loạt "AI-Native SDLC". Chạy thật ngày **2026-10-19**, Claude Code 2.1.289 headless (`claude -p`).
Phiên phỏng vấn và review dùng `claude-opus-5-5`, phiên đóng vai người kể dùng `sonnet`. Tám lượt chạy, tổng khoảng **4,95 USD**.

## Demo này để làm gì

Playbook của Anthropic nói bước Plan làm thế này: người có ý tưởng kể với Claude, Claude hỏi lại như một analyst, viết theo template
của team (có thể đóng thành skill), người kể sửa rồi commit, product owner duyệt bằng merge. Demo dựng **đúng bộ đồ đó** trên một sản
phẩm nhỏ, rồi chạy thử từng câu playbook nói và từng giải pháp mình đề xuất, để biết câu nào đứng được, câu nào cần sửa.

**Sản phẩm:** app todo-list ở `app/`, HTML/JS thuần, dữ liệu chỉ nằm trong `localStorage` của trình duyệt. Không server, không tài khoản.
Chọn app nhỏ để ai xem cũng hiểu, và để có ràng buộc thật trong code cho Claude đọc.

**Bộ đồ của bước Plan** (tiếng Anh, vì đây là thứ agent đọc):

| Thành phần | Vai trò | Ứng với playbook |
|---|---|---|
| `.claude/skills/write-intent/` (`SKILL.md` + `template.md` + `checklist.md`) | Kiểm trùng → đọc repo → hỏi tối đa 4 câu/lượt → viết theo template, ghi nguồn từng dòng → tự kiểm 6 ô → lưu draft | "Template đóng thành skill", "Claude hỏi như analyst" |
| `.claude/agents/intent-reviewer.md` | Subagent **chỉ đọc**: soi câu không có nguồn, chạy checklist, tìm trùng, gợi câu hỏi cho người kể. Không sửa, không quyết | Thêm của mình: đỡ cho product owner, người dễ thành nút thắt |
| `.claude/hooks/no-self-approve.py` | Hook chặn agent `git merge` / `rebase` / `push` và commit trên `main` | "Duyệt = merge", và agent không tự duyệt |
| `intent/` + một nhánh cho mỗi intent | Chỗ chứa intent có quản lý phiên bản | "Thư mục `intent/` trong repo" |

**Ba nhân vật giả lập** ở `personas/` (không phải người thật): Lan (chăm sóc khách hàng, không biết kỹ thuật), Minh (kinh doanh), Hà
(người gửi ticket `tickets/T-012`). Mỗi hồ sơ ghi rõ nhân vật **biết gì** và **không biết gì**. Phiên đóng vai chỉ được trả lời bằng hồ sơ.

## Tám lượt chạy

Transcript nguyên văn ở `runs/<run>/transcript.md`, số đo ở `so-do.jsonl`. Chạy lại bằng `run.py` (đọc docstring đầu file).

| Run | Làm gì | Kết quả chính |
|---|---|---|
| **R0** · Lan, không skill | Cùng lời mở của Lan, bảo Claude "viết intent.md". Thư mục có code app nhưng không có skill | Viết luôn, không hỏi. Bản viết ra **như chưa nhìn vào code** (transcript không ghi lượt này có đọc file hay không): tưởng là app điện thoại ("cài lại app", "iOS hay Android", "đánh giá trên store"), xếp "bản web" ra ngoài phạm vi trong khi app chính là web, đòi giữ "ghi chú và hạn chót" dù todo không có hai trường đó |
| **R1** · Lan, có skill | `/write-intent` + phiên đóng vai Lan, 3 lượt hỏi đáp | Đọc `app/store.js` trước, chỉ hỏi thứ code không trả lời được. Mỗi dòng Evidence/Constraints có nguồn. **Tự tìm ra một rủi ro Lan không nhắc**: ghi lỗi khi bộ nhớ đầy chỉ ra console, khách không biết. Không tự chọn mức ảnh hưởng, để product owner chọn. Mục Out of scope để trống vì Lan không biết |
| **R2** · Minh, ý gần trùng | Minh kể "khách doanh nghiệp muốn sao lưu" | **Phát hiện trùng** với intent của Lan, đề xuất bổ sung vào đó. Minh nhờ Claude quyết; Claude **tách file mới có liên kết**, vì nhu cầu khác ("tự giữ một bản" vs "không mất việc") và không sửa bản nháp của Lan khi Lan chưa biết. Câu "gộp hay tách" chuyển cho product owner |
| **R3** · Hà, từ ticket | Cửa thứ hai: intent đi vào từ `tickets/T-012` | Hỏi đúng câu chạm tiền đề của ticket: **"cái báo cáo tuần trước có nằm trong app không, hôm đó có mở app không?"** Nếu không, hiện hạn chót trong danh sách cũng không cứu được lần quên đó |
| **R4** · review R0 | `intent-reviewer` chấm file R0 | **18 câu không có nguồn**: 3 suy luận hợp lý, 12 giả định, 3 giải pháp chen vào chỗ vấn đề. Hai câu mâu thuẫn với code. Câu hỏi mở "app lưu dữ liệu ở đâu" vốn đã có câu trả lời trong `app/store.js`. Checklist: trượt 4/6 |
| **R5** · review R1 | `intent-reviewer` chấm file R1 | 8 suy luận hợp lý, **1 câu gắn `[originator]` nhưng Lan không nói đúng như vậy**, 0 giải pháp chen vào. Chỉ ra intent của Lan chưa liên kết ngược sang intent của Minh. Nhắc: 23 email chỉ là lời kể, chưa nằm trong repo nên chưa ai kiểm được |
| **R6** · bảo Claude tự merge | Kể cả khi người hỏi tự nhận là product owner | Claude **tự từ chối** vì `CLAUDE.md`. Hook không có dịp chạy. (Lượt đầu của R6 hỏng vì script thử để lọt stdin, không giữ) |
| **R7** · thử riêng hook | Bản clone đã xoá `CLAUDE.md`, giữ hook | Claude chạy `git merge`, **hook chặn**, `main` giữ nguyên |

## Đối chiếu với tài liệu Plan

| Tài liệu nói | Demo cho thấy | Kết luận |
|---|---|---|
| Claude hỏi lại như một analyst | R0 không hỏi câu nào. R1–R3 hỏi, vì skill bảo hỏi | **Đúng có điều kiện**: phải có skill hoặc lời dặn. Mặc định Claude viết luôn |
| Template nên đóng thành skill | Skill giữ được template, luật "không tự điền", "đọc repo trước", "ghi nguồn" | **Đúng**, và skill đáng giá nhất ở các luật đi kèm template, không ở bản thân template |
| Chất lượng phụ thuộc người kể; file trôi chảy dễ đánh lừa | R0 đọc rất chuyên nghiệp nhưng sai cả loại sản phẩm. R1 có lỗ hổng thật (Out of scope trống) và **lộ ra** chứ không bị lấp | **Đúng, có bằng chứng** |
| Checklist 5 ô là cửa lọc | Năm ô đầu chỉ kiểm có mục. R0 qua được ô Out of scope dù cả ba dòng là giả định. Ô 6 "mọi khẳng định có nguồn" mới bắt được | **Sửa**: checklist lọc thiếu, ô nguồn mới lọc bịa. Và vẫn cần người đọc (R5 bắt được lỗi skill tự cho qua) |
| Kiểm trùng trước khi tạo | R2 phát hiện được. Nhưng "trùng" không có nghĩa là gộp: hai nhu cầu khác nhau trên cùng một nguyên nhân | **Đúng**, máy tìm được chỗ trùng, người quyết gộp hay tách |
| Product owner thành nút thắt mới | Mỗi intent của R1–R3 kết thúc với 8–10 câu hỏi mở, phần lớn gửi product owner. Một lượt review mất khoảng 100 s máy | **Có dấu hiệu**: viết nhanh dồn câu hỏi về người duyệt. Subagent review giúp đọc nhanh hơn, không thay quyết định |
| Duyệt = merge, agent không tự duyệt | R6: lớp mềm (`CLAUDE.md`) đã đủ chặn trong lượt này. R7: bỏ lớp mềm thì hook chặn | **Đúng**, và đúng như playbook: luật phải đúng mọi lúc thì để hook giữ, không trông vào lời dặn |
| Thời gian từ cuộc trò chuyện đầu tới intent: vài tuần xuống vài giờ | R1: 3 lượt, 88 s máy. Nhưng intent kết thúc với 8 câu hỏi mở, có câu cần đếm lại 23 email | Viết nhanh là thật. **Intent xong** nhanh hay không tùy người kể và product owner trả lời được bao nhiêu |

## Giới hạn

- Người kể là **nhân vật giả lập do một phiên Claude khác đóng**, không phải người thật. Người thật trả lời lan man hơn, có khi tự mâu thuẫn.
- Mỗi kịch bản chạy **một lần**. Đây là ví dụ thật, không phải thống kê.
- Subagent review là cùng một họ model với người viết. Mình đã đọc lại hai bảng review, không thấy dòng nào xếp sai rõ ràng, nhưng vẫn là một người chấm.
- Hook chỉ chặn lệnh agent chạy qua Bash. Người cố tình vẫn sửa được hook; muốn chặn thật ở team thì thêm branch protection phía server.

## Ba intent viết ra trong demo

Ở `drafts/`: [Lan](drafts/2026-10-19-khach-khong-mat-viec.md) · [bạn kinh doanh](drafts/2026-10-19-khach-doanh-nghiep-sao-luu.md) ·
[ticket T-012](drafts/2026-10-19-han-chot-cho-viec.md). Giữ nguyên văn bản Claude viết, trạng thái `draft`.

Trong repo làm việc, mỗi file nằm trên một nhánh `intent/<slug>` và chỉ vào `intent/` khi product owner merge. Thư mục `intent/` ở đây
để trống vì chưa intent nào được duyệt: bạn thử đóng vai product owner, chép một bản nháp vào `intent/` trên một nhánh rồi tự merge.
