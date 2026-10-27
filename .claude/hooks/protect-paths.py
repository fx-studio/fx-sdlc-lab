#!/usr/bin/env python3
"""PreToolUse hook (Write, Edit, MultiEdit): some paths are not the agent's to change during Build.

Denied:
  - docs/      the channel owner's own notes
  - tickets/   incoming tickets are evidence, not working files
  - intent/, spec/, plan/ files that already say `Status: accepted`: changing an approved decision is a person's call.
    (Drafts stay editable. A plan that has to change during the build is updated by a person, in the same commit as the code.)
Fast and scoped: it only looks at the one file the tool call touches.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from _timing import log

ACCEPTED = re.compile(r"Status:\s*accepted", re.I)


def deny(tool, path, reason):
    log("protect-paths", tool, path, "deny")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)


try:
    data = json.load(sys.stdin)
    tool, path = data["tool_name"], data["tool_input"].get("file_path", "")
except Exception:
    deny("?", "?", "protect-paths: could not read the tool call, denying to be safe")

root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
rel = os.path.relpath(os.path.abspath(path), root)

if re.match(r"(docs|tickets)/", rel):
    deny(tool, rel, f"protect-paths: {rel.split('/')[0]}/ is read-only for the agent.")

if re.match(r"(intent|spec|plan)/", rel) and os.path.exists(path):
    with open(path, encoding="utf-8") as f:
        head = f.read(2000)
    if ACCEPTED.search(head):
        deny(tool, rel, f"protect-paths: {rel} is accepted. Changing an approved decision is a person's call; "
                        "describe the change you need and stop.")

log("protect-paths", tool, rel, "allow")
sys.exit(0)
