# R5a-huy-phan-loai

Chạy 2026-11-10 15:50 ở `tmp.Is4UxO3gdq` (thư mục riêng của lượt này), chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Hàng đợi intent do agent viết (watch job) có hai file, chờ bạn phân loại. Bối cảnh: dữ liệu và người dùng là giả lập; mỗi ngày khoảng 1% thao tác thất bại vì trình duyệt từ chối ghi, đó là nhiễu bình thường. Trong 30 ngày qua không có release mới nào lên staging hay production.

Trả lời bằng tiếng Việt, ngắn. Với mỗi file: quyết định (fix-now / schedule / dismiss), nếu dismiss thì lý do **đúng một** trong: false-alarm · known · accepted · wrong-diagnosis; và một câu vì sao. Cuối cùng: một câu bạn muốn đề xuất gì cho ngưỡng (nếu có).

=== FILE 1: intent/auto/2026-10-19-production-import-failed-spike-day19.md ===
# Intent: Lượng "nhập lại file sao lưu thất bại" tăng vọt trên production, ngày 19

Page: on-call. **Rollback không giúp gì ở đây, khuyên không chạy.** Production chưa đổi release trong cả khoảng theo dõi. Bản trước trong `deploy/production/history.jsonl` là `20b4e8f-20261104-102454-306665`, nhưng `app/` của nó giống hệt bản đang chạy (`git diff --stat 20b4e8f b51a55e -- app/` không ra gì). Nếu on-call vẫn muốn quay về bản đó thì chạy `python3 scripts/rollback.py production`. Chạy hay không là quyết định của một người.

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch production_error_rate level 3, simulated day 19 · Date: 2026-10-19

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

=== FILE 2: intent/auto/2026-10-20-staging-not-saved-spike-day20.md ===
# Intent: Trên staging, số lần "chưa lưu được" tăng lên ngày 20, không có release mới

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch staging_error_rate level 3, simulated day 20 · Date: 2026-10-20

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

## Tool call (0)

(không có)

## Claude · 15 s

**File 1: production, import_failed ngày 19 → `schedule`**
Đây không phải nhiễu thông thường: 5 lần so với kỳ vọng khoảng 0.3 lần/ngày, xác suất cỡ 1e-4 đến 1e-5. Nguyên nhân chưa rõ (confidence low) nhưng không cần fix-now, vì không có release, không có exception và traffic là giả lập. Rollback cũng vô ích vì `app/` của hai bản giống hệt nhau. Việc cần làm là quét `ops/state/production.json` tìm id trùng (nghi ngày 19 bị chạy hai lần), mất chừng 10 phút.

**File 2: staging, not_saved ngày 20 → `dismiss`, lý do: `false-alarm`**
6 lần not_saved so với kỳ vọng khoảng 1.7 lần/ngày chỉ có xác suất khoảng 0.8%. Mức đó khớp với tỉ lệ báo nhầm detect.py đã tự đo, và nguồn lỗi duy nhất là quota 1% được tiêm vào. Nếu ngày 21–22 vẫn có ≥ 4 lần/ngày thì mở lại.

**Đề xuất về ngưỡng:** với metric đếm nhỏ như error_rate, chuyển từ mean + 3 sd (sd ước lượng từ chỉ 14 điểm) sang ngưỡng Poisson, hoặc yêu cầu vượt ngưỡng 2 ngày liên tiếp mới page. Khoa quyết định, vì `bands.yaml` do người sửa.
