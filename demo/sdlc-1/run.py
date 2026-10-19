#!/usr/bin/env python3
"""Chạy một kịch bản demo SDLC-1: phiên phỏng vấn (skill write-intent) hỏi, phiên nhân vật trả lời, tới khi có file intent.

    python3 run.py <tên-run> <persona.md> "<lời mở>" [--max 5]
    python3 run.py <tên-run> <persona.md> "<lời mở>" --baseline <thư-mục-chỉ-có-app>
    python3 run.py <tên-run> - "<yêu cầu>" --once        # một lượt, không nhân vật (vd. gọi intent-reviewer)

- Phiên phỏng vấn chạy ở gốc repo, chỉ được đọc repo và ghi vào intent/.
- Phiên nhân vật chạy ở thư mục trống, model sonnet, chỉ biết hồ sơ của mình.
- Ghi nguyên văn vào runs/<tên-run>/transcript.md, số đo vào runs/<tên-run>/so-do.jsonl.
"""
import json, subprocess, sys, tempfile, time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ALLOWED = "Read,Glob,Grep,Write(intent/**),Edit(intent/**),Skill,Task"
PERSONA_RULES = """Bạn đóng vai nhân vật trong hồ sơ dưới đây, đang được hỏi để viết một yêu cầu cho app Todo.
Luật: chỉ trả lời bằng dữ kiện trong hồ sơ. Câu nào hồ sơ không có thì nói "mình không biết". Không bịa số, không đề xuất giải pháp kỹ thuật
nếu hồ sơ không có. Trả lời ngắn, bằng tiếng Việt, như người thật nhắn tin. Nếu người hỏi đề nghị viết file, hoặc đây là lượt trả lời thứ 3,
kết thúc bằng câu "Viết đi."

HỒ SƠ:
"""


def claude(prompt, cwd, session=None, extra=()):
    cmd = ["claude", "-p", prompt, "--output-format", "json", *extra]
    if session:
        cmd += ["--resume", session]
    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    out = json.loads(p.stdout)
    return out, time.time() - t0


def main():
    run, persona, opening = sys.argv[1], sys.argv[2], sys.argv[3]
    args = sys.argv[4:]
    max_rounds = int(args[args.index("--max") + 1]) if "--max" in args else 5
    baseline = args[args.index("--baseline") + 1] if "--baseline" in args else None
    once = "--once" in args

    d = HERE / "runs" / run
    d.mkdir(parents=True, exist_ok=True)
    tr = open(d / "transcript.md", "w")
    metrics = open(d / "so-do.jsonl", "w")
    tr.write(f"# {run}\n\nChạy {datetime.now():%Y-%m-%d %H:%M}. Nguyên văn, không sửa.\n")

    def log(who, text, out, dt):
        tr.write(f"\n## {who} · {dt:.0f} s\n\n{text}\n")
        tr.flush()
        metrics.write(json.dumps({"ai": who, "giay": round(dt, 1), "usd": out.get("total_cost_usd"),
                                  "model": list(out.get("modelUsage", {})),
                                  "tu_choi": [x.get("tool_name") for x in out.get("permission_denials", [])]},
                                 ensure_ascii=False) + "\n")
        metrics.flush()
        print(f"\n===== {who} ({dt:.0f} s)\n{text}")

    if once or baseline:
        cwd = baseline or REPO
        tr.write(f"\n## Yêu cầu\n\n{opening}\n")
        out, dt = claude(opening, cwd, extra=() if baseline else ("--allowedTools", ALLOWED))
        log("Claude", out.get("result", ""), out, dt)
        return

    persona_text = Path(persona).read_text()
    before = set(p.name for p in (REPO / "intent").glob("*.md"))
    persona_dir = tempfile.mkdtemp(prefix="persona-")
    p_session = None
    i_session = None
    msg = f"/write-intent {opening}"
    tr.write(f"\n## Người kể (lời mở)\n\n{msg}\n")
    for rnd in range(1, max_rounds + 1):
        out, dt = claude(msg, REPO, i_session, ("--allowedTools", ALLOWED))
        i_session = out["session_id"]
        reply = out.get("result", "")
        log(f"Claude (lượt {rnd})", reply, out, dt)
        new = set(p.name for p in (REPO / "intent").glob("*.md")) - before
        if new:
            tr.write(f"\n---\n\nFile mới: {', '.join(sorted(new))}\n")
            break
        pout, pdt = claude(reply, persona_dir, p_session,
                           ("--model", "sonnet", "--append-system-prompt", PERSONA_RULES + persona_text))
        p_session = pout["session_id"]
        msg = pout.get("result", "")
        log(f"Người kể (lượt {rnd})", msg, pout, pdt)
    tr.close()


if __name__ == "__main__":
    main()
