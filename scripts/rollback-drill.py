#!/usr/bin/env python3
"""Rehearse rollback in an environment N times: deploy the current HEAD, roll back, check the live release is the old one.

    python3 scripts/rollback-drill.py staging 10

Prints one line per round (seconds, ok/fail) and a summary. Needs one earlier release in <env> (deploy it once first).
A rollback that has never been rehearsed is a runbook, not a command.
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import deploy  # noqa: E402

env = sys.argv[1] if len(sys.argv) > 1 else "staging"
n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
if env == "production":
    sys.exit("rollback-drill: rehearse in staging or dev, not production")
if not deploy.current(env):
    deploy.deploy(env)

ok, times = 0, []
for i in range(1, n + 1):
    before = deploy.current(env)
    deploy.deploy(env)
    t0 = time.perf_counter()
    deploy.rollback(env)
    dt = time.perf_counter() - t0
    after = deploy.current(env)
    good = after == before
    ok += good
    times.append(dt)
    print(json.dumps({"round": i, "seconds": round(dt, 3), "ok": good, "live": after}))
summary = {"env": env, "rounds": n, "ok": ok, "max_seconds": round(max(times), 3), "avg_seconds": round(sum(times) / n, 3)}
deploy.log(action="rollback-drill", **summary)
print(json.dumps(summary))
sys.exit(0 if ok == n else 1)
