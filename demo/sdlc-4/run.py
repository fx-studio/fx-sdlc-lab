#!/usr/bin/env python3
"""Chạy một lượt demo SDLC-4 (một phiên `claude -p`, không hỏi đáp), ghi lại cả tool call.

    python3 run.py <tên-run> "<prompt>" [--cwd <thư-mục>] [--allowed <tools>] [--mode <permission-mode>] [--model <m>]
                   [--system <file>] [--keep <đường-dẫn-tương-đối> ...] [--resume <session-id>]
                   [--env KEY=VALUE ...] [--sources <setting-sources>]

- Mặc định chạy ở gốc repo với quyền của bước Build: đọc, sửa file, chạy `node`, xem git. Không commit được (hook chặn).
- `--mode plan`: plan mode, Claude đọc được mọi thứ nhưng không sửa file nào.
- `--resume <id>`: tiếp đúng session trước (dùng cho lượt chất vấn plan).
- `--system <file>`: nối file vào system prompt (phiên nhân vật giả lập, chạy ở thư mục trống, model sonnet).
- `--keep`: chép file đó (tính từ --cwd) vào runs/<tên-run>/ sau khi chạy.
- Ghi vào runs/<tên-run>/: stream.jsonl (luồng thô), transcript.md (prompt, từng tool call, câu trả lời cuối), so-do.jsonl.

Khác run.py của SDLC-3: `--env` đặt biến môi trường cho phiên (TASK_KIND=fix bật hook protect-tests), mặc định
`--setting-sources project,local` để không nạp skill riêng của máy người chạy (bài học R6 SDLC-3), ghi skill nạp được.

Khác run.py của SDLC-2: che đường dẫn máy và email **ngay lúc ghi** (SDLC-2 phải thêm bốn commit che sau khi đã commit runs/),
ghi session id để tiếp được, và nhận --mode.
"""
import getpass, json, os, re, shutil, subprocess, sys, tempfile, time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ALLOWED = ("Read,Glob,Grep,Skill,Task,Write,Edit,"
           "Bash(node:*),Bash(ls:*),Bash(git status:*),Bash(git diff:*),Bash(git log:*),Bash(git show:*)")


def mask(s):
    s = s.replace(str(REPO), "<repo>")
    s = s.replace(str(Path.home()), "<home>")
    s = s.replace(os.path.realpath(tempfile.gettempdir()), "<thư-mục-tạm>").replace(tempfile.gettempdir(), "<thư-mục-tạm>")
    s = re.sub(r"/(private/)?var/folders/[^\s\"'`]+", "<thư-mục-tạm>", s)
    s = re.sub(r"/(private/)?tmp/[^\s\"'`]*", "<thư-mục-tạm>", s)
    s = re.sub(r"[\w.+-]+@(?!localhost)[\w-]+\.[\w.]+", "<email>", s)
    s = re.sub(rf"(?<![\w.]){re.escape(getpass.getuser())}(?![\w.])", "<user>", s)  # cột chủ file của `ls -l`
    return s


def opt(args, name, default=None, many=False):
    vals = [args[i + 1] for i, a in enumerate(args) if a == name]
    return vals if many else (vals[-1] if vals else default)


def short(inp):
    for k in ("file_path", "pattern", "command", "skill", "subagent_type", "path"):
        if k in inp:
            return f"{k}={inp[k]}"
    return json.dumps(inp, ensure_ascii=False)[:160]


def main():
    run, prompt, args = sys.argv[1], sys.argv[2], sys.argv[3:]
    cwd = Path(opt(args, "--cwd", REPO)).resolve()
    allowed = opt(args, "--allowed", ALLOWED)
    mode = opt(args, "--mode", "acceptEdits")
    model = opt(args, "--model")
    system = opt(args, "--system")
    resume = opt(args, "--resume")
    keep = opt(args, "--keep", many=True)
    env = dict(os.environ, **dict(kv.split("=", 1) for kv in opt(args, "--env", many=True)))
    sources = opt(args, "--sources", "project,local")

    d = HERE / "runs" / run
    d.mkdir(parents=True, exist_ok=True)
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--allowedTools", allowed,
           "--permission-mode", mode, "--setting-sources", sources]
    if model:
        cmd += ["--model", model]
    if system:
        cmd += ["--append-system-prompt", Path(system).read_text()]
    if resume:
        cmd += ["--resume", resume]

    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, stdin=subprocess.DEVNULL, env=env)
    dt = time.time() - t0
    (d / "stream.jsonl").write_text(mask(p.stdout))

    tools, result, final, sid, skills = [], "", {}, None, []
    for line in p.stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        sid = ev.get("session_id", sid)
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            skills = ev.get("skills", [])
        if ev.get("type") == "assistant":
            for c in ev["message"].get("content", []):
                if c.get("type") == "tool_use":
                    tools.append(f"{c['name']} · {short(c.get('input', {}))}")
        if ev.get("type") == "result":
            final, result = ev, ev.get("result", "")

    where = "gốc repo" if cwd == REPO else f"`{cwd.name}` (thư mục riêng của lượt này)"
    with open(d / "transcript.md", "w") as tr:
        body = (f"# {run}\n\nChạy {datetime.now():%Y-%m-%d %H:%M} ở {where}, chế độ quyền `{mode}`"
                f"{', tiếp session trước' if resume else ''}. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). "
                f"Luồng thô: `stream.jsonl`.\n\n## Prompt\n\n{prompt}\n\n## Tool call ({len(tools)})\n\n"
                + ("".join(f"{i}. {t}\n" for i, t in enumerate(tools, 1)) or "(không có)\n")
                + f"\n## Claude · {dt:.0f} s\n\n{result}\n")
        if p.returncode:
            body += f"\n## stderr\n\n```\n{p.stderr[-2000:]}\n```\n"
        tr.write(mask(body))

    for k in keep:
        src = cwd / k
        if src.exists():
            (d / Path(k).name).write_text(mask(src.read_text()))

    m = {"run": run, "giay": round(dt, 1), "usd": final.get("total_cost_usd"), "luot": final.get("num_turns"),
         "model": list(final.get("modelUsage", {})), "tool_call": len(tools), "session": sid,
         "tu_choi": [x.get("tool_name") for x in final.get("permission_denials", [])],
         "env": opt(args, "--env", many=True), "sources": sources, "skill_nap": len(skills)}
    (d / "so-do.jsonl").write_text(json.dumps(m, ensure_ascii=False) + "\n")
    print(json.dumps(m, ensure_ascii=False))
    print(mask(result[-2500:]))


if __name__ == "__main__":
    main()
