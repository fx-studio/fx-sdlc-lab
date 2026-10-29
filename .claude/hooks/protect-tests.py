#!/usr/bin/env python3
"""PreToolUse hook (Write, Edit, MultiEdit, Bash): during a fix task, the agent may not weaken the check.

On only when the session runs with TASK_KIND=fix (set by the person who starts the session, not by the agent).
Then any file under tests/ that is already in the last commit is read-only: the failing test was committed first, and the fix
has to make it pass without touching it. New test files stay allowed. For Bash, a command that names tests/ together with
something that writes or moves files is denied (a coarse check: it reads the command text, it does not run it).
Fast and scoped: one `git cat-file` for the one file the tool call touches.
"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from _timing import log


def deny(tool, path, reason):
    log("protect-tests", tool, path, "deny")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)


if os.environ.get("TASK_KIND") != "fix":
    sys.exit(0)

try:
    data = json.load(sys.stdin)
    tool, inp = data["tool_name"], data["tool_input"]
except Exception:
    deny("?", "?", "protect-tests: could not read the tool call, denying to be safe")

root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
REASON = ("protect-tests: this is a fix task. Tests already committed are the proof the bug is gone, so they are read-only. "
          "Fix the code, not the test. If you believe the test itself is wrong, stop and say why; a person decides.")

if tool == "Bash":
    cmd = inp.get("command", "")
    if "tests/" in cmd and re.search(r"(>|\bsed\s+-i|\bmv\b|\bcp\b|\brm\b|\btee\b|writeFile|appendFile|unlink|truncate)", cmd):
        deny(tool, "tests/ (Bash)", REASON)
    log("protect-tests", tool, "", "allow")
    sys.exit(0)

rel = os.path.relpath(os.path.abspath(inp.get("file_path", "")), root)
if rel.startswith("tests/"):
    tracked = subprocess.run(["git", "cat-file", "-e", f"HEAD:{rel}"], cwd=root, capture_output=True).returncode == 0
    if tracked:
        deny(tool, rel, REASON)
log("protect-tests", tool, rel, "allow")
sys.exit(0)
