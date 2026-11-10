#!/usr/bin/env python3
"""Chạy các "ngày" giả lập của demo SDLC-6: mỗi ngày thu ba chỉ số rồi chạy một tick của watch job cho từng chỉ số.

    python3 demo/sdlc-6/ngay.py <từ-ngày> <tới-ngày> [--run <tên-lượt>] [--only <metric,...>] [--no-collect] [--max-level 2]

- Thu: `collect.py ci` (4 lượt node --test thật) · `collect.py traffic` cho staging và production (người dùng giả lập thật chạy bản
  đang ở môi trường đó).
- Tick: `watch.py tick <metric>`. Mức 0–1 chỉ ghi log. Mức 2–3 gọi Claude thật; phiên được ghi vào
  `demo/sdlc-6/runs/<tên-lượt>-day<NNN>-<metric>/` (transcript nguyên văn, chỉ che đường dẫn và email).
- Đồng hồ giả lập: ngày 1 = 2026-10-01. Người chạy demo bấm từng đoạn ngày bằng tay (chủ kênh chốt 2026-11-10).
In một dòng mỗi ngày: giá trị và mức của từng chỉ số.
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
METRICS = ["ci_fail_rate", "staging_error_rate", "production_error_rate"]


def sh(*a):
    return subprocess.run(a, cwd=ROOT, capture_output=True, text=True)


def main(a):
    d0, d1 = int(a[0]), int(a[1])
    run = a[a.index("--run") + 1] if "--run" in a else "R1"
    only = a[a.index("--only") + 1].split(",") if "--only" in a else METRICS
    extra = ["--max-level", a[a.index("--max-level") + 1]] if "--max-level" in a else []
    for d in range(d0, d1 + 1):
        if "--no-collect" not in a:
            if "ci_fail_rate" in only:
                sh("python3", "scripts/collect.py", "ci", "--day", str(d), "--runs", "4")
            for env in ("staging", "production"):
                if f"{env}_error_rate" in only:
                    sh("python3", "scripts/collect.py", "traffic", "--env", env, "--day", str(d))
        line = [f"day {d:3d}"]
        for m in only:
            rec = str(HERE / "runs" / f"{run}-day{d:03d}-{m}")
            p = sh("python3", "scripts/watch.py", "tick", m, "--record", rec, *extra)
            out = p.stdout.strip().splitlines()
            det = json.loads(out[0]) if out else {}
            tail = json.loads(out[1]) if len(out) > 1 else None
            line.append(f"{m.split('_')[0]}={det.get('value')} L{det.get('level')}{'*' if tail else ''}"
                        + (f" -> {tail['intent']} ({tail['queue']}, {tail.get('usd')} USD)" if tail else ""))
            if p.returncode:
                line.append(f"[lỗi {m}: {p.stderr[-300:]}]")
        print(" · ".join(line), flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
