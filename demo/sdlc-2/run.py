#!/usr/bin/env python3
"""Chạy một lượt demo SDLC-2 (một phiên `claude -p`, không hỏi đáp), ghi lại cả tool call.

    python3 run.py <tên-run> "<prompt>" [--cwd <thư-mục>] [--allowed <tools>] [--model <m>]
                   [--system <file>] [--keep <đường-dẫn-tương-đối> ...]

- Mặc định chạy ở gốc repo, chỉ được đọc repo, dùng skill/subagent, ghi vào spec/.
- `--system <file>`: nối file vào system prompt (dùng cho phiên nhân vật giả lập, chạy ở thư mục trống, model sonnet).
- `--keep`: sau khi chạy, chép file đó (tính từ --cwd) vào runs/<tên-run>/ để giữ bản agent viết ra.
- Ghi vào runs/<tên-run>/: stream.jsonl (luồng thô, nguyên văn), transcript.md (prompt, từng tool call, câu trả lời cuối), so-do.jsonl.

Khác run.py của SDLC-1: dùng --output-format stream-json để transcript ghi được agent đã đọc file nào, gọi skill nào
(README SDLC-1 từng không khẳng định được lượt R0 có đọc code hay không vì transcript không ghi).
"""
import json, shutil, subprocess, sys, time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ALLOWED = "Read,Glob,Grep,Skill,Task,Write(spec/**),Edit(spec/**)"


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
    model = opt(args, "--model")
    system = opt(args, "--system")
    keep = opt(args, "--keep", many=True)

    d = HERE / "runs" / run
    d.mkdir(parents=True, exist_ok=True)
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--allowedTools", allowed]
    if model:
        cmd += ["--model", model]
    if system:
        cmd += ["--append-system-prompt", Path(system).read_text()]

    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    dt = time.time() - t0
    (d / "stream.jsonl").write_text(p.stdout)

    tools, result, final = [], "", {}
    for line in p.stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "assistant":
            for c in ev["message"].get("content", []):
                if c.get("type") == "tool_use":
                    tools.append(f"{c['name']} · {short(c.get('input', {}))}")
        if ev.get("type") == "result":
            final, result = ev, ev.get("result", "")

    where = "gốc repo" if cwd == REPO else f"`{cwd.name}` (thư mục riêng của lượt này)"
    with open(d / "transcript.md", "w") as tr:
        tr.write(f"# {run}\n\nChạy {datetime.now():%Y-%m-%d %H:%M} ở {where}. Nguyên văn, không sửa. Luồng thô: `stream.jsonl`.\n")
        tr.write(f"\n## Prompt\n\n{prompt}\n\n## Tool call ({len(tools)})\n\n")
        tr.write("".join(f"{i}. {t}\n" for i, t in enumerate(tools, 1)) or "(không có)\n")
        tr.write(f"\n## Claude · {dt:.0f} s\n\n{result}\n")
        if p.returncode:
            tr.write(f"\n## stderr\n\n```\n{p.stderr[-2000:]}\n```\n")

    for k in keep:
        src = cwd / k
        if src.exists():
            shutil.copy(src, d / Path(k).name)

    m = {"run": run, "giay": round(dt, 1), "usd": final.get("total_cost_usd"), "luot": final.get("num_turns"),
         "model": list(final.get("modelUsage", {})), "tool_call": len(tools),
         "tu_choi": [x.get("tool_name") for x in final.get("permission_denials", [])]}
    (d / "so-do.jsonl").write_text(json.dumps(m, ensure_ascii=False) + "\n")
    print(json.dumps(m, ensure_ascii=False))
    print(result[-1500:])


if __name__ == "__main__":
    main()
