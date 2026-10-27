#!/usr/bin/env python3
"""PostToolUse hook (Write, Edit, MultiEdit): lint the file that just changed.

The app has no build step and no npm packages, so the "linter" is `node --check` on the one .js file just edited
(a syntax check). Fast and scoped: one file, no test suite (tests run at commit, by the verifier, or by people).
On failure the agent is told what broke, so it fixes it before moving on.
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from _timing import log

try:
    data = json.load(sys.stdin)
    tool, path = data["tool_name"], data["tool_input"].get("file_path", "")
except Exception:
    sys.exit(0)

if not path.endswith((".js", ".mjs")) or not os.path.exists(path):
    sys.exit(0)

p = subprocess.run(["node", "--check", path], capture_output=True, text=True)
if p.returncode:
    log("check-js", tool, path, "block")
    print(json.dumps({"decision": "block", "reason": f"check-js: node --check failed on {path}:\n{p.stderr[-1500:]}"}))
    sys.exit(0)
log("check-js", tool, path, "ok")
sys.exit(0)
