#!/usr/bin/env python3
"""PreToolUse hook (Bash, Write, Edit): drafting is the agent's job, approving is a human act.

Everything lives on main. Approving an intent or a spec = a person changes `Status: draft` to `Status: accepted` and commits.
So the agent is denied:
  - git merge / git rebase / git push (any target)
  - git commit while the current branch is main (on main, the agent never commits; people and the spec job do)
  - writing `Status: accepted` into intent/ or spec/, by Write, Edit, or a Bash command
Fails closed: if the input cannot be read, the action is denied.
"""
import json, re, subprocess, sys

ACCEPT = re.compile(r"Status:\s*accepted", re.I)


def decide(decision, reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": decision,
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)


try:
    data = json.load(sys.stdin)
    tool, inp = data["tool_name"], data["tool_input"]
except Exception:
    decide("deny", "no-self-approve: could not read the tool call, denying to be safe")

if tool in ("Write", "Edit", "MultiEdit"):
    path = inp.get("file_path", "")
    text = inp.get("content", "") + inp.get("new_string", "") + "".join(e.get("new_string", "") for e in inp.get("edits", []))
    if re.search(r"(^|/)(intent|spec)/", path) and ACCEPT.search(text):
        decide("deny", "no-self-approve: setting Status: accepted is the product owner's approval. Leave the file as draft.")
    sys.exit(0)

if tool == "Bash":
    cmd = inp.get("command", "")
    if re.search(r"\bgit\s+(merge|rebase|push)\b", cmd):
        decide("deny", "no-self-approve: merging and pushing belong to people.")
    if ACCEPT.search(cmd):
        decide("deny", "no-self-approve: setting Status: accepted is the product owner's approval. Leave the file as draft.")
    if re.search(r"\bgit\s+commit\b", cmd):
        branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
        if branch in ("main", "master"):
            decide("deny", "no-self-approve: the agent does not commit on main. People and the spec job commit; leave your files as drafts.")

sys.exit(0)
