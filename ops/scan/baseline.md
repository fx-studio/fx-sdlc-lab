# Scan baseline

full baseline scan · 24 file · 4 phát hiện · 2026-11-10 16:06 · read-only, chưa xác thực

| # | Mức | Tin cậy | Chỗ | Luật | Phát hiện | Đã bỏ qua trước đó |
|---|---|---|---|---|---|---|
| 1 | high | high | `scripts/watch.py:141` | CWE-22 | Watch job can append model output to any repo file via '..' in the merge target |  |
| 2 | medium | medium | `scripts/review.py:19` | CWE-73 | 'Read-only' allowlist Bash(git diff:*)/git log/git show lets the agent write files through --output |  |
| 3 | low | medium | `tools/deploy-mcp/server.py:41` | CWE-88 | Deploy MCP passes the agent-supplied 'ref' to git without '--' or validation |  |
| 4 | low | medium | `scripts/on-intent-accepted.sh:11` | other | Spec job treats 'Status: accepted' anywhere in the intent as approval |  |
