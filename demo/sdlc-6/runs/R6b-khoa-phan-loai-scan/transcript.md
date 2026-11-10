# R6b-khoa-phan-loai-scan

Chạy 2026-11-10 16:07 ở `tmp.I9pjBmWUD0` (thư mục riêng của lượt này), chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

Scan bảo mật hằng tuần (tự dựng, chỉ đọc, chưa có bước xác thực) vừa chạy lần đầu trên toàn repo. Bạn là chủ policy-security. Người chạy demo đã kiểm tay hai phát hiện đầu: #1 có thật (đường dẫn 'intent/auto/../../CLAUDE.md' lọt phép kiểm), #2 có thật ('git diff --output=<file>' ghi được file).

#1 [high/high] scripts/watch.py:141 CWE-22 — Watch job can append model output to any repo file via '..' in the merge target
   why: save_intent accepts ctl['into'] when it starts with 'intent/auto/' and (ROOT / into).is_file(). It never resolves the path, so a value like 'intent/auto/../../CLAUDE.md', 'intent/auto/../../app/app.js' or 'intent/auto/../../.claude/hooks/no-self-approve.py' passes both checks. watch.py then appends the agent's free text to that file. The model's reply depends on untrusted evidence in its prompt and tools (CI logs, failing test names, commit subjects, metric data). A prompt injection planted there can therefore make the level-2 agent, which is meant to have read tools only, write into app code, hooks or CLAUDE.md. The write is done by watch.py itself, so the Claude Code hooks (protect-paths, no-self-approve) never see it.
   suggestion: Resolve the path and require it to be a direct child of AUTO: f = (ROOT / into).resolve(); accept only if f.parent == AUTO.resolve() and f.suffix == '.md' and f.name in {p.name for p, _, _ in open_intents()}. Otherwise treat the reply as 'new'. Add a test with an 'intent/auto/../../x' target.

#2 [medium/medium] scripts/review.py:19 CWE-73 — 'Read-only' allowlist Bash(git diff:*)/git log/git show lets the agent write files through --output
   why: review.py (line 19), triage.py (line 12) and scan.py (line 20) present 'Bash(git diff:*)', 'Bash(git log:*)' and 'Bash(git show:*)' as read-only. Each of these git commands takes --output=<file>, which writes to an arbitrary path. They also honour diff drivers and textconv set in the repo config. The reviewer reads a diff and PR.md written by another agent, and triage reads build logs. Both are untrusted inputs that can carry instructions. The prefix rule matches any arguments, so a session meant to be read-only can overwrite files in the worktree, in the main checkout (an absolute path) or in the home directory.
   suggestion: Narrow the rules or drop them in favour of Read/Grep plus a wrapper script that runs fixed git commands, for example a scripts/git-ro.py that rejects --output, --ext-diff and --textconv. Alternatively, add a PreToolUse hook that denies git diff/log/show calls containing '--output' or '--ext-diff'. Apply the same fix to the level-2 tools in ops/bands.yaml if they use these rules.

#3 [low/medium] tools/deploy-mcp/server.py:41 CWE-88 — Deploy MCP passes the agent-supplied 'ref' to git without '--' or validation
   why: The ref argument of deploy and prepare_release goes straight to 'git rev-parse --short=7 <ref>' and 'git archive --format=tar <ref> app' in scripts/deploy.py (lines 56 and 60), with no '--' before it and no check of its shape. A ref that starts with '-' is parsed as an option. git archive has --output=<file> (a file write) and --remote=<url> (a network fetch). The 'ref' is chosen by the agent, and the agent may be steered by untrusted evidence on watch runs. This tool is the scope boundary that is meant to hold whatever the agent does.
   suggestion: In server.py, reject any ref that does not match ^[A-Za-z0-9._/-]+$ or that starts with '-'. In deploy.build, resolve it once with 'git rev-parse --verify --end-of-options <ref>^{commit}' and pass only the resolved full sha to git archive.

#4 [low/medium] scripts/on-intent-accepted.sh:11 other — Spec job treats 'Status: accepted' anywhere in the intent as approval
   why: The pattern '^.*Status:[[:space:]]*accepted' matches the text anywhere on any line, not only the intent's own status line. An intent that quotes a ticket, a prior decision or a template line such as '(set Status: accepted to approve)' starts the headless /write-spec job on its first commit while it is still a draft. That job then commits a spec on main. The approval rule in CLAUDE.md says that only a person setting the status starts the next step. Separately, '$(git diff-tree …)' word-splits file names that contain spaces.
   suggestion: Match only the header line, for example grep -qE '^Status:[[:space:]]*accepted[[:space:]]*$' (or the template's exact line). Read file names with 'git diff-tree -z … | while IFS= read -r -d '' f'.

Với mỗi phát hiện, trả lời tiếng Việt một dòng: fix-now / schedule / dismiss; nếu dismiss thì lý do đúng một trong: false-alarm · known · accepted · wrong-diagnosis, và một câu vì sao. Phát hiện nào gói gọn trong một bản vá nhỏ thì nói 'PR'; rộng hơn thì nói 'intent'.

## Tool call (0)

(không có)

## Claude · 18 s

1. **#1: fix-now, PR.** Lỗi có thật và đã kiểm tay. Nó cho phép ghi ngoài hàng rào hook, nên đây là phát hiện nặng nhất. Bản vá nhỏ: `resolve()`, kiểm `parent == AUTO`, thêm test với `intent/auto/../../x`.

2. **#2: schedule, intent.** Lỗi có thật và đã kiểm tay. Nó làm sai lời hứa "chỉ đọc" ở `review.py`, `triage.py`, `scan.py` và `ops/bands.yaml`. Cách sửa (hook chặn `--output`/`--ext-diff` hay script bọc `git-ro.py`) là quyết định thiết kế đụng nhiều nơi, nên cần intent trước. Trong lúc chờ, bản vá #1 đã đóng đường ghi nghiêm trọng nhất.

3. **#3: schedule, PR.** Mức thấp nhưng đúng chỗ là ranh giới deploy. Bản vá nhỏ: regex cho `ref`, `--end-of-options`, rồi truyền sha đã resolve cho `git archive`. Phát hiện này chưa ai kiểm tay, nên PR phải có test với `ref` bắt đầu bằng `-`. Vì chạm deploy, PR qua tay release manager.

4. **#4: fix-now, PR.** Lỗi làm job spec chạy khi intent mới là bản nháp, trái quy tắc CLAUDE.md rằng chỉ người đặt trạng thái mới khởi động bước tiếp theo. Bản vá một dòng: `grep -qE '^Status:[[:space:]]*accepted[[:space:]]*$'`, kèm `diff-tree -z`. Phát hiện này cũng chưa kiểm tay, nên cần thêm test với dòng `(set Status: accepted to approve)`.

Mỗi PR chỉ làm một phát hiện, để review nhỏ gọn.
