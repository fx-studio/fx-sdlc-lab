# R3-ha-ticket

Chạy 2026-10-19 06:36. Nguyên văn, không sửa.

## Người kể (lời mở)

/write-intent Viết intent từ ticket tickets/T-012-due-dates.md. Người gửi ticket là Hà, đang ở đây để trả lời.

## Claude (lượt 1) · 25 s

Trước khi hỏi, mình kiểm tra trùng lặp và đọc repo.

**Kiểm tra trùng:** Không trùng. Hai intent đang có (`khach-khong-mat-viec.md` của Lan, `khach-doanh-nghiep-sao-luu.md` của Minh) đều nói về chuyện mất danh sách việc. Cả hai chỉ nhắc T-012 trong phần câu hỏi mở, như một thứ có thể nằm ngoài phạm vi. Vì vậy mình tạo intent mới.

**Những gì repo đã cho biết:**
- Ticket T-012 do Hà gửi qua form góp ý ngày 12/10/2026, có 14 lượt +1. Nội dung: muốn đặt hạn chót cho từng việc, được nhắc khi gần tới hạn, vì hay quên những việc có deadline. [tickets/T-012-due-dates.md]
- Hiện một việc chỉ có id, tiêu đề, trạng thái xong và thời điểm tạo. Chưa có hạn chót. [app/app.js]
- Dữ liệu chỉ nằm trong trình duyệt đang dùng. App không có server, không có tài khoản. [app/store.js]

**Mình hỏi Hà 4 câu trước:**

1. **Nhắc như thế nào thì đủ?** Hà chỉ cần thấy rõ việc nào sắp tới hạn khi mở app ra? Hay cần được nhắc cả lúc **không mở app**, ví dụ khi đang làm việc khác?
2. **"Gần tới hạn" là trước bao lâu?** Ví dụ trước 1 ngày, trước vài giờ, hay Hà muốn tự chọn? Còn hạn chót thì chỉ cần ngày, hay cần cả giờ?
3. **Lần gần nhất Hà quên một việc có deadline là chuyện gì, và hậu quả ra sao?** Mỗi tuần Hà có khoảng bao nhiêu việc có deadline trong app?
4. **Làm sao để Hà biết là đã ổn?** Ví dụ: "một tháng không trễ việc nào", hay "sáng mở app là thấy ngay việc nào tới hạn hôm nay".

Hà trả lời được câu nào thì trả lời câu đó. Câu nào không biết thì cứ nói "không biết", mình sẽ để vào phần câu hỏi mở chứ không tự điền.

## Người kể (lượt 1) · 7 s

Mình trả lời được mấy câu thôi nha.

- Câu 1: Mình dùng app trên laptop ở chỗ làm, mỗi ngày. Mình muốn thấy hạn chót ngay trong danh sách và xếp việc theo hạn chót. Còn nhắc bằng cách nào thì mình không biết, mình chỉ muốn "đừng để quên".
- Câu 2: Mình không biết. Trước bao lâu, chỉ cần ngày hay cần cả giờ, mình chưa nghĩ tới.
- Câu 3: Tuần trước mình quên nộp một báo cáo vì không nhớ hạn. Hậu quả cụ thể và mỗi tuần có bao nhiêu việc có deadline thì mình không biết.
- Câu 4: Mình không có con số nào. Mình chỉ muốn nhìn danh sách là biết việc nào tới hạn trước.

## Claude (lượt 2) · 13 s

Cảm ơn Hà, vậy là đủ rõ phần chính. Còn thiếu **phạm vi** (cái gì không cần làm), và mình muốn hiểu kỹ hơn chuyện cái báo cáo tuần trước. Mình hỏi thêm 3 câu ngắn:

1. **Cái báo cáo tuần trước có nằm trong danh sách việc của app không?** Nếu hôm đó mở app ra mà thấy ngay việc đó đứng đầu danh sách kèm hạn chót, Hà có kịp nhớ ra không? Hay vì hôm đó Hà không mở app nên mới quên?
2. **Có thứ gì Hà chắc chắn không cần không?** Ví dụ: nhắc trên điện thoại (Hà đang dùng laptop), việc lặp lại hằng tuần, chia sẻ hạn chót cho đồng nghiệp. Hà chỉ cần nói "không cần" hay "không biết" cho từng cái.
3. Khi xếp theo hạn chót, **những việc không có hạn chót** nên nằm ở đâu? Nếu Hà chưa nghĩ tới thì cứ nói "không biết".

Nếu Hà muốn mình viết luôn thì nói "viết đi". Những gì chưa rõ mình sẽ để vào phần câu hỏi mở.

## Người kể (lượt 2) · 6 s

Mình trả lời như vầy nha.

- Câu 1: Mình chỉ nhớ là tuần trước mình quên nộp một báo cáo vì không nhớ hạn. Việc đó có nằm trong app không, hay hôm đó mình có mở app không, mình không biết.
- Câu 2: Mấy cái đó (nhắc trên điện thoại, việc lặp lại hằng tuần, chia sẻ hạn chót cho đồng nghiệp) mình đều không biết. Mình chưa nghĩ tới. Mình cũng không biết người khác cần gì.
- Câu 3: Việc không có hạn chót nên nằm ở đâu thì mình không biết.

Viết đi.

## Claude (lượt 3) · 43 s

Mình đã viết bản nháp vào **`intent/2026-10-19-han-chot-cho-viec.md`**, trạng thái `Status: draft`. Chưa commit, chưa merge. Phần đó để product owner làm.

**Kết quả checklist:**

| Mục | Kết quả |
|---|---|
| **Problem**: nói rõ ai bị ảnh hưởng, khi nào | ✅ Hà, dùng laptop ở chỗ làm mỗi ngày, hay quên việc có deadline |
| **Evidence**: có ít nhất một bằng chứng cụ thể | ✅ Ticket T-012, 14 lượt +1, một lần Hà quên nộp báo cáo |
| **Out of scope**: có và không để trống | ❌ **Đang trống.** Hà không biết nên bỏ những gì, nên mình không tự điền. Ba mục (nhắc trên điện thoại, việc lặp lại hằng tuần, chia sẻ hạn chót cho đồng nghiệp) đã chuyển sang câu hỏi mở cho product owner |
| **Success criteria**: kiểm được | ✅ Dựa trên hành vi Hà mô tả: nhìn danh sách là thấy hạn chót, và biết việc nào tới hạn trước. Chưa có con số, mục này đã ghi vào câu hỏi mở |
| **Open questions**: có mục riêng, mỗi câu ghi ai trả lời | ✅ Có 10 câu |
| **Sourced**: mỗi dòng ở Evidence và Constraints đều có nguồn, và nguồn đó nói đúng như vậy | ✅ Mình đã đối chiếu lại với ticket, `app/app.js`, `app/store.js` và câu trả lời của Hà |

**Bản nháp ghi như sau, Hà xem có đúng ý không:**
- Ý "hiện hạn chót trong danh sách và xếp theo hạn chót" được ghi là **gợi ý của Hà**, chưa phải quyết định.
- Cách nhắc, nhắc trước bao lâu, hạn chót chỉ cần ngày hay cần cả giờ: Hà đều nói không biết, nên mình để product owner quyết.
- Có một câu chỉ Hà trả lời được: **cái báo cáo tuần trước có nằm trong app không**. Hà có thể mở app trên laptop để xem. Câu này quan trọng vì nó cho biết hiện hạn chót trong danh sách có giúp được lần quên đó hay không.

Có chỗ nào mình hiểu sai thì Hà sửa giúp mình. Mình dừng ở đây.

---

File mới: 2026-10-19-han-chot-cho-viec.md
