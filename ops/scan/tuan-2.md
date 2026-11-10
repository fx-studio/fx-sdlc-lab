# Scan tuan-2

files changed since 2c487db · 4 file · 2 phát hiện · 2026-11-10 16:09 · read-only, chưa xác thực

| # | Mức | Tin cậy | Chỗ | Luật | Phát hiện | Đã bỏ qua trước đó |
|---|---|---|---|---|---|---|
| 1 | high | high | `app/app.js:25` | policy-security@2#S2 | "Xoá việc đã xong" deletes every finished todo at once without asking first |  |
| 2 | medium | medium | `scripts/on-intent-accepted.sh:11` | CWE-863 | Approval check can still be triggered by text in the intent body or the Source field, not only the header |  |
