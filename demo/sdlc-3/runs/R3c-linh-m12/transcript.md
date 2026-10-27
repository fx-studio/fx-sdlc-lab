# R3c-linh-m12

Chạy 2026-10-27 11:10 ở `persona-empty` (thư mục riêng của lượt này), chế độ quyền `default`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Bạn là Linh, người duyệt chữ trên app. Hai việc, trả lời ngắn, đánh số.

1) Câu M12 (dòng chữ "danh sách được giữ ở đâu"). Bạn đã thay thành: "Danh sách chỉ được lưu trên trình duyệt này. Đổi trình duyệt hoặc đổi máy là mất danh sách, trừ khi bạn đã sao lưu ra file." và nói nếu Khoa hoặc Mai muốn giữ ý "xoá dữ liệu" thì đề xuất cách nói khác.
Mai trả lời: phải giữ, vì P4 (khách được biết dữ liệu ở đâu và khi nào mất) và tiêu chí 23 của spec đã accepted đòi có ý đó. Mai đề xuất: "Danh sách chỉ được lưu trên trình duyệt này, nên xoá dữ liệu trình duyệt, đổi trình duyệt hoặc đổi máy là mất, trừ khi bạn đã sao lưu ra file." Mai gợi ý thêm "xoá lịch sử duyệt web" nếu bạn thấy "xoá dữ liệu trình duyệt" vẫn nặng. Linh quyết chữ cuối.
Ghi chú kỹ thuật của người chạy demo (không phải của Khoa hay Mai): trên đa số trình duyệt, chỉ xoá "lịch sử duyệt web" thì KHÔNG mất danh sách; phải xoá "cookie và dữ liệu trang web" mới mất.
→ Chốt đúng một câu M12.

2) Khoa review code, ghi: câu "Thay đổi vừa rồi chưa được lưu. Hãy sao lưu ra file, rồi xoá bớt việc đã xong." cũng hiện khi NHẬP file bị lỗi lúc lưu (bộ nhớ đầy), và lúc đó "thay đổi vừa rồi" hơi mơ hồ. Spec đã accepted ghi: nhập mà lưu lỗi thì "app báo như F3" (dùng chung câu với lỗi lưu thường).
→ Giữ chung một câu như spec, hay cần câu riêng cho lúc nhập? Nếu cần câu riêng thì đó là sửa spec đã accepted: nói rõ là việc của lần sau hay phải làm ngay.
Biết thêm: verifier đã chạy test, khi nhập mà lưu lỗi thì danh sách cũ còn nguyên, không mất, không lẫn.

## Tool call (0)

(không có)

## Claude · 16 s

1) **Chốt M12:**
"Danh sách chỉ được lưu trên trình duyệt này, nên xoá dữ liệu trang web, đổi trình duyệt hoặc đổi máy là mất, trừ khi bạn đã sao lưu ra file."
- Mình giữ ý xoá dữ liệu như Mai cần cho P4 và tiêu chí 23.
- Mình không dùng "xoá lịch sử duyệt web". Theo ghi chú kỹ thuật thì câu đó sai, vì xoá lịch sử không làm mất danh sách. Khách đọc xong sẽ tưởng mình xoá lịch sử là mất, hoặc xoá xong thì tưởng đã an toàn.
- Mình không dùng "cookie" vì là từ kỹ thuật. "Dữ liệu trang web" gần với tên mục khách sẽ thấy khi xoá trong trình duyệt.
- Nhờ Mai xác nhận lại câu này vẫn đạt P4 và tiêu chí 23.

2) **Giữ chung một câu như spec, chưa làm câu riêng cho lúc nhập.**
- Danh sách cũ còn nguyên, nên khách không mất gì. Lời khuyên "sao lưu ra file, xoá bớt việc đã xong" vẫn đúng. "Thay đổi vừa rồi" hơi mơ hồ nhưng không gây hại.
- Câu riêng là sửa spec đã accepted, nên cần Khoa, Mai và Thảo đồng ý. Mình chỉ có quyền quyết chữ, không có quyền đổi spec.
- **Việc của lần sau**, không chặn bản này. Mình đề xuất câu riêng: "Chưa nhập được file. Danh sách cũ của bạn vẫn nguyên. Hãy xoá bớt việc đã xong rồi thử lại."
- Câu đề xuất dựa trên kết quả verifier đã test là danh sách cũ còn nguyên. Hãy ghi kết quả đó vào phần ghi chú của spec, để lần sau không phải kiểm lại.
