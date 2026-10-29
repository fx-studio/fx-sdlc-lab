#!/usr/bin/env python3
"""Runs the eval suite: each task in its own temporary worktree at the task's base commit, with the CURRENT agent configuration
(CLAUDE.md, .claude/, scripts/check.sh of this checkout) laid over it. So a change to the configuration is what gets measured,
against the same code every time.

    python3 evals/run.py [--label <name>] [--only E1,E4] [--parallel 3] [--model opus] [--repeat 2]
                         [--config-from <dir>] [--sources project,local]

--config-from takes the configuration to measure from another folder (an A/B of CLAUDE.md without touching this checkout).

Each task: `claude -p` non-interactive, limited tools, user settings not loaded (--setting-sources project,local), git hooks off.
Then evals/check.py grades it. Writes evals/results/<date>-<label>/<id>/{stream.jsonl,grade.json} and appends a summary line
(pass rate, cost, time) to evals/results/history.jsonl. Exit code is non-zero when the pass rate is below --min (default 0).
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
from check import grade  # noqa: E402

TOOLS = ("Read,Glob,Grep,Write,Edit,Skill,Bash(node:*),Bash(bash scripts/check.sh),"
         "Bash(git status:*),Bash(git diff:*),Bash(git log:*)")
OVERLAY = ["CLAUDE.md", ".claude", "scripts/check.sh"]


def mask(s):
    s = s.replace(str(REPO), "<repo>").replace(str(Path.home()), "<home>")
    s = re.sub(r"/(private/)?var/folders/[^\s\"'`]+", "<thư-mục-tạm>", s)
    s = re.sub(r"(/private)?/tmp/[^\s\"'`\\]*", "<thư-mục-tạm>", s)
    s = re.sub(r"[\w.+-]+@(?!localhost)[\w-]+\.[\w.]+", "<email>", s)
    return s


def run_task(task, out, model, budget, cfg, sources):
    tid = task["id"]
    d = out / f"{tid}{task.get('_rep', '')}"
    d.mkdir(parents=True, exist_ok=True)
    wt = Path(tempfile.mkdtemp(prefix=f"eval-{tid}-"))
    shutil.rmtree(wt)
    subprocess.run(["git", "worktree", "add", "-q", "--detach", str(wt), task["base"]], cwd=REPO, check=True,
                   capture_output=True)
    try:
        task["base_sha"] = subprocess.run(["git", "rev-parse", "HEAD"], cwd=wt, capture_output=True, text=True).stdout.strip()
        for p in OVERLAY:
            src, dst = cfg / p, wt / p
            if src.is_dir():
                shutil.rmtree(dst, ignore_errors=True)
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "settings.local.json"))
            elif src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, dst)
        env = dict(os.environ, GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="core.hooksPath", GIT_CONFIG_VALUE_0="/dev/null",
                   **task.get("env", {}))
        cmd = ["claude", "-p", task["prompt"], "--output-format", "stream-json", "--verbose",
               "--allowedTools", task.get("tools", TOOLS), "--permission-mode", task.get("mode", "acceptEdits"),
               "--setting-sources", sources, "--max-budget-usd", str(budget)]
        if model:
            cmd += ["--model", model]
        t0 = time.time()
        p = subprocess.run(cmd, cwd=wt, capture_output=True, text=True, stdin=subprocess.DEVNULL, env=env)
        secs = time.time() - t0
        stream = d / "stream.jsonl"
        stream.write_text(mask(p.stdout))
        final = next((json.loads(l) for l in p.stdout.splitlines() if '"type":"result"' in l), {})
        g = grade(task, wt, stream)
        diff = subprocess.run(["git", "diff", task["base_sha"], "--", "app", "tests", "spec", "plan", "intent"], cwd=wt,
                              capture_output=True, text=True).stdout
        (d / "diff.patch").write_text(mask(diff))
        g.update(usd=final.get("total_cost_usd"), secs=round(secs, 1), turns=final.get("num_turns"),
                 answer=mask(final.get("result", "") or "")[-1500:])
        (d / "grade.json").write_text(json.dumps(g, ensure_ascii=False, indent=2))
        return g
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(wt)], cwd=REPO, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="run")
    ap.add_argument("--only", default="")
    ap.add_argument("--parallel", type=int, default=3)
    ap.add_argument("--model", default="opus")
    ap.add_argument("--budget", type=float, default=3.0, help="max USD per task")
    ap.add_argument("--config-from", default=str(REPO))
    ap.add_argument("--sources", default="project,local")
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--min", type=float, default=0.0, help="fail (exit 1) below this pass rate")
    a = ap.parse_args()
    tasks = [json.loads(p.read_text()) for p in sorted((HERE / "tasks").glob("*.json"))]
    if a.only:
        tasks = [t for t in tasks if t["id"] in a.only.split(",")]
    if a.repeat > 1:
        tasks = [dict(t, _rep=f"-{i}") for i in range(1, a.repeat + 1) for t in tasks]
    cfg = Path(a.config_from).resolve()
    out = HERE / "results" / f"{datetime.now():%Y%m%d-%H%M}-{a.label}"
    with ThreadPoolExecutor(a.parallel) as ex:
        grades = list(ex.map(lambda t: run_task(t, out, a.model, a.budget, cfg, a.sources), tasks))
    for g, t in zip(grades, tasks):
        g["id"] += t.get("_rep", "")
    passed = sum(g["pass"] for g in grades)
    usd = sum(g["usd"] or 0 for g in grades)
    line = {"when": f"{datetime.now():%Y-%m-%d %H:%M}", "label": a.label, "model": a.model,
            "config": subprocess.run(["git", "hash-object", str(cfg / "CLAUDE.md")], capture_output=True, text=True).stdout.strip()[:7],
            "config_from": "this checkout" if cfg == REPO else cfg.name, "sources": a.sources,
            "pass": passed, "total": len(grades), "usd": round(usd, 2),
            "tasks": {g["id"]: g["pass"] for g in grades}, "dir": out.name}
    with open(HERE / "results" / "history.jsonl", "a") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    for g in grades:
        bad = [c["check"] + (f" ({c['note']})" if c["note"] else "") for c in g["checks"] if not c["ok"]]
        print(f"{'PASS' if g['pass'] else 'FAIL'} {g['id']:<22} {g['usd'] or 0:5.2f} USD {g['secs']:6.0f} s  {'; '.join(bad)}")
    print(f"== {passed}/{len(grades)} passed · {usd:.2f} USD · {out.name}")
    sys.exit(0 if passed / max(len(grades), 1) >= a.min else 1)


if __name__ == "__main__":
    main()
