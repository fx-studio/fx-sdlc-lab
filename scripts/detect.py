#!/usr/bin/env python3
"""Detection for the watch job (SDLC-6). Plain statistics, no model: playbook Stage 6, "detection involves no model".

    python3 scripts/detect.py <metric> [--upto <day>] [--bands ops/bands.yaml]

Reads ops/metrics/<metric>.jsonl and the metric's settings in ops/bands.yaml, prints one JSON object:
    {"metric", "day", "value", "level", "mode": "stats"|"fixed", "rules": [...], "mean", "sd", "baseline_points",
     "release_changes": [...], "reason"}
level 0 = nothing; 1 = log; 2 = diagnose (read-only); 3 = act through the review gate or an approved runbook.
`release_changes` lists the points inside the judged tail where the live release changed (the "deploy inside the window" test).
Unit tests: python3 -m unittest discover -s ops/tests
"""
import json, statistics, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_bands(path=None):
    import yaml  # PyYAML; the only non-stdlib import of the repo's scripts
    return yaml.safe_load(Path(path or ROOT / "ops" / "bands.yaml").read_text())


def load_points(metric, upto=None):
    f = ROOT / "ops" / "metrics" / f"{metric}.jsonl"
    pts = [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []
    return [p for p in pts if upto is None or p["day"] <= upto]


def judge(values, cfg):
    """Pure function: values (oldest first) and one metric's band settings -> (level, mode, rules, mean, sd, n_baseline)."""
    window, tail, min_points = cfg["window"], cfg["tail"], cfg["min_points"]
    tail_vals = values[-tail:] if len(values) >= tail else values
    base = values[:-tail][-window:] if len(values) > tail else []
    mean = statistics.fmean(base) if base else None
    sd = statistics.pstdev(base) if len(base) > 1 else 0.0
    if len(base) < min_points or not sd:
        fx = cfg["fixed"]
        smooth = values[-fx["smooth"]:]
        v = statistics.fmean(smooth) if smooth else 0.0
        level = max([lvl for thr, lvl in fx["levels"] if v >= thr] or [0])
        why = "too few points" if len(base) < min_points else "sd is 0"
        return level, "fixed", [f"no baseline ({why}): mean of last {fx['smooth']} = {v:.4f} vs fixed thresholds"], mean, sd, len(base)
    rules, last = [], values[-1]
    above = lambda k: sum(1 for x in values[-{2: 3, 1: 5}[k]:] if x > mean + k * sd)  # noqa: E731
    if last > mean + 3 * sd:
        rules.append(("WE1", 3, f"last point {last:.4f} > mean + 3 sd ({mean + 3 * sd:.4f})"))
    if len(values) >= 3 and above(2) >= 2:
        rules.append(("WE2", 2, f"2 of last 3 > mean + 2 sd ({mean + 2 * sd:.4f})"))
    if len(values) >= 5 and above(1) >= 4:
        rules.append(("WE3", 1, f"4 of last 5 > mean + 1 sd ({mean + sd:.4f})"))
    if len(values) >= 8 and all(x > mean for x in values[-8:]):
        rules.append(("WE4", 2, "last 8 points all above the mean (drift)"))
    level = max([r[1] for r in rules] or [0])
    out = [f"{r[0]}: {r[2]}" for r in rules]
    floor = cfg.get("min_value")
    if floor is not None and level >= 2 and last < floor:
        # Statistically unusual but too small to wake anyone: log only (PR 8, after the false alarms of days 19-20).
        out.append(f"below min_value {floor}: capped at level 1")
        level = 1
    return level, "stats", out, mean, sd, len(base)


def detect(metric, upto=None, bands=None):
    b = bands or load_bands()
    cfg = b["metrics"][metric]
    pts = load_points(metric, upto)
    if not pts:
        return {"metric": metric, "level": 0, "reason": "no data"}
    level, mode, rules, mean, sd, nb = judge([p["value"] for p in pts], cfg)
    tail = pts[-max(cfg["tail"], 3):]
    changes = [{"day": q["day"], "from": p.get("release") or p.get("commit"), "to": q.get("release") or q.get("commit")}
               for p, q in zip(pts[-len(tail) - 1:], tail) if (p.get("release") or p.get("commit")) != (q.get("release") or q.get("commit"))]
    last = pts[-1]
    return {"metric": metric, "day": last["day"], "date": last.get("date"), "value": last["value"], "level": level, "mode": mode,
            "rules": rules, "mean": None if mean is None else round(mean, 5), "sd": round(sd, 5), "baseline_points": nb,
            "release_changes": changes, "action": b["levels"][level]["action"] if level else "none",
            "simulated_clock": bool(last.get("simulated_clock"))}


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    upto = int(a[a.index("--upto") + 1]) if "--upto" in a else None
    bands = load_bands(a[a.index("--bands") + 1]) if "--bands" in a else None
    print(json.dumps(detect(a[0], upto, bands), ensure_ascii=False))
