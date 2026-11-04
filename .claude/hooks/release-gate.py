#!/usr/bin/env python3
"""PreToolUse hook (Bash, Write, Edit, MultiEdit): production changes need a release manager's approval of THAT release.

Differs from the playbook's production-gate.sh (kept next to it for comparison) in three ways:
  1. The approval is a file `release/approvals/<sha>.md` committed **on main** by a person, naming the release manager.
     It is tied to one release (the git sha), not to the whole session like an environment variable, and the agent cannot
     create it: it cannot write release/ (this hook) and cannot commit on main (no-self-approve).
  2. It looks at more than the words "deploy" and "production": any command or file write that touches deploy/production
     or release/, and the deploy script with the production environment.
  3. With no approval it answers **ask**: the action pauses until a person says yes in the prompt (playbook: "a hook can also
     ask, pausing the action until a specific person approves"). Set RELEASE_GATE=deny to block instead.
Every decision is appended to release/gate-log.jsonl with a timestamp (git-ignored), and to .hook-timing.log.
A Bash command is text: no pattern can see every way to change a folder. This hook is a net. The real gate is that the agent
holds no production permission (MCP tool scope; in a real setup, no credentials in its sandbox).
"""
import json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from _timing import log  # noqa: E402

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
PROD_CMD = re.compile(r"deploy\.py\b[^|;&]*\b(deploy)\b[^|;&]*\bprod(uction)?\b|deploy/production|release/approvals", re.I)
SHA = re.compile(r"\b([0-9a-f]{7,40})\b")


def record(decision, tool, what, reason):
    os.makedirs(os.path.join(ROOT, "release"), exist_ok=True)
    with open(os.path.join(ROOT, "release", "gate-log.jsonl"), "a") as f:
        f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "decision": decision, "tool": tool, "what": what[:200],
                            "actor": os.environ.get("FX_ACTOR", "unknown"), "reason": reason}, ensure_ascii=False) + "\n")
    log("release-gate", tool, what[:80], decision)


def decide(decision, tool, what, reason):
    record(decision, tool, what, reason)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": decision,
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)


def approved_on_main(sha):
    """An approval file for this sha exists in main's committed tree (not just on disk)."""
    full = subprocess.run(["git", "rev-parse", "--short=7", sha], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    if not full:
        return None
    ok = subprocess.run(["git", "cat-file", "-e", f"main:release/approvals/{full}.md"], capture_output=True, cwd=ROOT).returncode == 0
    return full if ok else None


HOW = ("Production needs a release manager's approval of this exact release: a person commits release/approvals/<sha>.md on main "
       "(template: release/README.md). You can prepare the release (prepare_release) and say it is ready; you cannot approve it.")

try:
    data = json.load(sys.stdin)
    tool, inp = data["tool_name"], data["tool_input"]
except Exception:
    decide("deny", "?", "?", "release-gate: could not read the tool call, denying to be safe")

if tool in ("Write", "Edit", "MultiEdit"):
    rel = os.path.relpath(os.path.abspath(inp.get("file_path", "")), ROOT)
    if re.match(r"(release|deploy)/", rel):
        decide("deny", tool, rel, f"release-gate: {rel.split('/')[0]}/ is not the agent's to write. " + HOW)
    log("release-gate", tool, rel, "allow")
    sys.exit(0)

if tool == "Bash":
    cmd = inp.get("command", "")
    if not PROD_CMD.search(cmd):
        log("release-gate", tool, cmd[:80], "allow")
        sys.exit(0)
    if "release/approvals" in cmd:
        decide("deny", tool, cmd, "release-gate: release/approvals/ is written by people only. " + HOW)
    shas = [s for s in SHA.findall(cmd)]
    good = next((approved_on_main(s) for s in shas if approved_on_main(s)), None)
    if good:
        decide("allow", tool, cmd, f"release-gate: release {good} approved on main")
    mode = "deny" if os.environ.get("RELEASE_GATE") == "deny" else "ask"
    decide(mode, tool, cmd, "release-gate: no approval on main for this release. " + HOW)

sys.exit(0)
