# R5 · Đề xuất một dòng cho "Things Claude gets wrong"

Status: draft (người quyết định; mình không sửa `CLAUDE.md`)
Ngày: 2026-11-04

## Hai lần review bắt cùng một lỗi

| # | Run | PR · head | Mức | `claude_md_outdated` | Nội dung |
|---|---|---|---|---|---|
| 1 | `review/1/R2-review/findings.json` | PR 1 · 4ec1f73 | Important | `true` | PR thêm 1 test (44 → 45), `CLAUDE.md` › Verification vẫn ghi `tests 44 / pass 44` |
| 2 | `review/2/watch-1/findings.json` | PR 2 · 5a6d21b | Important | `true` | PR thêm 5 test (44 → 49), `CLAUDE.md` vẫn ghi 44; khối "How it was checked" trong PR.md cũng ghi 44, tức là **không dán từ một lần chạy thật** trên head đó |

**Sửa lại nguồn so với yêu cầu:** lần thứ hai không nằm ở `review/2/R4-review-0/findings.json`. Run đó (head 80c5c4a) có
`claude_md_outdated: false`; phát hiện liên quan ở đó là một Nit nói PR **không thêm test nào**, nên con số 44 vẫn đúng. Đó là lỗi
khác (thiếu test). Lần lặp lại thật sự là `watch-1` của cùng PR 2, sau khi các vòng sửa đã thêm test. Điều kiện "cùng lỗi lần hai"
của mục Deploy vẫn thoả, chỉ khác file chứng cứ.

Hiện trạng trên `main` (0c16734): `bash scripts/check.sh` ra 45/45, `CLAUDE.md:69-70` vẫn ghi 44. PR 1 đã merge với lỗi này còn
mở (`review/1/approval.md`: "để R5").

```
ℹ tests 45
ℹ pass 45
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

## Text đề xuất

Thêm vào cuối mục `## Things Claude gets wrong` trong `CLAUDE.md`:

```markdown
- 2026-11: Adding or removing tests without updating the healthy output under Verification (`ℹ tests N` / `ℹ pass N`), and
  writing a PR's check block from memory instead of pasting it (PR 1, PR 2). After the last test change, run
  `bash scripts/check.sh`, paste its real last lines into PR.md, and if the count changed, set the same N in CLAUDE.md in that PR.
```

## Vì sao viết như vậy

- **Nêu hành động, không chỉ nêu lỗi.** Cả hai lần, quy tắc "paste the last lines of its output" đã có sẵn; cái thiếu là bước nối
  "số test đổi → sửa con số trong CLAUDE.md". Dòng này gắn hai việc vào cùng một thời điểm: sau lần sửa test cuối cùng.
- **Gộp lỗi thứ hai của PR 2** (khối check trong PR.md ghi 44 trên head có 49). Cùng gốc: con số được viết lại từ trí nhớ thay vì lấy
  từ output thật. Sửa một mà bỏ một thì lần sau vẫn lệch.
- **"in that PR"**: cả hai finding đều yêu cầu sửa trong chính PR (REVIEW.md dòng 40). Để sau thì như PR 1: merge xong vẫn lệch.

## Điều người cần cân nhắc trước khi thêm

1. **Giá của việc sửa trong PR.** `scripts/pr.py` xếp `CLAUDE.md` vào rủi ro **high**. Ở PR 2, chỉ 2 dòng con số đã nâng PR từ medium
   lên high (cần 2 người, có tech lead; `review/2/watch.md`, mục Needs a person #4). Nếu áp dòng trên, **mọi PR thêm test sẽ thành
   high**. Hai cách tránh, người chọn:
   - (a) Giữ dòng trên, và cho `pr.py` bỏ qua diff `CLAUDE.md` chỉ đổi hai dòng `ℹ tests N` / `ℹ pass N`.
   - (b) Bỏ con số cứng khỏi Verification: ghi "healthy output ends with `ℹ fail 0` and `== check: OK`; `tests` equals `pass`".
     Khi đó lỗi này không còn chỗ để xảy ra và không cần dòng trong "Things Claude gets wrong". Đổi lại mất khả năng phát hiện
     test bị mất âm thầm (watch-1 có nêu rủi ro này).
2. **Nếu lặp lại lần ba** (theo luật của mục này: dòng thành hook): `scripts/check.sh` có thể so số `tests` thật với số trong
   `CLAUDE.md` và in `== check: FAILED` khi lệch. Mình chưa viết, chỉ ghi để người cân nhắc.
3. **Sửa con số trên `main` hiện tại** (44 → 45) là việc riêng, không thuộc dòng đề xuất; người làm khi commit dòng này là gọn nhất.
