# Nhánh của demo SDLC-6 (chép ra vì nhánh git không theo zip/PR)

| Nhánh | Trạng thái | Ở đâu |
|---|---|---|
| `feat/import-guard` (`2e2ce98`) | **Lỗi gài B**, lên staging + production ngày giả lập 38, rollback; **không bao giờ merge** | `feat_import-guard.diff` + `.log` (diff so với điểm rẽ nhánh) |
| `test/random-titles` (`9253a71`) | Lỗi gài A (test chập chờn), merge vào `main` ngày 31, sửa ở PR 9 + PR 10 | trong lịch sử `main` |
| `feat/clear-done` (`fe15d3e`) | Lỗi gài C (xoá hàng loạt không hỏi), merge cho scan tuần, **revert** `1e6f9d2` | trong lịch sử `main` |
| `pr/8` → `pr/12` | Merge (người duyệt, giả lập) | trong lịch sử `main`, `review/<n>/` |

Đáp án của cả ba lỗi gài: `../niem-phong/dap-an.md` (khớp `../dap-an.sha256`).
