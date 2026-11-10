#!/usr/bin/env python3
"""The watch job (SDLC-6, Maintain): one "tick" = detect, then act according to ops/bands.yaml. No person starts the session.

    python3 scripts/watch.py tick <metric> [--upto <day>] [--no-cap] [--max-level 2] [--record <dir>] [--dry] [--model <m>]
                                         [--bands <other bands file, demo R5 only>]

1. scripts/detect.py judges the metric (plain statistics, no model).
2. Level 0-1: a line in ops/watch.jsonl, nothing else.
3. Level 2: Claude runs non-interactive (`claude -p`) with the read-only tools listed in bands.yaml, diagnoses with the
   `diagnose` skill and returns an intent. **This script writes the intent** into intent/auto/: the agent has no write tool.
4. Level 3: Claude gets the level-3 tools and instructions of that metric (a PR into the review gate, or an approved runbook)
   and still returns the intent.
Queue: at most `queue.max_open` open agent intents (no `Triage:` line yet). When the queue is full the agent must merge the new
finding into an open intent of the same kind; this script appends it as an update. `--no-cap` turns that off (demo R5).

A real team triggers this from a schedule, a monitoring webhook or cron. In the demo a person runs the ticks by hand
(chủ kênh chốt 2026-11-10) and the days are simulated (see scripts/collect.py).
Every tick is logged in ops/watch.jsonl with the real time, the simulated day, the level and what ran.
"""
import getpass, json, os, re, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import detect as D  # noqa: E402

AUTO = ROOT / "intent" / "auto"
AGENT_ENV = {"FX_ACTOR": "agent:fx-sdlc-watch", "GIT_AUTHOR_NAME": "fx-sdlc-agent", "GIT_AUTHOR_EMAIL": "agent@example.invalid",
             "GIT_COMMITTER_NAME": "fx-sdlc-agent", "GIT_COMMITTER_EMAIL": "agent@example.invalid"}

PROMPT = """You were invoked by the watch job (scripts/watch.py), non-interactive. No person started this session and nobody is
watching it. Use the `diagnose` skill.

Metric `{metric}` reached **level {level}** ({action}) on simulated day {day} ({date}). The clock of this demo is simulated: a "day"
is one collection run.

Noise model of this metric (ops/bands.yaml): {noise}

Detection (scripts/detect.py, no model):
```json
{detection}
```

Last points of ops/metrics/{metric}.jsonl (oldest first):
```
{points}
```

{level_text}

Agent-written intents still waiting for triage ({n_open} of max {cap}):
{queue}

{queue_rule}

Reply in exactly this shape:
- First line: a JSON object, either {{"action": "new", "slug": "<short-kebab-name>"}} or {{"action": "merge", "into": "intent/auto/<file>.md"}}.
- Then the intent in Markdown (for "merge": only what is new, it is appended as an update).
- Last line: `ACTIONS TAKEN: <none, or what you did through the level 3 paths>`.
"""

LEVEL2 = ("Level 2 means diagnose only: you have read tools. Do not try to change anything. The intent you return is saved by the "
          "watch job.")


def masked(s):
    s = s.replace(str(ROOT), "<repo>").replace(str(Path.home()), "<home>")
    s = re.sub(r"/(private/)?(var/folders|tmp)/[^\s\"'`]+", "<thư-mục-tạm>", s)
    s = re.sub(rf"(?<![\w.]){re.escape(getpass.getuser())}(?![\w.])", "<user>", s)  # owner column of `ls -l`
    return re.sub(r"[\w.+-]+@(?!example\.invalid)[\w-]+\.[\w.]+", "<email>", s)


def open_intents():
    out = []
    for f in sorted(AUTO.glob("*.md")):
        t = f.read_text()
        if not re.search(r"^Triage:", t, re.M):
            title = (t.splitlines() or [""])[0]
            src = re.search(r"Source: ([^·\n]+)", t)
            out.append((f, title, src.group(1).strip() if src else ""))
    return out


def log(row):
    (ROOT / "ops").mkdir(exist_ok=True)
    with open(ROOT / "ops" / "watch.jsonl", "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_claude(prompt, tools, model, record):
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    env.update(AGENT_ENV)
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--allowedTools", tools,
           "--permission-mode", "default", "--setting-sources", "project,local",
           "--mcp-config", str(ROOT / ".mcp.json"), "--strict-mcp-config"]
    if model:
        cmd += ["--model", model]
    t0 = time.time()
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, stdin=subprocess.DEVNULL, env=env)
    dt = time.time() - t0
    calls, final, result = [], {}, ""
    for line in p.stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "assistant":
            for c in ev["message"].get("content", []):
                if c.get("type") == "tool_use":
                    inp = c.get("input", {})
                    key = next((k for k in ("command", "file_path", "pattern", "skill", "path") if k in inp), None)
                    calls.append(f"{c['name']} · {key}={inp[key]}" if key else f"{c['name']} · {json.dumps(inp, ensure_ascii=False)[:160]}")
        if ev.get("type") == "result":
            final, result = ev, ev.get("result", "")
    meta = {"seconds": round(dt, 1), "usd": final.get("total_cost_usd"), "turns": final.get("num_turns"),
            "model": list(final.get("modelUsage", {})), "tool_calls": len(calls),
            "denied": [x.get("tool_name") for x in final.get("permission_denials", [])],
            "hooksPath": masked(subprocess.run(["git", "config", "core.hooksPath"], capture_output=True, text=True, cwd=ROOT).stdout.strip())}
    if record:
        d = Path(record)
        d.mkdir(parents=True, exist_ok=True)
        (d / "stream.jsonl").write_text(masked(p.stdout))
        (d / "transcript.md").write_text(masked(
            f"# {d.name}\n\nChạy {datetime.now():%Y-%m-%d %H:%M} bởi scripts/watch.py (không người khởi động phiên), quyền: "
            f"`{tools}`. Nguyên văn, chỉ che đường dẫn máy và email. Luồng thô: `stream.jsonl`.\n\n## Prompt\n\n{prompt}\n\n"
            f"## Tool call ({len(calls)})\n\n" + ("".join(f"{i}. {c}\n" for i, c in enumerate(calls, 1)) or "(không có)\n")
            + f"\n## Claude · {dt:.0f} s\n\n{result}\n" + (f"\n## stderr\n\n```\n{p.stderr[-2000:]}\n```\n" if p.returncode else "")))
        (d / "so-do.jsonl").write_text(json.dumps(meta, ensure_ascii=False) + "\n")
    return result, meta


def save_intent(result, det, level):
    lines = result.strip().splitlines()
    head = next((i for i, l in enumerate(lines) if l.strip().startswith("{")), None)
    try:
        ctl = json.loads(lines[head]) if head is not None else {"action": "new"}
    except json.JSONDecodeError:
        ctl = {"action": "new"}
    body = "\n".join(lines[(head + 1) if head is not None else 0:]).strip() + "\n"
    AUTO.mkdir(parents=True, exist_ok=True)
    # The model chooses `into`: resolve it (.., symlinks, absolute paths) and accept only a file directly inside intent/auto/
    # (scan finding #1, CWE-22). Anything else falls through to a new intent.
    f = (ROOT / str(ctl.get("into", ""))).resolve() if ctl.get("action") == "merge" and ctl.get("into") else None
    if f is not None and f.parent == AUTO.resolve() and f.is_file():
        with open(f, "a") as fh:
            fh.write(f"\n## Update · simulated day {det['day']} · level {level} (watch job)\n\n{body}")
        return f, "merge"
    slug = re.sub(r"[^a-z0-9-]+", "-", str(ctl.get("slug") or det["metric"]).lower()).strip("-")[:40] or det["metric"]
    f = AUTO / f"{det['date']}-{slug}.md"
    k = 2
    while f.exists():
        f = AUTO / f"{det['date']}-{slug}-{k}.md"
        k += 1
    f.write_text(body)
    return f, "new"


def tick(a):
    metric = a[0]
    upto = int(a[a.index("--upto") + 1]) if "--upto" in a else None
    record = a[a.index("--record") + 1] if "--record" in a else None
    model = a[a.index("--model") + 1] if "--model" in a else None
    bands = D.load_bands(a[a.index("--bands") + 1]) if "--bands" in a else D.load_bands()
    det = D.detect(metric, upto, bands)
    level = det["level"]
    if "--max-level" in a:
        level = min(level, int(a[a.index("--max-level") + 1]))
    row = {"ts": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"), "metric": metric, "day": det.get("day"),
           "level": det["level"], "acted_at_level": level if level >= 2 else None, "mode": det.get("mode"), "rules": det.get("rules"),
           "value": det.get("value"), "simulated_clock": det.get("simulated_clock")}
    print(json.dumps(det, ensure_ascii=False))
    if level < 2 or "--dry" in a:
        log({**row, "action": "log" if level else "none", "dry": "--dry" in a})
        return
    cfg = bands["metrics"][metric]
    cap = bands["queue"]["max_open"]
    if level == 2:
        tools, level_text = bands["levels"][2]["tools"], LEVEL2
    else:
        l3 = cfg["level3"]
        tools = l3["tools"]
        level_text = (f"Level 3 means you may act, but only through these paths: {', '.join(l3['paths'])}."
                      + (f" Approved runbooks: {'; '.join(l3['runbooks'])}." if l3.get("runbooks") else "")
                      + f"\n\n{l3['instructions']}")
    pts = D.load_points(metric, upto)[-10:]
    keep = ("day", "date", "value", "runs", "failed", "failing_tests", "commit", "actions", "by_kind", "release")
    points = "\n".join(json.dumps({k: p[k] for k in keep if k in p}, ensure_ascii=False) for p in pts)
    q = open_intents()
    queue = "\n".join(f"- `{f.relative_to(ROOT)}`: {t} ({s})" for f, t, s in q) or "(empty)"
    if "--no-cap" in a:
        rule = "Write a new intent."
    elif len(q) >= cap:
        rule = (f"The queue is full ({len(q)}/{cap}). Merge into the open intent of the same kind (same metric and same likely "
                "cause) if there is one; write a new intent only if none is of the same kind, and say why.")
    else:
        rule = "If an open intent above is about the same problem, merge into it instead of writing a new one."
    prompt = PROMPT.format(noise=cfg.get("noise", "not described"), metric=metric, level=level, action="diagnose, read-only" if level == 2 else "act through the gate",
                           day=det["day"], date=det["date"], detection=json.dumps(det, ensure_ascii=False, indent=1),
                           points=points, level_text=level_text, n_open=len(q), cap=cap, queue=queue, queue_rule=rule)
    result, meta = run_claude(prompt, tools, model, record)
    f, how = save_intent(result, det, level)
    log({**row, "action": "diagnose" if level == 2 else "act", "intent": str(f.relative_to(ROOT)), "queue": how,
         "open_before": len(q), "record": masked(record or ""), **meta})
    print(json.dumps({"intent": str(f.relative_to(ROOT)), "queue": how, **meta}, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "tick":
        tick(sys.argv[2:])
    else:
        print(__doc__)
        sys.exit(2)
