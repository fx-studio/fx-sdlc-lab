# Triage of agent-written intents

Kept by the person who owns the queue this week (decision: fix-now / schedule / dismiss; reason only for dismiss, from the fixed
list in `scripts/triage-stats.py`). After a decision, that person adds a `Triage: <decision> (<name>, <date>)` line under the
header of the intent, so the watch job stops counting it as open. People here are simulated (SDLC-6 demo).

| intent | decision | reason | by | date |
|---|---|---|---|---|
| intent/auto/2026-10-19-production-import-failed-spike-day19.md | schedule | | Huy | ngày 21 |
| intent/auto/2026-10-20-staging-not-saved-spike-day20.md | dismiss | false-alarm | Huy | ngày 21 |
| intent/auto/2026-10-19-production-import-failed-spike-day19.md | dismiss | wrong-diagnosis | Huy | ngày 22 |
| intent/auto/2026-11-01-ci-random-titles-test-empty-title.md | fix-now | | Huy | ngày 37 |
| intent/auto/2026-11-07-import-refuses-duplicate-titles.md | fix-now | | Huy | ngày 40 |

Ghi chú:
- Ngày 21 (R5a, `demo/sdlc-6/runs/R5a-huy-phan-loai/`): Huy xếp lịch file 19 để "quét `ops/state/production.json` tìm id trùng" (giả thuyết
  2 của agent), bỏ qua file 20 là báo nhầm, và đề xuất ngưỡng cho chỉ số đếm nhỏ.
- Ngày 22: điều tra theo lịch. Phát lại ngày 1–19 của production trên một state mới (cùng seed, kết quả khớp từng số) và in lý do từng
  lần nhập lỗi: **cả 5 là `importNotSaved`**, tức trình duyệt giả lập từ chối ghi (nhiễu 1%), không có id trùng. Bộ sinh số ngẫu nhiên
  đúng phân phối (400 seed × 1.000 lượt: trung bình 9,98, phương sai 9,97). Ngày 19 là đuôi hiếm của nhiễu (9 lỗi khi kỳ vọng ~2,3).
  Đổi quyết định: bỏ qua, lý do `wrong-diagnosis` (agent loại nhiễu quá sớm và đưa ra một nguyên nhân không có thật).
- Ngày 37: intent CI (agent viết ngày 32, gộp thêm ngày 33–37) → `fix-now`. Agent đã mở PR 9 ở mức 3 (cách ly). Review PR 9 bắt hai
  Important, trong đó một là luật vênh nhau (`bands.yaml` cho cách ly, `CLAUDE.md` cấm sửa test); Khoa sửa `CLAUDE.md` (ngoại lệ hẹp)
  rồi merge PR 9, và PR 10 sửa bộ sinh, gỡ cách ly (`flaky.sh` 30 lượt: 0).
- Ngày 40: intent sự cố 2e2ce98 (agent viết ngày 38, gộp lượt production và ngày 39) → `fix-now`, đã xử lý. `intent-reviewer` (R8a)
  thấy intent đã cũ (người đã rollback production, bộ đo đã sửa), 12 câu không nguồn, hai câu sai về thời gian do đồng hồ giả lập.
