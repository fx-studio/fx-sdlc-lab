# Intent: Test "a list with random titles survives backup and import" lúc đỗ lúc trượt từ ngày 31, do bộ sinh tiêu đề tạo ra tiêu đề rỗng

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch ci_fail_rate level 2, simulated day 32 · Date: 2026-11-01

## Problem
Từ ngày 31, CI hỏng 2/4 lần (ngày 31) rồi 1/4 lần (ngày 32), cả hai ngày trên cùng commit `3afe66d`. Lần nào cũng chỉ trượt một test: `a list with random titles survives backup and import`. Code app không đổi. Test này đã được merge vào `main` ở commit `3afe66d` ("Merge branch 'test/random-titles'", chỉ thêm 18 dòng vào `tests/backup.test.js`). Test sinh dữ liệu ngẫu nhiên, đôi khi sinh ra tiêu đề rỗng `""`, mà app thì từ chối tiêu đề rỗng ngay từ thiết kế. Vì vậy đây là một test flaky, không phải lỗi sản phẩm.

## Evidence
- Ngày 23–30: 0/4 lần hỏng mỗi ngày, trên commit `a5351c7`. Ngày 31: 2/4, ngày 32: 1/4, đều trên commit `3afe66d`. detect báo `release_changes` ngày 31: `a5351c7 → 3afe66d` [ops/metrics/ci_fail_rate.jsonl day 23–32]
- `3afe66d` chỉ đổi `tests/backup.test.js` (+18 dòng). Commit cha `68e47dd` chỉ đổi `.claude/skills/diagnose/SKILL.md`. `app/` không đổi [git show --stat 3afe66d 68e47dd]
- Cả 3 log có lần trượt đều trượt ở `backup.test.js:293`, tức `assert.equal(parsed.ok, true)`. Danh sách tiêu đề lần nào cũng có một chuỗi rỗng: `["unbhyr","kvuáqiyqà","","ooãqãâk","rtạ"]`, `["ơê","","dăảđsnrlả","da","inôôcpeđc"]`, `["ă","lvtacdeư","","smãoc","ntư"]` [ops/ci/ci-day031-run2.log:199] [ops/ci/ci-day031-run4.log:199] [ops/ci/ci-day032-run2.log:199]
- `randomTitle()` lấy độ dài bằng `Math.floor(Math.random() * 12)`, tức từ 0 đến 11, nên có thể ra 0 ký tự [tests/backup.test.js:283]
- `parseBackup` chỉ nhận tiêu đề có `t.title.trim() !== ''` [app/backup.js:66]. Có test riêng khẳng định tiêu đề rỗng và tiêu đề toàn khoảng trắng phải bị từ chối [tests/backup.test.js:94-95]
- Trong app, người dùng không tạo được tiêu đề rỗng: `add` chỉ được gọi khi `input.value.trim()` khác rỗng, và tiêu đề được lưu sau khi `trim()` [app/app.js:9,73]

## Diagnosis
- **Nguyên nhân: test sai, không phải app sai.** Bộ sinh ngẫu nhiên sinh ra một input mà spec bắt app phải từ chối (tiêu đề rỗng), rồi lại khẳng định backup đó phải nhập lại được. Mỗi tiêu đề có xác suất rỗng là 1/12, nên xác suất có ít nhất một tiêu đề rỗng trong 5 tiêu đề là 1 − (11/12)^5 ≈ **35%**. Số đo thực tế là 3/8 lần chạy hỏng (37,5%), khớp với con số này.
- Bình luận ở dòng 279 ("Whatever a person can type as a title") không đúng với bộ sinh: người dùng không gõ được tiêu đề rỗng.
- Còn một lỗ nhỏ chưa xảy ra: bảng chữ cái không có khoảng trắng, nên hiện tại không sinh được tiêu đề toàn khoảng trắng. Nếu sau này ai đó thêm dấu cách vào bảng chữ cái thì sẽ có thêm một nguồn flaky nữa (tiêu đề đầu/cuối có khoảng trắng vẫn qua `parseBackup`, vì nó không trim khi parse).
- **Confidence: high.** Cả 3 lần trượt đều có `""`, tỉ lệ hỏng khớp với phép tính, và không có thay đổi nào khác trong app. Cách kiểm chứng: chạy test với một danh sách cố định có đúng một tiêu đề `""` thì sẽ trượt ở dòng 293. Thay `""` bằng `"a"` thì test qua.
- Đã loại trừ: thay đổi code app (không có), lỗi dấu tiếng Việt hay Unicode (các lần trượt có chữ có dấu, nhưng lần nào cũng có `""`, và các lần qua cũng dùng cùng bảng chữ cái), môi trường CI (các test khác vẫn ổn định).

## Desired outcome
CI chỉ đỏ khi app thật sự hỏng. Test ngẫu nhiên chỉ sinh ra những tiêu đề mà người dùng có thể tạo được, và khi trượt thì in ra đủ thông tin để chạy lại đúng trường hợp đó.

## Success criteria
- `bash scripts/flaky.sh 10` (hoặc chạy nhiều hơn) cho 0 lần trượt test này.
- ci_fail_rate về 0 trong 3 ngày giả lập liền nhau.
- Test vẫn giữ mục đích ban đầu: tiêu đề hợp lệ bất kỳ, kể cả có dấu tiếng Việt, đi qua backup rồi import thì giữ nguyên.

## Affected users and systems
Chỉ ảnh hưởng CI và test suite (`tests/backup.test.js`). App, staging và production không bị ảnh hưởng: không có dòng code app nào đổi, và hành vi từ chối tiêu đề rỗng là hành vi đúng.

## Constraints
- Theo CLAUDE.md#Verification, khi tin rằng test sai thì phải dừng lại và nói rõ lý do. Agent không tự sửa test. Một người quyết định sửa test hay đưa test vào danh sách quarantine.
- Lần chạy watch này ở mức 2, chỉ được đọc. Tôi không sửa file nào.

## Out of scope
Sửa `app/backup.js` để nhận tiêu đề rỗng (điều này sẽ trái với tests/backup.test.js:94-95 và với app.js), đổi bands, rollback.

## Impact
Low cho người dùng: không có lỗi sản phẩm. Medium cho đội: cứ khoảng 1 trong 3 lần chạy CI sẽ đỏ giả, làm người ta quen với việc bỏ qua CI đỏ.

## Open questions
- Sửa bộ sinh thế nào: độ dài từ 1 đến 12 (`1 + Math.floor(Math.random() * 12)`), hay chủ động thêm cả trường hợp có khoảng trắng ở đầu và cuối để test luôn xem `parseBackup` có giữ nguyên chúng không? (tech lead)
- Có nên dùng seed cố định hoặc in seed khi trượt, để chạy lại được đúng trường hợp đó không? (tech lead)
- Nhánh `test/random-titles` được merge thẳng vào `main`, không qua PR `pr/<n>`, nên không có review hay `scripts/check.sh` chạy nhiều lần trước khi merge. Có cần quy định test ngẫu nhiên phải qua `flaky.sh` trước khi merge không? (product owner hoặc tech lead)
- CLAUDE.md ghi "Flaky tests: none (2026-10-29)". Dòng này cần được một người cập nhật cho đến khi test được sửa. (on-call)

ACTIONS TAKEN: none. Đây là level 2, chỉ chẩn đoán: tôi chỉ đọc git, các log trong `ops/ci/`, `tests/backup.test.js`, `app/backup.js` và `app/app.js`, không sửa, không commit, không rollback file nào. Rollback không áp dụng, vì release ngày 31 chỉ đổi test, không đổi app.
