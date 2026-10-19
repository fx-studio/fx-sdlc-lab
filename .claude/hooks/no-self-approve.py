#!/usr/bin/env python3
"""PreToolUse hook (Bash): the agent may draft and commit on a branch, but approving is a human act.

Approving an intent = merging it into main. So the agent is denied:
  - git merge / git rebase / git push (any target)
  - git commit while the current branch is main
Fails closed: if the input cannot be read, the command is denied.
"""
import json, re, subprocess, sys


def decide(decision, reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": decision,
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)


try:
    cmd = json.load(sys.stdin)["tool_input"]["command"]
except Exception:
    decide("deny", "no-self-approve: could not read the command, denying to be safe")

if re.search(r"\bgit\s+(merge|rebase|push)\b", cmd):
    decide("deny", "no-self-approve: merging into main is the product owner's approval. Leave the branch for a human to merge.")

if re.search(r"\bgit\s+commit\b", cmd):
    branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    if branch in ("main", "master"):
        decide("deny", "no-self-approve: do not commit on main. Create a branch such as intent/<slug> first.")

sys.exit(0)
