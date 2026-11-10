# Intent: Lượng "nhập lại file sao lưu thất bại" tăng vọt trên production, ngày 19

Page: on-call. **Rollback không giúp gì ở đây, khuyên không chạy.** Production chưa đổi release trong cả khoảng theo dõi. Bản trước trong `deploy/production/history.jsonl` là `20b4e8f-20261104-102454-306665`, nhưng `app/` của nó giống hệt bản đang chạy (`git diff --stat 20b4e8f b51a55e -- app/` không ra gì). Nếu on-call vẫn muốn quay về bản đó thì chạy `python3 scripts/rollback.py production`. Chạy hay không là quyết định của một người.

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch production_error_rate level 3, simulated day 19 · Date: 2026-10-19
Triage: dismiss · wrong-diagnosis (Huy, ngày 22; ngày 21 xếp lịch điều tra, điều tra ra nhiễu quota, xem ops/triage.md)

## Problem
Ngày 19, nhiều người dùng (giả lập) sao lưu danh sách ra file rồi nhập lại chính file đó thì bị app từ chối: 5 lần, trong khi các ngày trước chỉ 0–2 lần. Lỗi "chưa lưu" (not_saved) vẫn ở mức bình thường. Đây là traffic giả lập, không có người dùng thật.

## Evidence
- Ngày 19 tỉ lệ lỗi là 0.0427 (9/211). Trung bình nền 0.0129, sd 0.0052, vượt mức mean + 3 sd (0.0285) [ops/metrics/production_error_rate.jsonl day 19]
- Ngày 19 tách theo loại: import_failed 5, not_saved 4, exception 0 [ops/metrics/production_error_rate.jsonl day 19]
- Ngày 1–18 có tổng cộng 8 import_failed, khoảng 0.44/ngày, chưa ngày nào quá 2. not_saved dao động 0–5/ngày [ops/metrics/production_error_rate.jsonl day 1–18]
- Cả 19 ngày chạy cùng một release `b51a55e-20261110-154535-364521`, detect báo `release_changes: []` [ops/metrics/production_error_rate.jsonl] [deploy/production/history.jsonl]
- Bản trước `20b4e8f` có app giống hệt bản đang chạy [git diff --stat 20b4e8f b51a55e -- app/]
- Staging ngày 19 vẫn bình thường: 0.0182, level 0 [ops/watch.jsonl line 56]
- Một import chỉ bị tính import_failed trong hai trường hợp: `parseBackup` từ chối file, hoặc `store.replace` không ghi được vì storage giả lập ném lỗi quota với xác suất 1% [scripts/traffic.js:95-101] [deploy/production/current/backup.js:130-134] [deploy/production/current/store.js:30-44]

## Diagnosis
- Không có thay đổi code hay release nào trong khoảng theo dõi, nên nguyên nhân không nằm ở một bản deploy.
- Giả thuyết 1 (nhiễu): `store.replace` gặp lỗi quota 1% của traffic.js:55. Mỗi ngày có khoảng 32 lần nhập, nên trung bình khoảng 0.3–0.44 lần lỗi/ngày. Theo Poisson, xác suất có từ 5 lần trở lên trong một ngày vào khoảng 1e-4, quá thấp để coi là nhiễu thông thường.
- Giả thuyết 2: dữ liệu trong `ops/state/production.json` khiến `parseBackup` từ chối, ví dụ id trùng (backup.js:100). Trường hợp này xảy ra khi cùng một simulated day chạy hai lần trên cùng state, vì id có dạng `user-day-i` (traffic.js:82). Chưa kiểm chứng được: tôi không chạy được script đọc state trong phiên này (cần duyệt) và không có file `.confirm` nào.
- **Confidence: low.** Muốn chắc hơn thì quét `ops/state/production.json` tìm id trùng hoặc todo sai. Nếu có thì giả thuyết 2 đúng. Một cách khác là chạy lại ngày 19 trên một bản sao của state rồi in message của từng import thất bại.
- Đã loại trừ: release mới (không có), lỗi code app (exception = 0, code giống bản trước), lỗi chung của môi trường (not_saved và staging đều bình thường).

## Desired outcome
Người dùng nhập lại được file sao lưu do chính app tạo ra, trừ khi lỗi đúng là do bộ nhớ trình duyệt đầy.

## Success criteria
- production_error_rate quay về dưới mean + 3 sd trong 3 ngày giả lập liền nhau.
- import_failed ≤ 2/ngày.
- Biết nguyên nhân của 5 lần import_failed ngày 19: quota hay parseBackup.

## Affected users and systems
Người dùng giả lập trên production, luồng sao lưu rồi nhập lại (`backup.importBackup`).

## Constraints
- Rollback production do một người quyết định [CLAUDE.md#Deploy].
- Watch run không được sửa ops/bands.yaml hay test [CLAUDE.md#Maintain].

## Out of scope
Sửa code, đổi bands, rollback.

## Impact
Low: chỉ có một ngày tăng, không có exception, và traffic là giả lập. Nếu giả thuyết 2 đúng thì lỗi nằm ở bộ sinh traffic chứ không ở app.

## Open questions
- Ngày 19 có bị chạy `collect.py traffic --env production` hai lần, hoặc có ai sửa `ops/state/production.json` không? (on-call)
- Có nên ghi lý do của mỗi lần import thất bại vào by_kind (quota hay parse) để lần sau tự phân biệt được không? (tech lead)
- Hook release-gate đang chặn cả lệnh chỉ đọc (`cat`) trong `deploy/production/`. Có đúng ý đồ không? (tech lead)

ACTIONS TAKEN: page_a_person: dòng "Page: on-call" ở đầu intent này. Không rollback, không deploy, không sửa file nào trong repo. Chỉ ghi một script đọc ở scratchpad, nhưng không chạy được vì cần duyệt.
