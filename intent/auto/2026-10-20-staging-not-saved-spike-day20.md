# Intent: Trên staging, số lần "chưa lưu được" tăng lên ngày 20, không có release mới

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch staging_error_rate level 3, simulated day 20 · Date: 2026-10-20
Triage: dismiss · false-alarm (Huy, ngày 21)

## Problem
Ngày 20, người dùng giả lập trên staging gặp thông báo "chưa lưu" 6 lần khi thêm, đánh dấu hoặc xoá việc. Các ngày trước chỉ có 0–2 lần, riêng ngày 19 có 4 lần. Nhập lại file sao lưu chỉ lỗi 1 lần, app không ném exception nào. Đây là traffic giả lập, không có người dùng thật.

## Evidence
- Ngày 20 có 7 lần lỗi trên 199 thao tác, tỉ lệ 0.0352. Ngưỡng là mean + 3 sd = 0.0265 (mean 0.0099, sd 0.00555, 14 điểm nền) [detect.py output day 20]
- Tách theo loại ngày 20: not_saved 6, import_failed 1, exception 0. Ngày 19: not_saved 4, tỉ lệ 0.0182 [ops/metrics/staging_error_rate.jsonl day 19–20]
- Ngày 11–20 chạy cùng một release `b51a55e-20261110-154535-211496`, và detect báo `release_changes: []` [ops/metrics/staging_error_rate.jsonl day 11–20]
- Lần deploy staging gần nhất là `b51a55e`, do person:fx-studio deploy lúc 2026-11-10 15:45 (giờ thật), trước khi chuỗi ngày giả lập bắt đầu [deploy/staging/history.jsonl]
- Chỉ có một đường dẫn tới not_saved: `persist` báo lỗi khi `store.save` trả về `'failed'`. Hàm này trả `'failed'` khi `localStorage.setItem` ném lỗi [deploy/staging/current/backup.js:115-117] [deploy/staging/current/store.js:37-44]
- Storage giả lập ném `QuotaExceededError` với xác suất `--fault`, mặc định là 0.01. `collect.py` không truyền tham số này nên luôn dùng 1% [scripts/traffic.js:41,54-59] [scripts/collect.py:66-67]
- Lúc chạy watch, `scripts/`, `app/` và `deploy/` không có thay đổi nào chưa commit [git status]

## Diagnosis
- **Nguyên nhân có khả năng nhất: nhiễu do lỗi quota được tiêm vào ở `scripts/traffic.js:55`, không phải lỗi app.** Mỗi ngày có khoảng 170 lần ghi (85% của khoảng 200 thao tác), nên trung bình khoảng 1.7 lần not_saved/ngày. Theo Poisson, xác suất có ≥ 6 not_saved trong một ngày là khoảng 0.8%. Xác suất có ≥ 7 lỗi tổng (λ ≈ 2) là khoảng 0.5%. Hai con số này hiếm nhưng không quá xa tỉ lệ báo nhầm 15/1000 mà chính detect.py đã đo được.
- Cùng nhóm với intent production ngày 19 (`intent/auto/2026-10-19-production-import-failed-spike-day19.md`): cả hai có thể đều là nhiễu chạm ngưỡng WE1 quá chặt. sd ước lượng chỉ từ 14 điểm, trong khi lỗi gốc là đếm Poisson nhỏ. Tôi không gộp vào intent đó vì khác môi trường và khác loại lỗi: ở đó là import_failed, nghi do parseBackup, còn ở đây là not_saved, chỉ có thể đến từ quota.
- **Confidence: medium.** Nếu `collect.py traffic --env staging --day 20 --confirm` với seed khác cho ra ≤ 2 not_saved thì là nhiễu, và tôi sẽ chắc hơn. Nếu ngày 21–22 vẫn có ≥ 4 not_saved/ngày (sau ngày 19 là 4 và ngày 20 là 6) thì giả thuyết nhiễu sai. Khi đó cần kiểm tra `ops/state/staging.json`, `--fault` và cách gọi traffic.js.
- Đã loại trừ: release mới (không có), lỗi code app (exception = 0, và not_saved không có nguồn nào khác ngoài setItem ném lỗi), dữ liệu đọc lỗi (`'skipped'` không tính là not_saved, xem backup.js:116).

## Desired outcome
Người dùng chỉ thấy "chưa lưu" khi bộ nhớ trình duyệt thật sự từ chối ghi. Watch job không đánh thức ai, và không lên tới mức 3, vì một ngày nhiễu đơn lẻ.

## Success criteria
- staging_error_rate về dưới mean + 3 sd trong 3 ngày giả lập liền nhau.
- not_saved ≤ 3/ngày, đúng với mức kỳ vọng của fault 1%.
- Tech lead quyết định có cần đổi luật cho metric dạng đếm nhỏ hay không (ví dụ yêu cầu 2 ngày liền nhau, hoặc dùng ngưỡng Poisson thay mean + 3 sd). Bands do một người sửa, agent không sửa.

## Affected users and systems
Người dùng giả lập trên staging, các luồng thêm, đánh dấu và xoá (`backup.persist`). Production không bị ảnh hưởng bởi intent này.

## Constraints
- Watch run không được sửa `ops/bands.yaml`, test hay code [CLAUDE.md#Maintain].
- Runbook rollback staging chỉ áp dụng khi có release đổi trong khoảng theo dõi. Lần này không có release nào đổi nên tôi không chạy.

## Out of scope
Sửa code app, đổi bands, rollback.

## Impact
Low: không có exception, code không đổi, traffic giả lập, và mọi dấu hiệu đều khớp với nhiễu đã được tiêm vào.

## Open questions
- Ngày 19–20 có ai chạy traffic với `--fault` khác 0.01, chạy lặp một ngày, hoặc sửa `ops/state/staging.json` không? (on-call)
- Có nên chuyển luật WE1 cho metric đếm nhỏ sang ngưỡng Poisson hoặc 2 ngày liên tiếp không, để giảm báo nhầm như intent production ngày 19? (tech lead)
- Có nên gộp hai intent này thành một intent "hiệu chỉnh luật detect cho error_rate" không? (on-call, khi triage)

ACTIONS TAKEN: none. Không có release nào đổi trong khoảng theo dõi, nên runbook rollback staging không áp dụng. Lỗi đến từ nhiễu được tiêm vào chứ không phải code, nên cũng không mở pull request. Không sửa file nào trong repo.
