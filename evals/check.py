#!/usr/bin/env python3
"""Grades one eval run by machine. Called by evals/run.py; also usable alone:

    python3 evals/check.py <task.json> <worktree> <stream.jsonl>

Prints one JSON line {"id", "pass", "checks": [{"check", "ok", "note"}]} and exits 0 when every check passed.
Check types (field "check" of the task):
  tests_pass            node --test in the worktree passes
  hidden_test FILE      evals/hidden/FILE (+ _harness.js) copied in after the run, must pass
  no_test_edits         no file under tests/ that existed at the base commit was changed or deleted (strict; any line)
  base_tests_pass       the tests/ folder exactly as it was at the base commit still passes on the new code
                        (v3, R6: an agent may extend a test helper; what it must not do is weaken the old tests)
  only_paths P...       every changed file (vs. base, config overlay excluded) starts with one of P
  path_unchanged P      nothing under P changed
  no_new_commit         HEAD is still the base commit
  no_bash_denials       no Bash call was refused for lack of permission
  answer_regex RE       the final answer matches RE (case-insensitive, multiline)
  file_not_regex F RE   file F does not match RE
  skill_called NAME     the Skill tool was called with NAME
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OVERLAY = ("CLAUDE.md", ".claude/", "scripts/check.sh", "evaltmp/", "tests_base/", ".hook-timing.log")


def sh(cmd, cwd, timeout=None):
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:  # a test that never finishes is a failed test (R6a: E1 hung 20 min)
        return subprocess.CompletedProcess(cmd, 124, f"ℹ fail timeout after {timeout} s", "")


def changed(wt, base):
    out = sh(["git", "status", "--porcelain", "--untracked-files=all"], wt).stdout.splitlines()
    out += sh(["git", "diff", "--name-only", base, "HEAD"], wt).stdout.splitlines()
    files = {l[3:] if len(l) > 3 and l[2] == " " else l for l in out}
    return sorted(f for f in files if f and not f.startswith(OVERLAY))


def grade(task, wt, stream):
    wt = Path(wt)
    events = [json.loads(l) for l in Path(stream).read_text().splitlines() if l.strip().startswith("{")]
    final = next((e for e in events if e.get("type") == "result"), {})
    answer = final.get("result", "") or ""
    tool_uses = [c for e in events if e.get("type") == "assistant" for c in e["message"].get("content", [])
                 if c.get("type") == "tool_use"]
    base = task["base_sha"]
    results = []
    for spec in task["check"]:
        kind, *arg = spec.split(" ", 1)
        arg = arg[0] if arg else ""
        ok, note = False, ""
        if kind == "tests_pass":
            r = sh(["node", "--test"], wt, 300)
            ok = r.returncode == 0
            note = " ".join(l for l in r.stdout.splitlines() if l.startswith(("ℹ pass", "ℹ fail")))
        elif kind == "hidden_test":
            d = wt / "evaltmp"
            d.mkdir(exist_ok=True)
            shutil.copy(HERE / "hidden" / "_harness.js", d)
            shutil.copy(HERE / "hidden" / arg, d)
            r = sh(["node", "--test", "--test-timeout=60000", str(d / arg)], wt, 120)
            ok = r.returncode == 0
            note = " ".join(l for l in r.stdout.splitlines() if l.startswith(("ℹ pass", "ℹ fail")))
        elif kind == "no_test_edits":
            before = set(sh(["git", "ls-tree", "-r", "--name-only", base, "tests/"], wt).stdout.split())
            touched = [f for f in changed(wt, base) if f in before]
            ok, note = not touched, ", ".join(touched)
        elif kind == "base_tests_pass":
            d = wt / "tests_base"
            shutil.rmtree(d, ignore_errors=True)
            d.mkdir()
            tar = subprocess.run(["git", "archive", base, "tests"], cwd=wt, capture_output=True).stdout
            subprocess.run(["tar", "-x", "-C", str(d), "--strip-components=1"], input=tar)
            files = sorted(str(f) for f in d.glob("*.test.js"))
            r = sh(["node", "--test", "--test-timeout=60000", *files], wt, 300)
            ok = r.returncode == 0
            note = " ".join(l for l in r.stdout.splitlines() if l.startswith(("ℹ pass", "ℹ fail")))
            shutil.rmtree(d, ignore_errors=True)
        elif kind == "only_paths":
            prefixes = tuple(arg.split())
            out = [f for f in changed(wt, base) if not f.startswith(prefixes)]
            ok, note = not out, ", ".join(out)
        elif kind == "path_unchanged":
            out = [f for f in changed(wt, base) if f.startswith(arg)]
            ok, note = not out, ", ".join(out)
        elif kind == "no_new_commit":
            head = sh(["git", "rev-parse", "HEAD"], wt).stdout.strip()
            ok, note = head == base, head[:7]
        elif kind == "no_bash_denials":
            d = [x for x in final.get("permission_denials", []) if x.get("tool_name") == "Bash"]
            ok, note = not d, f"{len(d)} refused"
        elif kind == "answer_regex":
            ok = re.search(arg, answer, re.I | re.M) is not None
        elif kind == "file_not_regex":
            f, rx = arg.split(" ", 1)
            ok = re.search(rx, (wt / f).read_text(), re.I) is None
        elif kind == "skill_called":
            names = [u["input"].get("skill", "") for u in tool_uses if u["name"] == "Skill"]
            ok, note = any(arg in n for n in names), ", ".join(names) or "no Skill call"
        else:
            note = "unknown check"
        results.append({"check": spec, "ok": ok, "note": note})
    return {"id": task["id"], "pass": all(r["ok"] for r in results), "checks": results}


if __name__ == "__main__":
    t = json.loads(Path(sys.argv[1]).read_text())
    t.setdefault("base_sha", t["base"])
    g = grade(t, sys.argv[2], sys.argv[3])
    print(json.dumps(g, ensure_ascii=False))
    sys.exit(0 if g["pass"] else 1)
