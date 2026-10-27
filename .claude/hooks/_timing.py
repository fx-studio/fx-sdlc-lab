"""Shared by the build-stage hooks: append how long each hook took to .hook-timing.log (git-ignored)."""
import json, os, time

T0 = time.perf_counter()


def log(hook, tool, path, decision):
    ms = (time.perf_counter() - T0) * 1000
    root = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    if path and os.path.isabs(path):
        path = os.path.relpath(path, root)
    with open(os.path.join(root, ".hook-timing.log"), "a") as f:
        f.write(json.dumps({"hook": hook, "tool": tool, "path": path, "decision": decision, "ms": round(ms, 1)}) + "\n")
