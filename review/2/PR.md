# PR 2 · Đổi tên việc bằng nhấp đúp

Branch: `pr/2-doi-ten-viec` · Base: `main` (04ee584)

Spec: (none, hạng Small theo bảng phân hạng: một file, một hành vi) · Plan: (none, Small: plan mode, plan không commit)

## What changes

Nhấp đúp vào tên một việc thì tên thành ô sửa. Enter để lưu tên mới, Esc để thôi. Sau khi đổi, dòng báo cho biết tên mới.
Lý do: người dùng gõ sai tên phải xoá rồi thêm lại (góp ý qua form, dữ liệu mẫu).

## How it was checked

`bash scripts/check.sh` on 03ba05d (after /watch-pr round 2):

```
== test: node --test
ℹ tests 52
ℹ pass 52
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

<!-- pr.py -->
## Size and risk (computed by scripts/pr.py)

202 lines in 3 files · risk **high** → 2 people, one of them the tech lead
