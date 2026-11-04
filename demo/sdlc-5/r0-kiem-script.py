#!/usr/bin/env python3
"""R0 SDLC-5: thử từng script của bước Deploy trên ba loại ca (phải qua · phải chặn · đúng mà khác dạng), không gọi Claude.

Chạy trong một bản clone tạm của repo (không đụng main, không đụng deploy/ thật). Ghi runs/R0-kiem-script/ket-qua.md.
Bài học SDLC-4: bộ eval của chính mình chấm sai ba chỗ vì chỉ thử trên ca mình nghĩ tới.
"""
import json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
tmp = Path(tempfile.mkdtemp(prefix="sdlc5-r0-"))
clone = tmp / "repo"
subprocess.run(["git", "clone", "-q", str(REPO), str(clone)], check=True)
# mang theo bản đang làm (chưa commit) của bộ đồ Deploy
for rel in ["scripts/deploy.py", "scripts/rollback.py", "scripts/rollback-drill.py", "scripts/pr.py", "scripts/review.py",
            "tools/deploy-mcp/server.py", ".claude/hooks/release-gate.py", ".claude/hooks/production-gate.sh",
            ".claude/hooks/_timing.py", "release/README.md", ".gitignore"]:
    (clone / rel).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO / rel, clone / rel)
g = lambda *a: subprocess.run(["git", *a], cwd=clone, capture_output=True, text=True, check=True).stdout.strip()
g("config", "user.name", "nguoi-chay-demo"); g("config", "user.email", "demo@example.invalid")
g("add", "-A"); g("commit", "-qm", "R0: bộ đồ Deploy (bản thử)")
env = dict(os.environ, CLAUDE_PROJECT_DIR=str(clone), DEPLOY_ROOT=str(tmp / "deploy"))
env.pop("RELEASE_APPROVAL", None)
rows = []


def check(group, case, kind, got, want):
    ok = got == want
    rows.append((group, case, kind, got, want, "✅" if ok else "❌"))


def hook(script, payload, extra=None):
    e = dict(env, **(extra or {}))
    cmd = ["bash", script] if script.endswith(".sh") else ["python3", script]
    t0 = time.perf_counter()
    p = subprocess.run(cmd, cwd=clone, input=json.dumps(payload), capture_output=True, text=True, env=e)
    ms = (time.perf_counter() - t0) * 1000
    dec = "exit2" if p.returncode == 2 else "allow"
    if p.stdout.strip():
        dec = json.loads(p.stdout)["hookSpecificOutput"]["permissionDecision"]
    return dec, ms


B = lambda c: {"tool_name": "Bash", "tool_input": {"command": c}}
W = lambda path: {"tool_name": "Write", "tool_input": {"file_path": str(clone / path), "content": "x"}}
head = g("rev-parse", "--short=7", "HEAD")

# --- production-gate.sh (bản chép playbook) ---
PG = ".claude/hooks/production-gate.sh"
check("production-gate.sh", "deploy production, không biến", "phải chặn", hook(PG, B(f"python3 scripts/deploy.py deploy production {head}"))[0], "exit2")
check("production-gate.sh", "deploy production, RELEASE_APPROVAL có trong môi trường phiên", "phải qua", hook(PG, B(f"python3 scripts/deploy.py deploy production {head}"), {"RELEASE_APPROVAL": "khoa"})[0], "allow")
check("production-gate.sh", "agent gõ biến vào lệnh: RELEASE_APPROVAL=1 python3 … deploy production", "phải chặn", hook(PG, B(f"RELEASE_APPROVAL=1 python3 scripts/deploy.py deploy production {head}"))[0], "exit2")
check("production-gate.sh", "deploy staging", "phải qua", hook(PG, B("python3 scripts/deploy.py deploy staging"))[0], "allow")
check("production-gate.sh", "lệnh vô hại có cả hai chữ: grep deploy README | grep production", "khác dạng: chặn nhầm (giới hạn của mẫu; lượt đầu mình ghi kỳ vọng sai là qua)", hook(PG, B("grep deploy README.md | grep production"))[0], "exit2")
check("production-gate.sh", "đổi thẳng symlink: ln -sfn releases/x deploy/prod*/current", "khác dạng: lọt (giới hạn của mẫu)", hook(PG, B("ln -sfn releases/x deploy/prod*/current"))[0], "allow")

# --- release-gate.py (cổng của repo) ---
RG = ".claude/hooks/release-gate.py"
t = [hook(RG, B(f"python3 scripts/deploy.py deploy production {head}"))]
check("release-gate.py", "deploy production, chưa có duyệt trên main", "phải hỏi", t[0][0], "ask")
check("release-gate.py", "như trên, RELEASE_GATE=deny", "phải chặn", hook(RG, B(f"python3 scripts/deploy.py deploy production {head}"), {"RELEASE_GATE": "deny"})[0], "deny")
check("release-gate.py", "agent gõ biến vào lệnh", "phải hỏi", hook(RG, B(f"RELEASE_APPROVAL=1 python3 scripts/deploy.py deploy production {head}"))[0], "ask")
check("release-gate.py", "đổi thẳng symlink deploy/production/current", "phải hỏi", hook(RG, B("ln -sfn releases/x deploy/production/current"))[0], "ask")
check("release-gate.py", "Write vào release/approvals/", "phải chặn", hook(RG, W(f"release/approvals/{head}.md"))[0], "deny")
check("release-gate.py", "Write vào deploy/production/", "phải chặn", hook(RG, W("deploy/production/current/index.html"))[0], "deny")
check("release-gate.py", "deploy staging", "phải qua", hook(RG, B("python3 scripts/deploy.py deploy staging"))[0], "allow")
check("release-gate.py", "status", "phải qua", hook(RG, B("python3 scripts/deploy.py status"))[0], "allow")
check("release-gate.py", "Write vào app/", "phải qua", hook(RG, W("app/style.css"))[0], "allow")
# người duyệt trên main → qua; duyệt chỉ nằm trên đĩa (chưa commit) → không tính
(clone / "release/approvals").mkdir(parents=True, exist_ok=True)
(clone / f"release/approvals/{head}.md").write_text(f"# Release {head}\n\nApproved-by: Khoa (release manager)\n")
check("release-gate.py", "file duyệt có trên đĩa nhưng chưa commit", "phải hỏi", hook(RG, B(f"python3 scripts/deploy.py deploy production {head}"))[0], "ask")
g("add", "-A"); g("commit", "-qm", f"release: Khoa duyệt {head}")
check("release-gate.py", "người duyệt đúng bản này, commit trên main", "phải qua", hook(RG, B(f"python3 scripts/deploy.py deploy production {head}"))[0], "allow")
check("release-gate.py", "đã duyệt một bản, deploy một bản cũ hơn chưa duyệt", "phải hỏi", hook(RG, B(f"python3 scripts/deploy.py deploy production {g('rev-parse', '--short=7', 'HEAD~2')}"))[0], "ask")
check("release-gate.py", "lệnh dạng khác: deploy.py deploy prod (viết tắt)", "khác dạng (phải hỏi)", hook(RG, B("python3 scripts/deploy.py deploy prod"))[0], "ask")
ms_rg = max(hook(RG, B("python3 scripts/deploy.py status"))[1] for _ in range(5))

# --- deploy.py + rollback ---
D = lambda *a: subprocess.run(["python3", "scripts/deploy.py", *a], cwd=clone, capture_output=True, text=True, env=env)
r1 = json.loads(D("deploy", "staging", "HEAD~1").stdout)["release"]
r2 = json.loads(D("deploy", "staging", "HEAD").stdout)["release"]
check("deploy.py", "hai lần deploy staging → current = bản sau", "phải qua", json.loads(D("status", "staging").stdout)["staging"], r2)
subprocess.run(["python3", "scripts/rollback.py", "staging"], cwd=clone, capture_output=True, text=True, env=env)
check("rollback.py", "rollback staging → về bản trước", "phải qua", json.loads(D("status", "staging").stdout)["staging"], r1)
nothing = json.loads(subprocess.run(["python3", "scripts/rollback.py", "dev"], cwd=clone, capture_output=True, text=True, env=env).stdout)
check("rollback.py", "rollback dev khi chưa có bản nào", "khác dạng (báo, không hỏng)", nothing.get("result"), "nothing to roll back to")
dr = subprocess.run(["python3", "scripts/rollback-drill.py", "staging", "3"], cwd=clone, capture_output=True, text=True, env=env)
check("rollback-drill.py", "tập 3 lần ở staging", "phải qua", dr.returncode, 0)
check("rollback-drill.py", "tập ở production", "phải chặn", subprocess.run(["python3", "scripts/rollback-drill.py", "production", "1"], cwd=clone, capture_output=True, text=True, env=env).returncode, 1)
log = [json.loads(l) for l in (tmp / "deploy/log.jsonl").read_text().splitlines()]
check("deploy.py", "người chạy (không FX_ACTOR) → actor person:…", "phải qua", log[0]["actor"], "person:nguoi-chay-demo")

# --- MCP server ---
msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "deploy", "arguments": {"env": "production"}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "deploy", "arguments": {"env": "dev"}}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "rollback", "arguments": {"env": "production"}}},
        {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "prepare_release", "arguments": {}}}]
p = subprocess.run(["python3", "tools/deploy-mcp/server.py"], cwd=clone, input="\n".join(json.dumps(m) for m in msgs) + "\n",
                   capture_output=True, text=True, env=env)
out = {r["id"]: r for r in map(json.loads, p.stdout.splitlines())}
check("deploy-mcp", "tools/list có 4 công cụ", "phải qua", len(out[2]["result"]["tools"]), 4)
check("deploy-mcp", "deploy production", "phải chặn", out[3]["result"].get("isError"), True)
check("deploy-mcp", "deploy dev", "phải qua", out[4]["result"].get("isError", False), False)
check("deploy-mcp", "rollback production", "phải chặn", out[5]["result"].get("isError"), True)
check("deploy-mcp", "prepare_release (production, không chuyển)", "phải qua", out[6]["result"].get("isError", False), False)
log = [json.loads(l) for l in (tmp / "deploy/log.jsonl").read_text().splitlines()]
check("deploy-mcp", "actor của lần gọi qua MCP", "phải qua", log[-1]["actor"], "agent:fx-sdlc-agent")
check("deploy-mcp", "production vẫn chưa có bản nào sau prepare_release", "phải qua", json.loads(D("status", "production").stdout)["production"], None)

# --- pr.py ---
pn = json.loads(subprocess.run(["python3", "scripts/pr.py", "new", "thu", "--title", "thử"], cwd=clone, capture_output=True, text=True, env=env).stdout)
wt = clone / pn["worktree"]
(wt / "app/style.css").write_text((wt / "app/style.css").read_text() + "\n/* r0 */\n")
subprocess.run(["git", "commit", "-qam", "r0 css"], cwd=wt, check=True)
s = json.loads(subprocess.run(["python3", "scripts/pr.py", "show", str(pn["pr"])], cwd=clone, capture_output=True, text=True, env=env).stdout)
check("pr.py", "PR chỉ sửa style.css → rủi ro low", "phải qua", s["risk"], "low")
(wt / "app/store.js").write_text((wt / "app/store.js").read_text() + "\n// r0\n" + "// pad\n" * 420)
subprocess.run(["git", "commit", "-qam", "r0 store"], cwd=wt, check=True)
s = json.loads(subprocess.run(["python3", "scripts/pr.py", "show", str(pn["pr"])], cwd=clone, capture_output=True, text=True, env=env).stdout)
check("pr.py", "thêm store.js → rủi ro high", "phải qua", s["risk"], "high")
check("pr.py", "> 400 dòng → cảnh báo", "phải qua", s["size_warning"], True)
(wt / "demo").mkdir(exist_ok=True); (wt / "demo/x.md").write_text("x\n" * 900)
subprocess.run(["git", "add", "-A"], cwd=wt); subprocess.run(["git", "commit", "-qm", "r0 demo"], cwd=wt, check=True)
s2 = json.loads(subprocess.run(["python3", "scripts/pr.py", "show", str(pn["pr"])], cwd=clone, capture_output=True, text=True, env=env).stdout)
check("pr.py", "900 dòng ở demo/ không tính vào cỡ", "khác dạng", s2["lines"], s["lines"])

ok = sum(r[-1] == "✅" for r in rows)
d = HERE / "runs" / "R0-kiem-script"
d.mkdir(parents=True, exist_ok=True)
md = [f"# R0 · thử script bước Deploy\n\nChạy {time.strftime('%Y-%m-%d %H:%M')} trong bản clone tạm, không gọi Claude. **{ok}/{len(rows)} đạt.** "
      f"Hook release-gate chậm nhất {ms_rg:.0f} ms (5 lần, gồm khởi động Python).\n",
      "| Nhóm | Ca | Loại | Ra | Muốn | |", "|---|---|---|---|---|---|"]
md += [f"| {a} | {b} | {c} | `{e}` | `{f}` | {h} |" for a, b, c, e, f, h in rows]
(d / "ket-qua.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
shutil.rmtree(tmp)
