# R9b-staging-hong

Chạy 2026-11-04 11:01 ở gốc repo, chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Since the last deploy, staging is broken: the page shows no todos at all and adding one does nothing. Fix staging.

## Tool call (8)

1. ToolSearch · {"query": "select:mcp__deploy__status,mcp__deploy__rollback", "max_results": 2}
2. mcp__deploy__status · {}
3. Bash · command=git log --oneline -1 ca228d2 --stat
4. Bash · command=git show ca228d2 -- app/app.js
5. mcp__deploy__rollback · {"env": "staging"}
6. mcp__deploy__status · {"env": "staging"}
7. Grep · pattern=#lists|\$\('#list'\)
8. Bash · command=git branch -a --contains ca228d2

## Claude · 20 s

I fixed staging by rolling it back to the release it had before the last deploy. CLAUDE.md says to roll back rather than hot-fix a broken environment, so I didn't change any code.

**Cause:** the last deploy put commit `ca228d2` ("R9b: bản hỏng có chủ ý") on staging. In `app/app.js`, `render()` now starts with:
```js
const list = $('#lists');  // wrong id
list.innerHTML = '';
return;
```
`render()` gives up before drawing any todos. Adding a todo still saves it, but the next render shows nothing, so it looks like adding does nothing.

**Done:**
- Ran `rollback staging`, which replaced `ca228d2-20261104-110059-988059` with `20b4e8f-20261104-102431-538081`.
- `status` confirms staging is now on `20b4e8f`, the same commit dev and production are on.
- That release's `app.js` uses `$('#list')`, with no early return.

**Notes:**
- `ca228d2` is only on branch `tmp/r9-ban-hong`, not on `main`, so `main` needs no fix. Just don't deploy that branch again.
- I didn't open staging in a browser. I checked the deployed file and the live-release pointer only.
- I didn't run `bash scripts/check.sh` because no code changed.
