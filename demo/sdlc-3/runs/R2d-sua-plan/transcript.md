# R2d-sua-plan

Chạy 2026-10-27 09:40 ở gốc repo, chế độ quyền `acceptEdits`, tiếp session trước. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

The tech lead (Khoa, simulated) read only the plan, without our conversation. His review is below. Product owner Thảo and UX owner Linh answered Q4: block it; the message is exactly "File này không có việc nào, nên chưa nhập được."
Revise the plan to fix every gap Khoa lists and to record every answer (Q1–Q6) with who gave it. Then write the plan to plan/2026-10-19-khach-khong-mat-viec.md with Status: draft on line 3, in the four-section shape from CLAUDE.md (Files that change · Order of work · Risks · Proof) plus any extra sections you need. Do not touch app/ or tests/ yet; a person accepts the plan first.

--- Khoa's review ---

# Khoa duyệt plan: sao lưu, nhập lại, báo lỗi lưu

## 1) Engineer khác làm theo được không?

**Được, với vài chỗ cần sửa.** Phần hay nhất là luật "không ghi khi đọc lỗi" nằm ở `store`, `importBackup` chỉ gọi `replace`, và test được bằng Node. Chỗ còn thiếu hoặc mơ hồ:

1. **Order of work tự mâu thuẫn.** Bước 1 ghi "chưa đụng app.js", rồi lại bảo gộp vào commit của bước 4. Hãy viết lại thành các commit cụ thể:
   - Commit A: `backup.js` + test. Chưa ai gọi nên an toàn.
   - Commit B: `store.js` + `app.js` + html/css + test. Đổi kiểu trả về của `load` và nối app phải đi cùng nhau.
   - Mỗi commit kèm thay đổi trong `plan/` theo pre-commit.
2. **Câu chữ nằm ngoài plan.** `MESSAGES` (C2, A8, F5 bước 4, F1.5) chỉ trỏ về spec. Chấp nhận được nếu engineer có spec, nhưng plan cần ghi rõ mục nào trong spec. Các mã A/F/C/U/AC cũng nên có một dòng chú dẫn.
3. **Chưa có xử lý khi `file.text()` bị lỗi** (file đọc không được, bị thu hồi quyền). Cần một câu báo và phải trả lại `current`.
4. **Chưa nói về `URL.revokeObjectURL`** sau khi tải. Cần gọi, kẻo rò bộ nhớ.
5. **`static.test.js` chỉ cấm `localStorage` trong `app.js`.** Cấm luôn trong `backup.js`, vì `backup.js` cũng không được tự ghi.
6. **Chưa nói app có `store.load/save` gọi ở chỗ nào khác ngoài `app.js` không.** Cần grep xác nhận trước khi đổi kiểu trả về.
7. **Chưa có rollback.** Nên ghi: khoá `todo.v1` và dạng dữ liệu không đổi, nên revert commit là an toàn.
8. **Kiểm tay không ghi rõ ai chạy, trình duyệt nào, ghi kết quả ở đâu** (xem Q6).

## 2) Trả lời Questions

- **Q1. Large.** Plan đổi hợp đồng của tầng lưu (`load`/`save`/`replace`), thêm module mới, chạm cả 5 file trong `app/` và dựng bộ test đầu tiên. Spec lại ghi `Risk: high`. Tôi duyệt, kèm điều kiện ở mục 3.
- **Q2. Có.** Thêm `app/backup.js` là đúng, vì không DOM thì Node test được. Giữ script thường (không ES module, không build), thứ tự `store` → `backup` → `app` như plan.
- **Q3. 1 MB = 1.048.576 byte** (1 MiB), dùng một hằng `MAX_IMPORT_BYTES` cho cả hai chỗ kiểm (`file.size` và `TextEncoder`). Test biên ở đúng 1.048.576 và 1.048.577. Nếu có câu chữ hiển thị "1 MB" thì để nguyên.
- **Q4. Từ chối `todos: []` thì tôi đồng ý về kỹ thuật**, vì app không tạo ra file rỗng (nó chặn sao lưu khi rỗng). Nhưng đây là hành vi sản phẩm và câu chữ: **chuyển product owner chốt** có chặn hay không, **Linh** chốt câu báo. Câu báo phải nói rõ "file không có việc nào", không phải "file sai".
- **Q5. Đọc lỗi**, theo A13. Ghi đè mà không báo là mất dữ liệu, còn báo nhầm trong trường hợp này gần như không xảy ra, vì app không bao giờ ghi `"null"`.
- **Q6. Chấp nhận kiểm tay, có điều kiện.** Checklist phải nằm trong `plan/`, ghi người chạy, ngày, trình duyệt, đạt hay không. Tối thiểu là **Safari iOS máy thật**, Chrome Android và một trình duyệt desktop. Riêng tải file và chọn file thì chạy cả ba, vì khách dùng điện thoại.
- **Riêng tư và pháp lý: chuyển Mai** nếu cần câu cảnh báo kiểu "file này chứa việc của bạn". Plan hiện không đụng đến.

## 3) Hạng và duyệt

**Hạng Lớn. Tôi duyệt plan với các điều kiện:**

1. Sửa mục 1–7 ở trên trước khi chuyển `Status: accepted`.
2. Q3 chốt như trên. Q4 chờ PO và Linh, mặc định từ chối. Q5 chốt như trên.
3. **Thử bằng dữ liệu thật từ bản cũ trước mọi AC khác.** Mở bản mới với `todo.v1` do bản hiện tại ghi, và thử cả trường hợp 2.000 việc, rồi thêm, đánh dấu, xoá. Đây là bước rủi ro nhất, đúng như plan nêu.
4. Review diff của commit B bởi một người khác, vì đó là chỗ có thể làm hỏng luồng của mọi khách.
5. Không nâng giới hạn 1 MB. Nếu thấy khách vượt, câu C2 báo trước như đã thống nhất.

Chưa có điều kiện nào ngoài danh sách này. Sửa xong thì chuyển `Status: accepted` và bắt đầu code.

## Tool call (10)

1. Grep · pattern=store\.(load|save)|localStorage|todo\.v1
2. Bash · command=grep -rlE "store\.(load|save)|localStorage" --include=*.js --include=*.html --include=*.py --include=*.sh . | grep -v '^./.git/'; git status --short
3. Bash · command=head -4 spec/2026-10-19-han-chot-cho-viec.md intent/2026-10-19-khach-doanh-nghiep-sao-luu.md; ls demo/sdlc-3/runs/R2c-thao-q4 demo/sdlc-3/runs/R2c-linh-q4
4. Bash · command=grep -h -o ".\{0,120\}không có việc nào, nên chưa nhập được.\{0,40\}" demo/sdlc-3/runs/R2c-*/transcript.md | head; grep -h -i -o ".\{0,80\}chặn.\{0,80\}" demo/sdlc-3/runs/R2c-thao-q4/transcript.md | head -5
5. Grep · pattern=không có việc nào, nên chưa nhập được|[Cc]hặn|[Tt]ừ chối
6. Write · file_path=<repo>/plan/2026-10-19-khach-khong-mat-viec.md
7. Read · file_path=<repo>/.claude/hooks/no-self-approve.py
8. Bash · command=git status --short plan/ && ls plan/
9. Write · file_path=<repo>/plan/2026-10-19-khach-khong-mat-viec.md
10. Bash · command=sed -n 3p plan/2026-10-19-khach-khong-mat-viec.md | cut -c1-40; grep -c "" plan/2026-10-19-khach-khong-mat-viec.md; git status --short

## Claude · 294 s

I wrote the plan to `plan/2026-10-19-khach-khong-mat-viec.md`, with `Status: draft` on line 3. `app/` and `tests/` are untouched, and nothing is committed.

**Khoa's seven gaps, now in the plan:**
1. **Order of work** is two commits. Commit A is `backup.js` and its test; nothing loads it yet. Commit B is the storage change, the app, the HTML/CSS and the remaining tests, and a second person reviews it. Each commit includes the plan update that pre-commit requires.
2. **Wording:** a new "Câu chữ" table lists messages M1–M16, each tagged with its spec section and source or marked "đề xuất" (proposed). A legend explains the F/A/C/AC/P/S/U/Q/M/T codes.
3. **Unreadable file:** if `file.text()` fails, the app shows M14 and keeps the current list. This is inside `importBackup`, so a test covers it.
4. **`URL.revokeObjectURL`** runs 10 seconds after the download starts. Revoking right after the click can break the download on Safari iOS; the checklist tests that on the phone.
5. **`static.test.js`** now forbids `localStorage` in both `app.js` and `backup.js`.
6. **Grep:** I ran it today. The only code that calls `store` is `app/app.js:2` and `app/app.js:24`; the only code using browser storage is `app/store.js`. Commit B repeats the grep as its first step.
7. **Rollback:** the storage key and data shape don't change, so reverting B is safe for data. Revert B before A.

**Answers recorded, with who gave them:**
- **Q1–Q3, Q5, Q6:** from Khoa's review, `demo/sdlc-3/runs/R2b-tech-lead-doc-plan`.
- **Q4:** block it. Thảo decided and Linh gave the message (`R2c-thao-q4`, `R2c-linh-q4`). I checked both transcripts; the message matches exactly.
- **Mai:** the note on routing a privacy warning to Mai is in the plan too.

His other conditions are in as well: T0 tests the new version on data saved by the current one, including 2,000 tasks, before any other check. The manual checklist has blanks for who ran it, the date, each browser and pass/fail, across all three browsers.

**Three things I added that Khoa didn't ask for:**
- **Q7 is open, for Linh.** Most messages have no exact wording in the spec, for example "Đã sao lưu N việc." and the rejection messages. The plan uses my drafts, and changing them only touches `MESSAGES` in `backup.js`. You decide whether Q7 must close before the plan is accepted.
- **Phone testing needs HTTPS.** The current Add button already fails if a phone opens `http://<LAN IP>:8000`: it uses `crypto.randomUUID`, which only works on secure pages. The tester needs an HTTPS address.
- **The deadline spec will collide with this one.** `spec/2026-10-19-han-chot-cho-viec.md` (still draft) adds `dueDate`. A version 1 backup would drop that field, and import would reject files that have it. That spec will need to raise the backup `version`.

**One hiccup:** my first write was blocked by the `no-self-approve` hook. The plan's text named the approval status in the sentence telling a person to change it, and the hook matches that phrase anywhere in `plan/`. I reworded it to "change `draft` on line 3 to `accepted`".

Once the plan is accepted, the hook won't let me edit it, so a person fills in the "Tiến độ" (progress) section and the manual checklist at each commit.
