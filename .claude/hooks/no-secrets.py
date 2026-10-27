#!/usr/bin/env python3
"""PreToolUse hook (Write, Edit, MultiEdit): keep credentials out of the diff.

Denies writing text that looks like a secret: private keys, cloud/API keys, tokens, `password = "..."`.
Fast and scoped: it only scans the text of this one tool call.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from _timing import log

PATTERNS = [
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "a private key"),
    (r"\bAKIA[0-9A-Z]{16}\b", "an AWS access key"),
    (r"\b(sk|rk|pk)-[A-Za-z0-9_-]{20,}", "an API key"),
    (r"\bgh[pousr]_[A-Za-z0-9]{30,}", "a GitHub token"),
    (r"\bAIza[0-9A-Za-z_-]{35}\b", "a Google API key"),
    (r"(?i)\b(api[_-]?key|secret|token|password|passwd)\b\s*[:=]\s*['\"][^'\"\s]{8,}['\"]", "a hard-coded credential"),
]

try:
    data = json.load(sys.stdin)
    tool, inp = data["tool_name"], data["tool_input"]
except Exception:
    sys.exit(0)

path = inp.get("file_path", "")
text = inp.get("content", "") + inp.get("new_string", "") + "".join(e.get("new_string", "") for e in inp.get("edits", []))
for pat, what in PATTERNS:
    if re.search(pat, text):
        log("no-secrets", tool, path, "deny")
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                 "permissionDecisionReason": f"no-secrets: this looks like {what}. "
                                                 "Credentials never go into the repo; read them from the environment."}}))
        sys.exit(0)
log("no-secrets", tool, path, "allow")
sys.exit(0)
