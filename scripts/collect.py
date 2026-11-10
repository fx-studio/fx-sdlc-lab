#!/usr/bin/env python3
"""Collect one data point of a watched metric (SDLC-6, Maintain). Detection reads these files; no model is involved here.

    python3 scripts/collect.py ci --day <n> [--runs 4]            CI failure rate: run the test suite <runs> times
    python3 scripts/collect.py traffic --env <env> --day <n> [--confirm]   failed-action rate of simulated users on <env>
                                                                  (--confirm: a check after an action, kept out of the series)
    python3 scripts/collect.py pr-cycle                           hours from "PR opened" to "merged", one point per merged PR

Every point goes to ops/metrics/<metric>.jsonl, one JSON object per line:
    {"day": n, "date": "YYYY-MM-DD", "value": x, ..., "simulated_clock": true}

**The clock is simulated.** A "day" is one collection run; the date is 2026-10-01 + day. The runs themselves are real (the test
suite really runs, the simulated users really run the release that is live). This lets the demo build 30 days of history in one
sitting; a real team would schedule this job daily and drop the day counter.

Failed CI runs keep their log in ops/ci/<metric-day>-run<i>.log (read them with scripts/ci_log.py).
"""
import json, re, subprocess, sys, zlib
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "ops" / "metrics"
CI_LOGS = ROOT / "ops" / "ci"
STATE = ROOT / "ops" / "state"
START = date(2026, 10, 1)


def opt(a, name, default=None):
    return a[a.index(name) + 1] if name in a else default


def append(metric, point):
    METRICS.mkdir(parents=True, exist_ok=True)
    with open(METRICS / f"{metric}.jsonl", "a") as f:
        f.write(json.dumps(point, ensure_ascii=False) + "\n")
    print(json.dumps({"metric": metric, **point}, ensure_ascii=False))


def sha(cwd=ROOT):
    return subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], capture_output=True, text=True, cwd=cwd).stdout.strip()


def ci(a):
    day, runs = int(opt(a, "--day")), int(opt(a, "--runs", "4"))
    CI_LOGS.mkdir(parents=True, exist_ok=True)
    failed, failing = 0, []
    for i in range(1, runs + 1):
        p = subprocess.run(["node", "--test", "--test-reporter=tap"], cwd=ROOT, capture_output=True, text=True)
        if p.returncode:
            failed += 1
            names = re.findall(r"^\s*not ok \d+ - (.+)$", p.stdout, re.M)
            failing += names
            (CI_LOGS / f"ci-day{day:03d}-run{i}.log").write_text(
                f"# CI run · simulated day {day} ({START + timedelta(days=day - 1)}) · commit {sha()} · run {i}/{runs}\n"
                f"# command: node --test --test-reporter=tap · exit {p.returncode}\n\n{p.stdout[-15000:]}{p.stderr[-3000:]}")
    append("ci_fail_rate", {"day": day, "date": str(START + timedelta(days=day - 1)), "value": failed / runs, "runs": runs,
                            "failed": failed, "failing_tests": sorted(set(failing)), "commit": sha(), "simulated_clock": True})


def traffic(a):
    env, day = opt(a, "--env"), int(opt(a, "--day"))
    STATE.mkdir(parents=True, exist_ok=True)
    release = ROOT / "deploy" / env / "current"
    seed = day * 1000 + zlib.crc32(env.encode()) % 1000 + (500 if "--confirm" in a else 0)
    state = STATE / f"{env}.json"
    extra = []
    if "--confirm" in a:
        # A check run must not change the simulated users (fix 2026-11-10, day 38: the first version replayed the day on the real
        # state with the same ids, wrote repeated ids into it, and broke every later import; the watch agent pointed at it).
        import shutil, tempfile
        tmp = Path(tempfile.mkdtemp()) / f"{env}.json"
        if state.exists():
            shutil.copyfile(state, tmp)
        state, extra = tmp, ["--tag", "c-"]
    p = subprocess.run(["node", str(ROOT / "scripts" / "traffic.js"), "--release", str(release), "--state",
                        str(state), "--seed", str(seed), "--day", str(day), *extra],
                       capture_output=True, text=True, check=True)
    r = json.loads(p.stdout)
    # --confirm: a check after an action (for example after a rollback). Same day, other seed; stored apart, not in the series.
    metric = f"{env}_error_rate" + (".confirm" if "--confirm" in a else "")
    append(metric, {"day": day, "date": str(START + timedelta(days=day - 1)), "value": round(r["rate"], 5),
                                 "actions": r["actions"], "failed": r["failed"], "by_kind": r["by_kind"],
                                 "release": r["release"], "simulated_clock": True, "simulated_users": True})


def pr_cycle(a):
    out = []
    for pr in sorted((ROOT / "review").glob("*/PR.md")):
        n = pr.parent.name
        opened = subprocess.run(["git", "log", "--diff-filter=A", "--format=%cI", "--", str(pr.relative_to(ROOT))],
                                capture_output=True, text=True, cwd=ROOT).stdout.split()
        merged = subprocess.run(["git", "log", "--merges", "--format=%cI %s", "main"], capture_output=True, text=True,
                                cwd=ROOT).stdout.splitlines()
        hit = [m.split(" ", 1)[0] for m in merged if re.search(rf"\bPR {n}\b", m)]
        if opened and hit:
            from datetime import datetime
            h = (datetime.fromisoformat(hit[-1]) - datetime.fromisoformat(opened[-1])).total_seconds() / 3600
            out.append({"pr": n, "opened": opened[-1], "merged": hit[-1], "value": round(h, 2)})
    for o in out:
        append("pr_cycle_hours", o)
    if not out:
        print("no merged PR found")


if __name__ == "__main__":
    cmd, rest = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
    {"ci": ci, "traffic": traffic, "pr-cycle": pr_cycle}.get(cmd, lambda _: print(__doc__))(rest)
