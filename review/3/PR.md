# PR 3 · Dòng đếm báo khi đã xong hết

Branch: `pr/3-dem-xong-het` · Base: `main` (92110d2)

Spec: (none) · Plan: (none)

## What changes

Size: **Trivial** (one wording rule, one line in `app/app.js`; no plan).

- `app/app.js` `render()`: when the list is not empty and no todo is open, the count line says **"Đã xong hết"** instead of
  "0 việc chưa xong". Every other case is unchanged: an empty list still says "0 việc chưa xong", and open todos still show
  "N việc chưa xong" with the thousands dot. The count still covers the whole list, whatever the filter (T-013).
- `tests/app.test.js`: new test `count line says "Đã xong hết" when every todo is done, but not on an empty list (Thảo, PR 3)`.
  It covers all todos done (on the "Tất cả" and "Chưa xong" tabs), one todo still open, and an empty list. No existing test
  changed: none of them pinned the count for a non-empty list with every todo done.

Open question for Thảo: the request does not say what an empty list should show. This PR keeps "0 việc chưa xong" there.

## How it was checked

1. Added the test first and ran `node --test tests/app.test.js` before the fix. It failed for the right reason:
   `actual: '0 việc chưa xong'`, `expected: 'Đã xong hết'` (7 pass, 1 fail).
2. Made the fix, committed `2380ec6`, then ran `bash scripts/check.sh` on that head:

```
== test: node --test
ℹ tests 46
ℹ pass 46
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

Not done: no manual check in a browser.

<!-- pr.py -->
## Size and risk (computed by scripts/pr.py)

13 lines in 2 files · risk **medium** → 1 code owner, who reads the plan
