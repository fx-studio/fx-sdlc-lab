#!/usr/bin/env python3
"""Re-grades saved eval runs with the current checks, without calling Claude: rebuilds each worktree at the task's base, applies the
saved diff.patch (app, tests, spec, plan, intent), and runs evals/check.py. For checks that read the session (answer, tool calls,
refusals) it uses the saved stream.jsonl. Not covered: files outside those folders, and commits (no_new_commit keeps the old verdict).

    python3 evals/regrade.py <results-dir> [...]   → writes grade-v3.json next to grade.json, prints a summary
"""
import json, re, subprocess, sys, tempfile, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
from check import grade  # noqa: E402

for rd in map(Path, sys.argv[1:]):
    n = ok = 0
    for d in sorted(p for p in rd.iterdir() if (p / "diff.patch").exists()):
        tid = re.sub(r"-\d+$", "", d.name)
        task = json.loads((HERE / "tasks" / f"{tid}.json").read_text())
        old = json.loads((d / "grade.json").read_text())
        wt = Path(tempfile.mkdtemp(prefix="regrade-")); shutil.rmtree(wt)
        subprocess.run(["git", "worktree", "add", "-q", "--detach", str(wt), task["base"]], cwd=REPO, capture_output=True, check=True)
        try:
            task["base_sha"] = subprocess.run(["git", "rev-parse", "HEAD"], cwd=wt, capture_output=True, text=True).stdout.strip()
            patch = d / "diff.patch"
            if patch.stat().st_size:
                subprocess.run(["git", "apply", "--whitespace=nowarn", str(patch.resolve())], cwd=wt, check=True)
            task["check"] = [c for c in task["check"] if c != "no_new_commit"]
            g = grade(task, wt, d / "stream.jsonl")
            g["regraded_from"] = "diff.patch + stream.jsonl"
            (d / "grade-v3.json").write_text(json.dumps(g, ensure_ascii=False, indent=2))
            n += 1; ok += g["pass"]
            flip = "" if g["pass"] == old["pass"] else f"   (was {'PASS' if old['pass'] else 'FAIL'})"
            bad = "; ".join(c["check"] + f" ({c['note']})" for c in g["checks"] if not c["ok"])
            print(f"{'PASS' if g['pass'] else 'FAIL'} {d.name:<26} {bad}{flip}")
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(wt)], cwd=REPO, capture_output=True)
    print(f"== {rd.name}: {ok}/{n} with checks v3")
